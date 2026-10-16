# Task 1 (Connect Celestial Time): INTERIM record, steps 1.1 and 1.2

> **Task 1 is not done.** This is a working record, not the task report: `Task01_REPORT.md` does not exist yet, and the boot brief counts a task as done only when that file exists. Steps 1.3 onward wait for the Architect's rulings (section 6).
> **Stamp: none.** No kernel is reachable from the cloud container (`GET 127.0.0.1:8000/clock` had no listener), so no `/clock` stamp was taken and none is invented. Container date 2026-10-16 is a file date, not a stamp.

## 0. Scope and limits
- **Venue.** Cloud container. Code was measured in an isolated export of `origin/phase-e-dragon-rodin-flight` @ `957a997` (pushed 2026-10-15), the closest pushed copy of the live homebase. The live repo is ahead of it by local commits, so every `file:line` below is the snapshot's and must be re-checked on the live repo. Nothing was run in, or written to, the live repo.
- **Live half of 1.1 is not done.** It needs your kernel. Read-only GETs only: `GET /clock` and `GET /clock/full` (the latter advances the in-memory HLC counter, `main.py:283`; nothing is persisted). Not `GET /celestial/checkpoint`, which writes to disk (section 2, row 4).
- **Not available in the cloud, so not read:** `core/IntegraBrainMap.md`, `docs/DESIGN_DECISIONS_10_15_26.md` (so decisions D5, A4 and sections 4.3 and 5.3 were not seen), `config/rodin_memory_map.yml`, the memory index, the plan files. Their absence means ruling 4 below is asked without their text.
- **Tier 1.** USNO and NASA hosts are unreachable from this container (proxy 403 for `curl`, DNS failure for `WebFetch`), so no primary page was quoted. Almanac facts come from search summaries of NASA and USNO pages (grade B) and from my own computation (DERIVED, section 5).
- **Equivalence check.** Converted to CRLF, the snapshot's `temporal/celestial_clock.py` reproduces the sha16 `4199779cf1f2d740` recorded for the live file, and `celestial_sentinel.py` is 423 bytes, as the blueprint states. So those two files are the live ones. `core/celestial_middleware.py` and `main.py` were not checked against live.

