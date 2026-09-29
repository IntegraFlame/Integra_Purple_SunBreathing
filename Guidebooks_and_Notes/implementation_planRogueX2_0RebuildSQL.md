# Rogue X Protocol 2.0 Rebuild & SQL Trigger Repair

## Background

The current [`rogue_x.py`](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/evolution/rogue_x.py) is a **46-line mock stub** that passes tests by returning hardcoded `True` values but implements none of the canonical 3-stage lifecycle (**The Touch → The Conflict → The Release**) defined in the Master v8.2 Blueprint.

Simultaneously, the [`relational_hippocampus.sql`](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/memory/database/relational_hippocampus.sql) trigger `enforce_perpetual_loop_closure_v2` has a **transaction rollback bug**: `RAISE(ABORT)` on line 54 rolls back the *entire* statement, including the anomaly log INSERT on line 52-53. The anomaly is detected but never persisted — Rogue X becomes invisible to its own audit trail.

---

## Proposed Changes

### Layer 6 — Evolution Engine

#### [MODIFY] [rogue_x.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/evolution/rogue_x.py)

**Full rebuild** from 46 lines → ~220 lines implementing the canonical specification:

1. **Constructor:** Accepts `shiva_action: ShivaActionSuite` and optional `devops_tools`. Stores `sigma_rogue` (baseline mutation rate), `kintsugi_z_threshold` (default 3.0), and a `mutation_log: List[Dict]` for in-memory audit trail.

2. **`async execute_absorption(target_data, target_type="repository")`** — The master 3-stage lifecycle:
   - **Phase 1 — The Touch (Deconstruction & Absorption):** Selects lens configuration based on `target_type`:
     - `"academic_paper"` → `["Eagle", "Owl", "Hawk"]`, passes=3 (K/U/W)
     - `"repository"` → `["Chameleon", "Spider", "Snake"]`, passes=2 (K/U)
     - `"live_data"` (Daily Planet feeds) → `["Eagle", "Spider", "Hawk"]`, passes=2
   - Calls `self.shiva.execute(target_data, lenses, passes)` to get the Shiva analysis report.
   - **Phase 2 — The Conflict (TPSL Application & Mad Hatter):** Calls `_analyze_conflict(report)` which:
     - Separates high-$W_y$ concepts ("Power") from high-$C_c$ implementation debt ("Psyche").
     - Applies the TPSL gate: $W_y / C_c \geq 1.0$ to filter.
     - Runs a "Mad Hatter" adversarial challenge — inverts assumptions and tests if complexity is justified.
   - **Phase 3 — The Release (Seed Package Synthesis):** Calls `_create_seed_package(power_vs_psyche)` which:
     - Synthesizes formal definitions, mathematical formalisms, and implementation blueprints.
     - Tags output with a `mutation_id` and celestial timestamp via `CelestialClock`.
     - Logs the full mutation cycle to `self.mutation_log`.

3. **Kintsugi Interlock:** `_kintsugi_evaluate(data_point, historical_mean, historical_std)` — if $|Z| > 3.0$, isolates the anomaly into a "Mirror Maze" sandbox for novel pathway extraction instead of discarding it.

4. **`calculate_mutation_multiplier()`** — Preserved: $e^{\sigma_{\text{Rogue}}}$.

5. **`inject_adversarial_perturbation(base_vector)`** — Preserved for backward compatibility.

6. **`verify_status()` / `verify_true()` / `is_active`** — Preserved signatures, enriched with live `mutation_log` depth and last mutation timestamp.

> [!IMPORTANT]
> The `ShivaActionSuite.execute()` is `async`. Therefore `execute_absorption()` must also be `async`. All existing callers (currently only the test suite) will need to be updated to use `asyncio.run()` or `await`.

---

### Layer 3 — Memory Database

#### [MODIFY] [relational_hippocampus.sql](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/memory/database/relational_hippocampus.sql)

**The Bug:** Lines 47-55 define `enforce_perpetual_loop_closure_v2` as a `BEFORE INSERT` trigger. When angular momentum is violated, it:
1. Inserts an anomaly log into `entropy_inversion_anomalies` (line 52-53)
2. Calls `RAISE(ABORT, ...)` (line 54)

