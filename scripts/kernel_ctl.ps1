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
