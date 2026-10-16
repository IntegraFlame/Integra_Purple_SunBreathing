"""
INTEGRA O/S: MULTI-LOBE IN-PLACE KNOWLEDGE INGESTION & THE HOARD CHROMADB PIPELINE
Script: scripts/ingest_knowledge.py
Layer: 3 (The Hoard / Geometric Memory Substrate)
Status: PRODUCTION IMPLEMENTATION (real embeddings, plan-first)

Architecture:
    Executes the 12th Step Orthogonal Ingestion across 4 physical lobes:
    1. Guidebooks_and_Notes                 -> operational_guidance
    2. BluprintArchitecture                 -> architecture
    3. Integra Self-Reflect and Think Forward -> evolution_reflection
    4. CODE                                 -> genesis_code

    Guarantees:
    - IN-PLACE: Zero physical folder flattening or moving.
    - PLAN FIRST: a default run only scans, chunks, deduplicates and prices. It embeds and writes nothing.
      `--apply` embeds the new or changed chunks with the real model (paid API calls) and indexes them in the
      active embedding space; chunks already indexed with the same text are skipped.
    - NO FAKE VECTORS: every vector comes from gemini-embedding-2 (memory/embedding_service.py) or the run stops
      and says why. The earlier SHA-256 pseudo-vectors are gone.
    - SAFE HYGIENE (opt-in): `--clean-first` lists what the hygiene step would remove (a dry run);
      `--apply-hygiene` actually deletes. Nothing is deleted by default.
      - Duplicate 85.75 MB .m4a audio file in 'Integra Self-Reflect and Think Forward'
        (canonical preserved in Audio_Lectures/).
      - 0-byte dummy files (e.g. Template to connect  Integra components.py).
      - Exact identical .txt duplicates where corresponding .md file exists.
    - 4-PASS MANIFOLD:
      - Pass 1 (Structure / Eagle Lens): Document hierarchy & perimeter mapping.
      - Pass 2 (Middle-Out / Chameleon Lens): Semantic chunking with overlap to eliminate attention dip.
      - Pass 3 (Density / Snake Lens): the chunk's embedding (768-d; documents use the "title | text" format).
      - Pass 4 (Synthesis / Owl Lens): Upsert into the active-space ChromaDB collection.
"""

import os
import sys
import json
import time
import argparse
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# Add integra-homebase to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
HOMEBASE_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(HOMEBASE_DIR))

from memory.embedding_service import (
    EmbeddingUnavailable,
    approx_tokens,
    estimate_cost_usd,
    get_operator_embedding_service,
)
from memory.the_hoard import TheHoard, HoardNode
from temporal.celestial_clock import DualTemporalEngine

# Root directory of the entire Integra_Purple_SunBreathing workspace
WORKSPACE_ROOT = HOMEBASE_DIR.parent

# 4 In-Place Lobes definition
LOBE_CONFIG = {
    "BluprintArchitecture": {
        "lobe": "architecture",
        "extensions": [".md", ".txt"],
        "description": "Master blueprints, architectural specs, and system guides",
        "layer": 2
    },
    "CODE": {
        "lobe": "genesis_code",
        "extensions": [".md", ".py", ".sql", ".rs", ".json", ".txt"],
        "description": "Kernel source code, hypervisors, schemas, and algorithms",
        "layer": 1
    },
    "Integra Self-Reflect and Think Forward": {
        "lobe": "evolution_reflection",
        "extensions": [".md", ".txt"],
        "description": "Metacognitive evolution, self-reflections, and domain expansions",
        "layer": 6
    },
    "Guidebooks_and_Notes": {
        "lobe": "operational_guidance",
        "extensions": [".md", ".txt"],
        "description": "Operational guidebooks, CLI references, and tactical playbooks",
        "layer": 4
    }
}

SHIVA_LENSES = (
    "Neji_Eagle (Structure)",
    "Chameleon (Middle-Out)",
    "Snake (Density/Kaigaku)",
    "Owl (Truth Synthesis)",
)


