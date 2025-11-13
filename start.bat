@echo off
REM Credit Management System - Startup Script
REM This script ensures the application runs using venv on port 5000

echo ========================================
echo Credit Management System - Startup
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please create venv first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if running from correct directory
if not exist "app.py" (
    echo ERROR: app.py not found!
    echo Please run this script from the project directory.
    pause
    exit /b 1
)

REM Kill any existing processes on port 5000
echo Checking for processes on port 5000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    echo Killing process %%a on port 5000...
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo ========================================
echo Starting Credit Management System
echo ========================================
echo.
echo Application will be available at: http://localhost:5000
echo Default login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the application
echo ========================================
echo.

REM Run the application using venv Python
python app.py

pause

