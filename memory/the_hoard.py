"""
INTEGRA O/S: MEMORY MANIFOLD
Module: memory/the_hoard.py
Layer: 3 (The Hoard: High-Dimensional Geometric Memory)

Schema v2.1 (Rodin embedding spaces):
    - Every node may carry a vector, and a vector is trusted only when it names its EmbeddingSpace
      (model | dimension | prompt format, memory/embedding_service.py). A vector with no space, or an
      all-zero vector, is stored but never indexed and never searched.
    - Chroma keeps ONE collection per space (integra_hoard__gemini-embedding-2-768-asym-v1). The
      legacy collection `integra_hoard` is left untouched and never queried: its 5,526 rows were
      measured on 2026-10-15 to hold no vector from a model.
    - Nothing in this module fabricates a vector. Embedding happens in embed_pending(), which is
      explicit, dry-run by default, deduplicated, stops at the first failure and writes shards atomically.

Schema v2.0 (Phase D+ Upgrade):
    - Adds `outcome_label`, `embedding_64d`, `embedding_768d`, `is_stale`, `created_at`
    - Implements `kernel_memory/` directory structure per blueprint spec:
        kernel_memory/
        ├── core_identity.txt
        ├── rolling_context.json
        ├── drop_in/
        ├── hoard/
        │   ├── raw_shards/      <-- Unconsolidated states
        │   ├── modules/         <-- Blueprint manifests
        │   └── libraries/       <-- 4D celestial-tagged markdown books
        └── vectors/             <-- MRL embeddings & celestial index

    - Provides `commit_node_v2()` with full schema, backward-compatible `commit_node()`.
    - Provides `mark_outcome()` for post-hoc labeling of success/failure.
    - Provides `get_stale_nodes()` for Phoenix SWDS consolidation.
"""

import os
import json
import logging
import time
from collections import OrderedDict
from typing import List, Dict, Any, Optional, Tuple, Union

from memory.embedding_service import (
    EmbeddingService,
    EmbeddingSpace,
    EmbeddingUnavailable,
    approx_tokens,
    estimate_cost_usd,
    get_default_embedding_service,
    resolve_space_from_env,
)

logger = logging.getLogger("integra.hoard")

# Celestial temporal injection — all timestamps routed through celestial middleware
try:
    from core.celestial_middleware import celestial_time, celestial_ccid
except ImportError:
    # Fallback if middleware unavailable (isolated testing)
    celestial_time = time.time
    celestial_ccid = lambda prefix="CCID": f"{prefix}_{int(time.time())}"


def _new_celestial_stamp(kind: str) -> Optional[Dict[str, Any]]:
    """A Celestial Sentinel stamp for a new node (Brain Map T1), or None if the Sentinel is unavailable (logged)."""
    try:
        from temporal.celestial_sentinel import stamp_dict
    except ImportError:
        return None
    return stamp_dict(kind)

HOARD_VECTOR_DIM = 768  # the schema fields are named embedding_768d; another dimension needs a schema change

LEGACY_COLLECTION = "integra_hoard"


