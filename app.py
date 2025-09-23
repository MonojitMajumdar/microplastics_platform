import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random
import time

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

def save_chemical_library(df, file_path='data/chemical_library.csv'):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving: {e}")
        return False

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
    st.subheader("API Connection Test (Simulated)")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Test API Health", use_container_width=True):
            data = {"status": "healthy", "timestamp": datetime.now().isoformat(), "version": "1.0.0"}
            st.success("API is running (simulated)!")
            st.json(data)

    with col2:
        if st.button("Load Regions", use_container_width=True):
            data = {"status": "success", "count": 8, "regions": ["Global", "North Atlantic", "South Pacific", "Indian Ocean", "Mediterranean", "Caribbean", "Arctic", "Antarctic"]}
            st.success(f"Loaded {data['count']} regions!")
            for region in data['regions']:
                st.write(f"- {region}")

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
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%I:%M %p IST, %B %d, %Y')}")  # Current date/time: 10:22 AM IST, September 23, 2025

    elif page == "Dashboard":
        st.header("Interactive Dashboard")
        st.info("Dashboard uses simulated data since API is not hosted separately.")
        
        if st.button("Load Sample Data", use_container_width=True):
            stats = {
                "total_samples": 1250,
                "regions_covered": 8,
                "avg_concentration": 45.7,
                "dominant_polymer": "Polyethylene",
                "last_updated": datetime.now().isoformat()
            }
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Samples", f"{stats['total_samples']:,}")
            with col2:
                st.metric("Regions", stats['regions_covered'])
            with col3:
                st.metric("Avg Concentration", f"{stats['avg_concentration']:.1f}")
            with col4:
                st.metric("Dominant Polymer", stats['dominant_polymer'])

            sample_data = {
                'Region': ['North Atlantic', 'South Pacific', 'Indian Ocean'],
                'Samples': [245, 187, 156],
                'Avg Concentration': [45.2, 67.8, 33.4]
            }
            df = pd.DataFrame(sample_data)
            st.dataframe(df, use_container_width=True)

    elif page == "Polymer Library":
        st.header("Polymer Chemical Library")
        
        chemical_df = load_chemical_library()
        
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("Current Chemical Library")
            if not chemical_df.empty:
                st.success(f"Loaded {len(chemical_df)} chemicals")
                st.dataframe(chemical_df, use_container_width=True)
                
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
                        if save_chemical_library(new_df):
                            st.success("Data saved!")
                            st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        st.markdown("---")
        st.subheader("Polymer Search")
        
        if not chemical_df.empty:
            search_term = st.text_input("Search polymers or diseases:", placeholder="e.g., Polyethylene or Cancer")
            
            if search_term:
                filtered = chemical_df[chemical_df['Chemical_Name'].str.contains(search_term, case=False) | 
                                     chemical_df['Associated_Disease'].str.contains(search_term, case=False)]
                
                if not filtered.empty:
                    st.success(f"Found {len(filtered)} matches")
                    st.dataframe(filtered, use_container_width=True)
                else:
                    st.warning("No matches found")
            
            st.subheader("All Chemicals")
            for idx, row in chemical_df.iterrows():
                with st.expander(row['Chemical_Name']):
                    st.write(f"**Diseases:** {row['Associated_Disease']}")
                    st.write(f"**FTIR Peaks:** {row['cm?¹']}")
            
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
        st.markdown(f"**Last Checked:** {datetime.now().strftime('%I:%M %p IST, %B %d, %Y')}")  # Current date/time

    elif page == "Citizen Science":
        st.header("👥 Citizen Science Portal")
        st.info("📷 Upload photos or 🔬 scan with Raman spectrometer to contribute to global monitoring!")
        
        tab_photo, tab_raman = st.tabs(["📸 Photo Upload", "🔬 Raman Scan"])
        
        with tab_photo:
            uploaded_file = st.file_uploader("Upload Photo of Debris", type=['jpg', 'jpeg', 'png'])
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Photo", use_column_width=True)
                st.success("Photo uploaded!")
                
                debris_type = st.selectbox("Debris Type", ["Plastic Bag", "Bottle", "Net", "Other"])
                location = st.text_input("Location")
                notes = st.text_area("Notes")
                
                if st.button("Submit Photo Report"):
                    st.success(f"Report submitted: {debris_type} at {location}")
        
        with tab_raman:
            st.subheader("🔬 Handheld Raman Spectrometer")
            st.markdown("**Scan microplastics in the field!** Place sample in collection window and get instant polymer identification.")
            
            col_left, col_right = st.columns([1, 3])
            
            with col_left:
                st.markdown("### Device Screen")
                st.markdown("**Scan Ready**")
                st.progress(1.0)
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("📚 Library", key="lib_cs"):
                        st.success("Library loaded!")
                with col_b:
                    if st.button("📊 Results", key="res_cs"):
                        st.success("Results shown!")
                st.markdown("**Depth: 2.5mm**")
                st.markdown("**Length: 15.2mm**")
            
            with col_right:
                if st.button("🔦 Start Raman Scan", type="primary", use_container_width=True):
                    with st.spinner("Scanning... (simulating Raman analysis)"):
                        time.sleep(2)
                        
                        chemical_df = load_chemical_library()
                        if not chemical_df.empty:
                            scanned_polymer = random.choice(chemical_df['Chemical_Name'].tolist())
                            row = chemical_df[chemical_df['Chemical_Name'] == scanned_polymer].iloc[0]
                            
                            st.success(f"✅ Scan Complete: **{scanned_polymer}** Detected!")
                            
                            col_res1, col_res2 = st.columns(2)
                            with col_res1:
                                st.metric("Polymer Type", scanned_polymer)
                                st.metric("Risk Level", f"{len(row['Associated_Disease'])} Diseases")
                            with col_res2:
                                if len(row['cm?¹']) > 0:
                                    st.metric("Primary Peak", f"{row['cm?¹'][0]} cm⁻¹")
                                st.metric("Confidence", "98%")
                            
                            st.subheader("Associated Health Risks")
                            for disease in row['Associated_Disease'][:3]:
                                st.warning(f"• {disease}")
                            if len(row['Associated_Disease']) > 3:
                                st.info(f"... +{len(row['Associated_Disease'])-3} more risks")
                            
                            st.subheader("FTIR Spectral Peaks")
                            peaks = row['cm?¹'] if isinstance(row['cm?¹'], list) else str(row['cm?¹']).split(', ')
                            for peak in peaks[:5]:
                                st.code(f"{peak.strip()} cm⁻¹", language=None)
                            
                            if st.button("📤 Submit Scan Data to Platform", use_container_width=True):
                                st.success("✅ Scan data submitted to global database!")
                                st.balloons()
                                st.info(f"Contributed {scanned_polymer} data from field analysis")
                        else:
                            st.error("No chemical library data - upload CSV first in Polymer Library!")
                
                with st.expander("ℹ️ What is Raman Spectroscopy?"):
                    st.markdown("""
                    **Raman spectroscopy** uses laser light to identify molecular composition:
                    
                    **How it works:**
                    1. Laser beam hits sample
                    2. Molecules scatter light with unique "fingerprint" wavelengths  
                    3. Device detects scattered light pattern
                    4. Matches to known polymer spectra (like your cm⁻¹ library)
                    
                    **Perfect for microplastics because:**
                    - Non-destructive (no sample prep needed)
                    - Works on <20μm particles
                    - Identifies PE, PP, PVC, PET in seconds
                    - Field-portable (no lab required)
                    
                    **Matches your library peaks:** 1440 cm⁻¹ (PE), 809 cm⁻¹ (PP), etc.
                    """)
        
        with st.expander("📋 Contribution Guide"):
            st.markdown("""
            ### How to Contribute with Raman Scanner
            
            **Photo Upload:**
            1. Take clear photo of debris
            2. Tag type, location, notes
            3. Submit to global map
            
            **Raman Scan:**
            1. Power on device (press power key)
            2. Place sample in collection window
            3. Press "Start Raman Scan" button
            4. View instant polymer identification
            5. Submit spectral data to platform
            
            **What we do:**
            - Add to global polymer database
            - Update chemical library with real spectra
            - Generate hotspot alerts
            - Support scientific research
            - Create policy reports
            
            **Recommended devices:** Metrohm MIRA DS, B&W Tek NanoRam
            """)

    elif page == "Resources":
        st.header("Microplastics Resources")
        st.markdown("Learn about microplastics, their sources, impacts, and solutions.")

    elif page == "About":
        st.header("About Us")
        st.markdown("A Microplastics Insight Platform - Making ocean pollution visible and actionable. DYPIU-Monojit-M ")

if __name__ == "__main__":
    main()