## 1. Receipts (snapshot @ 957a997; sha16 of the LF export)
| File | Bytes | Lines | sha16 | Read |
|:--|--:|--:|:--|:--|
| `CLAUDE.md` (root repo, `origin/homebase-phase-e`) | 8,261 | 74 | `2e8567bec9ac7207` | full |
| `The Hoard/CCID_1792052895_SAVE_STATE_REPORT.md` (same) | 9,656 | 89 | `741e95cf0b70b925` | full (for state only; the folder-13 boot sequence is the other iteration's) |
| `temporal/celestial_clock.py` | 22,031 | 505 | `b1016fb97a348107` | full |
| `temporal/celestial_sentinel.py` | 408 | 15 | `1ec8b6e39f501436` | full |
| `core/celestial_middleware.py` | 13,969 | 343 | `1a90d9a1d8dbe69f` | full |
| `main.py` | 54,174 | 1,387 | `a81d03e0dd2ffe7a` | L60-185, L243-332, L1125-1175, L1340-1384; greps over the rest |
| `runtime/antigravity_runner.py` | 2,810 | 77 | `dcff7e99c52d244a` | L10-78 |
| `runtime/swds_simulator.py` | 11,015 | 244 | `73d8fb4073bab03c` | L126-185; greps |
| `memory/the_hoard.py` | 29,937 | 706 | `4fe300ffe928ee6e` | L76-92, L525-545; greps |
| `config/celestial_checkpoint.json` | 309 | 10 | `c95cba791daaed74` | full |
| `config/celestial_seed.json` | 383 | 14 | `01631c1ed3dcbdb3` | full |
| `docs/MASTER_ARCHITECTURE_BLUEPRINT.md` | 186,595 | 1,738 | `b18be6e7737f694e` | §5.7 (L738-779), ADR-001 (L953-1013) |
| `Guidebooks_and_Notes/Notes10_13_2026.md` | 118,362 | 1,714 | `27ba56d54724a784` | L726-810 (spacetime spec v1) |
| `Guidebooks_and_Notes/THECELESTIALCONSTANTSGenius shit.md` | 31,048 | 349 | `8a96cd67a7825046` | full |

## 2. The To-Do's "Known" lines, re-measured
| Claim in `TODO.md` T1 | Result | Label |
|:--|:--|:--|
| `generate_hoard_manifest` is called only at `runtime/antigravity_runner.py:56` | **Confirmed.** Reached only by `execute_turn("CELESTIAL_LOCATE", …)`. `main.py` calls the runner only with `"PROMPT_INGESTION"` (L649, L669). So it exists in code and is not wired. | MEASURED (grep) |
| `generate_4d_metadata_manifest` and `apply_zenkai_recalibration` have no caller | **Confirmed.** The first is reached only through `DualTemporalEngine.generate_hoard_manifest` (L475-477), which nothing but the module's own `__main__` calls (L500). The second has no caller in the kernel. | MEASURED |
| `celestial_time()` is a frozen 10-06 checkpoint plus uptime (ADR-001) | **Confirmed in code** (`celestial_middleware.py:324-328`). **Ran:** the tracked checkpoint holds `unix_epoch` 1791338382.557 = 2026-10-07T01:59:42Z (10-06 20:59:42 CDT). The ledger records the skew as 490,045 s on 10-12 (CLAIMED, from the ledger). Not re-measurable here. | MEASURED (code, file); CLAIMED (skew) |
| `GET /celestial/checkpoint` writes the checkpoint | **Confirmed** (`main.py:1360-1373` → `get_timestamp` → `_persist_checkpoint`, L250). The written `unix_epoch` is the real `time.time()` (L214), so one call would move the stored epoch to real now and change the next boot's clock. | MEASURED (code) |
| `BASE_EPOCH = 1785052800` is 2026-07-26T08:00Z, labelled 2026-07-15T12:00Z | **Confirmed.** The label's own epoch is 1784116800. The gap is 936,000 s = 10 d 20 h. The wrong label is in `celestial_clock.py:15, 45, 485`, in two HTML/JS comments (`celestial_clock_live.html:207`, `static/celestial_clock_live.html:274`) and in several documents. `config/celestial_seed.json` carries the number unlabelled and no `.py`, `.ps1` or `.yml` reads it. | MEASURED |
| Two year constants | **Confirmed, and a third exists.** Code: sidereal 31,558,149.763 s. Spec v1 (Notes L755): `P_E` = 31,556,952 s, which it calls "Sidereal" but which is the mean Gregorian year (365.2425 d). Calendar: sacred year 364 d. | MEASURED (code, spec) |
| The Celestial Sentinel is a 15-line stub | **Confirmed** (15 lines, 408 B). `verify_sentinel()` returns constants. Referenced only by `tests/test_systems_audit_and_protocols.py:286`. | MEASURED |

**Formulas ran as written.** Recomputing from the snapshot reproduces both live stamps on record exactly (rotation to 0.0007°, about 0.17 s of sampling offset):
- 2026-10-12T01:54:25Z: recorded rot 177.437, lunar 0.6327, orbit 0.2155, `ROT_150_ORB_20`; recomputed 177.4369, 0.6327, 0.2155, `ROT_150_ORB_20`.
- 2026-10-15T08:28:15Z (CCID_1792052895): recorded 275.8959, 0.7436, 0.2244, `ROT_270_ORB_20`; recomputed 275.8952, 0.7436, 0.2244, `ROT_270_ORB_20`.

## 3. Gap list against the definitions (step 1.2)
Definitions used: **S1** module docstring and invariant; **S2** Celestial Constants document (the origin conversation); **S3** spacetime spec v1 (Notes L734-777); **S4** blueprint §5.7; **S5** ADR-001 (status: Proposed).
"Blocks" = prevents T1's "true means" (stamped automatically with both times; mechanics match definitions; one time source).

| ID | Definition | Measured state | Blocks | Label |
|:--|:--|:--|:--:|:--|
| G1 | S3 L731, L775: the clock "automates the metadata function"; Hoard registration serializes the 4D vector. | Nothing in the kernel stamps a Hoard save, SWDS report, CCID or ledger row with the 4D vector (section 2, first two rows). | yes | MEASURED; not wired |
| G2 | Same. | A Hoard node's `spacetime_anchor` is `{x: 30.5888, y: -91.1673, z: 0.0, t: celestial_time(), anchor, civil_time}` (`the_hoard.py:533-540`). No rotation, lunar, orbit, σ or bucket. `civil_time` is `""` unless the input already carried a stamp. `t` is the skewed clock. | yes | MEASURED |
| G3 | T1 "one time source"; S5 Option A. | Two sources: the celestial vector, `/clock` and the HLC read `time.time()`; `celestial_time()` reads the cached `/clock/full` response, else checkpoint + uptime, else `time.time()`. It feeds the SWDS scheduler, Hoard, Phoenix, the runner and `main.py`. The browser clock pages compute from the visitor's `Date.now()`, a third source. ADR-001 Option A is Proposed, not adopted. | yes | MEASURED |
| G4 | Middleware design: SOVEREIGN stamp carries civil time, celestial vector and bucket. | `_build_sovereign_timestamp` reads `digital_numerical_clock`, `local_datetime_cdt`, `celestial_spacetime_vector`, `celestial_kinematic_vector` and a top-level `grid_bucket` (`celestial_middleware.py:201-217`). None of those keys appears anywhere else in the code, and `/clock/full` returns `celestial_clock`, `digital_clock`, `sacred_calendar`, … So every SOVEREIGN stamp has civil time = UTC digits labelled "CDT", `celestial_vector` `{}`, `grid_bucket` null. **Ran:** the tracked checkpoint shows exactly that (`civil_dt` "01:59:42 CDT" against `utc_iso` 01:59:42Z). The ledger had the symptom as a lead; the cause is now traced. | yes | MEASURED (code + artifact) |
| G5 | S3: `Φ_lunar = ((t − T_new_moon)/P_L) mod 1`, `T_new_moon` a real new moon. | Code uses `(t − BASE_EPOCH)/P_L`, with one epoch for everything (section 5). | yes | MEASURED |
| G6 | S3: rotation and orbit measured from the baseline `T0`; seasonal position "accurate". | Orbit phase 0 is the epoch, which is 203.6 d after the real 2026 perihelion (section 5). Rotation phase depends on the epoch's time of day (finding K1). | yes | MEASURED + DERIVED |
| G7 | S3 `P_E`; S1 `SIDEREAL_YEAR`. | 31,558,149.763 s (code) against 31,556,952 s (spec, mislabelled): 1,197.763 s per year, 0.0137°/yr. Small, but two definitions of one constant. | no | MEASURED |
| G8 | S3 dim. 4: σ updated at equinox/solstice checkpoints from the bit-distance δ between the live hash and an immutable `H_target`; `σ+α` on a match, `σ−βδ` on a drift. | No `H_target`, no checkpoint dates, no caller: σ is 1.0 forever. The code's rule differs from the spec (threshold 1e-5, +0.01 / −0.1·drift). `generate_cosmic_checkpoint_hash` hashes the live coordinates, which change every ~0.02 s at 4 decimals, so it cannot equal a fixed target. If σ ever moved, `adjusted_elapsed = raw/σ` would scale the phases away from the sky. | no | MEASURED |
| G9 | S1: "verified identical across Python, Rust, JavaScript". | JavaScript: identical in four HTML files. **Rust: false.** The crate (`lib.rs`, `Cargo.toml`, `python_bridge.py`) holds none of the constants. | no | MEASURED |
| G10 | S1: anchor Baker, LA 30.5888, −91.1673. | An older script and guidebook use 30.6444, −91.1576 (`CelestialClockingCodescriptv.1.txt:109`, the v8.2 guidebook). Live code and `celestial_seed.json` agree on 30.5888, −91.1673. | no | MEASURED |
| G11 | S1/S3 "uncoupled from NTP". | False as independence: every vector reads `time.time()` (L231, L260), which Windows disciplines over NTP; the blueprint says so (§5.7.1). True only as "no network fetch; coordinates by formula". The origin text has the Architect asking to use "internet time for alignment cycles (initially)" (S2 L136); the assistant's reply calls it "training wheels" (S2 L172). | no | MEASURED; S2 CLAIMED |
| G12 | T1 / D5 (Sentinel as runtime owner). | The Sentinel is a stub with no wiring. Blueprint §5.7.3 calls it "Retired, as intended" (Architect: "UNNECESSARY REMOVE", `1_2T:L4724`); `sensory/cheshire_protocol.py:44` says its work was absorbed. D5 reverses that, so a ruling is needed. | yes | MEASURED; D5 text not seen |
| G13 | Civil time must be correct. | Scheduling uses naive `datetime.fromtimestamp(celestial_time())` (host time zone; `main.py:84, 1134`, `swds_simulator.py:86, 136, 167`). The SWDS report filename hard-codes `_CDT_` (`swds_simulator.py:177`). `DigitalNumericalClock` falls back silently to UTC while still reporting "America/Chicago" if `zoneinfo` fails (`celestial_clock.py:376-385`), and `tzdata` is not in `requirements.txt`. The live stamps print CDT, so it works today. | no | MEASURED |
| G14 | One engine, one HLC, one σ. | Eleven places create a new engine (kernel-reachable code and scripts), each instance with its own σ and, for the dual engine, its own HLC: `main.py:180-181`, `antigravity_runner.py:31, 56`, `swds_simulator.py:171`, `hunter_engine.py:817`, `daily_planet.py:299`, four scripts. Which of them coexist in one running kernel was not traced. | yes (for a single owner) | MEASURED (sites) |
| G15 | S5: the checkpoint "becomes a record". | `config/celestial_checkpoint.json` is tracked in the public repo (two commits) and written with a plain `open(..., "w")` (L117-118), not atomically. The only writer is the read route. | yes (design 1.4) | MEASURED |
| G16 | Reports must carry the celestial stamp. | `swds_simulator.py:172` calls `c.get_celestial_coordinates()`, a method that exists nowhere. The `AttributeError` is swallowed by `except Exception: pass`, so this code path can only ever write the fallback 282.85°. **Ran:** three of the five newest report filenames in the snapshot are `…CEL-282.85deg…` (2026-09-22 07:00:24, 09-23 07:00:37, 09-23 21:21:07); the other two (225.859°, 096.186°) carry other values, from an older version or another writer (not investigated). | yes | MEASURED (code + file names) |

**Other measured facts for the design (K = kept for step 1.4):**
- **K1.** Rotation is `lon + ω·(t − epoch)`. With the epoch at 08:00Z it equals the mean-sun hour angle plus 60° (checked: 2026-10-12T01:54:25Z gives 117.44° + 60° = 177.44°, the recorded value). With an epoch at 12:00Z it would equal the textbook hour angle (0° at local mean noon). The epoch's time of day therefore sets what the rotation number means.
- **K2.** `lenses.py:471` runs `asyncio.run(get_celestial_timestamp())` in an executor, and the middleware calls its own server over HTTP (`http://localhost:8000/clock/full`). ADR-001 already proposes removing the self-call.
- **K3.** `fortress/evolved_hunter_bridge.py:382` prints an un-awaited coroutine in its `__main__` demo (trivial).
- **K4.** Save-state finding 7 (CCID_1792052895): 17 of 18 `verify_true`/`is_active` methods return True unconditionally; the Sentinel is one of them.

## 4. What the tracked checkpoint file shows
`config/celestial_checkpoint.json`: `civil_dt` "2026-10-07 01:59:42 CDT" (UTC digits labelled CDT), `utc_iso` 2026-10-07T01:59:42Z, `unix_epoch` 1791338382.557, `celestial_vector` `{}`, `grid_bucket` null, `mode` "SOVEREIGN", `boot_uptime_s` 181.5. Last commit touching it on the remote branch: `e4e3949` (2026-10-08).

## 5. Epoch evidence for ruling 1 (step 1.3 preparation)
Script: `docs/brainmap/task01/epoch_check.py` (stdlib; no network; no writes). New moons use Meeus's main terms only (a few minutes' accuracy; DERIVED). My July new moon, 2026-07-14 09:45Z, agrees with NASA's date of July 14 (grade B). The perihelion instant is NASA APOD's 17:16 UTC on 2026-01-03; USNO lists 09:15 in UTC−8, which is 17:15 UTC (grade B, both via search summaries).

