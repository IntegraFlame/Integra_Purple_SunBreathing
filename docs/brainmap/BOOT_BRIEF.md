# BRAIN MAP BOOT BRIEF (entry point for the fresh thread)

> Written by task T0 on 2026-10-16 in the cloud session on branch `claude/brain-map-todo-session-8-ekpfg6`. The date is the container date, **not a `/clock` stamp**: no kernel was reachable from the cloud container, so no stamp exists and none is invented.
> Companion file: `TODO.md`, 16,046 bytes, 122 lines, **sha16 `4c355acea00e9f0c`** (first 16 hex characters of its SHA-256). `TODO.md` is authoritative for scope and rules. This brief only says how to start.

## 1. What you are continuing
The Architect's Brain Map To-Do (session 8bbd7f50, 2026-10-15): the 13 numbered map items worked as Tasks T1–T10 (with 3.5, 5.5 and 6.5), **one at a time, in the Architect's order**. T0 (set-up) is done. It created `TODO.md` and this file and nothing else: no measurement, no code, no change to any existing file.

A task counts as done only when its `docs/brainmap/TaskNN_REPORT.md` exists. State when this brief was written:

| Task | Subject | State |
|:--|:--|:--|
| T0 | Set-up | done (this file and `TODO.md`) |
| T1 | Connect Celestial Time | **next** |
| T2 | Connect the Hoard | not started |
| T3 | Phoenix Engine and the Atlas design | not started |
| T3.5 | Coordinate system and Braille points | not started |
| T4 | Taxonomy labelling | not started |
| T5 | Connect System, Iteration 1: Knowledge | not started |
| T5.5 | SWDS and Siesta | not started |
| T6 | Cheshire Cat: SWDS deep learning, security, Phoenix Force | not started |
| T6.5 | Connect System, Iteration 2: Understanding | not started |
| T7 | Mathematical expression | not started |
| T8 | Rodin and hot storage; historical-data test | not started |
| T9 | Scheduled task: Flight and Land sessions | not started |
| T10 | Curriculum wisdom pass (gate 10.0 first) | not started |

