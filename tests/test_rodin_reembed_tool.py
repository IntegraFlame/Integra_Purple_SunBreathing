"""
INTEGRA O/S: RODIN RE-EMBED TOOL TEST SUITE (offline)

tools/rodin_reembed.py moves the Hoard's shards into the current embedding space. It is the one step that spends
money, so: the default is a read-only plan, a real run needs BOTH --apply and --yes-paid, and a run stops at the
first failure and says what it finished.
"""

import json
import os

import pytest

from memory.embedding_service import EmbeddingService, EmbeddingSpace, EmbeddingUnavailable
from tests.embedding_fakes import ScriptedBackend, bow_vector
from tools.rodin_reembed import main

SPACE = EmbeddingSpace()


def write_shard(root, ccid, text=None, vector=None, space=None, extra=None):
    d = os.path.join(root, "kernel_memory", "hoard", "raw_shards")
    os.makedirs(d, exist_ok=True)
    data = {"ccid": ccid, "payload": {"text": text} if text is not None else None, "spacetime_anchor": {"t": 1},
            "embedding_64d": [0.0] * 64, "embedding_768d": vector or [0.0] * 768, "embed_space": space,
            "outcome_label": 1.0, "is_stale": False, "created_at": 1.0, "sufficiency_score": 1.0, "metadata": {}}
    data.update(extra or {})
    with open(os.path.join(d, f"{ccid}.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh)


def snapshot(root):
    out = {}
    for base, _, files in os.walk(root):
        for f in files:
            p = os.path.join(base, f)
            with open(p, "rb") as fh:
                out[os.path.relpath(p, root)] = fh.read()
    return out


@pytest.fixture()
def root(tmp_path):
    r = str(tmp_path / "home")
    write_shard(r, "A", "red apple orchard")
    write_shard(r, "B", "red apple orchard")
    write_shard(r, "C", "blue car engine")
    write_shard(r, "D", "green tea", vector=[0.3] * 768)                  # a vector with no named space
    write_shard(r, "E", "already done", vector=bow_vector("already done"), space=SPACE.id)
    return r


def run(root, *args, backend=None, capsys=None):
    svc = EmbeddingService(backend or ScriptedBackend(), SPACE)
    code = main(["--root", root, *args], embedder=svc)
    out = capsys.readouterr().out if capsys else ""
    return code, out, svc


def test_default_is_a_read_only_plan_that_creates_and_changes_nothing(root, capsys):
    before = snapshot(root)
    code, out, svc = run(root, capsys=capsys)
    assert code == 0 and "PLAN ONLY" in out
    plan = json.loads(out[out.index("{"):])
    assert plan["pending"] == 4 and plan["already_embedded"] == 1 and plan["unique_texts"] == 3
    assert plan["estimated_cost_usd"] >= 0
    assert snapshot(root) == before                                       # no file written, no folder created (no local_dbs)
    assert not os.path.exists(os.path.join(root, "local_dbs"))
    assert svc.stats()["calls"] == 0


def test_apply_alone_is_refused_without_the_paid_flag(root, capsys):
    before = snapshot(root)
    code, out, svc = run(root, "--apply", capsys=capsys)
    assert code == 2 and "--yes-paid" in out
    assert snapshot(root) == before and svc.stats()["calls"] == 0


def test_apply_with_the_paid_flag_embeds_and_updates_the_shards(root, capsys):
    code, out, svc = run(root, "--apply", "--yes-paid", capsys=capsys)
    assert code == 0
    receipt = json.loads(out[out.rindex("RECEIPT") + len("RECEIPT"):])
    assert receipt["embedded"] == 4 and receipt["stopped_early"] is False
    for ccid in "ABCD":
        with open(os.path.join(root, "kernel_memory", "hoard", "raw_shards", f"{ccid}.json"), encoding="utf-8") as fh:
            s = json.load(fh)
        assert s["embed_space"] == SPACE.id and any(s["embedding_768d"])
    assert svc.stats()["texts_sent"] == 3


def test_limit_makes_a_pilot_run(root, capsys):
    code, out, svc = run(root, "--apply", "--yes-paid", "--limit", "1", capsys=capsys)
    receipt = json.loads(out[out.rindex("RECEIPT") + len("RECEIPT"):])
    assert code == 0 and receipt["texts_sent"] == 1 and receipt["embedded"] >= 1


def test_a_failed_run_exits_nonzero_and_reports_the_progress(root, capsys):
    backend = ScriptedBackend(errors=[None, EmbeddingUnavailable("API_ERROR", "503 unavailable")])
    code, out, _ = run(root, "--apply", "--yes-paid", "--batch-size", "1", backend=backend, capsys=capsys)
    receipt = json.loads(out[out.rindex("RECEIPT") + len("RECEIPT"):])
    assert code == 1 and receipt["stopped_early"] is True and receipt["error"]["code"] == "API_ERROR"
    assert 0 < receipt["embedded"] < 4


def test_a_non_node_file_in_the_folder_is_reported_and_never_rewritten(root, capsys):
    odd = os.path.join(root, "kernel_memory", "hoard", "raw_shards", "SIM.json")
    with open(odd, "w", encoding="utf-8") as fh:
        json.dump({"simulation_id": "S1"}, fh)
    before = open(odd, "rb").read()
    code, out, _ = run(root, "--apply", "--yes-paid", capsys=capsys)
    receipt = json.loads(out[out.rindex("RECEIPT") + len("RECEIPT"):])
    assert code == 0 and receipt["shard_files"]["skipped_not_a_node"] == 1
    assert receipt["embedded"] == 4                                       # the four real pending nodes, not five
    assert open(odd, "rb").read() == before
    assert "UNKNOWN.json" not in os.listdir(os.path.dirname(odd))        # no junk node was written for it


def test_a_missing_shard_folder_is_a_clear_error(tmp_path, capsys):
    code, out, _ = run(str(tmp_path / "nowhere"), capsys=capsys)
    assert code == 2 and "raw_shards" in out
