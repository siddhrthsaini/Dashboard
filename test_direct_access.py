#!/usr/bin/env python3
"""
Test direct Google Sheet access
"""

import gspread
from google.oauth2.service_account import Credentials
import json

def test_direct():
    try:
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        print("✅ Client authorized successfully")
        
        # Try different approaches
        sheet_id = '1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-'
        
        print(f"\n🔍 Testing different access methods for sheet ID: {sheet_id}")
        
        # Method 1: Try to open by key
        print("\n1️⃣ Trying open_by_key...")
        try:
            sheet = client.open_by_key(sheet_id)
            print(f"✅ Success: {sheet.title}")
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Method 2: Try to open by URL
        print("\n2️⃣ Trying open_by_url...")
        try:
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
            sheet = client.open_by_url(url)
            print(f"✅ Success: {sheet.title}")
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Method 3: Try to list all sheets and find it
        print("\n3️⃣ Listing all accessible sheets...")
        try:
            sheets = client.openall()
            print(f"Found {len(sheets)} sheets:")
            for sheet in sheets:
                print(f"  - {sheet.title} (ID: {sheet.id})")
                if sheet.id == sheet_id:
                    print(f"    ✅ Found target sheet!")
        except Exception as e:
            print(f"❌ Failed to list sheets: {e}")
        
        # Method 4: Try to access with different scopes
        print("\n4️⃣ Testing with different scopes...")
        try:
            scope2 = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            creds2 = Credentials.from_service_account_file('google-credentials.json', scopes=scope2)
            client2 = gspread.authorize(creds2)
            sheet = client2.open_by_key(sheet_id)
            print(f"✅ Success with readonly scope: {sheet.title}")
        except Exception as e:
            print(f"❌ Failed with readonly scope: {e}")
            
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    test_direct()
