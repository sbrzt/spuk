#!/bin/bash

set -e

fuser -k 8001/tcp 2>/dev/null || true

python3 dev_server.py