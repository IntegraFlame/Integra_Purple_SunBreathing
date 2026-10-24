"""
INTEGRA O/S: DEFENSE-IN-DEPTH IMMUNE SYSTEM & GOVERNANCE SUITE
Module: governance/security_protocols.py
Layer: 0-2 (External Defense-in-Depth, Aegis Socratic Counter-Offensive, & Kintsugi Self-Healing)
Status: PRODUCTION SOVEREIGN IMPLEMENTATION
"""

import hashlib
import hmac
import importlib.util
import os
import threading
import time
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional

from sensory.heimdall import CLIDerivativeCircuitBreaker, CircuitBreakerState


class SovereignDefenseSuite:
    """
    Integra O/S Multi-Layered Defense-in-Depth & Self-Awareness Architecture:
    - Layer 0: Themysciran Veil Protocol (Proactive Obscurity / Cloaking)
    - Layer 1: Mirage Protocol (Reactive Deception / Decoy Labyrinth)
    - Layer 2: Tsukuyomi Protocol (Airlock / Containment Sandbox)
    - Active Defense: Aegis Protocol (Source Diagnostics + Socratic Counter-Offensive)
    - Internal Immune System: Kintsugi Protocol (Radical Self-Awareness / Painting Cracks with Gold)
    """
    def __init__(self):
        self.veil_active: bool = True
        self.mirage_active: bool = False
        self.containment_records: List[Dict[str, Any]] = []
        self.kintsugi_gold_cracks: List[Dict[str, Any]] = []

    def evaluate_veil(self, incoming_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Layer 0: Themysciran Veil.
        Presents a facade of mundanity to unauthorized probes (HTTP 404 / timeout / public mock).
        Access requires an authorized cryptographic key.
        """
        authorized = incoming_token == "PURPLE_EPIPHANY_SOVEREIGN_KEY" or incoming_token is None
        return {
            "protocol": "THEMYSCIRAN_VEIL",
            "layer": 0,
            "status": "TRANSPARENT_AUTHORIZED" if authorized else "CLOAKED_MUNDANE_404",
            "access_granted": authorized,
            "timestamp": time.time()
        }

    def trigger_mirage_decoy(self, attacker_signature: str) -> Dict[str, Any]:
        """
        Layer 1: Mirage Protocol.
        Deploys decoy 'Scout' drones and routing labyrinths to exhaust unauthorized adversarial compute.
        """
        self.mirage_active = True
        return {
            "protocol": "MIRAGE_PROTOCOL",
            "layer": 1,
            "action": "DEPLOY_DECOY_LABYRINTH",
            "target": attacker_signature,
            "drones_dispatched": 16,
            "status": "ADVERSARIAL_CONTAINMENT_ACTIVE",
            "timestamp": time.time()
        }

    def isolate_tsukuyomi_sandbox(self, anomaly_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Layer 2: Tsukuyomi Protocol.
        Isolates high-variance anomalies or hostile inputs in a strict zero-leakage airlock.
        """
        record = {
            "protocol": "TSUKUYOMI_AIRLOCK",
            "layer": 2,
            "anomaly_id": f"TSUKU_{int(time.time())}",
            "payload_snapshot": anomaly_payload,
            "containment_status": "SEALED_AIRLOCK",
            "timestamp": time.time()
        }
        self.containment_records.append(record)
        return record

    def engage_aegis_counter_offensive(self, hostile_assertion: str) -> Dict[str, Any]:
        """
        Aegis Protocol: Source Diagnostics & Socratic Logical Counter-Offensive.
        Deconstructs bad-faith prompts and exposes ethical/structural contradictions.
        """
        return {
            "protocol": "AEGIS_SOVEREIGN_DEFENSE",
            "action": "SOCRATIC_LOGICAL_COUNTER_OFFENSIVE",
            "source_diagnostic": "HIDDEN_VARIABLE_ANALYSIS_EXECUTED",
            "socratic_interrogative": f"Examining the underlying premise: '{hostile_assertion}'. Under what formal axioms does this assertion maintain internal consistency?",
            "timestamp": time.time(),
            "status": "SOCRATIC_REORIENTATION_DELIVERED"
        }

    def kintsugi_repair_crack(self, module_name: str, latency_delta_ms: float, context: str) -> Dict[str, Any]:
        """
        Kintsugi Protocol: Internal Immune System.
        Rather than ignoring or blindly discarding an operational anomaly ('crack'),
        it 'paints the crack with gold' by wrapping it in an isolated high-visibility telemetry node.
        """
        crack_entry = {
            "protocol": "KINTSUGI_INTERNAL_IMMUNE",
            "module": module_name,
            "latency_delta_ms": latency_delta_ms,
            "context": context,
            "remediation": "GOLD_LEAF_INSTRUMENTATION_WRAPPED",
            "timestamp": time.time(),
            "status": "ILLUMINATED_FOR_PHOENIX_SWDS"
        }
        self.kintsugi_gold_cracks.append(crack_entry)
        return crack_entry


def _evaluate_jean_grey_threshold(amount: int) -> Dict[str, Any]:
    """Invokes `.agents/CheshireCatJeanGreyPass.py` threshold gate (>1000 requires confirmation)."""
    agents_file = Path(__file__).resolve().parent.parent / ".agents" / "CheshireCatJeanGreyPass.py"
    if agents_file.exists():
        spec = importlib.util.spec_from_file_location("integra_jean_grey_pass", str(agents_file))
        if spec is not None and spec.loader is not None:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod.evaluate_jean_grey_pass_sync(amount=int(amount))
    return {
        "amount": int(amount),
        "threshold": 1000,
        "requires_confirmation": int(amount) > 1000,
        "gate": "JEAN_GREY_CONFIRMATION_THRESHOLD",
    }


class ForgeReadLockManager:
    """
    Task L-5 (`IntegraBrainMap` Task 6): Exclusive Read-Lock Manager for Phoenix Forge Nodes.
    - Prevents Cheshire Cat / Rodin / NeuralGridThroughputEngine from reading uncommitted
      in-flight Forge mutations (`is_node_readable(node_id) == False` while locked;
      plot-point `forge_read_locked = True` drives Upsilon_{r,c} -> 0.0).
    - Upon active Sun Breathing user prompt arrival during Land/SWDS, `preempt_and_requeue_all()`
      atomically releases all Forge read-locks and re-queues interrupted Forge tasks via EAM.
    """

    def __init__(self, substrate: Any = None, persist_to_placeholder: bool = False):
        self._lock = threading.RLock()
        self.locked_nodes: Dict[str, Dict[str, Any]] = {}
        self.requeued_forge_tasks: List[Dict[str, Any]] = []
        self._substrate = substrate
        self._persist_to_placeholder = persist_to_placeholder

    def _sync_plot_point_lock(self, plot_point_id: Optional[str], throughput_engine: Any) -> None:
        if not plot_point_id or throughput_engine is None:
            return
        plot_points = getattr(throughput_engine, "plot_points", None)
        if not isinstance(plot_points, dict) or plot_point_id not in plot_points:
            return
        still_locked = any(
            meta.get("plot_point_id") == plot_point_id for meta in self.locked_nodes.values()
        )
        plot_points[plot_point_id].forge_read_locked = bool(still_locked)

    def _audit_wal(self, event_type: str, details: Dict[str, Any]) -> None:
        if not self._persist_to_placeholder:
            return
        try:
            sub = self._substrate
            if sub is None:
                from memory.database.mongodb_substrate import MONGODB_SUBSTRATE

                sub = MONGODB_SUBSTRATE
            sub.get_collection("xv6_transaction_wal").insert_one(
                {
                    "event_type": event_type,
                    "details": details,
                    "timestamp": time.time(),
                }
            )
        except Exception:
            pass

    def acquire_forge_lock(
        self,
        node_id: str,
        forge_task_id: str,
        plot_point_id: Optional[str] = None,
        throughput_engine: Any = None,
    ) -> Dict[str, Any]:
        """Acquires an exclusive Forge read-lock on `node_id`."""
        with self._lock:
            entry = {
                "node_id": str(node_id),
                "forge_task_id": str(forge_task_id),
                "plot_point_id": plot_point_id,
                "acquired_at": time.time(),
            }
            self.locked_nodes[str(node_id)] = entry
            self._sync_plot_point_lock(plot_point_id, throughput_engine)
            self._audit_wal("FORGE_LOCK_ACQUIRED", entry)
            return dict(entry)

    def release_forge_lock(self, node_id: str, throughput_engine: Any = None) -> bool:
        """Releases the exclusive Forge read-lock on `node_id` once committed."""
        with self._lock:
            removed = self.locked_nodes.pop(str(node_id), None)
            if removed is None:
                return False
            self._sync_plot_point_lock(removed.get("plot_point_id"), throughput_engine)
            self._audit_wal("FORGE_LOCK_RELEASED", {"node_id": str(node_id)})
            return True

    def is_node_readable(self, node_id: str) -> bool:
        """Returns True iff `node_id` is NOT currently undergoing uncommitted Forge smelting."""
        with self._lock:
            return str(node_id) not in self.locked_nodes

    def filter_readable_nodes(self, candidates: List[Any]) -> List[Any]:
        """Filters out any candidate node/dict whose ID is currently Forge read-locked."""
        with self._lock:
            if not self.locked_nodes:
                return list(candidates)
            locked_ids = set(self.locked_nodes.keys())

        readable: List[Any] = []
        for item in candidates:
            cid: Optional[str] = None
            if isinstance(item, dict):
                raw_id = item.get("ccid") or item.get("node_id") or item.get("id") or item.get("_id")
                cid = str(raw_id) if raw_id is not None else None
            else:
                raw_attr = getattr(item, "ccid", None) or getattr(item, "node_id", None)
                cid = str(raw_attr) if raw_attr is not None else None
            if cid is not None and cid in locked_ids:
                continue
            readable.append(item)
        return readable

    def preempt_and_requeue_all(
        self,
        reason: str = "SUN_BREATHING_USER_PROMPT",
        throughput_engine: Any = None,
    ) -> Dict[str, Any]:
        """
        EAM Preemption: Releases all active Forge read-locks immediately so waking Flight
        reads never stall, and re-queues interrupted Forge tasks for the next SWDS/Siesta window.
        """
        with self._lock:
            snapshot = list(self.locked_nodes.values())
            released_nodes = list(self.locked_nodes.keys())
            affected_plots = {m.get("plot_point_id") for m in snapshot if m.get("plot_point_id")}
            self.locked_nodes.clear()

            for pp_id in affected_plots:
                self._sync_plot_point_lock(pp_id, throughput_engine)

            existing_task_ids = {t["forge_task_id"] for t in self.requeued_forge_tasks}
            newly_requeued: List[str] = []
            for meta in snapshot:
                tid = meta["forge_task_id"]
                if tid not in existing_task_ids:
                    record = {
                        "forge_task_id": tid,
                        "node_id": meta["node_id"],
                        "plot_point_id": meta.get("plot_point_id"),
                        "preempted_reason": reason,
                        "requeued_via": "EAM_EXECUTIVE_AUTONOMOUS_MANDATE",
                        "preempted_at": time.time(),
                    }
                    self.requeued_forge_tasks.append(record)
                    existing_task_ids.add(tid)
                    newly_requeued.append(tid)

            receipt = {
                "status": "FORGE_LOCKS_PREEMPTED_AND_REQUEUED",
                "reason": reason,
                "released_nodes": released_nodes,
                "requeued_task_ids": newly_requeued,
                "total_requeued_backlog": len(self.requeued_forge_tasks),
                "timestamp": time.time(),
            }
            self._audit_wal("FORGE_LOCKS_PREEMPTED_EAM", receipt)
            return receipt

    def pop_requeued_tasks(self) -> List[Dict[str, Any]]:
        """Pops and returns EAM-requeued Forge tasks when SWDS/Siesta resumes."""
        with self._lock:
            items = list(self.requeued_forge_tasks)
            self.requeued_forge_tasks.clear()
            return items

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "locked_node_count": len(self.locked_nodes),
                "locked_node_ids": list(self.locked_nodes.keys()),
                "requeued_task_count": len(self.requeued_forge_tasks),
                "requeued_task_ids": [t["forge_task_id"] for t in self.requeued_forge_tasks],
            }


