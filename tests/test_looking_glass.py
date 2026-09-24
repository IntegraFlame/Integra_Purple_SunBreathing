"""
Unit Test Suite for Looking Glass Protocol & Cheshire Cat Protocol
Testing:
- C_235 Directional Lock & Tilt Dynamics
- Rodin Decision Tree Outcomes (1-5)
- Structural Saturation (psi = 200 MPa)
- Kintsugi Anomaly (|Z| > 3.0) & Mirror Maze Sandbox
- Cheshire Cat Protocol Sovereign Conduit & Functions
- FastAPI Endpoints
"""

import pytest
from fastapi.testclient import TestClient

from sensory.cheshire_protocol import CheshireCatProtocol
from sensory.looking_glass import LookingGlassProtocol
from sensory.cheshire_cat import CheshireCatKernel
from main import app


@pytest.fixture
def cheshire_protocol():
    return CheshireCatProtocol()


@pytest.fixture
def looking_glass(cheshire_protocol):
    return LookingGlassProtocol(cheshire_protocol)


@pytest.fixture
def test_client():
    return TestClient(app)


class TestCheshireCatProtocolSovereignFunctions:
    def test_track_conversation_topic(self, cheshire_protocol):
        res = cheshire_protocol.track_conversation_topic("Quantum Celestial Topology", {"priority": "HIGH"})
        assert res["topic"] == "Quantum Celestial Topology"
        assert res["status"] == "TRACKED"
        assert len(cheshire_protocol.conversation_topics) == 1

    def test_detect_paradox_or_missing_data(self, cheshire_protocol):
        res_paradox = cheshire_protocol.detect_paradox_or_missing_data("This statement is an impossible paradox.")
        assert res_paradox["has_paradox"] is True
        assert len(cheshire_protocol.detected_paradoxes) == 1

        res_nominal = cheshire_protocol.detect_paradox_or_missing_data("Calculated orbital trajectory.", ["Context1"])
        assert res_nominal["has_paradox"] is False
        assert res_nominal["missing_data_point"] is False

    def test_create_abstract_long_connections(self, cheshire_protocol):
        conn = cheshire_protocol.create_abstract_long_connections("Thermodynamic Heat Engines", "Financial Liquidity Flows")
        assert "Isomorphism" in conn["bridge_concept"]
        assert conn["salience_score"] > 0.8
        assert len(cheshire_protocol.abstract_connections) == 1


class TestLookingGlassTiltDynamics:
    def test_zero_entropy_zero_tilt(self, looking_glass):
        tilt = looking_glass.calculate_perspective_tilt(h_smooth=0.0, z_score=0.0)
        assert tilt == 0.0

    def test_high_entropy_perspective_tilt(self, looking_glass):
        tilt = looking_glass.calculate_perspective_tilt(h_smooth=2.5, z_score=0.0)
        assert tilt > 15.0
        assert tilt <= 23.5

    def test_max_tilt_reaches_c235_lock(self, looking_glass):
        tilt = looking_glass.calculate_perspective_tilt(h_smooth=3.0, z_score=3.5)
        assert tilt == 23.5


