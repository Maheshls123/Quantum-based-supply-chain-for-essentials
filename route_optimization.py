import streamlit as st
import pandas as pd
from utils.map_renderer import create_base_map, add_warehouses_to_map, add_deliveries_to_map, draw_optimized_route, render_map
from utils.optimization import optimize_route_quantum_inspired, calculate_savings

def render_route_optimization():
    st.markdown('<h2 class="neon-title">Quantum Route Optimization</h2>', unsafe_allow_html=True)
    
    col_settings, col_map = st.columns([1, 2])
    
    with col_settings:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Optimization Engine")
        st.markdown("Select a central warehouse and compute the optimal delivery route using simulated quantum annealing.")
        
        if st.session_state.warehouses.empty:
            st.warning("No warehouses available. Please add one.")
            st.markdown('</div>', unsafe_allow_html=True)
            return
            
        if st.session_state.deliveries.empty:
            st.warning("No deliveries available. Please add deliveries.")
            st.markdown('</div>', unsafe_allow_html=True)
            return
            
        selected_warehouse_name = st.selectbox(
            "Select Origin Warehouse", 
            options=st.session_state.warehouses['name'].tolist()
        )
        
        selected_w_row = st.session_state.warehouses[st.session_state.warehouses['name'] == selected_warehouse_name].iloc[0]
        
        if st.button("Initialize Quantum Routing"):
            with st.spinner("Running quantum-inspired optimization (Simulated Annealing)..."):
                # Combine warehouse and deliveries into one dataframe for routing
                w_df = pd.DataFrame([{
                    "id": selected_w_row['id'],
                    "name": selected_w_row['name'],
                    "lat": selected_w_row['lat'],
                    "lon": selected_w_row['lon'],
                    "type": "Warehouse"
                }])
                
                d_df = st.session_state.deliveries[['id', 'destination', 'lat', 'lon']].copy()
                d_df.rename(columns={'destination': 'name'}, inplace=True)
                d_df['type'] = 'Delivery'
                
                routing_nodes = pd.concat([w_df, d_df], ignore_index=True)
                
                # Perform Optimization
                best_route_indices, optimized_distance = optimize_route_quantum_inspired(routing_nodes)
                
                # Calculate basic unoptimized distance (just going in order)
                # To simulate savings
                unoptimized_route = list(range(len(routing_nodes))) + [0]
                from utils.optimization import calculate_distance_matrix
                dist_matrix = calculate_distance_matrix(routing_nodes)
                unoptimized_distance = sum([dist_matrix[unoptimized_route[i], unoptimized_route[i+1]] for i in range(len(routing_nodes))]) * 111.32
                
                savings = calculate_savings(unoptimized_distance, optimized_distance)
                
                # Store results in session state
                route_coords = [[routing_nodes.iloc[idx]['lat'], routing_nodes.iloc[idx]['lon']] for idx in best_route_indices]
                st.session_state.current_route = route_coords
                st.session_state.optimization_results = savings
                st.session_state.active_warehouse = selected_w_row
                
            st.success("Optimization Complete!")
            
        # Display Results if available
        if st.session_state.optimization_results:
            st.markdown("### Optimization Metrics")
            res = st.session_state.optimization_results
            st.metric("Distance Saved", f"{res['distance_saved_km']} km")
            st.metric("Fuel Saved", f"{res['fuel_saved_liters']} L")
            st.metric("Efficiency Gain", f"{res['efficiency_gain_pct']}%", delta_color="normal")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_map:
        st.markdown("### Interactive Smart Map")
        
        # Center map on active warehouse or default
        if st.session_state.active_warehouse is not None:
            center_lat = st.session_state.active_warehouse['lat']
            center_lon = st.session_state.active_warehouse['lon']
        elif not st.session_state.warehouses.empty:
            center_lat = st.session_state.warehouses.iloc[0]['lat']
            center_lon = st.session_state.warehouses.iloc[0]['lon']
        else:
            center_lat, center_lon = 40.7128, -74.0060
            
        m = create_base_map(center_lat, center_lon)
        
        m = add_warehouses_to_map(m, st.session_state.warehouses)
        m = add_deliveries_to_map(m, st.session_state.deliveries)
        
        if st.session_state.current_route:
            m = draw_optimized_route(m, st.session_state.current_route)
            
        render_map(m)
