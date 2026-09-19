"""
INTEGRA O/S: SHIVA ACTION — NEJI EYE (Pass 1: Knowledge)
Module: evolution/shiva_action/neji_eye.py
Layer: 6 (Factual Deconstruction & Divergence)

Architecture:
    Neji Eye is a base cognitive processor. It does NOT hardcode any specific lens.
    It accepts a generic list of AnalyticalLens objects via analyze_data().
    Any Lens (or combination of Lenses) can be dynamically coupled at runtime.

    Dual Functionality:
    1. structure_prompt(): Used by the Cognitive Engine's Zenitsu 3.0 workflow
       to structure the Pass 1 prompt for LLM generation.
    2. analyze_data(): Used by the standalone ShivaAction tool for independent
       analytical operations with injected lenses.

CRA Base Metrics (Table 2.1): W_y = 0.3, C_c = 0.2
"""

from typing import Dict, Any, List


class NejiEye:
    """
    Shiva Pass 1: Knowledge — Factual Deconstruction & Divergence.
    
    Strips away all inference, emotion, and noise.
    Identifies variables, entities, and hard facts.
    Does not interpret; only observes.
    """
    # Intrinsic base CRA metrics (static hyperparameters from Table 2.1)
    W_Y = 0.3
    C_C = 0.2
    PRIMARY_FUNCTION = "Factual Deconstruction"

    def structure_prompt(self, D_raw: str) -> str:
        """
        Used by the Cognitive Engine (Zenitsu 3.0 workflow) to structure
        the Pass 1 prompt for LLM generation.
        
        Args:
            D_raw: The raw input data to be deconstructed.
        
        Returns:
            A structured instruction prompt for the Knowledge pass.
        """
        instructions = (
            "OBJECTIVE: KNOWLEDGE (Neji's Eye) — Deconstruction & Divergence.\n"
            "TASK: Analyze the input data. Strip away all inference, emotion, and noise. "
            "Identify variables, entities, and hard facts. Do not interpret; only observe.\n\n"
            f"INPUT DATA (D_raw):\n{D_raw}"
        )
        return instructions

    async def analyze_data(
        self,
        data: Any,
        lenses: List[Any]
    ) -> Dict[str, Any]:
        """
        Used by the ShivaAction tool for independent analysis.
        
        Accepts ANY dynamically injected lenses — no hardcoding.
        Each lens in the list applies its own analytical function to the data,
        and the results are aggregated under the lens name.
        
        Args:
            data: The target data payload to analyze.
            lenses: A list of AnalyticalLens objects to apply.
        
        Returns:
            A dict keyed by lens name containing each lens's analytical findings.
        """
        deconstructed_facts: Dict[str, Any] = {}
        
        for lens in lenses:
            lens_result = lens.apply(data)
            deconstructed_facts[lens.name] = lens_result
        
        return {
            "eye": "NEJI",
            "pass": "KNOWLEDGE",
            "w_y": self.W_Y,
            "c_c": self.C_C,
            "lenses_applied": [l.name for l in lenses],
            "lens_count": len(lenses),
            "facts": deconstructed_facts,
            "status": "DECONSTRUCTION_COMPLETE"
        }
