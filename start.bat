@echo off
setlocal
set ROOT=%~dp0

cd /d "%ROOT%\backend"
python -m venv .venv 2>nul
call .venv\Scripts\activate
pip install -r requirements.txt
start "EarthLens Backend" cmd /k uvicorn app.main:app --host 0.0.0.0 --port 8000

cd /d "%ROOT%\frontend"
if not exist node_modules (
  npm install
)
start "EarthLens Frontend" cmd /k npm run dev -- --host 0.0.0.0 --port 5173
