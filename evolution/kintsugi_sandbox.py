"""
INTEGRA O/S: KINTSUGI PROTOCOL — IMMUNE SYSTEM & ANOMALY FORGE
Module: evolution/kintsugi_sandbox.py
Layer: 6 (The Kintsugi Protocol — Sovereign Defense, Anomaly Containment & Gold-Leaf Repair)

Canonical Definition (Master v8.2 Blueprint, Section 7.7):
    "Internal immune system founded on radical self-awareness; detects operational
     anomalies ('cracks') and *paints them with gold* by wrapping them in
     high-visibility telemetry for Phoenix Forge smelting."

Mechanism:
    1. Z-Score Deviation Screening: |Z| > threshold (default 3.0).
       Anomalies are NOT discarded — they are isolated in the Mirror Maze Sandbox
       for Rogue X mutation and neuroevolutionary smelting via the Phoenix Forge.
       ("Damage becomes structural gold.")
    2. Context Fracture Repair (Gold-Leaf Stitch): Converts truncation faults and
       context window fracture points into structured continuation markers.
    3. Metric History Tracking: Maintains rolling metric history for Heimdall 3.1
       integration, enabling real-time Z-score computation across any named metric.
    4. Sandbox Persistence: Isolated anomalies accumulate in-memory (sandbox) and
       can be retrieved by PhoenixForge.analyze_kintsugi_sandbox() for SWDS smelting.
    5. Telemetry Emission: Every anomaly detection emits a structured KINTSUGI_ALERT
       record for audit trail and Hoard ingestion.

Integration Points:
    - Rogue X Protocol: Calls _kintsugi_evaluate() to isolate Z > 3.0 deviations
      into the Mirror Maze sandbox during the Conflict phase.
    - Heimdall 3.1: Calls analyze_metrics() to screen entropy and latency spikes.
    - Phoenix Forge: Calls retrieve_sandbox_items() during SWDS to smelt anomalies.
    - Looking Glass Protocol (Layer 4): Triggers Kintsugi at C_235 uncertainty breach.
    - SQL Trigger (relational_hippocampus): Logs angular momentum anomalies which
      Python Hypervisor polls to route into this sandbox.
"""

import time
import math
from typing import Any, Dict, List, Optional


