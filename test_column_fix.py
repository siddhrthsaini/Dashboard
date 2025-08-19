#!/usr/bin/env python3
"""
Test the column names fix
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def test_column_fix():
    try:
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        # Sheet URL
        sheet_url = "https://docs.google.com/spreadsheets/d/186RIUMro2AO0JofZjJFRV6HSLpGQN1PDJeTsqBYXde4/edit?usp=sharing"
        sheet_id = sheet_url.split('/')[5]
        
        print("🔍 Testing Column Names Fix...")
        
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
        
        # Find the maximum number of columns
        max_cols = max(len(row) for row in cleaned_values)
        
        # Pad rows to have the same number of columns
        padded_values = []
        for row in cleaned_values:
            padded_row = row + [''] * (max_cols - len(row))
            padded_values.append(padded_row)
        
        # Create DataFrame manually
        df = pd.DataFrame(padded_values[1:], columns=padded_values[0])
        
        print(f"Original columns: {list(df.columns)}")
        
        # Remove completely empty columns and rows
        df = df.dropna(axis=1, how='all')
        df = df.dropna(axis=0, how='all')
        
        print(f"After dropna columns: {list(df.columns)}")
        
        # Fix duplicate column names by making them unique
        df.columns = pd.Index(df.columns).str.replace('', f'Column_{pd.Index(df.columns).get_loc("")}', regex=False)
        df.columns = [f"{col}_{i}" if df.columns.tolist().count(col) > 1 else col for i, col in enumerate(df.columns)]
        
        print(f"After fixing duplicates: {list(df.columns)}")
        
        # Keep only the first two columns (Summary Metric and Value)
        if len(df.columns) >= 2:
            df = df.iloc[:, :2]
            df.columns = ['Summary Metric', 'Value']
        
        print(f"Final columns: {list(df.columns)}")
        print(f"✅ Successfully created DataFrame with {len(df)} rows")
        print("\nData preview:")
        print(df.head())
        
        # Test that it can be displayed
        try:
            # Simulate what Streamlit would do
            df.to_csv('test_output.csv', index=False)
            print("✅ DataFrame can be converted to CSV successfully")
        except Exception as e:
            print(f"❌ Error converting to CSV: {e}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_column_fix()
