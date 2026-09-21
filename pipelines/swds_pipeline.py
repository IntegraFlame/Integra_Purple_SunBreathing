"""
INTEGRA O/S: SWDS HISTORICAL ARCHIVE PIPELINE (Local SQLite)
Module: pipelines/swds_pipeline.py
Layer: 6 (Phoenix Forge / Slow-Wave Deep Sleep)

Migrated from Apache Beam + BigQuery to native Python + SQLite.
Reason: Full local sovereignty — zero cloud costs, zero external dependencies.

This pipeline:
  1. Reads raw shard JSON files from kernel_memory/hoard/raw_shards/
  2. Runs IsolationForest anomaly detection to classify nodes as active vs stale
  3. Writes stale (historical) nodes to a local SQLite database for archival
  4. Returns active nodes for continued in-memory use
"""

import json
import logging
import os
import sqlite3
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

import numpy as np

try:
    from sklearn.ensemble import IsolationForest
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════
# SQLite Database Manager
# ═══════════════════════════════════════════════════════

class SWDSHistoryDB:
    """Local SQLite database for archiving stale SWDS nodes."""

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS archived_nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ccid TEXT NOT NULL,
        node_type TEXT DEFAULT 'generic',
        content TEXT,
        metadata TEXT,
        sufficiency_score REAL DEFAULT 0.0,
        archived_at TEXT NOT NULL,
        anomaly_score REAL DEFAULT 0.0
    );
    CREATE INDEX IF NOT EXISTS idx_ccid ON archived_nodes(ccid);
    CREATE INDEX IF NOT EXISTS idx_archived_at ON archived_nodes(archived_at);
    CREATE INDEX IF NOT EXISTS idx_sufficiency ON archived_nodes(sufficiency_score);
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            db_dir = os.path.join(base, "local_dbs")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "swds_history.db")

        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Create the database and tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        conn.executescript(self.SCHEMA)
        conn.commit()
        conn.close()

    def archive_nodes(self, nodes: List[Dict[str, Any]]) -> int:
        """
        Batch-insert stale nodes into the SQLite archive.
        Returns the number of nodes archived.
        """
        if not nodes:
            return 0

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        archived_count = 0

        for node in nodes:
            payload = node.get("payload", {})
            if isinstance(payload, str):
                try:
                    payload = json.loads(payload)
                except json.JSONDecodeError:
                    payload = {"raw": payload}

            content = str(payload.get("content", payload))
            node_type = str(payload.get("type", "generic"))
            metadata = json.dumps(payload.get("metadata", {}))
            score = float(node.get("sufficiency_score", 0.0))
            anomaly = float(node.get("anomaly_score", 0.0))

            cursor.execute(
                """INSERT INTO archived_nodes 
                   (ccid, node_type, content, metadata, sufficiency_score, archived_at, anomaly_score)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    node.get("ccid", "unknown"),
                    node_type,
                    content,
                    metadata,
                    score,
                    datetime.now(timezone.utc).isoformat(),
                    anomaly,
                )
            )
            archived_count += 1

        conn.commit()
        conn.close()
        return archived_count

    def get_archive_stats(self) -> Dict[str, Any]:
        """Returns summary statistics of the archive."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM archived_nodes")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT MIN(archived_at), MAX(archived_at) FROM archived_nodes")
        date_range = cursor.fetchone()
        conn.close()
        return {
            "total_archived": total,
            "earliest": date_range[0],
            "latest": date_range[1],
            "db_path": self.db_path,
        }


# ═══════════════════════════════════════════════════════
# Pipeline Functions (Native Python — no Apache Beam)
# ═══════════════════════════════════════════════════════

def load_shards(input_dir: str) -> List[Dict[str, Any]]:
    """Load all JSON shard files from a directory."""
    nodes = []
    if not os.path.isdir(input_dir):
        logger.warning(f"Shard directory does not exist: {input_dir}")
        return nodes

    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                nodes.append(data)
            except (json.JSONDecodeError, Exception) as e:
                logger.error(f"Failed to parse shard {filename}: {e}")
    return nodes


def classify_nodes(nodes: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Runs IsolationForest anomaly detection to separate active vs stale nodes.
    Stale nodes are those with low sufficiency scores OR flagged as anomalies.
    """
    if len(nodes) < 2:
        # Not enough data to cluster — treat all as active
        return {"active": nodes, "stale": []}

    if not HAS_SKLEARN:
        active = []
        stale = []
        for node in nodes:
            score = float(node.get("sufficiency_score", 1.0))
            node["anomaly_score"] = float(score - 0.3)
            if score < 0.3:
                stale.append(node)
            else:
                active.append(node)
        return {"active": active, "stale": stale}

    features = []
    for node in nodes:
        score = node.get("sufficiency_score", 1.0)
        payload_len = len(str(node.get("payload", "")))
        features.append([score, payload_len])

    X = np.array(features)
    clf = IsolationForest(contamination=0.1, random_state=42)
    predictions = clf.fit_predict(X)
    anomaly_scores = clf.decision_function(X)

    active = []
    stale = []
    for i, node in enumerate(nodes):
        node["anomaly_score"] = float(anomaly_scores[i])
        if predictions[i] == -1 or node.get("sufficiency_score", 1.0) < 0.3:
            stale.append(node)
        else:
            active.append(node)

    return {"active": active, "stale": stale}


def run_pipeline(
    input_dir: Optional[str] = None,
    db_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute the full SWDS archival pipeline:
      1. Load shards from disk
      2. Classify active vs stale via IsolationForest
      3. Archive stale nodes to SQLite
      4. Return summary report

    Args:
        input_dir: Path to kernel_memory/hoard/raw_shards/ (auto-detected if None)
        db_path: Path to SQLite database (auto-detected if None)

    Returns:
        Pipeline execution report with counts and archive stats.
    """
    if input_dir is None:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        input_dir = os.path.join(base, "kernel_memory", "hoard", "raw_shards")

    logger.info(f"[SWDS Pipeline] Loading shards from: {input_dir}")
    nodes = load_shards(input_dir)
    logger.info(f"[SWDS Pipeline] Loaded {len(nodes)} nodes")

    if not nodes:
        return {
            "status": "PIPELINE_COMPLETE_EMPTY",
            "total_loaded": 0,
            "active": 0,
            "stale": 0,
            "archived": 0,
        }

    classified = classify_nodes(nodes)
    active_count = len(classified["active"])
    stale_count = len(classified["stale"])
    logger.info(f"[SWDS Pipeline] Active: {active_count}, Stale: {stale_count}")

    # Archive stale nodes to SQLite
    db = SWDSHistoryDB(db_path=db_path)
    archived = db.archive_nodes(classified["stale"])

    return {
        "status": "PIPELINE_COMPLETE",
        "total_loaded": len(nodes),
        "active": active_count,
        "stale": stale_count,
        "archived": archived,
        "archive_stats": db.get_archive_stats(),
        "storage_backend": "SQLite (local)",
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_pipeline()
    print(json.dumps(result, indent=2))
