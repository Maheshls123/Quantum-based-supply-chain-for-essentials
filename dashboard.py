import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.ai_models import DemandForecaster
from utils.data_generator import generate_historical_data

def render_dashboard():
    st.markdown('<h1 class="neon-title">QuantumChain Analytics</h1>', unsafe_allow_html=True)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    total_warehouses = len(st.session_state.warehouses)
    active_deliveries = len(st.session_state.deliveries)
    
    # Mock data for dashboard
    delivery_efficiency = "94.2%"
    fuel_saved = "1,245 L"
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Total Warehouses", total_warehouses)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Active Deliveries", active_deliveries)
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Delivery Efficiency", delivery_efficiency, "+5.4%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Fuel Saved (Monthly)", fuel_saved, "+12% vs last month")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### Regional Demand (Mock)")
        if not st.session_state.deliveries.empty:
            priority_counts = st.session_state.deliveries['priority'].value_counts().reset_index()
            priority_counts.columns = ['Priority', 'Count']
            
            fig = px.pie(
                priority_counts, 
                values='Count', 
                names='Priority', 
                hole=0.4,
                color='Priority',
                color_discrete_map={'High': '#ff4b4b', 'Medium': '#ffa500', 'Low': '#00d2ff'}
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No delivery data available.")

    with col_chart2:
        st.markdown("### AI Demand Forecasting")
        st.markdown("Using Scikit-learn Random Forest to predict next 7 days demand.")
        
        # Train model if not already done
        if 'ai_forecaster' not in st.session_state:
            st.session_state.ai_forecaster = DemandForecaster()
            hist_data = generate_historical_data()
            st.session_state.ai_forecaster.train(hist_data)
            
        predictions = st.session_state.ai_forecaster.predict_next_week()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=days, 
            y=predictions, 
            mode='lines+markers',
            line=dict(color='#00d2ff', width=3),
            marker=dict(size=10, color='#ff00ff'),
            name='Forecast'
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_title="Day of Week",
            yaxis_title="Predicted Demand",
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
