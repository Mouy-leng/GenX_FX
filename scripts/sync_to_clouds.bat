@echo off
REM ============================================
REM GenX_FX Cloud Sync Script
REM ============================================
REM This script syncs the GenX_FX project to multiple cloud providers
REM using rclone. It excludes large folders like .git, node_modules, and .venv
REM to save bandwidth and storage space.
REM
REM Prerequisites:
REM 1. Install rclone (https://rclone.org/downloads/)
REM 2. Configure remotes using 'rclone config'
REM 3. Set up remotes named: remote_dropbox, remote_gdrive, remote_onedrive
REM
REM For detailed setup instructions, see:
REM docs/CLOUD_SYNC_AND_SEO_GUIDE.md
REM ============================================

echo.
echo ============================================
echo   GenX_FX Cloud Sync Script
echo ============================================
echo.

REM Set the project path (modify if needed)
set PROJECT_PATH=%~dp0..
set PROJECT_NAME=GenX_FX
set CLOUD_BASE_PATH=/A6-9V/Projects

echo Project Path: %PROJECT_PATH%
echo Cloud Base Path: %CLOUD_BASE_PATH%
echo.

REM Check if rclone is installed
where rclone >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: rclone is not installed or not in PATH
    echo Please install rclone from https://rclone.org/downloads/
    echo.
    pause
    exit /b 1
)

echo rclone found!
echo.

REM Sync to Dropbox
echo ============================================
echo Syncing to Dropbox...
echo ============================================
rclone sync "%PROJECT_PATH%" remote_dropbox:%CLOUD_BASE_PATH%/%PROJECT_NAME% ^
    --progress ^
    --exclude ".git/**" ^
    --exclude "node_modules/**" ^
    --exclude ".venv/**" ^
    --exclude "venv/**" ^
    --exclude "__pycache__/**" ^
    --exclude "*.pyc" ^
    --exclude ".idea/**" ^
    --exclude "target/**" ^
    --exclude "build/**" ^
    --exclude "dist/**"

if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Dropbox sync failed or incomplete
) else (
    echo Dropbox sync completed successfully!
)
echo.

REM Sync to Google Drive
echo ============================================
echo Syncing to Google Drive...
echo ============================================
rclone sync "%PROJECT_PATH%" remote_gdrive:%CLOUD_BASE_PATH%/%PROJECT_NAME% ^
    --progress ^
    --exclude ".git/**" ^
    --exclude "node_modules/**" ^
    --exclude ".venv/**" ^
    --exclude "venv/**" ^
    --exclude "__pycache__/**" ^
    --exclude "*.pyc" ^
    --exclude ".idea/**" ^
    --exclude "target/**" ^
    --exclude "build/**" ^
    --exclude "dist/**"

if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Google Drive sync failed or incomplete
) else (
    echo Google Drive sync completed successfully!
)
echo.

REM Sync to OneDrive
echo ============================================
echo Syncing to OneDrive...
echo ============================================
rclone sync "%PROJECT_PATH%" remote_onedrive:%CLOUD_BASE_PATH%/%PROJECT_NAME% ^
    --progress ^
    --exclude ".git/**" ^
    --exclude "node_modules/**" ^
    --exclude ".venv/**" ^
    --exclude "venv/**" ^
    --exclude "__pycache__/**" ^
    --exclude "*.pyc" ^
    --exclude ".idea/**" ^
    --exclude "target/**" ^
    --exclude "build/**" ^
    --exclude "dist/**"

if %ERRORLEVEL% NEQ 0 (
    echo WARNING: OneDrive sync failed or incomplete
) else (
    echo OneDrive sync completed successfully!
)
echo.

echo ============================================
echo   Cloud Sync Complete!
echo ============================================
echo.
echo Your GenX_FX project has been synced to:
echo   - Dropbox: %CLOUD_BASE_PATH%/%PROJECT_NAME%
echo   - Google Drive: %CLOUD_BASE_PATH%/%PROJECT_NAME%
echo   - OneDrive: %CLOUD_BASE_PATH%/%PROJECT_NAME%
echo.
echo For more information, see: docs/CLOUD_SYNC_AND_SEO_GUIDE.md
echo.

pause