def compute_file_hash(path: Path) -> str:
    """Computes SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def perform_safe_hygiene(
    workspace_root: Optional[Path] = None,
    lobe_config: Optional[Dict[str, Any]] = None,
    dry_run: bool = True,
) -> Dict[str, Any]:
    """
    Safe file hygiene across the lobes. A DRY RUN by default: it lists what it would remove and deletes nothing.
    With dry_run=False it deletes:
    1. The duplicate .m4a audio file in 'Integra Self-Reflect and Think Forward'
       (canonical remains in Audio_Lectures/).
    2. 0-byte files.
    3. Exact identical .txt duplicates where a corresponding .md exists.
    """
    root = Path(workspace_root) if workspace_root else WORKSPACE_ROOT
    lobes = lobe_config if lobe_config is not None else LOBE_CONFIG
    results = {
        "dry_run": dry_run,
        "removed_m4a_duplicate": None,
        "removed_zero_byte_files": [],
        "removed_txt_duplicates": [],
        "bytes_freed": 0
    }
    verb = "WOULD REMOVE" if dry_run else "Removed"

    def remove(path: Path) -> None:
        if not dry_run:
            path.unlink()

    # 1. Check duplicate .m4a
    m4a_target = root / "Integra Self-Reflect and Think Forward" / "The_neuro-evolutionary_architecture_of_Integra_OS.m4a"
    m4a_canonical = root / "Audio_Lectures" / "The_neuro-evolutionary_architecture_of_Integra_OS.m4a"

    if m4a_target.exists() and m4a_canonical.exists():
        size_target = m4a_target.stat().st_size
        size_canon = m4a_canonical.stat().st_size
        if size_target == size_canon and size_target > 10_000_000:  # ~85.75 MB
            try:
                remove(m4a_target)
                results["removed_m4a_duplicate"] = str(m4a_target.relative_to(root))
                results["bytes_freed"] += size_target
                print(f"[HYGIENE] {verb} duplicate audio: {results['removed_m4a_duplicate']} ({size_target:,} bytes)")
            except Exception as e:
                print(f"[HYGIENE WARNING] Failed to remove duplicate audio: {e}")

    # 2. Check 0-byte files in the lobes
    for lobe_dir_name in lobes.keys():
        lobe_path = root / lobe_dir_name
        if not lobe_path.exists():
            continue
        for item in lobe_path.rglob("*"):
            if item.is_file() and item.stat().st_size == 0:
                try:
                    rel_name = str(item.relative_to(root))
                    remove(item)
                    results["removed_zero_byte_files"].append(rel_name)
                    print(f"[HYGIENE] {verb} 0-byte dummy file: {rel_name}")
                except Exception as e:
                    print(f"[HYGIENE WARNING] Could not remove 0-byte file {item}: {e}")

    # 3. Check identical .txt duplicates where .md exists in the same folder
    for lobe_dir_name in lobes.keys():
        lobe_path = root / lobe_dir_name
        if not lobe_path.exists():
            continue
        for txt_file in list(lobe_path.rglob("*.txt")):
            if not txt_file.exists():
                continue
            md_file = txt_file.with_suffix(".md")
            if md_file.exists():
                txt_hash = compute_file_hash(txt_file)
                md_hash = compute_file_hash(md_file)
                if txt_hash == md_hash:
                    size = txt_file.stat().st_size
                    try:
                        rel_name = str(txt_file.relative_to(root))
                        remove(txt_file)
                        results["removed_txt_duplicates"].append(rel_name)
                        results["bytes_freed"] += size
                        print(f"[HYGIENE] {verb} identical .txt duplicate: {rel_name} ({size:,} bytes)")
                    except Exception as e:
                        print(f"[HYGIENE WARNING] Could not remove txt duplicate {txt_file}: {e}")

        # Also check special typo duplicates
        typo_file = lobe_path / "HowToThin_Historical.txt"
        correct_file = lobe_path / "HowToThink_Historical.txt"
        if typo_file.exists() and correct_file.exists():
            if compute_file_hash(typo_file) == compute_file_hash(correct_file):
                size = typo_file.stat().st_size
                remove(typo_file)
                results["removed_txt_duplicates"].append(str(typo_file.relative_to(root)))
                results["bytes_freed"] += size
                print(f"[HYGIENE] {verb} typo duplicate: {typo_file.name}")

        # Also check learning_proposal.txt vs learning_proposal09162026.md
        prop_txt = lobe_path / "learning_proposal.txt"
        prop_md = lobe_path / "learning_proposal09162026.md"
        if prop_txt.exists() and prop_md.exists():
            if compute_file_hash(prop_txt) == compute_file_hash(prop_md):
                size = prop_txt.stat().st_size
                remove(prop_txt)
                results["removed_txt_duplicates"].append(str(prop_txt.relative_to(root)))
                results["bytes_freed"] += size
                print(f"[HYGIENE] {verb} duplicate learning_proposal.txt")

    return results


def chunk_document(
    content: str,
    chunk_size: int = 1500,
    overlap: int = 250
) -> List[Dict[str, Any]]:
    """
    Semantic chunking with sliding window overlap.
    Preserves section header context and paragraph integrity.
    """
    if not content or not content.strip():
        return []

    # Split by markdown headers or double newlines
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [content.strip()]

    chunks = []
    current_chunk = ""
    current_header = ""

    for p in paragraphs:
        if p.startswith("#"):
            current_header = p.split("\n")[0][:80]

        if len(current_chunk) + len(p) + 2 <= chunk_size:
            current_chunk = f"{current_chunk}\n\n{p}".strip()
        else:
            if current_chunk:
                chunks.append({
                    "text": current_chunk,
                    "header": current_header
                })
                # Sliding overlap from previous chunk
                overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                current_chunk = f"{overlap_text}\n\n{p}".strip()
            else:
                # Individual paragraph exceeds chunk_size — chunk by character window
                for i in range(0, len(p), chunk_size - overlap):
                    sub = p[i:i + chunk_size]
                    chunks.append({
                        "text": sub,
                        "header": current_header
                    })
                current_chunk = ""

    if current_chunk:
        chunks.append({
            "text": current_chunk,
            "header": current_header
        })

    return chunks


class MultiLobeIngestionEngine:
    """
    Orchestrates the 12th Step Orthogonal Ingestion into The Hoard's ChromaDB.
    """
    BATCH = 16

    def __init__(
        self,
        hoard: Optional[TheHoard] = None,
        embedder: Any = None,
        workspace_root: Optional[Path] = None,
        lobe_config: Optional[Dict[str, Any]] = None,
    ):
        self.hoard = hoard or TheHoard()
        self.embedder = embedder
        self.workspace_root = Path(workspace_root) if workspace_root else WORKSPACE_ROOT
        self.lobe_config = lobe_config if lobe_config is not None else LOBE_CONFIG
        self.clock = DualTemporalEngine()
        self._sleep = time.sleep
        self.stats = self._fresh_stats()

    @staticmethod
    def _fresh_stats() -> Dict[str, Any]:
        return {
            "files_scanned": 0,
            "files_ingested": 0,
            "total_chunks": 0,
            "duplicate_chunks_skipped": 0,
            "total_chars": 0,
            "by_lobe": {},
            "chroma_persisted": 0
        }

    def _scan(self, limit_files: Optional[int]) -> List[Dict[str, Any]]:
        """Passes 1-2: walk the lobes in place, chunk, drop exact duplicate chunks, name every chunk."""
        pending: List[Dict[str, Any]] = []
        seen_ids = set()
        seen_text = set()
        files_taken = 0

        for lobe_dir_name, config in self.lobe_config.items():
            lobe_path = self.workspace_root / lobe_dir_name
            lobe_tag = config["lobe"]
            self.stats["by_lobe"][lobe_tag] = {"files": 0, "chunks": 0, "chars": 0}

            if not lobe_path.exists():
                print(f"[WARNING] Lobe directory missing: {lobe_path}")
                continue

            print(f"\n[LOBE: {lobe_tag.upper()}] Scanning: {lobe_dir_name}")
            valid_exts = set(config["extensions"])

            for file_path in sorted(lobe_path.rglob("*")):
                if not file_path.is_file():
                    continue
                if file_path.suffix.lower() not in valid_exts:
                    continue
                if limit_files is not None and files_taken >= limit_files:
                    break

                self.stats["files_scanned"] += 1
                rel_path = file_path.relative_to(self.workspace_root)

                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                except Exception as e:
                    print(f"  [SKIP] Error reading {rel_path}: {e}")
                    continue

                if not content.strip():
                    continue

                chunks = chunk_document(content)
                if not chunks:
                    continue

                files_taken += 1
                self.stats["files_ingested"] += 1
                self.stats["by_lobe"][lobe_tag]["files"] += 1

                doc_clean_name = file_path.stem.replace(" ", "_").replace("#", "").replace(".", "_")[:40]
                total_chunks = len(chunks)

                for idx, ch in enumerate(chunks):
                    chunk_text = ch["text"]
                    char_len = len(chunk_text)
                    self.stats["total_chunks"] += 1

                    # Exact duplicate chunks (copies of a file, repeated boilerplate) are embedded once.
                    text_sha = hashlib.sha256(chunk_text.strip().encode("utf-8")).hexdigest()
                    if text_sha in seen_text:
                        self.stats["duplicate_chunks_skipped"] += 1
                        continue
                    seen_text.add(text_sha)

                    self.stats["total_chars"] += char_len
                    self.stats["by_lobe"][lobe_tag]["chunks"] += 1
                    self.stats["by_lobe"][lobe_tag]["chars"] += char_len

                    # Unique CCID for this chunk with extension tag to prevent .md/.txt collisions
                    ext_tag = file_path.suffix.lstrip(".").lower()[:3]
                    base_ccid = f"CCID_LOBE_{lobe_tag[:4].upper()}_{doc_clean_name}_{ext_tag}_{idx:03d}"
                    chunk_ccid = base_ccid
                    collision_idx = 1
                    while chunk_ccid in seen_ids:
                        chunk_ccid = f"{base_ccid}_v{collision_idx}"
                        collision_idx += 1
                    seen_ids.add(chunk_ccid)

                    payload = {
                        "text": chunk_text,
                        "header": ch.get("header", ""),
                        "source_file": str(rel_path),
                        "filename": file_path.name,
                        "lobe": lobe_tag,
                        "chunk_index": idx,
                        "total_chunks": total_chunks,
                        "layer": config["layer"]
                    }
                    meta = {
                        "lobe": lobe_tag,
                        "source_file": str(rel_path),
                        "filename": file_path.name,
                        "chunk_index": idx,
                        "total_chunks": total_chunks,
                        # Assign Shiva Lens based on chunk index (12th Step 4-pass manifold)
                        "shiva_lens": SHIVA_LENSES[idx % 4],
                        "layer": config["layer"],
                        "text_sha256": text_sha,
                    }
                    pending.append({
                        "ccid": chunk_ccid,
                        "text": chunk_text,
                        "title": file_path.name,
                        "payload": payload,
                        "meta": meta,
                        "text_sha256": text_sha,
                    })

                print(f"  -> Chunked: {file_path.name[:50]} ({total_chunks} chunks)")
        return pending

    def _split_by_index_state(self, pending: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
        """(chunks that need embedding, number already indexed with the same text). Read-only."""
        todo: List[Dict[str, Any]] = []
        already = 0
        for off in range(0, len(pending), 500):
            group = pending[off: off + 500]
            existing = self.hoard.chroma_get_metadata([it["ccid"] for it in group])
            for it in group:
                if existing.get(it["ccid"], {}).get("text_sha256") == it["text_sha256"]:
                    already += 1
                else:
                    todo.append(it)
        return todo, already

    def ingest_lobes(
        self,
        apply: bool = False,
        clean_first: bool = False,
        apply_hygiene: bool = False,
        limit_files: Optional[int] = None,
        pause_s: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Executes the multi-lobe in-place ingestion. By default it only PLANS (no embedding call, no write).
        apply=True embeds the chunks that are new or changed and indexes them in the active embedding space,
        pausing `pause_s` seconds between batches (pacing: a rate limit is a certainty on a free key).
        clean_first=True runs the hygiene step as a dry run; apply_hygiene=True lets it delete.
        """
        t0 = time.time()
        self.stats = self._fresh_stats()
        print("=== INTEGRA O/S: 12TH STEP ORTHOGONAL INGESTION PIPELINE ===")

        hygiene_results: Dict[str, Any] = {}
        if clean_first:
            print("\n--- PHASE 0: SAFE HYGIENE " + ("(DELETING)" if apply_hygiene else "(DRY RUN: nothing is deleted)") + " ---")
            hygiene_results = perform_safe_hygiene(self.workspace_root, self.lobe_config, dry_run=not apply_hygiene)
            print(f"[HYGIENE COMPLETE] Bytes {'freed' if apply_hygiene else 'that would be freed'}: {hygiene_results['bytes_freed']:,}")

        print("\n--- PHASE 1-2: SCAN, CHUNK, DEDUPLICATE ---")
        pending = self._scan(limit_files)
        todo, already = self._split_by_index_state(pending)
        tokens = sum(approx_tokens(it["text"]) for it in todo)
        plan = {
            "space": self.hoard.space.id,
            "files_scanned": self.stats["files_scanned"],
            "chunks_unique": len(pending),
            "duplicate_chunks_skipped": self.stats["duplicate_chunks_skipped"],
            "already_indexed": already,
            "to_embed": len(todo),
            "total_chars": self.stats["total_chars"],
            "estimated_tokens": tokens,
            "estimated_cost_usd": estimate_cost_usd(tokens),
            "estimated_cost_batch_usd": estimate_cost_usd(tokens, batch=True),
        }

        result: Dict[str, Any] = {
            "status": "INGESTION_PLAN_ONLY",
            "hygiene": hygiene_results,
            "stats": self.stats,
            "plan": plan,
            "chroma_chunks_persisted": 0,
            "error": None,
        }
        if not apply:
            print("\n--- PLAN ONLY: nothing was embedded or written. Re-run with --apply to embed (paid API calls). ---")
            result["elapsed_seconds"] = round(time.time() - t0, 2)
            return result

        if self.hoard.config_error:
            raise EmbeddingUnavailable("BAD_CONFIG", self.hoard.config_error)
        service = self.embedder or self.hoard.embedder or get_operator_embedding_service()
        if service.space != self.hoard.space:
            raise ValueError(f"embedder space {service.space.id} differs from the Hoard's {self.hoard.space.id}")

        celestial_stamp = self.clock.get_dual_telemetry()
        anchor_4d = {
            "x": 30.5888,
            "y": -91.1673,
            "z": 0.0,
            "t": celestial_stamp.get("digital_clock", {}).get("unix_epoch", time.time()),
            "anchor": "Baker, Louisiana",
            "civil_time": celestial_stamp.get("digital_clock", {}).get("iso_local", "")
        }

        print(f"\n--- PHASE 3-4: EMBED {len(todo)} CHUNKS AND INDEX (space {self.hoard.space.id}) ---")
        persisted = 0
        status = "INGESTION_COMPLETE"
        for off in range(0, len(todo), self.BATCH):
            if off > 0 and pause_s > 0:
                self._sleep(pause_s)
            batch = todo[off: off + self.BATCH]
            try:
                results = service.embed_documents([(it["text"], it["title"]) for it in batch])
            except EmbeddingUnavailable as exc:
                status = "INGESTION_STOPPED_EMBEDDING_UNAVAILABLE"
                result["error"] = {"code": exc.code, "detail": exc.detail}
                break
            nodes: List[Tuple[HoardNode, str]] = []
            for it, res in zip(batch, results):
                node = HoardNode(
                    ccid=it["ccid"],
                    payload=it["payload"],
                    spacetime_anchor=anchor_4d,
                    embedding_64d=list(res.vector[:64]),
                    embedding_768d=list(res.vector),
                    outcome_label=1.0,
                    is_stale=False,
                    created_at=time.time(),
                    metadata=it["meta"],
                    embed_space=res.space.id,
                )
                nodes.append((node, it["text"]))
            try:
                persisted += self.hoard.chroma_upsert_many(nodes)
            except RuntimeError as exc:
                status = "INGESTION_STOPPED_INDEX_ERROR"
                result["error"] = {"code": "INDEX_ERROR", "detail": str(exc)}
                break
            # Update the Hoard's in-memory sparse cache (replace a re-embedded chunk instead of duplicating it)
            replaced = {node.ccid for node, _ in nodes}
            self.hoard.local_sparse_cache = [n for n in self.hoard.local_sparse_cache if n.ccid not in replaced]
            self.hoard.local_sparse_cache.extend(node for node, _ in nodes)

        self.stats["chroma_persisted"] = persisted
        result["status"] = status
        result["chroma_chunks_persisted"] = persisted
        result["elapsed_seconds"] = round(time.time() - t0, 2)

        print(f"\n=== INGESTION SUMMARY ({result['elapsed_seconds']}s) — {status} ===")
        print(f"Files Scanned:    {self.stats['files_scanned']}")
        print(f"Chunks (unique):  {plan['chunks_unique']}   duplicates skipped: {plan['duplicate_chunks_skipped']}")
        print(f"Already indexed:  {plan['already_indexed']}   embedded now: {persisted}")
        for lobe, s in self.stats["by_lobe"].items():
            print(f"  - {lobe.upper()}: {s['files']} files, {s['chunks']} chunks, {s['chars']:,} chars")
        return result


