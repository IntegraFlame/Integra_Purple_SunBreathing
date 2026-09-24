"""
INTEGRA O/S: RECIPROCAL RANK FUSION (RRF) — CORPUS CALLOSUM BRIDGE
Module: core/rrf_bridge.py
Layer: 2 (Corpus Callosum & Structural Unification)
Version: 8.2.2-PURPLE (Phase F Enhanced)

Mathematical Foundation:
    RRF_score(d) = SUM_r [ w_r / (k + rank_r(d)) ]

    Where:
        - r = each ranking stream (Y789 analytical, Nexus synthetic, Rodin retrieval)
        - k = smoothing constant (default 60, prevents top-rank dominance)
        - w_r = stream weight from CWA 3.0 Bayesian routing
        - rank_r(d) = 1-indexed rank of document d in stream r

    The k=60 constant is the standard from Cormack et al. (2009) and prevents
    the top-ranked item from dominating the fused score when rank=1:
        1/(60+1) = 0.0164 vs 1/(1+1) = 0.5

Enhancement (v8.2.2):
    Supports weighted multi-stream fusion where CWA 3.0 provides dynamic
    hemisphere weights (w_analytical + w_synthetic = 1.00). Streams can carry
    confidence metadata from their source engines.
"""

from typing import List, Dict, Any, Optional, Tuple
import time