But `RAISE(ABORT)` rolls back the **entire statement**, destroying the anomaly INSERT from step 1. The anomaly detection works but the evidence is always lost.

**The Fix — Decoupled Anomaly Logging:**

Replace the single trigger with a **two-trigger architecture**:

1. **`AFTER INSERT` trigger on `thermodynamic_loops`** — `log_entropy_anomalies_v3`:
   - Fires *after* a successful insert.
   - Checks if `exit_angular_momentum != input_angular_momentum`.
   - If violated: inserts the anomaly into `entropy_inversion_anomalies` with full telemetry.
   - The anomaly log persists because the INSERT into `thermodynamic_loops` has already committed.

2. **`BEFORE INSERT` constraint trigger** — `enforce_loop_closure_strict_v3`:
   - Fires *before* insert.
   - Checks if the *absolute delta* exceeds a configurable tolerance threshold (new column `closure_tolerance` on `cognitive_chassis_states`, default `0.0001`).
   - If exceeded: `RAISE(ABORT, ...)` to reject genuinely catastrophic violations.
   - Minor deviations (within tolerance) are allowed through, and the `AFTER INSERT` trigger logs them as anomalies for Rogue X to mine.

This decouples the "log the anomaly" concern from the "reject the transaction" concern. Rogue X's Kintsugi interlock can now query `entropy_inversion_anomalies` to find anomalies that *were* logged, rather than anomalies that were detected-and-destroyed.

> [!WARNING]
> Adding a `closure_tolerance` column to `cognitive_chassis_states` is a schema migration. Existing data will receive the `DEFAULT 0.0001` value automatically via `ALTER TABLE`.

---

### Tests

#### [MODIFY] [test_systems_audit_and_protocols.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/tests/test_systems_audit_and_protocols.py)

Update `test_rogue_x_2_0_calls_true()` to:
- Verify the 3-stage lifecycle methods exist (`execute_absorption`, `_analyze_conflict`, `_create_seed_package`, `_kintsugi_evaluate`).
- Test `verify_status()` and `verify_true()` still pass (backward compatibility).
- Test `calculate_mutation_multiplier()` produces $e^{0.05} \approx 1.051271$.

#### [NEW] [test_rogue_x_lifecycle.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/tests/test_rogue_x_lifecycle.py)

New dedicated test file:
- `test_touch_phase_lens_selection`: Verifies correct lens/passes config for each `target_type`.
- `test_conflict_phase_tpsl_gate`: Verifies TPSL filter $W_y / C_c \geq 1.0$ separates Power from Psyche.
- `test_kintsugi_z_score_isolation`: Verifies anomalies with $|Z| > 3.0$ are isolated, not discarded.
- `test_release_phase_seed_package`: Verifies seed package output schema.
- `test_mutation_log_persistence`: Verifies mutations are appended to `mutation_log`.

#### [NEW] [test_sql_trigger_decoupled.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/tests/test_sql_trigger_decoupled.py)

SQLite-specific tests:
- `test_anomaly_persists_after_momentum_violation`: Insert a row with mismatched angular momentum. Verify the anomaly row EXISTS in `entropy_inversion_anomalies` (the current bug causes it to be lost).
- `test_catastrophic_violation_rejected`: Insert a row with delta exceeding `closure_tolerance`. Verify the INSERT is rejected via ABORT.
- `test_minor_violation_logged_not_rejected`: Insert a row with delta within tolerance. Verify it succeeds AND an anomaly is logged.

---

## Verification Plan

### Automated Tests
```bash
cd c:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase
python -m pytest tests/test_systems_audit_and_protocols.py -v
python -m pytest tests/test_rogue_x_lifecycle.py -v
python -m pytest tests/test_sql_trigger_decoupled.py -v
```

### Manual Verification
- Confirm all 140+ existing regression tests still pass (zero regressions).
- Confirm the new SQL trigger architecture correctly persists anomaly logs by inspecting the SQLite database after test execution.