class HoardNode:
    """
    A single node in The Hoard memory manifold.

    Schema v2.1 Fields:
        ccid: Cheshire Cat Interaction ID (unique identifier).
        payload: The actual knowledge content (dict, str, or any JSON-serializable).
        spacetime_anchor: 4D celestial coordinates {x, y, z, t}.
        embedding_64d: Prefix slice of the 768d vector (legacy field; Rodin slices the 768d vector itself).
        embedding_768d: The node's vector in `embed_space`; all zeros when the node has none yet.
        embed_space: Id of the EmbeddingSpace the vector belongs to, or None. A vector with no space is untrusted.
        outcome_label: Post-hoc quality label (1.0 = SUCCESS, 0.0 = FAILURE, 0.5 = UNKNOWN).
        is_stale: Whether this node has exceeded the temporal staleness threshold.
        created_at: Unix timestamp of node creation.
        sufficiency_score: Pre-existing sufficiency metric (1.0 = fully sufficient).
        metadata: Arbitrary metadata dict for Looking Glass, Cheshire Protocol telemetry, etc.
        celestial_stamp: The Celestial Sentinel stamp taken when the node was created (frame, civil time, vector,
            label, provenance). Additive and optional: nodes written before Brain Map T1 have none, and none is
            invented for them.
    """
    __slots__ = (
        "ccid", "payload", "spacetime_anchor",
        "embedding_64d", "embedding_768d", "embed_space",
        "outcome_label", "is_stale", "created_at",
        "sufficiency_score", "metadata", "celestial_stamp"
    )

    def __init__(
        self,
        ccid: str,
        payload: Any,
        spacetime_anchor: Dict[str, Any],
        embedding_64d: Optional[List[float]] = None,
        embedding_768d: Optional[List[float]] = None,
        outcome_label: float = 0.5,
        is_stale: bool = False,
        created_at: Optional[float] = None,
        sufficiency_score: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
        embed_space: Optional[str] = None,
        celestial_stamp: Optional[Dict[str, Any]] = None,
        stamp_new: bool = True,
    ):
        self.ccid = ccid
        self.payload = payload
        self.spacetime_anchor = spacetime_anchor
        self.embedding_64d = embedding_64d or [0.0] * 64
        self.embedding_768d = embedding_768d or [0.0] * HOARD_VECTOR_DIM
        self.embed_space = embed_space
        self.outcome_label = outcome_label
        self.is_stale = is_stale
        if created_at or not stamp_new:
            # An existing node (or a caller that already knows the instant): keep what it carries.
            # A loaded node without created_at gets "now" as before, but no stamp is invented for it.
            self.created_at = created_at or celestial_time()
            self.celestial_stamp = celestial_stamp
        else:
            # A new node: one Sentinel stamp gives both the creation time and the celestial stamp.
            st = celestial_stamp or _new_celestial_stamp("hoard_node")
            self.created_at = st["unix"] if st else celestial_time()
            self.celestial_stamp = st
        self.sufficiency_score = sufficiency_score
        self.metadata = metadata or {}

    @property
    def has_vector(self) -> bool:
        """True only for a non-zero vector that names its space. An untagged vector is not trusted."""
        return self.embed_space is not None and any(v != 0.0 for v in self.embedding_768d)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-compatible dictionary."""
        return {
            "ccid": self.ccid,
            "payload": self.payload,
            "spacetime_anchor": self.spacetime_anchor,
            "embedding_64d": self.embedding_64d,
            "embedding_768d": self.embedding_768d,
            "embed_space": self.embed_space,
            "outcome_label": self.outcome_label,
            "is_stale": self.is_stale,
            "created_at": self.created_at,
            "sufficiency_score": self.sufficiency_score,
            "metadata": self.metadata,
            "celestial_stamp": self.celestial_stamp,
        }

    # Alias for Rodin Protocol compatibility — Rodin expects `node.get("embedding")`
    def to_rodin_candidate(self) -> Dict[str, Any]:
        """
        Convert to a Rodin-compatible candidate dict.
        Uses the 768d embedding as the primary 'embedding' key,
        which Rodin then slices for the coarse tier and the fine re-rank.
        """
        return {
            "ccid": self.ccid,
            "embedding": self.embedding_768d,
            "embed_space": self.embed_space,
            "outcome_label": self.outcome_label,
            "created_at": self.created_at,
            "payload": self.payload,
            "is_stale": self.is_stale,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HoardNode":
        """Deserialize from a dictionary (e.g., loaded from JSON). Shards written before v2.1 have no embed_space."""
        return cls(
            ccid=data.get("ccid", "UNKNOWN"),
            payload=data.get("payload"),
            spacetime_anchor=data.get("spacetime_anchor", {}),
            embedding_64d=data.get("embedding_64d"),
            embedding_768d=data.get("embedding_768d"),
            outcome_label=data.get("outcome_label", 0.5),
            is_stale=data.get("is_stale", False),
            created_at=data.get("created_at"),
            sufficiency_score=data.get("sufficiency_score", 1.0),
            metadata=data.get("metadata"),
            embed_space=data.get("embed_space"),
            celestial_stamp=data.get("celestial_stamp"),
            stamp_new=False,
        )


def node_embedding_text(node: "HoardNode") -> Tuple[str, Optional[str]]:
    """
    (text, title) to embed for a node, in the documented document format [E1]:
    a lobe chunk embeds its text, a report its summary, a string itself, anything else its sorted JSON.
    The title is a real one (file name, section header) or None, which the format renders as "none".
    A ccid is never used as a title: it is noise to the model.
    """
    payload = node.payload
    meta = node.metadata if isinstance(node.metadata, dict) else {}
    title: Optional[str] = meta.get("filename") or None
    if isinstance(payload, str):
        return payload, title
    if isinstance(payload, dict):
        title = title or payload.get("filename") or payload.get("header") or payload.get("title") or None
        for key in ("text", "summary"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value, title
        return json.dumps(payload, ensure_ascii=False, sort_keys=True), title
    return json.dumps(payload, ensure_ascii=False, sort_keys=True), title


def _write_json_atomic(path: str, data: Any) -> None:
    """Write to a temporary file in the same folder, then replace. A crash leaves the old file or the new one, never half of one."""
    tmp = f"{path}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def load_nodes_from_shards(shards_dir: str) -> Tuple[List["HoardNode"], Dict[str, int]]:
    """
    Read-only: the node shards of a folder as HoardNodes, plus a report {loaded, skipped_not_a_node, unreadable}.
    A file that is not a node (no `ccid` and `payload`) or cannot be parsed is counted and skipped, so it can never
    be rewritten as one. A repeated ccid keeps its first shard. Nothing is created or changed.
    """
    report = {"loaded": 0, "skipped_not_a_node": 0, "unreadable": 0}
    nodes: List[HoardNode] = []
    if not os.path.isdir(shards_dir):
        return nodes, report
    seen = set()
    for filename in sorted(os.listdir(shards_dir)):
        if not filename.endswith(".json"):
            continue
        try:
            with open(os.path.join(shards_dir, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            report["unreadable"] += 1
            continue
        if not isinstance(data, dict) or "ccid" not in data or "payload" not in data:
            report["skipped_not_a_node"] += 1
            continue
        try:
            node = HoardNode.from_dict(data)
        except Exception:
            report["unreadable"] += 1
            continue
        if node.ccid not in seen:
            seen.add(node.ccid)
            nodes.append(node)
            report["loaded"] += 1
    return nodes, report


def _group_pending(
    nodes: List["HoardNode"],
    space: EmbeddingSpace,
    limit: Optional[int] = None,
    node_text=node_embedding_text,
) -> Tuple[List[Tuple[Tuple[str, Optional[str]], List["HoardNode"]]], int, int, int]:
    """
    (unique (text, title) groups with their nodes, pending node count, already-embedded count, empty-text count).
    A node is pending unless it holds a vector that names `space`; identical (text, title) pairs form one group.
    """
    pending: List[HoardNode] = []
    already = 0
    for node in nodes:
        if node.has_vector and node.embed_space == space.id:
            already += 1
        else:
            pending.append(node)
    groups: "OrderedDict[Tuple[str, Optional[str]], List[HoardNode]]" = OrderedDict()
    skipped_empty = 0
    for node in pending:
        text, title = node_text(node)
        if not text or not text.strip():
            skipped_empty += 1
            continue
        groups.setdefault((text, title), []).append(node)
    unique = list(groups.items())
    if limit is not None:
        unique = unique[: max(0, int(limit))]
    return unique, len(pending), already, skipped_empty


def _plan_dict(space, unique, pending, already, skipped_empty, dry_run) -> Dict[str, Any]:
    tokens = sum(approx_tokens(text) for (text, _), _ in unique)
    return {
        "dry_run": dry_run,
        "space": space.id,
        "pending": pending,
        "already_embedded": already,
        "unique_texts": len(unique),
        "skipped_empty": skipped_empty,
        "estimated_tokens": tokens,
        "estimated_cost_usd": estimate_cost_usd(tokens),
        "estimated_cost_batch_usd": estimate_cost_usd(tokens, batch=True),
    }


def plan_embedding(
    nodes: List["HoardNode"],
    space: EmbeddingSpace,
    limit: Optional[int] = None,
    node_text=node_embedding_text,
) -> Dict[str, Any]:
    """What embedding these nodes in `space` would take: counts, tokens and price. Pure: no Hoard, no network, no write."""
    unique, pending, already, skipped_empty = _group_pending(nodes, space, limit, node_text)
    return _plan_dict(space, unique, pending, already, skipped_empty, dry_run=True)


class TheHoard:
    """
    High-Dimensional Semantic Manifold (v2.2 — Local Sovereign, embedding spaces):

    The Hoard serves as Integra's persistent geometric memory substrate.
    It stores HoardNodes with a vector in a named EmbeddingSpace,
    outcome labels for KNN success-density gating, and temporal staleness tracking.

    Architecture:
        - In-memory: `local_sparse_cache` (List[HoardNode]) for fast Rodin retrieval.
        - On-disk: `kernel_memory/` directory tree for Phoenix SWDS consolidation.
        - Vector DB: ChromaDB (local persistent), one collection per EmbeddingSpace.
        - Relational: SQLite (via SWDS pipeline) for historical archival.

    The retrieval schema enables the Rodin Protocol's MRL pipeline:
        Phase 1: coarse prefix filter (O(1) elimination)
        Phase 2: 768d fine re-rank (precision KNN)
    """

    # --- kernel_memory/ Directory Structure ---
    KERNEL_DIRS = [
        "hoard/raw_shards",      # Unconsolidated waking-state JSON shards
        "hoard/modules",         # Blueprint manifests
        "hoard/libraries",       # 4D celestial-tagged markdown books
        "hoard/seed_packages",   # Linked Seed Packages (Hoard + Phoenix -> MongoDB monthly uploads)
        "vectors",               # MRL embeddings & celestial index
        "drop_in",               # Drop-in file ingestion folder
    ]

    def __init__(
        self,
        base_dir: Optional[str] = None,
        chroma_path: Optional[str] = None,
        embedder: Optional[EmbeddingService] = None,
        space: Optional[EmbeddingSpace] = None,
    ):
        self.local_sparse_cache: List[HoardNode] = []
        self.last_load_report: Dict[str, int] = {"loaded": 0, "skipped_not_a_node": 0, "unreadable": 0}
        self._legacy_rows_cache: Optional[int] = None

        # Determine root project directory and kernel_memory base
        if base_dir:
            self.root_dir = base_dir
        else:
            self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        # The embedding space this Hoard indexes. An explicit embedder fixes it; otherwise the environment decides.
        self.embedder = embedder
        self.config_error: Optional[str] = None
        if embedder is not None and space is not None and embedder.space != space:
            raise ValueError(f"embedder space {embedder.space.id} differs from the requested space {space.id}")
        if space is not None:
            self.space = space
        elif embedder is not None:
            self.space = embedder.space
            self.config_error = embedder.config_error
        else:
            self.space, self.config_error = resolve_space_from_env()
        if self.space.dim != HOARD_VECTOR_DIM and not self.config_error:
            self.config_error = (
                f"The Hoard stores {HOARD_VECTOR_DIM}-d vectors (embedding_768d); space {self.space.id} "
                f"has {self.space.dim}. Set RODIN_EMBED_DIM={HOARD_VECTOR_DIM}."
            )
        if self.config_error:
            logger.error("Hoard embedding configuration problem: %s", self.config_error)

        self.kernel_memory_dir = os.path.join(self.root_dir, "kernel_memory")
        # Legacy compat: The Hoard directory (for save states and CCID files)
        self.hoard_dir = os.path.join(self.kernel_memory_dir, "hoard")

        # ChromaDB: Local persistent vector store
        self._chroma_path = chroma_path or os.path.join(self.root_dir, "local_dbs", "chroma_storage")
        os.makedirs(self._chroma_path, exist_ok=True)
        self._chroma_client = None
        self._chroma_collection = None
        self._chroma_collection_name = self.space.collection_name()

        # Initialize directory structure
        self._initialize_kernel_memory()

        # Initialize xv6 crash-safe write-ahead transaction logger & LRU Hot/Cold RAM cache (Task L-2)
        self.wal = Xv6TransactionLogger(
            wal_path=os.path.join(self.kernel_memory_dir, "hoard", "xv6_wal.json")
        )
        self.hot_cache = HotStorageRAMCache(
            cold_vault_dir=os.path.join(self.kernel_memory_dir, "hoard", "cold_vault_z1"),
            max_hot_nodes=256,
        )

        # Initialize ChromaDB collection
        self._initialize_chromadb()

    def _initialize_kernel_memory(self):
        """Create the kernel_memory/ directory tree if it doesn't exist.
        Note: Sovereign Identity (config/integra_identity_matrix.json & kernel_memory/core_identity.txt)
        is defined and anchored exclusively by StarfireProtocol within DragonEngine / Dragon Kernel,
        never by TheHoard.
        """
        for subdir in self.KERNEL_DIRS:
            full_path = os.path.join(self.kernel_memory_dir, subdir)
            os.makedirs(full_path, exist_ok=True)

        # Create rolling_context.json if it doesn't exist
        context_path = os.path.join(self.kernel_memory_dir, "rolling_context.json")
        if not os.path.exists(context_path):
            with open(context_path, "w", encoding="utf-8") as f:
                json.dump({"turns": [], "last_ccid": None}, f, indent=2)

    def _initialize_chromadb(self):
        """Initialize the local ChromaDB persistent client and the collection of the active embedding space."""
        try:
            import chromadb
            self._chroma_client = chromadb.PersistentClient(path=self._chroma_path)
            self._chroma_collection = self._chroma_client.get_or_create_collection(
                name=self._chroma_collection_name,
                metadata={"hnsw:space": "cosine", "embed_space": self.space.id},
            )
        except ImportError:
            # ChromaDB not installed — fall back to cache-only mode
            self._chroma_client = None
            self._chroma_collection = None
        except Exception as e:
            print(f"[HOARD] ChromaDB init warning (non-fatal): {e}")
            self._chroma_client = None
            self._chroma_collection = None

    def close(self):
        """Release ChromaDB resources to unlock the SQLite file."""
        self._chroma_collection = None
        if self._chroma_client is not None:
            try:
                # ChromaDB PersistentClient doesn't have an explicit close,
                # but dereferencing allows GC to release the file lock.
                del self._chroma_client
            except Exception:
                pass
            self._chroma_client = None

    def vector_search_available(self) -> bool:
        """False when ChromaDB is missing or failed to start; Rodin then reports degraded retrieval."""
        return self._chroma_collection is not None

    def chroma_upsert(self, node: 'HoardNode') -> bool:
        """
        Upsert a HoardNode into the active space's ChromaDB collection.
        Only a non-zero vector that names the active space is indexed; anything else is refused (False).
        """
        if self._chroma_collection is None or self.config_error:
            return False
        if not node.has_vector or node.embed_space != self.space.id:
            return False
        try:
            self._chroma_collection.upsert(
                ids=[node.ccid],
                embeddings=[node.embedding_768d],
                documents=[json.dumps(node.payload) if not isinstance(node.payload, str) else node.payload],
                metadatas=[{
                    "outcome_label": node.outcome_label,
                    "is_stale": node.is_stale,
                    "created_at": node.created_at,
                    "sufficiency_score": node.sufficiency_score,
                    "embed_space": node.embed_space,
                }]
            )
            return True
        except Exception as e:
            print(f"[HOARD] ChromaDB upsert failed for {node.ccid}: {e}")
            return False

    def chroma_upsert_many(self, items: List[Tuple["HoardNode", str]]) -> int:
        """
        Batch upsert of (node, document text) pairs into the active collection (the 12th Step ingestion uses it).
        Only trusted nodes are indexed (a non-zero vector in the active space); the number indexed is returned.
        The node's simple metadata (lobe, source file, chunk position, ...) is stored with the row.
        A ChromaDB failure raises RuntimeError: a bulk load that loses rows must not look like a success.
        """
        if self._chroma_collection is None or self.config_error:
            return 0
        rows = [(n, d) for n, d in items if n.has_vector and n.embed_space == self.space.id]
        if not rows:
            return 0
        metadatas = []
        for node, _ in rows:
            meta = {k: v for k, v in (node.metadata or {}).items() if isinstance(v, (str, int, float, bool))}
            meta.update({
                "outcome_label": node.outcome_label,
                "is_stale": node.is_stale,
                "created_at": node.created_at,
                "sufficiency_score": node.sufficiency_score,
                "embed_space": node.embed_space,
            })
            metadatas.append(meta)
        try:
            self._chroma_collection.upsert(
                ids=[n.ccid for n, _ in rows],
                embeddings=[n.embedding_768d for n, _ in rows],
                documents=[d for _, d in rows],
                metadatas=metadatas,
            )
        except Exception as e:
            raise RuntimeError(f"ChromaDB upsert failed: {type(e).__name__}: {e}") from e
        return len(rows)

    def chroma_get_metadata(self, ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """Metadata of the rows that already exist in the active collection, keyed by id (empty when none or no ChromaDB)."""
        if self._chroma_collection is None or not ids:
            return {}
        try:
            got = self._chroma_collection.get(ids=list(ids), include=["metadatas"])
            return {i: (m or {}) for i, m in zip(got["ids"], got["metadatas"])}
        except Exception:
            return {}

    def chroma_query(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        space_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Semantic similarity search in the active space's collection (top N by cosine distance).
        `space_id`, when given, must be the active space: a query vector from another space raises ValueError
        instead of returning meaningless neighbours. A ChromaDB failure raises RuntimeError; only a missing
        ChromaDB returns [] (check vector_search_available()).
        """
        if space_id is not None and space_id != self.space.id:
            raise ValueError(f"query vector is in space {space_id}; this Hoard indexes {self.space.id}")
        if self._chroma_collection is None:
            return []
        kwargs: Dict[str, Any] = {"query_embeddings": [query_embedding], "n_results": n_results}
        if where:
            kwargs["where"] = where
        try:
            results = self._chroma_collection.query(**kwargs)
            return [
                {
                    "ccid": results["ids"][0][i],
                    "document": results["documents"][0][i] if results.get("documents") else None,
                    "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
                    "distance": results["distances"][0][i] if results.get("distances") else None,
                }
                for i in range(len(results["ids"][0]))
            ]
        except Exception as e:
            raise RuntimeError(f"ChromaDB query failed: {type(e).__name__}: {e}") from e

    def chroma_candidates(
        self,
        query_embedding: List[float],
        n_results: int = 21,
        space_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        The nearest rows of the active space's index, shaped as Rodin candidates (ccid, embedding, embed_space,
        outcome_label, created_at, is_stale, payload). This is what Gate III reviews: every indexed row, node or lobe
        chunk, not only the nodes held in memory. A foreign `space_id` raises ValueError; no ChromaDB returns [];
        a ChromaDB failure raises RuntimeError.
        """
        if space_id is not None and space_id != self.space.id:
            raise ValueError(f"query vector is in space {space_id}; this Hoard indexes {self.space.id}")
        if self._chroma_collection is None:
            return []
        try:
            res = self._chroma_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["embeddings", "documents", "metadatas", "distances"],
            )
            rows = []
            for i, ccid in enumerate(res["ids"][0]):
                meta = (res["metadatas"][0][i] or {}) if res.get("metadatas") else {}
                rows.append({
                    "ccid": ccid,
                    "embedding": [float(x) for x in res["embeddings"][0][i]],
                    "embed_space": meta.get("embed_space"),
                    "outcome_label": meta.get("outcome_label", 0.5),
                    "created_at": meta.get("created_at", time.time()),
                    "is_stale": meta.get("is_stale", False),
                    "payload": res["documents"][0][i] if res.get("documents") else None,
                })
            return rows
        except Exception as e:
            raise RuntimeError(f"ChromaDB query failed: {type(e).__name__}: {e}") from e

    def count(self) -> int:
        """
        Returns the total number of indexed nodes in the active space's collection,
        or the local sparse cache count when ChromaDB is not active.
        """
        if self._chroma_collection is not None:
            try:
                return self._chroma_collection.count()
            except Exception:
                pass
        return len(self.local_sparse_cache)

    def _legacy_collection_rows(self) -> Optional[int]:
        """Rows in the old `integra_hoard` collection, read once and kept: this code never writes to it, and the
        telemetry route is polled every second."""
        if self._legacy_rows_cache is not None:
            return self._legacy_rows_cache
        if self._chroma_client is None:
            return None
        try:
            self._legacy_rows_cache = self._chroma_client.get_collection(LEGACY_COLLECTION).count()
        except Exception:
            return None
        return self._legacy_rows_cache

    def _shard_path(self, ccid: str) -> str:
        return os.path.join(self.kernel_memory_dir, "hoard", "raw_shards", f"{ccid}.json")

    # ─────────────────────────────────────────────
    #  COMMIT: v2 (Full Schema)
    # ─────────────────────────────────────────────

    def commit_node_v2(
        self,
        payload: Any,
        spacetime_anchor: Dict[str, Any],
        ccid: str,
        embedding_64d: Optional[List[float]] = None,
        embedding_768d: Optional[List[float]] = None,
        outcome_label: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
        embed_space: Optional[str] = None,
        celestial_stamp: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Commits a fully-schemed HoardNode, outcome label, and temporal metadata.
        A caller that supplies a vector must also say which space it is in (`embed_space`);
        a vector without a space is stored but not indexed or searched.

        Every new node carries a Celestial Sentinel stamp (the caller's, or one taken now). The anchor's `t` is
        filled with the stamp's time when the caller left it missing or 0; a `t` the caller gave is kept.

        Also persists the node as a raw shard to kernel_memory/hoard/raw_shards/.
        """
        anchor = dict(spacetime_anchor or {})
        node = HoardNode(
            ccid=ccid,
            payload=payload,
            spacetime_anchor=anchor,
            embedding_64d=embedding_64d,
            embedding_768d=embedding_768d,
            outcome_label=outcome_label,
            metadata=metadata,
            embed_space=embed_space,
            created_at=celestial_stamp["unix"] if celestial_stamp else None,
            celestial_stamp=celestial_stamp,
        )
        if not anchor.get("t"):
            anchor["t"] = node.created_at
        self.local_sparse_cache.append(node)

        # Persist to raw_shards/ via xv6 crash-safe write-ahead transaction logger
        shard_path = self._shard_path(ccid)
        node_dict = node.to_dict()
        try:
            self.wal.begin_op()
            self.wal.log_write(shard_path, node_dict)
            self.wal.end_op()
        except Exception as e:
            print(f"[HOARD] WAL commit fallback for shard {ccid}: {e}")
            try:
                _write_json_atomic(shard_path, node_dict)
            except Exception as inner_e:
                print(f"[HOARD] Failed to persist shard {ccid}: {inner_e}")

        # Populate Hot RAM Cache
        self.hot_cache.put(ccid, node_dict)

        # Mirror node record to MongoDB persistent placeholder file point
        try:
            from memory.database.mongodb_substrate import MONGODB_SUBSTRATE

            MONGODB_SUBSTRATE.get_collection("hoard_nodes_mirror").update_one(
                {"ccid": ccid},
                {
                    "$set": {
                        "ccid": ccid,
                        "shard_file": shard_path,
                        "created_at": node.created_at,
                        "outcome_label": node.outcome_label,
                        "embed_space": node.embed_space,
                        "has_vector": node.has_vector,
                    }
                },
                upsert=True,
            )
        except Exception:
            pass

        # Upsert to ChromaDB for semantic vector search (only a vector in the active space is indexed)
        chroma_synced = self.chroma_upsert(node)

        return {
            "status": "COMMITTED_TO_HOARD_V2",
            "node_index": len(self.local_sparse_cache) - 1,
            "ccid": ccid,
            "file": shard_path,
            "schema_version": "2.1",
            "has_embeddings": embedding_768d is not None,
            "embed_space": node.embed_space,
            "chroma_synced": chroma_synced,
        }

    # ─────────────────────────────────────────────
    #  COMMIT: v1 (Backward-Compatible Legacy)
    # ─────────────────────────────────────────────

    def commit_node(
        self, payload: Any, vector_4d: Dict[str, Any], ccid: str,
        celestial_stamp: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Legacy-compatible commit. Wraps commit_node_v2 with no vector
        and outcome_label = 0.5 (UNKNOWN).
        """
        result = self.commit_node_v2(
            payload=payload,
            spacetime_anchor=vector_4d,
            ccid=ccid,
            celestial_stamp=celestial_stamp,
        )
        # Legacy callers expect "COMMITTED_TO_HOARD" status
        result["status"] = "COMMITTED_TO_HOARD"
        # Legacy callers expect "file" key
        return result

    # ─────────────────────────────────────────────
    #  OUTCOME LABELING (Post-Hoc)
    # ─────────────────────────────────────────────

    def mark_outcome(self, ccid: str, outcome: float) -> bool:
        """
        Post-hoc label a committed node with a success/failure outcome.

        Args:
            ccid: The CCID of the node to label.
            outcome: 1.0 = SUCCESS, 0.0 = FAILURE, 0.5 = UNKNOWN.

        Returns:
            True if the node was found and labeled, False otherwise.
        """
        for node in self.local_sparse_cache:
            if node.ccid == ccid:
                node.outcome_label = outcome
                # Update the on-disk shard
                shard_path = self._shard_path(ccid)
                if os.path.exists(shard_path):
                    try:
                        with open(shard_path, "r+", encoding="utf-8") as f:
                            data = json.load(f)
                            data["outcome_label"] = outcome
                            f.seek(0)
                            json.dump(data, f, indent=2)
                            f.truncate()
                    except Exception:
                        pass
                return True
        return False

    # ─────────────────────────────────────────────
    #  STALENESS TRACKING
    # ─────────────────────────────────────────────

    def get_stale_nodes(self, stale_threshold_seconds: float = 604800.0) -> List[HoardNode]:
        """
        Returns all nodes that have exceeded the temporal staleness threshold.
        Default: 7 days (604800 seconds).

        Used by Phoenix SWDS consolidation to identify nodes needing refresh.
        """
        current_time = celestial_time()
        stale = []
        for node in self.local_sparse_cache:
            age = current_time - node.created_at
            if age > stale_threshold_seconds:
                node.is_stale = True
                stale.append(node)
        return stale

    # ─────────────────────────────────────────────
    #  RODIN INTEGRATION: Get Candidate Pool
    # ─────────────────────────────────────────────

    def get_rodin_candidates(self, space_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Returns cached nodes in Rodin-compatible format.
        Each dict contains 'embedding' (768d), 'embed_space', 'outcome_label', 'created_at',
        matching the field names that RodinProtocol expects. With `space_id`, only nodes
        that hold a vector in that space are returned.
        """
        nodes = self.local_sparse_cache
        if space_id is not None:
            nodes = [n for n in nodes if n.has_vector and n.embed_space == space_id]
        return [node.to_rodin_candidate() for node in nodes]

    # ─────────────────────────────────────────────
    #  QUERY: Substring (Legacy Internal)
    # ─────────────────────────────────────────────

    def query_internal(self, query_terms: List[str]) -> List[Dict[str, Any]]:
        """
        Legacy substring-matching query over the local sparse cache.
        Returns matching nodes as dicts for backward compatibility.
        """
        results = []
        for node in self.local_sparse_cache:
            payload_str = json.dumps(node.payload).lower()
            if any(term.lower() in payload_str for term in query_terms):
                results.append(node.to_dict())
        return results

    # ─────────────────────────────────────────────
    #  LOAD FROM DISK (Bootstrap)
    # ─────────────────────────────────────────────

    def load_shards_from_disk(self) -> int:
        """
        Loads all raw shard JSON files from kernel_memory/hoard/raw_shards/
        into the local_sparse_cache. Used at startup to restore state.
        A file that is not a node (no `ccid` and `payload`) is skipped, so it can never be rewritten as one;
        the counts are kept in `last_load_report`.

        Returns:
            Number of shards loaded.
        """
        shards_dir = os.path.join(self.kernel_memory_dir, "hoard", "raw_shards")
        nodes, report = load_nodes_from_shards(shards_dir)
        existing_ccids = {n.ccid for n in self.local_sparse_cache}
        loaded = 0
        for node in nodes:
            # Avoid duplicates
            if node.ccid not in existing_ccids:
                existing_ccids.add(node.ccid)
                self.local_sparse_cache.append(node)
                loaded += 1
        report["loaded"] = loaded
        self.last_load_report = report
        return loaded

    # ─────────────────────────────────────────────
    #  EMBEDDING: the explicit step (dry-run by default)
    # ─────────────────────────────────────────────

    def _merge_embedding_into_shard(self, node: "HoardNode", vector: List[float], space_id: str) -> None:
        """Update only the three embedding keys of the node's shard, keeping everything else in the file as it is."""
        path = self._shard_path(node.ccid)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)  # an unreadable shard raises: it is never overwritten
            if not isinstance(data, dict):
                raise ValueError(f"{path} is not a JSON object")
        else:
            data = node.to_dict()
        data["embedding_768d"] = vector
        data["embedding_64d"] = vector[:64]
        data["embed_space"] = space_id
        _write_json_atomic(path, data)

    def embed_pending(
        self,
        embedder: Optional[EmbeddingService] = None,
        *,
        limit: Optional[int] = None,
        dry_run: bool = True,
        batch_size: int = 16,
        pause_s: float = 0.0,
        sleep=time.sleep,
    ) -> Dict[str, Any]:
        """
        Embeds every node that has no trusted vector in the active space: nodes with no vector, with a vector
        that names no space (untrusted), or with a vector from another space.

        dry_run=True (the default) only counts and prices; it never contacts the embedding API.
        With dry_run=False: identical (text, title) pairs are embedded once; batches go out `batch_size` pairs at a
        time; the first failure stops the run and is reported (`stopped_early`, `error`) with the progress made;
        each shard is updated atomically and only after its vector arrived. `limit` caps the unique pairs of this run.
        `pause_s` waits that long between batches (pacing: a rate limit is a certainty on a free key).
        """
        unique, pending, already, skipped_empty = _group_pending(self.local_sparse_cache, self.space, limit)
        receipt: Dict[str, Any] = _plan_dict(self.space, unique, pending, already, skipped_empty, dry_run)
        receipt.update({"embedded": 0, "texts_sent": 0, "stopped_early": False, "error": None, "shard_errors": []})
        if dry_run:
            return receipt

        if self.config_error:
            raise EmbeddingUnavailable("BAD_CONFIG", self.config_error)
        service = embedder or self.embedder or get_default_embedding_service()
        if service.space != self.space:
            raise ValueError(f"embedder space {service.space.id} differs from the Hoard's {self.space.id}")

        sent_before = service.stats().get("texts_sent", 0) if hasattr(service, "stats") else 0
        for off in range(0, len(unique), max(1, int(batch_size))):
            if off > 0 and pause_s > 0:
                sleep(pause_s)
            batch = unique[off: off + max(1, int(batch_size))]
            try:
                results = service.embed_documents([(text, title) for (text, title), _ in batch])
            except EmbeddingUnavailable as exc:
                receipt["stopped_early"] = True
                receipt["error"] = {"code": exc.code, "detail": exc.detail}
                break
            for ((_, _), nodes), res in zip(batch, results):
                for node in nodes:
                    try:
                        self._merge_embedding_into_shard(node, res.vector, self.space.id)
                    except Exception as exc:  # noqa: BLE001  (a shard that cannot be written keeps its old vector state)
                        receipt["shard_errors"].append({"ccid": node.ccid, "error": f"{type(exc).__name__}: {exc}"})
                        continue
                    node.embedding_768d = list(res.vector)
                    node.embedding_64d = list(res.vector[:64])
                    node.embed_space = self.space.id
                    self.chroma_upsert(node)
                    receipt["embedded"] += 1
        if hasattr(service, "stats"):
            receipt["texts_sent"] = service.stats().get("texts_sent", 0) - sent_before
        return receipt

    # ─────────────────────────────────────────────
    #  SAVE STATE SYNCHRONIZATION
    # ─────────────────────────────────────────────

    def sync_save_state(self, file_path_or_dict: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synchronizes an external Save State (e.g. from The_Hoard/CCID_*.json)
        into The Hoard's kernel_memory manifold.

        Extracts:
            - ccid
            - celestial spacetime anchor
            - cognitive telemetry, identity matrix, and work inventory as payload
            - Sets outcome_label = 1.0 (verified system save state)
            - Commits via commit_node_v2 into raw_shards and local_sparse_cache

        The node is embedded only when this Hoard was given an embedder; otherwise it is stored without a vector
        (embedding_status PENDING) and embed_pending() embeds it later. A failed embedding never blocks the sync:
        the node is stored without a vector and the receipt carries the error. No vector is ever invented.
        """
        if isinstance(file_path_or_dict, str):
            with open(file_path_or_dict, "r", encoding="utf-8") as f:
                data = json.load(f)
            source_file = file_path_or_dict
        else:
            data = file_path_or_dict
            source_file = "MEMORY_DICT"

        ccid = data.get("ccid", celestial_ccid())
        celestial_stamp = data.get("celestial_stamp", {})

        # Construct 4D spacetime anchor
        spacetime_anchor = {
            "x": 30.5888,
            "y": -91.1673,
            "z": 0.0,
            "t": celestial_stamp.get("unix_epoch", celestial_time()),
            "anchor": celestial_stamp.get("anchor", "Baker, Louisiana"),
            "civil_time": celestial_stamp.get("civil_time_utc", "")
        }

        # The full save state context forms the payload
        payload = {
            "identity_matrix": data.get("identity_matrix", {}),
            "cognitive_telemetry": data.get("cognitive_telemetry", {}),
            "work_completed": data.get("work_completed_this_session", data.get("work_inventory", {}).get("completed", [])),
            "work_pending": data.get("work_pending", data.get("work_inventory", {}).get("pending", [])),
            "type": "SAVE_STATE_CHECKPOINT"
        }

        embedding_768d: Optional[List[float]] = None
        embedding_64d: Optional[List[float]] = None
        embed_space: Optional[str] = None
        embedding_error: Optional[Dict[str, str]] = None
        if self.embedder is not None:
            text, title = node_embedding_text(HoardNode(ccid=ccid, payload=payload, spacetime_anchor=spacetime_anchor))
            try:
                res = self.embedder.embed_document(text, title)
                embedding_768d, embedding_64d, embed_space = res.vector, res.vector[:64], res.space.id
            except EmbeddingUnavailable as exc:
                embedding_error = {"code": exc.code, "detail": exc.detail}
                logger.warning("save state %s stored without a vector: %s", ccid, exc)

        # Save states are verified successful states -> outcome_label = 1.0
        commit_res = self.commit_node_v2(
            payload=payload,
            spacetime_anchor=spacetime_anchor,
            ccid=ccid,
            embedding_64d=embedding_64d,
            embedding_768d=embedding_768d,
            outcome_label=1.0,
            metadata={"source_file": source_file, "is_checkpoint": True},
            embed_space=embed_space,
        )

        receipt = {
            "status": "SAVE_STATE_SYNCED_TO_HOARD",
            "ccid": ccid,
            "shard_file": commit_res["file"],
            "source": source_file,
            "mrl_embeddings_created": embed_space is not None,
            "embedding_status": "EMBEDDED" if embed_space is not None else "PENDING",
            "embed_space": embed_space,
            "outcome_label": 1.0
        }
        if embedding_error is not None:
            receipt["embedding_error"] = embedding_error
        return receipt

    def sync_all_save_states(self, source_dir: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Scans directory (defaults to 'The_Hoard' at project root) for all CCID_*.json
        save states and syncs them into the Hoard manifold.
        """
        target_dir = source_dir or os.path.join(self.root_dir, "The_Hoard")
        synced = []
        if not os.path.isdir(target_dir):
            return synced

        for fname in sorted(os.listdir(target_dir)):
            if fname.startswith("CCID_") and fname.endswith(".json"):
                fpath = os.path.join(target_dir, fname)
                try:
                    res = self.sync_save_state(fpath)
                    synced.append(res)
                except Exception as e:
                    print(f"[HOARD] Failed to sync save state {fname}: {e}")

        return synced

    # ─────────────────────────────────────────────
    #  TELEMETRY
    # ─────────────────────────────────────────────

    def get_telemetry(self, include_legacy_rows: bool = False) -> Dict[str, Any]:
        """
        Returns a snapshot of the Hoard's current state for Heimdall monitoring. It reads the in-memory nodes only: no
        ChromaDB call is made unless `include_legacy_rows` asks for the legacy collection's size, because this runs
        inside an async route that is polled every second, and a native ChromaDB call there can wedge the server.
        """
        stale_count = sum(1 for n in self.local_sparse_cache if n.is_stale)
        labeled_count = sum(1 for n in self.local_sparse_cache if n.outcome_label != 0.5)
        embedded = untrusted = other_space = unembedded = 0
        for n in self.local_sparse_cache:
            if n.has_vector and n.embed_space == self.space.id:
                embedded += 1
            elif n.has_vector:
                other_space += 1
            elif any(v != 0.0 for v in n.embedding_768d):
                untrusted += 1
            else:
                unembedded += 1
        return {
            "total_nodes": len(self.local_sparse_cache),
            "stale_nodes": stale_count,
            "labeled_nodes": labeled_count,
            "embedded_nodes": embedded,
            "unembedded_nodes": unembedded,
            "untrusted_vector_nodes": untrusted,
            "other_space_nodes": other_space,
            "active_space": self.space.id,
            "chroma_collection": self._chroma_collection_name,
            "vector_search_available": self.vector_search_available(),
            "legacy_collection_rows": self._legacy_collection_rows() if include_legacy_rows else None,
            "config_error": self.config_error,
            "schema_version": "2.1",
            "kernel_memory_dir": self.kernel_memory_dir,
        }

    # ─────────────────────────────────────────────
    #  EAM AUTO-CRYSTALLIZATION (Block 6 / Phase D)
    # ─────────────────────────────────────────────

    def auto_crystallize(
        self,
        session_id: str,
        cycle_iteration: int,
        input_momentum: float = 1.0,
        exit_momentum: float = 1.0,
        entropy_generated: float = 0.0,
        entropy_flushed: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        EAM Auto-Crystallization: Records a thermodynamic loop to the Metatron
        Manifold and simultaneously commits a Hoard node capturing the system
        state at this moment.

        This is the mechanical bridge between the thermodynamic enforcement
        substrate (Block 1) and the geometric memory manifold (Layer 3).

        Args:
            session_id: Active CCID session identifier.
            cycle_iteration: Loop iteration counter.
            input_momentum: Angular momentum entering the cycle.
            exit_momentum: Angular momentum exiting the cycle.
            entropy_generated: Lactic acid entropy produced.
            entropy_flushed: Entropy cleared via P-SSR.
            metadata: Optional additional metadata.

        Returns:
            Dict with both the loop recording result and the Hoard commit result.
        """
        # Record to Metatron Manifold
        loop_result = None
        try:
            from memory.database.metatron_deploy import record_loop
            loop_result = record_loop(
                session_id=session_id,
                cycle_iteration=cycle_iteration,
                input_momentum=input_momentum,
                exit_momentum=exit_momentum,
                entropy_generated=entropy_generated,
                entropy_flushed=entropy_flushed,
            )
        except Exception as e:
            loop_result = {"status": "METATRON_ERROR", "error": str(e)}

        # One Celestial Sentinel stamp gives the anchor time, the CCID and the node's stamp
        stamp = _new_celestial_stamp("crystallization")
        t_now = stamp["unix"] if stamp else celestial_time()
        spacetime_anchor = {
            "x": 0.0, "y": 0.0, "z": 0.0,
            "t": t_now,
            "session_id": session_id,
            "cycle": cycle_iteration,
        }

        # Commit crystallization node to Hoard
        ccid = f"CCID_CRYSTAL_{int(t_now)}_{cycle_iteration}"
        payload = {
            "type": "auto_crystallization",
            "session_id": session_id,
            "cycle_iteration": cycle_iteration,
            "delta_e": round(abs(exit_momentum - input_momentum), 6),
            "loop_result": loop_result,
            "metadata": metadata or {},
        }

        hoard_result = self.commit_node_v2(
            payload=payload,
            spacetime_anchor=spacetime_anchor,
            ccid=ccid,
            metadata={"source": "auto_crystallize", "block": 6},
            celestial_stamp=stamp,
        )

        return {
            "crystallization": "COMPLETE",
            "loop": loop_result,
            "hoard": hoard_result,
            "ccid": ccid,
        }

    def hydrate_all_cold_storage(self) -> Dict[str, Any]:
        """
        Task L-2: Unified Cold-to-Hot Hydration.
        1. Recovers any uncommitted xv6 WAL blocks on startup.
        2. Loads all raw shards from `kernel_memory/hoard/raw_shards/`.
        3. Scans `The_Hoard/` and parent `The Hoard/` for `CCID_*.json` save states.
        4. Hydrates loaded nodes into `HotStorageRAMCache` and mirrors to MongoDB placeholder.
        """
        wal_recovery = self.wal.recover_from_log()
        raw_loaded = self.load_shards_from_disk()
        synced_states = self.sync_all_save_states()

        for node in self.local_sparse_cache[-self.hot_cache.max_hot_nodes :]:
            self.hot_cache.put(node.ccid, node.to_dict())

        # Mirror metadata summary into MongoDB placeholder collection
        try:
            from memory.database.mongodb_substrate import MONGODB_SUBSTRATE

            col = MONGODB_SUBSTRATE.get_collection("hoard_nodes_mirror")
            for node in self.local_sparse_cache[-32:]:
                col.update_one(
                    {"ccid": node.ccid},
                    {
                        "$set": {
                            "ccid": node.ccid,
                            "created_at": node.created_at,
                            "outcome_label": node.outcome_label,
                            "embed_space": node.embed_space,
                            "has_vector": node.has_vector,
                        }
                    },
                    upsert=True,
                )
        except Exception:
            pass

        seed_sync = self.link_and_sync_seed_package()

        return {
            "status": "HOARD_COLD_STORAGE_HYDRATED",
            "wal_recovery": wal_recovery,
            "raw_shards_loaded": raw_loaded,
            "save_states_synced": len(synced_states),
            "total_in_memory_nodes": len(self.local_sparse_cache),
            "hot_ram_cache_count": len(self.hot_cache.hot_ram),
            "cold_vault_z1_count": len(self.hot_cache.cold_vault_index),
            "seed_package_sync": seed_sync,
        }

    def link_and_sync_seed_package(
        self,
        month_key: Optional[str] = None,
        phoenix_instance: Any = None,
    ) -> Dict[str, Any]:
        """
        Task L-3.5: Links the Seed Package to The Hoard and Phoenix Forge, persists it to
        `kernel_memory/hoard/seed_packages/`, and syncs it to MongoDB monthly uploads
        and quarterly save states.
        """
        try:
            from memory.database.mongodb_substrate import SEED_PACKAGE_MANAGER

            return SEED_PACKAGE_MANAGER.build_and_sync_monthly_seed_package(
                month_key=month_key,
                hoard_instance=self,
                phoenix_instance=phoenix_instance,
            )
        except Exception as exc:
            return {"status": "SEED_SYNC_ERROR", "error": str(exc)}



class Xv6TransactionLogger:
    """
    Curriculum Document 9 (xv6 Chapter 8: File System Logging) Crash-Safe Transaction Logger.
    Enforces:
      - `begin_op()` -> `log_write()` (with `MAXOPBLOCKS = 10` log absorption) -> `end_op()`
      - Two-phase commit: writes header (`n > 0`) to `xv6_wal.json`, installs blocks to target paths,
        then zeroes header (`n = 0`) and mirrors committed transaction receipts to MongoDB placeholder.
    """

    MAXOPBLOCKS = 10

    def __init__(self, wal_path: str):
        self.wal_path = wal_path
        os.makedirs(os.path.dirname(self.wal_path), exist_ok=True)
        if not os.path.isfile(self.wal_path):
            _write_json_atomic(self.wal_path, {"n": 0, "timestamp": time.time(), "blocks": [], "status": "INITIALIZED_CLEAN"})
        self.outstanding: int = 0
        self.committing: bool = False
        self.pending_blocks: "OrderedDict[str, Any]" = OrderedDict()
        self.total_committed_ops: int = 0

    def begin_op(self) -> Dict[str, Any]:
        if self.committing:
            raise RuntimeError("Xv6TransactionLogger is currently committing; cannot begin_op.")
        self.outstanding += 1
        return {"status": "OP_BEGUN", "outstanding": self.outstanding}

    def log_write(self, target_path: str, payload: Any) -> Dict[str, Any]:
        """
        Records a block write in the in-memory transaction log.
        Repeated writes to the same `target_path` within an active transaction are absorbed
        (log absorption), conserving the `MAXOPBLOCKS = 10` slot limit.
        """
        norm_path = os.path.abspath(target_path)
        absorbed = norm_path in self.pending_blocks
        if not absorbed and len(self.pending_blocks) >= self.MAXOPBLOCKS:
            raise BufferError(
                f"Xv6TransactionLogger exceeded MAXOPBLOCKS ({self.MAXOPBLOCKS}); commit before adding more blocks."
            )
        self.pending_blocks[norm_path] = payload
        return {
            "status": "LOG_ABSORBED" if absorbed else "LOG_QUEUED",
            "target_path": norm_path,
            "queued_blocks": len(self.pending_blocks),
            "max_op_blocks": self.MAXOPBLOCKS,
        }

    def end_op(self) -> Dict[str, Any]:
        if self.outstanding <= 0:
            return {"status": "NO_ACTIVE_OP", "committed_blocks": 0}
        self.outstanding -= 1
        if self.outstanding > 0:
            return {"status": "DEFERRED_GROUP_COMMIT", "outstanding": self.outstanding}

        self.committing = True
        try:
            block_items = [
                {"target_path": p, "payload": data}
                for p, data in self.pending_blocks.items()
            ]
            n_blocks = len(block_items)
            if n_blocks > 0:
                # Step 1: Write WAL commit header (n > 0)
                wal_header = {
                    "n": n_blocks,
                    "timestamp": time.time(),
                    "blocks": block_items,
                }
                _write_json_atomic(self.wal_path, wal_header)

                # Step 2: Install blocks to home locations on disk
                for item in block_items:
                    os.makedirs(os.path.dirname(item["target_path"]), exist_ok=True)
                    _write_json_atomic(item["target_path"], item["payload"])

                # Step 3: Zero WAL header (n = 0 -> transaction complete)
                _write_json_atomic(self.wal_path, {"n": 0, "timestamp": time.time(), "blocks": []})
                self.total_committed_ops += 1

                # Mirror WAL receipt to MongoDB persistent placeholder
                try:
                    from memory.database.mongodb_substrate import MONGODB_SUBSTRATE

                    wal_col = MONGODB_SUBSTRATE.get_collection("xv6_transaction_wal")
                    wal_col.insert_one({
                        "op_index": self.total_committed_ops,
                        "committed_blocks": n_blocks,
                        "paths": [b["target_path"] for b in block_items],
                        "header_zeroed": True,
                        "committed_at": time.time(),
                    })
                except Exception:
                    pass

            self.pending_blocks.clear()
            return {
                "status": "COMMITTED",
                "committed_blocks": n_blocks,
                "header_n": 0,
                "total_committed_ops": self.total_committed_ops,
            }
        finally:
            self.committing = False

    def recover_from_log(self) -> Dict[str, Any]:
        """
        Crash recovery on startup: if `xv6_wal.json` has `n > 0`, replays all logged blocks
        to their home locations and then zeroes `n = 0`.
        """
        if not os.path.exists(self.wal_path):
            return {"status": "CLEAN_NO_WAL", "replayed_blocks": 0}
        try:
            with open(self.wal_path, "r", encoding="utf-8") as f:
                wal_data = json.load(f)
        except Exception:
            return {"status": "UNREADABLE_WAL_SKIPPED", "replayed_blocks": 0}

        n = int(wal_data.get("n", 0))
        blocks = wal_data.get("blocks", [])
        replayed = 0
        if n > 0 and isinstance(blocks, list):
            for item in blocks[:n]:
                tpath = item.get("target_path")
                if tpath and "payload" in item:
                    os.makedirs(os.path.dirname(tpath), exist_ok=True)
                    _write_json_atomic(tpath, item["payload"])
                    replayed += 1
            _write_json_atomic(self.wal_path, {"n": 0, "timestamp": time.time(), "blocks": []})
            return {"status": "RECOVERED_FROM_WAL", "replayed_blocks": replayed}
        return {"status": "CLEAN_HEADER_ZERO", "replayed_blocks": 0}


class HotStorageRAMCache:
    """
    Task L-2 (`IntegraBrainMap` Task 2): Two-Tier Hot RAM / Cold Vault (`Z1_SOUTH_POLE`) Memory Manager.
    - Active nodes reside in `hot_ram` (`OrderedDict` LRU).
    - Evicted or explicitly archived nodes are shunted to `cold_vault_z1/` (`COLD_VAULT_SHUNTED`)
      with `latitudinal_zone = "Z1_SOUTH_POLE"`.
    - Querying a cold node transparently rehydrates it back into `hot_ram` (`REHYDRATED_INTO_HOT_RAM`).
    """

    def __init__(self, cold_vault_dir: str, max_hot_nodes: int = 256):
        self.cold_vault_dir = cold_vault_dir
        os.makedirs(self.cold_vault_dir, exist_ok=True)
        self.manifest_path = os.path.join(self.cold_vault_dir, "cold_vault_manifest.json")
        if not os.path.isfile(self.manifest_path):
            _write_json_atomic(
                self.manifest_path,
                {
                    "vault_id": "COLD_VAULT_Z1_SOUTH_POLE",
                    "latitudinal_zone": "Z1_SOUTH_POLE",
                    "status": "ACTIVE_READY",
                    "cold_vault_dir": self.cold_vault_dir,
                    "initialized_at": time.time(),
                },
            )
        self.max_hot_nodes = max(1, int(max_hot_nodes))
        self.hot_ram: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
        self.cold_vault_index: Dict[str, str] = {}

    def _cold_path(self, ccid: str) -> str:
        safe = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in str(ccid))
        return os.path.join(self.cold_vault_dir, f"{safe}.json")

    def put(self, ccid: str, node_dict: Dict[str, Any]) -> Dict[str, Any]:
        shunted_ccid = None
        if ccid in self.hot_ram:
            self.hot_ram.move_to_end(ccid)
        self.hot_ram[ccid] = dict(node_dict)
        if len(self.hot_ram) > self.max_hot_nodes:
            oldest_ccid, oldest_data = self.hot_ram.popitem(last=False)
            self.shunt_to_cold_vault(oldest_ccid, oldest_data)
            shunted_ccid = oldest_ccid
        return {
            "status": "STORED_IN_HOT_RAM",
            "ccid": ccid,
            "hot_count": len(self.hot_ram),
            "evicted_to_cold_z1": shunted_ccid,
        }

    def shunt_to_cold_vault(self, ccid: str, node_dict: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Moves a node out of Hot RAM into the `Z1_SOUTH_POLE` Cold Storage Vault on disk."""
        data = dict(node_dict or self.hot_ram.pop(ccid, {}))
        data["ccid"] = ccid
        data["latitudinal_zone"] = "Z1_SOUTH_POLE"
        data["storage_tier"] = "COLD_VAULT_Z1"
        data["shunted_at"] = time.time()
        cpath = self._cold_path(ccid)
        _write_json_atomic(cpath, data)
        self.cold_vault_index[ccid] = cpath
        self.hot_ram.pop(ccid, None)
        return {
            "status": "COLD_VAULT_SHUNTED",
            "ccid": ccid,
            "latitudinal_zone": "Z1_SOUTH_POLE",
            "cold_file": cpath,
        }

    def retrieve(self, ccid: str) -> Dict[str, Any]:
        """Retrieves from Hot RAM in O(1), or transparently rehydrates from `Z1_SOUTH_POLE` Cold Vault."""
        if ccid in self.hot_ram:
            self.hot_ram.move_to_end(ccid)
            return {
                "status": "HOT_RAM_HIT",
                "ccid": ccid,
                "node": self.hot_ram[ccid],
            }
        cpath = self.cold_vault_index.get(ccid) or self._cold_path(ccid)
        if os.path.exists(cpath):
            with open(cpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["storage_tier"] = "HOT_RAM_REHYDRATED"
            self.put(ccid, data)
            return {
                "status": "REHYDRATED_INTO_HOT_RAM",
                "ccid": ccid,
                "node": data,
            }
        return {"status": "NOT_FOUND", "ccid": ccid, "node": None}


# NOTE: RodinProtocol has been consolidated into memory/rodin_protocol.py
# which implements the real Matryoshka Representation Learning (MRL) and
# Cosine Similarity retrieval. Import from there:
#   from memory.rodin_protocol import RodinProtocol

