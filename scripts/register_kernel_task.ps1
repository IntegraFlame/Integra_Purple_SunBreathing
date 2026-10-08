<#
.SYNOPSIS
    Registers (or updates in place) the "Integra Genesis Kernel" scheduled task.
    Idempotent: re-running replaces the existing definition.
    Runs as the current user (Interactive, Limited) -- no admin required.
#>
$ErrorActionPreference = "Stop"
$TaskName = "Integra Genesis Kernel"
$Homebase = "C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\integra-homebase"
$Script   = Join-Path $Homebase "scripts\start_kernel.ps1"
$User     = "$env:USERDOMAIN\$env:USERNAME"

$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Script`"" `
    -WorkingDirectory $Homebase

$trigger   = New-ScheduledTaskTrigger -AtLogOn -User $User
$principal = New-ScheduledTaskPrincipal -UserId $User -LogonType Interactive -RunLevel Limited
$settings  = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -RestartCount 5 -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Principal $principal -Settings $settings `
    -Description "Integra O/S Genesis Kernel (uvicorn main:app on 127.0.0.1:8000). Starts at logon; restarts on failure." `
    -Force | Out-Null

$t = Get-ScheduledTask -TaskName $TaskName
"Registered: $($t.TaskName)  State=$($t.State)"
"Battery: DisallowStart=$($t.Settings.DisallowStartIfOnBatteries) StopIfGoing=$($t.Settings.StopIfGoingOnBatteries)"
"Restart: count=$($t.Settings.RestartCount) interval=$($t.Settings.RestartInterval)  StartWhenAvailable=$($t.Settings.StartWhenAvailable)"
