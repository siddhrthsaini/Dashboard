import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os

st.title("🔍 Google Sheets Debug Test")

# Test the exact function from app.py
def load_google_sheet(sheet_url, worksheet_name):
    """Load data from Google Sheets with error handling"""
    try:
        # Check if credentials file exists
        if not os.path.exists('google-credentials.json'):
            st.error("Google credentials file not found.")
            return None
        
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        # Extract sheet ID from URL
        sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        st.write(f"Sheet ID: {sheet_id}")
        
        # Open the sheet
        sheet = client.open_by_key(sheet_id)
        st.write("✅ Sheet opened successfully")
        
        try:
            worksheet = sheet.worksheet(worksheet_name)
            st.write(f"✅ Worksheet '{worksheet_name}' opened successfully")
        except gspread.WorksheetNotFound:
            st.error(f"Worksheet '{worksheet_name}' not found in the Google Sheet.")
            return None
        
        # Special handling for Summary sheet to avoid duplicate column errors
        if worksheet_name == "Summary":
            st.write("Processing Summary sheet...")
            # Get all values and manually process to avoid duplicate columns
            all_values = worksheet.get_all_values()
            st.write(f"Got {len(all_values)} rows from Summary sheet")
            
            # Clean empty cells and ensure consistent structure
            cleaned_values = []
            max_cols = 0
            
            for row in all_values:
                # Remove empty cells from the end
                while row and row[-1] == '':
                    row = row[:-1]
                cleaned_values.append(row)
                max_cols = max(max_cols, len(row))
            
            # Pad rows to ensure consistent column count
            for i, row in enumerate(cleaned_values):
                while len(row) < max_cols:
                    row.append('')
                cleaned_values[i] = row
            
            # Create DataFrame
            df = pd.DataFrame(cleaned_values[1:], columns=cleaned_values[0])
            st.write(f"Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
            
            # Remove completely empty rows and columns
            df = df.dropna(axis=1, how='all')
            df = df.dropna(axis=0, how='all')
            st.write(f"After cleaning: {len(df)} rows and {len(df.columns)} columns")
            
            # For Summary sheet, only keep the first two columns to avoid duplicates
            if len(df.columns) >= 2:
                df = df.iloc[:, :2]
                df.columns = ['Summary Metric', 'Value']
                st.write("✅ Summary sheet processed successfully")
            
        else:
            st.write("Processing Dashboard sheet...")
            # For other sheets, use standard method
            all_records = worksheet.get_all_records()
            df = pd.DataFrame(all_records)
            st.write(f"✅ Dashboard sheet processed: {len(df)} rows")
        
        return df
        
    except Exception as e:
        st.error(f"Error loading {worksheet_name}: {str(e)}")
        st.write(f"Exception type: {type(e)}")
        import traceback
        st.write(f"Traceback: {traceback.format_exc()}")
        return None

# Test both sheets
sheet_url = 'https://docs.google.com/spreadsheets/d/186RIUMro2AO0JofZjJFRV6HSLpGQN1PDJeTsqBYXde4/edit?usp=sharing'

st.subheader("Testing Google Sheets Loading")

df1 = load_google_sheet(sheet_url, 'JNG V2.0_GTM Dashboard')
df2 = load_google_sheet(sheet_url, 'Summary')

st.subheader("Results")
st.write(f"df1 is None: {df1 is None}")
st.write(f"df2 is None: {df2 is None}")

if df1 is not None:
    st.write(f"df1 shape: {df1.shape}")
    st.write("df1 columns:", list(df1.columns))
    st.dataframe(df1.head())

if df2 is not None:
    st.write(f"df2 shape: {df2.shape}")
    st.write("df2 columns:", list(df2.columns))
    st.dataframe(df2.head())
