#!/bin/bash

set -e  # stop on error

echo "🔄 Cleaning previous build..."
rm -rf docs
mkdir docs

echo "🏗️  Generating static site from RDF..."
python3 main.py

echo "✅ Site built in ./docs/"
