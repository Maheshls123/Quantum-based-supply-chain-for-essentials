import streamlit as st
import pandas as pd

def render_warehouses():
    st.markdown('<h2 class="neon-title">Warehouse Management</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Add New Warehouse")
        with st.form("add_warehouse_form"):
            w_name = st.text_input("Warehouse Name")
            w_lat = st.number_input("Latitude", value=40.7128, format="%.4f")
            w_lon = st.number_input("Longitude", value=-74.0060, format="%.4f")
            w_capacity = st.number_input("Capacity", min_value=100, max_value=100000, value=5000, step=100)
            w_stock = st.number_input("Current Stock", min_value=0, max_value=100000, value=1000, step=100)
            
            submitted = st.form_submit_button("Add Warehouse")
            if submitted:
                if w_name:
                    new_id = f"W{len(st.session_state.warehouses) + 1}"
                    new_w = pd.DataFrame([{
                        "id": new_id,
                        "name": w_name,
                        "lat": w_lat,
                        "lon": w_lon,
                        "capacity": w_capacity,
                        "stock": w_stock
                    }])
                    st.session_state.warehouses = pd.concat([st.session_state.warehouses, new_w], ignore_index=True)
                    st.success(f"Warehouse '{w_name}' added successfully!")
                else:
                    st.error("Please enter a warehouse name.")
                    
    with col2:
        st.markdown("### Active Warehouses")
        st.dataframe(
            st.session_state.warehouses,
            use_container_width=True,
            column_config={
                "lat": st.column_config.NumberColumn("Latitude", format="%.4f"),
                "lon": st.column_config.NumberColumn("Longitude", format="%.4f"),
                "capacity": st.column_config.ProgressColumn("Capacity", format="%d", min_value=0, max_value=10000),
                "stock": st.column_config.NumberColumn("Stock", format="%d")
            },
            hide_index=True
        )
        
        if st.button("Reset Default Warehouses"):
            from utils.data_generator import generate_warehouses
            st.session_state.warehouses = generate_warehouses()
            st.rerun()
