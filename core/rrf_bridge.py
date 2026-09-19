"""
INTEGRA O/S: RECIPROCAL RANK FUSION
Module: core/rrf_bridge.py
Layer: 2 (Corpus Callosum & Structural Unification)
"""

from typing import List, Dict, Any

class ReciprocalRankFusionBridge:
    """
    Acts as the Corpus Callosum bridging Y789 analytical and Nexus synthetic outputs.
    Unifies disparate ranking streams into a single uncompressed packet.
    """
    def __init__(self, k_constant: int = 60):
        self.k = k_constant

    def fuse_rankings(self, y789_items: List[str], nexus_items: List[str]) -> List[Dict[str, Any]]:
        scores: Dict[str, float] = {}

        for rank, item in enumerate(y789_items):
            scores[item] = scores.get(item, 0.0) + (1.0 / (self.k + rank + 1))

        for rank, item in enumerate(nexus_items):
            scores[item] = scores.get(item, 0.0) + (1.0 / (self.k + rank + 1))

        fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{"concept": item, "fused_score": round(score, 6)} for item, score in fused]
