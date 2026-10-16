"""
INTEGRA O/S: RODIN MEMORY INVENTORY
Module: tools/rodin_memory_inventory.py
Layer: 3 (Memory)

Measures every store in config/rodin_memory_map.yml: does it exist, how many files, how many bytes, when was the
newest file written (file metadata only). It never opens a file's content, never opens a database and creates
nothing, so it is safe to run against the live folders. It also reports what validate_memory_map does not check:
the map's own holds/kinds consistency (audit), declared status against the disk, and declared `git:` state against
a read-only git (`--no-git` skips that; `--strict` makes any of these findings fail the run).

Usage (from integra-homebase):
    python tools/rodin_memory_inventory.py            # table
    python tools/rodin_memory_inventory.py --json     # machine-readable
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Optional

HOMEBASE_DIR = Path(__file__).resolve().parent.parent
if str(HOMEBASE_DIR) not in sys.path:
    sys.path.insert(0, str(HOMEBASE_DIR))

from memory.memory_map import (  # noqa: E402
    audit_memory_map,
    check_disk,
    check_git,
    inventory,
    load_memory_map,
    validate_memory_map,
)


def default_claude_memory_dir(repo: Path) -> Path:
    """Claude Code names a project's folder after its path with every non-alphanumeric character turned into '-'."""
    return Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(repo)) / "memory"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Measure the stores in the Rodin memory map (metadata only; read-only).")
    parser.add_argument("--homebase", default=str(HOMEBASE_DIR), help="the integra-homebase folder")
    parser.add_argument("--repo", default=None, help="the root repo folder (default: the parent of --homebase)")
    parser.add_argument("--claude-memory", default=None, help="the assistant's memory folder (default: derived from --repo)")
    parser.add_argument("--map", default=None, help="a memory map file (default: config/rodin_memory_map.yml)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    parser.add_argument("--strict", action="store_true", help="exit 1 on any audit, disk or git finding, not only on problems")
    parser.add_argument("--no-git", action="store_true", help="skip the read-only git check")
    args = parser.parse_args(argv)

    repo = Path(args.repo) if args.repo else Path(args.homebase).parent
    memory_map = load_memory_map(args.map)
    problems = validate_memory_map(memory_map)
    bases = {
        "homebase": args.homebase,
        "repo": str(repo),
        "claude_memory": args.claude_memory or str(default_claude_memory_dir(repo)),
    }
    rows = inventory(memory_map, bases)
    audit = audit_memory_map(memory_map)
    disk = check_disk(memory_map, bases)
    git = [] if args.no_git else check_git(memory_map, bases)

    if args.json:
        print(json.dumps({"map_status": memory_map["status"], "problems": problems, "audit": audit, "disk": disk,
                          "git": git, "stores": rows}, indent=2))
    else:
        print(f"Rodin memory map ({memory_map['status']}): {len(rows)} stores, {len(problems)} problem(s), "
              f"{len(audit)} audit, {len(disk)} disk and {len(git)} git finding(s)")
        for p in problems:
            print(f"  PROBLEM: {p}")
        for label, found in (("AUDIT", audit), ("DISK", disk), ("GIT", git)):
            for f in found:
                print(f"  {label}: {f}")
        print(f"{'store':22} {'tier':4} {'status':9} {'exists':6} {'files':>7} {'bytes':>13}  {'vis':11} {'git':12} newest file")
        for r in rows:
            exists = "ram" if r["exists"] is None else ("yes" if r["exists"] else "no")
            files = "-" if r["files"] is None else r["files"]
            size = "-" if r["bytes"] is None else f"{r['bytes']:,}"
            note = " (walk capped)" if r.get("truncated") else ""
            print(f"{r['id']:22} {r['tier']:4} {r['status']:9} {exists:6} {files!s:>7} {size:>13}  {r['visibility']:11} {r['git']:12} {r['newest_mtime'] or '-'}{note}")
    return 1 if problems or (args.strict and (audit or disk or git)) else 0


if __name__ == "__main__":
    sys.exit(main())
