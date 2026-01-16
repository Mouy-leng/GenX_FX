# Create-DropboxStructure.ps1
# Creates the complete Dropbox folder structure based on the blueprint

<#
.SYNOPSIS
    Creates the complete Dropbox folder structure for GenX_FX organization.

.DESCRIPTION
    This script creates all folders defined in the Dropbox Organization Blueprint.
    It sets up the complete directory structure ready for file migration.

.PARAMETER DropboxPath
    Path to Dropbox folder (defaults to %USERPROFILE%\Dropbox)

.PARAMETER DryRun
    If specified, shows what would be created without actually creating folders

.EXAMPLE
    .\Create-DropboxStructure.ps1
    Creates structure in default Dropbox location

.EXAMPLE
    .\Create-DropboxStructure.ps1 -DropboxPath "D:\Dropbox"
    Creates structure in custom Dropbox location

.EXAMPLE
    .\Create-DropboxStructure.ps1 -DryRun
    Shows what would be created without making changes

.NOTES
    Author: A6-9V GenX_FX System
    Version: 1.0
    Last Updated: 2026-01-06
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$DropboxPath = (Join-Path $env:USERPROFILE "Dropbox"),

    [Parameter(Mandatory=$false)]
    [switch]$DryRun
)

Write-Host "🗂️  Creating Dropbox Folder Structure" -ForegroundColor Cyan
Write-Host "Location: $DropboxPath" -ForegroundColor Gray
if ($DryRun) {
    Write-Host "Mode: DRY RUN (no changes will be made)" -ForegroundColor Yellow
}
Write-Host ""

# Define the complete folder structure
$folderStructure = @(
    # 00_System-Core
    "00_System-Core",
    "00_System-Core/Environment-Variables-Templates",
    "00_System-Core/API-Key-Placeholders",
    "00_System-Core/Architecture-Diagrams",
    "00_System-Core/Global-Configs",
    "00_System-Core/Security-Policies",

    # 01_Projects
    "01_Projects",
    "01_Projects/GenX_FX",
    "01_Projects/GenX_FX/src",
    "01_Projects/GenX_FX/ml_pipeline",
    "01_Projects/GenX_FX/docker",
    "01_Projects/GenX_FX/configs",
    "01_Projects/GenX_FX/logs",
    "01_Projects/GenX_FX/docs",
    "01_Projects/GenX_FX/tests",
    "01_Projects/GenX_FX/deployments",
    "01_Projects/ProductionApp",
    "01_Projects/Cloud-Automation",
    "01_Projects/Mobile-App",
    "01_Projects/Web-Services",

    # 02_Secure-Credentials
    "02_Secure-Credentials",
    "02_Secure-Credentials/VAPID-Keys",
    "02_Secure-Credentials/Broker-API-Keys",
    "02_Secure-Credentials/OAuth-Secrets",
    "02_Secure-Credentials/SSL-Certificates",
    "02_Secure-Credentials/Encrypted-Backups",
    "02_Secure-Credentials/ENV-Files-Encrypted",

    # 03_Automation-Scripts
    "03_Automation-Scripts",
    "03_Automation-Scripts/powershell",
    "03_Automation-Scripts/bash",
    "03_Automation-Scripts/monitoring",
    "03_Automation-Scripts/backup",
    "03_Automation-Scripts/deployment",
    "03_Automation-Scripts/restore",

    # 04_Documentation
    "04_Documentation",
    "04_Documentation/Startup-Guides",
    "04_Documentation/System-Diagrams",
    "04_Documentation/Troubleshooting",
    "04_Documentation/How-To-Deploy",
    "04_Documentation/Cloud-Setup-Notes",
    "04_Documentation/CI-CD-Notes",
    "04_Documentation/GenX_FX-Docs",

    # 05_Backups
    "05_Backups",
    "05_Backups/Database-Backups",
    "05_Backups/Database-Backups/Daily",
    "05_Backups/Database-Backups/Weekly",
    "05_Backups/Database-Backups/Monthly",
    "05_Backups/Config-Snapshots",
    "05_Backups/Config-Snapshots/trading-configs",
    "05_Backups/Config-Snapshots/server-configs",
    "05_Backups/Config-Snapshots/app-configs",
    "05_Backups/Project-Archives",
    "05_Backups/VPS-Images",
    "05_Backups/VPS-Images/server-configs",
    "05_Backups/VPS-Images/firewall-rules",
    "05_Backups/Monitoring-Data",

    # 06_Archive
    "06_Archive",
    "06_Archive/Old-Projects",
    "06_Archive/Legacy-Configs",
    "06_Archive/Unused-Scripts",
    "06_Archive/Historical-Logs",

    # 07_Personal
    "07_Personal",
    "07_Personal/Photos",
    "07_Personal/Videos",
    "07_Personal/Receipts",
    "07_Personal/Documents",

    # 08_Collaboration
    "08_Collaboration",
    "08_Collaboration/Shared-With-Clients",
    "08_Collaboration/Shared-With-Friends",
    "08_Collaboration/Temporary-Uploads",
    "08_Collaboration/Collab-Projects"
)

