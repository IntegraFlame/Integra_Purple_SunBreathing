"""
INTEGRA O/S: RODIN RE-EMBED TOOL
Module: tools/rodin_reembed.py
Layer: 3 (Memory)

Moves the Hoard's shards into the current embedding space (gemini-embedding-2, 768-d, "asym-v1" text format).
Why it is needed (MEASURED 2026-10-15 on copies of the live stores): of 307 shards, 257 held all-zero vectors,
4 held SHA-256 pseudo-vectors and 41 held unit-length pseudo-vectors (40 of them Daily Planet reports, whose routine builds
them from SHA-512); none came from a model. ADR-005 action 5.

Safety, in order:
  1. The DEFAULT is a read-only plan: it reads the shard files and prints counts, duplicates, tokens and price.
     It builds no Hoard, opens no database and creates nothing.
  2. A real run needs BOTH --apply and --yes-paid. It spends money (gemini-embedding-2: $0.20 per 1M tokens
     standard, $0.10 batch, pricing page 2026-10-15). Use the paid tier for private content: the pricing page marks the
     free tier "used to improve our products".
  3. Identical (text, title) pairs are embedded once; --limit N makes a pilot run; the first failure stops the run
     and the receipt says what was finished; each shard is replaced atomically, only after its vector arrived,
     and only its three embedding keys change.

Usage (from integra-homebase):
    python tools/rodin_reembed.py --root .                         # plan only
    python tools/rodin_reembed.py --root . --apply --yes-paid --limit 20   # a 20-text pilot
    python tools/rodin_reembed.py --root . --apply --yes-paid      # everything pending
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Optional

HOMEBASE_DIR = Path(__file__).resolve().parent.parent
if str(HOMEBASE_DIR) not in sys.path:
    sys.path.insert(0, str(HOMEBASE_DIR))

from memory.embedding_service import get_operator_embedding_service  # noqa: E402
from memory.the_hoard import TheHoard, load_nodes_from_shards, plan_embedding  # noqa: E402


def main(argv: Optional[List[str]] = None, embedder=None) -> int:
    parser = argparse.ArgumentParser(description="Embed the Hoard's shards in the current embedding space. A read-only plan unless --apply --yes-paid.")
    parser.add_argument("--root", default=str(HOMEBASE_DIR), help="the integra-homebase folder (holds kernel_memory/hoard/raw_shards)")
    parser.add_argument("--apply", action="store_true", help="embed for real (paid API calls); also needs --yes-paid")
    parser.add_argument("--yes-paid", action="store_true", help="confirm that this run may spend money")
    parser.add_argument("--limit", type=int, default=None, help="embed at most this many unique texts (a pilot run)")
    parser.add_argument("--batch-size", type=int, default=16, help="unique texts per request")
    parser.add_argument("--pause-s", type=float, default=0.5, help="seconds to wait between requests (pacing; a free key has rate limits)")
    args = parser.parse_args(argv)

    shards_dir = os.path.join(args.root, "kernel_memory", "hoard", "raw_shards")
    if not os.path.isdir(shards_dir):
        print(f"ERROR: no raw_shards folder at {shards_dir}")
        return 2
    if args.apply and not args.yes_paid:
        print("REFUSED: --apply spends money. Add --yes-paid to confirm, or drop --apply for the read-only plan.")
        return 2

    service = embedder or get_operator_embedding_service()

    if not args.apply:
        nodes, report = load_nodes_from_shards(shards_dir)
        plan = plan_embedding(nodes, service.space, limit=args.limit)
        plan["shard_files"] = report
        print("PLAN ONLY (read-only): nothing was embedded, written or created. To run for real add --apply --yes-paid (paid API calls).")
        print(json.dumps(plan, indent=2))
        return 0

    hoard = TheHoard(base_dir=args.root, embedder=service)
    hoard.load_shards_from_disk()
    receipt = hoard.embed_pending(dry_run=False, limit=args.limit, batch_size=args.batch_size, pause_s=args.pause_s)
    receipt["shard_files"] = hoard.last_load_report
    if receipt["stopped_early"]:
        print(f"STOPPED EARLY: {receipt['error']}. {receipt['embedded']} node(s) were embedded before the stop; the rest are unchanged.")
    print("RECEIPT" + json.dumps(receipt, indent=2))  # the JSON is always the last thing printed
    return 1 if receipt["stopped_early"] or receipt["shard_errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
