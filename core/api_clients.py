import os
import json
import re
import asyncio
import time
from typing import AsyncGenerator, Optional, Dict, Any, Callable
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
            return GenerationResult(
                text=response.text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2)
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
            return GenerationResult(
                text=response.content[0].text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2)
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
            return GenerationResult(
                text=response.text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=round(latency, 2)
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
            return GenerationResult(
                text=response.text, token_probabilities=[],
                model_name=self.model_name, latency_ms=round(latency, 2)
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
            return GenerationResult(
                text=response.text, token_probabilities=[],
                model_name=self.model_name, latency_ms=round(latency, 2)
            )
        except Exception as e:
            return GenerationResult(
                text=f"[JEAN_GREY API ERROR - {self.model_name}]: {str(e)}",
                token_probabilities=[], model_name=self.model_name, latency_ms=0.0
            )


class CelestialDaemonClient:
    """
    Gemini API Client — Celestial Daemon (Heartbeat & Temporal Continuity).
    
    Model: Gemini 3.8 Flash
    Role: Celestial Sentinel heartbeat intelligence, connects to Cheshire Cat Protocol,
          persists temporal checkpoints for reboot continuity.
    SDK: google-genai (modern) via client.aio.models.generate_content()
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.environ.get("CELESTIAL_DAEMON_MODEL", "gemini-3.8-flash")
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
                text="[ERROR: GEMINI_API_KEY not set or CelestialDaemonClient uninitialized]",
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
            return GenerationResult(
                text=response.text, token_probabilities=[],
                model_name=self.model_name, latency_ms=round(latency, 2)
            )
        except Exception as e:
            return GenerationResult(
                text=f"[CELESTIAL_DAEMON API ERROR - {self.model_name}]: {str(e)}",
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
            return GenerationResult(
                text=response.content[0].text, token_probabilities=[],
                model_name=self.model_name, latency_ms=round(latency, 2)
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
    "celestial_daemon": {
        "client_class": CelestialDaemonClient,
        "default_model": "gemini-3.8-flash",
        "description": "Celestial Sentinel — Heartbeat Intelligence & Temporal Continuity"
    },
    "shiva_orchestrator": {
        "client_class": ShivaOrchestratorClient,
        "default_model": "claude-sonnet-4-6",
        "description": "Shiva Action Suite — Multi-Lens Orchestration & Synthesis"
    },
}
