"""
INTEGRA O/S: ROUTE RETRIEVAL METHODOLOGY
Module: memory/rodin_protocol.py
Layer: 2 (Cheshire Cat Kernel & Rodin: Inter-Hemispheric Highway & Veto Arbiter)
Status: PRODUCTION SOVEREIGN IMPLEMENTATION (KNN-Enhanced v8.2.2, loud failures v8.2.3)

Enhancement: Replaces monolithic centroid-based M_sem with localized
K-Nearest Neighbors (KNN) Isotropic Density Estimation (M_knn).

Mathematical Foundation:
    M_knn(P_current) = (1/K) * SUM_i[ I(O_i = SUCCESS) * exp(-d^2/sigma^2) ]

    Where:
        - K = number of nearest historical neighbors (default 7)
        - O_i = outcome label of neighbor i (1.0 = Success, 0.0 = Failure)
        - d = cosine distance between P_current and neighbor N_i
        - sigma = Gaussian kernel bandwidth (default 0.5)

    (The code in calculate_neighborhood_density divides by the summed weights, not by K.
    That difference is recorded as an open question and is not changed here.)

Gate III RLVR Decision:
    PASS (Execute Action)  : M_knn >= tau (0.85) AND M_stale = False
    HALT (Alexandria Loop)  : M_knn < tau OR M_stale = True

v8.2.3, loud failures (ADR-005 action 2): the query vector comes from the embedding model
(memory/embedding_service.py) or the call raises EmbeddingUnavailable. There is no hash fallback.
A retrieval that could not use the model or the vector index says so (`degraded`, `fallback_reason`).
"""

import math
import time
from typing import List, Dict, Any, Tuple, Optional, Union

from memory.embedding_service import (
    EmbeddingResult,
    EmbeddingService,
    EmbeddingSpace,
    EmbeddingUnavailable,
    get_default_embedding_service,
)