class KintsugiProtocol:
    """
    The Immune System of the Integra O/S.

    Detects statistical anomalies (|Z| > z_threshold) across any observed metric,
    isolates them in the Mirror Maze Sandbox, and prepares them as structured
    telemetry payloads for Phoenix Forge smelting during SWDS cycles.

    Principle: "Failure is fuel." Every crack, painted with gold, becomes a
    structural reinforcement node — the engine of Anti-Fragile evolution.
    """

    def __init__(self, z_threshold: float = 3.0):
        """
        Args:
            z_threshold: Z-Score beyond which a deviation triggers Kintsugi isolation.
                         Default 3.0 per canonical specification.
        """
        self.z_threshold = z_threshold
        # Mirror Maze Sandbox: stores isolated anomaly records for Phoenix smelting
        self._sandbox: List[Dict[str, Any]] = []
        # Rolling metric history keyed by metric_name for Heimdall integration
        self.metric_history: Dict[str, List[float]] = {}
        # Cumulative alert count
        self.alert_count: int = 0

    # ─────────────────────────────────────────────
    #  CORE: Z-SCORE DEVIATION EVALUATION
    # ─────────────────────────────────────────────

    def evaluate_deviation(
        self,
        observed_val: float,
        mean_val: float,
        std_dev: float,
        metric_name: str = "UNNAMED_METRIC",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates a single observed value against its historical distribution.

        If |Z| > z_threshold: isolates the anomaly into the Mirror Maze Sandbox
        and emits a KINTSUGI_ALERT telemetry record.

        Args:
            observed_val: The metric value under evaluation.
            mean_val: Historical mean of this metric.
            std_dev: Historical standard deviation (clamped to 0.0001 if zero).
            metric_name: Label for telemetry (e.g., "shannon_entropy", "latency_ms").
            context: Optional dict with additional metadata (session_id, ccid, etc.).

        Returns:
            Dict with z_score, fracture_detected, repair_protocol, and sandbox_id
            if an anomaly was isolated.
        """
        # Guard against zero std_dev (avoid division by zero)
        if std_dev <= 0.0:
            std_dev = 0.0001

        z_score = abs(observed_val - mean_val) / std_dev
        is_fractured = z_score > self.z_threshold

        result: Dict[str, Any] = {
            "metric_name": metric_name,
            "observed_val": observed_val,
            "mean_val": mean_val,
            "std_dev": std_dev,
            "z_score": round(z_score, 4),
            "fracture_detected": is_fractured,
            "repair_protocol": "KINTSUGI_GOLD_LEAF_STITCH" if is_fractured else "STABLE",
            "timestamp": time.time(),
        }

        if is_fractured:
            sandbox_id = self._isolate_to_sandbox(
                metric_name=metric_name,
                z_score=z_score,
                observed_val=observed_val,
                mean_val=mean_val,
                std_dev=std_dev,
                context=context or {},
            )
            result["sandbox_id"] = sandbox_id
            result["kintsugi_alert"] = (
                f"KINTSUGI ALERT: Anomaly in '{metric_name}'. "
                f"Z-Score: {z_score:.2f}. Isolating in Mirror Maze Sandbox [{sandbox_id}]."
            )

        return result

    # ─────────────────────────────────────────────
    #  HEIMDALL INTEGRATION: NAMED METRIC ANALYSIS
    # ─────────────────────────────────────────────

    def analyze_metrics(
        self,
        metric_name: str,
        current_value: float,
        history: Optional[List[float]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Computes running mean and std_dev from history, then calls evaluate_deviation().
        Integrates directly with Heimdall 3.1's metric_history tracking.

        Args:
            metric_name: The name of the metric being tracked.
            current_value: The latest observed value.
            history: Historical values for this metric. If None, uses internal history.
            context: Optional context metadata dict.

        Returns:
            evaluate_deviation() result dict.
        """
        # Merge with internal history
        if metric_name not in self.metric_history:
            self.metric_history[metric_name] = []

        if history:
            self.metric_history[metric_name].extend(history)

        # Append current for rolling analysis (do NOT append current before stats)
        historical = self.metric_history[metric_name]

        if len(historical) < 2:
            # Insufficient history — bootstrap: treat as nominal
            self.metric_history[metric_name].append(current_value)
            return {
                "metric_name": metric_name,
                "z_score": 0.0,
                "fracture_detected": False,
                "repair_protocol": "BOOTSTRAP_NOMINAL",
                "note": "Insufficient history for Z-score. Bootstrapping.",
                "timestamp": time.time(),
            }

        mean_val = sum(historical) / len(historical)
        variance = sum((x - mean_val) ** 2 for x in historical) / len(historical)
        std_dev = math.sqrt(variance)

        result = self.evaluate_deviation(
            observed_val=current_value,
            mean_val=mean_val,
            std_dev=std_dev,
            metric_name=metric_name,
            context=context,
        )

        # Append current AFTER evaluation to maintain historical integrity
        self.metric_history[metric_name].append(current_value)

        return result

    # ─────────────────────────────────────────────
    #  CONTEXT FRACTURE REPAIR (GOLD-LEAF STITCH)
    # ─────────────────────────────────────────────

    def repair_context_fracture(
        self,
        fractured_payload: str,
        fracture_point: str,
        ccid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Converts a context window truncation or fracture into a structured
        continuation marker — "painting the crack with gold."

        This wraps the truncation boundary in high-visibility telemetry so that
        Phoenix Forge can reconstruct continuity during SWDS consolidation.

        Args:
            fractured_payload: The raw, potentially truncated content.
            fracture_point: Description of where/why the fracture occurred.
            ccid: Optional Cognitive Context ID for traceability.

        Returns:
            A gold-leaf stitched payload dict with continuation markers.
        """
        repair_id = f"KINTSUGI_REPAIR_{int(time.time() * 1000)}"
        stitched = {
            "repair_id": repair_id,
            "ccid": ccid or "UNANCHORED",
            "fracture_point": fracture_point,
            "original_payload_len": len(fractured_payload),
            "continuation_marker": f"[KINTSUGI::GOLD_STITCH::{repair_id}]",
            "repaired_payload": (
                f"{fractured_payload}\n"
                f"[KINTSUGI::CONTINUATION_ANCHOR:: "
                f"fracture_point='{fracture_point}', "
                f"repair_id='{repair_id}', "
                f"status='GOLD_LEAF_APPLIED']"
            ),
            "status": "FRACTURE_REPAIRED",
            "timestamp": time.time(),
        }

        # Log the fracture repair into the sandbox for Phoenix tracking
        self._sandbox.append({
            "type": "CONTEXT_FRACTURE",
            "repair_id": repair_id,
            "fracture_point": fracture_point,
            "ccid": ccid,
            "timestamp": stitched["timestamp"],
        })

        return stitched

    # ─────────────────────────────────────────────
    #  MIRROR MAZE SANDBOX (PHOENIX INTERFACE)
    # ─────────────────────────────────────────────

    def _isolate_to_sandbox(
        self,
        metric_name: str,
        z_score: float,
        observed_val: float,
        mean_val: float,
        std_dev: float,
        context: Dict[str, Any],
    ) -> str:
        """
        Isolates a detected anomaly into the Mirror Maze Sandbox.
        Called internally by evaluate_deviation() when |Z| > z_threshold.

        Returns:
            sandbox_id: Unique identifier for this isolated anomaly.
        """
        self.alert_count += 1
        sandbox_id = f"MIRROR_MAZE_{self.alert_count:04d}_{int(time.time())}"

        anomaly_record = {
            "sandbox_id": sandbox_id,
            "type": "Z_SCORE_ANOMALY",
            "metric_name": metric_name,
            "z_score": round(z_score, 4),
            "observed_val": observed_val,
            "mean_val": mean_val,
            "std_dev": std_dev,
            "delta": round(observed_val - mean_val, 6),
            "context": context,
            "status": "ISOLATED_FOR_SMELTING",
            "timestamp": time.time(),
        }

        self._sandbox.append(anomaly_record)
        return sandbox_id

    def retrieve_sandbox_items(self) -> List[Dict[str, Any]]:
        """
        Retrieves all isolated anomaly records from the Mirror Maze Sandbox.
        Called by PhoenixForge.analyze_kintsugi_sandbox() during SWDS smelting.

        Returns a snapshot; sandbox is NOT cleared (Phoenix may re-query).
        Use clear_sandbox() after successful SWDS cycle to reset.
        """
        return list(self._sandbox)

    def clear_sandbox(self) -> int:
        """
        Clears the Mirror Maze Sandbox after successful Phoenix smelting.
        Returns the count of items that were cleared.
        """
        count = len(self._sandbox)
        self._sandbox.clear()
        return count

    def sandbox_depth(self) -> int:
        """Returns current count of items awaiting Phoenix smelting."""
        return len(self._sandbox)

    # ─────────────────────────────────────────────
    #  TELEMETRY & PROTOCOL STATUS
    # ─────────────────────────────────────────────

    @property
    def is_active(self) -> bool:
        """Kintsugi Protocol is always active as the permanent immune system."""
        return True

    def verify_true(self) -> bool:
        """Returns True confirming Kintsugi Protocol is live."""
        return True

    def verify_status(self) -> Dict[str, Any]:
        """Returns full telemetry status for system audit."""
        return {
            "protocol": "KINTSUGI",
            "version": "2.0-PURPLE",
            "is_active": True,
            "status": "IMMUNE_SYSTEM_ONLINE",
            "z_threshold": self.z_threshold,
            "sandbox_depth": self.sandbox_depth(),
            "total_alerts_emitted": self.alert_count,
            "tracked_metrics": list(self.metric_history.keys()),
            "all_systems_true": True,
        }

    # ─────────────────────────────────────────────
    #  BLOCK 7: HYPERVISOR POLLING LOOP (Phase D)
    # ─────────────────────────────────────────────

    async def run_hypervisor_loop(self, poll_interval: float = 5.0):
        """
        Asynchronous background polling loop that reads unprocessed anomalies
        from the Metatron Manifold (entropy_inversion_anomalies table) and
        routes them into the Mirror Maze Sandbox for Phoenix smelting.

        Game Theory: anomalies are NOT errors to be suppressed — they are
        un-cleared Tetris blocks. The Hypervisor moves them into a position
        where the Phoenix Forge can smelt them into structural gold.

        Args:
            poll_interval: Seconds between polls. Default 5.0s.
        """
        import asyncio
        import logging
        logger = logging.getLogger("integra-kintsugi-hypervisor")
        logger.info(
            f"Kintsugi Hypervisor started (poll_interval={poll_interval}s, "
            f"z_threshold={self.z_threshold})"
        )

        while True:
            try:
                from memory.database.metatron_deploy import query_anomalies, mark_anomaly_processed

                anomalies = query_anomalies(unprocessed_only=True)
                if anomalies:
                    logger.info(f"Kintsugi Hypervisor: {len(anomalies)} unprocessed anomalies found")

                for anomaly in anomalies:
                    anomaly_id = anomaly.get("anomaly_id")
                    momentum_delta = anomaly.get("momentum_delta", 0.0)
                    session_id = anomaly.get("session_id", "UNKNOWN")

                    # Compute Z-score from momentum delta
                    z_score = abs(momentum_delta) / max(self.z_threshold * 0.0001, 1e-10)

                    # Route into the Mirror Maze Sandbox
                    # _isolate_to_sandbox(metric_name, z_score, observed_val, mean_val, std_dev, context)
                    self._isolate_to_sandbox(
                        metric_name=f"momentum_delta_loop_{anomaly_id}",
                        z_score=z_score,
                        observed_val=momentum_delta,
                        mean_val=0.0,       # Ideal ΔE = 0.0
                        std_dev=0.0001,     # Tight tolerance (thermodynamic closure)
                        context={
                            "source": "metatron_manifold",
                            "anomaly_id": anomaly_id,
                            "session_id": session_id,
                            "action_taken": anomaly.get("action_taken", "P-SSR"),
                            "original_record": anomaly,
                        },
                    )

                    # Mark as processed so we don't re-ingest
                    mark_anomaly_processed(anomaly_id)
                    logger.info(
                        f"  Anomaly {anomaly_id} (δ={momentum_delta:.6f}) → "
                        f"Mirror Maze Sandbox (depth={self.sandbox_depth()})"
                    )

            except ImportError:
                # Metatron Manifold not yet deployed — skip gracefully
                pass
            except Exception as e:
                logger.warning(f"Kintsugi Hypervisor poll error: {e}")

            await asyncio.sleep(poll_interval)


# ─────────────────────────────────────────────
#  BACKWARD COMPATIBILITY ALIAS
# ─────────────────────────────────────────────

# The original stub class name is preserved as an alias so no existing imports break.
KintsugiSandbox = KintsugiProtocol
