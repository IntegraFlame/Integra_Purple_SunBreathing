# Boot brief: the Brain Map run (written 2026-10-15 23:40 CDT, session 8bbd7f50)

This starts a fresh thread that works through `docs/brainmap/TODO.md`, one task at a time. It is separate from folder 13 (the other iteration's work, paused until the weekly reset on 2026-10-19 06:00 CDT).

## The Architect's instruction (verbatim)
"create a To-Do based on the contents of this file --- Do not use agents --- Do each task one at a time generate a report after each successful task completion and pause for approval to continue"

## Read, in this order (in full; report receipts: path, bytes, lines)
1. `CLAUDE.md` (standing rules and gotchas; CFA is on, so see the gotcha about what can write).
2. The memory index `MEMORY.md` and the notes it lists, especially `verify-before-claiming`, `integra-kernel-gotchas`, `artifact-publish-path-workaround`, `rodin-first-changeset-oct15`, `architect-decisions-oct15-design`, `celestial-clock-design-ruling`.
3. `integra-homebase/docs/brainmap/TODO.md` (this run's task list, rules and gates).
4. `integra-homebase/core/IntegraBrainMap.md` (the Architect's map; the source of the To-Do).
5. `integra-homebase/docs/DESIGN_DECISIONS_10_15_26.md` (decisions D1–D10, the Phoenix Force design, the Sentinel design, the always-on set).
6. `integra-homebase/config/rodin_memory_map.yml` and `integra-homebase/memory/memory_map.py` (the store map; needed from T2 on).
7. The newest save state in `The Hoard/` (report and JSON) for the current state. Its folder-13 work belongs to the other iteration: do not resume it.

## Rules that matter most
- **No agents.** One task at a time; after each task a report, then **stop** and wait for "continue".
- **Isolated copy for all code work and tests.** Never run the test suite in the live repo (tests write into live `kernel_memory`). How the last isolated copy was made is in the memory note `rodin-first-changeset-oct15`.
- **CFA is on** (since 2026-10-13). Write repo files with the Write/Edit tools; copy with `cmd.exe /c xcopy`; run scripts with `C:\Python313\python.exe -X utf8`. Python 3.14, Git Bash and `pwsh` writes into the repo are blocked.
- **Ask first:** a kernel restart; a paid model call or embedding probe; any POST (`/dragon/flight`, `/swds/*`, `/models/router/phoenix-force`); Chroma changes; Task Scheduler registration; env or key changes; copying changes into the live repo; commit or push.
- **Stamps** only from a successful `GET /clock`. **Provenance labels** on every claim. **No credentials** read or quoted. **Autonomous trading is out of scope.**
- **Usage:** call `get_usage` before each task and in each report. Weekly usage was 73% at 2026-10-15 23:40. If a task would push weekly past about 90%, say so before starting it.

## First actions in the fresh thread
1. Stamp (`GET /clock`), then read-only probes (`/heimdall/health`, `/swds/status`, the task's state, CFA, usage).
2. Report the receipts and the T1 plan in a few lines.
3. Run **T1 steps 1.1 and 1.2** (read-only measurement and the gap list). Then ask the T1 rulings in one batch (D-20 epoch, the year constant, Sentinel scope), and continue only on the answers.

## Boot line to paste
> Integra Brain Map run. Follow `integra-homebase/docs/brainmap/BOOT_BRIEF.md`: read what it lists, in full, report receipts, then start T1 with the read-only steps. No agents. One task at a time, a report after each, and stop for my approval before the next.
