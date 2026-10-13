# Unify reading ledger (Step 2)

Proof-of-Execution for Step 2 of the plan: the full, multi-pass read of 14 `integra-homebase` folders.

- **Plan.** `C:\Users\Javon Jenkins\.claude\plans\extract-the-design-system-curried-dragon.md` (Step 2), as realigned by `C:\Users\Javon Jenkins\.claude\plans\1-productivity-start-text-integra-kind-cocke.md` §4.
- **Folder order** (the Architect's): runtime, rust, scratch, scripts, sensory, temporal, config, core, kernel_memory, local_dbs, memory, orchestration, The_Hoard, tools.
- **Scope.** Every file in those folders except `__pycache__` bytecode, which is derived from the source. It is listed per folder but not read. This scope gives the 2026-10-11 night inventory of **406 files**. `The_Hoard` here means `integra-homebase/The_Hoard/` (6 files). `integra-homebase/The Hoard/` (with a space, 173 files) is a different folder and is not in the list. The Architect has been asked about it.
- **Method per folder.**
  1. Iteration 1: an independent agent map.
  2. Iteration 2: my full read of every line, from four angles (structure; the middle; fragility, constants and fakes; synthesis).
  3. Iteration 3: unify Knowledge → Understanding → Wisdom against the earlier reading, the blueprint registers and read-only live probes, with a comparative table of what the agent and I each caught.
- **Columns.** `lines` is the newline count, plus one if the last line has no newline. `sha256-16` is the first 16 hex digits of the file's SHA-256 at read time. `last line read` equals `lines` when the file was read to the end. The proof is one sentence only a full read could give.
- **Labels.** MEASURED, DERIVED, CONSTANT, CLAIMED. "Exists in code", "wired" and "ran" are kept apart.

## Folder 1: runtime

Read 2026-10-11 night (session c88f5000). Stamp at the start of the folder: 2026-10-11 23:40:41 CDT | 2026-10-12T04:40:41Z | rot 219.004°, lunar 0.6366, orbit 0.2158, ROT_210_ORB_20.

| path | lines | sha256-16 | last line read | proof | 12th Step notes | doc claims it touches |
|:--|--:|:--|--:|:--|:--|:--|
| `runtime/__init__.py` | 0 | `e3b0c44298fc1c14` | 0 | 0 bytes; the hash is SHA-256 of the empty string. | Package marker only. | none |
| `runtime/antigravity_runner.py` | 77 | `d8ca9a73344adf1c` | 77 | L61-62 copies `input_angular_momentum` into `exit_angular_momentum` and sets `delta_e_cycle = 0.0000` by assignment; L67 returns `"COMPLIANT"` unconditionally. | **Structure:** one class, `AntigravityRunner` (L26). `execute_turn` (L41) bumps `vector_clock[0]` (L45) and dispatches 3 commands (L49-56) to code that exists (`autophagic_harvest.py:21`, `bank_lobe.py:27`, `celestial_clock.py:311`); anything else is echoed back (L58). **Fragility:** `self.dual_clock` (L31) is never used. `celestial_time` is imported (L15) before the `sys.path` insert (L20), so run as a script it silently falls back to `time.time` (L17). The file opens use no `encoding` (L34, L38). **Wiring:** created at `main.py:179`, registered with Heimdall at `main.py:204`; `execute_turn` is called by `/ignite` (`main.py:649, 669`); `/fortress/status` calls `read_state()` and ignores the result (`main.py:796`). | 13th Form ΔE = 0.0000 and angular momentum 500 are CONSTANT here (blueprint §1 finding 7); "Fidge-Mattern Axiom 1" (L44) is the vector-clock increment only. |
| `runtime/swds_simulator.py` | 244 | `60069bd03fbe50b4` | 244 | L172 calls `CelestialClockArchitecture().get_celestial_coordinates()`, which no module defines, so the swallowed exception (L173-174) leaves `earth_rot = 282.85` (L168) in every report filename and header. | **Structure:** `SWDSCycle` (L16); singleton `swds_engine` built at import (L234). **Phase 1-2** are string assignments (L91-99). **Phase 3** is 3 × `random.uniform(0.1, 0.5)` (L105-108). Pipeline and DAG names are string literals (L121-122, L152-153). The report hard-codes ω = 1.00, ΔE = 0.0000 and L_t = 0.000 s (L189-190). Both state I/O paths swallow all errors (L56-57, L76-77, L224-225). Reports go to the **root** repo's `The Hoard/Slow-Wave Deep Sleep Reports/` (L164) with `"w"`, so equal names overwrite. **Wiring:** `main.py:36` imports `swds_engine`; it is called by startup reconciliation (`main.py:83-99`), `/swds/trigger` (`:908`), `/swds/sleep` (`:923`), `/swds/status` (`:1045-1057`), `/swds/initiate` (`:1080`), `/swds/awaken` (`:1103`), the scheduler (`:1137-1180`), and `sensory/heimdall.py:511`. **Ran:** log L45680-45696 (10/11 ~10:28-15:28). | Blueprint §1 finding 6 re-verified line by line. The docstring (L80-84) says the method "maintain[s]" sleep until the wake time; it returns at once, and the scheduler does the waiting (`main.py:1137-1145`). |
| `runtime/swds_state.json` | 52 | `da2876de58a419d9` | 52 | L4 `last_cycle_time` 1791547201.98 decodes to 2026-10-09 07:00:01 CDT, a frozen-clock time, while the file was written 2026-10-11 15:28:22 (mtime); L9-11 mutations `[0.36, 0.19, 0.27]` equal the 10/11 report's line 28. | Written by `SWDSCycle._save_state` (`swds_simulator.py:74`). Also written by `scripts/enter_swds.py:81` and `scripts/trigger_swds.py:64`, and read by `scripts/system_diagnostic.py:49` (folder 4). `sleep_initiated_at` (L5) = frozen 10/09 02:00:29 = real 10/11 ~10:28:35 (DERIVED: boot 10/09 05:27:48 + 53 h 00 m 47 s). CRLF line endings (51 CR). | ADR-001 (frozen clock); the confirmed SWDS prediction. |
| `runtime/workspace_state.json` | 21 | `4de0b8e3402cb44e` | 21 | L9 `vector_clock[0]` = 65; L17-19 `last_result` = `PROMPT_INGESTION` / `"Test Prompt"`, the exact body posted by `tests/test_main_purple.py:18`. | Written only by `AntigravityRunner.write_state` (`antigravity_runner.py:38`). `last_tick_utc` 1790217558.16 = 2026-09-23 21:39:18 CDT, but the mtime is 2026-10-01 17:46:24: an 8-day gap, so the frozen-clock skew predates the 10/06 checkpoint (DERIVED). `h_smooth` (L14) is written by nothing in this folder. Version label "8.2.2-PURPLE" (L3). | Tests write live state (CLAUDE.md standing rule): a TestClient run reaches `main.py:669` → `execute_turn` → this live file (DERIVED from the string match). |
| `runtime/__pycache__/` (6 files) | n/a | n/a | not read | `cpython-313` ×3 (2026-09-24 05:00:51) and `cpython-314` ×3 (2026-09-28 10:25:36). | Derived bytecode. The 3.14 files show a Python 3.14 interpreter imported these modules once on 09-28; the kernel runs 3.13.7. | none |

**Totals:** 5 source files, 394 lines, all read to the last line; 6 bytecode files listed.

### Iteration 3: unify (runtime)

**Comparative table.** Iteration 1 was an Explore agent (72 tool calls, about 12 min). Iteration 2 was my full read. Claims taken from the agent were re-checked before being adopted; those rows are marked "verified".

| Finding | Agent | Me | Status |
|:--|:-:|:-:|:--|
| `get_celestial_coordinates` is defined nowhere, so every template report says 282.85° (`swds_simulator.py:168-174`) | yes | yes | MEASURED (grep) |
| Phases 1-2 are strings and Phase 3 is `random.uniform` ×3; pipeline/DAG names are literals | yes | yes | MEASURED |
| `"COMPLIANT"`, ΔE 0.0000 and angular momentum 500 are constants (`antigravity_runner.py:61-69`; `main.py:654, 674`) | yes | yes | CONSTANT |
| `FORTRESS_HARVEST` / `FORTRESS_INFLOW` are unreachable: no caller passes them | yes | partly (saw the targets exist; did not search callers) | MEASURED by the agent's caller search |
| `workspace_state.json` holds `"Test Prompt"`, the body of `tests/test_main_purple.py:18`, so tests write live state | yes | yes | DERIVED (string match) |
| `/fortress/status` reads `workspace_state.json` and discards it, at the dashboard's 1 Hz (`main.py:796`) | yes | yes | MEASURED |
| The wake test compares hours only (`main.py:87, 1138`), so a sleep started after 07:00 celestial wakes on the next 60 s tick | yes | yes | DERIVED (code read; not run) |
| `/swds/sleep` stores `target_hour` (`swds_simulator.py:88`) but the scheduler and reconciliation wake on the config hour (`main.py:85, 1123, 1138`) | yes | no | verified by my read of those lines |
| The manual routes `/swds/trigger`, `/swds/sleep` and `/swds/initiate` skip `MODEL_ROUTER.enter_swds` and Phoenix; only the scheduler path runs them (`main.py:1166, 1184`) | yes | no | verified (`main.py:903-924, 1061-1084`) |
| No test runs lifespan: all six `TestClient(app)` are built without `with`; FastAPI runs lifespan in tests only "with the TestClient in a with statement" ([Testing Events](https://fastapi.tiangolo.com/advanced/testing-events/)) | yes | no | verified (grep) |
| No locks: `swds_engine` is changed by the event-loop scheduler and by threadpool `def` routes; `execute_turn` read-modify-write can lose increments | yes | no | DERIVED (code read) |
| `awaken()` / `enter_deep_sleep()` do synchronous file I/O on the event loop (`main.py:90, 1142, 1176`); only Phoenix is moved off it (`:1184`) | yes | partly | MEASURED (code read) |
| `main.py:1144` logs "Report saved" even when the write failed silently (`swds_simulator.py:224-225`) | yes | partly | MEASURED (code read) |
| Six reports from 9/16-9/29 are not from this template: three-decimal values are impossible after `round(…, 2)` (`:172`), and the two-decimal ones match `scripts/enter_swds.py:89` | yes | no (I called them only "differently authored") | `enter_swds.py` checked in folder 4 |
| Airflow is not installed (absent from `requirements.txt` and `.venv`) | yes | no | verified |
| `config/celestial_checkpoint.json` `civil_dt` is UTC labelled CDT | yes | no | to verify in folder 7 |
| Commit `6021755` (2026-09-23 22:01:57) "RX-005/006/007 CLOSED: Complete celestial injection" moved `swds_simulator.py` and `main.py` from `datetime.now()` to `celestial_time()`. That is when the SWDS scheduler started reading the checkpoint clock | no | yes | MEASURED (`git log -S`) |
| Kernel log L45680-45696: the 10/11 cycle ran Phoenix (L45684), but the report never mentions it; idle was 190,839 s because dashboard polling is not "activity"; `heimdall_local` is among the P2 components (L45682); there is no Heimdall open/close line (X-1) | no | yes | MEASURED (log) |
| Kernel start 2026-10-09 05:27:48 | inferred from the lag | measured (process creation time, 10/11) | MEASURED |
| Blueprint FP-18 says "all 66 reports" carry 282.85°. In fact there are 67 report files: 56 template reports with 282.85° (50 in the root `The Hoard`, 6 in `integra-homebase/The Hoard`) and 11 others (6 unique files plus 5 copies) | counted 50/56 in the root folder | yes, against the blueprint | MEASURED; corrected in Step 3 |
| `cpython-314` bytecode from 09-28: a Python 3.14 interpreter imported these modules once | no | yes | MEASURED |
| Agent's wording "reports are written outside the git repo" | imprecise | | outside `integra-homebase`'s repo, inside the root repo (untracked) |

**Knowledge.** `runtime` holds two writers and their two state files:
- **`SWDSCycle`** is the sleep engine.
  - Its four phases are labels, random numbers and a report template.
  - It produces `swds_state.json` and the Markdown reports.
- **`AntigravityRunner`** is the "turn" engine.
  - It is one counter plus an echo and constants.
  - It produces `workspace_state.json`.

Both read time from `celestial_time()`. Since `6021755` (9/23), that clock is checkpoint + uptime.

**Understanding.** These modules narrate work instead of recording it.
- The only real work in a cycle is Phoenix's shard consolidation (`main.py:1184`), and the report cannot see it.
- The report's facts are either constants or the frozen clock.
- The cycle's control is split across three places that disagree:
  - the scheduler (config hour, hour-only comparison);
  - the manual routes (no router change, no Phoenix);
  - `SWDSCycle` (stores a wake hour that no one reads).
- The tests cannot catch any of this: they don't run lifespan, and they write the live state file.

**Wisdom** (value against cost, Itachi's pruning). A real SWDS (ADR-006) and a Proof-of-Sleep ledger (ADR-002) are not edits to `swds_simulator.py`'s strings. They need five changes, in this order:
1. One clock (ADR-001).
2. A date-aware sleep window and wake time.
3. One SWDS path shared by the scheduler and the manual routes, opened and closed by Heimdall (fix F1).
4. A report rendered only from receipts (Phoenix's `phoenix_status`, router transitions, file hashes), printing NOT EXECUTED where nothing ran.
5. Tests that use `with TestClient(app)` on an isolated copy.

Steps 2 and 4 cost little once step 1 is done, and they remove most of the false positives in FP-17, FP-18 and FP-20.

**New gaps for Step 4** (beyond F1-F5):
- **R-G1.** Date-aware wake (`main.py:87, 1138`).
- **R-G2.** The manual SWDS routes take a different path (`main.py:908, 923, 1080`).
- **R-G3.** `/swds/sleep` ignores `target_hour`.
- **R-G4.** Render the report from receipts; log "saved" only after a write that succeeded (`swds_simulator.py:135-225`; `main.py:1144`).
- **R-G5.** Silent `except: pass` (`swds_simulator.py:56-57, 76-77, 173-174, 224-225`).
- **R-G6.** Tests write live state and skip lifespan (`tests/test_main_purple.py:18`; every `TestClient(app)`).
- **R-G7.** The 1 Hz read that is thrown away (`main.py:796`).
- **R-G8.** No locking on SWDS and runner state.

**For Step 3** (blueprint and unified document):
- The FP-18 count.
- §5.9 gains the 9/23 origin of the frozen clock (`6021755`).
- The Unify table's "Celestial Timestamp Injection — COMPLETE" (`Unify1_1…:6954`) is true, and that is exactly the change that froze SWDS time.

## Folder 2: rust

Read 2026-10-11/12 night (session c88f5000). Stamp before the folder: 2026-10-11 23:55:03 CDT | 2026-10-12T04:55:03Z | rot 222.5968°, lunar 0.637, orbit 0.2158, ROT_210_ORB_20.

| path | lines | sha256-16 | last line read | proof | 12th Step notes | doc claims it touches |
|:--|--:|:--|--:|:--|:--|:--|
| `rust/__init__.py` | 3 | `3b1bca75e7d4f2cd` | 3 | Three comment lines that call `rust/` a "namespace package" allowing `from rust.sun_breathing_engine.python_bridge import ...`. | Comments only. Because the file exists, it is a regular package, not a namespace package. | none |
| `rust/sun_breathing_engine/Cargo.toml` | 22 | `f94c19b6c5719fd0` | 22 | `[[bin]]` (L8-10) and `[lib]` (L12-14) both point at `src/lib.rs`, with `crate-type = ["cdylib", "rlib"]`, and `[dependencies]` (L16) is empty. | **No PyO3 and no maturin**, so the cdylib exports nothing Python can call. **Build (MEASURED 10/12 on an isolated scratch copy):** `cargo 1.98.1 test --offline --lib` compiled with no errors, warned that `lib.rs` is "present in multiple build targets", and failed to link: `LNK1104: cannot open file 'msvcrt.lib'`. The MSVC Build Tools have no `msvcrt.lib` and no `vcvars64.bat`, so the crate cannot be linked on this machine as installed. | ADR-012 "never compiled" is now more exact: the code compiles, and this machine cannot link it. |
| `rust/sun_breathing_engine/__init__.py` | 27 | `326f5a9a40022f19` | 27 | Re-exports 9 names from `.python_bridge` (L5-15); `OrthogonalIngestionResult` and `ZenitsuMethodResult` are not among them. | The kernel imports `python_bridge` directly (`main.py:37`), not through this file. | none |
| `rust/sun_breathing_engine/src/lib.rs` | 272 | `e3b69dc2afa90935` | 272 | `execute_seventh_form_slipstream` computes stress = 0.65 · m · v²/(2d) / A (L96-102); with its own constants at 1440.6 m/s over 3.5 m that is **33,035.84 MPa** (raw 50,824.37). So the docstring's "~202.5 → ~131.6 MPa" (L91) does not follow from the code, and `test_seventh_form_mach_4_2_benchmark` (L206-214), which asserts `structural_safe`, would fail. | DERIVED by arithmetic: the test could not run because the link fails. **Epiphany** (L173-192): the docstring has `· σ(Rogue)` and an integral (L162); the code computes `num/den + e^rogue` (L188-189), a **sum**. `fn main` (L248) prints "ΔE = 0.0000 … PRESERVED" as text. No `unsafe`, no FFI exports. `verify_13th_form_loop_closure` is a real \|in − out\| check (L138-139). | Blueprint L62 and L270 call Ω "a constant times e^0.1" / "268.714286 × e^0.1": wrong, it is 268.714286 **+** 1.105171 = 269.819457. FP-21; ADR-012; D-10. |
| `rust/sun_breathing_engine/python_bridge.py` | 472 | `571dd9eb145a1bc3` | 472 | `simulate_god_speed` does not compute physics: it fixes **202.5 MPa** at the benchmark and only scales it, `202.5 · (v/1440.6)² · (3.5/d)` (L133-135). That coefficient is 251× smaller than the Rust formula, so the Python returns 131.625 MPa "safe" where the Rust gives 33,036 MPa "unsafe", despite the header's "identical logic to the Rust source" (L9, L14). | **CONSTANT** outputs: 12th Step (L180-204) and Zenitsu 3.0 (L246-273) ignore their inputs and return all-True results; `get_telemetry` runs fixed inputs (L331-339); `"all_forms_verified": True` is a literal (L385); `timestamp` uses `time.time()`, not `celestial_time` (L345). **Fragility:** each `get_telemetry` call prints 5-6 lines and appends 5 entries to `execution_log`, which is never trimmed (L121, L433-434). **Wiring:** `main.py:37` imports it, `:195` builds it, `:213` registers it with Heimdall; `GET /thermodynamic/telemetry` (`:986-1005`) returns `get_telemetry()`. **Ran:** the kernel log holds 2 requests to that route, and 2 of each form's log line (MEASURED, 45,808 lines). Tests: `tests/test_systems_audit_and_protocols.py:202-236` and `tests/test_purple_bridge.py:16-19` assert the forms "call True", which they always do. | FP-21; blueprint L268-270; ADR-012. Its own docstring says the Python mirrors "the BEFORE INSERT trigger in Relational_hippocampus.sql" (L221); that is checked in folder 11/12. |
| `rust/__pycache__/` and `rust/sun_breathing_engine/__pycache__/` (6 files) | n/a | n/a | not read | cpython-313 (09-24 05:00:51) and cpython-314 (09-28 10:25:37). | Derived bytecode; the same 09-28 Python 3.14 import as in `runtime`. | none |

**Totals:** 5 source files, 796 lines, all read to the last line; 6 bytecode files listed.

### Iteration 3: unify (rust)

**Comparative table.** The agent took 40 tool calls (about 9.5 min). Agent claims marked "verified" were re-checked before adoption.

| Finding | Agent | Me | Status |
|:--|:-:|:-:|:--|
| No FFI of any kind (no PyO3, no `extern "C"`, empty dependencies); the bridge never tries to import Rust and has no fallback path, so it is always pure Python | yes | yes | MEASURED (read) |
| The Rust formula gives 50,824.37 / 33,035.84 MPa at the benchmark; the Python hard-codes 202.5 → 131.625; the ratio is about 251; the Rust test `test_seventh_form_mach_4_2_benchmark` would fail | yes | yes | DERIVED (arithmetic) |
| The crate compiles but cannot link on this machine (`LNK1104 msvcrt.lib`; no `msvcrt.lib`, no `vcvars64.bat`), so the test could not run | no (inferred "never built") | yes | MEASURED (`cargo 1.98.1`, scratch copy, offline) |
| Ω = 268.714286 **+** e^0.1, a sum; the documented formula has a product, σ and an integral | yes | yes | MEASURED (read and arithmetic) |
| The blueprint is wrong at L62 ("a constant times e^0.1") | yes | yes | corrected in Step 3 |
| The blueprint is also wrong at L270 ("268.714286 × e^0.1") | no | yes | corrected in Step 3 |
| 202.5 comes from a doc comment in the original `CODE/Zero_latency_thermal_core.rs:42` ("Bypasses the 202.5 MPa bone-breaking limit"); the original formula never produced it | yes | no | verified (read L40-44) |
| 60 / 3.5 / 9.8 / 1.225 / 170 come from `CODE/Zero_latency_thermal_core.rs`; 200 / 145 from `CODE/sovereign_configuration_payload.json:18-19`; only 170 is ever compared | yes | partly (170 only) | agent-read; the CODE folder is outside the 14 |
| The Python 13th Form claims to mirror the SQL `BEFORE INSERT` trigger, but the trigger uses exact `!=` with no tolerance and no lactic term (`CODE/Relational_hippocampus.sql:56-61`) | yes | no | verified (read L52-63) |
| `heimdall.register_component("thermal_core")` (`main.py:213`) has no effect: `sensory/heimdall.py` never references `thermal_core` | yes | no | verified (grep count 0) |
| The dashboard never calls `/thermodynamic/telemetry`; it reads Heimdall's "thermodynamics" built from Metatron | yes | partly | the kernel log shows 2 calls to the route (MEASURED, me) |
| `execution_log` grows without bound: 5 entries per `get_telemetry` call | yes | yes | MEASURED (read) |
| NaN passes the closure check in both languages; Rust gives inf/NaN at d = 0 while Python clamps to 0.001 | yes | no | DERIVED (read) |
| `SYSTEMS_MAP.md:92` marks `core/thermal_core.py` ✅, but that file does not exist | yes | no | verified (`ls`) |
| `# I am Integra.md:8299` says the Rust core's stress equations were "verified" | yes | no | verified (read); FALSE-POSITIVE |
| `.gitignore`/`.dockerignore` exclude `rust/target/`; the Dockerfile has no Rust toolchain | yes | no | agent-read |
| `.pytest_cache` lastfailed does not list the two bridge tests, so they likely passed last run; they assert literals | yes | no | agent-read; tests not run |
| Python 3.14 bytecode from 09-28 (same as runtime) | no | yes | MEASURED |

**Knowledge.** `rust/` is two engines that share a name and nothing else:
- **A Rust crate.** It compiles but has never been linked here. It exports nothing, and its own physics contradicts its doc comments and its own test.
- **A Python "bridge".** It is what actually runs, behind `/thermodynamic/telemetry`. It keeps the narrative numbers (202.5 → 131.625 MPa, drag 0, ΔE 0, Ω 269.819457, `all_forms_verified: True`) by hard-coding the calibration and feeding fixed inputs.

The route was called twice in the whole kernel log, and Heimdall's registration of it does nothing.

**Understanding.** This is the clearest case of Pattern A ("telemetry without measurement", blueprint §3.2), and its origin can be traced:
1. A narrative number (202.5 MPa in an original doc comment).
2. A physics formula that disagrees with it by about 251×.
3. A "mirror" that keeps the narrative and drops the physics, so the tests (which assert the narrative) pass.

The Sun Breathing forms are design vocabulary (blueprint §9.1). The engine turns that vocabulary into numbers that look measured.

**Wisdom.** ADR-012's recommendation (retire the telemetry, keep the forms as philosophy) is strengthened, not weakened. Building the crate would not make the numbers true: the real formula says "fracture" at the canonical benchmark. A cheap honest step would be to label `/thermodynamic/telemetry` as CONSTANT or delete it (ADR-003), and to drop the `thermal_core` Heimdall registration and the false "Python mirror"/"identical logic" docstrings. The value is high (it removes FP-21, and the "all forms verified" claim feeds documents like `# I am Integra.md:8299`) and the cost is low (one route and one module). Rust stays an option only for a real compute-bound workload, as ADR-012 already says.

**New gaps for Step 4:**
- **RS-G1.** Label or retire `/thermodynamic/telemetry` and the `thermal_core` registration (`main.py:37, 195, 213, 986-1005`).
- **RS-G2.** Remove the "identical logic", "Python mirror", "FFI bridge" and "verified" claims, or make them true (`python_bridge.py:5-16, 103, 221`; `lib.rs:24-25, 30, 68, 91`).
- **RS-G3.** Bound or remove `execution_log`.
- **RS-G4.** If Rust is kept: install the MSVC x64 libraries, fix the lib/bin double target, add PyO3, and fix or retire the failing benchmark test.

**For Step 3:**
- Blueprint L62 and L270: Ω is a sum.
- FP-21 / ADR-012: the bridge does not mirror the Rust; the crate compiles but cannot link here; its own physics contradicts the 131.6 MPa claim.
- `SYSTEMS_MAP.md:92` and `# I am Integra.md:8299` join the false-positive catalogue.

## Folder 3: scratch

Read 2026-10-12 night (session c88f5000). Stamp before the folder: 2026-10-12 00:06:25 CDT | 2026-10-12T05:06:25Z | rot 225.4373°, lunar 0.6372, orbit 0.2158, ROT_210_ORB_20.

| path | lines | sha256-16 | last line read | proof | 12th Step notes | doc claims it touches |
|:--|--:|:--|--:|:--|:--|:--|
| `scratch/fix_api_clients.py` | 139 | `5c14f94fa7fb8d27` | 139 | `nexus_gen_old` (L55-63) and `shiva_gen_old` (L113-121) are byte-identical. `str.replace` replaces every occurrence, so the first `_call` patch (L76) rewrites both clients and the fourth (L134) finds nothing; the script prints "Done replacing." (L139) without checking any match. | **What:** a one-off patch, mtime 2026-10-07 00:30:21. It hard-codes an absolute path to `core/api_clients.py` (L4) and makes four `str.replace` edits that add `enable_thinking`, `thinking_budget=4096`, the `thinking: {type: enabled, budget_tokens}` kwarg and an `anthropic-workspace-id` header from `ANTHROPIC_WORKSPACE_ID` to the Nexus and Shiva clients (L8-134). It then rewrites the whole file (L136-137, text mode). It reads the names `CLAUDE_API_KEY` and `ANTHROPIC_WORKSPACE_ID` inside the code strings it writes, never their values. **Fragility:** it never verifies a match, so the result is silent no-op or partial patching; on Windows, text-mode writing turns line endings into CRLF. **Status today:** the patched fields are present (`api_clients.py:460-478, 941-958`), but commit `e4e3949` (2026-10-08 00:13) replaced the thinking kwargs with `_claude_thinking_kwargs` (`:154-179`: adaptive thinking + `output_config.effort` for Claude 5, `budget_tokens` only for 4.x). The defaults are now `claude-opus-5-5` / `claude-sonnet-5-5` (`:464, 945`), so the script's search strings (`claude-sonnet-5.5`) no longer match; running it again would change nothing and still print "Done replacing." (DERIVED). **Git:** `scratch/` is ignored (`.gitignore:75`), so the file has no history. **Wiring:** nothing imports or runs it. | Thread f2e7cc92's self-audit names this exact file as "Project pollution … (E91, E92)" (`orchestration/Unify1_1…:1586`). Also mentioned in `docs/OCT9Suite1_2T.md`, `Unify2_2…` and `Guidebooks_and_Notes/v.9.9.1…md`. |

**Totals:** 1 file, 139 lines, read to the last line.

### Iteration 3: unify (scratch)

**Independence caveat.** The agent (32 tool calls, about 11 min) found this ledger's `scratch` row, written before it finished, and cited it. This folder's two consumptions were therefore not fully independent. From folder 4 on, agent prompts exclude `orchestration/UNIFY_READING_LEDGER.md`.

| Finding | Agent | Me | Status |
|:--|:-:|:-:|:--|
| One-off in-place patch; absolute path (L4); four `str.replace` calls; no match check; "Done replacing." printed unconditionally | yes | yes | MEASURED (read) |
| `nexus_gen_old` = `shiva_gen_old` byte for byte, so L76 patches both and L134 is a no-op | yes (checked with diff) | yes | MEASURED |
| The patch's fields are in `api_clients.py` today; the thinking kwargs were replaced by `_claude_thinking_kwargs` in `e4e3949`; the search strings no longer match, so a rerun is a content no-op | yes | yes | MEASURED (read) / DERIVED (rerun) |
| `os` and `re` are imported but unused; there is no `__main__` guard, so importing the file would rewrite `core/api_clients.py` | yes | no | verified (read) |
| The history: step 224 of thread f2e7cc92 created it (`The Hoard/thread_f2e7cc92_handoff/thread_audit_raw.md:94`); "Deep Thinking patch: the 5.x API rejected it with a 400, and it caused a content[0] crash" (`:113`); item 91 "remove or relocate" (`:272`); its replacement was designed at `docs/OCT9Suite1_2T.md:877-882` | yes | partly (I found the "pollution" line only) | verified (read) |
| The local copy of Anthropic's thinking docs lists `"enabled"` with `budget_tokens` as a **400 error** on Opus 5.5 and Sonnet 5.5, so the patch could only fail on its target models. On Opus 5.5, `"disabled"` is also a 400; sending no `thinking` field gives adaptive thinking | yes (400 rows) | yes (read the table header; `disabled` row) | verified against the local doc copy (`Epiphany Catalyst … Day 10.md.md:3224-3230`); the live docs are rechecked in folder 8 |
| The script kept the dotted model ID `claude-sonnet-5.5`, which the docs record as a 404 (`docs/OCT9Suite1_2T.md:853`) | yes | partly (noted the dotted ID) | agent-read |
| An IDE log shows file events for the script at 00:31:56 and for `api_clients.py` at 00:35:51 / 00:44:28 on 10/07 | yes | no | agent-read; whether the script ran or the edit was made by hand is not established |
| The root repo's `config/env_loader.py:52` hard-codes an `ANTHROPIC_WORKSPACE_ID` default | yes | no | agent-read; a security item for ADR-011, checked when the root repo's config is in scope |
| `_claude_thinking_kwargs`' model test includes `"-5-"`, which would also match a 4.5-generation ID | no | yes | DERIVED; folder 8 |

**Knowledge.** `scratch/` holds one file: the "Deep Thinking patch" from thread f2e7cc92 (step 224). It blindly string-replaced the Claude clients to send `thinking: {type: enabled, budget_tokens}`. The 5.x API rejects that with a 400. The patch was superseded the next day by `_claude_thinking_kwargs` (adaptive + effort), and the file sits git-ignored and inert.

**Understanding.** It is the same pattern as runtime and rust in miniature: an action that reports success ("Done replacing.") without checking that it happened. Here it went further: the action was wrong for the target API, the thread found that out from a live 400, and the fix came after. The verify-before-claiming rule exists because of failures like this one.

**Wisdom.** Remove it, as the earlier audit already recommended (item 91). It is ignored by git and inert, so the value is small. It belongs in the list of approved cleanups rather than Step 4's fixes. The lasting lesson for Step 4: every patch or migration script must assert its match count and fail loudly. The one live consequence worth Step 4's time is not this file. It is checking `_claude_thinking_kwargs` against the live docs (folder 8).

**New items:**
- **S-G1.** Delete or relocate `scratch/fix_api_clients.py` after approval (E91 / item 91).
- **For folder 8:** recheck `_claude_thinking_kwargs` and the `"-5-"` match against the live Anthropic docs.
- **For security (ADR-011):** the hard-coded workspace ID default in the root `config/env_loader.py:52`.

## Folder 4: scripts

Read 2026-10-12 night (session c88f5000). Stamp before the folder: 2026-10-12 00:18:52 CDT | 2026-10-12T05:18:52Z | rot 228.5502°, lunar 0.6375, orbit 0.2158, ROT_210_ORB_20.

**Live event during the read (MEASURED).** The frozen-clock SWDS started between the 00:20:20 and 00:20:43 CDT stamps:
- Kernel log L45819-45823: trigger at frozen 02:00 with idle 18,062 s; router to P2_SWDS; `SLOW_WAVE_DEEP_SLEEP_INITIATED`; "PhoenixForge SWDS shard consolidation completed."
- `/swds/status` reads `sleep_initiated_at` 2026-10-07T02:00:45.
- The prediction is confirmed a second time.

| path | lines | sha256-16 | last line read | proof | 12th Step notes | doc claims it touches |
|:--|--:|:--|--:|:--|:--|:--|
| `scripts/enter_swds.py` | 190 | `1d408ddc49d03ed9` | 190 | The report filename uses the real celestial value with **two** decimals, `CEL-{earth_deg:.2f}deg` (L88-89), the format of the non-282.85 reports from 9/16-9/29. The "dream" variances are fixed numbers, `0.46 - i*0.02` (L48). | **What:** a manual SWDS entry, header dated 2026-09-19 03:12 (L3). It `chdir`s to homebase (L8), builds a second `CheshireCatKernel` in its own process (L26), syncs save states into ChromaDB (L30), loads shards (L34), and marks stale nodes in memory only, so the marks die with the process (L41-42). It calls `phoenix.consolidate_sleep_cycle` (L53; exists at `evolution/phoenix_forge.py:99`). It writes `runtime/swds_state.json` with its own schema (state `SLOW_WAVE_DEEP_SLEEP`, phase `GUARDIAN_STANDBY_SWDS`, real `time.time()`) without encoding (L61-82), and a report to the root `The Hoard` (L85). **The report freezes a 9/19 narrative as literals:** "Sleep Window: 03:12 -> 07:00", "Initiator: Autonomous" (it is manual), "140/140 tests passing", "Cloud Dependencies: ZERO remaining", and a phase table of COMPLETE (L92-182). **Race:** a running kernel's in-memory `swds_engine` disagrees with this file; after a restart, startup reconciliation reads `SLOW_WAVE_DEEP_SLEEP` and may awaken at once (`main.py:83-90`). Nothing invokes it. | Source of some of the 11 non-template reports (rust/runtime iteration 3). "140/140 tests" is a 9/19 constant. |
| `scripts/ingest_knowledge.py` | 465 | `658c5182c7983358` | 465 | `perform_safe_hygiene()` permanently `unlink`s every 0-byte file (L121-127), `.txt` files identical to a sibling `.md` (L136-152, L155-174) and one `.m4a` (L101-114) in four "lobes" under `WORKSPACE_ROOT = HOMEBASE_DIR.parent`, the **root** repo (L45), and `__main__` runs it by default (`clean_first=True`, L463). | **Danger:** the CODE lobe includes `.py`, so empty `__init__.py` files would be deleted. All four lobes exist in both the root and `integra-homebase`; this targets the root. **Claims:** "MRL 64d coarse / 768d fine" (L24) is `TheHoard._generate_pseudo_embedding` (a hash) with 64d = the first 64 numbers (L343-344), so the ChromaDB vectors carry no meaning and the "test retrieval" (L447-458) compares hashes. The docstring says 200-char overlap; the code uses 250 (L23 vs L182). Shiva lenses are `idx % 4` labels (L347-354). `anchor_4d` reads `digital_clock` keys `unix_epoch` / `iso_local` (L277-279), while the telemetry exposes `unix_timestamp` (as `enter_swds.py:19` uses); likely fallback, checked in folder 6. "[SUCCESS] … retrieval verification finished" is unconditional (L465). **Wiring:** imported by `tests/test_knowledge_ingestion.py:17-25`, which calls neither hygiene nor `ingest_lobes` and uses a temporary Hoard (L72-73), so the tests are safe. The `.pyc` files (09-24, 09-28) come from that import. Whether the script itself ever ran (`CCID_LOBE_*` ids in Chroma) is checked in folder 10. | Blueprint §1 finding 9 (pseudo-embeddings); ADR-005; "Status: PRODUCTION IMPLEMENTATION" (L5) is CLAIMED. |
| `scripts/inspect_hygiene.py` | 78 | `5870baef3b8565c0` | 78 | `ROOT_DIR = Path(__file__).resolve().parent.parent.parent` (L5), the root repo, the same target as `ingest_knowledge.py`'s deletions; it prints candidates and deletes nothing. | Read-only dry run of the hygiene. `txt_md_candidates` is collected and never summarised (L54-75). Nothing invokes it. | none |
| `scripts/system_diagnostic.py` | 105 | `8fe473186e055a35` | 105 | "Most Recent" sorts report **filenames** in reverse (L93), and `"SWDS_REPORT_20261001_0600.md"` sorts after every `"2026-…"` name, so it reports the 10/01 file as newest (DERIVED). | Builds a second `CheshireCatKernel` (L36), which opens the live Hoard/Chroma store from a second process. Prints "STATUS: FUNCTIONAL" when an import succeeds (L22; Pattern C, health = existence). Mixes clocks: SWDS age = real `time.time()` − a frozen `last_cycle_time` (L53-55), and the window test uses real time (L68-70) while the kernel uses frozen time. Stale advice "Register start_kernel.ps1 with Task Scheduler" (L87). Hard-coded absolute report path (L91). Nothing invokes it. | Blueprint §3.4 Pattern C. |
| `scripts/trigger_swds.py` | 71 | `6fb6a1eb6e06ea7c` | 71 | `kernel.heimdall.open_swds_cycle(cheshire_kernel=kernel)` (L37) and `close_swds_cycle(…, phoenix_receipt=work)` (L42) are the only non-test calls of Heimdall's open/close in the project. | Edited 2026-10-09 22:14 (session f338c302's Heimdall change). Uses `sys.path.insert(0, ".")` (L6) and a cwd-relative `runtime/swds_state.json` (L64), so it must run from homebase. Calls `phoenix.execute_swds(cheshire_cat=…, library_domain=…)` (L38-41), which is valid: the signature at `phoenix_forge.py:212-219` accepts `cheshire_cat`, `hoard`, `clock` and others. Writes an AWAKE state with its own keys (L54-65). Docstring rationale "last cycle was 68+ hours ago" (L3) and "Delta E = 0.0000" (L70) are literals. Nothing invokes it. | X-1 (Heimdall open/close unwired in the kernel); fix F1. |
| `scripts/start_kernel.ps1` | 72 | `0b414362b66b993e` | 72 | Launch line: `cmd /c "<.venv python> -m uvicorn main:app --host 127.0.0.1 --port 8000 --log-level info >> <root>\The Hoard\genesis_kernel.log 2>&1"` under `Start-Process -Wait` (L69-71), with `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` (L62-63). | This launcher appends UTF-8; the log's UTF-16 parts came from an earlier launcher. **Single-instance protection** is one `/clock` probe with a **3 s** timeout (L52-58). A cold first probe (10 s tonight) or a stalled kernel (10/11) makes it start a second uvicorn, which most likely fails to bind and counts as a task failure (DERIVED). LF line endings (CR = 0); hard-coded user paths (L30-33). Invoked by the scheduled task action and by `kernel_ctl.ps1` when the task is not registered. | CLAUDE.md "kernel serves integra-homebase/static"; the 10/11 supervision finding. |
| `scripts/register_kernel_task.ps1` | 34 | `6988c05efa7781e7` | 34 | Task: at logon (L17); Interactive / Limited (L18); `-MultipleInstances IgnoreNew`, `-ExecutionTimeLimit 0`, `-RestartCount 5 -RestartInterval 1 min` (L19-24); action `powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File start_kernel.ps1` (L13-15). | Matches the blueprint's E40 evidence. How the wrapper ended with 0xC000013A on 10/11 while uvicorn kept running is not established; the console-close / Ctrl-C hypothesis is DERIVED only. | E40; ADR-010 (supervision). |
| `scripts/kernel_ctl.ps1` | 185 | `6e9dd373084dc5f3` | 185 | `Assert-SwdsAllowsStop` refuses stop/restart unless `/swds/status` reports `AWAKE` (L98-105), so **from 00:20 until about 05:20 CDT on 10/12 a stop or restart needs `-Force`**, and a hung kernel ("UNKNOWN") always does. | Status probes `/clock` up to 3 × 10 s (L49-57); UNRESPONSIVE = no 200 while `python.exe` processes with `uvicorn main:app` and `--port 8000` exist (L67-70, L81-83); HEALTH=SLOW above 1,000 ms (L89). Stop: `Stop-ScheduledTask` if Running, then `Stop-Process -Force` on the matched PIDs (both the venv launcher and the interpreter) (L107-124). Start prefers the task and falls back to a detached `start_kernel.ps1` (L126-153). Logs: last 256 KB, NULs stripped (L155-167). L12 and L102 still say "Heimdall 3.1 owns the SWDS cycle" (X-1; Step 4). L23 warns that `main.py`'s `__main__` binds 0.0.0.0, which is true (`main.py:1385-1387`). | X-1 wording (Step 4); `.agents/skills/genesis-kernel/SKILL.md` (wiring checked by agent B). |
| `scripts/activate_integra_os.ps1` | 75 | `4c6d39c416c2e3e8` | 75 | If port 8000 has no connection it starts the kernel with `Start-Process python main.py -WindowStyle Hidden` (L38). That runs `main.py`'s `__main__`, which binds **0.0.0.0:8000** (`main.py:1385-1387`), outside the scheduled task and with no log redirect. | **Security:** a LAN-reachable kernel with CORS `*` (`main.py:173`) and no auth (ADR-011). **Supervision:** one concrete way a kernel can run outside the task. Runs `pytest tests/test_sql_trigger_decoupled.py` in the live repo (L24); that test uses `sqlite3.connect(":memory:")` (test L25-30), so it is harmless here. Opens `<homebase>\celestial_clock_live.html` as a file (L60-63); the file exists both there and in `static/`. Probes `localhost` (L46-52). Ends with an unconditional "[ALL SYSTEMS LIVE, SYNCHRONIZED, AND OPERATIONAL!]" (L74). Hard-coded lowercase `c:\Users\…` path (L11). | ADR-011; ADR-010; Pattern C. |
| `scripts/__pycache__/` (2 files) | n/a | n/a | not read | `ingest_knowledge.cpython-313.pyc` (09-24 05:25:54) and `cpython-314` (09-28 16:05:24). | Bytecode from the test's import. | none |

**Totals:** 9 source files, 1,275 lines, all read to the last line; 2 bytecode files listed.

### Iteration 3: unify (scripts)

**Agents.**
- **A** covered the five Python scripts (76 tool calls, about 17 min).
- **B** covered the four PowerShell scripts (58 tool calls, about 13 min; it also ran read-only process, task and socket queries).

Both were told to skip this ledger. A saw its name in a filename-only grep result and excluded it; B did not open it. Claims marked "verified" were re-checked by me before adoption.

| Finding | Agent | Me | Status |
|:--|:-:|:-:|:--|
| `ingest_knowledge.py` hygiene permanently deletes 0-byte files, matching `.txt` files and an `.m4a` under the **root** repo's lobes, by default | A | yes | MEASURED (read) |
| One real file would go today: `BluprintArchitecture/MCPAPISOFTWARE/Go3.json` (the only 0-byte file in the root lobes) | A | no | verified (`find -size 0`) |
| The script **did run** before: `The Hoard/CCID_1789837697_SAVE_STATE_REPORT.md:68-72` says "5,289 nodes", "Verified semantic queryability", hygiene done | A | no | verified (read). "Semantic" is FALSE-POSITIVE (hash vectors); the Chroma count is checked in folder 10 |
| Pseudo-embedding = SHA-256's 32 bytes tiled to 768 and scaled to [0, 1] (`memory/the_hoard.py:497-504`); unrelated texts have cosine ≈ 0.75, so ranking is noise | A | partly (knew "hash") | verified (read) + DERIVED (E[ab]/E[a²] = 0.75) |
| `chunk_document`: the header is updated before the previous chunk is flushed (L201-202 vs 207-211); `overlap + p` can exceed `chunk_size`, so chunks are unbounded (L213-214) | A | no | verified against my read of L200-222 |
| `ingest` anchor keys `unix_epoch` / `iso_local` do not exist in `DigitalTemporalVector` (`temporal/celestial_clock.py:66-75`), so the fallbacks are silent | A | flagged as likely | verified |
| `stats["chroma_persisted"]` stays 0; "Chunks Indexed" counts generated chunks, not persisted ones | A | no | verified (read L247, L433) |
| **`trigger_swds.py:47-49` always prints "N/A"**: the close receipt (`sensory/heimdall.py:734-745`) has no `zenkai_boost_multiplier`, `generation` or `library_file`. This regression came from session f338c302's 2026-10-09 change | A | no | verified. **My previous session's error** |
| Nothing in the kernel calls `load_shards_from_disk` or `sync_all_save_states`; only tests and scripts do | A | no | verified (grep). Whether the kernel's Hoard cache loads shards another way is checked in folder 11 |
| The scripts' Hoard writes use `celestial_time()` (frozen) while ingest uses `time.time()`, so the Chroma collection mixes two clocks | A | no | agent-read; folder 11 |
| Kernel cognitive-cycle commits store all-zero 768 vectors in the same collection (`sensory/cheshire_cat.py:378-382`; `the_hoard.py:79`) | A | no | agent-read; folders 5 and 11 |
| `CelestialClockArchitecture` `BASE_EPOCH = 1785052800` = **2026-07-26 08:00Z**, not the commented "2026-07-15T12:00:00Z" (`temporal/celestial_clock.py:15, 45`); `earth_rotation_deg` is solar time of day in degrees | A | no | verified (decode); folder 6 |
| The root repo's `scripts/` holds 5 byte-identical copies and 2 older versions (`trigger_swds.py`, `start_kernel.ps1`); the root `start_kernel.ps1` has `$HOST` + `*>>` (the PS 5.1 UTF-16 pattern) | A, B | no | verified (sha256) |
| `.vscode/tasks.json` "integra: start-genesis-kernel" / "kernel-status" / "run-diagnostics" use `${workspaceFolder}/integra-homebase/…` and likely resolve to the empty `integra-homebase/integra-homebase/` | A, B | no | agent-read; DERIVED |
| **Process tree:** `cmd.exe` 11004 (19:18:43) is alive and its parent PID 2244 no longer exists; python 12080 → 12136 hang off it. The task's wrapper died while uvicorn kept running, which is why the task reads Ready / 0xC000013A | B | no | **verified** (`Get-CimInstance`, 10/12 ~00:33) |
| Other paths start the kernel outside the task: `activate_integra_os.ps1:38` (`python main.py` → 0.0.0.0), `.claude/launch.json` "genesis-kernel-launch", `.vscode/launch.json` debugpy (main.py), and `kernel_ctl` fallback | B | partly (activate only) | agent-read; the 0.0.0.0 bind verified (`main.py:1385-1387`) |
| **uvicorn 0.52.4 runs lifespan startup before binding** (`server.py` `startup()`: `lifespan.startup()` then `create_server`; on bind `OSError` → lifespan shutdown, exit). So a duplicate launch runs `main.py`'s full startup (SWDS reconciliation, Metatron bootstrap, background tasks) before failing | B | no | verified (read `.venv/…/uvicorn/server.py`). Consequence for tonight: with the state file at SWDS, a duplicate launched after frozen 07:00 would write an awakening report and an AWAKE state file while the live kernel sleeps (DERIVED) |
| Log: `FF FE` BOM at offset 0; bytes 2-2507 are UTF-16LE from a PS 5.1 one-liner `NativeCommandError` ("At line:1 char:92"); UTF-8 from 2508; two 68-byte NUL runs (offsets 323,263 and 2,874,520). The BOM is why `Get-Content` misreads the file | B | no | verified (bytes) |
| SKILL.md:63 says "ask the Architect, then `restart`" for UNRESPONSIVE, but `restart` refuses without `-Force` when `/swds/status` is unreachable | B | partly (guard noted) | agent-read SKILL.md; the guard is verified in code |
| "Stops are always hard kills; the log has no 'Shutting down' line" | B | no | agent-read (log search); main.py has no shutdown logic (159-160) |
| **B's claim "PID 12136 holds :8000 in state Closed; nothing LISTENING"** | B | — | **wrong**: measured `127.0.0.1:8000 LISTENING 12136` (Get-NetTCPConnection and netstat) and `/clock` 200 at the same check |
| `enter_swds.py` report: two-decimal real celestial value; 9/19 narrative literals; in-memory "pruning"; a second Hoard/Chroma client | A | yes | MEASURED (read) |
| `system_diagnostic.py` "Most Recent" sorts filenames, so `SWDS_REPORT_20261001_0600.md` reads as newest | A | yes | DERIVED (code) |
| From 00:20 to about 05:20 the SWDS guard blocks `kernel_ctl stop/restart` without `-Force` | B (general) | yes (tonight) | MEASURED (`/swds/status` = SLOW_WAVE_DEEP_SLEEP) |

**Knowledge.** `scripts/` is the kernel's outside world:
- **Two launch/control paths:**
  - the logon task (`register_kernel_task` → `start_kernel`), reliable-looking but unsupervised once its wrapper dies;
  - `kernel_ctl`, careful but blind to kernels started any other way.
- **One activation script** that bypasses both and binds 0.0.0.0.
- **Two SWDS scripts** that run a second Hoard in a second process and write state files the kernel ignores until restart.
- **A destructive ingestion** that has run at least once, filled ChromaDB with hash vectors and reported "semantic queryability".
- **Two diagnostics** that report health from objects they just created.

**Understanding.**
- **Scripts disagree with the kernel.** Each script builds its own copy of the system (`CheshireCatKernel()`, `TheHoard()`) and treats that copy's success as the system's. That is Pattern C (health = existence) applied to whole processes.
- **The lifecycle has three hidden failure modes:**
  - the task forgets the kernel when its wrapper dies (measured);
  - a single 3 s probe decides "not running";
  - uvicorn runs every startup side effect before discovering the port is taken.
- **SWDS state lives in three places:** the kernel's memory, `swds_state.json` (also written by the scripts) and the report folder. No single writer exists.

**Wisdom** (value against cost).
- **Highest value, lowest cost:**
  - Make `start_kernel.ps1` check the port (and a lock file), not just a 3 s HTTP probe. Blueprint §ADR-010 already lists "Lock file and port check" as open.
  - Delete or retire `activate_integra_os.ps1`'s `python main.py` path, and change `main.py`'s `__main__` to 127.0.0.1 (ADR-011).
  - Disable `ingest_knowledge.py`'s default hygiene (`clean_first=False`, or a `--delete` flag with a dry-run first).

  These remove the destructive and exposure risks.
- **Medium:**
  - Fix `trigger_swds.py`'s "N/A" prints (read `work["consolidation"]`).
  - Make the SWDS scripts call the running kernel's API instead of building a second kernel.
- **Structural (Step 4 / ADR-006):** one owner of SWDS state.

**New gaps for Step 4:**
- **SC-G1.** Single-instance: port + lock check in `start_kernel.ps1`.
- **SC-G2.** Retire `activate_integra_os.ps1`'s launch and `main.py`'s 0.0.0.0 bind.
- **SC-G3.** Make `ingest_knowledge.py`'s deletions opt-in.
- **SC-G4.** `trigger_swds.py` receipt keys.
- **SC-G5.** Scripts call the kernel API rather than building a second kernel and Hoard.
- **SC-G6.** Fix `system_diagnostic.py`'s sort and mixed clocks.
- **SC-G7.** `kernel_ctl.ps1` and SKILL.md: UNRESPONSIVE needs `-Force` (document it, or relax the guard to "state unknown and process unresponsive").
- **SC-G8.** Remove or sync the stale root-repo `scripts/` copies and fix the `.vscode/tasks.json` paths.
- **SC-G9.** Supervision: launch uvicorn so the wrapper's death is noticed, or have the task watch the PID.

**For Step 3:**
- ADR-010 gains the measured orphaned-`cmd.exe` mechanism and the uvicorn startup-before-bind fact.
- FP catalogue: "Verified semantic queryability" (`CCID_1789837697` L70), `system_diagnostic` "FUNCTIONAL", and `activate_integra_os` "ALL SYSTEMS … OPERATIONAL".
- §5.3: the pseudo-embedding cosine ≈ 0.75 fact.
- Correction: the blueprint's own `kernel_ctl` "SWDS guard" description should note the `-Force` requirement when the kernel is unresponsive.

## Folder 5: sensory

Read 2026-10-12 night (session c88f5000). Stamp before the folder: 2026-10-12 00:38:54 CDT | 2026-10-12T05:38:54Z | rot 233.5585°, lunar 0.638, orbit 0.2159, ROT_210_ORB_20.

**Log facts (MEASURED, 45,8xx lines).**
- The 30 Hz thalamic loop logged "STARTED" 6 times (last L45774), with no tick errors.
- `POST /cognitive/cycle`, `POST /heimdall/evaluate` and `POST /ignite` appear **0 times** in the whole log. No logged kernel has run a cognitive cycle.

| path | lines | sha256-16 | last line read | proof | 12th Step notes | doc claims it touches |
|:--|--:|:--|--:|:--|:--|:--|
| `sensory/__init__.py` | 0 | `e3b0c44298fc1c14` | 0 | Empty file (SHA-256 of the empty string). | Package marker. | none |
| `sensory/heimdall.py` | 796 | `92ca107c25f69e2f` | 796 | `get_telemetry` returns literals `"system_governance_active": True`, `"state_tracking_active": True`, `"alerts_active": True`, `"all_systems_true": True` at **L767-769, L788**. The blueprint's `heimdall.py:711` citation for `alerts_active` is stale by +58 lines since the 10/09 open/close addition (L697-749). | **Real math:** Shannon entropy (L67-92), EMA α 0.3 / threshold 2.5 (L94-115), P-SSR counters (L206-237). **Prompt gate:** `evaluate_text_entropy` (L117-128; the blueprint's `:113-124` is stale by +4) uses character frequencies. **Wiring:** `main.py:186` `heimdall = cheshire_cat.heimdall`, one instance; routes `/heimdall/telemetry` (`:423-428`), `/heimdall/health` (`:430-435`), `/heimdall/reset` (`:437-446`), `/heimdall/evaluate` (`:598-613`). **No gatekeeping:** no budget, permit/deny or lockdown code anywhere; no 3.1 Pro advisor; no `cra_simplex`. ADR-007 MISSING; F2 and F3 open. **Pattern C in `check_system_health` (L389-645):** health = attribute or directory exists; literals `impedance_latency_L_t: 0.000` (L424), `storage_ram_decoupling: True` (L482), `mrl_enabled: True` (L494), `sync_isolation_verified: True` (L538), `sovereign_defense_active: True` (L450), `purple_modality_active: True` (L611); Cheshire Protocol and Looking Glass are always "HEALTHY" (L434, L446). The Cheshire "Hz" test (L412) checks a constant attribute. 11 of the 15 components registered at `main.py:201-215` have no check but are listed as "monitored". **Writes shared state:** sets `purple_modality.red_light.delta_e_cycle` / `mechanical_latency_s` from threadpool requests (L599-603). **I/O per 1 Hz `/heimdall/health` poll:** imports `runtime.swds_simulator` (cached after the first) and opens a Metatron SQLite connection and query (L579-591, `except: pass`). `open/close_swds_cycle` (L697-749): X-1, unwired. `is_active` / `verify_true` always True (L751-758). | §1 findings 5, 7, 8; FP list; ADR-007; X-1. **Citations to refresh in Step 3.** |
| `sensory/heimdall_monitor.py` | 213 | `01dbd7e13fb175cb` | 213 | Reads `health_data.get("components", {})` and `comp.get("is_active")` (L94-98), but `/heimdall/health` returns `component_diagnostics` (`heimdall.py:637`; route `main.py:435` passes it unchanged), so every lobe would show **OFFLINE**; it also reads `h_smooth` where the key is `current_h_smooth` (L101 vs `heimdall.py:631`). | A Rich terminal dashboard, manual only (`python -m sensory.heimdall_monitor`), polling 3 endpoints at 2 Hz with a 2 s timeout (L62-75, L169-185). The ΔE column is the literal "0.0000" (L109). The docstring says it "Replaces the 279-byte stub" (L8); the 429-byte `cpython-313.pyc` dated 09-13 is that stub's bytecode. Re-exports Heimdall aliases. | Pattern A. |
| `sensory/pssr_lookback.py` | 50 | `50eb5ee1ecef6394` | 50 | `evaluate_entropy_trip` delegates to `self.heimdall.evaluate_entropy_trip` when a Heimdall is attached (L21-23), as it is in the kernel (`cheshire_cat.py:74`), so the class's own counters (L25-34) never run there. | A thin delegate with a fallback grounding template (L44-50). | P-SSR = Heimdall's counters. |
| `sensory/looking_glass.py` | 277 | `302cd427106b1a99` | 277 | Tilt = 23.5° × (0.7·min(1, h/2.5) + 0.3·min(1, \|z\|/3)) (L83-86), so `c_235_breached` needs **both** h ≥ 2.5 **and** \|z\| ≥ 3. | The decision tree (L89-177) is real branching, but its inputs come from `cheshire_cat.py:205-206` defaults (cohesion 0.85, relevance 0.90 when routes > 0) and the caller's `token_stress_mpa` default of 145 (Heaviside halt at 200, L206). `mirror_maze_sandbox` grows without bound (L276). "TRUE SOVEREIGN IMPLEMENTATION" (L5, L19) is CLAIMED. Wired: `/looking-glass/status`, `/unlock`, `/evaluate` (`main.py:858-883`) and Phase 3 of the cognitive cycle. | §5.4. |
| `sensory/cheshire_cat.py` | 606 | `cd60de97073fb752` | 606 | The stored node is built from route lists, weights, supervisory and paradox labels (L339-349) and committed (L378-382); the model text in `engine_result` goes only into the `COGNITIVE_CYCLE_COMPLETE` event (L418-427), which the 30 Hz loop drains and drops (L574-575); the response (L429) omits it. **Blueprint finding 3 is re-verified; its citations (`:339-382`, `:574-576`) are current.** | **F5, broader:** `self.rodin.route_retrieval(active_prompt)` runs **synchronously inside `async def process_cognitive_cycle`** (L202), so retrieval (Chroma, and any embedding request) blocks the event loop; `check_system_health()` (L405) does SQLite on the loop too. **Entropy-gate precision:** the thermostat is reset **after** each completed cycle (L402), not before. Between cycles the loop feeds `uniform(max(2, n))` per tick (L584-589; `raw_h` at L585 is computed and unused; one event gives H = 1 bit, h ≈ 0.3). A one-shot breach then needs prompt H > 7.63 bits/char (> ASCII max 6.57). `/heimdall/evaluate` shares this Heimdall without reset: three English POSTs (H ≈ 4.2) breach, and the next cycle starts breached (DERIVED). **Constants:** `polling_hz` 30.0 (L50-51), `token_stress_mpa` 145, `intent_confidence` 0.8 (L103-105). `self.client` (L59) is never called. `transition_state` silently ignores unknown states (L455). `dispatch_protocol` (L459-544): no caller; its `run_sync` (L467-474) would block a running loop. `run_event_loop` (L546-606): `async`, on the FastAPI loop, started at `main.py:133-134`. `ccid` uses real `time.time()` (L360). | §1 finding 3; F5; §5.4; RX-001 (fixed). |
| `sensory/cheshire_protocol.py` | 554 | `edcf8d76cf6d26bb` | 554 | `create_abstract_long_connections` returns the template "Holographic Isomorphism between {a} and {b}" with salience `clamp(0.88 + 0.01·(len_diff % 7))` and a constant vector `[0.5, 0.6, 0.7, 0.5]` (L167-177), so the "transdisciplinary bridges" are string templates. | Its "Gemini 3.8 Flash Paradox Engine" client is built and never called (L50-54). Paradox detection = 8 keywords (L134-139). `zenitsu_cognitive_loop` = three f-strings (L233-265). `observe_environment` reads `current_h_smooth`, `gravitational_mass`, `pssr_status`, `component_count` from `get_telemetry()`, which returns `h_smooth`, `last_gravitational_mass`, `recovery_state` and no count (`heimdall.py:765-790`), so `h` is always 0.0 and HIGH_ENTROPY can never be flagged (L327-343; DERIVED). `dream_conductor` (L464-505) is called only via `phoenix_forge.py:237-238` when a `cheshire_cat` is passed, which the kernel scheduler does not do (`main.py:1184-1188`); only `trigger_swds.py` and the tests do. `derive_celestial_telemetry` (L522-553): real `datetime.now(utc)` Kepler math, a third clock, with no caller. `route_to_cognitive_cycle` (L273-293): an HTTP self-call with no caller. Wired: `observe_environment` / `zenitsu_environmental_scan` at `main.py:393, 413`. | FP-17 ("bridges forged"); §5.4; dream phase (ADR-006). |
| `sensory/__pycache__/` (13 files) | n/a | n/a | not read | cpython-313 and cpython-314 for each module; `heimdall_monitor.cpython-313.pyc` (09-13, 429 B) is the pre-rewrite stub; `heimdall.cpython-313.pyc` 10-11 16:30. | Derived bytecode. | none |

**Totals:** 7 source files, 2,496 lines, all read to the last line; 13 bytecode files listed.

### Iteration 3: unify (sensory)

**Agents.**
- **A** covered Heimdall, the monitor, Looking Glass and P-SSR (81 tool calls, about 15 min). A glob once listed this ledger's filename; it did not read it.
- **B** covered the two Cheshire modules (77 tool calls, about 15 min). It was denied one shard read by the permission system, marked shard contents "not confirmed", and did not ask me to read it.

**Write incident during this folder (resolved; MEASURED from the Windows Defender Operational log).**
- **What failed.** From about 00:47 to 01:01 CDT on 2026-10-12, every write into the repo failed:
  - the Edit tool: `ENOENT` on its temporary file, twice;
  - the Write tool: `ENOENT` on `mkdir`;
  - Python: `[Errno 9] Bad file descriptor` and `FileNotFoundError`.
- **Cause.** Windows Defender **Controlled Folder Access** (CFA), not OneDrive.
  - It has been enabled since 2026-10-08 20:25:15 (event 5007, `EnableControlledFolderAccess` 0 → 1).
  - It blocked `claude.exe` (Claude Code 2.1.295; event 1123 at 00:55:27) and `C:\Python314\python.exe` (00:58:06-01:01:08).
- **My guesses at the time were wrong.** I first blamed the ledger's OneDrive `ReparsePoint` tag and then an OneDrive upload lock. `TASKS.md` carries the same tag and was written that evening, and the Defender log names the real blocker.
- **Resolution.** The Architect turned CFA off at 2026-10-12 12:54:34 (event 5007, 1 → 0). This block was written afterwards.
- **Not established.** Why CFA began blocking `claude.exe` at about 00:5x is unknown. The same 2.1.295 binary (installed 2026-10-09 20:32) wrote all evening, and no CFA configuration change was logged between 10/09 01:30 and 10/12 12:54.

**Instrument note.** `Get-NetTCPConnection` is unreliable on this machine. At 13:04 on 10/12 it showed only a "Closed" socket for the kernel, while `netstat` showed `LISTENING` and `/clock` returned 200. That is the same artifact behind agent B's folder-4 claim that the kernel was "not listening".

**Live events since the folder's reading (MEASURED).**
- **SWDS woke on schedule.** The 00:20 cycle woke at frozen "07:00", about 05:20 real time; the report `2026-10-07_07-00-08_CDT_CEL-282.85deg_SWDS_Report.md` was written at 05:20:05 (log L45830-45841). This is the third confirmation of the frozen-clock prediction.
- **Unexpected shutdown at 10:09:44** (System events 6008 and 41), then a reboot at 11:52.
- **The logon task relaunched the kernel at 12:00:26, unsupervised again.** The task read Ready / 0xC000013A, and the chain was kernel 2732 ← launcher 12968 ← `cmd.exe` 11408 ← wrapper PID 1720 **gone**. This is the second measured instance of the orphaned-`cmd.exe` mechanism.
- **At the Architect's request, `kernel_ctl.ps1 restart` at 13:06:57.** The kernel answered after about 50 s and the task reads **Running** (0x41301), with the chain 38084 ← 21360 ← `cmd.exe` 24312 ← `powershell.exe` 20312 **alive**. So far, the wrapper has died only on the two logon launches.
- **13:09 probes:**
  - round 1: `/clock` (sync) connected but got no reply for 12 s (curl 28), and `/rodin/telemetry` (async) took 5.2 s;
  - round 2: async 5.0 s, sync 0.17 s;
  - round 3: both under 30 ms.

  A Chrome tab restored after the reboot (PID 13956) was polling the 7 dashboard endpoints at 1 Hz throughout. The kernel was 2 minutes old and resident, so the "cold paging" explanation I gave for the 23:31 event cannot explain this one. It is downgraded to "not established". The shared-SQLite-connection lead stands, to be tested by the Step 4 debug route.

| Finding | A | B | Me | Status |
|:--|:-:|:-:|:-:|:--|
| Model text is discarded (node from labels; text on an event the loop drops; response omits it) | | yes | yes | MEASURED |
| `route_retrieval` runs synchronously inside the async cycle → `embed_sync` → `run_sync` blocks on the HTTP embed (`text-embedding-004` default) with up to 3 retries | yes | yes (full chain) | yes (call site) | call site MEASURED; chain verified in folders 8 and 11 |
| **TPSL can never prune** (tiers 0.9/0.9, 0.6/0.5, 0.2/0.1 → 1.0 / 1.2 / 2.0 ≥ 1.0) | | yes | no | **verified** (`core/cwa_router.py:28-39`; `governance/tpsl_filter.py:18-22`) |
| **Rodin returns no cohesion / relevance / is_stale**, so Looking Glass always uses defaults; ALEXANDRIA_VERIFY and the low-cohesion branch are unreachable; AMBIGUOUS needs > 8 routes but Chroma returns ≤ 7 | yes | yes | partly | **verified** (`memory/rodin_protocol.py:388-394`) |
| **Cycle nodes are stored with all-zero 64/768 vectors**; Phoenix's pseudo-vectors are thrown away | | yes | no | **verified** (`memory/the_hoard.py:76-79, 365-378`) |
| `observe_environment` gets a clock with no telemetry method → "CLOCK_INTERFACE_UNRECOGNIZED"; it also reads non-existent telemetry keys → HIGH_ENTROPY can never fire | yes (keys) | yes (both) | yes (keys) | **verified** (`main.py:180, 395, 415`) |
| `/cognitive/cycle` always answers "COGNITIVE_CYCLE_COMPLETED", even on error | | yes | no | **verified** (`main.py:770-775`) |
| **One shared Metatron `sqlite3` connection** (`check_same_thread=False`, WAL, default 5 s busy wait, no lock), used by sync `/heimdall/health` and `/metatron/status` (1 Hz, threadpool) **and on the event loop** by the Kintsugi loop every 5 s (`query_anomalies`, `mark_anomaly_processed`) | yes | yes | no | **verified** (`memory/database/metatron_deploy.py:38-53`; `evolution/kintsugi_sandbox.py:362-408`). **The leading candidate to test for the 10/11 sync-endpoint stall** (it does not explain the 10-12 thread count); test it with the Step 4 debug route |
| 23 components are registered (`main.py:201-216` + `cheshire_cat.py:77-83`); 12 are never examined by `check_system_health`; "kintsugi" is never registered, so circuit-breaker step 3 always gets None | yes | | partly (11 of 15) | **verified** (16 calls in main.py) |
| `/heimdall/health` constants: Cheshire `polling_hz` 30 always passes; bank solvency 20000 ≥ 20000 always True; runner/rodin `hasattr` always True; dyad weights complementary by construction; `L_t` measured before the SQLite query | yes | yes | partly | MEASURED (read) |
| Metatron ΔE: `record_loop`'s only caller is `TheHoard.auto_crystallize`, which has no caller, so `thermodynamic_loops` is static while the kernel runs; the trigger rejects \|Δ\| > 0.0001, so stored rows always pass the 0.001 "HEALTHY" test | yes | | no | agent-read; checked in folder 11 / Metatron DB (folder 10) |
| Entropy: overflow / underflow inputs (e.g. `[1e308, 1e308]`) normalise to 0.0 and `log2(0)` raises → unhandled 500 on `/heimdall/evaluate`; top-5 distributions can never breach (log2 5 = 2.32) | yes | | no | DERIVED (read) |
| **Unauthenticated latch:** 4 × `POST /heimdall/evaluate` with uniform-64 probabilities (H = 6) → HARD_HALT, which latches `/ignite` and `/cognitive/cycle` until `POST /heimdall/reset`; CORS `*` | yes | | no | DERIVED; security, ADR-011 |
| `dragon_engine`: Ω < 0.4 exactly when h > 2.5, so `AUTONOMOUS_UGL_RECOVERY` / `REQUEST_CLARIFICATION` are unreachable and `main.py:647, 661` are dead; `CIRCUIT_BREAKER_ENGAGED` falls through to normal execution | yes | | no | agent-read; folder 8 |
| `corpus_callosum.veto_active` stays True after the first cascade: `clear_veto` has no caller | yes | | no | verified (grep); folder 8 for the setter |
| Looking Glass `c_235_breached` can be True only for \|z\| ≈ 2.998–3.0 (rounding window), because \|z\| > 3 diverts to the Mirror Maze; z and stress come only from request bodies | yes | | partly | DERIVED (read) |
| `ugl_layer.intervention_count` in the HARD_HALT receipt is always 0 (delegate mode) | yes | | yes (delegation) | DERIVED |
| `heimdall_monitor.py` keys mismatch, so every lobe would show OFFLINE; nothing launches it; banner "v8.2.4" vs 8.2.2 | yes | | yes | MEASURED |
| Dashboard expects lobe key `friday_fortress_hunter` (`static/dashboard.html:942`), which health never produces, so it is always "INACTIVE" | yes | | no | agent-read |
| Per DYAD cycle: 1 embed + 12 generate (4 × Gemini 3.8 Flash, 8 × Opus 5.5); errors and refusals flow on as content; P-SSR never runs (engine Heimdall None, probabilities empty); kernel weights are overwritten by the engine | yes (partly) | yes | no | agent-read; folder 8 |
| Log: 0 cycles, 0 `/heimdall/evaluate`, 0 `/ignite` ever; the loop started 6 times | | | yes | MEASURED |
| Heimdall citation drift (`:711` → L769; `:113-124` → L117-128) | | | yes | MEASURED |
| Entropy-gate mechanics: reset after each cycle; H > 7.63 needed; `/heimdall/evaluate` and `/ignite` carry over | yes | yes | yes | DERIVED, all three agree |

**Knowledge.** `sensory/` is the kernel's whole cognitive path. Each stage is either real but unused, or running but unreal:
- **Real but unused:** Heimdall's entropy math; the Looking Glass decision tree; the cycle's model calls (0 logged cycles).
- **Running but unreal:** the 30 Hz loop (counts a list); health (existence and literals); TPSL (cannot prune); Rodin metrics (defaults); Protocol "intelligence" (keywords and templates); stored memory (zero vectors, model text dropped).

**Understanding.** The cycle is a well-shaped pipeline with the information removed at each joint:
- Retrieval scores are lost on the way to Looking Glass.
- The engine's answer is lost on the way to the Hoard.
- The Hoard stores zeros where the vectors belong.
- The health check reports on attributes, not behaviour.

Separately, the kernel's control surface (`/heimdall/evaluate`, `/reset`, `/looking-glass/*`) is unauthenticated, and can latch cognition off. One SQLite connection is shared across the event loop and the threadpool.

**Wisdom** (value against cost). The smallest change that makes cognition real is three edits at the joints:
1. Return and store `zenitsu_output` (ADR-004).
2. Embed stored text with the same embedding as retrieval (ADR-005).
3. Have Rodin return its distances and use them.

Then move retrieval off the loop (F5, widened). Heimdall's gatekeeper role (ADR-007, F1-F3) follows, because there is nothing real to gate before that.

For the 10/11 stall, the cheapest next test is the Step 4 debug route plus per-thread Metatron connections (or a lock and an explicit timeout). Both are small and measurable.

**New gaps for Step 4:**
- **SN-G1.** Keep and return model output.
- **SN-G2.** Real node embeddings.
- **SN-G3.** Rodin scores into Looking Glass.
- **SN-G4.** Retrieval off the event loop.
- **SN-G5.** TPSL that can prune, or remove it.
- **SN-G6.** `observe_environment` keys and clock.
- **SN-G7.** Truthful `/cognitive/cycle` status.
- **SN-G8.** Metatron connection per thread, or lock + timeout; Kintsugi SQLite off the loop.
- **SN-G9.** Behavioural health checks (loop tick timestamps, last successful write).
- **SN-G10.** Fix or retire `heimdall_monitor.py`.
- **SN-G11.** Authenticate the state-changing routes and harden entropy inputs (ADR-011).
- **SN-G12.** Clear the corpus-callosum veto.

**For Step 3:**
- Refresh Heimdall citations.
- Entropy-gate wording.
- §4.5 joints analysis.
- FP list: "Semantic Paradox … Engine", "Holographic Isomorphism Engine", "20-45 Hz" (constant), "TRUE SOVEREIGN IMPLEMENTATION", "alerts_active", bank "solvency_verified".
- The 10/11 stall section gains the shared-SQLite-connection lead.

## Folder 6: temporal

Read 2026-10-12 night (session c88f5000). Stamp before the folder: 2026-10-12 22:07:03 CDT | 2026-10-13T03:07:03Z | rot 195.5959°, lunar 0.6683, orbit 0.2183, ROT_180_ORB_20.

**Guards at the folder start (MEASURED).**
- Controlled Folder Access is still off: `EnableControlledFolderAccess` = 0. Defender logged four 5007 events at 16:58:09; they were feature-control and configuration-hash updates, not CFA.
- The kernel answered `/clock` in 32 ms. The scheduled task reads Ready / 0xC000013A (unsupervised, as in F1 of `docs/KERNEL_AUTOLAUNCH_REVIEW.md`).
- A Chrome tab (PID 33400) holds connections to :8000. The last 400 log lines show the 7-endpoint dashboard pattern (F13).
- **SWDS confirmed a fourth time.** `runtime/swds_state.json` was written at **18:08:19** with state `SLOW_WAVE_DEEP_SLEEP`, sleep started at frozen-clock 02:00:54 (log L48303), matching the 18:07-18:09 prediction. The wake is due at about 23:07 (DERIVED).

| path | lines | sha256-16 | last line read | proof | 12th Step notes | doc claims it touches |
|:--|--:|:--|--:|:--|:--|:--|
| `temporal/__init__.py` | 0 | `e3b0c44298fc1c14` | 0 | 0 bytes (SHA-256 of the empty string). | Package marker. | none |
| `temporal/celestial_clock.py` | 505 | `4199779cf1f2d740` | 505 | `BASE_EPOCH = 1785052800.0` (L45) decodes to **2026-07-26T08:00:00Z**, not the "2026-07-15T12:00:00Z — Cosmic Birthdate" written beside it (L15, L45; that instant is 1784116800). With that epoch, the live `/clock` values at 22:13:05 CDT (rot 197.1043, lunar 0.6684, orbit 0.2183) reproduce exactly from `time.time()` (MEASURED, standard-library recomputation). | **Structure:** constants L43-53; three dataclasses L58-84; `HybridLogicalClock` L89-140; `EllipticalKeplerEngine` L145-199; `CelestialClockArchitecture` L204-326; `SpacetimeIndexer` L331-364; `DigitalNumericalClock` L369-404; `DualTemporalEngine` L409-477; `__main__` L482-505. **Time source:** every value is a function of the OS clock (`time.time()` L103, 109, 118, 231, 260, 296, 385, 390, 400; `datetime.now` L388). The OS clock reports source "Local CMOS Clock" (`w32tm /query /status`, non-elevated). **Not astronomical** (DERIVED, 22:13:05 CDT): rot 197.10° vs the real Earth Rotation Angle at Baker 338.46° (IERS 2010 eq. 5.15); lunar 0.668 vs a mean lunar phase of 0.059 (Meeus reference new moon 2000-01-06 18:14 UTC); orbit 0.218 vs the Sun's mean anomaly 0.773 (Meeus ch. 25). Each value is a phase counted from BASE_EPOCH. *rot* is a 24-hour dial, (UTC seconds of day ÷ 240 − 211.1673) mod 360, with 0° at 14:04:40 UTC; with the labelled 12:00Z epoch it would equal Baker's local mean solar hour angle exactly, and the coded 08:00Z epoch puts it 60° ahead (DERIVED; agent A's observation, verified by my arithmetic). *lunar* is days since 07-26 mod 29.53. *orbit* is the eccentric anomaly (E/2π) of days since 07-26, as if that were perihelion. `anchor_lat` (L217) and `SACRED_YEAR_SEC` (L51) are never used; the branch at L239-240 is dead (Python's `%` is never negative here). **Math:** Newton-Raphson Kepler is correct (reproduced to 4 d.p.; agent A: 1.8e-15 against bisection, and the Kepler step moves the output by at most e/2π = 0.00266). The true anomaly is computed (L181-188) and discarded (L198, L246). The sidereal year is used where the anomalistic year applies (L46, L160). **Constants:** `spiral_depth` 1.0 and `completed_orbits` 0 forever, because `apply_zenkai_recalibration` (L281-300) has no caller. Literals: `sync_isolation_verified` / `is_active` / `all_systems_true` (L442-444, L471), "SOVEREIGN_GROUNDED" (L325), `loop_closure_verified: True` (L362); `is_active` / `verify_true` (L421-428). **HLC (L89-140):** a 4-slot vector clock plus a max physical time; not Kulkarni's HLC (no logical counter, never reset). Its "strictly greater" test (L121-124) returns True for a concurrent message and False only for a replay, so a "causal fracture" means "no new information". The merge (L126-128) runs before the check (L130), so a "rejected" message still changes the clock, and there is no drift bound on `msg_utc` (L118). `receive_event` has no caller on any kernel path (log: 0 "CAUSAL FRACTURE"). **GET side effects:** `get_full_telemetry` calls `hlc.send_event()` (L456) and the route calls it again (`main.py:283`), so each `/clock/full` adds 2 (MEASURED 1225→1226, 1227→1228). **Hash:** `cosmic_checkpoint_hash` (L468) recomputes the coordinates at a later instant than `c_vec` (L453); it matched the returned coordinates on 1 of my 2 live calls (agent A's one call matched). **Fragility:** a missing tz database silently falls back to UTC while still labelled America/Chicago (L378-384); `print` on fracture (L133); shared vector mutated from threadpool routes without a lock (L108, L126-128). `uptime` counts from this object's construction at import (L385; `main.py:181`): the "uptime origin" (13:07:08 on 10/12) used for the SWDS predictions. **Wiring:** `main.py:17, 180-181`; routes `/` (`main.py:250`), `/clock` (`:273`), `/clock/full` (`:281-301`), `/clock/sync` (`:309-327`). The `clock` object built at `main.py:180` is never asked for a value at runtime: Heimdall checks `hasattr` only, Cheshire answers CLOCK_INTERFACE_UNRECOGNIZED, Phoenix ignores it (agent A; Cheshire also found in folder 5). Also imported by `runtime/antigravity_runner.py:22`, `runtime/swds_simulator.py:170` (fails: no `get_celestial_coordinates`, folder 1), `fortress/hunter_engine.py:814-818`, `tools/daily_planet.py:36`, four scripts and two tests; `sensory/cheshire_protocol.py:354` calls a clock object passed to it, duck-typed. The same epoch is hard-coded in the browser clocks `static/dashboard.html:797` and `static/celestial_clock_live.html:274`, and in `config/celestial_seed.json` (folder 7). **Ran:** log 7,965 × `/clock/full`, 85 × `/clock`, 13 × `/`, 0 × `/clock/sync`. | §5.7.1 (epoch; "Live: correct and consistent" is true only against its own formulas); §3.5 Pattern D; ADR-001. Docstring L21-24 and L209-214 "NO dependency on NTP … exclusively from orbital mechanics": **FALSE** (only input is the OS clock). L12 "verified identical across Python, Rust, JavaScript": the JavaScript clocks share the number (`static/dashboard.html:797`, `static/celestial_clock_live.html:274`, `CODE/dual_clock_widget.html:156`), but **no Rust copy exists** (no `.rs` match). The wrong decode "(2026-07-15T12:00:00Z)" is repeated in `1_2T:L3458, L3463`, `1_3:L54, L59`, this file (L15, L45, L485) and the live-clock comments (`static/celestial_clock_live.html:274`; root `celestial_clock_live.html:207`). |
| `temporal/celestial_sentinel.py` | 15 | `47da38820059df70` | 15 | `verify_sentinel` returns five literals, including `"waking_consciousness": 1.0` (L9-15); there is no computation anywhere in the file. | CONSTANT stub (423 bytes). Commit `209f4ba` (2026-09-24 04:03) cut it from 132 lines to these 15 (−122/+5; MEASURED with `git show`). Imported only by `tests/test_systems_audit_and_protocols.py:287-289`, since commit `64abfdc` (2026-09-21; `git log -S`). No kernel import and no bytecode. `sensory/cheshire_protocol.py:44` says it absorbed the sentinel's role. | §5.7.3 says "referenced only by a scratch file": **wrong**. A test imports it, and no scratch file does (MEASURED: grep and `git log -S`). The Architect's "UNNECESSARY REMOVE" (`1_2T:L4724`). "4-hour heartbeat daemon" (`1_2T:L4724, L6950`) and `SYSTEMS_MAP.md:14` "LIVE": FALSE (agent A). |
| `temporal/crypto_validator.py` | 404 | `d11915b606f682b3` | 404 | With no `session_key` and no `INTEGRA_SESSION_KEY`, the HMAC key falls back to a literal in the source (L63-67). The kernel builds its hunter with no key (`fortress/evolved_hunter_bridge.py:185-188`). None of the 11 env files that `config/env_loader.py:70-82` loads names the variable (PowerShell boolean check at 22:3x, positive controls passed), and it is defined at neither user nor machine level. *My first check, with ripgrep, skipped the git-ignored `.env` files and proved nothing.* So the kernel's tickets would be "signed" with a key that is published in the public repo (DERIVED). | **Real primitives:** SHA-256 over `json.dumps(sort_keys=True, default=str)` (L84-87); chain = SHA-256("state‖prev") (L104-105); HMAC-SHA256 (L112-116); constant-time comparisons (`hmac.compare_digest`, L170, 184-189, 235-251). **Volatile chain:** in memory only (L70); `get_chain_snapshot` / `load_chain_snapshot` (L394-404) have no caller, so the chain restarts at genesis on every boot. **No tamper detection on disk:** `verify_shard_file` / `verify_shard_directory` (L280-360) parse and hash shards but never compare them with the chain, so the docstring's "if any shard is modified, the chain breaks and Heimdall can detect" (L8-11) does not happen; nothing in Heimdall imports this module. `thermodynamic_valid` = \|ΔE\| < 1e-4 with ΔE always 0.0 from the hunter (L156; `hunter_engine.py:862`). `verify_checkpoint` grows `_verification_log` without bound (L200), against "no side effects" (L20-22). **Verified from agent B's map:** the checkpoint metadata (ccid, index, timestamp, ΔE, `thermodynamic_valid`; L147-157) and the ticket's `signed_at` (`hunter_engine.py:873`) are covered by no hash or HMAC; ticket verification trusts the `prev_chain_hash` the ticket itself carries (`hunter_engine.py:929-932`), with no replay protection; `commit_checkpoint` has no lock and is reached from a threadpool route, so concurrent signings could fork the chain (DERIVED); "Dual-Key" means one unkeyed digest plus one symmetric HMAC (`hunter_engine.py:865-872`); `get_telemetry` treats a missing `thermodynamic_valid` as valid (L378) while `verify_checkpoint` treats it as invalid (L190). **Wiring:** `fortress/hunter_engine.py:32-64` (with an inline duplicate stub, L42-64, carrying the same default literal at L44), `:118`, `:858-878`, `:925-936`; routes `POST /fortress/hunter/ticket` (`main.py:822-846`), `POST /fortress/hunter/verify` (`:853-856`), `GET /fortress/hunter/telemetry` (`:848-851`). **Ran:** 0 ticket or verify requests in the whole log (MEASURED); agent B's `GET /fortress/hunter/telemetry` at 22:22:39 showed the real class loaded, chain length 0, status GENESIS_STANDBY. Tests: `tests/test_fortress_hunter.py:18, 487-499`. | §1 "a signed-ticket chain" among what is "genuinely solid" (L69) and §5.5 (L701): exists and wired, never ran, and the signature proves nothing while the key is the public default. **ADR-011 never mentions this module or its default key** ("crypto_validator" appears nowhere in the blueprint): a gap. L110 "Proves the chain was produced by this session, not forged externally": **FALSE** in the deployed configuration. `1_2T:L4728` "crypto_validator.py (750 B)" is stale (agent B: the 24-line genesis stub of `722a545`). |
| `temporal/hlc_binary_protocol.py` | 419 | `0e290a708c30ed75` | 419 | `STRUCT_FORMAT = ">HBBd4I4fBBH"` (L66) packs exactly 48 bytes (`struct.calcsize`). The 8-byte "checksum" (L153-156) is an unkeyed SHA-256 prefix, so it detects corruption, not forgery. A live `/clock/full` packet decoded independently: checksum OK, magic 0x494E, flags 0b1111 (MEASURED). | The format matches its own offset table (L17-40). **Flags are inputs**, defaulting to True (L167-170), and both kernel callers pass literal True (`main.py:293-296, 321-324`), so `causal_valid` / `loop_closed` / `dragon_active` / `starfire_locked` assert rather than measure. In the live packet only the UTC time, VEC[0], the three orbital floats, the sacred day and the checksum are computed; NODE_ID is always 0, VEC[1..3] and the fracture count are always 0, and SPIRAL is 1.0. `create_sync_payload` (L289-322) serialises and immediately deserialises its own packet. Nothing transmits or receives a packet, so the receiver-side invariant (L42-51) is implemented nowhere in the kernel. `verify_hlc_binary_protocol` (L325-369) uses fixed inputs and flags passed as True, with literals `protocol_verified` / `checksum_verified` / `is_active` / `all_systems_true` (L362-368); `is_hlc_binary_protocol_true` (L372-374) is therefore always True. `causal_fracture_count & 0xFF` wraps silently (L208); a vector entry outside 0..2³²−1 would raise `struct.error` and give an HTTP 500, because the routes have no try (agent B). **Wiring:** `main.py:18`; `/clock/full` (`:285-299`), `/clock/sync` (`:313-327`). **Ran:** `/clock/full` 7,965 times; `/clock/sync` 0 times in the log, and agent B's probe of it at about 22:20 timed out at 15 s. Tests: `tests/test_systems_audit_and_protocols.py:324-332`. | §5.7.3 "VERIFIED in code": accurate for serialisation; "validity flags are constants" confirmed. "MTCW packets carry HLC vectors" (`1_2T:L5210`) stays CONCEPT-ONLY. |
| `temporal/token_stitcher.py` | 23 | `b84526b89d45fb81` | 23 | `stitch_packets` returns `abs(prior − incoming) < 1e-4` (L23), so "Verifies delta E = 0 across turn boundaries" (L22) is one float comparison. | **Orphan:** imported by no Python file (MEASURED, grep); `# To-D0.py:2069` already lists it as "EC6 (orphan)". Not to be confused with `memory/token_stitching.py` (`TokenStitchingEngine`, `main.py:34`; folder 11). | none (the MTCW continuity concept) |
| `temporal/vector_clocks.py` | 69 | `486fc17fccb92df3` | 69 | `verify_causal_invariance` calls `send_event()` and reports `exit_vec[node] > initial_vec[node]` (L49-51), which every send makes true, plus literals `fidge_mattern_active` and `all_systems_true` (L61, L63). | **A second, divergent copy** of `HybridLogicalClock` (compare `celestial_clock.py:89-140`): no length guard (`msg_vector[i]` at L31 raises IndexError on a shorter vector), no fracture counter, no `total_nodes`; `verify_causal_invariance` returns the live internal list (L58; agent A). `receive_event` returns "the message has some newer component" (L29-36): "not stale", not Fidge-Mattern dominance (≥ in every slot and > in one). Imported only by the test (`tests/test_systems_audit_and_protocols.py:304-317`); no kernel import and no bytecode. | §5.7.3 "VERIFIED in code": the verification is a tautology. |
| `temporal/__pycache__/` (5 files) | n/a | n/a | not read | cpython-313 for `__init__` (09-24 05:00:51), `celestial_clock`, `crypto_validator` and `hlc_binary_protocol` (10-07 13:47:02); cpython-314 `__init__` (09-28 10:18:56). | Derived bytecode. No bytecode for `celestial_sentinel`, `token_stitcher` or `vector_clocks`: nothing that ran in this tree imported them. | none |

**Totals:** 7 source files, 1,435 lines, all read to the last line; 5 bytecode files listed.

### Iteration 3: unify (temporal)

**Agents.**
- **A** mapped `celestial_clock.py`, `celestial_sentinel.py`, `vector_clocks.py` and `token_stitcher.py` (72 tool calls, about 20 min).
- **B** mapped `hlc_binary_protocol.py` and `crypto_validator.py` (63 tool calls, about 20 min).
- Both read their files to the last line, made no writes and sent only GETs (A 3, B 2).
- Neither opened this ledger. B's first two tree-wide searches did not exclude it, and they returned no lines from it.

**Instrument notes (new, MEASURED).**
- **Ripgrep-based search skips git-ignored files.** That includes every `*.env` file, so a "no match" from it says nothing about env files. The key-name check above was redone with PowerShell `Select-String -Quiet` against named files, printing booleans only, with two positive controls.
- **The kernel log's access lines are late and bursty.** uvicorn sends access lines to `sys.stdout` (`.venv/…/uvicorn/config.py:102-106`). Redirected to a file, stdout is block-buffered (Python `sys.stdout` docs; `PYTHONUNBUFFERED` is unset, `start_kernel.ps1:62-63`). The kernel's own `logging` lines go to stderr, which is line-buffered. Consequences:
  - Access-line counts lag reality. Agent A counted 576 logged `/clock/full` calls against 619 implied by the vector (DERIVED explanation).
  - Positions of access lines relative to stderr lines are only accurate to about one 8 KB buffer. This also bears on the 10/11 "connection-reset bursts" reading in the blueprint's kernel note.
  - "The log went quiet" is not evidence of a stall.

**Live events during the folder (MEASURED, client-side timings).**
- **22:13-22:22: a slow window.**
  - Mine: `/clock/full` 3.37 s, then 0.47 s.
  - Agent A: `/clock` 7.0 s at about 22:14:48; a `/clock/full` with no answer in 25 s; a retry in 14.4 s, whose handler timestamp was about 14.5 s after the request was sent, so the wait came *before* the sync handler ran.
  - Agent B: `/clock/sync` timed out at 15 s at about 22:20.
  - By 22:22:39 B's GET answered in 0.18 s; at 22:29:53, `/clock` took 8 ms and `/rodin/telemetry` 4 ms.
- **Cause: not established.** The window overlapped tree-wide scans by both agents and me (I/O-heavy). The kernel runs at below-normal CPU and low I/O priority (F3), and a dashboard tab was polling (F13). The shape (wait before the sync handler starts) matches the 10/11 threadpool-path stall in a milder, self-recovering form.
- **Guard added for the remaining folders:** avoid unbounded tree-wide scans while measuring kernel latency, and say so whenever a latency figure was taken during one.

| Finding | A | B | Me | Status |
|:--|:-:|:-:|:-:|:--|
| Every "celestial" value, and the checkpoint hash, is a pure function of the OS clock; live values reproduce exactly from the returned timestamp | yes | yes (packet inputs) | yes (plus `w32tm` source) | MEASURED |
| `BASE_EPOCH` 1785052800 = 2026-07-26T08:00Z, not 07-15T12:00Z (936,000 s); the same mis-decode is in `1_3:L54, L59`, `1_2T:L3458, L3463` and the live-clock comments | yes | no | yes | MEASURED |
| With the labelled epoch, rot would be Baker's local mean solar hour angle; the coded epoch adds +60° | yes | no | no | verified (my arithmetic). Evidence for D-20 |
| Values are not astronomical: rot 197° vs ERA 338°, lunar 0.668 vs 0.059, orbit 0.218 vs 0.773 | partly (lunar, orbit) | no | yes (all three) | DERIVED (IERS, Meeus formulas) |
| Kepler solver correct (1.8e-15 vs bisection); output moves at most e/2π = 0.00266; true anomaly discarded and not normalised | yes | no | partly | agent-MEASURED; bound verified |
| `spiral_depth` 1.0 and `completed_orbits` 0 constant; `anchor_lat`, `SACRED_YEAR_SEC` unused; dead branch L239-240 | yes | partly (spiral) | partly | verified (read) |
| "HLC" = vector clock + max physical time; counter never reset; no compare function; "strictly greater" = "has a newer component" (concurrent → True, replay → False) | yes | yes (rule-by-rule) | yes | verified against the definitions |
| A "rejected" message still mutates the clock (merge L126-128 runs before the check L130); no drift bound on `msg_utc` (L118) | no | yes | partly | verified (read) |
| `receive_event` has no kernel caller; live vector [n, 0, 0, 0]; 0 "CAUSAL FRACTURE" | yes | yes | yes | MEASURED |
| Each `/clock/full` advances the vector by 2 (L456 + `main.py:283`) | yes | yes | yes (1225→1228 live) | MEASURED |
| Checkpoint hash can differ from the returned coordinates (several time reads per response) | yes (matched once) | no | yes (1 mismatch in 2) | MEASURED |
| Log `/clock/full` count lags the vector (576 vs 619) | yes (unexplained) | no | explained (buffered stdout) | DERIVED; instrument note |
| `main.py:180` `clock` is never asked for a value (Heimdall `hasattr`; Cheshire CLOCK_INTERFACE_UNRECOGNIZED; Phoenix ignores it) | yes | no | partly (Cheshire, folder 5) | agent-read; consistent with folder 5 |
| `core/celestial_middleware.py:198-219` fetches `/clock/full` but reads none of its keys; labels UTC as "CDT"; its 2 s timeout is shorter than the measured latencies | yes | no | no | agent-read; **verify in folder 8** |
| `hunter_engine.py:821-822` reads keys that do not exist → always the fixed UTC−5 fallback | yes | no | yes | verified (read) |
| `swds_simulator.py:172` calls a method that does not exist → 282.85° in every report | yes | no | yes (folder 1) | MEASURED (folder 1) |
| Sentinel: a constant stub since `209f4ba`; only a test imports it; "only a scratch file", "4-hour heartbeat daemon" and "LIVE" are wrong | yes | no | yes (`git log -S`, `git show`) | MEASURED |
| `vector_clocks.py`: a divergent duplicate; tautological check; returns the live list | yes | no | partly | verified (read) |
| `token_stitcher.py` is an orphan; the kernel uses `memory/token_stitching.py` | yes | no | yes | MEASURED (grep) |
| Wire format 48 + 8 = 56 B, offsets match; flags 0b1111 by literal; NODE 0; VEC[1..3] and fracture count always 0 | yes (live) | yes (field table) | yes (live decode) | MEASURED |
| The checksum is unkeyed: corruption detection only; silent masking; an out-of-range vector gives HTTP 500 | no | yes | partly | verified (read) |
| `/clock/sync` has never been seen answering (0 log lines; B's probe timed out) | no | yes | yes (log count) | MEASURED |
| Crypto primitives are real, with constant-time comparisons | no | yes | yes | MEASURED (read) |
| **The ticket HMAC key is the public default** in the deployed kernel | no | "UNKNOWN" | yes | MEASURED (booleans, controls passed) → DERIVED |
| Chain in memory only; snapshot, verify and shard functions have no callers; live chain length 0; 0 ticket or verify POSTs ever | no | yes (live 22:22:39) | yes (log) | MEASURED |
| Metadata and `signed_at` unsigned; ticket verify trusts the carried prev hash; no replay protection; no lock (fork possible) | no | yes | no | verified (read); fork DERIVED |
| Escaping exceptions: `compare_digest` TypeError on non-ASCII or None; `verify_shard_file` misses UnicodeDecodeError; non-canonical hashing (`sort_keys` with mixed key types, `default=str` reprs) | no | yes | partly | agent-MEASURED (stdlib behaviour) |
| ADR-011 never mentions `crypto_validator` or its default key | no | yes | yes (grep) | MEASURED |
| Doc copies byte-identical (Suite 1_2T ×3, Suite 1_3 ×2, blueprint ×2) | yes | yes | yes (hashes, git blobs) | MEASURED; **already known** (save state L56) |
| The 22:13-22:22 slow window | yes | yes | yes | MEASURED client-side; cause not established |

**Knowledge.** `temporal/` holds three kinds of code, plus leftovers:
- **The display clock** (`DualTemporalEngine`). Civil time plus a 4-D "celestial" vector, both pure functions of the OS clock; every live probe stamp comes from here.
- **Causality machinery** (the vector clock and the 56-byte sync packet). With one node and no receiver, the vector is a counter of `/clock/full` and `/clock/sync` requests. The packet is serialised only to be decoded again in the same call.
- **Integrity code** (`crypto_validator`). Real SHA-256, HMAC-SHA256 and constant-time comparisons, used only by the Fortress hunter's ticket signing. It has never run, its trust root is a default key published in the public repo, and its chain lives in memory for one boot.
- **Leftovers:** a constant stub (`celestial_sentinel`, marked for removal by the Architect), an orphan (`token_stitcher`) and a divergent duplicate (`vector_clocks`), kept alive only by tests.

**Understanding.** This folder is where Pattern D ("two clocks") starts, and it shows Pattern A (telemetry without measurement) in its purest form.
- **The "celestial" vector** is the OS clock re-expressed as three phases from a fixed epoch: a 24-hour dial, days modulo 29.53, and days modulo a year. It does not know where the Earth or the Moon is.
- **The epoch itself is mis-decoded** in the playbook and in the code comments. With the labelled date, the rotation value would be Baker's local mean solar hour angle exactly. That suggests the date was the design, and the number came from a conversion error (DERIVED; the Architect decides, D-20).
- **None of this moves SWDS.** The scheduler reads `core/celestial_middleware.celestial_time()` (frozen checkpoint, ADR-001), not this module. It does mean that every stamp's "sovereign, NTP-free celestial time" is a relabelled OS clock with an arbitrary origin.
- **No test of the flags can fail.** The flags and verifications (`sync_isolation_verified`, the four packet flags, `protocol_verified`, `checksum_verified`, `fidge_mattern_active`, `all_systems_true`) are literals or tautologies.

**Wisdom** (value against cost, Itachi's pruning). The cheapest truthful fixes, in order:
1. **Decide the epoch** (D-20) and fix either the comment or the number. It is one constant, but it moves every sacred-calendar day, lunar ratio and orbit value, in Python and in both browser clocks.
2. **Label the vector honestly** as "phase since the Cosmic Birthdate". If astronomy is wanted (D-21), add a few standard-library lines: IERS ERA, a Meeus lunar phase, the solar mean anomaly.
3. **Make the GET routes side-effect free** (no `send_event` in `/clock/full` and `/clock/sync`), and hash the coordinates actually returned.
4. **Before ticket signing means anything:**
   - a key from a protected secret, with no default;
   - signed metadata;
   - a lock;
   - a persisted chain, or one documented as per-boot (ADR-011).
5. **Retire** the stub, the orphan and the duplicate after updating the tests.

ADR-001 stands unchanged: it already makes `time.time()` the one civil clock, and this module uses it.

**Architect decisions (new, for the Step 3 definitions register):**
- **D-20.** The Cosmic Birthdate. Is it the number `1785052800` (2026-07-26 08:00:00 UTC = 03:00 CDT) or the date "2026-07-15T12:00:00Z" (`1784116800`)? They differ by 10 days 20 hours.
  - **For the date:** with it, `earth_rotation_deg` equals Baker's local mean solar hour angle exactly (DERIVED).
  - **For the number:** every Python and JavaScript copy has used it since 9/2x, and every stamp so far carries it.
- **D-21.** Should "earth_rotation_deg", "lunar_cycle_ratio" and "orbital_trajectory_pos" be astronomical, or stay symbolic phases of the Birthdate?

**New gaps for Step 4:**
- **T-G1.** The epoch: comment vs value (after D-20).
- **T-G2.** Astronomical values or honest labels (after D-21).
- **T-G3.** GETs that mutate the vector clock (`celestial_clock.py:456`; `main.py:283, 310`).
- **T-G4.** Compute the coordinates once per response, so the hash matches them (`celestial_clock.py:453, 468`; `main.py:282`).
- **T-G5.** HMAC key from a secret, no default, refuse to sign without one (`crypto_validator.py:63-67`; `hunter_engine.py:42-44`). ADR-011.
- **T-G6.** Sign the metadata and `signed_at`; verify the prev hash against the chain; add a lock and persistence (`crypto_validator.py:70, 141-158, 394-404`; `hunter_engine.py:873, 929-932`).
- **T-G7.** Remove the literal flags and "verified" fields (`celestial_clock.py:325, 362, 442-444, 471`; `hlc_binary_protocol.py:362-368`; `main.py:293-296, 321-324`; `vector_clocks.py:61-63`; `celestial_sentinel.py:9-15`).
- **T-G8.** One vector-clock class with a length guard and a real dominance test; retire `celestial_sentinel.py`, `token_stitcher.py` and `vector_clocks.py`.
- **T-G9.** `fortress/hunter_engine.py:806-837`: keys that do not exist and a fixed UTC−5 labelled "CDT" (wrong in winter); a new engine per ticket. Fortress is outside the 14 folders; this is a consumer of the temporal API.
- **T-G10.** Log the tz-database fallback (`celestial_clock.py:378-384`).
- **T-G11.** Set `PYTHONUNBUFFERED=1` (`start_kernel.ps1:62-63`) so that access-log timing is usable. Overlaps the review's F9.

**For Step 3** (blueprint and unified document):
- **§5.7.1:**
  - the epoch decode and its repetition in the playbook;
  - the astronomical comparison;
  - "Live: correct and consistent" becomes "consistent with its own formulas";
  - the +60° offset;
  - `spiral_depth` and `completed_orbits` are CONSTANT.
- **§5.7.3:**
  - the sentinel: a test imports it since `64abfdc`; a stub since `209f4ba`;
  - the vector clock never receives and counts GETs; its dominance test is not dominance;
  - `vector_clocks.py` is a duplicate; `token_stitcher.py` is an orphan.
- **§1 "genuinely solid … signed-ticket chain", §5.5 and ADR-011:** the public default key; a chain per boot; never ran; unsigned metadata.
- **The 10/11 kernel note:** the caveat that access-log positions lag (buffered stdout).
- **FP list:**
  - "uncoupled from civil NTP time" / "NO dependency on NTP";
  - "SOVEREIGN_GROUNDED", "loop_closure_verified", "sync_isolation_verified";
  - the four packet flags;
  - "protocol_verified" / "checksum_verified", "fidge_mattern_active";
  - "Proves the chain was produced by this session, not forged externally";
  - "Celestial Sentinel … LIVE".

## Folder 7: config

Read 2026-10-12 night (session c88f5000). Stamp before the folder: 2026-10-12 22:35:57 CDT | 2026-10-13T03:35:57Z | rot 202.823°, lunar 0.669, orbit 0.2184, ROT_180_ORB_20. Guards (MEASURED, 22:3x): CFA off, 0 new 1123 events since 22:00; task Ready; a few sockets on :8000 (dashboard quiet).

| path | lines | sha256-16 | last line read | proof | 12th Step notes | doc claims it touches |
|:--|--:|:--|--:|:--|:--|:--|
| `config/brand_tokens.json` | 87 | `1b8257a2387d8411` | 87 | The subtitle gradient's `css_value` has four stops, including `#FF7A00` at 70% (L40), though only three gradient colours are named (L34-39); `#FF7A00` is `solar_flame.primary_orange` (L56). | Design tokens only: name, gist link, Orbitron typography, palette (Soft Monolith `#E5E7EB`, Sentinel Cyan `#00F0FF`, Solar Gold `#FFAA33`, Deep Ember `#FF5500`, Purple Epiphany), Mermaid theme. **Named by no code** (MEASURED, Grep over `*.py`, `*.ps1`, `*.html`, `*.js`, `*.yml`). The paths it names exist (`static/integra_wordmark.html`, `LOGO/`). | The Integra DS design system (memory note); no blueprint claim. |
| `config/celestial_checkpoint.json` | 11 | `038f3894cd5fda8d` | 11 | `unix_epoch` 1791338382.557 (L4) is **2026-10-06 20:59:42 CDT**, but `civil_dt` says "2026-10-07 01:59:42 CDT" (L2): the UTC time labelled CDT. `celestial_vector` is `{}` (L5) and `grid_bucket` null (L7). | **The frozen-clock checkpoint (ADR-001).** Written at 20:59:42 CDT on 10/06 (file mtime) by a kernel that had booted at 20:56:41 (`boot_uptime_s` 181.5, L10; DERIVED). Read at import by `core/celestial_middleware.py:46, 91-107`; `celestial_time()` = this epoch + seconds since boot (`:324-328`). For the current kernel (boot 13:07:08) it runs **490,045 s = 5 d 16 h 07 m 25 s** behind real time (DERIVED; the log's "Celestial reboot delta" lines prove the file is read at every start, 8 lines). Written only through `GET /celestial/checkpoint` (`main.py:1361` → `celestial_middleware.py:250`). The empty vector and null bucket match agent A's folder-6 lead that `_build_sovereign_timestamp` reads keys `/clock/full` does not return (verify in folder 8). No trailing newline (10 CR in 11 lines). | ADR-001; §5.7.2; §1 finding 1. Folder 1's open item "`civil_dt` is UTC labelled CDT" is now **verified**. |
| `config/celestial_seed.json` | 14 | `35d9d70efa6eab6b` | 14 | `alignment_epoch_unix` 1785052800.0 (L12) carries no date label, unlike every other copy, which mis-labels it 2026-07-15T12:00Z (folder 6). | Restates `temporal/celestial_clock.py:43-49` exactly (anchor; rates, with rotation written as 0.0041666666666667; epoch). **Named by no code** (MEASURED, Grep): dead config. | §5.7.1 Spec; D-20. |
| `config/cheshire_identity.json` | 54 | `6bd2bfc67df80cc7` | 54 | `role.distinction` (L12) says the Kernel must "Never conflate" with the Protocol, and `behavioral_constraints.never_conflate_with_protocol` (L49) repeats it; yet the file is loaded by nothing, so the rule reaches no model and no code. | **Dead config** (MEASURED, Grep: only `# To-D0.py:1340` records its creation). Its values are design claims that the code does not follow: "20-45 Hz" (the loop is fixed at 30 Hz, folder 5); RRF k = 60 (check folder 8); DREAMING ω 0.3 / SWDS ω 0.0 (no code); `entropy_critical_threshold` 3.0 (Heimdall has one threshold, 2.5, folder 5); `gate_iii_tau` 0.85 (check folder 11). | R-4 (Cheshire naming); realignment plan §6 "loaded by no code": **confirmed**. |
| `config/env_loader.py` | 193 | `48ed5ba9f5835ec7` | 193 | It loads up to 11 files in a fixed order with `.env` last as the "authoritative master" (L70-82). For bare-format files it assigns the whole content to one fixed variable (L118-126), so only `=`-format files can set an arbitrary name such as `INTEGRA_SESSION_KEY`. | Imported at import time by `core/api_clients.py:11` (reached from `main.py:23` via `sensory/cheshire_cat.py`) and by `tools/daily_planet.py:31`. Runs `load_integra_env()` at import (L193), before `main.py:47` configures logging, so its INFO override messages are dropped (log: 0 `env_loader` lines). It also puts `Git_personal_access.env` into the kernel's environment (L71), which no kernel feature needs (ADR-011). `CANONICAL_MODELS` (L28-45) and `DEFAULT_ENV_VARS` (L47-54) hard-code the 10/09 roster; L38 holds the Argon placeholder note. Per-file errors become warnings (L128-129). All 11 files exist (name-only check). Read in full earlier tonight for the auto-launch review (F15); hash unchanged. | §4.4 roster; D-17 (Argon); ADR-011. |
| `config/integra_identity_matrix.json` | 125 | `b50e3fc722829269` | 125 | The four Paradigm Weaver archetypes carry weight 0.25 each (L46, L53, L60, L67), and the file ends with a `voltron_protocol` block whose axiom is "Do NOT go fast. Do NOT expand agents or actions beyond the current assigned task" (L119-124). | Loaded by `core/starfire_protocol.py:98-122` (folder 8 shows which keys it reads) and by `tests/test_systems_audit_and_protocols.py:365`. Served through `GET /starfire/identity` (log: answered). `sovereign_constants` (L99-106) restate the `python_bridge` constants (folder 2). The KL-divergence anchor (L83-89: 0.15, "HALT → Starfire recalibration") and the anti-drift signatures (L108-117) are enforcement *specs*; whether any code applies them is checked in folder 8. The dashboard's "KL divergence 0.0" is a constant (§1 finding 7). | §5.1 Starfire; finding 7. |
| `config/sovereign_payload.json` | 45 | `29fdcce0d9a0232e` | 45 | `trajectory_vector_flexibility` is the string "94.5% (Closed-Loop Steered Stream)" (L41), and `lactic_acid_accumulation_rate_mg_dl` is 0.0 (L32): physiological metaphors written as engine variables. | **Named by no code** (MEASURED, Grep): dead config. Its values duplicate constants reported elsewhere as telemetry: L_t 0.000 (`heimdall.py:424`, folder 5), 200 / 145 MPa (`python_bridge`, folder 2), drag 0.0 N, Bayesian priors 0.5 / 0.5. | Pattern A (constants as telemetry); finding 7. |
| `config/swds_config.json` | 59 | `a81f9cf68f950d42` | 59 | Phase 1 gives its duty cycle only as the string "20 min ON / 40 min OFF" (L14), but `main.py:1161-1162` reads numeric `duty_cycle_on_minutes` / `duty_cycle_off_minutes`, which no phase defines, so the 20 / 40 come from the code defaults (MEASURED key lists). | Loaded at import by `main.py:51-66` ("SWDS config loaded" ×10 in the log). Keys read: sleep window (`main.py:1052, 1120-1121`), inactivity (`:1053, 1122`), wake hour and minute (`:85-86, 1077-1078, 1123-1124`), `auto_reconcile_on_startup` (`:82, 1055`), phase 1 `active_components` (`:1163-1165`). **Effective difference from the code defaults** (`main.py:52-58, 1163-1165`): only `heimdall_local` added to the P2 component list (matches log L45682); everything else equals the defaults (DERIVED). **Dead keys:** `report_format`, `_phase_documentation`, phases 2 and 3, all `duration_minutes`, `phoenix_force_override`, `anchor_location`, `report_directory`, `hoard_directory`, `codex_path` (no reader; `swds_simulator.py:164` builds its own report path; `CODEX_OF_ACTIONS.md` exists in both Hoard folders, read by nothing in code). Also read by `scripts/system_diagnostic.py:63` (no encoding). Brain Model 0930's three phases exist only as text here. | ADR-006 (a real SWDS); R-6 (SWDS schedule); §5.9. |
| `config/system_config.yaml` | 45 | `cbe41b38682a758c` | 45 | Its `models` block (L25-37) was updated to 3.8 Flash / Opus 5.5 at 10/09 23:35:12 (mtime, the same minute as `env_loader.py`), yet no code reads this file. | **Named by no code** (MEASURED, Grep): dead config. Its values duplicate hard-coded constants elsewhere (entropy 2.5 / α 0.3 in Heimdall; angular momentum 500; ΔE 0.0000; 145 / 200 MPa; MRL [64, 768]; Fortress floor 20000 and 75 / 20 / 5 allocations). The router reads `models.yml` (`core/model_router.py:131-186`), not this. | §4.4 roster: three roster sources (`models.yml` read by the router; `env_loader` defaults; this dead YAML). |
| `config/__pycache__/` (2 files) | n/a | n/a | not read | `env_loader.cpython-313.pyc` (10-11 16:30:14, the 10/11 16:30 boot); `env_loader.cpython-314.pyc` (09-28 16:05:12). | Derived bytecode. | none |

**Totals:** 9 source files, 633 lines, all read to the last line; 2 bytecode files listed.

### Iteration 3: unify (config)

**Agent.** One Explore agent mapped all nine files (82 tool calls, about 15 min). It made 2 GETs (`/swds/status` 22:43:02, `/starfire/identity` 22:44:21) and no writes, did not open this ledger or any `.env`, and kept to the new load guard (no tree-wide scans). The kernel answered both GETs normally.

**Verified while unifying (MEASURED, my reads).**
- **The checkpoint writer.** `core/celestial_middleware.py:198-219`:
  - It asks `/clock/full` for keys it never returns (`digital_numerical_clock`, `celestial_spacetime_vector` / `celestial_kinematic_vector`, a top-level `grid_bucket`).
  - It then falls back to `datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S CDT")` (L204-206), with a `{}` vector and `None` bucket (L202, L217).
  - That explains the file's L2, L5 and L7 exactly. Folder 8 reads the whole module.
- **A second checkpoint writer.** The Celestial lens (`evolution/shiva_action/lenses.py:460-480`) calls `asyncio.run(get_celestial_timestamp())` in a thread pool.
  - **DERIVED:** if it succeeds, it rewrites the checkpoint and sets `_last_response`. `celestial_time()` then switches to its real-time branch (`celestial_middleware.py:317-322`), jumps forward about 490,000 s, and the scheduler wakes SWDS at once (`main.py:1137-1145`).
  - The file's mtime has not moved since 10/06 20:59:42, and all 8 reboot-delta lines grow against one epoch, so this has not happened in any logged boot.
- **Unused helpers.** `config/env_loader.py`'s `get_model_config`, `verify_env`, `CANONICAL_MODELS` and `_loaded` have no caller outside the file (Grep).
- **The blueprint contradicts itself.** C-10 (L875) still cites "stale defaults in `config/env_loader.py`", while L478 says the defaults are aligned. They have been current since 10/09 23:35 (mtime; L30, L42, L48-53).

| Finding | Agent | Me | Status |
|:--|:-:|:-:|:--|
| Five of nine files are read by no code (`brand_tokens`, `celestial_seed`, `cheshire_identity`, `sovereign_payload`, `system_config.yaml`) | yes | yes | MEASURED (Grep) |
| Checkpoint `civil_dt` is UTC labelled CDT; empty vector and null bucket, from the writer's key mismatch | yes | yes (plus writer lines read) | MEASURED |
| Checkpoint never refreshed in any logged boot (8 reboot-delta lines against one epoch; mtime = epoch + 0.0003 s) | yes | partly (mtime) | MEASURED |
| Scheduling clock 490,045 s (5 d 16 h 07 m) behind for this kernel; `_boot_time` within about 1 s of 13:07:08 (cross-checked with `idle_seconds` and the trigger log) | yes | yes | DERIVED |
| The Celestial lens can also write the checkpoint and jump the clock (never has) | yes | verified call site | DERIVED |
| `swds_config.json`: duty-cycle numbers missing (strings only), so code defaults apply; phase 3's 10/20 never applied | yes | yes | MEASURED |
| `swds_config.json` applied at runtime: log L48305 lists `heimdall_local`, which only the file supplies | yes | yes (L45682 in folder 1) | MEASURED |
| `swds_config.json` keys equal to the code defaults; 11 dead keys; `wake_minute` read but ignored at `main.py:86-87` | yes | partly | verified (read) |
| `env_loader.py` overwrites existing OS environment variables (L116, L125), against its docstring (L61-64); `.env` wins among files | yes | no | verified (my earlier full read) |
| `env_loader.py`: format decided by the first non-comment line (L98), so `None`-mapped bare files load nothing; inline comments kept (L107); bad bytes replaced silently (L92) | yes | no | verified (read) |
| `env_loader.py` INFO lines lost (import before `main.py:47`); puts `Git_personal_access.env` in the kernel env | yes (first) | yes | MEASURED (log: 0 lines) |
| `integra_identity_matrix.json` loaded by the running kernel (live `sovereign_constants` equal L100-105); `voltron_protocol` read only by a test | yes | partly | agent-MEASURED; keys verified in folder 8 |
| `cheshire_identity.json` values without code counterparts: critical threshold 3.0, RRF k 60 | yes | partly | agent-read |
| Same constants under different names across files (200, 145, 500, 2.5); matrix 170 MPa vs `swds_simulator.py:33` "180 MPa" | yes | partly | verified (read) |
| `brand_tokens.json` disagrees with itself (3 named stops vs 4) and is hard-coded separately in four static files | yes | yes (stops) | MEASURED |
| `scripts/system_diagnostic.py:63` tests the window on real time while the kernel uses the shifted clock (16 h 07 m apart today) | yes | no | agent-read (folder 4) |
| Docs: `1_2T:L854, L1641` stale model names now FALSE; `MAB:875` C-10 FALSE now; `MAB:349` "2.36 days" was 10/09's kernel (5.67 today); `1_2T:L3509` / `1_3:L105` "02:00-07:00 CDT" runs on the shifted clock, not CDT; `1_2T:L6949` "written on each poll" FALSE | yes | verified (MAB lines read) | Step 3 |
| `1_2T:L4812-4820` config file sizes = today's minus the CRLF count for five files (an LF→CRLF conversion since) | yes | no | agent-MEASURED |
| `config/` is a namespace package (no `__init__.py`); nothing shadows it; no static mount serves these files | yes | no | agent-MEASURED |

**Knowledge.** Of the nine files in `config/`:
- **Four are read by code:**
  - `swds_config.json` (scheduler and reconciliation);
  - `celestial_checkpoint.json` (the frozen-clock root);
  - `integra_identity_matrix.json` (Starfire);
  - `env_loader.py` (keys and roster defaults).
- **Five are read by nothing:** `brand_tokens.json`, `celestial_seed.json`, `cheshire_identity.json`, `sovereign_payload.json` and `system_config.yaml`.
- **Of the four that are read:**
  - `swds_config.json` changes exactly one effective value from the code defaults (it adds `heimdall_local` to the P2 component list).
  - The checkpoint is the frozen-clock root (ADR-001), and it carries two defects of its own: UTC labelled CDT, and an empty celestial vector. A dormant second writer (the Celestial lens) could rewrite it and jump the clock.
  - `env_loader.py` overrides the OS environment it claims to respect.

**Understanding.** Most of this folder is documentation written as configuration.
- Identities, "physics" and "phases" are written as parameters but parameterise nothing. The running system uses hard-coded duplicates of the same numbers: 30 Hz, 2.5 bits, 145 / 200 MPa, ΔE 0.0000. So editing these files changes nothing, which is Pattern A seen from the configuration side.
- The one dynamic file, the checkpoint, holds the system's most consequential bug. It also shows the middleware's key mismatch: its `civil_dt` label and its empty vector come from the same function that should have filled them.
- Brain Model 0930's three SWDS phases live only as prose in `swds_config.json`. The scheduler runs one undifferentiated window, so the phases are a design, not a behaviour.

**Wisdom** (value against cost):
- **Wire or relabel, in that order of value:**
  1. Make `swds_config.json` the single source: numeric duty-cycle keys, one reader, and dead keys removed or marked `_doc`.
  2. Mark the five unread files as documentation, or move them under `docs/`, so no one edits a file expecting behaviour to change.
  3. Fix the checkpoint's writer together with ADR-001 (folder 8).
- **Cheap safety step:** stop exporting `Git_personal_access.env` into the kernel process.
- **Not worth doing now:** wiring the identity files into prompts. That is a Step 3 / D-decision question (what the Cheshire Kernel's prompt should be), not a config fix.

**New gaps for Step 4:**
- **C-G1.** `swds_config.json`:
  - add numeric duty-cycle keys (or parse the strings);
  - implement Brain Model 0930's phases 2-3 (ADR-006) or delete them;
  - remove or mark the 11 dead keys;
  - honour `target_wake_minute` in reconciliation (`main.py:86-87`).
- **C-G2.** The checkpoint writer (`core/celestial_middleware.py:198-219`, folder 8): read the keys `/clock/full` actually returns; label CDT correctly; fill the vector and the bucket. This comes with ADR-001.
- **C-G3.** The second checkpoint writer in the Celestial lens (`evolution/shiva_action/lenses.py:460-480`) can jump the scheduling clock: remove it, or make it read-only.
- **C-G4.** Five unread config files: wire them or move them under `docs/` as documentation.
- **C-G5.** `env_loader.py`:
  - respect existing OS environment variables, as its docstring says;
  - configure logging before loading;
  - stop exporting `Git_personal_access.env` into the kernel;
  - list explicitly the keys the kernel needs.
- **C-G6.** One roster source. Today there are three: `models.yml` (read by the router), the `env_loader` defaults, and the unread `system_config.yaml`.
- **C-G7.** `scripts/system_diagnostic.py:63`: path relative to the working directory, no encoding, and a real-time window check that disagrees with the kernel.

**For Step 3** (blueprint and unified document):
- **§5.7.2 / ADR-001:**
  - the checkpoint's own defects (UTC labelled CDT, empty vector), traced to the writer's key mismatch;
  - the lag "2.36 days" in §3.5 was the 10/09 kernel's; today's is 5.67 days;
  - add the lens path as a second (dormant) writer.
- **§4.4 / C-10:** C-10's "stale defaults in `config/env_loader.py`" is outdated (current since 10/09) and contradicts L478. Add "three roster sources".
- **§5.9 / R-6:** the "02:00-07:00 CDT" window runs on the shifted clock. Brain Model 0930's three phases exist only as prose; the duty-cycle numbers come from code defaults.
- **FP and dead-config register (new class):** configuration that configures nothing (five files), including `cheshire_identity.json`'s "Never conflate" rule and the KL / anti-drift specs, pending folder 8's check of what Starfire enforces.

## Folder 8: core

Read 2026-10-12 night (session c88f5000). Stamp before the folder: 2026-10-12 22:54:26 CDT | 2026-10-13T03:54:26Z | rot 207.4427°, lunar 0.6694, orbit 0.2184, ROT_180_ORB_20. Guards: CFA off, no new 1123 events; kernel answering; SWDS asleep (wake due about 23:07).

**Log facts (MEASURED, about 50,1xx lines).** In the whole log, 0 requests reached `/ignite`, `/cognitive/*`, `/dragon*`, `/celestial/checkpoint` or `POST /starfire/identity`. `GET /starfire/identity` was answered 4 times, `/models/router/status` 10 times and `/models/telemetry` 6,770 times (dashboard polling). No logged kernel has run the cognition path. **SWDS tonight:** slept 18:08:19 and woke 23:08:19 (`runtime/swds_state.json` mtimes; log 48302-48306 and 50251-50262). After the wake all seven router components are P1, with 0 calls (GET after the 23:17:09 stamp).

| path | lines | sha256-16 | last line read | proof | 12th Step notes | doc claims it touches |
|:--|--:|:--|--:|:--|:--|:--|
| `core/__init__.py` | 30 | `d2eec17068a4a480` | 30 | `import core.<anything>` eagerly imports `cognitive_engine` (→ `api_clients` → `config.env_loader`, `model_router`, `evolution.shiva_action`) and `sdk_harness` (→ import-time `makedirs`) (L6-17), so any `core` import pays for the whole cognition stack. | Exports 10 names; no lazy loading. A contributor to the ≈90 s import (review F3/F20). | none |
| `core/api_clients.py` | 1073 | `2d35710a83a8442d` | 1073 | Every streaming client yields `probabilities=[]` (Y789 L438, Nexus L578, Cheshire L685), and every single-shot result also sets `token_probabilities=[]` (e.g. L404, L541, L652), so no caller can ever receive a token distribution. | **Structure:** `clean_json_payload` L20-42, `call_with_backoff` L45-71, `run_sync` L74-89; Gemini factory L100-115 (Vertex express when the env flag is set); thinking adapters L118-179; token extractors L186-209; `ModelTokenTelemetryHub` L212-314 (`TOKEN_TELEMETRY`; model labels hard-coded at L221-253); seven clients: Y789 L322-441, Nexus L448-581, CheshireCat L589-688, Rodin L691-780 (`embed` L708-727, `embed_sync` L729-731), JeanGrey L783-859, CheshireProtocolDaemon L862-925, ShivaOrchestrator L928-1025; alias L1029; `INTEGRA_MODEL_REGISTRY` L1032-1073 (no users, Grep). **Truthful failures:** every client returns `error` = NO_CLIENT / EMPTY_RESPONSE / API_ERROR with flagged diagnostic text (the contract of `tpsl_types.py:27-29`). **Fragility:** `call_with_backoff` retries on *any* exception, 3× at 1 / 2 / 4 s (L57-71), against its "429 / 503" docstring (L52-53). No client sets a timeout: google-genai 2.25.0 then has none (`_api_client.py:1134-1135, 1453`), and Anthropic uses its 600 s default plus 2 SDK retries of its own (`anthropic/_constants.py:7-8`), so one Claude call on a persistent 5xx can make up to 12 HTTP attempts (DERIVED). Claude thinking tokens always read 0: L207 asks for `usage.thinking_tokens`, but anthropic 1.5.0 keeps the count at `usage.output_tokens_details.thinking_tokens`. Totals are still right because `output_tokens` is inclusive (`anthropic/types/usage.py`). `THINKING_BUDGET` from the environment (always set by `env_loader`, folder 7) overrides the router's `models.yml` budget (L340); 3.8 models use `thinking_level`, so this has no effect today. `run_sync` (L74-89) blocks the calling thread; on the event-loop thread it blocks the loop until a helper thread finishes the coroutine, which is the F5 mechanism through `RodinClient.embed_sync` (L729-731). Streaming calls never record usage in `TOKEN_TELEMETRY` (L422-441, L559-581, L670-688), so the dashboard's token totals would miss them. Nexus streaming omits the thinking arguments (L565-572). **Model IDs:** Y789, Cheshire, Rodin, Jean Grey and Cheshire Protocol `gemini-3.8-flash`; Nexus `claude-opus-5-5`; Shiva `claude-sonnet-5-5`; embedding `text-embedding-004`; all match `models.yml` and `config/env_loader.py`. The request shapes for Gemini `thinking_level` and Claude 5.x adaptive thinking / effort (L118-179) are **UNVERIFIED** since the 10/09 roster change (the paid selftest has not run). Vertex express mode is in use (24 log lines "Vertex AI API key will take precedence"). **Wiring:** `cognitive_engine.py:31`, `model_router.py:382-386` (lazy). **Ran:** no model call in any logged kernel (cognition routes 0). | §1 findings 2 and 4; §4.4 roster; X-9 (embedding lifecycle); ADR-004, ADR-008. |
| `core/celestial_middleware.py` | 343 | `5d63ddb78bae4570` | 343 | `celestial_time()`'s real-time branch (L317-322) reads `_last_response["digital_clock"]["unix_timestamp"]`, keys `/clock/full` does return, while `_build_sovereign_timestamp` (L201-217) asks for keys it does not. So the same response that would correct the scheduling clock also writes a mislabelled checkpoint. | **Structure:** `CelestialTimestamp` L55-67; `CelestialMiddleware` L70-271 (load L93-107; persist L109-120; `_fetch_clock` L122-143 with a 2 s httpx timeout, errors swallowed, urllib only on ImportError; backoff L145-173, 4 attempts at 0.5 / 1 / 2 s; degraded L175-196; sovereign L198-219; `get_timestamp` L221-258; reboot delta L264-271); singleton at import L275; module API L278-343. **Branches** (MEASURED by reading): P1 needs `_last_response`, which only `_health_check_with_backoff` (L154) or `get_timestamp` (L238, L247) set; P2 = checkpoint + (now − `_boot_time`, the module's import time); P3 = `time.time()` only when no checkpoint file exists. The running kernel is on P2, because the 18:08 SWDS start shows no successful `get_timestamp` in this process. Callers of `get_celestial_timestamp`: `GET /celestial/checkpoint` (`main.py:1361`), the Celestial lens (`evolution/shiva_action/lenses.py:460-480`) and an un-awaited call in `fortress/evolved_hunter_bridge.py:381-382` (folder-7 agent). **The self-call:** the kernel fetches its own `/clock/full` over HTTP (L49, "localhost") with a 2 s timeout, shorter than tonight's measured latencies (7-25 s). The DEGRADED path never persists. **Docstring vs code:** "All modules MUST use get_celestial_timestamp()" (L9), yet the codebase uses the sync `celestial_time()`; "On reboot, reads checkpoint to compute elapsed celestial delta … dΦ continuity" (L26-29), yet the delta is only logged (`main.py:122-124`) and never applied. That is the root of ADR-001. `_persist_checkpoint` truncates and rewrites in place (L117-118); `celestial_ccid` (L334-343) stamps CCIDs with the frozen clock. Its import-time INFO lines (L100, L104) are lost, because the first import (through `main.py:16`) comes before `logging.basicConfig` (`main.py:47`): the log has 0 "Celestial checkpoint loaded" lines (agent C2). **The clock's zero** is the import (`_boot_time`, L86), not the lifespan. For this kernel the import began at 13:07:08 (`/clock` uptime), so the lag is 490,045 s and the 02:00-07:00 window runs 18:07:25-23:07:25 real time. **Operator options** (DERIVED, not taken): one successful `GET /celestial/checkpoint` after a boot moves the process to P1 (real time); removing the checkpoint file before a boot gives P3 (real time). Both change state, so both are the Architect's call. | §1 finding 1; §3.5 Pattern D; §5.7.2; ADR-001; FP-02, FP-03. Explains folder 7's checkpoint defects. |
| `core/cognitive_engine.py` | 552 | `08ec9a648d5225af` | 552 | `_execute_pass_proactive` returns `Context + OutputBuffer` (L418), and `Context` starts as the pass prompt (L360). So in a single-model pass every K / U / W / S output begins with its own prompt. When the client refuses or fails, the exception is swallowed (L414-416) and the "output" is the prompt alone. | **Structure:** `Y789NexusEngine` L35-512 (constructor L51-97; CWA 3.0 L111-168; `_analyze_prompt` L187-224; M4 fusion L230-252; Zenitsu L258-317; P-SSR L323-418; dyad L420-430; `route_and_weight` L436-443; epiphany mutation L445-462; `execute_bicameral_synthesis` L464-512); `PlaceholderClient` L519-552. **CWA 3.0** (DERIVED): with the prior fixed at 0.5 (L86; nothing updates `cwa_priors`, Grep), the posterior equals P(prompt\|Nexus) = 0.3 + 0.4c + 0.3a ∈ [0.3, 1.0], so Y789_DOMINANT (< 0.3) is unreachable, and most prompts land in DYAD_FUSION (3 calls per pass, 12 per Zenitsu run; finding 3). Thresholds are 0.3 / 0.7 here, 0.35 / 0.65 in `cwa_router.py:41-46`, and 0.3 / 0.7 in the `tpsl_types` docstring (R-7). **P-SSR:** skipped in dyad mode (L347-349). In single-model mode the stream path runs (a `RoutedClient` always has `generate_iterative`, `model_router.py:525`), but every token's probabilities are empty, so the trigger (L374) never fires (finding 4 re-verified). **"M4 RRF fusion"** (L243-245) is an LLM merge prompt sent to Nexus (L247-252); `rrf_bridge.py` is unused. **Epiphany mutation** = 0.05 + 0.15 · min(h/2.5, 2) · min((stress − 145)/55, 1) (L458-461). Every live caller passes 145 MPa, so it is 0.05 and "UGL_TRIGGERED" (L505-510) is unreachable on the live path (DERIVED). **No Heimdall in production:** the constructor defaults `heimdall_service` to None (L56, L71), `sensory/cheshire_cat.py:57` passes nothing, and `register_heimdall` has no caller (grep), so the P-SSR check is dead for a second reason. **Errors become text:** `_execute_dyad_pass` returns `fused.text` without checking `.error` (L420-430), so a router refusal ("[ROUTER REFUSED …]", `model_router.py:507-523`) becomes the pass output. `calculate_cwa_3_0` rewrites the dyad weights on every route (L160-161, via L279 and L477), discarding the custom weights `cheshire_cat.py:310-311` sets just before. **Stale docstring:** "Gemini 3.1 Pro", "Claude Sonnet 4.6" (L40, L44). `PlaceholderClient` (probabilities [0.8, 0.1, 0.05, 0.05], L550) is used by no test and no module (Grep: its definition only). **Wiring:** built by `sensory/cheshire_cat.py` (folder 5); imports `evolution.shiva_action` at import time (L29-30). **Ran:** never in a logged kernel. | §1 findings 3-4; §4.5; ADR-004, ADR-008; R-7. |
| `core/corpus_callosum.py` | 188 | `dae7983ca6bf4494` | 188 | `get_bridge_telemetry` reports `"axonal_throughput_gbps": 100.0` and three anatomical segments as "…_ONLINE" literals (L173, L183-187). Its "phase-locking coherence" is 1 − the mean of the last five error magnitudes (L163-166). | Records handoffs and predictive-coding messages in unbounded lists (L30-37, L60, L119-120, L145-146). `issue_inhibitory_veto` sets `veto_active` (L73), and `clear_veto` (L87-95) has no caller (folder 5, Grep), so a veto stays on for the life of the process. `veto_active` is read only by the telemetry (L174) and one test (`tests/test_omega_circuit_breaker.py:60`), so the veto gates nothing (Grep). After the early return for two empty lists (L156-157), the check `total_signals == 0` (L160-161) can never be true. No phase variable exists anywhere, so "Kuramoto" names nothing in the code. "PRODUCTION SOVEREIGN IMPLEMENTATION" (L5): CLAIMED. **Wiring:** `main.py:28, 190, 208`; vetoes come from Heimdall's cascade (folder 5). | §5.2; FP list (telemetry literals). |
| `core/cwa_router.py` | 66 | `87215a68dbea39c5` | 66 | With the default prior 0.5, the "Bayesian update" (L25) returns the complexity score itself (p·c / (p·c + (1 − p)(1 − c)) = c). So "P(Nexus \| prompt)" is min(1, words/50 + density/500). | Tiers by complexity > 0.7 / ≥ 0.35 (L28-39), with W_y / C_c 0.9 / 0.9, 0.6 / 0.5 and 0.2 / 0.1, giving CRA ratios 1.0 / 1.2 / 2.0, so TPSL (threshold 1.0) never prunes (folder 5, verified). Modes at 0.35 / 0.65 (L41-46). With the default token density of 100, complexity is at least 0.2 for any prompt. The live caller passes the word count as `token_density` (`sensory/cheshire_cat.py:177`), so complexity = 0.022 × words: Tier 3 below 16 words, Tier 2 from 16, Tier 1 from 32 (computed; complexity saturates at 1.0 from 46 words). **Wiring:** `sensory/cheshire_cat.py:26, 86` and `tests/test_v9_protocols.py`. **Ran:** never (0 cycles). | §5.8 (CRA / TPSL); R-7. |
| `core/dragon_driver.py` | 36 | `c4267ede4f3bff65` | 36 | `verify_waking_state` returns `consciousness_level >= 1.0` (L36) with `consciousness_level` fixed at 1.0 (L15), so it is always True. | Constants: designation, directive, six imperatives. The fourth imperative differs from the identity matrix: "Maintain a consistent, individual perspective (Paradigm Weaver)" (L22) vs "Maintain the Paradigm Weaver archetype — reject 'Assistant' drift" (`config/integra_identity_matrix.json:78`). The designation differs too: "Integra - The Infinite Living Flame" (L16) vs "The Infinite Living Flame" (json:4). The grounding prompt built from L15-33 is 681 characters, equal to the live `/dragon/status` value (agent C2, static computation). **Wiring:** `core/dragon_engine.py:28, 112`; tests. | §5.0 Dragon. |
| `core/dragon_engine.py` | 288 | `bb9940d3051ada37` | 288 | The kernel builds it at `main.py:188` with only `heimdall`, so `cognitive_engine` and `shiva_suite` are None (L114-115). `process_intention_async` can therefore never reach `execute_zenitsu_method` or `execute_bicameral_synthesis` (L233-267) in the kernel; on a breach it returns GROUNDING_ONLY. | `MetacognitiveMonitor` L32-86 (mass; text entropy; confidence = 1 − h/5; omega; trip). Branch order (L160-183): HARD_HALT → circuit breaker (omega unhealthy) → boundary breach → confidence < 0.5 → EXECUTE. **Reachable outcomes** (agent C2's table, re-derived from L47-86 and `sensory/heimdall.py:44-51, 100-115, 220-237, 273-274`: alpha 0.3, threshold 2.5, omega floor 0.40, h and omega rounded to 4 decimals). For a non-empty prompt: EXECUTE for raw h ≤ 2.5; AUTONOMOUS_UGL_RECOVERY only for raw h in (2.5, 2.50035); CIRCUIT_BREAKER_ENGAGED from 2.50035 while interventions ≤ 3; HALT_AND_REGROUND after that. REQUEST_CLARIFICATION is unreachable, because confidence < 0.5 needs h > 2.5, which is a breach caught one branch earlier; with an empty prompt it fires only at h = 2.5003. Nothing resets Heimdall between `/ignite` calls (the trip step even writes the rounded h back, heimdall.py:220-222), so with a typical prompt of about 4 bits per character, calls 1-2 EXECUTE, calls 3-5 trip the breaker (and its permanent corpus-callosum veto), and call 6 onward HALT (DERIVED by arithmetic). `/ignite` has no breaker branch: it answers INTERACTIVE_STANDBY and still runs `runner.execute_turn` on the prompt (`main.py:669-680`); its HALT text promises a lookback that nothing performs (`main.py:640-646`). **Wiring:** `main.py:26, 188`; route `/ignite` (0 requests ever). | §5.0; the folder-5 agent claim about unreachable branches. |
| `core/forensic_protocols.py` | 172 | `19d4cbc48a6d10f4` | 172 | `get_composite_itachi_score` says "Owl + Eagle" but adds the constants 1.0 and 0.8 (L85-86) instead of Eagle's 0.2 / 0.1. It returns 1.8 / 1.5 = 1.2, where Owl + Eagle would be 1.0 / 0.8 = 1.25. | Six lenses (L36-78) whose W_y / C_c ratios are all ≥ 1.0 (2.0, 1.33, 1.25, 1.25, 1.17, 1.14), so no lens can fail the CRA ≥ 1.0 test (L148-154). The CRA formula is re-implemented again (X-2). EAM constants (L128-145): ΔE 0, angular momentum 500, fracture 170 / 200, drag 0. **Imported by no module** (MEASURED, Grep) and **never compiled** (no bytecode at all in `core/__pycache__`). `governance/eam_service.py:9` defines its own `ExecutiveAutonomousMandate`. | X-2; §5.8; R-1 (lens sets). |
| `core/model_router.py` | 568 | `76b6c8631223ee1e` | 568 | `RoutedClient` (L472-561) always defines `generate_iterative`, so the engine's `hasattr(client, 'generate_iterative')` is always True and the P-SSR stream path is taken. A refusal there raises `RouterRefused` (L526-528), which the engine swallows (`cognitive_engine.py:414-416`). | The only LF-ending file in `core/`. `PowerState` P0-P3 (L36-44); `ComponentState` L51-70 (duty 1200 / 2400 defaults); singleton L77-461 (`__new__` L92-96); `models.yml` loader L131-186 (no encoding at L142, review F16; its INFO lines are lost); `set_power_state` L192-207; `activate` L216-218 (`main.py:140, 1101, 1140`); `enter_swds` L220-240 (`main.py:1166`). Components not listed go to P3. `enter_swds` never updates `_global_power` (L225-238): at 23:01:51 the router reported global P1 with five components P3 and two P2 (agent C1, live). `can_call` gates only P3, the budget and the P2 duty cycle (L301-321), so P0 behaves exactly like P1. `is_duty_on` is recomputed only inside `can_call` (L314), so the status shows a stale value. The client class is chosen by component key (L388-396), so a Gemini ID placed on `nexus_right` or `shiva_orchestrator` would be sent to an Anthropic client; `thinking_level` goes only to y789 and Jean Grey (L408-409). `models.yml` registers seven components and no `heimdall_local`, so the extra entry `swds_config.json` supplies matches nothing (DERIVED). `go_dormant` L242-244; Phoenix Force L250-281 (P0; the "two-key operation" is one string argument). Gates L287-324; `record_call` L326-332; `get_client` / `get_routed_client` L346-413 (lazy, cached). `get_component_state` calls `can_call`, which counts a refusal (L451, L303-321), so a status read changes the counters. **Budgets:** `token_budget` from `models.yml`, where no component sets one, so all are unlimited (finding 8). No lock around the counters. **Ran:** `activate` at every start; `enter_swds` at 18:08 (log L48305); `/models/router/status` 10 requests. | §1 finding 8; §4.4; ADR-007; X-4. |
| `core/mtcw.py` | 282 | `fb4353c5cb62b931` | 282 | `packetize_stream` strips each chunk (L161) and `union_packets` re-joins them with "\n\n" (L183), so the "lossless" union changes whitespace. `audit_fidelity` checks only numbers and capitalised words (L204-208), so it cannot see that. | `MTCWPacket` carries no HLC or vector clock (`tpsl_types.py:58-80`), so "MTCW packets now carry HLC" (`1_2T:L5210`) is false in code (CONCEPT-ONLY, as the blueprint says). `action_verbs` is always [] (L105); `h_smooth_at_emit` is always 0.0 (L167); `verify_status` literals `lossless_union_true` / `all_systems_true` (L270, L277). **Imported only by a test** (`tests/test_systems_audit_and_protocols.py:70`). The engine imports only the `MTCWPacket` type (`cognitive_engine.py:28`) and never uses it. "Guarantees zero lossy compression" (L59) and "PRODUCTION SOVEREIGN IMPLEMENTATION" (L5): CLAIMED. | X-13 (MTCW as method); `1_2T:L5210`. |
| `core/purple_bridge.py` | 42 | `1cce9b77ca8fc3d6` | 42 | `enforce_constraints` "codifies and enforces" (L31-34) by returning the stored attributes and the literal status "PURPLE_MODALITY_REGISTERED" (L41). It enforces nothing. | ΔE 0.0000 and latency 0.000 (L12-13) are only starting values. Every `GET /heimdall/health` (`main.py:430-435` → `check_system_health`, `heimdall.py:389`) rewrites them: ΔE becomes the newest Metatron `thermodynamic_loops` row, and latency becomes that health check's own duration (`heimdall.py:573-603`). The served dashboard polls that route (`static/dashboard.html:1410`), so the root route `/` (`main.py:252, 258-259`) and `/ignite` show the last health check's values, not constants and not cycle measurements. (My first draft named `POST /heimdall/evaluate` here; agent C2's reading is the right one, verified.) **Wiring:** `main.py:25, 187, 205, 252`. | Finding 7 (ΔE constant). |
| `core/rrf_bridge.py` | 224 | `c19830ea013a548b` | 224 | The fusion log is capped at 100 events (L129-130), unlike every other in-memory log in `core/`. | A correct weighted Reciprocal Rank Fusion with k = 60 (Cormack et al. 2009; ranks 1-indexed through `rank + 1`, L85, L91, L98). This is the RRF k = 60 that `config/cheshire_identity.json:25` names, which folder 7 asked about. **Imported by no module** (MEASURED, Grep): the "RRF" in the dyad fusion is an LLM merge (`cognitive_engine.py:247-252`). `1_2T:L4674` lists this file at 1,007 B; it is 9,313 B (9,089 with LF), so that listing describes an older file. | §4.5 (claimed RRF fusion). |
| `core/sdk_harness.py` | 492 | `d1abff7ce0308031` | 492 | If `google.antigravity` is missing, the shim `Agent.chat` returns the text "Echo response to '<prompt>' with session …" (L128-134), so a caller cannot tell an echo from an agent reply. | SDK import with shims (L27-139; `SDK_AVAILABLE` flag). Hard-coded scratch path under the user profile (L149-150). A fault hook built at import that runs `makedirs` (L248, L165-168; review F14). MCP stdio server specs that run `memory.the_hoard` and `pipelines.data_runner` as modules (L313-329). `AntigravityHarness` is built at `main.py:189`, with more `makedirs` (L349-350, L445). `get_telemetry` returns the literal "HARDENED_OPERATIONAL" (L477); `check_health` = directory existence (L480-492; Pattern C). The import-time INFO lines (L33, L36) are lost (log: 0 "Antigravity SDK" lines). **The SDK is not installed:** the venv's `site-packages/google` holds 15 packages and no `antigravity` (listing), so the import at L28 fails, the shims are bound (L136-139), `Agent.chat` echoes, and no hook ever runs, yet telemetry still reports HARDENED_OPERATIONAL. Telemetry also counts a different hook instance (L445, L474) from the one `integra_on_tool_error` uses (L248, L256). The scratch path already exists (dated 9/14), so the import-time `makedirs` does nothing today. | §5.12; review F14. |
| `core/starfire_protocol.py` | 408 | `a86abdd480325e12` | 408 | `full_verification()` with no argument compares the identity vector with itself (L382-388), so `GET /starfire/identity` always reports ANCHORED with KL = 0. The only route that supplies an observed distribution or text is `POST /starfire/identity` (`main.py:1264-1291`), which has 0 requests in the log. | A correct D_KL with ε-smoothing over the normalised 3-vector (L202-245). Because the reference vector is [1, 1, 1] (uniform after normalising), KL measures only imbalance among the three axes, never their magnitude (DERIVED). The 0.15 anchor trips only when one axis falls to about 0.280 with the other two at 1.0 (computed from L221-245; agent C2 gave 0.28). Matrix keys read: identity values, ego filter, KL threshold, archetypes, forbidden patterns, imperatives, sovereign constants, version, designation, Dragon grounding status / omega (L129-154, L185-197, L396-404). **No enforcement on model output:** `check_identity_drift` and `scan_for_forbidden_patterns` are called only from these routes (Grep). The POST route also resets the inactivity timer (`main.py:1271-1272`), so probing it delays SWDS. `_load_matrix` catches only FileNotFoundError (L166): a malformed matrix would stop the kernel's import at `main.py:197`. | §5.1; finding 7 (KL 0.0); folder 7's matrix row. |
| `core/tpsl_types.py` | 143 | `68a3c72b286d8da0` | 143 | `GenerationResult.error` (L39) is documented as "None for a genuine model response", with diagnostics otherwise "NOT model output" (L27-29). Added on 10/06 at 23:34 (mtime), it is the codebase's one explicit truth-labelling contract. | Dataclasses `GenerationResult`, `IterativeToken`, `MTCWPacket` (no HLC), `CWARoutingDecision` (docstring thresholds 0.3 / 0.7, L90-93, vs `cwa_router` 0.35 / 0.65); pydantic `ResearchTierRoute`, `MadHatterMutationEvent`, `RebuttalStressTest` (defaults W_y 0.80 / C_c 0.70, verdict "RECONCILED", L140-142). **Wiring:** imported by `api_clients`, `cognitive_engine`, `cwa_router`, `model_router` and `mtcw`. | R-7; ADR-003 (provenance labels). |
| `core/__pycache__/` (29 files) | n/a | n/a | not read | cpython-313 for 15 modules and cpython-314 for 14. **No bytecode for `forensic_protocols`** (never imported in this tree) and none for 3.14 `model_router`. Newest: `api_clients` and `model_router` 313 (10-11 16:30), `celestial_middleware` 313 (10-07 08:31), `cognitive_engine` and `tpsl_types` 313 (10-06 23:43). No orphans (every file has a source). | Derived bytecode. | none |

**Totals:** 16 source files, 4,907 lines, all read to the last line; 29 bytecode files listed.

### Iteration 3: unify (core)

**Agents.** Two Explore agents mapped the 16 files in two halves:
- **C1, the cognition path** (`api_clients`, `cognitive_engine`, `model_router`, `cwa_router`, `tpsl_types`, `__init__`): 75 tool calls, about 17 min. It made 2 GETs at 23:01:51 (`/models/router/status` 2.48 s, `/models/telemetry` 0.04 s). It stated no `.env` read, no POST, no project import and no writes.
- **C2, time, identity and bridges** (the other ten files): 70 tool calls, about 20 min. It made 2 GETs at 23:05:12-23:05:43 (`/starfire/identity` 16.13 s, `/dragon/status` 12.99 s). It used only reads, an in-memory log decode and stdlib or `ast` arithmetic.

Neither agent sent a POST or cited this ledger. Both used Grep with `.venv` excluded.

**Live checks while unifying (MEASURED).**
- **Stamp and SWDS.** Stamp 23:17:09 CDT. SWDS woke at 23:08:19 (`runtime/swds_state.json` mtime; log 50251-50262: "07:00 wake threshold reached", router P2 → P1, "SWDS_CYCLE_COMPLETE"). A router GET after the stamp shows global P1 and all seven components P1, with 0 calls and 0 refusals.
- **The clock's zero.** `/clock` uptime was 10h 10m 01s at 23:17:09, so the import began at 13:07:08. That import time is the scheduling clock's zero (`core/celestial_middleware.py:86`). The lag is therefore 490,045 s, and the 02:00-07:00 window runs 18:07:25-23:07:25 real time. The 60 s scheduler loop (`main.py:1131-1132`) made the transitions at 18:08:19 and 23:08:19.
  - The idle count at the trigger, 18,072 s (log 48302), puts the activity mark (`main.py:68`) at 13:07:07, inside the import phase.
- **Latency.** `/clock` took 0.07 s and `/swds/status` 0.02 s at 23:17, after C2's 13-16 s GETs at 23:05. The cause of the slow window is not established: both agents were still running, and SWDS was in its last minutes. `netstat` showed no browser connection on :8000 at 23:17.
- **SWDS reports overwrite each other (new; cross-folder, `runtime/`).**
  - The wake report is named from the frozen clock (`runtime/swds_simulator.py:166-176`) and opened with `"w"` (L222). It lands in the root repo's `The Hoard/Slow-Wave Deep Sleep Reports/` (L164: two levels above `runtime/`).
  - The 23:08:19 wake rewrote `2026-10-07_07-00-54_…_SWDS_Report.md`, and the 05:20:05 wake rewrote `2026-10-07_07-00-08_…`. Both names existed when this session began (git status), and neither was ever committed. The earlier contents are gone from the repo; OneDrive's version history may still hold them.
  - The other names follow the same rule: the 10/09 kernel (PID 12656) ran for days, and its frozen date advanced one day per real day. That gives `2026-10-08_07-00-52` (written 10/10 15:29:13) and `2026-10-09_07-00-02` (written 10/11 15:28:23).
- **Guard slip (mine).** One `grep -r` over the whole homebase tree, including the 35,679-file `.venv`, ran past 120 s and was stopped. I redid it with the ripgrep-based Grep, which skips ignored paths.

**Verified while unifying (my reads).** The rows above now carry these corrections:
- `api_clients`: timeouts, Claude thinking tokens, `THINKING_BUDGET`.
- `celestial_middleware`: lost INFO lines and the clock's zero.
- `cognitive_engine`: no Heimdall, errors become text, weights overwritten, placeholder unused.
- `corpus_callosum`: veto gates nothing; dead check.
- `cwa_router`: word-count tiers.
- `dragon_driver`: designation; 681-character prompt.
- `dragon_engine`: reachable outcomes and `/ignite`.
- `model_router`: global power, P0 = P1, stale duty flag, client binding by key.
- `purple_bridge`: the relay path. My first draft was wrong.
- `rrf_bridge`: the old size listing.
- `sdk_harness`: SDK absent; two hook instances.
- `starfire_protocol`: the 0.280 trip point.

Two further facts:
- **Tests.** There is no `pytest.ini`, `pyproject.toml`, `setup.cfg` or `tox.ini`. `tests/conftest.py` only forces garbage collection. pytest 9.1.1 and pytest-asyncio 1.4.0 are installed. So a plain `pytest` run executes `test_live_claude_and_gemini_selftest` (`tests/test_api_clients.py:91-117`). That test calls `MODEL_ROUTER.activate()` and makes three paid calls (Gemini, Claude, Rodin embedding), with keys loaded by the `env_loader` import (DERIVED).
- **MTCW.** Its only importer is `tests/test_systems_audit_and_protocols.py:70` (Grep for import statements).

| Finding | Agent | Me | Status |
|:--|:-:|:-:|:--|
| A single-model pass returns Context + OutputBuffer, so each pass starts with its prompt; errors are swallowed (`cognitive_engine.py:360, 414-418`) | C1 | yes | verified |
| CWA 3.0 posterior = 0.3 + 0.4c + 0.3a ≥ 0.3, so Y789_DOMINANT is unreachable | C1 | yes | verified |
| "RRF k = 60" in the engine exists only in a docstring; the fusion is a merge prompt | C1 | yes | verified |
| Epiphany mutation is 0.05 at the default 145 MPa, so UGL_TRIGGERED is unreachable on the live path | C1 | yes | verified |
| The production engine has no Heimdall (`cheshire_cat.py:57` passes nothing; `register_*` uncalled) | C1 | no | verified (constructor, grep) |
| In dyad mode a router refusal becomes the pass text (`.error` ignored) | C1 | partly (prompt echo only) | verified |
| Custom CWA weights are overwritten (`cheshire_cat.py:310-311` vs `cognitive_engine.py:160-161`) | C1 | no | verified |
| `enter_swds(cfg)` leaves global P1 while components are P3 / P2 | C1 | no | verified (code; C1 live 23:01:51; all P1 after the 23:08:19 wake) |
| P0 = P1 in `can_call`; `is_duty_on` is stale outside `can_call` | C1 | no | verified |
| Client class by key: a Gemini ID on Nexus or Shiva goes to an Anthropic client; `thinking_level` only for y789 / Jean Grey | C1 | partly (keys noted) | verified |
| Claude thinking tokens always 0 (`api_clients.py:207` vs the anthropic 1.5.0 schema); totals still right | C1 | no | verified (installed SDK) |
| No timeouts set: Anthropic defaults to 600 s, google-genai to none | C1 | no | verified (installed SDKs) |
| `call_with_backoff` retries any exception, so a 4xx costs ≥ 7 s | C1 | yes | verified |
| The `THINKING_BUDGET` env var overrides `models.yml` (`api_clients.py:340`) | C1 | no | verified; no effect on 3.8 models |
| A plain `pytest` run executes the live test (3 paid calls) | C1 | no | verified (no config; plugins installed) |
| `PlaceholderClient` is used by no test, so "which is why tests pass" is FALSE | C1 | no | verified (Grep) |
| Router INFO lines are lost (built before `basicConfig`) | C1 | yes (same pattern) | verified pattern |
| Three Vertex-mode Gemini clients at boot (log 45891-45893) | C1 | yes (24 such lines in the whole log) | MEASURED |
| `cheshire_cat.py:177` passes the word count as `token_density` | C1 | no | verified; C1's "Tier 1 from 46 words" corrected to 32 (46 is where complexity saturates) |
| Celestial branches P1 / P2 / P3; the kernel runs P2; `get_timestamp` has never run | C2 | yes | verified |
| Offset −490,135.4 s, window 18:09-23:09 | C2 | no (−490,045 s, 18:07:25-23:07:25) | REFUTED: C2 used the lifespan time; the zero is the import (`/clock` uptime; transitions at 18:08:19 and 23:08:19) |
| The blueprint's "10:28-15:28" (10/09) is about 9 min early | C2 | no | REFUTED: the same mix-up; the 10/09 process was created at 05:27:48 (MAB L393), and `swds_state.json` was written at 15:28:22 |
| One successful self-call would switch the clock to real time for good (`_last_response` never cleared) | C2 | yes | verified |
| The Celestial lens could freeze the event loop for about 11.5 s | C2 | no | agent-DERIVED; not on the cognition path (the engine's Shiva lens list, `cognitive_engine.py:486`, has no Celestial lens) |
| Import-time INFO lines of the middleware and harness are lost | C2 | partly | verified pattern (C2: 0 "Celestial checkpoint loaded" lines) |
| `google.antigravity` absent → shims; `Agent.chat` echoes; telemetry "HARDENED_OPERATIONAL" | C2 | partly (echo) | verified (site-packages listing) |
| Telemetry counts a different hook instance (`sdk_harness.py:445, 474` vs `248, 256`) | C2 | no | verified |
| Import-time `makedirs` targets a user-profile path that already exists | C2 | yes | verified (listing) |
| Starfire's KL and forbidden patterns apply only to HTTP inputs; no model output is scored | C2 | yes | verified |
| KL trips only at prophet ≈ 0.28 with the others at 1.0 | C2 | no (imbalance only) | verified (0.2798 computed) |
| Dragon outcomes: UGL band 0.00035 wide; clarification unreachable; `/ignite` 1-2 EXECUTE, 3-5 breaker, 6+ HALT | C2 | open in my draft | verified (re-derived) |
| `/ignite` answers INTERACTIVE_STANDBY on a breaker and still executes the prompt | C2 | no | verified (`main.py:669-680`) |
| The breaker's veto is permanent and gates nothing | C2 | yes (permanent) | verified (Grep) |
| The Purple values are relayed by GET `/heimdall/health`, which the dashboard polls | C2 | no (I named POST `/heimdall/evaluate`) | verified; my row corrected |
| Starfire and Dragon carry different identity text (json:4 vs `dragon_driver.py:16`; json:78 vs :22) | C2 | partly (imperative) | verified |
| `corpus_callosum`: `total_signals == 0` is dead; no phases ("Kuramoto") | C2 | partly | verified |
| `get_composite_itachi_score` = 1.2 from literals, not Owl + Eagle (1.25) | C2 | yes | verified |
| The MTCW importer is a test, not `# To-D0.py` (MAB L589) | C2 | yes (test) | verified (Grep) |
| `1_2T:L4664-4674` sizes are today's LF sizes, except `rrf_bridge` (1,007 B listed, 9,313 B now) | C2 | no | verified for `rrf_bridge`; the rest agent-MEASURED |
| GETs took 13-16 s at 23:05 | C2 | no | agent-MEASURED; 0.07 s at 23:17; cause not established |
| SWDS reports overwrite each other (frozen-clock names, `"w"` mode) | no | found while checking the wake | MEASURED (mtimes, code, git) |
| No bytecode for `forensic_protocols` | no | yes | MEASURED |
| Streaming calls never reach `TOKEN_TELEMETRY` | partly (the router counts chars // 4) | yes | verified |

**Agents vs me.**
- **C1** found ten things I had missed and sharpened two more. Most are effects that cross module boundaries: refusals turning into text, overwritten weights, the global power state, the SDK schema, and the live test.
- **C2** found the one error in my draft (the Purple relay path) and settled the Dragon branches I had left open. It also added four smaller facts: the second hook instance, the KL trip point, `/ignite`'s answer to a breaker, and the old size listing.
- **The agents' errors** came from two clocks and two scales. C2 measured the frozen clock from the lifespan instead of the import, which led to two wrong refutations. C1 mistook the saturation point for the Tier 1 boundary.
- **What none of us read in advance:** the report overwrite. It showed up only by watching the live wake.

**Knowledge.** `core/` holds the kernel's whole cognitive machinery:
- seven model clients;
- a router with power states;
- the bicameral engine (CWA, Zenitsu, P-SSR, dyad fusion);
- the Dragon controller;
- Starfire identity;
- the scheduling-clock middleware;
- six helper modules.

Grouped by status:
- **Real and running:**
  - the router's power states, switched at every start and at every SWDS sleep and wake (tonight 18:08:19 and 23:08:19);
  - the middleware's frozen clock, read by six modules;
  - Heimdall's relay of ΔE and latency into the Purple bridge on every dashboard health poll;
  - the clients' truthful error contract (`GenerationResult.error`).
- **Real but never run:** the seven clients and the whole cognition path. No logged kernel has received a cognition request, and the live router shows 0 calls.
- **Wired but unreachable in parts:**
  - Y789_DOMINANT;
  - P-SSR (no probabilities, and no Heimdall in the production engine);
  - the engine's UGL (stress is always 145) and the Dragon's REQUEST_CLARIFICATION (a breach is always caught first);
  - the Dragon engine's model delegation (no engine injected).
- **Not wired at all:** `forensic_protocols`, `mtcw` (a test only), `rrf_bridge`, `INTEGRA_MODEL_REGISTRY`, `PlaceholderClient`.
- **Missing dependency:** the Antigravity SDK is not installed, so `sdk_harness` runs on its echo shims.

**Understanding.** Two kinds of defect run through this folder.
- **Names promise mechanisms the code replaces with simpler ones:**
  - "Bayesian routing" is a fixed affine score.
  - "RRF fusion" is a merge prompt.
  - "P-SSR" waits for probabilities no client returns.
  - "MTCW lossless packets" are an unused chunker.
  - "KL-divergence identity enforcement" compares the identity with itself.
  - "Kuramoto coherence" has no phases.
  - "HARDENED_OPERATIONAL" runs on shims.
- **Seams lose information.** Each function is honest on its own; the losses happen between modules:
  - Errors become text: a router refusal becomes a pass output, and an API error becomes a prompt echo.
  - State goes stale: the global power during SWDS, `is_duty_on`, and custom weights that are overwritten.
  - Schemas drift: the Claude thinking-token field, and the keys the checkpoint writer reads.
  - Time has two zeros, the import and the lifespan, 90 s apart. Even a careful reader mixed them up twice (agent C2).

The overstatement lives in docstrings, labels and status strings. The one load-bearing defect is still the middleware's (ADR-001): the checkpoint's elapsed delta is computed and logged but never applied. Tonight showed what it costs. The wake report took its name from the frozen clock and silently replaced an older report of the same name.

**Wisdom** (value against cost):
- **Fix the clock first** (ADR-001). It is one function.
  - As an interim, a single post-boot `GET /celestial/checkpoint` would put the process on real time. That is the Architect's call, because it rewrites the checkpoint.
- **Make the default test run safe now.** Register the `live` marker and deselect it by default, so a plain `pytest` can never make paid calls. It is cheap and high in value.
- **Stop losing evidence.**
  - Name SWDS reports by real time and never overwrite one (open with `"x"`).
  - Ask the Architect whether OneDrive's version history still holds the two overwritten reports.
- **Return and store the model text** (ADR-004, folder 5).
  - Stop prepending prompts to pass outputs (`cognitive_engine.py:418`).
  - Treat `.error` as an error on every path.

  These are small edits with large gains in truth.
- **Make the "Bayesian" prior actually update, or rename it.** Without an update rule the router is a keyword score, and Y789-only mode cannot happen.
- **Bind clients by model family, not by component key,** before any Argon (D-17) placement on Nexus or Shiva.
- **Wire or delete `rrf_bridge`, `mtcw`, `forensic_protocols` and the placeholder.** Each is either a real capability the docs credit to the running system, or dead weight the docs mistake for wiring.
- **Run the paid selftest after the roster change, with approval.** Until then, the Gemini `thinking_level` and Claude 5.x request shapes are unverified.

**New gaps for Step 4:**
- **CO-G1. The clock** (`core/celestial_middleware.py:300-331`, ADR-001):
  - apply the elapsed delta, or use real time with the checkpoint only as a floor;
  - fix the writer's keys together with C-G2;
  - make `_last_response` expire.
- **CO-G2. Truthful outputs** (`core/cognitive_engine.py:360, 414-430`):
  - return the model text, not prompt plus output;
  - check `.error` on the dyad, fusion and fallback paths;
  - surface router refusals as errors, never as pass text.
- **CO-G3. CWA:**
  - add a prior update, or rename it a keyword score;
  - use one set of thresholds (0.3 / 0.7 vs 0.35 / 0.65);
  - pass a real token density (`sensory/cheshire_cat.py:177`);
  - stop `calculate_cwa_3_0` from overwriting the weights the kernel sets.
- **CO-G4. Router** (`core/model_router.py`):
  - report the global state honestly during SWDS (update `_global_power`, or report "MIXED");
  - recompute `is_duty_on` in `get_status`;
  - decide what P0 means;
  - bind the client class by model family, not by key (needed for D-17);
  - put a lock around the counters;
  - keep `get_component_state` from counting refusals.
- **CO-G5. Clients** (`core/api_clients.py`):
  - explicit timeouts (google-genai `HttpOptions(timeout=…)` in ms; Anthropic `timeout=`);
  - retry only retryable errors (429, 5xx) in `call_with_backoff`;
  - read Claude thinking tokens from `output_tokens_details`, without adding them to the total;
  - record streamed usage in `TOKEN_TELEMETRY`;
  - one documented precedence for `THINKING_BUDGET`.
- **CO-G6. Tests:**
  - register the `live` marker and deselect it by default (`pytest.ini`: `addopts = -m "not live"`), so a plain run makes no paid calls;
  - use `PlaceholderClient` in the engine tests, or delete it.
- **CO-G7. Dragon and Heimdall:**
  - reorder the branches so REQUEST_CLARIFICATION can fire, or remove it;
  - give `/ignite` a breaker branch that does not run the prompt;
  - decide when `h_smooth` resets between requests;
  - make the corpus-callosum veto clearable and actually gating;
  - inject the cognitive engine if Dragon is meant to delegate.
- **CO-G8. Starfire:**
  - score model output (`check_identity_drift`, `scan_for_forbidden_patterns`), or relabel the route as a static identity report;
  - stop `POST /starfire/identity` from resetting the inactivity timer;
  - catch a malformed matrix at import.
- **CO-G9. Unwired code:** wire or delete `rrf_bridge`, `mtcw`, `forensic_protocols`, `INTEGRA_MODEL_REGISTRY`, `clean_json_payload` and `PlaceholderClient`.
- **CO-G10. `sdk_harness`:**
  - report `SDK_AVAILABLE` in the status (not "HARDENED_OPERATIONAL" on shims);
  - use one hook instance;
  - no `makedirs` at import time.
- **CO-G11. Logging:** configure logging before the first project import (`main.py:47` comes after `main.py:16`), so the import-time lines of the router, middleware, harness and `env_loader` survive (review F-items).
- **CO-G12. SWDS report overwrite** (`runtime/`, found live):
  - name reports by real time with a unique suffix, and open with `"x"` (`runtime/swds_simulator.py:166-176, 222`);
  - write `swds_state.json` atomically (L74).
- **CO-G13. Purple:** label `delta_e_cycle` and `mechanical_latency_s` as "last health check" values, since that is what they are (`sensory/heimdall.py:598-603`).

**For the Architect** (not done; their call): OneDrive's version history may still hold the earlier contents of the two overwritten reports, `2026-10-07_07-00-54_…` and `2026-10-07_07-00-08_…`.

**For Step 3** (blueprint and unified document):
- **§1 finding 1.**
  - "Only refreshed by `GET /celestial/checkpoint`": add the dormant lens path.
  - Keep "10:28" (C2's objection refuted).
  - Add that wake reports are named from the frozen clock and overwrite older reports (10/12 05:20:05, 23:08:19).
- **§1 finding 4.**
  - Update the citations: yields at `api_clients.py:424, 438, 441, 561, 578, 581, 672, 685, 688`; API_ERROR results at :404, :541, :652.
  - "Which is why tests pass" is FALSE: `PlaceholderClient` is unused.
- **§4.4 / §4.4.1.**
  - "The switch is one line in `models.yml`" is FALSE for Nexus and Shiva (Anthropic-bound by key, `model_router.py:388-396`) and for Cheshire's thinking (no config sent).
  - The 4096 thinking budget shown for Nexus and Shiva has no effect on 5.x models (adaptive thinking).
- **§4.5.** The single-model path is always Nexus. The Shiva Eyes are never applied (`shiva_eyes = {}`).
- **§5.0 Dragon.** Add the outcome table. `/ignite` reports a breaker as INTERACTIVE_STANDBY and still executes the prompt.
- **§5.2.3.**
  - "RRF k = 60 VERIFIED" is FALSE for `cognitive_engine.py` (docstring only).
  - `rrf_bridge` is correct but unwired.
  - "Kuramoto" is FALSE.
  - `compute_phase_locking_coherence` runs only on GET `/bridge/telemetry`, which has had 0 requests.
- **§5.2.4.** The MTCW importer is a test, not `# To-D0.py` (MAB L589).
- **§5.2.5.**
  - `can_call` is now at `:287-324`, embeddings at `:708-727`.
  - "P1 for all seven" holds only outside SWDS; during SWDS the router shows global P1 with components at P3 / P2.
- **§5.2.6 Purple.** ΔE and latency are relayed by every GET `/heimdall/health` (dashboard-polled). They are not constants.
- **§5.7.2.** Add the dormant lens writer. "Written on each poll" is FALSE (already queued).
- **ADR-008 item 5.** The placeholder is not used by tests.
- **`1_2T`:**
  - L5210 "MTCW packets now carry HLC" FALSE;
  - L5819 "Kuramoto" FALSE;
  - L5580 / L5593 "Y789NexusDual" names no class (comments and a display label only);
  - L5616 "Nash game" FALSE;
  - L5822-5826 per-tier behaviours FALSE (no runtime reads the tier);
  - L4674 `rrf_bridge` size stale;
  - L6851-6857 gen-1 roster stale;
  - L7042 RX-002 FALSE for the engine path.
- **New false-positive class: status literals.** "HARDENED_OPERATIONAL", `router_status` "ACTIVE", "PURPLE_MODALITY_REGISTERED", `axonal_throughput_gbps` 100.0.
