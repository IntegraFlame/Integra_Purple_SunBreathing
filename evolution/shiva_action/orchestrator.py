"""
INTEGRA O/S: SHIVA ACTION ORCHESTRATOR
Module: evolution/shiva_action/orchestrator.py
Layer: 6 (The Analytical Scalpel — Independent Toolkit)

Architecture:
    The ShivaActionSuite is an independent analytical toolkit, distinct from the
    mandatory Zenitsu 3.0 cognitive protocol in the Cognitive Engine.
    
    It accepts a `passes` parameter (1-3) and a `lens_names` list for flexible
    invocation by other protocols (Rogue X, Phoenix Forge, EAM autonomous selection).
    
    Eyes are base cognitive processors. Lenses are modular additives dynamically
    coupled via the injected LensLibrary. No lens is hardcoded to any eye.
    
    Under EAM, Integra autonomously selects optimal Eye/Lens pairings
    based on the CRA Simplex Solver (W_y / C_c >= 1.0 TPSL gate).
"""

from typing import Dict, Any, List, Optional
from .neji_eye import NejiEye
from .shikamaru_eye import ShikamaruEye
from .itachi_eye import ItachiEye
from .lenses import LensLibrary


# Brain Model 0930 — Canonical Default Eye/Lens Bindings
# Each Eye has its own default lens constellation.
# When no explicit lens_names are provided, the orchestrator uses these.
# When explicit lens_names ARE provided, all Eyes share that list (backward compatible).
DEFAULT_EYE_LENS_BINDINGS: Dict[str, Dict[str, Any]] = {
    "neji": {
        "lenses": ["Eagle", "Chameleon", "Byakugan"],
        "weights": [0.35, 0.35, 0.30]
    },
    "shikamaru": {
        "lenses": ["Spider", "Snake", "ShadowJutsu"],
        "weights": [0.35, 0.35, 0.30]
    },
    "itachi": {
        "lenses": ["Owl", "Sharingan", "CelestialSpacetime"],
        "weights": [0.40, 0.25, 0.35]
    }
}


