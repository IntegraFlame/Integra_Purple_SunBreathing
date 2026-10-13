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
