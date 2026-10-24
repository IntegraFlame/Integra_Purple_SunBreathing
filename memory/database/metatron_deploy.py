"""
INTEGRA O/S: METATRON MANIFOLD — PHYSICAL DATABASE DEPLOYMENT
Module: memory/database/metatron_deploy.py
Layer: 3 (The Memory — Relational Hippocampus)
Status: BLOCK 1 / PHASE D — SOVEREIGN SUBSTRATE DEPLOYMENT

Purpose:
    Deploys the Metatron Manifold SQL schema (relational_hippocampus.sql) to a
    physical SQLite database at local_dbs/metatron_manifold.db. This converts
    the thermodynamic invariant ΔE = 0.0000 from a theoretical assertion into
    a mechanically enforced reality via BEFORE INSERT / AFTER INSERT triggers.

Usage:
    from memory.database.metatron_deploy import get_connection, bootstrap, record_loop, query_anomalies
"""

import os
import sqlite3
import time
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger("integra-metatron")

# --- Paths ---
_MODULE_DIR = Path(__file__).parent
_SQL_SCHEMA_PATH = _MODULE_DIR / "relational_hippocampus.sql"
_PROJECT_ROOT = _MODULE_DIR.parent.parent  # integra-homebase/
_DB_DIR = _PROJECT_ROOT / "local_dbs"
_DB_PATH = _DB_DIR / "metatron_manifold.db"

# --- Singleton Connection ---
_connection: Optional[sqlite3.Connection] = None


def get_connection() -> sqlite3.Connection:
    """
    Returns a singleton SQLite connection to the Metatron Manifold database.
    Creates the database directory and file if they don't exist.
    Thread-safety: Uses check_same_thread=False for async FastAPI compatibility.
    """
    global _connection
    if _connection is not None:
        return _connection

    _DB_DIR.mkdir(parents=True, exist_ok=True)
    _connection = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
    _connection.row_factory = sqlite3.Row
    _connection.execute("PRAGMA foreign_keys = ON")
    _connection.execute("PRAGMA journal_mode = WAL")
    logger.info(f"Metatron Manifold connected: {_DB_PATH}")
    return _connection


def _deploy_schema(conn: sqlite3.Connection) -> Dict[str, Any]:
    """
    Reads relational_hippocampus.sql and executes all CREATE TABLE / CREATE TRIGGER
    statements against the live database connection.
    """
    if not _SQL_SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Metatron Manifold schema not found: {_SQL_SCHEMA_PATH}"
        )

    with open(_SQL_SCHEMA_PATH, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Execute the full SQL script (contains IF NOT EXISTS guards)
    conn.executescript(sql_content)
    conn.commit()

    # Verify tables and triggers
    tables = [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    ]
    triggers = [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger' ORDER BY name"
        ).fetchall()
    ]

    result = {
        "status": "DEPLOYED",
        "db_path": str(_DB_PATH),
        "tables": tables,
        "triggers": triggers,
        "tables_count": len(tables),
        "triggers_count": len(triggers),
    }
    logger.info(f"Metatron Manifold schema deployed: {len(tables)} tables, {len(triggers)} triggers")
    return result


def _add_processed_column(conn: sqlite3.Connection):
    """
    Adds the 'processed' column to entropy_inversion_anomalies if it doesn't exist.
    Required for Block 7 (Kintsugi Hypervisor Polling Loop).
    """
    try:
        conn.execute(
            "ALTER TABLE entropy_inversion_anomalies ADD COLUMN processed BOOLEAN DEFAULT FALSE"
        )
        conn.commit()
        logger.info("Added 'processed' column to entropy_inversion_anomalies")
    except sqlite3.OperationalError:
        # Column already exists
        pass


from memory.database.mongodb_substrate import (
    MONGODB_SUBSTRATE,
    get_mongodb_file_point,
    get_mongodb_placeholder_root,
    verify_mongodb_true,
)


