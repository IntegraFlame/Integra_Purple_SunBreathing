"""
Unit and Integration Tests for Heimdall 3.1 Sensory Cortex & Health Sentinel
"""

import os
import sys
import math
import pytest
from fastapi.testclient import TestClient

# Ensure integra-homebase is on sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from sensory.heimdall import Heimdall31, HeimdallMonitor
from sensory.cheshire_cat import CheshireCatKernel
from sensory.pssr_lookback import PSSRLookback
from temporal.celestial_clock import CelestialClockArchitecture
from fortress.bank_lobe import FridayFortressBank
from main import app


class TestHeimdallCalculations:
    def test_pure_distribution_zero_entropy(self):
        heimdall = Heimdall31()
        h_instant = heimdall.calculate_instant_entropy([1.0])
        assert math.isclose(h_instant, 0.0, abs_tol=1e-5)

    def test_uniform_distribution_shannon_entropy(self):
        heimdall = Heimdall31()
        # 8 uniform states: log2(8) = 3.0 bits
        uniform_8 = [0.125] * 8
        h_instant = heimdall.calculate_instant_entropy(uniform_8)
        assert math.isclose(h_instant, 3.0, abs_tol=1e-5)

    def test_unnormalized_and_degenerate_entropy(self):
        heimdall = Heimdall31()
        # Unnormalized probabilities / frequencies: [2.0, 2.0] -> [0.5, 0.5] -> 1.0 bit
        h_unnorm = heimdall.calculate_instant_entropy([2.0, 2.0])
        assert math.isclose(h_unnorm, 1.0, abs_tol=1e-5)

        # Frequencies [50, 50] -> 1.0 bit
        h_freq = heimdall.calculate_instant_entropy([50.0, 50.0])
        assert math.isclose(h_freq, 1.0, abs_tol=1e-5)

        # Non-positive numbers and empty
        assert heimdall.calculate_instant_entropy([]) == 0.0
        assert heimdall.calculate_instant_entropy([-1.0, 0.0]) == 0.0

    def test_exponential_moving_average_smoothing(self):
        heimdall = Heimdall31(alpha=0.3)
        # First step: H_0 = 0.0, H_instant = 3.0
        # Expected: 0.3 * 3.0 + 0.7 * 0.0 = 0.90
        h_smooth, breached = heimdall.evaluate_probabilities([0.125] * 8)
        assert math.isclose(h_smooth, 0.90, abs_tol=1e-2)
        assert not breached

        # Second step: H_instant = 3.0
        # Expected: 0.3 * 3.0 + 0.7 * 0.9 = 0.9 + 0.63 = 1.53
        h_smooth, breached = heimdall.evaluate_probabilities([0.125] * 8)
        assert math.isclose(h_smooth, 1.53, abs_tol=1e-2)
        assert not breached

    def test_entropy_threshold_breach(self):
        heimdall = Heimdall31(alpha=1.0, trip_threshold=2.5)
        # With alpha=1.0, H_smooth = H_instant
        # 8 uniform states = 3.0 bits > 2.5 bits
        h_smooth, breached = heimdall.evaluate_probabilities([0.125] * 8)
        assert h_smooth == 3.0
        assert breached is True

    def test_text_entropy_evaluation(self):
        heimdall = Heimdall31(alpha=0.5)
        h_smooth, breached = heimdall.evaluate_text_entropy("The quick brown fox jumps over the lazy dog.")
        assert h_smooth > 0.0
        assert isinstance(breached, bool)

    def test_gravitational_mass_calculation(self):
        heimdall = Heimdall31()
        prompt = "Compute matrix decomposition and solve Kepler orbit with high precision"
        mass_meta = heimdall.calculate_gravitational_mass(prompt)
        assert "m_input" in mass_meta
        assert "i_total" in mass_meta
        assert mass_meta["token_count"] == 10
        assert mass_meta["m_input"] > 0.0
        assert mass_meta["i_total"] > 0.0
        assert mass_meta["vocabulary_density"] == 1.0

        # Empty prompt handling
        empty_meta = heimdall.calculate_gravitational_mass("")
        assert empty_meta["m_input"] == 0.0
        assert empty_meta["token_count"] == 0

    def test_token_stream_evaluation(self):
        heimdall = Heimdall31(alpha=0.8, trip_threshold=2.5)
        # Token 0: low entropy (deterministic)
        # Token 1: high entropy (16 uniform states = 4.0 bits) -> breaches threshold
        # Token 2: low entropy
        stream = [
            [0.98, 0.01, 0.01],
            [1.0 / 16.0] * 16,
            [0.99, 0.01]
        ]
        result = heimdall.evaluate_token_stream(stream)
        assert result["breached"] is True
        assert result["first_breach_index"] == 1
        assert result["tokens_processed"] == 2  # Paused at token 1


