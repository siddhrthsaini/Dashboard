import streamlit as st
import pandas as pd
import altair as alt
import gspread
from google.oauth2.service_account import Credentials
import os
import time

# Page config
st.set_page_config(
    page_title="Progress Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cache data loading for 10 minutes
@st.cache_data(ttl=600)
def load_google_sheet_fast(sheet_url, worksheet_name):
    """Load data from Google Sheets with minimal processing"""
    try:
        if not os.path.exists('google-credentials.json'):
            st.error("Google credentials file not found. Please add google-credentials.json to the project folder.")
            return None
        
        # Authenticate
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        # Extract sheet ID from URL
        sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        sheet = client.open_by_key(sheet_id)
        
        # Get worksheet
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            st.error(f"Worksheet '{worksheet_name}' not found in the Google Sheet.")
            return None
        
        # Get data
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Main app
st.title("📊 Progress Dashboard")
st.caption("🚀 Super Fast Version - Optimized for Streamlit Cloud")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    sheet_url = st.text_input(
        "Google Sheet URL",
        value="https://docs.google.com/spreadsheets/d/186RIUMro2AO0JofZjJFRV6HSLpGQN1PDJeTsqBYXde4/edit?usp=sharing",
        help="Enter your Google Sheet URL"
    )

# Load data with loading spinner
with st.spinner("🔄 Loading data from Google Sheets..."):
    df1 = load_google_sheet_fast(sheet_url, "JNG V2.0_GTM Dashboard")

if df1 is None:
    st.error("❌ Failed to load data. Please check your Google Sheet URL and credentials.")
    st.stop()

# Quick summary metrics
st.subheader("📌 Quick Summary")
col1, col2, col3, col4 = st.columns(4)

# Find status column
status_col = None
for col in df1.columns:
    if 'status' in col.lower():
        status_col = col
        break

if status_col:
    total = len(df1)
    completed = len(df1[df1[status_col] == 'Completed'])
    in_progress = len(df1[df1[status_col] == 'In Progress'])
    not_started = len(df1[df1[status_col] == 'Not Started'])
    
    col1.metric("Total", total)
    col2.metric("Completed", completed)
    col3.metric("In Progress", in_progress)
    col4.metric("Not Started", not_started)
else:
    col1.metric("Total Records", len(df1))
    col2.metric("Columns", len(df1.columns))
    col3.metric("Status Column", "Not Found")
    col4.metric("Data Loaded", "✅")

# Strategic Pillars Summary
st.subheader("🏛️ Strategic Pillars Summary")

# Find pillar column
pillar_col = None
for col in df1.columns:
    if 'pillar' in col.lower():
        pillar_col = col
        break

if pillar_col and status_col:
    # Create summary
    pillar_summary = df1.groupby(pillar_col)[status_col].value_counts().unstack(fill_value=0).reset_index()
    
    # Ensure all status columns exist
    for status in ['Completed', 'In Progress', 'Not Started']:
        if status not in pillar_summary.columns:
            pillar_summary[status] = 0
    
    # Calculate totals and percentages
    pillar_summary['Total'] = pillar_summary[['Completed', 'In Progress', 'Not Started']].sum(axis=1)
    pillar_summary['% Completed'] = (pillar_summary['Completed'] / pillar_summary['Total'] * 100).round(1)
    
    # Rename pillar column
    pillar_summary = pillar_summary.rename(columns={pillar_col: "Strategic Pillar"})
    
    # Display
    st.dataframe(pillar_summary, use_container_width=True)
else:
    st.info("Strategic Pillar or Status column not found in the data.")

# Simple status chart
if status_col:
    st.subheader("📈 Status Distribution")
    status_counts = df1[status_col].value_counts()
    chart_data = pd.DataFrame({
        'Status': status_counts.index,
        'Count': status_counts.values
    })
    
    chart = alt.Chart(chart_data).mark_bar().encode(
        x='Status:N',
        y='Count:Q',
        tooltip=['Status', 'Count']
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)

# Basic data table
st.subheader("📋 Data Table")
st.dataframe(df1, use_container_width=True)

st.caption("🚀 Super Fast Version - Ready for Streamlit Cloud deployment!")
