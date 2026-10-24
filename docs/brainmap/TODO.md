# Brain Map To-Do

**Source:** `integra-homebase/core/IntegraBrainMap.md` (31 lines, 13 numbered items), turned into a To-Do at the Architect's request (`/engineering:system-design`, 2026-10-15).
**Stamp (GET `/clock`, HTTP 200):** 2026-10-15 23:40:20 CDT | 2026-10-16T04:40:20Z | rotation 218.9201°, lunar 0.7721, orbit 0.2268, ROT_210_ORB_20 (kernel uptime 4 h 02 m).
**The Architect's instruction:** create a To-Do from the map. Do not use agents. Do each task one at a time, write a report after each successful task, and pause for approval to continue.
**Reconciled (2026-10-16, boot session f9e973c9, on the Architect's go; stamp GET `/clock` HTTP 200: 2026-10-16 00:27:29 CDT | 2026-10-16T05:27:29Z | rotation 230.7047°, lunar 0.7732, orbit 0.2268, ROT_210_ORB_20, kernel uptime 00 h 20 m):** this file stays the single To-Do. Merged in from save state `CCID_1792123400` (The Hoard): the Zenitsu order and its two gates, the decided Apophenic role, the cold-tier pointer v1 design (`~/.claude/plans/structured-spinning-codd.md`), the Braille assessment's keep/drop list (`~/.claude/projects/<project>/braille_assessment_2026-10-15/BRAILLE_ASSESSMENT.md`), and the facts measured after the 2026-10-16 00:05 reboot.

## Progress
| Task | What | Status | Report |
|:--|:--|:--|:--|
| T1 | Connect Celestial Time | **closed 2026-10-16 10:29** (frame 2 live; committed `95a7aab`, `c7053f1`, pushed 2026-10-17; gate K tally 6 of 8 live criteria met, 2 open live checks: a Hoard node and a save state; ADR-001 item 4: the skewed stamps are to be rewritten, ruling R8 of 2026-10-16) | `Task01_REPORT.md` (closing report at the top), `T1_CELESTIAL_SENTINEL_DESIGN.md` |
| T2 | Connect the Hoard | **in progress**: 2.1–2.3 done read-only, and re-measured independently 2026-10-16 12:40–12:57 on the Architect's instruction; the first pass (12:05–12:18, the boot session) holds up. Both map versions validate (0 problems) but no kernel code reads the map; 258 shards carry prompts (257 on `origin`) and 40 carry Daily Planet queries (all on `origin`); the save-state sync reads the wrong folder; 8 Hoard-like locations undeclared; 7 holds/kinds gaps; 3 of 15 kinds have no writer that can run. 2.4 rulings decided 2026-10-16 (R1–R8: keep publishing; the map goes live after 2.5 from HEAD; `memory.db` deferred to Phase 2; declare the 8 locations; nothing until T8; the save-state check stays open for the node path; the log waits for ADR-010; D-14: rewrite the stamps). 2.5 is planned (P1–P9, each with its own gates). **P3** (the validator's missing checks) was built and tested in isolation 2026-10-16 15:25–15:38 (473 passed, the same 3 known failures; 9 of 11 mutations killed, 2 equivalent) copied into the live tree on your go (hash-checked), and **committed as nested `e519534`** (2026-10-16 18:35:40; 3 files, +365/−9; pushed 2026-10-17, and the root gitlink records the later `287cf25`). Ruling 2026-10-16: the three kinds with no runnable writer (crystallization, thermo_loop, lobe_chunk) "are false and lead nowhere", so P1 retires them from the map instead of adding a `writer_state` rule; their dead code paths (`auto_crystallize` → `record_loop`; the `ingest_knowledge.py` lobe path) are listed for retirement at a later gate. The Architect accepted the five gap fixes, and **P1 was built and tested in isolation** 2026-10-16 19:30–19:55 (`%USERPROFILE%\t2p1\package`: 478 passed with the 3 known failures, 14 of 14 mutations killed; nothing applied; `metatron_db` kept live because the kernel still opens it). Next: the `metatron_db` ruling, then the apply go, then the commit go | `Task02_VERIFICATION_REPORT.md` (this pass), `Task02_REPORT.md` (first pass), `T2_5_PLAN.md` (the 2.5 plan) |
| T3 | Connect Phoenix Engine and design the Atlas | not started | |
| T3.5 | Coordinate system and Braille points | not started | |
| T4 | Taxonomy labelling | not started | |
| T5 | Connect System, Iteration 1: Knowledge | not started | |
| **Gate K** | Knowledge review: T1–T5 facts and tests; the Architect's go before U | not reached | |
| T5.5 | SWDS and Siesta | not started | |
| T6 | Cheshire Cat: SWDS deep learning, security, Phoenix Force | not started | |
| T6.5 | Connect System, Iteration 2: Understanding | not started | |
| **Gate U** | Understanding review: couplings and failure modes; the Architect's go before W | not reached | |
| T7 | Mathematical expression | not started | |
| T8 | Connect Rodin and hot storage; historical-data test in an SWDS cycle | not started | |
| T9 | Scheduled task: Rodin and Phoenix plot and label in Flight and Land sessions | not started | |
| T10 | Connect System: curriculum wisdom pass | **done 2026-10-16** (20:05–20:31 CDT, on the Architect's word, ahead of the K → U → W order): all 11 documents read in order, each in isolation and then compounded (reading ≈ 11 min, inside the 20-minute budget); unified into five laws, a crosswalk of Integra names to textbook mechanisms, corrections C1–C11 and a provisional design for T1–T9; reference script `integra_atlas_reference.py` (stdlib; 47/47 checks, 10/10 mutants; reproduces the live `/clock`, frame 2). Copied into `task10/` 2026-10-16 23:07 on the Architect's go (16 files, hash-equal; committed and pushed 2026-10-17). Open decisions: the 33 curriculum PDFs on `origin`; the Atlas rulings (meridians, kind → zone, hemispheres, pointer form); the T9 anchor rule; glossary corrections C1–C3 | `task10/Task10_REPORT.md`, `task10/TASK10_MASTER_DOCUMENT.md`, `task10/notes/` |
| **Unification** | Master document and code script, written outside the repo first | not started | |

The Architect's order is kept, grouped in Zenitsu order: **K** (Knowledge: T1–T5, then gate K), **U** (Understanding: T5.5–T6.5, then gate U), **W** (Wisdom: T7–T10), then **Unification**. Parked until after this list: the Braille Atlas four-pass study and its exhaustive report (plan file, section "PARKED").

**Parallel track, parked until the Architect says (save state §5 D):** the embedder-only key route (`RODIN_EMBED_API_KEY`, a Developer API client with Vertex off) is chosen and prepared, not applied: existing suites, mutation checks and a clean full run → apply on a go → the Architect adds the key → restart → `embed_probe_v2.py` pre-flight → one call on a go → pilot re-embed. T8's semantic placement waits on it.

## How the work runs
- **One task at a time, no agents.** Each task: (1) read-only measurement, (2) the questions it needs, batched once at the start, (3) work in an **isolated copy**, never the live repo, (4) apply to the live repo only after approval, (5) verify, (6) report, (7) **stop and wait for "continue"**.
- **Report** (saved as `docs/brainmap/TaskNN_REPORT.md`, summarised in chat): a `/clock` stamp; goal; what was measured (MEASURED / DERIVED / CONSTANT / CLAIMED; "exists in code / wired / ran" kept apart); what changed (files, sha16); test output verbatim; what is true now and what is not; decisions needed; the next task.
- **Ask first, inside any task:** a kernel restart; any paid model call or embedding probe; any POST (`/dragon/flight`, `/swds/*`, `/models/router/phoenix-force`); Chroma deletion or rebuild; Windows Task Scheduler registration; env or key changes; copying changes into the live repo; commit or push.
- **Never:** run the test suite in the live repo; read `.env` values; autonomous trading; invent a stamp.
- **Where it lives:** `integra-homebase/docs/brainmap/` (`TODO.md`, `BOOT_BRIEF.md`, `TaskNN_REPORT.md`). `productivity/TASKS.md` carries a one-line pointer to this file (added 2026-10-16 on the Architect's word).
- **Known tension to respect:** `docs/DESIGN_DECISIONS_10_15_26.md` says code moves after gate G3, but the Rodin-first change set was already applied on 10/15. Every task that changes code says so and asks.
- **Uncommitted code is live (MEASURED 2026-10-16 10:56, git status and the process list).** The kernel (python 3192/3216, started 09:14:21) loads the working tree, so it runs the peer sessions' uncommitted edits: `memory/the_hoard.py` (the identity hunks; in T1's isolated full-suite runs they fail `test_hoard_schema_v2::test_the_hoard_creates_kernel_memory_dirs` and `::test_core_identity_file_contents`), `core/dragon_engine.py`, `core/starfire_protocol.py`, `config/rodin_memory_map.yml`, and the deleted `config/Constructionreconfigure.md`. The ADR-001 clock edits (`core/celestial_middleware.py`, `main.py`) are no longer among them: T1 committed them in `95a7aab`. At runtime the kernel rewrites four tracked files, `runtime/swds_state.json`, `kernel_memory/core_identity.txt`, `kernel_memory/rolling_context.json` and `kernel_memory/hoard/libraries/library_genesis_purple.md`: never stage them with a task's change. Since `c7053f1`, `config/celestial_checkpoint.json` is untracked and no longer written; the Sentinel writes the git-ignored `local_dbs/celestial/checkpoint.json`. (Before T1: the Architect's PC restart, 2026-10-15 23:50:30, with a quick reboot at 23:51:10 and a power-off at 23:52:43, then boot 2026-10-16 00:05:41, brought up the 00:07 kernel that first ran these edits.)
- **Atlas ground rules (from the save state and the measured assessment):** the codex supplies concepts; its mechanics are rebuilt. Keep: a fixed-width self-describing label (start from pointer v1: 16 bytes, celestial word TURN/ORB/LUN/ROT, memory-map store and kind codes, SHA-256 node key), binary quantization plus rescoring on real embeddings (later), bit flags, Morton prefixes for taxonomy buckets. Braille is display only: never stored, parsed, logged, put in prompts or used in file names. Drop: the hash "embedding", the golden-ratio lat/lon projection and the SOM as a retrieval index, the 12 invented meridians, trading flags and verdicts, a second SQLite store. Whether a Unix epoch goes into the label is a ruling (pointer v1 says no).

