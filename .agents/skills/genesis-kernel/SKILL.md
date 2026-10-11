---
name: genesis-kernel
description: Check, start, stop, restart and read the Integra O/S Genesis Kernel (FastAPI on 127.0.0.1:8000) from Antigravity. Use whenever a task needs the kernel running, its live state, its logs, or its dashboard.
---
# Genesis Kernel — operating it from Antigravity

The Genesis Kernel is Integra's FastAPI/uvicorn server at **http://127.0.0.1:8000**, launched by the
Windows scheduled task **"Integra Genesis Kernel"** (`integra-homebase/scripts/start_kernel.ps1`,
loopback only, log in `The Hoard/genesis_kernel.log`). Operate it **only** through `kernel_ctl.ps1`.

## Commands (exact strings — run them as written)

| Purpose | Command | Side effects |
|---|---|---|
| Status (read-only) | `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase\scripts\kernel_ctl.ps1" status` | none |
| Last log lines (read-only) | `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase\scripts\kernel_ctl.ps1" logs` | none |
| Start | `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase\scripts\kernel_ctl.ps1" start` | starts the kernel if it is down; no-op if it is up |
| Restart | `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase\scripts\kernel_ctl.ps1" restart` | **ask the Architect first** |
| Stop | `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase\scripts\kernel_ctl.ps1" stop` | **ask the Architect first** |

`status` prints `KERNEL=UP|UNRESPONSIVE|DOWN`, `LATENCY_MS`, `HEALTH=OK|SLOW`, `SWDS_STATE`, `TASK_STATE`,
`PIDS`. Exit codes: 0 up, 1 down, 2 processes present but not answering.
`logs -Lines 200` shows more lines. `start` waits up to 120 s for the kernel to answer.

## Rules

1. **Never start the kernel any other way.** Not `python main.py` (its `__main__` binds 0.0.0.0, exposing an
   unauthenticated API to the LAN), not `uvicorn` by hand (bypasses the single-instance guard and the log).
2. **Stop / restart need the Architect's yes in chat.** The script also refuses unless `/swds/status`
   reports `AWAKE`: Heimdall 3.1 alone opens and closes the SWDS cycle. `-Force` overrides that guard; use it
   only after the Architect explicitly approves forcing it.
3. **GET routes are read-only; read them freely.** They do not count as activity, so they do not block SWDS:
   `/`, `/clock`, `/clock/full`, `/clock/live`, `/clock/sync`, `/dashboard`, `/swds/status`,
   `/heimdall/health`, `/heimdall/telemetry`, `/cheshire/status`, `/cheshire/environment`,
   `/models/router/status`, `/models/telemetry`, `/rodin/telemetry`, `/metatron/status`,
   `/looking-glass/status`, `/fortress/status`, `/fortress/hunter/telemetry`, `/antigravity/health`,
   `/antigravity/telemetry`, `/dragon/status`, `/epiphany/telemetry`, `/thermodynamic/telemetry`,
   `/defense/telemetry`, `/domain/telemetry`, `/bridge/telemetry`, `/starfire/identity`, `/celestial/checkpoint`.
   Example: `curl -s http://127.0.0.1:8000/swds/status`
4. **POST routes change state and count as activity (they reset the SWDS idle timer). Ask before any POST.**
   In particular:
   - `/swds/*` (`initiate`, `sleep`, `awaken`, `trigger`): Heimdall's authority. Never call without the Architect.
   - `/models/selftest`, `/cognitive/cycle`, `/rodin/query`, `/shiva/pass`, `/ignite`, `/dragon/flight`:
     may make **paid model calls**.
   - `/models/selftest` needs the `X-Integra-Admin` header. Never read `.env` files to get the token: ask the Architect.
   - `/fortress/*`: paper trading only. Never place, verify or route a trade.
5. **Do not hammer it.** The dashboard polls 7 endpoints every second; leaving it open slowed every request to
   several seconds on 2026-10-10. Close the dashboard tab when done; poll status no more than every 30 s.
   If `HEALTH=SLOW` persists with nothing polling, a restart is the usual fix (rule 2 applies).
6. **Do not run the test suite against the live repo.** Tests write into the live `kernel_memory` and the Hoard;
   run them only in an isolated copy.
7. **Report what you observed.** Quote `status` output; do not call the kernel "online" or a subsystem
   "working" without evidence (the Integra status legend: VERIFIED / HEURISTIC / CONSTANT / UNVERIFIED …).

## Viewing it

Open in the Antigravity browser: `http://127.0.0.1:8000/dashboard` (Heimdall 3.1 dashboard) or
`http://127.0.0.1:8000/clock/live` (celestial clock). Both are served by the kernel itself.

## When something is wrong

- `KERNEL=DOWN` → run `start`.
- `KERNEL=UNRESPONSIVE` (processes up, not answering) → `start` refuses on purpose; ask the Architect, then `restart`.
- `start` times out → run `logs` and report the last error lines verbatim.
- `TASK_STATE=NOT_REGISTERED` → `start` falls back to launching `start_kernel.ps1` detached; tell the Architect
  the task is missing (`integra-homebase/scripts/register_kernel_task.ps1` registers it).
