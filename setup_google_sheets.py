#!/usr/bin/env python3
"""
Google Sheets Connection Test Script
This script helps test the connection to your Google Sheet before running the main dashboard.
"""

import os
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def test_google_sheets_connection():
    """Test the connection to your Google Sheet"""
    
    # Your Google Sheet URL
    sheet_url = "https://docs.google.com/spreadsheets/d/1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-/edit?usp=sharing&ouid=108501907981210363712&rtpof=true&sd=true"
    
    print("🔍 Testing Google Sheets Connection...")
    print(f"Sheet URL: {sheet_url}")
    print("-" * 50)
    
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
        
        # Extract sheet ID from URL
        sheet_id = sheet_url.split('/')[5]
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
            dashboard_df = pd.DataFrame(dashboard_data)
            print(f"✅ Dashboard sheet loaded: {len(dashboard_df)} rows, {len(dashboard_df.columns)} columns")
            print(f"   Columns: {list(dashboard_df.columns)}")
        except gspread.WorksheetNotFound:
            print("❌ 'Dashboard' sheet not found!")
        
        # Test loading Summary sheet
        print("\n🔍 Testing 'Summary' sheet...")
        try:
            summary_ws = sheet.worksheet("Summary")
            summary_data = summary_ws.get_all_records()
            summary_df = pd.DataFrame(summary_data)
            print(f"✅ Summary sheet loaded: {len(summary_df)} rows, {len(summary_df.columns)} columns")
            print(f"   Columns: {list(summary_df.columns)}")
        except gspread.WorksheetNotFound:
            print("❌ 'Summary' sheet not found!")
        
        print("\n🎉 Connection test completed successfully!")
        print("You can now run your Streamlit dashboard with Google Sheets integration.")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure google-credentials.json is in the same folder")
        print("2. Check that the service account has access to the Google Sheet")
        print("3. Verify the Google Sheets API is enabled in Google Cloud Console")
        return False

if __name__ == "__main__":
    test_google_sheets_connection()
