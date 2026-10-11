Set-Location "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase"; powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing/integra-homebase/scripts/kernel_ctl.ps1' status; "exit=$LASTEXITCODE"
KERNEL=UP
URL=http://127.0.0.1:8000
LATENCY_MS=434
HEALTH=OK
SWDS_STATE=AWAKE
TASK_STATE=Running
PIDS=12700,12656
DASHBOARD=http://127.0.0.1:8000/dashboard
exit=0

This copy doesn’t have a LEARNINGS.md or LOCAL.md, so I’ll skip that step and instead create a new reference memory called antigravity-kernel-access to capture the kernel control path learnings, then add a concise index line for it.

Antigravity can now check, start, restart and stop the Genesis Kernel, read its logs, and open its dashboard. Everything runs through one new script, kernel_ctl.ps1, and a new Antigravity skill tells its agent how to use it. I haven’t seen the skill appear inside Antigravity, and I didn’t run stop or restart, because that would take your live kernel down.

What I added

The script: it has five actions: status, logs, start, stop, restart.
start goes through your existing “Integra Genesis Kernel” scheduled task. That’s the same launcher used at logon, so the kernel stays on 127.0.0.1 only and logs to the Hoard. If a kernel is already running, start does nothing.
stop and restart refuse unless the kernel reports SWDS as awake, because Heimdall owns the SWDS cycle. Adding -Force overrides that, and should be used only when you approve it.
The skill: ~/.gemini/config/skills/genesis-kernel/SKILL.md, next to your integra-protocol skill. It gives Antigravity’s agent the exact commands and these rules:
Never start the kernel with python main.py (it binds 0.0.0.0 and exposes the API to your network).
Ask you before stop, restart or any POST. POSTs can change SWDS state or make paid model calls.
Never read .env files for the admin token.
Never touch the trading routes.
Never run tests against the live repo.
It also lists the read-only routes, which the agent can query freely without blocking SWDS.
IDE task: the old “integra: start-genesis-kernel” task ran main.py directly, which binds 0.0.0.0. It now calls the script, and I added an “integra: kernel-status” task.
Testing

The script parses cleanly under Windows PowerShell 5.1 and PowerShell 7.
status, logs, start and the IDE task all work. start correctly did nothing because the kernel was already up.
stop, restart and their SWDS guard are untested.

<#
.SYNOPSIS
    Integra O/S Genesis Kernel control: status / start / stop / restart / logs.
    One entry point so an agent platform (Antigravity 2.0) can operate the kernel
    through a short list of exact, pre-approvable commands.

.DESCRIPTION
    start    Starts the kernel through the "Integra Genesis Kernel" scheduled task (the
             same launch path as at logon: start_kernel.ps1, 127.0.0.1:8000, log in
             The Hoard). Never launches a second kernel: exits 0 if one already answers,
             exits 2 if kernel processes exist but do not answer (use restart).
    stop     Refuses unless /swds/status reports AWAKE (Heimdall 3.1 owns the SWDS cycle).
             -Force overrides, for when the Architect has approved it.
    restart  stop, then start. Same SWDS guard.
    status   Read-only. Exit 0 = kernel answering, 1 = down, 2 = processes up but not answering.
    logs     Read-only. Last -Lines lines of genesis_kernel.log (mixed UTF-16/UTF-8: NULs stripped).

.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File integra-homebase\scripts\kernel_ctl.ps1 status

.NOTES
    Must work under Windows PowerShell 5.1 (no ?? / ternary operators; -UseBasicParsing).
    Never run main.py directly to start the kernel: its __main__ block binds 0.0.0.0.
#>
param(
    [Parameter(Position = 0)]
    [ValidateSet("status", "start", "stop", "restart", "logs")]
    [string]$Action = "status",
    [int]$Lines = 60,
    [switch]$Force
)

# NOTE: not "Stop" -- under PS 5.1, native stderr lines become terminating errors.
$ErrorActionPreference = "Continue"

# --- Configuration (derived from this script's location) ---
$HOMEBASE_DIR = Split-Path -Parent $PSScriptRoot
$REPO_DIR     = Split-Path -Parent $HOMEBASE_DIR
$START_SCRIPT = Join-Path $PSScriptRoot "start_kernel.ps1"
$LOG_FILE     = Join-Path (Join-Path $REPO_DIR "The Hoard") "genesis_kernel.log"
$TASK_NAME    = "Integra Genesis Kernel"
$BASE_URL     = "http://127.0.0.1:8000"
$START_WAIT_S = 120
$STOP_WAIT_S  = 30

