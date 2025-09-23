import streamlit as st
import requests
from datetime import datetime
import os
import random
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import uvicorn
import time

# Embedded FastAPI
app_api = FastAPI(title="Microplastics Insight API", version="1.0.0")

app_api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8502"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def load_chemical_library_api():
    try:
        file_path = 'data/chemical_library.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['Chemical_Name'] = df['Chemical_Name'].str.strip()
            return df.to_dict('records')
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading chemical data: {str(e)}")

@app_api.get("/")
async def root():
    return {"message": "Microplastics Insight Platform API", "status": "running", "python_version": "3.13"}

@app_api.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "version": "1.0.0"}

@app_api.get("/api/regions")
async def get_regions():
    regions = ["Global", "North Atlantic", "South Pacific", "Indian Ocean", "Mediterranean", "Caribbean", "Arctic", "Antarctic"]
    return {"status": "success", "count": len(regions), "regions": regions}

@app_api.get("/api/stats")
async def get_stats():
    return {
        "total_samples": 1250,
        "regions_covered": 8,
        "avg_concentration": 45.7,
        "dominant_polymer": "Polyethylene",
        "last_updated": datetime.now().isoformat()
    }

@app_api.get("/api/chemicals")
async def get_chemicals(search: str = None):
    chemicals = load_chemical_library_api()
    
    if search:
        filtered = [chem for chem in chemicals 
                   if search.lower() in chem['Chemical_Name'].lower() or 
                   any(search.lower() in str(disease).lower() for disease in eval(chem['Associated_Disease']))]
        return {"status": "success", "count": len(filtered), "chemicals": filtered}
    
    return {"status": "success", "count": len(chemicals), "chemicals": chemicals}

@app_api.get("/api/chemicals/{chemical_name}")
async def get_chemical(chemical_name: str):
    chemicals = load_chemical_library_api()
    for chem in chemicals:
        if chemical_name.lower() in chem['Chemical_Name'].lower():
            return {"status": "success", "chemical": chem}
    raise HTTPException(status_code=404, detail="Chemical not found")

@app_api.post("/api/chemicals/upload")
async def upload_chemicals(file: UploadFile = File(...)):
    try:
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        df = pd.read_csv(file_path)
        required_cols = ['Chemical_Name', 'Associated_Disease', 'cm?¹']
        
        if all(col in df.columns for col in required_cols):
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

@app_api.get("/api/chemicals/download")
async def download_chemicals():
    file_path = 'data/chemical_library.csv'
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            media_type='text/csv',
            filename='chemical_library.csv'
        )
    raise HTTPException(status_code=404, detail="Chemical library not found")

