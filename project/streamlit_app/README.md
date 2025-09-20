# Streamlit Application

This directory contains the Streamlit application for the SmartCompliance AI platform.

## Features

- AI-powered modern slavery compliance analysis
- Company risk assessment and benchmarking
- Industry trend analysis and predictions
- Interactive data visualizations
- PDF document analysis
- Real-time compliance scoring

## How to Run

1. Navigate to this directory in your terminal:
   ```bash
   cd project/streamlit_app
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run streamlit_app.py --server.port 8501
   ```

The application will be accessible in your browser, typically at `http://localhost:8501`.

## Dependencies

- streamlit
- pandas
- numpy
- plotly
- PyPDF2
- textblob
- networkx

## Usage

1. Open the application in your browser
2. Use the sidebar to configure analysis parameters
3. Upload company documents or select from the database
4. View interactive charts and compliance scores
5. Get AI-powered recommendations and insights