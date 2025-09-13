#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, DailyConsolidation
from datetime import date

def show_database_structure():
    """Show the complete structure of DailyConsolidation model"""
    with app.app_context():
        # Get the last successful entry to see all fields
        last_entry = DailyConsolidation.query.filter(
            DailyConsolidation.date == date(2025, 8, 20)
        ).filter(
            DailyConsolidation.shift == 'Night'
        ).first()
        
        if last_entry:
            print("Database Structure - All Fields:")
            print("="*50)
            
            # Get all column names
            columns = DailyConsolidation.__table__.columns.keys()
            
            for col in columns:
                value = getattr(last_entry, col)
                print(f"{col:25}: {value}")
                
            print("\n" + "="*50)
            print("Required fields for new entries identified!")

if __name__ == "__main__":
    show_database_structure()