## The tasks

**T1. Connect Celestial Time** (map L1).
- *True means:* every Hoard save, SWDS report, CCID node and ledger row is stamped automatically with celestial and civil time; the clock mechanics match their definitions; there is one time source.
- *Known (10/13–10/15; re-measure):*
  - Stamping is not wired: `generate_hoard_manifest` is called only at `runtime/antigravity_runner.py:56`; `generate_4d_metadata_manifest` and `apply_zenkai_recalibration` have no caller.
  - `celestial_time()` was a frozen 10-06 checkpoint plus uptime (ADR-001), and `GET /celestial/checkpoint` writes the checkpoint.
  - **Update 2026-10-16:** a peer session's ADR-001 Option A edit (`celestial_time()` returns `time.time()`; `core/celestial_middleware.py`, 2026-10-15 22:51, uncommitted) has run since the 00:07 kernel start. The checkpoint written at 00:19:42 holds the live time (`CCID_1792127982`), so SWDS should now follow real local time: sleep in the 02:00–07:00 window after 3,600 s idle, wake 07:00 (`main.py:1179-1209`; DERIVED).
  - `BASE_EPOCH = 1785052800` is 2026-07-26T08:00Z but is labelled 2026-07-15T12:00Z (decision D-20); there are two year constants.
  - The Celestial Sentinel is a 15-line stub; decision D5 makes it the runtime owner.
