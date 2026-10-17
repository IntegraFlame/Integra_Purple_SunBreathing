# Task 02 verification: Connect the Hoard (steps 2.1–2.3, re-measured independently, read-only)

**Stamps** (GET `/clock`, HTTP 200, frame 2):
- **Start:** 2026-10-16 12:40:09 CDT | 17:40:09Z | rotation 353.8716°, lunar 0.1944, orbit 0.7804, ROT_330_ORB_70.
- **End of measurement:** 12:57:13 CDT | 17:57:13Z | rotation 358.1384°, lunar 0.1948, orbit 0.7805, ROT_330_ORB_70; kernel uptime 03 h 42 m 46 s.

**Usage at the start:** 5-hour window 21%, weekly 79% (resets 2026-10-19 06:00 CDT).

**Session:** `462c5ee3` ("Save state checkpoint").

**Why this report exists.** The Architect: "ignore the integra boot thread, that thread should be suspended, determine your place within the To-Do and report and wait for approval to begin." The boot session's T2 results (`Task02_REPORT.md`, 12:22:58) were therefore treated as CLAIMED. This session's last verified position was "T2 not started", and the Architect approved this plan between the 12:34:35 report stamp and the 12:40:09 start: T2 steps 2.1–2.3 re-measured here, read-only, then a claim-by-claim comparison, then a stop before the 2.4 rulings. The boot session was idle throughout and received no messages.

**This report is public-safe.** It holds counts, file names, hashes and code-level facts only; no shard text, prompt, query or summary was printed. `<user>` stands for the Windows user folder.

**Labels:** MEASURED, DERIVED, CONSTANT, CLAIMED; "exists in code", "wired" and "ran" are kept apart.

## Scope and method

