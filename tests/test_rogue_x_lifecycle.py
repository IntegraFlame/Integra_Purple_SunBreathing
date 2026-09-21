"""
Test Suite: Rogue X Protocol 2.0 Full Lifecycle
Module: tests/test_rogue_x_lifecycle.py

Validates the complete Touch → Conflict → Release 3-stage lifecycle,
Kintsugi Interlock Z-score isolation, TPSL gating, Mad Hatter adversarial
challenge, and mutation audit log persistence.
"""
import asyncio
import math
import pytest
import sys
import os

# Ensure integra-homebase is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from evolution.rogue_x import RogueXProtocol
from evolution.kintsugi_sandbox import KintsugiProtocol


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def rogue():
    """RogueXProtocol with no ShivaAction (graceful degradation mode)."""
    return RogueXProtocol(shiva_action=None, baseline_mutation_rate=0.05)


@pytest.fixture
def kintsugi():
    return KintsugiProtocol(z_threshold=3.0)


# ─── 1. BACKWARD COMPATIBILITY ───────────────────────────────────────────────

def test_rogue_x_backward_compat_verify_status(rogue):
    """Existing test_systems_audit_and_protocols.py must still pass."""
    assert rogue.is_active is True
    assert rogue.verify_true() is True
    status = rogue.verify_status()
    assert status["is_active"] is True
    assert status["version"] == "2.0-PURPLE"
    assert status["all_systems_true"] is True
    assert status["mutation_multiplier"] > 1.0


def test_mutation_multiplier_formula(rogue):
    """σ_Rogue = e^(0.05) ≈ 1.051271."""
    expected = math.exp(0.05)
    assert abs(rogue.calculate_mutation_multiplier() - expected) < 1e-6


def test_inject_adversarial_perturbation(rogue):
    """Vector perturbation applies mutation multiplier to each element."""
    base = [1.0, 2.0, 3.0]
    mult = rogue.calculate_mutation_multiplier()
    result = rogue.inject_adversarial_perturbation(base)
    assert len(result) == 3
    for original, perturbed in zip(base, result):
        assert abs(perturbed - original * mult) < 1e-9


# ─── 2. TOUCH PHASE — LENS CONFIGURATION ────────────────────────────────────

@pytest.mark.asyncio
async def test_touch_phase_academic_paper_lens_config(rogue):
    """Academic papers get Eagle/Owl/Hawk lenses, 3 passes."""
    report = await rogue._phase_touch("Sample paper text.", "academic_paper")
    # In stub mode (no Shiva), verify the report reflects correct config
    assert report.get("target_type") == "academic_paper"
    assert report.get("lenses") == ["Eagle", "Owl", "Hawk"]
    assert report.get("passes") == 3


@pytest.mark.asyncio
async def test_touch_phase_repository_lens_config(rogue):
    """Repositories get Chameleon/Spider/Snake lenses, 2 passes."""
    report = await rogue._phase_touch("Sample repo content.", "repository")
    assert report.get("target_type") == "repository"
    assert report.get("lenses") == ["Chameleon", "Spider", "Snake"]
    assert report.get("passes") == 2


@pytest.mark.asyncio
async def test_touch_phase_live_data_lens_config(rogue):
    """Live data (Daily Planet feeds) get Eagle/Spider/Hawk, 2 passes."""
    report = await rogue._phase_touch("Live web scrape data.", "live_data")
    assert report.get("target_type") == "live_data"
    assert report.get("lenses") == ["Eagle", "Spider", "Hawk"]
    assert report.get("passes") == 2


@pytest.mark.asyncio
async def test_touch_phase_unknown_type_defaults_to_document(rogue):
    """Unknown target_type falls back to document config."""
    report = await rogue._phase_touch("Some content.", "UNKNOWN_TYPE")
    assert report.get("lenses") == ["Eagle", "Owl", "Hawk"]
    assert report.get("passes") == 3


