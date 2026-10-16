"""
INTEGRA O/S: RODIN MEMORY MAP TEST SUITE (offline)

config/rodin_memory_map.yml says where each kind of knowledge lives and where it must never go (Rodin's memory-mapping
role; ADR-005). These tests keep the map honest in three ways: it is internally consistent, it enforces the privacy
rules the Architect set (archive content and secrets never reach a public store), and it agrees with the code it
describes (shard folder, Chroma folder, collection name). The map describes; it moves nothing.
"""

import copy
import os

import pytest

from memory.embedding_service import EmbeddingSpace
from memory.memory_map import (
    default_map_path,
    inventory,
    load_memory_map,
    place,
    validate_memory_map,
)
from memory.the_hoard import TheHoard

MAP = load_memory_map()


def store(m, store_id):
    return next(s for s in m["stores"] if s["id"] == store_id)


# ───────────────────────── the shipped map ─────────────────────────


def test_the_shipped_map_is_valid():
    assert validate_memory_map(MAP) == []
    assert default_map_path().name == "rodin_memory_map.yml" and MAP["status"] == "PROPOSED"


def test_the_map_agrees_with_the_code_it_describes():
    raw = store(MAP, "raw_shards")
    assert raw["path"] == "kernel_memory/" + next(d for d in TheHoard.KERNEL_DIRS if d.endswith("raw_shards"))
    chroma = store(MAP, "chroma_active")
    assert chroma["path"] == "local_dbs/chroma_storage"
    assert chroma["collection"] == EmbeddingSpace().collection_name()
    assert MAP["embedding_space"] == EmbeddingSpace().id
    assert store(MAP, "chroma_legacy")["collection"] == "integra_hoard"


def test_every_hoard_directory_is_accounted_for():
    mapped = {s["path"] for s in MAP["stores"] if s.get("base") == "homebase" and s.get("path", "").startswith("kernel_memory/")}
    for d in TheHoard.KERNEL_DIRS:
        assert "kernel_memory/" + d in mapped, f"{d} has no store in the map"


# ───────────────────────── placement ─────────────────────────


def test_place_answers_where_each_kind_of_knowledge_goes():
    node = place("node")
    assert node["primary"] == "raw_shards" and "chroma_active" in node["also"] and node["embed"] is True
    chunk = place("lobe_chunk")
    assert chunk["primary"] == "chroma_active" and chunk["embed"] is True
    archive = place("conversation_archive")
    assert archive["primary"] == "antigravity_archive" and archive["visibility"] == "local-only"
    assert place("ruling")["primary"] == "docs_blueprint"
    assert place("working_context")["primary"] == "rolling_context"


def test_secrets_have_no_home_in_any_memory_store():
    secret = place("secret")
    assert secret["primary"] is None and secret["also"] == [] and secret["never"]


def test_an_unknown_kind_is_a_loud_error():
    with pytest.raises(KeyError) as exc:
        place("gossip")
    assert "node" in str(exc.value)


# ───────────────────────── the privacy rules, enforced ─────────────────────────


def test_conversation_archive_content_never_maps_to_a_public_store():
    for kind in ("conversation_archive", "secret"):
        spec = MAP["kinds"][kind]
        for sid in [spec.get("primary"), *spec.get("also", [])]:
            if sid:
                assert store(MAP, sid)["visibility"] == "local-only"


def test_validator_rejects_an_archive_kind_pointed_at_a_public_store():
    bad = copy.deepcopy(MAP)
    bad["kinds"]["conversation_archive"]["also"] = ["raw_shards"]
    problems = validate_memory_map(bad)
    assert any("conversation_archive" in p and "public" in p for p in problems)


def test_validator_rejects_a_secret_with_a_home_even_a_local_one():
    bad = copy.deepcopy(MAP)
    bad["kinds"]["secret"]["primary"] = "claude_memory_index"          # local-only, so only the "no home" rule can object
    assert any("secrets must not live" in p for p in validate_memory_map(bad))
    worse = copy.deepcopy(MAP)
    worse["kinds"]["secret"]["primary"] = "raw_shards"                  # public as well
    assert any("secret" in p and "public" in p for p in validate_memory_map(worse))


def test_validator_rejects_visibility_that_contradicts_git_state():
    bad = copy.deepcopy(MAP)
    store(bad, "chroma_active")["visibility"] = "public-repo"        # it is git-ignored
    assert any("chroma_active" in p and "git" in p for p in validate_memory_map(bad))


def test_validator_rejects_duplicate_ids_unknown_tiers_and_dangling_stores():
    bad = copy.deepcopy(MAP)
    bad["stores"].append(copy.deepcopy(bad["stores"][0]))
    store(bad, "raw_shards")["tier"] = "Z"
    bad["kinds"]["node"]["also"] = ["no_such_store"]
    problems = " | ".join(validate_memory_map(bad))
    assert "duplicate" in problems and "tier" in problems and "no_such_store" in problems


