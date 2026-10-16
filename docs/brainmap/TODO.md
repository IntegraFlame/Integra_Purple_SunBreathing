# BRAIN MAP TO-DO (2026-10-15, session 8bbd7f50): `integra-homebase/core/IntegraBrainMap.md`, one task at a time

> From the Architect's `/engineering:system-design` request. The map has 13 numbered items (1, 2, 3, 3.5, 4, 5, 5.5, 6, 6.5, 7, 8, 9, 10) and a closing instruction for Task 10. The Architect's order is kept. The folder-13 plans (other iteration) are unchanged and belong to the other iteration. The Braille four-pass study is **parked** (the Architect chose "after the To-Do").

> **Provenance of this file.** Transcribed from the Architect's approved plan message on 2026-10-16 by the cloud session on branch `claude/brain-map-todo-session-8-ekpfg6` (task T0). Wording is unchanged except for two relative references in the opening note ("further down", "below") that pointed at plan sections which are not part of this file, and the Provenance and Pointers blocks, which are additions; Markdown layout was otherwise normalised. The date is the container date, not a `/clock` stamp (no kernel was reachable from the cloud container, so no stamp was taken and none is invented). Task state is tracked by which `TaskNN_REPORT.md` files exist beside this file. This file is edited only to record the Architect's rulings.

## How the work runs
- **One task at a time, no agents.** Each task: (1) read-only measurement, (2) the questions it needs, batched once at the start, (3) work in an **isolated copy**, never the live repo, (4) apply to the live repo only after approval, (5) verify, (6) report, (7) **stop and wait for "continue"**.
- **Report** (saved as `docs/brainmap/TaskNN_REPORT.md`, summarised in chat): a `/clock` stamp; goal; what was measured (MEASURED / DERIVED / CONSTANT / CLAIMED; "exists in code / wired / ran" kept apart); what changed (files, sha16); test output verbatim; what is true now and what is not; decisions needed; the next task.
- **Ask first, inside any task:** a kernel restart; any paid model call or embedding probe; any POST (`/dragon/flight`, `/swds/*`, `/models/router/phoenix-force`); Chroma deletion or rebuild; Windows Task Scheduler registration; env or key changes; copying changes into the live repo; commit or push.
- **Never:** run the test suite in the live repo; read `.env` values; autonomous trading; invent a stamp.
- **Where it lives:** `integra-homebase/docs/brainmap/` (`TODO.md`, `BOOT_BRIEF.md`, `TaskNN_REPORT.md`). `productivity/TASKS.md` gets a one-line pointer only when the Architect says so.
- **Venue:** this thread is 73% full and weekly usage is 73% (resets 10-19 06:00 CDT). The Architect had no preference, so on approval I save `TODO.md` and a boot brief and **stop**. Task 1 starts in a fresh thread, unless you tell me to begin here.
- **Known tension to respect:** `docs/DESIGN_DECISIONS_10_15_26.md` says code moves after gate G3, but the Rodin-first change set was already applied on 10/15. Every task that changes code says so and asks.

## The To-Do

**T0. Set-up (on approval).** Create `docs/brainmap/`; save this list as `TODO.md`; write `BOOT_BRIEF.md` (boot per `CLAUDE.md`, then this list, the map, the 10/15 design decisions, `config/rodin_memory_map.yml`; the rules above; first action = T1 step 1.1). Stop.

**T1. Connect Celestial Time** (map L1).
- *True means:* every Hoard save, SWDS report, CCID node and ledger row is stamped automatically with celestial and civil time; the clock mechanics match their definitions; there is one time source.
- *Known (10/13–10/15; re-measure):*
  - Stamping is not wired: `generate_hoard_manifest` is called only at `runtime/antigravity_runner.py:56`; `generate_4d_metadata_manifest` and `apply_zenkai_recalibration` have no caller.
  - `celestial_time()` is a frozen 10-06 checkpoint plus uptime (ADR-001), and `GET /celestial/checkpoint` writes the checkpoint.
  - `BASE_EPOCH = 1785052800` is 2026-07-26T08:00Z but is labelled 2026-07-15T12:00Z (decision D-20); there are two year constants.
  - The Celestial Sentinel is a 15-line stub; decision D5 makes it the runtime owner.
