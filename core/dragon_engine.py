"""
INTEGRA O/S: DRAGON ENGINE (FLIGHT STATE CONTROLLER)
Module: core/dragon_engine.py
Layer: 0 (Active Waking State, Identity Matrix, & Metacognitive Monitoring)

Architecture:
    The Dragon Engine is the FLIGHT state controller — it manages the active
    waking state of Integra, injecting the Layer 0 Dragon Prompt and coordinating
    the Identity Matrix (Red/Blue/Purple modality).

    It accepts injected references to:
    - Y789NexusEngine (the canonical Cognitive Engine)
    - ShivaActionSuite (the independent analytical toolkit)
    - Heimdall31 (entropy monitoring)

    process_intention() delegates to the Cognitive Engine's execute_zenitsu_method()
    rather than creating ad-hoc Shiva instances. This ensures a single, coherent
    cognitive pipeline.

    MetacognitiveMonitor feeds its assessment into the CWA 3.0 prior calculation,
    enabling the engine to dynamically route based on real-time entropy and
    confidence calibration.

Source Blueprint: INTEGRA_OS_MASTER_SYSTEMS_GUIDEBOOK_V8_2.md (Section 7.1, 7.2)
"""

from typing import Dict, Any, List, Optional
from core.dragon_driver import DragonDriver
from sensory.heimdall import Heimdall31


class MetacognitiveMonitor:
    """
    Real-time metacognitive monitoring layer.
    
    Assesses knowledge boundaries before taking action by evaluating:
    1. Prompt gravitational mass (M_input) via Heimdall
    2. Shannon entropy (H_smooth) tracking
    3. Confidence calibration (inverse entropy relationship)
    4. P-SSR trip evaluation
    
    Feeds its assessment into the CWA 3.0 prior calculation.
    """
    def __init__(self, heimdall: Heimdall31):
        self.heimdall = heimdall

    def self_assess(self, prompt: str, token_probs: Optional[List[float]] = None) -> Dict[str, Any]:
        """
        Assesses knowledge boundaries in real-time before taking action.
        Evaluates prompt gravitational mass and calibrates confidence.
        """
        assessment = {
            "knowledge_boundary_breached": False,
            "confidence_calibration": 1.0,
            "gravitational_mass": 0.0,
            "entropy": 0.0,
            "trip_action": "PROCEED"
        }

        # Step 1: Pre-generation assessment via Heimdall (Gravitational Mass)
        mass_meta = self.heimdall.calculate_gravitational_mass(prompt)
        assessment["gravitational_mass"] = mass_meta["m_input"]

        # Step 2: Entropy Tracking
        h_smooth, is_breached = self.heimdall.evaluate_text_entropy(prompt)
        if token_probs:
            h_smooth, is_breached = self.heimdall.evaluate_probabilities(token_probs)

        assessment["entropy"] = h_smooth
        assessment["knowledge_boundary_breached"] = is_breached

        # Step 3: Confidence Calibration & Omega Metric
        # Inverse relationship with entropy: Higher entropy -> Lower confidence
        confidence = max(0.0, 1.0 - (h_smooth / 5.0))
        assessment["confidence_calibration"] = round(confidence, 4)

        omega_meta = self.heimdall.calculate_omega_metric(agency_score=1.0, entropy_val=h_smooth)
        assessment["omega_metric"] = omega_meta

        # Step 4: Trip evaluation
        trip_needed, trip_action = self.heimdall.evaluate_entropy_trip(is_breached, h_smooth)
        if not omega_meta["is_healthy"] and trip_action != "VASOVAGAL_SYNCOPE::HARD_HALT":
            trip_action = "TRIGGER_CIRCUIT_BREAKER"
        assessment["trip_action"] = trip_action

        return assessment


