#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, DailyConsolidation
from datetime import date

def manual_data_entry():
    """Manual data entry helper for PDF data"""
    print("Manual Data Entry from PDF Files")
    print("=" * 50)
    print("I'll help you enter the actual data from your PDF files.")
    print("\nFor each PDF file, I need the following information:")
    print("(Based on the AnyScanner filenames you provided)")
    
    # List the PDF files we know about
    pdf_files = [
        "AnyScanner 21-08-2025 15-32-19.pdf",
        "AnyScanner 22-08-2025 10-35-29.pdf", 
        "AnyScanner 23-08-2025 09-58-59.pdf",
        "AnyScanner 24-08-2025 18-24-52.pdf",
        "AnyScanner 25-08-2025 10-17-20.pdf",
        "AnyScanner 26-08-2025 10-17-51.pdf",
        "AnyScanner 27-08-2025 10-18-31.pdf",
        "AnyScanner 28-08-2025 10-19-04.pdf",
        "AnyScanner 29-08-2025 10-19-35.pdf",
        "AnyScanner 30-08-2025 10-20-08.pdf",
        "AnyScanner 31-08-2025 10-20-37.pdf",
        "AnyScanner 01-09-2025 10-21-08.pdf",
        "AnyScanner 02-09-2025 10-21-40.pdf",
        "AnyScanner 03-09-2025 10-22-12.pdf",
        "AnyScanner 04-09-2025 10-22-42.pdf",
        "AnyScanner 05-09-2025 10-23-17.pdf",
        "AnyScanner 06-09-2025 10-23-47.pdf",
        "AnyScanner 07-09-2025 10-24-20.pdf",
        "AnyScanner 08-09-2025 10-24-51.pdf",
        "AnyScanner 09-09-2025 10-25-24.pdf",
        "AnyScanner 10-09-2025 10-25-57.pdf",
        "AnyScanner 11-09-2025 10-26-25.pdf",
        "AnyScanner 12-09-2025 10-26-56.pdf"
    ]
    
    print(f"\nFound {len(pdf_files)} PDF files to process")
    print("\nFor each date, I need both DAY and NIGHT shift data:")
    
    template = """
    Date: {date}
    Shift: Day/Night
    Manager: 
    
    Fuel Rates:
    - MS Rate: 
    - HSD Rate: 
    - Power Rate: 
    
    Quantities Sold:
    - MS Quantity: 
    - HSD Quantity: 
    - Power Quantity: 
    
    Tank Readings:
    - HSD1 Tank: 
    - HSD2 Tank: 
    - MS1 Tank: 
    - MS2 Tank: 
    - Power1 Tank: 
    
    Collections:
    - Cash Collections: 
    - Card Collections: 
    - Paytm Collections: 
    - HP Transactions: 
    - HPCL Payment: 
    
    Outstanding Balance:
    - Total Outstanding: 
    
    Notes: 
    """
    
    print("Data Template for each entry:")
    print(template)

def add_single_entry():
    """Add a single entry with actual data"""
    print("Add Single Entry from PDF Data")
    print("=" * 40)
    
    # Get date
    date_str = input("Enter date (YYYY-MM-DD): ").strip()
    try:
        entry_date = date.fromisoformat(date_str)
    except:
        print("Invalid date format")
        return
    
    shift = input("Enter shift (Day/Night): ").strip()
    if shift not in ['Day', 'Night']:
        print("Shift must be 'Day' or 'Night'")
        return
    
    print("\nEntering data for", entry_date, shift)
    
    # Collect all the data
    entry_data = {
        'date': entry_date,
        'shift': shift,
        'manager': input("Manager: ").strip() or 'ga',
        'ms_rate': float(input("MS Rate: ") or 0),
        'ms_quantity': float(input("MS Quantity: ") or 0),
        'hsd_rate': float(input("HSD Rate: ") or 0),
        'hsd_quantity': float(input("HSD Quantity: ") or 0),
        'power_rate': float(input("Power Rate: ") or 0),
        'power_quantity': float(input("Power Quantity: ") or 0),
        'hsd1_tank': float(input("HSD1 Tank: ") or 0),
        'hsd2_tank': float(input("HSD2 Tank: ") or 0),
        'ms1_tank': float(input("MS1 Tank: ") or 0),
        'ms2_tank': float(input("MS2 Tank: ") or 0),
        'power1_tank': float(input("Power1 Tank: ") or 0),
        'cash_collections': float(input("Cash Collections: ") or 0),
        'card_collections': float(input("Card Collections: ") or 0),
        'paytm_collections': float(input("Paytm Collections: ") or 0),
        'hp_transactions': float(input("HP Transactions: ") or 0),
        'hpcl_payment': float(input("HPCL Payment: ") or 0),
        'total_outstanding': float(input("Total Outstanding: ") or 0),
        'manager_notes': input("Notes: ").strip()
    }
    
    # Calculate amounts
    entry_data['ms_amount'] = entry_data['ms_rate'] * entry_data['ms_quantity']
    entry_data['hsd_amount'] = entry_data['hsd_rate'] * entry_data['hsd_quantity']
    entry_data['power_amount'] = entry_data['power_rate'] * entry_data['power_quantity']
    
    # Add to database
    with app.app_context():
        try:
            entry = DailyConsolidation(**entry_data)
            db.session.add(entry)
            db.session.commit()
            print(f"✅ Successfully added entry for {entry_date} {shift}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error adding entry: {e}")

if __name__ == "__main__":
    print("PDF Data Entry Helper")
    print("=" * 30)
    
    choice = input("1. Show manual entry template\n2. Add single entry\nChoice: ").strip()
    
    if choice == '1':
        manual_data_entry()
    elif choice == '2':
        add_single_entry()
    else:
        print("Invalid choice")
