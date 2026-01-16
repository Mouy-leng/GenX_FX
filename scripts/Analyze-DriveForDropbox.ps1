# Analyze-DriveForDropbox.ps1
# Analyzes current drive structure and generates mapping to Dropbox organization

<#
.SYNOPSIS
    Analyzes your current drive and creates a detailed report for Dropbox migration.

.DESCRIPTION
    This script scans your current directory structure, categorizes files,
    calculates sizes, and generates a comprehensive migration plan for the
    Dropbox organization blueprint.

.PARAMETER SourcePath
    Path to analyze (defaults to current GenX_FX repository)

.PARAMETER OutputPath
    Path for analysis reports (defaults to ./dropbox-analysis)

.PARAMETER ExcludePatterns
    File patterns to exclude from analysis

.EXAMPLE
    .\Analyze-DriveForDropbox.ps1
    Analyzes current directory

.EXAMPLE
    .\Analyze-DriveForDropbox.ps1 -SourcePath "C:\Projects\GenX_FX"
    Analyzes specific path

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
    [string]$OutputPath = (Join-Path (Get-Location).Path "dropbox-analysis"),
    
    [Parameter(Mandatory=$false)]
    [string[]]$ExcludePatterns = @(
        "node_modules",
        "venv",
        "__pycache__",
        ".git",
        ".idea",
        "*.pyc",
        "*.tmp",
        "*.log"
    )
)

# Create output directory
if (-not (Test-Path $OutputPath)) {
    New-Item -Path $OutputPath -ItemType Directory -Force | Out-Null
}

Write-Host "🔍 Analyzing Drive Structure for Dropbox Migration" -ForegroundColor Cyan
Write-Host "Source: $SourcePath" -ForegroundColor Gray
Write-Host "Output: $OutputPath" -ForegroundColor Gray
Write-Host ""

# Initialize analysis data
$analysis = @{
    TotalFiles = 0
    TotalSize = 0
    Categories = @{}
    FileTypes = @{}
    LargeFiles = @()
    Mappings = @()
}

# Define category rules
$categoryRules = @{
    "Documentation" = @("*.md", "*.txt", "*.pdf", "*.docx")
    "Scripts-PowerShell" = @("*.ps1", "*.psm1", "*.psd1")
    "Scripts-Shell" = @("*.sh", "*.bash")
    "Scripts-Batch" = @("*.bat", "*.cmd")
    "Python-Source" = @("*.py")
    "JavaScript-Source" = @("*.js", "*.ts", "*.jsx", "*.tsx")
    "Config-Files" = @("*.json", "*.yaml", "*.yml", "*.toml", "*.ini", "*.conf")
    "Environment-Files" = @(".env", "*.env", ".env.*")
    "Credentials" = @("*secret*", "*credential*", "*password*", "*key*")
    "Docker-Files" = @("Dockerfile", "docker-compose.yml", "*.dockerfile")
    "Database-Files" = @("*.db", "*.sqlite", "*.sql")
    "Archive-Files" = @("*.zip", "*.tar", "*.gz", "*.7z", "*.rar")
    "Media-Files" = @("*.png", "*.jpg", "*.jpeg", "*.gif", "*.mp4", "*.mov")
}

# Function to check if file should be excluded
function Test-Excluded {
    param([string]$Path)
    
    foreach ($pattern in $ExcludePatterns) {
        if ($Path -like "*$pattern*") {
            return $true
        }
    }
    return $false
}

# Function to categorize file
function Get-FileCategory {
    param([string]$FileName, [string]$FullPath)
    
    foreach ($category in $categoryRules.Keys) {
        foreach ($pattern in $categoryRules[$category]) {
            if ($FileName -like $pattern -or $FullPath -like "*$pattern*") {
                return $category
            }
        }
    }
    return "Other"
}

