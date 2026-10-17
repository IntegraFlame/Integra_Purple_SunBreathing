# T2 step 2.5: the plan (from rulings R1–R8)

**Stamp** (GET `/clock`, HTTP 200, frame 2): 2026-10-16 15:18:00 CDT | 20:18:00Z | rotation 33.3344°, lunar 0.1981, orbit 0.7807, ROT_30_ORB_70.

**Usage:** 5-hour window 5%, weekly 80% (resets 2026-10-19 06:00 CDT).

**Session:** `462c5ee3`.

**Status: plan only.** Nothing was built, copied in, committed or restarted for this document. The Architect's instruction: "plan step 2.5 from rulings R1-R8 (isolated copy first, each piece its own go), including the R8 stamp-rewrite design and how the HEAD map replaces the peer's edit. Plan only, then stop."

**Inputs:**
- `Task02_VERIFICATION_REPORT.md` (measurements; the rulings table);
- `Task02_REPORT.md` (the first pass);
- blueprint v.9.9.1;
- new read-only measurements for this plan: `C:\Users\<user>\t2v\out\r8_scope.json` and a save-state type count (counts only).

**This document is public-safe.** `<user>` stands for the Windows user folder, `<project>` for the Claude project folder.

## The rulings this plan follows

| # | Ruling | Effect on 2.5 |
|:--|:--|:--|
| R1 | Keep publishing cold nodes | No untracking; `raw_shards` stays `public-repo` / `tracked` in the map |
| R2 | The map goes live after 2.5, from the HEAD version | P1 starts from HEAD's map; P9 flips the status |
| R3 | `memory.db` deferred to Phase 2 | Not in 2.5 |
| R4 | Declare the 8 locations; move nothing | P1 adds map entries only |
| R5 | Nothing until T8 | No telemetry or boot-loading change |
| R6 | The save-state check stays open for the node path | P6, then one approved run |
| R7 | The live log waits for ADR-010 | Not in 2.5 (declared in the map only) |
| R8 | D-14: rewrite the stamps | P7 |

## How every piece runs (the T1 method)

- **Gates.** Each piece has its own gates:
  1. build and test in an isolated copy;
  2. copy into the live tree;
  3. commit;
  4. for kernel code, a restart (or a natural reboot).

  Each gate is your go. Nothing is pushed; pushing stays on your word.
- **Isolated copy.** A fresh copy of the live nested tree, outside OneDrive. It is built with T1's `build_from_live.py` and run with `run_each.py` (both in `<project>/rodin_changeset_2026-10-15/applied_2026-10-15/`), each re-read before use.
  - The baseline suite runs first. The expected baseline is 3 known failures: 2 from the peer's `the_hoard.py` identity edit, and 1 env-only (Voltron).
  - Then the change runs: 0 new failures, plus mutation checks on every new guard.
  - Test runs go in the background, because the machine is often saturated.
- **Peer edits.** The live tree carries peer sessions' uncommitted edits: `memory/the_hoard.py` (identity hunks), `core/dragon_engine.py`, `core/starfire_protocol.py`, `config/rodin_memory_map.yml`.
  - Our changes to a file with peer hunks are committed hunk-wise (`git merge-file` + `hash-object` + `update-index`), leaving the peer hunks unstaged, as in T1.
  - The one exception is the map (P1); see "The HEAD map and the peer's edit".
- **Copy-in.** Scratch copy, then a hash check of the live target, then `cmd.exe /c copy`, then a hash check.
- **Commits.** Named files only, after the pre-commit forbidden-path check. Never a runtime-written file (`runtime/swds_state.json`, `kernel_memory/*`).
- **When kernel code takes effect.** The kernel-code changes (P2, P4, P5, P6, P8) apply only at the next kernel start. Batching them lets one approved restart cover them all.

## The pieces

