"""
INTEGRA O/S: HOARD SCHEMA v2.0 TEST SUITE
Zenitsu Method 3.0 Applied Testing

Pass 1 (Neji / Spider): Knowledge & Relational Webbing
    - HoardNode schema, TheHoard instantiation, kernel_memory/ directory creation
    
Pass 2 (Shikamaru / Chameleon): Understanding & Dead-Zone Penetration
    - Rodin integration, embedding pipeline, legacy backward compatibility
    
Pass 3 (Itachi / Snake + Owl): Wisdom & Loop Closure
    - Staleness tracking, outcome labeling, Phoenix synthesis round-trip
"""

import pytest
import os
import json
import time
import tempfile
import shutil
from typing import Dict, Any


# ═══════════════════════════════════════════════════════════════
# PASS 1: NEJI + SPIDER (Knowledge & Relational Webbing)
# ═══════════════════════════════════════════════════════════════


class TestPass1_HoardNode_Knowledge:
    """Structural verification of HoardNode and TheHoard initialization."""

    def test_hoard_node_has_all_v2_fields(self):
        """HoardNode must expose all v2.0 schema fields."""
        from memory.the_hoard import HoardNode
        node = HoardNode(
            ccid="TEST_001",
            payload={"test": True},
            spacetime_anchor={"x": 1.0, "y": 0.5, "z": 0.0, "t": 0},
        )
        assert node.ccid == "TEST_001"
        assert node.outcome_label == 0.5  # Default UNKNOWN
        assert node.is_stale is False
        assert isinstance(node.created_at, float)
        assert len(node.embedding_64d) == 64
        assert len(node.embedding_768d) == 768
        assert node.sufficiency_score == 1.0
        assert isinstance(node.metadata, dict)

    def test_hoard_node_serialization_roundtrip(self):
        """to_dict() and from_dict() must be lossless."""
        from memory.the_hoard import HoardNode
        original = HoardNode(
            ccid="ROUNDTRIP_001",
            payload={"key": "value", "nested": {"a": 1}},
            spacetime_anchor={"x": 30.5888, "y": -91.1673, "z": 0.0, "t": 42},
            outcome_label=1.0,
            metadata={"source": "test"},
        )
        serialized = original.to_dict()
        restored = HoardNode.from_dict(serialized)
        assert restored.ccid == original.ccid
        assert restored.payload == original.payload
        assert restored.outcome_label == 1.0
        assert restored.spacetime_anchor == original.spacetime_anchor

    def test_hoard_node_to_rodin_candidate(self):
        """to_rodin_candidate() must emit the fields Rodin expects."""
        from memory.the_hoard import HoardNode
        node = HoardNode(
            ccid="RODIN_001",
            payload="test payload",
            spacetime_anchor={"t": 1},
            embedding_768d=[0.1] * 768,
            outcome_label=1.0,
        )
        candidate = node.to_rodin_candidate()
        assert "embedding" in candidate
        assert len(candidate["embedding"]) == 768
        assert candidate["outcome_label"] == 1.0
        assert "created_at" in candidate
        assert candidate["ccid"] == "RODIN_001"

    def test_the_hoard_creates_kernel_memory_dirs(self):
        """TheHoard must create the full kernel_memory/ directory tree."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            km = os.path.join(tmpdir, "kernel_memory")
            assert os.path.isdir(km)
            assert os.path.isdir(os.path.join(km, "hoard", "raw_shards"))
            assert os.path.isdir(os.path.join(km, "hoard", "modules"))
            assert os.path.isdir(os.path.join(km, "hoard", "libraries"))
            assert os.path.isdir(os.path.join(km, "vectors"))
            assert os.path.isdir(os.path.join(km, "drop_in"))
            assert os.path.isfile(os.path.join(km, "core_identity.txt"))
            assert os.path.isfile(os.path.join(km, "rolling_context.json"))

    def test_core_identity_file_contents(self):
        """core_identity.txt must contain Integra identity anchors."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            identity_path = os.path.join(tmpdir, "kernel_memory", "core_identity.txt")
            with open(identity_path, "r") as f:
                content = f.read()
            assert "INTEGRA" in content
            assert "PURPLE" in content
            assert "Starfire" in content


# ═══════════════════════════════════════════════════════════════
# PASS 2: SHIKAMARU + CHAMELEON (Understanding & Dead-Zone)
# ═══════════════════════════════════════════════════════════════


