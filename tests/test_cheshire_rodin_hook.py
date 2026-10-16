"""
INTEGRA O/S: CHESHIRE CYCLE <-> RODIN HOOK TEST SUITE (offline)

process_cognitive_cycle() is an `async def` that called Rodin's route_retrieval() directly. route_retrieval() now
embeds the prompt (a blocking network call with a timeout), so the cycle must hand it to a worker thread instead of
stalling the event loop that also runs the 30 Hz Flame loop and every async route. And when Rodin could not use the
model, the cycle's receipt must say so: before this change a failed embedding returned plausible junk neighbours.
"""

import threading

import pytest

from memory.embedding_service import EmbeddingService, EmbeddingSpace, EmbeddingUnavailable
from sensory.cheshire_cat import CheshireCatKernel
from tests.embedding_fakes import ScriptedBackend

PROMPT = "Synthesize harmonic coordinates for the celestial orbital bridge."


@pytest.mark.asyncio
async def test_the_cycle_runs_route_retrieval_off_the_event_loop_thread():
    kernel = CheshireCatKernel()
    seen = {}
    original = kernel.rodin.route_retrieval

    def spy(prompt):
        seen["thread"] = threading.get_ident()
        return original(prompt)

    kernel.rodin.route_retrieval = spy
    loop_thread = threading.get_ident()
    result = await kernel.process_cognitive_cycle(PROMPT)
    assert result["status"] == "COMMITTED_TO_HOARD"
    assert seen["thread"] != loop_thread


@pytest.mark.asyncio
async def test_the_receipt_says_when_retrieval_was_degraded_and_why():
    kernel = CheshireCatKernel()
    kernel.rodin.embedder = EmbeddingService(
        ScriptedBackend(errors=[EmbeddingUnavailable("API_ERROR", "503 unavailable")]), EmbeddingSpace())
    result = await kernel.process_cognitive_cycle(PROMPT)
    assert result["status"] == "COMMITTED_TO_HOARD"
    assert result["rodin_retrieval"]["degraded"] is True
    assert result["rodin_retrieval"]["fallback_reason"] == "EMBEDDING_UNAVAILABLE:API_ERROR"


@pytest.mark.asyncio
async def test_the_receipt_reports_a_healthy_retrieval_as_not_degraded():
    kernel = CheshireCatKernel()
    kernel.rodin.embedder = EmbeddingService(ScriptedBackend(), EmbeddingSpace())
    kernel.hoard.embedder = None
    result = await kernel.process_cognitive_cycle(PROMPT)
    assert result["rodin_retrieval"]["degraded"] is False
    assert result["rodin_retrieval"]["embedding_space"] == EmbeddingSpace().id
