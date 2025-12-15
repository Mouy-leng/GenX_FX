@echo off
title A6-9V Auto-Startup Installer
color 0B
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         🚀 A6-9V Auto-Startup Configuration Tool           ║
echo ║              Windows Startup Installation                   ║
echo ║                Organization: A6-9V                           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Get the current directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "VBS_FILE=%SCRIPT_DIR%A6-9V_Silent_Launcher.vbs"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_FILE=%STARTUP_FOLDER%\A6-9V_Trading_System.lnk"

echo [INFO] Current Directory: %SCRIPT_DIR%
echo [INFO] VBScript File: %VBS_FILE%
echo [INFO] Startup Folder: %STARTUP_FOLDER%
echo.

REM Check if VBScript file exists
if not exist "%VBS_FILE%" (
    echo [ERROR] A6-9V_Silent_Launcher.vbs not found!
    echo [ERROR] Please ensure this script is in the same folder as A6-9V_Silent_Launcher.vbs
    echo.
    pause
    exit /b 1
)

echo What would you like to do?
echo.
echo 1. Install Auto-Startup (Add to Windows Startup)
echo 2. Uninstall Auto-Startup (Remove from Windows Startup)
echo 3. Check Auto-Startup Status
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto UNINSTALL
if "%choice%"=="3" goto STATUS
if "%choice%"=="4" goto EXIT
echo [ERROR] Invalid choice. Please run the script again.
pause
exit /b 1

:INSTALL
echo.
echo ════════════════════════════════════════════════════════════════
echo Installing A6-9V Auto-Startup...
echo ════════════════════════════════════════════════════════════════
echo.

REM Check if shortcut already exists
if exist "%SHORTCUT_FILE%" (
    echo [WARNING] Auto-startup shortcut already exists!
    set /p overwrite="Do you want to overwrite it? (Y/N): "
    if /i not "%overwrite%"=="Y" (
        echo [INFO] Installation cancelled.
        goto END
    )
    echo [INFO] Removing existing shortcut...
    del "%SHORTCUT_FILE%"
)

REM Create shortcut using PowerShell
echo [INFO] Creating startup shortcut...
powershell -ExecutionPolicy Bypass -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_FILE%'); $Shortcut.TargetPath = '%VBS_FILE%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'A6-9V Enhanced Trading System Auto-Startup'; $Shortcut.Save()"

if exist "%SHORTCUT_FILE%" (
    echo.
    echo ✅ [SUCCESS] Auto-startup installed successfully!
    echo.
    echo The A6-9V Enhanced Master Trading System will now start automatically
    echo when you log into Windows.
    echo.
    echo Location: %SHORTCUT_FILE%
) else (
    echo.
    echo ❌ [ERROR] Failed to create startup shortcut!
    echo Please check permissions and try running as Administrator.
)
goto END

:UNINSTALL
echo.
echo ════════════════════════════════════════════════════════════════
echo Uninstalling A6-9V Auto-Startup...
echo ════════════════════════════════════════════════════════════════
echo.

if exist "%SHORTCUT_FILE%" (
    del "%SHORTCUT_FILE%"
    echo ✅ [SUCCESS] Auto-startup removed successfully!
    echo.
    echo The A6-9V Enhanced Master Trading System will no longer start
    echo automatically on Windows login.
) else (
    echo [INFO] No auto-startup shortcut found.
    echo The system is not currently configured for auto-startup.
)
goto END

:STATUS
echo.
echo ════════════════════════════════════════════════════════════════
echo Checking A6-9V Auto-Startup Status...
echo ════════════════════════════════════════════════════════════════
echo.

if exist "%SHORTCUT_FILE%" (
    echo ✅ Status: AUTO-STARTUP ENABLED
    echo.
    echo The A6-9V Enhanced Master Trading System is configured to start
    echo automatically when you log into Windows.
    echo.
    echo Shortcut Location: %SHORTCUT_FILE%
    echo VBScript Target: %VBS_FILE%
) else (
    echo ❌ Status: AUTO-STARTUP DISABLED
    echo.
    echo The A6-9V Enhanced Master Trading System is NOT configured for
    echo automatic startup.
    echo.
    echo Run this script and select option 1 to enable auto-startup.
)
goto END

:EXIT
echo.
echo Exiting...
exit /b 0

:END
echo.
echo ════════════════════════════════════════════════════════════════
echo.
pause
