import os
import sqlite3
from flask import Flask

print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir())

# Create test Flask app
app = Flask(__name__)
print("Flask instance path:", app.instance_path)

# Check if instance directory exists
if os.path.exists('instance'):
    print("'instance' directory exists")
    print("Contents:", os.listdir('instance'))
else:
    print("'instance' directory does not exist")
    # Create it
    os.makedirs('instance', exist_ok=True)
    print("Created 'instance' directory")

# Try absolute path
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
print("Absolute instance path:", instance_path)
if os.path.exists(instance_path):
    print("Absolute instance path exists")
    print("Contents:", os.listdir(instance_path))
else:
    print("Absolute instance path does not exist")

# Try to connect to the database
db_path = 'instance/petrol_station.db'
print("Trying to connect to database at:", db_path)
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:", tables)
    
    # Count records in each table
    for table_name in [row[0] for row in tables]:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"Records in {table_name}: {count}")
        except Exception as e:
            print(f"Error counting records in {table_name}: {str(e)}")
    
    conn.close()
    print("Database connection successful")
except Exception as e:
    print("Database connection failed:", str(e))

# Try with absolute path
abs_db_path = os.path.join(instance_path, 'petrol_station.db')
print("Trying to connect to database with absolute path:", abs_db_path)
try:
    conn = sqlite3.connect(abs_db_path)
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database (absolute path):", tables)
    
    # Count records in each table
    for table_name in [row[0] for row in tables]:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"Records in {table_name} (absolute path): {count}")
        except Exception as e:
            print(f"Error counting records in {table_name} (absolute path): {str(e)}")
    
    conn.close()
    print("Database connection with absolute path successful")
except Exception as e:
    print("Database connection with absolute path failed:", str(e))
