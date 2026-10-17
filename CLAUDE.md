# Integra O/S: pointer file

This file only points. The content lives in the files below; read them rather than relying on this summary.

## Boot order (every new thread)
1. The newest save state in `The Hoard/`: `CCID_<unix>_SAVE_STATE_REPORT.md` and its `CCID_<unix>.json`. As of 2026-10-16 18:45 CDT that is `CCID_1792194308`. Read both in full. It comes with a step-by-step checklist, `The Hoard/CCID_1792194308_BOOT_SEQUENCE.md`; follow it. **Current directive:** the Architect's 10-step to-do in `integra-homebase/core/IntegraBrainMap.md` (the neural mapping / Atlas, with `integra-homebase/memory/Braille-BasedSemanticLabelingSystem.md` as its core codex), run from the single To-Do `integra-homebase/docs/brainmap/TODO.md`. T1 (Celestial Time) is closed: the Celestial Sentinel and frame 2 are live and committed in the nested repo (`95a7aab`, `c7053f1`; pushed 2026-10-17). T2 (Connect the Hoard) is at step 2.5: rulings R1–R8 decided, the plan is `docs/brainmap/T2_5_PLAN.md`, P3 is committed and pushed (nested `e519534`), and P1 is built and tested in isolation (`%USERPROFILE%\t2p1\package`). Resume at the `metatron_db` ruling, then the apply go. Folder 13 cycles are paused until 2026-10-19 06:00 CDT.
2. The plan files the save state names (for folder 13, those of the previous save state `CCID_1792052895`): `plan.file` in the JSON, then `plan.realignment_file` if present. Its section "Plan (2026-10-13 midday): folder 13" governs folder 13. Find the current step and gate there. During Step 2, the reading ledger `integra-homebase/orchestration/UNIFY_READING_LEDGER.md` shows which folders are done. For folder 13, the local, git-ignored `The Hoard/antigravity_conversations/_summaries/RESUME_HERE.md` gives the exact resume point. As of 2026-10-15 that is plan Step 4, reading cycle 24 of 45 (cycles 1-23 done; paused until the weekly reset).
3. The Claude memory index: `C:\Users\Javon Jenkins\.claude\projects\C--Users-Javon-Jenkins-OneDrive-Desktop-Integra-Purple-SunBreathing\memory\MEMORY.md`.
4. Live probes, then a stamp from `GET http://127.0.0.1:8000/clock`. Report what you read (receipts) and stop at the open gate.

