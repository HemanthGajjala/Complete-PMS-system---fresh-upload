import os
import sqlite3
from flask import Flask
import shutil

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

# Check for database file in instance directory
if not os.path.exists('instance/petrol_station.db'):
    print("Database file doesn't exist in instance directory")
    
    # Check if database exists in backend/instance
    if os.path.exists('backend/instance/petrol_station.db'):
        print("Database found in backend/instance, copying to instance directory")
        shutil.copy('backend/instance/petrol_station.db', 'instance/petrol_station.db')
        print("Database copied successfully")
    # Check if database exists in backend
    elif os.path.exists('backend/petrol_station.db'):
        print("Database found in backend, copying to instance directory")
        shutil.copy('backend/petrol_station.db', 'instance/petrol_station.db')
        print("Database copied successfully")
    # If no database found, create a new one
    else:
        print("No existing database found, creating a new one")
        conn = sqlite3.connect('instance/petrol_station.db')
        c = conn.cursor()
        
        # Create basic tables
        c.execute('''
        CREATE TABLE IF NOT EXISTS daily_consolidation (
            id INTEGER PRIMARY KEY,
            date DATE,
            ms_sales REAL,
            ms_amount REAL,
            hsd_sales REAL,
            hsd_amount REAL,
            power_sales REAL,
            power_amount REAL,
            cash_collections REAL,
            card_collections REAL,
            paytm_collections REAL,
            expenses REAL,
            comments TEXT
        )
        ''')
        
        c.execute('''
        CREATE TABLE IF NOT EXISTS procurement_data (
            id INTEGER PRIMARY KEY,
            date DATE,
            ms_received REAL,
            ms_amount REAL,
            hsd_received REAL,
            hsd_amount REAL,
            power_received REAL,
            power_amount REAL,
            payment_mode TEXT,
            invoice_number TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        print("Created new database with basic schema")

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
