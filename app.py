
import streamlit as st
import pandas as pd
import altair as alt
from io import StringIO
import gspread
from google.oauth2.service_account import Credentials
import time
import os

# Configure page
st.set_page_config(
    page_title="Progress Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add caching for Google Sheets data to improve performance
def load_google_sheet_cached(sheet_url, worksheet_name):
    """Cached version of load_google_sheet for better performance"""
    return load_google_sheet(sheet_url, worksheet_name)

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
        
        # Open the sheet
        sheet = client.open_by_key(sheet_id)
        
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            st.error(f"Worksheet '{worksheet_name}' not found in the Google Sheet.")
            return None
        
        # Special handling for Summary sheet to avoid duplicate column errors
        if worksheet_name == "Summary":
            # Get all values and manually process to avoid duplicate columns
            all_values = worksheet.get_all_values()
            
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
            
            # Remove completely empty rows and columns
            df = df.dropna(axis=1, how='all')
            df = df.dropna(axis=0, how='all')
            
            # For Summary sheet, only keep the first two columns to avoid duplicates
            if len(df.columns) >= 2:
                df = df.iloc[:, :2]
                df.columns = ['Summary Metric', 'Value']
            
        else:
            # For other sheets, use standard method
            all_records = worksheet.get_all_records()
            df = pd.DataFrame(all_records)
        
        return df
        
    except Exception as e:
        st.error(f"Error loading {worksheet_name}: {str(e)}")
        st.write(f"Exception type: {type(e)}")
        import traceback
        st.write(f"Traceback: {traceback.format_exc()}")
        return None

@st.cache_data
def load_csv(file):
    if file is None:
        return None
    return pd.read_csv(file)

@st.cache_data
def load_csv_path(path):
    try:
        return pd.read_csv(path)
    except Exception:
        return None

st.title("📊 Progress Dashboard")
st.caption("Built with Streamlit. Connect to Google Sheets for live updates or upload CSVs.")

# Add auto-refresh option
with st.sidebar:
    st.header("Data Sources")
    
    # Data source selection
    data_source = st.radio(
        "Choose data source:",
        ["📁 Local CSV Files", "☁️ Google Sheets (Live Updates)"],
        index=1  # Default to Google Sheets since it's working
    )
    
    # Auto-refresh toggle (disabled for faster deployment)
    auto_refresh = st.checkbox("🔄 Auto-refresh every 30 seconds", value=False)
    if auto_refresh:
        st.info("Auto-refresh enabled! Data will update automatically.")
        time.sleep(30)  # Simple refresh mechanism
        st.rerun()
    
    if data_source == "📁 Local CSV Files":
        st.write("Upload CSVs **or** auto-load by filename in the app folder.")
        up_df1 = st.file_uploader("Main Tracker (JNG_GTM_Dashboard-Tracker.csv)", type=["csv"], key="df1")
        up_df2 = st.file_uploader("Pillar Summary (Book1.csv)", type=["csv"], key="df2")
        up_df3 = st.file_uploader("Summary Metrics (Book2.csv)", type=["csv"], key="df3")

        # Toggle to use local files if present
        use_local = st.checkbox("Use local CSV files in current folder", value=True)
        st.markdown("""
        **Expected filenames**
        - `JNG_GTM_Dashboard-Tracker.csv`
        - `Book1.csv`
        - `Book2.csv`
        """)
        
        # Load data (uploaded takes precedence; fallback to local filenames)
        df1 = load_csv(up_df1) if up_df1 else (load_csv_path("JNG_GTM_Dashboard-Tracker.csv") if use_local else None)
        df2 = load_csv(up_df2) if up_df2 else (load_csv_path("Book1.csv") if use_local else None)
        df3 = load_csv(up_df3) if up_df3 else (load_csv_path("Book2.csv") if use_local else None)
        
    else:  # Google Sheets mode
        st.markdown("### ☁️ Google Sheets Setup")
        
        # Check if credentials exist
        if os.path.exists('google-credentials.json'):
            st.success("✅ Google credentials found!")
            
            # Pre-filled with the working Google Sheet URL
            default_sheet_url = "https://docs.google.com/spreadsheets/d/186RIUMro2AO0JofZjJFRV6HSLpGQN1PDJeTsqBYXde4/edit?usp=sharing"
            
            sheet_url = st.text_input(
                "Google Sheet URL:",
                value=default_sheet_url,
                help="Your Google Sheet URL (pre-filled with working sheet)"
            )
            
            if sheet_url:
                with st.spinner("🔄 Loading data from Google Sheets..."):
                    # Load both sheets: "JNG V2.0_GTM Dashboard" and "Summary"
                    df1 = load_google_sheet_cached(sheet_url, "JNG V2.0_GTM Dashboard")  # Main tracker data
                    df2 = load_google_sheet_cached(sheet_url, "Summary")    # Summary data
                    df3 = df2  # Use df2 for summary metrics
                
                # Debug information
                st.write(f"Debug: df1 is None: {df1 is None}")
                st.write(f"Debug: df2 is None: {df2 is None}")
                
                if df1 is not None:
                    st.success(f"✅ Successfully loaded Dashboard sheet with {len(df1)} rows")
                else:
                    st.error("❌ Failed to load Dashboard sheet")
                    
                if df2 is not None:
                    st.success(f"✅ Successfully loaded Summary sheet with {len(df2)} rows")
                else:
                    st.error("❌ Failed to load Summary sheet")
                    
            else:
                df1, df2, df3 = None, None, None
                
        else:
            st.error("❌ Google credentials not found!")
            st.markdown("""
            **Setup Required:**
            1. Follow the `google_sheets_setup.md` guide
            2. Download `google-credentials.json`
            3. Place it in this folder
            4. Restart the app
            """)
            df1, df2, df3 = None, None, None

# Minimal schema handling
def normalize_columns(df):
    if df is None:
        return None
    df.columns = [c.strip() for c in df.columns]
    return df

df1 = normalize_columns(df1)
df2 = normalize_columns(df2)
df3 = normalize_columns(df3)

# If df1 exists, infer choices
if df1 is not None:
    # Try to standardize expected column names
    col_map = {}
    for c in df1.columns:
        lc = c.lower()
        if "strategic pillar" in lc or "pillar" in lc:
            col_map["pillar"] = c
        elif "kpi" in lc or "metric" in lc:
            col_map["metric"] = c
        elif "responsible" in lc or "owner" in lc:
            col_map["owner"] = c
        elif "status" in lc:
            col_map["status"] = c
        elif "frequency" in lc:
            col_map["frequency"] = c
        elif "tat" in lc or "target" in lc:
            col_map["target"] = c
        elif "action" in lc:
            col_map["action"] = c

    # Build filter UI
    st.subheader("🔎 Filters")
    with st.expander("Show/Hide Filters", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        pillar_vals = sorted(df1[col_map.get("pillar")].dropna().unique()) if "pillar" in col_map else []
        status_vals = sorted(df1[col_map.get("status")].dropna().unique()) if "status" in col_map else []
        owner_vals = sorted(df1[col_map.get("owner")].dropna().unique()) if "owner" in col_map else []
        with col1:
            sel_pillars = st.multiselect("Strategic Pillar", options=pillar_vals, default=pillar_vals)
        with col2:
            sel_status = st.multiselect("Status", options=status_vals, default=status_vals)
        with col3:
            sel_owner = st.multiselect("Owner", options=owner_vals, default=owner_vals)
        with col4:
            search = st.text_input("Search KPI / Metric (contains)", "")

    # Apply filters
    filt = pd.Series([True] * len(df1))
    if "pillar" in col_map and sel_pillars:
        filt &= df1[col_map["pillar"]].isin(sel_pillars)
    if "status" in col_map and sel_status:
        filt &= df1[col_map["status"]].isin(sel_status)
    if "owner" in col_map and sel_owner:
        filt &= df1[col_map["owner"]].isin(sel_owner)
    if "metric" in col_map and search.strip():
        filt &= df1[col_map["metric"]].astype(str).str.contains(search, case=False, na=False)

    df1_f = df1[filt].copy()

    # ---- KPI cards (from df3 if present else compute from df1) ----
    st.subheader("📌 Summary KPIs")
    if df3 is not None and set(["Summary Metric","Value"]).issubset(set(df3.columns)):
        kpi_map = {row["Summary Metric"]: row["Value"] for _, row in df3.iterrows()}
        total = int(kpi_map.get("Total Deliverables", len(df1)))
        not_started = int(kpi_map.get("Not Started (count)", (df1[col_map["status"]]=="Not Started").sum() if "status" in col_map else 0))
        in_progress = int(kpi_map.get("In Progress (count)", (df1[col_map["status"]]=="In Progress").sum() if "status" in col_map else 0))
        completed = int(kpi_map.get("Completed (count)", (df1[col_map["status"]]=="Completed").sum() if "status" in col_map else 0))
        pct_completed = float(kpi_map.get("% Completed", round(100*completed/total,1) if total else 0))
    else:
        # Compute from df1
        total = len(df1)
        not_started = int((df1[col_map["status"]]=="Not Started").sum()) if "status" in col_map else None
        in_progress = int((df1[col_map["status"]]=="In Progress").sum()) if "status" in col_map else None
        completed = int((df1[col_map["status"]]=="Completed").sum()) if "status" in col_map else None
        pct_completed = round(100*completed/total,1) if total else 0

    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("Total Deliverables", total)
    k2.metric("Not Started", not_started)
    k3.metric("In Progress", in_progress)
    k4.metric("Completed", completed)
    k5.metric("% Completed", pct_completed if pct_completed is not None else 0)

    st.divider()

    # ---- Charts ----
    st.subheader("📈 Status Distribution")
    if "status" in col_map:
        with st.spinner("Generating charts..."):
            status_counts = df1_f[col_map["status"]].value_counts(dropna=False).rename_axis("Status").reset_index(name="Count")
            chart1 = alt.Chart(status_counts).mark_bar().encode(
                x=alt.X("Status:N", sort='-y'),
                y="Count:Q",
                tooltip=["Status:N","Count:Q"]
            ).properties(height=300)
            st.altair_chart(chart1, use_container_width=True)
    else:
        st.info("Status column not found for chart.")

    st.subheader("🏛️ Status by Strategic Pillar")
    if "pillar" in col_map and "status" in col_map:
        pivot = (df1_f.groupby([col_map["pillar"], col_map["status"]])
                 .size().reset_index(name="Count")
                 .rename(columns={col_map["pillar"]:"Pillar", col_map["status"]:"Status"}))
        chart2 = alt.Chart(pivot).mark_bar().encode(
            x=alt.X("Pillar:N", sort=alt.SortField(field="Pillar")),
            y=alt.Y("Count:Q", stack="zero"),
            color="Status:N",
            tooltip=["Pillar:N","Status:N","Count:Q"]
        ).properties(height=380)
        st.altair_chart(chart2, use_container_width=True)
    else:
        st.info("Need Pillar and Status columns for stacked bar.")

    # ---- Owner workload ----
    st.subheader("👤 Workload by Owner")
    if "owner" in col_map and "status" in col_map:
        owner_counts = (df1_f.groupby([col_map["owner"], col_map["status"]])
                        .size().reset_index(name="Count")
                        .rename(columns={col_map["owner"]:"Owner", col_map["status"]:"Status"}))
        chart3 = alt.Chart(owner_counts).mark_bar().encode(
            x=alt.X("Owner:N", sort=alt.SortField(field="Owner")),
            y=alt.Y("Count:Q", stack="zero"),
            color="Status:N",
            tooltip=["Owner:N","Status:N","Count:Q"]
        ).properties(height=320)
        st.altair_chart(chart3, use_container_width=True)
    else:
        st.info("Owner column not found for chart.")

    st.divider()

    # ---- Detailed table ----
    st.subheader("📋 Detailed Tracker")
    st.dataframe(df1_f, use_container_width=True)

    # Export filtered table
    csv = df1_f.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download filtered table as CSV", data=csv, file_name="filtered_tracker.csv", mime="text/csv")

else:
    st.warning("Could not find or load the main tracker CSV. Please upload it in the sidebar or place it next to app.py with the filename **JNG_GTM_Dashboard-Tracker.csv**.")

# Note: Basic summary data section removed - only showing Strategic Pillars Summary

# Create Strategic Pillars Summary from main tracker data
if df1 is not None and "pillar" in col_map:
    st.subheader("🏛️ Strategic Pillars Summary")
    
    # Create summary by strategic pillar using a simpler approach
    pillar_summary = df1.groupby(col_map["pillar"])[col_map["status"]].value_counts().unstack(fill_value=0).reset_index()
    
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
    
    # Rename the first column to "Strategic Pillar"
    pillar_summary = pillar_summary.rename(columns={col_map["pillar"]: "Strategic Pillar"})
    
    # Reorder columns
    pillar_summary = pillar_summary[["Strategic Pillar", "Total", "Completed", "In Progress", "Not Started", "% Completed"]]
    
    # Display strategic pillars summary
    st.dataframe(pillar_summary, use_container_width=True)
    
    # Export strategic pillars summary
    csv_pillars = pillar_summary.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Strategic Pillars Summary as CSV", data=csv_pillars, file_name="strategic_pillars_summary.csv", mime="text/csv")

st.caption("Tip: Use the sidebar to upload updated CSVs anytime.")
