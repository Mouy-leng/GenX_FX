@echo off
REM GenX_FX Repository Launch Script for Cloned Branch
REM Organization: A6-9V
REM Purpose: Quick launch script for the copilot/launch-repository-clone branch

title GenX_FX Repository Launcher - Cloned Branch
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🚀 GenX_FX Repository Launcher                 ║
echo ║              Launch on Cloned Branch (Windows)              ║
echo ║                    Organization: A6-9V                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Step 1: Verify git repository
echo [INFO] Step 1: Verifying Git repository...
if not exist ".git" (
    echo [ERROR] Not a Git repository. Please run this script from the GenX_FX root directory.
    pause
    exit /b 1
)
echo [OK] Git repository detected
echo.

REM Step 2: Check current branch
echo [INFO] Step 2: Checking current branch...
for /f "tokens=*" %%i in ('git branch --show-current') do set CURRENT_BRANCH=%%i
echo Current branch: %CURRENT_BRANCH%

if not "%CURRENT_BRANCH%"=="copilot/launch-repository-clone" (
    echo [WARNING] Not on the expected branch.
    set /p CHECKOUT="Do you want to checkout copilot/launch-repository-clone? (y/n): "
    if /i "%CHECKOUT%"=="y" (
        git checkout copilot/launch-repository-clone
        echo [OK] Switched to copilot/launch-repository-clone branch
    )
) else (
    echo [OK] Already on copilot/launch-repository-clone branch
)
echo.

REM Step 3: Verify repository structure
echo [INFO] Step 3: Verifying repository structure...
set MISSING_FILES=0

if exist "A6-9V_Master_System_README.md" (
    echo [✓] Found: A6-9V_Master_System_README.md
) else (
    echo [✗] Missing: A6-9V_Master_System_README.md
    set /a MISSING_FILES+=1
)

if exist "README-local.md" (
    echo [✓] Found: README-local.md
) else (
    echo [✗] Missing: README-local.md
    set /a MISSING_FILES+=1
)

if exist "A6-9V_Enhanced_Master_Launcher.bat" (
    echo [✓] Found: A6-9V_Enhanced_Master_Launcher.bat
) else (
    echo [✗] Missing: A6-9V_Enhanced_Master_Launcher.bat
    set /a MISSING_FILES+=1
)

if exist "REPOSITORY_LAUNCH_GUIDE.md" (
    echo [✓] Found: REPOSITORY_LAUNCH_GUIDE.md
) else (
    echo [✗] Missing: REPOSITORY_LAUNCH_GUIDE.md
    set /a MISSING_FILES+=1
)

if exist "MT_AutoLogin_Fixed.ps1" (
    echo [✓] Found: MT_AutoLogin_Fixed.ps1
) else (
    echo [✗] Missing: MT_AutoLogin_Fixed.ps1
    set /a MISSING_FILES+=1
)

if exist "Enable_MT_AutoTrading.ps1" (
    echo [✓] Found: Enable_MT_AutoTrading.ps1
) else (
    echo [✗] Missing: Enable_MT_AutoTrading.ps1
    set /a MISSING_FILES+=1
)
echo.

REM Step 4: Check Python environment
echo [INFO] Step 4: Checking Python environment...
python --version >nul 2>&1
if %errorlevel%==0 (
    for /f "tokens=*" %%i in ('python --version') do echo [OK] Python detected: %%i
) else (
    echo [WARNING] Python not found in PATH
)
echo.

REM Step 5: Check virtual environment
echo [INFO] Step 5: Checking virtual environment...
if exist "A6-9V\Trading\GenX_FX\venv" (
    echo [OK] Virtual environment found at A6-9V\Trading\GenX_FX\venv
) else (
    echo [WARNING] Virtual environment not found
    echo [INFO] You may need to create it manually
)
echo.

