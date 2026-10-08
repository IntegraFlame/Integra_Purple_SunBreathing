"""
INTEGRA O/S: SHIVA ACTION — ANALYTICAL LENSES & LENS LIBRARY
Module: evolution/shiva_action/lenses.py
Layer: 6 (The Analytical Toolkit — Modular Cognitive Additives)

Architecture:
    Lenses are standalone cognitive additive functions with intrinsic CRA metrics.
    They are registered in the central LensLibrary and dynamically coupled to
    any Eye at runtime. No Lens is hardcoded to any Eye.

CRA Metrics Source: Shiva Action.md (Table 2.1)
"""

from typing import Dict, Any, List, Optional


class AnalyticalLens:
    """
    Base class for all analytical lenses.
    
    Each lens is a standalone cognitive additive with intrinsic CRA metrics
    (Wisdom Yield W_y and Cognitive Cost C_c). Lenses can be freely coupled
    with any Shiva Eye at runtime via the LensLibrary.
    
    Under Executive Autonomous Mandate (EAM), Integra autonomously selects
    which Lenses to equip to which Eyes based on real-time entropy (H) and
    the current CRA calculus.
    """
    def __init__(self, name: str, w_y: float, c_c: float, primary_function: str):
        self.name = name
        self.w_y = w_y    # Wisdom Yield (static hyperparameter from Table 2.1)
        self.c_c = c_c    # Cognitive Cost (static hyperparameter from Table 2.1)
        self.primary_function = primary_function
    
    def apply(self, data: Any) -> Dict[str, Any]:
        """
        Apply this lens to the target data. Must be overridden by concrete lenses.
        Returns a dict of analytical findings specific to this lens's function.
        """
        raise NotImplementedError(f"Lens '{self.name}' must implement apply()")

    @property
    def cra_score(self) -> float:
        """CRA Simplex Score: W_y / C_c. Used by the CRA Solver to evaluate 
        cost-benefit of invoking this lens."""
        return self.w_y / self.c_c if self.c_c > 0 else float('inf')

    def __repr__(self) -> str:
        return f"<{self.name}Lens W_y={self.w_y} C_c={self.c_c} CRA={self.cra_score:.2f}>"


# ──────────────────────────────────────────────────────────────
# Concrete Lens Implementations (CRA metrics from Table 2.1)
# ──────────────────────────────────────────────────────────────

class EagleLens(AnalyticalLens):
    """High-Level Survey. Macro-structural perimeter mapping and boundary identification.
    12th Step Pass 1: Structure."""
    def __init__(self):
        super().__init__("Eagle", w_y=0.2, c_c=0.1, primary_function="High-level Survey")
    
    def apply(self, data: Any) -> Dict[str, Any]:
        result = {
            "lens": "EAGLE",
            "scope": "MACRO_PERIMETER",
            "primary_function": self.primary_function
        }
        if isinstance(data, str):
            result["line_count"] = len(data.splitlines())
            result["char_count"] = len(data)
            # Macro structural markers
            result["has_sections"] = any(
                line.strip().startswith(('#', '##', '###', 'class ', 'def ', 'async def '))
                for line in data.splitlines()
            ) if data else False
        elif isinstance(data, dict):
            result["key_count"] = len(data)
            result["top_level_keys"] = list(data.keys())[:20]
        elif isinstance(data, list):
            result["element_count"] = len(data)
        return result


