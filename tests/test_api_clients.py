import pytest
import os
import types
from core.api_clients import (
    _first_text,
    _claude_thinking_kwargs,
    _make_gemini_client,
    TOKEN_TELEMETRY,
    GenerationResult
)
from core.model_router import MODEL_ROUTER, PowerState


def test_first_text_with_leading_thinking_block():
    class DummyBlock:
        def __init__(self, type_, text=""):
            self.type = type_
            self.text = text

    class DummyResponse:
        def __init__(self, content):
            self.content = content

    resp = DummyResponse([
        DummyBlock("thinking", "Thinking step 1..."),
        DummyBlock("text", "Final Answer.")
    ])
    assert _first_text(resp) == "Final Answer."


def test_first_text_empty_and_text_only():
    class DummyBlock:
        def __init__(self, type_, text=""):
            self.type = type_
            self.text = text

    class DummyResponse:
        def __init__(self, content):
            self.content = content

    assert _first_text(None) == ""
    assert _first_text(DummyResponse([])) == ""
    assert _first_text(DummyResponse([DummyBlock("text", "Hello World")])) == "Hello World"


def test_claude_thinking_kwargs_generation_branching():
    # 5.x models should receive adaptive thinking + output_config.effort
    res_opus = _claude_thinking_kwargs("claude-opus-5-5", enable_thinking=True, effort="high")
    assert res_opus == {
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": "high"}
    }

    res_sonnet = _claude_thinking_kwargs("claude-sonnet-5-5", enable_thinking=True, effort="medium")
    assert res_sonnet == {
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": "medium"}
    }

    # 4.x models should receive enabled + budget_tokens
    res_legacy = _claude_thinking_kwargs("claude-sonnet-4-6", enable_thinking=True, thinking_budget=2048)
    assert res_legacy == {
        "thinking": {"type": "enabled", "budget_tokens": 2048}
    }

    # Disabled thinking returns empty dict
    assert _claude_thinking_kwargs("claude-opus-5-5", enable_thinking=False) == {}


def test_make_gemini_client_vertex_selection(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "AQ.test_key")
    monkeypatch.setenv("GOOGLE_GENAI_USE_VERTEXAI", "true")
    client = _make_gemini_client()
    assert client is not None
    assert getattr(client, "vertexai", False) is True


def test_model_router_has_all_7_components():
    status = MODEL_ROUTER.get_status()
    comps = status["components"]
    expected_keys = {
        "y789_left", "nexus_right", "cheshire_cat_kernel",
        "rodin_retrieval", "jean_grey_phoenix", "cheshire_protocol",
        "shiva_orchestrator"
    }
    for k in expected_keys:
        assert k in comps
        assert comps[k]["model"] != "unknown"


@pytest.mark.live
@pytest.mark.asyncio
async def test_live_claude_and_gemini_selftest():
    """
    Live test across model router clients. Requires valid API keys in environment.
    """
    MODEL_ROUTER.activate()
    
    # 1. Test Gemini 3.8 Flash
    cheshire = MODEL_ROUTER.get_routed_client("cheshire_cat_kernel")
    assert cheshire is not None
    res_cheshire = await cheshire.generate("Say OK")
    assert res_cheshire.error is None
    assert "OK" in res_cheshire.text.upper()

    # 2. Test Claude Opus 5.5
    nexus = MODEL_ROUTER.get_routed_client("nexus_right")
    assert nexus is not None
    res_nexus = await nexus.generate("Say OK")
    assert res_nexus.error is None
    assert len(res_nexus.text.strip()) > 0

    # 3. Test Rodin Embeddings (768 dimensions)
    rodin = MODEL_ROUTER.get_routed_client("rodin_retrieval")
    assert rodin is not None
    emb = await rodin.embed("Topological manifold embedding")
    assert len(emb) == 768
