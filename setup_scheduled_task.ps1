# Script to register GenX FX Trading Platform startup task in Windows Task Scheduler
# Run this script as administrator

# Get the current directory where the script is located
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$tradingScript = Join-Path $scriptPath "start_trading_local.ps1"

# Create the task action - run PowerShell with our script
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$tradingScript`"" `
    -WorkingDirectory $scriptPath

# Create the trigger - at system startup with delay
$trigger = New-ScheduledTaskTrigger -AtStartup
$trigger.Delay = "PT1M"  # 1 minute delay to ensure network is ready

# Set task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0)  # run indefinitely

# Create the task principal (run with highest privileges)
$principal = New-ScheduledTaskPrincipal `
    -UserId "SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

# Register the task
$taskName = "GenX FX Trading Platform - Startup"
$description = "Starts and monitors the GenX FX Trading Platform services"

try {
    # Remove existing task if it exists
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    
    # Register new task
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description $description

    Write-Host "Task scheduled successfully. The trading platform will start automatically at system boot."
    Write-Host "Task details:"
    Write-Host "- Name: $taskName"
    Write-Host "- Script: $tradingScript"
    Write-Host "- Runs as: SYSTEM"
    Write-Host "- Trigger: At startup (delayed by 1 minute)"
    Write-Host "- Auto-restart: Up to 3 times if fails"
} catch {
    Write-Host "Error creating scheduled task: $_"
    exit 1
}