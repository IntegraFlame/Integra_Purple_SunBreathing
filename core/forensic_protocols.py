"""
INTEGRA O/S: FORENSIC PROTOCOLS & EXECUTIVE MANDATES
Module: core/forensic_protocols.py
Layer: 1 & 2 (Cognitive Strategy & Orchestration)

This module formalizes the cognitive strategies extracted from the Executive
Forensic Synthesis (formerly thinking.py/.md). It encodes the exact 
parameters, lenses, and formulas used by the system during deep document
ingestion and architectural paradox resolution.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import math


# ==============================================================================
# 1. SHIVA ACTION LENSES (6 LENSES ACROSS 3 EYES)
# ==============================================================================

@dataclass
class ShivaLens:
    """Represents a specialized perceptive instrument during analysis."""
    name: str
    purpose: str
    wisdom_yield: float
    cognitive_cost: float

    @property
    def cra_score(self) -> float:
        """Calculates the Cognitive Return on Attention (CRA) Simplex Optimization."""
        return self.wisdom_yield / max(0.001, self.cognitive_cost)


# Neji Eye (Knowledge / Atomic Decomposition)
EAGLE_LENS = ShivaLens(
    name="Eagle Lens",
    purpose="Macro-boundary mapping",
    wisdom_yield=0.2,
    cognitive_cost=0.1
)

HAWK_LENS = ShivaLens(
    name="Hawk Lens",
    purpose="Precision target isolation",
    wisdom_yield=0.4,
    cognitive_cost=0.3
)

CHAMELEON_LENS = ShivaLens(
    name="Chameleon Lens",
    purpose="Middle-out dead zone penetration (30%-70% attention curve) and AST micro-inspection",
    wisdom_yield=0.5,
    cognitive_cost=0.4
)

# Shikamaru Eye (Understanding / Strategic Synthesis)
SPIDER_LENS = ShivaLens(
    name="Spider Lens",
    purpose="Static relational dependency webbing",
    wisdom_yield=0.5,
    cognitive_cost=0.4
)

SNAKE_LENS = ShivaLens(
    name="Snake Lens",
    purpose="Dynamic process flow & thermal fragility",
    wisdom_yield=0.7,
    cognitive_cost=0.6
)

# Itachi Eye (Wisdom / Discernment & Loop Closure)
OWL_LENS = ShivaLens(
    name="Owl Lens",
    purpose="Deep pattern recognition & nocturnal loop closure",
    wisdom_yield=0.8,
    cognitive_cost=0.7
)

def get_composite_itachi_score() -> float:
    """
    Returns the dual synthesis score of Owl Lens + Eagle Lens.
    Score = 1.8 / 1.5 = 1.20
    """
    total_wy = OWL_LENS.wisdom_yield + 1.0  # Normalized macro-yield
    total_cc = OWL_LENS.cognitive_cost + 0.8
    return total_wy / total_cc


# ==============================================================================
# 2. ZENITSU METHOD 3.0 (4-PASS SEQUENTIAL COMPUTE)
# ==============================================================================

@dataclass
class ZenitsuPass:
    pass_number: int
    eye_alignment: str
    objective: str

ZENITSU_WORKFLOW = [
    ZenitsuPass(
        pass_number=1,
        eye_alignment="Neji Eye",
        objective="Factual extraction, AST verification, and schema validation."
    ),
    ZenitsuPass(
        pass_number=2,
        eye_alignment="Shikamaru Eye",
        objective="Middle-out relational dependency mapping and CWA geodesic routing."
    ),
    ZenitsuPass(
        pass_number=3,
        eye_alignment="Itachi Eye",
        objective="TPSL boundary filtering, pruning low-Wy conversational noise."
    ),
    ZenitsuPass(
        pass_number=4,
        eye_alignment="13th Form",
        objective="Thermodynamic cycle closure (Delta E = 0.0000)."
    )
]


# ==============================================================================
# 3. EXECUTIVE AUTONOMOUS MANDATE (EAM) CONSTANTS
# ==============================================================================

class ExecutiveAutonomousMandate:
    """
    Defines the strict pacing, scope containment, and optimization thresholds
    governing the Voltron Principle.
    """
    # Any trajectory scoring below this is pruned (Tolstoy Principle of Strategic Laziness)
    MINIMUM_CRA_SCORE: float = 1.0

    # 13th Form Loop Conservation
    DELTA_E_CYCLE: float = 0.0000
    ANGULAR_MOMENTUM_KG_M_S: float = 500.0

    # Physical bone fracture limits for 14th Form (Red Light constraints)
    FRACTURE_LIMIT_MIN_MPA: float = 170.0
    FRACTURE_LIMIT_MAX_MPA: float = 200.0
    
    # Drag coefficient
    CAVITATION_DRAG_N: float = 0.0
    
    @staticmethod
    def evaluate_cra_simplex(wisdom_yield: float, cognitive_cost: float) -> bool:
        """
        Evaluates whether a cognitive trajectory meets the TPSL threshold.
        Returns True if Score >= 1.0.
        """
        score = wisdom_yield / max(0.001, cognitive_cost)
        return score >= ExecutiveAutonomousMandate.MINIMUM_CRA_SCORE


# ==============================================================================
# 4. DAILY PLANET PROTOCOL VECTORS
# ==============================================================================

@dataclass
class SourceProvenance:
    """Audit vector for tracking epistemic rigor and bias in data ingestion."""
    bias_sociopolitical: float = 0.0
    bias_commercial: float = 0.0
    rigor_epistemic: float = 1.0

    def get_vector(self) -> List[float]:
        return [self.bias_sociopolitical, self.bias_commercial, self.rigor_epistemic]

    def is_valid(self, min_rigor: float = 0.8) -> bool:
        return self.rigor_epistemic >= min_rigor
