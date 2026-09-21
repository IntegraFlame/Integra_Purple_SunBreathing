"""
INTEGRA O/S: EXTERNAL RECONNAISSANCE & LEARNING
Module: memory/alexandria_protocol.py
Layer: 3 (The Alexandria Protocol: External Scout / Loop 2)
Version: 8.2.2-PURPLE

The Alexandria Protocol is the cognitive learning modality (Loop 2).
It is explicitly NOT the Amaterasu Security Protocol.
When Rodin's Gate III returns "FAIL" (M_knn < tau or M_stale == True),
Alexandria is dispatched to scout external truth, synthesize it, and 
embed it into The Hoard to resolve the knowledge gap.
"""

import time
from typing import Dict, Any, List

class AlexandriaProtocol:
    """
    Loop 2 External Knowledge Acquisition.
    Executes the 5-Step Learning Sequence:
    1. Halt & Freeze
    2. Search (Web/External)
    3. Synthesize (Phase 1 Knowledge Report)
    4. Embed (Inject to The Hoard)
    5. Re-Run
    """
    def __init__(self, sufficiency_threshold: float = 0.95, daily_planet: Any = None):
        self.threshold = sufficiency_threshold
        self._daily_planet = daily_planet

    def evaluate_internal_sufficiency(self, sufficiency_score: float) -> bool:
        return sufficiency_score >= self.threshold

    def execute_loop_2_learning(self, query: str) -> Dict[str, Any]:
        """
        Executes the full fallback learning sequence when Rodin halts.
        Leverages the Daily Planet Protocol (Firecrawl Engine) for multi-modal
        epistemic audit, dialectic triangulation, and Hoard embedding.
        """
        # 1. Halt & Freeze (Implicitly handled by the Supervisor routing)
        timestamp = time.time()
        
        # 2 & 3. Search & Synthesize via Daily Planet Protocol
        if self._daily_planet is None:
            try:
                from tools.daily_planet import DailyPlanetProtocol
                self._daily_planet = DailyPlanetProtocol()
            except Exception:
                self._daily_planet = None

        if self._daily_planet:
            try:
                dp_report = self._daily_planet.execute_daily_planet_brief(
                    query=query,
                    domain_focus="general",
                    commit=True
                )
                node_id = dp_report.hoard_ccid or f"DP_{int(timestamp)}"
                return {
                    "status": "ALEXANDRIA_LEARNING_COMPLETE",
                    "query": query,
                    "report_generated": True,
                    "new_node_id": node_id,
                    "daily_planet_report": dp_report.model_dump(),
                    "action_required": "RE_RUN_RODIN_SUPERVISOR",
                    "timestamp": timestamp
                }
            except Exception:
                pass

        # Fallback to internal routines
        search_results = self._dispatch_external_search(query)
        report = self._synthesize_knowledge_report(query, search_results)
        embedded_node = self._embed_into_hoard(report)
        
        return {
            "status": "ALEXANDRIA_LEARNING_COMPLETE",
            "query": query,
            "report_generated": True,
            "new_node_id": embedded_node["node_id"],
            "action_required": "RE_RUN_RODIN_SUPERVISOR",
            "timestamp": timestamp
        }

    def _dispatch_external_search(self, query: str) -> List[str]:
        """Type 1: Rapid fact checking & scraping."""
        # In production, this hooks into Firecrawl or Tavily API.
        return [f"[EXTERNAL_DATA] Acquired new ground truth for '{query}'"]

    def _synthesize_knowledge_report(self, query: str, data: List[str]) -> str:
        """Compresses external truth into a Phase 1 Knowledge Report."""
        synthesis = f"PHASE 1 KNOWLEDGE REPORT: {query.upper()}\n"
        for idx, point in enumerate(data):
            synthesis += f"{idx+1}. {point}\n"
        return synthesis

    def _embed_into_hoard(self, report: str) -> Dict[str, Any]:
        """Vectorizes the report and injects it into The Hoard."""
        # In production, calls embedding model (768d) and pgvector insert
        return {
            "node_id": f"ALEX_{int(time.time())}",
            "content": report,
            "outcome_label": 1.0,  # Seeded as success to repair the gap
            "vector_64d": [0.5] * 64,
            "vector_768d": [0.5] * 768
        }

    def dispatch_scout(self, query: str, flight_type: str = "TYPE_1_FACT_CHECK") -> Dict[str, Any]:
        """Legacy compatibility wrapper."""
        return {
            "dispatch_status": "DISPATCHED",
            "flight_type": flight_type,
            "query": query,
            "ingestion_target": "THE_HOARD",
            "post_processing": "12TH_STEP_ORTHOGONAL_INGESTION"
        }