- *Steps:* 1.1 measure live and in code. 1.2 gap list against the definitions (`temporal/celestial_clock.py`, the Celestial Constants document, spacetime spec v1, blueprint 5.7, ADR-001). 1.3 ruling on D-20, with a Tier 1 almanac check. 1.4 design the Sentinel (stamp API, atomic checkpoint, read-only route; design decisions §4.3 and §5.3). 1.5 build and test in the isolated copy. 1.6 apply to the live repo and restart (two approvals). 1.7 verify: a fresh Hoard node, a save state and an SWDS report each carry both stamps, read back from disk.
- *Rulings needed:* D-20 (epoch); the year constant; Sentinel scope (A4).

**T2. Connect the Hoard** (L3): the global environment for cold storage.
- *True means:* each kind of knowledge goes to the store the map names; the cold store is the source of truth and nothing private is published; each function does what it claims.
- *Known (map PROPOSED 10/15):*
  - Cold truth is `kernel_memory/hoard/raw_shards`, which is tracked in the public repo, so every committed node is published.
  - The hot index is Chroma collection `integra_hoard__gemini-embedding-2-768-asym-v1` (derived). The legacy collection is retired: 5,526 rows, 2,974 exact duplicates.
  - The Metatron SQLite database lives in OneDrive. `memory.db` (`C:\IntegraData`) is only proposed (ADR-005). The kernel does not load shards at startup.
- *Steps:* 2.1 `memory_map.inventory` and `validate_memory_map` (counts and sizes only). 2.2 trace each Hoard function (`commit_node_v2`, `embed_pending`, `chroma_upsert`, `load_shards_from_disk`) from caller to store. 2.3 verdict table: kind → declared store → actual writer → state. 2.4 rulings: public or local-only for cold nodes; approve the map (PROPOSED → live); `memory.db`. 2.5 fixes in the isolated copy, e.g. a routing guard that refuses a `local-only` kind into a tracked store. 2.6 Chroma cleanup only after a backup and a quiesced kernel (approval).
- *Done when:* the map validates with 0 problems, every kind has a measured writer, and the routing test passes.

**T3. Connect Phoenix Engine and design the Atlas** (L5).
- *Goal:* a digital neural network that parallels a map (latitude/longitude matrix; sectors, hemispheres, poles; coordinates) for knowledge nodes, with Phoenix as the labeller.
- *Input:* `Braille-BasedSemanticLabelingSystem.md` and its HTML. Design input only: anything reused is run and tested, not trusted. The four-pass study stays parked.
- *Steps:* 3.1 requirements (functional; scale from 305 shards today to 10⁴–10⁶; hot and cold tiers). 3.2 measure Phoenix today (`evolution/phoenix_forge.py`; the 10/08 brief said it reads 10 of 305 shards; re-measure). 3.3 high-level design in the system-design framework: components, data flow (ingest → embed → label → place → store → query), API, storage. 3.4 deep dive: data model; where the "neural" layer sits. 3.5 trade-offs. 3.6 `docs/brainmap/ATLAS_DESIGN.md`.
- *Rulings needed:* scale target; self-organizing map versus a fixed taxonomy grid; equal-area grid.

