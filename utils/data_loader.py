import pandas as pd
import json
import os
import numpy as np
from datetime import datetime

def load_microplastics_data(file_path='data/sample_data.csv'):
    """
    Load and process microplastics data from CSV or generate sample data
    """
    try:
        if os.path.exists(file_path):
            # Load real data
            df = pd.read_csv(file_path)
        else:
            # Generate sample data matching NOAA format
            df = generate_sample_data()
            # Save sample data for future use
            df.to_csv(file_path, index=False)
            print(f"Generated sample data saved to {file_path}")
        
        # Standardize column names (NOAA format)
        column_mapping = {
            'lat': 'latitude',
            'lon': 'longitude',
            'conc': 'concentration',
            'sample_year': 'year',
            'poly_type': 'polymer_type',
            'source_type': 'source'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Ensure required columns exist
        required_cols = ['latitude', 'longitude', 'concentration', 'year', 'polymer_type', 'source']
        for col in required_cols:
            if col not in df.columns:
                if col == 'region':
                    df[col] = 'Global'
                elif col == 'concentration':
                    df[col] = np.random.uniform(1, 200, len(df))
                else:
                    df[col] = 'Unknown'
        
        # Data cleaning
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['concentration'] = pd.to_numeric(df['concentration'], errors='coerce').fillna(0)
        df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(datetime.now().year)
        
        # Add region information based on coordinates
        df['region'] = assign_regions(df['latitude'], df['longitude'])
        
        # Filter out invalid coordinates
        df = df[(df['latitude'].between(-90, 90)) & (df['longitude'].between(-180, 180))]
        
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return generate_sample_data()

def generate_sample_data(n_samples=1000):
    """Generate realistic sample microplastics data"""
    np.random.seed(42)
    
    # Generate coordinates (focus on coastal areas)
    lons = np.random.normal(0, 60, n_samples)
    lats = np.random.normal(0, 30, n_samples)
    
    # Adjust for coastal bias
    coastal_bias = np.random.exponential(1, n_samples)
    lats = np.clip(lats + coastal_bias * np.sign(lats) * 0.1, -90, 90)
    
    # Years (2010-2024)
    years = np.random.choice(range(2010, 2025), n_samples, p=np.linspace(0.05, 0.25, 15))
    
    # Concentrations (log-normal distribution)
    concentrations = np.random.lognormal(3, 1, n_samples)
    concentrations = np.clip(concentrations, 0.1, 500)
    
    # Polymer types (realistic distribution)
    polymers = np.random.choice([
        'Polyethylene (PE)', 'Polypropylene (PP)', 'Polystyrene (PS)', 
        'Polyethylene terephthalate (PET)', 'Polyvinyl chloride (PVC)',
        'Polycarbonate (PC)', 'Polyamide (PA)', 'Polyurethane (PU)'
    ], n_samples, p=[0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.05, 0.05])
    
    # Sources
    sources = np.random.choice([
        'Wastewater effluent', 'Stormwater runoff', 'Atmospheric deposition',
        'Fishing gear', 'Shipping', 'Aquaculture', 'Landfill leachate'
    ], n_samples, p=[0.25, 0.20, 0.15, 0.15, 0.10, 0.08, 0.07])
    
    # Sample dates
    base_date = datetime(2010, 1, 1)
    sample_dates = [base_date.replace(year=int(y)) + pd.Timedelta(days=np.random.randint(0, 365)) 
                    for y in years]
    
    data = pd.DataFrame({
        'sample_id': range(1, n_samples + 1),
        'latitude': lats,
        'longitude': lons,
        'concentration': concentrations,
        'sample_date': sample_dates,
        'year': years,
        'polymer_type': polymers,
        'source': sources,
        'method': np.random.choice(['Nets', 'Pumps', 'Grab samples'], n_samples),
        'depth': np.random.uniform(0, 200, n_samples),
        'salinity': np.random.uniform(25, 38, n_samples),
        'temperature': np.random.normal(15, 8, n_samples)
    })
    
    return data

def assign_regions(latitude, longitude):
    """Assign geographic regions based on coordinates"""
    regions = []
    
    for lat, lon in zip(latitude, longitude):
        if pd.isna(lat) or pd.isna(lon):
            regions.append('Unknown')
            continue
            
        if -10 <= lat <= 10:
            if -180 <= lon <= -30:
                region = 'South America Pacific'
            elif -30 <= lon <= 60:
                region = 'Atlantic'
            else:
                region = 'Indian Ocean'
        elif 10 < lat <= 60:
            if -180 <= lon <= 0:
                region = 'North America Pacific'
            elif 0 <= lon <= 60:
                region = 'Europe'
            else:
                region = 'Asia Pacific'
        elif -60 <= lat < -10:
            if -180 <= lon <= -110:
                region = 'South Pacific'
            elif -110 <= lon <= 20:
                region = 'South Atlantic'
            else:
                region = 'Indian Ocean'
        else:
            region = 'Polar Regions'
        
        regions.append(region)
    
    return regions

def get_additives_info():
    """Load polymer additives information from JSON or return sample data"""
    additives_file = 'data/additives.json'
    
    if os.path.exists(additives_file):
        with open(additives_file, 'r') as f:
            return json.load(f)
    else:
        # Generate sample additives data
        sample_additives = {
            "Polyethylene (PE)": {
                "uses": "Packaging, bottles, films",
                "degradation": "500+ years",
                "recyclable": "Yes (Type 2)",
                "risks": {
                    "Marine Life": 7,
                    "Human Health": 4,
                    "Bioaccumulation": 6
                },
                "additives": [
                    {
                        "name": "Irganox 1010",
                        "toxicity": "Low",
                        "marine_impact": "Minimal leaching",
                        "human_health": "Food contact approved"
                    },
                    {
                        "name": "Calcium Stearate",
                        "toxicity": "Low",
                        "marine_impact": "Biodegradable",
                        "human_health": "Generally recognized as safe"
                    }
                ]
            },
            "Polypropylene (PP)": {
                "uses": "Containers, automotive parts",
                "degradation": "400+ years",
                "recyclable": "Yes (Type 5)",
                "risks": {
                    "Marine Life": 6,
                    "Human Health": 3,
                    "Bioaccumulation": 5
                },
                "additives": [
                    {
                        "name": "Tinuvin 770",
                        "toxicity": "Moderate",
                        "marine_impact": "UV stabilizer, slow release",
                        "human_health": "Skin contact concerns"
                    }
                ]
            },
            "Polystyrene (PS)": {
                "uses": "Foam packaging, disposable cups",
                "degradation": "Never fully degrades",
                "recyclable": "Yes (Type 6)",
                "risks": {
                    "Marine Life": 9,
                    "Human Health": 7,
                    "Bioaccumulation": 8
                },
                "additives": [
                    {
                        "name": "HBCD (Flame Retardant)",
                        "toxicity": "High",
                        "marine_impact": "Persistent organic pollutant",
                        "human_health": "Probable carcinogen"
                    },
                    {
                        "name": "Styrene Monomer",
                        "toxicity": "High",
                        "marine_impact": "Toxic to aquatic life",
                        "human_health": "Neurotoxic, possible carcinogen"
                    }
                ]
            },
            "Polyethylene terephthalate (PET)": {
                "uses": "Bottles, clothing fibers",
                "degradation": "450+ years",
                "recyclable": "Yes (Type 1)",
                "risks": {
                    "Marine Life": 8,
                    "Human Health": 6,
                    "Bioaccumulation": 7
                },
                "additives": [
                    {
                        "name": "Antimony Trioxide",
                        "toxicity": "High",
                        "marine_impact": "Toxic to aquatic organisms",
                        "human_health": "Possible carcinogen"
                    }
                ]
            },
            "Polyvinyl chloride (PVC)": {
                "uses": "Pipes, flooring, medical devices",
                "degradation": "1000+ years",
                "recyclable": "Limited (Type 3)",
                "risks": {
                    "Marine Life": 10,
                    "Human Health": 9,
                    "Bioaccumulation": 9
                },
                "additives": [
                    {
                        "name": "DEHP (Phthalate)",
                        "toxicity": "Very High",
                        "marine_impact": "Endocrine disruptor",
                        "human_health": "Reproductive toxicity"
                    },
                    {
                        "name": "Lead Stabilizers",
                        "toxicity": "Extremely High",
                        "marine_impact": "Heavy metal contamination",
                        "human_health": "Neurotoxic"
                    }
                ]
            }
        }
        
        # Save sample data
        os.makedirs('data', exist_ok=True)
        with open(additives_file, 'w') as f:
            json.dump(sample_additives, f, indent=2)
        
        return sample_additives

def get_sample_locations(n=50):
    """Generate sample coastal locations for testing"""
    coastal_regions = [
        # North Atlantic
        (40.7, -74.0),   # New York
        (52.5, -2.0),    # UK
        (48.8, -4.3),    # France
        # South Atlantic
        (-34.6, -58.4),  # Buenos Aires
        (-23.5, -46.6),  # São Paulo
        # Mediterranean
        (41.9, 12.5),    # Rome
        (36.1, -5.4),    # Gibraltar
        # Indian Ocean
        (-33.9, 18.4),   # Cape Town
        (13.0, 80.2),    # Chennai
        # Pacific
        (35.7, 139.7),   # Tokyo
        (37.8, -122.4),  # San Francisco
        (33.7, -118.2),  # Los Angeles
        (-33.8, 151.2),  # Sydney
    ]
    
    locations = []
    for lat, lon in coastal_regions * (n // len(coastal_regions) + 1):
        # Add some variation around coastal points
        noise_lat = np.random.normal(0, 0.5)
        noise_lon = np.random.normal(0, 0.5)
        locations.append((lat + noise_lat, lon + noise_lon))
    
    return locations[:n]