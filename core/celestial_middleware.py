"""
INTEGRA O/S: CELESTIAL CLOCK MIDDLEWARE — TEMPORAL INVARIANT ENFORCEMENT
Module: core/celestial_middleware.py
Layer: 7 → 2 Bridge (Time → Mind)
Status: BLOCK 2 / PHASE D — SOVEREIGN TEMPORAL INJECTION

Purpose:
    Provides a single source of temporal truth for all Integra microservices.
    All modules MUST use get_celestial_timestamp() instead of datetime.now().
    
    The Celestial Clock is not decorative — it is the temporal anchor for:
    1. Save state metadata and CCID stamps
    2. SWDS cycle checkpoints
    3. Rodin mapping point coordinates
    4. Hoard node 4D spacetime stamps (x, y, z, t)
    5. Reboot continuity — on system restart, the clock can mathematically
       recall the last boot/live checkpoint and resume with correct celestial time.

Architecture:
    - On first call, attempts to reach http://localhost:8000/clock/full
    - Uses exponential backoff with 3 retries (health-check loop)
    - If kernel is unreachable (startup race), falls back to DEGRADED_MODE
      with datetime.now(UTC) + a warning flag
    - Once the kernel is up, automatically upgrades to SOVEREIGN_MODE
    
Checkpoint Persistence:
    - Writes last known celestial state to config/celestial_checkpoint.json
    - On reboot, reads checkpoint to compute elapsed celestial delta
    - Ensures dΦ continuity across restarts
"""

import os
import json
import time
import asyncio
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger("integra-celestial-middleware")

# --- Paths ---
_PROJECT_ROOT = Path(__file__).parent.parent  # integra-homebase/
_CHECKPOINT_PATH = _PROJECT_ROOT / "config" / "celestial_checkpoint.json"

# --- Clock Service Config ---
_CLOCK_URL = "http://localhost:8000/clock/full"
_MAX_RETRIES = 3
_INITIAL_DELAY = 0.5
_BACKOFF_FACTOR = 2.0