**T3.5. Coordinate system and Braille points** (L7).
- *Goal:* a lat/long grid and x/y node points that act as the Braille point system; named variables and quantifiable endpoints for a data point, knowledge node or memory state; the Apophenic Engine used.
- *Steps:* 3.5.1 compare the two Apophenic implementations (`core/apophenic_engine.py`: tracked, no importers, needs pandas, returns a trade verdict; and the document's codex) and pick one; keep trade verdicts out of the label (autonomous trading is out of scope). 3.5.2 spec: ranges, units, packet layout (time, codex, spatial, semantic). 3.5.3 reference encoder and decoder (standard library) with property tests: round-trip, bit budget, ordering. 3.5.4 `docs/brainmap/ATLAS_COORDINATES.md` and the codec (isolated copy first).
- *Note:* the math expression is Task 7, so this task uses provisional symbols that Task 7 ratifies.
- *Done when:* encode → decode round-trips on 10⁵ random points; every variable has a unit and range; the document's printed examples are reproduced or the differences explained.

**T4. Taxonomy labelling** (L9): poles, hemispheres and matrix.
- *Steps:* 4.1 fix what latitude and longitude mean for knowledge nodes and for series nodes (the document uses them two ways). 4.2 zones, meridians and matrix resolution as data (`config/atlas_taxonomy.yml`) with a validator in the style of `validate_memory_map`. 4.3 label function and tests: every label reachable, boundaries aligned with the grid. 4.4 place each `kinds` entry of `rodin_memory_map.yml` in a region.
- *Done when:* the validator reports 0 problems and label ↔ coordinate round-trips.

**T5. Connect System, Iteration 1: Knowledge** (L11).
- *Meaning:* the first end-to-end pass of Tasks 1–4, facts only.
- *Steps:* in the isolated copy, take N historical nodes from `raw_shards` → stamp (T1) → store through the Hoard (T2) → Phoenix labels and encodes (T3, T3.5, T4) → place → read back. Plus live read-only probes.
- *Done when:* N nodes round-trip with stamp, packet and label, and failures are listed.

**T5.5. SWDS and Siesta** (L13).
- *Goal:* connect SWDS and Siesta, with save states, memory, content labelling, placement and learning.
- *Known:* SWDS runs from `main.py`'s `swds_scheduler`; Heimdall's open/close are unwired (X-1); Siesta is unbuilt (re-measure).
- *Steps:* 5.5.1 measure the SWDS path (`PhoenixForge.execute_swds`). 5.5.2 define Siesta (the daytime short cycle; the phase table is in `config/swds_config.json`) as a function that reuses the SWDS path. 5.5.3 wire label and place into the consolidation step. 5.5.4 save states use the Sentinel stamp. 5.5.5 offline tests.
- *Gates:* any live SWDS trigger or `POST /swds/*`.

**T6. Cheshire Cat: SWDS deep learning, security, Phoenix Force** (L15).
- *Decided (design decisions D2, A1, §4.1, §5.1):* the second key is the Architect's authenticated prompt, valid only inside an open SWDS cycle; Heimdall performs the handover; Cheshire Cat covers Phoenix's land tasks while Phoenix flies.
- *Steps:* 6.1 restate D2 and ask for the predetermined operations list (its contents are OPEN). 6.2 implement `POST /swds/phoenix-force` (refuses outside SWDS or without the header), the authorization record, the handover, per-operation receipts and the abort path, in the isolated copy. 6.3 define and wire Cheshire Cat's SWDS deep-learning and security duties. 6.4 offline tests with a fake Jean Grey client: both refusals, handover order, abort at wake time, both roles restored on error.
- *Gates:* the live route stays unregistered until approved; no live Phoenix run.

**T6.5. Connect System, Iteration 2: Understanding** (L17).
- *Meaning:* relationships: Heimdall ↔ Cheshire ↔ Phoenix ↔ Rodin ↔ Hoard ↔ Atlas ↔ Sentinel.
- *Steps:* simulate one full SWDS night in the isolated copy with fake model clients (open → consolidate → label and place → Phoenix Force → close → wake report). Trace causes and effects; table of couplings and failure modes.
- *Done when:* the night runs to a wake report with every step ledgered, and the abort and missing-receipt paths are exercised.

**T7. Mathematical expression** (L19).
- *Goal:* a variable for predefined plot points through the neural grid, quantified and labelled when data is designated and routed by the taxonomic labels, for semantic-vector and relational search.
- *Steps:* 7.1 formal mapping f: node → (t, codex, φ, λ, semantic) from the variables of T3.5 and the labels of T4, with the routing rule and a search distance (Hamming, geodesic, codex mask). 7.2 invariants and error bounds. 7.3 executable spec with property tests. 7.4 reconcile T3.5 and T4.
- *Done when:* every symbol has a definition, range, unit and code counterpart, and the tests pass.

**T8. Connect Rodin and hot storage; historical-data test in an SWDS cycle** (L21).
- *Known:* `/rodin/telemetry` ONLINE is a constant; `orchestration/rodin_supervisor.py:88` uses a fixed `[0.1]*768`; the RAM tier is absent; embeddings are blocked until the key route (standard key, no Vertex) is settled. The Rodin-first change set (commit e81e9a0, local) has an unproven embedder.
- *Steps:* 8.1 measure Rodin. 8.2 RAM tier keyed by Atlas cell. 8.3 hand-off test: Phoenix labels → Rodin places → read back. 8.4 historical data (the Architect names the set), isolated first, then a live SWDS window (approval). 8.5 results.
- *Gates:* paid embedding calls and any live SWDS run; prerequisite: the key-route decision.

**T9. Scheduled task: Rodin and Phoenix plot and label in Flight and Land sessions** (L23).
- *Template:* `NewCurriculum2026/theritualdance.md`, a 13-hour cascade: one unit per hour, then a totality study, a master document and a verification. Its interruption rule: pause on an active conversation; resume after 1 hour of inactivity or at the nearer of 05:00 or 23:00 CDT. Its start date, 2026-08-13, is already past.
- *Steps:* 9.1 define the units (which historical data and large files, in what order, how much per hour). 9.2 map Flight (`/dragon/flight`) and Land sessions to the hours. 9.3 write the schedule as data, plus a runner stub that checks for an active conversation. 9.4 name the "minimal working task" days. 9.5 dry run in the isolated copy. 9.6 registration with Task Scheduler is its own approval.
- *Done when:* the dry run produces a per-hour ledger and honours the pause and resume rules.

**T10. Connect System: curriculum wisdom pass** (L25–31).
- *The map's rules:* spend 20 minutes; no report until every document is read in isolation and then with compounded knowledge; then unify into a master document and a code script.
- *Documents (12):*

  | Document | Size | Pages |
  |:--|--:|:--|
  | Tufte, *The Visual Display of Quantitative Information* (`Set1`) | 13.4 MB | unknown (scan) |
  | Buzsáki, *Time, space, memory and brain–body rhythms* (2025) | 3.7 MB | unknown |
  | `Purple3.pdf` | 1.0 MB | ~45 |
  | `K NN algorithm Modifications.md` | 77.5 KB | text |
  | `The 14th Form.pdf` | 143 KB | ~6 |
  | *Metacognition in LLMs: Foundations, Progress and Opportunities* | 1.4 MB | ~145 |
  | `NovelSeekUpdateInternAgent.pdf` | 7.3 MB | unknown |
  | `metacognition.pdf` | 445 KB | ~8 |
  | `Teaching operating systems.pdf` | 802 KB | unknown |
  | `Seventh Form_ Flaming Thunder God.pdf` | 1.1 MB | ~64 |
  | `Rotating Spiral Brain Waves Act as a Space and Time Clock` | 3.8 MB | ~18 |
  | `theritualdance.md` (read for Task 9) | 4.5 KB | text |

- *Cost (CLAIMED):* the six counted PDFs alone are about 286 pages, and a PDF page costs roughly 1.5–3K tokens, so this cannot fit one thread. Set1 also holds two earlier analyses (`Reviewof curriculumset1.md`, the Tufte "Response2" note) to cross-check against, not to substitute.
- *Gate 10.0 (first):* report the real volume and ask for scope (every page, or a priority order); check that the curriculum PDFs are not tracked in the public repo (copyright). Report only.
- *Method:* per document: read in isolation → `docs/brainmap/task10/NN_notes.md`; then re-read the previous notes plus this document → update `compound_notes.md` (K, U, W). 20-minute sittings, resumable from the notes. Notes are working files, not the report.
- *Output:* the master document and a code script. What the script does is settled at gate 10.0; proposal: the executable reference for Tasks 3.5–9 (encoder, labeller, placer, schedule).

## Verification of this plan's first action (T0)
- `docs/brainmap/TODO.md` and `BOOT_BRIEF.md` exist, read back byte-exact, with sha16 recorded.
- No existing file is changed; nothing is committed or pushed.
- I stop after T0 and tell you the boot line for the fresh thread.

## Pointers (not part of the list)
- The Braille four-pass study is **parked** until this To-Do is done (the Architect's choice, 10/15). Its inputs live only on the Architect's machine (`integra-homebase/memory/`, untracked).
- The folder-13 plans belong to the other iteration and are unchanged.
