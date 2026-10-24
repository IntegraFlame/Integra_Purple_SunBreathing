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
        self._neural_grid_router: Optional["CompleteNeuralGridRouterV2"] = None

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

    def get_neural_grid_router(self) -> "CompleteNeuralGridRouterV2":
        if self._neural_grid_router is None:
            self._neural_grid_router = CompleteNeuralGridRouterV2()
        return self._neural_grid_router

    def apply_mistake_loop_correction(self, correction_packet: Dict[str, str]) -> Dict[str, Any]:
        """Eq. 7.9: Applies a Mistake-Loop correction packet and updates the Shadow State Warm Cache."""
        return self.get_neural_grid_router().apply_mistake_loop_correction_packet(correction_packet)

    def route_neural_grid_query(
        self,
        prompt: str,
        thread_id: str = "THREAD_MTCW_07",
        intent_confidence: float = 0.92,
        stale_threshold_days: float = 7.0,
        active_context_tokens: int = 48000,
        indirect_bridge_score: float = 0.0,
    ) -> "RodinNexusRoutingResult":
        """Eq. 7.6-7.10: Executes Two-Stage MRL (64D->768D), M_knn, EIG, SSR >= 0.95 & Nexus Decision Tree."""
        return self.get_neural_grid_router().route_query_through_neural_grid(
            prompt=prompt,
            thread_id=thread_id,
            intent_confidence=intent_confidence,
            stale_threshold_days=stale_threshold_days,
            active_context_tokens=active_context_tokens,
            indirect_bridge_score=indirect_bridge_score,
        )

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


# ═════════════════════════════════════════════════════════════════════════════
# TASK L-4 (TASK 7 PACKET 2, EQ. 7.6 - 7.10):
# TWO-STAGE MRL (64D -> 768D), K-NN M_knn, EIG, SSR >= 0.95 CONFIDENCE GATE,
# 4-METRIC NEXUS DECISION TREE, MISTAKE LOOP & 4-STEP NEURON CHECKPOINTER
# ═════════════════════════════════════════════════════════════════════════════

import hashlib
import json
import struct
from dataclasses import asdict, dataclass, field


@dataclass
class PlotPoint768D:
    plot_point_id: str
    title: str
    ccid: str
    latitude_deg: float
    longitude_deg: float
    matrix_xy_16: Tuple[int, int]
    braille_packet_16: str
    braille_spatial_4: str
    taxonomy_uri: str
    vec_64d: List[float]
    vec_768d: List[float]
    stale_days: float = 0.0
    outcome_label: float = 1.0
    confidence_weight: float = 0.50
    warm_in_shadow_state: bool = True


@dataclass
class CheckpointerSnapshot:
    """Equation 7.10: 4-Step Neuron Checkpointer Snapshot (Freeze -> Serialize -> Commit -> Resume)."""

    thread_id: str
    step_index: int
    plot_point_id: str
    sequence_stages_completed: List[str]
    serialized_state_sha256: str
    pending_writes: List[str]
    axial_stress_mpa: float
    seventh_form_cavitation_active: bool
    heaviside_halt_triggered: bool = False
    angular_momentum_kg_m_s: float = 500.0
    delta_e_cycle: float = 0.0


