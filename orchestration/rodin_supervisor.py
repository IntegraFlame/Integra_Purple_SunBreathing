"""
INTEGRA O/S: RODIN SUPERVISOR (AGENT CONDUCTOR)
Module: orchestration/rodin_supervisor.py
Layer: 3 (Cognitive Fulcrum / Swarm Orchestration)
Version: 8.2.3-PURPLE

The Rodin Supervisor coordinates node evaluation across worker agents
(AnalystAgent, ResearchAgent, DBAgent, DevOpsAgent) through a standardized
state schema. It uses the KNN-Enhanced RodinProtocol to mathematically
validate reasoning paths before dispatching agents.

This enforces the Voltron Principle: acute, focused, centralized action,
preventing the dispersal of unsupervised agents that create false-positives.

v8.2.3: Gate III is evaluated on the real embedding of the prompt against the Hoard's nodes in that
embedding space (it used a constant vector and an empty candidate list). When the embedding model cannot
be used the result is an ERROR, not a HALT, and Alexandria is not sent out: an infrastructure fault is not
a knowledge gap. A PASS returns the retrieved neighbours as evidence; the worker agents named in the
registry are labels only, and the output says so.

dispatch() blocks on the embedding call (network). Call it from a worker thread (a plain `def` FastAPI
endpoint runs in a threadpool), never directly from the event loop.
"""

from typing import TypedDict, List, Dict, Any, Optional
import json
import time