# Function to determine Dropbox destination
function Get-DropboxDestination {
    param([string]$Category, [string]$RelativePath)
    
    switch ($Category) {
        "Documentation" { 
            return "04_Documentation/GenX_FX-Docs/$RelativePath"
        }
        "Scripts-PowerShell" { 
            return "03_Automation-Scripts/powershell/$RelativePath"
        }
        "Scripts-Shell" { 
            return "03_Automation-Scripts/bash/$RelativePath"
        }
        "Scripts-Batch" { 
            return "03_Automation-Scripts/powershell/$RelativePath"
        }
        "Python-Source" { 
            if ($RelativePath -match "test|spec") {
                return "01_Projects/GenX_FX/tests/$RelativePath"
            } else {
                return "01_Projects/GenX_FX/src/$RelativePath"
            }
        }
        "JavaScript-Source" { 
            return "01_Projects/ProductionApp/src/$RelativePath"
        }
        "Config-Files" { 
            if ($RelativePath -match "docker") {
                return "01_Projects/GenX_FX/docker/$RelativePath"
            } else {
                return "01_Projects/GenX_FX/configs/$RelativePath"
            }
        }
        "Environment-Files" { 
            return "02_Secure-Credentials/ENV-Files-Encrypted/$RelativePath"
        }
        "Credentials" { 
            return "02_Secure-Credentials/Encrypted/$RelativePath"
        }
        "Docker-Files" { 
            return "01_Projects/GenX_FX/docker/$RelativePath"
        }
        "Database-Files" { 
            return "05_Backups/Database-Backups/$RelativePath"
        }
        "Archive-Files" { 
            return "06_Archive/Old-Archives/$RelativePath"
        }
        "Media-Files" { 
            return "07_Personal/Media/$RelativePath"
        }
        default { 
            return "01_Projects/GenX_FX/misc/$RelativePath"
        }
    }
}

# Function to format file size
function Format-FileSize {
    param([long]$Size)
    
    if ($Size -gt 1GB) {
        return "{0:N2} GB" -f ($Size / 1GB)
    } elseif ($Size -gt 1MB) {
        return "{0:N2} MB" -f ($Size / 1MB)
    } elseif ($Size -gt 1KB) {
        return "{0:N2} KB" -f ($Size / 1KB)
    } else {
        return "$Size bytes"
    }
}

Write-Host "📊 Scanning files..." -ForegroundColor Yellow

# Scan all files
$files = Get-ChildItem -Path $SourcePath -Recurse -File -ErrorAction SilentlyContinue

$progress = 0
$totalFiles = $files.Count

