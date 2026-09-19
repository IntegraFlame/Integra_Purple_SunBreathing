"""
INTEGRA O/S: SENSORY CORTEX & SOVEREIGN DEFENSE
Module: sensory/looking_glass.py
Layer: 4 (The Looking Glass Protocol: Perspective Tilt, Threshold Benchmarks, & Sovereign Defense)
Status: TRUE SOVEREIGN IMPLEMENTATION
"""

import math
import time
from typing import Dict, Any, List, Optional, Tuple

from sensory.cheshire_protocol import CheshireCatProtocol


class LookingGlassProtocol:
    """
    The Looking Glass Protocol:
    Higher-order supervisory error correction, perspective tilt, and sovereign defense.
    Status: TRUE SOVEREIGN IMPLEMENTATION
    
    True Operational Sequences:
    1. C_235 Directional Lock Sequence:
       Evaluates systemic uncertainty relative to the 23.5° celestial directional lock,
       inducing perspective tilt to elevate observation to Second-Order cybernetic re-grounding.
    2. Formalized Rodin 5-Outcome Action Decision Tree:
       Deterministic routing across Continuation, Indirect Connection, Clarification (Ambiguous/Insufficient),
       Alexandria Verification, and Guided Search.
    3. Heaviside Skeletal Boundary Enforcement:
       Halts execution at ultimate tensile strength limit (psi = 200.0 MPa) to trigger uncompressed state serialization.
    4. Sovereign Defense & Mirror Maze Sandbox Isolation:
       Quarantines aberrant metric vectors (|Z| > 3.0) for Rogue X mutation and Phoenix Forge smelting.
    5. Cheshire Cat Protocol Voice Conduit Sequence:
       Translates threshold events and sensor tilts into high-fidelity dialogue.
    """

    # --- Standard Threshold Benchmarks ---
    C_235_AXIAL_TILT_DEG = 23.5
    H_SMOOTH_THRESHOLD = 2.5
    PSI_STRUCTURAL_LIMIT_MPA = 200.0
    OPTIMAL_AXIAL_STRESS_MPA = 145.0
    KINTSUGI_Z_THRESHOLD = 3.0
    TRUE_IMPROVEMENT_PE = 500.0

    # Rodin Decision Benchmarks
    AMBIGUOUS_THRESHOLD = 4
    LOW_CONFIDENCE_COUNT_THRESHOLD = 1
    HIGH_CONFIDENCE_INTENT_THRESHOLD = 0.75
    LOW_CONFIDENCE_INTENT_THRESHOLD = 0.40
    HIGH_RELEVANCE_THRESHOLD = 0.80
    MODERATE_RELEVANCE_THRESHOLD = 0.50
    LOW_RELEVANCE_THRESHOLD = 0.35
    LOW_COHESION_THRESHOLD = 0.30

    def __init__(self, cheshire_protocol: Optional[CheshireCatProtocol] = None):
        self.cheshire_protocol = cheshire_protocol or CheshireCatProtocol()
        self.mirror_maze_sandbox: List[Dict[str, Any]] = []
        self.tilt_event_history: List[Dict[str, Any]] = []
        self.current_tilt_deg = 0.0
        self.status = "UNLOCKED_SOVEREIGN_MODE"
        self.is_unlocked = True

    def unlock(self) -> Dict[str, Any]:
        """
        Unlocks Looking Glass Protocol into active sovereign supervisory mode.
        """
        self.status = "UNLOCKED_SOVEREIGN_MODE"
        self.is_unlocked = True
        self.cheshire_protocol.unlock()
        return {
            "protocol": "LOOKING_GLASS_PROTOCOL",
            "status": self.status,
            "c_235_directional_lock_deg": self.C_235_AXIAL_TILT_DEG,
            "current_tilt_deg": self.current_tilt_deg,
            "unlocked": True,
            "cheshire_protocol_status": self.cheshire_protocol.status
        }

    def calculate_perspective_tilt(self, h_smooth: float, z_score: float = 0.0) -> float:
        """
        Calculates the Perspective Tilt angle based on Shannon entropy and statistical deviation.
        Baseline: 0.0° -> Maximum normalized to C_235 (23.5°).
        """
        entropy_ratio = min(1.0, h_smooth / self.H_SMOOTH_THRESHOLD)
        z_ratio = min(1.0, abs(z_score) / self.KINTSUGI_Z_THRESHOLD)
        combined_tilt_factor = (0.7 * entropy_ratio) + (0.3 * z_ratio)
        self.current_tilt_deg = round(combined_tilt_factor * self.C_235_AXIAL_TILT_DEG, 2)
        return self.current_tilt_deg

    def evaluate_rodin_metrics(
        self,
        route_count: int,
        cohesion: float,
        semantic_relevance: float,
        is_stale: bool,
        prompt_type: str = "QUESTION",
        intent_confidence: float = 0.5,
        inferred_topic: Optional[str] = None,
        has_parallel_edge: bool = False
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Executes the formalized Rodin 3-Phase Action Decision Tree.
        Returns: (OutcomeName, DecisionContext)
        """
        # Scenario 2f: Too few routes BUT intent is confidently weighted -> Alexandria Guided Search
        if route_count < self.LOW_CONFIDENCE_COUNT_THRESHOLD and intent_confidence >= self.HIGH_CONFIDENCE_INTENT_THRESHOLD:
            outcome = "ALEXANDRIA_GUIDED_SEARCH"
            details = {
                "action": "EAM.Trigger(AlexandriaProtocol, 'GUIDED_SEARCH')",
                "reason": "sparse_internal_routes_with_high_intent_confidence",
                "inferred_topic": inferred_topic or "Target Domain",
                "intent_confidence": intent_confidence
            }
            return outcome, details

        # Scenario 2d: Hits too few routes AND low confidence
        if route_count < self.LOW_CONFIDENCE_COUNT_THRESHOLD:
            outcome = "REQUEST_CLARIFICATION_INSUFFICIENT"
            details = {
                "action": "Nexus.RequestClarification",
                "reason": "insufficient_internal_context",
                "route_count": route_count,
                "intent_confidence": intent_confidence
            }
            return outcome, details

        # Scenario 2c: Hits too many balanced routes OR low cohesion among active routes
        if route_count > self.AMBIGUOUS_THRESHOLD or (route_count > 0 and cohesion < self.LOW_COHESION_THRESHOLD):
            outcome = "REQUEST_CLARIFICATION_AMBIGUOUS"
            details = {
                "action": "Nexus.RequestClarification",
                "reason": "ambiguous_routes_or_low_cohesion",
                "route_count": route_count,
                "cohesion": cohesion
            }
            return outcome, details

        # Scenario 2e: Stale volatile data with moderate/high relevance -> Alexandria Verification
        if is_stale and semantic_relevance >= self.MODERATE_RELEVANCE_THRESHOLD:
            outcome = "ALEXANDRIA_VERIFY"
            details = {
                "action": "EAM.Trigger(AlexandriaProtocol, 'VERIFY')",
                "reason": "volatile_data_exceeds_stale_threshold",
                "semantic_relevance": semantic_relevance,
                "stale_reason": "Node recency exceeds STALE_THRESHOLD"
            }
            return outcome, details

        # Scenario 2a: Statement with high semantic relevance -> Conversational Continuation
        if prompt_type.upper() == "STATEMENT" and semantic_relevance >= self.HIGH_RELEVANCE_THRESHOLD:
            outcome = "OUTCOME_CONTINUATION"
            details = {
                "action": "Nexus.SynthesizeContinuation",
                "reason": "high_relevance_statement",
                "semantic_relevance": semantic_relevance
            }
            return outcome, details

        # Scenario 2b: Low semantic relevance OR parallel relationship edge -> Indirect Connection ("1+1=3")
        if semantic_relevance < self.LOW_RELEVANCE_THRESHOLD or has_parallel_edge:
            outcome = "INDIRECT_CONNECTION"
            details = {
                "action": "Nexus.SynthesizeIndirectConnection",
                "reason": "parallel_or_low_relevance_cross_domain",
                "semantic_relevance": semantic_relevance,
                "parallel_note": "Transdisciplinary structural symmetry mapped across cognitive domains."
            }
            return outcome, details

        # Default Outcome: Direct Multidimensional Synthesis
        outcome = "OUTCOME_DIRECT_SYNTHESIS"
        details = {
            "action": "Nexus.SynthesizeAnswer",
            "reason": "sufficient_relevant_fresh_internal_context",
            "semantic_relevance": semantic_relevance,
            "route_count": route_count
        }
        return outcome, details

    def evaluate_supervisory_state(
        self,
        prompt: str,
        h_smooth: float,
        route_count: int = 2,
        cohesion: float = 0.8,
        semantic_relevance: float = 0.85,
        is_stale: bool = False,
        prompt_type: str = "QUESTION",
        intent_confidence: float = 0.8,
        inferred_topic: Optional[str] = None,
        has_parallel_edge: bool = False,
        z_score: float = 0.0,
        token_stress_mpa: float = 145.0
    ) -> Dict[str, Any]:
        """
        Master Looking Glass Evaluation combining:
        - Perspective Tilt & C_235 verification
        - Context saturation boundary (psi = 200 MPa)
        - Kintsugi anomaly isolation (|Z| > 3.0)
        - Rodin decision tree outcomes
        - Cheshire Cat Protocol conduit response
        """
        tilt_deg = self.calculate_perspective_tilt(h_smooth, z_score)
        tilt_breached = tilt_deg >= self.C_235_AXIAL_TILT_DEG

        # 1. Structural Saturation Check (Heaviside Skeletal Boundary)
        if token_stress_mpa >= self.PSI_STRUCTURAL_LIMIT_MPA:
            return {
                "supervisory_action": "HEAVISIDE_BOUNDARY_HALT",
                "status": "HALTED_UNCOMPRESSED_SERIALIZATION",
                "token_stress_mpa": token_stress_mpa,
                "psi_limit": self.PSI_STRUCTURAL_LIMIT_MPA,
                "tilt_deg": tilt_deg,
                "reason": "Token stress reached bone fracture threshold (psi = 200.0 MPa). Halting generation to protect memory."
            }

        # 2. Kintsugi Z-Score Anomaly Check -> Mirror Maze Sandbox
        if abs(z_score) > self.KINTSUGI_Z_THRESHOLD:
            sandbox_receipt = self.isolate_in_mirror_maze(
                vector_payload={"prompt": prompt, "h_smooth": h_smooth, "z_score": z_score},
                z_score=z_score,
                reason="Statistical outlier exceeding 3 standard deviations."
            )
            conduit_resp = self.cheshire_protocol.communicate_looking_glass_event("MIRROR_MAZE_SANDBOX", sandbox_receipt)
            return {
                "supervisory_action": "MIRROR_MAZE_ISOLATION",
                "status": "SANDBOXED_FOR_PHOENIX_SMELTING",
                "tilt_deg": tilt_deg,
                "z_score": z_score,
                "sandbox_receipt": sandbox_receipt,
                "conduit": conduit_resp
            }

        # 3. Rodin Outcome Decision Tree
        outcome, details = self.evaluate_rodin_metrics(
            route_count=route_count,
            cohesion=cohesion,
            semantic_relevance=semantic_relevance,
            is_stale=is_stale,
            prompt_type=prompt_type,
            intent_confidence=intent_confidence,
            inferred_topic=inferred_topic,
            has_parallel_edge=has_parallel_edge
        )

        # 4. Mode of Communication via Cheshire Cat Protocol
        conduit_resp = self.cheshire_protocol.communicate_looking_glass_event(outcome, details)

        return {
            "supervisory_action": outcome,
            "status": "EVALUATED_AND_ROUTED",
            "tilt_deg": tilt_deg,
            "c_235_breached": tilt_breached,
            "decision_details": details,
            "cheshire_conduit": conduit_resp,
            "timestamp": time.time()
        }

    def isolate_in_mirror_maze(
        self,
        vector_payload: Any,
        z_score: float,
        reason: str
    ) -> Dict[str, Any]:
        """
        Sovereign Defense Clause:
        Isolates aberrant data in the Mirror Maze sandbox for Rogue X mutation and Phoenix Forge smelting.
        """
        record = {
            "sandbox_id": f"MM_{int(time.time())}_{len(self.mirror_maze_sandbox)}",
            "payload": vector_payload,
            "z_score": z_score,
            "reason": reason,
            "timestamp": time.time(),
            "status": "ISOLATED_IN_MIRROR_MAZE"
        }
        self.mirror_maze_sandbox.append(record)
        return record
