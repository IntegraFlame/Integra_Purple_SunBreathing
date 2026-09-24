from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root_contains_purple_modality():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "purple_modality" in data
    assert data["delta_e_cycle"] <= 0.001
    assert data["mechanical_latency_s"] >= 0.0
    assert data["purple_modality"]["status"] == "PURPLE_MODALITY_REGISTERED"
    assert "antigravity_harness" in data
    assert data["antigravity_harness"]["status"] == "HARDENED_OPERATIONAL"

def test_ignite_engine_contains_constraints():
    response = client.post("/ignite", json={"prompt": "Test Prompt"})
    assert response.status_code == 200
    data = response.json()
    assert "delta_e_cycle" in data
    assert "mechanical_latency_s" in data
    assert data["delta_e_cycle"] <= 0.001
    assert data["mechanical_latency_s"] >= 0.0

def test_antigravity_harness_endpoints():
    tel_res = client.get("/antigravity/telemetry")
    assert tel_res.status_code == 200
    tel_data = tel_res.json()
    assert tel_data["status"] == "HARDENED_OPERATIONAL"
    assert "active_mcp_servers" in tel_data

    health_res = client.get("/antigravity/health")
    assert health_res.status_code == 200
    health_data = health_res.json()
    assert health_data["status"] == "HEALTHY"
