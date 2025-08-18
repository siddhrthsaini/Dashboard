# Google Sheets Integration Setup Guide

## Your Google Sheet Structure
Your Google Sheet already has the correct structure:
- **Dashboard sheet**: Main tracker data (equivalent to JNG_GTM_Dashboard-Tracker.csv)
- **Summary sheet**: Summary metrics and KPIs

**Sheet URL**: https://docs.google.com/spreadsheets/d/1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-/edit?usp=sharing&ouid=108501907981210363712&rtpof=true&sd=true

## Step 1: Set Up Google Sheets API

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project** (or select existing)
3. **Enable Google Sheets API:**
   - APIs & Services → Library → Search "Google Sheets API" → Enable
4. **Create Service Account:**
   - APIs & Services → Credentials → Create Credentials → Service Account
   - Name: "streamlit-dashboard"
   - Role: Project → Editor
5. **Download JSON Key:**
   - Click on service account → Keys → Add Key → JSON
   - Download the JSON file
   - **Rename it to `google-credentials.json`**
   - **Place it in your project folder**

## Step 2: Share Your Google Sheet

1. **In your Google Sheet, click "Share"**
2. **Add your service account email** (from the JSON file)
3. **Give it "Editor" access**
4. **Your sheet URL is already configured in the dashboard**

## Step 3: Test the Connection

1. **Place `google-credentials.json` in your project folder**
2. **Restart your Streamlit app**
3. **Switch to "☁️ Google Sheets" mode in the sidebar**
4. **The URL should be pre-filled**
5. **Click "Load Data" to test the connection**

## Expected Data Structure

### Dashboard Sheet (Main Tracker):
- Strategic Pillar
- KPI / Metric  
- Max out Target TAT
- Frequency
- Who is Responsible
- Status
- Action Items

### Summary Sheet (KPIs):
- Summary metrics and key performance indicators
- Progress tracking data

## Benefits:
- ✅ Live updates when Excel changes
- ✅ No manual CSV uploads needed
- ✅ Real-time collaboration
- ✅ Automatic data synchronization
- ✅ Both Dashboard and Summary sheets loaded automatically
