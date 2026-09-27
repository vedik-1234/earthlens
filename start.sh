#!/bin/bash

# EarthLens Complete Startup Script for macOS/Linux
# Launches both backend and frontend with production settings

set -e

echo "🌍 EarthLens v2.0 - Production Ready"
echo "====================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Determine OS
OS="$(uname -s)"
case "${OS}" in
    Linux*) OS='Linux' ;;
    Darwin*) OS='Mac' ;;
    *) OS='UNKNOWN' ;;
esac

echo "Detected OS: ${OS}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 found${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js found${NC}"
echo ""

# Setup Backend
echo -e "${YELLOW}Setting up backend...${NC}"
cd backend

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "Generating secure JWT secret..."
if [ -z "$EARTHLENS_JWT_SECRET" ]; then
    export EARTHLENS_JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo "JWT_SECRET generated: $EARTHLENS_JWT_SECRET"
fi

echo "Initializing database..."
python3 -c "from app.services.auth_service import init_db; init_db()"

echo -e "${GREEN}✅ Backend ready${NC}"
echo ""

# Setup Frontend
echo -e "${YELLOW}Setting up frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install --silent
fi

echo -e "${GREEN}✅ Frontend ready${NC}"
echo ""

# Start services
echo -e "${YELLOW}Starting services...${NC}"
echo ""

# Start backend in background
cd ../backend
echo "Starting backend on http://0.0.0.0:8000..."
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend PID: ${BACKEND_PID}${NC}"

# Wait for backend to start
sleep 2

# Start frontend in background
cd ../frontend
echo "Starting frontend on http://localhost:5173..."
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend PID: ${FRONTEND_PID}${NC}"

echo ""
echo -e "${GREEN}=================================${NC}"
echo -e "${GREEN}🚀 EarthLens is running!${NC}"
echo -e "${GREEN}=================================${NC}"
echo ""
echo "📍 Frontend: http://localhost:5173"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Demo Credentials:"
echo "  Email: demo@earthlens.io"
echo "  Password: DemoPass123!"
echo ""
echo "For ngrok tunnels (public URLs):"
echo "  ./start-ngrok.sh"
echo ""
echo "To stop services: Press Ctrl+C"
echo ""

# Handle cleanup
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped'; exit 0" SIGINT SIGTERM

# Keep script running
wait
