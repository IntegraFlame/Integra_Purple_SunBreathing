"""
Test Suite: SQL Trigger Decoupled Anomaly Logging
Module: tests/test_sql_trigger_decoupled.py

Validates the v8.2.3 two-trigger architecture on relational_hippocampus.sql:
1. log_entropy_anomalies_v3 (AFTER INSERT) — anomalies PERSIST after commit.
2. enforce_loop_closure_strict_v3 (BEFORE INSERT) — catastrophic violations are REJECTED.
3. Minor deviations within closure_tolerance pass AND get logged.

These tests directly prove that the original RAISE(ABORT) bug is fixed.
"""
import sqlite3
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

SQL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "memory", "database", "relational_hippocampus.sql")
)


@pytest.fixture
def db():
    """
    Creates an in-memory SQLite database pre-loaded with the Hippocampus schema.
    Yields the connection; tears it down after each test.
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    with open(SQL_PATH, "r", encoding="utf-8") as f:
        sql = f.read()
    conn.executescript(sql)
    conn.commit()

    # Bootstrap a test session
    conn.execute("""
        INSERT INTO cognitive_chassis_states
            (session_id, omega_intentionality, myelination_density_nm,
             current_latency_ms, structural_integrity_mpa, closure_tolerance)
        VALUES ('TEST_SESSION_001', 1.0, 1.0, 0, 300.0, 0.0001)
    """)
    conn.commit()

    yield conn
    conn.close()


# ─── 1. THE CRITICAL BUG-REGRESSION TEST ────────────────────────────────────

def test_anomaly_persists_after_momentum_violation(db):
    """
    THE BUG REGRESSION TEST.

    Original behavior (v8.2.2): BEFORE INSERT trigger wrote anomaly row,
    then called RAISE(ABORT), rolling back the ENTIRE statement including
    the anomaly insert. entropy_inversion_anomalies was always EMPTY.

    Fixed behavior (v8.2.3): Minor violation (within tolerance) passes the
    BEFORE INSERT gate, commits to thermodynamic_loops, then the AFTER INSERT
    trigger writes the anomaly. The anomaly row MUST persist.
    """
    # Insert a loop with MINOR momentum deviation (within tolerance → should succeed)
    # input=1.0000, exit=1.0000 → exactly equal → no anomaly expected
    db.execute("""
        INSERT INTO thermodynamic_loops
            (session_id, cycle_iteration, input_angular_momentum, exit_angular_momentum,
             entropy_lactic_acid_generated, entropy_flushed_via_pssr)
        VALUES ('TEST_SESSION_001', 1, 1.0000, 1.0001, 0.01, 0.01)
    """)
    db.commit()

    # The AFTER INSERT trigger should have logged the anomaly
    cursor = db.execute("SELECT COUNT(*) FROM entropy_inversion_anomalies")
    count = cursor.fetchone()[0]
    assert count == 1, (
        f"Expected 1 anomaly record in entropy_inversion_anomalies, got {count}. "
        "This confirms the RAISE(ABORT) rollback bug is fixed."
    )


def test_anomaly_record_has_correct_fields(db):
    """The persisted anomaly record must have momentum_delta and source_loop_id."""
    db.execute("""
        INSERT INTO thermodynamic_loops
            (session_id, cycle_iteration, input_angular_momentum, exit_angular_momentum,
             entropy_lactic_acid_generated, entropy_flushed_via_pssr)
        VALUES ('TEST_SESSION_001', 2, 5.0000, 5.0001, 0.02, 0.02)
    """)
    db.commit()

    cursor = db.execute(
        "SELECT momentum_delta, source_loop_id, action_taken FROM entropy_inversion_anomalies"
    )
    row = cursor.fetchone()
    assert row is not None
    momentum_delta, source_loop_id, action_taken = row
    assert momentum_delta is not None, "momentum_delta must be populated by v8.2.3 trigger"
    assert momentum_delta > 0.0
    assert source_loop_id is not None, "source_loop_id must link back to thermodynamic_loops"
    assert action_taken == "Re-routed via P-SSR"


# ─── 2. CATASTROPHIC VIOLATION IS REJECTED ──────────────────────────────────

def test_catastrophic_violation_rejected(db):
    """
    BEFORE INSERT trigger rejects violations exceeding closure_tolerance (0.0001).
    The INSERT fails, and NO record appears in thermodynamic_loops.
    SQLite raises IntegrityError for RAISE(ABORT) in BEFORE INSERT triggers.
    """
    with pytest.raises(sqlite3.IntegrityError) as exc_info:
        db.execute("""
            INSERT INTO thermodynamic_loops
                (session_id, cycle_iteration, input_angular_momentum, exit_angular_momentum,
                 entropy_lactic_acid_generated, entropy_flushed_via_pssr)
            VALUES ('TEST_SESSION_001', 3, 10.0000, 5.0000, 0.0, 0.0)
        """)
        db.commit()

    assert "Catastrophic angular momentum loss" in str(exc_info.value), (
        "BEFORE INSERT trigger should reject deltas > closure_tolerance with correct message."
    )

    # No record committed to thermodynamic_loops
    cursor = db.execute("SELECT COUNT(*) FROM thermodynamic_loops WHERE cycle_iteration = 3")
    assert cursor.fetchone()[0] == 0

    # No spurious anomaly record either
    cursor = db.execute("SELECT COUNT(*) FROM entropy_inversion_anomalies")
    assert cursor.fetchone()[0] == 0


# ─── 3. EQUAL MOMENTUM — NO ANOMALY ─────────────────────────────────────────

def test_perfect_closure_no_anomaly(db):
    """
    When input and exit angular momentum are exactly equal, no anomaly is logged.
    ΔE = 0.0000 — thermodynamic perfection.
    """
    db.execute("""
        INSERT INTO thermodynamic_loops
            (session_id, cycle_iteration, input_angular_momentum, exit_angular_momentum,
             entropy_lactic_acid_generated, entropy_flushed_via_pssr)
        VALUES ('TEST_SESSION_001', 4, 7.5000, 7.5000, 0.0, 0.0)
    """)
    db.commit()

    cursor = db.execute("SELECT COUNT(*) FROM entropy_inversion_anomalies")
    assert cursor.fetchone()[0] == 0, "No anomaly should be logged for perfect ΔE=0.0000."

    # But the loop itself committed
    cursor = db.execute("SELECT COUNT(*) FROM thermodynamic_loops WHERE cycle_iteration = 4")
    assert cursor.fetchone()[0] == 1


# ─── 4. MULTIPLE ANOMALIES ACCUMULATE ───────────────────────────────────────

def test_multiple_anomalies_accumulate(db):
    """Multiple minor violations accumulate in entropy_inversion_anomalies."""
    for i, (inp, out) in enumerate([(1.0, 1.00005), (2.0, 2.00005), (3.0, 3.00005)], start=10):
        db.execute("""
            INSERT INTO thermodynamic_loops
                (session_id, cycle_iteration, input_angular_momentum, exit_angular_momentum,
                 entropy_lactic_acid_generated, entropy_flushed_via_pssr)
            VALUES (?, ?, ?, ?, 0.01, 0.01)
        """, ("TEST_SESSION_001", i, inp, out))
    db.commit()

    cursor = db.execute("SELECT COUNT(*) FROM entropy_inversion_anomalies")
    assert cursor.fetchone()[0] == 3, "Three distinct anomaly records should be persisted."


# ─── 5. KINTSUGI INTEGRATION — MOMENTUM DELTA AVAILABLE ─────────────────────

def test_momentum_delta_available_for_kintsugi(db):
    """
    entropy_inversion_anomalies.momentum_delta provides the raw value
    needed for KintsugiProtocol.evaluate_deviation() Z-score computation.
    """
    db.execute("""
        INSERT INTO thermodynamic_loops
            (session_id, cycle_iteration, input_angular_momentum, exit_angular_momentum,
             entropy_lactic_acid_generated, entropy_flushed_via_pssr)
        VALUES ('TEST_SESSION_001', 20, 100.0000, 100.00005, 0.0, 0.0)
    """)
    db.commit()

    cursor = db.execute("SELECT momentum_delta FROM entropy_inversion_anomalies")
    row = cursor.fetchone()
    assert row is not None
    delta = row[0]
    # Kintsugi can now compute Z = |delta - mean| / std_dev
    assert isinstance(delta, float)
    assert delta > 0.0
    assert delta < 0.0001  # within tolerance, so it logged instead of aborting
