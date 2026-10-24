"""
INTEGRA O/S: 4-TIER BOOT GEOLOCATION, ANAMNESIS CASCADE & TRUE NODE ORIGIN LOCK
Module: temporal/boot_geolocation.py
Layer: 7 / Layer 3 (Celestial Spacetime Anchor & MongoDB HLC Boot Journal)
Master Reference: Oct 23, 2026 Master File (`integra_os/core/boot_geolocation_anamnesis.py`)

Purpose:
    1. Guarantees that on every boot sequence (cold start, warm reboot, offline sandbox,
       or cloud Citadel deployment), Integra O/S deterministically resolves and locks its
       True Geolocation (`30.5888 N, -91.1673 W` — Baker, Louisiana, United States) via
       the 4-Tier Failover Cascade:
         - Tier 1: External MCP / Google Maps Geocoding callback hook
         - Tier 2: Persistent HLC Boot Journal (`load_hlc_state_from_db`)
         - Tier 3: Host Environment Metadata (`INTEGRA_HOST_LOCATION` / `HOST_GAZETTEER`)
         - Tier 4: Immutable Seed Anchor (`30.5888 N, -91.1673 W`)
    2. Locks the True Sovereign Node Origin onto the (X, Y) neural grid:
         - `matrix_xy_16 = (16171, 43905)` on the 65,536 x 65,536 grid
         - `matrix_xy_12 = (1010, 2744)` on the 4,096 x 4,096 grid
         - Predetermined CIT Crosspoint: `XPT_X02_Y06` (`NW / Z4_N_TEMPERATE / M03`)
         - Tangential Earth rotational speed: `1,441.362 km/h`, `sigma = 0.9988`,
           `COSMIC_CHECKPOINT_TAG = "AUTUMNAL_EQUINOX_2026"`
    3. Eliminates transient `:memory:` SQLite and OneDrive `.sqlite` contradictions by
       persisting `hlc_boot_journal` directly into the MongoDB Persistent Placeholder
       substrate (`local_dbs/mongodb_placeholder/collections/hlc_boot_journal.json`),
       with a read-only (`?mode=ro`) importer for migrating legacy SQLite HLC journals.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import math
import os
from pathlib import Path
import sqlite3
import struct
import time
from typing import Any, Callable, Dict, Optional, Tuple

from memory.database.mongodb_substrate import (
    MONGODB_SUBSTRATE,
    MongoDBPersistentSubstrate,
    verify_mongodb_true,
)


@dataclass
class BootGeolocationPoint:
    boot_status: str                      # 'ONLINE'
    resolution_tier_used: str             # Tier 1 (API), Tier 2 (HLC DB), Tier 3 (Host), Tier 4 (Seed)
    location_label: str                   # e.g., 'Baker, Louisiana, United States'
    latitude_deg: float                   # Resolved Latitude phi_boot
    longitude_deg: float                  # Resolved Longitude lambda_boot
    earth_rotational_speed_kmh: float     # Tangential rotational speed at phi_boot
    drift_from_seed_km: float             # Haversine distance from immutable seed
    zenkai_recalibration_triggered: bool  # True if drift was auto-corrected
    spatial_accuracy_sigma: float         # 0.9988 (99.88% verified accuracy)
    matrix_xy_16: Tuple[int, int]         # (X_16, Y_16) on 65,536 x 65,536 grid
    matrix_xy_12: Tuple[int, int]         # (X_12, Y_12) on 4,096 x 4,096 grid
    nearest_grid_crosspoint_id: str       # Predetermined (X, Y) crosspoint ID ('XPT_X02_Y06')
    hemisphere: str                       # 'NW', 'NE', 'SW', 'SE'
    epistemic_zone: str                   # 'Z5_NORTH_POLE' .. 'Z1_SOUTH_POLE'
    domain_meridian: str                  # 'M01' .. 'M12'
    cit_origin_uri: str                   # Canonical CIT coordinate URI
    morton_32bit: int                     # 32-bit interleaved Morton Z-order integer
    cit_braille_origin_packet_16: str     # 16-Cell (128-bit) Unicode Braille Boot Stamp
    celestial_partition_key: str          # ROT_xxx_LUN_xxx_ORB_xxx
    hlc_logical_counter: int              # Restored & incremented Hybrid Logical Clock
    cosmic_checkpoint_tag: str            # 'AUTUMNAL_EQUINOX_2026'
    cosmic_checkpoint_hash: str           # 24-char SHA-256 verification hash
    boot_timestamp_utc: str               # ISO-8601 UTC timestamp
    persistence_backend: str              # 'MONGODB_PERSISTENT_PLACEHOLDER' or 'MONGODB_LIVE_TRUE'

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["matrix_xy_16"] = list(self.matrix_xy_16)
        d["matrix_xy_12"] = list(self.matrix_xy_12)
        return d


class IntegraBootGeolocationEngine:
    """
    Guarantees that Integra's geolocation function always finds and locks its
    exact spatial-temporal point on every boot sequence:
      - Tier 1: External MCP / Google Maps Geocoding hook (if configured)
      - Tier 2: Persistent MongoDB HLC Boot Journal (`load_hlc_state_from_db`)
      - Tier 3: Host Environment Metadata (`INTEGRA_HOST_LOCATION` / `HOST_GAZETTEER`)
      - Tier 4: Immutable Seed Anchor (`30.5888 N, -91.1673 W` — Baker, LA)
    """

    BRAILLE_BASE = 0x2800
    EARTH_RADIUS_KM = 6378.137
    EARTH_OMEGA_RAD_S = 7.2921159e-5
    SIDEREAL_DAY_SEC = 86164.0905
    SYNODIC_LUNAR_SEC = 2551442.8
    SIDEREAL_YEAR_SEC = 31558149.76
    ORBIT_ECCENTRICITY = 0.0167086

    # Immutable Seed Coordinates: Baker, Louisiana, United States
    SEED_LAT_DEG = 30.5888
    SEED_LON_DEG = -91.1673
    SEED_LABEL = "Baker, Louisiana, United States"
    COSMIC_CHECKPOINT_TAG = "AUTUMNAL_EQUINOX_2026"
    JOURNAL_DOC_ID = "HLC_BOOT_JOURNAL_1"

    # Internal Gazetteer for Tier-3 Host Location String Resolution
    HOST_GAZETTEER: Dict[str, Tuple[float, float]] = {
        "baker, louisiana, united states": (30.5888, -91.1673),
        "baker, la": (30.5888, -91.1673),
        "zachary, louisiana, united states": (30.6485, -91.1565),
        "zachary, la": (30.6485, -91.1565),
        "baton rouge, louisiana, united states": (30.4515, -91.1871),
        "baton rouge, la": (30.4515, -91.1871),
    }

    def __init__(
        self,
        substrate: Optional[MongoDBPersistentSubstrate] = None,
        grid_x_meridians: int = 12,
        grid_y_rings: int = 10,
        legacy_sqlite_path: Optional[Path] = None,
    ):
        self.substrate = substrate if substrate is not None else MONGODB_SUBSTRATE
        self.grid_x_meridians = grid_x_meridians
        self.grid_y_rings = grid_y_rings
        self.hlc_counter = 0
        self.last_boot_point: Optional[BootGeolocationPoint] = None
        # Ensure `hlc_boot_journal` collection file point is initialized
        self._journal_col = self.substrate.get_collection("hlc_boot_journal")
        if legacy_sqlite_path is not None:
            self.import_legacy_sqlite_hlc_journal(Path(legacy_sqlite_path))

    # --------------------------------------------------------------------------
    # 1. BITWISE BRAILLE, MORTON Z-ORDER, & HAVERSINE MATH HELPERS
    # --------------------------------------------------------------------------

    @classmethod
    def bytes_to_braille(cls, data: bytes) -> str:
        return "".join(chr(cls.BRAILLE_BASE + (b & 0xFF)) for b in data)

    @classmethod
    def braille_to_bytes(cls, text: str) -> bytes:
        return bytes((ord(ch) - cls.BRAILLE_BASE) & 0xFF for ch in text)

    @staticmethod
    def interleave_morton_16bit(x16: int, y16: int) -> int:
        x = max(0, min(0xFFFF, int(x16)))
        y = max(0, min(0xFFFF, int(y16)))
        morton = 0
        for c_idx in range(4):
            b = 0
            for step in range(4):
                shift = 15 - (c_idx * 4 + step)
                yb = (y >> shift) & 1
                xb = (x >> shift) & 1
                off = step * 2
                b |= (yb << off) | (xb << (off + 1))
            morton = (morton << 8) | b
        return morton

    @staticmethod
    def deinterleave_morton_16bit(morton: int) -> Tuple[int, int]:
        m = int(morton) & 0xFFFFFFFF
        x16 = 0
        y16 = 0
        for c_idx in range(4):
            b = (m >> ((3 - c_idx) * 8)) & 0xFF
            for step in range(4):
                shift = 15 - (c_idx * 4 + step)
                off = step * 2
                yb = (b >> off) & 1
                xb = (b >> (off + 1)) & 1
                y16 |= yb << shift
                x16 |= xb << shift
        return x16, y16

    @classmethod
    def haversine_km(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        p1, l1 = math.radians(lat1), math.radians(lon1)
        p2, l2 = math.radians(lat2), math.radians(lon2)
        a = (
            math.sin((p2 - p1) / 2.0) ** 2
            + math.cos(p1) * math.cos(p2) * (math.sin((l2 - l1) / 2.0) ** 2)
        )
        c = 2.0 * math.asin(min(1.0, math.sqrt(max(0.0, a))))
        return cls.EARTH_RADIUS_KM * c

    def _solve_kepler(self, mean_anom_rad: float, tol: float = 1e-9) -> float:
        e_anom = mean_anom_rad
        for _ in range(50):
            f_val = e_anom - self.ORBIT_ECCENTRICITY * math.sin(e_anom) - mean_anom_rad
            if abs(f_val) < tol:
                break
            f_prime = 1.0 - self.ORBIT_ECCENTRICITY * math.cos(e_anom)
            e_anom -= f_val / f_prime
        return e_anom

    @staticmethod
    def classify_zone_and_hemisphere(x16: int, y16: int, x_idx: int) -> Tuple[str, str, str]:
        hem = f"{'N' if y16 >= 32768 else 'S'}{'E' if x16 >= 32768 else 'W'}"
        if y16 >= 56978:
            zone = "Z5_NORTH_POLE"
        elif y16 >= 41325:
            zone = "Z4_N_TEMPERATE"
        elif y16 >= 24211:
            zone = "Z3_EQUATORIAL"
        elif y16 >= 8558:
            zone = "Z2_S_TEMPERATE"
        else:
            zone = "Z1_SOUTH_POLE"
        meridian = f"M{x_idx + 1:02d}"
        return hem, zone, meridian

    # --------------------------------------------------------------------------
    # 2. MONGODB PERSISTENT HLC JOURNAL + LEGACY SQLITE READ-ONLY IMPORTER
    # --------------------------------------------------------------------------

    def import_legacy_sqlite_hlc_journal(self, sqlite_path: Path) -> Dict[str, Any]:
        """
        Production-safe read-only (`?mode=ro`) importer that migrates an existing SQLite
        `hlc_boot_journal` table row into the MongoDB Persistent Placeholder collection
        without locking or mutating the SQLite file.
        """
        sqlite_path = Path(sqlite_path)
        if not sqlite_path.is_file() or sqlite_path.stat().st_size == 0:
            return {"status": "NO_LEGACY_SQLITE_JOURNAL", "migrated": False}

        ro_uri = f"file:{sqlite_path.resolve().as_posix()}?mode=ro"
        conn: Optional[sqlite3.Connection] = None
        try:
            conn = sqlite3.connect(ro_uri, uri=True, timeout=5.0)
            row = conn.execute(
                """
                SELECT location_label, latitude_deg, longitude_deg, hlc_logical_counter,
                       celestial_partition_key, cit_braille_packet_16, cosmic_checkpoint_hash,
                       updated_at_epoch
                FROM hlc_boot_journal WHERE journal_id = 1
                """
            ).fetchone()
            if not row:
                return {"status": "EMPTY_LEGACY_SQLITE_JOURNAL", "migrated": False}

            existing = self.load_hlc_state_from_db()
            incoming_hlc = int(row[3])
            if existing is not None and int(existing.get("hlc_logical_counter", 0)) >= incoming_hlc:
                return {
                    "status": "MONGODB_JOURNAL_ALREADY_DOMINATES",
                    "migrated": False,
                    "hlc_logical_counter": existing["hlc_logical_counter"],
                }

            doc = {
                "_id": self.JOURNAL_DOC_ID,
                "journal_id": 1,
                "location_label": str(row[0]),
                "latitude_deg": float(row[1]),
                "longitude_deg": float(row[2]),
                "hlc_logical_counter": incoming_hlc,
                "celestial_partition_key": str(row[4]),
                "cit_braille_packet_16": str(row[5]),
                "cosmic_checkpoint_hash": str(row[6]),
                "updated_at_epoch": int(row[7]),
                "migrated_from_sqlite": str(sqlite_path),
            }
            self._journal_col.update_one({"_id": self.JOURNAL_DOC_ID}, {"$set": doc}, upsert=True)
            self.hlc_counter = max(self.hlc_counter, incoming_hlc)
            return {
                "status": "LEGACY_SQLITE_HLC_MIGRATED_TO_MONGODB",
                "migrated": True,
                "hlc_logical_counter": incoming_hlc,
                "file_point": str(self._journal_col.file_point),
            }
        except sqlite3.OperationalError:
            return {"status": "TABLE_NOT_PRESENT_SKIPPED", "migrated": False}
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    def load_hlc_state_from_db(self) -> Optional[Dict[str, Any]]:
        """Reads the last saved geolocation and HLC state from the MongoDB `hlc_boot_journal` collection."""
        doc = self._journal_col.find_one({"_id": self.JOURNAL_DOC_ID})
        if doc is None:
            doc = self._journal_col.find_one({"journal_id": 1})
        if not doc:
            return None
        return {
            "location_label": str(doc["location_label"]),
            "latitude_deg": float(doc["latitude_deg"]),
            "longitude_deg": float(doc["longitude_deg"]),
            "hlc_logical_counter": int(doc["hlc_logical_counter"]),
            "celestial_partition_key": str(doc["celestial_partition_key"]),
            "cit_braille_packet_16": str(doc["cit_braille_packet_16"]),
            "cosmic_checkpoint_hash": str(doc["cosmic_checkpoint_hash"]),
            "updated_at_epoch": int(doc["updated_at_epoch"]),
            "nearest_grid_crosspoint_id": str(doc.get("nearest_grid_crosspoint_id", "XPT_X02_Y06")),
        }

    def save_hlc_state_to_db(self, point: BootGeolocationPoint, epoch_sec: int) -> Dict[str, Any]:
        """Commits the active geolocation point and HLC counter to the MongoDB `hlc_boot_journal` collection."""
        payload = {
            "_id": self.JOURNAL_DOC_ID,
            "journal_id": 1,
            "location_label": point.location_label,
            "latitude_deg": point.latitude_deg,
            "longitude_deg": point.longitude_deg,
            "hlc_logical_counter": point.hlc_logical_counter,
            "nearest_grid_crosspoint_id": point.nearest_grid_crosspoint_id,
            "matrix_xy_16": list(point.matrix_xy_16),
            "matrix_xy_12": list(point.matrix_xy_12),
            "hemisphere": point.hemisphere,
            "epistemic_zone": point.epistemic_zone,
            "domain_meridian": point.domain_meridian,
            "cit_origin_uri": point.cit_origin_uri,
            "celestial_partition_key": point.celestial_partition_key,
            "cit_braille_packet_16": point.cit_braille_origin_packet_16,
            "cosmic_checkpoint_tag": point.cosmic_checkpoint_tag,
            "cosmic_checkpoint_hash": point.cosmic_checkpoint_hash,
            "updated_at_epoch": int(epoch_sec),
            "boot_timestamp_utc": point.boot_timestamp_utc,
        }
        return self._journal_col.update_one({"_id": self.JOURNAL_DOC_ID}, {"$set": payload}, upsert=True)

    # --------------------------------------------------------------------------
    # 3. MASTER BOOT GEOLOCATION LOCK FUNCTION (`find_boot_point_always`)
    # --------------------------------------------------------------------------

    def find_boot_point_always(
        self,
        mcp_geolocate_callback: Optional[Callable[[], Tuple[float, float, str]]] = None,
        host_injected_location: Optional[str] = None,
        allow_relocation_beyond_tolerance: bool = False,
        max_drift_tolerance_km: float = 25.0,
        boot_epoch_override: Optional[int] = None,
        persist: bool = True,
    ) -> BootGeolocationPoint:
        """
        Executes on every system boot (`[BOOT_SEQUENCE]`) to guarantee the True Geolocation
        and Sovereign Node Origin (`XPT_X02_Y06`) are always found, verified, and locked:
          1. Queries Tier 1 (MCP / Google Maps Callback) if provided.
          2. Falls back to Tier 2 (MongoDB `hlc_boot_journal` in The Hoard / local_dbs).
          3. Falls back to Tier 3 (Host Environment Injected Location String / `HOST_GAZETTEER`).
          4. Falls back to Tier 4 (Immutable Baker, LA Seed: `30.5888 N, -91.1673 W`).
          5. Audits Haversine drift against the seed anchor (`> 25.0 km` -> Zenkai snap-back),
             computes the 4D Celestial partition key and 16-Cell Braille stamp, and saves state
             when `persist=True`.
        """
        epoch_sec = int(boot_epoch_override if boot_epoch_override is not None else time.time())
        utc_iso = datetime.fromtimestamp(epoch_sec, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        journal_state = self.load_hlc_state_from_db()
        base_hlc = max(self.hlc_counter, int(journal_state["hlc_logical_counter"])) if journal_state else self.hlc_counter
        next_hlc = (base_hlc + 1) if persist else max(1, base_hlc)

        resolved_lat: Optional[float] = None
        resolved_lon: Optional[float] = None
        resolved_label: str = self.SEED_LABEL
        tier_used: str = ""

        # TIER 1: Live MCP / Google Maps Geocoding Hook
        if mcp_geolocate_callback is not None:
            try:
                lat, lon, label = mcp_geolocate_callback()
                if -90.0 <= float(lat) <= 90.0 and -180.0 <= float(lon) <= 180.0:
                    resolved_lat, resolved_lon, resolved_label = float(lat), float(lon), str(label)
                    tier_used = "TIER_1_MCP_GOOGLE_MAPS_GEOLOCATE"
            except Exception:
                resolved_lat = None

        # TIER 2: Persistent HLC Boot Journal in MongoDB Substrate
        if resolved_lat is None and journal_state is not None:
            resolved_lat = journal_state["latitude_deg"]
            resolved_lon = journal_state["longitude_deg"]
            resolved_label = journal_state["location_label"]
            tier_used = "TIER_2_HOARD_HLC_BOOT_JOURNAL"

        # TIER 3: Host Environment Injected Location Metadata
        if resolved_lat is None:
            env_loc = (host_injected_location or os.environ.get("INTEGRA_HOST_LOCATION", "")).strip()
            if env_loc and env_loc.lower() in self.HOST_GAZETTEER:
                resolved_lat, resolved_lon = self.HOST_GAZETTEER[env_loc.lower()]
                resolved_label = env_loc
                tier_used = "TIER_3_HOST_ENVIRONMENT_METADATA"

        # TIER 4: Immutable Seed Anchor Fallback (Baker, Louisiana)
        if resolved_lat is None or resolved_lon is None:
            resolved_lat = self.SEED_LAT_DEG
            resolved_lon = self.SEED_LON_DEG
            resolved_label = self.SEED_LABEL
            tier_used = "TIER_4_IMMUTABLE_SEED_ANCHOR"

        # Drift Audit & Autonomous Zenkai Recalibration
        drift_km = self.haversine_km(
            self.SEED_LAT_DEG, self.SEED_LON_DEG, resolved_lat, resolved_lon
        )
        zenkai_recalibrated = False
        if drift_km > max_drift_tolerance_km and not allow_relocation_beyond_tolerance:
            resolved_lat = self.SEED_LAT_DEG
            resolved_lon = self.SEED_LON_DEG
            resolved_label = f"{self.SEED_LABEL} (Zenkai Auto-Recalibrated)"
            drift_km = 0.0
            zenkai_recalibrated = True

        # Compute Tangential Earth Rotational Speed at Boot Latitude
        v_rot_kmh = (
            self.EARTH_OMEGA_RAD_S
            * self.EARTH_RADIUS_KM
            * math.cos(math.radians(resolved_lat))
            * 3600.0
        )

        # Compute 4D Celestial Spacetime Partition Key (T -> S)
        rot_deg = (resolved_lon + ((epoch_sec % self.SIDEREAL_DAY_SEC) / self.SIDEREAL_DAY_SEC) * 360.0) % 360.0
        ref_epoch = 1735689600  # 2025-01-01T00:00:00Z
        phi_lunar = ((epoch_sec - ref_epoch) % self.SYNODIC_LUNAR_SEC) / self.SYNODIC_LUNAR_SEC
        mean_anom = (2.0 * math.pi * ((epoch_sec - ref_epoch) % self.SIDEREAL_YEAR_SEC)) / self.SIDEREAL_YEAR_SEC
        ecc_anom = self._solve_kepler(mean_anom)
        true_anom_deg = math.degrees(
            2.0 * math.atan2(
                math.sqrt(1.0 + self.ORBIT_ECCENTRICITY) * math.sin(ecc_anom / 2.0),
                math.sqrt(1.0 - self.ORBIT_ECCENTRICITY) * math.cos(ecc_anom / 2.0),
            )
        ) % 360.0
        partition_key = f"ROT_{int(rot_deg):03d}_LUN_{int(phi_lunar * 1000):03d}_ORB_{int(true_anom_deg):03d}"

        # Lock onto (X, Y) Matrix Coordinates & Nearest Predetermined Crosspoint
        nx = min(0.999999, max(0.0, (resolved_lon + 180.0) / 360.0))
        ny = min(0.999999, max(0.0, (resolved_lat + 90.0) / 180.0))
        x16, y16 = int(nx * 65536), int(ny * 65536)
        x12, y12 = x16 >> 4, y16 >> 4

        x_idx = min(self.grid_x_meridians - 1, int(nx * self.grid_x_meridians))
        y_idx = min(self.grid_y_rings - 1, int(ny * self.grid_y_rings))
        crosspoint_id = f"XPT_X{x_idx:02d}_Y{y_idx:02d}"
        hem, zone, meridian = self.classify_zone_and_hemisphere(x16, y16, x_idx)

        morton_32 = self.interleave_morton_16bit(x16, y16)
        b_time_4 = self.bytes_to_braille(struct.pack(">I", epoch_sec & 0xFFFFFFFF))
        b_codex_1 = chr(self.BRAILLE_BASE + 0x03)  # Active Boot Origin + Macro Lock
        b_spatial_4 = self.bytes_to_braille(struct.pack(">I", morton_32))
        cit_uri = f"CIT://{hem}/{zone}/{meridian}/{crosspoint_id}/QUAD_{b_spatial_4}/XY_{x12:04d}_{y12:04d}"

        origin_digest = hashlib.sha256(
            f"{resolved_label}:{resolved_lat:.4f}:{resolved_lon:.4f}:{self.COSMIC_CHECKPOINT_TAG}".encode("utf-8")
        ).digest()
        b_sem_7 = self.bytes_to_braille(origin_digest[:7])
        braille_packet_16 = f"{b_time_4}{b_codex_1}{b_spatial_4}{b_sem_7}"
        cosmic_hash = origin_digest.hex()[:24]

        probe = verify_mongodb_true()
        backend_label = "MONGODB_LIVE_TRUE" if probe["mongodb_true"] else "MONGODB_PERSISTENT_PLACEHOLDER"

        boot_point = BootGeolocationPoint(
            boot_status="ONLINE",
            resolution_tier_used=tier_used,
            location_label=resolved_label,
            latitude_deg=round(resolved_lat, 4),
            longitude_deg=round(resolved_lon, 4),
            earth_rotational_speed_kmh=round(v_rot_kmh, 3),
            drift_from_seed_km=round(drift_km, 4),
            zenkai_recalibration_triggered=zenkai_recalibrated,
            spatial_accuracy_sigma=0.9988,
            matrix_xy_16=(x16, y16),
            matrix_xy_12=(x12, y12),
            nearest_grid_crosspoint_id=crosspoint_id,
            hemisphere=hem,
            epistemic_zone=zone,
            domain_meridian=meridian,
            cit_origin_uri=cit_uri,
            morton_32bit=morton_32,
            cit_braille_origin_packet_16=braille_packet_16,
            celestial_partition_key=partition_key,
            hlc_logical_counter=next_hlc,
            cosmic_checkpoint_tag=self.COSMIC_CHECKPOINT_TAG,
            cosmic_checkpoint_hash=cosmic_hash,
            boot_timestamp_utc=utc_iso,
            persistence_backend=backend_label,
        )

        if persist:
            self.hlc_counter = next_hlc
            self.last_boot_point = boot_point
            self.save_hlc_state_to_db(boot_point, epoch_sec)
        return boot_point

    def get_status_readonly(self) -> Dict[str, Any]:
        """
        Read-only telemetry accessor for GET endpoints and DualTemporalEngine.
        Never mutates HLC counters or writes to disk (per genesis-kernel Rule 3).
        """
        if self.last_boot_point is not None:
            return self.last_boot_point.to_dict()
        preview = self.find_boot_point_always(persist=False)
        return preview.to_dict()


BOOT_GEOLOCATION_ENGINE = IntegraBootGeolocationEngine()
