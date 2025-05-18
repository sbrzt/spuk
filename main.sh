#!/bin/bash

set -e

fuser -k 8001/tcp 2>/dev/null || true

echo "🔄 Building the static site..."
./build.sh

echo "🌐 Launching basic HTTP server for static files at http://127.0.0.1:8001"
python3 -m http.server 8001 --directory ./docs &

echo "✔️ Static site is being served at http://127.0.0.1:8001"
echo "✔️ Press Ctrl+C to stop both processes."

wait
