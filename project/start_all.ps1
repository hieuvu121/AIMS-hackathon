Write-Host "Starting Django Backend..."
Start-Process powershell -ArgumentList "-NoExit -Command `"cd django_backend; python manage.py runserver`""

Write-Host "Starting React Frontend..."
Start-Process powershell -ArgumentList "-NoExit -Command `"cd react_frontend; npm start`""

Write-Host "Starting Streamlit App..."
Start-Process powershell -ArgumentList "-NoExit -Command `"cd streamlit_app; streamlit run streamlit_app.py --server.port 8501`""

Write-Host "All services initiated."
Write-Host "You can access:"
Write-Host "  - React Frontend: http://localhost:3000 (or similar)"
Write-Host "  - Django Backend: http://localhost:8000"
Write-Host "  - Streamlit App:  http://localhost:8501"