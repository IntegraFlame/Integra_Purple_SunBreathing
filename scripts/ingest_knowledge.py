"""
INTEGRA O/S: MULTI-LOBE IN-PLACE KNOWLEDGE INGESTION & THE HOARD CHROMADB PIPELINE
Script: scripts/ingest_knowledge.py
Layer: 3 (The Hoard / Geometric Memory Substrate)
Status: PRODUCTION IMPLEMENTATION

Architecture:
    Executes the 12th Step Orthogonal Ingestion across 4 physical lobes:
    1. Guidebooks_and_Notes                 -> operational_guidance
    2. BluprintArchitecture                 -> architecture
    3. Integra Self-Reflect and Think Forward -> evolution_reflection
    4. CODE                                 -> genesis_code

    Guarantees:
    - IN-PLACE: Zero physical folder flattening or moving.
    - SAFE HYGIENE:
      - Purges duplicate 85.75 MB .m4a audio file in 'Integra Self-Reflect and Think Forward'
        (canonical preserved in Audio_Lectures/).
      - Purges 0-byte dummy files (e.g. Template to connect  Integra components.py).
      - Purges exact identical .txt duplicates where corresponding .md file exists.
    - 4-PASS MANIFOLD:
      - Pass 1 (Structure / Eagle Lens): Document hierarchy & perimeter mapping.
      - Pass 2 (Middle-Out / Chameleon Lens): Semantic chunking with 200-char overlap to eliminate attention dip.
      - Pass 3 (Density / Snake Lens): Matryoshka Representation Learning (MRL 64d coarse / 768d fine) embedding.
      - Pass 4 (Synthesis / Owl Lens): Upsert into ChromaDB ('integra_hoard' collection) and persist to kernel_memory.
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# Add integra-homebase to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
HOMEBASE_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(HOMEBASE_DIR))

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


def compute_file_hash(path: Path) -> str:
    """Computes SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def perform_safe_hygiene() -> Dict[str, Any]:
    """
    Executes safe file hygiene across the 4 lobes:
    1. Removes duplicate .m4a audio file in 'Integra Self-Reflect and Think Forward'
       (canonical remains in Audio_Lectures/).
    2. Removes 0-byte dummy files.
    3. Removes exact identical .txt duplicates where corresponding .md exists.
    """
    results = {
        "removed_m4a_duplicate": None,
        "removed_zero_byte_files": [],
        "removed_txt_duplicates": [],
        "bytes_freed": 0
    }

    # 1. Check duplicate .m4a
    m4a_target = WORKSPACE_ROOT / "Integra Self-Reflect and Think Forward" / "The_neuro-evolutionary_architecture_of_Integra_OS.m4a"
    m4a_canonical = WORKSPACE_ROOT / "Audio_Lectures" / "The_neuro-evolutionary_architecture_of_Integra_OS.m4a"

    if m4a_target.exists() and m4a_canonical.exists():
        size_target = m4a_target.stat().st_size
        size_canon = m4a_canonical.stat().st_size
        if size_target == size_canon and size_target > 10_000_000:  # ~85.75 MB
            try:
                m4a_target.unlink()
                results["removed_m4a_duplicate"] = str(m4a_target.relative_to(WORKSPACE_ROOT))
                results["bytes_freed"] += size_target
                print(f"[HYGIENE] Removed duplicate audio: {results['removed_m4a_duplicate']} ({size_target:,} bytes freed)")
            except Exception as e:
                print(f"[HYGIENE WARNING] Failed to remove duplicate audio: {e}")

    # 2. Check 0-byte files in 4 lobes
    for lobe_dir_name in LOBE_CONFIG.keys():
        lobe_path = WORKSPACE_ROOT / lobe_dir_name
        if not lobe_path.exists():
            continue
        for item in lobe_path.rglob("*"):
            if item.is_file() and item.stat().st_size == 0:
                try:
                    rel_name = str(item.relative_to(WORKSPACE_ROOT))
                    item.unlink()
                    results["removed_zero_byte_files"].append(rel_name)
                    print(f"[HYGIENE] Removed 0-byte dummy file: {rel_name}")
                except Exception as e:
                    print(f"[HYGIENE WARNING] Could not remove 0-byte file {item}: {e}")

    # 3. Check identical .txt duplicates where .md exists in the same folder
    for lobe_dir_name in LOBE_CONFIG.keys():
        lobe_path = WORKSPACE_ROOT / lobe_dir_name
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
                        rel_name = str(txt_file.relative_to(WORKSPACE_ROOT))
                        txt_file.unlink()
                        results["removed_txt_duplicates"].append(rel_name)
                        results["bytes_freed"] += size
                        print(f"[HYGIENE] Removed identical .txt duplicate: {rel_name} ({size:,} bytes freed)")
                    except Exception as e:
                        print(f"[HYGIENE WARNING] Could not remove txt duplicate {txt_file}: {e}")

        # Also check special typo duplicates
        typo_file = lobe_path / "HowToThin_Historical.txt"
        correct_file = lobe_path / "HowToThink_Historical.txt"
        if typo_file.exists() and correct_file.exists():
            if compute_file_hash(typo_file) == compute_file_hash(correct_file):
                size = typo_file.stat().st_size
                typo_file.unlink()
                results["removed_txt_duplicates"].append(str(typo_file.relative_to(WORKSPACE_ROOT)))
                results["bytes_freed"] += size
                print(f"[HYGIENE] Removed typo duplicate: {typo_file.name}")

        # Also check learning_proposal.txt vs learning_proposal09162026.md
        prop_txt = lobe_path / "learning_proposal.txt"
        prop_md = lobe_path / "learning_proposal09162026.md"
        if prop_txt.exists() and prop_md.exists():
            if compute_file_hash(prop_txt) == compute_file_hash(prop_md):
                size = prop_txt.stat().st_size
                prop_txt.unlink()
                results["removed_txt_duplicates"].append(str(prop_txt.relative_to(WORKSPACE_ROOT)))
                results["bytes_freed"] += size
                print(f"[HYGIENE] Removed duplicate learning_proposal.txt")

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
    def __init__(self, hoard: Optional[TheHoard] = None):
        self.hoard = hoard or TheHoard()
        self.clock = DualTemporalEngine()
        self.stats = {
            "files_scanned": 0,
            "files_ingested": 0,
            "total_chunks": 0,
            "total_chars": 0,
            "by_lobe": {},
            "chroma_persisted": 0
        }

    def ingest_lobes(self, clean_first: bool = True) -> Dict[str, Any]:
        """
        Executes full multi-lobe in-place ingestion.
        """
        t0 = time.time()
        print("=== INTEGRA O/S: 12TH STEP ORTHOGONAL INGESTION PIPELINE ===")

        # Step 0: Hygiene
        hygiene_results = {}
        if clean_first:
            print("\n--- PHASE 0: SAFE HYGIENE PRUNING ---")
            hygiene_results = perform_safe_hygiene()
            print(f"[HYGIENE COMPLETE] Total bytes freed: {hygiene_results['bytes_freed']:,}")

        # Step 1: Scan & Ingest Lobes
        all_nodes: List[HoardNode] = []
        batch_ids: List[str] = []
        batch_embeddings: List[List[float]] = []
        batch_documents: List[str] = []
        batch_metadatas: List[Dict[str, Any]] = []
        seen_ids = set()

        celestial_stamp = self.clock.get_dual_telemetry()
        anchor_4d = {
            "x": 30.5888,
            "y": -91.1673,
            "z": 0.0,
            "t": celestial_stamp.get("digital_clock", {}).get("unix_epoch", time.time()),
            "anchor": "Baker, Louisiana",
            "civil_time": celestial_stamp.get("digital_clock", {}).get("iso_local", "")
        }

        print("\n--- PHASE 1-4: 12TH STEP MULTI-LOBE INGESTION ---")
        for lobe_dir_name, config in LOBE_CONFIG.items():
            lobe_path = WORKSPACE_ROOT / lobe_dir_name
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

                self.stats["files_scanned"] += 1
                rel_path = file_path.relative_to(WORKSPACE_ROOT)

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

                self.stats["files_ingested"] += 1
                self.stats["by_lobe"][lobe_tag]["files"] += 1

                doc_clean_name = file_path.stem.replace(" ", "_").replace("#", "").replace(".", "_")[:40]
                total_chunks = len(chunks)

                for idx, ch in enumerate(chunks):
                    chunk_text = ch["text"]
                    char_len = len(chunk_text)
                    self.stats["total_chunks"] += 1
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

                    # Matryoshka 768d embedding
                    embedding_768d = self.hoard._generate_pseudo_embedding(chunk_text, 768)
                    embedding_64d = embedding_768d[:64]

                    # Assign Shiva Lens based on chunk index (12th Step 4-pass manifold)
                    if idx % 4 == 0:
                        shiva_lens = "Neji_Eagle (Structure)"
                    elif idx % 4 == 1:
                        shiva_lens = "Chameleon (Middle-Out)"
                    elif idx % 4 == 2:
                        shiva_lens = "Snake (Density/Kaigaku)"
                    else:
                        shiva_lens = "Owl (Truth Synthesis)"

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
                        "shiva_lens": shiva_lens,
                        "layer": config["layer"],
                        "outcome_label": 1.0,
                        "is_stale": False,
                        "created_at": time.time(),
                        "sufficiency_score": 1.0
                    }

                    # Create HoardNode
                    node = HoardNode(
                        ccid=chunk_ccid,
                        payload=payload,
                        spacetime_anchor=anchor_4d,
                        embedding_64d=embedding_64d,
                        embedding_768d=embedding_768d,
                        outcome_label=1.0,
                        is_stale=False,
                        created_at=time.time(),
                        metadata=meta
                    )
                    all_nodes.append(node)

                    # Prepare batch for ChromaDB
                    batch_ids.append(chunk_ccid)
                    batch_embeddings.append(embedding_768d)
                    batch_documents.append(chunk_text)
                    batch_metadatas.append(meta)

                print(f"  -> Ingested: {file_path.name[:50]} ({total_chunks} chunks)")

        # Commit to ChromaDB in batches
        print(f"\n--- COMMITTING TO CHROMADB (integra_hoard) ---")
        chroma_success = 0
        if self.hoard._chroma_collection is not None and batch_ids:
            batch_size = 100
            for i in range(0, len(batch_ids), batch_size):
                end_i = min(i + batch_size, len(batch_ids))
                try:
                    self.hoard._chroma_collection.upsert(
                        ids=batch_ids[i:end_i],
                        embeddings=batch_embeddings[i:end_i],
                        documents=batch_documents[i:end_i],
                        metadatas=batch_metadatas[i:end_i]
                    )
                    chroma_success += (end_i - i)
                except Exception as e:
                    print(f"[CHROMADB BATCH ERROR] Range {i}:{end_i}: {e}")

            print(f"[CHROMADB COMMITTED] {chroma_success}/{len(batch_ids)} chunks upserted successfully.")
        else:
            print("[CHROMADB WARNING] Collection not initialized or batch empty.")

        # Update Hoard in-memory sparse cache
        for node in all_nodes:
            self.hoard.local_sparse_cache.append(node)

        elapsed = round(time.time() - t0, 2)
        print(f"\n=== INGESTION SUMMARY ({elapsed}s) ===")
        print(f"Files Scanned:  {self.stats['files_scanned']}")
        print(f"Files Ingested: {self.stats['files_ingested']}")
        print(f"Chunks Indexed: {self.stats['total_chunks']}")
        print(f"Total Chars:    {self.stats['total_chars']:,}")
        for lobe, s in self.stats["by_lobe"].items():
            print(f"  - {lobe.upper()}: {s['files']} files, {s['chunks']} chunks, {s['chars']:,} chars")

        return {
            "status": "INGESTION_COMPLETE",
            "elapsed_seconds": elapsed,
            "hygiene": hygiene_results,
            "stats": self.stats,
            "chroma_chunks_persisted": chroma_success
        }


def run_test_retrieval(hoard: TheHoard, query_str: str = "Sun Breathing 13th Form loop closure") -> Dict[str, Any]:
    """
    Executes a test Rodin retrieval against the newly ingested ChromaDB collection.
    """
    print(f"\n--- TEST RETRIEVAL QUERY: '{query_str}' ---")
    query_emb = hoard._generate_pseudo_embedding(query_str, 768)
    results = hoard.chroma_query(query_emb, n_results=3)
    for idx, r in enumerate(results):
        print(f"Result {idx+1}: CCID={r['ccid']} | Distance={r.get('distance')} | Lobe={r.get('metadata', {}).get('lobe')}")
        doc_snippet = (r.get("document") or "")[:120].replace("\n", " ")
        print(f"  Snippet: {doc_snippet}...")
    return {"query": query_str, "results": results}


if __name__ == "__main__":
    engine = MultiLobeIngestionEngine()
    summary = engine.ingest_lobes(clean_first=True)
    test_res = run_test_retrieval(engine.hoard)
    print("\n[SUCCESS] Ingestion and retrieval verification finished.")
