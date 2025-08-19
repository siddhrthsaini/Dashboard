import streamlit as st
import pandas as pd
import altair as alt
import gspread
from google.oauth2.service_account import Credentials
import os

# Configure page for faster loading
st.set_page_config(
    page_title="Progress Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapsed for faster loading
)

# Add caching for better performance
@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_google_sheet_fast(sheet_url, worksheet_name):
    """Fast cached version of Google Sheets loading"""
    try:
        if not os.path.exists('google-credentials.json'):
            return None
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        sheet_id = sheet_url.split('/')[5]
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(worksheet_name)
        
        all_records = worksheet.get_all_records()
        return pd.DataFrame(all_records)
        
    except Exception as e:
        st.error(f"Error loading {worksheet_name}: {str(e)}")
        return None

# Main app
st.title("📊 Progress Dashboard")

# Simplified sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Google Sheets URL (pre-filled)
    default_sheet_url = "https://docs.google.com/spreadsheets/d/186RIUMro2AO0JofZjJFRV6HSLpGQN1PDJeTsqBYXde4/edit?usp=sharing"
    sheet_url = st.text_input("🔗 Google Sheet URL", value=default_sheet_url)

# Load data with loading indicator
if sheet_url and os.path.exists('google-credentials.json'):
    with st.spinner("🔄 Loading data..."):
        df1 = load_google_sheet_fast(sheet_url, "JNG V2.0_GTM Dashboard")
        df2 = load_google_sheet_fast(sheet_url, "Summary")
    
    if df1 is not None:
        st.success(f"✅ Loaded {len(df1)} rows from Dashboard")
        
        # Quick summary metrics
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
            
            with col1:
                st.metric("Total", total)
            with col2:
                st.metric("Completed", completed)
            with col3:
                st.metric("In Progress", in_progress)
            with col4:
                st.metric("Not Started", not_started)
        
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
                color='Status:N'
            ).properties(height=300)
            
            st.altair_chart(chart, use_container_width=True)
        
        # Strategic Pillars Summary
        pillar_col = None
        for col in df1.columns:
            if 'pillar' in col.lower() or 'strategic' in col.lower():
                pillar_col = col
                break
        
        if pillar_col and status_col:
            st.subheader("🏛️ Strategic Pillars Summary")
            
            # Create summary
            pillar_summary = df1.groupby(pillar_col)[status_col].value_counts().unstack(fill_value=0).reset_index()
            
            # Ensure all status columns exist
            for status in ['Completed', 'In Progress', 'Not Started']:
                if status not in pillar_summary.columns:
                    pillar_summary[status] = 0
            
            # Calculate totals
            pillar_summary['Total'] = pillar_summary[['Completed', 'In Progress', 'Not Started']].sum(axis=1)
            pillar_summary['% Completed'] = (pillar_summary['Completed'] / pillar_summary['Total'] * 100).round(1)
            
            # Rename and reorder
            pillar_summary = pillar_summary.rename(columns={pillar_col: "Strategic Pillar"})
            pillar_summary = pillar_summary[["Strategic Pillar", "Total", "Completed", "In Progress", "Not Started", "% Completed"]]
            
            st.dataframe(pillar_summary, use_container_width=True)
        
        # Main data table
        st.subheader("📋 Detailed Data")
        st.dataframe(df1, use_container_width=True)
        
    else:
        st.error("❌ Could not load data from Google Sheets")
        
else:
    st.error("❌ Google credentials not found or invalid URL")
    st.info("Please ensure google-credentials.json is in the app folder and the URL is correct.")

st.caption("🚀 Fast deployment version - optimized for Streamlit Cloud")