function Test-Kernel {
    # Returns latency in ms, or -1. Retries because a loaded kernel can refuse a connection
    # and then answer a moment later.
    for ($i = 0; $i -lt 3; $i++) {
        $sw = [Diagnostics.Stopwatch]::StartNew()
        try {
            $r = Invoke-WebRequest -Uri "$BASE_URL/clock" -UseBasicParsing -TimeoutSec 10
            if ($r.StatusCode -eq 200) { return [int]$sw.Elapsed.TotalMilliseconds }
        } catch { }
        Start-Sleep -Seconds 1
    }
    return -1
}

function Get-SwdsState {
    try {
        $r = Invoke-WebRequest -Uri "$BASE_URL/swds/status" -UseBasicParsing -TimeoutSec 15
        return ($r.Content | ConvertFrom-Json).state
    } catch { return "UNKNOWN" }
}

function Get-KernelProcesses {
    Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
        Where-Object { $_.CommandLine -like "*uvicorn main:app*" -and $_.CommandLine -like "*--port 8000*" }
}

function Get-TaskState {
    $t = Get-ScheduledTask -TaskName $TASK_NAME -ErrorAction SilentlyContinue
    if ($t) { return [string]$t.State }
    return "NOT_REGISTERED"
}

function Show-Status {
    $ms    = Test-Kernel
    $procs = @(Get-KernelProcesses)
    if ($ms -ge 0)            { $state = "UP" }
    elseif ($procs.Count -gt 0) { $state = "UNRESPONSIVE" }
    else                      { $state = "DOWN" }
    Write-Host "KERNEL=$state"
    Write-Host "URL=$BASE_URL"
    if ($ms -ge 0) {
        Write-Host "LATENCY_MS=$ms"
        # Healthy baseline is tens of ms; seconds means the kernel is degraded (restart candidate).
        if ($ms -le 1000) { Write-Host "HEALTH=OK" } else { Write-Host "HEALTH=SLOW" }
        Write-Host "SWDS_STATE=$(Get-SwdsState)"
    }
    Write-Host "TASK_STATE=$(Get-TaskState)"
    Write-Host "PIDS=$(($procs | ForEach-Object { $_.ProcessId }) -join ',')"
    Write-Host "DASHBOARD=$BASE_URL/dashboard"
    return $state
}

function Assert-SwdsAllowsStop {
    if ($Force) { Write-Host "[INTEGRA] -Force given: skipping the SWDS guard."; return $true }
    $swds = Get-SwdsState
    if ($swds -eq "AWAKE") { return $true }
    Write-Host "[INTEGRA] REFUSED: SWDS state is '$swds'. Heimdall 3.1 owns the SWDS cycle."
    Write-Host "[INTEGRA] Ask the Architect; if approved, re-run with -Force."
    return $false
}

function Stop-Kernel {
    if ((Get-TaskState) -eq "Running") {
        Stop-ScheduledTask -TaskName $TASK_NAME -ErrorAction SilentlyContinue
        Write-Host "[INTEGRA] Scheduled task stopped."
    }
    foreach ($p in @(Get-KernelProcesses)) {
        try {
            Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop
            Write-Host "[INTEGRA] Stopped kernel process $($p.ProcessId)."
        } catch { }
    }
    for ($i = 0; $i -lt $STOP_WAIT_S; $i++) {
        if (@(Get-KernelProcesses).Count -eq 0) { Write-Host "KERNEL=DOWN"; return $true }
        Start-Sleep -Seconds 1
    }
    Write-Host "[INTEGRA] ERROR: kernel processes still present after ${STOP_WAIT_S}s."
    return $false
}

