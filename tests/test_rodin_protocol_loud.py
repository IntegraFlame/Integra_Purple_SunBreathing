"""
INTEGRA O/S: RODIN PROTOCOL TEST SUITE, LOUD FAILURES (offline)

Before this change generate_query_vector() swallowed every error and returned a SHA-256 pseudo-vector that
looked like an embedding. These tests pin the replacement: the model's vector, or EmbeddingUnavailable, and a
retrieval result that says when it is degraded and why.
"""

import inspect

import pytest

import memory.rodin_protocol as rodin_module
from memory.embedding_service import EmbeddingService, EmbeddingSpace, EmbeddingUnavailable
from memory.rodin_protocol import RodinProtocol
from memory.the_hoard import TheHoard
from tests.embedding_fakes import ScriptedBackend, bow_vector

SPACE = EmbeddingSpace()
ANCHOR = {"t": 1}

DOCS = {
    "N_SUN": "sun breathing thirteenth form loop closure",
    "N_FLAME": "cheshire cat flame kernel thirty hertz loop",
    "N_BAKER": "baker louisiana celestial anchor coordinates",
}


def build(tmp_path, backend=None, embed=True):
    backend = backend or ScriptedBackend()
    svc = EmbeddingService(backend, SPACE)
    hoard = TheHoard(base_dir=str(tmp_path), embedder=svc)
    for ccid, text in DOCS.items():
        hoard.commit_node_v2(payload={"text": text}, spacetime_anchor=ANCHOR, ccid=ccid, outcome_label=1.0)
    if embed:
        hoard.embed_pending(dry_run=False)
    return RodinProtocol(hoard=hoard, embedder=svc), hoard, svc, backend


# ───────────────────────── the query vector ─────────────────────────


def test_query_vector_is_the_models_vector(tmp_path):
    rodin, _, _, _ = build(tmp_path)
    assert rodin.generate_query_vector("hello world") == bow_vector("hello world")


def test_query_vector_raises_when_the_embedder_fails_instead_of_returning_a_hash(tmp_path):
    rodin, _, svc, backend = build(tmp_path)
    backend._errors.append(EmbeddingUnavailable("API_ERROR", "404 model not found"))
    with pytest.raises(EmbeddingUnavailable) as exc:
        rodin.generate_query_vector("a query the cache has not seen")
    assert exc.value.code == "API_ERROR"


def test_no_hash_fallback_is_left_in_the_module():
    source = inspect.getsource(rodin_module)
    assert "hashlib" not in source and "sha256" not in source.lower()


def test_coarse_tier_defaults_to_the_documented_minimum_dimension_and_stays_configurable():
    assert RodinProtocol().coarse_dim == 128 and RodinProtocol().fine_dim == 768
    assert RodinProtocol(mrl_dimensions=(64, 768)).coarse_dim == 64


def test_query_dimension_must_match_the_fine_tier(tmp_path):
    svc = EmbeddingService(ScriptedBackend(), SPACE)
    rodin = RodinProtocol(mrl_dimensions=(128, 512), embedder=svc)
    with pytest.raises(EmbeddingUnavailable) as exc:
        rodin.generate_query_embedding("x")
    assert exc.value.code == "BAD_DIMENSION"


# ───────────────────────── route_retrieval ─────────────────────────


def test_route_retrieval_finds_the_relevant_node_through_chroma(tmp_path):
    rodin, hoard, _, _ = build(tmp_path)
    out = rodin.route_retrieval("what is the thirteenth form of sun breathing")
    assert out["retrieval_method"] == "MRL_COSINE_KNN_CHROMA"
    assert out["degraded"] is False and out["fallback_reason"] is None and out["embed_error"] is None
    assert out["embedding_space"] == SPACE.id
    assert out["retrieved_paths"][0]["ccid"] == "N_SUN"
    assert out["index_rows"] == 3


def test_route_retrieval_says_so_when_embedding_fails_and_falls_back_to_substring(tmp_path):
    rodin, _, _, backend = build(tmp_path)
    backend._errors.append(EmbeddingUnavailable("API_ERROR", "503 unavailable"))
    out = rodin.route_retrieval("cheshire")
    assert out["degraded"] is True
    assert out["fallback_reason"] == "EMBEDDING_UNAVAILABLE:API_ERROR"
    assert out["embed_error"] == {"code": "API_ERROR", "detail": "503 unavailable"}
    assert out["retrieval_method"] == "HOARD_SUBSTRING_FALLBACK" and out["candidate_count"] == 1


