#!/bin/bash
set -e

echo "=== RAILWAY DEPLOYMENT DEBUG ==="
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

echo "=== CHECKING DATABASE SOURCES ==="
# Check all possible database locations
if [ -f "backend/instance/petrol_station.db" ]; then
  echo "Found backend/instance/petrol_station.db - Size: $(stat -c%s backend/instance/petrol_station.db) bytes"
  sqlite3 backend/instance/petrol_station.db "SELECT name FROM sqlite_master WHERE type='table';" || echo "Cannot query backend database"
  sqlite3 backend/instance/petrol_station.db "SELECT COUNT(*) as daily_count FROM daily_consolidation;" || echo "Cannot count backend daily records"
else
  echo "backend/instance/petrol_station.db NOT FOUND"
fi

if [ -f "backend/petrol_station.db" ]; then
  echo "Found backend/petrol_station.db - Size: $(stat -c%s backend/petrol_station.db) bytes"
else
  echo "backend/petrol_station.db NOT FOUND"
fi

echo "=== SETTING UP INSTANCE DIRECTORY ==="
mkdir -p instance
chmod 777 instance

# Copy the database to instance if it's not there or empty
if [ ! -s "instance/petrol_station.db" ]; then
  echo "Database empty or not found, copying from backup..."
  if [ -f "backend/instance/petrol_station.db" ]; then
    cp -f backend/instance/petrol_station.db instance/
    echo "Copied from backend/instance/petrol_station.db"
  elif [ -f "backend/petrol_station.db" ]; then
    cp -f backend/petrol_station.db instance/
    echo "Copied from backend/petrol_station.db"
  else
    echo "NO DATABASE FOUND TO COPY!"
  fi
else
  echo "Database already exists in instance/"
fi

echo "=== VERIFYING COPIED DATABASE ==="
if [ -f "instance/petrol_station.db" ]; then
  echo "Final database size: $(stat -c%s instance/petrol_station.db) bytes"
  chmod 666 instance/petrol_station.db
  echo "Database tables:"
  sqlite3 instance/petrol_station.db "SELECT name FROM sqlite_master WHERE type='table';" || echo "Cannot query final database"
  echo "Record counts:"
  sqlite3 instance/petrol_station.db "SELECT COUNT(*) as daily_count FROM daily_consolidation;" || echo "Cannot count daily records"
  sqlite3 instance/petrol_station.db "SELECT COUNT(*) as procurement_count FROM procurement_data;" || echo "Cannot count procurement records"
else
  echo "FINAL DATABASE NOT FOUND!"
fi

echo "=== CHECKING FRONTEND BUILD ==="
if [ -d "static" ]; then
  echo "Static directory exists, listing contents:"
  ls -la static/
else
  echo "No static directory found!"
fi

# Update templates directory
mkdir -p templates
if [ -f "static/index.html" ]; then
  cp static/index.html templates/
  echo "Copied index.html to templates"
else
  echo "No index.html found in static directory!"
fi

echo "=== STARTING APPLICATION ==="
python app.py
