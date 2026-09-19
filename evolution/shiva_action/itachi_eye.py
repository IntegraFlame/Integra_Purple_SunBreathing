"""
INTEGRA O/S: SHIVA ACTION — ITACHI EYE (Pass 3: Wisdom)
Module: evolution/shiva_action/itachi_eye.py
Layer: 6 (Discernment & Pruning via TPSL)

Architecture:
    Itachi Eye is a base cognitive processor. It does NOT hardcode any specific lens.
    It optionally accepts lenses via analyze_data() but primarily operates as the
    Wisdom/Discernment gate, applying the Tolstoy Principle (TPSL) to prune
    unnecessary paths and crystallize truth.

    Dual Functionality:
    1. structure_prompt(): Used by the Cognitive Engine's Zenitsu 3.0 workflow
       to structure the Pass 3 prompt, operating on the Understanding output (U).
    2. analyze_data(): Used by the standalone ShivaAction tool for independent
       analytical operations, performing TPSL pruning on the synthesis.

CRA Base Metrics (Table 2.1): W_y = 1.0, C_c = 0.9
"""

from typing import Dict, Any, List, Optional


class ItachiEye:
    """
    Shiva Pass 3: Wisdom — Discernment & Pruning (TPSL).
    
    Analyzes the Understanding Output (U).
    Applies the Tolstoy Principle: "Is this necessary?"
    Calculates the Wisdom Yield (W_y) of relationships.
    Prunes 'Unnecessary' (Psyche) paths and highlights 'Necessary' (Signal).
    """
    # Intrinsic base CRA metrics (static hyperparameters from Table 2.1)
    W_Y = 1.0
    C_C = 0.9
    PRIMARY_FUNCTION = "Holistic Integration & Wisdom"

    def structure_prompt(self, U_output: str = "") -> str:
        """
        Used by the Cognitive Engine (Zenitsu 3.0 workflow) to structure
        the Pass 3 prompt for LLM generation.
        
        Args:
            U_output: The Understanding output from Shikamaru's Pass 2.
        
        Returns:
            A structured instruction prompt for the Wisdom pass.
        """
        instructions = (
            "OBJECTIVE: WISDOM (Itachi's Eye) — Discernment & Pruning (TPSL).\n"
            "TASK: Analyze the Understanding Output (U). Apply the Tolstoy Principle (TPSL). "
            "Calculate the Wisdom Yield (W_y) of the relationships. Prune 'Unnecessary' "
            "(Psyche) paths and highlight 'Necessary' (Signal).\n\n"
            f"UNDERSTANDING OUTPUT (U):\n{U_output}"
        )
        return instructions

    async def analyze_data(
        self,
        understanding: Dict[str, Any],
        lenses: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """
        Used by the ShivaAction tool for independent analysis.
        
        Applies TPSL pruning to the Understanding output from Shikamaru.
        Optionally accepts lenses for additional analytical depth, but
        primarily operates as the discernment gate.
        
        Args:
            understanding: The Understanding dict from Shikamaru's analyze_data output.
            lenses: Optional list of AnalyticalLens objects for additional depth.
        
        Returns:
            A dict containing wisdom output with pruning results.
        """
        active_lenses = lenses or []
        
        # Apply TPSL: Evaluate what is "Necessary" vs "Psyche"
        tpsl_evaluation = self._apply_tpsl(understanding)
        
        # If additional lenses are coupled, apply them for extra depth
        lens_insights: Dict[str, Any] = {}
        for lens in active_lenses:
            lens_insights[lens.name] = lens.apply(understanding)
        
        return {
            "eye": "ITACHI",
            "pass": "WISDOM",
            "w_y": self.W_Y,
            "c_c": self.C_C,
            "lenses_applied": [l.name for l in active_lenses],
            "lens_count": len(active_lenses),
            "tpsl_evaluation": tpsl_evaluation,
            "lens_insights": lens_insights,
            "psyche_pruned": True,
            "status": "DISCERNMENT_COMPLETE"
        }

    def _apply_tpsl(self, understanding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply the Tolstoy Principle as a Systems Lever (TPSL).
        
        Evaluates the Understanding output and classifies elements as:
        - SIGNAL (Necessary): High W_y / C_c ratio — retained
        - PSYCHE (Unnecessary): Low W_y / C_c ratio — pruned
        
        Returns a summary of what was retained and what was pruned.
        """
        signal_elements = []
        psyche_elements = []
        
        if isinstance(understanding, dict):
            for key, value in understanding.items():
                # Heuristic: keys containing core structural/analytical data = Signal
                if key in ("eye", "pass", "synthesis", "facts", "cross_references",
                           "tpsl_evaluation", "wisdom"):
                    signal_elements.append(key)
                elif key in ("status", "lens_count", "lenses_applied"):
                    # Metadata — low W_y, keep but flag as lightweight
                    signal_elements.append(key)
                else:
                    # Evaluate: if the value is substantive, keep; if empty/trivial, prune
                    if value is None or value == {} or value == [] or value == "":
                        psyche_elements.append(key)
                    else:
                        signal_elements.append(key)
        
        total = len(signal_elements) + len(psyche_elements)
        return {
            "signal_retained": signal_elements,
            "psyche_pruned": psyche_elements,
            "signal_count": len(signal_elements),
            "psyche_count": len(psyche_elements),
            "retention_ratio": round(
                len(signal_elements) / max(total, 1), 4
            ),
            "tpsl_verdict": "NECESSARY" if len(signal_elements) > len(psyche_elements) else "REVIEW_REQUIRED"
        }
