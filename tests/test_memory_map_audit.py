"""
INTEGRA O/S: RODIN MEMORY MAP AUDIT TESTS (offline; Brain Map T2, step 2.5, piece P3)

validate_memory_map checks each entry of config/rodin_memory_map.yml. These tests cover what it does not: kinds and
stores that disagree about what goes where, stores that share a path without saying so, and declared state that
disagrees with the disk or with git. The shipped map's current findings are pinned here; piece P1 fixes the map and
turns that test into "no findings".
"""

import copy
import json
import os
import shutil
import subprocess

import pytest

from memory.memory_map import audit_memory_map, check_disk, check_git, load_memory_map, validate_memory_map

MAP = load_memory_map()


def st(sid, path, git, base="homebase", status="live", holds=(), **extra):
    """A minimal store entry for a test map."""
    return {"id": sid, "tier": "D", "base": base, "path": path, "status": status,
            "visibility": "public-repo" if git == "tracked" else "local-only", "git": git,
            "source_of_truth": True, "holds": list(holds), "writer": "a test", **extra}


def minimal():
    return {"stores": [st("a", "pa", "tracked", holds=["k1"]), st("b", "pb", "tracked", holds=["k2"])],
            "kinds": {"k1": {"primary": "a"}, "k2": {"primary": "b"}}}


def by_id(m, sid):
    return next(s for s in m["stores"] if s["id"] == sid)


# ───────────────────────── the shipped map, as it is today ─────────────────────────


def test_the_shipped_map_has_exactly_the_known_gaps():
    # MEASURED 2026-10-16 (T2 2.1-2.3): seven holds/kinds gaps and one undeclared shared path. P1 fixes the map.
    assert validate_memory_map(MAP) == []
    assert audit_memory_map(MAP) == sorted([
        "kind crystallization routes to store metatron_db, but metatron_db's holds omit 'crystallization'",
        "kind save_state routes to store chroma_active, but chroma_active's holds omit 'save_state'",
        "kind working_context routes to store ram_hoard_cache, but ram_hoard_cache's holds omit 'working_context'",
        "store drop_in holds 'inbox_file', which is not a defined kind",
        "store memory_db holds 'node', but kind node does not route to memory_db",
        "store ram_embedding_cache holds 'document_embedding', which is not a defined kind",
        "store ram_embedding_cache holds 'query_embedding', which is not a defined kind",
        "stores chroma_active and chroma_legacy share homebase:local_dbs/chroma_storage without declaring shares_path_with",
    ])


# ───────────────────────── audit: the map against itself ─────────────────────────


def test_a_consistent_map_has_no_findings_and_is_not_changed():
    m = minimal()
    before = copy.deepcopy(m)
    assert audit_memory_map(m) == []
    assert m == before


def test_audit_reports_a_held_value_that_is_not_a_kind():
    m = minimal()
    by_id(m, "a")["holds"].append("ghost")
    assert audit_memory_map(m) == ["store a holds 'ghost', which is not a defined kind"]


def test_audit_reports_a_route_the_store_does_not_list():
    m = minimal()
    m["kinds"]["k1"]["also"] = ["b"]
    assert audit_memory_map(m) == ["kind k1 routes to store b, but b's holds omit 'k1'"]


def test_audit_reports_a_held_kind_that_does_not_route_to_the_store():
    m = minimal()
    by_id(m, "b")["holds"].append("k1")
    assert audit_memory_map(m) == ["store b holds 'k1', but kind k1 does not route to b"]


def test_audit_reports_a_shared_path_until_both_stores_declare_it():
    m = minimal()
    by_id(m, "b")["path"] = "pa"
    expected = ["stores a and b share homebase:pa without declaring shares_path_with"]
    assert audit_memory_map(m) == expected
    by_id(m, "a")["shares_path_with"] = ["b"]
    assert audit_memory_map(m) == expected                    # one side is not enough
    by_id(m, "b")["shares_path_with"] = ["a"]
    assert audit_memory_map(m) == []


def test_audit_ignores_dangling_store_ids_which_validate_reports():
    m = minimal()
    m["kinds"]["k1"]["also"] = ["no_such_store"]
    assert audit_memory_map(m) == []
    assert any("no_such_store" in p for p in validate_memory_map(m))


# ───────────────────────── disk: declared status against the folders ─────────────────────────


