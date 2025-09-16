#!/usr/bin/env python3
import os
import sys

# Simple Railway deployment - change to backend directory FIRST
if __name__ == '__main__':
    # Change to backend directory BEFORE importing Flask app
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Add backend to Python path
    sys.path.insert(0, backend_dir)
    
    # NOW import Flask app (so it initializes with correct working directory)
    from app import app
    
    # Get port from Railway environment
    port = int(os.environ.get('PORT', 5000))
    
    # Run the Flask app
    app.run(debug=False, host='0.0.0.0', port=port)
