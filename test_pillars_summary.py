#!/usr/bin/env python3
"""
Test the Strategic Pillars Summary functionality
"""

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def test_pillars_summary():
    try:
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        # Sheet URL
        sheet_url = "https://docs.google.com/spreadsheets/d/186RIUMro2AO0JofZjJFRV6HSLpGQN1PDJeTsqBYXde4/edit?usp=sharing"
        sheet_id = sheet_url.split('/')[5]
        
        print("🔍 Testing Strategic Pillars Summary...")
        
        # Open the sheet
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet("JNG V2.0_GTM Dashboard")
        
        # Get all data
        all_records = worksheet.get_all_records()
        df = pd.DataFrame(all_records)
        
        print(f"✅ Loaded {len(df)} rows from main tracker")
        print(f"Columns: {list(df.columns)}")
        
        # Find the pillar and status columns
        pillar_col = None
        status_col = None
        
        for col in df.columns:
            if 'pillar' in col.lower() or 'strategic' in col.lower():
                pillar_col = col
            elif 'status' in col.lower():
                status_col = col
        
        print(f"Pillar column: {pillar_col}")
        print(f"Status column: {status_col}")
        
        if pillar_col and status_col:
            # Create summary by strategic pillar using a simpler approach
            pillar_summary = df.groupby(pillar_col)[status_col].value_counts().unstack(fill_value=0).reset_index()
            
            # Ensure we have all status columns
            if 'Completed' not in pillar_summary.columns:
                pillar_summary['Completed'] = 0
            if 'In Progress' not in pillar_summary.columns:
                pillar_summary['In Progress'] = 0
            if 'Not Started' not in pillar_summary.columns:
                pillar_summary['Not Started'] = 0
            
            # Calculate totals and percentages
            pillar_summary['Total'] = pillar_summary[['Completed', 'In Progress', 'Not Started']].sum(axis=1)
            pillar_summary['% Completed'] = (pillar_summary['Completed'] / pillar_summary['Total'] * 100).round(1)
            
            # Reorder columns
            pillar_summary = pillar_summary[["Strategic Pillar", "Total", "Completed", "In Progress", "Not Started", "% Completed"]]
            
            print("\n🏛️ Strategic Pillars Summary:")
            print(pillar_summary.to_string(index=False))
            
            # Check for specific pillars mentioned
            expected_pillars = [
                "Account-Based GTM (ABM) & Client Acquisition",
                "Category Studios & Product Hooks", 
                "Channel & Distribution Build-Out",
                "Commercial & Financial Controls",
                "Compliance & Tech Stack",
                "Events & Visibility"
            ]
            
            print(f"\n📋 Found {len(pillar_summary)} strategic pillars:")
            for pillar in pillar_summary["Strategic Pillar"]:
                print(f"  • {pillar}")
            
            # Check if expected pillars are present
            found_pillars = pillar_summary["Strategic Pillar"].tolist()
            for expected in expected_pillars:
                if expected in found_pillars:
                    print(f"✅ Found: {expected}")
                else:
                    print(f"❌ Missing: {expected}")
            
            return pillar_summary
        else:
            print("❌ Could not find pillar or status columns")
            return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_pillars_summary()