## Pointers
| What | Where |
|---|---|
| Master Architecture Blueprint (v.9.9.1) | `integra-homebase/docs/MASTER_ARCHITECTURE_BLUEPRINT.md` (the only canonical); page https://claude.ai/artifact/CSEgvRaUnBzC5VdyRep98i |
| Blueprint index: every blueprint-like file, its role and hash, and the update procedure | `integra-homebase/docs/BLUEPRINTS_INDEX.md`. After each republish, re-copy the canonical over the two `v.9.9.1Integra Master Architecture Blueprint.md` exports. |
| Rodin sub-agent / Gemini lifecycle research | `integra-homebase/docs/RODIN_SUBAGENT_MODEL_RESEARCH.md` |
| Tasks and dashboard | `productivity/TASKS.md`, `productivity/dashboard.html` |
| Integra DS 2 (the design system; the Heimdall dashboard uses it since nested `287cf25`) | https://claude.ai/artifact/FvYZfmNY6HsfNNaFKivsJR; source build archived at `%USERPROFILE%\integra_thread_archive\2026-10-17\integra-homebase-review-f65bf3\_integra_ds2_build\` |
| Work archived from the fork worktrees on 2026-10-17 (DS 2 build, IBKR study, Voltron register, T10 working files) | `%USERPROFILE%\integra_thread_archive\2026-10-17\` (`MANIFEST.tsv`: 280 files, sha256) |
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
- The kernel's clock is live since 2026-10-16 (ADR-001). `celestial_time()` returns the OS clock (ADR-001 Option A, run from the 00:07 kernel start), and the Celestial Sentinel stamps frame 2 (from the 09:14 start). Both are committed in the nested repo as `95a7aab` (pushed 2026-10-17). `/clock` reports `"frame": 2`, and `GET /celestial/checkpoint` is read-only.
  - SWDS sleeps inside the real 02:00–07:00 window once the kernel has been idle for 1 h or more, and wakes at 07:00 (DERIVED from `main.py`'s SWDS scheduler; it slept at 02:00:59 on 10/16).
  - Stamps and report names from before 2026-10-16 are frame 1, taken from a checkpoint frozen at 2026-10-06 20:59:42, and their dates run up to 7 days behind. Use file times on disk for those, and never compare frame-1 with frame-2 stamps. Their correction note (ADR-001 item 4) is not written yet.
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
- Every launch leaves the kernel outside its task, sooner or later. Seen 7 times out of 7:
  - the 10/11 logon launch;
  - the 10/12 logon launch;
  - the 10/12 13:06:57 `kernel_ctl.ps1 restart` (task Running at 13:16, Ready / 0xC000013A by 14:52);
  - the 10/13 20:57:49 logon launch: the wrapper ended **2026-10-14 18:05:41** (Task Scheduler events 201 and 102; MEASURED 2026-10-15 03:18). The kernel kept answering, unsupervised.
  - the 10/15 19:37:24 `kernel_ctl.ps1 restart`: the wrapper ended 23:49:53, 37 s before the Start-menu restart at 23:50:30.
  - the 10/16 00:06:01 logon launch: the wrapper ended 03:13:27.
  - the 10/16 09:13:45 logon launch: the wrapper ended 09:26:47. At 10:56 the task read Ready (0xC000013A) while the kernel answered.
  - Not counted: a logon launch at 23:51:31 on 10/15, after a quick reboot (up 23:51:10); the power-off at 23:52:43 ended it 73 s later. The 10/15–10/16 times are MEASURED 2026-10-16 10:56 from the Task Scheduler and System logs.
  - Both 10/16 wrapper exits came 3–14 s after a read-only PowerShell probe by a Claude session. That is a coincidence to test, not an established cause.
  - Each time the wrapper PowerShell exits 0xC000013A and `cmd.exe` and uvicorn are orphaned, so restart-on-failure never covers the kernel.
  - **Leading cause (DERIVED):** Windows Terminal is the default console host, and closing its window or tab kills the wrapper.
  - **Also:** the task runs at priority 7 (below-normal CPU, low I/O and memory priority).
  - **Task Scheduler history has been on since 2026-10-13** (the Architect), so a wrapper exit now leaves a timestamped event. The 20:57:49 logon launch that day is the first recorded one:
    - events 119, 129, 100 and 200;
    - the wrapper on a classic `conhost`, and a Windows Terminal `-Embedding` instance 51 s later;
    - startup took about 9 min;
    - still supervised at 21:54; lost on 10/14 at 18:05:41 (above).
  - See `integra-homebase/docs/KERNEL_AUTOLAUNCH_REVIEW.md`.
- If the kernel stops answering, compare `GET /rodin/telemetry` (an `async def` endpoint) with `GET /clock` (a plain `def` endpoint). On 2026-10-11 the plain-`def` endpoints stalled while the async one and the SWDS scheduler kept running; the cause is unknown. Also check for a browser tab polling it. The kernel log's request lines show pollers more reliably than `netstat` does. Chrome restores the `/dashboard` tab after a reboot. A dashboard tab was polling throughout (blueprint v.9.9.1, "Kernel note").
- Desktop-app session worktrees (`.claude/worktrees/*`) are checkouts of the root repo's `main` (`204fac2`), which predates the `integra-homebase` split. Their top-level `static/`, `core/` and so on are stale copies; on 2026-10-17 their `static/dashboard.html` was 676 insertions behind the live file. For homebase work, add a nested worktree of `integra-homebase` that checks out only the paths you need (Claude memory note `nested-worktree-and-stub-ui-checks`).
- Never open `integra-homebase/static/dashboard.html` from `file://`. With no host, it falls back to `http://localhost:8000` and polls the live kernel at 1 Hz. Check pages against a local GET-only stub instead (same memory note).
