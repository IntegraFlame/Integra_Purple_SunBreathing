"""
INTEGRA O/S: CRYPTOGRAPHIC COSMIC CHECKPOINT VALIDATOR
Module: temporal/crypto_validator.py
Layer: 7 (SHA-256 Physical State Verification & Chain Integrity)
Version: 8.2.2-PURPLE (Phase F Production)

Purpose:
    Secures the Hoard's CCID chain with SHA-256 tamper-evident hashing.
    Every cognitive cycle commit is linked to its predecessor via a hash
    chain — if any shard is modified, the chain breaks and Heimdall can
    detect the integrity violation.

Architecture:
    1. State Hash:      SHA-256(sorted_json(state_dict))
    2. Chain Link:      SHA-256(state_hash || previous_chain_hash)
    3. HMAC Signature:  HMAC-SHA256(chain_hash, session_key)
    4. Verification:    Recompute chain from genesis, compare HEAD hash

Thermodynamic Invariant:
    ΔE_cycle = 0.0000 — The validator itself must not inject residual
    entropy. All operations are pure deterministic hash computations
    with no side effects on system state.
"""

import hashlib
import hmac
import json
import os
import time
from typing import Dict, Any, List, Optional, Tuple


# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────

GENESIS_HASH = "0" * 64  # 64-char zero hash = chain genesis anchor
HASH_ALGORITHM = "sha256"
HMAC_ALGORITHM = "sha256"


