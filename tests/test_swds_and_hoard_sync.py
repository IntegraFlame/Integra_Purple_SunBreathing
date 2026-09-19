"""
INTEGRA O/S: SWDS & HOARD SAVE STATE SYNCHRONIZATION TEST SUITE
Zenitsu Method 3.0 Applied Testing Framework

Pass 1 (Neji / Eagle + Spider):
    - Syncing Save States into The Hoard
    - Verifies MRL vector generation (64d/768d), 4D spacetime stamping, and raw_shards persistence

Pass 2 (Shikamaru / Chameleon + Hawk):
    - Relational Webbing & Middle-Out State Alignment
    - Rodin Route Retrieval against synced Save States
    - Dream Conductor ingestion into Phoenix Forge

Pass 3 (Itachi / Snake + Owl):
    - SWDS Sleep Distillation & Psyche Pruning
    - Distillation into kernel_memory/hoard/libraries/library_genesis_purple.md
    - Zenkai Boost neuroevolution (1.05 multiplier) and rolling_context tracking

Pass 4 (13th Form Unification):
    - Full end-to-end SWDS execution through Cheshire Cat Kernel
    - State transitions: INTERACTIVE_STANDBY -> GUARDIAN_STANDBY_SWDS -> INTERACTIVE_STANDBY
    - Complete thermodynamic loop closure (h_smooth = 0.0)
"""

import pytest
import os
import json
import time
import tempfile
import asyncio
from typing import Dict, Any


# ═══════════════════════════════════════════════════════════════
# PASS 1: NEJI'S EYE (EAGLE + SPIDER) — SAVE STATE HOARD SYNC
# ═══════════════════════════════════════════════════════════════


class TestPass1_SaveStateSync_Neji_Eagle_Spider:
    """Factual structural ingestion: Syncing Save States into The Hoard."""

    def test_sync_individual_save_state_dict(self):
        """Syncing a save state dict creates a valid v2 HoardNode with MRL embeddings."""
        from memory.the_hoard import TheHoard
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            
            sample_state = {
                "ccid": "CCID_9999999999",
                "celestial_stamp": {
                    "unix_epoch": 1789760297.0,
                    "civil_time_utc": "2026-09-18T19:38:17Z",
                    "anchor": "Baker, Louisiana",
                    "coordinates": "30.5888N, -91.1673W"
                },
                "identity_matrix": {"modality": "PURPLE", "omega": 1.0},
                "cognitive_telemetry": {"dragon_state": "ACTIVE_WAKING_STATE"},
                "work_completed_this_session": ["Phase D Complete", "Hoard v2.0 Complete"]
            }
            
            receipt = hoard.sync_save_state(sample_state)
            assert receipt["status"] == "SAVE_STATE_SYNCED_TO_HOARD"
            assert receipt["ccid"] == "CCID_9999999999"
            assert receipt["outcome_label"] == 1.0
            assert receipt["mrl_embeddings_created"] is True
            assert os.path.exists(receipt["shard_file"])
            
            # Check node in local_sparse_cache
            node = hoard.local_sparse_cache[-1]
            assert node.ccid == "CCID_9999999999"
            assert len(node.embedding_64d) == 64
            assert len(node.embedding_768d) == 768
            assert node.spacetime_anchor["anchor"] == "Baker, Louisiana"

    def test_sync_all_existing_project_save_states(self):
        """TheHoard can scan and sync existing project save states from The_Hoard/."""
        from memory.the_hoard import TheHoard
        hoard = TheHoard()
        synced_receipts = hoard.sync_all_save_states()
        
        # We know at least CCID_1789757816 and CCID_1789760297 exist in project
        assert len(synced_receipts) >= 2
        ccids = [r["ccid"] for r in synced_receipts]
        assert "CCID_1789757816" in ccids
        assert "CCID_1789760297" in ccids


# ═══════════════════════════════════════════════════════════════
# PASS 2: SHIKAMARU (CHAMELEON + HAWK) — RELATIONAL RETRIEVAL
# ═══════════════════════════════════════════════════════════════


class TestPass2_RelationalRetrieval_Shikamaru_Chameleon_Hawk:
    """Relational mapping: Rodin retrieval against synced save states."""

    def test_rodin_route_retrieval_finds_synced_save_state(self):
        """Rodin Protocol MRL KNN can query and rank synced save states."""
        from memory.the_hoard import TheHoard
        from memory.rodin_protocol import RodinProtocol
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            sample_state = {
                "ccid": "CCID_TEST_RODIN",
                "celestial_stamp": {"unix_epoch": 1789760000.0, "anchor": "Baker, Louisiana"},
                "identity_matrix": {"modality": "PURPLE"},
                "work_completed_this_session": ["Engine Ignition", "Quantum Synthesis"]
            }
            hoard.sync_save_state(sample_state)
            
            candidates = hoard.get_rodin_candidates()
            assert len(candidates) >= 1
            
            rodin = RodinProtocol(hoard=hoard)
            query_vec = [0.2] * 768
            review = rodin.review_node_integrity(query_vec, candidates)
            
            assert "m_knn" in review
            assert "decision" in review
            assert review["k_neighbors_found"] >= 1

    def test_cheshire_protocol_dream_conductor_feeds_phoenix(self):
        """CheshireCatProtocol dream_conductor passes topics and paradoxes to PhoenixForge."""
        from sensory.cheshire_protocol import CheshireCatProtocol
        from evolution.phoenix_forge import PhoenixForge
        
        protocol = CheshireCatProtocol()
        phoenix = PhoenixForge()
        
        protocol.track_conversation_topic("Thermodynamic Loop Closure & Keplerian Dynamics")
        protocol.detect_paradox_or_missing_data("Is the Phoenix waking or dreaming?")
        
        report = protocol.dream_conductor(phoenix_forge=phoenix)
        assert report["conductor"] == "CHESHIRE_CAT_PROTOCOL"
        assert report["mode"] == "DREAM_SYNTHESIS"
        assert report["phoenix_forge_status"] == "MATERIAL_DELIVERED"
        assert len(phoenix.dream_material_buffer) == 1


