#!/bin/bash
set -e

echo "=== DATABASE SETUP SCRIPT ==="
echo "Current directory: $(pwd)"
echo "Listing all .db files:"
find . -name "*.db" -type f

echo "Creating instance directory..."
mkdir -p instance

echo "Using the guaranteed database with real data..."
if [ -f "petrol_station_with_data.db" ]; then
    echo "Found real data database, copying..."
    cp petrol_station_with_data.db instance/petrol_station.db
    echo "Real data database copied successfully!"
elif [ -f "backend/instance/petrol_station.db" ]; then
    echo "Found database in backend/instance, copying..."
    cp backend/instance/petrol_station.db instance/petrol_station.db
    echo "Database copied from backend/instance!"
elif [ -f "backend/petrol_station.db" ]; then
    echo "Found database in backend root, copying..."
    cp backend/petrol_station.db instance/petrol_station.db
    echo "Database copied from backend root!"
else
    echo "ERROR: No database found anywhere!"
    exit 1
fi

echo "Verifying database has data..."
if command -v sqlite3 &> /dev/null; then
    echo "Daily records count:"
    sqlite3 instance/petrol_station.db "SELECT COUNT(*) FROM daily_consolidation;" || echo "Could not count daily records"
    echo "Procurement records count:"
    sqlite3 instance/petrol_station.db "SELECT COUNT(*) FROM procurement_data;" || echo "Could not count procurement records"
else
    echo "sqlite3 not available for verification"
fi

echo "Final instance directory contents:"
ls -la instance/

echo "Setting permissions..."
chmod -R 777 instance/

echo "=== DATABASE SETUP COMPLETE ==="