@echo off
echo Starting Microplastics Platform - Both API and Frontend...
echo.

REM Check files
if not exist "api.py" (echo ERROR: api.py missing! & pause & exit /b 1)
if not exist "app.py" (echo ERROR: app.py missing! & pause & exit /b 1)

echo ✅ Files OK

REM Start API in new window
start "API Backend - Port 8000" cmd /k "cd /d C:\Python313\microplastics_platform ^& C:\Python313\python.exe -m uvicorn api:app --reload --port 8000"

REM Wait for API to start
echo Waiting for API to start...
timeout /t 3 /nobreak >nul

REM Test API
echo Testing API...
curl -s http://localhost:8000/health | findstr "healthy"
if %errorlevel% == 0 (
    echo ✅ API ready!
) else (
    echo ⚠️ API test failed - check the API window
)

REM Start Streamlit in new window
start "Streamlit Frontend - Port 8501" cmd /k "cd /d C:\Python313\microplastics_platform ^& C:\Python313\python.exe -m streamlit run app.py --server.port 8501"

echo.
echo 🎉 Both Started!
echo.
echo 🌐 Frontend: http://localhost:8501
echo 📚 API Docs: http://localhost:8000/docs
echo.
timeout /t 2 /nobreak >nul
start http://localhost:8501
pause