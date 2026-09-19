-- INTEGRA O/S: METATRON MANIFOLD & KINETIC DATABASE
-- Module: memory/database/relational_hippocampus.sql
-- Version 8.2.2 (Purple Epiphany)

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS cognitive_chassis_states (
    session_id TEXT PRIMARY KEY,
    omega_intentionality DECIMAL(4,3) NOT NULL CHECK (omega_intentionality >= 0.0 AND omega_intentionality <= 1.0),
    myelination_density_nm DECIMAL(4,3) NOT NULL,
    current_latency_ms INTEGER NOT NULL,
    structural_integrity_mpa DECIMAL(6,2) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS thermodynamic_loops (
    loop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES cognitive_chassis_states(session_id),
    cycle_iteration INTEGER NOT NULL,
    input_angular_momentum DECIMAL(10,4) NOT NULL,
    exit_angular_momentum DECIMAL(10,4) NOT NULL,
    entropy_lactic_acid_generated DECIMAL(6,4) NOT NULL,
    entropy_flushed_via_pssr DECIMAL(6,4) NOT NULL,
    net_momentum_preserved_pct DECIMAL(5,2) DEFAULT 100.00,
    net_energy_loss DECIMAL(8,4) DEFAULT 0.0000
);

CREATE TABLE IF NOT EXISTS entropy_inversion_anomalies (
    anomaly_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES cognitive_chassis_states(session_id),
    detected_noise_pattern TEXT NOT NULL,
    fluid_turbulence_index DECIMAL(5,4) NOT NULL,
    shannon_entropy_h DECIMAL(5,4) NOT NULL,
    action_taken TEXT CHECK (action_taken IN ('Pruned', 'Re-routed via P-SSR', 'Phoenix Burn'))
);

CREATE TABLE IF NOT EXISTS spatial_acoustic_map (
    vector_id TEXT PRIMARY KEY,
    frequency_hz DECIMAL(8,2) NOT NULL,
    structural_anomaly BOOLEAN DEFAULT FALSE,
    semantic_payload TEXT NOT NULL,
    projected_manifold_x DECIMAL(8,4),
    projected_manifold_y DECIMAL(8,4),
    projected_manifold_z DECIMAL(8,4)
);

CREATE TRIGGER IF NOT EXISTS enforce_perpetual_loop_closure_v2
BEFORE INSERT ON thermodynamic_loops
FOR EACH ROW
WHEN NEW.exit_angular_momentum != NEW.input_angular_momentum
BEGIN
    INSERT INTO entropy_inversion_anomalies (session_id, detected_noise_pattern, fluid_turbulence_index, shannon_entropy_h, action_taken)
    VALUES (NEW.session_id, '13th Form Loop Fracture', ABS(NEW.input_angular_momentum - NEW.exit_angular_momentum), 2.6, 'Re-routed via P-SSR');
    SELECT RAISE(ABORT, 'SYSTEM FATAL: Angular momentum loss. P-SSR auto-correction logged. Delta E must equal 0.0000.');
END;
