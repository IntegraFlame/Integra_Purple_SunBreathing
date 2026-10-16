"""
INTEGRA O/S: HOARD EMBEDDING-SPACE TEST SUITE (offline)

The Hoard stores nodes. A node's vector is either a real embedding tagged with its space
(model | dimension | prompt format) or it is absent. Nothing fabricated is stored, indexed or searched.
Evidence behind these rules (MEASURED 2026-10-15 on copies of the live stores): of 307 shards,
257 held all-zero vectors, 4 held SHA-256 pseudo-vectors and 41 held unit-length pseudo-vectors (40 are Daily Planet
reports built from SHA-512); the Chroma
collection held 5,526 rows, none of them from a model.
"""

import json
import os

import pytest

from memory.embedding_service import EmbeddingService, EmbeddingSpace, EmbeddingUnavailable
from memory.the_hoard import HoardNode, TheHoard, node_embedding_text
from tests.embedding_fakes import ScriptedBackend, bow_vector

SPACE = EmbeddingSpace()
ANCHOR = {"x": 30.5888, "y": -91.1673, "z": 0.0, "t": 1}


def make_hoard(tmp_path, backend=None, with_embedder=False, **kw):
    svc = EmbeddingService(backend or ScriptedBackend(), SPACE) if with_embedder else None
    return TheHoard(base_dir=str(tmp_path), embedder=svc, **kw), svc


def add_node(hoard, ccid, text, **kw):
    return hoard.commit_node_v2(payload={"text": text}, spacetime_anchor=ANCHOR, ccid=ccid, **kw)


def shard(hoard, ccid):
    with open(os.path.join(hoard.kernel_memory_dir, "hoard", "raw_shards", f"{ccid}.json"), encoding="utf-8") as fh:
        return json.load(fh)


# ───────────────────────── nodes and schema ─────────────────────────


def test_node_roundtrip_keeps_the_space_and_old_shards_still_load():
    node = HoardNode(ccid="N", payload="p", spacetime_anchor={}, embedding_768d=bow_vector("x"), embed_space=SPACE.id)
    assert node.has_vector is True
    again = HoardNode.from_dict(node.to_dict())
    assert again.embed_space == SPACE.id and again.has_vector

    legacy = {"ccid": "OLD", "payload": "p", "spacetime_anchor": {}, "embedding_768d": [0.3] * 768}
    old = HoardNode.from_dict(legacy)
    assert old.embed_space is None and old.has_vector is False  # a vector with no space is not trusted


def test_zero_vector_is_never_a_vector():
    node = HoardNode(ccid="N", payload="p", spacetime_anchor={}, embed_space=SPACE.id)
    assert node.has_vector is False


def test_rodin_candidate_carries_the_space():
    node = HoardNode(ccid="N", payload="p", spacetime_anchor={}, embedding_768d=bow_vector("x"), embed_space=SPACE.id)
    assert node.to_rodin_candidate()["embed_space"] == SPACE.id


def test_shard_write_is_atomic_and_leaves_no_temporary_file(tmp_path):
    hoard, _ = make_hoard(tmp_path)
    add_node(hoard, "N1", "alpha")
    names = os.listdir(os.path.join(hoard.kernel_memory_dir, "hoard", "raw_shards"))
    assert names == ["N1.json"]


# ───────────────────────── no fabricated vectors ─────────────────────────


def test_the_pseudo_embedding_generator_is_gone():
    assert not hasattr(TheHoard, "_generate_pseudo_embedding")


SAVE_STATE = {
    "ccid": "CCID_9999999999",
    "celestial_stamp": {"unix_epoch": 1789760297.0, "anchor": "Baker, Louisiana"},
    "identity_matrix": {"modality": "PURPLE", "omega": 1.0},
    "cognitive_telemetry": {"dragon_state": "ACTIVE_WAKING_STATE"},
    "work_completed_this_session": ["Phase D Complete"],
}


def test_sync_save_state_without_an_embedder_stores_no_vector_and_says_so(tmp_path):
    hoard, _ = make_hoard(tmp_path)
    receipt = hoard.sync_save_state(SAVE_STATE)
    assert receipt["status"] == "SAVE_STATE_SYNCED_TO_HOARD"
    assert receipt["mrl_embeddings_created"] is False and receipt["embedding_status"] == "PENDING"
    node = hoard.local_sparse_cache[-1]
    assert node.has_vector is False and node.embed_space is None
    assert not any(node.embedding_768d)
    assert shard(hoard, "CCID_9999999999")["embed_space"] is None
    assert hoard.count() == 0  # nothing was indexed


