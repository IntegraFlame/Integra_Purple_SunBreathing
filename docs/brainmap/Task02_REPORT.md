# Task 02 report: Connect the Hoard (steps 2.1–2.3, read-only)

**Stamp (GET `/clock`, HTTP 200, frame 2):** 2026-10-16 12:18:12 CDT | 2026-10-16T17:18:12Z | rotation 348.3865°, lunar 0.1938, orbit 0.7804, ROT_330_ORB_70 (kernel uptime 03 h 03 m 45 s). Work began at the 12:05:16 CDT stamp (rotation 345.1524°, lunar 0.1935, orbit 0.7804). **Usage at the end:** 5-hour window 19%, weekly 79% (resets 2026-10-19 06:00 CDT).

**The Architect's go:** "Go: T2 steps 2.1-2.3, read-only, with your defaults. Report and stop." The defaults applied:
- both versions of the memory map were validated;
- the five undeclared Hoard-like folders were inventoried (metadata only);
- the new `temporal/Node IDLabeConigtiveConnections_10_16_26l.md` was left untouched (T3/T4 input).

The ADR-001 correction note is not part of this go and was not written.

**Scope: read-only.**
- **Not done:** no POST, no restart, no paid call, no test run, nothing staged or committed.
- **Written into the live tree:** this report and the T2 row in `TODO.md`.
- **Where the tools ran:** an isolated copy at `%USERPROFILE%\t2s\`, outside OneDrive, using the kernel venv's Python with `-I -B -X utf8`. Each copied file is hash-equal to its live original:
  - `memory/memory_map.py` (sha16 `50b50ce9b3c1322b`);
  - `memory/__init__.py` (0 B);
  - `tools/rodin_memory_inventory.py` (`0be01cb538a71244`);
  - the working-tree map (`00b961e6b4616bf7`, 12,893 B);
  - HEAD's map (blob `1a56596`, last changed in `e81e9a0`, 11,583 B).
- **Live-tree effects:** nothing was imported from the live tree, and no `.pyc` was written there (checked).
- **What each step read:**
  - 2.1 read file metadata and git's index only.
  - 2.2 read code. For the shard census it opened the shard JSON files and counted structure. No payload text, query, summary or shard file name is printed or quoted here.

**Evidence (outside the repo):** `~/.claude/projects/<project>/brainmap_t2_2026-10-16/` (the scripts, both map copies, `out/*.json`).

**Labels:** MEASURED, DERIVED, CONSTANT and CLAIMED; "exists in code", "wired" and "ran" are kept apart.

## Goal (map L3)

"Connect The Hoard and ensure its functions and Datbase routng and store state is true Hoard will act as the global environment for cold storage."

From `TODO.md`:
- **True means:** each kind of knowledge goes to the store the map names; the cold store is the source of truth and nothing private is published; each function does what it claims.
- **Done when:** the map validates with 0 problems, every kind has a measured writer, and the routing test passes.

## Bottom line

- **The map is consistent on paper but routes nothing.**
  - Both versions validate with 0 problems.
  - No kernel code reads the map: outside its own module, `load_memory_map` has only two callers, `tools/rodin_memory_inventory.py:44` and `tests/test_memory_map.py`.
  - So whether a kind lands in its declared store depends on each writer's own path, and nothing checks it.
- **Most writers land where the map says. Three do not:**
  - the save-state sync reads `integra-homebase/The_Hoard` (6 files from mid-September), and only two scripts call it;
  - Alexandria writes nodes through a second Hoard object;
  - crystallization and Metatron loop rows have no caller.
- **Private data is published.**
  - The cold store `kernel_memory/hoard/raw_shards` is tracked. 307 shard files are in `origin/phase-e-dragon-rodin-flight` (local remote-tracking ref; the repo is public per the save state).
  - Every cognitive-cycle node stores its prompt as `topic` (`sensory/cheshire_protocol.py:114-115` → `sensory/cheshire_cat.py:374`). 258 of the 304 nodes are cognitive-cycle nodes, and all 258 carry a non-empty `topic` string.
  - The live kernel log is tracked in the root repo, and an older 146,709 B copy of it is on `origin`.
  - A second, older copy of 239 shards sits in the root repo's `kernel_memory/`, also on `origin`.
- **What the map leaves out:** 8 Hoard-like locations, and 2 kinds of content inside declared stores (the live log; 4 non-node files in `raw_shards`).
- **No node has been written since T1 went live.**
  - None of the 304 nodes carries a `celestial_stamp`.
  - None has a trusted vector.
  - The kernel holds 0 of them in memory.

## 2.1 Inventory and validation

### Validation (MEASURED)
| Map version | Stores | Kinds | `validate_memory_map` |
|:--|--:|--:|:--|
| HEAD (`e81e9a0`, status PROPOSED) | 20 | 16 | 0 problems |
| Working tree (with the peer's uncommitted identity edit) | 21 | 16 | 0 problems |

The two versions differ only in the `identity_matrix` store and the routing of kind `identity` (working tree: primary `identity_matrix`, also `core_identity`).

### The declared stores on disk (MEASURED 12:05–12:10, working-tree map, metadata only)
| Store | Tier | Files | Bytes | Newest file | Map `git:` / measured |
|:--|:--|--:|--:|:--|:--|
| `rolling_context` | W | 1 | 381 | 10-16 02:00:59 | tracked / tracked |
| `identity_matrix` (working tree only) | D | 1 | 6,605 | 09-24 05:00:16 | tracked / tracked |
| `core_identity` | D | 1 | 509 | 10-16 09:15:30 | tracked / tracked |
| `claude_memory_index` | W | 24 | 93,394 | 10-16 11:29:10 | outside-repo |
| `raw_shards` | C | 308 | 7,344,087 | 10-15 21:12:14 | tracked / 307 tracked, 1 untracked |
| `chroma_active` and `chroma_legacy` (one folder) | H | 6 | 124,872,394 | 10-16 09:15:25 | ignored / 6 ignored |
| `libraries` | L | 4 | 144,488 | 10-16 02:00:59 | tracked / 4 tracked |
| `modules`, `vectors_dir`, `drop_in` | D, H, I | 0 each | 0 | — | tracked / empty folders (git keeps none) |
| `metatron_db` | R | 1 | 32,768 | 09-23 20:19:00 | ignored / ignored |
| `save_states_root` (root `The Hoard`, without its two sub-stores) | S | 207 | 5,455,644 | 10-16 11:44:32 (the live log) | tracked / 204 tracked, 3 untracked |
| `swds_reports` | S | 75 | 319,702 | 10-16 09:15:31 | tracked / 74 tracked, 1 untracked |
| `antigravity_archive` | A | 1,916 | 305,999,800 | 10-15 12:13:29 | ignored / 1,916 ignored |
| `docs_blueprint` | D | 15 | 1,135,964 | 10-16 11:27:43 | tracked / 10 tracked, 5 untracked (`docs/brainmap/`, the design decisions) |
| `reading_ledger` | D | 1 | 357,738 | 10-13 02:11:05 | tracked / tracked |
| `tasks` | D | 1 | 35,063 | 10-16 11:25:40 | tracked / tracked |
| `memory_db` (proposed) | C | does not exist | | | outside-repo |
| `ram_embedding_cache`, `ram_hoard_cache` | W | in RAM | | | n/a |

- **Chroma:** the two Chroma stores share one folder, so the inventory cannot tell them apart. No database was opened, and `/rodin/telemetry` gives no row count for the active collection.
- **RAM:** the kernel holds 0 nodes in memory (`hoard.total_nodes` 0 at 11:44), while 304 nodes are on disk.
- **Metatron:**
  - `metatron_manifold.db-wal` (4,152 B) was last written 09-23 20:51:17;
  - `-shm` was touched at 10-16 09:15:31, when the kernel opened the database at boot;
  - so no Metatron row has been written since 09-23 (DERIVED).
- **`save_states_root`:**
  - It also holds the live kernel log (3.9 MB of its 5.46 MB) and two other `genesis_kernel*.log` files.
  - By file name it holds:

    | Files | Count |
    |:--|--:|
    | `CCID_<unix>.json` | 116 |
    | save-state reports | 13 |
    | boot sequences | 4 |
    | other CCID reports | 27 |
    | `save_state_*.md` | 5 |
    | logs | 3 |
    | other | 9 |
- **`swds_reports`, by name:**

  | Name pattern | Count |
  |:--|--:|
  | `CEL-282.85deg` | 55 |
  | other frame-1 angles | 6 |
  | `CEL-F2-` | 1 |
  | other `.md` | 10 |
  | `.json` | 2 |
  | other | 1 |

### Hoard-like locations the map does not declare (MEASURED: metadata, git's index, local remote-tracking refs)
| Location | Files | Bytes | Newest | Git | On `origin` | Notes |
|:--|--:|--:|:--|:--|:--|:--|
| `integra-homebase/The Hoard/` | 173 | 1,190,010 | 10-02 19:13 | nested, 173 tracked | yes (173) | An older copy of root `The Hoard`: 170 of its 173 relative paths also exist there, 169 with the same size. It holds its own `Slow-Wave Deep Sleep Reports/` (the blueprint's "third SWDS report folder", E57) and an old 2,508 B `genesis_kernel.log` |
| `integra-homebase/The_Hoard/` | 6 | 17,439 | 09-24 | nested, 6 tracked | yes | 3 save states (JSON and report each; their CCIDs decode to 2026-09-18). **This is the default source of `sync_all_save_states`** |
| root `The_Hoard/` | 6 | 17,439 | 09-28 | root, 6 tracked | yes | The same names and sizes as the nested `The_Hoard/` |
| root `kernel_memory/` | 249 | 44,334,841,856 (Docker) + 4,941,182 | 10-16 10:32 (Docker) | root, 247 tracked, 2 ignored | yes (239 shards, 2 drop-in files) | A second kernel memory: `hoard/raw_shards/` (239 shards; all 239 names are also in the nested store, 238 with the same size), `hoard/libraries/` (4), `core_identity.txt`, `rolling_context.json`, `drop_in/` (2 Architect files, tracked), `DockerDesktopWSL/` (2 ignored files) |
| root `local_dbs/chroma_storage/` | 1 | 188,416 | 09-28 | root, ignored | no | An old Chroma file |
| `integra-homebase/kernel_memory/ClaudeMemSuite.md` | 1 | 63,664 | 10-11 00:59 | nested, tracked | yes | A document inside kernel memory |
| `integra-homebase/local_dbs/celestial/` | 1 | 624 | 10-16 12:02 | ignored | no | T1's Sentinel checkpoint (atomic, every 300 s) |
| `integra-homebase/runtime/swds_state.json` | 1 | 2,165 | 10-16 09:15:31 | tracked | yes | The SWDS state, rewritten by the kernel |
| inside `save_states_root`: `genesis_kernel.log` | 1 | 3,903,304 | live | root, tracked since `ed871f6` (10-08) | an older copy, 146,709 B | The live kernel log (never stage). Blueprint ADR-010 item 2 moves logs to `C:\IntegraData\logs\` |
| inside `raw_shards`: 4 non-node files | 4 | — | 09-29 or earlier | tracked | yes | 3 `CCID_SWDS_*_20260929` records (two hold trading-simulation statistics, one is a session record) and 1 event record. `load_nodes_from_shards` skips them |

The blueprint already knows part of this:
- §4.2 lists root `The_Hoard` and the third SWDS folder (E57).
- ADR-005 action 3 dedupes `The Hoard` against `The_Hoard`.
- ADR-013 action 2 quarantines two fabricated Daily Planet shards "and their copies in the outer repository's `kernel_memory`".

Nothing was moved, and none of these locations is in the map.

### What "0 problems" does not check (DERIVED from `memory/memory_map.py:38-86` and the map text; the same in both versions)
- **`holds` values that are not kinds:** `drop_in: inbox_file`, `ram_embedding_cache: query_embedding`, `ram_embedding_cache: document_embedding`.
- **Routes to a store that does not list the kind:** `working_context → ram_hoard_cache`, `save_state → chroma_active`, `crystallization → metatron_db`.
- **A store listing a kind that is not routed to it:** `memory_db: node`.
- **Not checked at all:**
  - whether a store's path exists for its status;
  - whether `git:` matches git (the table above);
  - whether the writer text is true (2.2);
  - whether anything Hoard-like is left undeclared.

## 2.2 Trace: caller → function → store

Read-only code reading. `file:line` refers to the working tree the kernel runs.

### The Hoard objects
- **One Hoard in the kernel.** `cheshire_cat = CheshireCatKernel()` (`main.py:220`) builds the kernel's single `TheHoard()` (`sensory/cheshire_cat.py:60`).
  - Rodin shares it (`main.py:233`, `cheshire_cat.py:61`).
  - So does Phoenix's SWDS run (`main.py:1242-1251`).
- **Every `TheHoard()` writes when it is built:**
  - it creates the `kernel_memory/` folders and an empty `rolling_context.json` if missing (`memory/the_hoard.py:409-423`);
  - it calls Chroma's `get_or_create_collection` for the active space (`:425-433`). That is why the Chroma folder changes at every start (09:15:25).
- **A second Hoard.** `DailyPlanetProtocol()` builds a new `TheHoard()` when it is given none (`tools/daily_planet.py:295`), and Alexandria builds it that way (`memory/alexandria_protocol.py:44-57`).
  - Its nodes reach disk but not the kernel's in-memory cache (DERIVED).
  - The Shiva toolkit's Daily Planet call (`tools/shiva_toolkit.py:130-132`) has only a test caller (`tests/test_daily_planet_lifecycle.py:244`, `commit=False`).

### The four named functions
| Function | Writes to | Called from | Wired? | Ran? |
|:--|:--|:--|:--|:--|
| `commit_node_v2` (`the_hoard.py:634-692`) | the RAM cache (`:671`); the shard `raw_shards/<ccid>.json`, atomically (`:220-232`, `:674-678`); Chroma through `chroma_upsert` (`:681`) | `commit_node` (`:698-715`) ← `cheshire_cat.py:380` ← `POST /cognitive/cycle` (`main.py:809-829`); `daily_planet.py:587` ← Alexandria on a Rodin HALT ← `POST /rodin/query` (`main.py:381-397`); `sync_save_state` (`:972`); `auto_crystallize` (`:1127`) | yes, behind two POST routes | yes in the past (304 nodes); **none since boot** (newest shard 10-15 21:12:14) |
| `chroma_upsert` and `chroma_upsert_many` (`:459-518`) | the active Chroma collection, but only for a non-zero vector that names the active space (`:466`, `:495`) | `commit_node_v2` (`:681`); `embed_pending` (`:902`); `scripts/ingest_knowledge.py:523` (`--apply`, paid) | yes, but no live writer passes a vector, so nothing is indexed (DERIVED) | no shard holds a trusted vector (below), so no node row has come from it |
| `embed_pending` (`:849-906`) | the three embedding keys of each shard, atomically (`:834-847`); Chroma | `tools/rodin_reembed.py:70-72`, only with `--apply --yes-paid` (the default is a read-only plan) | tool only | no: the embedder has made 0 calls, and the 10/15 probe got 404 |
| `load_shards_from_disk` (`:806-828`) | the RAM cache only (it reads the shards and skips non-nodes) | `scripts/enter_swds.py:34`, `tools/rodin_reembed.py:71` | **not by the kernel** | the kernel holds 0 nodes |

### The other writers in the map
| Kind and store | Writer (`file:line`) | Wired? | Ran? (MEASURED) |
|:--|:--|:--|:--|
| save state → root `The Hoard` | the assistant, at a thread's end | n/a | `CCID_1792164893`, 10:35:53–10:36:40 |
| save state → `raw_shards` (as a node) | `sync_save_state` (`the_hoard.py:912-995`) via `sync_all_save_states` (`:997-1016`), whose default folder is `<integra-homebase>/The_Hoard` (`:1002`) | scripts only (`scripts/enter_swds.py:30`, `scripts/trigger_swds.py:33`) | 5 save-state nodes exist (4 `SAVE_STATE_CHECKPOINT`, 1 with a string payload); 3 of them cite `The_Hoard`, 1 cites `The Hoard` |
| crystallization → `raw_shards`; thermo loop → `metatron_db` | `auto_crystallize` (`:1061-1140`) → `record_loop` (`memory/database/metatron_deploy.py:161-198`) | **no caller** | 0 `CCID_CRYSTAL_*` shards; no Metatron write since 09-23 |
| Metatron session | `metatron_deploy.bootstrap` (`:148-158`, called at `main.py:110`) seeds a session only when the table is empty (`:127-143`) | at start | the boot CCID is generated but not stored (DERIVED from `:132`) |
| working context → `rolling_context.json` | `TheHoard` creates it; `PhoenixForge.consolidate_sleep_cycle` rewrites it (`evolution/phoenix_forge.py:178-195`, plain write, errors swallowed) | SWDS scheduler | 02:00:59 |
| library book → `libraries` | `consolidate_sleep_cycle` appends a chapter (`phoenix_forge.py:156-176`); `analyze_kintsugi_sandbox` (`:301-369`) | SWDS scheduler; the Kintsugi path is unreachable (`_kintsugi_ref` is never set) | 02:00:59 |
| identity → `core_identity.txt` | `StarfireProtocol.anchor_core_identity` (`core/starfire_protocol.py:378-404`, plain write), called from `DragonEngine.__init__` and `ignite` (`core/dragon_engine.py:130`, `:145`; peer code, uncommitted). In HEAD, `TheHoard` created the file if missing | at start | 09:15:30 |
| identity → `config/integra_identity_matrix.json` | **nothing writes it**; Starfire reads it (`starfire_protocol.py:164`) | — | mtime 09-24 05:00:16 |
| SWDS report → `swds_reports` | `runtime/swds_simulator.py:162-177` (T1); also `scripts/enter_swds.py:84-185` | the wake and the startup reconciliation | 09:15:31 (`CEL-F2-302.71deg`) |
| lobe chunk → Chroma | `scripts/ingest_knowledge.py` (`CCID_LOBE_*` ids `:369`; indexing `:523`) | script only | not since the change set (DERIVED); no `CCID_LOBE_*` shard exists |
| RAM embedding cache | `EmbeddingService`, an LRU of 512 entries (`memory/embedding_service.py:323-338`, `:455-460`) | in the kernel process | 0 entries (`/rodin/telemetry`) |

### Who wrote the shards (MEASURED, from structure only)
Each writer leaves a fixed anchor and payload shape, which identifies it.

| Writer | Nodes |
|:--|--:|
| Cognitive cycle (anchor x 1.0, y 0.5; payload `fused_knowledge`, `looking_glass_telemetry`, `cheshire_protocol_telemetry`, in 3 shapes: 223, 24 and 11 nodes) | 258 |
| Daily Planet (the anchor carries the frame-1 vector; `metadata.module` is `tools.daily_planet`) | 40 |
| Save-state sync (the anchor is Baker's latitude and longitude) | 5 |
| Other | 1 |
| **Nodes in all** (plus 4 non-node files) | **304** |

What the 304 nodes carry:
- **Time:** 258 anchors have `t = 0`, all of them cognitive-cycle nodes. No node carries a `celestial_stamp`.
- **Vectors:** 258 are all zeros, 45 are non-zero but name no space (untrusted), and 1 node has no vector field. None is trusted.
- **Outcome labels:** 259 at 0.5, 44 at 1.0, 1 missing.
- **Prompts:** all 258 cognitive-cycle nodes carry a non-empty `topic` string, between 11 and 319 characters long (median 35).
  - Only 27 distinct lengths occur, so many prompts repeat.
  - For the Daily Planet nodes, ADR-013 already says "40 shards repeat a handful of test queries" (CLAIMED). Which runs wrote them is not established here.
  - The prompts themselves were not read.

### Claims checked against behaviour (DERIVED from code)
| Claim | Behaviour |
|:--|:--|
| `commit_node_v2` "also persists the node as a raw shard" (`the_hoard.py:646-655`) | A failed shard write is printed and swallowed (`:675-678`), and the return value still says `COMMITTED_TO_HOARD_V2` with the shard's path (`:683-692`). The failure is not loud |
| Writes are atomic | True for commits and re-embeds (`:220-232`, `:847`). Not true for `mark_outcome`, an in-place `r+` rewrite (`:739-744`), nor for the library append (`phoenix_forge.py:169`), `rolling_context.json` (`:192`) or `core_identity.txt` (`starfire_protocol.py:402`) |
| One node per CCID | A CCID repeated within one second (`f"CCID_{int(created_at)}"`, `phoenix_forge.py:470`) silently replaces the earlier shard (`the_hoard.py:627`, `os.replace`) and leaves two cache entries under one CCID. T1 recorded this as open |
| `embed_pending` changes "only the three embedding keys" | True (`:834-847`) |
| `has_embeddings` in the commit receipt | True whenever a vector argument is given, even an all-zero one (`:689`). `chroma_synced` is the real signal |
| Phoenix's "consolidation completed across N raw interaction nodes" | With an empty cache, Phoenix reads the **first 10 shard files by name**, the same 10 every night (`phoenix_forge.py:120-132`). It appends 4 fixed axiom lines and a count (`:138-176`). The library's "Celestial Metadata" is `celestial_time()` plus Baker constants, not a Sentinel stamp. ADR-006's context says the same |
| Phoenix's Mad Hatter scan of stale nodes | `get_stale_nodes` reads only the RAM cache (`the_hoard.py:754-768`). In a kernel that never loaded the shards, it falls back to two fixed texts (`phoenix_forge.py:401-412`) |
| The save-state sync "synchronizes an external Save State (e.g. from The_Hoard/CCID_*.json)" | True to its own docstring, false to the map. It reads `integra-homebase/The_Hoard`, not the root `The Hoard/` where save states are written. Because `celestial_stamp=` is not passed (`:972-981`), the synced node gets a **new** Sentinel stamp at sync time, while its anchor `t` keeps the save state's own time |
| Working-tree map: `identity_matrix` is written by StarfireProtocol | Starfire only reads it (`starfire_protocol.py:164`); its mtime is 09-24 |
| `core_identity.txt`: "Identity Matrix & 6-Point Star Status: DEFINED_AND_TRUE" | A literal string (`starfire_protocol.py:400`, CONSTANT), the ADR-003 pattern |
| `scripts/enter_swds.py` report: "140/140 tests passing", "Cloud Dependencies: ZERO remaining" | Hard-coded literals (`:106-176`, CONSTANT). Run today, the script would also name its report with a frame-1 angle, because it builds its own `DualTemporalEngine()` (`:15-17`, `:89`). This corrects T1's design note that the two SWDS scripts take their time from `/clock` |

## 2.3 Verdict table

**States:**
- **LIVE:** wired, and it wrote on 10-16 (the time is in 2.2).
- **WIRED:** reachable from a kernel route or loop, with past runs only.
- **SCRIPT:** only a script or tool reaches it.
- **NO CALLER:** the code exists, but nothing calls it.
- **BY HAND:** the assistant or the Architect writes it.

| Kind | Declared store (primary; also) | Actual writer | State | Issue |
|:--|:--|:--|:--|:--|
| identity | working tree: `identity_matrix`; `core_identity` (HEAD: `core_identity` only) | `starfire_protocol.py:378`, via `dragon_engine.py:130`; the matrix is written by hand | LIVE (core), BY HAND (matrix) | the working-tree map names the wrong writer for the matrix; a tracked file is rewritten at every start; contains the literal "TRUE" |
| working_context | `rolling_context`; `ram_hoard_cache` | `the_hoard.py:419`, `phoenix_forge.py:178` | LIVE | `ram_hoard_cache` does not list this kind; the content is free of prompts today (only `last_swds_epoch`) |
| assistant_note | `claude_memory_index` | the assistant | BY HAND | — |
| node | `raw_shards`; `chroma_active`, `ram_hoard_cache` | `commit_node_v2`, via `/cognitive/cycle` and via Alexandria → Daily Planet | WIRED | **publishes prompts**; no Chroma rows; a failed write is silent; same-second CCIDs overwrite; a second Hoard object |
| save_state | `save_states_root`; `raw_shards`, `chroma_active` | the file: the assistant; the node: `sync_save_state` | BY HAND (file), SCRIPT (node) | the node path reads `integra-homebase/The_Hoard`; the node gets a new stamp at sync time; `chroma_active` does not list this kind |
| crystallization | `raw_shards`; `metatron_db` | `auto_crystallize` | NO CALLER | `metatron_db` does not list this kind |
| thermo_loop | `metatron_db` | `record_loop` | NO CALLER | SQLite and its WAL sit in OneDrive (ADR-005 action 4) |
| swds_report | `swds_reports` | `swds_simulator.py:162` | LIVE | 61 names carry frame-1 angles (the correction note is pending); `enter_swds.py` writes literals |
| library_book | `libraries` | `phoenix_forge.py:156` | LIVE | the same 10 shards every night; fixed text; no Sentinel stamp |
| lobe_chunk | `chroma_active` | `ingest_knowledge.py:523` | SCRIPT | waits for the embedder; the script's `--apply-hygiene` flag deletes files |
| conversation_archive | `antigravity_archive` | the Architect | BY HAND | stays local (1,916 files, all ignored) |
| ruling | `docs_blueprint` | by hand | BY HAND | 5 files are untracked; no ingestion lobe covers `docs/` |
| reading_ledger_row | `reading_ledger` | the assistant | BY HAND | — |
| task | `tasks` | by hand | BY HAND | — |
| handoff | `save_states_root`; `memory_db` | the assistant | BY HAND (file); the database is not built | — |
| secret | none (never) | — | — | not measured: that would need a content scan |

**Tally (15 kinds excluding `secret`):**
- 12 have a writer that has run at least once:
  - 4 LIVE on 10-16: identity, working_context, swds_report, library_book;
  - 1 WIRED with past runs: node;
  - 7 BY HAND.
- 3 have no writer that has run: crystallization (no caller), thermo_loop (no caller; nothing since 09-23) and lobe_chunk (script only, nothing in the active collection; DERIVED).

### Against "True means" and "Done when"
**True means:**
- **Each kind goes to the store the map names: partly.**
  - The live writers hit their primary stores.
  - But nothing enforces it: the map is not read by code.
  - The save-state node path and Alexandria's second Hoard diverge.
  - 8 Hoard-like locations are undeclared.
- **The cold store is the source of truth: yes on disk.** The shards are the only copy of the nodes; Chroma has no node rows, and RAM holds none.
- **Nothing private is published: not true.**
  - 258 published shards carry prompts.
  - The live log is tracked.
  - A second published copy of 239 shards exists.
  - Trading-simulation records sit in the node store.
- **Each function does what it claims: mostly.** The exceptions are in the claims table above.

**Done when:**
- **The map validates with 0 problems: met by the current validator,** which misses the 7 consistency gaps above.
- **Every kind has a measured writer: not met** (3 of 15).
- **The routing test passes: not started.** There is no routing to test yet (that is 2.5).

## T1's two live checks (re-read at 12:18)
- **Hoard node: still open.** No shard has been written since 09:14.
  - New finding: a node appears only through `POST /cognitive/cycle` (which makes model calls) or through `POST /rodin/query` → Alexandria. The Alexandria path is blocked while the embedder fails (DERIVED: Rodin returns a 503 before it reaches the HALT).
  - SWDS writes no node.
  - So this check closes the next time you run a cognitive cycle, or on an approved test POST.
- **Save state: no new one.**
  - New finding: the sync that would turn a save state into a node reads `integra-homebase/The_Hoard`, and only scripts run it. As wired, the node form of this check cannot pass. See ruling (f).

## Rulings needed (2.4), one batch (the blueprint was checked first)
- **(a) Cold nodes: public or local-only?**
  - The blueprint has no ruling on publishing. ADR-005 (Proposed) moves memory to a local `memory.db`.
  - Measured: 307 shards are on `origin`, and 258 of them carry prompts.
  - The options:
    - A: keep publishing.
    - B: stop publishing new nodes by git-ignoring and untracking `raw_shards/`, as in S3 (the files stay on disk). The GitHub history keeps the old ones; purging it is a separate, destructive step.
    - C: move the cold truth out of the repo with ADR-005.
  - **Recommendation:** B now, C later.
- **(b) The map, PROPOSED → live, with or without the peer's identity edit?**
  - **Recommendation:** approve it after 2.5 has:
    - closed the 7 consistency gaps;
    - declared the 8 locations (copies as `retired`);
    - corrected the identity writer text.
  - The identity edit is its owner's call.
- **(c) `memory.db` (ADR-005, Proposed 2026-10-09):** approve now, or defer?
  - **Recommendation:** defer. It needs the embedder and ruling (a), and T2 does not depend on it.
- **(d) The undeclared copies:** `integra-homebase/The Hoard`, both `The_Hoard` folders, the root `kernel_memory/` and the root `local_dbs/`.
  - **Recommendation:** declare them in the map now and move nothing. Dedupe them later under ADR-005 (action 3) and ADR-013 (action 2), after a backup.
- **(e) Shards at boot: load them at startup, or have telemetry report the on-disk count?**
  - **Recommendation:** report the on-disk count now; it is cheap and honest. Loading them belongs to Rodin's RAM tier (T8).
- **(f) T1's save-state check:** close it on the session-written frame-2 stamp, or require the node path?
  - The node path needs a 2.5 change: point the sync at the real save-state folder and pass the save state's stamp. A script run would then need its own go.
  - **Recommendation:** close the file-level check now, and carry the node path into 2.5.
- **(g) The live kernel log in the root repo:** untrack and ignore it (the S3 pattern; an older copy is already on `origin`), as ADR-010 item 2 implies?
  - **Recommendation:** yes, on a go.

## Next
- **2.4:** your rulings on (a)–(g).
- **Then 2.5, in an isolated copy, each piece its own go:**
  - a routing guard: `commit_node_v2` consults `place(kind)` and refuses a local-only kind into a tracked store;
  - the validator's missing checks;
  - loud commit failures;
  - a guard against CCID collisions;
  - the save-state sync's folder and stamp;
  - the map's new entries.
- **2.6** (the Chroma cleanup) stays parked.
- **Carried along:** the ADR-001 correction note and T1's two live checks.