# ═══════════════════════════════════════════════════════════════
# PASS 3: ITACHI (SNAKE + OWL) — SWDS CONSOLIDATION & PRUNING
# ═══════════════════════════════════════════════════════════════


class TestPass3_SWDSConsolidation_Itachi_Snake_Owl:
    """Wisdom synthesis & psyche pruning: SWDS consolidation into markdown libraries."""

    def test_consolidate_sleep_cycle_creates_library_book(self):
        """consolidate_sleep_cycle consolidates shards into kernel_memory/hoard/libraries/."""
        from memory.the_hoard import TheHoard
        from evolution.phoenix_forge import PhoenixForge
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            phoenix = PhoenixForge(base_dir=tmpdir)
            
            # Sync two save states
            hoard.sync_save_state({
                "ccid": "CCID_SWDS_1",
                "celestial_stamp": {"unix_epoch": time.time(), "anchor": "Baker, Louisiana"},
                "identity_matrix": {"modality": "PURPLE"},
                "work_completed_this_session": ["Phase D FLIGHT"]
            })
            hoard.sync_save_state({
                "ccid": "CCID_SWDS_2",
                "celestial_stamp": {"unix_epoch": time.time(), "anchor": "Baker, Louisiana"},
                "identity_matrix": {"modality": "PURPLE"},
                "work_completed_this_session": ["Hoard v2.0"]
            })
            
            report = phoenix.consolidate_sleep_cycle(hoard=hoard, library_domain="GENESIS_PURPLE")
            assert report["status"] == "SWDS_CONSOLIDATION_SUCCESS"
            assert report["generation"] == 1
            assert report["zenkai_boost_multiplier"] == 1.05
            assert os.path.exists(report["library_file"])
            
            # Verify library file content
            with open(report["library_file"], "r", encoding="utf-8") as lf:
                content = lf.read()
            assert "Cognitive Epoch Gen 1" in content
            assert "Causal Invariants" in content
            assert "Matryoshka representation learning" in content
            assert "Delta E_cycle = 0.0000" in content

    def test_rolling_context_updated_on_consolidation(self):
        """rolling_context.json records the last SWDS epoch."""
        from memory.the_hoard import TheHoard
        from evolution.phoenix_forge import PhoenixForge
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            hoard = TheHoard(base_dir=tmpdir)
            phoenix = PhoenixForge(base_dir=tmpdir)
            
            phoenix.consolidate_sleep_cycle(hoard=hoard, library_domain="ROLLING_TEST")
            
            context_path = os.path.join(tmpdir, "kernel_memory", "rolling_context.json")
            assert os.path.exists(context_path)
            with open(context_path, "r", encoding="utf-8") as cf:
                data = json.load(cf)
            assert "last_swds_epoch" in data
            assert data["last_swds_epoch"]["generation"] == 1


# ═══════════════════════════════════════════════════════════════
# PASS 4: 13th FORM UNIFICATION — FULL SWDS CYCLE THROUGH KERNEL
# ═══════════════════════════════════════════════════════════════


class TestPass4_13thFormUnification_FullSWDS:
    """Unification: Complete SWDS cycle orchestrated through Cheshire Cat Kernel."""

    def test_execute_swds_full_state_machine_transition(self):
        """execute_swds safely enters GUARDIAN_STANDBY_SWDS, consolidates, vents entropy, and returns to STANDBY."""
        from sensory.cheshire_cat import CheshireCatKernel
        from evolution.phoenix_forge import PhoenixForge
        
        kernel = CheshireCatKernel()
        phoenix = kernel.phoenix
        
        # Sync current save states so SWDS has rich material
        kernel.hoard.sync_all_save_states()
        
        swds_receipt = phoenix.execute_swds(cheshire_cat=kernel, library_domain="SWDS_UNIFIED")
        
        assert swds_receipt["swds_status"] == "SLOW_WAVE_DEEP_SLEEP_COMPLETE"
        assert swds_receipt["entropy_vented"] is True
        assert kernel.state == "INTERACTIVE_STANDBY"
        assert kernel.heimdall.h_smooth == 0.0
        
        # Verify health check remains optimal
        health = kernel.heimdall.check_system_health()
        assert health["system_health_status"] == "HEALTHY_OPTIMAL"