foreach ($file in $files) {
    $progress++
    
    # Skip excluded files
    if (Test-Excluded -Path $file.FullName) {
        continue
    }
    
    # Update progress
    if ($progress % 100 -eq 0) {
        Write-Progress -Activity "Analyzing Files" -Status "$progress of $totalFiles" -PercentComplete (($progress / $totalFiles) * 100)
    }
    
    # Get file info
    $relativePath = $file.FullName.Substring($SourcePath.Length).TrimStart('\', '/')
    $category = Get-FileCategory -FileName $file.Name -FullPath $file.FullName
    $dropboxDest = Get-DropboxDestination -Category $category -RelativePath $relativePath
    
    # Update statistics
    $analysis.TotalFiles++
    $analysis.TotalSize += $file.Length
    
    # Count by category
    if (-not $analysis.Categories.ContainsKey($category)) {
        $analysis.Categories[$category] = @{
            Count = 0
            Size = 0
            Files = @()
        }
    }
    $analysis.Categories[$category].Count++
    $analysis.Categories[$category].Size += $file.Length
    $analysis.Categories[$category].Files += $file
    
    # Count by file type
    $ext = $file.Extension.ToLower()
    if ($ext) {
        if (-not $analysis.FileTypes.ContainsKey($ext)) {
            $analysis.FileTypes[$ext] = @{
                Count = 0
                Size = 0
            }
        }
        $analysis.FileTypes[$ext].Count++
        $analysis.FileTypes[$ext].Size += $file.Length
    }
    
    # Track large files (> 10 MB)
    if ($file.Length -gt 10MB) {
        $analysis.LargeFiles += [PSCustomObject]@{
            Name = $file.Name
            Path = $relativePath
            Size = $file.Length
            SizeFormatted = Format-FileSize -Size $file.Length
        }
    }
    
    # Add to mapping
    $analysis.Mappings += [PSCustomObject]@{
        SourcePath = $relativePath
        Category = $category
        DropboxDestination = $dropboxDest
        Size = $file.Length
        SizeFormatted = Format-FileSize -Size $file.Length
    }
}

Write-Progress -Activity "Analyzing Files" -Completed

Write-Host "✅ Scan completed!" -ForegroundColor Green
Write-Host ""

# Generate Summary Report
$summaryReport = @"
# 📊 Dropbox Migration Analysis Report

**Generated:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Source Path:** $SourcePath
**Total Files Analyzed:** $($analysis.TotalFiles)
**Total Size:** $(Format-FileSize -Size $analysis.TotalSize)

---

## 📁 Files by Category

| Category | Count | Total Size | Avg Size | Dropbox Destination |
|----------|-------|------------|----------|---------------------|
"@

foreach ($category in ($analysis.Categories.Keys | Sort-Object)) {
    $catData = $analysis.Categories[$category]
    $avgSize = if ($catData.Count -gt 0) { $catData.Size / $catData.Count } else { 0 }
    $destination = switch ($category) {
        "Documentation" { "04_Documentation/" }
        "Scripts-PowerShell" { "03_Automation-Scripts/powershell/" }
        "Scripts-Shell" { "03_Automation-Scripts/bash/" }
        "Scripts-Batch" { "03_Automation-Scripts/powershell/" }
        "Python-Source" { "01_Projects/GenX_FX/src/" }
        "Credentials" { "02_Secure-Credentials/" }
        default { "01_Projects/GenX_FX/" }
    }
    
    $summaryReport += "`n| $category | $($catData.Count) | $(Format-FileSize -Size $catData.Size) | $(Format-FileSize -Size $avgSize) | $destination |"
}

$summaryReport += @"


---

## 📈 Top File Types

| Extension | Count | Total Size |
|-----------|-------|------------|
"@

foreach ($ext in ($analysis.FileTypes.Keys | Sort-Object { $analysis.FileTypes[$_].Size } -Descending | Select-Object -First 10)) {
    $extData = $analysis.FileTypes[$ext]
    $summaryReport += "`n| $ext | $($extData.Count) | $(Format-FileSize -Size $extData.Size) |"
}

$summaryReport += @"


---

## 🚨 Large Files (> 10 MB)

| File | Path | Size |
|------|------|------|
"@

foreach ($file in ($analysis.LargeFiles | Sort-Object Size -Descending | Select-Object -First 20)) {
    $summaryReport += "`n| $($file.Name) | $($file.Path) | $($file.SizeFormatted) |"
}

$summaryReport += @"


---

## 🔐 Security Considerations

### Files Requiring Encryption
"@

$credentialFiles = $analysis.Mappings | Where-Object { $_.Category -eq "Credentials" -or $_.Category -eq "Environment-Files" }
if ($credentialFiles) {
    $summaryReport += "`n"
    foreach ($file in $credentialFiles) {
        $summaryReport += "`n- ⚠️ ``$($file.SourcePath)`` → Must be encrypted before moving to ``$($file.DropboxDestination)``"
    }
} else {
    $summaryReport += "`n- ✅ No credential files found"
}

$summaryReport += @"


---

## 📋 Recommendations

### Files to Sync Locally
- Documentation files (frequent reference)
- Active scripts (daily use)
- Current project files

### Files to Keep Online-Only
- Large media files
- Old backups
- Archive files
- Historical logs

### Files to Exclude
- node_modules/ directories
- Virtual environments (venv/)
- Compiled files (*.pyc, *.exe)
- Temporary files (*.tmp, *.log)
- IDE settings (.idea/, .vscode/)

---

## 🎯 Next Steps

1. **Review this report** to understand your current file distribution
2. **Run Create-DropboxStructure.ps1** to create the Dropbox folder structure
3. **Run Migrate-ToDropbox.ps1** to perform the migration
4. **Verify** all files are in correct locations
5. **Configure selective sync** based on recommendations
6. **Set up backup automation** using provided scripts

---

*Generated by Analyze-DriveForDropbox.ps1*
"@

# Save summary report
$summaryPath = Join-Path $OutputPath "01-Analysis-Summary.md"
$summaryReport | Out-File -FilePath $summaryPath -Encoding UTF8
Write-Host "📄 Summary report saved: $summaryPath" -ForegroundColor Green

# Generate detailed mapping CSV
$mappingPath = Join-Path $OutputPath "02-File-Mapping.csv"
$analysis.Mappings | Export-Csv -Path $mappingPath -NoTypeInformation -Encoding UTF8
Write-Host "📄 File mapping saved: $mappingPath" -ForegroundColor Green

# Generate category breakdown
$categoryPath = Join-Path $OutputPath "03-Category-Breakdown.json"
$analysis.Categories | ConvertTo-Json -Depth 3 | Out-File -FilePath $categoryPath -Encoding UTF8
Write-Host "📄 Category breakdown saved: $categoryPath" -ForegroundColor Green

# Generate migration script
$migrationScriptPath = Join-Path $OutputPath "04-Migration-Commands.ps1"
$migrationScript = @"
# Auto-generated migration commands
# Review before executing!

# WARNING: Review all paths before running this script!
# This script is generated automatically and should be reviewed carefully.

`$dropboxBase = "`$env:USERPROFILE\Dropbox"

Write-Host "🚀 Starting Dropbox Migration" -ForegroundColor Cyan
Write-Host "Source: $SourcePath" -ForegroundColor Gray
Write-Host "Destination: `$dropboxBase" -ForegroundColor Gray
Write-Host ""

# Create destination folders
Write-Host "📁 Creating folder structure..." -ForegroundColor Yellow

"@

# Add folder creation commands
$uniqueFolders = @{}
foreach ($mapping in $analysis.Mappings) {
    $folder = Split-Path -Parent $mapping.DropboxDestination
    if ($folder -and -not $uniqueFolders.ContainsKey($folder)) {
        $uniqueFolders[$folder] = $true
        $migrationScript += "`nNew-Item -Path (Join-Path `$dropboxBase '$folder') -ItemType Directory -Force | Out-Null"
    }
}

$migrationScript += @"


# Copy files (review and uncomment to execute)
Write-Host "`n📦 Ready to copy files..." -ForegroundColor Yellow
Write-Host "⚠️  Review the commands below and uncomment to execute" -ForegroundColor Red
Write-Host ""

"@

# Add file copy commands (commented out for safety)
foreach ($mapping in ($analysis.Mappings | Select-Object -First 50)) {
    $sourcePath = Join-Path $SourcePath $mapping.SourcePath
    $destPath = "`$dropboxBase\$($mapping.DropboxDestination)"
    $migrationScript += "`n# Copy-Item -Path '$sourcePath' -Destination '$destPath' -Force"
}

$migrationScript += @"


Write-Host "`n✅ Review completed. Uncomment copy commands to execute migration." -ForegroundColor Green
Write-Host "⚠️  Remember to encrypt credential files before copying!" -ForegroundColor Yellow
"@

$migrationScript | Out-File -FilePath $migrationScriptPath -Encoding UTF8
Write-Host "📄 Migration script saved: $migrationScriptPath" -ForegroundColor Green

Write-Host ""
Write-Host "✨ Analysis Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Results:" -ForegroundColor Cyan
Write-Host "  - $($analysis.TotalFiles) files analyzed"
Write-Host "  - $(Format-FileSize -Size $analysis.TotalSize) total size"
Write-Host "  - $($analysis.Categories.Count) categories identified"
Write-Host "  - $($analysis.LargeFiles.Count) large files found"
Write-Host ""
Write-Host "📁 Generated Reports:" -ForegroundColor Cyan
Write-Host "  1. $summaryPath"
Write-Host "  2. $mappingPath"
Write-Host "  3. $categoryPath"
Write-Host "  4. $migrationScriptPath"
Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Review the analysis summary"
Write-Host "  2. Run Create-DropboxStructure.ps1 to create folders"
Write-Host "  3. Review and customize migration commands"
Write-Host "  4. Execute migration in phases"
Write-Host ""
