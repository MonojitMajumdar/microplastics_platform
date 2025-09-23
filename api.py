from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
import pandas as pd
import os
import uvicorn

app = FastAPI(title="Microplastics Insight API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8502"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def load_chemical_library():
    """Load chemical library data"""
    try:
        file_path = 'data/chemical_library.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            # Clean data for API
            df['Chemical_Name'] = df['Chemical_Name'].str.strip()
            return df.to_dict('records')
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading chemical data: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Microplastics Insight Platform API", "status": "running", "python_version": "3.13"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "version": "1.0.0"}

@app.get("/api/regions")
async def get_regions():
    regions = ["Global", "North Atlantic", "South Pacific", "Indian Ocean", "Mediterranean", "Caribbean", "Arctic", "Antarctic"]
    return {"status": "success", "count": len(regions), "regions": regions}

@app.get("/api/stats")
async def get_stats():
    return {
        "total_samples": 1250,
        "regions_covered": 8,
        "avg_concentration": 45.7,
        "dominant_polymer": "Polyethylene",
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/chemicals")
async def get_chemicals(search: str = None):
    """Get chemical library data with optional search"""
    chemicals = load_chemical_library()
    
    if search:
        filtered = [chem for chem in chemicals 
                   if search.lower() in chem['Chemical_Name'].lower() or 
                   any(search.lower() in str(disease).lower() for disease in eval(chem['Associated_Disease']))]
        return {"status": "success", "count": len(filtered), "chemicals": filtered}
    
    return {"status": "success", "count": len(chemicals), "chemicals": chemicals}

@app.get("/api/chemicals/{chemical_name}")
async def get_chemical(chemical_name: str):
    """Get specific chemical data"""
    chemicals = load_chemical_library()
    for chem in chemicals:
        if chemical_name.lower() in chem['Chemical_Name'].lower():
            return {"status": "success", "chemical": chem}
    raise HTTPException(status_code=404, detail="Chemical not found")

@app.post("/api/chemicals/upload")
async def upload_chemicals(file: UploadFile = File(...)):
    """Upload new chemical library data"""
    try:
        # Save uploaded file
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Load and validate
        df = pd.read_csv(file_path)
        required_cols = ['Chemical_Name', 'Associated_Disease', 'cm?¹']
        
        if all(col in df.columns for col in required_cols):
            # Save to main library
            main_path = 'data/chemical_library.csv'
            df.to_csv(main_path, index=False)
            return {
                "status": "success",
                "message": f"Uploaded {len(df)} chemicals successfully",
                "filename": file.filename
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid CSV format")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/api/chemicals/download")
async def download_chemicals():
    """Download current chemical library"""
    file_path = 'data/chemical_library.csv'
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            media_type='text/csv',
            filename='chemical_library.csv'
        )
    raise HTTPException(status_code=404, detail="Chemical library not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")