
# 📊 Progress Dashboard

A modern, interactive dashboard built with Streamlit for tracking project progress, KPIs, and strategic initiatives.

## 🚀 Live Demo

**Deployed on Streamlit Cloud**: [Your Dashboard URL will appear here after deployment]

## ✨ Features

- **📈 Interactive Visualizations**: Status distribution, workload analysis, and progress tracking
- **🔍 Advanced Filtering**: Filter by Strategic Pillar, Status, Owner, and search functionality
- **📊 KPI Cards**: Real-time summary metrics and progress indicators
- **📁 Multiple Data Sources**: Support for CSV files and Google Sheets integration
- **🔄 Auto-refresh**: Automatic data updates every 30 seconds
- **📱 Mobile-friendly**: Responsive design works on all devices
- **💾 Data Export**: Download filtered data as CSV files

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Git

### Local Setup
```bash
# Clone the repository
git clone https://github.com/siddhrthsaini/Dashboard.git
cd Dashboard

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app_simple.py
```

## 📊 Data Structure

The dashboard expects the following data structure:

### Main Tracker (JNG_GTM_Dashboard-Tracker.csv)
- Strategic Pillar
- KPI / Metric
- Max out Target TAT
- Frequency
- Who is Responsible
- Status
- Action Items

### Summary Data (Book1.csv, Book2.csv)
- Summary metrics and KPIs
- Progress tracking data

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Set main file path: `app_simple.py`
6. Click "Deploy"

### Local Network Access
```bash
streamlit run app_simple.py --server.port 8501 --server.address 0.0.0.0
```
Share the network URL with your team.

## 🔗 Google Sheets Integration

For live Excel updates, follow the setup guide in `google_sheets_setup.md`:

1. Set up Google Sheets API credentials
2. Download `google-credentials.json`
3. Place it in the project folder
4. Use `app.py` instead of `app_simple.py`

## 📁 Project Structure

```
Dashboard/
├── app.py                 # Full version with Google Sheets
├── app_simple.py          # Simplified version (CSV only)
├── requirements.txt       # Python dependencies
├── setup_google_sheets.py # Google Sheets connection test
├── google_sheets_setup.md # Setup guide for Google Sheets
├── DEPLOYMENT_GUIDE.md    # Deployment instructions
├── QUICK_SETUP.md         # Quick start guide
├── JNG_GTM_Dashboard-Tracker.csv  # Main data file
├── Book1.csv              # Summary data
├── Book2.csv              # Additional metrics
└── README.md              # This file
```

## 🎯 Usage

1. **Upload Data**: Use the sidebar to upload CSV files or use local files
2. **Apply Filters**: Filter by Strategic Pillar, Status, Owner, or search
3. **View Charts**: Explore interactive visualizations
4. **Export Data**: Download filtered results as CSV
5. **Auto-refresh**: Enable automatic updates

## 🔧 Configuration

### Data Sources
- **CSV Files**: Upload or use local files
- **Google Sheets**: Live updates from Google Sheets (requires setup)

### Auto-refresh
- Toggle in sidebar
- Updates every 30 seconds when enabled

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- Check the `QUICK_SETUP.md` for troubleshooting
- Review `google_sheets_setup.md` for Google Sheets integration
- Open an issue for bugs or feature requests

## 🎉 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web app framework
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [Altair](https://altair-viz.github.io/) - Data visualization
- [Google Sheets API](https://developers.google.com/sheets/api) - Live data integration