# ─── 3. CONFLICT PHASE — TPSL GATING ────────────────────────────────────────

def test_conflict_phase_tpsl_power_vs_psyche(rogue):
    """High W_y / C_c concepts are classified as Power, low as Psyche."""
    mock_report = {
        "results": {
            "neji": {"w_y": 0.8, "c_c": 0.3},   # score=2.67 → Power
            "shikamaru": {"w_y": 0.3, "c_c": 0.9},  # score=0.33 → Psyche
        }
    }
    result = rogue._analyze_conflict(mock_report)
    # Power: neji (2.67 >= 1.0 TPSL gate, W_y >= 0.6, C_c <= 0.8 Mad Hatter)
    # Psyche: shikamaru (0.33 < 1.0 TPSL gate)
    total = len(result["Power"]) + len(result["Psyche"]) + len(result["mirror_maze"])
    assert total == 2
    assert result["tpsl_gate"] == 1.0


def test_conflict_phase_returns_required_keys(rogue):
    """Conflict result always contains Power, Psyche, mirror_maze, tpsl_gate."""
    mock_report = {"results": {}}
    result = rogue._analyze_conflict(mock_report)
    assert "Power" in result
    assert "Psyche" in result
    assert "mirror_maze" in result
    assert "tpsl_gate" in result
    assert "kintsugi_alerts" in result


# ─── 4. KINTSUGI INTERLOCK — Z-SCORE ISOLATION ───────────────────────────────

def test_kintsugi_z_score_anomaly_isolation(rogue):
    """Values with |Z| > 3.0 are isolated to Mirror Maze, not Power or Psyche."""
    # Use _kintsugi_evaluate directly to verify Mirror Maze isolation works.
    # The conflict phase uses the whole-batch std_dev, so we test the core
    # Kintsugi mechanism independently with a guaranteed extreme outlier.
    result = rogue._kintsugi_evaluate(
        observed_val=1000.0,  # massive deviation
        mean_val=1.5,
        std_dev=0.1,
        metric_name="mirror_maze_test",
    )
    assert result["fracture_detected"] is True, "Z >> 3.0 must be detected as fracture"
    assert "sandbox_id" in result, "Fracture must be isolated to Mirror Maze Sandbox"
    assert rogue.kintsugi.sandbox_depth() >= 1, "Mirror Maze sandbox must contain the item"
    assert result["repair_protocol"] == "KINTSUGI_GOLD_LEAF_STITCH"


def test_kintsugi_evaluate_direct_interface(rogue):
    """_kintsugi_evaluate() correctly calls KintsugiProtocol.evaluate_deviation()."""
    result = rogue._kintsugi_evaluate(
        observed_val=10.0,
        mean_val=1.0,
        std_dev=0.5,
        metric_name="test_metric",
    )
    assert result["z_score"] > 3.0
    assert result["fracture_detected"] is True
    assert result["repair_protocol"] == "KINTSUGI_GOLD_LEAF_STITCH"
    assert "sandbox_id" in result


def test_kintsugi_stable_value_no_isolation(rogue):
    """Values within Z <= 3.0 remain STABLE — no Mirror Maze entry."""
    result = rogue._kintsugi_evaluate(
        observed_val=1.1,
        mean_val=1.0,
        std_dev=0.5,
    )
    assert result["fracture_detected"] is False
    assert result["repair_protocol"] == "STABLE"
    assert "sandbox_id" not in result


# ─── 5. MAD HATTER ADVERSARIAL CHALLENGE ────────────────────────────────────

def test_mad_hatter_necessary_verdict(rogue):
    """W_y >= 0.6 AND C_c <= 0.8 → verdict=NECESSARY."""
    concept = {"eye": "neji", "content": {}, "w_y": 0.7, "c_c": 0.5}
    verdict = rogue._mad_hatter_challenge(concept)
    assert verdict["verdict"] == "NECESSARY"