class TestPSSRCircuitBreaker:
    def test_pssr_soft_lookback(self):
        heimdall = Heimdall31(trip_threshold=2.5, max_interventions=3)
        trip_occurred, action = heimdall.evaluate_entropy_trip(is_breached=True, current_h=2.8)
        assert trip_occurred is True
        assert action == "TRIGGER_PSSR_LOOKBACK"
        assert heimdall.recovery_state == "PSSR_RECOVERY"
        assert heimdall.intervention_count == 1

        prompt = heimdall.generate_grounding_prompt("raw divergent context query")
        assert "[P-SSR DYNAMIC GROUNDING INJECTION" in prompt
        assert "Uncertainty ceiling breached" in prompt
        assert "raw divergent context query" in prompt

    def test_vasovagal_syncope_hard_halt(self):
        heimdall = Heimdall31(trip_threshold=2.5, max_interventions=2)
        # Intervention 1
        trip1, act1 = heimdall.evaluate_entropy_trip(is_breached=True, current_h=3.0)
        assert act1 == "TRIGGER_PSSR_LOOKBACK"

        # Intervention 2
        trip2, act2 = heimdall.evaluate_entropy_trip(is_breached=True, current_h=3.0)
        assert act2 == "TRIGGER_PSSR_LOOKBACK"

        # Intervention 3 exceeds max_interventions=2 -> HARD HALT
        trip3, act3 = heimdall.evaluate_entropy_trip(is_breached=True, current_h=3.0)
        assert trip3 is True
        assert act3 == "VASOVAGAL_SYNCOPE::HARD_HALT"
        assert heimdall.recovery_state == "VASOVAGAL_SYNCOPE"

    def test_intervention_cooldown_and_recovery_reset(self):
        heimdall = Heimdall31(trip_threshold=2.5, max_interventions=3)
        # Trip once
        trip1, act1 = heimdall.evaluate_entropy_trip(is_breached=True, current_h=2.8)
        assert heimdall.intervention_count == 1

        # Mark recovery complete
        heimdall.mark_recovery_complete()
        assert heimdall.recovery_state == "NOMINAL_TRACKING"
        assert heimdall.intervention_count == 0
        assert heimdall.h_smooth <= heimdall.threshold

        # Nominal step decays any remaining interventions
        trip_nom, act_nom = heimdall.evaluate_entropy_trip(is_breached=False, current_h=0.5)
        assert not trip_nom
        assert act_nom == "PROCEED"
        assert heimdall.intervention_count == 0

    def test_pssr_lookback_helper_class(self):
        lookback = PSSRLookback(max_interventions=2)
        breached, act = lookback.evaluate_entropy_trip(is_breached=True, current_h=3.0)
        assert breached is True
        assert act == "TRIGGER_PSSR_LOOKBACK"
        lookback.mark_recovery_complete()
        assert lookback.intervention_count == 0


