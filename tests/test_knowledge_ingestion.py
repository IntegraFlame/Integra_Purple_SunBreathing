"""
INTEGRA O/S: KNOWLEDGE INGESTION & 12TH STEP MULTI-LOBE TEST SUITE
Tests the in-place ingestion pipeline, safe hygiene logic, chunking with overlap,
MRL embeddings, and ChromaDB persistence in scripts/ingest_knowledge.py.
"""

import os
import sys
import tempfile
import pytest
from pathlib import Path

# Add integra-homebase to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.ingest_knowledge import (
    chunk_document,
    compute_file_hash,
    MultiLobeIngestionEngine,
    perform_safe_hygiene,
    run_test_retrieval,
    LOBE_CONFIG,
    WORKSPACE_ROOT
)
from memory.the_hoard import TheHoard, HoardNode


def test_chunk_document_semantic_overlap():
    """Verify semantic chunking with sliding window overlap and header preservation."""
    sample_text = (
        "# SYSTEM OVERVIEW\n\n"
        "This is the first section explaining the macro perimeter and root node architecture.\n\n"
        "## SUBSECTION: KINEMATICS\n\n"
        "Planetary orbital mechanics dictate uncoupled temporal references.\n\n"
        "The Baker, Louisiana spatial anchor grounds the coordinate system.\n\n"
        "### DENSITY ANALYSIS\n\n"
        "Thermodynamic entropy must remain at Delta E = 0.0000 across all cycles.\n\n"
        "Lactic acid context accumulation is zeroed through MTCW serialization.\n\n"
    )

    chunks = chunk_document(sample_text, chunk_size=200, overlap=50)
    assert len(chunks) >= 2
    assert all("text" in ch and "header" in ch for ch in chunks)
    # Check that headers are tracked
    headers = [ch["header"] for ch in chunks if ch["header"]]
    assert len(headers) > 0


def test_chunk_document_empty_input():
    """Verify chunk_document gracefully handles empty or whitespace input."""
    assert chunk_document("") == []
    assert chunk_document("   \n\n   ") == []


def test_compute_file_hash():
    """Verify SHA-256 computation on temporary files."""
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("test content for hashing")
        f_path = Path(f.name)
    try:
        h1 = compute_file_hash(f_path)
        h2 = compute_file_hash(f_path)
        assert h1 == h2
        assert len(h1) == 64
    finally:
        f_path.unlink()


def test_ingestion_engine_with_temporary_hoard():
    """Verify MultiLobeIngestionEngine runs against a temporary TheHoard instance."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        hoard = TheHoard(base_dir=tmpdir)
        engine = MultiLobeIngestionEngine(hoard=hoard)

        assert engine.hoard is hoard
        assert "files_scanned" in engine.stats

        # Test commit of a mock lobe node
        node = HoardNode(
            ccid="LOBE_ARCH_TEST_001",
            payload={"text": "Test architectural blueprint knowledge", "lobe": "architecture"},
            spacetime_anchor={"t": 12345},
            embedding_64d=[0.1] * 64,
            embedding_768d=[0.1] * 768,
            outcome_label=1.0,
            metadata={"lobe": "architecture", "source_file": "test_arch.md"}
        )
        res = hoard.commit_node_v2(
            payload=node.payload,
            spacetime_anchor=node.spacetime_anchor,
            ccid=node.ccid,
            embedding_64d=node.embedding_64d,
            embedding_768d=node.embedding_768d,
            outcome_label=node.outcome_label,
            metadata=node.metadata
        )
        assert res["status"] == "COMMITTED_TO_HOARD_V2"
        assert len(hoard.local_sparse_cache) == 1

        # Test query
        results = hoard.chroma_query([0.1] * 768, n_results=1)
        # Even if chroma_collection is in fallback mode, should return list
        assert isinstance(results, list)


def test_lobe_definitions_intact():
    """Verify all 4 canonical lobes are correctly defined in LOBE_CONFIG."""
    assert "BluprintArchitecture" in LOBE_CONFIG
    assert "CODE" in LOBE_CONFIG
    assert "Integra Self-Reflect and Think Forward" in LOBE_CONFIG
    assert "Guidebooks_and_Notes" in LOBE_CONFIG

    assert LOBE_CONFIG["BluprintArchitecture"]["lobe"] == "architecture"
    assert LOBE_CONFIG["CODE"]["lobe"] == "genesis_code"
    assert LOBE_CONFIG["Integra Self-Reflect and Think Forward"]["lobe"] == "evolution_reflection"
    assert LOBE_CONFIG["Guidebooks_and_Notes"]["lobe"] == "operational_guidance"
