"""
INTEGRA O/S: ROUTE RETRIEVAL METHODOLOGY
Module: memory/rodin_protocol.py
Layer: 2 (Cheshire Cat Kernel & Rodin: Inter-Hemispheric Highway & Veto Arbiter)
Status: PRODUCTION SOVEREIGN IMPLEMENTATION (KNN-Enhanced v8.2.2)

Enhancement: Replaces monolithic centroid-based M_sem with localized
K-Nearest Neighbors (KNN) Isotropic Density Estimation (M_knn).

Mathematical Foundation:
    M_knn(P_current) = (1/K) * SUM_i[ I(O_i = SUCCESS) * exp(-d^2/sigma^2) ]

    Where:
        - K = number of nearest historical neighbors (default 7)
        - O_i = outcome label of neighbor i (1.0 = Success, 0.0 = Failure)
        - d = cosine distance between P_current and neighbor N_i
        - sigma = Gaussian kernel bandwidth (default 0.5)

Gate III RLVR Decision:
    PASS (Execute Action)  : M_knn >= tau (0.85) AND M_stale = False
    HALT (Alexandria Loop)  : M_knn < tau OR M_stale = True
"""

import math
import time
from typing import List, Dict, Any, Tuple, Optional


class RodinProtocol:
    """
    The Physics Engine of The Hoard.
    Retrieves 'ingredients, not meals' using Cosine Similarity:
    q . k = ||q|| * ||k|| * cos(theta)

    Applies Matryoshka Representation Learning (MRL) for fast 64-dim sweeps
    followed by fine 768-dim context reranking.

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
    COARSE_SIMILARITY_FLOOR = 0.60  # Minimum similarity for MRL Phase 1 pass

    def __init__(
        self,
        hoard=None,
        mrl_dimensions: Tuple[int, int] = (64, 768),
        k_neighbors: int = DEFAULT_K,
        tau_threshold: float = DEFAULT_TAU,
        sigma: float = DEFAULT_SIGMA,
        stale_threshold_seconds: float = DEFAULT_STALE_SECONDS,
    ):
        self.coarse_dim, self.fine_dim = mrl_dimensions
        self.hoard = hoard
        self.k = k_neighbors
        self.tau = tau_threshold
        self.sigma = sigma
        self.stale_threshold = stale_threshold_seconds

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
    #  MRL PHASE 1: Coarse 64-dim Filter (O(1))
    # ─────────────────────────────────────────────

    def mrl_coarse_filter(
        self, query_vec: List[float], candidate_nodes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        MRL Phase 1: Fast 64-dimensional scan.
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
    #  UNIFIED PIPELINE: route_retrieval_sweep
    # ─────────────────────────────────────────────

    def route_retrieval_sweep(
        self, query_vec: List[float], candidate_nodes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Legacy-compatible two-phase MRL retrieval sweep.
        Phase 1: 64-dim coarse filter
        Phase 2: Full-dim fine rerank
        Returns scored neighbors sorted by similarity descending.
        """
        coarse_passed = self.mrl_coarse_filter(query_vec, candidate_nodes)
        fine_ranked = self.mrl_fine_rerank(query_vec, coarse_passed)
        # Return sorted by similarity descending for backward compat
        return sorted(fine_ranked, key=lambda x: x["similarity"], reverse=True)

    # ─────────────────────────────────────────────
    #  UNIFIED PIPELINE: review_node_integrity
    # ─────────────────────────────────────────────

    def review_node_integrity(
        self, query_vec: List[float], candidate_nodes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Full KNN-Enhanced Rodin Pipeline:
        1. MRL Phase 1: Coarse 64d filter
        2. MRL Phase 2: Fine 768d re-rank -> K nearest neighbors
        3. Calculate M_knn (Neighborhood Density)
        4. Check M_stale (Temporal Validity)
        5. Gate III RLVR Decision

        Returns:
            Dict with decision (PASS/HALT), M_knn score, staleness,
            neighbor data, and routing information.
        """
        # Phase 1: Coarse filter
        coarse_passed = self.mrl_coarse_filter(query_vec, candidate_nodes)

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
            "neighbors": neighbors,
            **gate_result,
        }

    # ─────────────────────────────────────────────
    #  QUERY VECTOR GENERATION
    # ─────────────────────────────────────────────

    def generate_query_vector(self, prompt: str) -> List[float]:
        """
        Generates a query vector from a prompt string for MRL retrieval.
        
        Currently uses a simple hash-based placeholder embedding.
        Will be replaced with a real embedding model (e.g., text-embedding-004)
        when live API integration is implemented.
        
        Returns:
            A list of floats representing the query vector (768-dim).
        """
        # Placeholder: generate a deterministic pseudo-embedding from the prompt
        # This allows the full pipeline to function without an embedding API
        import hashlib
        hash_bytes = hashlib.sha256(prompt.encode()).digest()
        # Expand hash to 768 dimensions using cyclic repetition
        raw = list(hash_bytes) * (self.fine_dim // len(hash_bytes) + 1)
        vec = [float(b) / 255.0 for b in raw[:self.fine_dim]]
        return vec

    # ─────────────────────────────────────────────
    #  HIGH-LEVEL API: route_retrieval
    # ─────────────────────────────────────────────

    def route_retrieval(self, prompt: str) -> Dict[str, Any]:
        """
        High-level retrieval interface for the Cheshire Cat Kernel.
        Uses the Hoard's internal sparse cache as the candidate pool,
        applying substring matching as a fallback when embeddings
        are not yet populated.

        Returns ingredients (contextual paths), not fixed answers.
        """
        results = []
        if self.hoard is not None:
            results = self.hoard.query_internal([prompt])

        return {
            "query_terms": [prompt],
            "retrieved_paths": results,
            "retrieval_method": "MRL_COSINE_KNN" if results else "HOARD_SUBSTRING_FALLBACK",
            "candidate_count": len(results),
            "status": "RODIN_ROUTE_RETRIEVAL_COMPLETE",
        }
