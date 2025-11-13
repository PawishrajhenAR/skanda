# Credit Management System - PowerShell Startup Script
# This script ensures the application runs using venv on port 5000

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Credit Management System - Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create venv first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  venv\Scripts\activate" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Check if running from correct directory
if (-not (Test-Path "app.py")) {
    Write-Host "ERROR: app.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the project directory." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Kill any existing processes on port 5000
Write-Host "Checking for processes on port 5000..." -ForegroundColor Yellow
$processes = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Where-Object {$_.State -eq "Listen"}
if ($processes) {
    foreach ($conn in $processes) {
        Write-Host "Killing process $($conn.OwningProcess) on port 5000..." -ForegroundColor Yellow
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Credit Management System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Application will be available at: http://localhost:5000" -ForegroundColor Green
Write-Host "Default login credentials:" -ForegroundColor Yellow
Write-Host "  Username: admin" -ForegroundColor Yellow
Write-Host "  Password: admin123" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Run the application using venv Python
python app.py

Read-Host "Press Enter to exit"

