"""
INTEGRA O/S: RODIN CLIENT AND ENDPOINT TEST SUITE (offline)

RodinClient.embed() asked for the shut-down text-embedding-004 and returned [] on any error, so the caller could not
tell a failure from an empty answer. The kernel's /rodin/* routes reported a constant "ONLINE". These tests pin the
corrected client (gemini-embedding-2, 768-d, reason kept) and routes (state from evidence, 503 on an unavailable model).

Official sources (fetched 2026-10-15):
  [E1] https://ai.google.dev/gemini-api/docs/embeddings
  [E2] https://ai.google.dev/gemini-api/docs/deprecations  (text-embedding-004 shut down 2026-01-14)
  [F1] https://fastapi.tiangolo.com/async/  (a plain `def` path operation runs in an external threadpool instead of
       blocking the server; the embedding call is blocking network I/O)
"""

import asyncio
import inspect
import threading
import time

import pytest
from fastapi.testclient import TestClient

import memory.the_hoard as hoard_module
from core.api_clients import INTEGRA_MODEL_REGISTRY, RodinClient
from memory.embedding_service import EmbeddingService, EmbeddingSpace, EmbeddingUnavailable
from memory.rodin_protocol import RodinProtocol
from memory.the_hoard import TheHoard
from orchestration.rodin_supervisor import RodinSupervisor
from tests.embedding_fakes import FakeApiError, FakeGenaiClient, ScriptedBackend

SPACE = EmbeddingSpace()


@pytest.fixture(autouse=True)
def real_clock_for_node_timestamps(monkeypatch):
    monkeypatch.setattr(hoard_module, "celestial_time", time.time)  # see tests/test_rodin_supervisor.py


# ───────────────────────── RodinClient ─────────────────────────


def test_defaults_name_the_current_embedding_model_and_size(monkeypatch):
    monkeypatch.delenv("RODIN_EMBED_MODEL", raising=False)
    monkeypatch.delenv("RODIN_EMBED_DIM", raising=False)
    client = RodinClient()
    assert client.embedding_model == "gemini-embedding-2" and client.embedding_dim == 768
    assert INTEGRA_MODEL_REGISTRY["rodin_retrieval"]["embedding_model"] == "gemini-embedding-2"


def test_env_loader_defaults_set_the_embedding_model_explicitly():
    from config.env_loader import DEFAULT_ENV_VARS

    assert DEFAULT_ENV_VARS["RODIN_EMBED_MODEL"] == "gemini-embedding-2"
    assert DEFAULT_ENV_VARS["RODIN_EMBED_DIM"] == "768"


def test_embed_sync_asks_for_768_dimensions_from_the_current_model():
    client = RodinClient()
    client.client = FakeGenaiClient()
    vec = client.embed_sync("topological manifold")
    call = client.client.calls[0]
    assert len(vec) == 768 and call["model"] == "gemini-embedding-2"
    assert call["config"].output_dimensionality == 768
    assert client.last_embed_error is None


def test_embed_sync_keeps_the_legacy_empty_list_but_records_why():
    client = RodinClient()
    client.client = FakeGenaiClient(script=[FakeApiError(404, "models/text-embedding-004 is not found")] * 3)
    assert client.embed_sync("x", model_name="text-embedding-004") == []
    assert "API_ERROR" in client.last_embed_error and "text-embedding-004" in client.last_embed_error


def test_embed_without_a_client_returns_empty_and_says_no_client():
    client = RodinClient()
    client.client = None
    assert client.embed_sync("x") == [] and "NO_CLIENT" in client.last_embed_error


def test_async_embed_works_end_to_end_against_the_fake_client():
    client = RodinClient()
    client.client = FakeGenaiClient()
    assert len(asyncio.run(client.embed("topological manifold"))) == 768


def test_async_embed_runs_the_blocking_call_off_the_event_loop_thread():
    client = RodinClient()
    seen = {}

    def fake_embed_sync(text, model_name=None):
        seen["thread"] = threading.get_ident()
        return [0.0] * 768

    client.embed_sync = fake_embed_sync

    async def run():
        loop_thread = threading.get_ident()
        await client.embed("x")
        return loop_thread

    loop_thread = asyncio.run(run())
    assert seen["thread"] != loop_thread


