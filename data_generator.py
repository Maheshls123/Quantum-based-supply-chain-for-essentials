import pandas as pd
import numpy as np

def generate_warehouses():
    """Generates mock warehouse data."""
    warehouses = [
        {"id": "W1", "name": "Central Hub Alpha", "lat": 40.7128, "lon": -74.0060, "capacity": 5000, "stock": 4200},
        {"id": "W2", "name": "Northside Storage", "lat": 40.7580, "lon": -73.9855, "capacity": 3000, "stock": 2100},
        {"id": "W3", "name": "East River Depot", "lat": 40.6892, "lon": -74.0445, "capacity": 4500, "stock": 3800},
        {"id": "W4", "name": "Quantum Reserve", "lat": 40.7282, "lon": -73.7949, "capacity": 6000, "stock": 5500},
    ]
    return pd.DataFrame(warehouses)

def generate_deliveries(num_deliveries=15):
    """Generates mock delivery locations around the base coordinates."""
    # Base coords (NYC area approx)
    base_lat = 40.7128
    base_lon = -74.0060
    
    np.random.seed(42)  # For reproducibility
    
    deliveries = []
    for i in range(num_deliveries):
        # Generate random coordinates within ~15 miles of base
        lat = base_lat + np.random.uniform(-0.1, 0.1)
        lon = base_lon + np.random.uniform(-0.1, 0.1)
        
        deliveries.append({
            "id": f"D{i+1}",
            "destination": f"Destination {i+1}",
            "lat": lat,
            "lon": lon,
            "demand": np.random.randint(50, 500),
            "priority": np.random.choice(["High", "Medium", "Low"], p=[0.2, 0.5, 0.3])
        })
        
    return pd.DataFrame(deliveries)

def generate_historical_data():
    """Generates historical data for demand forecasting."""
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    np.random.seed(42)
    
    data = []
    for date in dates:
        # Base demand with some seasonality and noise
        day_of_week = date.dayofweek
        month = date.month
        
        base_demand = 1000
        weekend_modifier = 1.5 if day_of_week >= 5 else 1.0
        season_modifier = 1.2 if month in [11, 12] else 1.0 # Higher in winter
        
        noise = np.random.normal(0, 100)
        
        demand = int(base_demand * weekend_modifier * season_modifier + noise)
        
        data.append({
            "date": date,
            "day_of_week": day_of_week,
            "month": month,
            "is_weekend": 1 if day_of_week >= 5 else 0,
            "demand": max(100, demand) # Ensure positive demand
        })
        
    return pd.DataFrame(data)
