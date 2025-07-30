#!/bin/bash
# dev.sh — Start dev server with symlink to data/

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

if [ -L docs/data ]; then
    echo "[✓] Symlink docs/data already exists."
elif [ -e docs/data ]; then
    echo "[!] docs/data exists but is not a symlink. Removing..."
    rm -rf docs/data
    ln -s ../data docs/data
    echo "[+] Created symlink: docs/data → ../data"
else
    ln -s ../data docs/data
    echo "[+] Created symlink: docs/data → ../data"
fi

echo "[▶] Starting dev server..."
uv run server.py
