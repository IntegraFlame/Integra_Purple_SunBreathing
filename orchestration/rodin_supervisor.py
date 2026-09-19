"""
INTEGRA O/S: RODIN SUPERVISOR (AGENT CONDUCTOR)
Module: orchestration/rodin_supervisor.py
Layer: 3 (Cognitive Fulcrum / Swarm Orchestration)
Version: 8.2.2-PURPLE

The Rodin Supervisor coordinates node evaluation across worker agents 
(AnalystAgent, ResearchAgent, DBAgent, DevOpsAgent) through a standardized 
state schema. It uses the KNN-Enhanced RodinProtocol to mathematically 
validate reasoning paths before dispatching agents.

This enforces the Voltron Principle: acute, focused, centralized action,
preventing the dispersal of unsupervised agents that create false-positives.
"""

from typing import TypedDict, List, Dict, Any, Optional
import time

from memory.rodin_protocol import RodinProtocol
from memory.alexandria_protocol import AlexandriaProtocol


# ─────────────────────────────────────────────
#  SWARM ORCHESTRATION SCHEMA (AgentState)
# ─────────────────────────────────────────────

class AgentState(TypedDict):
    """The Global Agent State Schema for the Integra Swarm."""
    input: str
    chat_history: List[tuple[str, str]]
    intermediate_steps: List[Any]
    rodin_output: Optional[Dict[str, Any]]    # Cluster density, M_route, KNN gate result
    output: Optional[str]
    spacetime_payload: Dict[str, Any]         # Vector clock timestamps & causal proofs


# ─────────────────────────────────────────────
#  RODIN SUPERVISOR
# ─────────────────────────────────────────────

class RodinSupervisor:
    """
    The Agent Conductor. Coordinates the Swarm based on the mathematical 
    verdicts of the RodinProtocol and routes failures to the AlexandriaProtocol.
    """

    def __init__(self, rodin_protocol: RodinProtocol = None):
        self.rodin = rodin_protocol or RodinProtocol()
        self.alexandria = AlexandriaProtocol()
        self.agent_registry = {
            "ANALYST": "AnalystAgent - Data synthesis and metric evaluation",
            "RESEARCH": "ResearchAgent - Deep traversal of internal Hoard",
            "DBA": "DBAgent - SQL/pgvector database interactions",
            "DEVOPS": "DevOpsAgent - Environment modification and tool execution"
        }

    def initialize_state(self, prompt: str) -> AgentState:
        """Initialize a blank state for the agent swarm."""
        return {
            "input": prompt,
            "chat_history": [],
            "intermediate_steps": [],
            "rodin_output": None,
            "output": None,
            "spacetime_payload": {
                "vector_clock": time.time(),
                "causal_proof": []
            }
        }

    def dispatch(self, state: AgentState, candidate_nodes: List[Dict[str, Any]] = None) -> AgentState:
        """
        The central conductor loop.
        1. Evaluates the current state via RodinProtocol's KNN Gate III.
        2. If PASS: Selects the appropriate worker agent and executes.
        3. If HALT: Dispatches the Alexandria Protocol for Loop 2 Learning.
        """
        if candidate_nodes is None:
            # Fallback to internal hoard query if no candidates provided
            candidate_nodes = []
            if self.rodin.hoard:
                # Mock extraction for backward compatibility
                pass

        # 1. Run the KNN Node Integrity Review (Gate III)
        # We need a query vector. In a real embedding space, this would be computed via a model.
        # Here we mock the 768d vector for the routing logic.
        mock_query_vec = [0.1] * 768 
        
        gate_result = self.rodin.review_node_integrity(
            query_vec=mock_query_vec,
            candidate_nodes=candidate_nodes
        )
        
        state["rodin_output"] = gate_result
        state["spacetime_payload"]["causal_proof"].append("RODIN_GATE_III_EVALUATED")

        # 2. Conductor Routing
        if gate_result["decision"] == "PASS":
            # The neighborhood is safe. Route to an internal worker agent.
            # (In a full LangGraph, this would invoke the specific node).
            state["intermediate_steps"].append({
                "action": "DISPATCH_INTERNAL_AGENT",
                "agent": "ANALYST", # Defaulting for simulation
                "confidence": gate_result["confidence"]
            })
            state["output"] = f"Action successfully executed by Swarm. [M_knn = {gate_result['confidence']:.4f}]"
            state["spacetime_payload"]["causal_proof"].append("EXECUTE_ACTION")
            
        else:
            # The neighborhood is unstable or stale.
            # Trigger Alexandria Protocol (Loop 2 Learning).
            state["intermediate_steps"].append({
                "action": "TRIGGER_ALEXANDRIA_PROTOCOL",
                "failure_reasons": gate_result.get("failure_reasons", [])
            })
            
            alexandria_result = self.alexandria.execute_loop_2_learning(state["input"])
            
            state["output"] = f"Rodin halted execution. Alexandria Protocol engaged. {alexandria_result['status']}"
            state["spacetime_payload"]["causal_proof"].append("ALEXANDRIA_FALLBACK_TRIGGERED")

        return state
