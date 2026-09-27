#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR/backend"
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd "$ROOT_DIR/frontend"
if [ ! -d node_modules ]; then
  npm install
fi
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
