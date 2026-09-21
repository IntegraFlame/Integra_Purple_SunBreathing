"""
INTEGRA O/S: OMEGA METRIC & 4-STEP CIRCUIT BREAKER TESTS
Module: tests/test_omega_circuit_breaker.py
Layer: 4 (Sensory Cortex & Metacognitive Gating)

Tests:
    1. calculate_omega_metric: nominal and degraded states
    2. execute_circuit_breaker: Steps 1 (Throttle), 2 (Veto), 3 (Isolate), 4 (UGL Reset)
    3. cascade_circuit_breaker: full 4-step emergency sequence
    4. DragonEngine integration: hard cognitive halt and circuit breaker engagement
"""

import pytest
import os
import sys

# Ensure integra-homebase is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sensory.heimdall import Heimdall31
from core.dragon_engine import DragonEngine
from core.corpus_callosum import CorpusCallosumBridge
from evolution.kintsugi_sandbox import KintsugiProtocol


def test_calculate_omega_metric_nominal():
    heimdall = Heimdall31()
    # High agency (1.0), low entropy (0.2) -> Omega ~ 5.0 >> floor (0.40)
    res = heimdall.calculate_omega_metric(agency_score=1.0, entropy_val=0.2, celestial_scalar=1.0)
    assert res["is_healthy"] is True
    assert res["status"] == "NOMINAL"
    assert res["omega"] > 4.0


def test_calculate_omega_metric_degraded():
    heimdall = Heimdall31()
    # High entropy (3.5), agency (1.0) -> Omega ~ 0.2857 < floor (0.40)
    res = heimdall.calculate_omega_metric(agency_score=1.0, entropy_val=3.5, celestial_scalar=1.0)
    assert res["is_healthy"] is False
    assert res["status"] == "DEGRADED"
    assert res["omega"] < 0.40


def test_circuit_breaker_step_1_throttle():
    heimdall = Heimdall31()
    res = heimdall.execute_circuit_breaker(step=1)
    assert res["action"] == "STEP_1_THROTTLE"
    assert res["temperature_ceiling"] == 0.1
    assert res["latency_penalty_ms"] == 250


def test_circuit_breaker_step_2_veto_with_corpus_callosum():
    heimdall = Heimdall31()
    cc = CorpusCallosumBridge()
    heimdall.register_component("corpus_callosum", cc)

    res = heimdall.execute_circuit_breaker(step=2, context_data={"reason": "Test high entropy"})
    assert res["action"] == "STEP_2_VETO"
    assert res["inter_hemispheric_halt"] is True
    assert cc.veto_active is True
    assert "Test high entropy" in cc.veto_reason


def test_circuit_breaker_step_3_isolate_with_kintsugi():
    heimdall = Heimdall31()
    # Boost entropy to breach
    heimdall.h_smooth = 4.5
    kintsugi = KintsugiProtocol(z_threshold=1.0)
    # Seed history to allow z-score calculation
    kintsugi.metric_history["circuit_breaker_anomaly"] = [1.0, 1.2, 1.1]
    heimdall.register_component("kintsugi", kintsugi)

    res = heimdall.execute_circuit_breaker(step=3, context_data={"raw_input": "Anomalous prompt"})
    assert res["action"] == "STEP_3_ISOLATE"
    assert res["status"] == "ISOLATED_IN_MIRROR_MAZE"
    assert len(kintsugi.retrieve_sandbox_items()) >= 1


def test_circuit_breaker_step_4_ugl_reset():
    heimdall = Heimdall31()
    res = heimdall.execute_circuit_breaker(step=4, context_data={"raw_input": "Grounding seed content"})
    assert res["action"] == "STEP_4_UGL_RESET"
    assert "ugl_grounding_prompt" in res
    assert "Ground truth source anchor" in res["ugl_grounding_prompt"]
    assert res["recovery_state"] == "UGL_RESET_ENGAGED"


def test_cascade_circuit_breaker_runs_all_four_steps():
    heimdall = Heimdall31()
    cc = CorpusCallosumBridge()
    kintsugi = KintsugiProtocol()
    heimdall.register_component("corpus_callosum", cc)
    heimdall.register_component("kintsugi", kintsugi)

    cascade = heimdall.cascade_circuit_breaker(context_data={"raw_input": "Cascade test prompt"})
    assert len(cascade) == 4
    assert cascade[0]["action"] == "STEP_1_THROTTLE"
    assert cascade[1]["action"] == "STEP_2_VETO"
    assert cascade[2]["action"] == "STEP_3_ISOLATE"
    assert cascade[3]["action"] == "STEP_4_UGL_RESET"


def test_dragon_engine_triggers_circuit_breaker_on_omega_collapse():
    heimdall = Heimdall31()
    # Set high entropy so Omega collapses below 0.40
    heimdall.h_smooth = 3.8
    engine = DragonEngine(heimdall=heimdall)

    result = engine.process_intention("Evaluate catastrophic high entropy state")
    assert result["action_decision"] == "CIRCUIT_BREAKER_ENGAGED"
    assert "circuit_breaker_cascade" in result
    assert len(result["circuit_breaker_cascade"]) == 4