## 2. Boot order (read each file in full, then give receipts)
1. **Boot per `CLAUDE.md`** (workspace root). Follow its boot sequence in full, starting with its first step (the latest save-state CCID). Do not shortcut it.
2. `integra-homebase/docs/brainmap/TODO.md`. Check its sha16 is `4c355acea00e9f0c`. If it differs, say so and ask before relying on it (it is edited only to record the Architect's rulings).
3. `integra-homebase/core/IntegraBrainMap.md`: the map (13 numbered items and the closing instruction for Task 10).
4. `integra-homebase/docs/DESIGN_DECISIONS_10_15_26.md`: the tasks cite D2, D5, D-20, A1, A4 and sections 4.1, 4.3, 5.1 and 5.3.
5. `integra-homebase/config/rodin_memory_map.yml` (PROPOSED 10/15).
6. The rules in section 4 below.

**Receipts:** for every file, its path, bytes, lines read and sha16. Then a `GET /clock` stamp. If `/clock` does not answer, there is no stamp: say so and do not invent one.

## 3. First action: T1 step 1.1 (read-only)
Measure Celestial Time **live and in code**, and treat every "Known" line in `TODO.md` T1 as a claim to re-measure, not a fact:
- who calls `generate_hoard_manifest`, `generate_4d_metadata_manifest` and `apply_zenkai_recalibration`;
- what `celestial_time()` returns and where its checkpoint comes from (ADR-001);
- `BASE_EPOCH` (value versus label) and how many year constants exist;
- the size and role of the Celestial Sentinel.

Live probes are `GET /clock` (and `/clock/full` if it answers) only. **`GET /celestial/checkpoint` writes the checkpoint, so do not call it in step 1.1.** No POST, no restart, no paid call, no sub-agents.

After 1.1, follow the T1 steps in order and ask the batched questions **once** (rulings needed: D-20 epoch; the year constant; Sentinel scope A4) before step 1.3. Stop at every gate listed under "Ask first".

## 4. Rules (copied from `TODO.md`; `TODO.md` governs)
- **One task at a time, no agents.** Each task: (1) read-only measurement, (2) the questions it needs, batched once at the start, (3) work in an **isolated copy**, never the live repo, (4) apply to the live repo only after approval, (5) verify, (6) report, (7) **stop and wait for "continue"**.
- **Ask first, inside any task:** a kernel restart; any paid model call or embedding probe; any POST (`/dragon/flight`, `/swds/*`, `/models/router/phoenix-force`); Chroma deletion or rebuild; Windows Task Scheduler registration; env or key changes; copying changes into the live repo; commit or push.
- **Never:** run the test suite in the live repo; read `.env` values; autonomous trading; invent a stamp.
- **Report** (saved as `docs/brainmap/TaskNN_REPORT.md`, summarised in chat): a `/clock` stamp; goal; what was measured (MEASURED / DERIVED / CONSTANT / CLAIMED; "exists in code / wired / ran" kept apart); what changed (files, sha16); test output verbatim; what is true now and what is not; decisions needed; the next task.
- **Known tension:** `docs/DESIGN_DECISIONS_10_15_26.md` says code moves after gate G3, but the Rodin-first change set was already applied on 10/15. Every task that changes code says so and asks.
- `productivity/TASKS.md` gets a one-line pointer only when the Architect says so.

## 5. Environment facts that affect the start (MEASURED in the cloud container, 2026-10-16)
- **Venue.** T0 ran in a Linux cloud container, not on the Architect's PC. `GET http://127.0.0.1:8000/clock` there returned no listener (HTTP 000). T1 step 1.1 needs the live kernel and the live repo, so **the fresh thread should run on the Architect's machine**, or the Architect must supply the data. This is the Architect's call.
- **The cloud clone is the homebase repo.** `The_Hoard/` holds the six 9/18 save-state files. It is at `origin/main` (204fac2), 30 commits behind `origin/phase-e-dragon-rodin-flight` (957a997, 10/15). The working branch is `claude/brain-map-todo-session-8-ekpfg6`, based on `main`.
- **Not on any remote branch.** I searched every path on `main`, `phase-e-dragon-rodin-flight`, `homebase-phase-e` and `workspace-root`. These are absent: the Brain Map, `DESIGN_DECISIONS_10_15_26.md`, `rodin_memory_map.yml`, `memory/memory_map.py`, and the Braille document and HTML. They exist only on the Architect's machine. `core/apophenic_engine.py` is on `phase-e-dragon-rodin-flight` only.
- **Root repo.** `CLAUDE.md` and `productivity/TASKS.md` are on `origin/homebase-phase-e`, where `integra-homebase` is a gitlink to 957a997.
- **Line numbers drift.** The `file:line` anchors in `TODO.md` (for example `runtime/antigravity_runner.py:56`) come from the live repo, which is ahead of the remote. Re-measure them.

## 6. How these two files land
T0 created exactly two new files under `docs/brainmap/`. The cloud session's setup required committing and pushing to its designated branch. That departs from T0's "nothing is committed or pushed", which was written for the local live repo. To use the files, copy `docs/brainmap/` into `integra-homebase/docs/brainmap/` on the Architect's machine (a new directory, so nothing is overwritten), or merge the branch. A commit in the live homebase remains an "Ask first" item.

## 7. Parked and separate
- The **Braille four-pass study** is parked until this To-Do is done (the Architect's choice, 10/15). Its inputs sit untracked in `integra-homebase/memory/` on the Architect's machine.
- The **folder-13 plans** belong to the other iteration and are unchanged.

## 8. Boot line (paste into the fresh thread)
```
Boot per CLAUDE.md. Then read integra-homebase/docs/brainmap/BOOT_BRIEF.md and TODO.md in full (TODO.md sha16 must be 4c355acea00e9f0c), then core/IntegraBrainMap.md, docs/DESIGN_DECISIONS_10_15_26.md and config/rodin_memory_map.yml. Give receipts (path, bytes, lines, sha16) and a /clock stamp. Then start Task 1, step 1.1: read-only measurement only, no agents, no POSTs, no restarts, no GET /celestial/checkpoint. One task at a time; after the report, stop and wait for "continue".
```