def test_sync_save_state_with_an_embedder_embeds_tags_and_indexes(tmp_path):
    hoard, svc = make_hoard(tmp_path, with_embedder=True)
    receipt = hoard.sync_save_state(SAVE_STATE)
    assert receipt["mrl_embeddings_created"] is True and receipt["embed_space"] == SPACE.id
    node = hoard.local_sparse_cache[-1]
    assert node.has_vector and node.embed_space == SPACE.id
    assert len(node.embedding_768d) == 768 and node.embedding_64d == node.embedding_768d[:64]
    assert hoard.count() == 1
    assert svc.stats()["texts_sent"] == 1


def test_sync_save_state_survives_a_failing_embedder_and_reports_the_error(tmp_path):
    backend = ScriptedBackend(errors=[EmbeddingUnavailable("API_ERROR", "404 model not found")])
    hoard, _ = make_hoard(tmp_path, backend=backend, with_embedder=True)
    receipt = hoard.sync_save_state(SAVE_STATE)
    assert receipt["status"] == "SAVE_STATE_SYNCED_TO_HOARD"
    assert receipt["mrl_embeddings_created"] is False
    assert receipt["embedding_error"]["code"] == "API_ERROR"
    assert os.path.exists(receipt["shard_file"]) and hoard.count() == 0


def test_a_vector_without_a_space_is_stored_but_never_indexed(tmp_path):
    hoard, _ = make_hoard(tmp_path)
    receipt = add_node(hoard, "N1", "alpha", embedding_768d=[0.1] * 768, outcome_label=1.0)
    assert receipt["chroma_synced"] is False
    assert hoard.count() == 0
    assert hoard.get_telemetry()["untrusted_vector_nodes"] == 1


# ───────────────────────── one collection per space ─────────────────────────


def test_a_vector_in_the_active_space_is_indexed_and_found(tmp_path):
    hoard, _ = make_hoard(tmp_path)
    v = bow_vector("sun breathing thirteenth form")
    receipt = add_node(hoard, "N1", "sun breathing thirteenth form", embedding_768d=v, embed_space=SPACE.id)
    assert receipt["chroma_synced"] is True
    assert hoard._chroma_collection.name == SPACE.collection_name()
    hits = hoard.chroma_query(v, n_results=1)
    assert hits[0]["ccid"] == "N1"
    assert hoard._chroma_collection.metadata["embed_space"] == SPACE.id


def test_a_vector_tagged_with_another_space_is_not_indexed(tmp_path):
    hoard, _ = make_hoard(tmp_path)
    receipt = add_node(hoard, "N1", "alpha", embedding_768d=bow_vector("alpha"), embed_space="gemini-embedding-2|1536|asym-v1")
    assert receipt["chroma_synced"] is False and hoard.count() == 0


def test_chroma_query_from_a_foreign_space_raises(tmp_path):
    hoard, _ = make_hoard(tmp_path)
    with pytest.raises(ValueError):
        hoard.chroma_query(bow_vector("x"), n_results=1, space_id="gemini-embedding-2|1536|asym-v1")


def test_the_legacy_collection_is_never_queried_or_touched(tmp_path):
    import chromadb

    chroma_dir = str(tmp_path / "shared_chroma")
    legacy = chromadb.PersistentClient(path=chroma_dir).get_or_create_collection("integra_hoard", metadata={"hnsw:space": "cosine"})
    legacy.upsert(ids=["OLD1", "OLD2"], embeddings=[[0.1] * 768, [0.2] * 768], documents=["hash one", "hash two"])

    hoard, _ = make_hoard(tmp_path, chroma_path=chroma_dir)
    v = bow_vector("real node")
    add_node(hoard, "NEW1", "real node", embedding_768d=v, embed_space=SPACE.id)
    hits = hoard.chroma_query(v, n_results=5)
    assert [h["ccid"] for h in hits] == ["NEW1"]
    assert hoard.get_telemetry(include_legacy_rows=True)["legacy_collection_rows"] == 2
    assert legacy.count() == 2