class TestComponentHealthSurveillance:
    def test_full_system_health_optimal(self):
        cat = CheshireCatKernel()
        # Register celestial clock and bank
        clock = CelestialClockArchitecture()
        bank = FridayFortressBank()
        cat.heimdall.register_component("celestial_clock", clock)
        cat.heimdall.register_component("friday_fortress_bank", bank)

        report = cat.heimdall.check_system_health()
        assert report["heimdall_version"] == "3.1-PURPLE"
        assert report["system_health_status"] == "HEALTHY_OPTIMAL"
        assert "cheshire_cat" in report["component_diagnostics"]
        assert "cognitive_engine" in report["component_diagnostics"]
        assert "the_hoard" in report["component_diagnostics"]
        assert "rodin_protocol" in report["component_diagnostics"]
        assert "phoenix_forge" in report["component_diagnostics"]
        assert "celestial_clock" in report["component_diagnostics"]
        assert "friday_fortress_bank" in report["component_diagnostics"]
        assert "thermodynamics" in report["component_diagnostics"]

        assert report["component_diagnostics"]["cognitive_engine"]["dyad_invariant_preserved"] is True
        assert report["component_diagnostics"]["thermodynamics"]["loop_closure_sealed"] is True
        assert report["component_diagnostics"]["friday_fortress_bank"]["solvency_verified"] is True

    def test_degraded_cognitive_engine_weights(self):
        heimdall = Heimdall31()
        class MockBrokenEngine:
            analytical_weight = 0.8
            synthetic_weight = 0.8  # sum = 1.6 != 1.0
        
        report = heimdall.check_system_health({"cognitive_engine": MockBrokenEngine()})
        assert report["system_health_status"] == "DEGRADED_OR_RECOVERING"
        assert report["component_diagnostics"]["cognitive_engine"]["status"] == "UNBALANCED"

    def test_bank_margin_floor_breach(self):
        heimdall = Heimdall31()
        class MockBreachedBank:
            MARGIN_LOCK_FLOOR = 20000.0
            def verify_solvency(self, equity):
                return False
        
        report = heimdall.check_system_health({"friday_fortress_bank": MockBreachedBank()})
        assert report["system_health_status"] == "DEGRADED_OR_RECOVERING"
        assert report["component_diagnostics"]["friday_fortress_bank"]["status"] == "MARGIN_BREACHED"


@pytest.mark.asyncio
class TestCheshireCatHeimdallIntegration:
    async def test_nominal_cognitive_cycle(self):
        kernel = CheshireCatKernel()
        kernel.heimdall.reset_thermostat()
        # Normal low-entropy probabilities: almost deterministic (1.0)
        result = await kernel.process_cognitive_cycle(
            prompt="Compute matrix decomposition and solve Kepler orbit",
            token_probs=[0.99, 0.005, 0.005]
        )
        assert result["status"] == "COMMITTED_TO_HOARD"
        assert "heimdall_telemetry" in result
        assert result["heimdall_telemetry"]["is_breached"] is False
        assert result["system_health_status"] == "HEALTHY_OPTIMAL"
        assert kernel.state == "INTERACTIVE_STANDBY"
        assert "gravitational_mass" in result

    async def test_streaming_token_probs_cycle(self):
        kernel = CheshireCatKernel()
        kernel.heimdall.reset_thermostat()
        # Streaming token probabilities with safe low entropy
        stream = [
            [0.95, 0.05],
            [0.90, 0.10],
            [0.98, 0.02]
        ]
        result = await kernel.process_cognitive_cycle(
            prompt="Streaming token evaluation test",
            token_probs=stream
        )
        assert result["status"] == "COMMITTED_TO_HOARD"
        assert result["heimdall_telemetry"]["is_breached"] is False

    async def test_high_entropy_pssr_trigger_and_recovery(self):
        kernel = CheshireCatKernel()
        kernel.heimdall.reset_thermostat()
        # 16 uniform states = 4.0 bits, with alpha=0.8 will breach 2.5
        kernel.heimdall.alpha = 0.8
        high_entropy_probs = [1.0 / 16.0] * 16

        result = await kernel.process_cognitive_cycle(
            prompt="Speculative ambiguous divergent reasoning query",
            token_probs=high_entropy_probs
        )
        # Should have completed via P-SSR lookback and re-grounding
        assert result["status"] == "COMMITTED_TO_HOARD"
        assert "heimdall_telemetry" in result
        # Check event queue contains PSSR_LOOKBACK_TRIGGERED
        event_names = [ev["event"] for ev in kernel.event_queue]
        assert "PSSR_LOOKBACK_TRIGGERED" in event_names
        assert "COGNITIVE_CYCLE_COMPLETE" in event_names
        assert result["system_health_status"] == "HEALTHY_OPTIMAL"

    async def test_repeated_entropy_trips_lead_to_hard_halt(self):
        kernel = CheshireCatKernel()
        kernel.heimdall.reset_thermostat()
        kernel.heimdall.alpha = 1.0
        kernel.heimdall.max_interventions = 2
        high_entropy_probs = [1.0 / 32.0] * 32  # 5.0 bits

        # Turn 1: PSSR Soft Lookback
        res1 = await kernel.process_cognitive_cycle("divergent 1", high_entropy_probs)
        assert res1["status"] == "COMMITTED_TO_HOARD"

        # Turn 2: PSSR Soft Lookback
        # Manually keep intervention count for test
        kernel.heimdall.intervention_count = 2
        kernel.heimdall.h_smooth = 5.0

        # Turn 3: Exceeds max_interventions=2 -> Hard Halt
        res3 = await kernel.process_cognitive_cycle("divergent 3", high_entropy_probs)
        assert res3["status"] == "VASOVAGAL_SYNCOPE::HARD_HALT"
        assert "Pause generation" in res3["mandate"]
        assert kernel.state == "VASOVAGAL_SYNCOPE"


