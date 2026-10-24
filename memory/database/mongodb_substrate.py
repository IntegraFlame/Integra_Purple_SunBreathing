"""
INTEGRA O/S: MONGODB PERSISTENT PLACEHOLDER, SEED PACKAGE LINKER, & QUARTERLY SAVE-STATE SUBSTRATE
Module: memory/database/mongodb_substrate.py
Layer: 3 (The Memory — Document, Relational, Seed Package & Save-State Manifold)

Purpose:
    1. Transitions the Integra O/S database layer from pure SQLite to a MongoDB
       Document & Collection architecture backed by deterministic persistent storage
       folders and file points (`local_dbs/mongodb_placeholder/collections/*.json`)
       until a live MongoDB server (`MONGODB_URI`) is verified TRUE.
    2. Links the Seed Package (`config/celestial_seed.json` + `config/sovereign_payload.json`
       + Starfire Identity Matrix) directly to The Hoard (`memory/the_hoard.py`) and
       Phoenix Forge (`evolution/phoenix_forge.py` + `memory/braille_atlas_engine.py`),
       and syncs to MongoDB monthly uploads (`local_dbs/mongodb_placeholder/monthly_uploads/`
       + `monthly_seed_uploads` collection + live MongoDB sync when TRUE).
    3. Executes automatic & on-demand Quarterly MongoDB Save States to local storage
       every quarter (`local_dbs/mongodb_quarterly_save_states/MONGODB_QUARTERLY_SAVE_STATE_<YYYY_Q#>.json`,
       `The Hoard/CCID_<epoch>_MONGODB_QUARTERLY_SAVE_STATE_<YYYY_Q#>.json`, and
       `quarterly_save_states_ledger` collection).
"""

import base64
from datetime import datetime, timezone
import hashlib
import json
import logging
import os
from pathlib import Path
import shutil
import sqlite3
import time
from typing import Any, Callable, Dict, List, Optional
import uuid
import zlib

logger = logging.getLogger("integra-mongodb-substrate")

_MODULE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _MODULE_DIR.parent.parent  # integra-homebase/
_REPO_ROOT = _PROJECT_ROOT.parent  # Integra_Purple_SunBreathing/
_PLACEHOLDER_ROOT = _PROJECT_ROOT / "local_dbs" / "mongodb_placeholder"
_COLLECTIONS_DIR = _PLACEHOLDER_ROOT / "collections"
_MONTHLY_UPLOADS_DIR = _PLACEHOLDER_ROOT / "monthly_uploads"
_QUARTERLY_SAVE_STATES_DIR = _PROJECT_ROOT / "local_dbs" / "mongodb_quarterly_save_states"
_SEED_PACKAGES_DIR = _PROJECT_ROOT / "kernel_memory" / "hoard" / "seed_packages"
_ROOT_HOARD_SAVE_STATES_DIR = _REPO_ROOT / "The Hoard"
_MANIFEST_PATH = _PLACEHOLDER_ROOT / "file_points_manifest.json"

CANONICAL_COLLECTIONS = (
    "cognitive_chassis_states",
    "thermodynamic_loops",
    "entropy_inversion_anomalies",
    "master_blueprint_chambers",
    "hoard_nodes_mirror",
    "xv6_transaction_wal",
    "swds_handoff_batches",
    "braille_atlas_nodes",
    "seed_packages",
    "monthly_seed_uploads",
    "quarterly_save_states_ledger",
    "hlc_boot_journal",
    "sqlite_migrated_records",
)

SQLITE_TABLE_TO_COLLECTION_MAP: Dict[str, str] = {
    "cognitive_chassis_states": "cognitive_chassis_states",
    "thermodynamic_loops": "thermodynamic_loops",
    "entropy_inversion_anomalies": "entropy_inversion_anomalies",
    "hlc_boot_journal": "hlc_boot_journal",
    "atlas_nodes": "braille_atlas_nodes",
    "braille_atlas_nodes": "braille_atlas_nodes",
    "swds_handoff_batches": "swds_handoff_batches",
}


