#!/usr/bin/env python3
"""
Test the Summary data loading fix
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def test_summary_fix():
    try:
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        # Sheet URL
        sheet_url = "https://docs.google.com/spreadsheets/d/186RIUMro2AO0JofZjJFRV6HSLpGQN1PDJeTsqBYXde4/edit?usp=sharing"
        sheet_id = sheet_url.split('/')[5]
        
        print("🔍 Testing Summary Data Loading Fix...")
        
        # Open the sheet
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet("Summary")
        
        # Get all data as raw values first
        all_values = worksheet.get_all_values()
        print(f"Raw data rows: {len(all_values)}")
        print(f"Raw data columns: {len(all_values[0]) if all_values else 0}")
        
        # Clean up empty columns for Summary sheet
        cleaned_values = []
        for row in all_values:
            # Keep only non-empty columns
            cleaned_row = [cell for cell in row if cell.strip()]
            if cleaned_row:  # Only add rows that have some data
                cleaned_values.append(cleaned_row)
        
        print(f"Cleaned data rows: {len(cleaned_values)}")
        
        if len(cleaned_values) < 2:
            print("❌ Insufficient data in Summary worksheet")
            return None
        
        # Create DataFrame manually
        df = pd.DataFrame(cleaned_values[1:], columns=cleaned_values[0])
        
        print(f"✅ Successfully created DataFrame with {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        print("\nData preview:")
        print(df.head())
        
        # Test the summary metrics
        if 'Summary Metric' in df.columns and 'Value' in df.columns:
            print("\n📊 Summary Metrics:")
            for _, row in df.iterrows():
                print(f"  {row['Summary Metric']}: {row['Value']}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_summary_fix()
