#!/usr/bin/env python3
"""
Try different methods to access the original Google Sheet
"""

import gspread
from google.oauth2.service_account import Credentials
import re

def try_original_sheet():
    try:
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        print("✅ Client authorized successfully")
        
        # Your original sheet URL
        original_url = "https://docs.google.com/spreadsheets/d/1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-/edit?usp=sharing&ouid=108501907981210363712&rtpof=true&sd=true"
        
        # Extract sheet ID from URL
        sheet_id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', original_url)
        if sheet_id_match:
            sheet_id = sheet_id_match.group(1)
            print(f"📋 Extracted Sheet ID: {sheet_id}")
        else:
            print("❌ Could not extract sheet ID from URL")
            return
        
        print(f"\n🔍 Trying to access original sheet...")
        
        # Method 1: Try with the extracted ID
        print("\n1️⃣ Trying with extracted ID...")
        try:
            sheet = client.open_by_key(sheet_id)
            print(f"✅ Success: {sheet.title}")
            
            # List worksheets
            worksheets = sheet.worksheets()
            print(f"📊 Worksheets: {[ws.title for ws in worksheets]}")
            
            # Try to access Dashboard sheet
            try:
                dashboard = sheet.worksheet("Dashboard")
                data = dashboard.get_all_records()
                print(f"✅ Dashboard sheet: {len(data)} rows")
                if data:
                    print(f"   Columns: {list(data[0].keys())}")
            except Exception as e:
                print(f"❌ Dashboard sheet error: {e}")
            
            # Try to access Summary sheet
            try:
                summary = sheet.worksheet("Summary")
                data = summary.get_all_records()
                print(f"✅ Summary sheet: {len(data)} rows")
                if data:
                    print(f"   Columns: {list(data[0].keys())}")
            except Exception as e:
                print(f"❌ Summary sheet error: {e}")
                
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Method 2: Try with the full URL
        print("\n2️⃣ Trying with full URL...")
        try:
            sheet = client.open_by_url(original_url)
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
                    print(f"    ✅ Found your target sheet!")
        except Exception as e:
            print(f"❌ Failed to list sheets: {e}")
            
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    try_original_sheet()
