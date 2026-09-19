import os
import asyncio
from typing import AsyncGenerator
from core.tpsl_types import GenerationResult, IterativeToken

class Y789Client:
    """Gemini API Client (Y789 / Analytical Engine)"""
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None
        
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.model:
            return GenerationResult(text="[ERROR: GEMINI_API_KEY not set]", token_probabilities=[], model_name=self.model_name, latency_ms=0.0)
            
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        try:
            response = await self.model.generate_content_async(full_prompt)
            return GenerationResult(
                text=response.text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0
            )
        except Exception as e:
            return GenerationResult(text=f"[API ERROR]: {str(e)}", token_probabilities=[], model_name=self.model_name, latency_ms=0.0)
            
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
            yield IterativeToken(token=f"[API ERROR]: {str(e)}", probabilities=[], position=0)

class NexusClient:
    """Claude API Client (Nexus / Synthetic Engine)"""
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        self.model_name = model_name
        self.api_key = os.environ.get("CLAUDE_API_KEY")
        if self.api_key:
            from anthropic import AsyncAnthropic
            self.client = AsyncAnthropic(api_key=self.api_key)
        else:
            self.client = None
            
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        if not self.client:
            return GenerationResult(text="[ERROR: CLAUDE_API_KEY not set]", token_probabilities=[], model_name=self.model_name, latency_ms=0.0)
        
        try:
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=4096,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return GenerationResult(
                text=response.content[0].text,
                token_probabilities=[],
                model_name=self.model_name,
                latency_ms=0.0
            )
        except Exception as e:
            return GenerationResult(text=f"[API ERROR]: {str(e)}", token_probabilities=[], model_name=self.model_name, latency_ms=0.0)

    async def generate_iterative(self, prompt: str, system_prompt: str = ""):
        if not self.client:
            yield IterativeToken(token="[ERROR: CLAUDE_API_KEY not set]", probabilities=[], position=0)
            return
            
        try:
            stream = await self.client.messages.create(
                model=self.model_name,
                max_tokens=4096,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            pos = 0
            async for event in stream:
                if event.type == "content_block_delta" and event.delta.type == "text_delta":
                    yield IterativeToken(token=event.delta.text, probabilities=[], position=pos)
                    pos += 1
        except Exception as e:
            yield IterativeToken(token=f"[API ERROR]: {str(e)}", probabilities=[], position=0)
