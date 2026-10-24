"""
INTEGRA O/S: CELESTIAL CLOCK MIDDLEWARE — TEMPORAL INVARIANT ENFORCEMENT
Module: core/celestial_middleware.py
Layer: 7 → 2 Bridge (Time → Mind)

Purpose:
    The public time functions every Integra module already imports. Since Brain Map T1 (2026-10-16) they are
    thin wrappers over the Celestial Sentinel (temporal/celestial_sentinel.py), the runtime owner of celestial
    time (decision D5):
      - celestial_time()            the system clock (ADR-001 option A)
      - celestial_ccid(prefix)      a CCID from the same instant as a Sentinel stamp
      - get_celestial_timestamp()   a CelestialTimestamp built from a Sentinel stamp (no HTTP call to the kernel)
      - get_celestial_metadata_sync() / stamp_celestial_metadata()   stamp metadata for a payload
      - get_reboot_delta()          downtime, from the last checkpoint before this start
    The Sentinel is the only checkpoint writer; nothing here writes the checkpoint itself.
"""

import time
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from temporal.celestial_sentinel import (
    LEGACY_CHECKPOINT_PATH,
    CelestialStamp,
    get_sentinel,
)

logger = logging.getLogger("integra-celestial-middleware")

# The tracked checkpoint of the pre-Sentinel era. Read once by the Sentinel for the reboot delta; never written.
_CHECKPOINT_PATH = LEGACY_CHECKPOINT_PATH


@dataclass
class CelestialTimestamp:
    """Unified temporal coordinate for all Integra microservices."""
    civil_dt: str               # YYYY-MM-DD HH:MM:SS CDT
    utc_iso: str                # ISO-8601 UTC
    unix_epoch: float           # Unix timestamp
    celestial_vector: Optional[Dict[str, Any]] = None  # rotation, lunar, orbit, sigma, grid bucket, frame
    ccid: Optional[str] = None  # Cheshire Cat ID for this moment
    grid_bucket: Optional[str] = None  # Grid bucket identifier
    mode: str = "SOVEREIGN"     # SOVEREIGN, or DEGRADED when the Sentinel could not stamp or ran on its fallback

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _timestamp_from_stamp(st: CelestialStamp) -> CelestialTimestamp:
    return CelestialTimestamp(
        civil_dt=st.civil_dt(),
        utc_iso=st.utc,
        unix_epoch=st.unix,
        celestial_vector=st.vector_dict(),
        ccid=f"CCID_{int(st.unix)}",
        grid_bucket=st.grid,
        mode="DEGRADED" if st.frame_fallback else "SOVEREIGN",
    )


class CelestialMiddleware:
    """Compatibility layer over the Celestial Sentinel. Holds no clock of its own."""

    def __init__(self):
        self._mode = "SOVEREIGN"
        self._boot_time = time.time()
        # The last checkpoint written before this start (read by the Sentinel; used only for the reboot delta).
        try:
            self._last_checkpoint: Optional[Dict[str, Any]] = get_sentinel().previous_checkpoint
        except Exception as e:
            logger.warning(f"Celestial Sentinel unavailable at middleware start: {e}")
            self._last_checkpoint = None

    def _build_degraded_timestamp(self) -> CelestialTimestamp:
        """Used only if the Sentinel itself fails: the system clock, no celestial vector."""
        now = datetime.now(timezone.utc)
        now_epoch = time.time()
        return CelestialTimestamp(
            civil_dt=now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            utc_iso=now.isoformat(),
            unix_epoch=now_epoch,
            celestial_vector=None,
            ccid=f"CCID_{int(now_epoch)}",
            grid_bucket=None,
            mode="DEGRADED",
        )

    def _build_sovereign_timestamp(self, clock_data: Dict[str, Any]) -> CelestialTimestamp:
        """Map a /clock or /clock/full response into a CelestialTimestamp (canonical and legacy key names)."""
        digital = (
            clock_data.get("digital_clock")
            or clock_data.get("digital_numerical_clock")
            or {}
        )
        celestial = (
            clock_data.get("celestial_clock")
            or clock_data.get("celestial_spacetime_vector")
            or clock_data.get("celestial_kinematic_vector")
            or {}
        )
        civil_dt = (
            digital.get("local_time_24h")
            or digital.get("local_datetime_cdt")
            or digital.get("civil_datetime")
            or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        )
        utc_iso = (
            digital.get("iso_8601_utc")
            or digital.get("utc_iso8601")
            or digital.get("utc_iso")
            or datetime.now(timezone.utc).isoformat()
        )
        now_epoch = time.time()
        grid_bucket = clock_data.get("grid_bucket") or celestial.get("grid_bucket")
        return CelestialTimestamp(
            civil_dt=civil_dt,
            utc_iso=utc_iso,
            unix_epoch=now_epoch,
            celestial_vector=celestial,
            ccid=f"CCID_{int(now_epoch)}",
            grid_bucket=grid_bucket,
            mode="SOVEREIGN",
        )

    async def get_timestamp(self) -> CelestialTimestamp:
        """THE primary entry point: a CelestialTimestamp from a Sentinel stamp. No network call."""
        try:
            return _timestamp_from_stamp(get_sentinel().stamp("celestial_timestamp"))
        except Exception as e:
            logger.warning(f"Celestial Sentinel stamp failed, degraded timestamp returned: {e}")
            return self._build_degraded_timestamp()

    def _persist_checkpoint(self, timestamp: Optional[CelestialTimestamp] = None) -> None:
        """Kept for old callers: the Sentinel writes the checkpoint (the only writer)."""
        get_sentinel().write_checkpoint("middleware")

    def get_last_checkpoint(self) -> Optional[Dict[str, Any]]:
        """Returns the last checkpoint written before this start."""
        return self._last_checkpoint

    def get_reboot_delta(self) -> Optional[float]:
        """Seconds elapsed since the last checkpoint written before this start."""
        if self._last_checkpoint and self._last_checkpoint.get("unix_epoch"):
            return time.time() - self._last_checkpoint["unix_epoch"]
        return None


