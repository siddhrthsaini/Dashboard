
import streamlit as st
import pandas as pd
import altair as alt
from io import StringIO
import gspread
from google.oauth2.service_account import Credentials
import time
import os

st.set_page_config(page_title="Progress Dashboard", page_icon="📊", layout="wide")

# Google Sheets setup
def load_google_sheet(sheet_url, worksheet_name):
    """Load data from Google Sheets for live updates"""
    try:
        # Check if credentials file exists
        if not os.path.exists('google-credentials.json'):
            st.error("Google credentials file not found. Please follow the setup guide.")
            return None
            
        # Set up credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        # Extract sheet ID from URL
        sheet_id = sheet_url.split('/')[5]
        sheet = client.open_by_key(sheet_id)
        
        # Try to get the specific worksheet
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            st.error(f"Worksheet '{worksheet_name}' not found. Available sheets: {[ws.title for ws in sheet.worksheets()]}")
            return None
        
        # Get all data as raw values first
        all_values = worksheet.get_all_values()
        if not all_values:
            st.warning(f"No data found in worksheet '{worksheet_name}'")
            return None
        
        # Clean up empty columns for Summary sheet
        if worksheet_name == "Summary":
            # Remove completely empty columns
            cleaned_values = []
            for row in all_values:
                # Keep only non-empty columns
                cleaned_row = [cell for cell in row if cell.strip()]
                if cleaned_row:  # Only add rows that have some data
                    cleaned_values.append(cleaned_row)
            
            if len(cleaned_values) < 2:  # Need at least header + 1 data row
                st.warning(f"Insufficient data in Summary worksheet")
                return None
            
            # Create DataFrame with only the first two columns
            if len(cleaned_values[0]) >= 2:
                # Take only the first two columns from each row
                summary_data = []
                for row in cleaned_values:
                    if len(row) >= 2:
                        summary_data.append([row[0], row[1]])
                
                # Create DataFrame
                df = pd.DataFrame(summary_data[1:], columns=['Summary Metric', 'Value'])
            else:
                st.warning(f"Insufficient columns in Summary worksheet")
                return None
        else:
            # For other sheets, use the standard method
            try:
                data = worksheet.get_all_records()
                df = pd.DataFrame(data)
            except Exception as e:
                # Fallback to manual processing if get_all_records fails
                st.warning(f"Using fallback method for {worksheet_name}: {e}")
                if len(all_values) < 2:
                    return None
                df = pd.DataFrame(all_values[1:], columns=all_values[0])
        
        st.success(f"✅ Loaded {len(df)} rows from '{worksheet_name}' sheet")
        return df
        
    except Exception as e:
        st.error(f"Google Sheets error: {e}")
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
    
    # Auto-refresh toggle
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
                st.info("🔄 Loading data from Google Sheets...")
                
                # Load both sheets: "JNG V2.0_GTM Dashboard" and "Summary"
                df1 = load_google_sheet(sheet_url, "JNG V2.0_GTM Dashboard")  # Main tracker data
                df2 = load_google_sheet(sheet_url, "Summary")    # Summary data
                df3 = None  # We'll use df2 for summary metrics
                
                if df1 is not None:
                    st.success(f"✅ Successfully loaded Dashboard sheet with {len(df1)} rows")
                if df2 is not None:
                    st.success(f"✅ Successfully loaded Summary sheet with {len(df2)} rows")
                    
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
        total = kpi_map.get("Total Deliverables", len(df1))
        not_started = kpi_map.get("Not Started (count)", int((df1[col_map["status"]]=="Not Started").sum()) if "status" in col_map else None)
        in_progress = kpi_map.get("In Progress (count)", int((df1[col_map["status"]]=="In Progress").sum()) if "status" in col_map else None)
        completed = kpi_map.get("Completed (count)", int((df1[col_map["status"]]=="Completed").sum()) if "status" in col_map else None)
        pct_completed = kpi_map.get("% Completed", round(100*completed/total,1) if total else 0)
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

# Show Summary sheet data (from Google Sheets or CSV)
if df2 is not None:
    st.subheader("📊 Summary Data")
    if data_source == "☁️ Google Sheets (Live Updates)":
        st.info("📈 Data from Google Sheets 'Summary' sheet - Updates automatically!")
    else:
        st.info("📈 Data from uploaded CSV or local file")
    
    # Display summary data nicely
    if len(df2) > 0:
        # Try to create a nice summary display
        if 'Summary Metric' in df2.columns and 'Value' in df2.columns:
            # Create summary cards
            col1, col2, col3, col4 = st.columns(4)
            
            # Find key metrics
            total_deliverables = df2[df2['Summary Metric'] == 'Total Deliverables']['Value'].iloc[0] if len(df2[df2['Summary Metric'] == 'Total Deliverables']) > 0 else 'N/A'
            not_started = df2[df2['Summary Metric'] == 'Not Started (count)']['Value'].iloc[0] if len(df2[df2['Summary Metric'] == 'Not Started (count)']) > 0 else 'N/A'
            in_progress = df2[df2['Summary Metric'] == 'In Progress (count)']['Value'].iloc[0] if len(df2[df2['Summary Metric'] == 'In Progress (count)']) > 0 else 'N/A'
            completed = df2[df2['Summary Metric'] == 'Completed (count)']['Value'].iloc[0] if len(df2[df2['Summary Metric'] == 'Completed (count)']) > 0 else 'N/A'
            
            with col1:
                st.metric("Total Deliverables", total_deliverables)
            with col2:
                st.metric("Not Started", not_started)
            with col3:
                st.metric("In Progress", in_progress)
            with col4:
                st.metric("Completed", completed)
        
        # Show the full data table
        st.dataframe(df2, use_container_width=True)
        
        # Export summary data
        csv_summary = df2.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download summary data as CSV", data=csv_summary, file_name="summary_data.csv", mime="text/csv")
    else:
        st.warning("No summary data available")

# Show raw data tables for debugging
with st.expander("🔍 Raw Data Tables (for debugging)"):
    if df1 is not None:
        st.subheader("📋 Raw Dashboard Data")
        st.dataframe(df1, use_container_width=True)
    
    if df2 is not None:
        st.subheader("📋 Raw Summary Data") 
        st.dataframe(df2, use_container_width=True)

st.caption("Tip: Use the sidebar to upload updated CSVs anytime.")
