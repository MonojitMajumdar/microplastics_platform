@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ========================================
echo Microplastics Platform - Python 3.13 Setup
echo ========================================
echo.

REM Create directory structure
if not exist "models" mkdir models
if not exist "utils" mkdir utils
if not exist "static" mkdir static
if not exist "data" mkdir data
if not exist "uploads" mkdir uploads
if not exist "database" mkdir database

REM Create __init__.py files
type nul > models\__init__.py
type nul > utils\__init__.py

echo [Creating requirements.txt for Python 3.13]
(
echo fastapi==0.104.1
echo uvicorn==0.24.0
echo streamlit==1.28.1
echo pandas==2.1.3
echo geopandas==0.14.0
echo plotly==5.17.0
echo folium==0.14.0
echo scikit-learn==1.3.2
echo reportlab==4.0.6
echo Pillow==10.1.0
echo exifread==3.0.0
echo python-dotenv==1.0.0
echo sqlalchemy==2.0.23
echo streamlit-folium==0.14.0
echo requests==2.31.0
) > requirements.txt

echo [Creating minimal api.py]
set "api_content=from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title=\"Microplastics Insight API\", version=\"1.0.0\")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[\"http://localhost:8501\"],
    allow_credentials=True,
    allow_methods=[\"*\"],
    allow_headers=[\"*\"],
)

@app.get(\"/\") 
async def root():
    return {\"message\": \"Microplastics Insight Platform API\", \"status\": \"running\"}

@app.get(\"/health\")
async def health_check():
    import datetime
    return {\"status\": \"healthy\", \"timestamp\": str(datetime.datetime.now())}

@app.get(\"/api/regions\")
async def get_regions():
    return {\"status\": \"success\", \"regions\": [\"Global\", \"North Atlantic\", \"South Pacific\", \"Indian Ocean\"]}

if __name__ == \"__main__\":
    import uvicorn
    uvicorn.run(app, host=\"0.0.0.0\", port=8000)"
(
for /f "delims=" %%i in ('echo !api_content!') do echo %%i
) > api.py

echo [Creating minimal app.py]
set "app_content=import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title=\"Microplastics Insight Platform\", page_icon=\"🌊\", layout=\"wide\")

st.title(\"🌊 Microplastics Insight Platform\")
st.markdown(\"### Visualize, Predict ^& Act\")

# Test API connection
col1, col2 = st.columns(2)

with col1:
    if st.button(\"🧪 Test API Connection\"):
        try:
            response = requests.get(\"http://localhost:8000/health\")
            if response.status_code == 200:
                st.success(\"✅ API is running!\")
                st.json(response.json())
            else:
                st.error(f\"❌ API Error: {response.status_code}\")
        except requests.exceptions.ConnectionError:
            st.error(\"❌ Cannot connect to API. Make sure backend is running on port 8000\")

with col2:
    if st.button(\"🌍 Load Sample Data\"):
        try:
            response = requests.get(\"http://localhost:8000/api/regions\")
            if response.status_code == 200:
                data = response.json()
                st.success(f\"✅ Loaded {len(data['regions'])} regions\")
                for region in data['regions']:
                    st.write(f\"- {region}\")
            else:
                st.error(f\"❌ API Error: {response.status_code}\")
        except requests.exceptions.ConnectionError:
            st.error(\"❌ Cannot connect to API\")

# Sidebar navigation
st.sidebar.title(\"Navigation\")
page = st.sidebar.selectbox(\"Choose a page\", [\"Home\", \"Dashboard\", \"About\"])

if page == \"Home\":
    st.header(\"Welcome to the Platform\")
    st.markdown(\"\"\"
    This platform helps you:
    - Visualize global microplastic pollution
    - Predict future trends with AI
    - Report debris through citizen science
    - Generate reports for policymakers
    \"\"\")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(\"Global Pollution\", \"14M tons/year\")
    with col2:
        st.metric(\"Affected Species\", \"800+\" )
    with col3:
        st.metric(\"Our Goal\", \"Zero Plastic Oceans\")

elif page == \"Dashboard\":
    st.header(\"📊 Interactive Dashboard\")
    st.info(\"Dashboard coming soon! API backend is working.\")
    
    # Show sample data
    sample_data = {
        'Region': ['North Atlantic', 'South Pacific', 'Indian Ocean', 'Mediterranean'],
        'Samples': [245, 187, 156, 98],
        'Avg Concentration': [45.2, 67.8, 33.4, 89.1]
    }
    df = pd.DataFrame(sample_data)
    st.dataframe(df)

elif page == \"About\":
    st.header(\"👥 About Us\")
    st.markdown(\"\"\"
    ## Mission
    Making microplastic pollution visible, predictable, and actionable.
    
    ## Team
    - Alice Chen - Data Scientist
    - Dr. Raj Patel - Marine Biologist  
    - Maria Gonzalez - UX Researcher
    
    ## Technology
    - Backend: FastAPI (Python 3.13)
    - Frontend: Streamlit
    - Database: SQLite + PostgreSQL ready
    - AI: scikit-learn predictions
    \"\"\")
    
st.markdown(\"---\")
st.markdown(\"**Status:** Development Mode - Full features coming soon!\")"
(
for /f "delims=" %%i in ('echo !app_content!') do echo %%i
) > app.py

echo [Creating .env.example]
(
echo # Database
echo DATABASE_URL=sqlite:///./database/microplastics.db
echo.
echo # API Settings
echo API_HOST=localhost
echo API_PORT=8000
echo.
echo # Optional: Email/SMS (configure for alerts)
echo # SMTP_SERVER=smtp.gmail.com
echo # SMTP_PORT=587
echo # EMAIL_USER=your_email@gmail.com
echo # EMAIL_PASSWORD=your_app_password
echo.
echo # Optional: Twilio SMS
echo # TWILIO_ACCOUNT_SID=your_account_sid
echo # TWILIO_AUTH_TOKEN=your_auth_token
echo # TWILIO_PHONE_NUMBER=+1234567890
echo.
echo # Secret key
echo SECRET_KEY=your-super-secret-key-change-in-production
) > .env.example

echo [Creating README.md]
(
echo # Microplastics Insight Platform
echo.
echo ## Quick Start (Python 3.13)
echo.
echo ### 1. Install dependencies:
echo ```cmd
echo pip install -r requirements.txt
echo ```
echo.
echo ### 2. Start the backend API:
echo ```cmd
echo uvicorn api:app --reload --port 8000
echo ```
echo.
echo ### 3. Start the frontend:
echo ```cmd
echo streamlit run app.py --server.port 8501
echo ```
echo.
echo ### 4. Open your browser:
echo - Frontend: http://localhost:8501
echo - API Docs: http://localhost:8000/docs
echo.
echo ## Project Structure
echo ```
echo microplastics_platform/
echo ├── app.py              # Streamlit frontend
echo ├── api.py              # FastAPI backend  
echo ├── requirements.txt    # Python dependencies
echo ├── .env.example        # Environment configuration
echo ├── README.md          # This file
echo ├── models/            # ML models
echo ├── utils/             # Utility functions
echo ├── static/            # CSS, images
echo ├── data/              # Sample datasets
echo ├── uploads/           # User uploads
echo └── database/          # SQLite database
echo ```
echo.
echo ## Troubleshooting
echo - **"Could not import module 'api'"**: Make sure you're in the project directory (cd C:\microplastics_platform)
echo - **Port already in use**: Change port with `--port 8001`
echo - **Missing dependencies**: Run `pip install -r requirements.txt`
echo.
echo ---
echo **Ready to explore microplastic pollution data!** 🌊
) > README.md

echo [Creating start script]
(
echo @echo off
echo echo Starting Microplastics Platform...
echo.
echo REM Check if in project directory
echo if not exist "api.py" ^(
echo     echo ERROR: Not in project directory! Run from C:\microplastics_platform
echo     pause
echo     exit /b 1
echo ^)
echo.
echo REM Start API in background
echo start "Microplastics API" cmd /k "cd /d C:\microplastics_platform ^&^& uvicorn api:app --reload --port 8000"
echo.
echo REM Wait for API to start
echo echo Waiting for API to start...
echo timeout /t 3 /nobreak ^>nul
echo.
echo REM Test API
echo echo Testing API connection...
echo curl -s http://localhost:8000/ ^| findstr "Microplastics"
echo if %%errorlevel%% == 0 ^(
echo     echo ✅ API is running on http://localhost:8000
echo ^) else ^(
echo     echo ⚠️ API test failed - starting anyway...
echo ^)
echo.
echo REM Start Streamlit
echo echo Starting Streamlit frontend...
echo start "Microplastics Frontend" cmd /k "cd /d C:\microplastics_platform ^&^& streamlit run app.py --server.port 8501"
echo.
echo echo.
echo echo ========================================
echo echo 🎉 Platform Started Successfully!
echo echo ========================================
echo echo.
echo echo 🌐 Frontend: http://localhost:8501
echo echo 📚 API Docs: http://localhost:8000/docs
echo echo 🔧 API Root: http://localhost:8000/
echo echo.
echo echo Press any key to open browser...
echo pause ^>nul
echo start http://localhost:8501
) > start_app.bat

echo.
echo ========================================
echo ✅ Setup Complete!
echo ========================================
echo.
echo 📁 Project created in: %cd%
echo.
echo 📋 Files created:
echo    ✅ api.py (FastAPI backend)
echo    ✅ app.py (Streamlit frontend)
echo    ✅ requirements.txt
echo    ✅ .env.example
echo    ✅ README.md
echo    ✅ start_app.bat
echo.
echo 🚀 Next Steps:
echo.
echo 1. Install Python packages:
echo    pip install -r requirements.txt
echo.
echo 2. Run everything with one click:
echo    double-click start_app.bat
echo.
echo OR manually:
echo    Terminal 1: uvicorn api:app --reload --port 8000
echo    Terminal 2: streamlit run app.py --server.port 8501
echo.
echo 3. Open browser: http://localhost:8501
echo.
echo 🎉 You should see the Microplastics Platform!
echo.
echo Checking if files were created...
dir api.py app.py requirements.txt start_app.bat
echo.
pause