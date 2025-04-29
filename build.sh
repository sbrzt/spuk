#!/bin/bash

set -e  # stop on error

echo "🔄 Cleaning previous build..."
rm -rf docs
mkdir docs

cp static/style.css docs/

echo "🏗️  Generating static site from RDF..."
python3 main.py

echo "✅ Site built in ./docs/"