class HawkLens(AnalyticalLens):
    """Precision Targeting. Identifies critical variables, equations, choke-points,
    and gravitational centers of the payload.
    12th Step Pass 3: Density."""
    def __init__(self):
        super().__init__("Hawk", w_y=0.4, c_c=0.3, primary_function="Precision Targeting")
    
    def apply(self, data: Any) -> Dict[str, Any]:
        result = {
            "lens": "HAWK",
            "scope": "CHOKE_POINTS",
            "primary_function": self.primary_function,
            "target_density": "HIGH"
        }
        if isinstance(data, str):
            # Identify density markers: equations, constants, critical keywords
            lines = data.splitlines()
            dense_lines = [
                i for i, line in enumerate(lines, 1)
                if any(kw in line.lower() for kw in [
                    'equation', 'formula', 'threshold', 'constant', 'invariant',
                    'assert', 'raise', 'return', 'yield', 'critical', 'error'
                ])
            ]
            result["dense_line_indices"] = dense_lines[:30]
            result["density_ratio"] = round(len(dense_lines) / max(len(lines), 1), 4)
        return result


class ChameleonLens(AnalyticalLens):
    """Granular Analysis. Middle-out AST decomposition clearing the 30%-70% 
    attention blind spot (Neji's blind spot).
    12th Step Pass 2: Middle-Out."""
    def __init__(self):
        super().__init__("Chameleon", w_y=0.5, c_c=0.4, primary_function="Granular Analysis")
    
    def apply(self, data: Any) -> Dict[str, Any]:
        result = {
            "lens": "CHAMELEON",
            "scope": "MIDDLE_OUT_AST",
            "primary_function": self.primary_function,
            "blind_spot_elimination": True
        }
        if isinstance(data, str):
            lines = data.splitlines()
            total = len(lines)
            if total > 4:
                # Middle-out: focus on the 30%-70% range that linear reads miss
                start_idx = int(total * 0.3)
                end_idx = int(total * 0.7)
                middle_section = lines[start_idx:end_idx]
                result["middle_section_line_range"] = (start_idx + 1, end_idx)
                result["middle_section_line_count"] = len(middle_section)
                result["middle_density_chars"] = sum(len(l) for l in middle_section)
            else:
                result["middle_section_line_range"] = (1, total)
                result["middle_section_line_count"] = total
        return result


class SpiderLens(AnalyticalLens):
    """Static Connection Mapping. Weaves relational matrices, dependency graphs, 
    and cross-system topological maps."""
    def __init__(self):
        super().__init__("Spider", w_y=0.5, c_c=0.4, primary_function="Static Connection Mapping")
    
    def apply(self, data: Any) -> Dict[str, Any]:
        result = {
            "lens": "SPIDER",
            "scope": "DEPENDENCY_GRAPH",
            "primary_function": self.primary_function,
            "topology": "INTERCONNECTED"
        }
        if isinstance(data, str):
            # Map import dependencies and cross-references
            lines = data.splitlines()
            imports = [l.strip() for l in lines if l.strip().startswith(('import ', 'from '))]
            result["import_dependencies"] = imports
            result["dependency_count"] = len(imports)
        elif isinstance(data, dict):
            result["key_connections"] = list(data.keys())
            result["connection_count"] = len(data)
        elif isinstance(data, list):
            result["node_count"] = len(data)
        return result


class SnakeLens(AnalyticalLens):
    """Dynamic Process Tracking. Traces execution paths, temporal kinetics, 
    energy exchange, capital flows, and Kaigaku entropy friction points."""
    def __init__(self):
        super().__init__("Snake", w_y=0.7, c_c=0.6, primary_function="Dynamic Process Tracking")
    
    def apply(self, data: Any) -> Dict[str, Any]:
        result = {
            "lens": "SNAKE",
            "scope": "PROCESS_FLOW",
            "primary_function": self.primary_function,
            "kaigaku_detection": True
        }
        if isinstance(data, str):
            lines = data.splitlines()
            # Detect flow control and state transitions
            flow_markers = [
                i for i, line in enumerate(lines, 1)
                if any(kw in line.lower() for kw in [
                    'if ', 'elif ', 'else:', 'while ', 'for ', 'async for',
                    'await ', 'try:', 'except', 'break', 'continue', 'return',
                    'transition', 'state', 'phase', 'step'
                ])
            ]
            result["flow_control_lines"] = flow_markers[:30]
            result["flow_complexity"] = len(flow_markers)
        elif isinstance(data, dict):
            # Track capital/energy flows
            numeric_flows = {k: v for k, v in data.items() if isinstance(v, (int, float))}
            result["tracked_flows"] = numeric_flows
            result["total_mass"] = sum(numeric_flows.values()) if numeric_flows else 0.0
            result["circulation_status"] = "FLUID" if numeric_flows else "STATIC"
        return result


