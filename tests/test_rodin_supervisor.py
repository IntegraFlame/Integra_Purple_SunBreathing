"""
INTEGRA O/S: RODIN SUPERVISOR TEST SUITE (offline)

Before this change dispatch() evaluated Gate III on a constant vector ([0.1] * 768) against an empty candidate
list, so every call HALTed and sent the prompt to the Alexandria research loop. These tests pin the replacement:
the real prompt is embedded, candidates come from the Hoard in the query's space, an embedding failure is an
ERROR (not a HALT, and never a research trip), and a PASS returns evidence without claiming that an agent ran.
"""

import inspect
import time

import pytest

import memory.the_hoard as hoard_module
import orchestration.rodin_supervisor as supervisor_module
from memory.embedding_service import EmbeddingService, EmbeddingSpace, EmbeddingUnavailable
from memory.rodin_protocol import RodinProtocol
from memory.the_hoard import TheHoard
from orchestration.rodin_supervisor import RodinSupervisor
from tests.embedding_fakes import ScriptedBackend, bow_vector

SPACE = EmbeddingSpace()
ANCHOR = {"t": 1}


@pytest.fixture(autouse=True)
def real_clock_for_node_timestamps(monkeypatch):
    """
    Node timestamps come from the frozen celestial_time() (ADR-001), which runs about 7 to 9 days behind the clock
    that RodinProtocol.check_staleness() uses, so a node made now would already look stale. These tests are about
    the supervisor, not the clock, so they stamp nodes with real time. The clock defect is measured in the report.
    """
    monkeypatch.setattr(hoard_module, "celestial_time", time.time)


class SpyAlexandria:
    threshold = 0.95

    def __init__(self):
        self.calls = []

    def execute_loop_2_learning(self, query):
        self.calls.append(query)
        return {"status": "ALEXANDRIA_LEARNING_COMPLETE", "query": query}


def build(tmp_path, backend=None, texts=None):
    backend = backend or ScriptedBackend()
    svc = EmbeddingService(backend, SPACE)
    hoard = TheHoard(base_dir=str(tmp_path), embedder=svc)
    for ccid, text in (texts or {"N_SUN": "sun breathing thirteenth form loop closure",
                                 "N_FLAME": "cheshire cat flame kernel thirty hertz loop"}).items():
        hoard.commit_node_v2(payload={"text": text}, spacetime_anchor=ANCHOR, ccid=ccid, outcome_label=1.0)
    hoard.embed_pending(dry_run=False)
    spy = SpyAlexandria()
    sup = RodinSupervisor(RodinProtocol(hoard=hoard, embedder=svc), alexandria=spy)
    return sup, spy, backend, hoard


def test_no_mock_vector_is_left_in_the_supervisor():
    source = inspect.getsource(supervisor_module)
    assert "[0.1] * 768" not in source and "mock_query_vec" not in source


def test_initialize_state_is_unchanged():
    state = RodinSupervisor(RodinProtocol(embedder=EmbeddingService(ScriptedBackend(), SPACE))).initialize_state("p")
    assert set(state) == {"input", "chat_history", "intermediate_steps", "rodin_output", "output", "spacetime_payload"}
    assert state["spacetime_payload"]["causal_proof"] == []


def test_dispatch_embeds_the_real_prompt(tmp_path):
    sup, _, backend, _ = build(tmp_path)
    sup.dispatch(sup.initialize_state("sun breathing thirteenth form loop closure"))
    assert backend.calls[-1]["texts"] == ["task: search result | query: sun breathing thirteenth form loop closure"]


def test_pass_returns_the_neighbours_and_does_not_claim_an_agent_ran(tmp_path):
    sup, spy, _, _ = build(tmp_path)
    state = sup.dispatch(sup.initialize_state("sun breathing thirteenth form loop closure"))
    out = state["rodin_output"]
    assert out["decision"] == "PASS" and out["embedding_space"] == SPACE.id
    step = state["intermediate_steps"][0]
    assert step["action"] == "GATE_III_PASS" and step["worker_dispatch"] == "NOT_IMPLEMENTED"
    assert "N_SUN" in step["neighbors"]
    assert "No worker agent ran" in state["output"] and "successfully executed" not in state["output"]
    assert spy.calls == []
    assert state["spacetime_payload"]["causal_proof"] == ["RODIN_GATE_III_EVALUATED", "GATE_III_PASS_RETRIEVAL_ONLY"]


def test_low_density_halts_and_only_then_calls_alexandria(tmp_path):
    sup, spy, _, _ = build(tmp_path)
    state = sup.dispatch(sup.initialize_state("completely unrelated question about gardening tomatoes"))
    assert state["rodin_output"]["decision"] == "HALT"
    assert spy.calls == ["completely unrelated question about gardening tomatoes"]
    assert state["output"].startswith("Rodin halted execution. Alexandria Protocol engaged.")
    assert state["intermediate_steps"][0]["action"] == "TRIGGER_ALEXANDRIA_PROTOCOL"
    assert "ALEXANDRIA_FALLBACK_TRIGGERED" in state["spacetime_payload"]["causal_proof"]


