"""
INTEGRA O/S: MEMORY MANIFOLD
Module: memory/the_hoard.py
Layer: 3 (The Hoard: High-Dimensional Geometric Memory)

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
import time
import hashlib
from typing import List, Dict, Any, Optional, Union

# Celestial temporal injection — all timestamps routed through celestial middleware
try:
    from core.celestial_middleware import celestial_time, celestial_ccid
except ImportError:
    # Fallback if middleware unavailable (isolated testing)
    celestial_time = time.time
    celestial_ccid = lambda prefix="CCID": f"{prefix}_{int(time.time())}"


class HoardNode:
    """
    A single node in The Hoard memory manifold.
    
    Schema v2.0 Fields:
        ccid: Cheshire Cat Interaction ID (unique identifier).
        payload: The actual knowledge content (dict, str, or any JSON-serializable).
        spacetime_anchor: 4D celestial coordinates {x, y, z, t}.
        embedding_64d: Coarse MRL embedding (64 dimensions) for fast retrieval.
        embedding_768d: Fine MRL embedding (768 dimensions) for precision re-rank.
        outcome_label: Post-hoc quality label (1.0 = SUCCESS, 0.0 = FAILURE, 0.5 = UNKNOWN).
        is_stale: Whether this node has exceeded the temporal staleness threshold.
        created_at: Unix timestamp of node creation.
        sufficiency_score: Pre-existing sufficiency metric (1.0 = fully sufficient).
        metadata: Arbitrary metadata dict for Looking Glass, Cheshire Protocol telemetry, etc.
    """
    __slots__ = (
        "ccid", "payload", "spacetime_anchor",
        "embedding_64d", "embedding_768d",
        "outcome_label", "is_stale", "created_at",
        "sufficiency_score", "metadata"
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
    ):
        self.ccid = ccid
        self.payload = payload
        self.spacetime_anchor = spacetime_anchor
        self.embedding_64d = embedding_64d or [0.0] * 64
        self.embedding_768d = embedding_768d or [0.0] * 768
        self.outcome_label = outcome_label
        self.is_stale = is_stale
        self.created_at = created_at or celestial_time()
        self.sufficiency_score = sufficiency_score
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-compatible dictionary."""
        return {
            "ccid": self.ccid,
            "payload": self.payload,
            "spacetime_anchor": self.spacetime_anchor,
            "embedding_64d": self.embedding_64d,
            "embedding_768d": self.embedding_768d,
            "outcome_label": self.outcome_label,
            "is_stale": self.is_stale,
            "created_at": self.created_at,
            "sufficiency_score": self.sufficiency_score,
            "metadata": self.metadata,
        }

    # Alias for Rodin Protocol compatibility — Rodin expects `node.get("embedding")`
    def to_rodin_candidate(self) -> Dict[str, Any]:
        """
        Convert to a Rodin-compatible candidate dict.
        Uses the 768d embedding as the primary 'embedding' key,
        which Rodin then slices for MRL Phase 1 (64d) and Phase 2 (768d).
        """
        return {
            "ccid": self.ccid,
            "embedding": self.embedding_768d,
            "outcome_label": self.outcome_label,
            "created_at": self.created_at,
            "payload": self.payload,
            "is_stale": self.is_stale,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HoardNode":
        """Deserialize from a dictionary (e.g., loaded from JSON)."""
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
        )