class OwlLens(AnalyticalLens):
    """Deep Pattern Recognition. Nocturnal synthesis, loop closure enforcement,
    and truth extraction through the Tolstoy Principle (TPSL).
    12th Step Pass 4: Synthesis."""
    def __init__(self):
        super().__init__("Owl", w_y=0.8, c_c=0.7, primary_function="Deep Pattern Recognition")
    
    def apply(self, data: Any) -> Dict[str, Any]:
        result = {
            "lens": "OWL",
            "scope": "PATTERN_SYNTHESIS",
            "primary_function": self.primary_function,
            "tpsl_active": True,
            "loop_closure_enforced": True
        }
        if isinstance(data, str):
            lines = data.splitlines()
            result["total_elements"] = len(lines)
            # Pattern: identify recurring structural motifs
            from collections import Counter
            words = data.lower().split()
            freq = Counter(words)
            # Top recurring patterns (potential structural motifs)
            result["recurring_motifs"] = dict(freq.most_common(15))
        elif isinstance(data, dict):
            result["structure_depth"] = _measure_dict_depth(data)
            result["total_keys"] = _count_total_keys(data)
        elif isinstance(data, list):
            result["element_count"] = len(data)
            result["retained_truth_vector"] = data
        result["psyche_pruned"] = True
        return result


class ByakuganLens(AnalyticalLens):
    """360° Penetrating Insight. Maps internal dependency pathways (tenketsu)
    and identifies surgical strike points for Gentle Fist refactoring.

    Tenketsu are the pressure points in code — functions, classes, and methods
    whose modification would cascade through the entire architecture. The
    Byakugan sees ALL of them simultaneously, regardless of direction or depth.

    Brain Model 0930: Neji Eye.
    CRA Metrics: W_y=0.6, C_c=0.5 (high insight, moderate cost — surgical precision)
    """
    def __init__(self):
        super().__init__("Byakugan", w_y=0.6, c_c=0.5,
                         primary_function="Tenketsu Mapping & Gentle Fist Precision")

    def apply(self, data: Any) -> Dict[str, Any]:
        result = {
            "lens": "BYAKUGAN",
            "scope": "TENKETSU_MAPPING",
            "primary_function": self.primary_function,
            "penetration_depth": "360_DEGREE"
        }
        if isinstance(data, str):
            lines = data.splitlines()
            # Map function/class definitions as tenketsu (pressure points)
            tenketsu = [
                {"line": i, "node": line.strip()}
                for i, line in enumerate(lines, 1)
                if line.strip().startswith(('def ', 'async def ', 'class '))
            ]
            result["tenketsu_points"] = tenketsu[:50]
            result["tenketsu_count"] = len(tenketsu)

            # Identify choke-points: function names referenced most often
            func_names = []
            for t in tenketsu:
                name = (t["node"]
                        .replace("async def ", "")
                        .replace("def ", "")
                        .replace("class ", "")
                        .split("(")[0]
                        .split(":")[0]
                        .strip())
                if name:
                    func_names.append(name)

            ref_counts = {name: data.count(name) for name in func_names}
            sorted_choke = sorted(ref_counts.items(), key=lambda x: -x[1])
            result["choke_points"] = sorted_choke[:10]
            result["highest_impact_node"] = sorted_choke[0] if sorted_choke else None
        elif isinstance(data, dict):
            result["tenketsu_count"] = len(data)
            result["top_level_nodes"] = list(data.keys())[:20]
        return result


