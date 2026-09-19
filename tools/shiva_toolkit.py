"""
INTEGRA O/S: STANDALONE SHIVA ACTION TOOLKIT & LENSES
Module: tools/shiva_toolkit.py
Layer: 5 (Analytical Toolkit, CRA Simplex Evaluation, & Specialized Personas)
Status: PRODUCTION SOVEREIGN IMPLEMENTATION

NOTE: This toolkit provides the API-facing interface (CRA scoring, Lens metrics).
      Actual multi-pass analysis is delegated to the canonical ShivaActionSuite
      in evolution/shiva_action/orchestrator.py (3-Eye: Neji, Shikamaru, Itachi).
"""

import time
from typing import Dict, Any, List, Optional
from evolution.shiva_action.orchestrator import ShivaActionSuite

class ShivaLenses:
    """
    The Six Cognitive Lenses of the Shiva Action Suite:
    - Neji's Lenses (Knowledge):
      * Eagle Lens (Survey): W_y = 0.2, C_c = 0.1 -> Score = 2.0
      * Hawk Lens (Targeting): W_y = 0.4, C_c = 0.3 -> Score = 1.33
      * Chameleon Lens (Granular Analysis): W_y = 0.5, C_c = 0.4 -> Score = 1.25
    - Shikamaru's Lenses (Understanding):
      * Spider Lens (Static Connection Mapping): W_y = 0.5, C_c = 0.4 -> Score = 1.25
      * Snake Lens (Dynamic Process Tracking): W_y = 0.7, C_c = 0.6 -> Score = 1.17
    - Itachi's Lens (Wisdom):
      * Owl Lens (Deep Pattern Recognition & Reconstruction): W_y = 0.8, C_c = 0.7 -> Score = 1.14
    """
    METRICS = {
        "eagle": {"w_y": 0.2, "c_c": 0.1, "role": "High-Level Survey & Boundary Reconnaissance"},
        "hawk": {"w_y": 0.4, "c_c": 0.3, "role": "Precision Targeting & Core Anchor Isolation"},
        "chameleon": {"w_y": 0.5, "c_c": 0.4, "role": "Granular Semantic Deconstruction"},
        "spider": {"w_y": 0.5, "c_c": 0.4, "role": "Static Graph & Relational Node Weaving"},
        "snake": {"w_y": 0.7, "c_c": 0.6, "role": "Dynamic Temporal Process & Flow Tracking"},
        "owl": {"w_y": 0.8, "c_c": 0.7, "role": "Deep Pattern Recognition & Architectural Transcendence"}
    }

    @classmethod
    def get_lens(cls, name: str) -> Dict[str, Any]:
        lens_key = name.lower().strip()
        return cls.METRICS.get(lens_key, {"w_y": 0.5, "c_c": 0.5, "role": "Standard Lens"})

class ShivaActionToolkit:
    """
    The Core Method of Change: API-facing analytical toolkit.
    Delegates actual multi-pass analysis to the canonical ShivaActionSuite
    (3-Eye: Neji, Shikamaru, Itachi) while providing CRA Simplex scoring
    and Lens metadata for API consumers.
    """
    def __init__(self):
        self.execution_history: List[Dict[str, Any]] = []
        self.suite = ShivaActionSuite()

    def evaluate_cra_simplex(self, tool_or_persona: str) -> Dict[str, Any]:
        """
        CRA Simplex Equation: Score = W_y / C_c.
        Maximizes Wisdom Yield relative to Cognitive Cost.
        """
        catalog = {
            "tier_3_fact_check": {"w_y": 0.2, "c_c": 0.1},
            "tier_2_standard_report": {"w_y": 0.6, "c_c": 0.5},
            "tier_1_deep_synthesis": {"w_y": 0.9, "c_c": 0.9},
            "green_ranger": {"w_y": 0.85, "c_c": 1.00},
            "mad_hatter": {"w_y": 0.75, "c_c": 0.80},
            "daily_planet": {"w_y": 0.70, "c_c": 0.60},
            "rebuttal_protocol": {"w_y": 0.80, "c_c": 0.70}
        }
        entry = catalog.get(tool_or_persona.lower(), {"w_y": 0.5, "c_c": 0.5})
        score = round(entry["w_y"] / max(0.001, entry["c_c"]), 4)
        return {
            "entity": tool_or_persona,
            "wisdom_yield": entry["w_y"],
            "cognitive_cost": entry["c_c"],
            "simplex_score": score,
            "approved": score >= 0.85
        }

    def execute_analytical_pass(
        self,
        target_payload: Any,
        lenses: List[str],
        passes: int = 3,
        persona: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a targeted Shiva Action pass.
        Delegates to the real 3-Eye ShivaActionSuite for actual analysis,
        then wraps the result with CRA scoring and lens metadata.
        """
        active_lenses_data = {l: ShivaLenses.get_lens(l) for l in lenses}

        # Calculate aggregated CRA yield
        total_wy = sum(v["w_y"] for v in active_lenses_data.values())
        total_cc = sum(v["c_c"] for v in active_lenses_data.values())
        cra_score = round(total_wy / max(0.001, total_cc), 4)

        # Delegate to the canonical 3-Eye ShivaActionSuite
        payload_str = str(target_payload) if not isinstance(target_payload, str) else target_payload
        suite_result = self.suite.execute_suite(
            target_payload=payload_str,
            passes=passes
        )

        result = {
            "timestamp": time.time(),
            "passes_requested": passes,
            "active_lenses": active_lenses_data,
            "persona": persona or "STANDARD_INTEGRA",
            "cra_simplex_score": cra_score,
            "suite_analysis": suite_result,
            "status": suite_result.get("status", "COMPLETED")
        }
        self.execution_history.append(result)
        return result