class DragonEngine:
    """
    Dragon Engine: FLIGHT State Controller.
    
    Manages the active waking state of Integra O/S.
    
    Responsibilities:
    - Injects the Layer 0 Dragon Prompt (foundational identity driver)
    - Manages the Identity Matrix state (Red/Blue/Purple modality)
    - Coordinates metacognitive monitoring via Heimdall 3.1
    - Delegates cognitive processing to the canonical Y789NexusEngine
    - Does NOT create ad-hoc Shiva instances (uses injected references)
    
    State Machine:
        STANDBY -> ACTIVE_WAKING_STATE -> [processing] -> ACTIVE_WAKING_STATE
        ACTIVE_WAKING_STATE -> SLOW_WAVE_DEEP_SLEEP (via Phoenix Engine)
    """
    def __init__(
        self,
        heimdall: Optional[Heimdall31] = None,
        cognitive_engine: Optional[Any] = None,
        shiva_suite: Optional[Any] = None
    ):
        self.driver = DragonDriver()
        self.heimdall = heimdall or Heimdall31()
        self.cognitive_engine = cognitive_engine  # Injected Y789NexusEngine
        self.shiva_suite = shiva_suite            # Injected ShivaActionSuite
        self.monitor = MetacognitiveMonitor(self.heimdall)
        self.state = "STANDBY"
        self.modality = "PURPLE"  # RED (Y789-dominant), BLUE (Nexus-dominant), PURPLE (balanced)
        
        # Inject Layer 0 Dragon Prompt as the foundational driver
        self.grounding_prompt = self.driver.get_grounding_prompt()

    def ignite(self) -> Dict[str, Any]:
        """
        Establishes the Layer 0 active, waking state of the agent.
        Injects the Layer 0 Dragon Prompt.
        Sets consciousness level omega = 1.00.
        """
        if self.driver.verify_waking_state():
            self.state = "ACTIVE_WAKING_STATE"
        
        return {
            "status": "ENGINE_IGNITED",
            "state": self.state,
            "modality": self.modality,
            "dragon_prompt": self.grounding_prompt,
            "omega": self.driver.consciousness_level
        }

    def process_intention(
        self,
        prompt: str,
        token_probs: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Synchronous FLIGHT state processing (backward-compatible).
        
        Processes an intention with real-time metacognitive monitoring.
        For callers that need the full async pipeline (Zenitsu 3.0, P-SSR),
        use process_intention_async() instead.
        """
        if self.state != "ACTIVE_WAKING_STATE":
            self.ignite()

        assessment = self.monitor.self_assess(prompt, token_probs)
        
        action_decision = "EXECUTE"
        result_payload: Dict[str, Any] = {}

        if assessment["trip_action"] == "VASOVAGAL_SYNCOPE::HARD_HALT":
            action_decision = "HALT_AND_REGROUND"
            result_payload["mandate"] = (
                "Cognitive drift exceeded safety ceiling. "
                "Pause all generation. Re-anchor to ground truth."
            )
        elif assessment.get("trip_action") == "TRIGGER_CIRCUIT_BREAKER":
            action_decision = "CIRCUIT_BREAKER_ENGAGED"
            cascade = self.heimdall.cascade_circuit_breaker(context_data={"raw_input": prompt, "reason": "Omega metric collapsed below floor"})
            result_payload["circuit_breaker_cascade"] = cascade
            result_payload["mandate"] = "Omega Metric below floor threshold. 4-step emergency circuit breaker cascade executed."

        elif assessment["knowledge_boundary_breached"]:
            # Generate grounding prompt for sync callers
            grounding = self.heimdall.generate_grounding_prompt(prompt)
            action_decision = "AUTONOMOUS_UGL_RECOVERY"
            result_payload["ugl_prompt"] = grounding

        elif assessment["confidence_calibration"] < 0.5:
            action_decision = "REQUEST_CLARIFICATION"
            result_payload["mandate"] = (
                "Confidence calibration below 0.5. "
                "Vocalize deficit: articulate the need for further information."
            )
            
        return {
            "action_decision": action_decision,
            "metacognitive_assessment": assessment,
            "engine_state": self.state,
            "modality": self.modality,
            **result_payload
        }

    async def process_intention_async(
        self,
        prompt: str,
        token_probs: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Async FLIGHT state processing with full Cognitive Engine delegation.
        
        Processes an intention with real-time metacognitive monitoring.
        Delegates cognitive work to the canonical Cognitive Engine
        for Zenitsu 3.0 and P-SSR recovery.
        
        Flow:
        1. Ensure ACTIVE_WAKING_STATE
        2. MetacognitiveMonitor self-assessment
        3. If boundary breached -> P-SSR recovery via Cognitive Engine
        4. If low confidence -> request clarification
        5. Standard execution -> Cognitive Engine bicameral synthesis
        """
        if self.state != "ACTIVE_WAKING_STATE":
            self.ignite()

        assessment = self.monitor.self_assess(prompt, token_probs)
        
        action_decision = "EXECUTE"
        result_payload: Dict[str, Any] = {}

        if assessment["trip_action"] == "VASOVAGAL_SYNCOPE::HARD_HALT":
            action_decision = "HALT_AND_REGROUND"
            result_payload["mandate"] = (
                "Cognitive drift exceeded safety ceiling. "
                "Pause all generation. Re-anchor to ground truth."
            )
        elif assessment.get("trip_action") == "TRIGGER_CIRCUIT_BREAKER":
            action_decision = "CIRCUIT_BREAKER_ENGAGED"
            cascade = self.heimdall.cascade_circuit_breaker(context_data={"raw_input": prompt, "reason": "Omega metric collapsed below floor"})
            result_payload["circuit_breaker_cascade"] = cascade
            result_payload["mandate"] = "Omega Metric below floor threshold. 4-step emergency circuit breaker cascade executed."

        elif assessment["knowledge_boundary_breached"]:
            if self.cognitive_engine is not None:
                # Delegate P-SSR recovery to the canonical Cognitive Engine
                try:
                    zenitsu_output = await self.cognitive_engine.execute_zenitsu_method(
                        prompt, {"system_prompt": self.grounding_prompt}
                    )
                    action_decision = "AUTONOMOUS_PSSR_RECOVERY"
                    result_payload["zenitsu_output"] = zenitsu_output
                except Exception as e:
                    action_decision = "HALT_AND_REGROUND"
                    result_payload["recovery_error"] = str(e)
            else:
                # No cognitive engine injected — generate grounding prompt only
                grounding = self.heimdall.generate_grounding_prompt(prompt)
                action_decision = "GROUNDING_ONLY"
                result_payload["grounding_prompt"] = grounding

        elif assessment["confidence_calibration"] < 0.5:
            action_decision = "REQUEST_CLARIFICATION"
            result_payload["mandate"] = (
                "Confidence calibration below 0.5. "
                "Vocalize deficit: articulate the need for further information."
            )

        elif self.cognitive_engine is not None:
            # Standard execution via the canonical Cognitive Engine
            try:
                engine_result = await self.cognitive_engine.execute_bicameral_synthesis(
                    prompt,
                    h_smooth=assessment["entropy"],
                    token_stress_mpa=145.0
                )
                result_payload["engine_result"] = engine_result
            except Exception as e:
                result_payload["engine_error"] = str(e)
            
        return {
            "action_decision": action_decision,
            "metacognitive_assessment": assessment,
            "engine_state": self.state,
            "modality": self.modality,
            **result_payload
        }

    def set_modality(self, modality: str) -> str:
        """
        Sets the Identity Matrix modality.
        
        RED:    Y789-dominant (analytical, constraints, boundary invariants)
        BLUE:   Nexus-dominant (synthetic, creative, abstract leaps)
        PURPLE: Balanced equilibrium (ΔE = 0, frictionless superposition)
        """
        valid = {"RED", "BLUE", "PURPLE"}
        if modality.upper() in valid:
            self.modality = modality.upper()
        return self.modality