def test_an_embedding_failure_is_an_error_and_never_a_research_trip(tmp_path):
    sup, spy, backend, _ = build(tmp_path)
    backend._errors.append(EmbeddingUnavailable("API_ERROR", "503 unavailable"))
    state = sup.dispatch(sup.initialize_state("a prompt the cache has not seen"))
    out = state["rodin_output"]
    assert out["decision"] == "ERROR" and out["error"] == {"code": "API_ERROR", "detail": "503 unavailable"}
    assert spy.calls == []
    assert "embedding unavailable" in state["output"].lower() and "Alexandria was not triggered" in state["output"]
    assert state["intermediate_steps"][0]["action"] == "EMBEDDING_UNAVAILABLE"
    assert state["spacetime_payload"]["causal_proof"] == ["RODIN_EMBEDDING_UNAVAILABLE"]


def test_neighbours_in_the_state_carry_no_vectors_and_only_a_short_payload_preview(tmp_path):
    sup, _, _, hoard = build(tmp_path, texts={"BIG": "sun breathing thirteenth form " + "x" * 5000})
    state = sup.dispatch(sup.initialize_state("sun breathing thirteenth form"))
    n = state["rodin_output"]["neighbors"][0]
    assert n["ccid"] == "BIG" and "embedding" not in n and "payload" not in n
    assert 0 < len(n["payload_preview"]) <= 500 + 3


def test_candidates_are_the_hoards_nodes_in_the_query_space_only(tmp_path):
    sup, _, _, hoard = build(tmp_path)
    # an untagged vector that is a perfect match for the query: it must be ignored
    hoard.commit_node_v2(payload={"text": "x"}, spacetime_anchor=ANCHOR, ccid="UNTAGGED", outcome_label=1.0,
                         embedding_768d=bow_vector("sun breathing thirteenth form loop closure"))
    state = sup.dispatch(sup.initialize_state("sun breathing thirteenth form loop closure"))
    ids = [n["ccid"] for n in state["rodin_output"]["neighbors"]]
    assert "UNTAGGED" not in ids and "N_SUN" in ids
    assert state["rodin_output"]["candidates_total"] == 2  # filtered to the space before the review


def test_a_node_made_now_is_not_stale(tmp_path, monkeypatch):
    """ADR-001 regression (applied 2026-10-15): the real celestial_time() is the system clock, so a fresh node is fresh."""
    from core.celestial_middleware import celestial_time

    monkeypatch.setattr(hoard_module, "celestial_time", celestial_time)  # undo the fixture: use the real clock
    sup, _, _, _ = build(tmp_path)
    state = sup.dispatch(sup.initialize_state("sun breathing thirteenth form loop closure"))
    assert state["rodin_output"]["is_stale"] is False


def test_gate_iii_sees_indexed_chunks_that_are_not_in_the_in_memory_cache(tmp_path):
    """The 12th Step lobes put thousands of chunks in the index only; Gate III must be able to see them."""
    from memory.the_hoard import HoardNode

    sup, spy, _, hoard = build(tmp_path)
    text = "gardening tomatoes watering schedule for raised beds"
    vec = sup.rodin.generate_query_vector(text)
    chunk = HoardNode(ccid="LOBE_CHUNK", payload={"text": text}, spacetime_anchor={"t": 1}, embedding_768d=vec,
                      outcome_label=1.0, created_at=time.time(), embed_space=SPACE.id)
    assert hoard.chroma_upsert_many([(chunk, text)]) == 1
    assert "LOBE_CHUNK" not in [n.ccid for n in hoard.local_sparse_cache]

    state = sup.dispatch(sup.initialize_state(text))
    assert state["rodin_output"]["decision"] == "PASS" and state["rodin_output"]["candidate_source"] == "INDEX"
    assert "LOBE_CHUNK" in state["intermediate_steps"][0]["neighbors"] and spy.calls == []


def test_gate_iii_falls_back_to_the_cache_and_says_so_when_the_index_is_unavailable(tmp_path):
    sup, spy, _, hoard = build(tmp_path)
    hoard._chroma_collection = None
    state = sup.dispatch(sup.initialize_state("sun breathing thirteenth form loop closure"))
    assert state["rodin_output"]["candidate_source"] == "CACHE" and state["rodin_output"]["decision"] == "PASS"


def test_gate_iii_reports_an_index_error_and_uses_the_cache(tmp_path):
    sup, _, _, hoard = build(tmp_path)

    def boom(*a, **k):
        raise RuntimeError("ChromaDB query failed: index corrupt")

    hoard.chroma_candidates = boom
    state = sup.dispatch(sup.initialize_state("sun breathing thirteenth form loop closure"))
    out = state["rodin_output"]
    assert out["candidate_source"] == "CACHE" and "index corrupt" in out["candidate_source_note"]


def test_caller_supplied_candidates_are_used_as_given():
    svc = EmbeddingService(ScriptedBackend(), SPACE)
    sup = RodinSupervisor(RodinProtocol(embedder=svc), alexandria=SpyAlexandria())
    cand = [{"ccid": "C1", "embedding": bow_vector("sun breathing form"), "embed_space": SPACE.id,
             "outcome_label": 1.0, "created_at": 9e9}]
    state = sup.dispatch(sup.initialize_state("sun breathing form"), candidate_nodes=cand)
    assert state["rodin_output"]["decision"] == "PASS" and state["rodin_output"]["k_neighbors_found"] == 1


def test_without_a_hoard_or_candidates_the_gate_halts_with_zero_density():
    svc = EmbeddingService(ScriptedBackend(), SPACE)
    spy = SpyAlexandria()
    sup = RodinSupervisor(RodinProtocol(embedder=svc), alexandria=spy)
    state = sup.dispatch(sup.initialize_state("anything"))
    assert state["rodin_output"]["m_knn"] == 0.0 and state["rodin_output"]["decision"] == "HALT"
    assert spy.calls == ["anything"]
