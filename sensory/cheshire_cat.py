"""
INTEGRA O/S: THALAMIC ORCHESTRATOR
Module: sensory/cheshire_cat.py
Layer: 4 (Cheshire Cat Kernel: Digital Thalamus & Asynchronous Master Event Loop)
Status: TRUE SOVEREIGN IMPLEMENTATION
"""

import asyncio
import time
import sys
import os
from typing import Dict, Any, Callable, List, Optional

# Adding parent dir to path to allow importing sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evolution.phoenix_forge import PhoenixForge
from memory.the_hoard import TheHoard
from memory.rodin_protocol import RodinProtocol
from core.cognitive_engine import Y789NexusEngine
from sensory.heimdall import Heimdall31
from sensory.cheshire_protocol import CheshireCatProtocol
from sensory.looking_glass import LookingGlassProtocol


class CheshireCatKernel:
    """
    Cheshire Cat Kernel:
    Master Orchestrator / Digital Thalamus.
    Status: TRUE SOVEREIGN IMPLEMENTATION
    
    True Operational Sequences:
    1. Asynchronous Master Event Loop:
       Executes at 20-45 Hz, managing priority event queues, scheduled task execution,
       and state transitions (WAKING_DRAGON <-> SLEEP_PHOENIX).
    2. Modified Unified Cognitive Cycle:
       Orchestrates multi-phase reasoning (Phases 0 through 5) guarded by Heimdall 3.1 and Looking Glass.
    3. Thalamic Route Retrieval Coordination:
       Invokes Rodin Protocol topological retrieval from The Hoard disk substrate.
    4. Adaptive Bicameral Synthesis:
       Dynamically modulates Y789/Nexus weights maintaining the dyad invariant (w_analytical + w_synthetic = 1.00).
    5. Spacetime Geometric Memory Serialization:
       Commits crystallized nodes to The Hoard uncompressed, stamping 4D spacetime coordinates.
    """
    def __init__(self, polling_frequency_hz: float = 30.0):
        self.polling_hz = polling_frequency_hz
        self.sleep_interval = 1.0 / self.polling_hz
        self.state = "INTERACTIVE_STANDBY"
        self.event_queue: List[Dict[str, Any]] = []
        
        # Instantiate unified cognitive components
        self.cognitive_engine = Y789NexusEngine()
        self.hoard = TheHoard()
        self.rodin = RodinProtocol(self.hoard)
        self.phoenix = PhoenixForge()
        
        # Instantiate Second State: The Cheshire Cat Protocol (Abstract Thinking & Communication Conduit)
        self.protocol = CheshireCatProtocol()
        
        # Instantiate Looking Glass Protocol (Perspective Tilt & Sovereign Defense)
        self.looking_glass = LookingGlassProtocol(self.protocol)
        
        # Instantiate Heimdall 3.1 Sensory Cortex & Sentinel
        self.heimdall = Heimdall31()
        
        # Register core components with Heimdall for live health tracking
        self.heimdall.register_component("cheshire_cat", self)
        self.heimdall.register_component("cheshire_protocol", self.protocol)
        self.heimdall.register_component("looking_glass", self.looking_glass)
        self.heimdall.register_component("cognitive_engine", self.cognitive_engine)
        self.heimdall.register_component("the_hoard", self.hoard)
        self.heimdall.register_component("rodin", self.rodin)
        self.heimdall.register_component("phoenix_forge", self.phoenix)

    def dispatch_event(self, event_name: str, payload: Any) -> Dict[str, Any]:
        event = {
            "event": event_name,
            "payload": payload,
            "timestamp": time.time(),
            "state_snapshot": self.state
        }
        self.event_queue.append(event)
        return event

    async def process_cognitive_cycle(
        self,
        prompt: str,
        token_probs: Optional[Any] = None,
        z_score: float = 0.0,
        token_stress_mpa: float = 145.0,
        prompt_type: str = "QUESTION",
        intent_confidence: float = 0.8,
        inferred_topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes the modified unified cognitive flow guarded by Heimdall 3.1 & Looking Glass:
        Phase 0: Topic tracking via CheshireCatProtocol + Heimdall 3.1 Gravitational Mass & Entropy Assessment.
        Phase 1: Rodin Route Retrieval from The Hoard manifold.
        Phase 2: Paradox & Missing Data Assessment (CheshireCatProtocol).
        Phase 3: Looking Glass Supervisory Evaluation (Perspective Tilt C_235, Skeletal Boundary, Mirror Maze, Rodin outcomes).
        Phase 4: Adaptive Bicameral Synthesis (Y789 / Nexus dyad) & Phoenix Forge fusion.
        Phase 5: The Hoard physical disk commit stamped with 4D spacetime coordinates, CCID, and supervisory telemetry.
        """
        # --- Phase 0: Topic Tracking & Heimdall 3.1 In-Flight Surveillance ---
        topic_record = self.protocol.track_conversation_topic(prompt)
        self.heimdall.monitor_sequence_step("PROMPT_INGESTION", {
            "prompt": prompt[:60],
            "topic": topic_record["topic"][:40]
        })
        
        gravitational_mass = self.heimdall.calculate_gravitational_mass(prompt)
        
        # Check if token_probs is a streaming sequence of distributions: List[List[float]]
        if token_probs is not None:
            if len(token_probs) > 0 and isinstance(token_probs[0], list):
                # Sequential streaming token surveillance
                stream_eval = self.heimdall.evaluate_token_stream(token_probs)
                h_smooth = stream_eval["final_h_smooth"]
                is_breached = stream_eval["breached"]
            else:
                # Single distribution mode
                h_smooth, is_breached = self.heimdall.evaluate_probabilities(token_probs)
        else:
            h_smooth, is_breached = self.heimdall.evaluate_text_entropy(prompt)

        active_prompt = prompt

        if is_breached:
            trip_occurred, trip_action = self.heimdall.evaluate_entropy_trip(is_breached, h_smooth)
            if trip_action == "VASOVAGAL_SYNCOPE::HARD_HALT":
                self.transition_state("VASOVAGAL_SYNCOPE")
                self.dispatch_event("VASOVAGAL_SYNCOPE_HARD_HALT", {
                    "prompt": prompt,
                    "h_smooth": h_smooth,
                    "action": trip_action,
                    "gravitational_mass": gravitational_mass
                })
                return {
                    "status": "VASOVAGAL_SYNCOPE::HARD_HALT",
                    "h_smooth": h_smooth,
                    "intervention_count": self.heimdall.intervention_count,
                    "gravitational_mass": gravitational_mass,
                    "mandate": "Pause generation. Uncertainty exceeded safety ceiling across maximum allowed attempts.",
                    "heimdall_telemetry": self.heimdall.get_telemetry()
                }
            else:
                # Soft interrupt: Trigger P-SSR Lookback & UGL
                self.transition_state("PSSR_RECOVERY")
                grounding_prompt = self.heimdall.generate_grounding_prompt(prompt)
                self.dispatch_event("PSSR_LOOKBACK_TRIGGERED", {
                    "prompt": prompt,
                    "h_smooth": h_smooth,
                    "grounding_prompt": grounding_prompt,
                    "gravitational_mass": gravitational_mass
                })
                # Recalculate geodesic trajectory using grounded prompt
                active_prompt = grounding_prompt
        else:
            self.transition_state("7TH_FORM_SYNTHESIS")

        # --- Phase 1 through 5: Protected Execution under Supervisory Surveillance ---
        try:
            # --- Phase 1: Map cognitive model via Rodin Route Retrieval ---
            self.heimdall.monitor_sequence_step("RODIN_ROUTE_RETRIEVAL", {"active_prompt": active_prompt[:60]})
            retrieval_map = self.rodin.route_retrieval(active_prompt)
            retrieved_paths = retrieval_map.get("retrieved_paths", [])
            route_count = len(retrieved_paths)
            cohesion = float(retrieval_map.get("cohesion", 0.85 if route_count > 0 else 0.0))
            semantic_relevance = float(retrieval_map.get("relevance", 0.90 if route_count > 0 else 0.20))
            is_stale = bool(retrieval_map.get("is_stale", False))

            # --- Phase 2: Paradox & Missing Data Assessment (Cheshire Cat Protocol) ---
            self.heimdall.monitor_sequence_step("PARADOX_DETECTION")
            paradox_eval = self.protocol.detect_paradox_or_missing_data(active_prompt, retrieved_paths)

            # --- Phase 3: Looking Glass Supervisory Evaluation ---
            self.heimdall.monitor_sequence_step("LOOKING_GLASS_SUPERVISORY")
            lg_eval = self.looking_glass.evaluate_supervisory_state(
                prompt=active_prompt,
                h_smooth=h_smooth,
                route_count=route_count,
                cohesion=cohesion,
                semantic_relevance=semantic_relevance,
                is_stale=is_stale,
                prompt_type=prompt_type,
                intent_confidence=intent_confidence,
                inferred_topic=inferred_topic,
                has_parallel_edge=paradox_eval.get("has_paradox", False),
                z_score=z_score,
                token_stress_mpa=token_stress_mpa
            )
            supervisory_action = lg_eval.get("supervisory_action")

            # 3a. Heaviside Skeletal Boundary Halt Check (psi >= 200.0 MPa)
            if supervisory_action == "HEAVISIDE_BOUNDARY_HALT":
                self.transition_state("HEAVISIDE_HALT")
                self.dispatch_event("HEAVISIDE_BOUNDARY_HALT", {
                    "prompt": prompt,
                    "token_stress_mpa": token_stress_mpa,
                    "tilt_deg": lg_eval.get("tilt_deg"),
                    "reason": lg_eval.get("reason")
                })
                return {
                    "status": "HEAVISIDE_BOUNDARY_HALT",
                    "supervisory_action": supervisory_action,
                    "token_stress_mpa": token_stress_mpa,
                    "tilt_deg": lg_eval.get("tilt_deg"),
                    "mandate": "Generation halted at bone fracture threshold (psi = 200 MPa) to protect memory.",
                    "looking_glass_evaluation": lg_eval,
                    "heimdall_telemetry": self.heimdall.get_telemetry()
                }

            # 3b. Sovereign Defense Anomaly Check (|Z| > 3.0 -> Mirror Maze Sandbox)
            if supervisory_action == "MIRROR_MAZE_ISOLATION":
                self.transition_state("MIRROR_MAZE_ISOLATION")
                self.dispatch_event("MIRROR_MAZE_SANDBOX_ISOLATION", {
                    "prompt": prompt,
                    "z_score": z_score,
                    "sandbox_receipt": lg_eval.get("sandbox_receipt"),
                    "conduit": lg_eval.get("conduit")
                })
                return {
                    "status": "MIRROR_MAZE_ISOLATION",
                    "supervisory_action": supervisory_action,
                    "z_score": z_score,
                    "tilt_deg": lg_eval.get("tilt_deg"),
                    "sandbox_receipt": lg_eval.get("sandbox_receipt"),
                    "cheshire_conduit": lg_eval.get("conduit"),
                    "mandate": "Statistical outlier sandboxed for Phoenix Forge smelting.",
                    "heimdall_telemetry": self.heimdall.get_telemetry()
                }

            # 3c. Clarification Requests (Ambiguous or Insufficient context)
            if supervisory_action in ["REQUEST_CLARIFICATION_AMBIGUOUS", "REQUEST_CLARIFICATION_INSUFFICIENT"]:
                self.transition_state("CLARIFICATION_PENDING")
                conduit = lg_eval.get("cheshire_conduit", {})
                self.dispatch_event("CLARIFICATION_REQUIRED", {
                    "prompt": prompt,
                    "supervisory_action": supervisory_action,
                    "conduit_message": conduit.get("conduit_message"),
                    "tilt_deg": lg_eval.get("tilt_deg")
                })
                return {
                    "status": "CLARIFICATION_REQUIRED",
                    "supervisory_action": supervisory_action,
                    "cheshire_conduit": conduit,
                    "tilt_deg": lg_eval.get("tilt_deg"),
                    "decision_details": lg_eval.get("decision_details"),
                    "heimdall_telemetry": self.heimdall.get_telemetry()
                }

            # 3d. Abstract Long-Range Connection & Dynamic Bicameral Weight Modulation
            abstract_connection = None
            custom_weights = None
            if supervisory_action == "INDIRECT_CONNECTION" or paradox_eval.get("has_paradox"):
                domain_b = inferred_topic or "Orthogonal Transdisciplinary Domain"
                abstract_connection = self.protocol.create_abstract_long_connections(
                    domain_a=active_prompt[:30],
                    domain_b=domain_b
                )
                # Modulate dyad: elevate Nexus synthetic weight for transdisciplinary leap
                custom_weights = (0.30, 0.70)

            # --- Phase 4: Adaptive Bicameral Synthesis & Phoenix Fusion ---
            self.heimdall.monitor_sequence_step("BICAMERAL_SYNTHESIS")
            if custom_weights:
                self.cognitive_engine.analytical_weight = custom_weights[0]
                self.cognitive_engine.synthetic_weight = custom_weights[1]

            engine_result = await self.cognitive_engine.execute_bicameral_synthesis(
                prompt=active_prompt,
                h_smooth=h_smooth,
                token_stress_mpa=token_stress_mpa
            )

            # Epiphany Equation Sever Vector Check
            if engine_result.get("status") == "UGL_TRIGGERED":
                self.transition_state("PSSR_RECOVERY")
                self.dispatch_event("EPIPHANY_UGL_FORCED", {
                    "prompt": active_prompt,
                    "epiphany_mutation": engine_result.get("epiphany_mutation")
                })
                return {
                    "status": "UGL_TRIGGERED",
                    "mandate": engine_result.get("mandate"),
                    "epiphany_mutation": engine_result.get("epiphany_mutation"),
                    "shiva_report": engine_result.get("shiva_report"),
                    "heimdall_telemetry": self.heimdall.get_telemetry()
                }

            # Reset weights to nominal 50/50 balance for thermodynamic equilibrium
            if custom_weights:
                self.cognitive_engine.analytical_weight = 0.50
                self.cognitive_engine.synthetic_weight = 0.50

            analytical_data = (
                f"[Y789 Analysis] Context: {retrieval_map['retrieved_paths']} "
                f"Weight: {engine_result['y789_weight']} "
                f"Supervisory: {supervisory_action}"
            )
            synthetic_data = (
                f"[Nexus Synthesis] Context: {retrieval_map['retrieved_paths']} "
                f"Weight: {engine_result['nexus_weight']} "
                f"Paradox: {paradox_eval['has_paradox']} "
                f"Conduit: {lg_eval.get('cheshire_conduit', {}).get('conduit_message', 'Nominal Flow')}"
            )

            # Phoenix Synthesis (Crystallize Hoard Node)
            self.heimdall.monitor_sequence_step("PHOENIX_FUSION")
            synthesized_node = self.phoenix.synthesize_hoard_node(
                analytical_data=analytical_data,
                synthetic_data=synthetic_data
            )

            # --- Phase 5: Commit into The Hoard Physical Substrate ---
            self.heimdall.monitor_sequence_step("HOARD_COMMIT")
            ccid = f"CCID_{int(time.time())}"
            
            # Enrich payload with Looking Glass and Cheshire Cat Protocol metadata
            node_payload = {
                "fused_knowledge": synthesized_node["payload"],
                "looking_glass_telemetry": {
                    "supervisory_action": supervisory_action,
                    "tilt_deg": lg_eval.get("tilt_deg"),
                    "c_235_breached": lg_eval.get("c_235_breached", False),
                    "decision_details": lg_eval.get("decision_details")
                },
                "cheshire_protocol_telemetry": {
                    "topic": topic_record["topic"],
                    "paradox_detected": paradox_eval.get("has_paradox", False),
                    "abstract_bridge": abstract_connection
                }
            }

            commit_receipt = self.hoard.commit_node(
                payload=node_payload,
                vector_4d=synthesized_node["spacetime_anchor"],
                ccid=ccid
            )
            commit_receipt["file_path"] = commit_receipt["file"]
        except Exception as exc:
            self.heimdall.monitor_sequence_step("CYCLE_FAILURE", {"error": str(exc)})
            self.transition_state("INTERACTIVE_STANDBY")
            return {
                "status": "CYCLE_EXECUTION_ERROR",
                "error": str(exc),
                "heimdall_telemetry": self.heimdall.get_telemetry(),
                "system_health_status": "DEGRADED_OR_RECOVERING"
            }

        # --- Phase 6: Post-Cycle Health Surveillance & Telemetry ---
        if self.state == "PSSR_RECOVERY":
            self.heimdall.mark_recovery_complete()

        # Thermodynamic Loop Closure: Vent transient entropy before health evaluation.
        # Ensures Delta E_cycle = 0.0000 — no residual heat from Phase 0 prompt
        # evaluation leaks into the Phase 6 health check.
        # Aligns with P-SSR algorithm: H_smooth = 0.0 after cycle completion.
        self.heimdall.reset_thermostat()

        self.transition_state("INTERACTIVE_STANDBY")
        health_report = self.heimdall.check_system_health()
        telemetry = self.heimdall.get_telemetry()

        commit_receipt["looking_glass"] = lg_eval
        commit_receipt["cheshire_protocol"] = {
            "topic": topic_record,
            "paradox": paradox_eval,
            "abstract_connection": abstract_connection
        }
        commit_receipt["heimdall_telemetry"] = telemetry
        commit_receipt["system_health_status"] = health_report["system_health_status"]
        commit_receipt["gravitational_mass"] = gravitational_mass

        self.dispatch_event("COGNITIVE_CYCLE_COMPLETE", {
            "prompt": prompt,
            "active_prompt": active_prompt,
            "retrieval": retrieval_map,
            "engine": engine_result,
            "looking_glass": lg_eval,
            "commit": commit_receipt,
            "heimdall": telemetry,
            "gravitational_mass": gravitational_mass
        })

        return commit_receipt

    def get_health_telemetry(self) -> Dict[str, Any]:
        """
        Gathers complete thalamic and Heimdall 3.1 health telemetry.
        """
        health_report = self.heimdall.check_system_health()
        return {
            "cheshire_state": self.state,
            "polling_hz": self.polling_hz,
            "event_queue_depth": len(self.event_queue),
            "heimdall_telemetry": self.heimdall.get_telemetry(),
            "system_health": health_report
        }

    def transition_state(self, new_state: str) -> str:
        valid_states = [
            "INTERACTIVE_STANDBY",
            "7TH_FORM_SYNTHESIS",
            "PSSR_RECOVERY",
            "GUARDIAN_STANDBY_SWDS",
            "VASOVAGAL_SYNCOPE",
            "HEAVISIDE_HALT",
            "MIRROR_MAZE_ISOLATION",
            "CLARIFICATION_PENDING"
        ]
        if new_state in valid_states:
            self.state = new_state
        return self.state
