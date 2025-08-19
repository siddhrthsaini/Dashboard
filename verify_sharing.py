#!/usr/bin/env python3
"""
Verify Google Sheet Sharing Status
"""

import json

def verify_sharing():
    print("🔍 Google Sheet Sharing Verification")
    print("=" * 50)
    
    # Load service account email
    with open('google-credentials.json', 'r') as f:
        creds = json.load(f)
    
    service_account_email = creds['client_email']
    
    print(f"Service Account Email: {service_account_email}")
    print()
    
    print("📋 SHARING CHECKLIST:")
    print("1. ✅ Google Sheets API enabled")
    print("2. ✅ Google Drive API enabled")
    print("3. ❓ Google Sheet shared with service account")
    print("4. ❓ Correct permissions set")
    print()
    
    print("🔧 TROUBLESHOOTING STEPS:")
    print()
    print("STEP 1: Verify Google Sheet URL")
    print("   Your sheet URL: https://docs.google.com/spreadsheets/d/1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-/edit")
    print()
    
    print("STEP 2: Check Sharing Settings")
    print("   1. Open your Google Sheet")
    print("   2. Click 'Share' button (top right)")
    print("   3. Look for this email in the list:")
    print(f"      {service_account_email}")
    print("   4. If NOT found, add it with 'Editor' access")
    print()
    
    print("STEP 3: Alternative Sharing Method")
    print("   If the above doesn't work, try:")
    print("   1. Make the sheet 'Anyone with the link can edit'")
    print("   2. Test the connection")
    print("   3. Then change back to specific sharing")
    print()
    
    print("STEP 4: Check Sheet Restrictions")
    print("   Some sheets have restrictions that prevent API access:")
    print("   1. Check if the sheet is in a shared drive")
    print("   2. Check if there are domain restrictions")
    print("   3. Try creating a copy of the sheet")
    print()
    
    print("🎯 QUICK FIX:")
    print("   1. Go to your Google Sheet")
    print("   2. Click 'Share'")
    print("   3. Click 'Change to anyone with the link'")
    print("   4. Set to 'Editor'")
    print("   5. Copy the link")
    print("   6. Test connection")
    print("   7. Change back to specific sharing if needed")
    print()
    
    print("📞 Need help? The issue is likely with sharing permissions.")
    print("   Try the 'Quick Fix' above first.")

if __name__ == "__main__":
    verify_sharing()