# Create README files for each top-level folder
$readmeContent = @{
    "00_System-Core" = @"
# 00_System-Core

**Purpose:** Foundation files that define your entire ecosystem

## Contents
- Environment variable templates
- API key placeholder documentation
- System architecture diagrams
- Global configuration templates
- Security policies and guidelines

## Sync Strategy
✅ Sync locally - Frequent reference needed

## Important
- No actual credentials should be stored here
- Only templates and placeholders
- Keep architecture diagrams up to date
"@

    "01_Projects" = @"
# 01_Projects

**Purpose:** All active development projects

## Contents
- GenX_FX trading system
- ProductionApp
- Other active projects

## Sync Strategy
🔀 Selective sync - Only active projects need to be local

## Organization
Each project should have its own subfolder with:
- src/ - Source code
- docs/ - Project documentation
- tests/ - Test files
- configs/ - Configuration files
"@

    "02_Secure-Credentials" = @"
# 02_Secure-Credentials

**Purpose:** Encrypted storage for all sensitive credentials

## ⚠️ SECURITY WARNING
ALL files in this folder MUST be encrypted before syncing!

## Sync Strategy
☁️ Online-only - For security and space management

## Encryption Requirements
1. Use password-protected ZIP or encrypted containers
2. Never store plain-text credentials
3. Use .encrypted suffix for encrypted files
4. Store encryption passwords in password manager
5. Enable 2FA on Dropbox account

## What Goes Here
- VAPID keys (encrypted)
- Broker API keys (encrypted)
- OAuth secrets (encrypted)
- SSL/TLS certificates (encrypted)
- Environment files (encrypted)
- Service account credentials (encrypted)
"@

    "03_Automation-Scripts" = @"
# 03_Automation-Scripts

**Purpose:** Your complete automation toolbox

## Contents
- PowerShell scripts
- Bash/Shell scripts
- Monitoring scripts
- Backup automation
- Deployment scripts
- Restore procedures

## Sync Strategy
✅ Sync locally - Daily use

## Organization
- powershell/ - Windows automation
- bash/ - Linux/Mac scripts
- monitoring/ - Health checks
- backup/ - Backup automation
- deployment/ - CI/CD scripts
- restore/ - Recovery scripts
"@

    "04_Documentation" = @"
# 04_Documentation

**Purpose:** All guides, READMEs, SOPs, and notes

## Contents
- Startup guides
- System architecture documentation
- Troubleshooting procedures
- Deployment instructions
- Cloud setup notes
- CI/CD documentation

## Sync Strategy
✅ Sync locally - Frequent reference

## Best Practices
- Keep documentation up to date
- Use markdown for consistency
- Include diagrams where helpful
- Maintain version history
"@

    "05_Backups" = @"
# 05_Backups

**Purpose:** Versioned backups with Dropbox history

## Sync Strategy
☁️ Online-only - Saves disk space

## Backup Schedule
- Daily: Database dumps, config snapshots
- Weekly: Full project archives, VPS configs
- Monthly: Complete system snapshots

## Retention Policy
- Daily: Keep last 7 days
- Weekly: Keep last 4 weeks
- Monthly: Keep last 12 months

## Important
- Test restore procedures regularly
- Verify backup integrity monthly
- Keep offline backup copy
- Document restore procedures
"@

    "06_Archive" = @"
# 06_Archive

**Purpose:** Old versions and deprecated content

## Sync Strategy
☁️ Online-only

## Contents
- Old project versions
- Deprecated code
- Historical logs
- Unused configuration files
- Legacy documentation

## Retention Policy
- Keep for 6-12 months
- Review quarterly
- Delete after team verification
"@

    "07_Personal" = @"
# 07_Personal

**Purpose:** Non-work files

## Sync Strategy
🔀 Selective sync - Based on needs

## Contents
- Personal photos and videos
- Financial documents
- Receipts and invoices
- Personal projects
- Learning materials
"@

    "08_Collaboration" = @"
# 08_Collaboration

**Purpose:** Shared workspaces

## Sync Strategy
🔀 Selective sync - Active collaborations only

## Contents
- Files shared with clients
- Team collaboration folders
- Temporary file exchanges
- Joint project workspaces

## Best Practices
- Set expiration on shared links
- Review access quarterly
- Clean up temporary files regularly
"@
}