| Reference instant | Offset from the nearest real new moon | Position against the 2026 perihelion (the clock calls this instant phase 0 for both) |
|:--|:--|:--|
| `BASE_EPOCH` value, 2026-07-26T08:00Z | +11.93 d (+0.404 cycle): a waxing gibbous | 203.61 d after perihelion (0.557 of an anomalistic year) |
| Label, 2026-07-15T12:00Z | +1.09 d (+0.037 cycle): a day-old crescent | 192.78 d after perihelion (0.528) |

Neither candidate is a new moon or a perihelion, and no single instant can be both. Consequence for the stamps: the clock's lunar field differs from the true lunar age fraction by a constant −0.415 cycle, and its orbit field differs from the true mean-anomaly fraction by +0.443 cycle (checked at the 10-12 stamp and at container time). The numbers are internally consistent monotone counters from the epoch; they do not match the sky.

Year definitions (days): code sidereal 365.25636; spec `P_E` 365.24250; anomalistic 365.259636 and tropical 365.24219 (both CLAIMED standard values, not fetched); sacred 364. The 964-day Jubilee is 2.639 sidereal years and has no astronomical basis (blueprint §5.7.1).

Script output, verbatim (trimmed to the numbers used above):
```
k=328  new moon 2026-07-14 09:45Z
k=329  new moon 2026-08-12 17:38Z
k=331  new moon 2026-10-10 15:51Z
BASE_EPOCH value 2026-07-26T08:00Z: nearest new moon 2026-07-14 09:45Z, offset +11.927 d = +0.4039 cycle
label 2026-07-15T12:00Z: nearest new moon 2026-07-14 09:45Z, offset +1.094 d = +0.0370 cycle
BASE_EPOCH value: 203.61 d after the 2026 perihelion = 0.5574 of an anomalistic year
label: 192.78 d after the 2026 perihelion = 0.5278 of an anomalistic year
code minus spec = 1,197.763 s per year = 19.96 min; as a phase = 3.80e-05 cycle/yr = 0.0137 deg/yr
```

