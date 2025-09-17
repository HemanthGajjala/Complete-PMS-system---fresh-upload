#!/bin/bash
set -e

echo "Checking database status..."
mkdir -p instance
chmod 777 instance
ls -la instance/ || echo "Instance directory issue"

# Copy the database to instance if it's not there or empty
if [ ! -s "instance/petrol_station.db" ]; then
  echo "Database empty or not found, copying from backup..."
  cp -f backend/instance/petrol_station.db instance/ || cp -f backend/petrol_station.db instance/ || echo "No database found to copy"
  echo "After copy:"
  ls -la instance/
  # Make sure the database is writable
  chmod 666 instance/petrol_station.db || echo "Couldn't set permissions on database file"
fi

echo "Starting app with database in instance directory..."
python app.py
