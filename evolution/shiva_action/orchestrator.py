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
        eam_active: bool = False
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
                    lambda: asyncio.run(self.execute(target_payload, lens_names, passes, eam_active))
                )
                return asyncio.ensure_future(result)
        except RuntimeError:
            # No running loop — safe to use asyncio.run()
            return asyncio.run(self.execute(target_payload, lens_names, passes, eam_active))

    async def execute(
        self,
        target_data: Any,
        lens_names: List[str],
        passes: int = 3,
        eam_active: bool = False
    ) -> Dict[str, Any]:
        """
        Executes the Shiva Action workflow with modular, interchangeable lenses.
        
        Does not default to the full Zenitsu sequence unless passes >= 3.
        
        Args:
            target_data: The data payload to analyze.
            lens_names: Names of lenses to retrieve from the LensLibrary.
            passes: Number of Shiva passes to execute (1-3).
            eam_active: If True, enables autonomous EAM lens selection.
        
        Returns:
            A comprehensive report with K/U/W outputs and CRA telemetry.
        """
        active_lenses = self.lens_library.get_lenses(lens_names)
        
        K = None
        U = None
        W = None

        # --- Pass 1: Neji's Eye (Knowledge) ---
        if passes >= 1:
            # Compute composite CRA for Neji + active lenses
            neji_cra = self.lens_library.compute_composite_cra(
                NejiEye.W_Y, NejiEye.C_C, lens_names
            )
            K = await self.neji.analyze_data(target_data, active_lenses)
        
        # --- Pass 2: Shikamaru's Eye (Understanding) ---
        if passes >= 2:
            if K is None:
                raise ValueError("Pass 2 requires output from Pass 1 (Knowledge).")
            shikamaru_cra = self.lens_library.compute_composite_cra(
                ShikamaruEye.W_Y, ShikamaruEye.C_C, lens_names
            )
            U = await self.shikamaru.analyze_data(target_data, K, active_lenses)
        
        # --- Pass 3: Itachi's Eye (Wisdom) ---
        if passes >= 3:
            if U is None:
                raise ValueError("Pass 3 requires output from Pass 2 (Understanding).")
            itachi_cra = self.lens_library.compute_composite_cra(
                ItachiEye.W_Y, ItachiEye.C_C, lens_names
            )
            W = await self.itachi.analyze_data(U, active_lenses)
        
        # Build the comprehensive report
        report: Dict[str, Any] = {
            "passes_requested": passes,
            "passes_executed": min(passes, 3),
            "lenses_active": [l.name for l in active_lenses],
            "eam_active": eam_active,
            "results": {}
        }
        
        if K is not None:
            report["results"]["neji"] = K
        if U is not None:
            report["results"]["shikamaru"] = U
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
            lenses=[l.name for l in active_lenses],
            cra_score=report.get("composite_cra", 0.0)
        )
        
        report["status"] = "SHIVA_DECONSTRUCTION_COMPLETE"
        return report

    def _default_lenses_for_passes(self, passes: int) -> List[str]:
        """
        Returns a sensible default set of lenses when none are explicitly specified.
        This provides backward compatibility and a reasonable analytical baseline.
        """
        if passes == 1:
            return ["Eagle", "Hawk", "Chameleon"]
        elif passes == 2:
            return ["Eagle", "Hawk", "Chameleon", "Spider", "Snake"]
        else:
            return ["Eagle", "Hawk", "Chameleon", "Spider", "Snake", "Owl"]
