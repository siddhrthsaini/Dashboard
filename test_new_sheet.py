#!/usr/bin/env python3
"""
Test connection to the new Google Sheet
"""

import gspread
from google.oauth2.service_account import Credentials
import re

def test_new_sheet():
    try:
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        print("✅ Client authorized successfully")
        
        # New sheet URL
        new_sheet_url = "https://docs.google.com/spreadsheets/d/186RIUMro2AO0JofZjJFRV6HSLpGQN1PDJeTsqBYXde4/edit?usp=sharing"
        
        # Extract sheet ID from URL
        sheet_id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', new_sheet_url)
        if sheet_id_match:
            sheet_id = sheet_id_match.group(1)
            print(f"📋 New Sheet ID: {sheet_id}")
        else:
            print("❌ Could not extract sheet ID from URL")
            return
        
        print(f"\n🔍 Testing new Google Sheet...")
        
        # Method 1: Try to open by key
        print("\n1️⃣ Trying open_by_key...")
        try:
            sheet = client.open_by_key(sheet_id)
            print(f"✅ Success: {sheet.title}")
            
            # List worksheets
            worksheets = sheet.worksheets()
            print(f"📊 Worksheets: {[ws.title for ws in worksheets]}")
            
            # Try to access the first worksheet
            try:
                first_ws = sheet.get_worksheet(0)
                data = first_ws.get_all_records()
                print(f"✅ First worksheet: {len(data)} rows")
                if data:
                    print(f"   Columns: {list(data[0].keys())}")
                    print(f"   Sample data: {data[:2]}")
            except Exception as e:
                print(f"❌ First worksheet error: {e}")
                
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Method 2: Try to open by URL
        print("\n2️⃣ Trying open_by_url...")
        try:
            sheet = client.open_by_url(new_sheet_url)
            print(f"✅ Success: {sheet.title}")
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Method 3: Try to list all accessible sheets
        print("\n3️⃣ Listing all accessible sheets...")
        try:
            sheets = client.openall()
            print(f"Found {len(sheets)} accessible sheets:")
            for sheet in sheets:
                print(f"  - {sheet.title} (ID: {sheet.id})")
                if sheet.id == sheet_id:
                    print(f"    ✅ Found your new target sheet!")
        except Exception as e:
            print(f"❌ Failed to list sheets: {e}")
            
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    test_new_sheet()
