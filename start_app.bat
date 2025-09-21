@echo off
echo ========================================
echo    Tender Processing System Launcher
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

:: Install/upgrade requirements
echo [INFO] Installing requirements...
pip install -r requirements_app.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

:: Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found
    echo Please create .env file with your API keys
    echo See .env.example for reference
    pause
)

:: Start the application
echo [INFO] Starting Tender Processing System...
echo [INFO] The application will open in your default browser
echo [INFO] Press Ctrl+C to stop the application
echo.
python run_app.py

:: Deactivate virtual environment
deactivate

echo.
echo Application stopped.
pause