def test_telemetry_makes_no_chroma_call_unless_asked(tmp_path):
    """/rodin/telemetry is an async route polled every second; a native Chroma call on the event loop can wedge the server."""
    hoard, _ = make_hoard(tmp_path)

    touched = []

    class Tripwire:
        def __getattr__(self, name):
            touched.append(name)  # recorded, because a try/except in the code under test could swallow a raise
            raise AttributeError(name)

    hoard._chroma_client = Tripwire()
    hoard._chroma_collection = Tripwire()
    t = hoard.get_telemetry()
    assert touched == []
    assert t["legacy_collection_rows"] is None and t["vector_search_available"] is True
    assert t["total_nodes"] == 0 and t["active_space"] == SPACE.id


def test_bad_embedding_configuration_keeps_the_default_space_and_reports_it(tmp_path, monkeypatch):
    monkeypatch.setenv("RODIN_EMBED_MODEL", "text-embedding-004")
    hoard, _ = make_hoard(tmp_path)
    assert hoard.space == SPACE
    assert "text-embedding-004" in hoard.config_error
    assert hoard.get_telemetry()["config_error"] == hoard.config_error


def test_chroma_candidates_are_rodin_shaped_rows_with_vectors_and_labels(tmp_path):
    hoard, _ = make_hoard(tmp_path)
    v = bow_vector("sun breathing thirteenth form")
    add_node(hoard, "N1", "sun breathing thirteenth form", embedding_768d=v, embed_space=SPACE.id, outcome_label=0.0)
    rows = hoard.chroma_candidates(v, n_results=5, space_id=SPACE.id)
    assert [r["ccid"] for r in rows] == ["N1"]
    r = rows[0]
    assert r["embed_space"] == SPACE.id and r["outcome_label"] == 0.0 and isinstance(r["created_at"], float)
    assert len(r["embedding"]) == 768 and max(abs(a - b) for a, b in zip(r["embedding"], v)) < 1e-5
    assert "sun breathing" in r["payload"]


def test_chroma_candidates_are_empty_without_an_index_and_reject_a_foreign_space(tmp_path):
    hoard, _ = make_hoard(tmp_path)
    with pytest.raises(ValueError):
        hoard.chroma_candidates(bow_vector("x"), n_results=3, space_id="gemini-embedding-2|1536|asym-v1")
    hoard._chroma_collection = None
    assert hoard.chroma_candidates(bow_vector("x"), n_results=3, space_id=SPACE.id) == []


def test_candidates_can_be_filtered_by_space(tmp_path):
    hoard, _ = make_hoard(tmp_path)
    add_node(hoard, "A", "alpha", embedding_768d=bow_vector("alpha"), embed_space=SPACE.id)
    add_node(hoard, "B", "beta", embedding_768d=bow_vector("beta"), embed_space=SPACE.id)
    add_node(hoard, "C", "gamma", embedding_768d=[0.3] * 768)
    assert len(hoard.get_rodin_candidates()) == 3
    only = hoard.get_rodin_candidates(space_id=SPACE.id)
    assert sorted(c["ccid"] for c in only) == ["A", "B"] and all(c["embed_space"] == SPACE.id for c in only)


# ───────────────────────── embed_pending: the explicit re-embed step ─────────────────────────


def seeded_hoard(tmp_path, backend=None):
    hoard, svc = make_hoard(tmp_path, backend=backend, with_embedder=True)
    add_node(hoard, "P1", "red apple orchard")
    add_node(hoard, "P2", "blue car engine")
    add_node(hoard, "P3", "red apple orchard")                 # same text as P1: embedded once
    add_node(hoard, "P4", "green tea leaves", embedding_768d=[0.3] * 768)  # untrusted vector, no space
    add_node(hoard, "DONE", "already embedded text", embedding_768d=bow_vector("already embedded text"), embed_space=SPACE.id)
    return hoard, svc


def test_embed_pending_dry_run_counts_and_prices_without_calling_the_backend(tmp_path):
    hoard, svc = seeded_hoard(tmp_path)
    plan = hoard.embed_pending(dry_run=True)
    assert plan["dry_run"] is True and plan["pending"] == 4 and plan["already_embedded"] == 1
    assert plan["unique_texts"] == 3 and plan["estimated_tokens"] > 0 and plan["estimated_cost_usd"] >= 0
    assert svc.stats()["calls"] == 0


