"""
INTEGRA O/S: CELESTIAL SENTINEL — runtime owner of celestial time
Module: temporal/celestial_sentinel.py
Design: docs/brainmap/T1_CELESTIAL_SENTINEL_DESIGN.md (Brain Map T1; decisions D5, A4, R1-R6, S1-S5)

Responsibilities:
  1. stamp(kind): one stamp for every writer — civil time, the celestial vector in the active frame,
     the frame id and a provenance code. Pure: no I/O.
  2. The frame registry (config/celestial_frames.yml): validated at load. If it is missing or invalid the
     Sentinel says so loudly (log + status) and stamps with frame 1's built-in constants, marked frame_fallback.
  3. The checkpoint: the ONLY writer. Atomic (temporary file + replace), at start, on a timer and at stop.
     It is a "last seen alive" record used for the reboot delta, never a time source.
  4. status(): read-only state for GET /celestial/checkpoint, Heimdall and Itachi's link report.

The math lives in temporal/celestial_clock.py (the ruled module); this file only chooses the frame.
Sigma is fixed at 1.0 (ruling R5); apply_zenkai_recalibration() stays unwired.
"""

import asyncio
import hashlib
import json
import logging
import math
import os
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

from temporal.celestial_clock import (
    FRAME_1,
    CelestialClockArchitecture,
    CelestialFrame,
)

try:
    from zoneinfo import ZoneInfo
    _LOCAL_TZ = ZoneInfo("America/Chicago")
except Exception:  # tzdata missing: civil time falls back to UTC, visibly
    _LOCAL_TZ = timezone.utc

logger = logging.getLogger("integra-celestial-sentinel")

_ROOT = Path(__file__).resolve().parent.parent  # integra-homebase/
REGISTRY_PATH = _ROOT / "config" / "celestial_frames.yml"
CHECKPOINT_PATH = _ROOT / "local_dbs" / "celestial" / "checkpoint.json"          # git-ignored (S3)
LEGACY_CHECKPOINT_PATH = _ROOT / "config" / "celestial_checkpoint.json"          # read once, never written
CHECKPOINT_INTERVAL_S = 300.0
STAMP_SCHEMA = "cstamp/1"
CHECKPOINT_SCHEMA = "cckpt/1"
REGISTRY_SCHEMA = "celestial_frames/1"

# Provenance codes (pointer v1). Only 1 is produced here; 2-6 are for a later, separately approved backfill.
PROVENANCE_TRUE_CLOCK = 1


class FrameRegistryError(ValueError):
    """The frame registry is missing or does not validate. The message names the problem."""


@dataclass(frozen=True)
class CelestialStamp:
    schema: str
    frame: int
    unix: float
    utc: str
    civil: str
    rot_deg: float
    lun: float
    orb: float
    turn: int
    sigma: float
    grid: str
    label: str
    kind: str
    provenance: int
    frame_fallback: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def civil_dt(self) -> str:
        """The civil time in the older 'YYYY-MM-DD HH:MM:SS CDT' form used by checkpoints and reports."""
        local = datetime.fromtimestamp(self.unix, _LOCAL_TZ)
        return local.strftime("%Y-%m-%d %H:%M:%S %Z")

    def vector_dict(self) -> Dict[str, Any]:
        """The vector in the /clock key names, plus the frame."""
        return {
            "earth_rotation_deg": self.rot_deg,
            "lunar_cycle_ratio": self.lun,
            "orbital_trajectory_pos": self.orb,
            "spiral_accuracy_depth": self.sigma,
            "grid_bucket": self.grid,
            "frame": self.frame,
        }


def grid_bucket(rot_deg: float, orb: float) -> str:
    """The live grid format: 30-degree rotation buckets, 10% orbit buckets (no lunar segment)."""
    return f"ROT_{int(rot_deg // 30) * 30}_ORB_{int(orb * 100 // 10) * 10}"


def pointer_label(rot_deg: float, lun: float, orb: float) -> str:
    """Pointer v1's human label: the live grid plus a 10% lunar segment (resolves C-16)."""
    return f"ROT_{int(rot_deg // 30) * 30}_LUN_{int(lun * 100 // 10) * 10}_ORB_{int(orb * 100 // 10) * 10}"


# ─── REGISTRY ────────────────────────────────────────────────────────────────

