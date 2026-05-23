import numpy as np
from sko.SA import SA_TSP
from scipy.spatial.distance import cdist

def calculate_distance_matrix(locations_df):
    """
    Calculates the Euclidean distance matrix between all locations.
    """
    coords = locations_df[['lat', 'lon']].values
    dist_matrix = cdist(coords, coords, metric='euclidean')
    return dist_matrix

def optimize_route_quantum_inspired(locations_df):
    """
    Uses Simulated Annealing (a quantum-inspired optimization technique)
    to solve the Traveling Salesperson Problem (TSP) for the given locations.
    Returns the optimized indices and the total distance.
    """
    if len(locations_df) <= 2:
        return locations_df.index.tolist(), 0
        
    dist_matrix = calculate_distance_matrix(locations_df)
    num_points = len(locations_df)
    
    # Objective function for SA_TSP
    def cal_total_distance(routine):
        num_points, = routine.shape
        return sum([dist_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])
    
    # Initialize Simulated Annealing
    # This acts as a proxy for quantum annealing
    sa_tsp = SA_TSP(func=cal_total_distance, x0=range(num_points), T_max=100, T_min=1, L=10 * num_points)
    
    best_points, best_distance = sa_tsp.run()
    
    # Standardize the route to start at the first point (usually the warehouse)
    best_points = list(best_points)
    zero_idx = best_points.index(0)
    best_points = best_points[zero_idx:] + best_points[:zero_idx]
    
    # Make it a round trip by appending the start to the end
    best_points.append(best_points[0])
    
    # Convert arbitrary distance units to approximate kilometers (very rough approx)
    distance_km = best_distance * 111.32 
    
    return best_points, distance_km

def calculate_savings(original_distance, optimized_distance):
    """
    Calculates metrics based on the optimized distance.
    """
    distance_saved = original_distance - optimized_distance
    # Assume 10 km per liter of fuel
    fuel_saved_liters = distance_saved / 10.0
    efficiency_gain = (distance_saved / original_distance) * 100 if original_distance > 0 else 0
    
    return {
        "distance_saved_km": round(distance_saved, 2),
        "fuel_saved_liters": round(fuel_saved_liters, 2),
        "efficiency_gain_pct": round(efficiency_gain, 1)
    }