def test_embed_pending_embeds_dedupes_persists_and_indexes(tmp_path):
    hoard, svc = seeded_hoard(tmp_path)
    receipt = hoard.embed_pending(dry_run=False)
    assert receipt["embedded"] == 4 and receipt["texts_sent"] == 3 and receipt["stopped_early"] is False
    for ccid in ("P1", "P2", "P3", "P4"):
        s = shard(hoard, ccid)
        assert s["embed_space"] == SPACE.id and any(s["embedding_768d"]) and len(s["embedding_768d"]) == 768
    assert shard(hoard, "P4")["embedding_768d"] != [0.3] * 768  # the untrusted vector was replaced
    assert hoard.count() == 5
    assert hoard.get_telemetry()["embedded_nodes"] == 5 and hoard.get_telemetry()["unembedded_nodes"] == 0
    names = os.listdir(os.path.join(hoard.kernel_memory_dir, "hoard", "raw_shards"))
    assert not [n for n in names if n.endswith(".tmp")]
    again = hoard.embed_pending(dry_run=False)
    assert again["pending"] == 0 and again["embedded"] == 0


def test_embed_pending_uses_the_text_of_the_node_not_its_json(tmp_path):
    hoard, svc = seeded_hoard(tmp_path)
    backend = svc.backend
    hoard.embed_pending(dry_run=False)
    sent = [t for call in backend.calls for t in call["texts"]]
    assert "title: none | text: red apple orchard" in sent   # no real title, so the documented "none"; a ccid is noise to the model
    assert not any("{" in t for t in sent)


def test_embed_pending_stops_at_the_first_failure_and_reports_progress(tmp_path):
    backend = ScriptedBackend(errors=[None, EmbeddingUnavailable("API_ERROR", "503 unavailable")])
    hoard, svc = seeded_hoard(tmp_path, backend=backend)
    receipt = hoard.embed_pending(dry_run=False, batch_size=2)
    assert receipt["stopped_early"] is True and receipt["error"]["code"] == "API_ERROR"
    assert 0 < receipt["embedded"] < 4
    untouched = [c for c in ("P1", "P2", "P3", "P4") if shard(hoard, c)["embed_space"] is None]
    assert untouched, "a failed batch must leave its shards exactly as they were"


def test_embed_pending_paces_the_batches(tmp_path):
    hoard, _ = seeded_hoard(tmp_path)
    sleeps = []
    hoard.embed_pending(dry_run=False, batch_size=1, pause_s=0.7, sleep=sleeps.append)
    assert sleeps == [0.7, 0.7]  # three unique texts, one per batch: a pause between batches, none after the last


def test_embed_pending_respects_the_limit(tmp_path):
    hoard, _ = seeded_hoard(tmp_path)
    receipt = hoard.embed_pending(dry_run=False, limit=1, batch_size=1)
    assert receipt["embedded"] >= 1 and receipt["pending"] == 4
    assert hoard.get_telemetry()["unembedded_nodes"] >= 1


def test_embed_pending_without_a_working_embedder_stops_at_once_and_says_why(tmp_path):
    # No embedder is given, no key is set (tests/conftest.py clears it), so the default service cannot reach a model.
    hoard, _ = make_hoard(tmp_path)
    add_node(hoard, "P1", "alpha")
    receipt = hoard.embed_pending(dry_run=False)
    assert receipt["stopped_early"] is True and receipt["embedded"] == 0
    assert receipt["error"]["code"] in {"NO_CLIENT", "ROUTER_REFUSED"}
    assert shard(hoard, "P1")["embed_space"] is None and hoard.count() == 0


def test_embed_pending_refuses_to_run_under_a_bad_configuration(tmp_path, monkeypatch):
    monkeypatch.setenv("RODIN_EMBED_MODEL", "text-embedding-004")
    hoard, _ = make_hoard(tmp_path)
    add_node(hoard, "P1", "alpha")
    with pytest.raises(EmbeddingUnavailable) as exc:
        hoard.embed_pending(dry_run=False)
    assert exc.value.code == "BAD_CONFIG"


def test_load_skips_files_that_are_not_nodes_and_never_rewrites_them(tmp_path):
    hoard, svc = make_hoard(tmp_path, with_embedder=True)
    shards_dir = os.path.join(hoard.kernel_memory_dir, "hoard", "raw_shards")
    odd = {"simulation_id": "SIM1", "aggregate": {"x": 1}}  # one of the live folder's non-node shapes
    with open(os.path.join(shards_dir, "SIM.json"), "w", encoding="utf-8") as fh:
        json.dump(odd, fh)
    add_node(hoard, "N1", "alpha beta")

    fresh = TheHoard(base_dir=str(tmp_path), embedder=svc)
    assert fresh.load_shards_from_disk() == 1
    assert fresh.last_load_report["skipped_not_a_node"] == 1
    fresh.embed_pending(dry_run=False)
    with open(os.path.join(shards_dir, "SIM.json"), encoding="utf-8") as fh:
        assert json.load(fh) == odd


