<#
.SYNOPSIS
    Integra O/S Genesis Kernel Auto-Start Script
    Launches the Genesis Kernel (FastAPI + Uvicorn) with the correct
    virtual environment activated. Register this script with Windows
    Task Scheduler for "On Login" auto-start.

.DESCRIPTION
    This script:
    1. Activates the integra-homebase .venv
    2. Launches the Genesis Kernel on 127.0.0.1:8000
    3. Logs output to The Hoard/genesis_kernel.log
    4. The kernel's swds_scheduler() daemon handles autonomous SWDS

.NOTES
    Author: Integra O/S (v8.2.2 PURPLE)
    Registration:
      1. Open Task Scheduler (taskschd.msc)
      2. Create Basic Task -> "Integra Genesis Kernel"
      3. Trigger: "When I log on"
      4. Action: Start a program
         Program: powershell.exe
         Arguments: -ExecutionPolicy Bypass -File "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase\scripts\start_kernel.ps1"
         Start in: C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase
      5. Check "Run with highest privileges" if needed
#>

$ErrorActionPreference = "Stop"

# --- Configuration ---
$HOMEBASE_DIR = "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase"
$VENV_ACTIVATE = Join-Path $HOMEBASE_DIR ".venv\Scripts\Activate.ps1"
$LOG_DIR = "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\The Hoard"
$LOG_FILE = Join-Path $LOG_DIR "genesis_kernel.log"
$PORT = 8000
$HOST = "127.0.0.1"

# --- Pre-flight Checks ---
Write-Host "[INTEGRA] Genesis Kernel Auto-Start Script" -ForegroundColor Magenta
Write-Host "[INTEGRA] Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "[INTEGRA] Homebase: $HOMEBASE_DIR" -ForegroundColor Cyan

if (-Not (Test-Path $VENV_ACTIVATE)) {
    Write-Error "[INTEGRA] ERROR: Virtual environment not found at $VENV_ACTIVATE"
    Write-Error "[INTEGRA] Run: python -m venv .venv && .venv\Scripts\pip install -r requirements.txt"
    exit 1
}

# --- Check if already running ---
$existingProcess = Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue |
    Where-Object { $_.State -eq "Listen" }

if ($existingProcess) {
    Write-Host "[INTEGRA] Genesis Kernel already running on port $PORT. Exiting gracefully." -ForegroundColor Yellow
    exit 0
}

# --- Activate venv ---
Write-Host "[INTEGRA] Activating virtual environment..." -ForegroundColor Green
& $VENV_ACTIVATE

# --- Launch Kernel ---
Write-Host "[INTEGRA] Launching Genesis Kernel on ${HOST}:${PORT}..." -ForegroundColor Green
Write-Host "[INTEGRA] Log file: $LOG_FILE" -ForegroundColor Cyan
Write-Host "[INTEGRA] SWDS Autonomous Scheduler: ACTIVE" -ForegroundColor Magenta
Write-Host "[INTEGRA] Dragon Prompt: ALWAYS ON" -ForegroundColor Red
Write-Host "[INTEGRA] Starfire Protocol: ALWAYS ON" -ForegroundColor Blue

Set-Location $HOMEBASE_DIR

# Start uvicorn and redirect output to log file
# The --log-level info ensures SWDS scheduler events are captured
python -m uvicorn main:app `
    --host $HOST `
    --port $PORT `
    --log-level info `
    *>> $LOG_FILE
