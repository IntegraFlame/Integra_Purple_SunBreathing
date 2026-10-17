# Task 01 report: Connect Celestial Time (closed; two live checks open)

## Closing report

**Stamp (GET `/clock`, HTTP 200, frame 2):** 2026-10-16 10:29:27 CDT | 2026-10-16T15:29:27Z | rotation 321.1961°, lunar 0.1913, orbit 0.7802, ROT_300_ORB_70 (kernel uptime 01 h 15 m). **Usage:** 5-hour window 8%, weekly 77% (resets 2026-10-19 06:00 CDT).
**Scope of this closing step:** read-only checks and this text. Nothing changed in code, nothing committed, nothing pushed.

### What is true now (MEASURED at 10:29 unless noted)
- **One clock.** `celestial_time()` is the system clock (ADR-001 A). The kernel no longer reads a frozen checkpoint or calls itself over HTTP for time.
- **One stamp.** The Celestial Sentinel (`temporal/celestial_sentinel.py`) is the runtime owner of celestial time (D5). Since the 09:14:21 kernel start it has stamped: http_response 229, checkpoint 15, swds_report 1, ccid 1. Registry valid, frame 2 active, no fallback, σ 1.0, `clock_stepped_back` 0, no checkpoint error.
- **The sky, for the first time.** Frame 2 (rotation from 2026-07-15 12:00Z, lunar from the USNO new moon 2026-07-14 09:43Z, orbit from the USNO perihelion 2026-01-03 17:15Z, anomalistic year 31,558,310.6 s) is live on `/clock`, in every response header, in the checkpoint and on the dashboard. Tested against USNO/NASA/Espenak: the Moon within 0.81 d and the orbit within 1.32 d for 2026–2036. Frame 1 stays readable (`/clock?frame=1`) and reproduces the old values exactly.
- **SWDS on real time.** It slept at 02:00:59, and at the 09:14 start the reconciliation woke it. The first stamped report is `2026-10-16_09-15-31_CDT_CEL-F2-302.71deg_SWDS_Report.md`: real rotation, the written-at time in UTC, the frame-2 vector. The constant 282.85° is gone.
- **The checkpoint.** It is a record, never a time source. One atomic writer, every 300 s, in the git-ignored `local_dbs/celestial/`. The old tracked file is no longer written and no longer tracked. `GET /celestial/checkpoint` is read-only.
- **Committed** in the nested repo, `phase-e-dragon-rodin-flight`: `95a7aab` (the Sentinel and frame 2, 18 files) and `c7053f1` (S3). Not pushed (ahead 4); the root gitlink is not recorded.
- **Tested.** The tree of each commit: 461 passed, 1 failed (the environment-only Voltron test). Mutation checks caught 8 of 9; the ninth was an equivalent change.

### Gate K tally for T1
| T1 "true means" or done-when item | Status |
|:--|:--|
| Clock mechanics match their definitions | **Met.** Frame-1 parity at 11,000 instants; frame 2 against Tier 1 almanacs |
| One time source | **Met** for stamping. The 634 duration and log reads were excluded by design |
| SWDS reports stamped | **Met, live** (the 09:15:31 report) |
| CCIDs stamped from the same instant | **Met, live** (the Metatron session CCID, `ccid` 1); Phoenix and crystallization covered by tests |
| HTTP responses stamped | **Met, live** (`X-Celestial-Frame: 2`) |
| The checkpoint as a single atomic writer, its route read-only | **Met, live** |
| A fresh Hoard node carries both stamps, read back from disk | **Open, live.** Met in the isolated tests; no shard has been written since the 09:14 start |
| A save state carries both stamps | **Open, live.** Its source (`/clock`) is frame 2 now; no save state written since the start. The Hoard's save-state sync path is covered by the node test |
| Ledger rows stamped | **Not applicable yet:** no ledger exists (ADR-002, Phase 1); `stamp()` is ready for it |