def run_test_retrieval(hoard: TheHoard, query_str: str = "Sun Breathing 13th Form loop closure", embedder: Any = None) -> Dict[str, Any]:
    """
    Executes a test Rodin retrieval against the active-space ChromaDB collection:
    the query is embedded in the documented query format by the real model.
    """
    print(f"\n--- TEST RETRIEVAL QUERY: '{query_str}' ---")
    service = embedder or hoard.embedder or get_operator_embedding_service()
    emb = service.embed_query(query_str)
    results = hoard.chroma_query(emb.vector, n_results=3, space_id=emb.space.id)
    for idx, r in enumerate(results):
        print(f"Result {idx+1}: CCID={r['ccid']} | Distance={r.get('distance')} | Lobe={r.get('metadata', {}).get('lobe')}")
        doc_snippet = (r.get("document") or "")[:120].replace("\n", " ")
        print(f"  Snippet: {doc_snippet}...")
    return {"query": query_str, "results": results}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="12th Step Orthogonal Ingestion. A plan by default; nothing is embedded or deleted unless asked.")
    parser.add_argument("--apply", action="store_true", help="embed the new or changed chunks with the real model and index them (paid API calls)")
    parser.add_argument("--clean-first", action="store_true", help="run the hygiene step as a DRY RUN (lists files, deletes nothing)")
    parser.add_argument("--apply-hygiene", action="store_true", help="let the hygiene step DELETE the files it lists (implies --clean-first)")
    parser.add_argument("--limit-files", type=int, default=None, help="stop after this many files (a pilot run)")
    parser.add_argument("--pause-s", type=float, default=0.5, help="seconds to wait between embedding requests (pacing)")
    args = parser.parse_args(argv)

    engine = MultiLobeIngestionEngine()
    summary = engine.ingest_lobes(
        apply=args.apply,
        clean_first=args.clean_first or args.apply_hygiene,
        apply_hygiene=args.apply_hygiene,
        limit_files=args.limit_files,
        pause_s=args.pause_s,
    )
    print("\n" + json.dumps(summary["plan"], indent=2))
    if summary["error"]:
        print(f"\n[STOPPED] {summary['error']}")
    if args.apply and summary["status"] == "INGESTION_COMPLETE":
        run_test_retrieval(engine.hoard)
        print("\n[SUCCESS] Ingestion and retrieval verification finished.")
    return 0 if summary["status"] in ("INGESTION_COMPLETE", "INGESTION_PLAN_ONLY") else 1


if __name__ == "__main__":
    sys.exit(main())
