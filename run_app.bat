@echo off
echo Starting Candidate Elimination Algorithm Tool...

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Change to application directory
cd /d "%~dp0"

REM Check and install dependencies if needed
echo Checking dependencies...
python -c "import pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pandas...
    python -m pip install pandas
)

python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing tkinter...
    python -m pip install tk
)

REM Run the application
echo Launching application...
python app.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)