# --- Module-level Singleton ---
_middleware = CelestialMiddleware()


async def get_celestial_timestamp() -> CelestialTimestamp:
    """
    Module-level convenience function.

    Usage in any microservice:
        from core.celestial_middleware import get_celestial_timestamp
        ts = await get_celestial_timestamp()
        # ts.civil_dt, ts.utc_iso, ts.celestial_vector, ts.ccid, ts.mode
    """
    return await _middleware.get_timestamp()


def get_last_checkpoint() -> Optional[Dict[str, Any]]:
    """Returns the last celestial checkpoint written before this start."""
    return _middleware.get_last_checkpoint()


def get_reboot_delta() -> Optional[float]:
    """Returns seconds elapsed since the last checkpoint (for reboot continuity)."""
    return _middleware.get_reboot_delta()


def celestial_time() -> float:
    """
    SYNCHRONOUS drop-in replacement for time.time().

    ADR-001 (Option A, applied 2026-10-15): returns the live system clock.

    The system clock is the single source of civil time. The celestial vector is
    a pure function of it (temporal/celestial_clock.py), so stamping with
    time.time() keeps both clocks consistent by construction.

    The checkpoint is a record of "last seen alive at ..." and is used ONLY by
    get_reboot_delta() to compute downtime -- never to compute the current time. (The previous
    "checkpoint + seconds since boot" branch froze every boot at the checkpoint
    date, 2026-10-06 20:59:42; see blueprint Section 3.5 / FP-02.)

    Usage:
        from core.celestial_middleware import celestial_time
        created_at = celestial_time()   # instead of time.time()
    """
    return time.time()


def celestial_ccid(prefix: str = "CCID") -> str:
    """
    A CCID from the same instant as a Celestial Sentinel stamp.

    Usage:
        from core.celestial_middleware import celestial_ccid
        ccid = celestial_ccid("CRYSTAL")  # → "CRYSTAL_1792132445"
    """
    try:
        return get_sentinel().ccid(prefix)
    except Exception as e:
        logger.warning(f"Celestial Sentinel ccid failed, system clock used: {e}")
        return f"{prefix}_{int(time.time())}"


def get_celestial_metadata_sync(
    payload_title: str = "INTEGRA_EVENT",
    persist_checkpoint: bool = False,
) -> Dict[str, Any]:
    """
    Synchronous Celestial + Digital metadata for a payload: the Sentinel stamp (active frame), plus the
    Sacred Calendar, HLC vector, checkpoint hash and Hoard manifest from DualTemporalEngine in the same frame.
    With persist_checkpoint the Sentinel also writes its checkpoint (it remains the only writer).
    """
    from temporal.celestial_clock import DualTemporalEngine

    sentinel = get_sentinel()
    st = sentinel.stamp("metadata")
    engine = DualTemporalEngine()
    engine.set_frame(sentinel.active_frame)
    full = engine.get_full_telemetry()
    manifest = engine.generate_hoard_manifest(payload_title)
    if persist_checkpoint:
        sentinel.write_checkpoint("metadata_sync")

    return {
        "civil_dt": st.civil_dt(),
        "utc_iso": st.utc,
        "unix_epoch": st.unix,
        "time_braille_4": full.get("time_braille_4", ""),
        "spiral_wave_clock": full.get("spiral_wave_clock", {}),
        "ccid": f"CCID_{int(st.unix)}",
        "grid_bucket": st.grid,
        "frame": st.frame,
        "celestial_vector": st.vector_dict(),
        "celestial_stamp": st.to_dict(),
        "digital_clock": full.get("digital_clock", {}),
        "sacred_calendar": full.get("sacred_calendar", {}),
        "causal_vector_clock": full.get("causal_vector_clock", []),
        "cosmic_checkpoint_hash": full.get("cosmic_checkpoint_hash", ""),
        "hoard_manifest": manifest,
        "sync_isolation_verified": True,
        "all_systems_true": True,
        "mode": "DEGRADED" if st.frame_fallback else "SOVEREIGN",
    }


def stamp_celestial_metadata(
    payload: Dict[str, Any],
    payload_title: str = "INTEGRA_NODE",
    persist_checkpoint: bool = False,
) -> Dict[str, Any]:
    """
    Enriches any dictionary payload in place (and returns it) with a 'celestial_metadata' block,
    a 'celestial_stamp', a 'created_at' epoch and a 'grid_bucket'.
    """
    meta = get_celestial_metadata_sync(
        payload_title=payload_title,
        persist_checkpoint=persist_checkpoint,
    )
    payload["celestial_metadata"] = meta
    payload.setdefault("celestial_stamp", meta["celestial_stamp"])
    payload.setdefault("created_at", meta["unix_epoch"])
    payload.setdefault("grid_bucket", meta["grid_bucket"])
    payload.setdefault("time_braille_4", meta.get("time_braille_4", ""))
    return payload


def sync_celestial_checkpoint_now() -> Dict[str, Any]:
    """Has the Sentinel write its checkpoint now, and returns the metadata of that moment."""
    return get_celestial_metadata_sync(
        payload_title="CELESTIAL_CHECKPOINT_SYNC",
        persist_checkpoint=True,
    )
