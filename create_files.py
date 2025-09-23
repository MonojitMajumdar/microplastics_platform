(
echo import os
echo.
echo api_content = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
.
app = FastAPI(title="Microplastics Insight API", version="1.0.0")
.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8502"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
).
@app.get("/")
async def root():
    return {"message": "Microplastics Insight Platform API", "status": "running", "python_version": "3.13"}
.
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "version": "1.0.0"}
.
@app.get("/api/regions")
async def get_regions():
    regions = ["Global", "North Atlantic", "South Pacific", "Indian Ocean", "Mediterranean", "Caribbean", "Arctic", "Antarctic"]
    return {"status": "success", "count": len(regions), "regions": regions}
.
@app.get("/api/stats")
async def get_stats():
    return {
        "total_samples": 1250,
        "regions_covered": 8,
        "avg_concentration": 45.7,
        "dominant_polymer": "Polyethylene",
        "last_updated": datetime.now().isoformat()
    }
.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
'''
.
with open("api.py", "w", encoding="utf-8") as f:
    f.write(api_content)
print("✅ api.py created successfully!")
.
app_content = '''import streamlit as st
import requests
import pandas as pd
from datetime import datetime
.
st.set_page_config(
    page_title="Microplastics Insight Platform", 
    page_icon="🌊", 
    layout="wide", 
    initial_sidebar_state="expanded"
).
def main():
    st.title("🌊 Microplastics Insight Platform")
    st.markdown("<h3 style='color: #1e40af;'>Visualize • Predict • Act</h3>", unsafe_allow_html=True).
    # Status bar
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Global Pollution", "14M tons/year")
    with col2:
        st.metric("Affected Species", "800+")
    with col3:
        st.metric("Data Points", "1,250+").
    # API Test section
    st.markdown("---")
    st.subheader("🔌 API Connection Test")
    col1, col2 = st.columns(2).
    with col1:
        if st.button("🧪 Test API Health", use_container_width=True):
            try:
                response = requests.get("http://localhost:8000/health", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ API is running!")
                    st.json(data)
                    st.balloons()
                else:
                    st.error(f"❌ API Error: HTTP {response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")
                st.info("💡 Make sure the API is running: `uvicorn api:app --port 8000`").
    with col2:
        if st.button("🌍 Load Regions", use_container_width=True):
            try:
                response = requests.get("http://localhost:8000/api/regions", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Loaded {data['count']} regions!")
                    for region in data['regions']:
                        st.write(f"• {region}")
                else:
                    st.error(f"❌ API Error: HTTP {response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}").
    # Navigation
    st.markdown("---")
    page = st.sidebar.selectbox("Navigate", [
        "🏠 Home", "📊 Dashboard", "🔮 Predictions", 
        "👥 Citizen Science", "📚 Resources", "👥 About"
    ]).
    if page == "🏠 Home":
        st.header("Welcome to the Platform")
        st.markdown("""
        ### Why Microplastics Matter
        
        Microplastics are tiny plastic particles (^<5mm^) that pollute our oceans, 
        rivers, and even our food chain. This platform helps you:
        
        - **Visualize** global pollution patterns
        - **Predict** future trends with AI
        - **Report** debris through citizen science
        - **Act** with data-driven insights for cleanup
        
        ---
        
        **Quick Stats:**
        - 14 million tons of plastic enter oceans annually
        - 800+ marine species affected
        - Found in 88% of surface ocean waters
        - Detected in human blood and lungs
        """).
    elif page == "📊 Dashboard":
        st.header("📊 Interactive Dashboard")
        st.info("💡 Dashboard requires API connection. Test above first!").
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
                        st.metric("Avg Concentration", f"{stats['avg_concentration']:.1f} particles/m³")
                    with col4:
                        st.metric("Dominant Polymer", stats['dominant_polymer'])
                else:
                    st.error("Failed to load stats from API").
                # Sample table
                sample_data = {
                    'Region': ['North Atlantic', 'South Pacific', 'Indian Ocean', 'Mediterranean', 'Caribbean'],
                    'Samples': [245, 187, 156, 98, 203],
                    'Avg Conc': [45.2, 67.8, 33.4, 89.1, 52.6],
                    'Dominant Polymer': ['PE', 'PP', 'PS', 'PET', 'PVC']
                }
                df = pd.DataFrame(sample_data)
                st.dataframe(df, use_container_width=True).
            except Exception as e:
                st.error(f"Error loading data: {str(e)}").
    elif page == "🔮 Predictions":
        st.header("🔮 AI Predictions")
        st.warning("AI predictions coming soon! Requires ML packages.")
        st.info("Current prediction: +15% increase expected in 2025 for high-risk regions.").
    elif page == "👥 Citizen Science":
        st.header("👥 Citizen Science Portal")
        st.info("📷 Upload photos of plastic debris to contribute to global monitoring!")
        uploaded_file = st.file_uploader("Choose a photo...", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.success("✅ File uploaded! (GPS extraction coming soon)").
    elif page == "📚 Resources":
        st.header("📚 Learn More")
        st.markdown("""
        ### What are Microplastics?
        Tiny plastic particles (^<5mm^) from:
        - **Primary**: Microbeads in cosmetics
        - **Secondary**: Breakdown of larger plastics
        
        ### Key Sources
        - Laundry fibers: 35%
        - Tire wear: 28%
        - Cosmetics: 2%
        - Fishing gear: 10%
        
        ### Impacts
        - 800+ marine species affected
        - Enters human food chain
        - Carries toxins (heavy metals, POPs)
        
        ### Resources
        - [NOAA Marine Debris Program](https://marinedebris.noaa.gov/)
        - [UNEP Clean Seas](https://www.cleanseas.org/)
        - [Our World in Data - Plastics](https://ourworldindata.org/plastic-pollution)
        """).
    elif page == "👥 About":
        st.header("👥 About Us")
        col1, col2 = st.columns(2).
        with col1:
            st.markdown("""
            ## Our Mission
            **"Making microplastic pollution visible, predictable, and actionable"**
            
            We collect scattered microplastics data from global sources and transform 
            it into actionable insights for researchers, policymakers, NGOs, and citizens.
            
            ### Why We Built This
            1. **Data Fragmentation**: Scattered datasets, different formats
            2. **Public Awareness**: Complex science, limited accessibility
            3. **Action Gap**: No clear path from data to decision-making
            """).
        with col2:
            st.markdown("""
            ## 🌟 Features
            ✅ Interactive global maps
            ✅ AI-powered predictions
            ✅ Citizen science uploads
            ✅ Automated reports
            ✅ Educational resources
            
            ## 🛠️ Technology
            - **Backend**: FastAPI (Python 3.13)
            - **Frontend**: Streamlit
            - **Data**: NOAA + Citizen Science
            - **AI**: scikit-learn
            """).
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: #6b7280;'>Built with ❤️ for ocean conservation</p>", unsafe_allow_html=True).
if __name__ == "__main__":
    main()
'''
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_content)
print("✅ app.py created successfully!").
print("✅ Both files created - test with: python -m py_compile api.py && python -m py_compile app.py")
) > create_files.py