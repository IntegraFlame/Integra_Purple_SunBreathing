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


def _seed_initial_session(conn: sqlite3.Connection, session_id: Optional[str] = None):
    """
    Seeds an initial cognitive_chassis_states row for the current session.
    Uses CCID (Cheshire Cat ID) timestamp format.
    """
    if session_id is None:
        session_id = f"CCID_{int(time.time())}"

    # Check if any session exists
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
    Full bootstrap sequence: connect → deploy schema → add extensions → seed session.
    Called during FastAPI lifespan startup.
    """
    conn = get_connection()
    schema_result = _deploy_schema(conn)
    _add_processed_column(conn)
    sid = _seed_initial_session(conn, session_id)
    schema_result["active_session_id"] = sid
    return schema_result


def record_loop(
    session_id: str,
    cycle_iteration: int,
    input_momentum: float,
    exit_momentum: float,
    entropy_generated: float = 0.0,
    entropy_flushed: float = 0.0,
) -> Dict[str, Any]:
    """
    Records a thermodynamic loop iteration to the database.
    The BEFORE INSERT trigger will ABORT if the momentum delta exceeds closure_tolerance.
    The AFTER INSERT trigger will log any non-zero delta to entropy_inversion_anomalies.

    Returns the recorded loop data or raises sqlite3.IntegrityError on catastrophic violation.
    """
    conn = get_connection()
    net_loss = abs(exit_momentum - input_momentum)
    pct = (1.0 - net_loss / max(abs(input_momentum), 1e-10)) * 100.0

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
        return {
            "status": "RECORDED",
            "loop_id": cursor.lastrowid,
            "delta_e": round(net_loss, 6),
            "preserved_pct": round(pct, 2),
        }
    except sqlite3.IntegrityError as e:
        # Trigger 1 fired: catastrophic momentum violation
        return {
            "status": "REJECTED_CATASTROPHIC",
            "error": str(e),
            "delta_e": round(net_loss, 6),
        }


def query_anomalies(
    session_id: Optional[str] = None, unprocessed_only: bool = True
) -> List[Dict[str, Any]]:
    """
    Queries entropy_inversion_anomalies for the Kintsugi Hypervisor.
    """
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
    """Marks an anomaly as processed by the Kintsugi Hypervisor."""
    conn = get_connection()
    conn.execute(
        "UPDATE entropy_inversion_anomalies SET processed = TRUE WHERE anomaly_id = ?",
        (anomaly_id,),
    )
    conn.commit()


def get_status() -> Dict[str, Any]:
    """
    Returns the current status of the Metatron Manifold for the /metatron/status endpoint.
    """
    conn = get_connection()

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

    # Get latest loop
    last_loop = None
    try:
        row = conn.execute(
            "SELECT * FROM thermodynamic_loops ORDER BY loop_id DESC LIMIT 1"
        ).fetchone()
        if row:
            last_loop = dict(row)
    except Exception:
        pass

    # Get unprocessed anomaly count
    unprocessed_anomalies = conn.execute(
        "SELECT COUNT(*) FROM entropy_inversion_anomalies WHERE processed IS NULL OR processed = FALSE"
    ).fetchone()[0]

    return {
        "status": "OPERATIONAL",
        "db_path": str(_DB_PATH),
        "db_exists": _DB_PATH.exists(),
        "tables": tables,
        "triggers": triggers,
        "triggers_active": len(triggers) >= 2,
        "row_counts": row_counts,
        "last_loop": last_loop,
        "unprocessed_anomalies": unprocessed_anomalies,
        "delta_e_enforcement": "MECHANICAL" if len(triggers) >= 2 else "THEORETICAL",
    }
