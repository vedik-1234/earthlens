# EarthLens startup helper for a public ngrok demo.
# Prerequisite: Docker Desktop and an ngrok auth token.

set -e

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env. Add NGROK_AUTHTOKEN, then rerun this script."
  exit 1
fi

if ! grep -q '^NGROK_AUTHTOKEN=.[^ ]' .env; then
  echo "Set NGROK_AUTHTOKEN in .env before starting ngrok."
  exit 1
fi

echo "Starting EarthLens with frontend and backend ngrok tunnels..."
docker compose --profile tunnel up --build
