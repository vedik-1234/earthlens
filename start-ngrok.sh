#!/bin/bash

# EarthLens ngrok startup script for macOS/Linux

set -e

echo "🌍 EarthLens ngrok Tunnel Setup"
echo "================================"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed. Install it from https://ngrok.com/download"
    exit 1
fi

# Check if ngrok authtoken is set
if [ -z "$(ngrok config get authtoken 2>/dev/null)" ]; then
    echo "❌ ngrok authtoken not configured."
    echo "   Run: ngrok config add-authtoken <your-token>"
    echo "   Get token from: https://dashboard.ngrok.com/auth/your-authtoken"
    exit 1
fi

echo "✅ ngrok configured and ready"
echo ""
echo "Starting ngrok tunnels..."
echo ""

# Start ngrok with the config file
ngrok start --config ngrok.yml earthlens-backend earthlens-frontend
