# ============================================
# GenX_FX Cloud Sync Script (PowerShell)
# ============================================
# This script syncs the GenX_FX project to multiple cloud providers
# using rclone. It excludes large folders like .git, node_modules, and .venv
# to save bandwidth and storage space.
#
# Prerequisites:
# 1. Install rclone (https://rclone.org/downloads/)
# 2. Configure remotes using 'rclone config'
# 3. Set up remotes named: remote_dropbox, remote_gdrive, remote_onedrive
#
# For detailed setup instructions, see:
# docs/CLOUD_SYNC_AND_SEO_GUIDE.md
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  GenX_FX Cloud Sync Script" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Set the project path (modify if needed)
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectPath = Split-Path -Parent $ScriptPath
$ProjectName = "GenX_FX"

# Determine cloud base path:
# - Prefer environment variable GENXFX_CLOUD_BASE_PATH if set
# - Fall back to a generic default ("/Projects") otherwise
$EnvCloudBasePath = $env:GENXFX_CLOUD_BASE_PATH
if ([string]::IsNullOrWhiteSpace($EnvCloudBasePath)) {
    $CloudBasePath = "/Projects"
} else {
    $CloudBasePath = $EnvCloudBasePath
}

Write-Host "Project Path: $ProjectPath"
Write-Host "Cloud Base Path: $CloudBasePath"
Write-Host ""

# Check if rclone is installed
try {
    $rcloneVersion = & rclone version 2>&1 | Select-Object -First 1
    Write-Host "rclone found: $rcloneVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "ERROR: rclone is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install rclone from https://rclone.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Define common exclusions
$Exclusions = @(
    "--exclude", ".git/**",
    "--exclude", "node_modules/**",
    "--exclude", ".venv/**",
    "--exclude", "venv/**",
    "--exclude", "__pycache__/**",
    "--exclude", "*.pyc",
    "--exclude", ".idea/**",
    "--exclude", "target/**",
    "--exclude", "build/**",
    "--exclude", "dist/**"
)

# Function to sync to a cloud provider
function Sync-ToCloud {
    param(
        [string]$RemoteName,
        [string]$DisplayName
    )
    
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "Syncing to $DisplayName..." -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    
    $RemotePath = "${RemoteName}:${CloudBasePath}/$ProjectName"
    
    try {
        $rcloneArgs = @("sync", $ProjectPath, $RemotePath, "--progress") + $Exclusions
        & rclone $rcloneArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "$DisplayName sync completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "WARNING: $DisplayName sync failed or incomplete" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "ERROR: Failed to sync to $DisplayName" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
    
    Write-Host ""
}

# Sync to each cloud provider
Sync-ToCloud -RemoteName "remote_dropbox" -DisplayName "Dropbox"
Sync-ToCloud -RemoteName "remote_gdrive" -DisplayName "Google Drive"
Sync-ToCloud -RemoteName "remote_onedrive" -DisplayName "OneDrive"

# Summary
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Cloud Sync Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your GenX_FX project has been synced to:" -ForegroundColor Green
Write-Host "  - Dropbox: $CloudBasePath/$ProjectName" -ForegroundColor White
Write-Host "  - Google Drive: $CloudBasePath/$ProjectName" -ForegroundColor White
Write-Host "  - OneDrive: $CloudBasePath/$ProjectName" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see: docs/CLOUD_SYNC_AND_SEO_GUIDE.md" -ForegroundColor Cyan
Write-Host ""

pause
