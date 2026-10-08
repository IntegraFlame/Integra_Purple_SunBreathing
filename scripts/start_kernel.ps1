<#
.SYNOPSIS
    Integra O/S Genesis Kernel Auto-Start Script
    Launches the Genesis Kernel (FastAPI + Uvicorn) with the project venv's
    python. Registered with Windows Task Scheduler ("Integra Genesis Kernel")
    for "At log on" auto-start.

.DESCRIPTION
    This script:
    1. Exits 0 if a kernel already answers on 127.0.0.1:8000/clock
    2. Launches the Genesis Kernel on 127.0.0.1:8000 using .venv python
    3. Appends output to The Hoard/genesis_kernel.log (UTF-8)
    4. Blocks while the kernel runs and exits with uvicorn's exit code, so
       Task Scheduler's restart-on-failure policy works.
    5. The kernel's swds_scheduler() daemon handles autonomous SWDS

.NOTES
    Author: Integra O/S (v8.2.2 PURPLE)
    Must work under Windows PowerShell 5.1 (what Task Scheduler's powershell.exe is).
    Registration (see scripts/register_kernel_task.ps1):
      Program:  powershell.exe
      Arguments: -ExecutionPolicy Bypass -WindowStyle Hidden -File "<homebase>\scripts\start_kernel.ps1"
      Start in: <homebase>
#>

# NOTE: not "Stop" -- under PS 5.1, native stderr lines become terminating errors.
$ErrorActionPreference = "Continue"

# --- Configuration ---
$HOMEBASE_DIR = "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase"
$PYTHON_EXE   = Join-Path $HOMEBASE_DIR ".venv\Scripts\python.exe"
$LOG_DIR      = "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\The Hoard"
$LOG_FILE     = Join-Path $LOG_DIR "genesis_kernel.log"
$PORT = 8000
# NOTE: do not name this $HOST -- it collides with PowerShell's read-only automatic $Host
# variable and aborts the script at assignment (verified 2026-10-07).
$BIND_HOST = "127.0.0.1"

Write-Host "[INTEGRA] Genesis Kernel Auto-Start Script" -ForegroundColor Magenta
Write-Host "[INTEGRA] Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "[INTEGRA] Homebase: $HOMEBASE_DIR" -ForegroundColor Cyan

# --- Pre-flight ---
if (-Not (Test-Path $PYTHON_EXE)) {
    Write-Host "[INTEGRA] ERROR: venv python not found at $PYTHON_EXE" -ForegroundColor Red
    Write-Host "[INTEGRA] Run: python -m venv .venv ; .venv\Scripts\pip install -r requirements.txt"
    exit 1
}
if (-Not (Test-Path $LOG_DIR)) { New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null }

# --- Already running? (HTTP probe; Get-NetTCPConnection proved unreliable here) ---
try {
    $r = Invoke-WebRequest -Uri "http://${BIND_HOST}:${PORT}/clock" -UseBasicParsing -TimeoutSec 3
    if ($r.StatusCode -eq 200) {
        Write-Host "[INTEGRA] Genesis Kernel already answering on port $PORT. Exiting gracefully." -ForegroundColor Yellow
        exit 0
    }
} catch { }

# --- Launch Kernel ---
Set-Location $HOMEBASE_DIR
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

Write-Host "[INTEGRA] Launching Genesis Kernel on ${BIND_HOST}:${PORT}..." -ForegroundColor Green
Write-Host "[INTEGRA] Log file: $LOG_FILE" -ForegroundColor Cyan

# Redirect inside cmd.exe so PS 5.1 never sees uvicorn's stderr as error records.
$cmdLine = '"{0}" -m uvicorn main:app --host {1} --port {2} --log-level info >> "{3}" 2>&1' -f $PYTHON_EXE, $BIND_HOST, $PORT, $LOG_FILE
$proc = Start-Process -FilePath "cmd.exe" -ArgumentList @('/c', "`"$cmdLine`"") `
    -WorkingDirectory $HOMEBASE_DIR -WindowStyle Hidden -PassThru -Wait
exit $proc.ExitCode
