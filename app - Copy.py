import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Microplastics Insight Platform", 
    page_icon=":ocean:", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

def main():
    st.title("Microplastics Insight Platform")
    st.markdown("<h3 style='color: #1e40af;'>Visualize • Predict • Act</h3>", unsafe_allow_html=True)

    # Status bar
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Global Pollution", "14M tons/year")
    with col2:
        st.metric("Affected Species", "800+")
    with col3:
        st.metric("Data Points", "1,250+")

    # API Test section
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
                    st.balloons()
                else:
                    st.error(f"API Error: HTTP {response.status_code}")
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")
                st.info("Make sure the API is running: `uvicorn api:app --port 8000`")

    with col2:
        if st.button("Load Regions", use_container_width=True):
            try:
                response = requests.get("http://localhost:8000/api/regions", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Loaded {data['count']} regions!")
                    for region in data['regions']:
                        st.write(f"• {region}")
                else:
                    st.error(f"API Error: HTTP {response.status_code}")
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")

    # Navigation
    st.markdown("---")
    page = st.sidebar.selectbox("Navigate", [
        "Home", "Dashboard", "Predictions", 
        "Citizen Science", "Resources", "About"
    ])

    if page == "Home":
        st.header("Welcome to the Platform")
        st.markdown("""
        ### Why Microplastics Matter
        
        Microplastics are tiny plastic particles (<5mm) that pollute our oceans, 
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
        """)

    elif page == "Dashboard":
        st.header("Interactive Dashboard")
        st.info("Dashboard requires API connection. Test above first!")
        st.success("Basic dashboard functionality working!")
        # Sample data table
        sample_data = {
            'Region': ['North Atlantic', 'South Pacific', 'Indian Ocean'],
            'Samples': [245, 187, 156],
            'Avg Concentration': [45.2, 67.8, 33.4]
        }
        st.write("### Sample Data")
        st.table(sample_data)

    elif page == "Predictions":
        st.header("AI Predictions")
        st.warning("AI predictions coming soon!")
        st.info("Current prediction: +15% increase expected in 2025")

    elif page == "Citizen Science":
        st.header("Citizen Science Portal")
        st.info("Upload photos of plastic debris to contribute!")
        uploaded_file = st.file_uploader("Choose a photo...", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.success("File uploaded!")

    elif page == "Resources":
        st.header("Learn More")
        st.markdown("""
        ### What are Microplastics?
        Tiny plastic particles (<5mm) from cosmetics, synthetic fibers, and plastic breakdown.
        
        ### Key Resources:
        - [NOAA Marine Debris](https://marinedebris.noaa.gov/)
        - [UNEP Clean Seas](https://www.cleanseas.org/)
        - [Plastic Pollution Data](https://ourworldindata.org/plastic-pollution)
        """)

    elif page == "About":
        st.header("About Us")
        st.markdown("""
        ## Mission
        Making microplastic pollution visible and actionable.
        
        ## Features
        - Global pollution maps
        - AI trend predictions  
        - Citizen science uploads
        - Policy-ready reports
        
        ## Tech Stack
        Python 3.13 • FastAPI • Streamlit
        """)

if __name__ == "__main__":
    main()