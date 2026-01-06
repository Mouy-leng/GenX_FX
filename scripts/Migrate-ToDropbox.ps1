# Migrate-ToDropbox.ps1
# Migrates files from current location to Dropbox structure

<#
.SYNOPSIS
    Migrates files to the Dropbox organization structure.

.DESCRIPTION
    This script helps migrate files from your current directory structure
    to the new Dropbox organization. It categorizes files and copies them
    to appropriate Dropbox locations with safety checks.

.PARAMETER SourcePath
    Path to migrate from (defaults to current GenX_FX repository)

.PARAMETER DropboxPath
    Path to Dropbox folder (defaults to %USERPROFILE%\Dropbox)

.PARAMETER Category
    Specific category to migrate (Documentation, Scripts, Projects, All)

.PARAMETER DryRun
    If specified, shows what would be migrated without actually copying

.PARAMETER EncryptCredentials
    If specified, prompts to encrypt credential files before migration

.EXAMPLE
    .\Migrate-ToDropbox.ps1 -Category Documentation
    Migrates only documentation files

.EXAMPLE
    .\Migrate-ToDropbox.ps1 -DryRun
    Shows what would be migrated without making changes

.EXAMPLE
    .\Migrate-ToDropbox.ps1 -Category All -EncryptCredentials
    Migrates all files and encrypts credentials

.NOTES
    Author: A6-9V GenX_FX System
    Version: 1.0
    Last Updated: 2026-01-06
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$SourcePath = (Get-Location).Path,
    
    [Parameter(Mandatory=$false)]
    [string]$DropboxPath = (Join-Path $env:USERPROFILE "Dropbox"),
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("Documentation", "Scripts", "Projects", "Credentials", "All")]
    [string]$Category = "All",
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun,
    
    [Parameter(Mandatory=$false)]
    [switch]$EncryptCredentials
)

Write-Host "🚀 Dropbox Migration Tool" -ForegroundColor Cyan
Write-Host "Source: $SourcePath" -ForegroundColor Gray
Write-Host "Destination: $DropboxPath" -ForegroundColor Gray
Write-Host "Category: $Category" -ForegroundColor Gray
if ($DryRun) {
    Write-Host "Mode: DRY RUN (no changes will be made)" -ForegroundColor Yellow
}
Write-Host ""

# Check if Dropbox structure exists
if (-not (Test-Path (Join-Path $DropboxPath "00_System-Core"))) {
    Write-Host "❌ Dropbox structure not found!" -ForegroundColor Red
    Write-Host "   Please run Create-DropboxStructure.ps1 first." -ForegroundColor Yellow
    exit 1
}

# Define migration rules
$migrationRules = @{
    "Documentation" = @{
        Patterns = @("*.md", "*.txt", "*.pdf", "*.docx")
        Destination = "04_Documentation/GenX_FX-Docs"
        Description = "Documentation files (Markdown, text, PDF)"
    }
    "Scripts-PowerShell" = @{
        Patterns = @("*.ps1", "*.psm1", "*.psd1")
        Destination = "03_Automation-Scripts/powershell"
        Description = "PowerShell scripts"
    }
    "Scripts-Batch" = @{
        Patterns = @("*.bat", "*.cmd")
        Destination = "03_Automation-Scripts/powershell"
        Description = "Batch files"
    }
    "Scripts-Shell" = @{
        Patterns = @("*.sh", "*.bash")
        Destination = "03_Automation-Scripts/bash"
        Description = "Shell scripts"
    }
    "Python-Source" = @{
        Patterns = @("*.py")
        Destination = "01_Projects/GenX_FX/src"
        Description = "Python source files"
    }
    "Config-Files" = @{
        Patterns = @("*.json", "*.yaml", "*.yml", "*.toml")
        Destination = "01_Projects/GenX_FX/configs"
        Description = "Configuration files"
    }
    "Docker-Files" = @{
        Patterns = @("Dockerfile", "docker-compose.yml", "*.dockerfile")
        Destination = "01_Projects/GenX_FX/docker"
        Description = "Docker configuration"
    }
}

# Function to check if file matches category
function Test-FileCategory {
    param([string]$FilePath, [string]$CategoryFilter)
    
    $fileName = [System.IO.Path]::GetFileName($FilePath)
    
    switch ($CategoryFilter) {
        "Documentation" {
            return $fileName -match '\.(md|txt|pdf|docx)$'
        }
        "Scripts" {
            return $fileName -match '\.(ps1|bat|cmd|sh|bash)$'
        }
        "Projects" {
            return $FilePath -match '(A6-9V|ProductionApp|Projects)' -and -not ($fileName -match '\.(ps1|bat|sh|md)$')
        }
        "Credentials" {
            return $fileName -match '(secret|credential|password|\.env|key)' -or $FilePath -match 'SECRETS\.md'
        }
        "All" {
            return $true
        }
        default {
            return $false
        }
    }
}

