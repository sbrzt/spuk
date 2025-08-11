#!/bin/bash
# dev.sh

set -e

cd "$(dirname "$0")"

if lsof -iTCP:8000 -sTCP:LISTEN -t >/dev/null; then
  PID=$(lsof -iTCP:8000 -sTCP:LISTEN -t)
  echo "[dev.sh] Port 8000 is in use by PID $PID. Killing it..."
  kill "$PID"
  sleep 1
fi


echo "[dev.sh] Running initial build..."
uv run main.py

echo "[▶] Starting dev server..."
uv run server.py