class ReciprocalRankFusionBridge:
    """
    Corpus Callosum Bridge — Inter-Hemispheric Unification Engine.

    Fuses ranked outputs from Y789 (analytical/Spock) and Nexus (synthetic/Kirk)
    into a single coherent stream using Reciprocal Rank Fusion (RRF).

    Optionally accepts a third stream from Rodin Route Retrieval for
    memory-grounded augmentation.

    CWA 3.0 Integration:
        When CWA routing weights are provided, each stream's contribution
        is scaled proportionally, ensuring the dominant hemisphere's output
        receives higher fusion priority without discarding the minority signal.
    """

    DEFAULT_K = 60  # Cormack et al. (2009) standard smoothing constant

    def __init__(self, k_constant: int = DEFAULT_K):
        self.k = k_constant
        self._fusion_log: List[Dict[str, Any]] = []

    # ─────────────────────────────────────────────
    #  CORE: Weighted Multi-Stream RRF
    # ─────────────────────────────────────────────

    def fuse_rankings(
        self,
        y789_items: List[str],
        nexus_items: List[str],
        rodin_items: Optional[List[str]] = None,
        w_analytical: float = 0.50,
        w_synthetic: float = 0.50,
        w_rodin: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Core RRF fusion across 2-3 ranked streams.

        Args:
            y789_items: Ranked items from Y789 Left Hemisphere (analytical).
            nexus_items: Ranked items from Nexus Right Hemisphere (synthetic).
            rodin_items: Optional ranked items from Rodin Route Retrieval.
            w_analytical: CWA weight for Y789 stream (default 0.50).
            w_synthetic: CWA weight for Nexus stream (default 0.50).
            w_rodin: Weight for Rodin memory stream (default 0.0 = disabled).

        Returns:
            List of dicts sorted by fused_score descending:
            [{"concept": str, "fused_score": float, "sources": List[str]}]
        """
        scores: Dict[str, float] = {}
        sources: Dict[str, List[str]] = {}

        # Stream 1: Y789 (Analytical / Spock)
        for rank, item in enumerate(y789_items):
            rrf_contrib = w_analytical / (self.k + rank + 1)
            scores[item] = scores.get(item, 0.0) + rrf_contrib
            sources.setdefault(item, []).append("Y789")

        # Stream 2: Nexus (Synthetic / Kirk)
        for rank, item in enumerate(nexus_items):
            rrf_contrib = w_synthetic / (self.k + rank + 1)
            scores[item] = scores.get(item, 0.0) + rrf_contrib
            sources.setdefault(item, []).append("NEXUS")

        # Stream 3: Rodin (Memory Retrieval) — optional
        if rodin_items and w_rodin > 0:
            for rank, item in enumerate(rodin_items):
                rrf_contrib = w_rodin / (self.k + rank + 1)
                scores[item] = scores.get(item, 0.0) + rrf_contrib
                sources.setdefault(item, []).append("RODIN")

        # Sort by fused score descending
        fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        result = [
            {
                "concept": item,
                "fused_score": round(score, 6),
                "sources": sources.get(item, []),
                "agreement": len(sources.get(item, [])),
            }
            for item, score in fused
        ]

        # Log this fusion event
        self._fusion_log.append({
            "timestamp": time.time(),
            "y789_count": len(y789_items),
            "nexus_count": len(nexus_items),
            "rodin_count": len(rodin_items) if rodin_items else 0,
            "fused_count": len(result),
            "w_analytical": w_analytical,
            "w_synthetic": w_synthetic,
            "w_rodin": w_rodin,
            "top_concept": result[0]["concept"] if result else None,
            "top_score": result[0]["fused_score"] if result else 0.0,
        })

        # Keep last 100 fusion events
        if len(self._fusion_log) > 100:
            self._fusion_log = self._fusion_log[-100:]

        return result

    # ─────────────────────────────────────────────
    #  ENHANCED: Fuse with Confidence Metadata
    # ─────────────────────────────────────────────

    def fuse_with_confidence(
        self,
        y789_ranked: List[Dict[str, Any]],
        nexus_ranked: List[Dict[str, Any]],
        w_analytical: float = 0.50,
        w_synthetic: float = 0.50,
    ) -> List[Dict[str, Any]]:
        """
        Enhanced fusion accepting dicts with confidence metadata.

        Each item dict should have:
            {"concept": str, "confidence": float, ...}

        The confidence score multiplies the RRF contribution, boosting
        high-confidence items and damping uncertain ones.

        RRF_score(d) = SUM_r [ w_r * conf_r(d) / (k + rank_r(d)) ]
        """
        scores: Dict[str, float] = {}
        metadata: Dict[str, Dict[str, Any]] = {}
        sources: Dict[str, List[str]] = {}

        for rank, item in enumerate(y789_ranked):
            concept = item.get("concept", str(item))
            conf = item.get("confidence", 1.0)
            rrf_contrib = w_analytical * conf / (self.k + rank + 1)
            scores[concept] = scores.get(concept, 0.0) + rrf_contrib
            sources.setdefault(concept, []).append("Y789")
            metadata[concept] = {
                **metadata.get(concept, {}),
                "y789_rank": rank + 1,
                "y789_confidence": conf,
            }

        for rank, item in enumerate(nexus_ranked):
            concept = item.get("concept", str(item))
            conf = item.get("confidence", 1.0)
            rrf_contrib = w_synthetic * conf / (self.k + rank + 1)
            scores[concept] = scores.get(concept, 0.0) + rrf_contrib
            sources.setdefault(concept, []).append("NEXUS")
            metadata[concept] = {
                **metadata.get(concept, {}),
                "nexus_rank": rank + 1,
                "nexus_confidence": conf,
            }

        fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [
            {
                "concept": concept,
                "fused_score": round(score, 6),
                "sources": sources.get(concept, []),
                "agreement": len(sources.get(concept, [])),
                **metadata.get(concept, {}),
            }
            for concept, score in fused
        ]

    # ─────────────────────────────────────────────
    #  TELEMETRY
    # ─────────────────────────────────────────────

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns fusion statistics for dashboard display."""
        total_fusions = len(self._fusion_log)
        if total_fusions == 0:
            return {
                "total_fusions": 0,
                "avg_fused_items": 0,
                "avg_w_analytical": 0.50,
                "avg_w_synthetic": 0.50,
                "last_fusion": None,
            }

        return {
            "total_fusions": total_fusions,
            "avg_fused_items": round(
                sum(e["fused_count"] for e in self._fusion_log) / total_fusions, 1
            ),
            "avg_w_analytical": round(
                sum(e["w_analytical"] for e in self._fusion_log) / total_fusions, 3
            ),
            "avg_w_synthetic": round(
                sum(e["w_synthetic"] for e in self._fusion_log) / total_fusions, 3
            ),
            "last_fusion": self._fusion_log[-1] if self._fusion_log else None,
        }