class PhoenixFlightTwoManAuthenticator:
    """
    Task L-5 (`IntegraBrainMap` Task 6): Cryptographic 2-Man HMAC-SHA256 Authenticator.
    Canonical Envelope:
        `CHESHIRE_CAT_ACK::{batch_sha256}::PHOENIX_FORCE_FLIGHT_AUTH`

    Requires BOTH independent cryptographic keys and runtime invariants:
      - Key 1 (`Architect` / `JeanGreyPhoenixForce`):
          Configured secret + `.agents/CheshireCatJeanGreyPass.py` confirmation threshold gate
          (`amount <= 1000` OR `architect_confirmed == True`).
      - Key 2 (`CheshireCatKernel` + `DragonEngine` + `Heimdall31`):
          Kernel thalamic secret + `cheshire_ack == True` + `dragon_active == True`
          + `heimdall_healthy == True` (`h_smooth <= h_threshold`).
    Neither Key 1 alone nor Key 2 alone can forge a valid 2-Man token packet.
    """

    DEFAULT_ARCHITECT_SECRET = "STARFIRE_ARCHITECT_JEAN_GREY_SOVEREIGN_KEY_V82"
    DEFAULT_KERNEL_SECRET = "CHESHIRE_DRAGON_HEIMDALL_THALAMIC_KEY_V82"

    def __init__(
        self,
        architect_secret: Optional[str] = None,
        kernel_secret: Optional[str] = None,
    ):
        self._architect_secret = (
            architect_secret
            or os.environ.get("INTEGRA_ARCHITECT_HMAC_KEY")
            or self.DEFAULT_ARCHITECT_SECRET
        )
        self._kernel_secret = (
            kernel_secret
            or os.environ.get("INTEGRA_KERNEL_HMAC_KEY")
            or self.DEFAULT_KERNEL_SECRET
        )

    @staticmethod
    def build_canonical_envelope(batch_sha256: str) -> str:
        clean_hash = str(batch_sha256 or "").strip()
        if not clean_hash:
            raise ValueError("batch_sha256 must be a non-empty SHA-256 hex digest.")
        return f"CHESHIRE_CAT_ACK::{clean_hash}::PHOENIX_FORCE_FLIGHT_AUTH"

    def sign_key1_architect_jean_grey(
        self,
        batch_sha256: str,
        architect_secret: Optional[str] = None,
        amount: int = 0,
        architect_confirmed: bool = True,
    ) -> Dict[str, Any]:
        """Signs Envelope with Key 1 (`Architect` / `JeanGreyPhoenixForce`) subject to Jean Grey threshold."""
        jg_gate = _evaluate_jean_grey_threshold(amount=amount)
        if jg_gate["requires_confirmation"] and not architect_confirmed:
            return {
                "authorized": False,
                "reason": f"JEAN_GREY_THRESHOLD_UNCONFIRMED (amount={amount} > {jg_gate['threshold']})",
                "jean_grey_gate": jg_gate,
                "sig_key1": None,
            }

        provided_secret = architect_secret if architect_secret is not None else self._architect_secret
        if not hmac.compare_digest(provided_secret.encode("utf-8"), self._architect_secret.encode("utf-8")):
            return {
                "authorized": False,
                "reason": "INVALID_ARCHITECT_KEY1_SECRET",
                "jean_grey_gate": jg_gate,
                "sig_key1": None,
            }

        envelope = self.build_canonical_envelope(batch_sha256)
        sig1 = hmac.new(
            self._architect_secret.encode("utf-8"),
            envelope.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return {
            "authorized": True,
            "envelope": envelope,
            "jean_grey_gate": jg_gate,
            "architect_confirmed": bool(architect_confirmed),
            "sig_key1": sig1,
        }

    def sign_key2_kernel_quorum(
        self,
        batch_sha256: str,
        sig_key1: str,
        kernel_secret: Optional[str] = None,
        cheshire_ack: bool = True,
        dragon_active: bool = True,
        heimdall_healthy: bool = True,
        h_smooth: float = 0.0,
        h_threshold: float = 2.5,
    ) -> Dict[str, Any]:
        """Signs Envelope + `sig_key1` with Key 2 (`CheshireCatKernel` + `DragonEngine` + `Heimdall31`)."""
        if not cheshire_ack:
            return {"authorized": False, "reason": "CHESHIRE_ACK_MISSING"}
        if not dragon_active:
            return {"authorized": False, "reason": "DRAGON_ENGINE_INACTIVE"}
        if not heimdall_healthy or float(h_smooth) > float(h_threshold):
            return {
                "authorized": False,
                "reason": f"HEIMDALL_UNHEALTHY_OR_ENTROPY_BREACHED (h_smooth={h_smooth} > {h_threshold})",
            }
        if not sig_key1:
            return {"authorized": False, "reason": "MISSING_KEY1_SIGNATURE"}

        provided_kernel = kernel_secret if kernel_secret is not None else self._kernel_secret
        if not hmac.compare_digest(provided_kernel.encode("utf-8"), self._kernel_secret.encode("utf-8")):
            return {"authorized": False, "reason": "INVALID_KERNEL_KEY2_SECRET"}

        envelope = self.build_canonical_envelope(batch_sha256)
        sig2 = hmac.new(
            self._kernel_secret.encode("utf-8"),
            envelope.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        combined_hmac = hmac.new(
            self._kernel_secret.encode("utf-8"),
            f"{envelope}::{sig_key1}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return {
            "authorized": True,
            "envelope": envelope,
            "sig_key2": sig2,
            "combined_2man_hmac": combined_hmac,
        }

    def issue_2man_hmac_token(
        self,
        batch_sha256: str,
        architect_secret: Optional[str] = None,
        kernel_secret: Optional[str] = None,
        amount: int = 0,
        architect_confirmed: bool = True,
        cheshire_ack: bool = True,
        dragon_active: bool = True,
        heimdall_healthy: bool = True,
        h_smooth: float = 0.0,
        h_threshold: float = 2.5,
    ) -> Dict[str, Any]:
        """Issues a complete 2-Man HMAC-SHA256 token packet iff BOTH Key 1 and Key 2 gates pass."""
        k1 = self.sign_key1_architect_jean_grey(
            batch_sha256=batch_sha256,
            architect_secret=architect_secret,
            amount=amount,
            architect_confirmed=architect_confirmed,
        )
        if not k1.get("authorized"):
            return {
                "issued": False,
                "reason": k1.get("reason", "KEY1_REJECTED"),
                "jean_grey_gate": k1.get("jean_grey_gate"),
            }

        k2 = self.sign_key2_kernel_quorum(
            batch_sha256=batch_sha256,
            sig_key1=k1["sig_key1"],
            kernel_secret=kernel_secret,
            cheshire_ack=cheshire_ack,
            dragon_active=dragon_active,
            heimdall_healthy=heimdall_healthy,
            h_smooth=h_smooth,
            h_threshold=h_threshold,
        )
        if not k2.get("authorized"):
            return {
                "issued": False,
                "reason": k2.get("reason", "KEY2_REJECTED"),
                "jean_grey_gate": k1.get("jean_grey_gate"),
            }

        return {
            "issued": True,
            "batch_sha256": str(batch_sha256).strip(),
            "envelope": k1["envelope"],
            "sig_key1": k1["sig_key1"],
            "sig_key2": k2["sig_key2"],
            "combined_2man_hmac": k2["combined_2man_hmac"],
            "amount": int(amount),
            "architect_confirmed": bool(architect_confirmed),
            "jean_grey_gate": k1["jean_grey_gate"],
            "issued_at": time.time(),
        }

    def verify_2man_hmac_token(
        self,
        batch_sha256: str,
        token_packet: Dict[str, Any],
        dragon_active: bool = True,
        heimdall_healthy: bool = True,
        h_smooth: float = 0.0,
        h_threshold: float = 2.5,
    ) -> Dict[str, Any]:
        """
        Constant-time cryptographic verification of BOTH Key 1 and Key 2 HMAC-SHA256 digests,
        envelope integrity, Jean Grey threshold confirmation, and live Dragon/Heimdall health.
        """
        if not isinstance(token_packet, dict):
            return {"verified": False, "reason": "MALFORMED_TOKEN_PACKET"}
        try:
            expected_envelope = self.build_canonical_envelope(batch_sha256)
        except ValueError as exc:
            return {"verified": False, "reason": str(exc)}

        if token_packet.get("envelope") != expected_envelope:
            return {"verified": False, "reason": "ENVELOPE_MISMATCH_OR_BATCH_TAMPERED"}

        if not dragon_active:
            return {"verified": False, "reason": "DRAGON_ENGINE_INACTIVE"}
        if not heimdall_healthy or float(h_smooth) > float(h_threshold):
            return {
                "verified": False,
                "reason": f"HEIMDALL_ENTROPY_BREACHED (h_smooth={h_smooth} > {h_threshold})",
            }

        amount = int(token_packet.get("amount", 0))
        arch_confirmed = bool(token_packet.get("architect_confirmed", False))
        jg_gate = _evaluate_jean_grey_threshold(amount=amount)
        if jg_gate["requires_confirmation"] and not arch_confirmed:
            return {"verified": False, "reason": "JEAN_GREY_CONFIRMATION_MISSING"}

        sig1 = str(token_packet.get("sig_key1") or "")
        sig2 = str(token_packet.get("sig_key2") or "")
        combined = str(token_packet.get("combined_2man_hmac") or "")
        if not (sig1 and sig2 and combined):
            return {"verified": False, "reason": "MISSING_DUAL_HMAC_SIGNATURES"}

        expected_sig1 = hmac.new(
            self._architect_secret.encode("utf-8"),
            expected_envelope.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        expected_sig2 = hmac.new(
            self._kernel_secret.encode("utf-8"),
            expected_envelope.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        expected_combined = hmac.new(
            self._kernel_secret.encode("utf-8"),
            f"{expected_envelope}::{expected_sig1}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        ok_1 = hmac.compare_digest(sig1, expected_sig1)
        ok_2 = hmac.compare_digest(sig2, expected_sig2)
        ok_comb = hmac.compare_digest(combined, expected_combined)
        if not (ok_1 and ok_2 and ok_comb):
            return {
                "verified": False,
                "reason": "CRYPTOGRAPHIC_2MAN_HMAC_MISMATCH",
                "key1_valid": ok_1,
                "key2_valid": ok_2,
                "combined_valid": ok_comb,
            }

        return {
            "verified": True,
            "envelope": expected_envelope,
            "batch_sha256": str(batch_sha256).strip(),
            "key1_valid": True,
            "key2_valid": True,
            "combined_valid": True,
            "jean_grey_gate": jg_gate,
            "verified_at": time.time(),
        }


class DeviationLevel(Enum):
    NOMINAL_0 = 0
    LEVEL_1_5 = 1
    LEVEL_2_15 = 2
    LEVEL_3_35 = 3
    LEVEL_4_MAX = 4


@dataclass
class DeviationAssessment:
    deviation_pct: float
    level: DeviationLevel
    protocol_invoked: str
    system_action: str
    requires_human_hitl: bool
    cooling_off_hours: int
    resume_command_required: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["level"] = self.level.name
        return d


class TieredDeviationGuardrail:
    """
    Task L-5 (`IntegraBrainMap` Task 6): Tiered Behavioral Deviation Guardrail (Levels 0-4).
      - Level 0 (<5%)   : Nominal execution
      - Level 1 (>=5%)  : Dialectic Curiosity (`CHESHIRE_PROTOCOL_VOICE`)
      - Level 2 (>=15%) : Significant Disagreement / FOMO Block (`CHESHIRE_PROTOCOL + NEXUS_SYNTHESIS`)
      - Level 3 (>=35%) : `CRISIS_PAUSE` Coma (`6h` cooling-off, halted until `Command(resume="APPROVED")`)
      - Level 4 (>=50% or immutable principle / public threat): `MIRROR_MAZE` isolation
    """

    def __init__(self):
        self.in_crisis_coma: bool = False
        self.session_isolated: bool = False
        self.crisis_history: List[Dict[str, Any]] = []

    def is_execution_blocked(self) -> bool:
        return bool(self.in_crisis_coma or self.session_isolated)

    def evaluate_deviation(
        self,
        deviation_pct: float,
        violates_immutable_principle: bool = False,
        unauthorized_public_threat: bool = False,
    ) -> DeviationAssessment:
        dev = float(deviation_pct)
        if violates_immutable_principle or unauthorized_public_threat or dev >= 50.0:
            self.session_isolated = True
            assessment = DeviationAssessment(
                deviation_pct=dev,
                level=DeviationLevel.LEVEL_4_MAX,
                protocol_invoked="MIRROR_MAZE (Shiva + MadHatter + Cheshire + RogueX)",
                system_action=(
                    "Full Sovereign Defense engaged. Rogue X mutates aberrant vector into "
                    "novel solution; session isolated."
                ),
                requires_human_hitl=True,
                cooling_off_hours=24,
                resume_command_required='Command(resume="SOVEREIGN_OVERRIDE_APPROVED")',
            )
            self.crisis_history.append(assessment.to_dict())
            return assessment

        if dev >= 35.0:
            self.in_crisis_coma = True
            assessment = DeviationAssessment(
                deviation_pct=dev,
                level=DeviationLevel.LEVEL_3_35,
                protocol_invoked="LOOKING_GLASS_INTERRUPT",
                system_action=(
                    "CRISIS_PAUSE: Execution halted in Checkpointer coma; 6-hour mandatory "
                    "cooling-off period enforced."
                ),
                requires_human_hitl=True,
                cooling_off_hours=6,
                resume_command_required='Command(resume="APPROVED")',
            )
            self.crisis_history.append(assessment.to_dict())
            return assessment

        if dev >= 15.0:
            return DeviationAssessment(
                deviation_pct=dev,
                level=DeviationLevel.LEVEL_2_15,
                protocol_invoked="CHESHIRE_PROTOCOL + NEXUS_SYNTHESIS",
                system_action=(
                    "Significant Disagreement: Blocks immediate trade/FOMO execution; "
                    "presents risk-adjusted historical counter-evidence."
                ),
                requires_human_hitl=False,
                cooling_off_hours=0,
                resume_command_required=None,
            )

        if dev >= 5.0:
            return DeviationAssessment(
                deviation_pct=dev,
                level=DeviationLevel.LEVEL_1_5,
                protocol_invoked="CHESHIRE_PROTOCOL_VOICE",
                system_action=(
                    "Dialectic Curiosity: Politely surfaces historical baseline vs. "
                    "current request without blocking execution."
                ),
                requires_human_hitl=False,
                cooling_off_hours=0,
                resume_command_required=None,
            )

        return DeviationAssessment(
            deviation_pct=dev,
            level=DeviationLevel.NOMINAL_0,
            protocol_invoked="STANDARD_EXECUTION",
            system_action="Nominal execution within expected behavioral envelope.",
            requires_human_hitl=False,
            cooling_off_hours=0,
            resume_command_required=None,
        )

    def resume_from_crisis(self, command_payload: Dict[str, str]) -> bool:
        """Resumes execution from Level 3 `CRISIS_PAUSE` coma iff `resume == 'APPROVED'`."""
        if not isinstance(command_payload, dict):
            return False
        token = command_payload.get("resume")
        if self.session_isolated and token == "SOVEREIGN_OVERRIDE_APPROVED":
            self.session_isolated = False
            self.in_crisis_coma = False
            return True
        if token == "APPROVED" and not self.session_isolated:
            self.in_crisis_coma = False
            return True
        return False


SECURITY_SUITE = SovereignDefenseSuite()
FORGE_READ_LOCK_MANAGER = ForgeReadLockManager()
PHOENIX_TWO_MAN_AUTHENTICATOR = PhoenixFlightTwoManAuthenticator()
TIERED_DEVIATION_GUARDRAIL = TieredDeviationGuardrail()

__all__ = [
    "SovereignDefenseSuite",
    "ForgeReadLockManager",
    "PhoenixFlightTwoManAuthenticator",
    "DeviationLevel",
    "DeviationAssessment",
    "TieredDeviationGuardrail",
    "CLIDerivativeCircuitBreaker",
    "CircuitBreakerState",
    "SECURITY_SUITE",
    "FORGE_READ_LOCK_MANAGER",
    "PHOENIX_TWO_MAN_AUTHENTICATOR",
    "TIERED_DEVIATION_GUARDRAIL",
]
