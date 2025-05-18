#!/bin/bash

set -e 

echo "🔄 Cleaning previous build..."
rm -rf docs
mkdir docs

cp static/style.css docs/
cp static/img/ -r docs/

echo "🏗️  Generating static site from RDF..."
python3 main.py

echo "✅ Site built in ./docs/"
