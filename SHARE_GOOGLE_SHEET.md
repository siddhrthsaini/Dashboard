# 🔗 Share Your Google Sheet with Service Account

## **Service Account Email**
Your service account email is: **`dashboard@gothic-calling-469504-k0.iam.gserviceaccount.com`**

## **Step-by-Step Instructions**

### **Step 1: Open Your Google Sheet**
1. Go to: https://docs.google.com/spreadsheets/d/1j1KMU21-H6wlrz5j2KZeqMWktrTDUJ5-/edit?usp=sharing&ouid=108501907981210363712&rtpof=true&sd=true

### **Step 2: Share the Sheet**
1. **Click the "Share" button** (top right, blue button)
2. **In the sharing dialog, add this email**:
   ```
   dashboard@gothic-calling-469504-k0.iam.gserviceaccount.com
   ```
3. **Set permission to "Editor"**
4. **Uncheck "Notify people"** (important!)
5. **Click "Share"**

### **Step 3: Verify Access**
After sharing, run this command to test:
```bash
python test_google_sheets.py
```

## **Expected Result**
You should see:
```
✅ Successfully connected to: JNG_GTM Strategy_v8.25_Dashboard-Tracker
📊 Found 2 worksheets:
   - Dashboard
   - Summary
✅ Dashboard sheet loaded: X rows
✅ Summary sheet loaded: Y rows
🎉 Connection test completed successfully!
```

## **If You Still Get Errors**
1. **Make sure the email is exactly**: `dashboard@gothic-calling-469504-k0.iam.gserviceaccount.com`
2. **Check that permission is set to "Editor"**
3. **Verify the Google Sheets API is enabled in Google Cloud Console**
4. **Wait a few minutes** for permissions to propagate

## **Next Steps After Success**
1. **Test connection**: `python test_google_sheets.py`
2. **Run dashboard**: `streamlit run app.py`
3. **Select "☁️ Google Sheets"** in sidebar
4. **Enjoy live updates!**
