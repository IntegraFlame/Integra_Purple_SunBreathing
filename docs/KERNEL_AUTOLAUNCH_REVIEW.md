# Kernel auto-launch review: what delays or degrades the Genesis Kernel's start

**Stamp:** 2026-10-12 15:33:49 CDT | 2026-10-12T20:33:49Z | rot 97.2898°, lunar 0.6591, orbit 0.2176, ROT_90_ORB_20 (`GET /clock`, HTTP 200, kernel uptime 02 h 26 m 41 s).
**Author:** Claude (Opus 5.5), session c88f5000, for the Architect. This is plan section F of 2026-10-12, the Architect's request: "For Kernel determine any additional possible errors that would delay or degrade Kernel auto-launch code processes".

**Method.** Read-only, following the planning agent's six-stage plan (task trigger and wrapper; `start_kernel.ps1`; import chain and constructors; lifespan and loops; external factors; observability).
- **Not done:**
  - no restart and no task start/stop;
  - no POST, and no `GET /celestial/checkpoint`;
  - no project-module import, no tests, no paid calls;
  - no `.env` value read.
- **Live probes:** `GET /clock` (15:10, 15:29 ×2, 15:33, 15:40 ×3) and one `GET /rodin/telemetry` (15:40).
- **Everything else:** event logs, process and file metadata, the task's exported XML, source reads, and the kernel log decoded in memory.

**Labels.**
- **MEASURED** = observed directly.
- **DERIVED** = computed from measured facts.
- **CLAIMED** = from a document or a person, not checked.
- Status is Confirmed / Supported / Hypothesis / Refuted.
- "Exists in code", "wired" and "ran" are kept apart.

## Summary

The kernel itself starts reliably: 9 startups, 9 binds, 0 bind errors, 0 lost background tasks in 47,596 log lines. What goes wrong is everything around it:

1. **No launch stays supervised (3 of 3 checked; none of the 10 wrappers since 10/08 logged a stop event).** The task's PowerShell wrapper runs in a console that Windows Terminal hosts. Windows Terminal is the default terminal here, and Microsoft's own tracker says `-WindowStyle Hidden` is not respected in that case. The window can be closed, which kills only the wrapper. The kernel keeps running, but the task reads Ready, so restart-on-failure never covers it.
2. **Startup time is unpredictable: 26 s to about 13 min.**
   - Two post-reboot logon launches took about 9 and 13 minutes from wrapper start to lifespan; the others took 26-98 s.
   - The task runs at the default priority 7, which is below-normal CPU, low I/O and low memory priority.
   - No timestamps exist to say where the time goes.
3. **Several silent-failure paths can degrade a start without a trace:**
   - non-atomic state writes plus forced kills;
   - swallowed exceptions;
   - unreferenced background tasks;
   - a single 3-second probe as the only duplicate-launch guard, while uvicorn runs the whole startup before it binds.
4. **External conditions decide whether the kernel can write at all** (Controlled Folder Access), and when SWDS fires (the frozen clock).

**Verdict: Request changes (Step 4).** Nothing here needs an emergency fix. F1 and F2 mean the "auto-restart" promise in `start_kernel.ps1:13-14` is not true today. F3 and F20 explain most of the slow and stalled starts.

## Critical issues