def test_route_retrieval_is_degraded_when_chroma_is_unavailable(tmp_path):
    rodin, hoard, _, _ = build(tmp_path)
    hoard._chroma_collection = None
    out = rodin.route_retrieval("baker")
    assert out["degraded"] is True and out["fallback_reason"] == "VECTOR_SEARCH_UNAVAILABLE"
    assert out["retrieval_method"] == "HOARD_SUBSTRING_FALLBACK"


def test_route_retrieval_reports_a_vector_search_error_instead_of_hiding_it(tmp_path):
    rodin, hoard, _, _ = build(tmp_path)

    def boom(*a, **k):
        raise RuntimeError("ChromaDB query failed: index corrupt")

    hoard.chroma_query = boom
    out = rodin.route_retrieval("baker")
    assert out["degraded"] is True and out["fallback_reason"].startswith("VECTOR_SEARCH_ERROR:RuntimeError")


def test_route_retrieval_with_nothing_embedded_yet_is_not_degraded_but_says_so(tmp_path):
    rodin, hoard, _, _ = build(tmp_path, embed=False)
    out = rodin.route_retrieval("cheshire")
    assert out["degraded"] is False and out["fallback_reason"] == "NO_VECTOR_MATCH"
    assert out["index_rows"] == 0 and out["retrieval_method"] == "HOARD_SUBSTRING_FALLBACK"


def test_route_retrieval_without_a_hoard():
    out = RodinProtocol(embedder=EmbeddingService(ScriptedBackend(), SPACE)).route_retrieval("x")
    assert out["retrieval_method"] == "NO_HOARD" and out["retrieved_paths"] == []


# ───────────────────────── the Gate III review ─────────────────────────


def candidate(ccid, text, space=SPACE.id, dim=768, outcome=1.0):
    v = bow_vector(text, dim)
    return {"ccid": ccid, "embedding": v, "embed_space": space, "outcome_label": outcome, "created_at": 9e9}


def test_review_excludes_other_spaces_and_wrong_dimensions_and_counts_them():
    rodin = RodinProtocol(embedder=EmbeddingService(ScriptedBackend(), SPACE))
    q = bow_vector("sun breathing form")
    nodes = [
        candidate("OK1", "sun breathing form"),
        candidate("OLD", "sun breathing form", space=None),
        candidate("OTHER", "sun breathing form", space="gemini-embedding-2|1536|asym-v1"),
        candidate("SHORT", "sun breathing form", dim=64),
    ]
    out = rodin.review_node_integrity(q, nodes, space=SPACE)
    assert out["candidates_total"] == 4 and out["excluded_other_space"] == 2 and out["excluded_dim_mismatch"] == 1
    assert [n["ccid"] for n in out["neighbors"]] == ["OK1"]
    assert out["embedding_space"] == SPACE.id


def test_review_without_a_space_keeps_the_legacy_behaviour():
    rodin = RodinProtocol()
    q = bow_vector("sun breathing form")
    out = rodin.review_node_integrity(q, [candidate("A", "sun breathing form", space=None)])
    assert out["k_neighbors_found"] == 1 and out["decision"] == "PASS"


def test_gate_iii_decisions_are_unchanged():
    rodin = RodinProtocol()
    assert rodin.gate_iii_decision(0.9, False)["decision"] == "PASS"
    halt = rodin.gate_iii_decision(0.5, True)
    assert halt["decision"] == "HALT" and len(halt["failure_reasons"]) == 2


@pytest.mark.xfail(strict=True, reason=(
    "OPEN, not changed here: the module docstring defines M_knn = (1/K) * SUM[I(success) * exp(-d^2/sigma^2)], "
    "but the code returns SUM(w*o)/SUM(w), so a single distant success neighbour scores 1.0 and passes Gate III."))
def test_one_distant_success_neighbour_should_not_pass_gate_iii():
    rodin = RodinProtocol()
    assert rodin.calculate_neighborhood_density([{"distance": 0.9, "outcome_label": 1.0}]) < rodin.tau


# ───────────────────────── status ─────────────────────────


def test_status_reports_the_embedder_state_and_configuration(tmp_path):
    rodin, _, svc, _ = build(tmp_path, embed=False)
    s = rodin.status()
    assert s["embedder_state"] == "UNPROVEN" and s["embedding"]["space"] == SPACE.id
    assert s["coarse_dim"] == 128 and s["fine_dim"] == 768
    rodin.route_retrieval("cheshire")
    assert rodin.status()["embedder_state"] == "READY"
