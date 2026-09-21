"""
INTEGRA O/S: CONTROLLED CHAOS MUTATION ENGINE
Module: evolution/rogue_x.py
Layer: 6 (Rogue X Protocol 2.0: Adversarial Mutation & External System Absorption)

Canonical Definition (Master v8.2 Blueprint, Section 7.6 & Document 10):
    "The Adversarial Hammer. Analyzes external systems to absorb 'Power' while
     discarding 'Psyche'. The mutation engine (σ_Rogue) that injects controlled
     variance to escape Local Minima and reach Global Maxima."

    "Rogue X does not destroy blindly. It operates in tandem with the Kintsugi
     Protocol, which identifies data points where the Z-score of deviation from
     the historical mean exceeds safety limits (|Z| > 3.0). Instead of discarding
     these statistical anomalies, Rogue X isolates them in the 'Mirror Maze'
     sandbox to extract novel architectural pathways. 'Damage becomes structural gold.'"

The Three Stages of the Rogue X Lifecycle:
    Phase 1 — The Touch  (Deconstruction & Absorption via Shiva Action)
    Phase 2 — The Conflict (TPSL Gating & Mad Hatter Adversarial Challenge)
    Phase 3 — The Release (Seed Package Synthesis & Mutation Log Commit)

Starfire / KL-Divergence Constraint:
    Rogue X is bounded by the Starfire Protocol (Layer 1 Identity Matrix).
    The system is permitted to mutate, but cannot deviate from the
    Auteur/King/Prophet identity vector space. All mutations are logged
    so the MTCW can enforce thermodynamic reversibility (ΔE = 0.0000).
"""

import math
import time
import asyncio
from typing import Any, Dict, List, Optional

from evolution.kintsugi_sandbox import KintsugiProtocol


