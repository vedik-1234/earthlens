@echo off
REM EarthLens Complete Startup Script for Windows
REM Launches both backend and frontend with production settings

setlocal enabledelayedexpansion

echo 🌍 EarthLens v2.0 - Production Ready
echo =====================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3 is not installed or not in PATH
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python 3 found

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo    Download from: https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js found
echo.

REM Setup Backend
echo Setting up backend...
cd backend

if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo Initializing database...
python -c "from app.services.auth_service import init_db; init_db()"

echo ✅ Backend ready
echo.

REM Setup Frontend
echo Setting up frontend...
cd ..\frontend

if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install --silent
)

echo ✅ Frontend ready
echo.

REM Start services
echo Starting services...
echo.

echo Starting backend on http://0.0.0.0:8000...
start cmd /k "cd backend && .venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ✅ Backend started

REM Wait for backend to start
timeout /t 2 /nobreak

echo Starting frontend on http://localhost:5173...
start cmd /k "cd frontend && npm run dev"
echo ✅ Frontend started

echo.
echo =====================================
echo 🚀 EarthLens is running!
echo =====================================
echo.
echo 📍 Frontend: http://localhost:5173
echo 📍 Backend API: http://localhost:8000
echo 📍 API Docs: http://localhost:8000/docs
echo.
echo Demo Credentials:
echo   Email: demo@earthlens.io
echo   Password: DemoPass123!
echo.
echo For ngrok tunnels (public URLs):
echo   start-ngrok.bat
echo.
echo Close the terminal windows to stop services.
echo.
pause
