#!/usr/bin/env python3
"""
Simple Google Sheets Test
"""

import gspread
from google.oauth2.service_account import Credentials
import json

def test_simple():
    try:
        # Load credentials
        with open('google-credentials.json', 'r') as f:
            creds_data = json.load(f)
        
        print("✅ Credentials loaded successfully")
        print(f"Service Account Email: {creds_data['client_email']}")
        
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        print("✅ Client authorized successfully")
        
        # Try to list all accessible sheets
        print("\n📋 Listing accessible sheets...")
        try:
            sheets = client.openall()
            print(f"Found {len(sheets)} accessible sheets:")
            for sheet in sheets:
                print(f"  - {sheet.title} (ID: {sheet.id})")
        except Exception as e:
            print(f"❌ Error listing sheets: {e}")
        
        # Try to access the specific sheet
        sheet_id = '1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-'
        print(f"\n🔍 Trying to access sheet ID: {sheet_id}")
        
        try:
            sheet = client.open_by_key(sheet_id)
            print(f"✅ Successfully opened: {sheet.title}")
            
            # List worksheets
            worksheets = sheet.worksheets()
            print(f"📊 Worksheets: {[ws.title for ws in worksheets]}")
            
            # Try to access Dashboard sheet
            try:
                dashboard = sheet.worksheet("Dashboard")
                data = dashboard.get_all_records()
                print(f"✅ Dashboard sheet: {len(data)} rows")
            except Exception as e:
                print(f"❌ Dashboard sheet error: {e}")
            
            # Try to access Summary sheet
            try:
                summary = sheet.worksheet("Summary")
                data = summary.get_all_records()
                print(f"✅ Summary sheet: {len(data)} rows")
            except Exception as e:
                print(f"❌ Summary sheet error: {e}")
                
        except Exception as e:
            print(f"❌ Error accessing sheet: {e}")
            
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    test_simple()
