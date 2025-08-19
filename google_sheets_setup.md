# Google Sheets Integration Setup Guide

## Your Google Sheet Structure
Your Google Sheet already has the correct structure:
- **Dashboard sheet**: Main tracker data (equivalent to JNG_GTM_Dashboard-Tracker.csv)
- **Summary sheet**: Summary metrics and KPIs

**Sheet URL**: https://docs.google.com/spreadsheets/d/1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-/edit?usp=sharing&ouid=108501907981210363712&rtpof=true&sd=true

## Step 1: Set Up Google Sheets API

### 1.1 Go to Google Cloud Console
1. **Visit [console.cloud.google.com](https://console.cloud.google.com/)**
2. **Sign in with your Google account**
3. **Create a new project** (or select existing)

### 1.2 Enable Google Sheets API
1. **Go to "APIs & Services" → "Library"**
2. **Search for "Google Sheets API"**
3. **Click on "Google Sheets API"**
4. **Click "Enable"**

### 1.3 Create Service Account
1. **Go to "APIs & Services" → "Credentials"**
2. **Click "Create Credentials" → "Service Account"**
3. **Fill in the details:**
   - **Service account name**: `streamlit-dashboard`
   - **Service account ID**: `streamlit-dashboard-123` (auto-generated)
   - **Description**: `Service account for Streamlit dashboard`
4. **Click "Create and Continue"**
5. **Skip role assignment** (click "Continue")
6. **Skip user access** (click "Done")

### 1.4 Download JSON Key
1. **Click on your service account** (streamlit-dashboard)
2. **Go to "Keys" tab**
3. **Click "Add Key" → "Create new key"**
4. **Select "JSON" format**
5. **Click "Create"**
6. **Download the JSON file**
7. **Rename it to `google-credentials.json`**
8. **Place it in your project folder** (same folder as app.py)

## Step 2: Share Your Google Sheet

1. **Open your Google Sheet**: https://docs.google.com/spreadsheets/d/1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-/edit?usp=sharing&ouid=108501907981210363712&rtpof=true&sd=true

2. **Click "Share" button** (top right)

3. **Add your service account email**:
   - Open the downloaded `google-credentials.json` file
   - Find the `client_email` field (looks like: `streamlit-dashboard-123@project-id.iam.gserviceaccount.com`)
   - Copy this email address

4. **In Google Sheets sharing dialog**:
   - Paste the service account email
   - Set permission to **"Editor"**
   - **Uncheck "Notify people"**
   - Click **"Share"**

## Step 3: Test the Connection

1. **Place `google-credentials.json` in your project folder**
2. **Run the test script**:
   ```bash
   python -c "
   import gspread
   from google.oauth2.service_account import Credentials
   scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
   creds = Credentials.from_service_account_file('google-credentials.json', scopes=scope)
   client = gspread.authorize(creds)
   sheet = client.open_by_key('1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-')
   print('✅ Successfully connected to:', sheet.title)
   print('📊 Worksheets:', [ws.title for ws in sheet.worksheets()])
   "
   ```

## Step 4: Run Your Dashboard with Google Sheets

1. **Stop your current dashboard** (Ctrl+C)
2. **Run the full version**:
   ```bash
   streamlit run app.py
   ```
3. **In the sidebar, select "☁️ Google Sheets (Live Updates)"**
4. **The URL should be pre-filled**
5. **Data will load automatically from both sheets**

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

## Troubleshooting

### "Google credentials file not found"
- Make sure `google-credentials.json` is in the same folder as `app.py`
- Check the file name (exactly `google-credentials.json`)

### "Worksheet not found"
- Verify your Google Sheet has sheets named "Dashboard" and "Summary"
- Check the sharing permissions

### "Permission denied"
- Make sure the service account email has "Editor" access
- Check that the Google Sheets API is enabled

## Benefits:
- ✅ Live updates when Excel changes
- ✅ No manual CSV uploads needed
- ✅ Real-time collaboration
- ✅ Automatic data synchronization
- ✅ Both Dashboard and Summary sheets loaded automatically
