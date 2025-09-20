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

echo "=== SETTING UP ROOT DATABASE ==="
# Copy the database to root if it's not there or empty
if [ ! -s "petrol_station.db" ]; then
  echo "Root database empty or not found, copying from backup..."
  if [ -f "backend/instance/petrol_station.db" ]; then
    cp -f backend/instance/petrol_station.db petrol_station.db
    echo "Copied to root from backend/instance/petrol_station.db"
  elif [ -f "backend/petrol_station.db" ]; then
    cp -f backend/petrol_station.db petrol_station.db
    echo "Copied to root from backend/petrol_station.db"
  elif [ -f "instance/petrol_station.db" ]; then
    cp -f instance/petrol_station.db petrol_station.db
    echo "Copied to root from instance/petrol_station.db"
  else
    echo "NO DATABASE FOUND TO COPY!"
  fi
  
  # Make sure database is writable
  chmod 666 petrol_station.db || echo "Couldn't set permissions on database file"
else
  echo "Database already exists at root"
fi

echo "=== VERIFYING ROOT DATABASE ==="
if [ -f "petrol_station.db" ]; then
  echo "Root database size: $(stat -c%s petrol_station.db) bytes"
  echo "Database tables:"
  sqlite3 petrol_station.db "SELECT name FROM sqlite_master WHERE type='table';" || echo "Cannot query root database"
  echo "Record counts:"
  sqlite3 petrol_station.db "SELECT COUNT(*) as daily_count FROM daily_consolidation;" || echo "Cannot count daily records"
  sqlite3 petrol_station.db "SELECT COUNT(*) as procurement_count FROM procurement_data;" || echo "Cannot count procurement records"
else
  echo "ROOT DATABASE NOT FOUND!"
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