# Statistics
$stats = @{
    Created = 0
    AlreadyExists = 0
    Failed = 0
}

# Create folders
Write-Host "📁 Creating folder structure..." -ForegroundColor Yellow
Write-Host ""

foreach ($folder in $folderStructure) {
    $fullPath = Join-Path $DropboxPath $folder

    if ($DryRun) {
        Write-Host "  [DRY RUN] Would create: $folder" -ForegroundColor Gray
        $stats.Created++
    }
    else {
        try {
            if (Test-Path $fullPath) {
                Write-Host "  ✓ Already exists: $folder" -ForegroundColor DarkGray
                $stats.AlreadyExists++
            }
            else {
                New-Item -Path $fullPath -ItemType Directory -Force | Out-Null
                Write-Host "  ✅ Created: $folder" -ForegroundColor Green
                $stats.Created++
            }
        }
        catch {
            Write-Host "  ❌ Failed: $folder - $($_.Exception.Message)" -ForegroundColor Red
            $stats.Failed++
        }
    }
}

# Create README files for top-level folders
if (-not $DryRun) {
    Write-Host ""
    Write-Host "📄 Creating README files..." -ForegroundColor Yellow

    foreach ($folderName in $readmeContent.Keys) {
        $readmePath = Join-Path $DropboxPath "$folderName\README.md"

        try {
            if (-not (Test-Path $readmePath)) {
                $readmeContent[$folderName] | Out-File -FilePath $readmePath -Encoding UTF8
                Write-Host "  ✅ Created README: $folderName\README.md" -ForegroundColor Green
            }
        }
        catch {
            Write-Host "  ⚠️  Could not create README: $folderName\README.md" -ForegroundColor Yellow
        }
    }
}

# Create .dropboxignore file
$dropboxIgnorePath = Join-Path $DropboxPath ".dropboxignore"
$dropboxIgnoreContent = @"
# Dropbox Ignore File
# Files and folders matching these patterns won't sync

# Development artifacts
node_modules/
venv/
__pycache__/
*.pyc
.pytest_cache/
.coverage

# Build outputs
dist/
build/
*.exe
*.dll
*.so
*.dylib

# IDE files
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# OS files
Thumbs.db
desktop.ini
$RECYCLE.BIN/

# Temporary files
*.tmp
*.temp
*.bak
~$*

# Large log files (keep important ones)
*.log

# Git repository (problematic with Dropbox)
.git/
.gitignore

# Database files (if they're being backed up separately)
# *.db
# *.sqlite

# Large media (unless essential)
# *.mp4
# *.mov
# *.avi
"@

if (-not $DryRun) {
    try {
        $dropboxIgnoreContent | Out-File -FilePath $dropboxIgnorePath -Encoding UTF8
        Write-Host "  ✅ Created .dropboxignore file" -ForegroundColor Green
    }
    catch {
        Write-Host "  ⚠️  Could not create .dropboxignore file" -ForegroundColor Yellow
    }
}

