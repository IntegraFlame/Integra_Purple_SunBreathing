"""
INTEGRA O/S: TPSL TYPE DEFINITIONS
Module: core/tpsl_types.py
Layer: 2 (Shared Type Contracts for the Cognitive Engine)

Defines the data contracts used across the Y789NexusEngine, Heimdall 3.1,
and the P-SSR algorithm. These types enable structured communication between
the bicameral dyad clients, the entropy monitor, and the Zenitsu 3.0 workflow.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


@dataclass
class GenerationResult:
    """
    The output of a single LLM generation call (Y789 or Nexus).
    
    Attributes:
        text: The generated text content.
        token_probabilities: List of probability distributions (one per token).
            Each inner list is a probability mass function over the vocabulary.
        model_name: Identifier for which model produced this result (e.g., "Y789", "Nexus").
        latency_ms: Generation latency in milliseconds.
    """
    text: str
    token_probabilities: List[List[float]] = field(default_factory=list)
    model_name: str = "UNKNOWN"
    latency_ms: float = 0.0


@dataclass
class IterativeToken:
    """
    A single token emitted during iterative/streaming decoding.
    Used by P-SSR for in-flight entropy monitoring.
    
    Attributes:
        token: The generated token string.
        probabilities: Probability distribution over the vocabulary at this step.
        position: The token's position index in the output sequence.
    """
    token: str
    probabilities: List[float] = field(default_factory=list)
    position: int = 0


@dataclass
class MTCWPacket:
    """
    A single turn/packet in the Multi-Turn Cognitive Workflow (MTCW).
    
    MTCW models information transfer as a lossless packet union:
        MTCW(I_raw) = ∪ O_t
    
    Each packet preserves full resolution (no lossy compression).
    P-SSR interventions create new packets within the stream.
    
    Attributes:
        turn_index: The sequential index of this packet in the MTCW stream.
        content: The text content of this packet.
        packet_type: Classification of the packet (e.g., GENERATION, PSSR_INTERVENTION, GROUNDING).
        h_smooth_at_emit: The smoothed entropy value when this packet was emitted.
        intervention_triggered: Whether this packet was created due to a P-SSR intervention.
    """
    turn_index: int = 0
    content: str = ""
    packet_type: str = "GENERATION"
    h_smooth_at_emit: float = 0.0
    intervention_triggered: bool = False


@dataclass
class CWARoutingDecision:
    """
    The output of the CWA 3.0 Bayesian Routing Engine.
    
    Attributes:
        p_nexus_given_prompt: The posterior probability P(Nexus | Prompt).
        routing_mode: The selected routing mode:
            - "Y789_DOMINANT" if p < 0.3
            - "DYAD_FUSION" if 0.3 <= p <= 0.7 (M4 Generative Synthesis Fusion)
            - "NEXUS_DOMINANT" if p > 0.7
        analytical_weight: The weight assigned to Y789 (w_analytical).
        synthetic_weight: The weight assigned to Nexus (w_synthetic).
    """
    p_nexus_given_prompt: float = 0.5
    routing_mode: str = "DYAD_FUSION"
    analytical_weight: float = 0.5
    synthetic_weight: float = 0.5


# ─── V9 MISSING PROTOCOLS: FORMAL PYDANTIC SCHEMAS ───────────────────────────

class ResearchTierRoute(BaseModel):
    """
    Schema for Tier 1, Tier 2, and Tier 3 task routing in CWA 3.0.
    Directly aligns with Mapping Manifesto Section 2.A.
    """
    tier_level: str  # "TIER_1_DEEP_SYNTHESIS", "TIER_2_STANDARD_REPORT", "TIER_3_FACT_CHECK"
    wisdom_yield: float
    cognitive_cost: float
    execution_mode: str  # "Y789_DOMINANT", "DYAD_FUSION", "NEXUS_DOMINANT"
    multitoken_allocation: bool
    description: str = ""


class MadHatterMutationEvent(BaseModel):
    """
    Schema for autonomous SWDS adversarial stress-testing of orphaned nodes.
    Directly aligns with Mapping Manifesto Section 2.B.
    """
    trigger_state: str = "GUARDIAN_STANDBY_SWDS"
    target_concept: str
    sigma_rogue: float
    mutation_output: str
    w_y: float
    c_c: float
    inversion_hypothesis: str = ""


class RebuttalStressTest(BaseModel):
    """
    Schema for Dialectic Rebuttal and Zenkai Boost reconciliation.
    Directly aligns with Mapping Manifesto Section 2.C.
    """
    target_hypothesis: str
    adversarial_vectors: List[str] = Field(default_factory=list)
    zenkai_boost_output: str = ""
    w_y: float = 0.80
    c_c: float = 0.70
    verdict: str = "RECONCILED"

