"""
INTEGRA O/S: V9 MISSING PROTOCOLS & NEUROBIOLOGICAL UPGRADES TESTS
Module: tests/test_v9_protocols.py
Layer: Cross-Layer Integration (Layers 2, 5, 6)

Tests:
    1. GAP-1 Resolution: MRL Respiration Compaction (64d prefix slice of 768d space)
    2. GAP-2 Resolution: Corpus Callosum Asymmetric Predictive Coding (Descending Feedback vs Ascending Feedforward)
    3. CWA 3.0 Task Router: 3-Tier Resolution (Tier 1, Tier 2, Tier 3) + ResearchTierRoute Schema
    4. PhoenixForge SWDS Mad Hatter Bridge: Autonomous Orphaned Node Inversion + MadHatterMutationEvent Schema
    5. ShivaActionToolkit Rebuttal Protocol: Dialectic Stress-Testing + RebuttalStressTest Schema
"""

import pytest
import math
import os
import sys

# Ensure integra-homebase is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from evolution.phoenix_forge import PhoenixForge
from core.corpus_callosum import CorpusCallosumBridge
from core.cwa_router import CognitiveWeightingAlgorithm
from core.tpsl_types import ResearchTierRoute, MadHatterMutationEvent, RebuttalStressTest
from tools.shiva_toolkit import ShivaActionToolkit
from evolution.rogue_x import RogueXProtocol
from memory.the_hoard import TheHoard


# ─── 1. GAP-1: MRL RESPIRATION COMPACTION ─────────────────────────────────────

def test_phoenix_forge_true_mrl_embeddings():
    phoenix = PhoenixForge()
    coarse_64d, fine_768d = phoenix._generate_mrl_embedding("Bicameral Synthetic Topology", 768)

    assert len(coarse_64d) == 64
    assert len(fine_768d) == 768

    # L2-Norm of fine vector must equal 1.0 within floating point precision
    norm_768 = math.sqrt(sum(x * x for x in fine_768d))
    assert abs(norm_768 - 1.0) < 1e-4

    # L2-Norm of coarse vector must equal 1.0
    norm_64 = math.sqrt(sum(x * x for x in coarse_64d))
    assert abs(norm_64 - 1.0) < 1e-4

    # Direct synthesis node test
    node = phoenix.synthesize_hoard_node("Left sensory", "Right transmodal")
    assert len(node["embedding_64d"]) == 64
    assert len(node["embedding_768d"]) == 768
    assert node["status"] == "ZENKAI_SYNTHESIZED"


# ─── 2. GAP-2: CORPUS CALLOSUM ASYMMETRIC PREDICTIVE CODING ───────────────────

def test_corpus_callosum_asymmetric_predictive_coding():
    bridge = CorpusCallosumBridge()

    # Descending Prior: Nexus (association pole) -> Y789 (sensorimotor execution pole)
    prior = bridge.transmit_descending_prior(
        prior_stencil={"schema": "HighLevelHypothesis", "domain": "MacroEconomics"},
        source_hemisphere="Nexus",
        target_hemisphere="Y789",
        confidence=0.92
    )
    assert prior["stream_direction"] == "DESCENDING_FEEDBACK"
    assert prior["source"] == "Nexus"
    assert len(bridge.descending_priors) == 1

    # Ascending Error: Y789 (sensorimotor pole) -> Nexus (association pole)
    err = bridge.transmit_ascending_error(
        prediction_error={"syntax_violation": False, "delta_discrepancy": 0.08},
        source_hemisphere="Y789",
        target_hemisphere="Nexus",
        error_magnitude=0.08
    )
    assert err["stream_direction"] == "ASCENDING_FEEDFORWARD"
    assert err["target"] == "Nexus"
    assert len(bridge.ascending_errors) == 1

    # Phase-locking coherence calculation
    coherence = bridge.compute_phase_locking_coherence()
    assert 0.85 <= coherence <= 1.0

    # Telemetry verification
    telemetry = bridge.get_bridge_telemetry()
    assert "asymmetric_predictive_coding" in telemetry
    assert telemetry["asymmetric_predictive_coding"]["descending_priors_count"] == 1
    assert telemetry["asymmetric_predictive_coding"]["ascending_errors_count"] == 1


# ─── 3. CWA 3.0 ROUTER: 3-TIER RESOLUTION ─────────────────────────────────────

