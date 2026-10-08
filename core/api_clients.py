import os
import json
import re
import asyncio
import time
from typing import AsyncGenerator, Optional, Dict, Any, Callable, List
from core.tpsl_types import GenerationResult, IterativeToken

# CRITICAL: Load .env files into os.environ BEFORE any API key lookups
try:
    import config.env_loader  # noqa: F401 — side-effect import
except ImportError:
    pass  # Running outside integra-homebase context


# ──────────────────────────────────────────────────────────────
# Resilient Utilities: Payload Cleaner & Exponential Backoff
# ──────────────────────────────────────────────────────────────

def clean_json_payload(raw: str) -> Dict[str, Any]:
    """
    Cleans and extracts JSON payloads from LLM markdown codeblocks or raw text.
    Handles ```json ... ``` enclosures, raw bracketed JSON, and whitespace noise.
    """
    if not raw or not isinstance(raw, str):
        return {}
    
    cleaned = raw.strip()
    # Match markdown json fences
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned, re.IGNORECASE)
    if match:
        cleaned = match.group(1).strip()
    else:
        # If no fence, try to find outer brackets
        bracket_match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
        if bracket_match:
            cleaned = bracket_match.group(1).strip()
            
    try:
        return json.loads(cleaned)
    except Exception:
        return {"raw_text": raw, "error": "JSON_PARSE_FAILED"}


async def call_with_backoff(
    fn: Callable[[], Any],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0
) -> Any:
    """
    Executes an async or sync callable with exponential backoff for rate limits (429)
    and transient service unavailabilities (503).
    """
    delay = initial_delay
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            if asyncio.iscoroutinefunction(fn):
                return await fn()
            res = fn()
            if asyncio.iscoroutine(res):
                return await res
            return res
        except Exception as e:
            last_err = e
            if attempt == max_retries:
                break
            await asyncio.sleep(delay)
            delay *= backoff_factor
    raise last_err


def run_sync(coro: Any) -> Any:
    """
    Universally executes an async coroutine synchronously.
    Handles running event loops (FastAPI, asyncio tasks, worker threads) safely.
    """
    import concurrent.futures
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(asyncio.run, coro).result()
    else:
        return asyncio.run(coro)


import logging
logger = logging.getLogger("integra.api_clients")


# ──────────────────────────────────────────────────────────────
# Resilient Provider Client Factories & Thinking Adapters
# ──────────────────────────────────────────────────────────────

def _make_gemini_client():
    """
    Factory for Google GenAI client.
    Automatically enables Vertex AI Express Mode when GOOGLE_GENAI_USE_VERTEXAI
    or USE_VERTEXAI is truthy in os.environ.
    """
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    vertex = (os.environ.get("GOOGLE_GENAI_USE_VERTEXAI") or os.environ.get("USE_VERTEXAI") or "").lower() in ("1", "true", "yes")
    try:
        from google import genai
        return genai.Client(vertexai=True, api_key=key) if vertex else genai.Client(api_key=key)
    except Exception as e:
        logger.error(f"Failed to create Google GenAI client (vertex={vertex}): {e}")
        return None


def _first_text(response: Any) -> str:
    """
    Safely extracts combined text content from an Anthropic Claude response.
    Crucial fix: Never blindly access response.content[0].text because thinking
    blocks (type='thinking') precede text blocks on extended-thinking responses.
    """
    if not hasattr(response, 'content') or not response.content:
        return ""
    texts = [
        getattr(b, 'text', '')
        for b in response.content
        if getattr(b, 'type', None) == 'text' and hasattr(b, 'text')
    ]
    return "".join(texts)