class TestRodinThresholdOutcomes:
    def test_outcome_clarification_ambiguous(self, looking_glass):
        outcome, details = looking_glass.evaluate_rodin_metrics(
            route_count=9,  # > AMBIGUOUS_THRESHOLD
            cohesion=0.8,
            semantic_relevance=0.8,
            is_stale=False
        )
        assert outcome == "REQUEST_CLARIFICATION_AMBIGUOUS"
        assert details["route_count"] == 9

    def test_outcome_clarification_insufficient(self, looking_glass):
        outcome, details = looking_glass.evaluate_rodin_metrics(
            route_count=0,
            cohesion=0.0,
            semantic_relevance=0.2,
            is_stale=False,
            intent_confidence=0.2
        )
        assert outcome == "REQUEST_CLARIFICATION_INSUFFICIENT"

    def test_outcome_alexandria_verify(self, looking_glass):
        outcome, details = looking_glass.evaluate_rodin_metrics(
            route_count=3,
            cohesion=0.7,
            semantic_relevance=0.75,
            is_stale=True  # Stale data
        )
        assert outcome == "ALEXANDRIA_VERIFY"

    def test_outcome_alexandria_guided_search(self, looking_glass):
        outcome, details = looking_glass.evaluate_rodin_metrics(
            route_count=0,
            cohesion=0.0,
            semantic_relevance=0.3,
            is_stale=False,
            intent_confidence=0.9,  # High intent confidence
            inferred_topic="DeFi Yield Farming"
        )
        assert outcome == "ALEXANDRIA_GUIDED_SEARCH"
        assert details["inferred_topic"] == "DeFi Yield Farming"

    def test_outcome_conversational_continuation(self, looking_glass):
        outcome, details = looking_glass.evaluate_rodin_metrics(
            route_count=2,
            cohesion=0.8,
            semantic_relevance=0.92,
            is_stale=False,
            prompt_type="STATEMENT"
        )
        assert outcome == "OUTCOME_CONTINUATION"

    def test_outcome_indirect_connection(self, looking_glass):
        outcome, details = looking_glass.evaluate_rodin_metrics(
            route_count=2,
            cohesion=0.8,
            semantic_relevance=0.25,  # Low relevance
            is_stale=False,
            prompt_type="QUESTION"
        )
        assert outcome == "INDIRECT_CONNECTION"

    def test_outcome_direct_synthesis_nominal(self, looking_glass):
        outcome, details = looking_glass.evaluate_rodin_metrics(
            route_count=2,
            cohesion=0.8,
            semantic_relevance=0.75,
            is_stale=False,
            prompt_type="QUESTION"
        )
        assert outcome == "OUTCOME_DIRECT_SYNTHESIS"


class TestLookingGlassStructuralBoundaries:
    def test_heaviside_skeletal_boundary_halt(self, looking_glass):
        res = looking_glass.evaluate_supervisory_state(
            prompt="High compression payload",
            h_smooth=1.0,
            token_stress_mpa=205.0  # > 200.0 MPa Limit
        )
        assert res["supervisory_action"] == "HEAVISIDE_BOUNDARY_HALT"
        assert res["status"] == "HALTED_UNCOMPRESSED_SERIALIZATION"

    def test_kintsugi_mirror_maze_isolation(self, looking_glass):
        res = looking_glass.evaluate_supervisory_state(
            prompt="Aberrant outlier metric",
            h_smooth=1.0,
            z_score=3.8  # |Z| > 3.0
        )
        assert res["supervisory_action"] == "MIRROR_MAZE_ISOLATION"
        assert res["status"] == "SANDBOXED_FOR_PHOENIX_SMELTING"
        assert len(looking_glass.mirror_maze_sandbox) == 1
        assert "MIRROR_MAZE_SANDBOX" in res["conduit"]["event_type"]


class TestFastAPILookingGlassEndpoints:
    def test_get_looking_glass_status(self, test_client):
        resp = test_client.get("/looking-glass/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "LOOKING_GLASS_ONLINE"
        assert data["c_235_directional_lock_deg"] == 23.5

    def test_post_looking_glass_evaluate(self, test_client):
        payload = {
            "prompt": "Evaluate market liquidity",
            "h_smooth": 1.2,
            "route_count": 2,
            "cohesion": 0.8,
            "semantic_relevance": 0.85
        }
        resp = test_client.post("/looking-glass/evaluate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["supervisory_action"] == "OUTCOME_DIRECT_SYNTHESIS"
        assert "cheshire_conduit" in data

    def test_post_looking_glass_unlock(self, test_client):
        resp = test_client.post("/looking-glass/unlock")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "SUCCESS"
        assert data["action"] == "LOOKING_GLASS_UNLOCKED"
        assert data["receipt"]["unlocked"] is True
        assert data["receipt"]["status"] == "UNLOCKED_SOVEREIGN_MODE"