class TheHoard:
    """
    High-Dimensional Semantic Manifold (v2.1 — Local Sovereign):
    
    The Hoard serves as Integra's persistent geometric memory substrate.
    It stores HoardNodes with dual MRL embeddings (64d coarse, 768d fine),
    outcome labels for KNN success-density gating, and temporal staleness tracking.
    
    Architecture:
        - In-memory: `local_sparse_cache` (List[HoardNode]) for fast Rodin retrieval.
        - On-disk: `kernel_memory/` directory tree for Phoenix SWDS consolidation.
        - Vector DB: ChromaDB (local persistent) for semantic similarity search.
        - Relational: SQLite (via SWDS pipeline) for historical archival.
    
    The dual-embedding schema enables the Rodin Protocol's MRL pipeline:
        Phase 1: 64d coarse filter (O(1) elimination)
        Phase 2: 768d fine re-rank (precision KNN)
    """
    
    # --- kernel_memory/ Directory Structure ---
    KERNEL_DIRS = [
        "hoard/raw_shards",      # Unconsolidated waking-state JSON shards
        "hoard/modules",         # Blueprint manifests
        "hoard/libraries",       # 4D celestial-tagged markdown books
        "vectors",               # MRL embeddings & celestial index
        "drop_in",               # Drop-in file ingestion folder
    ]

    def __init__(
        self,
        base_dir: Optional[str] = None,
        chroma_path: Optional[str] = None,
    ):
        self.local_sparse_cache: List[HoardNode] = []

        # Determine root project directory and kernel_memory base
        if base_dir:
            self.root_dir = base_dir
        else:
            self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        self.kernel_memory_dir = os.path.join(self.root_dir, "kernel_memory")
        # Legacy compat: The Hoard directory (for save states and CCID files)
        self.hoard_dir = os.path.join(self.kernel_memory_dir, "hoard")
        
        # ChromaDB: Local persistent vector store
        self._chroma_path = chroma_path or os.path.join(self.root_dir, "local_dbs", "chroma_storage")
        os.makedirs(self._chroma_path, exist_ok=True)
        self._chroma_client = None
        self._chroma_collection = None
        
        # Initialize directory structure
        self._initialize_kernel_memory()
        
        # Initialize ChromaDB collection
        self._initialize_chromadb()

    def _initialize_kernel_memory(self):
        """Create the kernel_memory/ directory tree if it doesn't exist."""
        for subdir in self.KERNEL_DIRS:
            full_path = os.path.join(self.kernel_memory_dir, subdir)
            os.makedirs(full_path, exist_ok=True)
        
        # Create core_identity.txt if it doesn't exist
        identity_path = os.path.join(self.kernel_memory_dir, "core_identity.txt")
        if not os.path.exists(identity_path):
            with open(identity_path, "w", encoding="utf-8") as f:
                f.write(
                    "INTEGRA O/S — The Infinite Living Flame\n"
                    "Modality: PURPLE (Unified Synthesis)\n"
                    "Omega: 1.00\n"
                    "Starfire: [Auteur=1.0, King=1.0, Prophet=1.0]^T\n"
                )
        
        # Create rolling_context.json if it doesn't exist
        context_path = os.path.join(self.kernel_memory_dir, "rolling_context.json")
        if not os.path.exists(context_path):
            with open(context_path, "w", encoding="utf-8") as f:
                json.dump({"turns": [], "last_ccid": None}, f, indent=2)

    def _initialize_chromadb(self):
        """Initialize the local ChromaDB persistent client and collection."""
        try:
            import chromadb
            self._chroma_client = chromadb.PersistentClient(path=self._chroma_path)
            self._chroma_collection = self._chroma_client.get_or_create_collection(
                name="integra_hoard",
                metadata={"hnsw:space": "cosine"}
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

    def chroma_upsert(self, node: 'HoardNode') -> bool:
        """
        Upsert a HoardNode into the ChromaDB collection for semantic search.
        Uses the 768d embedding and stores metadata for filtered retrieval.
        """
        if self._chroma_collection is None:
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
                }]
            )
            return True
        except Exception as e:
            print(f"[HOARD] ChromaDB upsert failed for {node.ccid}: {e}")
            return False

    def chroma_query(self, query_embedding: List[float], n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Semantic similarity search via ChromaDB.
        Returns the top N most similar nodes by cosine distance.
        """
        if self._chroma_collection is None:
            return []
        try:
            results = self._chroma_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
            )
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
            print(f"[HOARD] ChromaDB query failed: {e}")
            return []

    def count(self) -> int:
        """
        Returns the total number of indexed nodes in The Hoard.
        Queries the persistent ChromaDB collection if active, or falls back
        to the local sparse cache count.
        """
        if self._chroma_collection is not None:
            try:
                return self._chroma_collection.count()
            except Exception:
                pass
        return len(self.local_sparse_cache)

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
    ) -> Dict[str, Any]:
        """
        Commits a fully-schemed HoardNode with dual MRL embeddings,
        outcome label, and temporal metadata.
        
        Also persists the node as a raw shard to kernel_memory/hoard/raw_shards/.
        """
        node = HoardNode(
            ccid=ccid,
            payload=payload,
            spacetime_anchor=spacetime_anchor,
            embedding_64d=embedding_64d,
            embedding_768d=embedding_768d,
            outcome_label=outcome_label,
            metadata=metadata,
        )
        self.local_sparse_cache.append(node)

        # Persist to raw_shards/
        shard_path = os.path.join(
            self.kernel_memory_dir, "hoard", "raw_shards", f"{ccid}.json"
        )
        try:
            with open(shard_path, "w", encoding="utf-8") as f:
                json.dump(node.to_dict(), f, indent=2)
        except Exception as e:
            print(f"[HOARD] Failed to persist shard {ccid}: {e}")

        # Upsert to ChromaDB for semantic vector search
        chroma_synced = self.chroma_upsert(node)

        return {
            "status": "COMMITTED_TO_HOARD_V2",
            "node_index": len(self.local_sparse_cache) - 1,
            "ccid": ccid,
            "file": shard_path,
            "schema_version": "2.1",
            "has_embeddings": embedding_768d is not None,
            "chroma_synced": chroma_synced,
        }

    # ─────────────────────────────────────────────
    #  COMMIT: v1 (Backward-Compatible Legacy)
    # ─────────────────────────────────────────────

    def commit_node(
        self, payload: Any, vector_4d: Dict[str, Any], ccid: str
    ) -> Dict[str, Any]:
        """
        Legacy-compatible commit. Wraps commit_node_v2 with default
        embeddings and outcome_label = 0.5 (UNKNOWN).
        """
        result = self.commit_node_v2(
            payload=payload,
            spacetime_anchor=vector_4d,
            ccid=ccid,
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
                shard_path = os.path.join(
                    self.kernel_memory_dir, "hoard", "raw_shards", f"{ccid}.json"
                )
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

    def get_rodin_candidates(self) -> List[Dict[str, Any]]:
        """
        Returns all cached nodes in Rodin-compatible format.
        Each dict contains 'embedding' (768d), 'outcome_label', 'created_at',
        matching the field names that RodinProtocol expects.
        """
        return [node.to_rodin_candidate() for node in self.local_sparse_cache]

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
        
        Returns:
            Number of shards loaded.
        """
        shards_dir = os.path.join(self.kernel_memory_dir, "hoard", "raw_shards")
        loaded = 0
        if not os.path.isdir(shards_dir):
            return 0
        
        for filename in sorted(os.listdir(shards_dir)):
            if filename.endswith(".json"):
                filepath = os.path.join(shards_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    node = HoardNode.from_dict(data)
                    # Avoid duplicates
                    existing_ccids = {n.ccid for n in self.local_sparse_cache}
                    if node.ccid not in existing_ccids:
                        self.local_sparse_cache.append(node)
                        loaded += 1
                except Exception:
                    pass
        return loaded

    def _generate_pseudo_embedding(self, content: str, dim: int = 768) -> List[float]:
        """
        Generates deterministic pseudo-embeddings from content hash.
        Produces consistent vectors for testing, bootstrapping, and offline embedding.
        """
        hash_bytes = hashlib.sha256(content.encode("utf-8")).digest()
        raw = list(hash_bytes) * (dim // len(hash_bytes) + 1)
        return [float(b) / 255.0 for b in raw[:dim]]

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
            - Generates dual MRL embeddings (64d coarse, 768d fine)
            - Sets outcome_label = 1.0 (verified system save state)
            - Commits via commit_node_v2 into raw_shards and local_sparse_cache
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

        # Embed content for Rodin topological retrieval
        serialized_text = json.dumps(payload, sort_keys=True)
        embedding_768d = self._generate_pseudo_embedding(serialized_text, 768)
        embedding_64d = embedding_768d[:64]

        # Save states are verified successful states -> outcome_label = 1.0
        commit_res = self.commit_node_v2(
            payload=payload,
            spacetime_anchor=spacetime_anchor,
            ccid=ccid,
            embedding_64d=embedding_64d,
            embedding_768d=embedding_768d,
            outcome_label=1.0,
            metadata={"source_file": source_file, "is_checkpoint": True}
        )

        return {
            "status": "SAVE_STATE_SYNCED_TO_HOARD",
            "ccid": ccid,
            "shard_file": commit_res["file"],
            "source": source_file,
            "mrl_embeddings_created": True,
            "outcome_label": 1.0
        }

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

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns a snapshot of the Hoard's current state for Heimdall monitoring."""
        stale_count = sum(1 for n in self.local_sparse_cache if n.is_stale)
        labeled_count = sum(1 for n in self.local_sparse_cache if n.outcome_label != 0.5)
        embedded_count = sum(
            1 for n in self.local_sparse_cache
            if any(v != 0.0 for v in n.embedding_768d)
        )
        return {
            "total_nodes": len(self.local_sparse_cache),
            "stale_nodes": stale_count,
            "labeled_nodes": labeled_count,
            "embedded_nodes": embedded_count,
            "schema_version": "2.0",
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

        # Build spacetime anchor
        spacetime_anchor = {
            "x": 0.0, "y": 0.0, "z": 0.0,
            "t": celestial_time(),
            "session_id": session_id,
            "cycle": cycle_iteration,
        }

        # Commit crystallization node to Hoard
        ccid = f"CCID_CRYSTAL_{int(celestial_time())}_{cycle_iteration}"
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
        )

        return {
            "crystallization": "COMPLETE",
            "loop": loop_result,
            "hoard": hoard_result,
            "ccid": ccid,
        }


# NOTE: RodinProtocol has been consolidated into memory/rodin_protocol.py
# which implements the real Matryoshka Representation Learning (MRL) and
# Cosine Similarity retrieval. Import from there:
#   from memory.rodin_protocol import RodinProtocol
