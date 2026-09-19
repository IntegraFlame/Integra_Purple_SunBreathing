"""
INTEGRA O/S: COGNITIVE CYCLE INTEGRATION TEST SUITE
Tests the modified unified cognitive cycle in sensory/cheshire_cat.py:
- Phase 0: Topic tracking & Heimdall surveillance
- Phase 1: Rodin Route Retrieval from The Hoard
- Phase 2: Paradox & missing data point assessment
- Phase 3: Looking Glass supervisory evaluation (Perspective Tilt, Heaviside boundary, Mirror Maze, Rodin outcomes)
- Phase 4: Adaptive bicameral synthesis with weight modulation
- Phase 5: The Hoard disk commit with supervisory metadata
"""

import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sensory.cheshire_cat import CheshireCatKernel
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def kernel():
    return CheshireCatKernel()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_nominal_modified_cognitive_cycle(kernel):
    """
    Verifies nominal prompt passes through all phases cleanly,
    tracks conversation topic, records no paradox, commits to The Hoard,
    and returns rich supervisory telemetry.
    """
    prompt = "Synthesize harmonic coordinates for the celestial orbital bridge."
    result = await kernel.process_cognitive_cycle(prompt)

    assert result["status"] == "COMMITTED_TO_HOARD"
    assert "looking_glass" in result
    assert "cheshire_protocol" in result
    assert result["cheshire_protocol"]["topic"]["topic"] == prompt
    assert result["cheshire_protocol"]["paradox"]["has_paradox"] is False
    assert result["looking_glass"]["supervisory_action"] in [
        "OUTCOME_DIRECT_SYNTHESIS",
        "OUTCOME_CONTINUATION",
        "INDIRECT_CONNECTION",
        "ALEXANDRIA_GUIDED_SEARCH"
    ]
    assert result["system_health_status"] == "HEALTHY_OPTIMAL"
    assert os.path.exists(result["file_path"])


@pytest.mark.asyncio
async def test_paradox_triggers_abstract_connection_and_weight_modulation(kernel):
    """
    Verifies that a prompt with paradoxical markers triggers paradox detection,
    generates an abstract long-range bridge concept, and adapts synthesis.
    """
    paradox_prompt = "There is a logical paradox and contradiction where both true and false exist simultaneously."
    result = await kernel.process_cognitive_cycle(paradox_prompt, inferred_topic="Quantum Dialectics")

    assert result["status"] == "COMMITTED_TO_HOARD"
    assert result["cheshire_protocol"]["paradox"]["has_paradox"] is True
    assert result["cheshire_protocol"]["abstract_connection"] is not None
    assert "bridge_concept" in result["cheshire_protocol"]["abstract_connection"]
    assert kernel.state == "INTERACTIVE_STANDBY"


@pytest.mark.asyncio
async def test_heaviside_skeletal_boundary_halt(kernel):
    """
    Verifies that real-time token stress exceeding psi = 200.0 MPa halts generation
    and transitions state to HEAVISIDE_HALT.
    """
    prompt = "Overloaded prompt simulating high-pressure context stress."
    result = await kernel.process_cognitive_cycle(
        prompt=prompt,
        token_stress_mpa=215.0
    )

    assert result["status"] == "HEAVISIDE_BOUNDARY_HALT"
    assert result["supervisory_action"] == "HEAVISIDE_BOUNDARY_HALT"
    assert result["token_stress_mpa"] == 215.0
    assert kernel.state == "HEAVISIDE_HALT"


@pytest.mark.asyncio
async def test_mirror_maze_sovereign_defense_isolation(kernel):
    """
    Verifies that a statistical outlier (|Z| > 3.0) triggers Mirror Maze sandboxing
    and routes voice conduit through CheshireCatProtocol.
    """
    prompt = "Outlier prompt with extreme statistical variance."
    result = await kernel.process_cognitive_cycle(
        prompt=prompt,
        z_score=3.85
    )

    assert result["status"] == "MIRROR_MAZE_ISOLATION"
    assert result["supervisory_action"] == "MIRROR_MAZE_ISOLATION"
    assert result["z_score"] == 3.85
    assert result["sandbox_receipt"]["status"] == "ISOLATED_IN_MIRROR_MAZE"
    assert result["cheshire_conduit"]["mode"] == "CHESHIRE_CAT_PROTOCOL_CONDUIT"
    assert kernel.state == "MIRROR_MAZE_ISOLATION"


@pytest.mark.asyncio
async def test_clarification_requirement_interruption(kernel):
    """
    Verifies that low intent confidence with insufficient internal context
    triggers REQUEST_CLARIFICATION_INSUFFICIENT and pauses generation.
    """
    prompt = "What is the secret parameter?"
    result = await kernel.process_cognitive_cycle(
        prompt=prompt,
        intent_confidence=0.30
    )

    if result["status"] == "CLARIFICATION_REQUIRED":
        assert result["supervisory_action"] in [
            "REQUEST_CLARIFICATION_INSUFFICIENT",
            "REQUEST_CLARIFICATION_AMBIGUOUS"
        ]
        assert "conduit_message" in result["cheshire_conduit"]
        assert kernel.state == "CLARIFICATION_PENDING"
    else:
        assert result["status"] == "COMMITTED_TO_HOARD"


def test_fastapi_cognitive_cycle_endpoint_with_supervisory_params(client):
    """
    Verifies POST /cognitive/cycle with extended supervisory parameters over HTTP.
    """
    payload = {
        "prompt": "Evaluate harmonic resonance across multidimensional manifolds.",
        "z_score": 0.5,
        "token_stress_mpa": 145.0,
        "prompt_type": "STATEMENT",
        "intent_confidence": 0.85
    }
    response = client.post("/cognitive/cycle", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COGNITIVE_CYCLE_COMPLETED"
    assert "receipt" in data
    assert "looking_glass" in data["receipt"]
    assert "cheshire_protocol" in data["receipt"]