@dataclass
class CelestialTimestamp:
    """Unified temporal coordinate for all Integra microservices."""
    civil_dt: str               # YYYY-MM-DD HH:MM:SS CDT
    utc_iso: str                # ISO-8601 UTC
    unix_epoch: float           # Unix timestamp
    celestial_vector: Optional[Dict[str, Any]] = None  # dΦ, angular momentum, etc.
    ccid: Optional[str] = None  # Cheshire Cat ID for this moment
    grid_bucket: Optional[str] = None  # Grid bucket identifier
    mode: str = "SOVEREIGN"     # SOVEREIGN or DEGRADED
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CelestialMiddleware:
    """
    Singleton middleware managing celestial clock connections and checkpoint persistence.
    
    Architecture:
        - Health-check loop with exponential backoff on startup
        - Persists last known state to celestial_checkpoint.json
        - On reboot, loads checkpoint and computes celestial delta
        - Automatically upgrades from DEGRADED to SOVEREIGN when clock comes online
    """
    
    def __init__(self):
        self._mode = "INITIALIZING"
        self._last_response: Optional[Dict[str, Any]] = None
        self._last_checkpoint: Optional[Dict[str, Any]] = None
        self._boot_time = time.time()
        self._clock_online = False
        self._http_client = None
        
        # Load last checkpoint for reboot continuity
        self._load_checkpoint()
    
    def _load_checkpoint(self):
        """Load the last celestial checkpoint from disk for reboot continuity."""
        try:
            if _CHECKPOINT_PATH.exists():
                with open(_CHECKPOINT_PATH, "r", encoding="utf-8") as f:
                    self._last_checkpoint = json.load(f)
                logger.info(
                    f"Celestial checkpoint loaded — last boot: "
                    f"{self._last_checkpoint.get('civil_dt', 'UNKNOWN')}"
                )
            else:
                logger.info("No celestial checkpoint found — fresh boot.")
        except Exception as e:
            logger.warning(f"Failed to load celestial checkpoint: {e}")
            self._last_checkpoint = None
    
    def _persist_checkpoint(self, timestamp: CelestialTimestamp):
        """Persist the current celestial state to disk for reboot continuity."""
        try:
            _CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
            checkpoint_data = timestamp.to_dict()
            checkpoint_data["persisted_at"] = datetime.now(timezone.utc).isoformat()
            checkpoint_data["boot_uptime_s"] = round(time.time() - self._boot_time, 2)
            
            with open(_CHECKPOINT_PATH, "w", encoding="utf-8") as f:
                json.dump(checkpoint_data, f, indent=2, default=str)
        except Exception as e:
            logger.warning(f"Failed to persist celestial checkpoint: {e}")
    
    async def _fetch_clock(self) -> Optional[Dict[str, Any]]:
        """Fetch /clock/full from the Genesis Kernel with error handling."""
        try:
            # Lazy import to avoid circular dependency at module load time
            import httpx
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(_CLOCK_URL)
                if response.status_code == 200:
                    return response.json()
        except ImportError:
            # httpx not available, try urllib
            try:
                import urllib.request
                import urllib.error
                req = urllib.request.Request(_CLOCK_URL)
                with urllib.request.urlopen(req, timeout=2) as resp:
                    return json.loads(resp.read().decode())
            except Exception:
                pass
        except Exception:
            pass
        return None
    
    async def _health_check_with_backoff(self) -> bool:
        """
        Attempt to reach the Celestial Clock with exponential backoff.
        Returns True if clock is online, False if all retries exhausted.
        """
        delay = _INITIAL_DELAY
        for attempt in range(_MAX_RETRIES + 1):
            result = await self._fetch_clock()
            if result is not None:
                self._last_response = result
                self._clock_online = True
                self._mode = "SOVEREIGN"
                logger.info(f"Celestial Clock online (attempt {attempt + 1})")
                return True
            if attempt < _MAX_RETRIES:
                logger.info(
                    f"Celestial Clock not ready (attempt {attempt + 1}/{_MAX_RETRIES + 1}), "
                    f"retrying in {delay:.1f}s..."
                )
                await asyncio.sleep(delay)
                delay *= _BACKOFF_FACTOR
        
        self._mode = "DEGRADED"
        logger.warning(
            "Celestial Clock unreachable after backoff — entering DEGRADED_MODE. "
            "Using UTC fallback. Will auto-upgrade when clock comes online."
        )
        return False
    
    def _build_degraded_timestamp(self) -> CelestialTimestamp:
        """Build a degraded timestamp using system UTC when clock is unreachable."""
        now = datetime.now(timezone.utc)
        civil_dt = now.strftime("%Y-%m-%d %H:%M:%S UTC")
        
        # If we have a checkpoint, compute elapsed delta
        elapsed_note = None
        if self._last_checkpoint:
            last_epoch = self._last_checkpoint.get("unix_epoch", 0)
            if last_epoch:
                elapsed = time.time() - last_epoch
                elapsed_note = f"Elapsed since last checkpoint: {elapsed:.0f}s"
        
        return CelestialTimestamp(
            civil_dt=civil_dt,
            utc_iso=now.isoformat(),
            unix_epoch=time.time(),
            celestial_vector=self._last_checkpoint.get("celestial_vector") if self._last_checkpoint else None,
            ccid=f"CCID_{int(time.time())}",
            grid_bucket=None,
            mode="DEGRADED",
        )
    
    def _build_sovereign_timestamp(self, clock_data: Dict[str, Any]) -> CelestialTimestamp:
        """Build a sovereign timestamp from live /clock/full response."""
        # Extract fields from the clock response
        digital = clock_data.get("digital_numerical_clock", {})
        celestial = clock_data.get("celestial_spacetime_vector", clock_data.get("celestial_kinematic_vector", {}))
        
        civil_dt = digital.get("local_datetime_cdt", 
                    digital.get("civil_datetime",
                    datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S CDT")))
        utc_iso = digital.get("utc_iso8601",
                   digital.get("utc_iso",
                   datetime.now(timezone.utc).isoformat()))
        
        return CelestialTimestamp(
            civil_dt=civil_dt,
            utc_iso=utc_iso,
            unix_epoch=time.time(),
            celestial_vector=celestial,
            ccid=f"CCID_{int(time.time())}",
            grid_bucket=clock_data.get("grid_bucket"),
            mode="SOVEREIGN",
        )
    
    async def get_timestamp(self) -> CelestialTimestamp:
        """
        THE primary entry point. All microservices call this instead of datetime.now().
        
        Behavior:
        1. If clock is online → returns SOVEREIGN timestamp with live dΦ
        2. If clock was online but becomes unreachable → attempts reconnect
        3. If clock never reached → returns DEGRADED with UTC + checkpoint data
        """
        if not self._clock_online:
            # Try to connect (with backoff on first attempt, single try on subsequent)
            if self._mode == "INITIALIZING":
                await self._health_check_with_backoff()
            else:
                # Quick single attempt to auto-upgrade
                result = await self._fetch_clock()
                if result is not None:
                    self._last_response = result
                    self._clock_online = True
                    self._mode = "SOVEREIGN"
        
        if self._clock_online:
            # Try to get fresh data
            result = await self._fetch_clock()
            if result is not None:
                self._last_response = result
                ts = self._build_sovereign_timestamp(result)
                self._persist_checkpoint(ts)
                return ts
            else:
                # Clock went offline — degrade gracefully
                self._clock_online = False
                self._mode = "DEGRADED"
                logger.warning("Celestial Clock went offline — degrading to UTC fallback")
        
        return self._build_degraded_timestamp()
    
    def get_last_checkpoint(self) -> Optional[Dict[str, Any]]:
        """Returns the last persisted checkpoint for reboot delta computation."""
        return self._last_checkpoint
    
    def get_reboot_delta(self) -> Optional[float]:
        """
        Computes the time elapsed since the last checkpoint.
        Used on reboot to mathematically recall the correct celestial position.
        """
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
    """Returns the last persisted celestial checkpoint."""
    return _middleware.get_last_checkpoint()


def get_reboot_delta() -> Optional[float]:
    """Returns seconds elapsed since last checkpoint (for reboot continuity)."""
    return _middleware.get_reboot_delta()


def celestial_time() -> float:
    """
    SYNCHRONOUS drop-in replacement for time.time().
    
    Returns the unix epoch from the last known celestial state.
    If the middleware has a cached server response, uses that.
    If checkpoint exists, uses checkpoint + elapsed since boot.
    Falls back to time.time() if nothing is available.
    
    Usage:
        from core.celestial_middleware import celestial_time
        created_at = celestial_time()   # instead of time.time()
    """
    # Priority 1: Last server response (SOVEREIGN mode)
    if _middleware._last_response:
        dig = _middleware._last_response.get("digital_clock", {})
        epoch = dig.get("unix_timestamp")
        if epoch:
            return float(epoch)
    
    # Priority 2: Checkpoint + elapsed delta
    cp = _middleware._last_checkpoint
    if cp and cp.get("unix_epoch"):
        elapsed = time.time() - _middleware._boot_time
        return cp["unix_epoch"] + elapsed
    
    # Priority 3: Raw system time (DEGRADED)
    return time.time()


def celestial_ccid(prefix: str = "CCID") -> str:
    """
    Generate a CCID stamped with celestial epoch instead of system time.
    
    Usage:
        from core.celestial_middleware import celestial_ccid
        ccid = celestial_ccid("CRYSTAL")  # → "CCID_CRYSTAL_1790214787"
    """
    epoch = int(celestial_time())
    return f"{prefix}_{epoch}"
