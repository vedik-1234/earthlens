@echo off
setlocal
if not exist .env (
  copy .env.example .env
  echo Created .env. Add NGROK_AUTHTOKEN, then run this script again.
  exit /b 1
)

echo Starting EarthLens with frontend and backend ngrok tunnels...
docker compose --profile tunnel up --build
