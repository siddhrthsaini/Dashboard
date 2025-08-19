#!/usr/bin/env python3
"""
Create a test Google Sheet to verify API access
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def create_test_sheet():
    try:
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        print("✅ Client authorized successfully")
        
        # Create a new test sheet
        print("📝 Creating test Google Sheet...")
        test_sheet = client.create('Test Dashboard Data')
        
        print(f"✅ Created test sheet: {test_sheet.title}")
        print(f"📋 Sheet ID: {test_sheet.id}")
        print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{test_sheet.id}/edit")
        
        # Get the first worksheet
        worksheet = test_sheet.get_worksheet(0)
        
        # Add some test data
        test_data = [
            ['Strategic Pillar', 'KPI / Metric', 'Status', 'Owner'],
            ['Account-Based GTM', 'Top-100 Target List', 'In Progress', 'MD'],
            ['Category Studios', '3D-First Sampling', 'Not Started', 'COO'],
            ['Channel & Distribution', 'US Pool Partners', 'Completed', 'SCM']
        ]
        
        worksheet.update('A1:D4', test_data)
        print("✅ Added test data to sheet")
        
        # Test reading the data back
        data = worksheet.get_all_records()
        print(f"✅ Successfully read {len(data)} rows from test sheet")
        
        # Create a second worksheet for summary data
        summary_worksheet = test_sheet.add_worksheet(title="Summary", rows=10, cols=5)
        summary_data = [
            ['Metric', 'Value'],
            ['Total Items', '3'],
            ['In Progress', '1'],
            ['Completed', '1'],
            ['Not Started', '1']
        ]
        summary_worksheet.update('A1:B5', summary_data)
        print("✅ Added summary worksheet with test data")
        
        print("\n🎉 Test sheet created successfully!")
        print(f"📊 You can now use this sheet for testing: https://docs.google.com/spreadsheets/d/{test_sheet.id}/edit")
        
        # Save the test sheet ID for later use
        with open('test_sheet_id.txt', 'w') as f:
            f.write(test_sheet.id)
        
        print(f"📝 Test sheet ID saved to: test_sheet_id.txt")
        
        return test_sheet.id
        
    except Exception as e:
        print(f"❌ Error creating test sheet: {e}")
        return None

if __name__ == "__main__":
    create_test_sheet()