# ───────────────────────── /rodin/* routes ─────────────────────────


@pytest.fixture()
def wired(tmp_path, monkeypatch):
    """main.app with a hermetic supervisor: temp Hoard, scripted embedder, spy Alexandria."""
    import main

    backend = ScriptedBackend()
    svc = EmbeddingService(backend, SPACE)
    hoard = TheHoard(base_dir=str(tmp_path), embedder=svc)
    hoard.commit_node_v2(payload={"text": "sun breathing thirteenth form loop closure"}, spacetime_anchor={"t": 1},
                         ccid="N_SUN", outcome_label=1.0)
    hoard.embed_pending(dry_run=False)

    class Spy:
        threshold = 0.95
        calls = []

        def execute_loop_2_learning(self, query):
            self.calls.append(query)
            return {"status": "ALEXANDRIA_LEARNING_COMPLETE"}

    spy = Spy()
    spy.calls = []
    sup = RodinSupervisor(RodinProtocol(hoard=hoard, embedder=svc), alexandria=spy)
    monkeypatch.setattr(main, "rodin_supervisor", sup)
    return TestClient(main.app), sup, backend, spy


def test_query_route_is_a_plain_def_so_fastapi_runs_it_in_a_threadpool():
    import main

    route = next(r for r in main.app.routes if getattr(r, "path", None) == "/rodin/query")
    assert not inspect.iscoroutinefunction(route.endpoint)


def test_query_route_returns_evidence_on_a_pass(wired):
    client, _, _, spy = wired
    r = client.post("/rodin/query", json={"prompt": "sun breathing thirteenth form loop closure"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "RODIN_CONDUCTOR_COMPLETE"
    out = body["swarm_state"]["rodin_output"]
    assert out["decision"] == "PASS" and out["neighbors"][0]["ccid"] == "N_SUN"
    assert "embedding" not in out["neighbors"][0]                    # no vectors in the response
    assert "payload_preview" in out["neighbors"][0]
    assert "No worker agent ran" in body["swarm_state"]["output"]
    assert spy.calls == []


def test_query_route_is_503_when_the_model_is_unavailable(wired):
    client, _, backend, spy = wired
    backend._errors.append(EmbeddingUnavailable("API_ERROR", "503 unavailable"))
    r = client.post("/rodin/query", json={"prompt": "a prompt the cache has not seen"})
    assert r.status_code == 503
    body = r.json()
    assert body["status"] == "RODIN_CONDUCTOR_ERROR"
    assert body["swarm_state"]["rodin_output"]["decision"] == "ERROR"
    assert spy.calls == []


def test_telemetry_keeps_the_dashboard_fields_and_adds_evidence(wired):
    client, sup, _, _ = wired
    body = client.get("/rodin/telemetry").json()
    for key in ("knn_k", "gate_iii_tau", "gaussian_sigma", "stale_threshold_s", "coarse_floor",
                "alexandria_threshold", "registered_agents"):
        assert key in body                                            # the fields static/dashboard.html reads
    assert body["embedder_state"] in {"UNPROVEN", "READY"} and body["embedding"]["space"] == SPACE.id
    assert body["coarse_dim"] == 128 and body["fine_dim"] == 768
    assert body["hoard"]["active_space"] == SPACE.id and body["hoard"]["embedded_nodes"] == 1


def test_telemetry_status_turns_from_online_to_degraded_after_a_failed_embedding(wired):
    client, sup, backend, _ = wired
    assert client.get("/rodin/telemetry").json()["status"] == "ONLINE"
    backend._errors.append(EmbeddingUnavailable("API_ERROR", "503 unavailable"))
    client.post("/rodin/query", json={"prompt": "another prompt the cache has not seen"})
    body = client.get("/rodin/telemetry").json()
    assert body["status"] == "DEGRADED" and body["embedder_state"] == "DEGRADED"
    assert body["embedding"]["last_error"]["code"] == "API_ERROR"