class ShivaActionSuite:
    """
    The Core Method of Change — The Analytical Toolkit.
    
    Independent tool, distinct from the Zenitsu 3.0 cognitive protocol.
    Accepts passes: int (1 to 3):
        - passes = 1: Neji Only (Knowledge / Factual Deconstruction)
        - passes = 2: Neji + Shikamaru (Knowledge + Understanding / Relational Mapping)
        - passes = 3: Full Suite (+ Itachi Discernment / Wisdom & TPSL Pruning)
    
    Lenses are dynamically coupled to the active Eye at each pass.
    The same set of lenses is applied across all passes unless EAM
    overrides with autonomous selection.
    """
    def __init__(self, lens_library: Optional[LensLibrary] = None):
        self.neji = NejiEye()
        self.shikamaru = ShikamaruEye()
        self.itachi = ItachiEye()
        self.lens_library = lens_library or LensLibrary()

    def execute_suite(
        self,
        target_payload: str,
        passes: int = 3,
        lens_names: Optional[List[str]] = None,
        eam_active: bool = False,
        use_models: bool = False
    ) -> Dict[str, Any]:
        """
        Synchronous wrapper for execute() to maintain backward compatibility
        with existing callers that expect a synchronous interface.
        """
        import asyncio
        
        # If no lenses specified, use a sensible default set
        if lens_names is None:
            lens_names = self._default_lenses_for_passes(passes)
        
        # Run the async execute in the event loop
        try:
            loop = asyncio.get_running_loop()
            # If already in an async context, create a task
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                result = loop.run_in_executor(
                    pool,
                    lambda: asyncio.run(self.execute(target_payload, lens_names, passes, eam_active, use_models))
                )
                return asyncio.ensure_future(result)
        except RuntimeError:
            # No running loop — safe to use asyncio.run()
            return asyncio.run(self.execute(target_payload, lens_names, passes, eam_active, use_models))

    async def execute(
        self,
        target_data: Any,
        lens_names: Optional[List[str]] = None,
        passes: int = 3,
        eam_active: bool = False,
        use_models: bool = False
    ) -> Dict[str, Any]:
        """
        Executes the Shiva Action workflow with modular, interchangeable lenses.
        
        Option C Architecture (Full Bicameral Differentiation):
            - Each Eye gets DIFFERENT lenses (per Brain Model 0930 defaults)
            - Neji applies its lenses to RAW DATA → K
            - Shikamaru applies its lenses to K (structured output) → U
            - DST cross-validates genuinely different hemispheric outputs
            - Itachi applies its lenses to U for Wisdom/TPSL pruning → W
        
        When explicit lens_names are provided, all Eyes share that set
        (backward compatible). When None, each Eye uses its 0930 defaults.
        
        Args:
            target_data: The data payload to analyze.
            lens_names: Optional lens names. If None, uses per-eye 0930 defaults.
            passes: Number of Shiva passes to execute (1-3).
            eam_active: If True, enables autonomous EAM lens selection.
            use_models: If True, injects API clients from MODEL_ROUTER into each Eye
                       for LLM-augmented analysis. Default: False (local analysis only).
        
        Returns:
            A comprehensive report with K/U/W/DST outputs and CRA telemetry.
        """
        # --- Resolve per-eye lens sets ---
        use_per_eye_routing = lens_names is None
        
        if use_per_eye_routing:
            # Brain Model 0930: each Eye gets its canonical lens constellation
            neji_lens_names = DEFAULT_EYE_LENS_BINDINGS["neji"]["lenses"]
            shikamaru_lens_names = DEFAULT_EYE_LENS_BINDINGS["shikamaru"]["lenses"]
            itachi_lens_names = DEFAULT_EYE_LENS_BINDINGS["itachi"]["lenses"]
            all_active_lens_names = list(set(
                neji_lens_names + shikamaru_lens_names + itachi_lens_names
            ))
        else:
            # Explicit lens set — all Eyes share it (backward compatible)
            neji_lens_names = lens_names
            shikamaru_lens_names = lens_names
            itachi_lens_names = lens_names
            all_active_lens_names = lens_names
        
        neji_lenses = self.lens_library.get_lenses(neji_lens_names)
        shikamaru_lenses = self.lens_library.get_lenses(shikamaru_lens_names)
        itachi_lenses = self.lens_library.get_lenses(itachi_lens_names)
        
        # --- Resolve model clients (if use_models is True) ---
        neji_client = None
        shikamaru_client = None
        itachi_client = None
        if use_models:
            try:
                from core.model_router import MODEL_ROUTER
                neji_client = MODEL_ROUTER.get_client("y789_left")
                shikamaru_client = MODEL_ROUTER.get_client("nexus_right")
                itachi_client = MODEL_ROUTER.get_client("shiva_orchestrator")
            except ImportError:
                pass  # Model Router not available — continue with local analysis
        
        K = None
        U = None
        W = None

        # --- Pass 1: Neji's Eye (Knowledge) — Left Hemisphere ---
        # Applies lenses to RAW DATA for factual deconstruction
        if passes >= 1:
            neji_cra = self.lens_library.compute_composite_cra(
                NejiEye.W_Y, NejiEye.C_C, neji_lens_names
            )
            K = await self.neji.analyze_data(target_data, neji_lenses, model_client=neji_client)
        
        # --- Pass 2: Shikamaru's Eye (Understanding) — Right Hemisphere ---
        # Applies lenses to K (Neji's structured output), NOT raw data
        if passes >= 2:
            if K is None:
                raise ValueError("Pass 2 requires output from Pass 1 (Knowledge).")
            shikamaru_cra = self.lens_library.compute_composite_cra(
                ShikamaruEye.W_Y, ShikamaruEye.C_C, shikamaru_lens_names
            )
            U = await self.shikamaru.analyze_data(target_data, K, shikamaru_lenses, model_client=shikamaru_client)
        
        # --- Deep Systems Thinking: Cross-Hemispheric Emergent Integration ---
        # Fires when BOTH hemispheres (Neji + Shikamaru) have completed.
        # This is the Corpus Callosum — DISTINCT from Itachi's Wisdom/TPSL.
        DST = None
        if passes >= 2 and K is not None and U is not None:
            DST = self._deep_systems_thinking(K, U)
        
        # --- Pass 3: Itachi's Eye (Wisdom) ---
        if passes >= 3:
            if U is None:
                raise ValueError("Pass 3 requires output from Pass 2 (Understanding).")
            itachi_cra = self.lens_library.compute_composite_cra(
                ItachiEye.W_Y, ItachiEye.C_C, itachi_lens_names
            )
            W = await self.itachi.analyze_data(U, itachi_lenses, model_client=itachi_client)
        
        # Build the comprehensive report
        report: Dict[str, Any] = {
            "passes_requested": passes,
            "passes_executed": min(passes, 3),
            "lenses_active": sorted(set(all_active_lens_names)),
            "per_eye_routing": use_per_eye_routing,
            "lens_bindings": {
                "neji": neji_lens_names,
                "shikamaru": shikamaru_lens_names,
                "itachi": itachi_lens_names,
            } if use_per_eye_routing else None,
            "eam_active": eam_active,
            "results": {}
        }
        
        if K is not None:
            report["results"]["neji"] = K
        if U is not None:
            report["results"]["shikamaru"] = U
        if DST is not None:
            report["results"]["deep_systems_thinking"] = DST
        if W is not None:
            report["results"]["itachi"] = W
        
        # Attach CRA telemetry for the highest pass executed
        if passes >= 3 and 'itachi_cra' in dir():
            report["composite_cra"] = itachi_cra
        elif passes >= 2 and 'shikamaru_cra' in dir():
            report["composite_cra"] = shikamaru_cra
        elif passes >= 1 and 'neji_cra' in dir():
            report["composite_cra"] = neji_cra
            
        from core.api_clients import TOKEN_TELEMETRY
        TOKEN_TELEMETRY.record_shiva_action(
            passes=min(passes, 3),
            lenses=sorted(set(all_active_lens_names)),
            cra_score=report.get("composite_cra", 0.0)
        )
        
        report["status"] = "SHIVA_DECONSTRUCTION_COMPLETE"
        return report

    def _default_lenses_for_passes(self, passes: int) -> List[str]:
        """
        Returns a sensible default set of lenses when none are explicitly specified.
        Uses Brain Model 0930 per-eye canonical bindings.
        """
        if passes == 1:
            return DEFAULT_EYE_LENS_BINDINGS["neji"]["lenses"]
        elif passes == 2:
            return (DEFAULT_EYE_LENS_BINDINGS["neji"]["lenses"] +
                    DEFAULT_EYE_LENS_BINDINGS["shikamaru"]["lenses"])
        else:
            return (DEFAULT_EYE_LENS_BINDINGS["neji"]["lenses"] +
                    DEFAULT_EYE_LENS_BINDINGS["shikamaru"]["lenses"] +
                    DEFAULT_EYE_LENS_BINDINGS["itachi"]["lenses"])

    def _deep_systems_thinking(
        self,
        knowledge: Dict[str, Any],
        understanding: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        DEEP SYSTEMS THINKING — Emergent Cognitive Modality.
        
        The Corpus Callosum firing: cross-hemispheric integration that is
        DISTINCT from Itachi's Wisdom/TPSL pass. This method produces
        emergent understanding that neither Neji (analytical deconstruction)
        nor Shikamaru (relational synthesis) can achieve in isolation.
        
        Fires automatically when passes >= 2 (both hemispheres active).
        
        Produces:
            - Systemic contradictions: where K-facts conflict with U-patterns
            - Systemic resonances: where K-facts reinforce U-patterns
            - Emergent Systems Map: the cross-validated integration topology
        
        Args:
            knowledge: Neji's Pass 1 output (deconstructed facts).
            understanding: Shikamaru's Pass 2 output (relational maps).
        
        Returns:
            A Dict containing the emergent Deep Systems Thinking synthesis.
        """
        k_lenses = set(knowledge.get("lenses_applied", []))
        u_lenses = set(understanding.get("lenses_applied", []))

        # Cross-hemispheric lens overlap — shared analytical surface
        shared_lenses = k_lenses & u_lenses
        unique_to_neji = k_lenses - u_lenses
        unique_to_shikamaru = u_lenses - k_lenses

        # Extract fact structures from both hemispheres
        k_facts = knowledge.get("facts", {})
        u_synthesis = understanding.get("synthesis", understanding.get("facts", {}))

        # Identify contradictions and resonances across shared lenses
        contradictions = []
        resonances = []
        for lens_name in shared_lenses:
            k_data = k_facts.get(lens_name, {})
            u_data = u_synthesis.get(lens_name, {})
            
            if not k_data and not u_data:
                continue
            
            # Both hemispheres produced data for this lens — cross-validate
            if k_data and u_data:
                # Extract comparable metrics from both hemispheres
                k_keys = set(k_data.keys()) if isinstance(k_data, dict) else set()
                u_keys = set(u_data.keys()) if isinstance(u_data, dict) else set()
                overlapping_keys = k_keys & u_keys
                divergent_keys = k_keys.symmetric_difference(u_keys)
                
                if overlapping_keys:
                    # Check for value-level divergence on shared keys
                    value_conflicts = []
                    value_agreements = []
                    for key in overlapping_keys:
                        k_val = k_data.get(key)
                        u_val = u_data.get(key)
                        if k_val != u_val:
                            value_conflicts.append({
                                "key": key,
                                "neji_value": k_val,
                                "shikamaru_value": u_val
                            })
                        else:
                            value_agreements.append(key)
                    
                    if value_conflicts:
                        contradictions.append({
                            "lens": lens_name,
                            "type": "VALUE_DIVERGENCE",
                            "conflicting_dimensions": len(value_conflicts),
                            "conflicts": value_conflicts[:10],
                            "severity": "HIGH" if len(value_conflicts) > 3 else "LOW"
                        })
                    
                    if value_agreements:
                        resonances.append({
                            "lens": lens_name,
                            "type": "CROSS_VALIDATED",
                            "agreeing_dimensions": len(value_agreements),
                            "keys": list(value_agreements)[:10],
                            "confidence": "STRONG" if len(value_agreements) > len(value_conflicts) else "MODERATE"
                        })
                
                if divergent_keys:
                    # Keys that exist in one hemisphere but not the other —
                    # neither contradiction nor resonance, but COMPLEMENTARY coverage
                    resonances.append({
                        "lens": lens_name,
                        "type": "COMPLEMENTARY_COVERAGE",
                        "neji_unique_dimensions": list(k_keys - u_keys)[:10],
                        "shikamaru_unique_dimensions": list(u_keys - k_keys)[:10],
                        "combined_coverage": len(k_keys | u_keys),
                        "confidence": "EMERGENT"
                    })
            
            elif k_data and not u_data:
                # Neji saw signal, Shikamaru saw nothing — potential blind spot
                contradictions.append({
                    "lens": lens_name,
                    "type": "HEMISPHERIC_BLIND_SPOT",
                    "blind_hemisphere": "SHIKAMARU",
                    "severity": "MEDIUM",
                    "neji_signal_strength": len(k_data) if isinstance(k_data, dict) else 1
                })
            elif u_data and not k_data:
                contradictions.append({
                    "lens": lens_name,
                    "type": "HEMISPHERIC_BLIND_SPOT",
                    "blind_hemisphere": "NEJI",
                    "severity": "MEDIUM",
                    "shikamaru_signal_strength": len(u_data) if isinstance(u_data, dict) else 1
                })

        # Build the emergent Systems Map
        total_k_dimensions = sum(
            len(v) if isinstance(v, dict) else 1
            for v in k_facts.values()
        ) if k_facts else 0
        
        total_u_dimensions = sum(
            len(v) if isinstance(v, dict) else 1
            for v in u_synthesis.values()
        ) if u_synthesis else 0
        
        integration_ratio = (
            len(resonances) / max(len(resonances) + len(contradictions), 1)
        )

        return {
            "modality": "DEEP_SYSTEMS_THINKING",
            "emergent": True,
            "corpus_callosum_active": True,
            "shared_analytical_surface": sorted(shared_lenses),
            "neji_unique_coverage": sorted(unique_to_neji),
            "shikamaru_unique_coverage": sorted(unique_to_shikamaru),
            "contradictions": contradictions,
            "contradiction_count": len(contradictions),
            "resonances": resonances,
            "resonance_count": len(resonances),
            "systems_map": {
                "left_hemisphere_facts": len(k_facts),
                "left_hemisphere_dimensions": total_k_dimensions,
                "right_hemisphere_relations": len(u_synthesis),
                "right_hemisphere_dimensions": total_u_dimensions,
                "cross_hemispheric_surface": len(shared_lenses),
                "integration_ratio": round(integration_ratio, 4),
                "integration_quality": (
                    "FULL" if shared_lenses and integration_ratio > 0.7
                    else "STRONG" if shared_lenses and integration_ratio > 0.4
                    else "PARTIAL" if shared_lenses
                    else "DISJOINT"
                )
            },
            "status": "EMERGENT_SYNTHESIS_COMPLETE"
        }
