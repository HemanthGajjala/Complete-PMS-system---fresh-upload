#!/usr/bin/env python3
import sqlite3
import os
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    # Try multiple database locations
    db_paths = [
        'petrol_station_with_data.db',
        'instance/petrol_station.db',
        'backend/instance/petrol_station.db'
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            print(f"Found database at: {db_path}")
            return sqlite3.connect(db_path)
    
    print("No database found!")
    return None

@app.route('/api/daily-consolidation')
def get_daily_data():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database not found'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM daily_consolidation')
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute('PRAGMA table_info(daily_consolidation)')
        columns = [col[1] for col in cursor.fetchall()]
        
        # Convert to dictionaries
        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))
        
        conn.close()
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/procurement')
def get_procurement_data():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database not found'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM procurement_data')
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute('PRAGMA table_info(procurement_data)')
        columns = [col[1] for col in cursor.fetchall()]
        
        # Convert to dictionaries
        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))
        
        conn.close()
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-direct-db')
def test_direct_db():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database not found'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Count records directly
        cursor.execute('SELECT COUNT(*) FROM daily_consolidation')
        daily_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM procurement_data')
        procurement_count = cursor.fetchone()[0]
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return jsonify({
            'database_found': True,
            'daily_records': daily_count,
            'procurement_records': procurement_count,
            'all_tables': tables
        })
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return '''
    <h1>Direct Database Test</h1>
    <p><a href="/api/test-direct-db">Test Direct Database Access</a></p>
    <p><a href="/api/daily-consolidation">Get Daily Data</a></p>
    <p><a href="/api/procurement">Get Procurement Data</a></p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)