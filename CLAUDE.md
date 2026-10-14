# Integra O/S: pointer file

This file only points. The content lives in the files below; read them rather than relying on this summary.

## Boot order (every new thread)
1. The newest save state in `The Hoard/`: `CCID_<unix>_SAVE_STATE_REPORT.md` and its `CCID_<unix>.json`. As of 2026-10-13 that is `CCID_1791929018`. Read both in full. It comes with a step-by-step checklist, `The Hoard/CCID_1791929018_BOOT_SEQUENCE.md`; follow it.
2. The plan files the save state names: `plan.file` in the JSON, then `plan.realignment_file` if present. Its section "Plan (2026-10-13 midday): folder 13" governs folder 13. Find the current step and gate there. During Step 2, the reading ledger `integra-homebase/orchestration/UNIFY_READING_LEDGER.md` shows which folders are done. For folder 13, the local, git-ignored `The Hoard/antigravity_conversations/_summaries/RESUME_HERE.md` gives the exact resume point.
3. The Claude memory index: `C:\Users\Javon Jenkins\.claude\projects\C--Users-Javon-Jenkins-OneDrive-Desktop-Integra-Purple-SunBreathing\memory\MEMORY.md`.
4. Live probes, then a stamp from `GET http://127.0.0.1:8000/clock`. Report what you read (receipts) and stop at the open gate.

## Pointers
| What | Where |
|---|---|
| Master Architecture Blueprint (v.9.9.1) | `integra-homebase/docs/MASTER_ARCHITECTURE_BLUEPRINT.md` (the only canonical); page https://claude.ai/artifact/CSEgvRaUnBzC5VdyRep98i |
| Blueprint index: every blueprint-like file, its role and hash, and the update procedure | `integra-homebase/docs/BLUEPRINTS_INDEX.md`. After each republish, re-copy the canonical over the two `v.9.9.1Integra Master Architecture Blueprint.md` exports. |
| Rodin sub-agent / Gemini lifecycle research | `integra-homebase/docs/RODIN_SUBAGENT_MODEL_RESEARCH.md` |
| Tasks and dashboard | `productivity/TASKS.md`, `productivity/dashboard.html` |
| Kernel control (status/logs/start/stop/restart, SWDS guard) | `integra-homebase/scripts/kernel_ctl.ps1` |
| Genesis Kernel skill | `.agents/skills/genesis-kernel/SKILL.md` |
| Handoff package from thread f2e7cc92 | `The Hoard/thread_f2e7cc92_handoff/` |
| Folder 13 (local Antigravity archive): method, tools, validation gate | `The Hoard/antigravity_conversations/_summaries/` (git-ignored; start at `RESUME_HERE.md`; gate in `gate/GATE_NOTES.md`). Archive content never goes into the public repo. |
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
- `celestial_time()` restarts from a frozen checkpoint (2026-10-06 20:59:42) at every boot (ADR-001). SWDS times and artifact dates are skewed, so use file times on disk as the true times.
  - SWDS fires about 5 h 00 m after each kernel start.
  - After the 2026-10-13 20:57 reboot the kernel started at 20:59, in step with the checkpoint's time of day. So SWDS falls at about 02:00 CDT and wakes about 07:00 (DERIVED). File dates still run 7 days behind.
- Set `PYTHONIOENCODING=utf-8`; cp1252 crashes on Δ. With `python -I`, that variable is ignored (as is every `PYTHON*` variable), so use `-X utf8` instead.
- Failed writes into this repo come from Windows Defender **Controlled Folder Access** (CFA), which blocks per program. This is MEASURED from the Defender Operational log, 10/08-10/12: event 1123 = blocked write, 5007 = setting changed.
  - The earlier diagnoses "the sandbox blocked writes" (10/09) and "OneDrive cloud placeholders deny overwrites" (10/11) were both CFA.
  - Symptoms: `ENOENT` on the Edit/Write tools' temp file or `mkdir`; Python `Errno 9` or `FileNotFoundError`; `cp`/`Copy-Item` denied. Reads still work.
  - Diagnose with `(Get-MpPreference).EnableControlledFolderAccess` and the 1123 events. Never change the setting yourself; ask the Architect.
  - The Architect turned CFA off on 2026-10-12 at 12:54, then **back ON on 2026-10-13 at 20:09:53**, with an allow rule for `...\AppData\Roaming\Claude\claude-code\*\*\claude.exe` (Defender 5007, 20:09:33).
  - **With CFA on:**
    - These can write: the Write/Edit tools, `git`, `cmd.exe` and `C:\Python313\python.exe` (verified 20:11 by a live write).
    - These are blocked: `python` on PATH (3.14), Git Bash (`cp`, `mkdir`, `cat >>`) and `pwsh`.
    - So run scripts with `C:\Python313\python.exe -X utf8` and write files with the Write/Edit tools.
- `python` on PATH is `C:\Python314` (3.14). The kernel runs 3.13 from `integra-homebase\.venv`.
- The TCP tables are unreliable here. Judge liveness by an HTTP probe; `netstat -ano` can still give the owning PID.
  - On 10/12 `Get-NetTCPConnection` showed only "Closed" while the kernel was LISTENING.
  - After the 2026-10-13 reboot, both it and `netstat` showed the listener 127.0.0.1:8000 as FIN_WAIT_1 while HTTP answered. `netstat` sometimes dropped the row entirely.
- Every launch leaves the kernel outside its task, sooner or later. Seen 3 times out of 3:
  - the 10/11 logon launch;
  - the 10/12 logon launch;
  - the 10/12 13:06:57 `kernel_ctl.ps1 restart` (task Running at 13:16, Ready / 0xC000013A by 14:52).
  - Each time the wrapper PowerShell exits 0xC000013A and `cmd.exe` and uvicorn are orphaned, so restart-on-failure never covers the kernel.
  - **Leading cause (DERIVED):** Windows Terminal is the default console host, and closing its window or tab kills the wrapper.
  - **Also:** the task runs at priority 7 (below-normal CPU, low I/O and memory priority).
  - **Task Scheduler history has been on since 2026-10-13** (the Architect), so a wrapper exit now leaves a timestamped event. The 20:57:49 logon launch that day is the first recorded one:
    - events 119, 129, 100 and 200;
    - the wrapper on a classic `conhost`, and a Windows Terminal `-Embedding` instance 51 s later;
    - startup took about 9 min;
    - still supervised at 21:54.
  - See `integra-homebase/docs/KERNEL_AUTOLAUNCH_REVIEW.md`.
- If the kernel stops answering, compare `GET /rodin/telemetry` (an `async def` endpoint) with `GET /clock` (a plain `def` endpoint). On 2026-10-11 the plain-`def` endpoints stalled while the async one and the SWDS scheduler kept running; the cause is unknown. Also check for a browser tab polling it. The kernel log's request lines show pollers more reliably than `netstat` does. Chrome restores the `/dashboard` tab after a reboot. A dashboard tab was polling throughout (blueprint v.9.9.1, "Kernel note").
