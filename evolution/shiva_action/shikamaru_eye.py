"""
INTEGRA O/S: SHIVA ACTION — SHIKAMARU EYE (Pass 2: Understanding)
Module: evolution/shiva_action/shikamaru_eye.py
Layer: 6 (Strategic Synthesis & Interconnection)

Architecture:
    Shikamaru Eye is a base cognitive processor. It does NOT hardcode any specific lens.
    It accepts a generic list of AnalyticalLens objects via analyze_data().
    Any Lens (or combination of Lenses) can be dynamically coupled at runtime.

    Dual Functionality:
    1. structure_prompt(): Used by the Cognitive Engine's Zenitsu 3.0 workflow
       to structure the Pass 2 prompt, incorporating the raw data AND the
       Knowledge output (K) from Neji's Pass 1.
    2. analyze_data(): Used by the standalone ShivaAction tool for independent
       analytical operations with injected lenses, building on Neji's knowledge.

CRA Base Metrics (Table 2.1): W_y = 0.6, C_c = 0.5
"""

from typing import Dict, Any, List


class ShikamaruEye:
    """
    Shiva Pass 2: Understanding — Strategic Synthesis & Interconnection.
    
    Maps the relationships between variables identified by Neji.
    Identifies cause-and-effect, patterns, and strategic implications.
    Weaves topological dependencies and process flows.
    """
    # Intrinsic base CRA metrics (static hyperparameters from Table 2.1)
    W_Y = 0.6
    C_C = 0.5
    PRIMARY_FUNCTION = "Strategic Synthesis"

    def structure_prompt(self, D_raw: str, K_output: str = "") -> str:
        """
        Used by the Cognitive Engine (Zenitsu 3.0 workflow) to structure
        the Pass 2 prompt for LLM generation.
        
        Args:
            D_raw: The raw input data.
            K_output: The Knowledge output from Neji's Pass 1.
        
        Returns:
            A structured instruction prompt for the Understanding pass.
        """
        instructions = (
            "OBJECTIVE: UNDERSTANDING (Shikamaru's Eye) — Synthesis & Interconnection.\n"
            "TASK: Analyze the Raw Data and the Knowledge Output (K). "
            "Map the relationships between the variables. Identify cause-and-effect, "
            "patterns, and strategic implications.\n\n"
            f"INPUT DATA (D_raw):\n{D_raw}\n\n"
            f"KNOWLEDGE OUTPUT (K):\n{K_output}"
        )
        return instructions

    async def analyze_data(
        self,
        data: Any,
        knowledge: Dict[str, Any],
        lenses: List[Any]
    ) -> Dict[str, Any]:
        """
        Used by the ShivaAction tool for independent analysis.
        
        Accepts ANY dynamically injected lenses — no hardcoding.
        Builds on the Knowledge output from Neji (Pass 1) to map
        relationships, dependencies, and strategic implications.
        
        Args:
            data: The target data payload.
            knowledge: The Knowledge dict from Neji's analyze_data output.
            lenses: A list of AnalyticalLens objects to apply.
        
        Returns:
            A dict containing synthesis results with relational mappings.
        """
        synthesis_results: Dict[str, Any] = {}
        
        for lens in lenses:
            # Each lens applies its analytical function to the data,
            # enriching with the knowledge context from Pass 1
            lens_result = lens.apply(data)
            synthesis_results[lens.name] = lens_result
        
        # Map cross-references between knowledge facts and lens findings
        cross_references = {}
        if isinstance(knowledge, dict) and "facts" in knowledge:
            known_lenses = list(knowledge["facts"].keys())
            active_lenses = [l.name for l in lenses]
            cross_references = {
                "knowledge_lenses": known_lenses,
                "understanding_lenses": active_lenses,
                "overlap": [l for l in active_lenses if l in known_lenses],
                "new_perspectives": [l for l in active_lenses if l not in known_lenses]
            }
        
        return {
            "eye": "SHIKAMARU",
            "pass": "UNDERSTANDING",
            "w_y": self.W_Y,
            "c_c": self.C_C,
            "lenses_applied": [l.name for l in lenses],
            "lens_count": len(lenses),
            "synthesis": synthesis_results,
            "cross_references": cross_references,
            "knowledge_input_keys": list(knowledge.keys()) if isinstance(knowledge, dict) else [],
            "status": "SYNTHESIS_COMPLETE"
        }