REM Step 6: Display configuration summary
echo [INFO] Step 6: Configuration Summary
echo ════════════════════════════════════════════════════════════════
echo Repository: Mouy-leng/GenX_FX
echo Branch: %CURRENT_BRANCH%
echo Working Directory: %CD%
echo Git Status:
git status --short
echo.

REM Step 7: Display next steps
echo [SUCCESS] Repository verification complete!
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Next Steps:
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 📖 For detailed instructions, read:
echo    • REPOSITORY_LAUNCH_GUIDE.md - Complete launch guide
echo    • A6-9V_Master_System_README.md - System overview
echo    • README-local.md - Local workspace information
echo.
echo 🚀 Launch Options:
echo    1. Full System Launch (Recommended):
echo       A6-9V_Enhanced_Master_Launcher.bat
echo.
echo    2. MT5 Platform Only:
echo       Start MetaTrader 5 EXNESS manually
echo       Run: powershell -ExecutionPolicy Bypass -File "MT_AutoLogin_Fixed.ps1" -Platform mt5
echo.
echo    3. Enable Expert Advisors:
echo       powershell -ExecutionPolicy Bypass -File "Enable_MT_AutoTrading.ps1"
echo.
echo 🤖 MT5 Trading Platform Setup:
echo    • Account: Exness-MT5Trial8 (Demo)
echo    • Login: 279260115
echo    • Server: Exness-MT5Trail8
echo    • Balance: 39,499.31 USD
echo.
echo 📊 Expert Advisors Available:
echo    • ExpertMAPSAR_Enhanced
echo    • ExpertMACD
echo    • ExpertMAMA
echo    • ExpertMAPSAR
echo    • ExpertMAPSARSizeOptimized
echo    • bridges3rd
echo    • Advisors_backup_20251226_235613
echo.
echo 💹 Market Watch Symbols:
echo    • XAUUSD, BTCUSD, EURUSD, USDJPY, ETHUSD
echo    • BTCCNH, BTCXAU, BTCZAR
echo    • GBPJPY, GBPUSD, USDARS, USDCAD, USDCHF
echo.
echo 🔗 Additional Resources:
echo    • Code With Me: https://code-with-me.global.jetbrains.com/ZhaX8frcoZS0qveUMv8vAg
echo    • Documentation: docs\README.md
echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🎯 A6-9V GenX_FX Repository Ready for Launch!
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Ask user what they want to do
echo What would you like to do?
echo.
echo [1] Launch Full System (MT5 + Python + Development Environment)
echo [2] Launch MT5 Platform Only
echo [3] View Launch Guide
echo [4] Exit
echo.
set /p CHOICE="Enter your choice (1-4): "

if "%CHOICE%"=="1" (
    echo.
    echo [INFO] Launching full A6-9V system...
    call A6-9V_Enhanced_Master_Launcher.bat
) else if "%CHOICE%"=="2" (
    echo.
    echo [INFO] Launching MT5 platform...
    if exist "C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe" (
        start "MT5-EXNESS" "C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe" /portable
        timeout /t 5 /nobreak >nul
        powershell -ExecutionPolicy Bypass -File "MT_AutoLogin_Fixed.ps1" -Platform mt5
    ) else (
        echo [ERROR] MT5 EXNESS not found at standard location
        echo Please launch MT5 manually and then run:
        echo powershell -ExecutionPolicy Bypass -File "MT_AutoLogin_Fixed.ps1" -Platform mt5
    )
) else if "%CHOICE%"=="3" (
    echo.
    echo [INFO] Opening launch guide...
    if exist "REPOSITORY_LAUNCH_GUIDE.md" (
        type REPOSITORY_LAUNCH_GUIDE.md | more
    ) else (
        echo [ERROR] REPOSITORY_LAUNCH_GUIDE.md not found
    )
) else if "%CHOICE%"=="4" (
    echo.
    echo Exiting...
    exit /b 0
) else (
    echo.
    echo [ERROR] Invalid choice. Exiting...
)

echo.
pause