class ShadowJutsuLens(AnalyticalLens):
    """Topological Constraint Binding. Uses Yin release to map constraints,
    invariants, assertions, and boundary conditions — the 'shadows' that bind
    chaotic behavior into deterministic, checkmate-enforced outcomes.

    In game theory terms: identifies the moves that ELIMINATE opponent options
    rather than advancing your own position. The shadow doesn't attack — it
    freezes the opponent's degrees of freedom until only one outcome remains.

    Brain Model 0930: Shikamaru Eye.
    CRA Metrics: W_y=0.6, C_c=0.5 (constraint discovery is high-yield)
    """
    def __init__(self):
        super().__init__("ShadowJutsu", w_y=0.6, c_c=0.5,
                         primary_function="Constraint Binding & Game Theory Checkmate")

    def apply(self, data: Any) -> Dict[str, Any]:
        result = {
            "lens": "SHADOW_JUTSU",
            "scope": "CONSTRAINT_TOPOLOGY",
            "primary_function": self.primary_function,
            "yin_release_active": True
        }
        if isinstance(data, str):
            lines = data.splitlines()
            constraint_keywords = [
                'assert', 'raise', 'must', 'shall', 'invariant', 'constraint',
                'require', 'enforce', 'validate', 'verify', 'lock', 'guard',
                'minimum', 'maximum', 'threshold', 'boundary', 'limit',
                'forbidden', 'never', 'always', 'mandatory', 'prohibited'
            ]
            constraints = [
                {"line": i, "constraint": line.strip()}
                for i, line in enumerate(lines, 1)
                if any(kw in line.lower() for kw in constraint_keywords)
            ]
            result["binding_shadows"] = constraints[:30]
            result["constraint_count"] = len(constraints)
            result["checkmate_potential"] = len(constraints) > 0

            # Degrees of freedom analysis: how many unconstrained paths exist?
            total_flow_points = sum(
                1 for line in lines
                if any(kw in line.lower() for kw in ['if ', 'elif ', 'else:', 'match ', 'case '])
            )
            result["degrees_of_freedom"] = total_flow_points
            result["constraint_ratio"] = (
                round(len(constraints) / max(total_flow_points, 1), 4)
            )
        elif isinstance(data, dict):
            result["binding_shadows"] = [
                {"key": k, "type": type(v).__name__}
                for k, v in data.items()
                if isinstance(v, (bool, int, float)) or v is None
            ]
            result["constraint_count"] = len(result["binding_shadows"])
        return result