function Start-Kernel {
    if ((Test-Kernel) -ge 0) { Write-Host "[INTEGRA] Already running."; Show-Status | Out-Null; return 0 }
    if (@(Get-KernelProcesses).Count -gt 0) {
        Write-Host "[INTEGRA] Kernel processes exist but do not answer. Use: restart"
        return 2
    }
    $taskState = Get-TaskState
    if ($taskState -eq "NOT_REGISTERED") {
        # Detached fallback: start_kernel.ps1 blocks while the kernel runs.
        Start-Process -FilePath "powershell.exe" -WindowStyle Hidden -WorkingDirectory $HOMEBASE_DIR `
            -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$START_SCRIPT`"") | Out-Null
        Write-Host "[INTEGRA] Scheduled task not registered; launched start_kernel.ps1 detached."
    } else {
        # A Running task with no kernel process is a stuck launcher; clear it first.
        if ($taskState -eq "Running") { Stop-ScheduledTask -TaskName $TASK_NAME -ErrorAction SilentlyContinue }
        Start-ScheduledTask -TaskName $TASK_NAME
        Write-Host "[INTEGRA] Started scheduled task '$TASK_NAME'."
    }
    for ($i = 0; $i -lt $START_WAIT_S; $i += 2) {
        Start-Sleep -Seconds 2
        try {
            $r = Invoke-WebRequest -Uri "$BASE_URL/clock" -UseBasicParsing -TimeoutSec 5
            if ($r.StatusCode -eq 200) { Write-Host "[INTEGRA] Kernel answering after ~$($i + 2)s."; Show-Status | Out-Null; return 0 }
        } catch { }
    }
    Write-Host "[INTEGRA] ERROR: kernel did not answer within ${START_WAIT_S}s. Check: kernel_ctl.ps1 logs"
    return 1
}

function Show-Logs {
    if (-Not (Test-Path $LOG_FILE)) { Write-Host "[INTEGRA] No log at $LOG_FILE"; return }
    $fs = [System.IO.File]::Open($LOG_FILE, 'Open', 'Read', 'ReadWrite')
    try {
        $take = [Math]::Min($fs.Length, 262144)
        $fs.Seek(-$take, 'End') | Out-Null
        $buf = New-Object byte[] $take
        $n = $fs.Read($buf, 0, $take)
    } finally { $fs.Close() }
    # UTF-16LE segments decode as text interleaved with NUL chars; dropping NULs recovers them.
    $text = [System.Text.Encoding]::UTF8.GetString($buf, 0, $n).Replace([string][char]0, "")
    $text -split "`r?`n" | Select-Object -Last $Lines
}

switch ($Action) {
    "status" {
        $s = Show-Status
        if ($s -eq "UP") { exit 0 } elseif ($s -eq "UNRESPONSIVE") { exit 2 } else { exit 1 }
    }
    "logs"   { Show-Logs; exit 0 }
    "start"  { exit (Start-Kernel) }
    "stop"   {
        if (-Not (Assert-SwdsAllowsStop)) { exit 2 }
        if (Stop-Kernel) { exit 0 } else { exit 1 }
    }
    "restart" {
        if (-Not (Assert-SwdsAllowsStop)) { exit 2 }
        if (-Not (Stop-Kernel)) { exit 1 }
        exit (Start-Kernel)
    }
}




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


{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "tasks: build",
            "type": "shell",
            "command": "npm run build",
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "problemMatcher": [
                "$tsc"
            ]
        },
        {
            "label": "npm: watch",
            "type": "shell",
            "command": "npm run watch",
            "isBackground": true,
            "problemMatcher": [
                "$tsc-watch"
            ]
        },
        {
            "label": "npm: watch-tests",
            "type": "shell",
            "command": "npm run watch-tests",
            "isBackground": true,
            "problemMatcher": [
                "$tsc-watch"
            ]
        },
        {
            "label": "integra: build-python-env",
            "type": "shell",
            "command": "& '${workspaceFolder}/integra-homebase/.venv/Scripts/python.exe' -m pip install -r '${workspaceFolder}/integra-homebase/requirements.txt'",
            "options": {
                "cwd": "${workspaceFolder}/integra-homebase"
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "integra: run-diagnostics",
            "type": "shell",
            "command": "& '${workspaceFolder}/integra-homebase/.venv/Scripts/python.exe' '${workspaceFolder}/integra-homebase/scripts/system_diagnostic.py'",
            "options": {
                "cwd": "${workspaceFolder}/integra-homebase"
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "integra: run-tests",
            "type": "shell",
            "command": "& '${workspaceFolder}/integra-homebase/.venv/Scripts/python.exe' -m pytest tests",
            "options": {
                "cwd": "${workspaceFolder}/integra-homebase"
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "integra: start-genesis-kernel",
            "type": "shell",
            "command": "powershell -NoProfile -ExecutionPolicy Bypass -File '${workspaceFolder}/integra-homebase/scripts/kernel_ctl.ps1' start",
            "options": {
                "cwd": "${workspaceFolder}/integra-homebase"
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "integra: kernel-status",
            "type": "shell",
            "command": "powershell -NoProfile -ExecutionPolicy Bypass -File '${workspaceFolder}/integra-homebase/scripts/kernel_ctl.ps1' status",
            "options": {
                "cwd": "${workspaceFolder}/integra-homebase"
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            },
            "problemMatcher": []
        }
    ]
}
