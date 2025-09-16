#!/usr/bin/env python3
import os
import sys
import subprocess

# Simple Railway deployment script
if __name__ == '__main__':
    # Change to backend directory and run the Flask app
    os.chdir('backend')
    subprocess.run([sys.executable, 'app.py'])
