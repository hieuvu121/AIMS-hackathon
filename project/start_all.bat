@echo off
echo Starting Django Backend...
start cmd /k "cd django_backend && python manage.py runserver"

echo Starting React Frontend...
start cmd /k "cd react_frontend && npm start"

echo Starting Streamlit App...
start cmd /k "cd streamlit_app && streamlit run streamlit_app.py --server.port 8501"

echo All services initiated.
echo You can access:
echo   - React Frontend: http://localhost:3000 (or similar)
echo   - Django Backend: http://localhost:8000
echo   - Streamlit App:  http://localhost:8501
pause