class RodinProtocol:
    """
    The Physics Engine of The Hoard.
    Retrieves 'ingredients, not meals' using Cosine Similarity:
    q . k = ||q|| * ||k|| * cos(theta)

    Applies Matryoshka Representation Learning (MRL): a fast coarse sweep on the
    first `coarse_dim` coordinates, then a fine 768-dim rerank. gemini-embedding-2 is
    trained with MRL and documents 128-3072 as its supported sizes, so the coarse
    tier defaults to 128 (the earlier 64 is below the documented minimum).

    KNN Enhancement (v8.2.2):
        Instead of comparing against a single centroid, the protocol now
        evaluates the local topology of the K nearest historical nodes
        and their outcome labels (Success/Failure) to produce M_knn,
        a Gaussian-weighted success density metric.

    Accepts an optional TheHoard instance for backward compatibility
    with direct retrieval from the Hoard's local sparse cache.
    """

    # --- Configuration Constants ---
    DEFAULT_K = 7                   # Number of nearest neighbors
    DEFAULT_TAU = 0.85              # Gate III RLVR threshold
    DEFAULT_SIGMA = 0.5             # Gaussian kernel bandwidth
    DEFAULT_STALE_SECONDS = 604800  # 7 days in seconds
    COARSE_SIMILARITY_FLOOR = 0.60  # Minimum similarity for MRL Phase 1 pass (not yet calibrated on real embeddings)
    DEFAULT_COARSE_DIM = 128        # documented minimum of gemini-embedding-2

    def __init__(
        self,
        hoard=None,
        mrl_dimensions: Tuple[int, int] = (DEFAULT_COARSE_DIM, 768),
        k_neighbors: int = DEFAULT_K,
        tau_threshold: float = DEFAULT_TAU,
        sigma: float = DEFAULT_SIGMA,
        stale_threshold_seconds: float = DEFAULT_STALE_SECONDS,
        embedder: Optional[EmbeddingService] = None,
    ):
        self.coarse_dim, self.fine_dim = mrl_dimensions
        self.hoard = hoard
        self.k = k_neighbors
        self.tau = tau_threshold
        self.sigma = sigma
        self.stale_threshold = stale_threshold_seconds
        self.embedder = embedder

    def _service(self) -> EmbeddingService:
        return self.embedder or get_default_embedding_service()

    # ─────────────────────────────────────────────
    #  CORE MATH: Cosine Similarity / Distance
    # ─────────────────────────────────────────────

    def calculate_cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Computes cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def calculate_cosine_distance(self, vec_a: List[float], vec_b: List[float]) -> float:
        """
        Cosine Distance: d(u, v) = 1 - cos_sim(u, v)
        Range: [0.0, 2.0] where 0.0 = identical, 1.0 = orthogonal.
        """
        return 1.0 - self.calculate_cosine_similarity(vec_a, vec_b)

    # ─────────────────────────────────────────────
    #  MRL PHASE 1: Coarse prefix filter (O(1))
    # ─────────────────────────────────────────────

    def mrl_coarse_filter(
        self, query_vec: List[float], candidate_nodes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        MRL Phase 1: Fast scan on the first `coarse_dim` coordinates.
        Eliminates candidates below the coarse similarity floor.
        Returns a reduced candidate set for Phase 2 fine re-ranking.
        """
        passed = []
        for node in candidate_nodes:
            key_vec = node.get("embedding", [0.0] * len(query_vec))
            sim = self.calculate_cosine_similarity(
                query_vec[: self.coarse_dim], key_vec[: self.coarse_dim]
            )
            if sim > self.COARSE_SIMILARITY_FLOOR:
                passed.append({**node, "_coarse_sim": round(sim, 4)})
        return passed

    # ─────────────────────────────────────────────
    #  MRL PHASE 2: Fine 768-dim Re-Rank
    # ─────────────────────────────────────────────

    def mrl_fine_rerank(
        self, query_vec: List[float], coarse_candidates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        MRL Phase 2: Full 768-dimensional fidelity re-ranking.
        Computes exact cosine distance and selects the true K nearest neighbors.
        """
        scored = []
        for node in coarse_candidates:
            key_vec = node.get("embedding", [0.0] * len(query_vec))
            fine_distance = self.calculate_cosine_distance(
                query_vec[: self.fine_dim], key_vec[: self.fine_dim]
            )
            fine_similarity = 1.0 - fine_distance
            scored.append({
                **node,
                "distance": round(fine_distance, 6),
                "similarity": round(fine_similarity, 4),
            })

        # Sort by distance ascending (closest first), take top K
        scored.sort(key=lambda x: x["distance"])
        return scored[: self.k]

    # ─────────────────────────────────────────────
    #  KNN CORE: Neighborhood Density (M_knn)
    # ─────────────────────────────────────────────

    def calculate_neighborhood_density(self, neighbors: List[Dict[str, Any]]) -> float:
        """
        Computes M_knn: the Gaussian-weighted success density of K nearest neighbors.

        M_knn(P) = (1/K) * SUM_i[ I(O_i = SUCCESS) * exp(-d_i^2 / sigma^2) ]

        Where:
            O_i = outcome_label of neighbor i (1.0 = success, 0.0 = failure)
            d_i = cosine distance between P_current and neighbor i
            sigma = Gaussian kernel bandwidth

        Returns:
            float in [0.0, 1.0] representing local reliability density.
        """
        if not neighbors:
            return 0.0

        weighted_sum = 0.0
        total_weight = 0.0

        for n in neighbors:
            distance = n.get("distance", 1.0)
            outcome = n.get("outcome_label", 0.5)  # Default 0.5 = unknown

            # Gaussian weight: closer neighbors contribute more
            weight = math.exp(-(distance ** 2) / (self.sigma ** 2))

            weighted_sum += outcome * weight
            total_weight += weight

        if total_weight == 0.0:
            return 0.0

        return weighted_sum / total_weight

    # ─────────────────────────────────────────────
    #  STALENESS CHECK (M_stale)
    # ─────────────────────────────────────────────

    def check_staleness(self, neighbors: List[Dict[str, Any]]) -> bool:
        """
        Checks if any neighbor in the set has exceeded the temporal
        staleness threshold (T_stale, default 7 days).

        M_stale = (Now - node.Timestamp > T_stale)

        Returns True if ANY neighbor is stale (conservative approach).
        """
        current_time = time.time()
        for n in neighbors:
            timestamp = n.get("created_at", n.get("stale_timestamp", current_time))
            if isinstance(timestamp, (int, float)):
                age = current_time - timestamp
                if age > self.stale_threshold:
                    return True
        return False

    # ─────────────────────────────────────────────
    #  GATE III RLVR: Pre-Action Decision Gate
    # ─────────────────────────────────────────────

    def gate_iii_decision(
        self, m_knn: float, is_stale: bool, m_route: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Gate III RLVR Decision Function:

        Decision(A) = {
            EXECUTE  if M_knn >= tau AND M_stale = False AND M_route >= tau
            HALT     otherwise
        }

        Returns a decision dict with routing information.
        """
        passes_density = m_knn >= self.tau
        passes_staleness = not is_stale
        passes_route = (m_route is None) or (m_route >= self.tau)

        if passes_density and passes_staleness and passes_route:
            return {
                "decision": "PASS",
                "action_route": "LOOP_1_PERFORMANCE",
                "confidence": round(m_knn, 4),
                "log": "Gate III Locked. Commit to Hoard.",
            }
        else:
            # Determine the specific failure reason for logging
            failure_reasons = []
            if not passes_density:
                failure_reasons.append(f"M_knn={m_knn:.4f} < tau={self.tau}")
            if not passes_staleness:
                failure_reasons.append("M_stale=True (temporal expiry)")
            if not passes_route:
                failure_reasons.append(f"M_route={m_route:.4f} < tau={self.tau}")

            return {
                "decision": "HALT",
                "action_route": "LOOP_2_LEARNING",
                "confidence": round(m_knn, 4),
                "failure_reasons": failure_reasons,
                "log": f"Density Failure ({m_knn:.4f}). Triggering Alexandria Protocol.",
            }

    # ─────────────────────────────────────────────
    #  CANDIDATE HYGIENE: same space, same size
    # ─────────────────────────────────────────────

    @staticmethod
    def _space_id(space: Union[EmbeddingSpace, str, None]) -> Optional[str]:
        return space.id if isinstance(space, EmbeddingSpace) else space

    def _usable_candidates(
        self,
        query_vec: List[float],
        candidate_nodes: List[Dict[str, Any]],
        space: Union[EmbeddingSpace, str, None] = None,
    ) -> Tuple[List[Dict[str, Any]], int, int]:
        """
        Keeps candidates whose vector is in the query's space (when a space is given) and has the query's length.
        Vectors from another model, or from no named space, are not comparable, so they never take part.
        Returns (usable, excluded_other_space, excluded_dim_mismatch).
        """
        space_id = self._space_id(space)
        usable: List[Dict[str, Any]] = []
        other_space = dim_mismatch = 0
        for node in candidate_nodes:
            if space_id is not None and node.get("embed_space") != space_id:
                other_space += 1
                continue
            emb = node.get("embedding")
            if not emb or len(emb) != len(query_vec):
                dim_mismatch += 1
                continue
            usable.append(node)
        return usable, other_space, dim_mismatch

    # ─────────────────────────────────────────────
    #  UNIFIED PIPELINE: route_retrieval_sweep
    # ─────────────────────────────────────────────

    def route_retrieval_sweep(
        self,
        query_vec: List[float],
        candidate_nodes: List[Dict[str, Any]],
        space: Union[EmbeddingSpace, str, None] = None,
    ) -> List[Dict[str, Any]]:
        """
        Legacy-compatible two-phase MRL retrieval sweep.
        Phase 1: coarse prefix filter
        Phase 2: Full-dim fine rerank
        Returns scored neighbors sorted by similarity descending.
        """
        usable, _, _ = self._usable_candidates(query_vec, candidate_nodes, space)
        coarse_passed = self.mrl_coarse_filter(query_vec, usable)
        fine_ranked = self.mrl_fine_rerank(query_vec, coarse_passed)
        # Return sorted by similarity descending for backward compat
        return sorted(fine_ranked, key=lambda x: x["similarity"], reverse=True)

    # ─────────────────────────────────────────────
    #  UNIFIED PIPELINE: review_node_integrity
    # ─────────────────────────────────────────────

    def review_node_integrity(
        self,
        query_vec: List[float],
        candidate_nodes: List[Dict[str, Any]],
        space: Union[EmbeddingSpace, str, None] = None,
    ) -> Dict[str, Any]:
        """
        Full KNN-Enhanced Rodin Pipeline:
        1. Candidate hygiene: same space, same dimension (counted, never silent)
        2. MRL Phase 1: Coarse prefix filter
        3. MRL Phase 2: Fine 768d re-rank -> K nearest neighbors
        4. Calculate M_knn (Neighborhood Density)
        5. Check M_stale (Temporal Validity)
        6. Gate III RLVR Decision

        Returns:
            Dict with decision (PASS/HALT), M_knn score, staleness,
            neighbor data, routing information and the candidate counts.
        """
        usable, other_space, dim_mismatch = self._usable_candidates(query_vec, candidate_nodes, space)

        # Phase 1: Coarse filter
        coarse_passed = self.mrl_coarse_filter(query_vec, usable)

        # Phase 2: Fine re-rank -> top K
        neighbors = self.mrl_fine_rerank(query_vec, coarse_passed)

        # Calculate metrics
        m_knn = self.calculate_neighborhood_density(neighbors)
        is_stale = self.check_staleness(neighbors)

        # Gate III Decision
        gate_result = self.gate_iii_decision(m_knn, is_stale)

        return {
            "m_knn": round(m_knn, 4),
            "is_stale": is_stale,
            "k_neighbors_found": len(neighbors),
            "coarse_candidates": len(coarse_passed),
            "candidates_total": len(candidate_nodes),
            "excluded_other_space": other_space,
            "excluded_dim_mismatch": dim_mismatch,
            "embedding_space": self._space_id(space),
            "neighbors": neighbors,
            **gate_result,
        }

    # ─────────────────────────────────────────────
    #  QUERY VECTOR GENERATION
    # ─────────────────────────────────────────────

    def generate_query_embedding(self, prompt: str, task: str = "search result") -> EmbeddingResult:
        """
        The query's embedding from the model, in the documented query format, with the space it belongs to.
        Raises EmbeddingUnavailable when the model cannot be used. There is no substitute vector.
        """
        result = self._service().embed_query(prompt, task=task)
        if result.space.dim != self.fine_dim:
            raise EmbeddingUnavailable(
                "BAD_DIMENSION",
                f"space {result.space.id} has {result.space.dim} dimensions but Rodin's fine tier uses {self.fine_dim}",
            )
        return result

    def generate_query_vector(self, prompt: str, task: str = "search result") -> List[float]:
        """The query vector (unit length, fine_dim values) or EmbeddingUnavailable."""
        return self.generate_query_embedding(prompt, task=task).vector

    # ─────────────────────────────────────────────
    #  HIGH-LEVEL API: route_retrieval
    # ─────────────────────────────────────────────

    def route_retrieval(self, prompt: str) -> Dict[str, Any]:
        """
        High-level retrieval interface for the Cheshire Cat Kernel.
        Embeds the prompt, searches the Hoard's vector index for that embedding space, and falls back to
        substring matching when it cannot. The fallback is never silent: `degraded` is True when the model or
        the vector index could not be used, `fallback_reason` says why, and `embed_error` carries the model's error.

        Returns ingredients (contextual paths), not fixed answers.
        """
        results: List[Dict[str, Any]] = []
        retrieval_method = "NO_HOARD"
        degraded = False
        fallback_reason: Optional[str] = None
        embed_error: Optional[Dict[str, str]] = None
        search_error: Optional[str] = None
        space_id: Optional[str] = None
        index_rows: Optional[int] = None

        if self.hoard is not None:
            vector: Optional[List[float]] = None
            try:
                emb = self.generate_query_embedding(prompt)
                vector, space_id = emb.vector, emb.space.id
            except EmbeddingUnavailable as exc:
                degraded = True
                fallback_reason = f"EMBEDDING_UNAVAILABLE:{exc.code}"
                embed_error = {"code": exc.code, "detail": exc.detail}

            if vector is not None:
                if not self.hoard.vector_search_available():
                    degraded = True
                    fallback_reason = "VECTOR_SEARCH_UNAVAILABLE"
                else:
                    try:
                        results = self.hoard.chroma_query(vector, n_results=self.k, space_id=space_id)
                        index_rows = self.hoard.count()
                        if results:
                            retrieval_method = "MRL_COSINE_KNN_CHROMA"
                        else:
                            fallback_reason = "NO_VECTOR_MATCH"
                    except Exception as exc:  # noqa: BLE001  (reported below, never hidden)
                        degraded = True
                        fallback_reason = f"VECTOR_SEARCH_ERROR:{type(exc).__name__}"
                        search_error = str(exc)[:300]

            # Fallback to internal substring query
            if not results:
                results = self.hoard.query_internal([prompt])
                retrieval_method = "HOARD_SUBSTRING_FALLBACK" if results else "NO_RESULTS"

        return {
            "query_terms": [prompt],
            "retrieved_paths": results,
            "retrieval_method": retrieval_method,
            "candidate_count": len(results),
            "degraded": degraded,
            "fallback_reason": fallback_reason,
            "embed_error": embed_error,
            "search_error": search_error,
            "embedding_space": space_id,
            "index_rows": index_rows,
            "status": "RODIN_ROUTE_RETRIEVAL_COMPLETE",
        }

    # ─────────────────────────────────────────────
    #  STATUS (what GET /rodin/telemetry reports)
    # ─────────────────────────────────────────────

    def status(self) -> Dict[str, Any]:
        """
        Evidence, not a constant: the embedder's state (UNPROVEN until a call has been made, READY after a call
        returned valid vectors, DEGRADED after a failure, MISCONFIGURED on a bad setting) and its counters.
        """
        stats = self._service().stats()
        return {
            "embedder_state": stats["state"],
            "embedding": stats,
            "coarse_dim": self.coarse_dim,
            "fine_dim": self.fine_dim,
        }