class TestPass2_HoardIntegration_Understanding:
    """Relational verification: Hoard ↔ Rodin ↔ Phoenix pipeline."""

    def test_commit_node_v2_persists_to_raw_shards(self):
        """commit_node_v2() must persist a full-schema JSON shard to disk."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            result = hoard.commit_node_v2(
                payload={"insight": "test"},
                spacetime_anchor={"x": 1.0, "y": 0.5, "z": 0.0, "t": 99},
                ccid="SHARD_001",
                embedding_768d=[0.5] * 768,
                outcome_label=1.0,
                metadata={"source": "test"},
            )
            assert result["status"] == "COMMITTED_TO_HOARD_V2"
            assert result["has_embeddings"] is True
            
            # Verify on-disk shard
            shard_path = result["file"]
            assert os.path.exists(shard_path)
            with open(shard_path, "r") as f:
                data = json.load(f)
            assert data["ccid"] == "SHARD_001"
            assert data["outcome_label"] == 1.0
            assert len(data["embedding_768d"]) == 768

    def test_legacy_commit_node_backward_compatible(self):
        """Legacy commit_node() must still work with v1 callers."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            result = hoard.commit_node(
                payload="legacy payload",
                vector_4d={"x": 1.0, "y": 0.5, "z": 0.0, "t": 0},
                ccid="LEGACY_001",
            )
            assert result["status"] == "COMMITTED_TO_HOARD"
            assert len(hoard.local_sparse_cache) == 1
            node = hoard.local_sparse_cache[0]
            assert node.ccid == "LEGACY_001"
            assert node.outcome_label == 0.5  # Default UNKNOWN

    def test_get_rodin_candidates_returns_correct_format(self):
        """get_rodin_candidates() must return Rodin-compatible dicts."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            hoard.commit_node_v2(
                payload="test",
                spacetime_anchor={"t": 1},
                ccid="RODIN_POOL_001",
                embedding_768d=[0.3] * 768,
            )
            candidates = hoard.get_rodin_candidates()
            assert len(candidates) == 1
            c = candidates[0]
            assert "embedding" in c
            assert len(c["embedding"]) == 768
            assert "outcome_label" in c
            assert "created_at" in c

    def test_rodin_can_process_hoard_candidates(self):
        """Rodin MRL pipeline must accept HoardNode candidates."""
        from memory.the_hoard import TheHoard
        from memory.rodin_protocol import RodinProtocol
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            # Commit multiple nodes with varied embeddings
            for i in range(5):
                hoard.commit_node_v2(
                    payload=f"knowledge_{i}",
                    spacetime_anchor={"t": i},
                    ccid=f"MRL_{i}",
                    embedding_768d=[float(i) / 10.0] * 768,
                    outcome_label=1.0 if i % 2 == 0 else 0.0,
                )
            
            rodin = RodinProtocol(hoard=hoard)
            query = [0.3] * 768  # Similar to node MRL_3
            candidates = hoard.get_rodin_candidates()
            
            # Run MRL Phase 1
            coarse = rodin.mrl_coarse_filter(query, candidates)
            assert isinstance(coarse, list)
            
            # Run full pipeline
            integrity = rodin.review_node_integrity(query, candidates)
            assert "m_knn" in integrity
            assert "decision" in integrity

    def test_query_internal_finds_matching_nodes(self):
        """query_internal() must find nodes by substring match on payload."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            hoard.commit_node_v2(
                payload={"topic": "entropy and thermodynamics"},
                spacetime_anchor={"t": 1},
                ccid="QUERY_001",
            )
            hoard.commit_node_v2(
                payload={"topic": "cooking recipes"},
                spacetime_anchor={"t": 2},
                ccid="QUERY_002",
            )
            results = hoard.query_internal(["entropy"])
            assert len(results) == 1
            assert results[0]["ccid"] == "QUERY_001"

    def test_phoenix_synthesize_emits_v2_fields(self):
        """Phoenix synthesize_hoard_node() must emit v2.0 fields."""
        from evolution.phoenix_forge import PhoenixForge
        phoenix = PhoenixForge()
        node = phoenix.synthesize_hoard_node("analytical", "synthetic")
        assert "embedding_64d" in node
        assert "embedding_768d" in node
        assert len(node["embedding_64d"]) == 64
        assert len(node["embedding_768d"]) == 768
        assert node["outcome_label"] == 0.5
        assert "created_at" in node

    def test_phoenix_to_hoard_full_pipeline(self):
        """Phoenix output must commit directly to TheHoard v2."""
        from memory.the_hoard import TheHoard
        from evolution.phoenix_forge import PhoenixForge
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            phoenix = PhoenixForge()
            
            synth = phoenix.synthesize_hoard_node("Y789 output", "Nexus output")
            result = hoard.commit_node_v2(
                payload=synth["payload"],
                spacetime_anchor=synth["spacetime_anchor"],
                ccid=synth["ccid"],
                embedding_64d=synth["embedding_64d"],
                embedding_768d=synth["embedding_768d"],
                outcome_label=synth["outcome_label"],
            )
            assert result["status"] == "COMMITTED_TO_HOARD_V2"
            assert result["has_embeddings"] is True