# Create main README
$mainReadmePath = Join-Path $DropboxPath "README-DROPBOX-STRUCTURE.md"
$mainReadmeContent = @"
# Dropbox Organization Structure

**Created:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**System:** A6-9V GenX_FX Trading Platform

## 📁 Folder Structure

This Dropbox is organized using the GenX_FX Organization Blueprint.

### Top-Level Folders

| Folder | Purpose | Sync Strategy |
|--------|---------|---------------|
| 00_System-Core | Foundation files and templates | ✅ Local |
| 01_Projects | Active development projects | 🔀 Selective |
| 02_Secure-Credentials | Encrypted credentials only | ☁️ Online |
| 03_Automation-Scripts | Automation toolbox | ✅ Local |
| 04_Documentation | Guides and documentation | ✅ Local |
| 05_Backups | Versioned backups | ☁️ Online |
| 06_Archive | Old and deprecated content | ☁️ Online |
| 07_Personal | Personal files | 🔀 Selective |
| 08_Collaboration | Shared workspaces | 🔀 Selective |

### Sync Strategy Legend
- ✅ Local = Always synced to device
- ☁️ Online = Cloud-only (saves space)
- 🔀 Selective = Choose specific folders

## 🔐 Security Notes

1. **Never** store plain-text credentials
2. All files in 02_Secure-Credentials MUST be encrypted
3. Enable 2FA on Dropbox account
4. Review shared folder access quarterly
5. Use .encrypted suffix for encrypted files

## 📚 Documentation

For complete documentation, see:
- DROPBOX_ORGANIZATION_BLUEPRINT.md (in GenX_FX repository)
- Individual README.md files in each top-level folder

## 🚀 Getting Started

1. Review each folder's README.md file
2. Configure selective sync based on your needs
3. Start migrating files from old structure
4. Set up backup automation
5. Test restore procedures

## 🎯 Next Steps

- [ ] Configure selective sync settings
- [ ] Migrate documentation files
- [ ] Migrate automation scripts
- [ ] Set up backup automation
- [ ] Encrypt and move credentials
- [ ] Test file access from all devices
- [ ] Clean up old file structure

---

*Generated by Create-DropboxStructure.ps1*
"@

if (-not $DryRun) {
    try {
        $mainReadmeContent | Out-File -FilePath $mainReadmePath -Encoding UTF8
        Write-Host "  ✅ Created main README" -ForegroundColor Green
    }
    catch {
        Write-Host "  ⚠️  Could not create main README" -ForegroundColor Yellow
    }
}

# Display summary
Write-Host ""
Write-Host "✨ Structure Creation Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Summary:" -ForegroundColor Cyan
Write-Host "  - Folders created: $($stats.Created)" -ForegroundColor Green
Write-Host "  - Already existed: $($stats.AlreadyExists)" -ForegroundColor Gray
if ($stats.Failed -gt 0) {
    Write-Host "  - Failed: $($stats.Failed)" -ForegroundColor Red
}
Write-Host ""

if ($DryRun) {
    Write-Host "🔍 This was a dry run. No changes were made." -ForegroundColor Yellow
    Write-Host "   Run without -DryRun flag to create the structure." -ForegroundColor Yellow
}
else {
    Write-Host "📁 Dropbox structure created at:" -ForegroundColor Cyan
    Write-Host "   $DropboxPath" -ForegroundColor White
    Write-Host ""
    Write-Host "🎯 Next Steps:" -ForegroundColor Yellow
    Write-Host "   1. Review the created folder structure"
    Write-Host "   2. Read README files in each top-level folder"
    Write-Host "   3. Run Analyze-DriveForDropbox.ps1 to analyze current files"
    Write-Host "   4. Run Migrate-ToDropbox.ps1 to start migration"
    Write-Host "   5. Configure Dropbox selective sync"
    Write-Host ""
    Write-Host "📚 Documentation:" -ForegroundColor Cyan
    Write-Host "   - Main README: README-DROPBOX-STRUCTURE.md"
    Write-Host "   - Complete guide: DROPBOX_ORGANIZATION_BLUEPRINT.md"
    Write-Host "   - Ignore rules: .dropboxignore"
}
Write-Host ""
