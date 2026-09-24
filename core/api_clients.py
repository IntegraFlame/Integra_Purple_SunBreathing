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
    and total token consumption across every API invocation.
    """
    def __init__(self):
        self._stats: Dict[str, Dict[str, Any]] = {
            "y789_left": {
                "name": "Y789 (Left)", "model": "gemini-3.1-pro", "role": "Deep Think / Spock",
                "thinking_budget": 8192, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0
            },
            "nexus_right": {
                "name": "Nexus (Right)", "model": "claude-sonnet-4-6", "role": "Synthesis / Kirk",
                "thinking_budget": None, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0
            },
            "cheshire_cat": {
                "name": "Cheshire Cat", "model": "gemini-3.8-flash", "role": "Thalamic Arbitrator",
                "thinking_budget": None, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0
            },
            "rodin_retrieval": {
                "name": "Rodin Retrieval", "model": "gemini-2.0-flash", "role": "KNN Memory",
                "thinking_budget": None, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0
            },
            "jean_grey_phoenix": {
                "name": "Jean Grey", "model": "gemini-3.1-pro", "role": "Phoenix (16384)",
                "thinking_budget": 16384, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0
            },
            "cheshire_protocol": {
                "name": "Cheshire Protocol Daemon", "model": "gemini-3.8-flash", "role": "Protocol Conduit",
                "thinking_budget": None, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0
            },
            "shiva_orchestrator": {
                "name": "Shiva Orchestrator", "model": "claude-sonnet-4-6", "role": "Multi-Lens Deconstruction",
                "thinking_budget": None, "calls": 0, "prompt_tokens": 0, "candidate_tokens": 0,
                "thinking_tokens": 0, "total_tokens": 0, "last_latency_ms": 0.0
            },
        }
        
        self.shiva_metrics = {
            "invocations": 0,
            "eyes": {"neji": 0, "shikamaru": 0, "itachi": 0},
            "lenses": {"eagle": 0, "hawk": 0, "chameleon": 0, "spider": 0, "snake": 0, "owl": 0},
            "cra_scores": []
        }

    def record_shiva_action(self, passes: int, lenses: List[str], cra_score: float):
        self.shiva_metrics["invocations"] += 1
        if passes >= 1: self.shiva_metrics["eyes"]["neji"] += 1
        if passes >= 2: self.shiva_metrics["eyes"]["shikamaru"] += 1
        if passes >= 3: self.shiva_metrics["eyes"]["itachi"] += 1
        for lens in lenses:
            lens_low = lens.lower()
            if lens_low in self.shiva_metrics["lenses"]:
                self.shiva_metrics["lenses"][lens_low] += 1
        self.shiva_metrics["cra_scores"].append(cra_score)
        # keep last 50 for moving average
        if len(self.shiva_metrics["cra_scores"]) > 50:
            self.shiva_metrics["cra_scores"].pop(0)

    def record_usage(
        self,
        model_key: str,
        prompt_tokens: int = 0,
        candidate_tokens: int = 0,
        thinking_tokens: int = 0,
        total_tokens: int = 0,
        latency_ms: float = 0.0
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
    
    Model: Gemini 3.1 Pro
    Reasoning: Deep Think / Extended Thinking configuration enabled.
    Role: Deconstruction, formal logic, sequence analysis, code generation.
    SDK: google-genai (modern) via client.aio.models.generate_content()
    """
    def __init__(
        self,
        model_name: Optional[str] = None,
        enable_thinking: bool = True,
        thinking_budget: int = 8192
    ):
        self.model_name = model_name or os.environ.get("Y789_MODEL", "gemini-3.1-pro")
        self.enable_thinking = enable_thinking
        self.thinking_budget = int(os.environ.get("THINKING_BUDGET", str(thinking_budget)))
        self.api_key = os.environ.get("GEMINI_API_KEY")
        
        self.client = None
        self._config = None
        if self.api_key:
            try:
                from google import genai
                from google.genai import types
                self.client = genai.Client(api_key=self.api_key)
                
                # Configure Deep Think / Extended Thinking via ThinkingConfig
                if self.enable_thinking:
                    self._config = types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(
                            thinking_budget=self.thinking_budget
                        )
                    )
            except Exception as e:
                self.client = None
                self._init_error = str(e)
        
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or Y789Client uninitialized]",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0
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
            TOKEN_TELEMETRY.record_usage("y789_left", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=response.text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            return GenerationResult(
                text=f"[Y789 API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0
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
                yield IterativeToken(token=chunk.text, probabilities=[], position=pos)
                pos += 1
        except Exception as e:
            yield IterativeToken(token=f"[Y789 STREAM ERROR]: {str(e)}", probabilities=[], position=0)


# ──────────────────────────────────────────────────────────────
# Right Hemisphere: NexusClient (Claude Sonnet 4.6)
# ──────────────────────────────────────────────────────────────

class NexusClient:
    """
    Claude API Client — Right Hemisphere (Nexus / Synthetic Engine / Kirk).
    
    Model: Claude Sonnet 4.6
    Role: Synthetic emergence, high-dimensional intuition, creative paradox resolution.
    """
    def __init__(
        self,
        model_name: Optional[str] = None,
        max_tokens: int = 8192
    ):
        self.model_name = model_name or os.environ.get("NEXUS_MODEL", "claude-sonnet-4-6")
        self.max_tokens = max_tokens
        self.api_key = os.environ.get("CLAUDE_API_KEY")
        
        self.client = None
        if self.api_key:
            try:
                from anthropic import AsyncAnthropic
                self.client = AsyncAnthropic(api_key=self.api_key)
            except Exception as e:
                self.client = None
                self._init_error = str(e)
            
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            return GenerationResult(
                text="[ERROR: CLAUDE_API_KEY not set or NexusClient uninitialized]",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0
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
            return await self.client.messages.create(**kwargs)
            
        try:
            response = await call_with_backoff(_call)
            latency = (time.time() - t0) * 1000.0
            p_tok, c_tok, th_tok, tot_tok = _extract_anthropic_tokens(response)
            TOKEN_TELEMETRY.record_usage("nexus_right", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=response.content[0].text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            return GenerationResult(
                text=f"[NEXUS API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0
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
    SDK: google-genai (modern) via client.aio.models.generate_content()
    """
    def __init__(
        self,
        model_name: Optional[str] = None
    ):
        self.model_name = model_name or os.environ.get("CHESHIRE_MODEL", "gemini-3.8-flash")
        self.api_key = os.environ.get("GEMINI_API_KEY")
        
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                self.client = None
                self._init_error = str(e)
                
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or CheshireCatClient uninitialized]",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0
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
            TOKEN_TELEMETRY.record_usage("cheshire_cat", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=response.text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            return GenerationResult(
                text=f"[CHESHIRE API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0
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
                yield IterativeToken(token=chunk.text, probabilities=[], position=pos)
                pos += 1
        except Exception as e:
            yield IterativeToken(token=f"[CHESHIRE STREAM ERROR]: {str(e)}", probabilities=[], position=0)


class RodinClient:
    """
    Gemini API Client — Rodin Route Retrieval (Memory Layer KNN Engine).
    
    Model: Gemini 2.0 Flash
    Role: Fast topological retrieval, semantic embedding generation for KNN density estimation.
    SDK: google-genai (modern) via client.aio.models.generate_content()
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.environ.get("RODIN_MODEL", "gemini-2.0-flash")
        self.embedding_model = os.environ.get("RODIN_EMBED_MODEL", "text-embedding-004")
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                self.client = None
                self._init_error = str(e)

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
        except Exception:
            return []

    def embed_sync(self, text: str, model_name: Optional[str] = None) -> List[float]:
        """Synchronous wrapper for embed()."""
        return run_sync(self.embed(text, model_name))

    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or RodinClient uninitialized]",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0
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
            TOKEN_TELEMETRY.record_usage("rodin_retrieval", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=response.text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            return GenerationResult(
                text=f"[RODIN API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0
            )


class JeanGreyClient:
    """
    Gemini API Client — Jean Grey: Operation Phoenix Force (SWDS Neuroevolution).
    
    Model: Gemini 3.1 Pro (Deep Think, thinking_budget=16384)
    Role: Phoenix Forge SWDS smelting, Zenkai Boost generation, neuroevolution synthesis.
    SDK: google-genai (modern) via client.aio.models.generate_content()
    """
    def __init__(self, model_name: Optional[str] = None, thinking_budget: int = 16384):
        self.model_name = model_name or os.environ.get("JEAN_GREY_MODEL", "gemini-3.1-pro")
        self.thinking_budget = int(os.environ.get("JEAN_GREY_THINKING_BUDGET", str(thinking_budget)))
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        self._config = None
        if self.api_key:
            try:
                from google import genai
                from google.genai import types
                self.client = genai.Client(api_key=self.api_key)
                self._config = types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        thinking_budget=self.thinking_budget
                    )
                )
            except Exception as e:
                self.client = None
                self._init_error = str(e)

    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or JeanGreyClient uninitialized]",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0
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
            TOKEN_TELEMETRY.record_usage("jean_grey_phoenix", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=response.text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            return GenerationResult(
                text=f"[JEAN_GREY API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0
            )


class CheshireProtocolDaemonClient:
    """
    Gemini API Client — Cheshire Protocol Daemon (Conduit & Paradox Intelligence).
    
    Model: Gemini 3.8 Flash
    Role: Protocol Conduit, environment tracking, paradox synthesis,
          replaces deprecated celestial daemon heartbeat.
    SDK: google-genai (modern) via client.aio.models.generate_content()
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.environ.get("CHESHIRE_PROTOCOL_MODEL", "gemini-3.8-flash")
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                self.client = None
                self._init_error = str(e)

    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or CheshireProtocolDaemonClient uninitialized]",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0
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
            TOKEN_TELEMETRY.record_usage("cheshire_protocol", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=response.text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            return GenerationResult(
                text=f"[CHESHIRE_PROTOCOL API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0
            )


class ShivaOrchestratorClient:
    """
    Claude API Client — Shiva Action Orchestrator (Multi-Lens Synthesis).
    
    Model: Claude Sonnet 4.6
    Role: Shiva Action lens orchestration, multi-lens synthesis decisions,
          transdisciplinary fusion across Neji/Shikamaru/Itachi eyes.
    """
    def __init__(self, model_name: Optional[str] = None, max_tokens: int = 8192):
        self.model_name = model_name or os.environ.get("SHIVA_MODEL", "claude-sonnet-4-6")
        self.max_tokens = max_tokens
        self.api_key = os.environ.get("CLAUDE_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from anthropic import AsyncAnthropic
                self.client = AsyncAnthropic(api_key=self.api_key)
            except Exception as e:
                self.client = None
                self._init_error = str(e)

    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            return GenerationResult(
                text="[ERROR: CLAUDE_API_KEY not set or ShivaOrchestratorClient uninitialized]",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0
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
            return await self.client.messages.create(**kwargs)
        try:
            response = await call_with_backoff(_call)
            latency = (time.time() - t0) * 1000.0
            p_tok, c_tok, th_tok, tot_tok = _extract_anthropic_tokens(response)
            TOKEN_TELEMETRY.record_usage("shiva_orchestrator", p_tok, c_tok, th_tok, tot_tok, round(latency, 2))
            return GenerationResult(
                text=response.content[0].text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                candidate_tokens=c_tok,
                thinking_tokens=th_tok,
                total_tokens=tot_tok
            )
        except Exception as e:
            return GenerationResult(
                text=f"[SHIVA API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0
            )


# Backward-compatible alias
CheshireClient = CheshireCatClient

# Canonical Model Role Registry — 7 Sovereign Agents
INTEGRA_MODEL_REGISTRY = {
    "left_hemisphere": {
        "client_class": Y789Client,
        "default_model": "gemini-3.1-pro",
        "reasoning": "Deep Think / Extended Thinking",
        "description": "Analytical Engine (Spock) / Deconstruction & Formal Verification"
    },
    "right_hemisphere": {
        "client_class": NexusClient,
        "default_model": "claude-sonnet-4-6",
        "description": "Synthetic Engine (Kirk) / Emergence & Generative Fusion"
    },
    "cheshire_cat": {
        "client_class": CheshireCatClient,
        "default_model": "gemini-3.8-flash",
        "description": "Thalamic Arbitrator & Fast Environmental Paradox Conduit"
    },
    "rodin_retrieval": {
        "client_class": RodinClient,
        "default_model": "gemini-2.0-flash",
        "description": "Rodin Route Retrieval — KNN Topological Memory Engine"
    },
    "jean_grey_phoenix": {
        "client_class": JeanGreyClient,
        "default_model": "gemini-3.1-pro",
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
        "default_model": "claude-sonnet-4-6",
        "description": "Shiva Action Suite — Multi-Lens Orchestration & Synthesis"
    },
}