## 6. Rulings needed (asked once, as the rules require)
1. **D-20, the epoch.** (a) Keep one epoch, 1785052800, and correct only the labels. (b) Use the label's instant, 1784116800, for everything. (c) Follow the spec: separate constants `T0` (Cosmic Birthdate, for rotation and the sacred calendar), `T_new_moon` and `T_perihelion`, taken from an almanac. Recommendation: (c), because spec v1 itself defines the lunar phase from `T_new_moon` and the orbit from a baseline, and (c) is the only option under which the lunar and orbit fields match the sky. Any option changes the values of every future stamp, so each stamp would also carry a `clock_version`.
2. **The year constant** driving the mean anomaly: sidereal (code), spec `P_E`, anomalistic, or tropical. Recommendation, if (c): anomalistic, because the orbit phase is measured from perihelion; the 364-day sacred year stays a calendar unit.
3. **One time source (ADR-001 Option A, currently Proposed).** `celestial_time()` returns `time.time()`; the checkpoint becomes a record used only for downtime; the self-HTTP call goes. Recommendation: adopt.
4. **Sentinel scope (A4) and D5.** Confirm D5 supersedes "Retired, as intended" and choose the scope: stamp API only; stamp API plus owning the checkpoint (atomic write, timer, read-only route); or both plus wiring into the Hoard commit and the SWDS report. Recommendation: stamp API plus checkpoint ownership designed in 1.4, wiring in 1.5 to 1.6, behind your two approvals. Also: whether `config/celestial_checkpoint.json` leaves the public repo (T2's public/local-only question).

## 7. Not done, and next
- **Not done:** the live half of 1.1; Tier 1 primary quotes for the almanac facts; the text of D5, A4, §4.3 and §5.3; any design, build or test (1.4 to 1.7).
- **Next, after the rulings:** 1.3 write-up of the ruling with the almanac evidence, 1.4 Sentinel design, then 1.5 build and test in an isolated copy.
