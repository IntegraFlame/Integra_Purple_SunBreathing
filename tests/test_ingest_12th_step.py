"""
INTEGRA O/S: 12TH STEP ORTHOGONAL INGESTION TEST SUITE (offline)

The 12th Step ingestion (scripts/ingest_knowledge.py) used to give every chunk a SHA-256 pseudo-vector and write it
to Chroma, and it deleted files ("safe hygiene") before every run. Measured 2026-10-15 on a copy of the live store:
5,242 of the 5,526 Chroma rows came from it, none held a model's vector, and 2,974 rows were exact duplicate chunks.

New contract: a default run only PLANS (counts, duplicates, tokens, price) and touches nothing; --apply embeds the
deduplicated chunks with the real model and indexes them in the active embedding space; file hygiene is a separate,
explicit, dry-run-first step.
"""

import inspect
import os

import pytest

import scripts.ingest_knowledge as ingest_module
from memory.embedding_service import EmbeddingService, EmbeddingSpace, EmbeddingUnavailable, max_body_chars
from memory.the_hoard import TheHoard
from scripts.ingest_knowledge import MultiLobeIngestionEngine, chunk_document, perform_safe_hygiene, run_test_retrieval
from tests.embedding_fakes import ScriptedBackend

SPACE = EmbeddingSpace()
LOBES = {"lobeA": {"lobe": "architecture", "extensions": [".md", ".txt"], "description": "test lobe", "layer": 2}}

PARAS = [f"Paragraph {i} about topic{i} " + ("filler words " * 90) for i in range(24)]  # about 1,200 characters each


def make_workspace(tmp_path):
    lobe = tmp_path / "ws" / "lobeA"
    lobe.mkdir(parents=True)
    (lobe / "alpha.md").write_text("# Alpha\n\n" + "\n\n".join(PARAS[:3]), encoding="utf-8")
    (lobe / "beta.md").write_text("# Beta\n\n" + "\n\n".join(PARAS[:3]), encoding="utf-8")   # same chunks as alpha: duplicates
    (lobe / "empty.md").write_text("", encoding="utf-8")                                      # a 0-byte file hygiene would delete
    return tmp_path / "ws"


def make_engine(tmp_path, backend=None, workspace=None):
    backend = backend or ScriptedBackend()
    svc = EmbeddingService(backend, SPACE)
    hoard = TheHoard(base_dir=str(tmp_path / "home"), embedder=svc)
    ws = workspace or make_workspace(tmp_path)
    return MultiLobeIngestionEngine(hoard=hoard, embedder=svc, workspace_root=ws, lobe_config=LOBES), hoard, svc, backend, ws


def test_no_pseudo_embedding_call_remains_in_the_script():
    source = inspect.getsource(ingest_module)
    assert "_generate_pseudo_embedding" not in source and "/ 255" not in source  # the byte-to-float hash vector is gone


def test_default_run_is_a_plan_only_and_touches_nothing(tmp_path):
    engine, hoard, svc, backend, ws = make_engine(tmp_path)
    result = engine.ingest_lobes()
    assert result["status"] == "INGESTION_PLAN_ONLY" and result["chroma_chunks_persisted"] == 0
    plan = result["plan"]
    assert plan["chunks_unique"] >= 1 and plan["duplicate_chunks_skipped"] >= 1
    assert plan["estimated_tokens"] > 0 and plan["estimated_cost_usd"] >= 0
    assert svc.stats()["calls"] == 0 and hoard.count() == 0 and hoard.local_sparse_cache == []
    assert (ws / "lobeA" / "empty.md").exists()


def test_hygiene_is_off_by_default_a_dry_run_when_asked_and_deletes_only_when_applied(tmp_path):
    engine, _, _, _, ws = make_engine(tmp_path)
    zero = ws / "lobeA" / "empty.md"
    engine.ingest_lobes()
    assert zero.exists()
    dry = engine.ingest_lobes(clean_first=True)
    assert zero.exists() and dry["hygiene"]["dry_run"] is True
    assert any(p.endswith("empty.md") for p in dry["hygiene"]["removed_zero_byte_files"])
    engine.ingest_lobes(clean_first=True, apply_hygiene=True)
    assert not zero.exists()


def test_perform_safe_hygiene_defaults_to_a_dry_run(tmp_path):
    ws = make_workspace(tmp_path)
    out = perform_safe_hygiene(workspace_root=ws, lobe_config=LOBES)
    assert out["dry_run"] is True and (ws / "lobeA" / "empty.md").exists()


def test_apply_embeds_the_deduplicated_chunks_and_indexes_them_in_the_active_space(tmp_path):
    engine, hoard, svc, backend, ws = make_engine(tmp_path)
    plan = engine.ingest_lobes()["plan"]
    result = engine.ingest_lobes(apply=True)
    assert result["status"] == "INGESTION_COMPLETE"
    assert result["chroma_chunks_persisted"] == plan["chunks_unique"] == hoard.count()
    sent = [t for call in backend.calls for t in call["texts"]]
    assert len(sent) == plan["chunks_unique"] and all(t.startswith("title: ") for t in sent)
    assert any(t.startswith("title: alpha.md | text: ") for t in sent)
    row = hoard._chroma_collection.get(include=["metadatas"], limit=1)["metadatas"][0]
    assert row["lobe"] == "architecture" and row["embed_space"] == SPACE.id and "shiva_lens" in row
    assert all(n.has_vector and n.embed_space == SPACE.id for n in hoard.local_sparse_cache)