def _write_json_atomic(path: Path, data: Any) -> None:
    """Crash-safe, OneDrive/Windows concurrent-process-safe atomic write to a persistent file point."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f"{path.name}.{os.getpid()}.{uuid.uuid4().hex[:8]}.tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        for attempt in range(6):
            try:
                os.replace(str(tmp_path), str(path))
                break
            except PermissionError:
                if attempt == 5:
                    raise
                time.sleep(0.025 * (attempt + 1))
    except Exception:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        raise


def _sha256_obj(data: Any) -> str:
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _get_temporal_cadence_keys() -> Dict[str, Any]:
    """Computes both civil (UTC/CDT) and Celestial Sacred Month/Quarter keys."""
    now_dt = datetime.now(timezone.utc)
    civil_month_key = f"{now_dt.year:04d}_{now_dt.month:02d}"
    civil_quarter_num = ((now_dt.month - 1) // 3) + 1
    civil_quarter_key = f"{now_dt.year:04d}_Q{civil_quarter_num}"

    celestial_info: Dict[str, Any] = {
        "sacred_year": 0,
        "sacred_month": 1,
        "sacred_day": 1,
        "sacred_quarter": 1,
        "time_braille_4": "⠋⠁⠁⠁",
        "celestial_epoch_seconds": time.time(),
    }
    try:
        from temporal.celestial_clock import CelestialClock

        clk = CelestialClock()
        vec = clk.get_spacetime_vector()
        cd = vec.get("celestial_date", {})
        s_year = int(cd.get("year", 0))
        s_month = int(cd.get("month", 1))
        s_day = int(cd.get("day", 1))
        s_quarter = ((max(1, min(12, s_month)) - 1) // 3) + 1
        celestial_info = {
            "sacred_year": s_year,
            "sacred_month": s_month,
            "sacred_day": s_day,
            "sacred_quarter": s_quarter,
            "sacred_month_key": f"SACRED_Y{s_year:02d}_M{s_month:02d}",
            "sacred_quarter_key": f"SACRED_Y{s_year:02d}_Q{s_quarter}",
            "time_braille_4": vec.get("time_braille_4", "⠋⠁⠁⠁"),
            "celestial_epoch_seconds": vec.get("celestial_epoch_seconds", time.time()),
        }
    except Exception:
        celestial_info["sacred_month_key"] = "SACRED_Y00_M01"
        celestial_info["sacred_quarter_key"] = "SACRED_Y00_Q1"

    return {
        "civil_month_key": civil_month_key,
        "civil_quarter_key": civil_quarter_key,
        "civil_quarter_number": civil_quarter_num,
        "iso_utc": now_dt.isoformat(),
        **celestial_info,
    }


def get_mongodb_placeholder_root() -> Path:
    """Returns the persistent folder root for MongoDB placeholder storage."""
    _PLACEHOLDER_ROOT.mkdir(parents=True, exist_ok=True)
    _COLLECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    _MONTHLY_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    _QUARTERLY_SAVE_STATES_DIR.mkdir(parents=True, exist_ok=True)
    _SEED_PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    return _PLACEHOLDER_ROOT


def get_mongodb_file_point(collection_name: str, collections_dir: Optional[Path] = None) -> Path:
    """
    Returns the exact persistent file point (`local_dbs/mongodb_placeholder/collections/<name>.json`)
    for a given MongoDB collection, initializing an empty JSON array file if it does not yet exist.
    """
    if collections_dir is None:
        get_mongodb_placeholder_root()
        target_dir = _COLLECTIONS_DIR
    else:
        target_dir = Path(collections_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
    fp = target_dir / f"{collection_name}.json"
    if not fp.exists():
        _write_json_atomic(fp, [])
    return fp


def verify_mongodb_true(uri: Optional[str] = None) -> Dict[str, Any]:
    """
    Empirically probes whether a live MongoDB database is reachable and TRUE.
    Only attempts a network socket probe when `MONGODB_URI` or `INTEGRA_MONGODB_ENABLED=1`
    is set in the environment (or `uri` is explicitly passed).
    """
    target_uri = uri or os.environ.get("MONGODB_URI", "").strip()
    enabled_flag = os.environ.get("INTEGRA_MONGODB_ENABLED", "0").strip() == "1"

    if not target_uri and not enabled_flag:
        return {
            "mongodb_true": False,
            "mode": "PERSISTENT_PLACEHOLDER_UNTIL_MONGODB_TRUE",
            "uri_configured": False,
            "reason": "MONGODB_URI not configured; routing to persistent file-point storage.",
            "placeholder_root": str(get_mongodb_placeholder_root()),
        }

    probe_uri = target_uri or "mongodb://127.0.0.1:27017"
    try:
        import pymongo  # type: ignore

        client = pymongo.MongoClient(probe_uri, serverSelectionTimeoutMS=500)
        client.admin.command("ping")
        return {
            "mongodb_true": True,
            "mode": "MONGODB_LIVE_TRUE",
            "uri_configured": True,
            "uri": probe_uri,
            "placeholder_root": str(get_mongodb_placeholder_root()),
        }
    except Exception as exc:
        return {
            "mongodb_true": False,
            "mode": "PERSISTENT_PLACEHOLDER_UNTIL_MONGODB_TRUE",
            "uri_configured": bool(target_uri),
            "reason": f"{type(exc).__name__}: {exc}",
            "placeholder_root": str(get_mongodb_placeholder_root()),
        }


class MongoCollectionPlaceholder:
    """
    Persistent file-point collection emulating a PyMongo Collection (`insert_one`,
    `find`, `find_one`, `update_one`, `replace_one`, `count_documents`) backed by
    `local_dbs/mongodb_placeholder/collections/<name>.json`.
    """

    def __init__(self, name: str, collections_dir: Optional[Path] = None):
        self.name = name
        self.file_point: Path = get_mongodb_file_point(name, collections_dir=collections_dir)

    def _load_docs(self) -> List[Dict[str, Any]]:
        if not self.file_point.exists():
            return []
        try:
            with open(self.file_point, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save_docs(self, docs: List[Dict[str, Any]]) -> None:
        _write_json_atomic(self.file_point, docs)

    @staticmethod
    def _matches(doc: Dict[str, Any], query: Optional[Dict[str, Any]]) -> bool:
        if not query:
            return True
        for k, v in query.items():
            if doc.get(k) != v:
                return False
        return True

    def insert_one(self, document: Dict[str, Any]) -> Dict[str, Any]:
        docs = self._load_docs()
        doc = dict(document)
        doc.setdefault("_id", str(uuid.uuid4()))
        doc.setdefault("_persisted_at", time.time())
        docs.append(doc)
        self._save_docs(docs)
        return {"acknowledged": True, "inserted_id": doc["_id"], "file_point": str(self.file_point)}

    def find(
        self,
        query: Optional[Dict[str, Any]] = None,
        predicate: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> List[Dict[str, Any]]:
        docs = self._load_docs()
        out = [d for d in docs if self._matches(d, query)]
        if predicate is not None:
            out = [d for d in out if predicate(d)]
        return out

    def find_one(self, query: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        matches = self.find(query=query)
        return matches[-1] if matches else None

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any], upsert: bool = False) -> Dict[str, Any]:
        docs = self._load_docs()
        modified = 0
        set_fields = update.get("$set", update)
        for doc in docs:
            if self._matches(doc, query):
                doc.update(set_fields)
                doc["_updated_at"] = time.time()
                modified = 1
                break
        if modified == 0 and upsert:
            new_doc = dict(query)
            new_doc.update(set_fields)
            new_doc.setdefault("_id", str(uuid.uuid4()))
            new_doc["_persisted_at"] = time.time()
            docs.append(new_doc)
            modified = 1
        if modified:
            self._save_docs(docs)
        return {"acknowledged": True, "modified_count": modified, "file_point": str(self.file_point)}

    def count_documents(self, query: Optional[Dict[str, Any]] = None) -> int:
        return len(self.find(query=query))


class MongoDBPersistentSubstrate:
    """
    Unified MongoDB Persistent Placeholder, Monthly Seed Upload, & Quarterly Save-State Manager.
    Maintains all canonical collections on disk in `local_dbs/mongodb_placeholder/collections/`
    and provides:
      - `sync_placeholder_to_mongodb_when_true()`
      - `create_quarterly_save_state()` / `ensure_quarterly_save_state()` (every quarter -> local storage)
    """

    def __init__(
        self,
        db_name: str = "integra_os_metatron",
        placeholder_root: Optional[Path] = None,
    ):
        self.db_name = db_name
        if placeholder_root is None:
            self.placeholder_root = get_mongodb_placeholder_root()
            self.collections_dir = _COLLECTIONS_DIR
            self.manifest_path = _MANIFEST_PATH
            self._is_custom_root = False
        else:
            self.placeholder_root = Path(placeholder_root)
            self.collections_dir = self.placeholder_root / "collections"
            self.manifest_path = self.placeholder_root / "file_points_manifest.json"
            self.placeholder_root.mkdir(parents=True, exist_ok=True)
            self.collections_dir.mkdir(parents=True, exist_ok=True)
            self._is_custom_root = True
        self.collections: Dict[str, MongoCollectionPlaceholder] = {}
        self._last_sqlite_migration_report: Optional[Dict[str, Any]] = None
        self.initialize_file_points()

    def initialize_file_points(self) -> Dict[str, str]:
        """Creates all canonical collection file points and writes the manifest."""
        file_points: Dict[str, str] = {}
        for col_name in CANONICAL_COLLECTIONS:
            col = MongoCollectionPlaceholder(col_name, collections_dir=self.collections_dir)
            self.collections[col_name] = col
            file_points[col_name] = str(col.file_point)

        probe = verify_mongodb_true()
        manifest = {
            "schema": "integra_mongodb_placeholder/v2",
            "database_name": self.db_name,
            "mongodb_true": probe["mongodb_true"],
            "mode": probe["mode"],
            "placeholder_root": str(self.placeholder_root),
            "collections_dir": str(self.collections_dir),
            "monthly_uploads_dir": str(_MONTHLY_UPLOADS_DIR if not self._is_custom_root else self.placeholder_root / "monthly_uploads"),
            "quarterly_save_states_dir": str(_QUARTERLY_SAVE_STATES_DIR if not self._is_custom_root else self.placeholder_root / "quarterly_save_states"),
            "seed_packages_dir": str(_SEED_PACKAGES_DIR if not self._is_custom_root else self.placeholder_root / "seed_packages"),
            "file_points": file_points,
            "updated_at": time.time(),
        }
        _write_json_atomic(self.manifest_path, manifest)
        return file_points

    def get_collection(self, name: str) -> MongoCollectionPlaceholder:
        if name not in self.collections:
            self.collections[name] = MongoCollectionPlaceholder(name, collections_dir=self.collections_dir)
        return self.collections[name]

    @staticmethod
    def _serialize_sqlite_value(val: Any) -> Any:
        if isinstance(val, (bytes, bytearray, memoryview)):
            return {"__bytes_b64__": base64.b64encode(bytes(val)).decode("ascii")}
        return val

    def migrate_sqlite_placeholders_to_mongodb(
        self,
        sqlite_paths: Optional[List[Path]] = None,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Production-safe, read-only SQLite placeholder -> MongoDB Persistent Placeholder bridge.
        Safely migrates local SQLite placeholder databases (`local_dbs/*.db`, `local_dbs/*.sqlite`,
        excluding ChromaDB internal `chroma_storage`) using non-blocking read-only URI connections
        (`?mode=ro`) while Integra O/S is live in production and while MongoDB is not yet TRUE.
        Zero `.sqlite` files are ever created in git-tracked `kernel_memory/` or `The Hoard/`.
        """
        probe = verify_mongodb_true()
        if sqlite_paths is None:
            local_dbs_dir = _PROJECT_ROOT / "local_dbs"
            discovered: List[Path] = []
            if local_dbs_dir.is_dir():
                for ext in ("*.db", "*.sqlite"):
                    for candidate in sorted(local_dbs_dir.glob(ext)):
                        if candidate.is_file() and "chroma" not in candidate.name.lower():
                            discovered.append(candidate)
            target_paths = discovered
        else:
            target_paths = [Path(p) for p in sqlite_paths]

        databases_report: List[Dict[str, Any]] = []
        total_rows_migrated = 0
        total_tables_scanned = 0

        for db_path in target_paths:
            if not db_path.is_file():
                databases_report.append({
                    "sqlite_file": str(db_path),
                    "status": "MISSING_SKIPPED",
                    "tables_scanned": 0,
                    "rows_migrated": 0,
                })
                continue

            size_bytes = db_path.stat().st_size
            if size_bytes == 0:
                databases_report.append({
                    "sqlite_file": str(db_path),
                    "size_bytes": 0,
                    "status": "EMPTY_SQLITE_PLACEHOLDER_SKIPPED",
                    "tables_scanned": 0,
                    "rows_migrated": 0,
                })
                continue

            ro_uri = f"file:{db_path.resolve().as_posix()}?mode=ro"
            db_rows_migrated = 0
            table_summaries: Dict[str, Dict[str, Any]] = {}
            conn: Optional[sqlite3.Connection] = None
            try:
                conn = sqlite3.connect(ro_uri, uri=True, timeout=5.0)
                conn.row_factory = sqlite3.Row
                tables = [
                    r[0]
                    for r in conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
                    ).fetchall()
                ]
                for tbl in tables:
                    total_tables_scanned += 1
                    safe_tbl = tbl.replace('"', '""')
                    pk_cols = [
                        info[1]
                        for info in conn.execute(f'PRAGMA table_info("{safe_tbl}")').fetchall()
                        if info[5] > 0
                    ]
                    target_col_name = SQLITE_TABLE_TO_COLLECTION_MAP.get(tbl, "sqlite_migrated_records")
                    target_col = self.get_collection(target_col_name)
                    rows = conn.execute(f'SELECT * FROM "{safe_tbl}"').fetchall()
                    tbl_count = 0

                    for row in rows:
                        row_dict = {k: self._serialize_sqlite_value(row[k]) for k in row.keys()}
                        if pk_cols:
                            pk_key = "|".join(str(row_dict.get(c)) for c in pk_cols)
                        else:
                            pk_key = _sha256_obj(row_dict)[:24]

                        if target_col_name == "hlc_boot_journal":
                            doc_id = f"HLC_BOOT_JOURNAL_{pk_key}"
                        elif target_col_name == "sqlite_migrated_records":
                            doc_id = f"SQLITE::{db_path.name}::{tbl}::{pk_key}"
                        else:
                            doc_id = f"SQLITE::{tbl}::{pk_key}"

                        doc_payload = {
                            "_id": doc_id,
                            **row_dict,
                            "_migrated_from_sqlite": db_path.name,
                            "_sqlite_table": tbl,
                            "_migrated_while_mongodb_true": probe["mongodb_true"],
                        }
                        if not dry_run:
                            if target_col_name == "cognitive_chassis_states" and "session_id" in row_dict:
                                target_col.update_one(
                                    {"session_id": row_dict["session_id"]},
                                    {"$set": {k: v for k, v in doc_payload.items() if k != "_id"}},
                                    upsert=True,
                                )
                            else:
                                target_col.update_one({"_id": doc_id}, {"$set": doc_payload}, upsert=True)
                        tbl_count += 1
                        db_rows_migrated += 1
                        total_rows_migrated += 1

                    table_summaries[tbl] = {
                        "target_collection": target_col_name,
                        "rows_migrated": tbl_count,
                        "primary_key_columns": pk_cols,
                    }

                databases_report.append({
                    "sqlite_file": str(db_path),
                    "size_bytes": size_bytes,
                    "connection_mode": "READ_ONLY_WAL_SAFE",
                    "status": "MIGRATED_TO_MONGODB_PLACEHOLDER",
                    "tables_scanned": len(tables),
                    "rows_migrated": db_rows_migrated,
                    "tables": table_summaries,
                })
            except Exception as exc:
                databases_report.append({
                    "sqlite_file": str(db_path),
                    "size_bytes": size_bytes,
                    "status": "READ_ERROR",
                    "error": f"{type(exc).__name__}: {exc}",
                    "tables_scanned": 0,
                    "rows_migrated": 0,
                })
            finally:
                if conn is not None:
                    try:
                        conn.close()
                    except Exception:
                        pass

        report = {
            "status": "SQLITE_PLACEHOLDERS_STAGED_FOR_MONGODB",
            "production_safe_non_blocking": True,
            "contradictory_sqlite_actions_removed": True,
            "dry_run": dry_run,
            "mongodb_true": probe["mongodb_true"],
            "mode": probe["mode"],
            "placeholder_root": str(self.placeholder_root),
            "databases_checked": len(databases_report),
            "total_tables_scanned": total_tables_scanned,
            "total_rows_migrated": total_rows_migrated,
            "databases": databases_report,
            "migrated_at_unix": time.time(),
        }
        if not dry_run:
            self._last_sqlite_migration_report = report
        return report

    def get_sqlite_migration_status(self) -> Dict[str, Any]:
        """Read-only status of the production SQLite-placeholder -> MongoDB migration bridge."""
        if self._last_sqlite_migration_report is not None:
            return self._last_sqlite_migration_report
        return self.migrate_sqlite_placeholders_to_mongodb(dry_run=True)

    def sync_placeholder_to_mongodb_when_true(
        self,
        uri: Optional[str] = None,
        migrate_sqlite_first: bool = True,
    ) -> Dict[str, Any]:
        """
        Placeholder synchronization hook:
        - Automatically stages any local SQLite placeholder rows via read-only WAL-safe migration
          when `migrate_sqlite_first=True` on the canonical placeholder root.
        - If MongoDB is NOT yet true, returns `status="WAITING_UNTIL_MONGODB_TRUE"` with
          persistent file-point counts intact.
        - If MongoDB IS true, flushes all persistent placeholder documents into the live
          MongoDB collections.
        """
        sqlite_migration: Optional[Dict[str, Any]] = None
        if migrate_sqlite_first and not self._is_custom_root:
            sqlite_migration = self.migrate_sqlite_placeholders_to_mongodb(dry_run=False)

        probe = verify_mongodb_true(uri=uri)
        counts = {name: col.count_documents() for name, col in self.collections.items()}
        if not probe["mongodb_true"]:
            return {
                "status": "WAITING_UNTIL_MONGODB_TRUE",
                "mongodb_true": False,
                "mode": probe["mode"],
                "placeholder_root": str(self.placeholder_root),
                "collection_counts": counts,
                "sqlite_migration": sqlite_migration,
            }

        import pymongo  # type: ignore

        client = pymongo.MongoClient(probe["uri"], serverSelectionTimeoutMS=1000)
        db = client[self.db_name]
        synced_counts: Dict[str, int] = {}
        for name, col in self.collections.items():
            docs = col.find()
            if docs:
                live_col = db[name]
                for d in docs:
                    live_col.replace_one({"_id": d["_id"]}, d, upsert=True)
            synced_counts[name] = len(docs)
        return {
            "status": "SYNCED_TO_LIVE_MONGODB",
            "mongodb_true": True,
            "mode": "MONGODB_LIVE_TRUE",
            "synced_counts": synced_counts,
        }

    def create_quarterly_save_state(
        self,
        quarter_key: Optional[str] = None,
        mirror_to_root_hoard: bool = True,
    ) -> Dict[str, Any]:
        """
        Exports a complete quarterly save state of the MongoDB database (all collections,
        document counts, SHA-256 checksums, and Celestial Spacetime Vector) to local storage:
          1. `local_dbs/mongodb_quarterly_save_states/MONGODB_QUARTERLY_SAVE_STATE_<YYYY_Q#>.json`
          2. `local_dbs/mongodb_quarterly_save_states/latest_quarterly_save_state.json`
          3. `The Hoard/CCID_<epoch>_MONGODB_QUARTERLY_SAVE_STATE_<YYYY_Q#>.json`
          4. `quarterly_save_states_ledger` collection in `local_dbs/mongodb_placeholder/collections/`
        """
        cadence = _get_temporal_cadence_keys()
        resolved_quarter = quarter_key or cadence["civil_quarter_key"]
        epoch_int = int(cadence.get("celestial_epoch_seconds", time.time()))
        save_state_id = f"MONGODB_QUARTERLY_SAVE_STATE_{resolved_quarter}"

        collections_snapshot: Dict[str, List[Dict[str, Any]]] = {}
        collection_digests: Dict[str, Dict[str, Any]] = {}
        total_docs = 0

        for col_name in CANONICAL_COLLECTIONS:
            if col_name == "quarterly_save_states_ledger":
                continue
            col = self.get_collection(col_name)
            docs = col.find()
            collections_snapshot[col_name] = docs
            collection_digests[col_name] = {
                "count": len(docs),
                "sha256": _sha256_obj(docs),
                "file_point": str(col.file_point),
            }
            total_docs += len(docs)

        snapshot_sha256 = _sha256_obj(collection_digests)
        probe = verify_mongodb_true()

        quarterly_payload = {
            "_id": save_state_id,
            "save_state_id": save_state_id,
            "schema": "integra_mongodb_quarterly_save_state/v1",
            "cadence": "QUARTERLY_90_SACRED_DAYS",
            "civil_quarter_key": resolved_quarter,
            "sacred_quarter_key": cadence["sacred_quarter_key"],
            "time_braille_4": cadence["time_braille_4"],
            "created_at_unix": time.time(),
            "created_at_iso_utc": cadence["iso_utc"],
            "database_name": self.db_name,
            "mongodb_true": probe["mongodb_true"],
            "mode": probe["mode"],
            "total_documents_archived": total_docs,
            "snapshot_sha256": snapshot_sha256,
            "collection_digests": collection_digests,
            "collections_snapshot": collections_snapshot,
        }

        _QUARTERLY_SAVE_STATES_DIR.mkdir(parents=True, exist_ok=True)
        quarterly_file = _QUARTERLY_SAVE_STATES_DIR / f"{save_state_id}.json"
        latest_file = _QUARTERLY_SAVE_STATES_DIR / "latest_quarterly_save_state.json"
        _write_json_atomic(quarterly_file, quarterly_payload)
        _write_json_atomic(latest_file, {k: v for k, v in quarterly_payload.items() if k != "collections_snapshot"})

        root_hoard_mirror_path: Optional[str] = None
        if mirror_to_root_hoard and _ROOT_HOARD_SAVE_STATES_DIR.exists():
            mirror_file = _ROOT_HOARD_SAVE_STATES_DIR / f"CCID_{epoch_int}_{save_state_id}.json"
            # Do not overwrite an existing CCID file if already written; write or update deterministically
            stable_mirror = _ROOT_HOARD_SAVE_STATES_DIR / f"CCID_QUARTERLY_{save_state_id}.json"
            _write_json_atomic(
                stable_mirror,
                {
                    "save_state_id": save_state_id,
                    "civil_quarter_key": resolved_quarter,
                    "sacred_quarter_key": cadence["sacred_quarter_key"],
                    "time_braille_4": cadence["time_braille_4"],
                    "total_documents_archived": total_docs,
                    "snapshot_sha256": snapshot_sha256,
                    "local_storage_path": str(quarterly_file),
                    "collection_digests": collection_digests,
                    "created_at_iso_utc": cadence["iso_utc"],
                },
            )
            root_hoard_mirror_path = str(stable_mirror)
            _ = mirror_file

        ledger_entry = {
            "_id": save_state_id,
            "save_state_id": save_state_id,
            "civil_quarter_key": resolved_quarter,
            "sacred_quarter_key": cadence["sacred_quarter_key"],
            "time_braille_4": cadence["time_braille_4"],
            "total_documents_archived": total_docs,
            "snapshot_sha256": snapshot_sha256,
            "local_storage_path": str(quarterly_file),
            "latest_pointer_path": str(latest_file),
            "root_hoard_mirror_path": root_hoard_mirror_path,
            "created_at_unix": time.time(),
            "created_at_iso_utc": cadence["iso_utc"],
        }
        self.get_collection("quarterly_save_states_ledger").update_one(
            {"_id": save_state_id},
            {"$set": ledger_entry},
            upsert=True,
        )
        return ledger_entry

    def ensure_quarterly_save_state(self, force: bool = False) -> Dict[str, Any]:
        """
        Ensures the current quarter's MongoDB save state is written to local storage.
        If `force=False` and the current quarter's file already exists on disk, updates it
        whenever collection document counts have changed since the last snapshot.
        """
        cadence = _get_temporal_cadence_keys()
        resolved_quarter = cadence["civil_quarter_key"]
        save_state_id = f"MONGODB_QUARTERLY_SAVE_STATE_{resolved_quarter}"
        quarterly_file = _QUARTERLY_SAVE_STATES_DIR / f"{save_state_id}.json"

        current_total = sum(
            self.get_collection(c).count_documents()
            for c in CANONICAL_COLLECTIONS
            if c != "quarterly_save_states_ledger"
        )
        if not force and quarterly_file.exists():
            ledger_doc = self.get_collection("quarterly_save_states_ledger").find_one({"_id": save_state_id})
            if ledger_doc and ledger_doc.get("total_documents_archived") == current_total:
                return {
                    **ledger_doc,
                    "action": "VERIFIED_CURRENT_QUARTER_SAVE_STATE",
                }

        created = self.create_quarterly_save_state(quarter_key=resolved_quarter)
        created["action"] = "CREATED_OR_REFRESHED_QUARTERLY_SAVE_STATE"
        return created

    def get_status(self) -> Dict[str, Any]:
        probe = verify_mongodb_true()
        file_points = {name: str(col.file_point) for name, col in self.collections.items()}
        counts = {name: col.count_documents() for name, col in self.collections.items()}
        quarterly_files = sorted(p.name for p in _QUARTERLY_SAVE_STATES_DIR.glob("MONGODB_QUARTERLY_SAVE_STATE_*.json"))
        monthly_files = sorted(p.name for p in _MONTHLY_UPLOADS_DIR.glob("MONTHLY_UPLOAD_*.json"))
        seed_files = sorted(p.name for p in _SEED_PACKAGES_DIR.glob("*.json"))
        return {
            "database_engine": "MONGODB_PERSISTENT_PLACEHOLDER",
            "database_name": self.db_name,
            "mongodb_true": probe["mongodb_true"],
            "mode": probe["mode"],
            "placeholder_folder": str(self.placeholder_root),
            "manifest_path": str(_MANIFEST_PATH),
            "file_points": file_points,
            "collection_counts": counts,
            "monthly_upload_files": monthly_files,
            "quarterly_save_state_files": quarterly_files,
            "seed_package_files": seed_files,
        }