- *Steps:* 1.1 measure live and in code. 1.2 gap list against the definitions (`temporal/celestial_clock.py`, the Celestial Constants document, spacetime spec v1, blueprint 5.7, ADR-001). 1.3 ruling on D-20, with a Tier 1 almanac check. 1.4 design the Sentinel (stamp API, atomic checkpoint, read-only route; design decisions §4.3 and §5.3). 1.5 build and test in the isolated copy. 1.6 apply to the live repo and restart (two approvals). 1.7 verify: a fresh Hoard node, a save state and an SWDS report each carry both stamps, read back from disk.
- *Rulings needed:* D-20 (epoch); the year constant; Sentinel scope (A4); who commits the ADR-001 edit that is already running, and when.

**T2. Connect the Hoard** (L3): the global environment for cold storage.
- *True means:* each kind of knowledge goes to the store the map names; the cold store is the source of truth and nothing private is published; each function does what it claims.
- *Known (map PROPOSED 10/15):*
  - Cold truth is `kernel_memory/hoard/raw_shards`, which is tracked in the public repo, so every committed node is published.
  - The hot index is Chroma collection `integra_hoard__gemini-embedding-2-768-asym-v1` (derived). The legacy collection is retired: 5,526 rows, 2,974 exact duplicates.
  - The Metatron SQLite database lives in OneDrive. `memory.db` (`C:\IntegraData`) is only proposed (ADR-005). The kernel does not load shards at startup.
- *Carried from T1 (save state `CCID_1792164893` §5 B):*
  - ADR-001 item 4: the correction note for artifacts stamped before 2026-10-16. T1 counted 42 of 308 shards with the frame-1 vector, 258 of 304 anchors with t = 0, and 55 of 61 SWDS reports named `CEL-282.85deg`; report-name dates ran 7 days behind file times. D-14 was decided 2026-10-16 (ruling R8): **rewrite the stamps** in the artifacts themselves, not a relabelling note; the rewrite gets its own design first.
  - T1's two open live checks, as of 2026-10-16 10:56 (MEASURED). The Hoard-node check is still open: no shard in `kernel_memory/hoard/raw_shards/` is newer than 2026-10-15 21:12:14. On the save-state check, `The Hoard/CCID_1792164893.json` does carry a frame-2 `celestial_stamp`, but a session wrote it from a `/clock` reading, not kernel code. Ruled R6: the save-state check stays open until the node path works.