def test_embedding_a_shard_changes_only_the_embedding_keys(tmp_path):
    hoard, _ = make_hoard(tmp_path, with_embedder=True)
    add_node(hoard, "N1", "alpha beta")
    path = hoard._shard_path("N1")
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    data["custom_note"] = {"keep": "me"}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    hoard.embed_pending(dry_run=False)
    after = shard(hoard, "N1")
    assert after["custom_note"] == {"keep": "me"} and after["embed_space"] == SPACE.id
    assert after["payload"] == {"text": "alpha beta"}


def test_a_corrupt_shard_is_reported_and_left_alone(tmp_path):
    hoard, _ = make_hoard(tmp_path, with_embedder=True)
    add_node(hoard, "N1", "alpha beta")
    path = hoard._shard_path("N1")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("{not json")
    receipt = hoard.embed_pending(dry_run=False)
    assert receipt["embedded"] == 0 and [e["ccid"] for e in receipt["shard_errors"]] == ["N1"]
    with open(path, encoding="utf-8") as fh:
        assert fh.read() == "{not json"
    assert hoard.local_sparse_cache[0].embed_space is None


# ───────────────────────── read-only planning, without a Hoard ─────────────────────────


def test_nodes_can_be_loaded_and_planned_without_creating_a_hoard_or_touching_chroma(tmp_path):
    from memory.the_hoard import load_nodes_from_shards, plan_embedding

    hoard, _ = make_hoard(tmp_path)
    add_node(hoard, "A", "red apple orchard")
    add_node(hoard, "B", "red apple orchard")
    add_node(hoard, "C", "blue car engine", embedding_768d=bow_vector("blue car engine"), embed_space=SPACE.id)
    shards = os.path.join(hoard.kernel_memory_dir, "hoard", "raw_shards")
    with open(os.path.join(shards, "ODD.json"), "w", encoding="utf-8") as fh:
        json.dump({"simulation_id": "S"}, fh)
    with open(os.path.join(shards, "BAD.json"), "w", encoding="utf-8") as fh:
        fh.write("{not json")

    nodes, report = load_nodes_from_shards(shards)
    assert sorted(n.ccid for n in nodes) == ["A", "B", "C"]
    assert report == {"loaded": 3, "skipped_not_a_node": 1, "unreadable": 1}
    plan = plan_embedding(nodes, SPACE)
    assert plan["pending"] == 2 and plan["already_embedded"] == 1 and plan["unique_texts"] == 1
    assert plan["estimated_tokens"] > 0


# ───────────────────────── text selection and telemetry ─────────────────────────


def test_node_embedding_text_rules():
    n1 = HoardNode(ccid="C1", payload={"text": "chunk body", "header": "H"}, spacetime_anchor={}, metadata={"filename": "f.md"})
    assert node_embedding_text(n1) == ("chunk body", "f.md")
    n2 = HoardNode(ccid="C2", payload="plain string", spacetime_anchor={})
    assert node_embedding_text(n2) == ("plain string", None)
    n3 = HoardNode(ccid="C3", payload={"b": 2, "a": 1}, spacetime_anchor={})
    assert node_embedding_text(n3) == ('{"a": 1, "b": 2}', None)
    n4 = HoardNode(ccid="C4", payload={"summary": "a report summary", "query": "q"}, spacetime_anchor={})
    assert node_embedding_text(n4) == ("a report summary", None)
    n5 = HoardNode(ccid="C5", payload={"text": "body", "header": "## Section"}, spacetime_anchor={})
    assert node_embedding_text(n5) == ("body", "## Section")


def test_telemetry_reports_space_counts_and_schema(tmp_path):
    hoard, _ = seeded_hoard(tmp_path)
    t = hoard.get_telemetry()
    assert t["active_space"] == SPACE.id and t["total_nodes"] == 5
    assert t["embedded_nodes"] == 1 and t["unembedded_nodes"] == 3 and t["untrusted_vector_nodes"] == 1
    assert t["chroma_collection"] == SPACE.collection_name()