**T1 tally: 6 of 8 live criteria met, 2 open (both met in tests), 1 not applicable.**
Gaps from 1.2: G2, G5 items 1–3, G6, G7, G8, G11, G12 and G15 are closed. G1, G3 and G4 are closed in code (live check open). G9 is documented. G10 is σ fixed (its revival is open). G13 is partly closed (the checkpoint route; `/clock`'s literal flags remain). G14 is superseded for stamping.

### What is open
1. **Live checks (read-only):** the next naturally written Hoard node and the next save state, each read back from disk for `celestial_stamp` and frame 2.
2. **ADR-001 item 4's correction note** for the frozen-era artefacts was not written: 55 SWDS reports named `CEL-282.85deg`, report-name dates 7 days behind their file times, and 258 shards with `t = 0`. It is a small documentation task, and T2 would be a natural place for it.
3. **On the Architect's word only:** record `95a7aab`/`c7053f1` in the root repo's gitlink, and push.
4. **Supervision, again.** The task's wrapper ended at **09:26:47** (Task Scheduler 201/102; task Ready since), 12.5 minutes after this start, while python 3216/3192 run on. That makes 7 of 7 launches.
   - New observation, a timing coincidence and not an established cause: both exits today (03:13:27 and 09:26:47) came 3–14 s after one of my read-only probe commands finished.
   - This belongs to the Phase 0 supervision task (ADR-010; the review is `docs/KERNEL_AUTOLAUNCH_REVIEW.md`).
5. **Not T1's, still in the live tree:** the peer's uncommitted `memory/the_hoard.py` identity edit makes two `test_hoard_schema_v2` tests fail. Its owner should decide it.
6. **Later design items:**
   - `/clock`'s literal flags (ADR-003, Phase 0);
   - the equation of time (apparent Sun);
   - σ revival with a real drift measure;
   - what anchor x, y, z mean (T3/T4);
   - back-filling old nodes (T2/T5);
   - the Coordinate Beta packet's frame field;
   - same-second CCID collisions.
7. **Machine load:** `/clock` latencies of 6–18 s while the CPU was at 100% (the Gemini app, Explorer, OneDrive). Not T1's.

### Evidence
- **This file** (steps 1.1–1.7, S3 and R4).
- **`T1_CELESTIAL_SENTINEL_DESIGN.md`.**
- **Outside the repo, `~/.claude/projects/<project>/brainmap_t1_2026-10-16/`:**
  - the almanac data and frame scripts;
  - `build_1.5/` (patch, `FILES.tsv`, changed files, test outputs, mutation scripts);
  - `commit_prep/` (both commit messages, the staging and export scripts, the commit-tree test outputs).

### Next task
**T2: Connect the Hoard**, on the Architect's go. Its first steps are read-only:
- the memory-map inventory;
- a trace of each Hoard function from caller to store;
- the verdict table.

The two open T1 live checks can be read whenever a node or a save state appears.

---

Steps 1.1–1.2 were reported at 00:39 (below). The Architect then accepted the recommended rulings R1–R6 and decisions S1–S5. The rest follows at the end of this file: steps 1.3 (the almanac check), 1.4 (the Sentinel design), 1.5 (build and test in an isolated copy), 1.6 (copy into the live tree; the new code went live when the machine came back from a power loss) and 1.7 (live verification). Nothing is committed. The design itself is `T1_CELESTIAL_SENTINEL_DESIGN.md`.

**Stamp (GET `/clock`, HTTP 200, 0.64 s):** 2026-10-16 00:39:12 CDT | 2026-10-16T05:39:12Z | rotation 233.6328°, lunar 0.7735, orbit 0.2269, ROT_210_ORB_20 (kernel uptime 00 h 31 m 46 s).
**Session:** f9e973c9 (boot session, no agents). **Usage at the stamp:** 5-hour window 4%, weekly 75% (resets 2026-10-19 06:00 CDT).
**Scope:** read-only. No code changed, no POST, no restart, no paid call, no test run. Files written: this report and one progress row in `TODO.md`. Every claim carries MEASURED (I ran or read it), DERIVED (computed from measured values), CONSTANT (a literal in code) or CLAIMED (a document or published constant says so).

## Goal (map L1)
"Connect Celestial Time --- ensure metadata and active time stamping is true. Also make sure Celestial Clock/Time mechanics and functions as defined are true." From `TODO.md`: every Hoard save, SWDS report, CCID node and ledger row is stamped automatically with celestial and civil time; the mechanics match their definitions; there is one time source.

## Bottom line
- **The math is right as written.** The kernel's celestial vector reproduces exactly from the formulas in 6 of 6 live readings, and `temporal/celestial_clock.py` is byte-identical to the copy the Architect ruled correct (sha16 `4199779CF1F2D740`).
- **The time source is now one OS clock, but only in the uncommitted working tree.** The running kernel uses the ADR-001 fix (`celestial_time()` returns `time.time()`). Nothing of it is committed.
- **Active stamping is not true yet.** 2 of 308 Hoard shards carry any celestial coordinate. 258 of 304 node anchors have `t = 0`. 55 of 61 SWDS reports carry the same hard-coded 282.85° in their name. No ledger exists.
- **As a picture of the sky, the vector is referenced to the wrong instant** (D-20). The lunar ratio reads 0.77 while the Moon is about 5 days past new (≈0.17). The orbit coordinate is not measured from perihelion. These are constant choices, not formula errors; the rulings below decide them.

## 1.1 Measurement

### Live (MEASURED)
| What | Result |
|:--|:--|
| Kernel | Boot 2026-10-16 00:05:41 after the Architect's restart (System 1074 at 23:50:30 and 23:52:43). Task "Integra Genesis Kernel" Running since 00:06:01; python 14668/14680 since 00:07:08. It loads the working tree, so it runs the peers' uncommitted edits. |
| `GET /clock` | Answered at 00:21:13, 00:27:29, 00:33:38, 00:39:12; σ (`spiral_accuracy_depth`) 1.0 every time. |
| Response stamping | Every HTTP response now carries `X-Sovereign-Timestamp`, `X-Baker-Time`, `X-Celestial-Vector` (rot, lunar, orbit, sigma) and `X-Celestial-Grid-Bucket` (seen on `/clock` at 00:33:38). Source: the uncommitted middleware `inject_celestial_temporal_headers` in `main.py`. |
| Checkpoint | `config/celestial_checkpoint.json` written at 00:19:42 by the startup sync (`main.py:127-140` → `sync_celestial_checkpoint_now()`): live time, `CCID_1792127982`, full vector, ROT_210_ORB_20, mode SOVEREIGN. Before the fix it held 2026-10-06 20:59:42. The file is tracked in git and now ` M`. |
| `/swds/status` | AWAKE; idle 1,908 s at 00:39 (≈ uptime: GET probes do not count as activity). Scheduler: sleep when 02:00 ≤ local hour < 07:00 and idle ≥ 3,600 s, wake at 07:00 (`main.py:1179-1209`). So the first SWDS on the live clock is due about 02:00 tonight (DERIVED). |

### The formulas against the live readings (MEASURED)
An independent re-implementation of `temporal/celestial_clock.py:225-253` (no project import; script `scratchpad/t1/clock_check.py`, run with `C:\Python313\python.exe -I -X utf8`):

| Reading | UTC | rot (code / live) | lunar | orbit | bucket | Verdict |
|:--|:--|:--|:--|:--|:--|:--|
| save state | 04:03:20 | 209.6695 / 209.6695 | 0.7712 | 0.2267 | ROT_180_ORB_20 | match |
| peer TODO | 04:40:20 | 218.9160 / 218.9201 | 0.7721 | 0.2268 | ROT_210_ORB_20 | match (1 s) |
| checkpoint | 05:19:42 | 228.7584 / 228.7584 | 0.7730 | 0.2268 | ROT_210_ORB_20 | match |
| `/clock` | 05:21:13 | 229.1392 / 229.1392 | 0.7730 | 0.2268 | ROT_210_ORB_20 | match |
| `/clock` | 05:27:29 | 230.7050 / 230.7047 | 0.7732 | 0.2268 | ROT_210_ORB_20 | match |
| `/clock` header | 05:33:38 | 232.2410 / 232.2419 | 0.7733 | 0.2269 | ROT_210_ORB_20 | match (whole-second time) |

The largest rotation difference is 0.0041°, about 1 s of rotation, from readings recorded to the whole second. The first two readings came from the 19:37 kernel and the rest from the 00:07 kernel: the vector did not change with the clock fix, as expected, because `/clock` always read `time.time()`.

### In code: exists, wired, ran
| Function | Exists | Wired (production caller) | Ran (evidence) |
|:--|:--|:--|:--|
| `celestial_time()` = `time.time()` (ADR-001 A) | yes, **uncommitted** (`core/celestial_middleware.py:339-359`) | 39 calls in 7 files (main, the_hoard, phoenix_forge, swds_simulator, antigravity_runner, lenses, the middleware) | yes: the checkpoint's live time; SWDS idle counter |
| `celestial_ccid()` | yes | `memory/the_hoard.py:899`, `evolution/shiva_action/lenses.py:476-480` | not observed since the 00:07 start |
| `get_celestial_metadata_sync()`, `sync_celestial_checkpoint_now()` | yes, **new and uncommitted** (`:374-449`) | lifespan (`main.py:134`), `GET /celestial/checkpoint` (`main.py:1427`) | yes: checkpoint at 00:19:42 |
| `stamp_celestial_metadata()` (stamps any payload) | yes, **new and uncommitted** (`:422-438`) | **none**: only `tests/test_celestial_time_adr001.py` | no |
| HTTP header stamping | yes, **new and uncommitted** (`main.py`, `inject_celestial_temporal_headers`) | every response | yes (00:33:38) |
| `CelestialClockArchitecture.generate_hoard_manifest()` | yes (`celestial_clock.py:311-326`) | `runtime/antigravity_runner.py:56` only | not observed |
| `SpacetimeIndexer.generate_4d_metadata_manifest()` | yes (`:343-364`) | inside `get_celestial_metadata_sync()` | computed at boot, then discarded: the checkpoint stores only the timestamp fields |
| `apply_zenkai_recalibration()` (σ) | yes (`:281-300`) | **none** | no; σ = 1.0 is CONSTANT |
| Celestial Sentinel | 423-byte stub, all True flags (`temporal/celestial_sentinel.py`, unchanged since 2026-09-28) | only a test | no |
| `get_celestial_timestamp()` (async; the kernel calls its own `/clock/full` over HTTP) | yes | `GET /celestial/checkpoint`, Shiva lenses | not called by me (that route writes) |

### What stored data actually carries (MEASURED census, read-only; script `scratchpad/t1/stamp_census.py`)
- **Hoard raw shards (308 files):**
  - 2 contain any celestial field (`earth_rotation_deg`, `lunar_cycle_ratio`, `orbital_trajectory_pos`) or a ROT/ORB bucket.
  - 304 have a `spacetime_anchor`: in 258 `t` is 0; in 46 it looks like an epoch. Key sets: 259 `{t,x,y,z}`, 40 add `orbital_index`, 4 add `anchor` and `civil_time`, 1 adds `celestial`.
  - The anchors' x and y are constants, not coordinates: Baker's latitude/longitude (save-state sync, `the_hoard.py:903-910`), `1.0 / 0.5` from Phoenix (`evolution/phoenix_forge.py:468-473`, where `t` is Phoenix's generation counter, not a time), or `0 / 0` for crystallizations (`the_hoard.py:1070-1075`).
  - Nodes do get `created_at = celestial_time()` (`the_hoard.py:112`): a true Unix time since the fix, with no celestial vector beside it.
  - The newest shard, `CCID_1792116734.json` (untracked, file time 2026-10-15 21:12:14), has the Phoenix anchor pattern (`x 1.0, y 0.5, t 0`). Which process wrote it is not established.
- **SWDS reports (61):** 55 are named `CEL-282.85deg`. Cause: `runtime/swds_simulator.py:168-174` calls `CelestialClockArchitecture().get_celestial_coordinates()`, a method that exists nowhere in the repo. The AttributeError is swallowed and the fallback literal 282.85 is used (first seen in the report of 2026-09-13, file time 2026-09-28). The report names' dates ran 7 days behind their file times during the frozen-clock era. Tonight's report should carry the true date and still the constant 282.85° (DERIVED).
- **Save states:** stamped by the agent from `GET /clock` by hand, not by code.
- **Ledger rows:** no ledger code exists (no `record()` or ledger class in any `.py`; ADR-002 is still a Phase 1 task).
- **Direct clock reads** (`.py` outside `tests/`, `CODE/`, `scratch/` and venvs): `time.time()` 382 sites in 115 files, `datetime.now(` 248 in 142, `datetime.utcnow(` 4 in 4, against `celestial_time()` 39 in 7. All of them now read the same OS clock, so the value is consistent. There is still no single stamp function.

### Tests (not run)
`tests/test_celestial_time_adr001.py` (7 tests, uncommitted) covers the stale-checkpoint case, the CCID, the canonical `/clock/full` keys, the stamp helper and the checkpoint sync. Not run: the suite never runs in the live repo, and the isolated run belongs to step 1.5. **Finding:** `test_sync_celestial_checkpoint_now_persists_full_vector` writes the real `config/celestial_checkpoint.json` (it does not redirect `_CHECKPOINT_PATH`), so running it in the live tree would overwrite a tracked, live file.

## 1.2 Gap list against the definitions
Definitions used: **D1** `temporal/celestial_clock.py` (ruled correct, "Celestial Time CORRECT", 10/13); **D2** spacetime spec v1, `Guidebooks_and_Notes/Notes10_13_2026.md` L731-777; **D3** the Celestial Constants document, `Guidebooks_and_Notes/THECELESTIALCONSTANTSGenius shit.md` L134-148 and L180-185; **D4** blueprint §5.7.1-5.7.3 (L740-758) and ADR-001 (L955-1012); **D5** `docs/DESIGN_DECISIONS_10_15_26.md` §4.3 and §5.3 (L101-110, L142-144) and A4 (L27).

| # | Gap | What the definition says | What is measured | Fix belongs to |
|:--|:--|:--|:--|:--|
| G1 | Nodes are not stamped with the celestial vector | D2 L774-776: when an entry enters the Hoard it is serialized with [θ_rot, Φ_lunar, E_orbit, σ]. D3 L180-185: every data point anchored to rotation, lunar cycle and orbit. D2 L731: "should already be occurring". D5 §5.3(a): one `stamp()` every writer calls | 2 of 308 shards carry a vector; `stamp_celestial_metadata()` exists with no caller | 1.4 design, 1.5 build (Sentinel `stamp()`) |
| G2 | SWDS reports carry a constant 282.85° | D4 ADR-001 item 4: reports get a true time; D5 §4.3: stamp(kind) → SWDS | 55 of 61 report names; call to a non-existent method, error swallowed | 1.5 (one-line fix plus `report_written_at`) |
| G3 | Node anchors are placeholders | D2/D3: a real 4-D coordinate per node | `t = 0` in 258 of 304; Phoenix `t` = generation counter; x, y constants | 1.5 for `t`; what x, y, z mean is T3/T4 (Atlas) |
| G4 | No single stamp function | D5 §5.3(a) | 634 direct OS-clock reads against 39 `celestial_time()` calls; values agree since ADR-001 | 1.4 (decide which writers move first: Hoard, SWDS, CCID, checkpoint) |
| G5 | ADR-001 only partly done | D4 L1009-1012: 1 `celestial_time()` = `time.time()`; 2 checkpoint on a timer; 3 regression test; 4 `report_written_at` and a correction note. Option A also "removes the self-HTTP fetch" (L970) | 1 done, **uncommitted**, running; 2 not done (written at boot and on demand); 3 written, not run, and it writes the live checkpoint; 4 not done (no `report_written_at` anywhere); the self-HTTP fetch remains in `get_celestial_timestamp()` | 1.5, and the commit ruling R4 |
| G6 | Several checkpoint writers, not atomic | D5 §4.3 and A4: the Sentinel is the only writer, atomic; `GET /celestial/checkpoint` read-only | Writers: the startup sync, `GET /celestial/checkpoint` (writes twice per call), `get_celestial_timestamp()` (Shiva lenses). Plain `open('w')`, no temp file and rename. A tracked file is rewritten at every start | 1.4/1.5 (A4) |
| G7 | The epoch value disagrees with its label (D-20) | D1's own comment: 2026-07-15T12:00:00Z. D2 L748: Φ_lunar counts from a new moon, `T_new_moon`, separate from T0 | `BASE_EPOCH` 1785052800 = 2026-07-26T08:00:00Z, 10.83 days later. Effects (DERIVED; mean-element constants from Meeus, CLAIMED; to be checked against an almanac in 1.3): **rotation** = Baker's local mean-solar hour angle + 60° (with a 12:00Z epoch it would equal the hour angle exactly); **lunar** 0.7733 now, while the Moon's mean phase is ≈0.170 (age 5.0 d; last mean new moon 2026-10-11 05:19Z). The epoch is 11.7 days after a new moon; the labelled epoch would be 0.9 days after one. **Orbit** 0.2269 now, while Earth's mean anomaly is 0.7816 of an orbit (mean perihelion 2026-01-03). Neither epoch is a perihelion, so the Kepler correction is applied at the wrong point of the orbit | 1.3 ruling R1 |
| G8 | Year constant | D2 L755: P_E = 31,556,952 s, labelled "Sidereal Year" (that number is the Gregorian mean year) | D1 uses 31,558,149.763 s (sidereal). The difference is under 1e-5 of an orbit now, and code and spec drift apart by about 20 minutes per year. An orbit measured from perihelion would use the anomalistic year (≈31,558,432 s; CLAIMED) | 1.3 ruling R2 |
| G9 | "Earth rotation" is a solar-day angle | D2 L739: ω = 360°/86400 s (solar day). D3 L134: rotational speed is "time to reach the original ping point" | D1 matches D2. Not Earth's sidereal rotation (86,164.09 s), which blueprint §5.7.1 already notes. No change unless ruled | information |
| G10 | σ (Zenkai) is a constant | D2 L763-772, D3 L138-148: celestial events (equinox, solstice, eclipse) are checkpoints that correct σ | No caller, no event table, no target hash; σ = 1.0. DERIVED design note: a SHA-256 byte distance cannot measure how large a drift is (any change scrambles the hash), so the loop as written would only ever lower σ | 1.3 ruling R5 |
| G11 | Grid bucket has no lunar segment (C-16) | Rodin §8a and the spec: `ROT_XXX_LUN_YYY_ORB_ZZZ` | Live bucket `ROT_210_ORB_20` (30° and 10% buckets) | T3.5/T4: the pointer v1 label adds LUN |
| G12 | The Sentinel is a stub | D5 D5/§5.3: the runtime owner of celestial time | 15-line stub with True flags; blueprint §5.7.3 still says "Retired" | 1.4 design; blueprint text in Step 3 |
| G13 | Decorative constants | ADR-003: no literal status flags | `/clock` returns `sync_isolation_verified`, `is_active`, `all_systems_true` as literals (`celestial_clock.py:442-445`); `/celestial/checkpoint` returns `all_systems_true: True` as a literal | 1.5, or the Phase 0 ADR-003 task |
| G14 | Two manifests with one name | D5 §4.3: one stamp | `CelestialClockArchitecture.generate_hoard_manifest()` (bucket + vector + `status: SOVEREIGN_GROUNDED`) differs from `DualTemporalEngine.generate_hoard_manifest()` (bucket + HLC vector + hash + `loop_closure_verified: True` as a literal) | 1.4 (pick one) |
| G15 | Everything above the math is uncommitted | — | The clock fix, the stamp helpers, the startup sync, the header middleware and the regression test exist only in the working tree. A checkout or a revert brings back the frozen clock at the next start | ruling R4 |

**True now:** the math matches its definition (D1) exactly; one OS clock feeds everything in the running kernel; the checkpoint holds the live time and the full vector; every HTTP response carries both clocks; SWDS should fire in the real 02:00-07:00 window (first observation due tonight).
**Not true yet:** automatic celestial stamping of Hoard nodes, SWDS reports, CCID nodes and ledger rows; a real σ; a single checkpoint writer; a committed fix; the epoch's meaning (D-20).

## Rulings needed (one batch)
- **R1, the epoch (D-20).**
  - (a) Keep 1785052800 and correct the label to 2026-07-26 08:00Z. Nothing moves.
  - (b) Restore the label's 2026-07-15 12:00Z. Every coordinate shifts (in pointer v1 terms, a new celestial frame).
  - (c) Keep the formulas but give each dimension its own reference: T0 at 12:00Z for rotation (then it is the local hour angle), a real new moon for Φ_lunar (as spec v1 L748 already says), and perihelion for the orbit.
  - My recommendation: (c), checked against a Tier 1 almanac in step 1.3 and introduced as frame 2, so stamps stay comparable within each frame. It changes constants, not the math the ruling protects.
- **R2, the year constant.** Keep the code's sidereal year, adopt spec v1's 31,556,952 s, or use the anomalistic year if R1(c) measures the orbit from perihelion. Recommendation: anomalistic with (c), otherwise keep the code's.
- **R3, the Sentinel's scope (A4).** It owns `stamp()`, is the only checkpoint writer (atomic, on a timer), serves `GET /celestial/checkpoint` read-only and runs in the kernel process. Recommendation: yes, as designed in §5.3.
- **R4, the running uncommitted edits.** These are the clock fix, the stamp helpers, the startup sync, the header middleware and the regression test. Recommendation: run them in an isolated copy (after fixing the test that writes the live checkpoint), then commit only the clock files, on your go. The other peer edits (`dragon_engine.py`, `starfire_protocol.py`, `the_hoard.py`, `rodin_memory_map.yml`) stay out of a T1 commit.
- **R5, σ.** Fix σ at 1.0 for stamps until a real drift measure exists (pointer v1 already does this), and record the spec's hash loop as an open design item. Recommendation: yes.
- **R6, the SWDS report constant.** Fix it in step 1.5 together with `report_written_at`. Recommendation: yes; tonight's report will still carry 282.85°.

## Next (as planned at 00:39)
After the rulings:
- 1.3: the almanac check (read-only; Tier 1 sources for the new moon and perihelion of 2026).
- 1.4: the Sentinel design (stamp API, writer list, migration order).
- 1.5: build and test in an isolated copy.
- 1.6: apply and restart (two approvals).
- 1.7: verify that a fresh Hoard node, a save state and an SWDS report each carry both stamps, read back from disk.

---

## 1.3 Almanac check

**Stamp (GET `/clock`, HTTP 200, 0.71 s):** 2026-10-16 01:37:38 CDT | 2026-10-16T06:37:38Z | rotation 248.2413°, lunar 0.7748, orbit 0.2270, ROT_240_ORB_20 (kernel uptime 01 h 30 m 12 s). **Usage:** 5-hour window 5%, weekly 75%.
**Rulings applied (Architect, after the 00:39 report):** R1 option (c), R2 the anomalistic year, R3 the Sentinel scope as designed, R4 isolated test then a clock-only commit on a go, R5 σ fixed at 1.0, R6 fix the SWDS constant in 1.5.
**Scope:** read-only. Three public GETs to almanac services; nothing was sent except the URLs (no location, no data). No code changed. Evidence (scripts, downloaded data, full output) is outside the repo: `~/.claude/projects/<project>/brainmap_t1_2026-10-16/`.

### Sources (Tier 1) and cross-checks (MEASURED)
- **USNO Astronomical Applications API 4.0.1:** `api/moon/phases/year?year=2026` (50 phases) and `api/seasons?year=2026` and `2027` (perihelion, aphelion, equinoxes, solstices), all in UT.
- **NASA GSFC, *Phases of the Moon 2001 to 2100*** (F. Espenak): every 2026 new moon agrees with USNO to the minute; one full moon differs by 1 minute (Jun 29, 23:57 against 23:56).
- **F. Espenak, *Earth at Perihelion and Aphelion 2001 to 2100*** (astropixels.com): the 2026 perihelion 17:16 against USNO 17:15, aphelion 17:31 against 17:30, and the 2027 perihelion identical (02:33).

### Reference instants and periods
| Quantity | Value | Provenance |
|:--|:--|:--|
| New moon nearest the labelled epoch | 2026-07-14 09:43 UT (1.1 days before the label's 2026-07-15 12:00Z) | MEASURED (USNO = NASA) |
| Last new moon before today | 2026-10-10 15:50 UT; next 2026-11-09 07:02 UT | MEASURED |
| Perihelion 2026 | 2026-01-03 17:15 UT | MEASURED (USNO; Espenak 17:16) |
| Aphelion 2026 | 2026-07-06 17:30 UT | MEASURED |
| Perihelion 2027 | 2027-01-03 02:33 UT | MEASURED |
| Anomalistic year | **31,558,310.6 s = 365.258224 d**: least-squares fit over all 100 perihelia 2001–2100. Single intervals range 363.08–367.86 d because the Moon makes Earth's perihelion wander; residuals around the fit are within 1.35 d | DERIVED from MEASURED tables |
| Synodic month | 2,551,442.4 s = 29.530584 d: least-squares fit over 1,237 new moons 2001–2100. **The code's 2,551,442.8 s is confirmed (0.4 s apart)** | DERIVED |
| Year in the code | 31,558,149.763 s (sidereal). For an orbit measured from perihelion this is the wrong period: it gains 2.7 minutes per year on the anomalistic year | DERIVED |

**A correction made during the run:** my first estimate of the anomalistic year used only the first and last perihelion and gave 365.234 d. That value is wrong, because the two endpoint perihelia wobble. The least-squares fit above replaces it.

### Frame 2 (R1 (c), R2, R5): same formulas, new references
| Dimension | Formula (unchanged from `celestial_clock.py:225-253`) | Reference | Period |
|:--|:--|:--|:--|
| Rotation | (λ + 360°·(u − T_rot)/86,400) mod 360 | **T_rot = 2026-07-15 12:00:00Z**, the code's own "Cosmic Birthdate" label. Rotation then equals Baker's local mean-solar hour angle: 0° at local mean noon (18:04:40Z) | 86,400 s (unchanged) |
| Lunar | ((u − T_nm)/P_L) mod 1 | **T_nm = 2026-07-14 09:43:00Z** (USNO) | P_L = 2,551,442.8 s (unchanged, confirmed) |
| Orbit | E/2π, with M = 2π·(((u − T_peri)/P_A) mod 1) and Kepler solved by Newton–Raphson | **T_peri = 2026-01-03 17:15:00Z** (USNO) | **P_A = 31,558,310.6 s**; e = 0.0167086 (unchanged) |
| σ | fixed 1.0 (R5) | | |
| TURN (pointer v1) | ⌊(u − T_peri)/P_A⌋, the number of perihelion passages | | |

Unix values: T_rot 1784116800, T_nm 1784022180, T_peri 1767460500.

### Test against the almanac (MEASURED comparisons; script `frame2_check.py`)
| Test | Frame 1 (today's constants) | Frame 2 |
|:--|:--|:--|
| Lunar ratio at the 25 USNO new and full moons of 2026 (expected 0.0 and 0.5) | off by up to 0.415 (12.3 days) | within 0.026 (0.78 d) at new moons, 0.016 (0.48 d) at full moons |
| Lunar ratio at the 136 NASA new moons 2026–2036 | off by up to 0.416 (12.3 d) | within 0.028 (0.81 d); mean 0.011 |
| Orbit at aphelion 2026 (expected 0.5) | 0.9454 (off by 0.445) | 0.5037 (off by 0.0037) |
| Orbit at the 11 perihelia 2026–2036 (expected 0.0) | off by up to 0.447 (163 d) | within 0.0036 (1.32 d) |
| Rotation at Baker's local mean noon (expected 0°) | 60.0° | 0.0° (359.999°) |

The remaining frame-2 errors come from using mean periods: real lunations vary in length, and the Moon pulls Earth's perihelion back and forth. They do not come from the reference instants. Frame 2 places the Moon within a day and the orbit within about a day and a half, for at least ten years.

**An alternative, recorded but not adopted:** using the fitted mean instants (new moon 2026-07-14 15:10:27Z, perihelion 2026-01-03 18:57:34Z, P_L 2,551,442.4 s) tightens the decade errors to 0.59 d (Moon) and 1.24 d (orbit). The almanac instants stay as ruled because each one cites a single USNO event.

### What frame 2 changes (DERIVED; nothing applied)
- **The live stamp at 01:34:05 CDT:**
  - frame 1: rotation 247.35°, lunar 0.7748, orbit 0.2270, grid `ROT_240_ORB_20`, pointer label `ROT_240_LUN_70_ORB_20`;
  - frame 2: rotation 187.35°, lunar 0.1787, orbit 0.7792, grid `ROT_180_ORB_70`, pointer label `ROT_180_LUN_10_ORB_70`.
  - The Moon was 5.6 days past the 10-10 15:50 UT new moon (a true ratio of about 0.19). Frame 2's 0.179 is within its stated error; frame 1's 0.775 is not.
- **Every value of the vector changes** on `/clock`, the dashboard, the checkpoint, response headers and new stamps. Stamps already written stay frame 1. Under pointer v1's rule, stamps from different frames are never compared, so every stored stamp needs its frame id. The frame registry and the switch-over belong to the Sentinel design (1.4) and a restart (1.6).
- **Season markers in frame 2's orbit coordinate** (informational, from USNO 2026): March equinox 0.2104, June solstice 0.4623, September equinox 0.7155, December solstice 0.9635.

### Not verified
- **The apparent Sun.** Frame 2's rotation is the *mean*-solar hour angle. The real Sun runs ahead of or behind it by the equation of time (up to about ±16 minutes, ±4°; CLAIMED). I did not fetch a solar-transit time for Baker, so as not to send the anchor location to an outside service.
- **σ checkpoints.** The NASA table also marks 2026's eclipses (Feb 17, Mar 3, Aug 12, Aug 28). They are candidate checkpoints if σ is ever revived. Nothing changes now (R5).
- **Tests.** None run; nothing was built.

### Where each ruling stands
| Ruling | Status after 1.3 |
|:--|:--|
| R1 (c) | Reference instants verified against Tier 1 sources; frame 2 defined and tested (above). Goes into code at 1.5 |
| R2 | P_A = 31,558,310.6 s (fitted) |
| R3 | Next: the Sentinel design (1.4) |
| R4 | At 1.5: fix the test that writes the live checkpoint, run the suite in an isolated copy, then a clock-only commit on a go |
| R5 | σ = 1.0 in frame 2 |
| R6 | At 1.5. Tonight's SWDS report will still be named `CEL-282.85deg` (SWDS was due at about 02:00; at 01:37 the kernel was still AWAKE, idle 5,413 s) |

## Next (as planned at 01:37): 1.4, the Sentinel design (documentation only)
- **Stamp:** one `stamp(kind)` API returning civil time, the frame-2 vector, the frame id and the provenance.
- **Frames:** a registry with frames 1 and 2, and where it lives (with pointer v1's `celestial_frames:`).
- **Checkpoint:** a single, atomic writer on a timer; `GET /celestial/checkpoint` becomes read-only.
- **Writers:** the order in which they move to `stamp()`: Hoard nodes and anchors, SWDS reports, CCIDs, the checkpoint, response headers.
- **Display:** how `/clock` and the dashboard switch frames.
- **Tests** for 1.5.

---

## 1.4 The Sentinel design

**Stamp (GET `/clock`, HTTP 200):** 2026-10-16 02:31:36 CDT | 2026-10-16T07:31:36Z | rotation 261.7352°, lunar 0.7761, orbit 0.2271, ROT_240_ORB_20 (frame 1). **Usage:** 5-hour window 6%, weekly 75%.
**Scope:** documentation only. Read-only code reading and GETs; no code changed. **Deliverable:** `docs/brainmap/T1_CELESTIAL_SENTINEL_DESIGN.md`.

### Measured along the way
- **SWDS ran on the live clock, as derived in step 1.1.** `/swds/status` at 02:31 reads `SLOW_WAVE_DEEP_SLEEP`, phase 3, `sleep_initiated_at` 2026-10-16 02:00:59 CDT (MEASURED). Wake is due at 07:00. Its report will still be named `CEL-282.85deg` until step 1.5 (R6).
- **Correction to step 1.1 (G1).** The 40 Daily Planet shards do carry the frame-1 vector. It sits in the anchor's x, y, z and `orbital_index` (`tools/daily_planet.py:474-484`, `:556-565`), not in named fields, which is why my census missed it. **42 of 308 shards carry the vector, not 2.** The other findings stand: 258 of 304 anchors have `t = 0`, and no stamp is applied automatically.
- **The dashboard and the clock-live page compute the vector themselves**, in JavaScript with frame-1 constants (`static/dashboard.html:794-920`, `static/celestial_clock_live.html:273-330`). A frame switch must reach them, so the design adds a read-only `GET /celestial/frame`.
- **More git-tracked files the kernel rewrites at runtime:** `config/celestial_checkpoint.json`, `runtime/swds_state.json` and `kernel_memory/core_identity.txt`. `local_dbs/` is git-ignored (`.gitignore:35`).
- **`config/celestial_seed.json`** holds the frame-1 constants and has no Python reader.
- **Peer edits (for the commit plan).** All of `main.py`'s uncommitted hunks are clock-related. `memory/the_hoard.py`'s uncommitted hunks are identity changes (the `core_identity.txt` creation moved to Starfire), not clock. A T1 commit must stage only its own hunks in that file.
- **The old stub** (`temporal/celestial_sentinel.py`) is imported only by `tests/test_systems_audit_and_protocols.py:286-289`, which asserts its True flags.

### The design in brief
- **One `stamp(kind, at=None)`** returns a `celestial_stamp` record: schema, frame, unix, UTC, civil, `rot_deg`, `lun`, `orb`, `turn`, σ = 1.0, the live `grid` format, pointer v1's `label` with LUN, kind, provenance.
- **A frame registry** (`config/celestial_frames.yml`): append-only, with frame 1 kept for old stamps and frame 2 as defined in 1.3. It is validated at load; if it fails, the Sentinel falls back loudly.
- **The ruled math is parameterized by frame** (S1), with a frame-1 parity test.
- **One checkpoint writer:** atomic, every 300 s plus at start and stop, in the git-ignored `local_dbs/celestial/`. `GET /celestial/checkpoint` becomes read-only and returns `status()`.
- **Writers move in a set order:** checkpoint and routes; SWDS reports (`CEL-F2-…`, `report_written_at`); Hoard nodes (`celestial_stamp`, `t` filled when missing, Phoenix's counter moved to `generation`); CCIDs; headers (`X-Celestial-Frame`); displays (`/clock` with `?frame=1`, both HTML pages reading `GET /celestial/frame`).
- **Twelve offline tests,** including the almanac fixture and the R4 isolation fix.
- **Build, apply and verify plan:** hunk-limited staging; restart only while AWAKE.

### Decisions needed (one batch; recommendations in the design's §6)
| Id | Question | Recommendation |
|:--|:--|:--|
| S1 | Where the frame-aware math lives | Parameterize `temporal/celestial_clock.py`: one implementation; its hash changes; a frame-1 parity test pins today's behaviour |
| S2 | Where the frame registry lives | A new `config/celestial_frames.yml` (not the peer-edited memory map) |
| S3 | The checkpoint file | Move it to `local_dbs/celestial/checkpoint.json` and untrack the old file on a go |
| S4 | The switch to frame 2 | Everything at once at the 1.6 restart, with `?frame=1` for comparison |
| S5 | The SWDS report name | `CEL-F2-{rot}deg` |

### Next (as planned at 02:31): 1.5, build and test in an isolated copy (nothing live)
Build a copy from the live tree; implement §4.8 in order; run the 12 new tests, the fixed ADR-001 tests, the clock, Hoard and SWDS suites, and the full suite. Deliver the patch, the file list and the verbatim output. The live tree, commits and the restart wait for 1.6 and their own gos.

---

## 1.5 Build and test in an isolated copy

**Stamp (GET `/clock`, HTTP 200):** 2026-10-16 02:43:23 CDT | 2026-10-16T07:43:23Z | rotation 264.6803°, lunar 0.7764, orbit 0.2271, ROT_240_ORB_20 (frame 1; the live kernel was in SWDS phase 3). **Usage:** 5-hour window 7%, weekly 76%.
**Decisions applied:** S1–S5 as recommended (Architect, after the 02:31 report).
**Scope:** nothing live was touched. The live tree was only read (to build the copy); no repo file changed, nothing committed, no restart, no POST, no paid call. The work ran in `%USERPROFILE%\t1s\` (outside OneDrive and outside the CFA-protected folders), with a scratch git repo for the diff.
**Evidence package (outside the repo):** `~/.claude/projects/<project>/brainmap_t1_2026-10-16/build_1.5/`: `T1_celestial_sentinel.patch` (113,307 B), `FILES.tsv` (each file's hash in the live tree at copy time and after the change), `changed_files/` (the 17 files), `baseline_results.txt`, `full_results.txt`, the mutation scripts, the fixture builder, and `manifest.txt` (the 171 copied files).

### The copy
- Built with the Rodin package's `build_from_live.py`: 171 tracked and untracked files from the live nested tree, **including the peers' uncommitted edits** (the baseline the patch applies to). No `.env*`, logs, `kernel_memory` or Chroma data.
- `main.py`, `core/celestial_middleware.py`, `temporal/celestial_clock.py`, `memory/the_hoard.py` and `runtime/swds_simulator.py` were checked hash-identical to the live tree.

### Baseline (the copy unchanged, full suite, MEASURED)
`TOTAL passed=441 failed=3 errors=0 timeouts=0 files=34 wall=746s`. The 3 failures exist **before** this change:
- `test_hoard_schema_v2.py::test_the_hoard_creates_kernel_memory_dirs` and `::test_core_identity_file_contents` fail because a peer's uncommitted `memory/the_hoard.py` edit removed the creation of `core_identity.txt` (identity moved to Starfire). This is a real regression in the live working tree that is not T1's, and its owner should know.
- `test_systems_audit_and_protocols.py::test_voltron_protocol_registered_in_todo_and_config` is the known environment-only failure (it needs a root-repo file).

### What was built (17 files: +1,342 / −431)
| File | Change |
|:--|:--|
| `temporal/celestial_clock.py` | `CelestialFrame` and `FRAME_1`; `compute_4d_coordinates(at=None, frame=None)`; per-dimension references; Kepler period as a parameter; `DualTemporalEngine.set_frame()` and a `frame` key in `/clock` and `/clock/full`. Without a frame the output is exactly today's. The D-20 note sits next to `BASE_EPOCH` |
| `config/celestial_frames.yml` (new) | The registry: frame 1 (legacy) and frame 2 (active), with their sources |
| `temporal/celestial_sentinel.py` (replaces the 15-line stub) | Registry loader and validator (named errors); `CelestialStamp`; `stamp()`, `ccid()`, `vector()`, `frame_constants()`; the only checkpoint writer (atomic; start, every 300 s, stop; in `local_dbs/celestial/`); the reboot delta from the previous checkpoint (new path, then the legacy file, read only); `status()`; a loud frame-1 fallback |
| `core/celestial_middleware.py` | Thin wrappers over the Sentinel. **The self-HTTP call is gone**; no file is opened; the public names are kept |
| `main.py` | Lifespan: Sentinel start plus the checkpoint timer, and the stop checkpoint at shutdown. Response headers from one stamp, plus `X-Celestial-Frame`. `/clock?frame=N`. `GET /celestial/checkpoint` is **read-only** (`status()`). New `GET /celestial/frame` |
| `runtime/swds_simulator.py` | R6/S5: the name `…_CDT_CEL-F2-{rot}deg_SWDS_Report.md` comes from a real stamp, with the true CDT/CST label. The body has `Report Written At (UTC)` and the frame-2 vector. Without a stamp the name says `CEL-UNSTAMPED` and the body gives the error, never a made-up value. `REPORTS_DIR` is a module constant (so tests can redirect it) |
| `memory/the_hoard.py` | `HoardNode.celestial_stamp` (optional, carried by `to_dict`/`from_dict`; **no stamp is invented for nodes loaded from disk**). `commit_node_v2(..., celestial_stamp=None)` fills the anchor's `t` only when it is missing or 0. Crystallizations take time, CCID and stamp from one stamp. `commit_node()` passes a stamp through |
| `evolution/phoenix_forge.py` | `t` = creation time; the generation counter moves to `generation`; `celestial_stamp` in the output |
| `sensory/cheshire_cat.py` | The cycle's commit uses Phoenix's CCID and stamp |
| `memory/database/metatron_deploy.py` | The session CCID from the Sentinel |
| `static/dashboard.html`, `static/celestial_clock_live.html` | Constants come from `GET /celestial/frame` (frame 1 only as a labelled fallback); the frame is shown next to the grid bucket |
| `tests/conftest.py` | Autouse fixture: the Sentinel's checkpoint paths point into each test's `tmp_path` (R4) |
| `tests/test_celestial_sentinel.py` (new), `tests/fixtures/almanac_2026_2036.json` (new) | 18 tests (§7 of the design) and the Tier 1 almanac fixture (USNO 2026 phases and aphelion, 136 NASA new moons and 11 Espenak perihelia, 2026–2036) |
| `tests/test_celestial_time_adr001.py` | The test that wrote the live checkpoint now checks the Sentinel's (tmp) checkpoint and asserts the legacy file is untouched. The two tests that patched the removed HTTP cache now check the stamp path |
| `tests/test_systems_audit_and_protocols.py` | The stub's True-flag test is replaced by a test of the Sentinel's measured status (ADR-003) |

**Deviations from the design (stated, small):**
- The Hoard schema string stays "2.1": `celestial_stamp` is an additive optional field, and a test pins the telemetry's "2.1".
- Shiva lenses (`lenses.py`) were not edited: they call `get_celestial_timestamp()`, which now comes from a stamp with no HTTP call, so they are migrated through the wrapper.
- Line endings of the files written whole were normalized to CRLF, like their originals.

### Tests (MEASURED, verbatim totals)
- **New and changed clock tests:** `tests/test_celestial_sentinel.py` 18 passed; `tests/test_celestial_time_adr001.py` 7 passed (`TOTAL passed=25 failed=0`). The one warning is Starlette's test client (`anyio.abc.BlockingPortal` deprecation), as in the other route tests.
- **Full suite on the changed copy:** `TOTAL passed=459 failed=3 errors=0 timeouts=0 files=35 wall=830s`.
  - The 3 failures are the same 3 tests that fail on the unchanged baseline (above). No new failure.
  - 459 = the baseline's 441 + the 18 new tests.
  - The run used the test file before 1,000 parity instants with a non-default σ and longitude were added (after M3c). That file was re-run on its own afterwards: 18 passed.
- **Stamp at the end of the run (GET `/clock`):** 2026-10-16 03:13:13 CDT | 2026-10-16T08:13:13Z | rotation 272.1386°, lunar 0.7771, orbit 0.2272, ROT_270_ORB_20 (frame 1; live SWDS still in phase 3). **Usage:** 5-hour window 13%, weekly 76%.
- **Mutation checks** (break one behaviour, run its test, restore with git):

  | Mutation | Result |
  |:--|:--|
  | M1 SWDS name back to the constant | caught |
  | M2 the checkpoint route writes | caught |
  | M3 frame-1 float order changed (`x*(360/86400)` → `x/86400*360`) | **not caught: an equivalent change.** At the clock's 4-decimal output the results are identical at all 10,000 instants |
  | M3b frame-1 rotation uses the sidereal day | caught |
  | M3c frame-1 ignores the engine's own σ and longitude | caught, **after a test was added**. My first M3c run did not run at all (two test paths passed as one argument); the gap it revealed (no test with a non-default σ or longitude) is now covered by 1,000 more parity instants |
  | M4 frame-2 perihelion moved 3 days | caught |
  | M5 anchor `t` no longer filled | caught |
  | M6 checkpoint written in place (not atomic) | caught |
  | M7 the registry's frame-1 check removed | caught |

- **The pages' JavaScript:** both inline scripts pass `node --check` (Node 24.21.0); no reference to the removed constants remains; the pages' formula gives 187.3541°, 0.1787, 0.7792 at 06:34:05Z, the same as the Python stamp.
- **Secret scan of the patch:** 1,350 added lines, 0 secret-shaped matches.

### What is true now, and what is not
- **True (in the isolated copy, tested):**
  - one stamp function feeds the Hoard, Phoenix, crystallizations, Cheshire's commits, SWDS reports, CCIDs, response headers, the checkpoint and the displays;
  - frame 2 is active and matches the almanac;
  - frame 1 is unchanged for old stamps;
  - the checkpoint has one atomic writer outside git, and its route is read-only;
  - no test writes the checkpoint of its tree.
- **Not true yet (live):** nothing is applied. The live kernel still runs the old middleware with frame 1, and tonight's SWDS report will still be named `CEL-282.85deg`.

### Next: 1.6, apply to the live tree (two separate gos)
1. **Copy the 17 files into the live nested tree** with `cmd.exe /c copy`, after re-checking that each live file still has the hash in `FILES.tsv`. Any drift stops the copy.
2. **Restart the kernel.** Only when `/swds/status` is AWAKE (after the 07:00 wake), with `kernel_ctl.ps1 restart` and no `-Force`.
3. **Then 1.7 (read-only):**
   - `/clock` shows frame 2;
   - `GET /celestial/checkpoint` writes nothing;
   - `local_dbs/celestial/checkpoint.json` appears and refreshes within 5 minutes;
   - the next naturally written Hoard node and the next SWDS report carry the stamp.
4. **Commits are separate gos:**
   - R4's clock-only commit stages only T1's hunks; the identity hunks in `the_hoard.py` stay unstaged for their owner;
   - untracking the old `config/celestial_checkpoint.json` (S3).

---

## 1.6, first action: copy into the live tree (no restart, no commit)

**Stamp (GET `/clock`, HTTP 200):** 2026-10-16 03:58:03 CDT | 2026-10-16T08:58:03Z | rotation 283.3455°, lunar 0.7781, orbit 0.2272, ROT_270_ORB_20 (frame 1; live SWDS in phase 3). **Usage:** 5-hour window 13%, weekly 76%.
**The Architect's go:** "Go: T1 step 1.6, first action only. Copy the 17 files into the live tree after the hash check, verify, report, and stop. No restart and no commit yet."

### What was done (MEASURED)
1. **Drift gate.** Every one of the 17 live target files still had the hash it had when the isolated copy was built (`FILES.tsv`, column `live_at_copy_sha16`): 0 drift. It was checked twice, the second time immediately before copying. The package's `changed_files/` and the tested copy (`t1s\hb`, scratch commit `74d9d7e`) both matched the `changed_sha16` column.
2. **Copy.** `cmd.exe /c mkdir integra-homebase\tests\fixtures`, then 17 × `cmd.exe /c copy /Y` from `build_1.5\changed_files\`. Each reported "1 file(s) copied".
3. **Verification.**
   - **Files:** all 17 live files now equal the tested files byte for byte (SHA-256).
   - **Git status:** against a snapshot taken just before, `git status` gained exactly the expected entries: ` M` on 10 files that had no uncommitted change before (`phoenix_forge.py`, `metatron_deploy.py`, `swds_simulator.py`, `cheshire_cat.py`, both HTML pages, `celestial_clock.py`, `celestial_sentinel.py`, `conftest.py`, `test_systems_audit_and_protocols.py`) and `??` on `config/celestial_frames.yml`, `tests/fixtures/` and `tests/test_celestial_sentinel.py`. The four files that already carried peer edits (`main.py`, `memory/the_hoard.py`, `core/celestial_middleware.py`, `tests/test_celestial_time_adr001.py`) stay modified, now with T1's change on top. No other path changed.
   - **Nothing staged, nothing committed.** The tests were not run in the live tree (they ran in the copy).
4. **The running kernel is unchanged, as intended** (code loads only at start):
   - same python PIDs 14668/14680 (created 00:07:08);
   - `GET /clock` at 03:59:24 still frame 1, with no `frame` key and no `X-Celestial-Frame` header;
   - `GET /celestial/frame` gives 404.

### Things to know before the restart
- **The kernel is unsupervised again.** The scheduled task reads **Ready**. Its wrapper ended at **2026-10-16 03:13:27** (Task Scheduler events 201 and 102), while python 14668/14680 keep running. That makes 6 launches out of 6 that lost supervision.
  - That time is 14 s after my 03:13:13 `/clock` probe, at the end of the isolated full-suite run.
  - I found no mechanism on my side: no code in the tested copy touches tasks or processes, and the test run used its own processes and folders. The cause is not established.
  - `kernel_ctl.ps1 restart` restarts through the task, so 1.6's restart also restores supervision, until the next loss.
- **Live tree and running code now differ until the restart.** Any start of the kernel loads the new code and switches to frame 2: a planned restart, a reboot or logon launch, or a manual start. Everything copied is the tested change, so an early start means an earlier switch, not untested code.
- **The pages change now.** `/dashboard` and `/clock/live` are read from disk on each request, so a page loaded from now on is the new version. Until the restart, its `GET /celestial/frame` returns 404, and it falls back to frame-1 constants with a visible "frame 1 (fallback)" label on the clock page. It does not break.
- **Tonight's wake report** (07:00) comes from the old code still in memory, so it will be named `CEL-282.85deg` one last time.
- **The two `test_hoard_schema_v2` failures** from the peer's identity edit are still in the live tree; they are not T1's.

### Next: 1.6, second action, the restart (its own go)
- **Restart:** after the 07:00 wake, when `/swds/status` reads AWAKE, run `kernel_ctl.ps1 restart` with no `-Force`, then poll `kernel_ctl.ps1 status` until UP. Startup can take several minutes, and `kernel_ctl` may exit 1 at 120 s while the kernel is still starting.
- **Then 1.7 (read-only):**
  - `/clock` frame 2;
  - `X-Celestial-Frame: 2`;
  - `GET /celestial/frame` 200;
  - `GET /celestial/checkpoint` read-only (file mtime unchanged across two calls);
  - `local_dbs/celestial/checkpoint.json` written at start and refreshed within 5 minutes;
  - the task back to Running;
  - the next natural Hoard node and the next SWDS report carry the stamp.
- **Commits stay separate gos:** R4's clock-only commit (hunk-limited for `the_hoard.py`), then untracking the old checkpoint (S3).

---

## 1.6 second action and 1.7: the new code is live (after a power loss), verified read-only

**Stamp (GET `/clock`, HTTP 200, frame 2):** 2026-10-16 09:23:20 CDT | 2026-10-16T14:23:20Z | rotation 304.6689°, lunar 0.1897, orbit 0.7801, ROT_300_ORB_70, **frame 2** (kernel uptime 00 h 08 m 53 s).

### What happened (MEASURED)
- **The planned restart did not happen; a power loss did it instead.** The Architect's go was "after the 07:00 wake, when /swds/status reads AWAKE, restart with kernel_ctl.ps1".
  - At 05:16:32 the machine powered off (System event 1074 from winlogon; the Architect: "the machine was powered down when battery went out"). The old kernel (00:07) never reached the 07:00 wake.
  - The machine booted at 08:51:29, slept from 09:07:04 to 09:13:21 (Kernel-Power 42/107, then a system-time correction), and the logon task launched the kernel at 09:13:45. Python 3216/3192 started at 09:14:21.
  - That start loaded the live tree, with T1's 17 files: still all 17 hash-equal to the tested files after the power loss.
  - **I did not run `kernel_ctl.ps1` start or restart.** The Architect's later message, "lets get everything booted back up", found the kernel already starting.
- **Startup** (kernel log; `kernel_ctl.ps1 logs`):
  - the SWDS reconciliation woke the deferred cycle ("Machine was asleep during SWDS cycle … Deferred SWDS Report: SWDS_CYCLE_COMPLETE");
  - `Celestial reboot delta: 32083.8s since the last checkpoint (legacy)`;
  - `Celestial Sentinel ONLINE: frame 2, checkpoint every 300s -> …\local_dbs\celestial\checkpoint.json`;
  - `Uvicorn running on http://127.0.0.1:8000`.
  - The first probe at about 09:18 timed out at 30 s while startup was still running; `kernel_ctl status` read UNRESPONSIVE at about 09:21; HTTP 200 from 09:23.

### 1.7 checks (all read-only GETs and file reads)
| Check | Result |
|:--|:--|
| `/clock` in frame 2 | `"frame": 2`; rotation 304.6689° is Baker's mean-solar hour angle (local mean noon 18:04:40Z); lunar 0.1897. The true value is about 0.20 (5.9 days after the 10-10 15:50 UT new moon), within frame 2's ±0.03 |
| Response headers | `X-Celestial-Frame: 2` on `/clock`, `/swds/status` and `/rodin/telemetry` |
| `/clock?frame=1` / `?frame=9` | frame 1 values (rotation 4.9489°, lunar 0.7858, orbit 0.2279, `"frame": 1`) / 404 |
| `GET /celestial/frame` | 200; frame 2 constants (rotation ref 1784116800, lunar ref 1784022180, orbit ref 1767460500, period 31,558,310.6 s, σ 1.0), `frame_fallback: false` |
| `GET /celestial/checkpoint` is read-only | two calls at 09:24: checkpoint mtime unchanged (09:21:26.217), `writes_since_boot` 2 and 2; no decorative literals in the body |
| Sentinel status | registry valid (sha16 `58f55575e544d3c1`, matches the tested file), active frame 2, `frame_fallback` false, σ 1.0, `clock_stepped_back` 0, `last_error` none; stamps since boot by 09:24: http_response 8, checkpoint 2, swds_report 1, ccid 1 |
| The checkpoint: written at start, then on the timer | `local_dbs/celestial/checkpoint.json` (git-ignored): start write 09:15:31, timer writes 09:21:26 and 09:26:37. The record has `writer: celestial_sentinel`, `frame: 2`, `label: ROT_300_LUN_10_ORB_70` |
| The legacy tracked checkpoint is no longer written | `config/celestial_checkpoint.json` mtime still 2026-10-16 00:19:42 |
| SWDS report (R6, S5) | **`2026-10-16_09-15-31_CDT_CEL-F2-302.71deg_SWDS_Report.md`**. Body: "Report Written At (UTC): 2026-10-16T14:15:31Z" and "Frame 2 \| Earth Rotation 302.7143° \| Lunar 0.1895 \| Orbit 0.7801 \| ROT_300_LUN_10_ORB_70". 302.71° checks by hand from frame 2's formula at 14:15:31Z. **No more 282.85** |
| Dashboard | `/dashboard` is served with the `fetch('/celestial/frame')` code |
| Supervision | task "Integra Genesis Kernel" Running, PIDs 3216/3192 (`kernel_ctl status`) |
| A naturally written Hoard node with `celestial_stamp` | **Open.** No shard has been written since boot (no cognitive cycle or SWDS node yet). Check again after the next natural write |

### Notes
- **The reboot delta overstates this one downtime.** 32,083.8 s is measured from the legacy checkpoint (00:19:42), because the old code wrote no timed checkpoints. The real downtime was 05:16:32 to 09:14:26, about 3 h 58 m (DERIVED from System 1074 and the process start). From now on the 300 s timer bounds it.
- **Slow responses (MEASURED, not caused by T1 as far as I can tell).** `kernel_ctl status` measured 18.3 s on `/clock` at about 09:24 (HEALTH=SLOW). Four probes at 09:25:44–09:26:00 took 6.39, 0.16, 11.78 and 0.04 s. CPU load read 100%, with the Gemini app, Explorer, OneDrive and three Claude processes the largest CPU users. This is the same pattern as 2026-10-15 (machine saturated; the kernel task runs at below-normal priority). A stamp is arithmetic, microseconds per response.
- **The kernel log shows `"WebSocket /" 403`.** Some local client tried a WebSocket on `/` right after startup and was refused. Not T1; the source is unknown.
- **Unchanged and still open:** the two `test_hoard_schema_v2` failures from the peer's `the_hoard.py` identity edit.

### What remains for T1 (as of 09:27)
1. The Hoard-node stamp seen live on the next natural write (read-only check).
2. **Commits (each its own go):**
   - R4's clock-only commit of T1's files, with `the_hoard.py` staged hunk-limited so the peer's identity hunks stay out, plus the pre-commit forbidden-path check;
   - untracking `config/celestial_checkpoint.json` (S3).
3. Then the closing T1 report and gate K's tally for T1.

---

## R4: the clock-only commit

**Commit `95a7aab`** in the nested repo, branch `phase-e-dragon-rodin-flight`, git time 2026-10-16 09:50:46 CDT. **Not pushed:** ahead 3; `origin/phase-e-dragon-rodin-flight` is still `957a997`. The root repo is untouched: its `integra-homebase` gitlink stays ` M`, and recording it needs its own go. The Architect's words: "prepare R4's clock-only T1 commit … wait for my word before committing", then "Commit the 18 staged files in the nested repo with the prepared message. No push."

### What it holds (18 files, +1,528 / −368)
- **Whole files:** T1's 17 files, minus `memory/the_hoard.py`, plus `tests/test_rodin_supervisor.py`. This set includes the peer's clock pieces T1 built on: the ADR-001 edit in `core/celestial_middleware.py` and `main.py` (whose uncommitted hunks were all clock-related, MEASURED), and `tests/test_celestial_time_adr001.py`.
- **`memory/the_hoard.py`:** HEAD plus T1's hunks only. It was built with `git merge-file` (current = live file, base = live at copy time, other = HEAD) and staged with `hash-object` and `update-index`; the working file was not touched. The peer's identity hunks (the `core_identity.txt` creation moved to Starfire) stay unstaged, exactly as they were.
- **`tests/test_rodin_supervisor.py`:** added after the first test run of the commit tree. HEAD's version kept a strict xfail documenting the frozen clock, which now unexpectedly passes and so fails. The peer's uncommitted edit (2026-10-15 20:44; one hunk) removes exactly that xfail.
- **Left out:** `core/dragon_engine.py`, `core/starfire_protocol.py`, `config/rodin_memory_map.yml`, the deleted `config/Constructionreconfigure.md`, the files the kernel writes at runtime (`config/celestial_checkpoint.json`, `runtime/swds_state.json`, `kernel_memory/*`), and every untracked file, `docs/brainmap/` included.

### Checks before committing (MEASURED)
- "no forbidden paths staged", checked at staging and again immediately before the commit.
- **Secret scan:** 0 matches. With the autocrlf override the scanner reads a superset of lines (7,763), so the scan is stricter, not looser. No personal paths in the added lines.
- **The commit's own tree, tested in isolation** (`git checkout-index` of the index, 169 files, full suite):
  - first run, 17 files: 460 passed, 2 failed (the strict xfail above, and Voltron);
  - after staging the test follow-up: **461 passed, 1 failed**, the environment-only `test_voltron_protocol_registered_in_todo_and_config`.
  - In this tree the two `test_hoard_schema_v2` identity tests pass, because the peer's identity change is not in it.
- After the commit: nothing staged; the committed `the_hoard.py` blob is `156c7e9`, the one that was tested.

### What remains for T1 (as of 09:50)
1. The Hoard-node stamp seen live on the next natural write (read-only).
2. Untracking `config/celestial_checkpoint.json` (S3), its own go.
3. Recording the new nested commit in the root repo's gitlink, and any push, only on the Architect's word.
4. Then the closing T1 report and gate K's tally for T1.

---

## S3: the legacy checkpoint untracked

**Commit `c7053f1`** in the nested repo, git time 2026-10-16 10:11:42 CDT. **Not pushed:** ahead 4; origin still `957a997`. The Architect's words: "prepare S3 … wait for my word", then "Commit the staged S3 change (untrack plus the .gitignore rule) in the nested repo with the prepared message. No push."
- **The untrack:** `git rm --cached config/celestial_checkpoint.json`. The file stays on disk unchanged (sha16 `D7C868BF06416D80`, mtime 2026-10-16 00:19:42).
- **The ignore rule:** `.gitignore` gains one rule (`config/celestial_checkpoint.json`, line 37) with a comment, so the file cannot be swept back in. Line endings were kept CRLF in the working tree.
- **Checks:**
  - "no forbidden paths staged"; secret scan 0 matches.
  - Only the Sentinel's read-once legacy path refers to the file in code; the other references are historical documents.
  - The commit's own tree, exported without the file: **461 passed, 1 failed** (the environment-only Voltron test), the same as `95a7aab`'s tree.
- **After the commit:** nothing staged; the file is ignored and no longer appears in `git status`.

### What remains for T1
1. The Hoard-node stamp seen live on the next natural write (read-only).
2. Recording the nested commits (`95a7aab`, `c7053f1`) in the root repo's gitlink, and any push, only on the Architect's word.
3. Then the closing T1 report and gate K's tally for T1.
