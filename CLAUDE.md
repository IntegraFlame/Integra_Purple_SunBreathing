# Integra O/S: pointer file

This file only points. The content lives in the files below; read them rather than relying on this summary.

## Boot order (every new thread)
1. The newest save state in `The Hoard/`: `CCID_<unix>_SAVE_STATE_REPORT.md` and its `CCID_<unix>.json`. As of 2026-10-11 that is `CCID_1791704093`. Read both in full.
2. The plan files the save state names: `plan.file` in the JSON, then `plan.realignment_file` if present (it governs Step 1b and the Step 2 method). Find the current step and gate there. During Step 2, the reading ledger `integra-homebase/orchestration/UNIFY_READING_LEDGER.md` shows which folders are done.
3. The Claude memory index: `C:\Users\Javon Jenkins\.claude\projects\C--Users-Javon-Jenkins-OneDrive-Desktop-Integra-Purple-SunBreathing\memory\MEMORY.md`.
4. Live probes, then a stamp from `GET http://127.0.0.1:8000/clock`. Report what you read (receipts) and stop at the open gate.

## Pointers
| What | Where |
|---|---|
| Master Architecture Blueprint (v.9.9.1) | `integra-homebase/docs/MASTER_ARCHITECTURE_BLUEPRINT.md`; page https://claude.ai/artifact/CSEgvRaUnBzC5VdyRep98i |
| Rodin sub-agent / Gemini lifecycle research | `integra-homebase/docs/RODIN_SUBAGENT_MODEL_RESEARCH.md` |
| Tasks and dashboard | `productivity/TASKS.md`, `productivity/dashboard.html` |
| Kernel control (status/logs/start/stop/restart, SWDS guard) | `integra-homebase/scripts/kernel_ctl.ps1` |
| Genesis Kernel skill | `.agents/skills/genesis-kernel/SKILL.md` |
| Handoff package from thread f2e7cc92 | `The Hoard/thread_f2e7cc92_handoff/` |
| Session transcripts | `C:\Users\Javon Jenkins\.claude\projects\C--Users-Javon-Jenkins-OneDrive-Desktop-Integra-Purple-SunBreathing\` |

## Repo layout
- Root repo: branch `homebase-phase-e`.
- `integra-homebase/`: a separate repo on branch `phase-e-dragon-rodin-flight`, recorded in root as a gitlink. There is no `.gitmodules` entry.
- Both repos push to the same origin, `github.com/IntegraFlame/Integra_Purple_SunBreathing`, on different branches.
- With no `.gitmodules` entry, a clone of the root has nowhere to fetch `integra-homebase` from. Clone that branch separately.
- The kernel listens on `127.0.0.1:8000` and runs from `integra-homebase/.venv`. It is normally started by the scheduled task "Integra Genesis Kernel". On 2026-10-11 it ran outside that task's supervision (task Ready, 0xC000013A), so check the task is Running.
- The kernel serves `/dashboard` and `/clock/live` from `integra-homebase/static/`, not from the root repo's `static/`.

## Standing rules
- One step at a time. Read everything in full. Stop at each gate.
- Stamp only from a successful `GET /clock` (CDT | UTC | celestial). Never fabricate telemetry or stamps.
- Label provenance: MEASURED, DERIVED, CONSTANT or CLAIMED. Keep three things apart: "exists in code", "wired", and "ran".
- Never read `.env` values or the `github-recovery-codes` files. Never stage them, live logs, or the Docker `.vhdx` files.
- Never run the test suite in the live repo; tests write into live `kernel_memory`. Use an isolated copy.
- Never make paid model calls or restart the kernel without the Architect's approval.
- Autonomous trading stays out of scope.

## Gotchas
- `The Hoard/genesis_kernel.log` mixes UTF-16 and UTF-8. Read the bytes, strip NULs, and decode as UTF-8.
- `celestial_time()` restarts from a frozen checkpoint at every boot (ADR-001). SWDS times and artifact dates are skewed, so use file times on disk as the true times.
- Set `PYTHONIOENCODING=utf-8`; cp1252 crashes on Δ. With `python -I`, that variable is ignored (as is every `PYTHON*` variable), so use `-X utf8` instead.
- Shell writes into this OneDrive repo are inconsistent:
  - On 2026-10-09 the sandbox blocked them.
  - On 2026-10-11, Python and git wrote new files without trouble. But `cp` and `Copy-Item` could not overwrite files carrying OneDrive's cloud reparse tag (`0x9000601a`), even with the sandbox off.
  - Check `(Get-Item <file>).Attributes` for `ReparsePoint` before planning an overwrite.
- If the kernel stops answering, compare `GET /rodin/telemetry` (an `async def` endpoint) with `GET /clock` (a plain `def` endpoint). On 2026-10-11 the plain-`def` endpoints stalled while the async one and the SWDS scheduler kept running; the cause is unknown. Also check `Get-NetTCPConnection -RemotePort 8000` for a browser tab polling it: a dashboard tab was polling throughout (blueprint v.9.9.1, "Kernel note").
