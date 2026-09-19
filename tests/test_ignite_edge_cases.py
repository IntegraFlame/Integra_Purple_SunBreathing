from fastapi.testclient import TestClient
from main import app, dragon_engine

client = TestClient(app)

def test_ignite_halt_and_reground():
    # To force a breach, we need high entropy.
    # The default threshold is 2.5. We can send a prompt with all unique characters to maximize entropy.
    # A string with many unique characters:
    prompt = "".join(chr(i) for i in range(32, 127)) * 10
    
    # We might need to mock or just send it directly if Heimdall works reliably
    # But Heimdall uses EMA (alpha = 0.3). We might need to send a few requests to raise h_smooth.
    # Instead of fighting EMA, let's just mock the assessment.
    
    original_process = dragon_engine.process_intention
    
    def mock_process_intention(prompt, token_probs=None):
        return {
            "action_decision": "HALT_AND_REGROUND",
            "metacognitive_assessment": {
                "knowledge_boundary_breached": True,
                "confidence_calibration": 0.4,
                "gravitational_mass": 0.0,
                "entropy": 3.0,
                "trip_action": "TRIGGER_PSSR_LOOKBACK"
            },
            "engine_state": "ACTIVE_WAKING_STATE"
        }
        
    dragon_engine.process_intention = mock_process_intention
    try:
        response = client.post("/ignite", json={"prompt": "test"})
        assert response.status_code == 200
        data = response.json()
        assert data["state"] == "HALT_AND_REGROUND"
        assert "Execution halted" in data["response"]
        assert "execution_meta" not in data # Ensure we didn't execute
    finally:
        dragon_engine.process_intention = original_process

def test_ignite_request_clarification():
    original_process = dragon_engine.process_intention
    
    def mock_process_intention(prompt, token_probs=None):
        return {
            "action_decision": "REQUEST_CLARIFICATION",
            "metacognitive_assessment": {
                "knowledge_boundary_breached": False,
                "confidence_calibration": 0.4,
                "gravitational_mass": 0.0,
                "entropy": 2.0,
                "trip_action": "PROCEED"
            },
            "engine_state": "ACTIVE_WAKING_STATE"
        }
        
    dragon_engine.process_intention = mock_process_intention
    try:
        response = client.post("/ignite", json={"prompt": "test"})
        assert response.status_code == 200
        data = response.json()
        assert data["state"] == "REQUEST_CLARIFICATION"
        assert "Execution paused" in data["response"]
        assert "execution_meta" not in data # Ensure we didn't execute
    finally:
        dragon_engine.process_intention = original_process
