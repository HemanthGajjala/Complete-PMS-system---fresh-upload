#!/bin/bash
set -e

echo "=== DATABASE SETUP SCRIPT ==="
echo "Current directory: $(pwd)"
echo "Listing all files:"
find . -name "*.db" -type f

echo "Creating instance directory..."
mkdir -p instance

echo "Looking for database files in backend/instance..."
if [ -f "backend/instance/petrol_station.db" ]; then
    echo "Found database in backend/instance, copying..."
    cp backend/instance/petrol_station.db instance/petrol_station.db
    echo "Database copied successfully!"
else
    echo "No database found in backend/instance"
fi

echo "Looking for database files in backend..."
if [ -f "backend/petrol_station.db" ]; then
    echo "Found database in backend root, copying..."
    cp backend/petrol_station.db instance/petrol_station.db
    echo "Database copied from backend root!"
else
    echo "No database found in backend root"
fi

echo "Final instance directory contents:"
ls -la instance/

echo "Setting permissions..."
chmod -R 777 instance/

echo "=== DATABASE SETUP COMPLETE ==="