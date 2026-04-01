# GitHub Trending System Level Task Setup Script
# Run PowerShell as administrator to execute this script
# This task will run even if no user is logged in

$taskName = "GitHub Trending Daily Push"
$scriptPath = "C:\Users\Z00575KC\Desktop\LQS\Others\Github daily trending\run_trending.bat"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Task already exists, deleting old task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create task trigger (daily at 9:00 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At "09:00"

# Create task action
$action = New-ScheduledTaskAction -Execute $scriptPath

# Create task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -WakeToRun

# Create task principal (SYSTEM user, runs even if no user is logged in)
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# Register task
Register-ScheduledTask `
    -TaskName $taskName `
    -Trigger $trigger `
    -Action $action `
    -Settings $settings `
    -Principal $principal `
    -Description "Automatically push GitHub Trending Top10 projects to email every day at 9:00 AM (system level task, no user login required)"

Write-Host "System level task created successfully!" -ForegroundColor Green
Write-Host "Task Name: $taskName" -ForegroundColor Cyan
Write-Host "Execution Time: Every day at 09:00" -ForegroundColor Cyan
Write-Host "Run As: SYSTEM (no user login required)" -ForegroundColor Cyan
Write-Host "Wake Computer: Enabled" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tip: This task will run normally even if user is not logged in or switched" -ForegroundColor Green
