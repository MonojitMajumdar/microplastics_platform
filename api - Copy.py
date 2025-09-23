from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

app = FastAPI(title="Microplastics Insight API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8502"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
