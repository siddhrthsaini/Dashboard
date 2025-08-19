#!/usr/bin/env python3
"""
Simple Google Sheets Connection Test
Run this to verify your Google Sheets setup before using the dashboard.
"""

import os
import gspread
from google.oauth2.service_account import Credentials

def test_connection():
    """Test the Google Sheets connection"""
    
    print("🔍 Testing Google Sheets Connection...")
    print("=" * 50)
    
    # Check if credentials file exists
    if not os.path.exists('google-credentials.json'):
        print("❌ ERROR: google-credentials.json not found!")
        print("Please follow the google_sheets_setup.md guide to set up credentials.")
        return False
    
    try:
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        # Your Google Sheet ID
        sheet_id = '1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-'
        print(f"📋 Sheet ID: {sheet_id}")
        
        # Open the sheet
        sheet = client.open_by_key(sheet_id)
        print(f"✅ Successfully connected to: {sheet.title}")
        
        # List all worksheets
        worksheets = sheet.worksheets()
        print(f"📊 Found {len(worksheets)} worksheets:")
        for ws in worksheets:
            print(f"   - {ws.title}")
        
        # Test loading Dashboard sheet
        print("\n🔍 Testing 'Dashboard' sheet...")
        try:
            dashboard_ws = sheet.worksheet("Dashboard")
            dashboard_data = dashboard_ws.get_all_records()
            print(f"✅ Dashboard sheet loaded: {len(dashboard_data)} rows")
            if dashboard_data:
                print(f"   Columns: {list(dashboard_data[0].keys())}")
        except gspread.WorksheetNotFound:
            print("❌ 'Dashboard' sheet not found!")
        
        # Test loading Summary sheet
        print("\n🔍 Testing 'Summary' sheet...")
        try:
            summary_ws = sheet.worksheet("Summary")
            summary_data = summary_ws.get_all_records()
            print(f"✅ Summary sheet loaded: {len(summary_data)} rows")
            if summary_data:
                print(f"   Columns: {list(summary_data[0].keys())}")
        except gspread.WorksheetNotFound:
            print("❌ 'Summary' sheet not found!")
        
        print("\n🎉 Connection test completed successfully!")
        print("You can now run: streamlit run app.py")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure google-credentials.json is in the same folder")
        print("2. Check that the service account has access to the Google Sheet")
        print("3. Verify the Google Sheets API is enabled in Google Cloud Console")
        return False

if __name__ == "__main__":
    test_connection()
