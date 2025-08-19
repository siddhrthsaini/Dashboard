#!/usr/bin/env python3
"""
Debug Summary sheet data
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def debug_summary():
    try:
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        # Sheet URL
        sheet_url = "https://docs.google.com/spreadsheets/d/186RIUMro2AO0JofZjJFRV6HSLpGQN1PDJeTsqBYXde4/edit?usp=sharing"
        sheet_id = sheet_url.split('/')[5]
        
        print("🔍 Debugging Summary Sheet...")
        print(f"Sheet ID: {sheet_id}")
        
        # Open the sheet
        sheet = client.open_by_key(sheet_id)
        print(f"Sheet Title: {sheet.title}")
        
        # List all worksheets
        worksheets = sheet.worksheets()
        print(f"Worksheets: {[ws.title for ws in worksheets]}")
        
        # Check Summary worksheet
        print("\n📊 Checking Summary worksheet...")
        try:
            summary_ws = sheet.worksheet("Summary")
            print(f"✅ Found Summary worksheet")
            
            # Get all data
            all_data = summary_ws.get_all_values()
            print(f"Raw data rows: {len(all_data)}")
            print(f"Raw data columns: {len(all_data[0]) if all_data else 0}")
            
            # Show first few rows
            print("\nFirst 5 rows of raw data:")
            for i, row in enumerate(all_data[:5]):
                print(f"Row {i+1}: {row}")
            
            # Try to get records
            try:
                records = summary_ws.get_all_records()
                print(f"\nRecords: {len(records)}")
                if records:
                    print(f"Record columns: {list(records[0].keys())}")
                    print("First 3 records:")
                    for i, record in enumerate(records[:3]):
                        print(f"Record {i+1}: {record}")
                else:
                    print("No records found - might be empty or header issues")
            except Exception as e:
                print(f"Error getting records: {e}")
                
        except Exception as e:
            print(f"❌ Error accessing Summary worksheet: {e}")
        
        # Check if there are other worksheets that might contain summary data
        print("\n🔍 Checking all worksheets for summary data...")
        for ws in worksheets:
            print(f"\nWorksheet: {ws.title}")
            try:
                data = ws.get_all_values()
                print(f"  Rows: {len(data)}")
                if data:
                    print(f"  Columns: {len(data[0])}")
                    print(f"  First row: {data[0]}")
            except Exception as e:
                print(f"  Error: {e}")
                
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    debug_summary()
