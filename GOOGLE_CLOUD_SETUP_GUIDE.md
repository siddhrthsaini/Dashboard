# 🔧 Google Cloud Console Setup - Visual Guide

## **Complete Step-by-Step Setup**

### **Step 1: Access Google Cloud Console**

1. **Go to**: https://console.cloud.google.com/
2. **Sign in** with your Google account
3. **Accept terms** if prompted

### **Step 2: Create New Project**

1. **Click "Select a project"** (top of page)
2. **Click "New Project"**
3. **Enter project details**:
   - **Project name**: `streamlit-dashboard`
   - **Project ID**: `streamlit-dashboard-123` (auto-generated)
4. **Click "Create"**

### **Step 3: Enable Google Sheets API**

1. **In your project, go to "APIs & Services" → "Library"**
2. **Search for "Google Sheets API"**
3. **Click on "Google Sheets API"**
4. **Click "Enable"** (blue button)

### **Step 4: Create Service Account**

1. **Go to "APIs & Services" → "Credentials"**
2. **Click "Create Credentials" → "Service Account"**
3. **Fill in service account details**:
   - **Service account name**: `streamlit-dashboard`
   - **Service account ID**: `streamlit-dashboard-123` (auto-generated)
   - **Description**: `Service account for Streamlit dashboard`
4. **Click "Create and Continue"**
5. **Skip role assignment** → Click "Continue"
6. **Skip user access** → Click "Done"

### **Step 5: Generate JSON Key**

1. **Click on your service account** (streamlit-dashboard)
2. **Go to "Keys" tab**
3. **Click "Add Key" → "Create new key"**
4. **Select "JSON" format**
5. **Click "Create"**
6. **File will download automatically**

### **Step 6: Prepare Credentials File**

1. **Find the downloaded file** (usually in Downloads folder)
2. **Rename it to**: `google-credentials.json`
3. **Move it to your project folder** (same folder as app.py)

### **Step 7: Share Google Sheet**

1. **Open your Google Sheet**: https://docs.google.com/spreadsheets/d/1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-/edit?usp=sharing&ouid=108501907981210363712&rtpof=true&sd=true

2. **Click "Share" button** (top right, blue button)

3. **Get service account email**:
   - Open `google-credentials.json` in a text editor
   - Find the `client_email` field
   - Copy the email (looks like: `streamlit-dashboard-123@project-id.iam.gserviceaccount.com`)

4. **Add to Google Sheet**:
   - Paste the service account email in the sharing dialog
   - Set permission to **"Editor"**
   - **Uncheck "Notify people"**
   - Click **"Share"**

## **🔍 What to Look For**

### **In google-credentials.json:**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "streamlit-dashboard-123@your-project-id.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

### **File Structure After Setup:**
```
gtm_dashboard_streamlit/
├── app.py
├── app_simple.py
├── google-credentials.json  ← This file should be here
├── requirements.txt
└── ... (other files)
```

## **✅ Verification Steps**

### **1. Check File Location:**
```bash
ls -la google-credentials.json
```

### **2. Test Connection:**
```bash
python test_google_sheets.py
```

### **3. Expected Output:**
```
🔍 Testing Google Sheets Connection...
==================================================
📋 Sheet ID: 1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-
✅ Successfully connected to: JNG_GTM Strategy_v8.25_Dashboard-Tracker
📊 Found 2 worksheets:
   - Dashboard
   - Summary
✅ Dashboard sheet loaded: 25 rows
✅ Summary sheet loaded: 10 rows
🎉 Connection test completed successfully!
```

## **🚨 Common Issues & Solutions**

### **"File not found"**
- Make sure `google-credentials.json` is in the same folder as `app.py`
- Check the file name (exactly `google-credentials.json`)

### **"Permission denied"**
- Verify the service account email has "Editor" access to the Google Sheet
- Check that Google Sheets API is enabled

### **"Worksheet not found"**
- Ensure your Google Sheet has sheets named "Dashboard" and "Summary"
- Check the sharing permissions

### **"Authentication failed"**
- Verify the JSON file is complete and not corrupted
- Check that the service account was created correctly

## **🎯 Next Steps After Setup**

1. **Test the connection**: `python test_google_sheets.py`
2. **Run the dashboard**: `streamlit run app.py`
3. **Select "☁️ Google Sheets"** in the sidebar
4. **Enjoy live updates!**

---

**Need help?** Check the troubleshooting section or run the test script to verify your setup.