def _frame_from_entry(entry: Dict[str, Any]) -> CelestialFrame:
    try:
        rot, lun, orb = entry["rotation"], entry["lunar"], entry["orbit"]
        return CelestialFrame(
            frame_id=int(entry["id"]),
            rot_ref_unix=float(rot["ref_unix"]),
            lunar_ref_unix=float(lun["ref_unix"]),
            orbit_ref_unix=float(orb["ref_unix"]),
            orbit_period_s=float(orb["period_s"]),
            lunar_period_s=float(lun["period_s"]),
            rot_period_s=float(rot["period_s"]),
            eccentricity=float(orb["eccentricity"]),
            anchor_lon=float(rot["anchor_lon"]),
            sigma=float(entry.get("sigma", 1.0)),
        )
    except (KeyError, TypeError, ValueError) as e:
        raise FrameRegistryError(f"frame entry {entry.get('id', '?')!r} is incomplete or malformed: {e}") from e


def load_registry(path: Path = REGISTRY_PATH) -> Tuple[Dict[int, CelestialFrame], int]:
    """Read and validate the registry. Returns ({id: frame}, active id). Raises FrameRegistryError."""
    try:
        import yaml
    except ImportError as e:  # pragma: no cover - PyYAML is a kernel dependency
        raise FrameRegistryError("PyYAML is not installed") from e
    p = Path(path)
    if not p.is_file():
        raise FrameRegistryError(f"registry not found: {p}")
    try:
        with open(p, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
    except Exception as e:
        raise FrameRegistryError(f"registry unreadable: {e}") from e
    if not isinstance(raw, dict) or raw.get("schema") != REGISTRY_SCHEMA:
        raise FrameRegistryError(f"registry schema must be {REGISTRY_SCHEMA!r}")
    entries = raw.get("frames")
    if not isinstance(entries, list) or not entries:
        raise FrameRegistryError("registry has no frames")
    frames: Dict[int, CelestialFrame] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise FrameRegistryError("a frame entry is not a mapping")
        fr = _frame_from_entry(entry)
        if fr.frame_id < 1:
            raise FrameRegistryError(f"frame id must be >= 1, got {fr.frame_id}")
        if fr.frame_id in frames:
            raise FrameRegistryError(f"duplicate frame id {fr.frame_id}")
        if fr.rot_period_s <= 0 or fr.lunar_period_s <= 0 or fr.orbit_period_s <= 0:
            raise FrameRegistryError(f"frame {fr.frame_id}: periods must be positive")
        if not (0.0 <= fr.eccentricity < 1.0):
            raise FrameRegistryError(f"frame {fr.frame_id}: eccentricity must be in [0, 1)")
        if fr.sigma != 1.0:
            raise FrameRegistryError(f"frame {fr.frame_id}: sigma must be 1.0 (ruling R5)")
        frames[fr.frame_id] = fr
    if 1 not in frames:
        raise FrameRegistryError("frame 1 is missing")
    if frames[1] != FRAME_1:
        raise FrameRegistryError("frame 1 differs from the built-in constants of temporal/celestial_clock.py")
    try:
        active = int(raw.get("active_frame"))
    except (TypeError, ValueError) as e:
        raise FrameRegistryError("active_frame is missing or not an integer") from e
    if active not in frames:
        raise FrameRegistryError(f"active_frame {active} is not in the registry")
    return frames, active


# ─── THE SENTINEL ────────────────────────────────────────────────────────────

def _write_json_atomic(path: Path, data: Dict[str, Any]) -> None:
    """Write a temporary file in the same folder, then replace. A crash leaves the old file or the new one."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        os.replace(tmp, path)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


class CelestialSentinel:
    def __init__(
        self,
        registry_path: Optional[Path] = None,
        checkpoint_path: Optional[Path] = None,
        legacy_checkpoint_path: Optional[Path] = None,
        interval_s: float = CHECKPOINT_INTERVAL_S,
        clock: Callable[[], float] = time.time,
    ):
        self.registry_path = Path(registry_path) if registry_path else REGISTRY_PATH
        self.checkpoint_path = Path(checkpoint_path) if checkpoint_path else CHECKPOINT_PATH
        self.legacy_checkpoint_path = Path(legacy_checkpoint_path) if legacy_checkpoint_path else LEGACY_CHECKPOINT_PATH
        self.interval_s = float(interval_s)
        self._clock = clock
        self._engine = CelestialClockArchitecture()
        self._boot_unix = clock()
        self._counts: Dict[str, int] = {}
        self._last_stamp: Optional[CelestialStamp] = None
        self._clock_stepped_back = 0
        self._checkpoint_writes = 0
        self._checkpoint_last_written: Optional[float] = None
        self._checkpoint_last_error: Optional[str] = None
        self._previous_checkpoint: Optional[Dict[str, Any]] = None
        self._previous_source: Optional[str] = None
        self._started = False
        self.frames: Dict[int, CelestialFrame] = {1: FRAME_1}
        self.active_frame: CelestialFrame = FRAME_1
        self.registry_error: Optional[str] = None
        self.frame_fallback = False
        self._load_registry()
        self._read_previous_checkpoint()

    # -- registry --------------------------------------------------------------
    def _load_registry(self) -> None:
        try:
            frames, active = load_registry(self.registry_path)
            self.frames, self.active_frame = frames, frames[active]
            self.registry_error, self.frame_fallback = None, False
        except FrameRegistryError as e:
            self.frames, self.active_frame = {1: FRAME_1}, FRAME_1
            self.registry_error, self.frame_fallback = str(e), True
            logger.error(f"Celestial frame registry invalid ({e}); stamping with frame 1's built-in constants, marked frame_fallback.")

    def frame(self, frame_id: int) -> CelestialFrame:
        if frame_id not in self.frames:
            raise KeyError(f"unknown celestial frame {frame_id}")
        return self.frames[frame_id]

    def frame_constants(self, frame_id: Optional[int] = None) -> Dict[str, Any]:
        """The constants a display needs to compute the same vector (GET /celestial/frame)."""
        fr = self.active_frame if frame_id is None else self.frame(frame_id)
        return {
            "frame": fr.frame_id,
            "active": fr.frame_id == self.active_frame.frame_id,
            "frame_fallback": self.frame_fallback,
            "rotation": {"ref_unix": fr.rot_ref_unix, "period_s": fr.rot_period_s, "anchor_lon": fr.anchor_lon},
            "lunar": {"ref_unix": fr.lunar_ref_unix, "period_s": fr.lunar_period_s},
            "orbit": {"ref_unix": fr.orbit_ref_unix, "period_s": fr.orbit_period_s, "eccentricity": fr.eccentricity},
            "sigma": fr.sigma,
        }

    # -- stamping --------------------------------------------------------------
    def vector(self, at: float, frame: Optional[CelestialFrame] = None) -> Tuple[float, float, float, int, float]:
        fr = frame or self.active_frame
        v = self._engine.compute_4d_coordinates(at=at, frame=fr)
        turn = math.floor((at - fr.orbit_ref_unix) / fr.orbit_period_s)
        return v.earth_rotation_deg, v.lunar_cycle_ratio, v.orbital_trajectory_pos, turn, v.spiral_accuracy_depth

    def stamp(self, kind: str = "event", at: Optional[float] = None) -> CelestialStamp:
        """One stamp: civil time + the active frame's vector + frame id + provenance. No I/O."""
        now = self._clock() if at is None else float(at)
        if at is None and self._last_stamp is not None and now < self._last_stamp.unix - 1.0:
            self._clock_stepped_back += 1
        fr = self.active_frame
        rot, lun, orb, turn, sigma = self.vector(now, fr)
        st = CelestialStamp(
            schema=STAMP_SCHEMA,
            frame=fr.frame_id,
            unix=now,
            utc=datetime.fromtimestamp(now, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            civil=datetime.fromtimestamp(now, _LOCAL_TZ).isoformat(timespec="seconds"),
            rot_deg=rot,
            lun=lun,
            orb=orb,
            turn=turn,
            sigma=sigma,
            grid=grid_bucket(rot, orb),
            label=pointer_label(rot, lun, orb),
            kind=str(kind),
            provenance=PROVENANCE_TRUE_CLOCK,
            frame_fallback=self.frame_fallback,
        )
        self._counts[st.kind] = self._counts.get(st.kind, 0) + 1
        if at is None:
            self._last_stamp = st
        return st

    def ccid(self, prefix: str = "CCID", stamp: Optional[CelestialStamp] = None) -> str:
        st = stamp or self.stamp("ccid")
        return f"{prefix}_{int(st.unix)}"

    # -- checkpoint ------------------------------------------------------------
    def _read_previous_checkpoint(self) -> None:
        """Read the last checkpoint once (new path first, then the legacy tracked file). Never writes."""
        for source, path in (("checkpoint", self.checkpoint_path), ("legacy", self.legacy_checkpoint_path)):
            try:
                if path.is_file():
                    with open(path, "r", encoding="utf-8") as fh:
                        data = json.load(fh)
                    if isinstance(data, dict) and isinstance(data.get("unix_epoch"), (int, float)):
                        self._previous_checkpoint, self._previous_source = data, source
                        return
            except Exception as e:
                logger.warning(f"Could not read celestial checkpoint {path}: {e}")

    @property
    def previous_checkpoint(self) -> Optional[Dict[str, Any]]:
        return self._previous_checkpoint

    def reboot_delta(self) -> Optional[float]:
        """Seconds between the last checkpoint before this start and this start (downtime, bounded by the timer)."""
        if self._previous_checkpoint is None:
            return None
        return self._boot_unix - float(self._previous_checkpoint["unix_epoch"])

    def write_checkpoint(self, reason: str = "timer") -> Optional[Dict[str, Any]]:
        """The only writer of the checkpoint. Atomic. Returns the record, or None if the write failed (logged)."""
        st = self.stamp("checkpoint")
        record = {
            "schema": CHECKPOINT_SCHEMA,
            "writer": "celestial_sentinel",
            "reason": reason,
            "pid": os.getpid(),
            "frame": st.frame,
            "unix_epoch": st.unix,
            "utc_iso": st.utc,
            "civil_dt": st.civil_dt(),
            "celestial_vector": st.vector_dict(),
            "grid_bucket": st.grid,
            "label": st.label,
            "boot_unix": self._boot_unix,
            "written_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            _write_json_atomic(self.checkpoint_path, record)
        except Exception as e:
            self._checkpoint_last_error = f"{type(e).__name__}: {e}"
            logger.warning(f"Celestial checkpoint write failed: {self._checkpoint_last_error}")
            return None
        self._checkpoint_writes += 1
        self._checkpoint_last_written = st.unix
        self._checkpoint_last_error = None
        return record

    def start(self) -> Optional[float]:
        """Kernel start: report the reboot delta, then write the first checkpoint. Returns the delta."""
        delta = self.reboot_delta()
        if delta is not None:
            logger.info(f"Celestial reboot delta: {delta:.1f}s since the last checkpoint ({self._previous_source})")
        else:
            logger.info("No earlier celestial checkpoint found: fresh temporal boot.")
        if self.frame_fallback:
            logger.error(f"Celestial Sentinel running on frame-1 fallback: {self.registry_error}")
        self.write_checkpoint("start")
        self._started = True
        return delta

    def stop(self) -> None:
        if self._started:
            self.write_checkpoint("stop")
            self._started = False

    async def run_checkpoint_loop(self) -> None:
        """Lifespan task: one checkpoint every interval. Failures are recorded and retried at the next tick."""
        while True:
            await asyncio.sleep(self.interval_s)
            self.write_checkpoint("timer")

    # -- status ----------------------------------------------------------------
    def status(self) -> Dict[str, Any]:
        """Read-only state. Calling it never writes anything."""
        now = self._clock()
        last = self._last_stamp
        try:
            reg_hash = hashlib.sha256(self.registry_path.read_bytes()).hexdigest()[:16]
        except Exception:
            reg_hash = None
        return {
            "service": "celestial_sentinel",
            "active_frame": self.active_frame.frame_id,
            "frames": sorted(self.frames),
            "frame_fallback": self.frame_fallback,
            "registry": {"path": str(self.registry_path), "sha16": reg_hash, "valid": self.registry_error is None,
                         "error": self.registry_error},
            "sigma": self.active_frame.sigma,
            "sigma_note": "fixed at 1.0 (ruling R5); Zenkai recalibration is not wired",
            "last_stamp": ({"unix": last.unix, "utc": last.utc, "kind": last.kind, "label": last.label}
                           if last else None),
            "stamps_since_boot": dict(sorted(self._counts.items())),
            "clock_stepped_back": self._clock_stepped_back,
            "boot_unix": self._boot_unix,
            "reboot_delta_s": self.reboot_delta(),
            "checkpoint": {
                "path": str(self.checkpoint_path),
                "writes_since_boot": self._checkpoint_writes,
                "last_written_unix": self._checkpoint_last_written,
                "age_s": (now - self._checkpoint_last_written) if self._checkpoint_last_written else None,
                "interval_s": self.interval_s,
                "last_error": self._checkpoint_last_error,
                "previous_source": self._previous_source,
            },
        }


# ─── PROCESS-WIDE INSTANCE ───────────────────────────────────────────────────

_SENTINEL: Optional[CelestialSentinel] = None


def get_sentinel() -> CelestialSentinel:
    """The process-wide Sentinel, created on first use (reads the registry and the last checkpoint; writes nothing)."""
    global _SENTINEL
    if _SENTINEL is None:
        _SENTINEL = CelestialSentinel()
    return _SENTINEL


def set_sentinel(sentinel: Optional[CelestialSentinel]) -> None:
    """Replace the process-wide Sentinel (tests)."""
    global _SENTINEL
    _SENTINEL = sentinel


def stamp(kind: str = "event", at: Optional[float] = None) -> CelestialStamp:
    return get_sentinel().stamp(kind, at)


def stamp_dict(kind: str = "event") -> Optional[Dict[str, Any]]:
    """A stamp as a dict for a writer, or None if stamping failed (logged; a writer never fails because of it)."""
    try:
        return get_sentinel().stamp(kind).to_dict()
    except Exception as e:
        logger.warning(f"Celestial stamp failed for {kind}: {e}")
        return None