class TestFastAPIEndpoints:
    def setup_method(self):
        self.client = TestClient(app)

    def test_root_telemetry_includes_heimdall(self):
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "heimdall_telemetry" in data
        assert "Heimdall 3.1" in data["heimdall_telemetry"]["version"]

    def test_heimdall_telemetry_endpoint(self):
        response = self.client.get("/heimdall/telemetry")
        assert response.status_code == 200
        data = response.json()
        assert "h_smooth" in data
        assert "threshold" in data
        assert data["threshold"] == 2.5
        assert "last_gravitational_mass" in data

    def test_heimdall_health_endpoint(self):
        response = self.client.get("/heimdall/health")
        assert response.status_code == 200
        data = response.json()
        assert data["heimdall_version"] == "3.1-PURPLE"
        assert "system_health_status" in data
        assert "component_diagnostics" in data
        assert "celestial_clock" in data["component_diagnostics"]
        assert "friday_fortress_bank" in data["component_diagnostics"]

    def test_heimdall_evaluate_endpoint(self):
        # Evaluate low entropy
        response = self.client.post("/heimdall/evaluate", json={"probs": [0.95, 0.05]})
        assert response.status_code == 200
        data = response.json()
        assert data["is_breached"] is False
        assert data["trip_action"] == "PROCEED"

        # Evaluate text prompt (returns gravitational mass)
        response_text = self.client.post("/heimdall/evaluate", json={"prompt": "Strict mathematical prompt for Kepler orbit"})
        assert response_text.status_code == 200
        data_text = response_text.json()
        assert "h_smooth" in data_text
        assert "gravitational_mass" in data_text
        assert data_text["gravitational_mass"]["m_input"] > 0.0

    def test_heimdall_reset_endpoint(self):
        response = self.client.post("/heimdall/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "THERMOSTAT_RESET_COMPLETED"
        assert data["telemetry"]["h_smooth"] == 0.0
        assert data["telemetry"]["interventions"] == 0

    def test_cognitive_cycle_api_endpoint(self):
        response = self.client.post(
            "/cognitive/cycle",
            json={"prompt": "Validate unified spacetime kinematics"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "COGNITIVE_CYCLE_COMPLETED"
        assert "receipt" in data
        assert "heimdall_telemetry" in data
