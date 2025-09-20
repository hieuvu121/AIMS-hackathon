# Fullstack SmartCompliance AI Platform

This repository contains a fullstack application for SmartCompliance AI, comprising a Django backend, a React frontend, and a Streamlit application for advanced data exploration.

## Project Structure

```
project/
├── django_backend/          # Django REST API and backend services
├── react_frontend/          # React.js single-page application  
├── streamlit_app/          # Streamlit application for interactive data analysis
└── README.md               # This file
```

## Getting Started

Follow the instructions in each subdirectory's `README.md` to set up and run the individual services.

## Running All Services

To start all services simultaneously, use the provided startup scripts:

### For Windows (Batch file):
```bash
start_all.bat
```

### For PowerShell:
```powershell
.\start_all.ps1
```

This will typically start:
- Django backend (e.g., `http://localhost:8000`)
- React frontend (e.g., `http://localhost:3000`) 
- Streamlit app (e.g., `http://localhost:8501`)

## Individual Service Setup

### Django Backend
```bash
cd django_backend
pip install -r requirements.txt
python manage.py runserver
```

### React Frontend
```bash
cd react_frontend
npm install
npm start
```

### Streamlit App
```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8501
```

## Features

- **React Frontend**: Modern web interface with exploration button that links to the AI analysis platform
- **Django Backend**: REST API for data management and business logic
- **Streamlit App**: Advanced AI-powered compliance analysis and visualization platform

## Architecture

The application follows a microservices-like architecture where:
- The React frontend serves as the main user interface
- The Django backend provides API endpoints and data management
- The Streamlit app provides specialized AI analysis capabilities
- Services communicate via HTTP APIs and can be deployed independently