def test_a_second_apply_embeds_nothing_new(tmp_path):
    engine, hoard, svc, backend, _ = make_engine(tmp_path)
    engine.ingest_lobes(apply=True)
    rows, sent = hoard.count(), svc.stats()["texts_sent"]
    engine2 = MultiLobeIngestionEngine(hoard=hoard, embedder=svc, workspace_root=engine.workspace_root, lobe_config=LOBES)
    result = engine2.ingest_lobes(apply=True)
    assert result["status"] == "INGESTION_COMPLETE" and result["chroma_chunks_persisted"] == 0
    assert result["plan"]["already_indexed"] == rows
    assert svc.stats()["texts_sent"] == sent and hoard.count() == rows


def test_changed_chunks_are_re_embedded_and_unchanged_ones_are_skipped(tmp_path):
    engine, hoard, svc, backend, ws = make_engine(tmp_path)
    engine.ingest_lobes(apply=True)
    rows, sent = hoard.count(), svc.stats()["texts_sent"]
    (ws / "lobeA" / "alpha.md").write_text("# Alpha\n\n" + "A completely rewritten paragraph about new topics. " * 4, encoding="utf-8")
    engine2 = MultiLobeIngestionEngine(hoard=hoard, embedder=svc, workspace_root=ws, lobe_config=LOBES)
    result = engine2.ingest_lobes(apply=True)
    assert result["chroma_chunks_persisted"] >= 1
    assert svc.stats()["texts_sent"] - sent == result["chroma_chunks_persisted"]
    assert hoard.count() >= rows - 1


def test_apply_stops_when_embedding_is_unavailable_and_reports_progress(tmp_path):
    ws = tmp_path / "ws"
    (ws / "lobeA").mkdir(parents=True)
    (ws / "lobeA" / "big.md").write_text("\n\n".join(PARAS), encoding="utf-8")                # about 24 chunks
    backend = ScriptedBackend(errors=[None, EmbeddingUnavailable("API_ERROR", "503 unavailable")])
    engine, hoard, svc, _, _ = make_engine(tmp_path, backend=backend, workspace=ws)
    result = engine.ingest_lobes(apply=True)
    assert result["status"] == "INGESTION_STOPPED_EMBEDDING_UNAVAILABLE"
    assert result["error"]["code"] == "API_ERROR"
    assert 0 < result["chroma_chunks_persisted"] < result["plan"]["chunks_unique"]
    assert hoard.count() == result["chroma_chunks_persisted"]


def test_apply_paces_the_batches(tmp_path):
    ws = tmp_path / "ws"
    (ws / "lobeA").mkdir(parents=True)
    (ws / "lobeA" / "big.md").write_text("\n\n".join(PARAS), encoding="utf-8")                # about 24 chunks: two batches of 16
    engine, hoard, svc, backend, _ = make_engine(tmp_path, workspace=ws)
    sleeps = []
    engine._sleep = sleeps.append
    result = engine.ingest_lobes(apply=True, pause_s=0.5)
    assert result["status"] == "INGESTION_COMPLETE" and len(backend.calls) == 2
    assert sleeps == [0.5]                                                                      # between the two batches only


def test_lens_tags_follow_the_four_pass_manifold(tmp_path):
    ws = tmp_path / "ws"
    (ws / "lobeA").mkdir(parents=True)
    (ws / "lobeA" / "big.md").write_text("\n\n".join(PARAS[:8]), encoding="utf-8")
    engine, hoard, *_ = make_engine(tmp_path, workspace=ws)
    engine.ingest_lobes(apply=True)
    metas = sorted(hoard._chroma_collection.get(include=["metadatas"])["metadatas"], key=lambda m: m["chunk_index"])
    lenses = [m["shiva_lens"] for m in metas[:4]]
    assert lenses == ["Neji_Eagle (Structure)", "Chameleon (Middle-Out)", "Snake (Density/Kaigaku)", "Owl (Truth Synthesis)"]


def test_run_test_retrieval_embeds_the_query_in_the_documented_format(tmp_path):
    engine, hoard, svc, backend, _ = make_engine(tmp_path)
    engine.ingest_lobes(apply=True)
    out = run_test_retrieval(hoard, "topic1 filler words", embedder=svc)
    assert out["results"] and backend.calls[-1]["texts"] == ["task: search result | query: topic1 filler words"]


def test_chunks_stay_far_inside_the_embedding_input_limit():
    chunks = chunk_document("\n\n".join(PARAS))
    assert max(len(c["text"]) for c in chunks) < max_body_chars() / 5