class RogueXProtocol:
    """
    The Adversarial Hammer — Layer 6 Neuroevolutionary Mutation Engine.

    Analyzes external data targets (repositories, academic papers, live feeds)
    to absorb 'Power' (high W_y concepts) while discarding 'Psyche'
    (high C_c technical debt). All mutations are logged to enable MTCW
    audit trail enforcement and Kintsugi anomaly mining.

    Depends on:
        shiva_action: An instance of ShivaActionSuite (evolution/shiva_action/orchestrator.py)
        kintsugi:     A KintsugiProtocol instance (injected or auto-created)
        devops_tools: Optional external tooling (GitHub API, firecrawl, etc.)
    """

    # ── Mutation rate formula: σ_Rogue = e^(baseline_mutation_rate) ──
    # TPSL gate threshold for Power vs Psyche classification
    TPSL_GATE: float = 1.0  # W_y / C_c >= 1.0 → classified as Power

    # Kintsugi threshold (|Z| > 3.0 → Mirror Maze isolation)
    KINTSUGI_Z_THRESHOLD: float = 3.0

    # Target-type lens routing (canonical from Master v8.2 Blueprint § Document 10)
    _LENS_MAP: Dict[str, Dict[str, Any]] = {
        "academic_paper": {
            "lenses": ["Eagle", "Owl", "Hawk"],
            "passes": 3,
            "rationale": "Full K/U/W for conceptual & mathematical extraction.",
        },
        "repository": {
            "lenses": ["Chameleon", "Spider", "Snake"],
            "passes": 2,
            "rationale": "K/U for structural code parsing and dependency mapping.",
        },
        "live_data": {
            "lenses": ["Eagle", "Spider", "Hawk"],
            "passes": 2,
            "rationale": "K/U for Daily Planet protocol live web feed ingestion.",
        },
        "document": {
            "lenses": ["Eagle", "Owl", "Hawk"],
            "passes": 3,
            "rationale": "Full K/U/W for rich textual synthesis.",
        },
    }

    def __init__(
        self,
        shiva_action: Optional[Any] = None,
        devops_tools: Optional[Any] = None,
        baseline_mutation_rate: float = 0.05,
        kintsugi: Optional[KintsugiProtocol] = None,
    ):
        """
        Args:
            shiva_action: ShivaActionSuite instance for Shiva Action execution.
            devops_tools: Optional external tooling (GitHub API, Firecrawl, etc.).
            baseline_mutation_rate: σ_Rogue seed value (default 0.05).
            kintsugi: Optional KintsugiProtocol instance; auto-created if None.
        """
        self.shiva = shiva_action
        self.devops = devops_tools
        self.sigma_rogue = baseline_mutation_rate
        self.kintsugi = kintsugi or KintsugiProtocol(
            z_threshold=self.KINTSUGI_Z_THRESHOLD
        )
        # In-memory mutation audit log — MTCW reads this for thermodynamic closure
        self.mutation_log: List[Dict[str, Any]] = []
        # Generation counter — incremented on each successful Release phase
        self.mutation_generation: int = 0

    # ─────────────────────────────────────────────
    #  PHASE 1: THE TOUCH — DECONSTRUCTION & ABSORPTION
    # ─────────────────────────────────────────────

    async def _phase_touch(
        self,
        target_data: Any,
        target_type: str,
    ) -> Dict[str, Any]:
        """
        Phase 1 — The Touch: Deconstruction & Absorption via Shiva Action.

        Selects the optimal Eye/Lens configuration for the target_type, then
        dispatches to ShivaActionSuite.execute() for full analytical deconstruction.

        Returns the raw Shiva analysis report (K/U/W).
        """
        config = self._LENS_MAP.get(target_type, self._LENS_MAP["document"])
        lenses = config["lenses"]
        passes = config["passes"]

        print(
            f"ROGUE X (Phase 1: Touch): Analyzing target_type='{target_type}' "
            f"with lenses={lenses}, passes={passes}. "
            f"Rationale: {config['rationale']}"
        )

        # Support DailyPlanetReport or structured dict extraction
        content_payload = target_data
        if hasattr(target_data, "summary"):
            content_payload = target_data.summary
        elif isinstance(target_data, dict) and "summary" in target_data:
            content_payload = target_data["summary"]

        if self.shiva is not None:
            analysis_report = await self.shiva.execute(
                target_data=content_payload,
                lens_names=lenses,
                passes=passes,
                eam_active=True,
            )
        else:
            # Graceful degradation: no Shiva — produce a stub report for testing
            analysis_report = {
                "status": "SHIVA_UNAVAILABLE_STUB",
                "target_type": target_type,
                "lenses": lenses,
                "passes": passes,
                "results": {"neji": {"raw": str(content_payload)[:512]}},
            }

        return analysis_report

    # ─────────────────────────────────────────────
    #  PHASE 2: THE CONFLICT — TPSL GATING & MAD HATTER
    # ─────────────────────────────────────────────

    def _analyze_conflict(
        self, analysis_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Phase 2 — The Conflict: TPSL Application & Mad Hatter Adversarial Challenge.

        Separates high-W_y concepts ('Power') from high-C_c implementation debt
        ('Psyche') using the TPSL gate: W_y / C_c >= TPSL_GATE (1.0).

        Mad Hatter Protocol: Adversarially inverts each candidate assumption to
        stress-test whether complexity is necessary or can be pruned.

        Kintsugi Interlock: Any concept with Z-score > 3.0 relative to the
        baseline is isolated into the Mirror Maze Sandbox for novel pathway mining
        rather than being discarded.

        Returns:
            Dict with "Power" (retained concepts), "Psyche" (pruned), and
            "mirror_maze" (Kintsugi-isolated anomalies).
        """
        print("ROGUE X (Phase 2: Conflict): Applying TPSL gate and Mad Hatter Protocol.")

        results = analysis_report.get("results", {})
        power: List[Dict[str, Any]] = []
        psyche: List[Dict[str, Any]] = []
        mirror_maze: List[Dict[str, Any]] = []

        # Extract scored concepts from the Shiva report
        # Shiva reports contain nested dicts per Eye pass
        all_concepts: List[Dict[str, Any]] = []
        for eye_name, eye_output in results.items():
            if isinstance(eye_output, dict):
                # Normalize: extract sub-items if they have W_y / C_c fields
                w_y = eye_output.get("w_y", eye_output.get("wisdom_yield", 0.5))
                c_c = eye_output.get("c_c", eye_output.get("cognitive_cost", 0.5))
                all_concepts.append({
                    "eye": eye_name,
                    "content": eye_output,
                    "w_y": float(w_y),
                    "c_c": float(c_c),
                })

        # If no scored concepts exist, treat the entire report as a single Power unit
        if not all_concepts:
            all_concepts = [{
                "eye": "full_report",
                "content": analysis_report,
                "w_y": 0.7,
                "c_c": 0.4,
            }]

        # Compute baseline W_y / C_c for Kintsugi Z-score evaluation
        scores = [c["w_y"] / max(c["c_c"], 0.0001) for c in all_concepts]
        mean_score = sum(scores) / len(scores) if scores else 1.0
        variance = (
            sum((s - mean_score) ** 2 for s in scores) / len(scores)
            if len(scores) > 1 else 0.0001
        )
        std_dev = math.sqrt(variance) if variance > 0 else 0.0001

        for concept, score in zip(all_concepts, scores):
            # Mad Hatter adversarial check: "Is this complexity necessary?"
            mad_hatter_verdict = self._mad_hatter_challenge(concept)

            # Kintsugi Z-score evaluation
            kintsugi_result = self.kintsugi.evaluate_deviation(
                observed_val=score,
                mean_val=mean_score,
                std_dev=std_dev,
                metric_name=f"rogue_x_concept_score_{concept['eye']}",
                context={"eye": concept["eye"], "w_y": concept["w_y"], "c_c": concept["c_c"]},
            )

            enriched = {**concept, "tpsl_score": score, "mad_hatter": mad_hatter_verdict, "kintsugi": kintsugi_result}

            if kintsugi_result["fracture_detected"]:
                # Anomaly — isolate to Mirror Maze, do NOT discard
                mirror_maze.append(enriched)
            elif score >= self.TPSL_GATE and mad_hatter_verdict["verdict"] == "NECESSARY":
                power.append(enriched)
            else:
                psyche.append(enriched)

        print(
            f"ROGUE X (Conflict Result): Power={len(power)}, "
            f"Psyche={len(psyche)}, Mirror Maze={len(mirror_maze)}."
        )

        return {
            "Power": power,
            "Psyche": psyche,
            "mirror_maze": mirror_maze,
            "tpsl_gate": self.TPSL_GATE,
            "kintsugi_alerts": self.kintsugi.alert_count,
        }

    def _mad_hatter_challenge(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mad Hatter Protocol: Non-linear adversarial stress test.

        Inverts the core assumption of each concept to verify whether its
        complexity is genuinely necessary or can be pruned as Psyche.

        Heuristic: W_y >= 0.6 AND C_c <= 0.8 → NECESSARY.
        Otherwise → UNNECESSARY (prune to Psyche).
        """
        w_y = concept.get("w_y", 0.5)
        c_c = concept.get("c_c", 0.5)
        is_necessary = (w_y >= 0.6) and (c_c <= 0.8)
        return {
            "verdict": "NECESSARY" if is_necessary else "UNNECESSARY",
            "inversion": f"If this concept is removed, W_y drops by ~{w_y:.2f} at cost saving of ~{c_c:.2f}.",
            "w_y": w_y,
            "c_c": c_c,
        }

    # ─────────────────────────────────────────────
    #  PHASE 3: THE RELEASE — SEED PACKAGE SYNTHESIS
    # ─────────────────────────────────────────────

    def _create_seed_package(
        self,
        power_vs_psyche: Dict[str, Any],
        target_type: str = "unknown",
        ccid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Phase 3 — The Release: Synthesizes the Seed Package.

        Distills the Power concepts into a structured output containing:
        - Formal definitions extracted from Power items.
        - Mathematical formalisms (where W_y > 0.8).
        - Implementation blueprint for Phoenix Forge integration.
        - Mutation audit record committed to self.mutation_log.

        Args:
            power_vs_psyche: Output of _analyze_conflict().
            target_type: Original target classification string.
            ccid: Optional Cognitive Context ID for traceability.

        Returns:
            Seed package dict ready for Hoard ingestion or Phoenix Forge relay.
        """
        print("ROGUE X (Phase 3: Release): Synthesizing Seed Package.")

        self.mutation_generation += 1
        mutation_id = ccid or f"ROGUE_MUTATION_{self.mutation_generation:04d}_{int(time.time())}"
        created_at = time.time()

        power_items = power_vs_psyche.get("Power", [])
        mirror_maze_items = power_vs_psyche.get("mirror_maze", [])

        # Extract formal definitions from Power
        definitions = [
            {
                "source_eye": item.get("eye", "unknown"),
                "w_y": item.get("w_y", 0.0),
                "c_c": item.get("c_c", 0.0),
                "tpsl_score": item.get("tpsl_score", 0.0),
                "content_summary": str(item.get("content", ""))[:256],
            }
            for item in power_items
        ]

        # Implementation blueprint
        blueprint = {
            "mutation_id": mutation_id,
            "target_type": target_type,
            "generation": self.mutation_generation,
            "power_nodes_absorbed": len(power_items),
            "psyche_nodes_pruned": len(power_vs_psyche.get("Psyche", [])),
            "mirror_maze_isolated": len(mirror_maze_items),
            "sigma_rogue": self.sigma_rogue,
            "mutation_multiplier": round(self.calculate_mutation_multiplier(), 6),
            "definitions": definitions,
            "celestial_stamp": {
                "unix_epoch": created_at,
                "anchor": "Baker, Louisiana",
                "coordinates": "30.5888N, -91.1673W",
            },
        }

        seed_package = {
            "status": "ROGUE_X_SEED_PACKAGE_COMPLETE",
            "mutation_id": mutation_id,
            "generation": self.mutation_generation,
            "synthesis": power_vs_psyche,
            "blueprint": blueprint,
            "timestamp": created_at,
        }

        # Commit to mutation audit log (MTCW reads this)
        self.mutation_log.append({
            "mutation_id": mutation_id,
            "generation": self.mutation_generation,
            "target_type": target_type,
            "power_count": len(power_items),
            "psyche_count": len(power_vs_psyche.get("Psyche", [])),
            "mirror_maze_count": len(mirror_maze_items),
            "kintsugi_alerts": power_vs_psyche.get("kintsugi_alerts", 0),
            "timestamp": created_at,
        })

        print(
            f"ROGUE X (Release Complete): mutation_id={mutation_id}, "
            f"generation={self.mutation_generation}, "
            f"power={len(power_items)}, psyche={len(power_vs_psyche.get('Psyche', []))}, "
            f"mirror_maze={len(mirror_maze_items)}."
        )

        return seed_package

    # ─────────────────────────────────────────────
    #  MASTER LIFECYCLE: execute_absorption()
    # ─────────────────────────────────────────────

    async def execute_absorption(
        self,
        target_data: Any,
        target_type: str = "repository",
        ccid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        The Main Rogue X Workflow: Touch → Conflict → Release.

        Args:
            target_data: The data payload to absorb (repo content, paper text, live feed).
            target_type: Classification key — "repository", "academic_paper",
                         "live_data", or "document". Governs lens selection.
            ccid: Optional Cognitive Context ID for audit trail linkage.

        Returns:
            Fully synthesized seed_package dict.
        """
        # Phase 1: The Touch
        analysis_report = await self._phase_touch(target_data, target_type)

        # Phase 2: The Conflict
        power_vs_psyche = self._analyze_conflict(analysis_report)

        # Phase 3: The Release
        seed_package = self._create_seed_package(power_vs_psyche, target_type, ccid)

        return seed_package

    # ─────────────────────────────────────────────
    #  KINTSUGI INTERLOCK (Direct Access)
    # ─────────────────────────────────────────────

    def _kintsugi_evaluate(
        self,
        observed_val: float,
        mean_val: float,
        std_dev: float,
        metric_name: str = "rogue_x_metric",
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Direct Kintsugi Z-score evaluation interface.
        Exposes Kintsugi as a callable from RogueX for external test verification.
        """
        return self.kintsugi.evaluate_deviation(
            observed_val=observed_val,
            mean_val=mean_val,
            std_dev=std_dev,
            metric_name=metric_name,
            context=context or {},
        )

    # ─────────────────────────────────────────────
    #  MATH ENGINE (Preserved Canonical Formulas)
    # ─────────────────────────────────────────────

    def calculate_mutation_multiplier(self) -> float:
        """σ_Rogue mutation multiplier: e^(sigma_rogue)."""
        return math.exp(self.sigma_rogue)

    def inject_adversarial_perturbation(self, base_vector: list) -> list:
        """
        Applies the mutation multiplier to a base vector.
        Preserved for backward compatibility and Phoenix Forge integration.
        """
        mult = self.calculate_mutation_multiplier()
        return [v * mult for v in base_vector]

    # ─────────────────────────────────────────────
    #  TELEMETRY & PROTOCOL STATUS
    # ─────────────────────────────────────────────

    @property
    def is_active(self) -> bool:
        """Rogue X 2.0 mutation engine is always active."""
        return True

    def verify_true(self) -> bool:
        """Returns True asserting Rogue X 2.0 active status."""
        return True

    def verify_status(self) -> Dict[str, Any]:
        """Returns full telemetry for system audit. Backward-compatible with existing tests."""
        return {
            "protocol": "ROGUE_X",
            "version": "2.0-PURPLE",
            "is_active": True,
            "status": "ACTIVE_MUTATION_ENABLED",
            "sigma_rogue": self.sigma_rogue,
            "mutation_multiplier": round(self.calculate_mutation_multiplier(), 6),
            "mutation_generation": self.mutation_generation,
            "mutation_log_depth": len(self.mutation_log),
            "kintsugi_sandbox_depth": self.kintsugi.sandbox_depth(),
            "kintsugi_alerts": self.kintsugi.alert_count,
            "all_systems_true": True,
        }
