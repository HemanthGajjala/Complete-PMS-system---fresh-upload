#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, DailyConsolidation
from datetime import datetime, date

with app.app_context():
    # Get all existing entries after 2025-08-19
    entries = DailyConsolidation.query.filter(
        DailyConsolidation.date > date(2025, 8, 19)
    ).order_by(DailyConsolidation.date, DailyConsolidation.shift).all()

    print('Existing entries after 2025-08-19:')
    for entry in entries:
        print(f'{entry.date} - {entry.shift} - Manager: {entry.manager or "N/A"}')

    print(f'\nTotal entries found: {len(entries)}')
    
    # Show latest entry
    if entries:
        latest = entries[-1]
        print(f'\nLatest entry: {latest.date} - {latest.shift}')
    
    # Check what dates are missing from Aug 21 to Sep 12
    from datetime import timedelta
    start_date = date(2025, 8, 21)
    end_date = date(2025, 9, 12)
    
    existing_dates = set((entry.date, entry.shift) for entry in entries)
    
    print('\nMissing entries:')
    current_date = start_date
    while current_date <= end_date:
        for shift in ['Day', 'Night']:
            if (current_date, shift) not in existing_dates:
                print(f'{current_date} - {shift}')
        current_date += timedelta(days=1)