| Piece | What | Files | Tests | Depends on |
|:--|:--|:--|:--|:--|
| **P1** | The map from HEAD, fixed (R2, R4) | `config/rodin_memory_map.yml` | the stronger validator reports 0 problems | P3 (built together) |
| **P2** | Routing guard | `memory/the_hoard.py` | new `tests/test_hoard_routing.py` (T2's routing test) | P1, P3 |
| **P3** | The validator's missing checks | `memory/memory_map.py`, `tools/rodin_memory_inventory.py` | `tests/test_memory_map.py` | built with P1 |
| **P4** | Loud commit failures | `memory/the_hoard.py`, `memory/alexandria_protocol.py` | `tests/test_hoard_schema_v2.py` | — |
| **P5** | CCID collision guard | `memory/the_hoard.py` (plus the CCID policy decided at the gate) | the same file | P4 |
| **P6** | The save-state sync: folder, filter and stamp (R6) | `memory/the_hoard.py`, new `tools/sync_save_states.py` | `tests/test_swds_and_hoard_sync.py` | P5 |
| **P7** | The R8 stamp rewrite | new `tools/stamp_rewrite.py`, its tests and fixtures | new `tests/test_stamp_rewrite.py` | none (P6 first, so no sync runs meanwhile) |
| **P8** | One Hoard object | `orchestration/rodin_supervisor.py` or `main.py`, `memory/alexandria_protocol.py` | a wiring test | — |
| **P9** | Close 2.5: the map goes live (R2), Done-when, the T2 report | — | re-run 2.1 and the routing test | P1–P6, P8 |

**Not in 2.5:**
- R1: no untracking. R3: `memory.db` is Phase 2. R5: no telemetry or boot loading before T8. R7: the log waits for ADR-010.
- The SWDS consolidation logic (the first 10 shards, the fixed axioms) is T5.5 and ADR-006.
- The Chroma cleanup (2.6) and the embedder key route stay parked.

## P1 + P3: the map from HEAD, and a validator that checks it

### The HEAD map and the peer's edit (R2)

- **The base** is HEAD's map: blob `1a56596`, 11,583 B, last changed in `e81e9a0`.
- **The live file** (sha16 `00b961e6b4616bf7`) also carries a peer session's uncommitted edit, +17/−3 lines:
  - a new `identity_matrix` store;
  - new writer text for `core_identity`;
  - kind `identity` routed to `identity_matrix`.
- **Why the edit must leave the working tree.** R2 makes the HEAD version the live map, and P2's guard will read the file at runtime. If the peer's edit stayed in the working tree, the running kernel would route by it. A hunk-wise commit is not enough here.
- **At the apply gate:**
  1. Check that the peer sessions are idle and the live file still hashes `00b961e6b4616bf7`.
  2. Save the peer's edit as a patch outside the repo (`git diff HEAD -- config/rodin_memory_map.yml`) in `<project>/brainmap_t2_2026-10-16/`, with its sha16.
  3. Copy in the HEAD-based fixed map, and check its hash.
  4. Commit it (its own gate).
- **The peer's code edits are not touched** (`the_hoard.py` identity hunks, `dragon_engine.py`, `starfire_protocol.py`).
  - While they run, Starfire writes `core_identity.txt` (`starfire_protocol.py:378-402`, from `dragon_engine.py:130,145`); HEAD's code instead lets TheHoard create it if missing (`the_hoard.py:415-416` at HEAD).
  - The HEAD-based map states both in a note, so its writer text is true for committed and running code alike.
- **If you accept the identity edit later,** the patch re-applies with `git apply --3way`, and the map is validated again.

### Map fixes, each a proposed resolution for your OK at the build gate

**The 7 holds/kinds gaps:**
1. `ram_embedding_cache` holds `query_embedding` and `document_embedding`, which are not kinds. Fix: define the two kinds (primary `ram_embedding_cache`, `embed: false`).
2. `drop_in` holds `inbox_file`, which is not a kind. Fix: define it (primary `drop_in`).
3. `memory_db` holds `node`, but `node` does not route there. Fix: since R3 defers `memory.db`, drop `node` from its `holds` until ADR-005. `handoff` routes there correctly.
4. `working_context` lists `ram_hoard_cache`, whose `holds` omit it. Fix: drop `ram_hoard_cache` from `working_context.also`, because the RAM cache holds only HoardNodes (`the_hoard.py:362`; DERIVED).
5. `save_state` lists `chroma_active`, whose `holds` omit it. Fix: add `save_state` to `chroma_active.holds`; it is true once a save-state node is embedded (`the_hoard.py:962-981`).
6. `crystallization` lists `metatron_db`, whose `holds` omit it. Fix: drop `metatron_db` from `crystallization.also`. Metatron gets a `thermo_loop` row, which is a different kind (`the_hoard.py:1094-1102`).

That is 7 gaps in 6 fixes (item 1 covers two).

**Declaring the 8 locations (R4; nothing moves):** new store entries with the measured git state. Retired copies hold nothing.
- `integra-homebase/The Hoard/` (retired copy; tracked);
- `integra-homebase/The_Hoard/` (retired; tracked; the sync's old default);
- root `The_Hoard/` (retired; tracked);
- root `kernel_memory/` (retired copy; tracked; `DockerDesktopWSL/` noted as foreign application data, ignored, ADR-011 N4);
- root `local_dbs/` (retired; ignored);
- `kernel_memory/ClaudeMemSuite.md` (document; tracked);
- `local_dbs/celestial/` (live; ignored; written by the Sentinel, `celestial_sentinel.py:341`);
- `runtime/swds_state.json` (live; tracked; `swds_simulator.py:75`; rewritten by the kernel).

**Also:**
- `The Hoard/genesis_kernel.log` as its own live store, excluded from `save_states_root`, with a note that it waits for ADR-010 (R7);
- a note on the 4 non-node files in `raw_shards`;
- optionally `runtime/workspace_state.json` (`antigravity_runner.py:38`).

**Writer text checked against code (2.2):**
- `swds_reports`: `runtime/swds_simulator.py` (plus `scripts/enter_swds.py`);
- `raw_shards`: also `mark_outcome` (an in-place `r+` write);
- `ram_hoard_cache`: also `tools/rodin_reembed.py`;
- `metatron_db`: also `metatron_deploy.bootstrap` at start (from the first pass; verified at the build gate).

**Kinds without a writer that can run** (crystallization and thermo_loop have no caller; lobe_chunk waits for the embedder). T2's "every kind has a measured writer" cannot be met for them without wiring them. Proposal: a per-kind `writer_state` (`live` | `no-caller` | `blocked`) that the validator reports. Done-when would then read "every live kind has a measured writer". Your ruling at the build gate.

### Validator checks to add

In `memory/memory_map.py`, pure functions; each gets a failing-map test and a passing-map test in `tests/test_memory_map.py`, plus mutation checks.
1. Every `holds` value is a defined kind.
2. Every kind→store route appears in that store's `holds`, and every `holds` entry is routed back.
3. Stores that share a path say so (`shares_path_with`), as `chroma_active` and `chroma_legacy` do.
4. In the inventory tool, not the pure validator: `check_disk` (a live store exists, a proposed one does not; metadata only).
5. Also in the inventory tool: `check_git` (declared `git:` against `git ls-files` / `check-ignore`; read-only).

## P2: the routing guard (T2's routing test)

- **The change:**
  - `commit_node_v2` gains `kind: str = "node"`, and callers pass their kind: the cognitive cycle and Daily Planet `node`, `sync_save_state` `save_state`, `auto_crystallize` `crystallization`.
  - `TheHoard` loads and validates the map once, at construction.
  - Before writing a shard, it checks with `memory_map.place(kind)` that `raw_shards` is the kind's primary or `also` store.
  - A kind not routed there, an unknown kind, or a kind that must stay local-only (`conversation_archive`, `secret`) is refused loudly: `HoardRoutingError`, logged.
- **R1's effect:** `node`, `save_state` and `crystallization` keep landing in the public store.
- **Your ruling at the build gate:** if the map cannot be read at start, fail closed (no commits) or fail open with a loud error on every receipt (`routing_check: UNAVAILABLE`)?
- **The routing test:**
  - each routed kind lands in `raw_shards`;
  - `conversation_archive` and `secret` are refused;
  - an unknown kind is refused;
  - a broken map behaves as ruled.

## P4: loud commit failures

- **In `commit_node_v2`:**
  - add the node to the RAM cache only after its shard is written;
  - on a failed write, raise `HoardWriteError` (logged), never `COMMITTED_TO_HOARD_V2` (today: `the_hoard.py:671-692`);
  - make `has_embeddings` true only for a trusted vector (`:689`).
- **`mark_outcome`** uses the atomic writer (`:739-744`).
- **Callers:**
  - the cognitive cycle already turns an exception into `CYCLE_EXECUTION_ERROR` (`cheshire_cat.py:387-395`);
  - Alexandria's `except Exception: pass` (`alexandria_protocol.py:68-69`) logs and returns a failure instead.

## P5: CCID collision guard

- **The guard:** `commit_node_v2` refuses to replace an existing shard or a CCID already in the RAM cache, with `HoardCollisionError`. Re-embedding keeps its own path (`_merge_embedding_into_shard`).
- **The cause:** CCIDs are `CCID_<int unix>` (`phoenix_forge.py:470`; the Sentinel's `ccid()`, `celestial_sentinel.py:294-296`), so two nodes in one second collide.
- **Your ruling at the build gate:** either (a) the caller retries with a suffix (`CCID_<unix>_2`), or (b) the Sentinel's `ccid()` gains a per-second sequence. (b) changes T1 code.

## P6: the save-state sync (R6)

- **Folder:** the default becomes the map's `save_states_root` (root `The Hoard/`), instead of `integra-homebase/The_Hoard` (`the_hoard.py:1002`).
- **Which files (MEASURED for this plan):**
  - the folder holds 117 `CCID_*.json`, of which only 7 carry `"type": "SAVE_STATE"`, 11 have a sibling `_SAVE_STATE_REPORT.md`, and 110 have no type;
  - today's sync would turn all 117 into save-state nodes;
  - proposal: a file counts if it has the type or the sibling report (your ruling at the build gate).
- **Already synced:** skip a CCID whose shard exists (this works with P5).
- **The stamp:** the node gets a Sentinel stamp taken at the save state's own time, `CelestialSentinel.stamp("save_state", at=<the file's celestial_stamp.unix_epoch>)` (`celestial_sentinel.py:265-292`, no I/O), instead of a new stamp at sync time. The anchor's `t` uses the same time. Only 5 of the 117 files carry `celestial_stamp.unix_epoch` (MEASURED; which of them are save states is not yet measured). A save state without it falls back to the CCID's own unix time, marked as such.
- **Payload:** the mapping also reads `work_pending_in_order` (the key `CCID_1792164893.json` uses).
- **The run:** a small `tools/sync_save_states.py`, a dry run by default, with `--apply` on your go. Not `scripts/enter_swds.py`, which also writes an SWDS report with a frame-1 name. One approved run writes the save-state nodes into `raw_shards`, which is published under R1. Reading one back with a frame-2 `celestial_stamp` closes T1's save-state check.

## P7: the R8 stamp rewrite (D-14 = rewrite)

**What is wrong, and the key for the true time** (MEASURED for this plan, counts only):

| Artifact | Count | What is wrong | True-time key |
|:--|--:|:--|:--|
| SWDS report names and headers (root `The Hoard/Slow-Wave Deep Sleep Reports/`, 74 tracked of 75 files) | 55 `CEL-282.85deg` (a constant fallback), 14 other frame-1 angles, 1 already `CEL-F2-`, 5 undated | dates from the frozen clock; the angle is a constant or frame 1. Name times trail file times by under 1 h (10), 1 h–1 d (41), 1–7 d (14), 7–14 d (4), 14–60 d (1) | the file time for the 61 files with distinct times. 12 files share one second (09-28 02:35:19) and 2 share another (09-29 03:15:46), both bulk copies: for those, the kernel log or the report's own text, otherwise marked unresolved |
| Library chapters (`library_genesis_purple.md`) | 69 chapters, stamped 09-18 to 10-16; 12 stamped 10-07 to 10-09 | `unix_epoch` from the frozen clock, and no frame-2 vector | per chapter, the true time of its SWDS cycle, matched to that cycle's report (the per-day counts match: 10-02: 19 each, 10-03: 18 each) |
| Shard anchors with `t` = 0 | 258 | the time is missing | the node's own `created_at` |
| Shards with a frame-1 vector | 42 (40 Daily Planet anchors in x/y/z/orbital_index, 2 with named fields) | frame-1 values | recomputed in frame 2 at the node's `created_at` |
| `created_at` itself | 304 | cannot be checked for most nodes: 201 shards carry 09-24 file times and 164 share one second (a bulk copy), so file times are not creation times | **not rewritten** (no better key); flagged |

**The design:**
- **Rewrite in place, with an audit trail.**
  - Shards get a `stamp_rewrite` field: the old values, the key used, the date.
  - Reports and the library keep the old line in an HTML comment.
  - One correction table (JSON) in the Hoard lists every change.
  - Git history keeps the originals.
- **New stamps come from the Sentinel's frame math at the true time** (`stamp(kind, at=…)`, no I/O), so they are frame 2. The Sentinel has one provenance code today (`PROVENANCE_TRUE_CLOCK = 1`), so rewritten stamps need their own (for example `2` = rewritten from a recorded key). That is a small Sentinel change, ruled at the design gate.
- **Identifiers stay.** CCIDs and Daily Planet report IDs are not renamed. SWDS report file names are stamps, so they are renamed with `git mv`, old → new recorded in the table.
- **Scope:** canonical artifacts only. The retired copies (R4: nested `The Hoard/`, both `The_Hoard/`, root `kernel_memory/`) stay as they are.
- **Tool:** `tools/stamp_rewrite.py`, a dry run by default. It writes the correction table and a diff in the isolated copy, and is tested on fixtures.
  - Then, for each artifact class, a gate to apply it in the live tree while no kernel write runs.
  - Then a gate per commit: the nested repo for shards and the library, the root repo for reports.
  - R1: the rewritten shards are published.
- **What it replaces:** ADR-001 action 4's correction note (D-14 is now "rewrite"), and T1's rule that "frame-1 stamps stay valid only within frame 1" for the rewritten artifacts. The blueprint's §11 D-14 row and ADR-001 action 4 change at the next blueprint revision.

## P8: one Hoard object

- **Today:** Alexandria builds `DailyPlanetProtocol()` with no Hoard (`alexandria_protocol.py:44-47`), which builds a second `TheHoard()` (`daily_planet.py:295`).
- **The fix:** the kernel passes its own Hoard down, `AlexandriaProtocol(daily_planet=DailyPlanetProtocol(hoard=cheshire_cat.hoard))`, where `rodin_supervisor.py:60` and `main.py:233` build it. Daily Planet nodes then reach the kernel's RAM cache and its single Chroma client.

## P9: closing 2.5

- **The map goes live:** its status changes from PROPOSED to live once P1–P6 and P8 are in (R2).
- **Re-measure:** run 2.1 again (the stronger validator and the inventory), plus the routing test; check T2's Done-when.
- **Report:** write the T2 report, then stop for gate K's tally.

## Order and gates

1. **P3 + P1** (validator and the HEAD map): build gate, then apply gate (the peer's patch is saved first), then commit gate.
2. **P2, P4, P5** (`the_hoard.py`; one build, three reviewable changes): build, apply, commit hunk-wise, then a restart gate (batched).
3. **P8:** build, apply, commit. Its restart is batched with step 2.
4. **P6:** build, apply, commit, restart (batched), then the gate for the one sync run.
5. **P7:** the design gate (this plan), then a dry-run gate, then an apply gate per artifact class, then a commit gate per repo.
6. **P9.**

**Budget:**
- This session's context window was 74% full when this plan was written.
- A save state before step 1's build would let a fresh session carry 2.5.
- Weekly usage is 80% until 2026-10-19 06:00 CDT.

## Rulings to make at the gates (not now)

- **P1:** the 6 gap fixes and the `writer_state` rule for kinds without a runnable writer.
- **P2:** fail closed or fail open when the map cannot be read.
- **P5:** a suffix retry, or a Sentinel sequence.
- **P6:** which files count as save states.
- **P7:**
  - the provenance code for rewritten stamps;
  - the key for the 12 + 2 bulk-copied reports;
  - whether the audit trail stays inside each artifact.

## Done when (2.5)

- the stronger validator reports 0 problems on the live map;
- the routing test passes;
- every live kind has a measured writer (or the agreed `writer_state` rule holds);
- T1's save-state check is closed by a read-back node carrying a frame-2 stamp;
- the R8 correction table is applied and verified by a second census (no frozen-clock or frame-1 stamps left in canonical artifacts, apart from the flagged `created_at` values);
- the map is live.