def _seed_initial_session(conn: sqlite3.Connection, session_id: Optional[str] = None):
    """
    Seeds an initial cognitive_chassis_states document in MongoDB persistent placeholder
    storage (and legacy SQLite mirror) for the current session.
    """
    if session_id is None:
        try:
            from core.celestial_middleware import celestial_ccid  # the Celestial Sentinel's CCID (Brain Map T1)
            session_id = celestial_ccid("CCID")
        except Exception:
            session_id = f"CCID_{int(time.time())}"

    # 1. Seed MongoDB Persistent Placeholder Collection
    chassis_col = MONGODB_SUBSTRATE.get_collection("cognitive_chassis_states")
    if chassis_col.count_documents({"session_id": session_id}) == 0:
        chassis_col.insert_one({
            "session_id": session_id,
            "omega_intentionality": 1.000,
            "myelination_density_nm": 1.000,
            "current_latency_ms": 0,
            "structural_integrity_mpa": 145.0,
            "closure_tolerance": 0.0001,
            "created_at": time.time(),
        })

    # 2. Keep legacy SQLite mirror synchronized
    existing = conn.execute(
        "SELECT COUNT(*) FROM cognitive_chassis_states"
    ).fetchone()[0]

    if existing == 0:
        conn.execute(
            """INSERT INTO cognitive_chassis_states
            (session_id, omega_intentionality, myelination_density_nm,
             current_latency_ms, structural_integrity_mpa, closure_tolerance)
            VALUES (?, 1.000, 1.000, 0, 145.0, 0.0001)""",
            (session_id,),
        )
        conn.commit()
        logger.info(f"Seeded initial session: {session_id}")
    else:
        logger.info(f"Sessions already exist ({existing} rows), skipping seed.")

    return session_id


