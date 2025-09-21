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

:: Upgrade pip first
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet

:: Install/upgrade requirements
echo [INFO] Installing requirements...
echo [INFO] This may take a few minutes for first-time setup...
pip install -r requirements_app.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    echo [INFO] Trying with verbose output...
    pip install -r requirements_app.txt
    pause
    exit /b 1
)

:: Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found
    echo Please create .env file with your API keys
    echo See .env.example for reference
    echo.
    echo Example .env content:
    echo OPENAI_API_KEY=your_openai_api_key_here
    echo OPENAI_BASE_URL=https://api.openai.com/v1
    echo.
    pause
)

:: Create necessary directories
echo [INFO] Creating data directories...
if not exist "data" mkdir data
if not exist "data\input" mkdir data\input
if not exist "data\processed" mkdir data\processed
if not exist "data\output" mkdir data\output
if not exist "data\backup" mkdir data\backup
if not exist "logs" mkdir logs

:: Start the application
echo [INFO] Starting Tender Processing System...
echo [INFO] The application will open in your default browser
echo [INFO] Press Ctrl+C to stop the application
echo.
echo ========================================
echo    Application Starting...
echo ========================================
echo.

python run_app.py

:: Deactivate virtual environment
deactivate

echo.
echo ========================================
echo    Application stopped.
echo ========================================
pause