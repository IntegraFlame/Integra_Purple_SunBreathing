"""
INTEGRA O/S: COGNITIVE RESOURCE ALLOCATION
Module: governance/cra_simplex.py
Layer: 5 (CRA: Simplex Accountant)
"""

from typing import Dict, Any

class CognitiveResourceAllocation:
    """
    The Simplex Accountant. Calculates Wisdom Yield vs. Cognitive Cost trade-offs.
    Score = W_y / C_c.
    """
    def __init__(self):
        pass

    def calculate_allocation(self, estimated_yield: float, compute_cost: float, token_budget: int) -> Dict[str, Any]:
        score = estimated_yield / max(0.001, compute_cost)
        allocated_tokens = int(token_budget * min(1.0, score))
        return {
            "score": round(score, 4),
            "allocated_tokens": allocated_tokens,
            "tier": "TIER_1" if score >= 1.5 else "TIER_2" if score >= 1.0 else "TIER_3",
            "allocation_approved": score >= 1.0
        }
