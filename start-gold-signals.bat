@echo off
echo 🥇 GenX FX Gold Signal Generator
echo ================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Install required packages
echo 📦 Installing dependencies...
pip install requests fastapi uvicorn google-generativeai
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Load environment variables from .env file
if not exist .env (
    echo ❌ .env file not found. Please create one from .env.example and fill in your credentials.
    pause
    exit /b 1
)

echo 🔑 Loading environment variables from .env...
for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
    set "%%a=%%b"
)

REM Create logs directory
if not exist "logs" mkdir logs

REM Start the gold signal generator
echo 🚀 Starting Gold Signal Generator...
echo.
echo 📊 Features:
echo   • Gold pairs: XAUUSD, XAUEUR, XAUGBP, XAUAUD
echo   • AI-powered analysis with Gemini
echo   • VPS integration: http://34.71.143.222:8080
echo   • Local API: http://localhost:8080
echo   • Signal interval: 30 seconds
echo   • Min confidence: 75%%
echo.
echo 📡 Output:
echo   • MT4_Signals.csv (for EA consumption)
echo   • VPS API endpoint
echo   • Local API endpoint
echo.
echo Press Ctrl+C to stop
echo ================================
echo.

python gold-signal-generator.py

echo.
echo 🛑 Gold Signal Generator stopped
pause
