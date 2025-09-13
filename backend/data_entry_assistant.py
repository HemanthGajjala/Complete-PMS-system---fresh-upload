#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, DailyConsolidation
from datetime import date

# Data entries based on the PDF files and logical progression
# Since these are scanned documents and complex to parse automatically,
# I'll create template entries that you can verify and adjust

daily_entries = [
    # August 21, 2025 entries
    {
        'date': date(2025, 8, 21),
        'shift': 'Day',
        'manager': 'ga',  # Using same manager from previous entries
        'ms_rate': 108.56,
        'ms_quantity': 800.0,  # Estimated based on typical daily sales
        'ms_amount': 86848.0,
        'hsd_rate': 96.46,
        'hsd_quantity': 1200.0,
        'hsd_amount': 115752.0,
        'power_rate': 108.0,
        'power_quantity': 200.0,
        'power_amount': 21600.0,
        'cash_collections': 80000.0,
        'card_collections': 100000.0,
        'paytm_collections': 15000.0,
        'hp_transactions': 5000.0,
        'hpcl_payment': 0.0,
        'total_outstanding': 2300000.0  # Estimated progression
    },
    {
        'date': date(2025, 8, 21),
        'shift': 'Night',
        'manager': 'ga',
        'ms_rate': 108.56,
        'ms_quantity': 650.0,
        'ms_amount': 70564.0,
        'hsd_rate': 96.46,
        'hsd_quantity': 950.0,
        'hsd_amount': 91637.0,
        'power_rate': 108.0,
        'power_quantity': 150.0,
        'power_amount': 16200.0,
        'cash_collections': 65000.0,
        'card_collections': 85000.0,
        'paytm_collections': 12000.0,
        'hp_transactions': 3000.0,
        'hpcl_payment': 0.0,
        'total_outstanding': 2400000.0
    }
]

def add_daily_entries():
    """Add the daily entries to the database"""
    with app.app_context():
        print("Adding daily entries to database...")
        
        for entry_data in daily_entries:
            # Check if entry already exists
            existing = DailyConsolidation.query.filter_by(
                date=entry_data['date'],
                shift=entry_data['shift']
            ).first()
            
            if existing:
                print(f"Entry already exists for {entry_data['date']} {entry_data['shift']} - skipping")
                continue
            
            # Calculate tank readings (placeholder values)
            entry_data.update({
                'hsd1_tank': 5000.0,
                'hsd2_tank': 3000.0,
                'ms1_tank': 4000.0,
                'ms2_tank': 2500.0,
                'power1_tank': 1500.0
            })
            
            # Create new entry
            entry = DailyConsolidation(**entry_data)
            
            try:
                db.session.add(entry)
                db.session.commit()
                print(f"✅ Added entry for {entry_data['date']} {entry_data['shift']}")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error adding entry for {entry_data['date']} {entry_data['shift']}: {e}")
        
        print("Done adding initial entries!")
        print("\nNOTE: These are template entries with estimated values.")
        print("Please review and update them with actual values from your physical forms.")

def show_template_for_manual_entry():
    """Show a template for manual data entry"""
    print("\n" + "="*80)
    print("MANUAL DATA ENTRY TEMPLATE")
    print("="*80)
    print("\nFor each PDF file, please provide the following information:")
    print("I'll create entries that you can verify and adjust.")
    print("\nThe following dates need data entry:")
    
    from datetime import timedelta
    start_date = date(2025, 8, 21)
    end_date = date(2025, 9, 12)
    
    current_date = start_date
    while current_date <= end_date:
        print(f"• {current_date.strftime('%Y-%m-%d')} (Day & Night shifts)")
        current_date += timedelta(days=1)

if __name__ == "__main__":
    print("Daily Data Entry Assistant")
    print("="*40)
    
    choice = input("What would you like to do?\n1. Add sample entries for Aug 21\n2. Show manual entry template\nChoice (1/2): ")
    
    if choice == '1':
        add_daily_entries()
    elif choice == '2':
        show_template_for_manual_entry()
    else:
        print("Invalid choice")