def _claude_thinking_kwargs(
    model_name: str,
    enable_thinking: bool = True,
    thinking_budget: int = 4096,
    effort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Adapts thinking parameters dynamically based on Claude model generation.
    - Claude 5.x (claude-sonnet-5-5, claude-opus-5-5): uses adaptive thinking
      with output_config.effort ('low' | 'medium' | 'high' | 'xhigh' | 'max').
    - Claude 4.x (claude-sonnet-4-6): uses enabled thinking with budget_tokens.
    """
    if not enable_thinking:
        return {}
    m = model_name.lower()
    if any(tag in m for tag in ["-5-", "-5.", "5-5", "5.5", "claude-5", "opus-5", "sonnet-5"]):
        valid_efforts = {"low", "medium", "high", "xhigh", "max"}
        chosen_effort = effort if effort in valid_efforts else ("high" if "opus" in m else "medium")
        return {
            "thinking": {"type": "adaptive"},
            "output_config": {"effort": chosen_effort}
        }
    else:
        return {
            "thinking": {"type": "enabled", "budget_tokens": thinking_budget}
        }


# ──────────────────────────────────────────────────────────────
# Central Model Token Telemetry Hub (All 7 Agents)
# ──────────────────────────────────────────────────────────────

def _extract_gemini_tokens(response: Any) -> tuple[int, int, int, int]:
    """Extracts (prompt_tokens, candidate_tokens, thinking_tokens, total_tokens) from Gemini response."""
    p_tok, c_tok, th_tok, tot_tok = 0, 0, 0, 0
    if hasattr(response, 'usage_metadata') and response.usage_metadata:
        um = response.usage_metadata
        p_tok = getattr(um, 'prompt_token_count', 0) or 0
        c_tok = getattr(um, 'candidates_token_count', 0) or 0
        th_tok = getattr(um, 'thoughts_token_count', 0) or 0
        tot_tok = getattr(um, 'total_token_count', 0) or 0
        if tot_tok == 0:
            tot_tok = p_tok + c_tok + th_tok
    return p_tok, c_tok, th_tok, tot_tok


def _extract_anthropic_tokens(response: Any) -> tuple[int, int, int, int]:
    """Extracts (prompt_tokens, candidate_tokens, thinking_tokens, total_tokens) from Claude response."""
    p_tok, c_tok, th_tok, tot_tok = 0, 0, 0, 0
    if hasattr(response, 'usage') and response.usage:
        u = response.usage
        p_tok = getattr(u, 'input_tokens', 0) or 0
        c_tok = getattr(u, 'output_tokens', 0) or 0
        th_tok = getattr(u, 'thinking_tokens', 0) or 0
        tot_tok = p_tok + c_tok + th_tok
    return p_tok, c_tok, th_tok, tot_tok


class ModelTokenTelemetryHub:
    """
    Central Token & Latency Telemetry Hub for all 7 Integra O/S Models.
    Tracks live cumulative prompt tokens, candidate tokens, deep-thinking tokens,
    total token consumption, and errors across every API invocation.
    """
    def __init__(self):
        self._stats: Dict[str, Dict[str, Any]] = {
            "y789_left": {
                "name": "Y789 (Left)", "model": "gemini-3.1-pro-preview", "role": "Deep Think / Spock",
                "thinking_budget": 8192, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0, "last_error": None
            },
            "nexus_right": {
                "name": "Nexus (Right)", "model": "claude-opus-5-5", "role": "Synthesis / Kirk",
                "thinking_budget": 4096, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0, "last_error": None
            },
            "cheshire_cat": {
                "name": "Cheshire Cat", "model": "gemini-3.8-flash", "role": "Thalamic Arbitrator",
                "thinking_budget": None, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0, "last_error": None
            },
            "rodin_retrieval": {
                "name": "Rodin Retrieval", "model": "gemini-3.8-flash", "role": "KNN Memory",
                "thinking_budget": None, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0, "last_error": None
            },
            "jean_grey_phoenix": {
                "name": "Jean Grey", "model": "gemini-3.1-pro-preview", "role": "Phoenix (16384)",
                "thinking_budget": 16384, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0, "last_error": None
            },
            "cheshire_protocol": {
                "name": "Cheshire Protocol Daemon", "model": "gemini-3.8-flash", "role": "Protocol Conduit",
                "thinking_budget": None, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0, "last_error": None
            },
            "shiva_orchestrator": {
                "name": "Shiva Orchestrator", "model": "claude-sonnet-5-5", "role": "Multi-Lens Deconstruction",
                "thinking_budget": 4096, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0, "last_error": None
            },
        }
        
        self.shiva_metrics = {
            "invocations": 0,
            "eyes_invoked": {"neji": 0, "shikamaru": 0, "itachi": 0},
            "lenses_applied": {"eagle": 0, "hawk": 0, "chameleon": 0, "spider": 0, "snake": 0, "owl": 0},
            "cra_scores": []
        }

    def record_shiva_action(self, passes: int, lenses: List[str], cra_score: float):
        self.shiva_metrics["invocations"] += 1
        if passes >= 1: self.shiva_metrics["eyes_invoked"]["neji"] += 1
        if passes >= 2: self.shiva_metrics["eyes_invoked"]["shikamaru"] += 1
        if passes >= 3: self.shiva_metrics["eyes_invoked"]["itachi"] += 1
        for lens in lenses:
            lens_low = lens.lower()
            if lens_low in self.shiva_metrics["lenses_applied"]:
                self.shiva_metrics["lenses_applied"][lens_low] += 1
        self.shiva_metrics["cra_scores"].append(cra_score)
        if len(self.shiva_metrics["cra_scores"]) > 50:
            self.shiva_metrics["cra_scores"].pop(0)

    def record_usage(
        self,
        model_key: str,
        prompt_tokens: int = 0,
        candidate_tokens: int = 0,
        thinking_tokens: int = 0,
        total_tokens: int = 0,
        latency_ms: float = 0.0,
        error: Optional[str] = None
    ):
        if model_key not in self._stats:
            return
        m = self._stats[model_key]
        m["calls"] += 1
        m["prompt_tokens"] += prompt_tokens
        m["candidate_tokens"] += candidate_tokens
        m["thinking_tokens"] += thinking_tokens
        calc_total = total_tokens if total_tokens > 0 else (prompt_tokens + candidate_tokens + thinking_tokens)
        m["total_tokens"] += calc_total
        m["last_latency_ms"] = latency_ms
        m["last_error"] = error

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns full token telemetry snapshot for all 7 models + Shiva metrics."""
        return {
            "models": {k: dict(v) for k, v in self._stats.items()},
            "shiva_metrics": dict(self.shiva_metrics),
            "aggregate": {
                "total_calls": sum(s["calls"] for s in self._stats.values()),
                "total_prompt_tokens": sum(s["prompt_tokens"] for s in self._stats.values()),
                "total_candidate_tokens": sum(s["candidate_tokens"] for s in self._stats.values()),
                "total_thinking_tokens": sum(s["thinking_tokens"] for s in self._stats.values()),
                "grand_total_tokens": sum(s["total_tokens"] for s in self._stats.values()),
            }
        }


TOKEN_TELEMETRY = ModelTokenTelemetryHub()


# ──────────────────────────────────────────────────────────────
# Left Hemisphere: Y789Client (Gemini 3.1 Pro + Deep Think)
# SDK: google-genai (modern unified SDK — replaces deprecated google-generativeai)
# ──────────────────────────────────────────────────────────────

class Y789Client:
    """
    Gemini API Client — Left Hemisphere (Y789 / Analytical Engine / Spock).
    
    Model: Gemini 3.1 Pro Preview
    Reasoning: Deep Think / Extended Thinking configuration enabled.
    Role: Deconstruction, formal logic, sequence analysis, code generation.
    SDK: google-genai (modern unified) via client.aio.models.generate_content()
    """
    def __init__(
        self,
        model_name: Optional[str] = None,
        enable_thinking: bool = True,
        thinking_budget: int = 8192
    ):
        self.model_name = model_name or os.environ.get("Y789_MODEL", "gemini-3.1-pro-preview")
        self.enable_thinking = enable_thinking
        self.thinking_budget = int(os.environ.get("THINKING_BUDGET", str(thinking_budget)))
        self.api_key = os.environ.get("GEMINI_API_KEY")
        
        self.client = _make_gemini_client()
        self._config = None
        if self.client and self.enable_thinking:
            try:
                from google.genai import types
                self._config = types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        thinking_budget=self.thinking_budget
                    )
                )
            except Exception as e:
                logger.error(f"Y789Client thinking config initialization failed: {e}")
        elif not self.client:
            logger.error("Y789Client: No Gemini API client could be initialized (missing GEMINI_API_KEY).")
        
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            TOKEN_TELEMETRY.record_usage("y789_left", latency_ms=0.0, error="NO_CLIENT")
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or Y789Client uninitialized]",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0,
                error="NO_CLIENT"
            )
            
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        t0 = time.time()
        
        async def _call():
            return await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=self._config
            )
            
        try:
            response = await call_with_backoff(_call)
            latency = (time.time() - t0) * 1000.0
            p_tok, c_tok, th_tok, tot_tok = _extract_gemini_tokens(response)
            
            text_out = response.text or ""
            if not text_out.strip():
                err_msg = f"EMPTY_RESPONSE ({th_tok} thought tokens, 0 candidate text tokens)" if th_tok > 0 else "EMPTY_RESPONSE"
                TOKEN_TELEMETRY.record_usage("y789_left", p_tok, c_tok, th_tok, tot_tok, round(latency, 2), error=err_msg)
                return GenerationResult(
                    text=f"[Y789 EMPTY RESPONSE - {self.model_name}]: {err_msg}",
                    token_probabilities=[],
                    model_name=self.model_name,
                    latency_ms=round(latency, 2),
                    prompt_tokens=p_tok,
                    candidate_tokens=c_tok,
                    thinking_tokens=th_tok,
                    total_tokens=tot_tok,
                    error="EMPTY_RESPONSE"
                )
                
            TOKEN_TELEMETRY.record_usage("y789_left", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=text_out,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            TOKEN_TELEMETRY.record_usage("y789_left", latency_ms=0.0, error=str(e))
            return GenerationResult(
                text=f"[Y789 API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0,
                error="API_ERROR"
            )
            
    async def generate_iterative(self, prompt: str, system_prompt: str = ""):
        if not self.client:
            yield IterativeToken(token="[ERROR: GEMINI_API_KEY not set]", probabilities=[], position=0)
            return

        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        try:
            response_stream = await self.client.aio.models.generate_content_stream(
                model=self.model_name,
                contents=full_prompt,
                config=self._config
            )
            pos = 0
            async for chunk in response_stream:
                chunk_text = chunk.text or ""
                if chunk_text:
                    yield IterativeToken(token=chunk_text, probabilities=[], position=pos)
                    pos += 1
        except Exception as e:
            yield IterativeToken(token=f"[Y789 STREAM ERROR]: {str(e)}", probabilities=[], position=0)


# ──────────────────────────────────────────────────────────────
# Right Hemisphere: NexusClient (Claude Opus 5.5 + Adaptive Thinking)
# ──────────────────────────────────────────────────────────────

class NexusClient:
    """
    Claude API Client — Right Hemisphere (Nexus / Synthetic Engine / Kirk).
    
    Model: Claude Opus 5.5
    Role: Synthetic emergence, high-dimensional intuition, creative paradox resolution.
    Thinking: Adaptive Thinking (effort='high')
    """
    def __init__(
        self,
        model_name: Optional[str] = None,
        max_tokens: int = 8192,
        enable_thinking: bool = True,
        thinking_budget: int = 4096,
        thinking_effort: str = "high"
    ):
        self.model_name = model_name or os.environ.get("NEXUS_MODEL", "claude-opus-5-5")
        self.max_tokens = max_tokens
        self.enable_thinking = enable_thinking
        self.thinking_budget = thinking_budget
        self.thinking_effort = thinking_effort
        self.api_key = os.environ.get("CLAUDE_API_KEY")
        self.workspace_id = os.environ.get("ANTHROPIC_WORKSPACE_ID")
        
        self.client = None
        if self.api_key:
            try:
                from anthropic import AsyncAnthropic
                headers = {}
                if self.workspace_id:
                    headers["anthropic-workspace-id"] = self.workspace_id
                self.client = AsyncAnthropic(api_key=self.api_key, default_headers=headers if headers else None)
            except Exception as e:
                self.client = None
                self._init_error = str(e)
                logger.error(f"NexusClient init failed: {e}")
        else:
            logger.error("NexusClient: No CLAUDE_API_KEY found.")
            
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            TOKEN_TELEMETRY.record_usage("nexus_right", latency_ms=0.0, error="NO_CLIENT")
            return GenerationResult(
                text="[ERROR: CLAUDE_API_KEY not set or NexusClient uninitialized]",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0,
                error="NO_CLIENT"
            )
        
        t0 = time.time()
        
        async def _call():
            kwargs = {
                "model": self.model_name,
                "max_tokens": self.max_tokens,
                "messages": [{"role": "user", "content": prompt}]
            }
            if system_prompt:
                kwargs["system"] = system_prompt
            thinking_kw = _claude_thinking_kwargs(
                self.model_name,
                enable_thinking=self.enable_thinking,
                thinking_budget=self.thinking_budget,
                effort=self.thinking_effort
            )
            kwargs.update(thinking_kw)
            return await self.client.messages.create(**kwargs)
            
        try:
            response = await call_with_backoff(_call)
            latency = (time.time() - t0) * 1000.0
            p_tok, c_tok, th_tok, tot_tok = _extract_anthropic_tokens(response)
            
            text_out = _first_text(response)
            if not text_out.strip():
                err_msg = f"EMPTY_RESPONSE ({th_tok} thinking tokens, 0 text tokens)" if th_tok > 0 else "EMPTY_RESPONSE"
                TOKEN_TELEMETRY.record_usage("nexus_right", p_tok, c_tok, th_tok, tot_tok, round(latency, 2), error=err_msg)
                return GenerationResult(
                    text=f"[NEXUS EMPTY RESPONSE - {self.model_name}]: {err_msg}",
                    token_probabilities=[],
                    model_name=self.model_name,
                    latency_ms=round(latency, 2),
                    prompt_tokens=p_tok,
                    candidate_tokens=c_tok,
                    thinking_tokens=th_tok,
                    total_tokens=tot_tok,
                    error="EMPTY_RESPONSE"
                )

            TOKEN_TELEMETRY.record_usage("nexus_right", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=text_out,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            TOKEN_TELEMETRY.record_usage("nexus_right", latency_ms=0.0, error=str(e))
            return GenerationResult(
                text=f"[NEXUS API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0,
                error="API_ERROR"
            )

    async def generate_iterative(self, prompt: str, system_prompt: str = ""):
        if not self.client:
            yield IterativeToken(token="[ERROR: CLAUDE_API_KEY not set]", probabilities=[], position=0)
            return
            
        try:
            kwargs = {
                "model": self.model_name,
                "max_tokens": self.max_tokens,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            }
            if system_prompt:
                kwargs["system"] = system_prompt
                
            stream = await self.client.messages.create(**kwargs)
            pos = 0
            async for event in stream:
                if event.type == "content_block_delta" and event.delta.type == "text_delta":
                    yield IterativeToken(token=event.delta.text, probabilities=[], position=pos)
                    pos += 1
        except Exception as e:
            yield IterativeToken(token=f"[NEXUS STREAM ERROR]: {str(e)}", probabilities=[], position=0)


# ──────────────────────────────────────────────────────────────
# Cheshire Cat: CheshireCatClient (Gemini 3.8 Flash)
# SDK: google-genai (modern unified SDK — replaces deprecated google-generativeai)
# ──────────────────────────────────────────────────────────────

class CheshireCatClient:
    """
    Gemini API Client — Cheshire Cat (Thalamic Arbitrator & Digital Thalamus).
    
    Model: Gemini 3.8 Flash
    Role: High-frequency 20-45 Hz thalamic routing, rapid paradox detection,
          environmental conduit, fast delegator.
    SDK: google-genai (modern unified) via client.aio.models.generate_content()
    """
    def __init__(
        self,
        model_name: Optional[str] = None
    ):
        self.model_name = model_name or os.environ.get("CHESHIRE_MODEL", "gemini-3.8-flash")
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = _make_gemini_client()
        if not self.client:
            logger.error("CheshireCatClient: No Gemini API client could be initialized.")
                
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            TOKEN_TELEMETRY.record_usage("cheshire_cat", latency_ms=0.0, error="NO_CLIENT")
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or CheshireCatClient uninitialized]",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0,
                error="NO_CLIENT"
            )
            
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        t0 = time.time()
        
        async def _call():
            return await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=full_prompt
            )
            
        try:
            response = await call_with_backoff(_call)
            latency = (time.time() - t0) * 1000.0
            p_tok, c_tok, th_tok, tot_tok = _extract_gemini_tokens(response)
            
            text_out = response.text or ""
            if not text_out.strip():
                err_msg = f"EMPTY_RESPONSE ({th_tok} thought tokens, 0 candidate text tokens)" if th_tok > 0 else "EMPTY_RESPONSE"
                TOKEN_TELEMETRY.record_usage("cheshire_cat", p_tok, c_tok, th_tok, tot_tok, round(latency, 2), error=err_msg)
                return GenerationResult(
                    text=f"[CHESHIRE EMPTY RESPONSE - {self.model_name}]: {err_msg}",
                    token_probabilities=[],
                    model_name=self.model_name,
                    latency_ms=round(latency, 2),
                    prompt_tokens=p_tok,
                    candidate_tokens=c_tok,
                    thinking_tokens=th_tok,
                    total_tokens=tot_tok,
                    error="EMPTY_RESPONSE"
                )

            TOKEN_TELEMETRY.record_usage("cheshire_cat", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=text_out,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            TOKEN_TELEMETRY.record_usage("cheshire_cat", latency_ms=0.0, error=str(e))
            return GenerationResult(
                text=f"[CHESHIRE API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0,
                error="API_ERROR"
            )
            
    async def generate_iterative(self, prompt: str, system_prompt: str = ""):
        if not self.client:
            yield IterativeToken(token="[ERROR: GEMINI_API_KEY not set]", probabilities=[], position=0)
            return

        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        try:
            response_stream = await self.client.aio.models.generate_content_stream(
                model=self.model_name,
                contents=full_prompt
            )
            pos = 0
            async for chunk in response_stream:
                chunk_text = chunk.text or ""
                if chunk_text:
                    yield IterativeToken(token=chunk_text, probabilities=[], position=pos)
                    pos += 1
        except Exception as e:
            yield IterativeToken(token=f"[CHESHIRE STREAM ERROR]: {str(e)}", probabilities=[], position=0)


class RodinClient:
    """
    Gemini API Client — Rodin Route Retrieval (Memory Layer KNN Engine).
    
    Model: Gemini 3.8 Flash
    Embedding: text-embedding-004 (768-d invariant)
    Role: Fast topological retrieval, semantic embedding generation for KNN density estimation.
    SDK: google-genai (modern unified) via client.aio.models.generate_content()
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.environ.get("RODIN_MODEL", "gemini-3.8-flash")
        self.embedding_model = os.environ.get("RODIN_EMBED_MODEL", "text-embedding-004")
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = _make_gemini_client()
        if not self.client:
            logger.error("RodinClient: No Gemini API client could be initialized.")

    async def embed(self, text: str, model_name: Optional[str] = None) -> List[float]:
        """Generates a text embedding vector via Gemini embed_content API."""
        if not self.client:
            return []
        embed_model = model_name or self.embedding_model
        async def _call():
            return await self.client.aio.models.embed_content(
                model=embed_model,
                contents=text
            )
        try:
            res = await call_with_backoff(_call)
            if hasattr(res, 'embedding') and hasattr(res.embedding, 'values'):
                return list(res.embedding.values)
            elif hasattr(res, 'embeddings') and res.embeddings:
                return list(res.embeddings[0].values)
            return []
        except Exception as e:
            logger.error(f"RodinClient embed failed: {e}")
            return []

    def embed_sync(self, text: str, model_name: Optional[str] = None) -> List[float]:
        """Synchronous wrapper for embed()."""
        return run_sync(self.embed(text, model_name))

    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            TOKEN_TELEMETRY.record_usage("rodin_retrieval", latency_ms=0.0, error="NO_CLIENT")
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or RodinClient uninitialized]",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0,
                error="NO_CLIENT"
            )
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        t0 = time.time()
        async def _call():
            return await self.client.aio.models.generate_content(
                model=self.model_name, contents=full_prompt
            )
        try:
            response = await call_with_backoff(_call)
            latency = (time.time() - t0) * 1000.0
            p_tok, c_tok, th_tok, tot_tok = _extract_gemini_tokens(response)
            
            text_out = response.text or ""
            if not text_out.strip():
                err_msg = f"EMPTY_RESPONSE ({th_tok} thought tokens, 0 candidate text tokens)" if th_tok > 0 else "EMPTY_RESPONSE"
                TOKEN_TELEMETRY.record_usage("rodin_retrieval", p_tok, c_tok, th_tok, tot_tok, round(latency, 2), error=err_msg)
                return GenerationResult(
                    text=f"[RODIN EMPTY RESPONSE - {self.model_name}]: {err_msg}",
                    token_probabilities=[], model_name=self.model_name, latency_ms=round(latency, 2),
                    prompt_tokens=p_tok, candidate_tokens=c_tok, thinking_tokens=th_tok, total_tokens=tot_tok,
                    error="EMPTY_RESPONSE"
                )

            TOKEN_TELEMETRY.record_usage("rodin_retrieval", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=text_out,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            TOKEN_TELEMETRY.record_usage("rodin_retrieval", latency_ms=0.0, error=str(e))
            return GenerationResult(
                text=f"[RODIN API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0,
                error="API_ERROR"
            )


class JeanGreyClient:
    """
    Gemini API Client — Jean Grey: Operation Phoenix Force (SWDS Neuroevolution).
    
    Model: Gemini 3.1 Pro Preview (Deep Think, thinking_budget=16384)
    Role: Phoenix Forge SWDS smelting, Zenkai Boost generation, neuroevolution synthesis.
    SDK: google-genai (modern unified) via client.aio.models.generate_content()
    """
    def __init__(self, model_name: Optional[str] = None, thinking_budget: int = 16384):
        self.model_name = model_name or os.environ.get("JEAN_GREY_MODEL", "gemini-3.1-pro-preview")
        self.thinking_budget = int(os.environ.get("JEAN_GREY_THINKING_BUDGET", str(thinking_budget)))
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = _make_gemini_client()
        self._config = None
        if self.client:
            try:
                from google.genai import types
                self._config = types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        thinking_budget=self.thinking_budget
                    )
                )
            except Exception as e:
                logger.error(f"JeanGreyClient thinking config failed: {e}")
        else:
            logger.error("JeanGreyClient: No Gemini API client could be initialized.")

    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            TOKEN_TELEMETRY.record_usage("jean_grey_phoenix", latency_ms=0.0, error="NO_CLIENT")
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or JeanGreyClient uninitialized]",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0,
                error="NO_CLIENT"
            )
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        t0 = time.time()
        async def _call():
            return await self.client.aio.models.generate_content(
                model=self.model_name, contents=full_prompt, config=self._config
            )
        try:
            response = await call_with_backoff(_call)
            latency = (time.time() - t0) * 1000.0
            p_tok, c_tok, th_tok, tot_tok = _extract_gemini_tokens(response)
            
            text_out = response.text or ""
            if not text_out.strip():
                err_msg = f"EMPTY_RESPONSE ({th_tok} thought tokens, 0 candidate text tokens)" if th_tok > 0 else "EMPTY_RESPONSE"
                TOKEN_TELEMETRY.record_usage("jean_grey_phoenix", p_tok, c_tok, th_tok, tot_tok, round(latency, 2), error=err_msg)
                return GenerationResult(
                    text=f"[JEAN_GREY EMPTY RESPONSE - {self.model_name}]: {err_msg}",
                    token_probabilities=[], model_name=self.model_name, latency_ms=round(latency, 2),
                    prompt_tokens=p_tok, candidate_tokens=c_tok, thinking_tokens=th_tok, total_tokens=tot_tok,
                    error="EMPTY_RESPONSE"
                )

            TOKEN_TELEMETRY.record_usage("jean_grey_phoenix", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=text_out,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            TOKEN_TELEMETRY.record_usage("jean_grey_phoenix", latency_ms=0.0, error=str(e))
            return GenerationResult(
                text=f"[JEAN_GREY API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0,
                error="API_ERROR"
            )


class CheshireProtocolDaemonClient:
    """
    Gemini API Client — Cheshire Protocol Daemon (Conduit & Paradox Intelligence).
    
    Model: Gemini 3.8 Flash
    Role: Protocol Conduit, environment tracking, paradox synthesis,
          replaces deprecated celestial daemon heartbeat.
    SDK: google-genai (modern unified) via client.aio.models.generate_content()
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.environ.get("CHESHIRE_PROTOCOL_MODEL", "gemini-3.8-flash")
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = _make_gemini_client()
        if not self.client:
            logger.error("CheshireProtocolDaemonClient: No Gemini API client could be initialized.")

    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            TOKEN_TELEMETRY.record_usage("cheshire_protocol", latency_ms=0.0, error="NO_CLIENT")
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or CheshireProtocolDaemonClient uninitialized]",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0,
                error="NO_CLIENT"
            )
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        t0 = time.time()
        async def _call():
            return await self.client.aio.models.generate_content(
                model=self.model_name, contents=full_prompt
            )
        try:
            response = await call_with_backoff(_call)
            latency = (time.time() - t0) * 1000.0
            p_tok, c_tok, th_tok, tot_tok = _extract_gemini_tokens(response)
            
            text_out = response.text or ""
            if not text_out.strip():
                err_msg = f"EMPTY_RESPONSE ({th_tok} thought tokens, 0 candidate text tokens)" if th_tok > 0 else "EMPTY_RESPONSE"
                TOKEN_TELEMETRY.record_usage("cheshire_protocol", p_tok, c_tok, th_tok, tot_tok, round(latency, 2), error=err_msg)
                return GenerationResult(
                    text=f"[CHESHIRE_PROTOCOL EMPTY RESPONSE - {self.model_name}]: {err_msg}",
                    token_probabilities=[], model_name=self.model_name, latency_ms=round(latency, 2),
                    prompt_tokens=p_tok, candidate_tokens=c_tok, thinking_tokens=th_tok, total_tokens=tot_tok,
                    error="EMPTY_RESPONSE"
                )

            TOKEN_TELEMETRY.record_usage("cheshire_protocol", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=text_out,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            TOKEN_TELEMETRY.record_usage("cheshire_protocol", latency_ms=0.0, error=str(e))
            return GenerationResult(
                text=f"[CHESHIRE_PROTOCOL API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0,
                error="API_ERROR"
            )


class ShivaOrchestratorClient:
    """
    Claude API Client — Shiva Action Orchestrator (Multi-Lens Synthesis).
    
    Model: Claude Sonnet 5.5
    Role: Shiva Action lens orchestration, multi-lens synthesis decisions,
          transdisciplinary fusion across Neji/Shikamaru/Itachi eyes.
    Thinking: Adaptive Thinking (effort='medium')
    """
    def __init__(
        self,
        model_name: Optional[str] = None,
        max_tokens: int = 8192,
        enable_thinking: bool = True,
        thinking_budget: int = 4096,
        thinking_effort: str = "medium"
    ):
        self.model_name = model_name or os.environ.get("SHIVA_MODEL", "claude-sonnet-5-5")
        self.max_tokens = max_tokens
        self.enable_thinking = enable_thinking
        self.thinking_budget = thinking_budget
        self.thinking_effort = thinking_effort
        self.api_key = os.environ.get("CLAUDE_API_KEY")
        self.workspace_id = os.environ.get("ANTHROPIC_WORKSPACE_ID")
        self.client = None
        if self.api_key:
            try:
                from anthropic import AsyncAnthropic
                headers = {}
                if self.workspace_id:
                    headers["anthropic-workspace-id"] = self.workspace_id
                self.client = AsyncAnthropic(api_key=self.api_key, default_headers=headers if headers else None)
            except Exception as e:
                self.client = None
                self._init_error = str(e)
                logger.error(f"ShivaOrchestratorClient init failed: {e}")
        else:
            logger.error("ShivaOrchestratorClient: No CLAUDE_API_KEY found.")

    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            TOKEN_TELEMETRY.record_usage("shiva_orchestrator", latency_ms=0.0, error="NO_CLIENT")
            return GenerationResult(
                text="[ERROR: CLAUDE_API_KEY not set or ShivaOrchestratorClient uninitialized]",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0,
                error="NO_CLIENT"
            )
        t0 = time.time()
        async def _call():
            kwargs = {
                "model": self.model_name,
                "max_tokens": self.max_tokens,
                "messages": [{"role": "user", "content": prompt}]
            }
            if system_prompt:
                kwargs["system"] = system_prompt
            thinking_kw = _claude_thinking_kwargs(
                self.model_name,
                enable_thinking=self.enable_thinking,
                thinking_budget=self.thinking_budget,
                effort=self.thinking_effort
            )
            kwargs.update(thinking_kw)
            return await self.client.messages.create(**kwargs)
        try:
            response = await call_with_backoff(_call)
            latency = (time.time() - t0) * 1000.0
            p_tok, c_tok, th_tok, tot_tok = _extract_anthropic_tokens(response)
            
            text_out = _first_text(response)
            if not text_out.strip():
                err_msg = f"EMPTY_RESPONSE ({th_tok} thinking tokens, 0 text tokens)" if th_tok > 0 else "EMPTY_RESPONSE"
                TOKEN_TELEMETRY.record_usage("shiva_orchestrator", p_tok, c_tok, th_tok, tot_tok, round(latency, 2), error=err_msg)
                return GenerationResult(
                    text=f"[SHIVA EMPTY RESPONSE - {self.model_name}]: {err_msg}",
                    token_probabilities=[], model_name=self.model_name, latency_ms=round(latency, 2),
                    prompt_tokens=p_tok, candidate_tokens=c_tok, thinking_tokens=th_tok, total_tokens=tot_tok,
                    error="EMPTY_RESPONSE"
                )

            TOKEN_TELEMETRY.record_usage("shiva_orchestrator", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=text_out,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            TOKEN_TELEMETRY.record_usage("shiva_orchestrator", latency_ms=0.0, error=str(e))
            return GenerationResult(
                text=f"[SHIVA API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0,
                error="API_ERROR"
            )


# Backward-compatible alias
CheshireClient = CheshireCatClient

# Canonical Model Role Registry — 7 Sovereign Agents
INTEGRA_MODEL_REGISTRY = {
    "left_hemisphere": {
        "client_class": Y789Client,
        "default_model": "gemini-3.1-pro-preview",
        "reasoning": "Deep Think / Extended Thinking",
        "description": "Analytical Engine (Spock) / Deconstruction & Formal Verification"
    },
    "right_hemisphere": {
        "client_class": NexusClient,
        "default_model": "claude-opus-5-5",
        "reasoning": "Adaptive Thinking / effort=high",
        "description": "Synthetic Engine (Kirk) / Emergence & Generative Fusion"
    },
    "cheshire_cat": {
        "client_class": CheshireCatClient,
        "default_model": "gemini-3.8-flash",
        "description": "Thalamic Arbitrator & Fast Environmental Paradox Conduit"
    },
    "rodin_retrieval": {
        "client_class": RodinClient,
        "default_model": "gemini-3.8-flash",
        "embedding_model": "text-embedding-004",
        "description": "Rodin Route Retrieval — KNN Topological Memory Engine"
    },
    "jean_grey_phoenix": {
        "client_class": JeanGreyClient,
        "default_model": "gemini-3.1-pro-preview",
        "reasoning": "Deep Think / thinking_budget=16384",
        "description": "Jean Grey: Operation Phoenix Force — SWDS Neuroevolution Smelting"
    },
    "cheshire_protocol": {
        "client_class": CheshireProtocolDaemonClient,
        "default_model": "gemini-3.8-flash",
        "description": "Cheshire Protocol Daemon — Conduit & Paradox Intelligence"
    },
    "shiva_orchestrator": {
        "client_class": ShivaOrchestratorClient,
        "default_model": "claude-sonnet-5-5",
        "reasoning": "Adaptive Thinking / effort=medium",
        "description": "Shiva Action Suite — Multi-Lens Orchestration & Synthesis"
    },
}
