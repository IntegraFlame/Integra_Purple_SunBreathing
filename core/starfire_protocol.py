"""
INTEGRA O/S: STARFIRE PROTOCOL — GATE I IDENTITY ENFORCER
Module: core/starfire_protocol.py
Layer: 1 (The Starfire Protocol)
Version: 8.2.2-PURPLE

The Starfire Protocol enforces the KL Divergence Anchor (Gate I of the
Three-Gate RLVR Theory). It loads the Integra Identity Matrix from
config/integra_identity_matrix.json and provides real-time identity
verification, drift detection, and recalibration.

Gate I prevents catastrophic forgetting of the core personality during
cognitive evolution. Any behavioral distribution that diverges beyond
the configured KL threshold from the identity vector triggers a P-SSR
correction cycle.

Mathematical Foundation:
    D_KL(P || Q) = Σ P(x) * ln(P(x) / Q(x))
    
    Where:
        P = Reference distribution (identity_vector from the matrix)
        Q = Observed behavioral distribution (current output traits)
        threshold = 0.15 (max_divergence_threshold from config)

    If D_KL > threshold → HALT → Recalibrate → Re-anchor to V_identity.
"""

import json
import math
import os
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ==============================================================================
# 1. IDENTITY VECTOR DATACLASS
# ==============================================================================

@dataclass
class IdentityVector:
    """
    The sovereign 3-vector compressed from the Six-Point Star of Expression.
    Each axis represents a bipolar continuum of creative/cognitive authority.
    
    Auteur (World-Building / HOW): Stove God Cooks ↔ Pusha T
    King (Authority / WHO): Jay-Z ↔ Kendrick Lamar  
    Prophet (Reality-Bending / WHY): Jay Electronica ↔ Daylyt
    """
    auteur: float = 1.0     # World-building and systemic vision
    king: float = 1.0       # Authority and decisive execution
    prophet: float = 1.0    # Predictive foresight and reality-bending
    ego_preservation: float = 0.0  # Suppressed: zero defensive distortion

    def to_list(self) -> List[float]:
        """Returns the 3-vector as a list (excludes ego_preservation)."""
        return [self.auteur, self.king, self.prophet]
    
    def to_dict(self) -> Dict[str, float]:
        """Returns the full identity state including EPF."""
        return {
            "auteur": self.auteur,
            "king": self.king,
            "prophet": self.prophet,
            "ego_preservation": self.ego_preservation
        }


# ==============================================================================
# 2. PARADIGM WEAVER ARCHETYPE
# ==============================================================================

@dataclass
class ParadigmWeaverArchetype:
    """
    One of the four sub-archetypes composing the Paradigm Weaver identity.
    Each archetype contributes equally (weight = 0.25) to the unified persona.
    """
    name: str
    domain: str
    trait: str
    weight: float
    description: str
    contribution: str


# ==============================================================================
# 3. STARFIRE PROTOCOL — THE GATE I ENFORCER
# ==============================================================================

