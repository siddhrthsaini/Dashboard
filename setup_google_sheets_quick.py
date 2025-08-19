#!/usr/bin/env python3
"""
Quick Google Sheets Setup Guide
This script will help you set up Google Sheets integration step by step.
"""

import os
import webbrowser
import time

def print_step(step_num, title, description):
    """Print a formatted step"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title}")
    print(f"{'='*60}")
    print(description)
    print()

def check_credentials():
    """Check if credentials file exists"""
    if os.path.exists('google-credentials.json'):
        print("✅ google-credentials.json found!")
        return True
    else:
        print("❌ google-credentials.json not found!")
        return False

def main():
    print("🚀 Google Sheets Integration Setup")
    print("This will help you connect your dashboard to Google Sheets for live updates.")
    
    # Step 1: Introduction
    print_step(1, "Overview", 
        "You'll need to:\n"
        "1. Set up Google Cloud Console\n"
        "2. Enable Google Sheets API\n"
        "3. Create service account credentials\n"
        "4. Download and place credentials file\n"
        "5. Share your Google Sheet\n"
        "6. Test the connection")
    
    input("Press Enter to continue...")
    
    # Step 2: Google Cloud Console
    print_step(2, "Google Cloud Console Setup",
        "1. Go to Google Cloud Console\n"
        "2. Create a new project\n"
        "3. Enable Google Sheets API\n"
        "4. Create service account\n"
        "5. Download JSON credentials")
    
    print("Opening Google Cloud Console...")
    webbrowser.open("https://console.cloud.google.com/")
    
    input("Press Enter when you've completed the Google Cloud Console setup...")
    
    # Step 3: Check credentials
    print_step(3, "Check Credentials File",
        "Make sure you have downloaded google-credentials.json and placed it in this folder.")
    
    if check_credentials():
        print("Great! Credentials file is ready.")
    else:
        print("Please download google-credentials.json and place it in this folder.")
        input("Press Enter when you have the credentials file...")
        if check_credentials():
            print("✅ Credentials file found!")
        else:
            print("❌ Still no credentials file. Please check the setup guide.")
            return
    
    # Step 4: Share Google Sheet
    print_step(4, "Share Your Google Sheet",
        "1. Open your Google Sheet\n"
        "2. Click 'Share' button\n"
        "3. Add the service account email (from google-credentials.json)\n"
        "4. Give 'Editor' access\n"
        "5. Uncheck 'Notify people'")
    
    print("Opening your Google Sheet...")
    webbrowser.open("https://docs.google.com/spreadsheets/d/1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-")
    
    input("Press Enter when you've shared the Google Sheet...")
    
    # Step 5: Test connection
    print_step(5, "Test Connection",
        "Now let's test if everything is working...")
    
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key('1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-')
        print(f"✅ Successfully connected to: {sheet.title}")
        
        worksheets = sheet.worksheets()
        print(f"📊 Found worksheets: {[ws.title for ws in worksheets]}")
        
        # Test Dashboard sheet
        try:
            dashboard_ws = sheet.worksheet("Dashboard")
            dashboard_data = dashboard_ws.get_all_records()
            print(f"✅ Dashboard sheet: {len(dashboard_data)} rows")
        except:
            print("❌ Dashboard sheet not found")
        
        # Test Summary sheet
        try:
            summary_ws = sheet.worksheet("Summary")
            summary_data = summary_ws.get_all_records()
            print(f"✅ Summary sheet: {len(summary_data)} rows")
        except:
            print("❌ Summary sheet not found")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Please check your setup and try again.")
        return
    
    # Step 6: Success
    print_step(6, "Success! 🎉",
        "Google Sheets integration is working!\n\n"
        "Now you can:\n"
        "1. Run: streamlit run app.py\n"
        "2. Select '☁️ Google Sheets (Live Updates)' in the sidebar\n"
        "3. Your data will load automatically from Google Sheets\n"
        "4. Any changes in Excel will appear live in the dashboard!")
    
    print("\n🚀 Ready to run your dashboard with live Google Sheets updates!")

if __name__ == "__main__":
    main()