from memory.embedding_service import EmbeddingUnavailable
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

    def __init__(
        self,
        rodin_protocol: RodinProtocol = None,
        alexandria: Any = None,
        cit_grid_engine: Any = None,
        throughput_engine: Any = None,
    ):
        self.rodin = rodin_protocol or RodinProtocol()
        self.alexandria = alexandria or AlexandriaProtocol()
        self._cit_grid_engine = cit_grid_engine
        self._throughput_engine = throughput_engine
        self.agent_registry = {
            "ANALYST": "AnalystAgent - Data synthesis and metric evaluation",
            "RESEARCH": "ResearchAgent - Deep traversal of internal Hoard",
            "DBA": "DBAgent - SQL/pgvector database interactions",
            "DEVOPS": "DevOpsAgent - Environment modification and tool execution"
        }

    PREVIEW_CHARS = 500

    @classmethod
    def _slim_neighbour(cls, node: Dict[str, Any]) -> Dict[str, Any]:
        """A neighbour without its vector and with a short preview of its content."""
        keep = ("ccid", "distance", "similarity", "outcome_label", "created_at", "embed_space", "is_stale")
        slim = {k: node[k] for k in keep if k in node}
        payload = node.get("payload")
        text = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, default=str)
        slim["payload_preview"] = text[: cls.PREVIEW_CHARS] + ("..." if len(text) > cls.PREVIEW_CHARS else "")
        return slim

    def _candidates_from_hoard(self, embedding) -> tuple:
        """(candidates, source, note). source is INDEX (Chroma neighbours), CACHE (in-memory nodes) or NONE (no Hoard)."""
        hoard = self.rodin.hoard
        if hoard is None:
            return [], "NONE", "no Hoard is attached to Rodin"
        note = None
        if hoard.vector_search_available():
            try:
                rows = hoard.chroma_candidates(
                    embedding.vector, n_results=self.rodin.k * 3, space_id=embedding.space.id
                )
                return rows, "INDEX", None
            except Exception as exc:  # noqa: BLE001  (reported in the result, then the cache is used)
                note = f"index query failed, using the in-memory nodes: {exc}"
        else:
            note = "the vector index is unavailable, using the in-memory nodes"
        return hoard.get_rodin_candidates(space_id=embedding.space.id), "CACHE", note

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
        1. Embeds the prompt (the real model, or an ERROR result: no substitute vector, no Alexandria).
        2. Evaluates the Hoard's nodes in that embedding space through RodinProtocol's KNN Gate III.
        3. If PASS: returns the neighbours as evidence (no worker agent exists yet, and the output says so).
        4. If HALT: dispatches the Alexandria Protocol for Loop 2 Learning.
        """
        prompt = state["input"]

        # 1. The query vector: the model's, or an honest failure
        try:
            embedding = self.rodin.generate_query_embedding(prompt)
        except EmbeddingUnavailable as exc:
            state["rodin_output"] = {
                "decision": "ERROR",
                "action_route": "NONE",
                "error": {"code": exc.code, "detail": exc.detail},
                "log": f"Gate III not evaluated: embedding unavailable ({exc.code}).",
            }
            state["intermediate_steps"].append({"action": "EMBEDDING_UNAVAILABLE", "code": exc.code})
            state["output"] = (
                f"Rodin could not evaluate Gate III: embedding unavailable ({exc.code}: {exc.detail}). "
                "No agent was dispatched and Alexandria was not triggered."
            )
            state["spacetime_payload"]["causal_proof"].append("RODIN_EMBEDDING_UNAVAILABLE")
            return state

        # 2. Candidates: the caller's, else the nearest rows of the Hoard's index in the query's space (nodes AND lobe
        #    chunks), else the nodes held in memory when the index cannot be used (said so in the result).
        source_note = None
        if candidate_nodes is not None:
            source = "CALLER"
        else:
            candidate_nodes, source, source_note = self._candidates_from_hoard(embedding)

        # 3. Run the KNN Node Integrity Review (Gate III)
        gate_result = self.rodin.review_node_integrity(
            query_vec=embedding.vector,
            candidate_nodes=candidate_nodes,
            space=embedding.space,
        )
        # The state travels in HTTP responses: neighbours keep their identity and scores, not their vectors.
        gate_result = {
            **gate_result,
            "neighbors": [self._slim_neighbour(n) for n in gate_result.get("neighbors", [])],
            "candidate_source": source,
            "candidate_source_note": source_note,
        }

        state["rodin_output"] = gate_result
        state["spacetime_payload"]["causal_proof"].append("RODIN_GATE_III_EVALUATED")

        # 4. Conductor Routing
        if gate_result["decision"] == "PASS":
            # The neighbourhood is reliable. Rodin retrieves ingredients, not meals: the neighbours are the result.
            neighbour_ids = [n.get("ccid") for n in gate_result.get("neighbors", [])]
            state["intermediate_steps"].append({
                "action": "GATE_III_PASS",
                "confidence": gate_result["confidence"],
                "neighbors": neighbour_ids,
                "worker_dispatch": "NOT_IMPLEMENTED",
            })
            state["output"] = (
                f"Gate III PASS [M_knn = {gate_result['confidence']:.4f}]. "
                f"{len(neighbour_ids)} neighbour node(s) retrieved: {', '.join(str(i) for i in neighbour_ids)}. "
                "No worker agent ran: the swarm roles are not implemented."
            )
            state["spacetime_payload"]["causal_proof"].append("GATE_III_PASS_RETRIEVAL_ONLY")

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

    def get_attached_rodin_extensions(self, query: str = "Starfire Sovereign Identity") -> Dict[str, Any]:
        """
        Verifies live attachment of `memory/PhoenixRodin.py`, `memory/_settings.py`,
        and `memory/Rodin_orchestrator_sub_agents_blueprint.py` to RodinSupervisor.
        """
        from memory.PhoenixRodin import DEFAULT_MONGODB_TOOL_SETTINGS, search_mongodb_substrate_sync
        from memory.Rodin_orchestrator_sub_agents_blueprint import LoopAgent, LoopAgentState

        loop_agent = LoopAgent(name="rodin_sub_agent_loop", sub_agents=[], max_iterations=3)
        loop_state = LoopAgentState(current_sub_agent="gate_iii_verifier", times_looped=0)
        search_res = search_mongodb_substrate_sync(
            collection_name="braille_atlas_nodes",
            query=query,
            limit=5,
            settings=DEFAULT_MONGODB_TOOL_SETTINGS,
        )
        return {
            "status": "LIVE_AND_ATTACHED",
            "loop_agent_name": getattr(loop_agent, "name", "rodin_sub_agent_loop"),
            "loop_state_sub_agent": loop_state.current_sub_agent,
            "phoenix_rodin_search_status": search_res.get("status"),
            "phoenix_rodin_mode": search_res.get("mode"),
            "rows_returned": len(search_res.get("rows", [])),
        }

    @property
    def cit_grid_engine(self):
        if self._cit_grid_engine is None:
            from memory.braille_atlas_engine import PHOENIX_CELESTIAL_GRID_ENGINE

            self._cit_grid_engine = PHOENIX_CELESTIAL_GRID_ENGINE
        return self._cit_grid_engine

    @property
    def throughput_engine(self):
        if self._throughput_engine is None:
            from memory.braille_atlas_engine import NEURAL_GRID_THROUGHPUT_ENGINE

            self._throughput_engine = NEURAL_GRID_THROUGHPUT_ENGINE
        return self._throughput_engine

    def dispatch_cit_orbital_route(
        self,
        prompt: str,
        search_epoch_sec: Optional[int] = None,
        cwa_nexus_posterior: float = 0.50,
        intent_confidence: float = 0.92,
        active_context_tokens: int = 48000,
        indirect_bridge_score: float = 0.0,
        top_k: int = 3,
    ) -> Dict[str, Any]:
        """
        Task L-4 Unified Conductor:
          1. Sweeps Occupied CIT (X, Y) Crosspoints along the Planetary Trajectory (`D_orbital`).
          2. Evaluates Master Plot-Point Throughput (`Upsilon_{r,c}`) & Multi-Modal RRF (`k=60`).
          3. If `RodinProtocol.neural_grid_router` holds registered 768D plot points, executes
             Two-Stage MRL (`64D -> 768D`), `M_knn`, `EIG`, `SSR >= 0.95`, Nexus Decision Tree,
             and the 4-Step Neuron Checkpointer.
        """
        epoch = int(time.time() if search_epoch_sec is None else search_epoch_sec)
        orbital_sweep = self.cit_grid_engine.phoenix_orbital_locate_nodes(
            query_text=prompt,
            search_epoch_sec=epoch,
            top_k=top_k,
        )
        throughput_eval = self.throughput_engine.evaluate_neural_grid_throughput(
            query_text=prompt,
            cwa_nexus_posterior=cwa_nexus_posterior,
            top_k=top_k,
        )
        router = self.rodin.get_neural_grid_router()
        nexus_route = None
        if router.plot_points:
            nexus_route = router.route_query_through_neural_grid(
                prompt=prompt,
                intent_confidence=intent_confidence,
                active_context_tokens=active_context_tokens,
                indirect_bridge_score=indirect_bridge_score,
            ).to_dict()

        return {
            "prompt": prompt,
            "search_epoch_sec": epoch,
            "cit_capacity": self.cit_grid_engine.grid_capacity_telemetry(),
            "orbital_sweep": orbital_sweep,
            "throughput_calculus": throughput_eval,
            "nexus_decision_route": nexus_route,
        }

    def apply_mistake_loop_correction(self, correction_packet: Dict[str, str]) -> Dict[str, Any]:
        """Forwards user Correction Packet to Rodin's Mistake Loop & Shadow State Warm Cache."""
        return self.rodin.apply_mistake_loop_correction(correction_packet)
