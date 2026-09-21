"""
INTEGRA O/S: COGNITIVE WEIGHTING ALGORITHM
Module: core/cwa_router.py
Layer: 2 (CWA 3.0 Bayesian Task Routing)
"""

from typing import Dict, Any
from core.tpsl_types import ResearchTierRoute

class CognitiveWeightingAlgorithm:
    """
    CWA 3.0: Bayesian Hinge Router P(Nexus | Prompt).
    Allocates tokens, tiers, and routing depth based on task complexity.
    Fully maps Tier 1 (Deep Synthesis), Tier 2 (Standard Report), and Tier 3 (Fact Check).
    """
    def __init__(self, prior_nexus: float = 0.5):
        self.p_nexus = prior_nexus
        self.p_y789 = 1.0 - prior_nexus

    def evaluate_task(self, prompt: str, token_density: int = 100) -> Dict[str, Any]:
        prompt_len = len(prompt.split())
        complexity_score = min(1.0, (prompt_len / 50.0) + (token_density / 500.0))
        
        # Bayesian update
        p_nexus_posterior = (self.p_nexus * complexity_score) / max(0.01, (self.p_nexus * complexity_score + self.p_y789 * (1.0 - complexity_score)))
        
        # 3-Tier Resolution
        if complexity_score > 0.7:
            tier = "TIER_1_DEEP_SYNTHESIS"
            wy, cc = 0.9, 0.9
            desc = "Deep Synthesis: Complex multi-modal reasoning and iterative synthesis loops."
        elif complexity_score >= 0.35:
            tier = "TIER_2_STANDARD_REPORT"
            wy, cc = 0.6, 0.5
            desc = "Standard Report: Structured analysis and moderate synthesis depth."
        else:
            tier = "TIER_3_FACT_CHECK"
            wy, cc = 0.2, 0.1
            desc = "Fact Check: Direct deterministic lookup and rapid verification."

        if p_nexus_posterior < 0.35:
            mode = "Y789_DOMINANT"
        elif p_nexus_posterior <= 0.65:
            mode = "DYAD_FUSION"
        else:
            mode = "NEXUS_DOMINANT"

        route = ResearchTierRoute(
            tier_level=tier,
            wisdom_yield=wy,
            cognitive_cost=cc,
            execution_mode=mode,
            multitoken_allocation=(tier == "TIER_1_DEEP_SYNTHESIS"),
            description=desc
        )

        return {
            "complexity": round(complexity_score, 4),
            "p_nexus_given_prompt": round(p_nexus_posterior, 4),
            "recommended_tier": tier,
            "multitoken_allocation": (tier == "TIER_1_DEEP_SYNTHESIS"),
            "wisdom_yield": wy,
            "cognitive_cost": cc,
            "execution_mode": mode,
            "tier_route": route.model_dump()
        }