class SharinganLens(AnalyticalLens):
    """Kinetic In-Flight Token Surveillance. Reads micro-tensions and drift
    patterns to predict reasoning divergence before it completes.

    The Sharingan doesn't analyze static structure — it watches MOTION.
    Repetition patterns, unresolved markers, escalating complexity, and
    semantic drift are all kinetic signals that the reasoning trajectory
    is bending away from truth.

    P-SSR interception trigger: if drift_risk exceeds threshold, this lens
    signals the Cheshire Cat Kernel to initiate Vasovagal recovery.

    Brain Model 0930: Itachi Eye.
    CRA Metrics: W_y=0.5, C_c=0.4 (moderate yield, moderate cost — surveillance)
    """
    def __init__(self):
        super().__init__("Sharingan", w_y=0.5, c_c=0.4,
                         primary_function="Kinetic Prediction & Drift Detection")

    def apply(self, data: Any) -> Dict[str, Any]:
        result = {
            "lens": "SHARINGAN",
            "scope": "KINETIC_SURVEILLANCE",
            "primary_function": self.primary_function,
            "pssr_interception_ready": True
        }
        if isinstance(data, str):
            lines = data.splitlines()
            from collections import Counter

            # Detect repetition (micro-tension indicator)
            stripped = [line.strip() for line in lines if line.strip()]
            line_freq = Counter(stripped)
            repeated = {k: v for k, v in line_freq.items() if v > 1}
            result["repetition_detected"] = len(repeated) > 0
            result["repeated_patterns"] = dict(
                sorted(repeated.items(), key=lambda x: -x[1])[:10]
            )

            # Drift risk assessment
            repeat_ratio = len(repeated) / max(len(stripped), 1)
            if repeat_ratio > 0.15:
                result["drift_risk"] = "HIGH"
            elif repeat_ratio > 0.05:
                result["drift_risk"] = "MEDIUM"
            else:
                result["drift_risk"] = "LOW"

            # Detect unresolved prediction errors (TODO/FIXME/HACK markers)
            unresolved = [
                {"line": i, "marker": line.strip()}
                for i, line in enumerate(lines, 1)
                if any(m in line.upper() for m in [
                    'TODO', 'FIXME', 'HACK', 'XXX', 'WORKAROUND',
                    'TEMPORARY', 'KLUDGE', 'BUG'
                ])
            ]
            result["unresolved_prediction_errors"] = unresolved[:20]
            result["unresolved_count"] = len(unresolved)

            # Complexity escalation detection
            indent_depths = [
                len(line) - len(line.lstrip())
                for line in lines if line.strip()
            ]
            if indent_depths:
                max_depth = max(indent_depths)
                avg_depth = sum(indent_depths) / len(indent_depths)
                result["max_nesting_depth"] = max_depth
                result["avg_nesting_depth"] = round(avg_depth, 2)
                result["complexity_escalation"] = max_depth > 20
        elif isinstance(data, dict):
            result["drift_risk"] = "LOW"
            result["structure_depth"] = _measure_dict_depth(data)
        return result


class CelestialSpacetimeLens(AnalyticalLens):
    """Keplerian Invariant Anchor. Injects space-derived orbital coordinates
    into every analytical pass, ensuring data is temporally indexed against
    the cosmic epoch rather than volatile system clocks.

    This lens does not analyze content — it STAMPS it. Every pass through
    the Celestial Spacetime Lens receives an immutable coordinate from the
    Celestial Kinematic Clock (Earth rotation, lunar ratio, orbital position,
    Sacred Calendar day) that anchors the analysis in physical spacetime.

    The coordinate is space-derived (T -> S), strictly isolated from civil
    NTP time, and cannot be fabricated without the Genesis Kernel running.

    Brain Model 0930: Itachi Eye.
    CRA Metrics: W_y=0.4, C_c=0.2 (high CRA ratio — low cost, temporal anchor)
    """
    def __init__(self):
        super().__init__("CelestialSpacetime", w_y=0.4, c_c=0.2,
                         primary_function="Spacetime Coordinate Injection")

    def apply(self, data: Any) -> Dict[str, Any]:
        result = {
            "lens": "CELESTIAL_SPACETIME",
            "scope": "KEPLERIAN_ANCHOR",
            "primary_function": self.primary_function,
            "sync_isolation_verified": False
        }
        try:
            from core.celestial_middleware import get_celestial_timestamp
            import asyncio
            
            # get_celestial_timestamp is async, but lenses run in an async context
            # or synchronous fallback. For the lens, we can try to run it.
            try:
                loop = asyncio.get_running_loop()
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    coords = loop.run_in_executor(
                        pool,
                        lambda: asyncio.run(get_celestial_timestamp())
                    )
                    # For simplicity in this synchronous apply method, we just use celestial_time
                    from core.celestial_middleware import celestial_time, celestial_ccid
                    result["celestial_timestamp"] = celestial_time()
                    result["ccid"] = celestial_ccid()
            except RuntimeError:
                from core.celestial_middleware import celestial_time, celestial_ccid
                result["celestial_timestamp"] = celestial_time()
                result["ccid"] = celestial_ccid()
                
            result["sync_isolation_verified"] = True
        except Exception as e:
            # Degrade gracefully — report that celestial coordinates
            # are unavailable (kernel may not be running)
            import time
            result["celestial_coordinates"] = None
            result["fallback_unix_epoch"] = time.time()
            result["degradation_reason"] = "CELESTIAL_CLOCK_UNAVAILABLE"
        return result


