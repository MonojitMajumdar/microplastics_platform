echo import os > generate_files.py
echo. >> generate_files.py
echo with open('api.py', 'w', encoding='utf-8') as f: >> generate_files.py
echo     f.write('''from fastapi import FastAPI >> generate_files.py
echo from fastapi.middleware.cors import CORSMiddleware >> generate_files.py
echo from datetime import datetime >> generate_files.py
echo import uvicorn >> generate_files.py
echo . >> generate_files.py
echo app = FastAPI^(title="Microplastics Insight API", version="1.0.0"^) >> generate_files.py
echo . >> generate_files.py
echo app.add_middleware^( >> generate_files.py
echo     CORSMiddleware, >> generate_files.py
echo     allow_origins=^["http://localhost:8501", "http://localhost:8502"^], >> generate_files.py
echo     allow_credentials=True, >> generate_files.py
echo     allow_methods=^["*"^], >> generate_files.py
echo     allow_headers=^["*"^] >> generate_files.py
echo ^) >> generate_files.py
echo . >> generate_files.py
echo @app.get^^("/"^) >> generate_files.py
echo async def root^(^): >> generate_files.py
echo     return ^^{"message": "Microplastics Insight Platform API", "status": "running", "python_version": "3.13"}^^} >> generate_files.py
echo . >> generate_files.py
echo @app.get^("/health"^) >> generate_files.py
echo async def health_check^(^): >> generate_files.py
echo     return ^^{"status": "healthy", "timestamp": datetime.now^(^.isoformat^%^, "version": "1.0.0"}^^} >> generate_files.py
echo . >> generate_files.py
echo if __name__ == "__main__": >> generate_files.py
echo     uvicorn.run^(app, host="0.0.0.0", port=8000, log_level="info"^) >> generate_files.py
echo . >> generate_files.py
echo print^('✅ api.py created!'^) >> generate_files.py