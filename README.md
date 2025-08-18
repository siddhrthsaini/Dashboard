
# GTM Progress Dashboard (Streamlit)

This is a ready-made dashboard for your **GTM KPIs**. It reads three CSVs:
- `JNG_GTM_Dashboard-Tracker.csv` (main tracker)
- `Book1.csv` (pillar summary, optional)
- `Book2.csv` (summary metrics, optional)

## One-time setup (Mac)
1. Install Python 3.9+ (usually pre-installed on macOS).
2. Open **Terminal** in this folder and run:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

## One-click (double-click) on Mac
- Double-click `run_dashboard.command`. It will set up a virtual environment, install packages, and start the app.

## How to use
- Keep your CSVs next to `app.py` with the exact filenames above, **or** upload them from the sidebar.
- Use filters for **Strategic Pillar**, **Status**, **Owner**, or search by **KPI/Metric**.
- Download the filtered table via the button at the bottom.

## Notes
- If your column names are slightly different, the app tries to auto-detect by keywords (e.g., "pillar", "status", "responsible").
- The optional files (`Book1.csv`, `Book2.csv`) will be shown if present, but aren't required.