@dataclass
class RodinNexusRoutingResult:
    """Equations 7.6 - 7.10: Complete MRL 64D->768D, M_knn, EIG, SSR, and Nexus Decision Output."""

    prompt: str
    prompt_type_m_type: str
    candidates_screened_64d: int
    candidates_reranked_768d: int
    winning_plot_point_id: str
    winning_braille_packet_16: str
    m_sem_768d: float
    m_knn: float
    m_route_count: int
    m_stale: bool
    expected_information_gain_eig_bits: float
    ssr_confidence_score: float
    ssr_gate_action: str
    upsilon_throughput: float
    loop_selected: str
    nexus_decision_outcome: str
    rodin_constitutional_outcome: str
    output_message: str
    checkpointer_receipt: CheckpointerSnapshot

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CompleteNeuralGridRouterV2:
    """
    Completes Task 7 (Equations 7.6 - 7.10):
      - Eq. 7.6 : Two-Stage Matryoshka (64D Fast Search -> 768D Precise Reranking) + Gaussian M_knn
      - Eq. 7.7 : Expected Information Gain (EIG) & SSR Confidence (0.95 Gate)
      - Eq. 7.8 : 4-Metric Nexus Decision Tree (Scenarios 2a, 2e, 2f, Indirect Connection, Clarify, Direct)
      - Eq. 7.9 : The 'Mistake Loop' Correction Packet & Shadow State Warm Cache
      - Eq. 7.10: 4-Step Neuron Checkpointer (1_FREEZE -> 2_SERIALIZE -> 3_COMMIT -> 4_RESUME)
                  & Context Axial Stress Monitor (170 MPa Cavitation / 200 MPa Heaviside Ceiling)
    """

    BRAILLE_BASE = 0x2800
    DIM_COARSE = 64
    DIM_FULL = 768

    def __init__(self, max_context_tokens: int = 200000, k_neighbors: int = 7, sigma: float = 0.50):
        self.max_context_tokens = max_context_tokens
        self.k_neighbors = k_neighbors
        self.sigma = sigma
        self.plot_points: Dict[str, PlotPoint768D] = {}
        self.shadow_state_warm_cache: Dict[str, PlotPoint768D] = {}
        self.trigger_confidence_map: Dict[str, Dict[str, float]] = {}
        self.checkpoint_chain: List[CheckpointerSnapshot] = []

    @classmethod
    def encode_mrl_768d_and_64d(cls, text: str) -> Tuple[List[float], List[float]]:
        raw_768 = [0.0] * cls.DIM_FULL
        tokens = text.lower().replace("?", "").replace(".", "").replace(",", "").split() or [text]
        shingles = tokens + [f"{tokens[i]}_{tokens[i + 1]}" for i in range(len(tokens) - 1)]

        for tok in shingles:
            digest = hashlib.sha512(tok.encode("utf-8")).digest()
            for i in range(cls.DIM_FULL):
                w = 2.0 if i < cls.DIM_COARSE else 1.0
                byte_val = digest[i % len(digest)]
                bit = (byte_val >> (i % 8)) & 1
                raw_768[i] += w if bit else -w

        norm_768 = math.sqrt(sum(x * x for x in raw_768)) or 1.0
        vec_768 = [x / norm_768 for x in raw_768]

        slice_64 = vec_768[: cls.DIM_COARSE]
        norm_64 = math.sqrt(sum(x * x for x in slice_64)) or 1.0
        vec_64 = [x / norm_64 for x in slice_64]
        return vec_64, vec_768

    @classmethod
    def _encode_morton_braille_4(cls, y16: int, x16: int) -> str:
        from memory.braille_atlas_engine import CITBrailleCodec

        morton = CITBrailleCodec.interleave_morton_xy16(x16=x16, y16=y16)
        return CITBrailleCodec.bytes_to_braille(struct.pack(">I", morton))

    def register_plot_point(
        self,
        plot_point_id: str,
        title: str,
        raw_content: str,
        ccid: str,
        lat_deg: float,
        lon_deg: float,
        stale_days: float = 0.0,
        epoch_sec: int = 1792180000,
        codex_byte: int = 0x03,
        trigger_keyword: Optional[str] = None,
        initial_conf: float = 0.50,
        outcome_label: float = 1.0,
    ) -> PlotPoint768D:
        vec_64, vec_768 = self.encode_mrl_768d_and_64d(f"{title} {raw_content}")
        nx = min(0.9999999, max(0.0, (lon_deg + 180.0) / 360.0))
        ny = min(0.9999999, max(0.0, (lat_deg + 90.0) / 180.0))
        x16, y16 = int(nx * 65536), int(ny * 65536)
        x12, y12 = x16 >> 4, y16 >> 4

        braille_spatial_4 = self._encode_morton_braille_4(y16, x16)
        time_b4 = "".join(chr(self.BRAILLE_BASE + b) for b in struct.pack(">I", int(epoch_sec) & 0xFFFFFFFF))
        codex_b1 = chr(self.BRAILLE_BASE + (int(codex_byte) & 0xFF))
        bq_56 = 0
        for i in range(56):
            bq_56 = (bq_56 << 1) | (1 if vec_64[i] > 0.0 else 0)
        sem_b7 = "".join(chr(self.BRAILLE_BASE + b) for b in bq_56.to_bytes(7, "big"))
        packet_16 = f"{time_b4}{codex_b1}{braille_spatial_4}{sem_b7}"

        hem = f"{'N' if y16 >= 32768 else 'S'}{'E' if x16 >= 32768 else 'W'}"
        uri = f"CIT://{hem}/{plot_point_id}/QUAD_{braille_spatial_4}/XY_{x12:04d}_{y12:04d}"

        warm = initial_conf >= 0.40
        pp = PlotPoint768D(
            plot_point_id=plot_point_id,
            title=title,
            ccid=ccid,
            latitude_deg=lat_deg,
            longitude_deg=lon_deg,
            matrix_xy_16=(x16, y16),
            braille_packet_16=packet_16,
            braille_spatial_4=braille_spatial_4,
            taxonomy_uri=uri,
            vec_64d=vec_64,
            vec_768d=vec_768,
            stale_days=stale_days,
            outcome_label=outcome_label,
            confidence_weight=initial_conf,
            warm_in_shadow_state=warm,
        )
        self.plot_points[plot_point_id] = pp
        if warm:
            self.shadow_state_warm_cache[plot_point_id] = pp
        if trigger_keyword:
            t_key = trigger_keyword.lower()
            self.trigger_confidence_map.setdefault(t_key, {})[plot_point_id] = initial_conf
        return pp

    def apply_mistake_loop_correction_packet(self, correction_packet: Dict[str, str]) -> Dict[str, Any]:
        """
        Equation 7.9: Processes a Frontend/User Correction Packet:
          {"trigger": "hoard", "previous_id": "HOARD_CONV_HIST",
           "new_id": "HOARD_FILE_VIEW", "user_feedback": "direct_correction"}
        """
        trig = correction_packet["trigger"].lower()
        prev_id = correction_packet["previous_id"]
        new_id = correction_packet["new_id"]

        conf_dict = self.trigger_confidence_map.setdefault(trig, {})
        old_prev = conf_dict.get(
            prev_id,
            self.plot_points[prev_id].confidence_weight if prev_id in self.plot_points else 0.50,
        )
        old_new = conf_dict.get(
            new_id,
            self.plot_points[new_id].confidence_weight if new_id in self.plot_points else 0.50,
        )

        updated_prev = max(0.05, old_prev * 0.35)
        updated_new = min(0.98, old_new * 1.75)
        total = updated_prev + updated_new
        norm_prev = round(updated_prev / total, 4)
        norm_new = round(updated_new / total, 4)

        conf_dict[prev_id] = norm_prev
        conf_dict[new_id] = norm_new

        if prev_id in self.plot_points:
            self.plot_points[prev_id].confidence_weight = norm_prev
            self.plot_points[prev_id].warm_in_shadow_state = norm_prev >= 0.40
            if not self.plot_points[prev_id].warm_in_shadow_state:
                self.shadow_state_warm_cache.pop(prev_id, None)

        if new_id in self.plot_points:
            self.plot_points[new_id].confidence_weight = norm_new
            self.plot_points[new_id].warm_in_shadow_state = True
            self.shadow_state_warm_cache[new_id] = self.plot_points[new_id]

        return {
            "trigger": trig,
            "previous_id": prev_id,
            "new_id": new_id,
            "previous_confidence_before": round(old_prev, 4),
            "previous_confidence_after": norm_prev,
            "new_confidence_before": round(old_new, 4),
            "new_confidence_after": norm_new,
            "previous_id_confidence": f"{old_prev:.2f} -> {norm_prev:.4f}",
            "new_id_confidence": f"{old_new:.2f} -> {norm_new:.4f}",
            "active_shadow_state_ids": sorted(self.shadow_state_warm_cache.keys()),
        }

    def execute_neuron_checkpoint(
        self,
        thread_id: str,
        plot_point_id: str,
        pending_writes: List[str],
        active_context_tokens: int = 48000,
    ) -> CheckpointerSnapshot:
        axial_mpa = round(200.0 * (active_context_tokens / max(1, self.max_context_tokens)), 3)
        cavitation_7th_form = axial_mpa >= 170.0
        heaviside_halt = axial_mpa >= 200.0

        state_payload = json.dumps(
            {
                "thread_id": thread_id,
                "plot_point_id": plot_point_id,
                "pending_writes": pending_writes,
                "axial_mpa": axial_mpa,
            },
            sort_keys=True,
        ).encode("utf-8")
        digest = hashlib.sha256(state_payload).hexdigest()[:20]

        snap = CheckpointerSnapshot(
            thread_id=thread_id,
            step_index=len(self.checkpoint_chain) + 1,
            plot_point_id=plot_point_id,
            sequence_stages_completed=["1_FREEZE", "2_SERIALIZE", "3_COMMIT", "4_RESUME"],
            serialized_state_sha256=digest,
            pending_writes=pending_writes,
            axial_stress_mpa=axial_mpa,
            seventh_form_cavitation_active=cavitation_7th_form,
            heaviside_halt_triggered=heaviside_halt,
        )
        self.checkpoint_chain.append(snap)
        return snap

    def compute_knn_density(self, scored_768: List[Tuple[float, float, PlotPoint768D]]) -> float:
        """Gaussian-weighted K-NN success density M_knn across top-K 768D neighbors."""
        top_k = scored_768[: self.k_neighbors]
        if not top_k:
            return 0.0
        w_sum = 0.0
        w_tot = 0.0
        for _, sim_768, pp in top_k:
            cos_dist = max(0.0, 2.0 * (1.0 - sim_768))
            w = math.exp(-(cos_dist ** 2) / (self.sigma ** 2))
            w_sum += pp.outcome_label * w
            w_tot += w
        return round(w_sum / w_tot, 4) if w_tot > 0.0 else 0.0

    def route_query_through_neural_grid(
        self,
        prompt: str,
        thread_id: str = "THREAD_MTCW_07",
        intent_confidence: float = 0.92,
        stale_threshold_days: float = 7.0,
        active_context_tokens: int = 48000,
        indirect_bridge_score: float = 0.0,
    ) -> RodinNexusRoutingResult:
        if not self.plot_points:
            raise RuntimeError("No plot points registered in CompleteNeuralGridRouterV2.")

        p_clean = prompt.strip()
        if p_clean.endswith("?"):
            m_type = "QUESTION"
        elif (
            any(p_clean.lower().startswith(cmd) for cmd in ("show", "open", "run", "execute"))
            and not p_clean.endswith(".")
        ):
            m_type = "COMMAND"
        else:
            m_type = "STATEMENT"

        q_64, q_768 = self.encode_mrl_768d_and_64d(p_clean)

        # Stage 1: 64D Fast Search Screening
        stage1_candidates: List[Tuple[float, PlotPoint768D]] = []
        for pp in self.plot_points.values():
            sim_64 = (1.0 + sum(a * b for a, b in zip(q_64, pp.vec_64d))) / 2.0
            if sim_64 >= 0.45:
                stage1_candidates.append((sim_64, pp))

        if not stage1_candidates:
            stage1_candidates = [
                ((1.0 + sum(a * b for a, b in zip(q_64, pp.vec_64d))) / 2.0, pp)
                for pp in self.plot_points.values()
            ]

        # Stage 2: 768D Precise Reranking + Mistake-Loop Confidence Weighting
        scored_768: List[Tuple[float, float, PlotPoint768D]] = []
        for sim_64, pp in stage1_candidates:
            sim_768 = (1.0 + sum(a * b for a, b in zip(q_768, pp.vec_768d))) / 2.0
            blended_mrl = (0.30 * sim_64 + 0.70 * sim_768) * (0.50 + 0.50 * pp.confidence_weight)
            scored_768.append((blended_mrl, sim_768, pp))

        scored_768.sort(key=lambda x: x[0], reverse=True)
        best_blended, best_sim_768, winner = scored_768[0]

        m_knn = self.compute_knn_density(scored_768)
        m_route_count = sum(1 for _, s768, _ in scored_768 if s768 >= 0.62)
        m_stale = winner.stale_days > stale_threshold_days

        # Equation 7.7: Expected Information Gain (EIG in bits) & SSR Confidence (0.95 Gate)
        prior_entropy_h = 2.50
        post_prob = max(0.05, min(0.999, best_sim_768 * winner.confidence_weight))
        post_entropy_h = -(
            post_prob * math.log2(post_prob)
            + (1.0 - post_prob) * math.log2(max(1e-9, 1.0 - post_prob))
        )
        eig_bits = max(0.0, prior_entropy_h - post_entropy_h)

        raw_ssr = 0.55 * best_sim_768 + 0.25 * winner.confidence_weight + 0.20 * (0.0 if m_stale else 1.0)
        ssr_conf = min(0.995, round(raw_ssr + 0.12 * (1.0 if m_route_count >= 1 else 0.0), 4))
        ssr_action = "PROCEED_TO_OUTPUT" if ssr_conf >= 0.95 else "RE_TRIGGER_PASS_2"

        rss_denom = max(0.04, (1.0 - best_sim_768) + 0.05)
        upsilon = round((best_blended * (1.0 + eig_bits)) / rss_denom, 4)

        # Equation 7.8 + GEMINI.md §9: 4-Metric Nexus Decision Tree & 5 Constitutional Rodin Outcomes
        if m_type == "STATEMENT" and best_sim_768 >= 0.65 and not m_stale:
            loop_sel = "LOOP_1_INTERNAL_SYNTHESIS"
            outcome = "SCENARIO_2A_CONVERSATIONAL_CONTINUATION"
            const_outcome = "CONVERSATIONAL_CONTINUATION"
            msg = (
                f"Validated statement against Plot Point {winner.plot_point_id} "
                f"({winner.title}). Synthesizing continuation without external search."
            )
        elif m_stale and best_sim_768 >= 0.55:
            loop_sel = "LOOP_2_AUTONOMOUS_LEARNING"
            outcome = "SCENARIO_2E_ALEXANDRIA_VERIFY_STALE"
            const_outcome = "ALEXANDRIA_VERIFICATION"
            msg = (
                f"Recalling discussion on {winner.title}; data is {winner.stale_days:.0f} days old. "
                "Initiating Alexandria Protocol to verify volatile data."
            )
        elif not m_stale and 0.45 <= best_sim_768 < 0.65 and indirect_bridge_score >= 0.60:
            loop_sel = "LOOP_1_INTERNAL_SYNTHESIS"
            outcome = "TRANSDISCIPLINARY_INDIRECT_CONNECTION"
            const_outcome = "INDIRECT_CONNECTION"
            msg = (
                f"Wove transdisciplinary indirect connection via Plot Point {winner.plot_point_id} "
                f"(bridge_score={indirect_bridge_score:.2f})."
            )
        elif m_route_count < 1 and intent_confidence > 0.80:
            loop_sel = "LOOP_2_AUTONOMOUS_LEARNING"
            outcome = "SCENARIO_2F_ALEXANDRIA_GUIDED_SEARCH"
            const_outcome = "ALEXANDRIA_GUIDED_SEARCH"
            msg = (
                f"Internal routes sparse for [{p_clean}], intent confidence={intent_confidence:.2f}. "
                "Initiating Alexandria Guided Search."
            )
        elif m_route_count < 1:
            loop_sel = "LOOP_2_AUTONOMOUS_LEARNING"
            outcome = "NEXUS_REQUEST_CLARIFICATION"
            const_outcome = "REQUEST_CLARIFICATION"
            msg = "Insufficient internal context to form a confident inference; requesting clarification."
        else:
            loop_sel = "LOOP_1_INTERNAL_SYNTHESIS"
            outcome = "DIRECT_MULTIDIMENSIONAL_ANSWER"
            const_outcome = "CONVERSATIONAL_CONTINUATION"
            msg = f"Synthesized direct multidimensional answer from {winner.plot_point_id} ({winner.taxonomy_uri})."

        ckpt = self.execute_neuron_checkpoint(
            thread_id=thread_id,
            plot_point_id=winner.plot_point_id,
            pending_writes=[f"ROUTE_{outcome}", f"SSR_{ssr_action}"],
            active_context_tokens=active_context_tokens,
        )

        return RodinNexusRoutingResult(
            prompt=prompt,
            prompt_type_m_type=m_type,
            candidates_screened_64d=len(stage1_candidates),
            candidates_reranked_768d=len(scored_768),
            winning_plot_point_id=winner.plot_point_id,
            winning_braille_packet_16=winner.braille_packet_16,
            m_sem_768d=round(best_sim_768, 4),
            m_knn=m_knn,
            m_route_count=m_route_count,
            m_stale=m_stale,
            expected_information_gain_eig_bits=round(eig_bits, 4),
            ssr_confidence_score=ssr_conf,
            ssr_gate_action=ssr_action,
            upsilon_throughput=upsilon,
            loop_selected=loop_sel,
            nexus_decision_outcome=outcome,
            rodin_constitutional_outcome=const_outcome,
            output_message=msg,
            checkpointer_receipt=ckpt,
        )
