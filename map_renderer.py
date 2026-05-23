import folium
import pandas as pd
from streamlit_folium import st_folium

def create_base_map(center_lat=40.7128, center_lon=-74.0060, zoom_start=11):
    """Creates a basic Folium map with a dark theme tile layer."""
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=zoom_start,
        tiles='cartodbdark_matter' # Dark theme map to match UI
    )
    return m

def add_warehouses_to_map(m, warehouses_df):
    """Adds warehouse markers to the map."""
    for idx, row in warehouses_df.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"<b>{row['name']}</b><br>Stock: {row['stock']}/{row['capacity']}",
            tooltip=row['name'],
            icon=folium.Icon(color='blue', icon='home', prefix='fa')
        ).add_to(m)
    return m

def add_deliveries_to_map(m, deliveries_df):
    """Adds delivery locations to the map."""
    for idx, row in deliveries_df.iterrows():
        color = 'red' if row['priority'] == 'High' else 'orange' if row['priority'] == 'Medium' else 'green'
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=6,
            popup=f"<b>{row['destination']}</b><br>Demand: {row['demand']}<br>Priority: {row['priority']}",
            tooltip=row['destination'],
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)
    return m

def draw_optimized_route(m, route_coords, color='#00d2ff', weight=3):
    """Draws a polyline connecting the points in the route."""
    if len(route_coords) > 1:
        folium.PolyLine(
            route_coords,
            color=color,
            weight=weight,
            opacity=0.8,
            dash_array='10, 10'
        ).add_to(m)
        
        # Add animated arrows or similar if needed, here we just use PolyLine
    return m

def render_map(m, width=700, height=500):
    """Renders the Folium map in Streamlit."""
    return st_folium(m, width=width, height=height, returned_objects=[])
