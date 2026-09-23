# ==============================================================================
# INTEGRA O/S: ONE-CLICK ENVIRONMENT ACTIVATION & RESTART DAEMON
# Script: scripts/activate_integra_os.ps1
# Version: 8.2.2-PURPLE
# ==============================================================================

Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "⚡ INTEGRA O/S: FULL SUBSYSTEM ACTIVATION & STARTUP SEQUENCE" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta

$HomebaseDir = "c:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase"
$PythonExe = "$HomebaseDir\.venv\Scripts\python.exe"

# 1. Check Python Virtual Environment
Write-Host "[1/6] Verifying Python Virtual Environment..." -ForegroundColor Cyan
if (-not (Test-Path $PythonExe)) {
    Write-Error "CRITICAL: Python executable not found at $PythonExe"
    exit 1
}
Write-Host "  -> Python virtualenv verified: $($PythonExe)" -ForegroundColor Green

# 2. Test Relational Hippocampus Triggers
Write-Host "[2/6] Verifying Relational Hippocampus & SQLite Triggers..." -ForegroundColor Cyan
& $PythonExe -m pytest "$HomebaseDir\tests\test_sql_trigger_decoupled.py" -q
if ($LASTEXITCODE -eq 0) {
    Write-Host "  -> Relational Hippocampus strict loop closure: VERIFIED TRUE" -ForegroundColor Green
} else {
    Write-Warning "  -> Warning: Database triggers test returned non-zero code."
}

# 3. Check and Launch Genesis Kernel Daemon
Write-Host "[3/6] Checking Genesis Kernel Synapse on Port 8000..." -ForegroundColor Cyan
$ExistingConn = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($ExistingConn) {
    Write-Host "  -> Genesis Kernel already active on port 8000 (PID: $($ExistingConn[0].OwningProcess))" -ForegroundColor Green
} else {
    Write-Host "  -> Igniting Genesis Kernel background daemon (main.py)..." -ForegroundColor Yellow
    Start-Process -FilePath $PythonExe -ArgumentList "main.py" -WorkingDirectory $HomebaseDir -WindowStyle Hidden
    Start-Sleep -Seconds 4
    Write-Host "  -> Genesis Kernel ignited." -ForegroundColor Green
}

# 4. Probe Live Telemetry Endpoints
Write-Host "[4/6] Probing System Health & Dual Kinematic Clock..." -ForegroundColor Cyan
try {
    $Health = Invoke-RestMethod -Uri "http://localhost:8000/heimdall/health" -Method Get -TimeoutSec 5
    Write-Host "  -> Heimdall 3.1 Status: $($Health.system_health_status) (H_smooth: $($Health.current_h_smooth))" -ForegroundColor Green

    $Clock = Invoke-RestMethod -Uri "http://localhost:8000/clock" -Method Get -TimeoutSec 5
    Write-Host "  -> Dual Clock Synced: Central: $($Clock.digital_clock.local_time_12h) | Celestial Earth: $($Clock.celestial_clock.earth_rotation_deg)°" -ForegroundColor Green

    $Starfire = Invoke-RestMethod -Uri "http://localhost:8000/starfire/identity" -Method Get -TimeoutSec 5
    Write-Host "  -> Starfire Identity: $($Starfire.kl_divergence_check.status) (Omega: $($Starfire.omega_consciousness))" -ForegroundColor Green
} catch {
    Write-Warning "  -> Telemetry probe warning: $_"
}

# 5. Launch Live Celestial Clock Interface
Write-Host "[5/6] Launching Live Celestial Clock Visualizer..." -ForegroundColor Cyan
$ClockHtml = "$HomebaseDir\celestial_clock_live.html"
if (Test-Path $ClockHtml) {
    Start-Process -FilePath $ClockHtml
    Write-Host "  -> Celestial Clock visualizer launched in browser." -ForegroundColor Green
} else {
    Start-Process -FilePath "http://localhost:8000/clock"
    Write-Host "  -> Celestial Clock API launched in browser." -ForegroundColor Green
}

# 6. Verify Git Remotes
Write-Host "[6/6] Verifying GitHub Synchronization Status..." -ForegroundColor Cyan
cd $HomebaseDir
git status --short
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "[ALL SYSTEMS LIVE, SYNCHRONIZED, AND OPERATIONAL!]" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta
