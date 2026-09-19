"""
INTEGRA O/S Test Configuration.
Handles Windows ChromaDB file lock cleanup for TemporaryDirectory.
"""
import gc
import pytest


@pytest.fixture(autouse=True)
def force_gc_between_tests():
    """Force garbage collection between tests to release ChromaDB file locks."""
    yield
    gc.collect()
