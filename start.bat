@echo off
REM Start EarthLens development servers on Windows

setlocal enabledelayedexpansion

echo.
echo *** EarthLens Startup Script ***
echo.

set "ROOT=%~dp0"

echo Setting up backend...
cd /d "%ROOT%backend"

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

if not exist ".env" (
    copy .env.example .env
    echo Created .env file
)

echo Installing backend dependencies...
pip install -q -r requirements.txt

if errorlevel 1 (
    echo Failed to install backend dependencies
    pause
    exit /b 1
)

echo Backend ready
echo.

echo Setting up frontend...
cd /d "%ROOT%frontend"

if not exist ".env" (
    copy .env.example .env
    echo Created .env file
)

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
) else (
    echo Frontend dependencies already installed
)

echo Frontend ready
echo.

echo.
echo Launching EarthLens...
echo.
echo Backend starting on http://localhost:8000
echo Frontend starting on http://localhost:5173
echo.
echo Press Ctrl+C in each terminal to stop
echo.

echo Starting backend...
start "EarthLens Backend" cmd /k "cd /d %ROOT%backend && call .venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo Starting frontend...
cd /d "%ROOT%frontend"
start "EarthLens Frontend" cmd /k "npm run dev -- --host 0.0.0.0 --port 5173"

echo.
echo EarthLens is launching! Check the terminal windows.
echo.
pause
