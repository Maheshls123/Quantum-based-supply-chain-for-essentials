import streamlit as st
import pandas as pd
import numpy as np

def render_deliveries():
    st.markdown('<h2 class="neon-title">Delivery Management</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Add Delivery Location")
        with st.form("add_delivery_form"):
            d_dest = st.text_input("Destination Name")
            d_lat = st.number_input("Latitude", value=40.7300, format="%.4f")
            d_lon = st.number_input("Longitude", value=-73.9900, format="%.4f")
            d_demand = st.number_input("Demand Quantity", min_value=1, max_value=5000, value=100, step=10)
            d_priority = st.selectbox("Priority Level", ["High", "Medium", "Low"])
            
            submitted = st.form_submit_button("Add Delivery")
            if submitted:
                if d_dest:
                    new_id = f"D{len(st.session_state.deliveries) + 1}"
                    new_d = pd.DataFrame([{
                        "id": new_id,
                        "destination": d_dest,
                        "lat": d_lat,
                        "lon": d_lon,
                        "demand": d_demand,
                        "priority": d_priority
                    }])
                    st.session_state.deliveries = pd.concat([st.session_state.deliveries, new_d], ignore_index=True)
                    st.success(f"Delivery to '{d_dest}' added successfully!")
                else:
                    st.error("Please enter a destination name.")
                    
    with col2:
        st.markdown("### Pending Deliveries")
        
        # Color coding for priority
        def highlight_priority(val):
            color = ''
            if val == 'High': color = '#ff4b4b'
            elif val == 'Medium': color = '#ffa500'
            elif val == 'Low': color = '#00d2ff'
            return f'color: {color}; font-weight: bold'
            
        styled_df = st.session_state.deliveries.style.map(highlight_priority, subset=['priority'])
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            column_config={
                "lat": st.column_config.NumberColumn("Latitude", format="%.4f"),
                "lon": st.column_config.NumberColumn("Longitude", format="%.4f"),
            },
            hide_index=True
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Generate Random Deliveries"):
                from utils.data_generator import generate_deliveries
                new_deliveries = generate_deliveries(num_deliveries=5)
                # Ensure unique IDs
                start_idx = len(st.session_state.deliveries)
                new_deliveries['id'] = [f"D{start_idx + i + 1}" for i in range(len(new_deliveries))]
                st.session_state.deliveries = pd.concat([st.session_state.deliveries, new_deliveries], ignore_index=True)
                st.rerun()
        with col_btn2:
            if st.button("Clear All Deliveries"):
                st.session_state.deliveries = pd.DataFrame(columns=["id", "destination", "lat", "lon", "demand", "priority"])
                st.rerun()
