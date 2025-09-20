#!/bin/bash
set -e

echo "=== STARTING APPLICATION ==="
echo "Current directory: $(pwd)"
echo "All database files:"
find . -name "*.db" -type f

echo "Ensuring templates directory..."
mkdir -p templates
if [ -f "static/index.html" ]; then
  cp static/index.html templates/
  echo "Frontend template ready"
fi

echo "Starting Flask application..."
python app.py
