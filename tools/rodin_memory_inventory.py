"""
INTEGRA O/S: RODIN MEMORY INVENTORY
Module: tools/rodin_memory_inventory.py
Layer: 3 (Memory)

Measures every store in config/rodin_memory_map.yml: does it exist, how many files, how many bytes, when was the
newest file written (file metadata only). It never opens a file's content, never opens a database and creates
nothing, so it is safe to run against the live folders.

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

from memory.memory_map import inventory, load_memory_map, validate_memory_map  # noqa: E402


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
    args = parser.parse_args(argv)

    repo = Path(args.repo) if args.repo else Path(args.homebase).parent
    memory_map = load_memory_map(args.map)
    problems = validate_memory_map(memory_map)
    rows = inventory(memory_map, {
        "homebase": args.homebase,
        "repo": str(repo),
        "claude_memory": args.claude_memory or str(default_claude_memory_dir(repo)),
    })

    if args.json:
        print(json.dumps({"map_status": memory_map["status"], "problems": problems, "stores": rows}, indent=2))
    else:
        print(f"Rodin memory map ({memory_map['status']}): {len(rows)} stores, {len(problems)} problem(s)")
        for p in problems:
            print(f"  PROBLEM: {p}")
        print(f"{'store':22} {'tier':4} {'status':9} {'exists':6} {'files':>7} {'bytes':>13}  {'vis':11} {'git':12} newest file")
        for r in rows:
            exists = "ram" if r["exists"] is None else ("yes" if r["exists"] else "no")
            files = "-" if r["files"] is None else r["files"]
            size = "-" if r["bytes"] is None else f"{r['bytes']:,}"
            note = " (walk capped)" if r.get("truncated") else ""
            print(f"{r['id']:22} {r['tier']:4} {r['status']:9} {exists:6} {files!s:>7} {size:>13}  {r['visibility']:11} {r['git']:12} {r['newest_mtime'] or '-'}{note}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
