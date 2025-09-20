# Data-Driven Insights Integration

## Overview
The "DATA-DRIVEN INSIGHTS" card in the React frontend (Light Carriers website) now links to a separate Streamlit dashboard application that provides detailed analytics and insights.

## Setup Instructions

### Option 1: Use the Startup Scripts (Recommended)
1. **Windows Batch File**: Double-click `start_insights.bat`
2. **PowerShell Script**: Right-click `start_insights.ps1` and select "Run with PowerShell"

### Option 2: Manual Startup
1. **Start the Insights Dashboard**:
   ```bash
   cd "D:\AIMS\Insights\Gongpals\report_line"
   streamlit run dashboardp3.py --server.port 8053
   ```

2. **Start the Comprehensive Analysis**:
   ```bash
   cd "D:\AIMS"
   streamlit run comprehensive.py --server.port 8052
   ```

## Access URLs
- **React Frontend (Light Carriers)**: http://localhost:3000
- **Comprehensive Analysis**: http://localhost:8052
- **Data-Driven Insights Dashboard**: http://localhost:8053

## Button Functionality
- Click the **"DATA-DRIVEN INSIGHTS"** card in the React frontend home page
  - Opens the insights dashboard (http://localhost:8053) in a new browser tab
  - Provides detailed analytics and data visualizations
- Click the **"COMPREHENSIVE ASSESSMENT"** card in the React frontend home page
  - Opens the comprehensive analysis (http://localhost:8052) in a new browser tab
  - Provides in-depth modern slavery analysis and statistics

## File Structure
```
D:\AIMS\
├── project\
│   ├── react_frontend\       # React frontend (port 3000)
│   │   └── src\
│   │       └── pages\
│   │           └── Home.tsx  # Home page with clickable cards
│   └── streamlit_app\
│       └── ai_analysis1.py   # AI Analysis app (unused in current setup)
├── Insights\                 # Copied from D:\Insights
│   └── Gongpals\
│       └── report_line\
│           └── dashboardp3.py # Insights dashboard (port 8053)
├── comprehensivep3.py        # Additional analysis app
├── comprehensive.py          # Comprehensive analysis (port 8052)
├── start_insights.bat        # Windows batch startup script
├── start_insights.ps1        # PowerShell startup script
└── INSIGHTS_SETUP.md         # This documentation
```

## Notes
- Both applications need to be running simultaneously
- The button uses JavaScript to open the dashboard in a new tab
- Make sure ports 8501 and 8502 are available
- The Insights folder has been copied to the AIMS directory for easier access
