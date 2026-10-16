"""
INTEGRA O/S: RODIN MEMORY MAP
Module: memory/memory_map.py
Layer: 3 (Memory)

Rodin's memory-mapping role: one declared answer to "where does this kind of knowledge live, what indexes it,
and where must it never go". The data is config/rodin_memory_map.yml; this module loads it, checks it, answers
place(kind), and measures the stores (sizes and counts only: it never opens a file's content and creates nothing).

The map DESCRIBES. It moves no data. Every move it proposes (ADR-005) needs the Architect's approval.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

TIERS = ("W", "H", "C", "L", "R", "S", "A", "D", "I")
VISIBILITY = ("public-repo", "local-only")
GIT_STATES = ("tracked", "ignored", "outside-repo", "n/a")
BASES = ("homebase", "repo", "claude_memory", "absolute", "ram")
STATUSES = ("live", "unused", "retired", "proposed")
REQUIRED_STORE_FIELDS = ("id", "tier", "base", "visibility", "git", "source_of_truth", "holds", "writer")
MAX_ENTRIES_WALKED = 300_000


def default_map_path() -> Path:
    return Path(__file__).resolve().parent.parent / "config" / "rodin_memory_map.yml"


def load_memory_map(path: Optional[str] = None) -> Dict[str, Any]:
    with open(path or default_map_path(), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_memory_map(m: Dict[str, Any]) -> List[str]:
    """Every problem found, as a sentence. An empty list means the map is consistent."""
    problems: List[str] = []
    stores = m.get("stores") or []
    kinds = m.get("kinds") or {}
    by_id: Dict[str, Dict[str, Any]] = {}

    for s in stores:
        sid = s.get("id", "<missing id>")
        for field in REQUIRED_STORE_FIELDS:
            if field not in s:
                problems.append(f"store {sid}: missing field {field!r}")
        if sid in by_id:
            problems.append(f"duplicate store id {sid!r}")
        by_id[sid] = s
        if s.get("tier") not in TIERS:
            problems.append(f"store {sid}: unknown tier {s.get('tier')!r}")
        if s.get("base") not in BASES:
            problems.append(f"store {sid}: unknown base {s.get('base')!r}")
        if s.get("visibility") not in VISIBILITY:
            problems.append(f"store {sid}: unknown visibility {s.get('visibility')!r}")
        if s.get("git") not in GIT_STATES:
            problems.append(f"store {sid}: unknown git state {s.get('git')!r}")
        if s.get("status", "live") not in STATUSES:
            problems.append(f"store {sid}: unknown status {s.get('status')!r}")
        if s.get("base") != "ram" and not s.get("path"):
            problems.append(f"store {sid}: a store outside RAM needs a path")
        if s.get("visibility") == "public-repo" and s.get("git") != "tracked":
            problems.append(f"store {sid}: visibility public-repo contradicts git state {s.get('git')!r} (it must be tracked)")
        if s.get("visibility") == "local-only" and s.get("git") == "tracked":
            problems.append(f"store {sid}: visibility local-only contradicts git state 'tracked' (a tracked file is published)")
        if s.get("tier") == "H" and s.get("source_of_truth"):
            problems.append(f"store {sid}: a hot index is derived and cannot be the source of truth")

    for kind, spec in kinds.items():
        primary = spec.get("primary")
        also = list(spec.get("also") or [])
        for sid in ([primary] if primary else []) + also:
            if sid not in by_id:
                problems.append(f"kind {kind}: store {sid!r} is not defined")
        if primary is None and not spec.get("never"):
            problems.append(f"kind {kind}: no primary store and no 'never' reason")
        if kind in ("conversation_archive", "secret"):
            for sid in ([primary] if primary else []) + also:
                if sid in by_id and by_id[sid].get("visibility") != "local-only":
                    problems.append(f"kind {kind}: store {sid!r} is public; this kind must stay in local-only stores")
        if kind == "secret" and (primary or also):
            problems.append("kind secret: secrets must not live in any memory store")
    return problems


def place(kind: str, m: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Where a kind of knowledge goes: its primary store, the stores that also hold or index it, whether it is embedded."""
    m = m or load_memory_map()
    spec = (m.get("kinds") or {}).get(kind)
    if spec is None:
        raise KeyError(f"unknown kind {kind!r}; known kinds: {sorted(m.get('kinds') or {})}")
    stores = {s["id"]: s for s in m["stores"]}
    primary = spec.get("primary")
    return {
        "kind": kind,
        "primary": primary,
        "also": list(spec.get("also") or []),
        "embed": bool(spec.get("embed", False)),
        "visibility": stores[primary]["visibility"] if primary else None,
        "never": spec.get("never"),
        "description": spec.get("description", ""),
    }


def _measure(path: str, exclude: Optional[List[str]] = None) -> Dict[str, Any]:
    """exists / files / bytes / newest mtime for a file or folder, from file metadata only. `exclude` skips sub-folders that are stores of their own."""
    if not os.path.exists(path):
        return {"exists": False, "files": 0, "bytes": 0, "newest_mtime": None, "truncated": False}
    if os.path.isfile(path):
        st = os.stat(path)
        return {"exists": True, "files": 1, "bytes": st.st_size, "truncated": False,
                "newest_mtime": datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(timespec="seconds")}
    skip = {os.path.normcase(os.path.normpath(p)) for p in (exclude or [])}
    files = total = seen = 0
    newest = 0.0
    truncated = False
    stack = [path]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    seen += 1
                    if seen > MAX_ENTRIES_WALKED:
                        truncated = True
                        stack.clear()
                        break
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            if os.path.normcase(os.path.normpath(entry.path)) not in skip:
                                stack.append(entry.path)
                        elif entry.is_file(follow_symlinks=False):
                            st = entry.stat(follow_symlinks=False)
                            files += 1
                            total += st.st_size
                            newest = max(newest, st.st_mtime)
                    except OSError:
                        continue
        except OSError:
            continue
    return {"exists": True, "files": files, "bytes": total, "truncated": truncated,
            "newest_mtime": datetime.fromtimestamp(newest).astimezone().isoformat(timespec="seconds") if newest else None}


def inventory(m: Dict[str, Any], bases: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    One row per store with what is on disk. `bases` maps homebase / repo / claude_memory to folders. RAM stores
    have nothing to measure (exists None). Reads file metadata only; never opens content; creates nothing.
    """
    rows: List[Dict[str, Any]] = []
    for s in m["stores"]:
        row: Dict[str, Any] = {
            "id": s["id"], "tier": s["tier"], "base": s["base"], "path": s.get("path"),
            "status": s.get("status", "live"), "visibility": s["visibility"], "git": s["git"],
            "source_of_truth": s["source_of_truth"], "onedrive": s.get("onedrive"),
        }
        if s["base"] == "ram":
            row.update({"exists": None, "files": None, "bytes": None, "newest_mtime": None, "truncated": False})
        else:
            base_dir = "" if s["base"] == "absolute" else bases.get(s["base"], "")
            root = s["path"] if s["base"] == "absolute" else os.path.join(base_dir, s["path"])
            skip = [os.path.join(base_dir, sub) for sub in s.get("exclude", [])]
            row.update(_measure(os.path.normpath(root), skip))
        rows.append(row)
    return rows
