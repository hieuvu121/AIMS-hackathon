@echo off
echo Starting Light Carriers Full Stack Application...
echo.

echo Starting React Frontend...
cd /d "D:\AIMS\project\react_frontend"
start "React Frontend" cmd /k "npm start"
echo React Frontend started on http://localhost:3000
echo.

echo Starting Data-Driven Insights Dashboard...
cd /d "D:\AIMS\Insights\Gongpals\report_line"
start "Insights Dashboard" cmd /k "streamlit run dashboardp3.py --server.port 8053"
echo Insights Dashboard started on http://localhost:8053
echo.

echo Starting Comprehensive Analysis...
cd /d "D:\AIMS"
start "Comprehensive Analysis" cmd /k "streamlit run comprehensive.py --server.port 8052"
echo Comprehensive Analysis started on http://localhost:8052
echo.

echo All applications are now running!
echo - React Frontend (Light Carriers): http://localhost:3000
echo - Comprehensive Analysis: http://localhost:8052
echo - Data-Driven Insights: http://localhost:8053
echo.
echo Click the "Data-Driven Insights" card in the React frontend to access the dashboard!
pause