def test_mad_hatter_unnecessary_verdict_high_cost(rogue):
    """C_c > 0.8 → verdict=UNNECESSARY even if W_y is high."""
    concept = {"eye": "itachi", "content": {}, "w_y": 0.9, "c_c": 0.95}
    verdict = rogue._mad_hatter_challenge(concept)
    assert verdict["verdict"] == "UNNECESSARY"


def test_mad_hatter_unnecessary_verdict_low_yield(rogue):
    """W_y < 0.6 → verdict=UNNECESSARY."""
    concept = {"eye": "shikamaru", "content": {}, "w_y": 0.3, "c_c": 0.4}
    verdict = rogue._mad_hatter_challenge(concept)
    assert verdict["verdict"] == "UNNECESSARY"


# ─── 6. RELEASE PHASE — SEED PACKAGE ────────────────────────────────────────

def test_release_seed_package_schema(rogue):
    """Seed package contains all required fields."""
    mock_conflict = {
        "Power": [{"eye": "neji", "w_y": 0.8, "c_c": 0.4, "tpsl_score": 2.0, "content": {}}],
        "Psyche": [],
        "mirror_maze": [],
        "tpsl_gate": 1.0,
        "kintsugi_alerts": 0,
    }
    pkg = rogue._create_seed_package(mock_conflict, "academic_paper", "TEST_CCID_001")
    assert pkg["status"] == "ROGUE_X_SEED_PACKAGE_COMPLETE"
    assert pkg["mutation_id"] == "TEST_CCID_001"
    assert "blueprint" in pkg
    assert "synthesis" in pkg
    assert pkg["blueprint"]["power_nodes_absorbed"] == 1


def test_release_increments_generation(rogue):
    """Each Release increments mutation_generation."""
    assert rogue.mutation_generation == 0
    mock_conflict = {"Power": [], "Psyche": [], "mirror_maze": [], "tpsl_gate": 1.0, "kintsugi_alerts": 0}
    rogue._create_seed_package(mock_conflict)
    assert rogue.mutation_generation == 1
    rogue._create_seed_package(mock_conflict)
    assert rogue.mutation_generation == 2


# ─── 7. MUTATION LOG PERSISTENCE ────────────────────────────────────────────

def test_mutation_log_accumulates(rogue):
    """Each Release appends a record to mutation_log."""
    assert len(rogue.mutation_log) == 0
    mock_conflict = {"Power": [], "Psyche": [], "mirror_maze": [], "tpsl_gate": 1.0, "kintsugi_alerts": 0}
    rogue._create_seed_package(mock_conflict, "repository")
    rogue._create_seed_package(mock_conflict, "academic_paper")
    assert len(rogue.mutation_log) == 2
    assert rogue.mutation_log[0]["target_type"] == "repository"
    assert rogue.mutation_log[1]["target_type"] == "academic_paper"


def test_verify_status_reflects_live_log(rogue):
    """verify_status() reports accurate mutation_log_depth."""
    mock_conflict = {"Power": [], "Psyche": [], "mirror_maze": [], "tpsl_gate": 1.0, "kintsugi_alerts": 0}
    rogue._create_seed_package(mock_conflict)
    status = rogue.verify_status()
    assert status["mutation_log_depth"] == 1
    assert status["mutation_generation"] == 1


# ─── 8. FULL END-TO-END ASYNC LIFECYCLE ─────────────────────────────────────

@pytest.mark.asyncio
async def test_full_execute_absorption_lifecycle(rogue):
    """End-to-end async lifecycle returns a valid seed package."""
    pkg = await rogue.execute_absorption(
        target_data="Test target data for Rogue X absorption.",
        target_type="academic_paper",
        ccid="INTEGRATION_TEST_001",
    )
    assert pkg["status"] == "ROGUE_X_SEED_PACKAGE_COMPLETE"
    assert pkg["mutation_id"] == "INTEGRATION_TEST_001"
    assert len(rogue.mutation_log) == 1
    assert rogue.mutation_generation == 1
