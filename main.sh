#!/bin/bash

# Exit if any command fails
set -e

echo "🔄 Building the static site..."
./build.sh  # Run the site generator (build.sh)

echo "🏗️  Launching the FastAPI API server..."
uvicorn api:app --reload &  # Start FastAPI API in the background

echo "🌐 Launching basic HTTP server for static files at http://127.0.0.1:8001"
# Start a simple HTTP server in the site/ directory to serve static content
python3 -m http.server 8001 --directory ./docs &

echo "✔️ Static site is being served at http://127.0.0.1:8001"
echo "✔️ API server is running at http://127.0.0.1:8000"
echo "✔️ Press Ctrl+C to stop both processes."

wait  # Keep the script running to handle API requests
