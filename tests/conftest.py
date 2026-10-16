"""
INTEGRA O/S Test Configuration.
Handles Windows ChromaDB file lock cleanup for TemporaryDirectory, and keeps the offline tests offline.
"""
import gc
import pytest


@pytest.fixture(autouse=True)
def force_gc_between_tests():
    """Force garbage collection between tests to release ChromaDB file locks."""
    yield
    gc.collect()


@pytest.fixture(autouse=True)
def no_real_model_calls(request, monkeypatch):
    """
    Offline tests must never reach a paid model, even on a machine whose environment holds a key.
    Tests marked `live` are exempt; they exist to call the real APIs and are skipped unless asked for.
    The process-wide embedding service is cleared before and after every test.
    """
    from memory.embedding_service import reset_default_embedding_service

    if request.node.get_closest_marker("live") is None:
        for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_GENAI_USE_VERTEXAI", "USE_VERTEXAI"):
            monkeypatch.delenv(name, raising=False)
    reset_default_embedding_service(None)
    yield
    reset_default_embedding_service(None)