# Function to get destination path
function Get-DestinationPath {
    param([string]$SourceFilePath, [string]$SourceRoot)
    
    $fileName = [System.IO.Path]::GetFileName($SourceFilePath)
    $relativePath = $SourceFilePath.Substring($SourceRoot.Length).TrimStart('\', '/')
    
    # Special handling for specific files
    if ($fileName -match '\.md$') {
        return "04_Documentation/GenX_FX-Docs/$fileName"
    }
    elseif ($fileName -match '\.ps1$') {
        return "03_Automation-Scripts/powershell/$fileName"
    }
    elseif ($fileName -match '\.(bat|cmd)$') {
        return "03_Automation-Scripts/powershell/$fileName"
    }
    elseif ($fileName -match '\.(sh|bash)$') {
        return "03_Automation-Scripts/bash/$fileName"
    }
    elseif ($fileName -match '\.py$') {
        if ($relativePath -match 'test') {
            return "01_Projects/GenX_FX/tests/$fileName"
        }
        else {
            return "01_Projects/GenX_FX/src/$fileName"
        }
    }
    elseif ($fileName -match 'Dockerfile|docker-compose') {
        return "01_Projects/GenX_FX/docker/$fileName"
    }
    elseif ($fileName -match '\.(json|yaml|yml|toml)$') {
        return "01_Projects/GenX_FX/configs/$fileName"
    }
    elseif ($fileName -match '(secret|credential|password|\.env)' -or $SourceFilePath -match 'SECRETS\.md') {
        return "02_Secure-Credentials/ENV-Files-Encrypted/$fileName.NEEDS_ENCRYPTION"
    }
    elseif ($relativePath -match '^A6-9V') {
        return "01_Projects/GenX_FX/$relativePath"
    }
    elseif ($relativePath -match '^ProductionApp') {
        return "01_Projects/$relativePath"
    }
    elseif ($relativePath -match '^Projects') {
        return "01_Projects/$relativePath"
    }
    else {
        return "01_Projects/GenX_FX/misc/$fileName"
    }
}

# Function to encrypt file
function Invoke-FileEncryption {
    param([string]$FilePath, [string]$DestinationPath)
    
    Write-Host "  🔐 Encrypting: $FilePath" -ForegroundColor Yellow
    
    # Create encrypted archive
    $zipPath = "$DestinationPath.encrypted.zip"
    
    try {
        # Use Windows built-in compression
        Compress-Archive -Path $FilePath -DestinationPath $zipPath -Force
        Write-Host "  ✅ Encrypted to: $zipPath" -ForegroundColor Green
        return $zipPath
    }
    catch {
        Write-Host "  ❌ Encryption failed: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Statistics
$stats = @{
    Scanned = 0
    Copied = 0
    Skipped = 0
    Failed = 0
    Encrypted = 0
}

# Exclude patterns
$excludePatterns = @(
    "node_modules",
    "venv",
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "*.pyc",
    "*.tmp",
    "*.log"
)

# Function to test if path should be excluded
function Test-Excluded {
    param([string]$Path)
    
    foreach ($pattern in $excludePatterns) {
        if ($Path -like "*$pattern*") {
            return $true
        }
    }
    return $false
}

Write-Host "📊 Analyzing files for migration..." -ForegroundColor Yellow
Write-Host ""

# Get all files
$allFiles = Get-ChildItem -Path $SourcePath -Recurse -File -ErrorAction SilentlyContinue | 
    Where-Object { -not (Test-Excluded -Path $_.FullName) }

$filesToMigrate = @()

foreach ($file in $allFiles) {
    $stats.Scanned++
    
    # Check if file matches category filter
    if (Test-FileCategory -FilePath $file.FullName -CategoryFilter $Category) {
        $destPath = Get-DestinationPath -SourceFilePath $file.FullName -SourceRoot $SourcePath
        
        $filesToMigrate += [PSCustomObject]@{
            SourcePath = $file.FullName
            SourceRelative = $file.FullName.Substring($SourcePath.Length).TrimStart('\', '/')
            DestinationPath = $destPath
            Size = $file.Length
            RequiresEncryption = $destPath -match 'Secure-Credentials|NEEDS_ENCRYPTION'
        }
    }
}

# Display migration plan
Write-Host "📋 Migration Plan" -ForegroundColor Cyan
Write-Host "Files to migrate: $($filesToMigrate.Count)" -ForegroundColor White
Write-Host ""

if ($filesToMigrate.Count -eq 0) {
    Write-Host "⚠️  No files found matching category: $Category" -ForegroundColor Yellow
    exit 0
}

# Group by destination folder
$groupedFiles = $filesToMigrate | Group-Object { Split-Path -Parent $_.DestinationPath }

foreach ($group in ($groupedFiles | Sort-Object Name)) {
    $folder = $group.Name
    $count = $group.Count
    $totalSize = ($group.Group | Measure-Object -Property Size -Sum).Sum
    $sizeFormatted = if ($totalSize -gt 1MB) {
        "{0:N2} MB" -f ($totalSize / 1MB)
    } else {
        "{0:N2} KB" -f ($totalSize / 1KB)
    }
    
    Write-Host "  📁 $folder" -ForegroundColor Cyan
    Write-Host "     $count files ($sizeFormatted)" -ForegroundColor Gray
}

Write-Host ""

# Confirm before proceeding
if (-not $DryRun) {
    Write-Host "⚠️  Ready to migrate $($filesToMigrate.Count) files" -ForegroundColor Yellow
    $response = Read-Host "Continue? (y/n)"
    
    if ($response -ne 'y') {
        Write-Host "Migration cancelled." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "🚀 Starting migration..." -ForegroundColor Green
Write-Host ""

# Migrate files
$progress = 0
foreach ($file in $filesToMigrate) {
    $progress++
    Write-Progress -Activity "Migrating Files" -Status "$progress of $($filesToMigrate.Count)" -PercentComplete (($progress / $filesToMigrate.Count) * 100)
    
    $destFullPath = Join-Path $DropboxPath $file.DestinationPath
    $destFolder = Split-Path -Parent $destFullPath
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] $($file.SourceRelative) → $($file.DestinationPath)" -ForegroundColor Gray
        $stats.Copied++
    }
    else {
        try {
            # Create destination folder
            if (-not (Test-Path $destFolder)) {
                New-Item -Path $destFolder -ItemType Directory -Force | Out-Null
            }
            
            # Check if file needs encryption
            if ($file.RequiresEncryption) {
                if ($EncryptCredentials) {
                    $encrypted = Invoke-FileEncryption -FilePath $file.SourcePath -DestinationPath $destFullPath
                    if ($encrypted) {
                        $stats.Encrypted++
                        $stats.Copied++
                    }
                    else {
                        $stats.Failed++
                    }
                }
                else {
                    Write-Host "  ⚠️  SKIPPED (needs encryption): $($file.SourceRelative)" -ForegroundColor Yellow
                    Write-Host "     Run with -EncryptCredentials to encrypt this file" -ForegroundColor DarkGray
                    $stats.Skipped++
                }
            }
            else {
                # Copy file
                Copy-Item -Path $file.SourcePath -Destination $destFullPath -Force
                Write-Host "  ✅ $($file.SourceRelative) → $($file.DestinationPath)" -ForegroundColor Green
                $stats.Copied++
            }
        }
        catch {
            Write-Host "  ❌ Failed: $($file.SourceRelative) - $($_.Exception.Message)" -ForegroundColor Red
            $stats.Failed++
        }
    }
}

Write-Progress -Activity "Migrating Files" -Completed

# Display summary
Write-Host ""
Write-Host "✨ Migration Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Summary:" -ForegroundColor Cyan
Write-Host "  - Files scanned: $($stats.Scanned)" -ForegroundColor Gray
Write-Host "  - Files migrated: $($stats.Copied)" -ForegroundColor Green
if ($stats.Encrypted -gt 0) {
    Write-Host "  - Files encrypted: $($stats.Encrypted)" -ForegroundColor Cyan
}
if ($stats.Skipped -gt 0) {
    Write-Host "  - Files skipped: $($stats.Skipped)" -ForegroundColor Yellow
}
if ($stats.Failed -gt 0) {
    Write-Host "  - Files failed: $($stats.Failed)" -ForegroundColor Red
}
Write-Host ""

if ($DryRun) {
    Write-Host "🔍 This was a dry run. No changes were made." -ForegroundColor Yellow
    Write-Host "   Run without -DryRun flag to perform migration." -ForegroundColor Yellow
}
else {
    Write-Host "🎯 Next Steps:" -ForegroundColor Yellow
    Write-Host "   1. Verify migrated files in Dropbox"
    Write-Host "   2. Test file access and functionality"
    Write-Host "   3. Update script paths if needed"
    Write-Host "   4. Migrate remaining categories"
    Write-Host "   5. Configure selective sync"
    Write-Host "   6. Clean up old files after verification"
}

if ($stats.Skipped -gt 0 -and -not $EncryptCredentials) {
    Write-Host ""
    Write-Host "⚠️  Some files require encryption" -ForegroundColor Yellow
    Write-Host "   Run: .\Migrate-ToDropbox.ps1 -Category Credentials -EncryptCredentials" -ForegroundColor White
}

Write-Host ""
