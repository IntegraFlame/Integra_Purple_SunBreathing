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


@pytest.fixture(autouse=True)
def celestial_checkpoint_in_tmp(tmp_path, monkeypatch):
    """
    No test writes the celestial checkpoint of the tree it runs in (Brain Map T1, R4): the process-wide
    Celestial Sentinel's checkpoint paths point into the test's tmp_path for the duration of each test.
    """
    from temporal.celestial_sentinel import get_sentinel

    sentinel = get_sentinel()
    monkeypatch.setattr(sentinel, "checkpoint_path", tmp_path / "celestial" / "checkpoint.json")
    monkeypatch.setattr(sentinel, "legacy_checkpoint_path", tmp_path / "celestial" / "legacy_checkpoint.json")
    yield
