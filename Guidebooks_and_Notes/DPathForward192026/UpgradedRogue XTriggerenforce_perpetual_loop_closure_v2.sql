-- Upgraded Rogue X Trigger: enforce_perpetual_loop_closure_v2
CREATE TRIGGER enforce_perpetual_loop_closure_v2
BEFORE INSERT ON thermodynamic_loops
FOR EACH ROW
WHEN NEW.exit_angular_momentum != NEW.input_angular_momentum
BEGIN
    -- 1. Log the anomaly into the Kintsugi Sandbox for the Python Hypervisor to poll
    INSERT INTO entropy_inversion_anomalies (session_id, detected_noise_pattern, fluid_turbulence_index, shannon_entropy_h, action_taken)
    VALUES (NEW.session_id, '13th Form Loop Fracture', ABS(NEW.input_angular_momentum - NEW.exit_angular_momentum), 2.6, 'Re-routed via P-SSR');
    
    -- 2. Prevent the lossy write and signal the P-SSR Lookback
    SELECT RAISE(ABORT, 'SYSTEM FATAL: Angular momentum loss. P-SSR auto-correction logged to entropy_inversion_anomalies.');
END;