def test_a_derived_index_is_never_the_source_of_truth():
    bad = copy.deepcopy(MAP)
    store(bad, "chroma_active")["source_of_truth"] = True
    assert any("chroma_active" in p and "source" in p for p in validate_memory_map(bad))


# ───────────────────────── inventory: measure, never read content ─────────────────────────


def test_inventory_measures_sizes_without_reading_or_creating_anything(tmp_path):
    home = tmp_path / "home"
    (home / "kernel_memory" / "hoard" / "raw_shards").mkdir(parents=True)
    (home / "kernel_memory" / "hoard" / "raw_shards" / "A.json").write_text("{}", encoding="utf-8")
    (home / "kernel_memory" / "hoard" / "raw_shards" / "B.json").write_text("{ }", encoding="utf-8")
    (home / "kernel_memory" / "rolling_context.json").write_text("{}", encoding="utf-8")
    before = sorted(str(p) for p in tmp_path.rglob("*"))

    rows = {r["id"]: r for r in inventory(MAP, {"homebase": str(home), "repo": str(tmp_path / "repo"),
                                                "claude_memory": str(tmp_path / "cm")})}
    assert rows["raw_shards"]["exists"] is True and rows["raw_shards"]["files"] == 2 and rows["raw_shards"]["bytes"] == 5
    assert rows["rolling_context"]["exists"] is True and rows["rolling_context"]["files"] == 1
    assert rows["chroma_active"]["exists"] is False and rows["antigravity_archive"]["exists"] is False
    assert rows["ram_embedding_cache"]["exists"] is None                  # RAM stores have no path to measure
    assert sorted(str(p) for p in tmp_path.rglob("*")) == before


def test_a_store_that_contains_other_stores_does_not_count_them_twice(tmp_path):
    repo = tmp_path / "repo"
    (repo / "The Hoard" / "antigravity_conversations").mkdir(parents=True)
    (repo / "The Hoard" / "Slow-Wave Deep Sleep Reports").mkdir(parents=True)
    (repo / "The Hoard" / "CCID_1.md").write_text("abc", encoding="utf-8")
    (repo / "The Hoard" / "antigravity_conversations" / "x.md").write_text("0123456789", encoding="utf-8")
    (repo / "The Hoard" / "Slow-Wave Deep Sleep Reports" / "r.md").write_text("zz", encoding="utf-8")
    rows = {r["id"]: r for r in inventory(MAP, {"homebase": str(tmp_path / "h"), "repo": str(repo), "claude_memory": str(tmp_path / "c")})}
    assert rows["save_states_root"]["files"] == 1 and rows["save_states_root"]["bytes"] == 3
    assert rows["antigravity_archive"]["bytes"] == 10 and rows["swds_reports"]["bytes"] == 2


def test_every_exclusion_names_another_store_inside_the_container():
    by_path = {(s["base"], s.get("path")) for s in MAP["stores"]}
    for s in MAP["stores"]:
        for sub in s.get("exclude", []):
            assert (s["base"], sub) in by_path, f"{s['id']} excludes {sub!r}, which no store describes"
            assert sub.startswith(s["path"]), f"{sub!r} is not inside {s['path']!r}"


def test_inventory_tool_prints_json_and_creates_nothing(tmp_path, capsys):
    import json

    from tools.rodin_memory_inventory import default_claude_memory_dir, main

    home = tmp_path / "home"
    (home / "kernel_memory" / "hoard" / "raw_shards").mkdir(parents=True)
    before = sorted(str(p) for p in tmp_path.rglob("*"))
    code = main(["--homebase", str(home), "--repo", str(tmp_path / "repo"), "--claude-memory", str(tmp_path / "cm"), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0 and out["problems"] == [] and out["map_status"] == "PROPOSED"
    assert {r["id"] for r in out["stores"]} >= {"raw_shards", "chroma_active", "antigravity_archive", "memory_db"}
    assert sorted(str(p) for p in tmp_path.rglob("*")) == before
    assert str(default_claude_memory_dir(tmp_path / "repo")).endswith("memory")


def test_claude_memory_folder_name_follows_claude_codes_rule():
    from pathlib import Path

    from tools.rodin_memory_inventory import default_claude_memory_dir

    p = default_claude_memory_dir(Path(r"C:\Users\Some One\OneDrive\Desktop\My_Project"))   # a made-up path: every non-alphanumeric becomes '-'
    assert p.parent.name == "C--Users-Some-One-OneDrive-Desktop-My-Project"


def test_inventory_marks_proposed_stores_and_does_not_invent_them(tmp_path):
    rows = {r["id"]: r for r in inventory(MAP, {"homebase": str(tmp_path), "repo": str(tmp_path), "claude_memory": str(tmp_path)})}
    assert rows["memory_db"]["status"] == "proposed" and isinstance(rows["memory_db"]["exists"], bool)
    assert not os.path.exists(os.path.join(str(tmp_path), "memory.db"))