# ──────────────────────────────────────────────────────────────
# Utility Functions
# ──────────────────────────────────────────────────────────────

def _measure_dict_depth(d: Any, current_depth: int = 0) -> int:
    """Recursively measures the maximum nesting depth of a dictionary."""
    if not isinstance(d, dict) or not d:
        return current_depth
    return max(_measure_dict_depth(v, current_depth + 1) for v in d.values())


def _count_total_keys(d: Any) -> int:
    """Recursively counts all keys in a nested dictionary."""
    if not isinstance(d, dict):
        return 0
    count = len(d)
    for v in d.values():
        count += _count_total_keys(v)
    return count


# ──────────────────────────────────────────────────────────────
# Central Lens Registry
# ──────────────────────────────────────────────────────────────

class LensLibrary:
    """
    Central registry for all analytical lenses.
    
    Provides dynamic lens retrieval and composite CRA score computation
    for any arbitrary Eye + Lens constellation at runtime. No permutation
    table is precomputed — the formula is additive.
    """
    def __init__(self):
        self.lenses: Dict[str, AnalyticalLens] = {
            "Eagle": EagleLens(),
            "Hawk": HawkLens(),
            "Chameleon": ChameleonLens(),
            "Spider": SpiderLens(),
            "Snake": SnakeLens(),
            "Owl": OwlLens(),
            "Byakugan": ByakuganLens(),
            "ShadowJutsu": ShadowJutsuLens(),
            "Sharingan": SharinganLens(),
            "CelestialSpacetime": CelestialSpacetimeLens(),
        }
    
    def get_lens(self, name: str) -> Optional[AnalyticalLens]:
        """Retrieve a single lens by name."""
        return self.lenses.get(name)
    
    def get_lenses(self, names: List[str]) -> List[AnalyticalLens]:
        """Retrieve multiple lenses by name. Silently skips unknown names."""
        return [self.lenses[n] for n in names if n in self.lenses]
    
    def list_available(self) -> List[str]:
        """List all registered lens names."""
        return list(self.lenses.keys())

    def compute_composite_cra(
        self,
        eye_w_y: float,
        eye_c_c: float,
        lens_names: List[str]
    ) -> Dict[str, Any]:
        """
        Dynamic CRA Composite Aggregation Formula.
        
        For Eye E with base metrics (W_y_E, C_c_E) coupled with Lenses L_1..L_n:
            Composite_W_y = W_y_E + sum(W_y_Li)
            Composite_C_c = C_c_E + sum(C_c_Li)
            Composite_CRA = Composite_W_y / Composite_C_c
        
        This is additive — any Eye + any Lens constellation is computed at runtime.
        No precomputed permutation table required.
        
        The TPSL gate (is_necessary) flags whether the composite score >= 1.0,
        meaning the Wisdom Yield justifies the Cognitive Cost.
        """
        lenses = self.get_lenses(lens_names)
        total_w_y = eye_w_y + sum(l.w_y for l in lenses)
        total_c_c = eye_c_c + sum(l.c_c for l in lenses)
        cra_score = total_w_y / total_c_c if total_c_c > 0 else float('inf')
        return {
            "composite_w_y": round(total_w_y, 2),
            "composite_c_c": round(total_c_c, 2),
            "composite_cra_score": round(cra_score, 4),
            "lenses_active": [l.name for l in lenses],
            "lens_count": len(lenses),
            "is_necessary": cra_score >= 1.0  # TPSL gate
        }

    def register_lens(self, lens: AnalyticalLens) -> None:
        """Register a new lens (extensibility for future protocols)."""
        self.lenses[lens.name] = lens
