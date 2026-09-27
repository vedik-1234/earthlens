#!/bin/bash
# Start EarthLens development servers

set -e

echo "🌍 Starting EarthLens..."
echo ""

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up backend...${NC}"
cd "$ROOT_DIR/backend"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file. Update with your settings if needed."
fi

echo "Installing backend dependencies..."
pip install -q -r requirements.txt 2>/dev/null || {
    echo -e "${RED}Failed to install backend dependencies${NC}"
    exit 1
}

echo -e "${GREEN}✓ Backend ready${NC}"
echo ""

echo -e "${YELLOW}Setting up frontend...${NC}"
cd "$ROOT_DIR/frontend"

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file."
fi

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install -q 2>/dev/null || {
        echo -e "${RED}Failed to install frontend dependencies${NC}"
        exit 1
    }
else
    echo "Frontend dependencies already installed."
fi

echo -e "${GREEN}✓ Frontend ready${NC}"
echo ""

echo -e "${GREEN}Launching EarthLens...${NC}"
echo ""
echo -e "${YELLOW}Backend starting on http://localhost:8000${NC}"
echo -e "${YELLOW}Frontend starting on http://localhost:5173${NC}"
echo ""
echo "Press Ctrl+C to stop both servers."
echo ""

cd "$ROOT_DIR/backend"
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > /tmp/earthlens-backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

sleep 2

cd "$ROOT_DIR/frontend"
npm run dev -- --host 0.0.0.0 --port 5173 > /tmp/earthlens-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo -e "${GREEN}✓ EarthLens is running!${NC}"
echo ""

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'; exit 0" EXIT INT TERM

wait
