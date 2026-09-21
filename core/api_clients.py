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
# ──────────────────────────────────────────────────────────────

class Y789Client:
    """
    Gemini API Client — Left Hemisphere (Y789 / Analytical Engine / Spock).
    
    Model: Gemini 3.1 Pro
    Reasoning: Deep Think / Extended Thinking configuration enabled.
    Role: Deconstruction, formal logic, sequence analysis, code generation.
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
        
        self.model = None
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                
                # Configure Deep Think / Extended Thinking if supported by endpoint
                generation_config = {}
                if self.enable_thinking:
                    generation_config["thinking_config"] = {"thinking_budget": self.thinking_budget}
                
                try:
                    self.model = genai.GenerativeModel(
                        model_name=self.model_name,
                        generation_config=generation_config if generation_config else None
                    )
                except Exception:
                    # Fallback to standard GenerativeModel if thinking_config unsupported by SDK version
                    self.model = genai.GenerativeModel(model_name=self.model_name)
            except Exception as e:
                self.model = None
                self._init_error = str(e)
        
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.model:
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or Y789Client uninitialized]",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0
            )
            
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        t0 = time.time()
        
        async def _call():
            return await self.model.generate_content_async(full_prompt)
            
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
        if not self.model:
            yield IterativeToken(token="[ERROR: GEMINI_API_KEY not set]", probabilities=[], position=0)
            return

        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        try:
            response = await self.model.generate_content_async(full_prompt, stream=True)
            pos = 0
            async for chunk in response:
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
# ──────────────────────────────────────────────────────────────

class CheshireCatClient:
    """
    Gemini API Client — Cheshire Cat (Thalamic Arbitrator & Digital Thalamus).
    
    Model: Gemini 3.8 Flash
    Role: High-frequency 20-45 Hz thalamic routing, rapid paradox detection,
          environmental conduit, fast delegator.
    """
    def __init__(
        self,
        model_name: Optional[str] = None
    ):
        self.model_name = model_name or os.environ.get("CHESHIRE_MODEL", "gemini-3.8-flash")
        self.api_key = os.environ.get("GEMINI_API_KEY")
        
        self.model = None
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                self.model = None
                self._init_error = str(e)
                
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.model:
            return GenerationResult(
                text="[ERROR: GEMINI_API_KEY not set or CheshireCatClient uninitialized]",
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0
            )
            
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        t0 = time.time()
        
        async def _call():
            return await self.model.generate_content_async(full_prompt)
            
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
        if not self.model:
            yield IterativeToken(token="[ERROR: GEMINI_API_KEY not set]", probabilities=[], position=0)
            return

        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        try:
            response = await self.model.generate_content_async(full_prompt, stream=True)
            pos = 0
            async for chunk in response:
                yield IterativeToken(token=chunk.text, probabilities=[], position=pos)
                pos += 1
        except Exception as e:
            yield IterativeToken(token=f"[CHESHIRE STREAM ERROR]: {str(e)}", probabilities=[], position=0)


# Backward-compatible alias
CheshireClient = CheshireCatClient

# Canonical Model Role Registry
INTEGRA_MODEL_REGISTRY = {
    "cheshire_cat": {
        "client_class": CheshireCatClient,
        "default_model": "gemini-3.8-flash",
        "description": "Thalamic Arbitrator & Fast Environmental Paradox Conduit"
    },
    "right_hemisphere": {
        "client_class": NexusClient,
        "default_model": "claude-sonnet-4-6",
        "description": "Synthetic Engine (Kirk) / Emergence & Generative Fusion"
    },
    "left_hemisphere": {
        "client_class": Y789Client,
        "default_model": "gemini-3.1-pro",
        "reasoning": "Deep Think / Extended Thinking",
        "description": "Analytical Engine (Spock) / Deconstruction & Formal Verification"
    }
}