- *Rulings (2.4, the Architect, 2026-10-16; recorded at the 14:55:27 CDT stamp; details in `Task02_VERIFICATION_REPORT.md`):*
  - **R1:** keep publishing cold nodes (`raw_shards` stays tracked).
  - **R2:** the map goes live after 2.5, from the HEAD version (without the peer's identity edit).
  - **R3:** `memory.db` (ADR-005) is deferred to Phase 2.
  - **R4:** declare the 8 Hoard-like locations in the map; move nothing.
  - **R5:** no telemetry or boot-loading change until T8.
  - **R6:** T1's save-state check stays open for the node path (2.5 fixes the sync's folder and stamp; one approved script run closes it).
  - **R7:** the live log waits for ADR-010.
  - **R8:** D-14: rewrite the skewed stamps (overrides the blueprint's "relabel, don't rewrite").
- *Steps:* 2.1 `memory_map.inventory` and `validate_memory_map` (counts and sizes only). 2.2 trace each Hoard function (`commit_node_v2`, `embed_pending`, `chroma_upsert`, `load_shards_from_disk`) from caller to store. 2.3 verdict table: kind → declared store → actual writer → state. 2.4 rulings: public or local-only for cold nodes; approve the map (PROPOSED → live); `memory.db`. 2.5 fixes in the isolated copy, e.g. a routing guard that refuses a `local-only` kind into a tracked store. 2.6 Chroma cleanup only after a backup and a quiesced kernel (approval).
- *Done when:* the map validates with 0 problems, every kind has a measured writer, and the routing test passes.

**T3. Connect Phoenix Engine and design the Atlas** (L5).
- *Goal:* a digital neural network that parallels a map (latitude/longitude matrix; sectors, hemispheres, poles; coordinates) for knowledge nodes, with Phoenix as the labeller.
- *Input:* `Braille-BasedSemanticLabelingSystem.md` and its HTML (both in `integra-homebase/memory/`). Design input only: anything reused is run and tested, not trusted. The four-pass study stays parked.
- *Steps:* 3.1 requirements (functional; scale from 305 shards today to 10⁴–10⁶; hot and cold tiers). 3.2 measure Phoenix today (`evolution/phoenix_forge.py`; the 10/08 brief said it reads 10 of 305 shards; re-measure). 3.3 high-level design in the system-design framework: components, data flow (ingest → embed → label → place → store → query), API, storage. 3.4 deep dive: data model; where the "neural" layer sits. 3.5 trade-offs. 3.6 `docs/brainmap/ATLAS_DESIGN.md`.
- *Rulings needed:* scale target; self-organizing map versus a fixed taxonomy grid; equal-area grid.

**T3.5. Coordinate system and Braille points** (L7).
- *Goal:* a lat/long grid and x/y node points that act as the Braille point system; named variables and quantifiable endpoints for a data point, knowledge node or memory state; the Apophenic Engine used.
- *Decided (Architect, 2026-10-15):* the Apophenic Engine draws **pattern links (edges) between Atlas nodes**. It sets no coordinates and gives no sell or buyback verdicts or action flags.
- *Steps:* 3.5.1 define the pattern-link function from the math in `core/apophenic_engine.py` (tracked, no importers, needs pandas) and the document's codex, used for link detection only; no trade verdict reaches a label (autonomous trading is out of scope). 3.5.2 spec: ranges, units, packet layout. Start from pointer v1 plus an ATLAS field (the Morton cell of the T4 bands); the document's 16-cell packet (time, codex, spatial, semantic) is the alternative, and choosing between them is a ruling. 3.5.3 reference encoder and decoder (standard library) with property tests: round-trip, bit budget, ordering. 3.5.4 `docs/brainmap/ATLAS_COORDINATES.md` and the codec (isolated copy first).
- *Note:* the math expression is Task 7, so this task uses provisional symbols that Task 7 ratifies.
- *Done when:* encode → decode round-trips on 10⁵ random points; every variable has a unit and range; the document's printed examples are reproduced or the differences explained.

**T4. Taxonomy labelling** (L9): poles, hemispheres and matrix.
- *Starting point (save state):* latitude bands from the memory-map tiers and kinds, using the codex's five zones (poles, temperate belts, equator); meridians from Integra's own domains (the Architect approves the list); MSB-first Morton codes for the grid. Lat/lon here is a taxonomy bucket, never a semantic-neighbour index (assessment: 8.8% topic agreement).
- *Rulings needed:* the meridian (domain) list; the kind → latitude-band mapping.
- *Steps:* 4.1 fix what latitude and longitude mean for knowledge nodes and for series nodes (the document uses them two ways). 4.2 zones, meridians and matrix resolution as data (`config/atlas_taxonomy.yml`) with a validator in the style of `validate_memory_map`. 4.3 label function and tests: every label reachable, boundaries aligned with the grid. 4.4 place each `kinds` entry of `rodin_memory_map.yml` in a region.
- *Done when:* the validator reports 0 problems and label ↔ coordinate round-trips.

**T5. Connect System, Iteration 1: Knowledge** (L11).
- *Meaning:* the first end-to-end pass of Tasks 1–4, facts only.
- *Steps:* in the isolated copy, take N historical nodes from `raw_shards` → stamp (T1) → store through the Hoard (T2) → Phoenix labels and encodes (T3, T3.5, T4) → place → read back. Plus live read-only probes.
- *Done when:* N nodes round-trip with stamp, packet and label, and failures are listed.
- **Gate K follows:** a combined report on T1–T5; nothing in U starts without the Architect's go.

**T5.5. SWDS and Siesta** (L13).
- *Goal:* connect SWDS and Siesta, with save states, memory, content labelling, placement and learning.
- *Known:* SWDS runs from `main.py`'s `swds_scheduler`; Heimdall's open/close are unwired (X-1); Siesta is unbuilt (re-measure).
- *Steps:* 5.5.1 measure the SWDS path (`PhoenixForge.execute_swds`). 5.5.2 define Siesta (the daytime short cycle; the phase table is in `config/swds_config.json`) as a function that reuses the SWDS path. 5.5.3 wire label and place into the consolidation step. 5.5.4 save states use the Sentinel stamp. 5.5.5 offline tests.
- *Gates:* any live SWDS trigger or `POST /swds/*`.
- *Rulings needed:* the SWDS schedule conflict C-07 and D-4 (windows in real local time); the Siesta definition (ADR-006).

**T6. Cheshire Cat: SWDS deep learning, security, Phoenix Force** (L15).
- *Decided (design decisions D2, A1, §4.1, §5.1):* the second key is the Architect's authenticated prompt, valid only inside an open SWDS cycle; Heimdall performs the handover; Cheshire Cat covers Phoenix's land tasks while Phoenix flies.
- *Steps:* 6.1 restate D2 and ask for the predetermined operations list (its contents are OPEN). 6.2 implement `POST /swds/phoenix-force` (refuses outside SWDS or without the header), the authorization record, the handover, per-operation receipts and the abort path, in the isolated copy. 6.3 define and wire Cheshire Cat's SWDS deep-learning and security duties. 6.4 offline tests with a fake Jean Grey client: both refusals, handover order, abort at wake time, both roles restored on error.
- *Gates:* the live route stays unregistered until approved; no live Phoenix run.

**T6.5. Connect System, Iteration 2: Understanding** (L17).
- *Meaning:* relationships: Heimdall ↔ Cheshire ↔ Phoenix ↔ Rodin ↔ Hoard ↔ Atlas ↔ Sentinel.
- *Steps:* simulate one full SWDS night in the isolated copy with fake model clients (open → consolidate → label and place → Phoenix Force → close → wake report). Trace causes and effects; table of couplings and failure modes.
- *Done when:* the night runs to a wake report with every step ledgered, and the abort and missing-receipt paths are exercised.
- **Gate U follows:** a combined report on T5.5–T6.5; nothing in W starts without the Architect's go.

**T7. Mathematical expression** (L19).
- *Goal:* a variable for predefined plot points through the neural grid, quantified and labelled when data is designated and routed by the taxonomic labels, for semantic-vector and relational search.
- *Steps:* 7.1 formal mapping f: node → (t, codex, φ, λ, semantic) from the variables of T3.5 and the labels of T4, with the routing rule and a search distance (Hamming, geodesic, codex mask). 7.2 invariants and error bounds. 7.3 executable spec with property tests. 7.4 reconcile T3.5 and T4.
- *Done when:* every symbol has a definition, range, unit and code counterpart, and the tests pass.

**T8. Connect Rodin and hot storage; historical-data test in an SWDS cycle** (L21).
- *Known:* `/rodin/telemetry` ONLINE is a constant; `orchestration/rodin_supervisor.py:88` uses a fixed `[0.1]*768`; the RAM tier is absent; embeddings are blocked until the key route (standard key, no Vertex) is settled. The Rodin-first change set (commit e81e9a0, local) has an unproven embedder.
- *Steps:* 8.1 measure Rodin. 8.2 RAM tier keyed by Atlas cell. 8.3 hand-off test: Phoenix labels → Rodin places → read back. 8.4 historical data (the Architect names the set), isolated first, then a live SWDS window (approval). 8.5 results.
- *Gates:* paid embedding calls and any live SWDS run; prerequisite: the key route. Decided 10/15: embedder-only (`RODIN_EMBED_API_KEY`); prepared, not applied (see the parallel track above).
- *Design inputs:* framework §8a (hot tier `hoard_working_memory`: session state plus expanded nodes; cold tier: pointers; node and token budgets, least-recently-routed eviction, Heimdall sees cache pressure). The cheap RAM win is a float32 matrix (3,072 B per 768-d vector against 25,368 B as a Python list; assessment, MEASURED). A RAM tier will not stay resident while the task runs at priority 7 and Windows trims the working set (126 MB → 4 MB seen 10/15): that is a ruling.

**T9. Scheduled task: Rodin and Phoenix plot and label in Flight and Land sessions** (L23).
- *Template:* `NewCurriculum2026/theritualdance.md`, a 13-hour cascade: one unit per hour, then a totality study, a master document and a verification. Its interruption rule: pause on an active conversation; resume after 1 hour of inactivity or at the nearer of 05:00 or 23:00 CDT. Its start date, 2026-08-13, is already past.
- *Steps:* 9.1 define the units (which historical data and large files, in what order, how much per hour). 9.2 map Flight (`/dragon/flight`) and Land sessions to the hours. 9.3 write the schedule as data, plus a runner stub that checks for an active conversation. 9.4 name the "minimal working task" days. 9.5 dry run in the isolated copy. 9.6 registration with Task Scheduler is its own approval.
- *Done when:* the dry run produces a per-hour ledger and honours the pause and resume rules.

**T10. Connect System: curriculum wisdom pass** (L25–31).
- *The map's rules:* spend 20 minutes; no report until every document is read in isolation and then with compounded knowledge; then unify into a master document and a code script.
- *Documents (12):* page counts MEASURED 2026-10-16 by T10 (they replace the earlier estimates); the second row was corrected the same day: the file holds the OUP chapter, not the review its file name gives.

  | Document | Size | Pages |
  |:--|--:|:--|
  | Tufte, *The Visual Display of Quantitative Information* (`NewCurriculum2026/Set1`) | 13.4 MB | 191 (scan, OCR'd) |
  | Buzsáki & Végh, "Space, Time, and Memory", ch. 3 of *Space, Time, and Memory* (L. Nadel & S. Aronowitz, eds., OUP 2025) (`set2`; the file is named "Buzsáki, G. Time, space, memory and brain–body rhythms. Nat. Rev. Neurosci. (2025)") | 3.7 MB | 21 |
  | `set2/Purple3.pdf` | 1.0 MB | 45 |
  | `BluprintArchitecture/K NN algorithm Modifications.md` | 77.5 KB | text (1,736 lines) |
  | `Integra Self-Reflect and Think Forward/The 14th Form.pdf` | 143 KB | 6 |
  | `AntiGravityconversionprocess/Metacognition in LLMs Foundations Progress and Opportunities(1).pdf` | 1.4 MB | 145 (HTML print; body + references) |
  | `AntiGravityconversionprocess/NovelSeekUpdateInternAgent.pdf` | 7.3 MB | 34 |
  | `AntiGravityconversionprocess/metacognition.pdf` | 445 KB | 8 |
  | `AntiGravityconversionprocess/Teaching operating systems.pdf` | 802 KB | 116 |
  | `AntiGravityconversionprocess/Seventh Form_ Flaming Thunder God.pdf` | 1.1 MB | 63 |
  | `AntiGravityconversionprocess/Rotating Spiral Brain Waves Act as a SpaceandTime Clock Neurosc(1).pdf` | 3.8 MB | 18 |
  | `NewCurriculum2026/theritualdance.md` (read for Task 9) | 4.5 KB | text |

- *Cost (CLAIMED):* the six counted PDFs alone are about 286 pages, and a PDF page costs roughly 1.5–3K tokens, so this cannot fit one thread. `NewCurriculum2026/Set1` also holds two earlier analyses (`Reviewof curriculumset1.md`, the Tufte "Response2" note) to cross-check against, not to substitute. The page counts above were estimated from the PDF page trees; "unknown" means the tree was compressed.
- *Gate 10.0 (first):* report the real volume and ask for scope (every page, or a priority order); check that the curriculum PDFs are not tracked in the public repo (copyright). Report only.
- *Method:* per document: read in isolation → `docs/brainmap/task10/NN_notes.md`; then re-read the previous notes plus this document → update `compound_notes.md` (K, U, W). 20-minute sittings, resumable from the notes. Notes are working files, not the report.
- *Output:* the master document and a code script. What the script does is settled at gate 10.0; proposal: the executable reference for Tasks 3.5–9 (encoder, labeller, placer, schedule).
- *Budget note (2026-10-16 00:27):* weekly usage is 75% with the reset on 2026-10-19 06:00 CDT. A full-depth T10 probably fits only after that reset; say so at gate 10.0.
- *Pace:* settled 2026-10-16 by the Architect ("Spend 20 min on task 10. Do not generate report until all files are read in isolation and with compounded knowledge").
- **Done 2026-10-16** (session be77ce02; stamps GET `/clock`: start 20:05:34 CDT | 2026-10-17T01:05:34Z, frame 2, `ROT_90_ORB_70`; end 20:31:03 CDT | 2026-10-17T01:31:03Z, frame 2, `ROT_90_ORB_70`):
  - *Read:* all 11 documents in the order above, ≈ 192,000 extracted words over 647 PDF pages plus the Markdown file; notes per document and a compound ledger (`task10/notes/`). The Tufte scan has no text layer: its 191 pages were OCR'd with Windows' built-in engine (figures seen only as labels). Extraction tools and text stay outside the repo (`%USERPROFILE%\t10\`) because several sources are copyrighted.
  - *Gate 10.0 (MEASURED):* 33 curriculum PDFs are tracked and on `origin/homebase-phase-e`, `origin/phase-e-dragon-rodin-flight` and `origin/workspace-root`, including the Tufte book and a BookZZ copy of Einstein/Greene. Not acted on: a decision for the Architect.
  - *Outputs:* `task10/TASK10_MASTER_DOCUMENT.md` (receipts; knowledge per document; crosswalk; five laws: identity invariant / file by taxonomy, find by relation / independent evidence / phase orders, the clock records, one writer / every threshold is a measured claim; corrections C1–C11; provisional design for T1–T9; the T7 expression with units and ranges), `task10/Task10_REPORT.md`, `task10/integra_atlas_reference.py` (sha16 `9164eb103ed5f76b`), `task10/evidence/selftest_output.txt`.
  - *Proposals for later rulings (not decided):* five dyadic equal-area zones (north = invariant, south = time-bound; promotion moves north); eight meridians (time, memory, cognition, governance, evolution, research, identity, operations); a 20-byte atlas pointer = pointer v1 + a 4-byte ATLAS word (depth + Morton code); the T9 anchor rule overriding an ongoing conversation.
  - *Copied in:* 2026-10-16 23:07 on the Architect's go (stamp 23:07:13 CDT | 2026-10-17T04:07:13Z, frame 2, `ROT_150_ORB_70`): 16 files with `xcopy`, each SHA-256 compared, 0 mismatches. This T10 entry, the Buzsáki row and the page counts were edited the same way, and the `TASKS.md` pointer was updated.

**Unification** (map L31, Zenitsu pass 4).
- *Goal:* unify the knowledge, understanding and wisdom of T1–T10 into a master document and a code script.
- *Rule:* both are written outside the repo first and enter it only on the Architect's go.
- *Done when:* every claim in the master document cites a task report or a source; the code script runs in an isolated copy with its tests.

## Oct 23 master document: added content as To-Do items (design input, not ruled)

**Source:** `integra-homebase/memory/Master_Gemini_Neural_Map_Core_OTC23_2026Braille-Based Semantic Labeling System.md` (484,386 B, 7,694 lines, sha16 `9367a6edf679b694`, written 2026-10-23 22:18). Only the content added after the Oct 17 version (sha16 `29dff6d850680637`) is listed here: the note block at L7–13 and the two new turns at L6524–7695. These items were added on the Architect's word "add document contents as todo items".
**Stamp** (GET `/clock`, HTTP 200, frame 2): 2026-10-23 22:31:52 CDT | 2026-10-24T03:31:52Z | rotation 141.7998°, lunar 0.4453, orbit 0.8008, ROT_120_ORB_80.

**Status of everything below:** design input only. None of it exists in the live kernel; a grep of the live tree on 2026-10-23 found none of the new classes or functions. Gemini's code and its "verified" tables are CLAIMED. Its printed Braille packets (for example `jmw¼⠃⡓ २४…`) cannot come from its own code, which emits only U+2800–U+28FF. Each item keeps the review note made on 2026-10-23 against official sources.

**A. The note block (L7–13), the Architect's corrections**
- [ ] **A1. Identity comes only from the Starfire Protocol** (Identity Matrix and 6-Point Star, `[Auteur, King, Prophet] = [1.0, 1.0, 1.0]`, EPF 0.0) inside the Dragon Engine and Dragon Kernel, never from TheHoard or a generic script. *Fit:* the kind `identity` in the live map already routes to `identity_matrix`, though that map is Antigravity's uncommitted edit of 2026-10-18. *Next:* confirm, then carry it into T2's map ruling (P1 is blocked).
- [ ] **A2. A persistent Braille Atlas and plot-point lattice** on disk (`kernel_memory/hoard/braille_atlas.sqlite`, `kernel_memory/hoard/plot_points_state.json`), synced with TheHoard (`raw_shards`, root `The Hoard/`). *Conflict:* a new SQLite store goes against ADR-005, ruling R3 (`memory.db` deferred to Phase 2) and the Atlas ground rules ("a second SQLite store": drop). *Ruling needed* (T2/T3).
- [ ] **A3. MongoDB.** *Fit:* Antigravity's uncommitted code already has a MongoDB placeholder: `memory/database/mongodb_substrate.py`, `mongodb_true=False`, with Metatron still on the SQLite file. *Next:* its review is the TASKS.md item "Review Antigravity's uncommitted kernel edits".
- [ ] **A4. Add the lexicon project and the seed package to the master.** *Fit:* Antigravity's code writes `kernel_memory/hoard/seed_packages/` and a quarterly MongoDB save state. *Next:* define both in the master document (Unification), after the Antigravity review.

**B. The Phoenix orbital trajectory and the CIT crosspoint grid (L6524–7262; script `integra_os/core/phoenix_celestial_grid_loop.py`)**
- [ ] **B1. The (X,Y) crosspoint grid** (R × C points on a 65,536² and 4,096² matrix) with the **20–30% initial-capacity rule**: 25% pre-seeded, 70–80% left open for new data. *Note:* the demo grid has 120 points, against 307 shards today. *Ruling needed:* grid size and capacity rule (T3/T3.5).
- [ ] **B2. The CIT 16-cell label:** time (cells 0–3), an 8-bit archetype/orbit register (cell 4), Morton (X,Y) (cells 5–8) and a 56-bit semantic hash (cells 9–15). *Conflict:* it stores and compares Braille strings, against the ground rule "Braille is display only". *Next:* T3.5 chooses between pointer v1 and the 16-cell packet (already a listed ruling).
- [ ] **B3. Three storage archetypes on the grid:** KNOWLEDGE_DOCUMENT, SAVE_STATE_MEMORY (Siesta/SWDS checkpoints) and ISOLATED_NODE (Kintsugi \|Z\| > 3, routed automatically). *Next:* map them to the memory-map kinds (`node`, `save_state`, and a new kind for isolated nodes) in T4 and T5.5/T6.
- [ ] **B4. Placement by the composite orbital distance** `D_orbital` = 0.40 geodesic + 0.25 trajectory + 0.20 Hamming + 0.15 vector, against a moving "planetary trajectory" point (latitude = solar declination × 3.2 + 5.145° × sin(lunar phase)). *Conflict:* the same document lands in different cells depending on when it arrives, against the ground rule that lat/lon is a taxonomy bucket and never a time or semantic index. The vectors are SHA-512 shingle hashes (the dropped "hash embedding"). *Ruling needed:* placement by trajectory or by taxonomy (T3.5/T4).
- [ ] **B5. The Phoenix orbital sweep search:** rank occupied crosspoints by trajectory arc, 56-bit Hamming and 64D→768D similarity, with throughput Υ. *Note:* real vectors wait on the embedder key route (T8, parked).

**C. Boot geolocation and anamnesis (L7264–7695; script `integra_os/core/boot_geolocation_anamnesis.py`)**
- [ ] **C1. A 4-tier boot geolocation cascade:** (1) MCP or the Google Maps Geolocation API; (2) the HLC boot journal in the Hoard; (3) the host environment variable `INTEGRA_HOST_LOCATION` with a gazetteer; (4) the fixed Baker seed. *Note:* Tier 1 is a paid, key-based external call that sends network data, so it needs the Architect's approval. Google's documentation was not fetched in the 2026-10-23 review (UNVERIFIED).
- [ ] **C2. The seed anchor: Baker, LA, 30.5888° N, −91.1673° W.** *Checked 2026-10-23:* the US Census Bureau's 2024 Gazetteer gives Baker city's interior point as 30.583197, −91.158179, about 1.1 km away, so the seed lies within Baker. It matches the live frame-2 registry (`anchor_lon` −91.1673) and `config/celestial_seed.json`. Earlier parts of the same document use 30.5882, −91.1668, about 80 m off. *Next:* one anchor, ruled. The gazetteer's Zachary (30.6485, −91.1565) and Baton Rouge (30.4515, −91.1871) points are about 2.0 km and 5.3 km from the Census points.
- [ ] **C3. The drift audit with Zenkai snap-back:** a reading more than 25 km from the seed is replaced by Baker and logged with drift 0.0. *Conflict:* it hides a real reading, against the provenance rule. *Proposal:* record both values and flag the mismatch. *Ruling needed.*
- [ ] **C4. The HLC boot journal** (`load_hlc_state_from_db` / `save_hlc_state_to_db`, one SQLite row with the last location, HLC counter, partition key and stamp). *Conflict:* another SQLite store (R3/ADR-005). *Fit:* the Sentinel's checkpoint (`local_dbs/celestial/checkpoint.json`) already persists boot time across restarts.
- [ ] **C5. The ephemeris partition key** `ROT_xxx_LUN_xxx_ORB_xxx` at boot. *Checked 2026-10-23 against USNO:*
  - Its lunar reference, 2025-01-01 00:00Z treated as a new moon, is 25.5 h after the real one (2024-12-30 22:27 UTC).
  - Its orbit is counted from 2025-01-01 with the sidereal year; the perihelion was 2025-01-04 13:28 UTC.
  - Its rotation is longitude plus (unix time mod sidereal day), which has no reference date.
  - Frame 2's references (new moon 2026-07-14 09:43Z, perihelion 2026-01-03 17:15Z) are confirmed by USNO.
  - The key format also differs from the Sentinel's live label (e.g. `ROT_120_LUN_40_ORB_80`).
  - *Ruling needed:* keep frame 2 (rulings R1–R6), or open a frame 3 (T1).
- [ ] **C6. A fixed accuracy constant** (`spatial_accuracy_sigma` 0.9988, "3.0016 km / 99.88%"), taken from the document's own simulation. *Status:* CONSTANT/CLAIMED; nothing measures it.
- [ ] **C7. The boot order:** the runbook in this document (L3586) says "Dragon Kernel -> Flame Kernel"; the Architect's 2026-10-17 message says Flame → Genesis/Dragon. Antigravity's live watchdog runs Dragon → Flame, and its "Flame" is `thermal_core`, not `sensory/cheshire_cat.py`. *Ruling needed:* the canonical order, and which component is the Flame.

**Batched rulings for these items** (ask once, blueprint checked first):
1. the clock references (C5);
2. the seed anchor (C2);
3. snap-back or record-and-flag (C3);
4. Tier 1 Google geolocation (C1);
5. placement by trajectory or by taxonomy (B4);
6. new SQLite stores (A2, C4);
7. the boot order and the Flame component (C7);
8. grid size and capacity rule (B1).
