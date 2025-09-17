#!/bin/bash
set -e

echo "Checking database status..."
ls -la instance/
echo "Database size:"
du -sh instance/petrol_station.db || echo "Database not found"

echo "Starting app..."
python app.py