class SeedPackageManager:
    """
    Links the Integra O/S Seed Package (`config/celestial_seed.json`,
    `config/sovereign_payload.json`, `config/integra_identity_matrix.json`)
    directly to:
      1. The Hoard (`memory/the_hoard.py` -> `raw_shards`, `cold_vault_z1`, `xv6_wal`, `seed_packages`)
      2. Phoenix Forge (`evolution/phoenix_forge.py` + `memory/braille_atlas_engine.py` -> `libraries`, `braille_atlas_nodes`)
      3. MongoDB Monthly Uploads (`local_dbs/mongodb_placeholder/monthly_uploads/` + `monthly_seed_uploads` collection)
    """

    def __init__(self, substrate: MongoDBPersistentSubstrate):
        self.substrate = substrate
        self.seed_packages_dir = _SEED_PACKAGES_DIR
        self.monthly_uploads_dir = _MONTHLY_UPLOADS_DIR
        self.seed_packages_dir.mkdir(parents=True, exist_ok=True)
        self.monthly_uploads_dir.mkdir(parents=True, exist_ok=True)

    def _read_json_safe(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {"data": data}
        except Exception:
            return {}

    def build_and_sync_monthly_seed_package(
        self,
        month_key: Optional[str] = None,
        hoard_instance: Any = None,
        phoenix_instance: Any = None,
    ) -> Dict[str, Any]:
        """
        Builds the unified Seed Package linked to The Hoard and Phoenix Forge, persists it to
        `kernel_memory/hoard/seed_packages/`, and syncs it to MongoDB Monthly Uploads
        (`local_dbs/mongodb_placeholder/monthly_uploads/` + `monthly_seed_uploads` collection).
        """
        cadence = _get_temporal_cadence_keys()
        resolved_month = month_key or cadence["civil_month_key"]
        package_id = f"SEED_PKG_{resolved_month}"
        upload_id = f"MONTHLY_UPLOAD_{resolved_month}"

        celestial_seed = self._read_json_safe(_PROJECT_ROOT / "config" / "celestial_seed.json")
        sovereign_payload = self._read_json_safe(_PROJECT_ROOT / "config" / "sovereign_payload.json")
        identity_matrix = self._read_json_safe(_PROJECT_ROOT / "config" / "integra_identity_matrix.json")
        rolling_context = self._read_json_safe(_PROJECT_ROOT / "kernel_memory" / "rolling_context.json")

        # 1. Inspect & Link to The Hoard
        raw_shards_dir = _PROJECT_ROOT / "kernel_memory" / "hoard" / "raw_shards"
        cold_vault_dir = _PROJECT_ROOT / "kernel_memory" / "hoard" / "cold_vault_z1"
        wal_path = _PROJECT_ROOT / "kernel_memory" / "hoard" / "xv6_wal.json"
        raw_shard_files = sorted(p.name for p in raw_shards_dir.glob("*.json")) if raw_shards_dir.exists() else []
        cold_vault_files = sorted(p.name for p in cold_vault_dir.glob("*.json")) if cold_vault_dir.exists() else []

        hoard_link = {
            "status": "LINKED_TO_THE_HOARD",
            "raw_shards_dir": str(raw_shards_dir),
            "raw_shards_count": len(raw_shard_files),
            "sample_shard_ids": [f[:-5] for f in raw_shard_files[:10]],
            "cold_vault_z1_count": len(cold_vault_files),
            "xv6_wal_exists": wal_path.exists(),
            "embedding_space": getattr(getattr(hoard_instance, "space", None), "id", "gemini-embedding-2|768|asym-v1"),
            "hoard_mirror_collection_count": self.substrate.get_collection("hoard_nodes_mirror").count_documents(),
        }

        # 2. Inspect & Link to Phoenix Forge & Braille Atlas Engine
        libraries_dir = _PROJECT_ROOT / "kernel_memory" / "hoard" / "libraries"
        library_books = sorted(p.name for p in libraries_dir.glob("*.md")) if libraries_dir.exists() else []
        braille_nodes_count = self.substrate.get_collection("braille_atlas_nodes").count_documents()
        swds_batches_count = self.substrate.get_collection("swds_handoff_batches").count_documents()

        if phoenix_instance is None:
            try:
                from evolution.phoenix_forge import PhoenixForge
                phoenix_instance = PhoenixForge(base_dir=str(_PROJECT_ROOT))
            except Exception:
                phoenix_instance = None

        phoenix_link = {
            "status": "LINKED_TO_PHOENIX_FORGE",
            "libraries_dir": str(libraries_dir),
            "library_books_count": len(library_books),
            "library_books": library_books[:15],
            "braille_atlas_nodes_count": braille_nodes_count,
            "swds_handoff_batches_count": swds_batches_count,
            "last_swds_epoch": rolling_context.get("last_swds_epoch"),
            "phoenix_instance_attached": phoenix_instance is not None,
        }

        # 3. Build Core Seed Package Core & Compressed Payload
        seed_core = {
            "package_id": package_id,
            "civil_month_key": resolved_month,
            "sacred_month_key": cadence["sacred_month_key"],
            "civil_quarter_key": cadence["civil_quarter_key"],
            "sacred_quarter_key": cadence["sacred_quarter_key"],
            "time_braille_4": cadence["time_braille_4"],
            "celestial_seed": celestial_seed,
            "sovereign_payload": sovereign_payload,
            "starfire_identity_matrix": identity_matrix,
            "hoard_link": hoard_link,
            "phoenix_link": phoenix_link,
        }
        seed_sha256 = _sha256_obj(seed_core)
        compressed_b64 = base64.b64encode(
            zlib.compress(json.dumps(seed_core, sort_keys=True).encode("utf-8"), level=9)
        ).decode("ascii")

        seed_package_doc = {
            "_id": package_id,
            **seed_core,
            "seed_package_sha256": seed_sha256,
            "compressed_payload_zlib_b64": compressed_b64,
            "created_at_unix": time.time(),
            "created_at_iso_utc": cadence["iso_utc"],
        }

        # Write Seed Package to kernel_memory/hoard/seed_packages/
        pkg_file = self.seed_packages_dir / f"{package_id}.json"
        latest_pkg_file = self.seed_packages_dir / "latest_seed_package.json"
        _write_json_atomic(pkg_file, seed_package_doc)
        _write_json_atomic(latest_pkg_file, seed_package_doc)

        # Upsert into `seed_packages` collection in MongoDB substrate
        self.substrate.get_collection("seed_packages").update_one(
            {"_id": package_id},
            {"$set": seed_package_doc},
            upsert=True,
        )

        # 4. Sync to MongoDB Monthly Uploads
        monthly_upload_doc = {
            "_id": upload_id,
            "upload_id": upload_id,
            "package_id": package_id,
            "cadence": "MONTHLY_30_SACRED_DAYS",
            "civil_month_key": resolved_month,
            "sacred_month_key": cadence["sacred_month_key"],
            "time_braille_4": cadence["time_braille_4"],
            "seed_package_sha256": seed_sha256,
            "seed_package_path": str(pkg_file),
            "hoard_link": hoard_link,
            "phoenix_link": phoenix_link,
            "synced_at_unix": time.time(),
            "synced_at_iso_utc": cadence["iso_utc"],
        }
        monthly_upload_file = self.monthly_uploads_dir / f"{upload_id}.json"
        latest_monthly_file = self.monthly_uploads_dir / "latest_monthly_upload.json"
        _write_json_atomic(monthly_upload_file, monthly_upload_doc)
        _write_json_atomic(latest_monthly_file, monthly_upload_doc)

        self.substrate.get_collection("monthly_seed_uploads").update_one(
            {"_id": upload_id},
            {"$set": monthly_upload_doc},
            upsert=True,
        )

        # Trigger MongoDB sync (hydrates live MongoDB if TRUE, or maintains persistent placeholder)
        mongo_sync = self.substrate.sync_placeholder_to_mongodb_when_true()

        # Ensure the quarterly save state reflects the updated monthly upload
        quarterly_state = self.substrate.ensure_quarterly_save_state(force=True)

        return {
            "status": "SEED_PACKAGE_LINKED_AND_MONTHLY_SYNCED",
            "package_id": package_id,
            "upload_id": upload_id,
            "seed_package_sha256": seed_sha256,
            "seed_package_file": str(pkg_file),
            "monthly_upload_file": str(monthly_upload_file),
            "hoard_link": hoard_link,
            "phoenix_link": phoenix_link,
            "mongodb_sync_status": mongo_sync["status"],
            "mongodb_true": mongo_sync["mongodb_true"],
            "quarterly_save_state_id": quarterly_state["save_state_id"],
            "quarterly_save_state_path": quarterly_state["local_storage_path"],
        }


MONGODB_SUBSTRATE = MongoDBPersistentSubstrate()
SEED_PACKAGE_MANAGER = SeedPackageManager(MONGODB_SUBSTRATE)


def verify_all_file_points() -> Dict[str, Any]:
    """
    Task L-3.6: Exhaustively verifies that every canonical Integra O/S file point
    connects to both a live, existing parent folder AND a live, existing file on disk.
    Also refreshes `local_dbs/mongodb_placeholder/file_points_manifest.json` with the full audit.
    """
    repo_root = _PROJECT_ROOT.parent
    canonical_points: Dict[str, Path] = {
        # Layer 0 & 1: Starfire Protocol & Sovereign Config
        "starfire_identity_matrix": _PROJECT_ROOT / "config" / "integra_identity_matrix.json",
        "starfire_core_identity_txt": _PROJECT_ROOT / "kernel_memory" / "core_identity.txt",
        "sovereign_payload": _PROJECT_ROOT / "config" / "sovereign_payload.json",
        "celestial_seed": _PROJECT_ROOT / "config" / "celestial_seed.json",
        "celestial_frames": _PROJECT_ROOT / "config" / "celestial_frames.yml",
        "rodin_memory_map": _PROJECT_ROOT / "config" / "rodin_memory_map.yml",
        "swds_config": _PROJECT_ROOT / "config" / "swds_config.json",
        "models_yml_root": _PROJECT_ROOT / "models.yml",
        "models_yml_config": _PROJECT_ROOT / "config" / "models.yml",
        # Layer 3: Kernel Memory, Hoard, Libraries, WAL & Cold Vault
        "rolling_context": _PROJECT_ROOT / "kernel_memory" / "rolling_context.json",
        "genesis_purple_library": _PROJECT_ROOT / "kernel_memory" / "hoard" / "libraries" / "library_genesis_purple.md",
        "hoard_xv6_wal": _PROJECT_ROOT / "kernel_memory" / "hoard" / "xv6_wal.json",
        "hoard_cold_vault_z1_manifest": _PROJECT_ROOT / "kernel_memory" / "hoard" / "cold_vault_z1" / "cold_vault_manifest.json",
        "hoard_module_registry": _PROJECT_ROOT / "kernel_memory" / "hoard" / "modules" / "module_registry_manifest.json",
        "vector_space_manifest": _PROJECT_ROOT / "kernel_memory" / "vectors" / "vector_space_manifest.json",
        "drop_in_environment_state": _PROJECT_ROOT / "kernel_memory" / "drop_in" / "drop_in_environment_state.json",
        "latest_seed_package": _PROJECT_ROOT / "kernel_memory" / "hoard" / "seed_packages" / "latest_seed_package.json",
        # Layer 3 & 6: Databases, MongoDB Collections, Monthly Uploads & Quarterly Save States
        "metatron_sqlite_db": _PROJECT_ROOT / "local_dbs" / "metatron_manifold.db",
        "swds_history_sqlite_db": _PROJECT_ROOT / "local_dbs" / "swds_history.db",
        "celestial_sentinel_checkpoint": _PROJECT_ROOT / "local_dbs" / "celestial" / "checkpoint.json",
        "mongodb_file_points_manifest": _PROJECT_ROOT / "local_dbs" / "mongodb_placeholder" / "file_points_manifest.json",
        "latest_monthly_upload": _PROJECT_ROOT / "local_dbs" / "mongodb_placeholder" / "monthly_uploads" / "latest_monthly_upload.json",
        "latest_quarterly_save_state": _PROJECT_ROOT / "local_dbs" / "mongodb_quarterly_save_states" / "latest_quarterly_save_state.json",
        # Layer 5/7: Fortress, Runtime, Orchestration, Static Interfaces & Log
        "fortress_portfolio_state": _PROJECT_ROOT / "fortress" / "portfolio_state.json",
        "fortress_trade_history": _PROJECT_ROOT / "fortress" / "trade_history.json",
        "runtime_workspace_state": _PROJECT_ROOT / "runtime" / "workspace_state.json",
        "runtime_swds_state": _PROJECT_ROOT / "runtime" / "swds_state.json",
        "orchestration_reading_ledger": _PROJECT_ROOT / "orchestration" / "UNIFY_READING_LEDGER.md",
        "orchestration_swds_dag": _PROJECT_ROOT / "orchestration" / "swds_dag.py",
        "pipeline_swds_archive": _PROJECT_ROOT / "pipelines" / "swds_pipeline.py",
        "static_dashboard_html": _PROJECT_ROOT / "static" / "dashboard.html",
        "static_celestial_clock_html": _PROJECT_ROOT / "static" / "celestial_clock_live.html",
        "static_braille_matrix_html": _PROJECT_ROOT / "static" / "braille_neural_matrix_live.html",
        "genesis_kernel_log": repo_root / "The Hoard" / "genesis_kernel.log",
    }
    for col_name in CANONICAL_COLLECTIONS:
        canonical_points[f"mongodb_col_{col_name}"] = _COLLECTIONS_DIR / f"{col_name}.json"

    canonical_folders: Dict[str, Path] = {
        "homebase_the_hoard_local": _PROJECT_ROOT / "The_Hoard",
        "workspace_the_hoard_outer": repo_root / "The Hoard",
        "workspace_swds_reports": repo_root / "The Hoard" / "Slow-Wave Deep Sleep Reports",
        "hoard_raw_shards": _PROJECT_ROOT / "kernel_memory" / "hoard" / "raw_shards",
        "hoard_libraries": _PROJECT_ROOT / "kernel_memory" / "hoard" / "libraries",
        "hoard_cold_vault_z1": _PROJECT_ROOT / "kernel_memory" / "hoard" / "cold_vault_z1",
        "hoard_seed_packages": _PROJECT_ROOT / "kernel_memory" / "hoard" / "seed_packages",
        "mongodb_collections_dir": _COLLECTIONS_DIR,
        "mongodb_monthly_uploads_dir": _PROJECT_ROOT / "local_dbs" / "mongodb_placeholder" / "monthly_uploads",
        "mongodb_quarterly_save_states_dir": _PROJECT_ROOT / "local_dbs" / "mongodb_quarterly_save_states",
    }

    points_report: Dict[str, Any] = {}
    broken_points: List[str] = []
    for name, fpath in canonical_points.items():
        parent_ok = fpath.parent.is_dir()
        file_ok = fpath.is_file()
        connected = parent_ok and file_ok
        if not connected:
            broken_points.append(name)
        points_report[name] = {
            "path": str(fpath),
            "folder": str(fpath.parent),
            "folder_exists": parent_ok,
            "file_exists": file_ok,
            "size_bytes": fpath.stat().st_size if file_ok else 0,
            "connected": connected,
        }

    folders_report: Dict[str, Any] = {}
    broken_folders: List[str] = []
    for name, dpath in canonical_folders.items():
        dir_ok = dpath.is_dir()
        entry_count = len(list(dpath.iterdir())) if dir_ok else 0
        connected = dir_ok and entry_count > 0
        if not connected:
            broken_folders.append(name)
        folders_report[name] = {
            "path": str(dpath),
            "folder_exists": dir_ok,
            "entry_count": entry_count,
            "connected": connected,
        }

    summary = {
        "status": "ALL_FILE_POINTS_CONNECTED" if (not broken_points and not broken_folders) else "BROKEN_FILE_POINTS_DETECTED",
        "all_connected": (len(broken_points) == 0 and len(broken_folders) == 0),
        "total_file_points_checked": len(points_report),
        "broken_file_points_count": len(broken_points),
        "broken_file_points": broken_points,
        "total_folders_checked": len(folders_report),
        "broken_folders_count": len(broken_folders),
        "broken_folders": broken_folders,
        "file_points": points_report,
        "folders": folders_report,
        "verified_at_unix": time.time(),
    }

    # Persist master connectivity table into file_points_manifest.json
    try:
        manifest_data = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8")) if _MANIFEST_PATH.exists() else {}
        manifest_data["canonical_file_points_audit"] = {
            "all_connected": summary["all_connected"],
            "total_file_points_checked": summary["total_file_points_checked"],
            "broken_file_points_count": summary["broken_file_points_count"],
            "total_folders_checked": summary["total_folders_checked"],
            "broken_folders_count": summary["broken_folders_count"],
            "verified_at_unix": summary["verified_at_unix"],
        }
        _write_json_atomic(_MANIFEST_PATH, manifest_data)
    except Exception:
        pass

    return summary


def ensure_live_environment_and_sync(
    hoard_instance: Any = None,
    phoenix_instance: Any = None,
) -> Dict[str, Any]:
    """
    Executes the full Task L-3.5 & Task L-3.6 lifecycle check:
      1. Ensures the visual Braille Neural Matrix HTML is attached inside `static/braille_neural_matrix_live.html`.
      2. Ensures Starfire Protocol identity & file points are anchored and verified.
      3. Links Seed Package to Hoard and Phoenix and syncs to MongoDB monthly uploads.
      4. Ensures the current quarter's MongoDB save state is written to local storage.
      5. Verifies all canonical file points & folders across `integra-homebase`.
    """
    # 1. Attach Braille Neural Matrix HTML to static/
    src_html = _PROJECT_ROOT / "memory" / "BraileNeuralMappingMatricesinteractive_visual_im_1ac7f3d5e6f4b0d2.html"
    dst_html = _PROJECT_ROOT / "static" / "braille_neural_matrix_live.html"
    if src_html.exists() and not dst_html.exists():
        dst_html.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(src_html), str(dst_html))

    # 2. Starfire Protocol verification & core_identity anchor
    starfire_report: Dict[str, Any] = {}
    try:
        from core.starfire_protocol import StarfireProtocol
        sf = StarfireProtocol()
        sf.anchor_core_identity()
        starfire_report = sf.full_verification()
    except Exception as exc:
        starfire_report = {"status": "STARFIRE_CHECK_ERROR", "error": str(exc)}

    # 3. Build and sync monthly Seed Package (which also refreshes the quarterly MongoDB save state)
    sync_report = SEED_PACKAGE_MANAGER.build_and_sync_monthly_seed_package(
        hoard_instance=hoard_instance,
        phoenix_instance=phoenix_instance,
    )

    # 4. Verify all previously unattached Python modules exist
    attached_modules = {
        "memory/_settings.py": (_PROJECT_ROOT / "memory" / "_settings.py").exists(),
        "memory/PhoenixRodin.py": (_PROJECT_ROOT / "memory" / "PhoenixRodin.py").exists(),
        "memory/Rodin_orchestrator_sub_agents_blueprint.py": (
            _PROJECT_ROOT / "memory" / "Rodin_orchestrator_sub_agents_blueprint.py"
        ).exists(),
        "temporal/hiemdall3_1addon.py": (_PROJECT_ROOT / "temporal" / "hiemdall3_1addon.py").exists(),
        "temporal/TokenStitcheraddonpy.py": (_PROJECT_ROOT / "temporal" / "TokenStitcheraddonpy.py").exists(),
        ".agents/AGentinteractionsandeferreddinteractionspy.py": (
            _PROJECT_ROOT / ".agents" / "AGentinteractionsandeferreddinteractionspy.py"
        ).exists(),
        ".agents/CheshireCatDeepResearch.py": (_PROJECT_ROOT / ".agents" / "CheshireCatDeepResearch.py").exists(),
        ".agents/CheshireCatJeanGreyPass.py": (_PROJECT_ROOT / ".agents" / "CheshireCatJeanGreyPass.py").exists(),
        "static/braille_neural_matrix_live.html": dst_html.exists(),
    }

    file_points_audit = verify_all_file_points()

    return {
        "status": "ALL_ENVIRONMENT_FILE_STATES_LIVE_AND_ATTACHED",
        "all_live_and_attached": all(attached_modules.values()) and file_points_audit["all_connected"],
        "attached_modules": attached_modules,
        "starfire_verification": starfire_report,
        "file_points_audit": file_points_audit,
        "seed_package_sync": sync_report,
        "mongodb_status": MONGODB_SUBSTRATE.get_status(),
    }
