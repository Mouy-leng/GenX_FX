# GenX_FX Scripts

This directory contains utility scripts for the GenX_FX project.

## Cloud Sync Scripts

### sync_to_clouds.bat (Windows Batch)
Syncs the GenX_FX project to multiple cloud providers (Dropbox, Google Drive, OneDrive) using rclone.

**Usage:**
```batch
cd scripts
sync_to_clouds.bat
```

### sync_to_clouds.ps1 (PowerShell)
PowerShell version of the cloud sync script with enhanced error handling and colored output.

**Usage:**
```powershell
cd scripts
.\sync_to_clouds.ps1
```

**Prerequisites for Cloud Sync:**
1. Install rclone from https://rclone.org/downloads/
2. Configure rclone remotes using `rclone config`
3. Create three remotes named:
   - `remote_dropbox` (for Dropbox)
   - `remote_gdrive` (for Google Drive)
   - `remote_onedrive` (for OneDrive)

For detailed setup instructions, see: [../docs/CLOUD_SYNC_AND_SEO_GUIDE.md](../docs/CLOUD_SYNC_AND_SEO_GUIDE.md)

## Other Scripts

### bootstrap.ps1
Bootstrap script for initial project setup.

### convert-to-submodules.ps1
Utility script for converting directories to Git submodules.

### .env.sample
Sample environment variables file. Copy to `.env` and configure for your environment.

## IntelliJ Scripts

The `intellij/` directory contains scripts for IntelliJ IDEA optimization and configuration.