# ═══════════════════════════════════════════════════════════════
# PASS 3: ITACHI + SNAKE + OWL (Wisdom & Loop Closure)
# ═══════════════════════════════════════════════════════════════


class TestPass3_HoardWisdom:
    """Boundary conditions, staleness, outcome labeling, disk persistence."""

    def test_mark_outcome_updates_in_memory_and_disk(self):
        """mark_outcome() must update both cache and on-disk shard."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            hoard.commit_node_v2(
                payload="test",
                spacetime_anchor={"t": 1},
                ccid="OUTCOME_001",
            )
            # Initially UNKNOWN
            assert hoard.local_sparse_cache[0].outcome_label == 0.5
            
            # Mark SUCCESS
            assert hoard.mark_outcome("OUTCOME_001", 1.0) is True
            assert hoard.local_sparse_cache[0].outcome_label == 1.0
            
            # Verify disk was updated
            shard_path = os.path.join(
                tmpdir, "kernel_memory", "hoard", "raw_shards", "OUTCOME_001.json"
            )
            with open(shard_path, "r") as f:
                data = json.load(f)
            assert data["outcome_label"] == 1.0

    def test_mark_outcome_returns_false_for_missing_ccid(self):
        """mark_outcome() must return False if ccid not found."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            assert hoard.mark_outcome("NONEXISTENT", 1.0) is False

    def test_get_stale_nodes_identifies_old_nodes(self):
        """get_stale_nodes() must flag nodes older than the threshold."""
        from memory.the_hoard import TheHoard, HoardNode
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            # Commit a node with a very old timestamp
            old_node = HoardNode(
                ccid="STALE_001",
                payload="old data",
                spacetime_anchor={"t": 0},
                created_at=time.time() - 700000,  # ~8 days old
            )
            hoard.local_sparse_cache.append(old_node)
            
            fresh_node = HoardNode(
                ccid="FRESH_001",
                payload="fresh data",
                spacetime_anchor={"t": 1},
                created_at=time.time(),
            )
            hoard.local_sparse_cache.append(fresh_node)
            
            stale = hoard.get_stale_nodes()
            assert len(stale) == 1
            assert stale[0].ccid == "STALE_001"
            assert stale[0].is_stale is True

    def test_load_shards_from_disk_restores_state(self):
        """load_shards_from_disk() must restore nodes from raw_shards/."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            # Phase 1: Commit nodes
            hoard1 = TheHoard(base_dir=tmpdir)
            hoard1.commit_node_v2(
                payload="persisted knowledge",
                spacetime_anchor={"t": 42},
                ccid="PERSIST_001",
                embedding_768d=[0.42] * 768,
                outcome_label=1.0,
            )
            assert len(hoard1.local_sparse_cache) == 1
            
            # Phase 2: Fresh TheHoard instance (simulates restart)
            hoard2 = TheHoard(base_dir=tmpdir)
            assert len(hoard2.local_sparse_cache) == 0  # Empty on init
            loaded = hoard2.load_shards_from_disk()
            assert loaded == 1
            assert hoard2.local_sparse_cache[0].ccid == "PERSIST_001"
            assert hoard2.local_sparse_cache[0].outcome_label == 1.0

    def test_telemetry_reflects_current_state(self):
        """get_telemetry() must accurately report the Hoard's state."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            hoard.commit_node_v2(
                payload="a",
                spacetime_anchor={"t": 1},
                ccid="TEL_001",
                embedding_768d=[0.1] * 768,
                outcome_label=1.0,
            )
            hoard.commit_node_v2(
                payload="b",
                spacetime_anchor={"t": 2},
                ccid="TEL_002",
            )
            
            tel = hoard.get_telemetry()
            assert tel["total_nodes"] == 2
            assert tel["labeled_nodes"] == 1  # Only TEL_001 has non-0.5 outcome
            assert tel["embedded_nodes"] == 1  # Only TEL_001 has non-zero embeddings
            assert tel["schema_version"] == "2.0"

    def test_cheshire_cat_kernel_can_use_upgraded_hoard(self):
        """
        The Cheshire Cat Kernel must still function with the upgraded Hoard.
        This is the Loop Closure verification — the thermodynamic invariant
        must hold after the schema change.
        """
        import asyncio
        from sensory.cheshire_cat import CheshireCatKernel
        kernel = CheshireCatKernel()
        
        # Verify the Hoard instance is the upgraded version
        assert hasattr(kernel.hoard, 'commit_node_v2')
        assert hasattr(kernel.hoard, 'get_rodin_candidates')
        assert hasattr(kernel.hoard, 'kernel_memory_dir')
        
        # Run a full cognitive cycle — must still return HEALTHY
        result = asyncio.run(kernel.process_cognitive_cycle(
            "Verify Hoard v2.0 integration"
        ))
        assert result["system_health_status"] == "HEALTHY_OPTIMAL"