- **No POST, kernel restart, paid call or test-suite run.** No code edit, no Chroma or SQLite opened, nothing staged or committed, no `.env` value read.
- **Isolated copy** `C:\Users\<user>\t2v\` (new; not the boot session's `t2s`), outside OneDrive. Hash-equal to the live files:

  | File | sha16 |
  |:--|:--|
  | `memory/memory_map.py` | `50b50ce9b3c1322b` |
  | `memory/__init__.py` | `e3b0c44298fc1c14` (0 B) |
  | `tools/rodin_memory_inventory.py` | `0be01cb538a71244` |
  | working-tree `config/rodin_memory_map.yml` | `00b961e6b4616bf7` (12,893 B) |
  | HEAD's map | blob `1a56596` (11,583 B; last changed in `e81e9a0`) |

- **How the code ran.** Three read-only scripts ran there with the kernel venv's Python (`-I -B -X utf8`), importing `memory_map` from `t2v` only (checked at run time):
  - `run_2_1.py`: validation and inventory, file metadata only;
  - `census_2_2.py`: opened each shard read-only and printed counts of keys and shapes;
  - `gaps_2_2.py`: map consistency, plus how many prompt-carrying shards are on `origin`.
- **The rest:** `grep`, reading code, `git ls-files` / `ls-tree` / `check-ignore`, and file metadata.
- **Evidence:** `t2v/scripts/` and `t2v/out/` (outside the repos).
- **Live tree unchanged by the measurement:**
  - root and nested `git status` were identical before (12:40) and after (12:57);
  - no `.pyc` and no other file under `integra-homebase/` changed after the 12:40:09 start marker (a `find -newer` run after the 12:57:13 stamp, pruning `.venv` and the vendored `Antigravity` folders, and excluding the kernel's own runtime writes: the Sentinel checkpoint every 300 s and the files it rewrites).

## Bottom line

- **The map validates but routes nothing.**
  - Both versions validate with 0 problems: HEAD has 20 stores and 16 kinds, the working tree 21 and 16.
  - No kernel code reads the map. Its only users are `tools/rodin_memory_inventory.py` and `tests/test_memory_map.py` (MEASURED, grep). Where a kind lands therefore depends on each writer's own path.
- **"0 problems" is the validator's limit, not the map's state:**
  - the map has 7 holds/kinds inconsistencies;
  - 2 stores' declared git state differs from git;
  - 8 Hoard-like locations are undeclared.
- **Private text is published** (MEASURED):
  - 258 nodes store the cycle's prompt (`payload.cheshire_protocol_telemetry.topic`; `sensory/cheshire_cat.py:118` passes the prompt in), and 257 of them are on `origin`;
  - all 40 Daily Planet nodes store their query, and all 40 are on `origin`;
  - the live kernel log is tracked in the root repo, and an older copy is on `origin`;
  - 239 shard copies are tracked in the root repo's `kernel_memory/` and are on its `origin` branch.
- **No node has been written since T1 went live.**
  - The newest shard is from 2026-10-15 21:12:14.
  - None of the 304 nodes carries a `celestial_stamp` or a trusted vector.
- **The boot session's report holds up.** Every claim I re-measured agrees with mine. The differences are later writes, plus one precision fix: 257 of the 258 prompt-carrying shards are on `origin`, not all 258.

## 2.1 Validation and inventory (MEASURED)

`run_2_1.py` output, verbatim headlines:
```
=== map HEAD: status PROPOSED, 20 stores, 16 kinds, 0 problem(s), measured in 0.2 s ===
=== map worktree: status PROPOSED, 21 stores, 16 kinds, 0 problem(s), measured in 0.2 s ===
```

The two versions differ only by the peer session's uncommitted identity edit:
- a new `identity_matrix` store;
- `core_identity`'s writer text changed from "TheHoard" to "StarfireProtocol";
- kind `identity` now has primary `identity_matrix`, also `core_identity`.

**Stores on disk** (working-tree map; the inventory's output file was written at 12:42:31; declared `git:` checked against git):

| Store | Tier | Files | Bytes | Newest file | Declared git / measured |
|:--|:--|--:|--:|:--|:--|
| `rolling_context` | W | 1 | 381 | 10-16 02:00:59 | tracked / tracked |
| `identity_matrix` (working tree only) | D | 1 | 6,605 | 09-24 05:00:16 | tracked / tracked |
| `core_identity` | D | 1 | 509 | 10-16 09:15:30 | tracked / tracked |
| `claude_memory_index` | W | 24 | 95,629 | 10-16 12:24:44 | outside-repo |
| `raw_shards` | C | 308 | 7,344,087 | 10-15 21:12:14 | tracked / **307 tracked, 1 untracked**; 307 on `origin` |
| `chroma_active`, `chroma_legacy` (one folder) | H | 6 | 124,872,394 | 10-16 09:15:25 | ignored / ignored |
| `libraries` | L | 4 | 144,488 | 10-16 02:00:59 | tracked / tracked |
| `modules`, `vectors_dir`, `drop_in` | D, H, I | 0 | 0 | — | tracked / empty |
| `metatron_db` | R | 1 | 32,768 | 09-23 20:19:00 | ignored / ignored |
| `save_states_root` (root `The Hoard`, without its two sub-stores) | S | 207 | 5,455,818 | see the inventory caveat | tracked / 204 tracked, 3 untracked |
| `swds_reports` | S | 75 | 319,702 | 10-16 09:15:31 | tracked / 74 tracked, 1 untracked |
| `antigravity_archive` | A | 1,916 | 305,999,800 | 10-15 12:13:29 | ignored / ignored |
| `docs_blueprint` | D | 16 | 1,164,384 | 10-16 12:23:32 | tracked / **10 tracked, 6 untracked** |
| `reading_ledger` | D | 1 | 357,738 | 10-13 02:11:05 | tracked / tracked |
| `tasks` | D | 1 | 35,063 | 10-16 11:25:40 | tracked / tracked |
| `memory_db` (proposed) | C | does not exist | | | outside-repo |
| `ram_embedding_cache`, `ram_hoard_cache` | W | RAM | | | n/a |

**Metatron:**
- the database was last written 09-23 20:19:00;
- `-wal` (4,152 B) at 09-23 20:51:17;
- `-shm` was touched at 10-16 09:15:31 (MEASURED).

**Inventory caveat** (MEASURED values; cause DERIVED). For `save_states_root`, the inventory at 12:42:31 reported its newest file as 12:18:12. Yet the live log had been written at 12:40:09, and at 12:45:17 both `os.scandir` and `os.stat` read 12:40:09. A file another process holds open can show a stale time in a directory listing, so `newest_mtime` can lag for the live log.

### What "0 problems" does not check

**DERIVED** from `memory/memory_map.py:38-86`; the gaps were MEASURED by `gaps_2_2.py` and are identical in both versions.
- **`holds` values that are not kinds:**
  - `ram_embedding_cache`: `query_embedding`, `document_embedding`;
  - `drop_in`: `inbox_file`.
- **A kind routed to a store whose `holds` omit it:**
  - `working_context` → `ram_hoard_cache`;
  - `save_state` → `chroma_active`;
  - `crystallization` → `metatron_db`.
- **A store that holds a kind which does not route to it:** `memory_db` holds `node`.
- **Not checked at all:**
  - path existence;
  - declared `git:` against git (2 mismatches above);
  - stores that share a path (`chroma_active` and `chroma_legacy`);
  - whether the writer text is true (2.2);
  - Hoard-like locations left undeclared (below).

### Hoard-like locations the map does not declare (MEASURED: metadata, git index, local remote-tracking refs)

| Location | Files | Bytes | Newest | Git | Note |
|:--|--:|--:|:--|:--|:--|
| `integra-homebase/The Hoard/` | 173 | 1,190,010 | 10-02 | 173 tracked, 173 on `origin` | an older copy of root `The Hoard` |
| `integra-homebase/The_Hoard/` | 6 | 17,439 | 09-24 | 6 tracked | 3 `CCID_*.json`; **the default source of `sync_all_save_states`** |
| root `The_Hoard/` | 6 | 17,439 | 09-28 | 6 tracked | same size as the nested one |
| root `kernel_memory/` | 249 | 44,339,783,038 | 10-16 10:34 | 247 tracked (239 shard copies), 247 on `origin` | holds Docker Desktop's WSL disks: `DockerDesktopWSL/disk/docker_data.vhdx` (44,234,178,560 B, written 10:34) and `main/ext4.vhdx`, both ignored |
| root `local_dbs/` | 1 | 188,416 | 09-28 | ignored | an old Chroma file |
| `integra-homebase/kernel_memory/ClaudeMemSuite.md` | 1 | 63,664 | 10-11 00:59 | tracked | a document inside kernel memory |
| `integra-homebase/local_dbs/celestial/` | 1 | 624 | 10-16 | ignored | T1's Sentinel checkpoint |
| `integra-homebase/runtime/swds_state.json` | 1 | 2,165 | 10-16 | tracked | rewritten by the kernel |

**Undeclared content inside declared stores:**
- the live log `The Hoard/genesis_kernel.log` (about 3.9 MB, tracked; `origin` holds a 146,709 B copy);
- 4 non-node files in `raw_shards`.

**Also unmapped** (runtime state, not Hoard-like): `runtime/workspace_state.json` (486 B, tracked, last written 10-01). It is written by `AntigravityRunner`, which `main.py:189` builds.

**Checked and not published:** the nested repo's `Antigravity/` and `Antigravity IDE/` folders (18,301 files) are git-ignored.

## 2.2 Trace: caller → function → store

Read-only code reading, MEASURED from the working tree the kernel runs.

**Hoard objects:**
- **The kernel's single Hoard** is `TheHoard()` at `sensory/cheshire_cat.py:60`. Rodin shares it (`main.py:233`), and so does the SWDS run (`main.py:1243-1248`).
- **Every `TheHoard()` writes when it is built** (`memory/the_hoard.py:396-433`):
  - the `kernel_memory/` folders;
  - `rolling_context.json` if missing;
  - Chroma's `get_or_create_collection`.
- **A second Hoard:** Alexandria builds `DailyPlanetProtocol()` with no Hoard (`memory/alexandria_protocol.py:44-47`), which builds its own `TheHoard()` (`tools/daily_planet.py:295`).

| Function | Writes | Called from | Wired | Ran |
|:--|:--|:--|:--|:--|
| `commit_node_v2` (`the_hoard.py:634-692`) | RAM cache (`:671`); shard, atomically (`:674-676`, via `:220-232`); Chroma via `chroma_upsert` (`:681`) | `commit_node` (`:698-715`) ← `cheshire_cat.py:380` ← `POST /cognitive/cycle` (`main.py:809`); `daily_planet.py:587` ← Alexandria ← `rodin_supervisor.py:190` (on a HALT) ← `POST /rodin/query` (`main.py:381`); `sync_save_state` (`:972`); `auto_crystallize` (`:1127`) | yes, behind two POST routes | newest shard 10-15 21:12:14; **none since T1** |
| `chroma_upsert`, `chroma_upsert_many` (`:459-518`) | the active collection, only for a non-zero vector that names the active space (`:466`, `:495`) | `commit_node_v2`; `embed_pending` (`:902`); `scripts/ingest_knowledge.py:523` | yes | no shard holds a trusted vector, so no node row came this way (DERIVED); Chroma not opened |
| `embed_pending` (`:849-906`) | three embedding keys per shard (`:834-847`); Chroma | `tools/rodin_reembed.py:70-72` | tool only | no trusted vector exists |
| `load_shards_from_disk` (`:806-828`) | RAM cache only | `scripts/enter_swds.py:34`, `tools/rodin_reembed.py:71` | **not by the kernel** (no call in `main.py`) | the kernel loads no shard (DERIVED) |
| `sync_all_save_states` (`:997-1016`) | nodes, via `sync_save_state` → `commit_node_v2` | `scripts/enter_swds.py:30`, `scripts/trigger_swds.py:33` | scripts only | reads `integra-homebase/The_Hoard` (`:1002`), not root `The Hoard` |

**Other writers:**
- **`rolling_context`:**
  - `the_hoard.py:419-423` creates it if missing;
  - `phoenix_forge.py:178-195` rewrites it with a plain write and swallows errors;
  - called from the SWDS scheduler; ran 02:00:59.
- **`libraries`:**
  - `phoenix_forge.py:156-176` appends a chapter (SWDS); ran 02:00:59;
  - the Kintsugi book (`:301`) cannot be reached: `_kintsugi_ref` is never assigned.
- **`core_identity`:** `core/starfire_protocol.py:378-402`, called from `core/dragon_engine.py:130,145` (peer code, uncommitted); ran 09:15:30. HEAD's map still names TheHoard.
- **`identity_matrix`:** nothing writes it. Starfire only builds its path (`starfire_protocol.py:122`) to read it. Last written 09-24.
- **`swds_reports`:** `runtime/swds_simulator.py:163-238`, with the Sentinel stamp, on wake (`main.py:1202`) and at the startup reconciliation; ran 09:15:31 (`CEL-F2-`).
- **`metatron_db`:** `record_loop` (`memory/database/metatron_deploy.py:161`) is called only from `auto_crystallize`, which has no caller.
- **`lobe_chunk`:** only `scripts/ingest_knowledge.py:523` writes it; there are no `CCID_LOBE_*` shards.
- **Writers the map does not name:**
  - `temporal/celestial_sentinel.py:341` (`local_dbs/celestial/checkpoint.json`);
  - `runtime/swds_simulator.py:75` (`runtime/swds_state.json`);
  - `core/sdk_harness.py:386-401` (session manifests; no caller);
  - `runtime/antigravity_runner.py:38` (`runtime/workspace_state.json`).

**Claims checked against behaviour** (DERIVED from code):

| Claim | Behaviour |
|:--|:--|
| A commit persists the shard | A failed shard write is printed and swallowed (`the_hoard.py:677-678`), and the receipt still says `COMMITTED_TO_HOARD_V2` |
| One node per CCID | Phoenix names nodes `f"CCID_{int(created_at)}"` (`phoenix_forge.py:470`), and `commit_node_v2` replaces an existing shard with no check (`:674-676`) |
| `has_embeddings` in the receipt | True for any vector argument, even all zeros (`:689`) |
| Writes are atomic | True for commits and re-embeds. Not true for `mark_outcome` (an `r+` rewrite, `:739-744`), the library append, `rolling_context.json` or `core_identity.txt` |
| SWDS consolidates the night's nodes | It reads the first 10 shard files by name (`phoenix_forge.py:119-132`) and appends 4 fixed axioms (`:138-143`). The library's "Celestial Metadata" is `celestial_time()` plus constants, not a Sentinel stamp (`:146-153`) |
| The save-state sync | The synced node gets a new Sentinel stamp at sync time, because no `celestial_stamp` is passed (`:972-981`) |
| `core_identity.txt` "DEFINED_AND_TRUE" | A literal string (`starfire_protocol.py:400`, CONSTANT) |

**Shard census** (`census_2_2.py`; MEASURED; counts only):

| Measure | Count |
|:--|--:|
| files | 308 |
| nodes | 304 |
| non-node files | 4 |
| nodes with a `celestial_stamp` | 0 |
| nodes with a trusted vector (`embed_space` set) | 0 |
| non-zero vectors that name no space (untrusted) | 45 |
| anchor `t` = 0 or missing | 258 |
| `cheshire_protocol_telemetry` with a non-empty `topic` (the prompt) | 258, of which 257 on `origin` |
| Daily Planet nodes (CCID shape) | 40, all on `origin`, each with a non-empty query |
| `SAVE_STATE_CHECKPOINT` payloads | 4 |
| `CCID_CRYSTAL_*` or `CCID_LOBE_*` shards | 0 |

## 2.3 Verdict table

**States:**
- **RAN 10-16:** wired, and it wrote today.
- **WIRED:** reachable from a kernel route or loop, with past writes only.
- **SCRIPT:** only a script or tool reaches it.
- **NO CALLER:** the code exists, but nothing calls it.
- **BY HAND:** the assistant or the Architect writes it.

| Kind | Declared (primary; also) | Actual writer | State | Issue |
|:--|:--|:--|:--|:--|
| identity | working tree: `identity_matrix`; `core_identity` (HEAD: `core_identity`) | `starfire_protocol.py:378` via `dragon_engine.py:130`; the matrix only by hand | RAN 10-16 (core), BY HAND (matrix) | the working-tree map names a reader as the matrix's writer; HEAD's writer text is stale; a tracked file is rewritten at each start |
| working_context | `rolling_context`; `ram_hoard_cache` | `the_hoard.py:419`, `phoenix_forge.py:178` | RAN 10-16 | `ram_hoard_cache` omits this kind; the write swallows errors |
| assistant_note | `claude_memory_index` | the assistant | BY HAND | — |
| node | `raw_shards`; `chroma_active`, `ram_hoard_cache` | `commit_node_v2` via `/cognitive/cycle` and Alexandria | WIRED | prompts and queries published; silent write failure; same-second CCID overwrite; a second Hoard object; nothing since T1 |
| save_state | `save_states_root`; `raw_shards`, `chroma_active` | the file: the assistant; the node: `sync_save_state` | BY HAND (file), SCRIPT (node) | the node path reads the wrong folder; the node's stamp is the sync time; `chroma_active` omits this kind |
| crystallization | `raw_shards`; `metatron_db` | `auto_crystallize` | NO CALLER | `metatron_db` omits this kind |
| thermo_loop | `metatron_db` | `record_loop` | NO CALLER (last write 09-23) | SQLite and its WAL in OneDrive (ADR-005) |
| swds_report | `swds_reports` | `swds_simulator.py:163` | RAN 10-16 | the frame-1 names await the correction note |
| library_book | `libraries` | `phoenix_forge.py:156` | RAN 10-16 | the same 10 shards nightly; fixed text; no Sentinel stamp |
| lobe_chunk | `chroma_active` | `ingest_knowledge.py:523` | SCRIPT | waits for the embedder; Chroma rows not checked |
| conversation_archive | `antigravity_archive` | the Architect | BY HAND | all 1,916 files ignored |
| ruling | `docs_blueprint` | the assistant and the Architect | BY HAND | 6 files untracked although the store says tracked |
| reading_ledger_row | `reading_ledger` | the assistant | BY HAND | — |
| task | `tasks` | the assistant and the Architect | BY HAND | — |
| handoff | `save_states_root`; `memory_db` | the assistant | BY HAND (file); the database does not exist | — |
| secret | none (never) | — | — | not measured (it would need a content scan) |

**Tally (15 kinds, `secret` excluded):**
- **12 with a writer that has run:**
  - 4 ran on 10-16: identity, working_context, swds_report, library_book;
  - 1 WIRED with past writes: node;
  - 7 BY HAND.
- **3 with no writer that can run now:** crystallization (no caller), thermo_loop (no caller; last write 09-23) and lobe_chunk (script only).

**Against T2's "True means":**
- **Each kind goes to the store the map names: partly.** The live writers hit their primary stores, but nothing enforces it.
- **The cold store is the source of truth: yes on disk.** The shards are the only node copy, the kernel holds none in RAM, and Chroma can hold no trusted node row (DERIVED).
- **Nothing private is published: not true.** See the bottom line.
- **Each function does what it claims: mostly.** The exceptions are in the claims table.

**Against "Done when":**
- **The map validates with 0 problems:** met by the current validator, which misses the gaps above.
- **Every kind has a measured writer:** not met (3 of 15).
- **The routing test passes:** not started; that is step 2.5.

## T1's two live checks (measured 12:42:31–12:45:17, the file times of the inventory and census outputs)

- **Hoard node: still open.** No shard has been written since 2026-10-15 21:12:14. Only `POST /cognitive/cycle` (model calls) or `POST /rodin/query` → Alexandria writes a node; SWDS writes none.
- **Save state: open, and a ruling.**
  - `The Hoard/CCID_1792164893.json` (written 10:36:27 by session `f9e973c9`) carries a frame-2 `celestial_stamp` taken from a `/clock` reading, not from kernel code.
  - The node form cannot pass as wired, because the sync reads the wrong folder.

## Cross-check with `Task02_REPORT.md` (the boot session's first pass, 28,100 B, sha16 `f045d9119ab5cc07` MEASURED; CLAIMED until now)

- **Agree:**
  - validation and store counts;
  - git states;
  - the 8 undeclared locations, including the root `kernel_memory/` byte total, to the byte;
  - Metatron's database, WAL and SHM times;
  - the 7 holds/kinds gaps;
  - the one-Hoard / second-Hoard trace;
  - the four-function table;
  - the other writers;
  - the claims-vs-behaviour items I checked: silent failure, CCID overwrite, `has_embeddings`, non-atomic writes, SWDS's first 10 shards, the library stamp, the sync stamp, the Starfire reader, the literal "TRUE";
  - the shard census (304 nodes, 4 non-nodes, 258 with a prompt and t = 0, 45 untrusted vectors, 0 stamps, 40 Daily Planet);
  - the verdict table and its tally;
  - the T1 live checks.
- **Differ, explained by later writes:**
  - `docs_blueprint` is 28,420 B larger: its own `Task02_REPORT.md` plus its `TODO.md` edit.
  - `claude_memory_index` has grown since its own 12:24 memory edits.
  - `save_states_root` grew with the live log.
  - Root `kernel_memory/` is newer because Docker kept writing.
- **Precision fix:** "258 published shards carry prompts" should read **258 carry prompts, 257 of them on `origin`**. The 258th is the untracked 10-15 21:12 shard.
- **Added here:**
  - the 40 Daily Planet nodes on `origin` store their query text;
  - the inventory's newest-file lag for an open file;
  - the unmapped runtime writers (`celestial_sentinel.py:341`, `swds_simulator.py:75`, `sdk_harness.py:386-401`, `antigravity_runner.py:38`);
  - the `Antigravity` folders are ignored.
- **Not checked here:**
  - outcome-label counts and prompt-length statistics;
  - the RAM node count from `/rodin/telemetry` (DERIVED instead from code);
  - the Shiva toolkit's test-only caller;
  - `metatron_deploy.bootstrap` at start;
  - the embedding cache's LRU size;
  - the Mad Hatter fallback;
  - the `enter_swds.py` literals;
  - Rodin's 503 before a HALT.

## What is true now, and what is not

- **True (MEASURED):** both maps validate. The live writers of identity, working context, SWDS reports and library books ran today. The cold store on disk is the only node copy. The Sentinel checkpoint and reports carry frame 2.
- **Not true:**
  - the map routes nothing;
  - nothing private is published (it is);
  - every kind has a writer that ran;
  - nodes carry stamps (none since T1);
  - the save-state sync reads the real save states.

## Decisions needed (the 2.4 batch, to be asked at the next gate after checking the blueprint)

1. **Cold nodes:** keep publishing `raw_shards`, or make the cold store local-only? And what about the 257 prompt shards and 40 query shards already on `origin`? Purging history is a separate, destructive step.
2. **The map:** PROPOSED → live: when, and with or without the peer's identity edit?
3. **`memory.db` (ADR-005, Proposed):** approve or defer?
4. **The 8 undeclared locations:** declare them, move them, or leave them?
5. **Shards at boot:** load them (the RAM tier, T8), or have telemetry report the on-disk count?
6. **T1's save-state check:** does the session-written frame-2 save state count, or must the node path work first?
7. **The live kernel log in the root repo:** untrack and ignore it?
8. **The map's writer text** (the `identity_matrix` reader; HEAD's `core_identity`): correct it in 2.5's map fixes?

## Rulings (2.4): the Architect, 2026-10-16

**Recorded at** GET `/clock` 14:55:27 CDT | 19:55:27Z | rotation 27.6979°, lunar 0.1975, orbit 0.7807, ROT_0_ORB_70, frame 2.

**How they were asked:**
- the blueprint (v.9.9.1, sha16 `cbcebbf137168db1`) was checked first, along with the 10-15 design decisions;
- each question showed the measurements and the blueprint's lines;
- options were given with no recommended set.

The batch folded the eight topics above into R1–R8: topic 8 (writer text) became part of R2, and D-14 (carried from T1) became R8.

| # | Ruling | What it means for T2 |
|:--|:--|:--|
| R1 | **Keep publishing** cold nodes | `raw_shards` stays tracked and pushed, and the map keeps it `public-repo` / `tracked`. No history change. |
| R2 | **The map goes live after 2.5, from the HEAD version** (without the peer's identity edit) | 2.5's map fixes start from HEAD's map (blob `1a56596`): close the 7 holds/kinds gaps, declare the 8 locations, correct the writer text. The live working tree holds the peer's uncommitted edit of the same file, so the 2.5 plan must say how the HEAD-based map replaces it (that is your go). |
| R3 | **`memory.db` (ADR-005) is deferred to Phase 2** | `raw_shards` stays the cold truth through T2; ADR-005 keeps its roadmap place (L1586). |
| R4 | **Declare the 8 locations; move nothing** | 2.5 adds map entries for them (the copies as retired). Nothing moves or is untracked. |
| R5 | **Nothing until T8** | No telemetry or boot-loading change in T2. |
| R6 | **T1's save-state check stays open for the node path** | 2.5 points the sync at the real save-state folder and passes each save state's own stamp. The check closes after one approved script run reads a stamped node back. |
| R7 | **The live log waits for ADR-010** | No untracking now. |
| R8 | **D-14: rewrite the stamps.** This overrides the blueprint's recommendation, "relabel with a correction note, don't rewrite" (L1006, L1644). | The T1 leftover becomes a rewrite of the skewed stamps in the artifacts themselves, not a note. Before any change it needs its own design: which artifacts (shard anchors, SWDS report names and headers, library epochs); which true time (the file times are the key); how frame-1 values are recomputed (the Sentinel's frame math); and, since R1 keeps the shards published, the rewritten shards are published too. |

The blueprint's §11 D-14 row and ADR-001 action 4 still carry the old recommendation. They change at the next blueprint revision.

## Files

- **Outside the repos:**
  - `C:\Users\<user>\t2v\`: copies, three scripts, outputs;
  - this report's scratch copy.
- **Written into the live tree after the measurement** (scratch → hash check → `cmd.exe /c copy` → hash check):
  - this report;
  - the T2 row in `docs/brainmap/TODO.md`;
  - the pointer line in `productivity/TASKS.md`.
- **Outside the repos:** the Neural Atlas memory note and its index line.
- **Not committed or staged.** `docs/brainmap/` is untracked in the nested repo; `productivity/TASKS.md` was already modified in the root.

## Next

- **The 2.4 rulings are decided** (above).
- **The next gate is the 2.5 plan**, on the Architect's go. It covers work in an isolated copy, each piece its own go:
  - a routing guard;
  - the validator's missing checks;
  - loud commit failures;
  - a CCID collision guard;
  - the save-state sync's folder and stamp (R6);
  - the map's fixes and new entries from HEAD (R2, R4);
  - the R8 stamp rewrite, as its own design inside the plan.
- **2.6 (Chroma cleanup)** stays parked.
- **Carried along:** the ADR-001 correction note and T1's two live checks.
