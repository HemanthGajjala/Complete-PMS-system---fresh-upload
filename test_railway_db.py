import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Configure a minimal Flask app for testing database connection
app = Flask(__name__)

# Set up database connection
instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/petrol_station.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def test_database_connection():
    print("RAILWAY DATABASE TEST")
    print("=====================")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir()}")
    print(f"Instance directory path: {instance_dir}")
    
    if os.path.exists(instance_dir):
        print(f"Instance directory exists: {instance_dir}")
        print(f"Files in instance directory: {os.listdir(instance_dir)}")
        
        db_path = os.path.join(instance_dir, 'petrol_station.db')
        if os.path.exists(db_path):
            print(f"Database file exists: {db_path}")
            print(f"Database file size: {os.path.getsize(db_path)} bytes")
        else:
            print(f"Database file does not exist: {db_path}")
    else:
        print(f"Instance directory does not exist: {instance_dir}")
    
    try:
        with app.app_context():
            # Test basic connection
            result = db.session.execute(text('SELECT 1')).scalar()
            print(f"Database connection test: {result}")
            
            # Test table existence
            try:
                tables = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
                print(f"Tables in database: {[table[0] for table in tables]}")
                
                # Count records in each table
                for table in [table[0] for table in tables]:
                    try:
                        count = db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                        print(f"Records in {table}: {count}")
                    except Exception as e:
                        print(f"Error counting records in {table}: {str(e)}")
                
                print("Database test successful!")
            except Exception as e:
                print(f"Error checking tables: {str(e)}")
    except Exception as e:
        print(f"Database connection error: {str(e)}")

if __name__ == "__main__":
    test_database_connection()
