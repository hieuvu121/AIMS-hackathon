Write-Host "Starting Light Carriers Full Stack Application..." -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting React Frontend..." -ForegroundColor Green
Set-Location "D:\AIMS\project\react_frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start"
Write-Host "React Frontend started on http://localhost:3000" -ForegroundColor Yellow

Write-Host "`nStarting Data-Driven Insights Dashboard..." -ForegroundColor Green
Set-Location "D:\AIMS\Insights\Gongpals\report_line"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "streamlit run dashboardp3.py --server.port 8053"
Write-Host "Insights Dashboard started on http://localhost:8053" -ForegroundColor Yellow

Write-Host "`nStarting Comprehensive Analysis..." -ForegroundColor Green
Set-Location "D:\AIMS"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "streamlit run comprehensive.py --server.port 8052"
Write-Host "Comprehensive Analysis started on http://localhost:8052" -ForegroundColor Yellow

Write-Host "`nAll applications are now running!" -ForegroundColor Cyan
Write-Host "- React Frontend (Light Carriers): http://localhost:3000" -ForegroundColor White
Write-Host "- Comprehensive Analysis: http://localhost:8052" -ForegroundColor White
Write-Host "- Data-Driven Insights: http://localhost:8053" -ForegroundColor White
Write-Host "`nClick the 'Data-Driven Insights' card in the React frontend to access the dashboard!" -ForegroundColor Green
Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