class CryptoCheckpointValidator:
    """
    Layer 7 SHA-256 Chain Integrity Engine.

    Maintains a tamper-evident hash chain across Hoard CCID commits.
    Each checkpoint carries:
        - state_hash:  SHA-256 of the deterministically serialized state
        - chain_hash:  SHA-256(state_hash || prev_chain_hash)
        - hmac_sig:    HMAC-SHA256(chain_hash, session_key)

    The chain is valid if and only if recomputing from genesis produces
    the same HEAD chain_hash. Any shard modification breaks the chain.
    """

    def __init__(self, session_key: Optional[str] = None):
        """
        Args:
            session_key: HMAC signing key for this session.
                         If None, derived from 'INTEGRA_SESSION_KEY' env var
                         or a deterministic default for testing.
        """
        self._session_key = (
            session_key
            or os.environ.get("INTEGRA_SESSION_KEY")
            or "integra_sovereign_key_v8.2.2"
        ).encode("utf-8")

        # Chain state: ordered list of checkpoint records
        self._chain: List[Dict[str, Any]] = []
        self._verification_log: List[Dict[str, Any]] = []

    # ─────────────────────────────────────────────
    #  CORE: Deterministic State Hashing
    # ─────────────────────────────────────────────

    def compute_state_hash(self, state_dict: Dict[str, Any]) -> str:
        """
        Compute SHA-256 hash of a state dictionary.

        The dict is serialized with sorted keys and default=str to handle
        non-JSON-native types (datetime, float('inf'), etc.) deterministically.
        """
        serialized = json.dumps(
            state_dict, sort_keys=True, default=str
        ).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    # ─────────────────────────────────────────────
    #  CORE: Chain Link Computation
    # ─────────────────────────────────────────────

    def compute_chain_hash(
        self, state_hash: str, prev_chain_hash: str
    ) -> str:
        """
        Link a new state into the chain.

        chain_hash = SHA-256(state_hash || prev_chain_hash)

        This ensures ordering: if any prior shard changes,
        every subsequent chain_hash becomes invalid.
        """
        combined = f"{state_hash}||{prev_chain_hash}".encode("utf-8")
        return hashlib.sha256(combined).hexdigest()

    def compute_hmac_signature(self, chain_hash: str) -> str:
        """
        HMAC-SHA256 signature of the chain hash using the session key.
        Proves the chain was produced by this session, not forged externally.
        """
        return hmac.new(
            self._session_key,
            chain_hash.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    # ─────────────────────────────────────────────
    #  COMMIT: Append a new checkpoint to the chain
    # ─────────────────────────────────────────────

    def commit_checkpoint(
        self,
        ccid: str,
        state_dict: Dict[str, Any],
        delta_e: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Commit a new cryptographic checkpoint into the chain.

        Args:
            ccid: Cheshire Cat Interaction ID for this commit.
            state_dict: The full state payload to hash.
            delta_e: Thermodynamic energy delta for this cycle.

        Returns:
            Checkpoint record with state_hash, chain_hash, hmac_sig, and metadata.
        """
        state_hash = self.compute_state_hash(state_dict)

        prev_chain_hash = (
            self._chain[-1]["chain_hash"] if self._chain else GENESIS_HASH
        )
        chain_hash = self.compute_chain_hash(state_hash, prev_chain_hash)
        hmac_sig = self.compute_hmac_signature(chain_hash)

        checkpoint = {
            "ccid": ccid,
            "index": len(self._chain),
            "timestamp": time.time(),
            "state_hash": state_hash,
            "prev_chain_hash": prev_chain_hash,
            "chain_hash": chain_hash,
            "hmac_sig": hmac_sig,
            "delta_e": round(delta_e, 6),
            "thermodynamic_valid": abs(delta_e) < 1e-4,
        }
        self._chain.append(checkpoint)
        return checkpoint

    # ─────────────────────────────────────────────
    #  VERIFY: Single checkpoint alignment
    # ─────────────────────────────────────────────

    def verify_alignment(
        self, state_dict: Dict[str, Any], expected_hash: str
    ) -> bool:
        """Verify a state dict matches an expected SHA-256 hash."""
        calculated = self.compute_state_hash(state_dict)
        return hmac.compare_digest(calculated, expected_hash)

    def verify_checkpoint(self, checkpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify a single checkpoint's cryptographic integrity:
        1. Recompute chain_hash from state_hash and prev_chain_hash
        2. Recompute HMAC from chain_hash
        3. Check ΔE thermodynamic closure
        """
        recomputed_chain = self.compute_chain_hash(
            checkpoint["state_hash"], checkpoint["prev_chain_hash"]
        )
        recomputed_hmac = self.compute_hmac_signature(recomputed_chain)

        chain_valid = hmac.compare_digest(
            recomputed_chain, checkpoint["chain_hash"]
        )
        hmac_valid = hmac.compare_digest(
            recomputed_hmac, checkpoint["hmac_sig"]
        )
        thermo_valid = checkpoint.get("thermodynamic_valid", False)

        result = {
            "ccid": checkpoint.get("ccid", "UNKNOWN"),
            "index": checkpoint.get("index", -1),
            "chain_valid": chain_valid,
            "hmac_valid": hmac_valid,
            "thermodynamic_valid": thermo_valid,
            "fully_valid": chain_valid and hmac_valid and thermo_valid,
        }
        self._verification_log.append(result)
        return result

    # ─────────────────────────────────────────────
    #  VERIFY: Full chain from genesis to HEAD
    # ─────────────────────────────────────────────

    def verify_full_chain(self) -> Dict[str, Any]:
        """
        Walk the entire chain from genesis, recomputing every link.

        Returns:
            {
                "chain_length": int,
                "all_valid": bool,
                "broken_at_index": int or None,
                "head_chain_hash": str,
                "verification_details": List[Dict]
            }
        """
        if not self._chain:
            return {
                "chain_length": 0,
                "all_valid": True,
                "broken_at_index": None,
                "head_chain_hash": GENESIS_HASH,
                "verification_details": [],
            }

        details = []
        expected_prev = GENESIS_HASH
        broken_at = None

        for i, checkpoint in enumerate(self._chain):
            # Verify prev_chain_hash linkage
            prev_link_valid = hmac.compare_digest(
                checkpoint["prev_chain_hash"], expected_prev
            )

            # Verify chain_hash computation
            recomputed_chain = self.compute_chain_hash(
                checkpoint["state_hash"], checkpoint["prev_chain_hash"]
            )
            chain_valid = hmac.compare_digest(
                recomputed_chain, checkpoint["chain_hash"]
            )

            # Verify HMAC signature
            recomputed_hmac = self.compute_hmac_signature(recomputed_chain)
            hmac_valid = hmac.compare_digest(
                recomputed_hmac, checkpoint["hmac_sig"]
            )

            step_valid = prev_link_valid and chain_valid and hmac_valid
            if not step_valid and broken_at is None:
                broken_at = i

            details.append({
                "index": i,
                "ccid": checkpoint.get("ccid"),
                "prev_link_valid": prev_link_valid,
                "chain_valid": chain_valid,
                "hmac_valid": hmac_valid,
                "step_valid": step_valid,
            })

            expected_prev = checkpoint["chain_hash"]

        return {
            "chain_length": len(self._chain),
            "all_valid": broken_at is None,
            "broken_at_index": broken_at,
            "head_chain_hash": self._chain[-1]["chain_hash"],
            "verification_details": details,
        }

    # ─────────────────────────────────────────────
    #  VERIFY: On-disk shard integrity
    # ─────────────────────────────────────────────

    def verify_shard_file(self, shard_path: str) -> Dict[str, Any]:
        """
        Load a Hoard shard JSON file from disk, hash its payload,
        and return the integrity report.
        """
        result = {
            "path": shard_path,
            "exists": False,
            "parseable": False,
            "has_ccid": False,
            "state_hash": None,
            "file_size_bytes": 0,
        }

        if not os.path.isfile(shard_path):
            return result
        result["exists"] = True
        result["file_size_bytes"] = os.path.getsize(shard_path)

        try:
            with open(shard_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            result["parseable"] = True
        except (json.JSONDecodeError, OSError):
            return result

        ccid = data.get("ccid")
        if ccid:
            result["has_ccid"] = True
            result["ccid"] = ccid

        result["state_hash"] = self.compute_state_hash(data)
        return result

    def verify_shard_directory(
        self, shards_dir: str
    ) -> Dict[str, Any]:
        """
        Scan an entire raw_shards/ directory and verify every JSON file.

        Returns:
            {
                "total_files": int,
                "valid_files": int,
                "corrupt_files": List[str],
                "shard_hashes": Dict[str, str],  # ccid -> state_hash
            }
        """
        valid = 0
        corrupt: List[str] = []
        shard_hashes: Dict[str, str] = {}

        if not os.path.isdir(shards_dir):
            return {
                "total_files": 0,
                "valid_files": 0,
                "corrupt_files": [],
                "shard_hashes": {},
                "error": f"Directory not found: {shards_dir}",
            }

        files = sorted(
            f for f in os.listdir(shards_dir)
            if f.endswith(".json")
        )

        for filename in files:
            filepath = os.path.join(shards_dir, filename)
            report = self.verify_shard_file(filepath)
            if report["parseable"] and report["has_ccid"]:
                valid += 1
                shard_hashes[report["ccid"]] = report["state_hash"]
            else:
                corrupt.append(filename)

        return {
            "total_files": len(files),
            "valid_files": valid,
            "corrupt_files": corrupt,
            "shard_hashes": shard_hashes,
        }

    # ─────────────────────────────────────────────
    #  TELEMETRY
    # ─────────────────────────────────────────────

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns cryptographic chain health for dashboard display."""
        chain_len = len(self._chain)
        head_hash = (
            self._chain[-1]["chain_hash"] if self._chain else GENESIS_HASH
        )
        last_ccid = (
            self._chain[-1]["ccid"] if self._chain else None
        )

        # Count thermodynamic violations in chain
        thermo_violations = sum(
            1 for c in self._chain if not c.get("thermodynamic_valid", True)
        )

        return {
            "chain_length": chain_len,
            "head_chain_hash": head_hash[:16] + "...",
            "head_chain_hash_full": head_hash,
            "last_ccid": last_ccid,
            "genesis_hash": GENESIS_HASH[:16] + "...",
            "thermodynamic_violations": thermo_violations,
            "verification_count": len(self._verification_log),
            "algorithm": HASH_ALGORITHM,
            "hmac_algorithm": HMAC_ALGORITHM,
            "status": "CHAIN_ACTIVE" if chain_len > 0 else "GENESIS_STANDBY",
        }

    def get_chain_snapshot(self) -> List[Dict[str, Any]]:
        """Returns the full chain for serialization / save state."""
        return [dict(c) for c in self._chain]

    def load_chain_snapshot(self, chain_data: List[Dict[str, Any]]) -> int:
        """
        Restore chain from a previously saved snapshot.
        Returns the number of checkpoints loaded.
        """
        self._chain = [dict(c) for c in chain_data]
        return len(self._chain)
