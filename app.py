import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(
    page_title="QuantumChain AI",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Initialize Session State
if 'warehouses' not in st.session_state:
    from utils.data_generator import generate_warehouses
    st.session_state.warehouses = generate_warehouses()

if 'deliveries' not in st.session_state:
    from utils.data_generator import generate_deliveries
    st.session_state.deliveries = generate_deliveries(15)

if 'current_route' not in st.session_state:
    st.session_state.current_route = None

if 'optimization_results' not in st.session_state:
    st.session_state.optimization_results = None

if 'active_warehouse' not in st.session_state:
    st.session_state.active_warehouse = None

# Sidebar Navigation
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h1 style='color: #00d2ff; font-weight: 800; font-size: 2rem;'>QuantumChain AI</h1>
    <p style='color: #94a3b8; font-size: 0.9rem;'>Quantum for Social Good</p>
    <p style='color: #ff00ff; font-size: 0.8rem; font-weight: bold;'>Team: Coding Jutsu</p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Warehouses", "Deliveries", "Route Optimization"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**SDG Alignment**
* 🌍 SDG 9: Industry, Innovation & Infrastructure
* 🏙️ SDG 11: Sustainable Cities & Communities
""")

# Route to respective view
if page == "Dashboard":
    from views.dashboard import render_dashboard
    render_dashboard()
elif page == "Warehouses":
    from views.warehouses import render_warehouses
    render_warehouses()
elif page == "Deliveries":
    from views.deliveries import render_deliveries
    render_deliveries()
elif page == "Route Optimization":
    from views.route_optimization import render_route_optimization
    render_route_optimization()