# Streamlit app
st.set_page_config(
    page_title="Microplastics Insight Platform", 
    page_icon="🌊", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

def load_chemical_library(file_path='data/chemical_library.csv'):
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['Chemical_Name'] = df['Chemical_Name'].str.strip()
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def main():
    st.title("Microplastics Insight Platform")
    st.markdown("<h3 style='color: #1e40af;'>Visualize Predict Act</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Global Pollution", "14M tons/year")
    with col2:
        st.metric("Affected Species", "800+")
    with col3:
        st.metric("Data Points", "1,250+")

    st.markdown("---")
    st.subheader("API Connection Test")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Test API Health", use_container_width=True):
            try:
                response = requests.get("http://localhost:8000/health", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    st.success("API is running!")
                    st.json(data)
                else:
                    st.error(f"API Error: HTTP {response.status_code}")
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")
                st.info("Make sure API is running: uvicorn api:app --port 8000")

    with col2:
        if st.button("Load Regions", use_container_width=True):
            try:
                response = requests.get("http://localhost:8000/api/regions", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Loaded {data['count']} regions!")
                    for region in data['regions']:
                        st.write(f"- {region}")
                else:
                    st.error(f"API Error: HTTP {response.status_code}")
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")

    st.markdown("---")
    page = st.sidebar.selectbox("Navigate", [
        "Home", "Dashboard", "Polymer Library", 
        "Predictions", "Citizen Science", "Resources", "About"
    ])

    if page == "Home":
        st.header("Welcome to the Platform")
        st.markdown("Microplastics are tiny plastic particles <5mm that pollute our oceans and food chain.")
        st.markdown("- Visualize global pollution patterns")
        st.markdown("- Predict future trends with AI")
        st.markdown("- Research polymer toxicity")
        st.markdown("- Report debris through citizen science")
        st.markdown("- Act with data-driven insights")

    elif page == "Dashboard":
        st.header("Interactive Dashboard")
        st.info("Dashboard requires API connection. Test above first!")
        
        if st.button("Load Sample Data", use_container_width=True):
            try:
                response = requests.get("http://localhost:8000/api/stats", timeout=5)
                if response.status_code == 200:
                    stats = response.json()
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Samples", f"{stats['total_samples']:,}")
                    with col2:
                        st.metric("Regions", stats['regions_covered'])
                    with col3:
                        st.metric("Avg Concentration", f"{stats['avg_concentration']:.1f}")
                    with col4:
                        st.metric("Dominant Polymer", stats['dominant_polymer'])
                else:
                    st.error("Failed to load stats from API")

                sample_data = {
                    'Region': ['North Atlantic', 'South Pacific', 'Indian Ocean'],
                    'Samples': [245, 187, 156],
                    'Avg Concentration': [45.2, 67.8, 33.4]
                }
                df = pd.DataFrame(sample_data)
                st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f"Error loading data: {str(e)}")

    elif page == "Polymer Library":
        st.header("Polymer Chemical Library")
        
        # Load chemical data
        chemical_df = load_chemical_library()
        
        # Upload section
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("Current Chemical Library")
            if not chemical_df.empty:
                st.success(f"Loaded {len(chemical_df)} chemicals")
                st.dataframe(chemical_df, use_container_width=True)
                
                # Download button
                csv = chemical_df.to_csv(index=False)
                st.download_button(
                    label="Download Current Library",
                    data=csv,
                    file_name="chemical_library.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No chemical library data found")
        
        with col2:
            st.subheader("Upload New Data")
            uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
            
            if uploaded_file is not None:
                try:
                    new_df = pd.read_csv(uploaded_file)
                    st.success(f"Uploaded {len(new_df)} chemicals")
                    st.dataframe(new_df.head())
                    
                    if st.button("Save to Library", use_container_width=True):
                        os.makedirs('data', exist_ok=True)
                        new_df.to_csv('data/chemical_library.csv', index=False)
                        st.success("Data saved!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        # Search functionality
        st.markdown("---")
        st.subheader("Polymer Search")
        
        if not chemical_df.empty:
            search_term = st.text_input("Search polymers or diseases:", placeholder="e.g., Polyethylene or Cancer")
            
            if search_term:
                # Simple search
                filtered = chemical_df[chemical_df['Chemical_Name'].str.contains(search_term, case=False) | 
                                     chemical_df['Associated_Disease'].str.contains(search_term, case=False)]
                
                if not filtered.empty:
                    st.success(f"Found {len(filtered)} matches")
                    st.dataframe(filtered, use_container_width=True)
                else:
                    st.warning("No matches found")
            
            # Display all chemicals
            st.subheader("All Chemicals")
            for idx, row in chemical_df.iterrows():
                with st.expander(row['Chemical_Name']):
                    st.write(f"**Diseases:** {row['Associated_Disease']}")
                    st.write(f"**FTIR Peaks:** {row['cm?¹']}")
            
            # Statistics
            st.subheader("Library Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Chemicals", len(chemical_df))
            with col2:
                st.metric("Avg Diseases", chemical_df['Associated_Disease'].str.len().mean())
            with col3:
                st.metric("Avg Peaks", chemical_df['cm?¹'].str.len().mean())

    elif page == "Predictions":
        st.header("AI Predictions")
        st.warning("AI predictions coming soon!")

    elif page == "Resources":
        st.header("Microplastics Resources")
        st.markdown("Learn about microplastics, their sources, impacts, and solutions.")

    elif page == "About":
        st.header("About Us")
        st.markdown("A Microplastics Insight Platform - Making ocean pollution visible and actionable. DYPIU-Monojit-M ")

if __name__ == "__main__":
    main()