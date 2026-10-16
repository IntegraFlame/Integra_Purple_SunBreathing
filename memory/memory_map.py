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
import subprocess
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
            skip = [os.path.join(base_dir, sub) for sub in s.get("exclude", [])]
            row.update(_measure(_store_root(s, bases), skip))
        rows.append(row)
    return rows


def _store_root(s: Dict[str, Any], bases: Dict[str, str]) -> str:
    """The folder or file a store's path names, resolved against its base."""
    if s["base"] == "absolute":
        return os.path.normpath(s["path"])
    return os.path.normpath(os.path.join(bases.get(s["base"], ""), s["path"]))


# ───────────── checks validate_memory_map does not make (Brain Map T2, step 2.5, piece P3) ─────────────


def audit_memory_map(m: Dict[str, Any]) -> List[str]:
    """
    Consistency findings that validate_memory_map does not report, as sentences, sorted; an empty list means none.
    A `holds` value that is not a defined kind; a kind routed to a store whose `holds` omit it; a store that holds a
    kind which does not route to it; stores that share a path without naming each other in `shares_path_with`.
    Pure: it reads the map and nothing else. Dangling store ids are validate_memory_map's to report.
    """
    findings: List[str] = []
    stores = {s.get("id"): s for s in (m.get("stores") or [])}
    kinds = m.get("kinds") or {}
    routed: Dict[str, set] = {}
    for kind, spec in kinds.items():
        for sid in ([spec.get("primary")] if spec.get("primary") else []) + list(spec.get("also") or []):
            routed.setdefault(sid, set()).add(kind)
            if sid in stores and kind not in (stores[sid].get("holds") or []):
                findings.append(f"kind {kind} routes to store {sid}, but {sid}'s holds omit {kind!r}")
    for sid, s in stores.items():
        for kind in s.get("holds") or []:
            if kind not in kinds:
                findings.append(f"store {sid} holds {kind!r}, which is not a defined kind")
            elif kind not in routed.get(sid, set()):
                findings.append(f"store {sid} holds {kind!r}, but kind {kind} does not route to {sid}")
    by_path: Dict[Any, List[str]] = {}
    for sid, s in stores.items():
        if s.get("base") != "ram" and s.get("path"):
            by_path.setdefault((s["base"], s["path"]), []).append(sid)
    for (base, path), ids in by_path.items():
        for a in ids:
            for b in ids:
                declared = b in (stores[a].get("shares_path_with") or []) and a in (stores[b].get("shares_path_with") or [])
                if a < b and not declared:
                    findings.append(f"stores {a} and {b} share {base}:{path} without declaring shares_path_with")
    return sorted(findings)


def check_disk(m: Dict[str, Any], bases: Dict[str, str]) -> List[str]:
    """
    Declared status against the disk, from metadata only (os.path.exists): a live store whose path is missing, and a
    proposed store whose path already exists. RAM, unused and retired stores are not judged. Creates nothing.
    """
    findings: List[str] = []
    for s in m.get("stores") or []:
        if s.get("base") == "ram" or not s.get("path"):
            continue
        status, root = s.get("status", "live"), _store_root(s, bases)
        if status == "live" and not os.path.exists(root):
            findings.append(f"live store {s['id']}: {root} does not exist")
        elif status == "proposed" and os.path.exists(root):
            findings.append(f"proposed store {s['id']}: {root} already exists")
    return sorted(findings)


def _git_lines(git: str, repo: str, *args: str, stdin: Optional[str] = None) -> List[str]:
    """NUL-separated output of a read-only git command run in `repo` (no optional locks, so the index is not rewritten)."""
    cp = subprocess.run([git, "--no-optional-locks", "-C", repo, *args], input=stdin.encode("utf-8") if stdin else None,
                        capture_output=True, check=False)
    if cp.returncode not in (0, 1):   # check-ignore answers 1 when nothing is ignored
        raise RuntimeError(cp.stderr.decode("utf-8", "replace").strip() or f"git exited {cp.returncode}")
    return [p for p in cp.stdout.decode("utf-8", "replace").split("\0") if p]


def check_git(m: Dict[str, Any], bases: Dict[str, str], git: str = "git") -> List[str]:
    """
    Declared `git:` state against git's own view, read-only (ls-files, check-ignore; about four calls per repository).
    A store declared tracked may hold no untracked, not-ignored file and must not be ignored itself; a store declared
    ignored must be ignored and hold no tracked file. Sub-stores named in `exclude` are left to their own entries.
    A base that is not the top of a git repository, or that git cannot read, gives one finding instead of a crash.
    """
    findings: List[str] = []
    by_base: Dict[str, List[Dict[str, Any]]] = {}
    for s in m.get("stores") or []:
        if s.get("base") in ("homebase", "repo") and s.get("git") in ("tracked", "ignored") and s.get("path"):
            by_base.setdefault(s["base"], []).append(s)
    for base, members in sorted(by_base.items()):
        repo = bases.get(base, "")
        try:
            top = subprocess.run([git, "-C", repo, "rev-parse", "--show-toplevel"], capture_output=True, check=False)
            top_dir = top.stdout.decode("utf-8", "replace").strip()
            if top.returncode != 0 or os.path.normcase(os.path.normpath(top_dir)) != os.path.normcase(os.path.normpath(repo)):
                findings.append(f"base {base}: {repo} is not the top of a git repository")
                continue
            tracked = _git_lines(git, repo, "ls-files", "-z")
            untracked = _git_lines(git, repo, "ls-files", "-z", "--others", "--exclude-standard")
            paths = [s["path"].replace("\\", "/").rstrip("/") for s in members]
            ignored = set(_git_lines(git, repo, "check-ignore", "-z", "--stdin", stdin="\0".join(paths) + "\0"))
        except (OSError, RuntimeError) as exc:
            findings.append(f"base {base}: git could not read {repo}: {exc}")
            continue

        def under(files: List[str], s: Dict[str, Any]) -> int:
            root = s["path"].replace("\\", "/").rstrip("/")
            skip = [x.replace("\\", "/").rstrip("/") + "/" for x in s.get("exclude", [])]
            return sum(1 for f in files if (f == root or f.startswith(root + "/")) and not any(f.startswith(x) for x in skip))

        for s in members:
            path = s["path"].replace("\\", "/").rstrip("/")
            if s["git"] == "tracked":
                if path in ignored:
                    findings.append(f"store {s['id']}: declared tracked, but {path} is git-ignored")
                n = under(untracked, s)
                if n:
                    findings.append(f"store {s['id']}: declared tracked, but {n} file(s) under {path} are untracked")
            else:
                if path not in ignored:
                    findings.append(f"store {s['id']}: declared ignored, but {path} is not git-ignored")
                n = under(tracked, s)
                if n:
                    findings.append(f"store {s['id']}: declared ignored, but {n} file(s) under {path} are tracked")
    return sorted(findings)