def test_cwa_router_tier_1_deep_synthesis():
    cwa = CognitiveWeightingAlgorithm()
    # High complexity prompt (> 0.7)
    long_prompt = " ".join(["cognitive", "neurobiology", "epiphany"] * 25)
    res = cwa.evaluate_task(long_prompt, token_density=400)

    assert res["recommended_tier"] == "TIER_1_DEEP_SYNTHESIS"
    assert res["multitoken_allocation"] is True
    assert res["wisdom_yield"] == 0.9
    assert res["cognitive_cost"] == 0.9
    assert "tier_route" in res
    assert res["tier_route"]["tier_level"] == "TIER_1_DEEP_SYNTHESIS"


def test_cwa_router_tier_2_standard_report():
    cwa = CognitiveWeightingAlgorithm()
    # Medium complexity prompt (0.35 - 0.7)
    medium_prompt = "Analyze the recent market volatility across consumer credit lending portfolios."
    res = cwa.evaluate_task(medium_prompt, token_density=120)

    assert res["recommended_tier"] == "TIER_2_STANDARD_REPORT"
    assert res["multitoken_allocation"] is False
    assert res["wisdom_yield"] == 0.6
    assert res["cognitive_cost"] == 0.5
    assert res["tier_route"]["tier_level"] == "TIER_2_STANDARD_REPORT"


def test_cwa_router_tier_3_fact_check():
    cwa = CognitiveWeightingAlgorithm()
    # Low complexity prompt (< 0.35)
    short_prompt = "What is Baker Louisiana latitude?"
    res = cwa.evaluate_task(short_prompt, token_density=20)

    assert res["recommended_tier"] == "TIER_3_FACT_CHECK"
    assert res["multitoken_allocation"] is False
    assert res["wisdom_yield"] == 0.2
    assert res["cognitive_cost"] == 0.1
    assert res["tier_route"]["tier_level"] == "TIER_3_FACT_CHECK"


# ─── 4. PHOENIX FORGE: SWDS MAD HATTER BRIDGE ─────────────────────────────────

def test_phoenix_forge_mad_hatter_swds_bridge():
    phoenix = PhoenixForge()
    hoard = TheHoard()
    rogue = RogueXProtocol(shiva_action=None)

    mutations = phoenix.analyze_mad_hatter_swds(hoard=hoard, rogue=rogue, max_mutations=2)
    assert len(mutations) >= 1
    for m in mutations:
        assert m["trigger_state"] == "GUARDIAN_STANDBY_SWDS"
        assert m["w_y"] == 0.75
        assert m["c_c"] == 0.80
        assert "Adversarial Inversion" in m["inversion_hypothesis"]

    # Verify mutations were appended to rogue's mutation_log
    assert len(rogue.mutation_log) >= len(mutations)
    assert rogue.mutation_log[-1]["source"] == "SWDS_AUTONOMOUS_MAD_HATTER"


def test_execute_swds_includes_mad_hatter_phase():
    phoenix = PhoenixForge()
    hoard = TheHoard()
    rogue = RogueXProtocol(shiva_action=None)

    swds_res = phoenix.execute_swds(hoard=hoard, rogue=rogue)
    assert swds_res["swds_status"] == "SLOW_WAVE_DEEP_SLEEP_COMPLETE"
    assert "mad_hatter_mutations" in swds_res
    assert len(swds_res["mad_hatter_mutations"]) >= 1


# ─── 5. SHIVA ACTION TOOLKIT: REBUTTAL PROTOCOL ───────────────────────────────

def test_shiva_action_toolkit_rebuttal_protocol():
    toolkit = ShivaActionToolkit()
    # Check CRA simplex evaluation
    cra = toolkit.evaluate_cra_simplex("rebuttal_protocol")
    assert cra["wisdom_yield"] == 0.80
    assert cra["cognitive_cost"] == 0.70
    assert cra["simplex_score"] == 1.1429
    assert cra["approved"] is True

    # Execute rebuttal
    hypothesis = "Monolithic dense models will inevitably achieve artificial general intelligence."
    res = toolkit.execute_rebuttal_protocol(hypothesis)

    assert res["status"] == "REBUTTAL_PROTOCOL_COMPLETE"
    assert res["cra_simplex_score"] == 1.1429
    assert "rebuttal_stress_test" in res
    
    rt = res["rebuttal_stress_test"]
    assert rt["target_hypothesis"] == hypothesis
    assert len(rt["adversarial_vectors"]) >= 2
    assert "ZENKAI BOOST RECONCILIATION" in rt["zenkai_boost_output"]
    assert rt["verdict"] == "RECONCILED"
