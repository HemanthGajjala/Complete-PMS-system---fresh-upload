#!/usr/bin/env python3

import sys
import os
import re
from datetime import datetime, date
import pdfplumber

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app, db, DailyConsolidation

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def parse_date_from_filename(filename):
    """Extract date from filename like AnyScanner_08_25_2025(1).pdf"""
    match = re.search(r'(\d{2})_(\d{2})_(\d{4})', filename)
    if match:
        month, day, year = match.groups()
        return date(int(year), int(month), int(day))
    return None

def parse_petrol_station_data(text, file_date):
    """Parse petrol station daily data from extracted text"""
    if not text:
        return None
    
    # Clean up text
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)
    
    # Initialize data structure
    data = {
        'date': file_date,
        'shift': None,
        'manager': None,
        'ms_rate': None,
        'ms_quantity': None,
        'ms_amount': None,
        'hsd_rate': None,
        'hsd_quantity': None,
        'hsd_amount': None,
        'power_rate': None,
        'power_quantity': None,
        'power_amount': None,
        'cash_collections': None,
        'card_collections': None,
        'paytm_collections': None,
        'hp_transactions': None,
        'total_outstanding': None
    }
    
    try:
        # Extract shift information
        if 'Day' in text or 'day' in text:
            data['shift'] = 'Day'
        elif 'Night' in text or 'night' in text:
            data['shift'] = 'Night'
        
        # Extract manager/bunk boy name
        # Look for patterns like "Bunk Boy: Name" or just common names
        manager_patterns = [
            r'(?:Bunk\s*Boy|Manager):\s*([A-Za-z]+)',
            r'([A-Za-z]{3,})\s*(?:shift|Shift)',
        ]
        
        for pattern in manager_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['manager'] = match.group(1).strip()
                break
        
        # Extract fuel sales data
        # Look for patterns like rates, quantities, and amounts
        
        # MS data
        ms_matches = re.findall(r'MS.*?(\d+\.?\d*)', text, re.IGNORECASE)
        if len(ms_matches) >= 3:
            data['ms_rate'] = float(ms_matches[0]) if ms_matches[0] else None
            data['ms_quantity'] = float(ms_matches[1]) if ms_matches[1] else None
            data['ms_amount'] = float(ms_matches[2]) if ms_matches[2] else None
        
        # HSD data
        hsd_matches = re.findall(r'HSD.*?(\d+\.?\d*)', text, re.IGNORECASE)
        if len(hsd_matches) >= 3:
            data['hsd_rate'] = float(hsd_matches[0]) if hsd_matches[0] else None
            data['hsd_quantity'] = float(hsd_matches[1]) if hsd_matches[1] else None
            data['hsd_amount'] = float(hsd_matches[2]) if hsd_matches[2] else None
        
        # POWER data
        power_matches = re.findall(r'POWER.*?(\d+\.?\d*)', text, re.IGNORECASE)
        if len(power_matches) >= 3:
            data['power_rate'] = float(power_matches[0]) if power_matches[0] else None
            data['power_quantity'] = float(power_matches[1]) if power_matches[1] else None
            data['power_amount'] = float(power_matches[2]) if power_matches[2] else None
        
        # Extract payment data
        # Look for cash, card, paytm, hp transactions
        cash_match = re.search(r'Cash.*?(\d+\.?\d*)', text, re.IGNORECASE)
        if cash_match:
            data['cash_collections'] = float(cash_match.group(1))
        
        card_match = re.search(r'Card.*?(\d+\.?\d*)', text, re.IGNORECASE)
        if card_match:
            data['card_collections'] = float(card_match.group(1))
        
        paytm_match = re.search(r'Paytm.*?(\d+\.?\d*)', text, re.IGNORECASE)
        if paytm_match:
            data['paytm_collections'] = float(paytm_match.group(1))
        
        hp_match = re.search(r'HP.*?(\d+\.?\d*)', text, re.IGNORECASE)
        if hp_match:
            data['hp_transactions'] = float(hp_match.group(1))
        
        # Extract outstanding balance
        outstanding_match = re.search(r'Outstanding.*?(\d+\.?\d*)', text, re.IGNORECASE)
        if outstanding_match:
            data['total_outstanding'] = float(outstanding_match.group(1))
            
    except Exception as e:
        print(f"Error parsing data: {e}")
    
    return data

def process_pdf_files():
    """Process all PDF files in the downloads directory"""
    pdf_directory = r"c:\Users\GHemanthReddy\Downloads\New folder (2)"
    
    if not os.path.exists(pdf_directory):
        print(f"Directory not found: {pdf_directory}")
        return
    
    # Get all PDF files
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf') and 'AnyScanner' in f]
    pdf_files.sort()
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    with app.app_context():
        for pdf_file in pdf_files:
            print(f"\nProcessing: {pdf_file}")
            
            # Extract date from filename
            file_date = parse_date_from_filename(pdf_file)
            if not file_date:
                print(f"Could not parse date from {pdf_file}")
                continue
                
            print(f"Date: {file_date}")
            
            # Extract text from PDF
            pdf_path = os.path.join(pdf_directory, pdf_file)
            text = extract_text_from_pdf(pdf_path)
            
            if not text:
                print(f"Could not extract text from {pdf_file}")
                continue
            
            print(f"Extracted {len(text)} characters of text")
            
            # Parse the data
            parsed_data = parse_petrol_station_data(text, file_date)
            
            if parsed_data:
                print(f"Parsed data: {parsed_data}")
                
                # For now, let's just print the parsed data
                # We'll add database insertion later after reviewing the results
            else:
                print("Failed to parse data")

if __name__ == "__main__":
    process_pdf_files()