| # | Stage | Finding | Evidence | Status |
|:--|:--|:--|:--|:--|
| F1 | 1 | **The wrapper dies with 0xC000013A and leaves the kernel unsupervised.** The wrapper `powershell.exe -WindowStyle Hidden -File start_kernel.ps1` is attached to a console that the default terminal (Windows Terminal) hosts. Closing that window or tab sends CTRL_CLOSE_EVENT. The default handler calls `ExitProcess`, which gives exit 0xC000013A (STATUS_CONTROL_C_EXIT). `cmd.exe` and uvicorn sit in their own hidden classic `conhost` and keep running, orphaned. | **MEASURED:** (1) Task Ready, LastTaskResult 3221225786 = 0xC000013A, LastRunTime 13:06:57, while the kernel answers. (2) Windows PowerShell log: **all 10 wrapper hosts since 10/08 have event 400 (engine start) and none has 403 (engine stop)**. Control: 67 of 95 PowerShell hosts in the same period did log 403, so the detector works. Some of the 10 wrappers ended with a reboot, which also leaves no 403. The decisive ones are 12:00:21 and 13:06:59 on 10/12: both died while the machine kept running. (3) `HKCU\Console\%%Startup` = `{2EACA947…}` / `{E12CFF52…}`, which Microsoft documents as the "Windows Terminal" values. (4) `WindowsTerminal.exe -Embedding` PID 11684 started 12:00:10, 11 s before the 12:00:21 wrapper engine start; it is still alive and now has no child processes. (5) The kernel's `cmd.exe` 24312 has its own classic `conhost.exe` 21948 (`0x4`), and its parent wrapper 20312 is gone. (6) No application crash (1000/1001/1002) for the terminal, conhost, PowerShell or python, and no sleep/resume events. **Tier 1:** microsoft/terminal#12464 (open, Backlog): with Windows Terminal as default, `-WindowStyle Hidden` "is not respected"; the window "is visible and remains visible", and there is "no repro" with Windows Console Host. The default handler calls ExitProcess on CTRL_CLOSE_EVENT ([HandlerRoutine](https://learn.microsoft.com/windows/console/handlerroutine)). | **Supported** (DERIVED; one question for the Architect would confirm it, see Actions) |
| F2 | 1 | **Restart-on-failure does not cover this exit.** `start_kernel.ps1:13-14` says the script "exits with uvicorn's exit code, so Task Scheduler's restart-on-failure policy works". But the wrapper is killed before line 72, and no restart followed the 13:06 wrapper's death. | **MEASURED:** RestartOnFailure PT1M × 5 is in the task XML, yet LastRunTime stayed at 13:06:57 after the wrapper died (gone by 14:52). Microsoft documents RestartOnFailure only as "if the task fails for any reason" ([RestartOnFailure](https://learn.microsoft.com/windows/win32/taskschd/taskschedulerschema-restartonfailure-settingstype-element)); it does not define which exits count. Task history is disabled (F9), so the scheduler's own view is not recorded. | **Supported** (1 observed instance) |
| F3 | 3 | **The task runs at priority 7.** The task XML sets no `<Priority>`; the default is 7. | **MEASURED:** python 21360 / 38084 are BelowNormal, base priority 6. **Tier 1:** priority 7 = `BELOW_NORMAL_PRIORITY_CLASS`, `IoPriorityLow`, `MEMORY_PRIORITY_LOW`; "Priority levels 7 and 8 are used for background tasks, and priority levels 4, 5, and 6 are used for interactive tasks" ([Priority element](https://learn.microsoft.com/windows/win32/taskschd/taskschedulerschema-priority-settingstype-element)). **Consequences (DERIVED):** under load, imports and the 102 MB Chroma open get CPU and I/O last. The working set is trimmed: 10.6 MB resident of 218.6 MB private at 15:29. **Today's measured cost of the trimming was small:** after about 19 min idle, the first `/clock` took 198 ms with 28 page faults, and the second took 19 ms. The 10 s first-probe stalls of 10/11 23:31 and 10/12 13:09 happened under a polling dashboard and/or startup load. **Recurrence at 15:40 under load (MEASURED, no poller connected):**
- The first `/clock` got no answer within 15 s. Then `/clock` took 5.3 s and the *async* `/rodin/telemetry` 3.5 s, so the whole process was slow, not just the sync path. The next `/clock` took 76 ms.
- The kernel's page faults rose by 1,020 since 15:29 (working set 10.6 → 14.3 MB), and system CPU was at 46%.
- `OneDrive.exe` (Normal priority) had used 13,843 CPU-seconds since logon, about one core on average. It was syncing this session's new files, including about 163 MB of local Antigravity copies.

So a below-normal kernel stalls when a normal-priority process is busy (DERIVED). | **Confirmed** (setting); contribution to stalls **Supported** (load-dependent: 0.2 s idle-only at 15:29, 15 s+ under OneDrive load at 15:40) |
| F20 | 3, 5 | **New: startup time ranges from 26 s to about 13 min.** The table below pairs each wrapper engine start (event 400, MEASURED) with the next lifespan time (DERIVED: the log's "Celestial reboot delta" plus checkpoint epoch 1791338382.557). | **MEASURED / DERIVED.** Post-reboot logon launches: **10/09 05:27:43 → 05:36:44 (≈9 min)**; **10/11 16:30:01 → 16:42:58 (≈13 min)**; 10/11 19:18:38 → 19:20:05 (87 s); 10/12 12:00:21 → 12:00:47 (26 s). The `kernel_ctl` restart 10/12 13:06:59 → 13:08:37 took 98 s; its process timeline (worker 13:07:03, `chroma.sqlite3` written 13:08:33, listener 13:08:37) puts ≈90 s in imports and constructors. In the 10/11 16:28-16:44 window, Defender logged 2 × event 2000 and 5 × event 2010 (signature update and dynamic signatures), and Hyper-V/WSL and Docker were starting. **Where the minutes went is unknown:** before python started, or inside the imports. No timestamps exist (F9). | **Confirmed** (variance); cause **Hypothesis**: priority 7 under logon load (Docker/WSL, OneDrive, Defender), and Defender on-access scanning of 36k venv files after a signature update |
| F4 | 2 | **A duplicate launch runs the full startup before it fails to bind.** `start_kernel.ps1:52-58` is the only single-instance guard: one `GET /clock` with a 3 s timeout and an empty `catch`. First probes have taken 5-12 s (F3), so a slow kernel reads as "not running". uvicorn 0.52.4 runs `await self.lifespan.startup()` (`uvicorn/server.py:106-107`) before `loop.create_server(...)` (`:173-180`). So a second process would run SWDS reconciliation (`main.py:82-99`, which can write a report and `swds_state.json`), Metatron `executescript`, and a second Chroma client on the live database, and only then fail. | **MEASURED** (code read; installed uvicorn version and lines); log: 9 startups, 9 binds, **0** bind errors, so **0 incidents so far**. Paths that bypass `kernel_ctl`'s process guard (`kernel_ctl.ps1:128-131`): a manual or agent `Start-ScheduledTask` while the task reads Ready (which is always, per F1), or a restart-on-failure that does fire. | **Supported** (latent) |
| F5 | 5 | **Controlled Folder Access decides whether the kernel can write at all.** The task launches `cmd.exe`, which opens the log for `>>` (`start_kernel.ps1:69`), and the base interpreter `C:\Python313\python.exe` (the venv launcher re-executes it). Both must be on Defender's allowed list. | **MEASURED** (Defender 1123): `cmd.exe` blocked on `The Hoard\` at **10/08 21:45:33** and **10/09 01:00:30**, 18 s and 15 s after the wrapper starts of 21:45:15 and 01:00:15. `C:\Python313\python.exe` blocked on `kernel_memory\drop_in` at 21:51:22 and 01:00:49. The 01:00:49 block is the `makedirs` in TheHoard's constructor (`memory/the_hoard.py:154-160, 191-195`), so the kernel process ran (DERIVED). **No lifespan line was logged for either launch**; its output had nowhere to go. Both programs were allowed at 10/09 01:30; no block since. CFA has been off since 10/12 12:54:34. | **Confirmed** (historical); conditional on how CFA is re-enabled |
| F7 | 4, 5 | **The frozen clock moves SWDS to boot + 5 h 00 m 18 s.** `celestial_time()` = checkpoint epoch (10/06 20:59:42, file last written then) + seconds since boot (`core/celestial_middleware.py:324-328`). The scheduler (`main.py:1134, 1148`) and reconciliation (`main.py:84`) read it. So every restart moves the next SWDS. During a false SWDS, `kernel_ctl stop/restart` refuses without `-Force` (`kernel_ctl.ps1:98-105`), and the router drops components to P2/P3 for 5 hours in daytime. | **Confirmed** (predicted and observed three times; ADR-001). Next, from the 13:07 boot: about 18:07-18:09 CDT, waking about 23:07-23:09 (DERIVED). | **Confirmed** |

## Suggestions

| # | Stage | Finding | Evidence | Status |
|:--|:--|:--|:--|:--|
| F6 | 5 | **All kernel files are OneDrive cloud placeholders, hydrated and unpinned.** If Storage Sense or "Free up space" dehydrates them, a launch would first download up to ~1 GB. | **MEASURED** (PowerShell attributes, 15:31): `.venv` 35,679, `local_dbs` 9, `config` 11, `kernel_memory` 314, and code folders 131: **all** have the cloud reparse bit, **0 dehydrated, 0 pinned, 0 unpinned**. *Instrument note:* Python reports these files as plain (0x20). The cloud files API "always hides its reparse points from all applications except for sync engines and processes whose main image resides under %systemroot%" ([Microsoft Learn](https://learn.microsoft.com/windows/win32/cfapi/build-a-cloud-file-sync-engine#compatibility-with-applications-that-use-reparse-points)). Use `powershell.exe` from System32 for this check. | **Confirmed** (state); risk latent |
| F8 | 2 | **`kernel_ctl start` gives up after "120 s" and miscounts.** `START_WAIT_S = 120` (`kernel_ctl.ps1:43`). The loop adds 2 per iteration but each iteration costs 2 s of sleep plus up to 5 s of probe (`:144-148`), so "answering after ~50s" understates. Measured starts reach 98 s off-logon and ≈13 min after a reboot (F20). | **MEASURED** (code); DERIVED (comparison) | **Supported** |
| F9 | 6 | **The kernel's start cannot be timed or audited:** no timestamps, lost import-time logs, no launch record, buffered output, and no task history. | **No timestamps:** `logging.basicConfig(level=INFO)` with the default format (`main.py:47`), and uvicorn's formats are `%(levelprefix)s %(message)s` (`uvicorn/config.py:88, 93`). **Import-time logs are lost:** logging is configured after 40 import lines (`main.py:7-45`), so `env_loader` and `ModelRouter: Registered` INFO lines never appear (log: 0 and 0). **No launch record:** `start_kernel.ps1` writes only `Write-Host` to its own console (log: 0 `[INTEGRA] Timestamp`). **Buffered output:** `PYTHONUNBUFFERED` is not set (`start_kernel.ps1:62-63`), and stdout redirected to a file is block-buffered ([sys.stdout](https://docs.python.org/3/library/sys.html#sys.stdout)). `print()` is used in `memory/the_hoard.py:228` and elsewhere. Every kernel lifetime ended in a forced kill (log: 0 "Shutting down", 0 "Finished server process"), so a buffered tail is lost. **Task Scheduler history is disabled** (`wevtutil gl Microsoft-Windows-TaskScheduler/Operational` → `enabled: false`). | **Confirmed** |
| F10 | 4 | **State writes are not atomic, and their errors are swallowed.** `_save_state` truncates and rewrites `runtime/swds_state.json` (`runtime/swds_simulator.py:74-75`) inside `except Exception: pass` (`:76-77`). `_load_state` swallows a parse error and silently starts from defaults (`:56-57`). With forced kills and 2 unexpected shutdowns since 10/11 (System 6008 at 10/11 17:48:41 and 10/12 10:09:44), a kill mid-write would silently reset the SWDS state. | **MEASURED:** the file parses now (2,165 bytes, state AWAKE, written 10/12 05:20:05). The failure has not been seen. | **Supported** (latent) |
| F11 | 4 | **Background tasks are not referenced, and the scheduler body is unguarded.** `asyncio.create_task(...)` results are discarded at `main.py:103, 134, 150`. Python: "Save a reference to the result of this function, to avoid a task disappearing mid-execution. The event loop only keeps weak references to tasks" ([asyncio.create_task](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task)). The scheduler loop body (`main.py:1131-1191`) guards only the Phoenix call (`:1183-1191`). An exception in `swds_engine.awaken()`, `enter_deep_sleep()` or `MODEL_ROUTER` would end SWDS scheduling silently for the rest of the process. The Cheshire and Kintsugi loops do catch per tick (`sensory/cheshire_cat.py:603-604`, `evolution/kintsugi_sandbox.py:402-406`). | **MEASURED** (code); log: 0 "Task exception was never retrieved" | **Supported** (latent) |
| F12 | 4 | **One shared SQLite connection serves the event loop and the threadpool.** `metatron_deploy.get_connection()` is a module singleton with `check_same_thread=False` and WAL (`memory/database/metatron_deploy.py:37-53`), with no lock. The Kintsugi loop runs synchronous queries on the event loop every 5 s (`kintsugi_sandbox.py:366, 396`). Sync handlers (`/heimdall/health`, `/metatron/status`) use the same connection from worker threads. Python: with `check_same_thread=False`, "write operations may need to be serialized by the user"; the default busy `timeout` is 5.0 s ([sqlite3.connect](https://docs.python.org/3/library/sqlite3.html#sqlite3.connect)). This is the leading lead for the sync-path stalls; it is not shown. | **MEASURED** (code); log: 0 "database is locked" | **Supported** (lead) |
| F13 | 5 | **The dashboard has no in-flight guard.** A restored Chrome tab polls 7 endpoints at 1 Hz (`static/dashboard.html:1114, 1407-1416`) with a 3 s abort, which starts the next round whether or not the last one finished. This was the precondition of the 10/11 stall and of the 10/12 13:09 first-probe stall. | **MEASURED** (earlier sessions); **none polling at 15:29** (0 connections to :8000 besides the listener) | **Confirmed** |
| F14 | 3 | **Import-time `makedirs` on paths outside the repo.** `core/sdk_harness.py:248` constructs `AntigravityFaultTolerantHook()` at import, which runs `os.makedirs(r"C:\Users\Javon Jenkins\.gemini\antigravity\scratch\Integra_Project")` (`:149, 168`). A failure there would abort the kernel's import. | **MEASURED:** the directory exists; `exist_ok=True` swallows the existing-directory case | **Hypothesis**, low likelihood |
| F15 | 3 | **Key loading is silent.** `config/env_loader.py:193` reads up to 11 key files at import (`:70-82`); all 11 exist (checked by name and attribute only). Read errors are logged only as warnings (`:128-129`), before logging is configured. A missing key leaves a client unbuilt for the whole process. | **MEASURED** (code, file existence); log: 0 `env_loader` lines. Out of scope, noted only: the loader also puts `Git_personal_access.env` into the kernel's environment, which no kernel feature needs (security review, Step 4). | **Supported**, 0 incidents |
| F16 | 3 | **`models.yml` is opened without an encoding** (`core/model_router.py:142`). Only `yaml.YAMLError` is caught (`:150, 157`), so a `UnicodeDecodeError` would abort `MODEL_ROUTER = ModelRouter()` (`:568`) and the kernel's import. This only matters on a launch path without `PYTHONUTF8=1` (`start_kernel.ps1:63` sets it). | **MEASURED:** `models.yml` is 982 bytes of pure ASCII today, so it decodes under cp1252 as well | **Supported**, latent only |
| F17 | 4 | **The 30 Hz Cheshire loop** (`sensory/cheshire_cat.py:546-606`) wakes about 2.6 million times a day with nothing to do. | Planning agent: 38 s of CPU in 94 min (CLAIMED, not re-measured) | Minor |
| F21 | 4 | **New: `MODEL_ROUTER.activate()` runs unconditionally at startup** (`main.py:140`), after reconciliation. Today reconciliation always wakes SWDS at boot (the frozen clock's hour is about 21 at boot, `main.py:84-87`), so the two never conflict. Once the clock is fixed (ADR-001), a restart during a real SWDS would set the router to P1 while the engine still reads SLOW_WAVE_DEEP_SLEEP. | **MEASURED** (code); log: 0 "RECONCILIATION" lines | **Hypothesis** (after ADR-001) |

## Refuted

| # | Claim | Why it is refuted |
|:--|:--|:--|
| F18 | A network call hangs the import | **Verified in installed source:** chromadb `ProductTelemetryClient.capture` is `pass` (`chromadb/telemetry/product/posthog.py:10-11`). google-genai calls `load_auth()` / `google.auth.default()` only when there is no API key (`google/genai/_api_client.py:788-794`). Not a cause. |
| F19 | Python 3.14 on PATH breaks the launch | The task uses the venv interpreter by full path (`start_kernel.ps1:31`); `pyvenv.cfg` home is `C:\Python313`. Python 3.14 matters only for agents running `python` from PATH, and for CFA (blocked 5 times). |

## What looks good

- **The kernel binds correctly and only once:** 9 startups, 9 "Uvicorn running on", 0 bind errors in 47,596 log lines. It binds `127.0.0.1`, not `0.0.0.0` (`start_kernel.ps1:37`).
- **No background task has failed:** 0 "Task exception was never retrieved", 0 "database is locked", 0 Metatron FAILED, 0 Kintsugi or Cheshire tick errors. The only tracebacks (23) are `ConnectionResetError [WinError 10054]`, which are aborted dashboard requests.
- **`kernel_ctl.ps1` is careful:**
  - It refuses to start a second kernel when processes exist (`:128-131`).
  - Its SWDS guard (`:98-105`) protects a real cycle.
  - It reads the log through a ReadWrite-share handle (`:157-165`).
- **`start_kernel.ps1` avoids two known PowerShell 5.1 traps:** the `$Host` name collision (`:35-37`), and stderr-as-error by redirecting inside `cmd.exe` (`:68-69`).
- **The task definition is otherwise sound:** IgnoreNew, no execution time limit, runs on battery, Interactive and Limited.
- **Nothing at import touches the network** (F18). The Metatron schema deploy is idempotent (`IF NOT EXISTS`).

## Step 4 proposals (not executed; each checked against official docs before use)

1. **Get the wrapper out of a closable console (F1, F2).** Options, in order of least change:
   - (a) **The Architect sets the default terminal to "Windows Console Host"** (Settings, or `HKCU\Console\%%Startup` = `{B23D10C0-E52E-411E-9D5B-C09FDF709C7D}` for both values, as documented in [Group Policy for Windows Terminal](https://learn.microsoft.com/windows/terminal/group-policy#policies)). Per #12464, `-WindowStyle Hidden` then works. It affects every console app on the machine, so it is the Architect's call.
   - (b) **Launch through `conhost.exe --headless`** (`C:\Windows\System32\conhost.exe --headless powershell.exe …`). Headless conhost instances already run on this machine (for example PID 15040). This is the workaround reported in #12464. It is not an endorsed, documented interface, so test it first.
   - (c) **Run the task "whether the user is logged on or not"** (non-interactive), after checking Microsoft's docs on what that changes for OneDrive paths and the user profile.
   - **Never `-NoNewWindow` alone:** it would put uvicorn into the closable window, so closing it would kill the kernel instead of orphaning it.
2. **Task priority 4** (NORMAL class, normal I/O and memory priority, per the table above). Re-register with `-Priority 4` (F3, F20).
3. **Timestamps and phase timings (F9, F20):**
   - a timestamped `logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s")` *before* the imports in `main.py`;
   - a uvicorn log config with `asctime`;
   - `PYTHONUNBUFFERED=1`;
   - one line each for "imports done", "constructors done" and every lifespan step;
   - `start_kernel.ps1` writing its own timestamped launch, probe and exit lines to the log.
4. **A real single-instance guard (F4):**
   - In `start_kernel.ps1`: a process check (same filter as `kernel_ctl.ps1:67-70`), a check for a listener on 8000, a retrying probe, and a named mutex.
   - In `main.py`: a bind pre-check at the top of the lifespan, so a duplicate exits before reconciliation.
5. **Keep task references** and add done-callbacks that log failures. Wrap the scheduler body in `try/except` (F11).
6. **Atomic state writes:** write a temp file, then `os.replace` ([os.replace](https://docs.python.org/3/library/os.html#os.replace)). Log load failures instead of passing (F10).
7. **One lock or per-thread connections for Metatron (F12).** Move Kintsugi's synchronous queries off the event loop (`asyncio.to_thread`).
8. **Dashboard:** skip a poll while the previous one is in flight (F13).
9. **`kernel_ctl.ps1`:** count real elapsed time, raise `START_WAIT_S` to at least 180, and on timeout report "still starting" when the processes exist (F8, F20).
10. **An `async def /debug/startup` route:** phase durations, AnyIO limiter tokens, and thread stacks via `faulthandler`. It works even when sync handlers stall.

Not low-risk, so kept separate: the clock fix (ADR-001) and graceful shutdown in place of `Stop-Process -Force`.

## Actions for the Architect

1. **One question.** After logon, or after the 13:06 relaunch, did a terminal window or tab titled "Windows PowerShell" (or showing `start_kernel.ps1`) appear, and was it closed? A yes confirms F1.
2. **Enable Task Scheduler history** (a system logging setting). Use Task Scheduler → Actions → "Enable All Tasks History", or, in an elevated shell: `wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true`.
3. **When re-enabling CFA:**
   - use `Add-MpPreference` for `claude.exe`, never `Set-MpPreference -ControlledFolderAccessAllowedApplications` (that replaces the list);
   - keep `C:\Python313\python.exe` and `C:\Windows\System32\cmd.exe` allowed (F5).
4. **Optional:**
   - choose option 1(a);
   - pin `.venv` and `local_dbs` with OneDrive's "Always keep on this device";
   - approve one `-X importtime` run of third-party packages (`chromadb`, `google.genai`, `anthropic`, `fastapi`) from outside the repo, to split the ≈90 s import.

## Not done in this review

- `-X importtime` (needs the Architect's OK).
- Pairing of PowerShell/Operational 53504 events.
- A measured Defender scan cost: exclusions need admin, and scan cost stays a hypothesis.
- Which of the logon minutes in F20 came before python started: no process-creation audit exists for those boots.
- No fix was applied or tested.

## Sources (Tier 1)

- Task Scheduler [Priority element](https://learn.microsoft.com/windows/win32/taskschd/taskschedulerschema-priority-settingstype-element) and [RestartOnFailure element](https://learn.microsoft.com/windows/win32/taskschd/taskschedulerschema-restartonfailure-settingstype-element).
- Windows Console: [HandlerRoutine](https://learn.microsoft.com/windows/console/handlerroutine) and [CTRL+CLOSE signal](https://learn.microsoft.com/windows/console/ctrl-close-signal).
- [Group Policy for Windows Terminal](https://learn.microsoft.com/windows/terminal/group-policy#policies), for the `%%Startup` delegation values.
- [microsoft/terminal#12464](https://github.com/microsoft/terminal/issues/12464), "PowerShell argument `WindowStyle -Hidden` is not respected when the default terminal application is Windows Terminal" (open, Backlog; read 2026-10-12).
- [Build a cloud sync engine: compatibility with applications that use reparse points](https://learn.microsoft.com/windows/win32/cfapi/build-a-cloud-file-sync-engine#compatibility-with-applications-that-use-reparse-points).
- Python docs: [asyncio.create_task](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task), [sys.stdout](https://docs.python.org/3/library/sys.html#sys.stdout), [sqlite3.connect](https://docs.python.org/3/library/sqlite3.html#sqlite3.connect) and [os.replace](https://docs.python.org/3/library/os.html#os.replace).
- Installed sources: uvicorn 0.52.4 `server.py:106-107, 173-180` and `config.py:88, 93`; chromadb `telemetry/product/posthog.py:10-11`; google-genai `_api_client.py:788-794`.
