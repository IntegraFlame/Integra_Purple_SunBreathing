# Celestial Sentinel: design (Brain Map T1, step 1.4)

**Status:** design only. Nothing is built, applied or committed. Build is step 1.5 (in an isolated copy), apply and restart are step 1.6 (two approvals), verification is step 1.7.
**Stamp (GET `/clock`, HTTP 200):** 2026-10-16 02:31:36 CDT | 2026-10-16T07:31:36Z | rotation 261.7352°, lunar 0.7761, orbit 0.2271, ROT_240_ORB_20 (frame 1; kernel uptime 02 h 24 m).
**Inputs:** `Task01_REPORT.md` (steps 1.1–1.3: gaps G1–G15, frame 2 tested against USNO/NASA), the Architect's rulings R1–R6 (2026-10-16), `docs/DESIGN_DECISIONS_10_15_26.md` §4.3 and §5.3 (D5, A4), blueprint ADR-001 and ADR-003, pointer v1 (`~/.claude/plans/structured-spinning-codd.md`).
**Provenance labels:** MEASURED, DERIVED, CONSTANT, CLAIMED, as in the report. Everything under "Design" is a PROPOSAL.

## 1. Requirements

### Functional
| Id | Requirement | Source |
|:--|:--|:--|
| F1 | One `stamp(kind)` that every stamping writer calls. It returns civil time, the celestial vector in the active frame, the frame id and a provenance code | D5 §5.3(a); G1, G4 |
| F2 | A frame registry holding frame 1 (today's constants) and frame 2 (R1 (c), R2, R5). One active frame. Stamps from different frames are never compared | R1; pointer v1 |
| F3 | One checkpoint writer: atomic, on a timer, plus at start and stop. The checkpoint is a "last seen alive" record and is never a time source | A4; ADR-001 items 1–2; G6 |
| F4 | `GET /celestial/checkpoint` becomes read-only and serves the Sentinel's status | A4; G6 |
| F5 | Writers move to `stamp()`: Hoard nodes and anchors, Phoenix, SWDS reports, CCIDs, Daily Planet, response headers, Shiva lenses, Metatron session ids | G1–G4 |
| F6 | Displays show the active frame and its id: `/clock`, `/clock/full`, `/clock/sync`, the dashboard and the clock-live page | S4 below |
| F7 | σ is fixed at 1.0; `apply_zenkai_recalibration()` stays unwired, and the drift loop is recorded as an open design item | R5; G10 |
| F8 | SWDS reports carry the real vector, `report_written_at` and the frame id | R6; G2; ADR-001 item 4 |
| F9 | `status()` feeds Itachi's link report (interface only; Itachi is not built) | D6 §4.3 |

### Non-functional
- **In the kernel process, with no new port** (DESIGN_DECISIONS §7).
- **No network.** The kernel stops calling its own `/clock/full` over HTTP (ADR-001 option A; today `get_celestial_timestamp()` does).
- **A pure core.** The vector is a function of (instant, frame) only, so it can be computed for any instant and tested offline.
- **Loud failure.** A broken registry or a failed checkpoint write shows up in the log and in `status()`; it never silently produces values.
- **No new store** beyond the checkpoint file (ADR-005 rule), and no runtime write into a git-tracked file (S3).
- **Cost:** a stamp is arithmetic plus a Kepler solve. Microseconds are expected (DERIVED); 1.5 measures it.
- **The ruled math stays as it is.** Only the reference constants change by frame (R1 (c)).

## 2. Current state (MEASURED in steps 1.1–1.3, with one correction)
| Writer or display | Today | Where |
|:--|:--|:--|
| Clock source | `celestial_time()` = `time.time()` (the uncommitted ADR-001 edit, running since 00:07) | `core/celestial_middleware.py:339-359` |
| Checkpoint | 3 writers (startup sync, `GET /celestial/checkpoint` twice per call, `get_celestial_timestamp()`); plain `open('w')`; the path is git-tracked | middleware `:109-120`, `:441-449`; `main.py:127-140`, `:1419-1437` |
| Hoard node | `created_at` = true time; no celestial block; `spacetime_anchor.t` = 0 in 258 of 304 shards | `memory/the_hoard.py:90-114`, `:608-657` |
| Phoenix node | anchor `{x 1.0, y 0.5, z 0, t = generation counter}` | `evolution/phoenix_forge.py:462-484` |
| Daily Planet node | **correction to 1.1:** anchor x, y, z, `orbital_index` = the frame-1 vector (rot, lunar, orbit, σ) and `t` = true time, in 40 shards. With the 2 shards that name the fields, **42 of 308 shards carry the frame-1 vector**, not 2 as reported at 00:39 | `tools/daily_planet.py:474-484`, `:556-565` |
| Save-state sync | anchor x, y = Baker's latitude and longitude (constants); `t` from the save state's stamp | `the_hoard.py:899-910` |
| Crystallization | anchor `{0, 0, 0, t = true time}`; `CCID_CRYSTAL_<unix>_<n>` | `the_hoard.py:1070-1078` |
| SWDS report | name `CEL-282.85deg` (a constant: calls a method that does not exist); no `report_written_at` | `runtime/swds_simulator.py:162-177` |
| SWDS state | `runtime/swds_state.json` (git-tracked), true time since the fix | `swds_simulator.py:14`, `:59`, `:86`, `:133` |
| CCIDs | `int(time.time())` or `celestial_time()` in 8 places | `sensory/cheshire_cat.py:361`, `memory/database/metatron_deploy.py:121`, `phoenix_forge.py:464`, `the_hoard.py:899,1078`, middleware `:362-371`, `scripts/trigger_swds.py:21`, `scripts/enter_swds.py:19` |
| Response headers | 4 `X-` headers with the frame-1 vector (uncommitted middleware) | `main.py`, `inject_celestial_temporal_headers` |
| Displays | `/clock` and `/clock/full` from `DualTemporalEngine` (frame 1). **The dashboard and the clock-live page compute the vector in JavaScript with frame-1 constants** | `static/dashboard.html:794-920`, `static/celestial_clock_live.html:273-330` |
| Unused config | `config/celestial_seed.json` holds the frame-1 constants; no Python reader found | — |
| SWDS on the live clock | **Observed:** slept at 2026-10-16 02:00:59 CDT (`/swds/status` `sleep_initiated_at`), as derived in step 1.1; phase 3 at 02:31 | MEASURED |

## 3. High-level design
```
config/celestial_frames.yml  (registry: frames 1 and 2, active_frame; append-only; validated at load)
        |
        v
temporal/celestial_clock.py  compute_4d_coordinates(at, frame)        <- the ruled math, references per frame (S1)
        ^
        |  pure calls
temporal/celestial_sentinel.py  (the Sentinel; replaces the 15-line stub)
   stamp(kind, at=None) -> CelestialStamp --> Hoard nodes, Phoenix, SWDS reports, CCIDs, Daily Planet,
                                               response headers, Shiva lenses, Metatron session id
   ccid(prefix, stamp)
   checkpoint task (lifespan: at start, every 300 s, at stop) --> local_dbs/celestial/checkpoint.json (atomic) (S3)
   status() --> GET /celestial/checkpoint (read-only), Heimdall health field, Itachi link input
   frame_constants() --> GET /celestial/frame (read-only) --> dashboard.html, celestial_clock_live.html
core/celestial_middleware.py  keeps its public names as thin wrappers over the Sentinel (compatibility):
   celestial_time() -> time.time(); celestial_ccid() -> Sentinel.ccid(); get_celestial_timestamp() -> from stamp(), no HTTP
```

## 4. Deep dive

### 4.1 The stamp record (`CelestialStamp`, frozen dataclass; JSON key `celestial_stamp`)
| Field | Type and unit | Range | Meaning |
|:--|:--|:--|:--|
| `schema` | str | `"cstamp/1"` | record version |
| `frame` | int | 1, 2, … | registry id; stamps of different frames are never compared |
| `unix` | float, s (UTC) | — | the instant (`time.time()` unless `at` is given) |
| `utc` | str | ISO-8601 `Z` | civil UTC |
| `civil` | str | ISO-8601 with offset, America/Chicago | civil local time (CDT/CST) |
| `rot_deg` | float, ° | [0, 360) | frame 2: Baker's local mean-solar hour angle |
| `lun` | float | [0, 1) | frame 2: fraction of the lunation since the reference new moon |
| `orb` | float | [0, 1) | eccentric anomaly / 2π from perihelion |
| `turn` | int | ≥ 0 after the reference | perihelion passages since the frame's reference |
| `sigma` | float | 1.0 | fixed (R5) |
| `grid` | str | `ROT_{30°}_ORB_{10%}` | the live `grid_bucket` format, for compatibility |
| `label` | str | `ROT_{30°}_LUN_{10%}_ORB_{10%}` | pointer v1's human label (adds LUN; C-16) |
| `kind` | str | memory-map kind or a stamp kind (`hoard_node`, `swds_report`, `checkpoint`, `http_response`, `ccid`, …) | who asked |
| `provenance` | int | pointer v1 codes 0–15 | 1 = true clock at creation; 2–6 only for backfill (not in T1) |
| `frame_fallback` | bool | — | true only if the registry failed and frame 1's built-in constants were used (§4.10) |

Example (DERIVED from step 1.3's frame-2 values at 2026-10-16 06:34:05Z):
```json
{"schema": "cstamp/1", "frame": 2, "unix": 1792132445.131, "utc": "2026-10-16T06:34:05Z",
 "civil": "2026-10-16T01:34:05-05:00", "rot_deg": 187.3541, "lun": 0.1787, "orb": 0.7792, "turn": 0,
 "sigma": 1.0, "grid": "ROT_180_ORB_70", "label": "ROT_180_LUN_10_ORB_70",
 "kind": "hoard_node", "provenance": 1, "frame_fallback": false}
```
About 350 bytes per node as JSON (DERIVED). The record keeps `unix`; pointer v1's "no Unix epoch" rule applies to the 16-byte pointer (T3.5), not to this record. No Braille anywhere (display only, and not here).

### 4.2 The frame registry (`config/celestial_frames.yml`, S2)
```yaml
schema: celestial_frames/1
active_frame: 1            # becomes 2 at the step-1.6 restart (S4)
math_module: temporal/celestial_clock.py
frames:
  - id: 1
    name: legacy single epoch
    status: legacy          # valid for reading stamps made before the switch
    rotation: {ref_unix: 1785052800.0, period_s: 86400.0, anchor_lon: -91.1673}
    lunar:    {ref_unix: 1785052800.0, period_s: 2551442.8}
    orbit:    {ref_unix: 1785052800.0, period_s: 31558149.763, eccentricity: 0.0167086}
    sigma: 1.0
    note: "BASE_EPOCH decodes to 2026-07-26T08:00Z although labelled 2026-07-15T12:00Z (D-20)"
  - id: 2
    name: almanac references (R1 c, R2, R5; 2026-10-16)
    status: active
    rotation: {ref_unix: 1784116800.0, ref_utc: "2026-07-15T12:00:00Z", period_s: 86400.0, anchor_lon: -91.1673}
    lunar:    {ref_unix: 1784022180.0, ref_utc: "2026-07-14T09:43:00Z", period_s: 2551442.8, source: "USNO API 4.0.1 = NASA GSFC phases"}
    orbit:    {ref_unix: 1767460500.0, ref_utc: "2026-01-03T17:15:00Z", period_s: 31558310.6, eccentricity: 0.0167086,
               source: "USNO seasons API; period = least-squares over Espenak perihelia 2001-2100"}
    sigma: 1.0
    verified: "Moon within 0.81 d at 136 new moons 2026-2036; orbit within 1.32 d at 11 perihelia (Task01_REPORT 1.3)"
```
Rules: ids are append-only and never reused. A frame's constants are never edited; a correction is a new frame. The loader validates the schema, unique ids, that `active_frame` exists, and that frame 1 equals the module's built-in constants. `config/celestial_seed.json` (frame-1 constants, no reader) is marked legacy in its own text, or removed, on a go.

### 4.3 Frame-aware math (S1)
**Recommended (A'): parameterize the ruled module; one implementation.**
- Add a `CelestialFrame` dataclass to `temporal/celestial_clock.py`.
- `compute_4d_coordinates(self, at: float | None = None, frame: CelestialFrame | None = None)`. `frame=None` means frame 1, byte-for-byte today's behaviour; `at=None` means `time.time()`.
- The three formulas are unchanged. Each dimension reads its own reference and period from the frame.
- The Kepler solver is untouched.
- The file's sha16 (`4199779CF1F2D740`) changes. A parity test pins frame 1 to today's output at 10,000 instants.

**Alternative (B):** the Sentinel holds its own copy of the three formulas and imports the solver. The ruled file stays byte-identical, but there are two implementations to keep in step.

### 4.4 `stamp(kind, at=None)`
- Read `at` (default `time.time()`); take the active frame; compute the vector; build the record; increment the counter for that kind; return. No I/O.
- **Clock guard:** if `at` is more than 1 s earlier than the previous stamp's `at`, count `clock_stepped_back` in `status()` and still stamp. NTP or a manual clock change can do this; the HLC in `celestial_clock.py` remains the causal order.

### 4.5 CCIDs
`ccid(prefix="CCID", stamp=None)` returns `f"{prefix}_{int(stamp.unix)}"`, so a node's CCID and its stamp come from the same instant. The existing forms stay: `CCID_<unix>`, `CCID_CRYSTAL_<unix>_<n>`, `CCID_DAILY_PLANET_DP_<local>_<hash>`, `CCID_LOBE_*`. Two nodes in the same second can collide today, and the design does not change that; it is noted for T2.

### 4.6 The checkpoint (F3, S3)
- **Path:** `local_dbs/celestial/checkpoint.json`. `local_dbs/` is git-ignored (MEASURED, `.gitignore:35`). On the first start, the Sentinel reads the old tracked `config/celestial_checkpoint.json` once, for the reboot delta. Untracking the old file (`git rm --cached`) needs its own go. ADR-005's `C:\IntegraData` is the later home.
- **Record:** `{schema: "cckpt/1", writer: "celestial_sentinel", pid, frame, unix, utc, civil, vector, boot_unix, written_at}`.
- **Atomic write:** a temporary file in the same folder, then `os.replace`, the same pattern as the Hoard's `_write_json_atomic` (`the_hoard.py:194-206`).
- **When:** at start (after the previous checkpoint is read for the reboot delta), every 300 s (a lifespan task), and at stop. Downtime is then known to within 5 minutes.
- **Only writer:** `_persist_checkpoint()` and `sync_celestial_checkpoint_now()` delegate to the Sentinel or are removed. A test fails if any other module opens the path for writing.

### 4.7 Read-only routes
- **`GET /celestial/checkpoint`** returns `status()`: active frame; last stamp (unix, kind); stamps since boot by kind; checkpoint (path, age, last write, last error); reboot delta; registry (path, sha16, valid); σ = 1.0 (fixed); `clock_stepped_back` count. **It writes nothing**; a test calls it twice and asserts the file's mtime did not change. The `status: SOVEREIGN_GROUNDED` and `all_systems_true: True` literals go (ADR-003, G13).
- **`GET /celestial/frame`** (new) returns the active frame's constants, so the JavaScript pages compute the same vector.

### 4.8 Writer migration, in order (each one is a separate, testable change)
1. **Checkpoint and routes.** The middleware delegates; the startup sync becomes the Sentinel's first checkpoint; `GET /celestial/checkpoint` becomes read-only; `get_celestial_timestamp()` is rebuilt from `stamp()` with no HTTP call (callers: the route and `evolution/shiva_action/lenses.py:460-480`).
2. **SWDS reports (R6, F8).** `swds_simulator.py:167-177` takes the vector from `stamp("swds_report")`. The name becomes `{local date-time}_CDT_CEL-F2-{rot:.2f}deg_SWDS_Report.md`, so frame-2 names cannot be mistaken for frame-1 names (S5). The body gets `report_written_at` (UTC) and the stamp block.
3. **Hoard nodes.**
   - `HoardNode` gains an optional `celestial_stamp` slot (schema 2.2), carried by `to_dict` and `from_dict` and set at creation when absent.
   - `commit_node_v2()` fills `spacetime_anchor["t"]` with `stamp.unix` only when `t` is missing or 0, so callers that pass a real `t` keep it.
   - Phoenix's generation counter moves from `t` to `spacetime_anchor["generation"]` (`phoenix_forge.py:468-473`).
   - `x`, `y`, `z` stay as callers write them. What they mean is the Atlas question (T3/T4), and the Daily Planet's vector-in-x/y/z remains readable.
4. **CCIDs.** `cheshire_cat.py:361`, `metatron_deploy.py:121`, `phoenix_forge.py:464`, `the_hoard.py:899,1078` and `celestial_ccid()` use `Sentinel.ccid()`. The two SWDS scripts already take the time from `/clock` and stay as they are.
5. **Response headers.** They add `X-Celestial-Frame`, and the vector comes from the Sentinel.
6. **Displays (S4).**
   - `/clock` and `/clock/full` use the active frame and add `"frame"`; `?frame=1` shows frame 1 for comparison.
   - `/clock/sync`'s 56-byte packet has no frame field. It is documented as "active frame"; changing the binary layout is out of T1.
   - Both HTML pages fetch `GET /celestial/frame` at load, keep their local animation, and show the frame id. If the fetch fails they fall back to frame 1 with a visible "frame 1 (fallback)" label.
7. **Not moved in T1:**
   - The 634 other direct clock reads. They time durations and log lines; they are not stamps. A ledger does not exist yet (ADR-002).
   - The two `generate_hoard_manifest()` functions (G14). `stamp()` replaces them for stamping; they stay for their current callers (`runtime/antigravity_runner.py:56`, and inside the metadata helper until step 1 of this list removes it), and their docstrings say so.
   - The old stub's class `CelestialSentinelAgent` is imported only by `tests/test_systems_audit_and_protocols.py:286-289` (`test_celestial_sentinel_calls_true`), which asserts its True flags. That test is replaced by test 3 below (ADR-003).

### 4.9 Historical data
Nothing is rewritten (ADR-001: "re-label, not rewrite").
- Frame-1 values already stored stay frame 1: the checkpoint history, 40 Daily Planet anchors, save-state stamps and SWDS names.
- A correction note in the Hoard (ADR-001 item 4) lists the frozen-era artefacts: 55 SWDS reports with the constant, report-name dates 7 days behind their file times, and 258 shards with `t = 0`.
- Back-filling `celestial_stamp` into old shards uses pointer v1's provenance codes 2–6. It belongs to T2 or T5, needs its own go, and never presents a back-filled value as measured.

### 4.10 Failure handling
| Failure | Behaviour |
|:--|:--|
| Registry missing or invalid | Log ERROR at startup; `status().registry.valid = false`; stamps use frame 1's built-in constants with `frame_fallback: true`. Loud, never silent |
| Checkpoint write fails | Log WARNING; `status().checkpoint.last_error` set; stamping continues; the next timer tick retries |
| Clock steps back | Counted in `status()`; stamping continues |
| Kepler does not converge | Cannot happen at e = 0.0167 within 100 iterations; covered by a test over 10,000 instants |

## 5. Scale and reliability
- **One process and one user.** Stamps are cheap (to be measured in 1.5).
- **Storage:** about 350 B per node; the 308 existing shards would add about 0.1 MB if back-filled (DERIVED).
- **Checkpoint traffic:** 288 small writes a day into `local_dbs/`, which OneDrive syncs. Acceptable until ADR-005 moves runtime data to `C:\IntegraData`.
- **Restarts:** the reboot delta is now bounded by the 5-minute timer instead of the last on-demand write.
- **Observability:** `status()` through the read-only route and a Heimdall health field.

## 5a. Coverage check: every ruling and gap
| Item | Where this design handles it |
|:--|:--|
| R1 (c), R2 | §4.2 frame 2; §4.3 |
| R3 (Sentinel scope, A4) | §3; §4.6; §4.7 |
| R4 (isolated test, clock-only commit) | §7 test 12; §8 (hunk-limited staging) |
| R5 (σ = 1.0) | §4.1; §4.2 |
| R6 (SWDS constant) | §4.8 step 2; §7 test 9 |
| G1, G3, G4 (stamping) | §4.1; §4.8 steps 3–5; durations excluded (§4.8 step 7) |
| G2 (SWDS name) | §4.8 step 2 |
| G5 (ADR-001 items) | 1 commit (§8); 2 timer (§4.6); 3 test (§7 test 12); 4 `report_written_at` and the correction note (§4.8 step 2, §4.9); self-HTTP removed (§4.8 step 1) |
| G6 (checkpoint writers) | §4.6; §4.7; §7 tests 6–8 |
| G7, G8 (epoch, year) | frame 2 |
| G9 (solar rotation) | kept, documented (§4.1 meaning of `rot_deg`) |
| G10 (σ) | fixed; the revival is open (§9) |
| G11 (no LUN) | `label` field (§4.1) |
| G12 (stub) | replaced (§3); its True-flag test replaced (§4.8 step 7) |
| G13 (literal flags) | checkpoint route in T1 (§4.7); `/clock` stays with ADR-003 (§9) |
| G14 (two manifests) | superseded for stamping, kept for callers (§4.8 step 7) |
| G15 (uncommitted) | §8 |

## 6. Trade-offs and the decisions they need
| Id | Choice | Option A | Option B | Recommendation |
|:--|:--|:--|:--|:--|
| S1 | Where the frame-aware math lives | A': parameterize `celestial_clock.py`. One implementation; the file's hash changes; a frame-1 parity test pins today's behaviour | B: a copy of the formulas in the Sentinel. The ruled file stays byte-identical; two implementations | **A'** |
| S2 | Where the registry lives | A new `config/celestial_frames.yml`, owned by the Sentinel | A `celestial_frames:` section in `config/rodin_memory_map.yml` (pointer v1's idea), a file with uncommitted peer edits | **A**; the memory map can point to it later |
| S3 | The checkpoint file | `local_dbs/celestial/checkpoint.json` (git-ignored); untrack the old file on a go | Keep the tracked `config/celestial_checkpoint.json` (the repo stays dirty after every start) | **A** |
| S4 | The switch to frame 2 | Everything switches at the 1.6 restart (stamps, `/clock`, headers, pages), with `?frame=1` for comparison | Stamps switch first and displays later | **A**: one active frame everywhere, so displays and stamps agree |
| S5 | The SWDS report name | Add a frame marker: `CEL-F2-{rot}deg` | Keep `CEL-{rot}deg` | **A** |

## 7. Tests for step 1.5 (offline, in an isolated copy)
1. **Frame-1 parity:** at 10,000 instants (seeded), `compute_4d_coordinates(at, FRAME_1)` equals today's output exactly (4 dp).
2. **Frame-2 almanac:** a fixture `tests/fixtures/almanac_2026_2036.json` holds the USNO 2026 phases, the 136 NASA new moons 2026–2036 and the 11 Espenak perihelia (public almanac data, with sources). Assert lunar within 0.03, orbit within 0.004, rotation 0° at local mean noon.
3. **Stamp record:** every field present; frame, ranges, `grid` and `label` formats; provenance 1; no Braille.
4. **CCID:** `ccid(stamp)` equals `int(stamp.unix)`; existing forms unchanged.
5. **Registry validator:** missing file, a duplicate id, an unknown active frame, and frame 1 differing from the built-ins each give a named error and `frame_fallback`.
6. **Checkpoint atomicity:** a write interrupted between the temporary file and the replace leaves the old file intact; the record schema is valid.
7. **Single writer:** no module other than the Sentinel opens the checkpoint path for writing (static scan plus a runtime check).
8. **Read-only route:** two calls to `GET /celestial/checkpoint` leave the file's mtime unchanged; the response carries no decorative literals.
9. **SWDS report:** the name carries `CEL-F2-` and the real rotation (never 282.85 unless it is real); the body has `report_written_at` and the stamp.
10. **Hoard:** a committed node has `celestial_stamp`; `t` is filled when absent or 0 and kept when given; Phoenix's counter lands in `generation`.
11. **Headers:** `X-Celestial-Frame` is present and the values match `stamp()`.
12. **Isolation (the R4 fix):** a `conftest` fixture redirects every checkpoint path to `tmp_path`, so no test writes `config/` or `local_dbs/` of the tree it runs in. `tests/test_celestial_time_adr001.py::test_sync_celestial_checkpoint_now_persists_full_vector` gets that fixture.

Then the existing clock, Hoard and SWDS suites, and the full suite in a clean copy built from the live tree, with long timeouts (the machine is often saturated).

## 8. Build, apply and verify (steps 1.5–1.7)
- **1.5 (starts on the Architect's go like every step; nothing live is touched):**
  - build an isolated copy from the live tree (the `build_from_live.py` method from the Rodin package);
  - apply the change in the order of §4.8;
  - run the tests above and the suites;
  - deliver a patch, the file list and the test output verbatim.
- **1.6 (two gos, one per action):**
  - **Copy into the live tree.**
    - `main.py`'s uncommitted peer hunks are all clock-related (MEASURED), so the R4 commit can carry them.
    - `memory/the_hoard.py`'s uncommitted peer hunks are identity changes, not clock. The commit stages only this task's hunks: a hunk-limited patch applied to the index with `git apply --cached`, leaving the identity hunks unstaged for their owner.
    - The pre-commit forbidden-path check runs before any commit.
  - **Restart.** Only while SWDS is AWAKE (`kernel_ctl.ps1` refuses otherwise), so not between about 02:00 and 07:00.
- **1.7 (read-only):**
  - `/clock` shows frame 2 with the expected values;
  - `GET /celestial/checkpoint` is read-only (mtime unchanged);
  - the checkpoint file appears in `local_dbs/celestial/` and refreshes within 5 minutes;
  - the next naturally written Hoard node and the next SWDS report carry the stamp. Creating a node on purpose would need a POST, which needs its own go.

## 9. Still open after this design
- `/clock`'s literal flags (`sync_isolation_verified`, `is_active`, `all_systems_true`; `celestial_clock.py:442-445`; G13). They stay with the Phase 0 ADR-003 task unless the Architect wants them in T1. Only the checkpoint route's literals go in T1.
- The apparent Sun (equation of time, about ±16 min). Frame 2's rotation is the mean-solar hour angle; a later frame could add it.
- σ revival: a real drift measure. The spec's hash comparison cannot measure size; candidate checkpoints are the 2026 eclipses (Feb 17, Mar 3, Aug 12, Aug 28).
- What anchor x, y, z mean (Atlas, T3/T4).
- Back-filling old nodes (T2/T5).
- The Coordinate Beta packet's frame field.
- Same-second CCID collisions.
