import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os

st.title("🔍 Simple Google Sheets Test")

def load_google_sheet_simple(sheet_url, worksheet_name):
    """Simple version without caching"""
    try:
        if not os.path.exists('google-credentials.json'):
            st.error("Google credentials file not found.")
            return None
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(worksheet_name)
        
        if worksheet_name == "Summary":
            all_values = worksheet.get_all_values()
            cleaned_values = []
            max_cols = 0
            
            for row in all_values:
                while row and row[-1] == '':
                    row = row[:-1]
                cleaned_values.append(row)
                max_cols = max(max_cols, len(row))
            
            for i, row in enumerate(cleaned_values):
                while len(row) < max_cols:
                    row.append('')
                cleaned_values[i] = row
            
            df = pd.DataFrame(cleaned_values[1:], columns=cleaned_values[0])
            df = df.dropna(axis=1, how='all')
            df = df.dropna(axis=0, how='all')
            
            if len(df.columns) >= 2:
                df = df.iloc[:, :2]
                df.columns = ['Summary Metric', 'Value']
        else:
            all_records = worksheet.get_all_records()
            df = pd.DataFrame(all_records)
        
        return df
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Test
sheet_url = 'https://docs.google.com/spreadsheets/d/186RIUMro2AO0JofZjJFRV6HSLpGQN1PDJeTsqBYXde4/edit?usp=sharing'

st.write("Testing Google Sheets loading...")

df1 = load_google_sheet_simple(sheet_url, 'JNG V2.0_GTM Dashboard')
df2 = load_google_sheet_simple(sheet_url, 'Summary')

st.write(f"df1 is None: {df1 is None}")
st.write(f"df2 is None: {df2 is None}")

if df1 is not None:
    st.success(f"✅ Dashboard loaded: {len(df1)} rows")
    st.dataframe(df1.head())
else:
    st.error("❌ Dashboard failed to load")

if df2 is not None:
    st.success(f"✅ Summary loaded: {len(df2)} rows")
    st.dataframe(df2.head())
else:
    st.error("❌ Summary failed to load")
