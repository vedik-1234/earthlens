@echo off
REM EarthLens ngrok startup script for Windows

echo 🌍 EarthLens ngrok Tunnel Setup
echo ================================

REM Check if ngrok is installed
where ngrok >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ngrok is not installed. Install it from https://ngrok.com/download
    exit /b 1
)

echo ✅ ngrok found
echo.
echo Starting ngrok tunnels...
echo.

REM Start ngrok with the config file
ngrok start --config ngrok.yml earthlens-backend earthlens-frontend

if %errorlevel% neq 0 (
    echo.
    echo ❌ ngrok tunnel failed. Check your authtoken:
    echo    ngrok config add-authtoken ^<your-token^>
    echo    Get token from: https://dashboard.ngrok.com/auth/your-authtoken
    exit /b 1
)
