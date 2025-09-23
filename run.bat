@echo off
echo Starting Microplastics Platform...
echo.

REM Check files exist
if not exist "api.py" (
    echo ERROR: api.py not found!
    pause
    exit /b 1
)
if not exist "app.py" (
    echo ERROR: app.py not found!
    pause
    exit /b 1
)

echo ✅ Files found
echo.

echo [1/2] Starting API on port 8000...
start "API Server" cmd /k "cd /d C:\Python313\microplastics_platform ^& C:\Python313\python.exe -m uvicorn api:app --reload --port 8000"

echo [2/2] Starting Streamlit in 3 seconds...
timeout /t 3 /nobreak >nul

start "Streamlit App" cmd /k "cd /d C:\Python313\microplastics_platform ^& C:\Python313\python.exe -m streamlit run app.py --server.port 8501"

echo.
echo 🎉 Platform Started!
echo.
echo Open: http://localhost:8501
echo.
start http://localhost:8501
pause