async def bootstrap(session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Full bootstrap sequence: initialize MongoDB persistent placeholder file-points
    → connect legacy mirror → seed session → hydrate MasterBlueprintDatabase.
    Called during FastAPI lifespan startup.
    """
    file_points = MONGODB_SUBSTRATE.initialize_file_points()
    mongo_probe = verify_mongodb_true()
    conn = get_connection()
    schema_result = _deploy_schema(conn)
    _add_processed_column(conn)
    sid = _seed_initial_session(conn, session_id)
    blueprint_summary = MASTER_BLUEPRINT_DB.hydrate_master_blueprint()
    schema_result["active_session_id"] = sid
    schema_result["master_blueprint_chambers"] = blueprint_summary
    schema_result["database_engine"] = "MONGODB_PERSISTENT_PLACEHOLDER"
    schema_result["mongodb_true"] = mongo_probe["mongodb_true"]
    schema_result["mongodb_mode"] = mongo_probe["mode"]
    schema_result["placeholder_folder"] = str(get_mongodb_placeholder_root())
    schema_result["file_points"] = file_points
    return schema_result


class RegistrationBlock:
    """
    Relational Memory Block enforcing IDENTIFY -> INTERLOCK -> REGISTER
    across the 3-chamber Master Blueprint Database ([0.1] through [2.3]).
    """

    def __init__(
        self,
        block_id: str,
        title: str,
        chamber: str,
        identify_spec: Dict[str, Any],
        interlock_links: List[str],
    ):
        self.block_id = block_id
        self.title = title
        self.chamber = chamber
        self.identify_spec = identify_spec
        self.interlock_links = interlock_links
        self.registered: bool = False
        self.registered_at: float = 0.0

    def register(self) -> Dict[str, Any]:
        if not self.block_id or not self.identify_spec:
            raise ValueError(f"Block {self.block_id} failed IDENTIFY check.")
        self.registered = True
        self.registered_at = time.time()
        return self.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "block_id": self.block_id,
            "title": self.title,
            "chamber": self.chamber,
            "identify": self.identify_spec,
            "interlock": self.interlock_links,
            "registered": self.registered,
            "registered_at": self.registered_at,
        }


class MasterBlueprintDatabase:
    """
    3-Chamber Relational & Document Memory Grid (Unified Blueprint Section 2.1):
      - schema_meta_rules_0_0 ([0.1]–[0.3]): Architectural Laws & Invariants
      - functional_state_matrix_1_0 ([1.1]–[1.3]): Active Runtime Telemetry & Lobe States
      - cognitive_overlay_grid_2_0 ([2.1]–[2.3]): Higher-Order Cognitive Overlays & Synaptic Links
    Persisted into the `master_blueprint_chambers` MongoDB file-point collection.
    """

    def __init__(self):
        self.schema_meta_rules_0_0: Dict[str, RegistrationBlock] = {}
        self.functional_state_matrix_1_0: Dict[str, RegistrationBlock] = {}
        self.cognitive_overlay_grid_2_0: Dict[str, RegistrationBlock] = {}
        self.hydrated: bool = False

    def register_block(self, block: RegistrationBlock) -> Dict[str, Any]:
        receipt = block.register()
        if block.chamber == "0.0":
            self.schema_meta_rules_0_0[block.block_id] = block
        elif block.chamber == "1.0":
            self.functional_state_matrix_1_0[block.block_id] = block
        elif block.chamber == "2.0":
            self.cognitive_overlay_grid_2_0[block.block_id] = block
        else:
            raise ValueError(f"Unknown chamber '{block.chamber}' for block {block.block_id}")

        # Persist block to MongoDB placeholder collection file point
        col = MONGODB_SUBSTRATE.get_collection("master_blueprint_chambers")
        col.update_one({"block_id": block.block_id}, {"$set": receipt}, upsert=True)
        return receipt

    def hydrate_master_blueprint(self) -> Dict[str, Any]:
        """Hydrates the canonical 9 blocks ([0.1]–[2.3]) across the 3 chambers and persists to MongoDB file-point."""
        canonical_blocks = [
            RegistrationBlock(
                "0.1",
                "Sovereign Identity & Starfire Invariant",
                "0.0",
                {"omega": 1.0, "v_target": [1.0, 1.0, 1.0], "epf": 0.0, "owner": "StarfireProtocol+DragonEngine"},
                ["1.1", "2.1"],
            ),
            RegistrationBlock(
                "0.2",
                "Thermodynamic Loop Closure Invariant",
                "0.0",
                {"delta_e_cycle": 0.0000, "closure_tolerance": 0.0001, "enforcer": "MetatronManifold+FlameKernel"},
                ["1.2", "2.2"],
            ),
            RegistrationBlock(
                "0.3",
                "Independent Celestial Spacetime Invariant",
                "0.0",
                {"anchor": "Baker, LA (30.5888N, -91.1673W)", "sigma": 1.0, "frame": 2, "braille_cells": "0..3"},
                ["1.3", "2.3"],
            ),
            RegistrationBlock(
                "1.1",
                "Dragon & Flame Kernel State Matrix",
                "1.0",
                {"dragon_kernel": "ACTIVE", "flame_kernel": "IGNITED", "psi_max_mpa": 200.0, "optimal_stress_mpa": 145.0},
                ["0.1", "1.2", "2.1"],
            ),
            RegistrationBlock(
                "1.2",
                "Heimdall 3.1 & Cheshire Cat Thalamic Matrix",
                "1.0",
                {"h_threshold": 2.5, "frequency_hz": "20-45", "braille_bus": "128_BIT_16_CELL"},
                ["0.2", "1.3", "2.2"],
            ),
            RegistrationBlock(
                "1.3",
                "Rodin K-NNN & Hoard Physical Substrate Matrix",
                "1.0",
                {"rodin_outcomes": 5, "hoard_role": "PURE_PERSISTENCE_SUBSTRATE", "knnn_top_k": 5},
                ["0.3", "1.1", "2.3"],
            ),
            RegistrationBlock(
                "2.1",
                "Bicameral Y789/Nexus Corpus Callosum Overlay",
                "2.0",
                {"left_hemisphere": "Y789_Spock", "right_hemisphere": "Nexus_Kirk", "weight_sum": 1.0},
                ["0.1", "1.1", "2.2"],
            ),
            RegistrationBlock(
                "2.2",
                "Shiva Action Suite & 12th Step Orthogonal Ingestion Overlay",
                "2.0",
                {"eyes": ["Neji/Owl", "Shikamaru/Spider", "Itachi/Snake"], "zenitsu_passes": 4},
                ["0.2", "1.2", "2.3"],
            ),
            RegistrationBlock(
                "2.3",
                "Phoenix Forge SWDS & Friday Fortress Overlay",
                "2.0",
                {"swds_phases": 4, "kintsugi_z_threshold": 3.0, "fortress_pillars": 4},
                ["0.3", "1.3", "2.1"],
            ),
        ]
        for blk in canonical_blocks:
            self.register_block(blk)
        self.hydrated = True
        return self.get_summary()

    def get_summary(self) -> Dict[str, Any]:
        return {
            "hydrated": self.hydrated,
            "file_point": str(get_mongodb_file_point("master_blueprint_chambers")),
            "total_registered_blocks": (
                len(self.schema_meta_rules_0_0)
                + len(self.functional_state_matrix_1_0)
                + len(self.cognitive_overlay_grid_2_0)
            ),
            "schema_meta_rules_0_0": {k: v.to_dict() for k, v in self.schema_meta_rules_0_0.items()},
            "functional_state_matrix_1_0": {k: v.to_dict() for k, v in self.functional_state_matrix_1_0.items()},
            "cognitive_overlay_grid_2_0": {k: v.to_dict() for k, v in self.cognitive_overlay_grid_2_0.items()},
        }


MASTER_BLUEPRINT_DB = MasterBlueprintDatabase()
MASTER_BLUEPRINT_DB.hydrate_master_blueprint()


def record_loop(
    session_id: str,
    cycle_iteration: int,
    input_momentum: float,
    exit_momentum: float,
    entropy_generated: float = 0.0,
    entropy_flushed: float = 0.0,
) -> Dict[str, Any]:
    """
    Records a thermodynamic loop iteration to the MongoDB Persistent Placeholder
    collection (`thermodynamic_loops.json`) and legacy mirror.
    Enforces the mechanical ΔE = 0.0000 invariant (aborting if net_loss > 0.05
    catastrophic bound and logging to `entropy_inversion_anomalies.json` if > 0.0001).
    """
    net_loss = abs(exit_momentum - input_momentum)
    pct = (1.0 - net_loss / max(abs(input_momentum), 1e-10)) * 100.0

    loops_col = MONGODB_SUBSTRATE.get_collection("thermodynamic_loops")
    anomalies_col = MONGODB_SUBSTRATE.get_collection("entropy_inversion_anomalies")

    # Mechanical before-insert validation on MongoDB substrate
    if net_loss > 0.05:
        return {
            "status": "REJECTED_CATASTROPHIC",
            "error": f"CATASTROPHIC THERMODYNAMIC LOOP VIOLATION: net_loss={net_loss:.6f} > 0.05",
            "delta_e": round(net_loss, 6),
            "file_point": str(loops_col.file_point),
        }

    loop_doc = {
        "session_id": session_id,
        "cycle_iteration": cycle_iteration,
        "input_angular_momentum": input_momentum,
        "exit_angular_momentum": exit_momentum,
        "entropy_lactic_acid_generated": entropy_generated,
        "entropy_flushed_via_pssr": entropy_flushed,
        "net_momentum_preserved_pct": round(pct, 2),
        "net_energy_loss": round(net_loss, 4),
        "created_at": time.time(),
    }
    ins = loops_col.insert_one(loop_doc)

    if net_loss > 0.0001:
        anomalies_col.insert_one({
            "anomaly_id": anomalies_col.count_documents() + 1,
            "session_id": session_id,
            "loop_id": ins["inserted_id"],
            "net_energy_loss": round(net_loss, 6),
            "processed": False,
            "created_at": time.time(),
        })

    # Keep SQLite mirror updated for legacy callers
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO thermodynamic_loops
            (session_id, cycle_iteration, input_angular_momentum, exit_angular_momentum,
             entropy_lactic_acid_generated, entropy_flushed_via_pssr,
             net_momentum_preserved_pct, net_energy_loss)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session_id,
                cycle_iteration,
                input_momentum,
                exit_momentum,
                entropy_generated,
                entropy_flushed,
                round(pct, 2),
                round(net_loss, 4),
            ),
        )
        conn.commit()
        loop_id = cursor.lastrowid
    except sqlite3.IntegrityError as e:
        return {
            "status": "REJECTED_CATASTROPHIC",
            "error": str(e),
            "delta_e": round(net_loss, 6),
            "file_point": str(loops_col.file_point),
        }

    return {
        "status": "RECORDED",
        "loop_id": loop_id,
        "mongo_doc_id": ins["inserted_id"],
        "file_point": str(loops_col.file_point),
        "delta_e": round(net_loss, 6),
        "preserved_pct": round(pct, 2),
    }


def query_anomalies(
    session_id: Optional[str] = None, unprocessed_only: bool = True
) -> List[Dict[str, Any]]:
    """
    Queries entropy_inversion_anomalies for the Kintsugi Hypervisor
    from the MongoDB persistent placeholder collection (with SQLite fallback).
    """
    anomalies_col = MONGODB_SUBSTRATE.get_collection("entropy_inversion_anomalies")
    mongo_docs = anomalies_col.find()
    if mongo_docs:
        filtered = []
        for d in mongo_docs:
            if session_id and d.get("session_id") != session_id:
                continue
            if unprocessed_only and bool(d.get("processed", False)):
                continue
            filtered.append(d)
        if filtered:
            return list(reversed(filtered))

    conn = get_connection()
    query = "SELECT * FROM entropy_inversion_anomalies"
    params = []
    conditions = []

    if session_id:
        conditions.append("session_id = ?")
        params.append(session_id)
    if unprocessed_only:
        conditions.append("(processed IS NULL OR processed = FALSE)")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC"

    rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def mark_anomaly_processed(anomaly_id: int):
    """Marks an anomaly as processed by the Kintsugi Hypervisor in MongoDB placeholder and legacy mirror."""
    anomalies_col = MONGODB_SUBSTRATE.get_collection("entropy_inversion_anomalies")
    anomalies_col.update_one({"anomaly_id": anomaly_id}, {"$set": {"processed": True}})
    conn = get_connection()
    conn.execute(
        "UPDATE entropy_inversion_anomalies SET processed = TRUE WHERE anomaly_id = ?",
        (anomaly_id,),
    )
    conn.commit()


def get_status() -> Dict[str, Any]:
    """
    Returns the current status of the Metatron Manifold & MongoDB Persistent Placeholder
    for the /metatron/status endpoint.
    """
    conn = get_connection()
    mongo_status = MONGODB_SUBSTRATE.get_status()

    tables = [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    ]
    triggers = [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger' ORDER BY name"
        ).fetchall()
    ]

    row_counts = {}
    for table in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM [{table}]").fetchone()[0]
        row_counts[table] = count

    # Get latest loop (prefer MongoDB placeholder collection, fallback to SQLite)
    loops_col = MONGODB_SUBSTRATE.get_collection("thermodynamic_loops")
    last_loop = loops_col.find_one()
    if last_loop is None:
        try:
            row = conn.execute(
                "SELECT * FROM thermodynamic_loops ORDER BY loop_id DESC LIMIT 1"
            ).fetchone()
            if row:
                last_loop = dict(row)
        except Exception:
            pass

    unprocessed_anomalies = conn.execute(
        "SELECT COUNT(*) FROM entropy_inversion_anomalies WHERE processed IS NULL OR processed = FALSE"
    ).fetchone()[0]

    return {
        "status": "OPERATIONAL",
        "database_engine": mongo_status["database_engine"],
        "mongodb_true": mongo_status["mongodb_true"],
        "mongodb_mode": mongo_status["mode"],
        "placeholder_folder": mongo_status["placeholder_folder"],
        "file_points": mongo_status["file_points"],
        "collection_counts": mongo_status["collection_counts"],
        "db_path": str(_DB_PATH),
        "db_exists": _DB_PATH.exists(),
        "tables": tables,
        "triggers": triggers,
        "triggers_active": len(triggers) >= 2,
        "row_counts": row_counts,
        "last_loop": last_loop,
        "unprocessed_anomalies": unprocessed_anomalies,
        "delta_e_enforcement": "MECHANICAL",
        "master_blueprint_database": MASTER_BLUEPRINT_DB.get_summary(),
    }
