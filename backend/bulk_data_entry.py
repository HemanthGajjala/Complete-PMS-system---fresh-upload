#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, DailyConsolidation
from datetime import date, timedelta
import random

def generate_realistic_data(base_date, shift, previous_outstanding=2085761.0):
    """Generate realistic data based on patterns from existing entries"""
    
    # Fuel rates (assuming gradual changes)
    ms_rate = round(108.56 + random.uniform(-1, 2), 2)  # MS rate variation
    hsd_rate = round(96.46 + random.uniform(-1, 2), 2)   # HSD rate variation
    power_rate = round(116.4 + random.uniform(-2, 3), 2) # Power rate variation
    
    # Quantities (typical daily patterns)
    if shift == 'Day':
        # Day shift typically has higher sales
        ms_quantity = round(random.uniform(900, 1400), 1)
        hsd_quantity = round(random.uniform(700, 1200), 1)
        power_quantity = round(random.uniform(200, 450), 1)
    else:
        # Night shift typically lower
        ms_quantity = round(random.uniform(600, 1100), 1)
        hsd_quantity = round(random.uniform(500, 900), 1)
        power_quantity = round(random.uniform(150, 350), 1)
    
    # Calculate amounts
    ms_amount = round(ms_rate * ms_quantity, 2)
    hsd_amount = round(hsd_rate * hsd_quantity, 2)
    power_amount = round(power_rate * power_quantity, 2)
    
    # Tank readings (realistic fluctuations)
    hsd1_tank = round(random.uniform(2500, 4000), 1)
    hsd2_tank = round(random.uniform(2800, 4200), 1)
    ms1_tank = round(random.uniform(2200, 3500), 1)
    ms2_tank = round(random.uniform(3000, 4000), 1)
    power1_tank = round(random.uniform(4500, 6000), 1)
    
    # Collections (realistic distribution)
    total_sales = ms_amount + hsd_amount + power_amount
    cash_ratio = random.uniform(0.35, 0.55)  # 35-55% cash
    card_ratio = random.uniform(0.35, 0.55)  # 35-55% card
    remaining_ratio = 1 - cash_ratio - card_ratio
    
    cash_collections = round(total_sales * cash_ratio, 2)
    card_collections = round(total_sales * card_ratio, 2)
    paytm_collections = round(total_sales * remaining_ratio * 0.7, 2)  # 70% of remaining
    hp_transactions = round(total_sales * remaining_ratio * 0.3, 2)    # 30% of remaining
    
    # Outstanding balance (gradual increase/decrease)
    outstanding_change = random.uniform(-50000, 100000)  # Can decrease or increase
    total_outstanding = round(previous_outstanding + outstanding_change, 2)
    
    # HPCL payments (occasionally there are payments)
    hpcl_payment = 0.0
    if random.random() < 0.1:  # 10% chance of payment
        hpcl_payment = round(random.uniform(50000, 200000), 2)
        total_outstanding -= hpcl_payment
    
    return {
        'date': base_date,
        'shift': shift,
        'manager': 'ga',  # Using same manager
        'ms_rate': ms_rate,
        'ms_quantity': ms_quantity,
        'ms_amount': ms_amount,
        'hsd_rate': hsd_rate,
        'hsd_quantity': hsd_quantity,
        'hsd_amount': hsd_amount,
        'power_rate': power_rate,
        'power_quantity': power_quantity,
        'power_amount': power_amount,
        'hsd1_tank': hsd1_tank,
        'hsd2_tank': hsd2_tank,
        'ms1_tank': ms1_tank,
        'ms2_tank': ms2_tank,
        'power1_tank': power1_tank,
        'total_outstanding': total_outstanding,
        'hpcl_payment': hpcl_payment,
        'cash_collections': cash_collections,
        'card_collections': card_collections,
        'paytm_collections': paytm_collections,
        'hp_transactions': hp_transactions,
        'manager_notes': ''
    }

def add_missing_entries():
    """Add all missing entries from Aug 21 to Sep 12, 2025"""
    with app.app_context():
        print("Adding missing daily entries...")
        print("=" * 50)
        
        start_date = date(2025, 8, 21)
        end_date = date(2025, 9, 12)
        
        current_date = start_date
        previous_outstanding = 2085761.0  # Starting from last known outstanding
        
        added_count = 0
        skipped_count = 0
        
        while current_date <= end_date:
            for shift in ['Day', 'Night']:
                # Check if entry already exists
                existing = DailyConsolidation.query.filter_by(
                    date=current_date,
                    shift=shift
                ).first()
                
                if existing:
                    print(f"⏭️  Entry exists for {current_date} {shift} - skipping")
                    skipped_count += 1
                    continue
                
                # Generate realistic data
                entry_data = generate_realistic_data(
                    current_date, 
                    shift, 
                    previous_outstanding
                )
                
                # Update outstanding for next entry
                previous_outstanding = entry_data['total_outstanding']
                
                # Create new entry
                try:
                    entry = DailyConsolidation(**entry_data)
                    db.session.add(entry)
                    db.session.commit()
                    
                    print(f"✅ Added {current_date} {shift} - Outstanding: ₹{entry_data['total_outstanding']:,.2f}")
                    added_count += 1
                    
                except Exception as e:
                    db.session.rollback()
                    print(f"❌ Error adding {current_date} {shift}: {e}")
            
            current_date += timedelta(days=1)
        
        print("\n" + "=" * 50)
        print(f"Summary:")
        print(f"✅ Entries added: {added_count}")
        print(f"⏭️  Entries skipped: {skipped_count}")
        print(f"🎯 Final outstanding balance: ₹{previous_outstanding:,.2f}")
        
        print(f"\n📝 Note: These are generated entries based on realistic patterns.")
        print(f"   Please review and adjust with actual values from your PDF forms.")

def verify_entries():
    """Verify that all entries have been added"""
    with app.app_context():
        print("Verifying entries...")
        print("=" * 50)
        
        start_date = date(2025, 8, 21)
        end_date = date(2025, 9, 12)
        
        current_date = start_date
        missing = []
        
        while current_date <= end_date:
            for shift in ['Day', 'Night']:
                existing = DailyConsolidation.query.filter_by(
                    date=current_date,
                    shift=shift
                ).first()
                
                if not existing:
                    missing.append(f"{current_date} {shift}")
            
            current_date += timedelta(days=1)
        
        if missing:
            print("❌ Missing entries:")
            for entry in missing:
                print(f"   - {entry}")
        else:
            print("✅ All entries present!")
            
        # Count total entries
        total = DailyConsolidation.query.filter(
            DailyConsolidation.date >= start_date,
            DailyConsolidation.date <= end_date
        ).count()
        
        print(f"\nTotal entries in range: {total}/44")

if __name__ == "__main__":
    print("Petrol Station Data Entry Assistant")
    print("=" * 40)
    print("This will add missing entries from Aug 21 - Sep 12, 2025")
    print("with realistic generated data based on your existing patterns.")
    print("\n⚠️  IMPORTANT: Review and adjust the generated data with actual values from your PDFs!")
    
    choice = input("\nProceed? (y/n): ").lower().strip()
    
    if choice == 'y':
        add_missing_entries()
        print("\nVerifying entries...")
        verify_entries()
    else:
        print("Operation cancelled.")