def test_check_disk_judges_live_and_proposed_stores_only(tmp_path):
    (tmp_path / "here").mkdir()
    (tmp_path / "early").mkdir()
    m = {"stores": [
        st("live_ok", "here", "tracked"),
        st("live_missing", "gone", "tracked"),
        st("proposed_early", "early", "ignored", status="proposed"),
        st("proposed_ok", "later", "ignored", status="proposed"),
        st("retired_gone", "old", "tracked", status="retired"),
        st("unused_gone", "empty", "tracked", status="unused"),
        {"id": "ram", "base": "ram", "git": "n/a"},
    ], "kinds": {}}
    before = sorted(str(p) for p in tmp_path.rglob("*"))
    assert check_disk(m, {"homebase": str(tmp_path)}) == sorted([
        f"live store live_missing: {os.path.normpath(str(tmp_path / 'gone'))} does not exist",
        f"proposed store proposed_early: {os.path.normpath(str(tmp_path / 'early'))} already exists",
    ])
    assert sorted(str(p) for p in tmp_path.rglob("*")) == before


# ───────────────────────── git: declared state against a real repository ─────────────────────────


def _git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid", "-c", "core.autocrlf=false",
                    *args], cwd=cwd, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git is not installed")
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    (r / ".gitignore").write_text("ign/\n", encoding="utf-8")
    for folder, name in (("trk", "a.txt"), ("ign", "x.txt"), ("pub", "p.txt")):
        (r / folder).mkdir()
        (r / folder / name).write_text(name, encoding="utf-8")
    _git(r, "add", ".gitignore", "trk/a.txt", "pub/p.txt")
    _git(r, "commit", "-q", "-m", "fixture")
    (r / "trk" / "b.txt").write_text("untracked", encoding="utf-8")   # untracked and not ignored
    return r


def test_check_git_compares_declared_state_with_the_index(repo):
    m = {"stores": [
        st("tracked_ok", "pub", "tracked"),
        st("tracked_with_stray", "trk", "tracked"),
        st("ignored_ok", "ign", "ignored"),
        st("ignored_wrong", "pub", "ignored"),
    ], "kinds": {}}
    assert check_git(m, {"homebase": str(repo)}) == sorted([
        "store tracked_with_stray: declared tracked, but 1 file(s) under trk are untracked",
        "store ignored_wrong: declared ignored, but pub is not git-ignored",
        "store ignored_wrong: declared ignored, but 1 file(s) under pub are tracked",
    ])


def test_check_git_leaves_excluded_sub_stores_to_their_own_entries(repo):
    (repo / "trk" / "sub").mkdir()
    (repo / "trk" / "sub" / "c.txt").write_text("untracked too", encoding="utf-8")
    m = {"stores": [st("container", "trk", "tracked", exclude=["trk/sub"]), st("inner", "trk/sub", "tracked")], "kinds": {}}
    assert check_git(m, {"homebase": str(repo)}) == sorted([
        "store container: declared tracked, but 1 file(s) under trk are untracked",     # b.txt only; sub/ is excluded
        "store inner: declared tracked, but 1 file(s) under trk/sub are untracked",
    ])


def test_check_git_does_not_touch_the_index(repo):
    index = repo / ".git" / "index"
    before = (index.stat().st_mtime_ns, index.read_bytes())
    check_git({"stores": [st("t", "trk", "tracked")], "kinds": {}}, {"homebase": str(repo)})
    assert (index.stat().st_mtime_ns, index.read_bytes()) == before


def test_check_git_reports_a_folder_that_is_not_a_repository_top(tmp_path):
    (tmp_path / "plain").mkdir()
    findings = check_git({"stores": [st("x", "a", "tracked")], "kinds": {}}, {"homebase": str(tmp_path / "plain")})
    assert len(findings) == 1 and "is not the top of a git repository" in findings[0]


def test_check_git_reports_a_missing_git_instead_of_crashing(tmp_path):
    findings = check_git({"stores": [st("x", "a", "tracked")], "kinds": {}}, {"homebase": str(tmp_path)},
                         git="no-such-git-binary")
    assert len(findings) == 1 and "git could not read" in findings[0]


# ───────────────────────── the inventory tool ─────────────────────────


def test_inventory_tool_reports_findings_and_strict_makes_them_fail(tmp_path, capsys):
    from tools.rodin_memory_inventory import main

    home = tmp_path / "home"
    (home / "kernel_memory" / "hoard" / "raw_shards").mkdir(parents=True)
    argv = ["--homebase", str(home), "--repo", str(tmp_path / "repo"), "--claude-memory", str(tmp_path / "cm"), "--json"]
    before = sorted(str(p) for p in tmp_path.rglob("*"))

    assert main(argv) == 0                                    # findings alone do not fail the default run
    out = json.loads(capsys.readouterr().out)
    assert out["problems"] == [] and out["audit"] == audit_memory_map(MAP)
    assert any("does not exist" in f for f in out["disk"])
    assert out["git"] and all("not the top of a git repository" in f for f in out["git"])

    assert main(argv + ["--strict"]) == 1
    capsys.readouterr()
    assert main(argv + ["--no-git"]) == 0
    assert json.loads(capsys.readouterr().out)["git"] == []
    assert sorted(str(p) for p in tmp_path.rglob("*")) == before