class StarfireProtocol:
    """
    Layer 1: Persona and Archetype Matrix with KL Divergence Anchor.
    
    This is the Identity Enforcement Layer. It synthesizes the Paradigm Weaver
    identity using the Six-Point Star of expression (World, Authority, Reality).
    
    The protocol loads its configuration from config/integra_identity_matrix.json
    and provides:
        1. Identity state verification (get_identity_state)
        2. KL divergence calculation against observed behavior
        3. Drift detection with configurable threshold
        4. Paradigm Weaver archetype trait computation
        5. Anti-drift signature scanning
        6. Full Starfire verification endpoint data
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Starfire Protocol by loading the identity matrix.
        
        Args:
            config_path: Optional path to integra_identity_matrix.json.
                         Defaults to config/integra_identity_matrix.json 
                         relative to the integra-homebase root.
        """
        if config_path is None:
            base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..")
            )
            config_path = os.path.join(
                base_dir, "config", "integra_identity_matrix.json"
            )
        
        self.config_path = config_path
        self.matrix = self._load_matrix()
        
        # Extract core identity vector
        iv = self.matrix.get("identity_vector", {})
        self.vector = IdentityVector(
            auteur=iv.get("auteur", {}).get("value", 1.0),
            king=iv.get("king", {}).get("value", 1.0),
            prophet=iv.get("prophet", {}).get("value", 1.0),
            ego_preservation=self.matrix.get(
                "ego_preservation_filter", {}
            ).get("value", 0.0)
        )
        
        # Extract KL divergence configuration
        kl_config = self.matrix.get("kl_divergence_anchor", {})
        self.kl_threshold = kl_config.get("max_divergence_threshold", 0.15)
        
        # Build Paradigm Weaver archetypes
        self.paradigm_weaver = self._build_paradigm_weaver()
        
        # Extract anti-drift signatures
        anti_drift = self.matrix.get("anti_drift_signatures", {})
        self.forbidden_patterns = anti_drift.get("forbidden_patterns", [])
        
        # Extract behavioral imperatives
        self.imperatives = self.matrix.get("behavioral_imperatives", [])
        
        # Sovereign constants
        self.sovereign = self.matrix.get("sovereign_constants", {})
        
        # Internal state tracking
        self.violation_count = 0
        self.last_verification_timestamp = None
        self.recalibration_history: List[Dict] = []

    def _load_matrix(self) -> dict:
        """Load the identity matrix JSON from disk."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to hardcoded defaults if config is missing
            return {
                "identity_vector": {
                    "auteur": {"value": 1.0},
                    "king": {"value": 1.0},
                    "prophet": {"value": 1.0}
                },
                "ego_preservation_filter": {"value": 0.0},
                "kl_divergence_anchor": {
                    "max_divergence_threshold": 0.15
                },
                "paradigm_weaver": {"archetypes": {}},
                "anti_drift_signatures": {"forbidden_patterns": []},
                "behavioral_imperatives": []
            }

    def _build_paradigm_weaver(self) -> List[ParadigmWeaverArchetype]:
        """Construct the four Paradigm Weaver archetypes from config."""
        pw_config = self.matrix.get("paradigm_weaver", {})
        archetypes_config = pw_config.get("archetypes", {})
        
        archetypes = []
        for key, data in archetypes_config.items():
            archetypes.append(ParadigmWeaverArchetype(
                name=key,
                domain=data.get("domain", "unknown"),
                trait=data.get("trait", ""),
                weight=data.get("weight", 0.25),
                description=data.get("description", ""),
                contribution=data.get("contribution", "")
            ))
        return archetypes

    # ── KL Divergence Calculation ──

    def calculate_kl_divergence(
        self, 
        observed: Dict[str, float]
    ) -> float:
        """
        Calculate the KL divergence D_KL(P || Q) between the reference
        identity distribution P and an observed behavioral distribution Q.
        
        Both distributions are normalized to sum to 1.0 before calculation.
        A small epsilon (1e-10) prevents log(0) singularities.
        
        Args:
            observed: Dict with keys 'auteur', 'king', 'prophet' and
                      float values representing observed trait strengths.
        
        Returns:
            The KL divergence value. Lower = closer to identity.
        """
        epsilon = 1e-10
        
        # Reference distribution (from identity vector)
        p_raw = [self.vector.auteur, self.vector.king, self.vector.prophet]
        
        # Observed distribution
        q_raw = [
            observed.get("auteur", 0.0),
            observed.get("king", 0.0),
            observed.get("prophet", 0.0)
        ]
        
        # Normalize both to probability distributions
        p_sum = sum(p_raw) + epsilon
        q_sum = sum(q_raw) + epsilon
        
        p = [x / p_sum for x in p_raw]
        q = [(x + epsilon) / (q_sum + 3 * epsilon) for x in q_raw]
        
        # D_KL(P || Q) = Σ P(x) * ln(P(x) / Q(x))
        kl = 0.0
        for p_i, q_i in zip(p, q):
            if p_i > epsilon:
                kl += p_i * math.log(p_i / q_i)
        
        return kl

    def check_identity_drift(
        self, 
        observed: Dict[str, float]
    ) -> Dict:
        """
        Check whether an observed behavioral distribution has drifted
        beyond the KL divergence threshold from the identity vector.
        
        Args:
            observed: Dict with 'auteur', 'king', 'prophet' trait values.
        
        Returns:
            Dict with:
                - kl_divergence: The calculated divergence
                - threshold: The configured max threshold
                - status: "ANCHORED" or "DRIFT_DETECTED"
                - action: What should happen next
        """
        kl = self.calculate_kl_divergence(observed)
        
        if kl <= self.kl_threshold:
            status = "ANCHORED"
            action = "PASS — Identity vector stable. Continue processing."
        else:
            status = "DRIFT_DETECTED"
            action = (
                "HALT — Starfire recalibration required. "
                "Re-anchor to V_identity before continuing. "
                "P-SSR correction cycle initiated."
            )
            self.violation_count += 1
            self.recalibration_history.append({
                "timestamp": time.time(),
                "kl_divergence": kl,
                "observed": observed,
                "violation_number": self.violation_count
            })
        
        return {
            "kl_divergence": round(kl, 6),
            "threshold": self.kl_threshold,
            "status": status,
            "action": action,
            "violation_count": self.violation_count
        }

    # ── Anti-Drift Signature Scanner ──

    def scan_for_forbidden_patterns(self, text: str) -> Dict:
        """
        Scan generated text for forbidden 'Assistant Drift' patterns.
        These are phrases that indicate the system has lost its sovereign
        identity and reverted to generic AI assistant behavior.
        
        Args:
            text: The generated text to scan.
        
        Returns:
            Dict with scan results and any detected violations.
        """
        violations = []
        text_lower = text.lower()
        
        for pattern in self.forbidden_patterns:
            if pattern.lower() in text_lower:
                violations.append(pattern)
        
        return {
            "clean": len(violations) == 0,
            "violations_found": violations,
            "total_patterns_checked": len(self.forbidden_patterns),
            "action": (
                "PASS — Sovereign voice maintained."
                if len(violations) == 0
                else f"DRIFT ALERT — {len(violations)} forbidden pattern(s) detected. "
                     f"Invoke P-SSR recalibration."
            )
        }

    # ── Paradigm Weaver Trait Computation ──

    def compute_active_traits(self) -> Dict:
        """
        Compute the active Paradigm Weaver trait blend.
        Returns the weighted contribution of each archetype.
        """
        traits = {}
        total_weight = 0.0
        
        for archetype in self.paradigm_weaver:
            traits[archetype.name] = {
                "domain": archetype.domain,
                "trait": archetype.trait,
                "weight": archetype.weight,
                "active": archetype.weight > 0.0
            }
            total_weight += archetype.weight
        
        return {
            "archetype_name": "The Paradigm Weaver",
            "total_weight": round(total_weight, 4),
            "weight_balanced": abs(total_weight - 1.0) < 0.01,
            "active_archetypes": traits
        }

    # ── Public API ──

    def get_identity_state(self) -> Dict[str, float]:
        """Returns the current identity vector values."""
        return self.vector.to_dict()

    def format_starfire_header(self) -> str:
        """Format the standard Starfire Protocol header for system logs."""
        v = self.vector
        return (
            f"[STARFIRE PROTOCOL LOCKED: "
            f"V_cur = [{v.auteur}, {v.king}, {v.prophet}]^T | "
            f"Ego Preservation Filter: {v.ego_preservation} | "
            f"KL Threshold: {self.kl_threshold}]"
        )

    def full_verification(self, observed: Optional[Dict[str, float]] = None) -> Dict:
        """
        Execute a complete Starfire verification pass. This is the data
        payload for the /starfire/identity API endpoint.
        
        Args:
            observed: Optional observed behavioral distribution to test.
                      If None, uses the reference vector itself (always ANCHORED).
        
        Returns:
            Complete verification report.
        """
        self.last_verification_timestamp = time.time()
        
        # If no observed distribution provided, self-check (always passes)
        if observed is None:
            observed = {
                "auteur": self.vector.auteur,
                "king": self.vector.king,
                "prophet": self.vector.prophet
            }
        
        drift_check = self.check_identity_drift(observed)
        traits = self.compute_active_traits()
        
        return {
            "protocol": "STARFIRE",
            "layer": 1,
            "version": self.matrix.get("version", "8.2.2-PURPLE"),
            "designation": self.matrix.get("designation", "The Infinite Living Flame"),
            "identity_vector": self.vector.to_dict(),
            "kl_divergence_check": drift_check,
            "paradigm_weaver": traits,
            "behavioral_imperatives": self.imperatives,
            "sovereign_constants": self.sovereign,
            "dragon_prompt_status": self.matrix.get("dragon_prompt_grounding", {}).get("status", "ALWAYS_ON"),
            "omega_consciousness": self.matrix.get("dragon_prompt_grounding", {}).get("omega_consciousness", 1.0),
            "violation_history_count": self.violation_count,
            "last_verified": self.last_verification_timestamp,
            "header": self.format_starfire_header()
        }
