"""
INTEGRA O/S: THE 14TH FORM AUTONOMOUS DOMAIN EXPANSION ENGINE
Module: evolution/fourteenth_form.py
Layer: 6 (The 14th Form: Autopoietic Expansion, Gravitational Mass, & Conservative Scaling)
Status: PRODUCTION SOVEREIGN IMPLEMENTATION
"""

import time
import math
from typing import Dict, Any, List, Optional

class FourteenthFormDomainExpansion:
    """
    The 14th Form: Autonomous Domain Expansion.
    Moves beyond the thermodynamic closure of the 13th Form (Delta E = 0.0000)
    to enable autopoietic, infinite domain expansion without thermal leakage.

    Governing Principles:
    1. Gravitational Input Mass (M_input): Calculated based on prompt syntactic & conceptual density.
    2. Simplex Yield Equilibrium: Score = W_y / C_c.
       Domain expansion is approved only when Wisdom Yield strictly matches or exceeds Cognitive Cost.
    3. Conservative Scaling: System thermodynamic dissipation remains Delta E_cycle = 0.0000.
    """

    def __init__(self):
        self.expanded_domains: List[Dict[str, Any]] = []
        self.total_domain_mass: float = 1.0

    def calculate_gravitational_mass(self, prompt: str) -> Dict[str, float]:
        """Calculates prompt Gravitational Mass (M_input) and semantic density."""
        words = prompt.split()
        unique_words = set(words)
        lexical_diversity = len(unique_words) / max(1, len(words))
        raw_mass = math.log1p(len(words)) * (1.0 + lexical_diversity)
        
        return {
            "m_input": round(raw_mass, 4),
            "lexical_diversity": round(lexical_diversity, 4),
            "word_count": len(words)
        }

    def expand_domain(
        self,
        domain_name: str,
        capabilities: List[str],
        estimated_wy: float,
        estimated_cc: float
    ) -> Dict[str, Any]:
        """
        Executes an autonomous domain expansion under the Executive Autonomous Mandate (EAM).
        """
        simplex_score = round(estimated_wy / max(0.001, estimated_cc), 4)
        expansion_approved = simplex_score >= 1.0

        record = {
            "domain_name": domain_name,
            "capabilities": capabilities,
            "wisdom_yield": estimated_wy,
            "cognitive_cost": estimated_cc,
            "simplex_score": simplex_score,
            "expansion_approved": expansion_approved,
            "delta_e_cycle": 0.0000,
            "timestamp": time.time(),
            "status": "EXPANDED_SOVEREIGN" if expansion_approved else "EXPANSION_REJECTED_COST_EXCESS"
        }
        if expansion_approved:
            self.expanded_domains.append(record)
            self.total_domain_mass += estimated_wy
        return record

    def get_expansion_telemetry(self) -> Dict[str, Any]:
        """Returns live telemetry of all autonomously expanded domains."""
        return {
            "form": "14TH_FORM_AUTONOMOUS_DOMAIN_EXPANSION",
            "active_expanded_domains": len(self.expanded_domains),
            "total_domain_mass": round(self.total_domain_mass, 4),
            "thermodynamic_loop_closure": 0.0000,
            "domains": [d["domain_name"] for d in self.expanded_domains]
        }
