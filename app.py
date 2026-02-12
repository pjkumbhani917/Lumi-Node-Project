import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Lumi-Node Dashboard", 
    layout="wide", 
    page_icon="💡",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title and Header
st.title("💡 LUMI-NODE: Smart Streetlight Network")
st.markdown("**AI-Powered Adaptive Street Lighting for Indian Cities**")
st.markdown("---")

# Sidebar - Configuration
st.sidebar.header("⚙️ System Configuration")
st.sidebar.markdown("Adjust parameters to see real-time impact")

num_lights = st.sidebar.slider(
    "Number of Streetlights", 
    min_value=50, 
    max_value=500, 
    value=100, 
    step=10,
    help="Total streetlights in the zone"
)

power_per_light = st.sidebar.slider(
    "Power per Light (Watts)", 
    min_value=50, 
    max_value=250, 
    value=150, 
    step=10,
    help="LED streetlights typically use 100-200W"
)

electricity_rate = st.sidebar.slider(
    "Electricity Rate (₹/kWh)", 
    min_value=5, 
    max_value=15, 
    value=7, 
    step=1,
    help="Municipal electricity rate in India"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Adjust sliders to see how different configurations affect savings!")

# Load or Generate Data
@st.cache_data
def load_traffic_data():
    """Load traffic analysis data from CSV or generate synthetic data"""
    try:
        # Try to load from CSV file
        df = pd.read_csv('traffic_analysis.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.sidebar.success("✅ Loaded real data from CSV")
        return df
    except FileNotFoundError:
        # Generate synthetic data if file doesn't exist
        st.sidebar.warning("⚠️ CSV not found, generating synthetic data")
        
        timestamps = []
        people = []
        vehicles = []
        
        for hour in range(24):
            for minute in range(0, 60, 5):
                time = datetime(2026, 2, 12, hour, minute)
                timestamps.append(time)
                
                # Traffic patterns
                if 6 <= hour <= 9:  # Morning rush
                    people.append(np.random.randint(20, 50))
                    vehicles.append(np.random.randint(40, 80))
                elif 17 <= hour <= 20:  # Evening rush
                    people.append(np.random.randint(25, 55))
                    vehicles.append(np.random.randint(50, 90))
                elif 12 <= hour <= 14:  # Lunch
                    people.append(np.random.randint(10, 30))
                    vehicles.append(np.random.randint(20, 40))
                elif 22 <= hour or hour <= 5:  # Night
                    people.append(np.random.randint(0, 5))
                    vehicles.append(np.random.randint(0, 10))
                else:  # Normal hours
                    people.append(np.random.randint(5, 20))
                    vehicles.append(np.random.randint(10, 30))
        
        df = pd.DataFrame({
            'timestamp': timestamps,
            'people_count': people,
            'vehicle_count': vehicles,
            'total_activity': np.array(people) + np.array(vehicles)
        })
        
        # Calculate brightness levels
        def activity_to_brightness(activity):
            if activity <= 5:
                return 20
            elif activity <= 15:
                return 40
            elif activity <= 30:
                return 60
            elif activity <= 50:
                return 80
            else:
                return 100
        
        df['optimal_brightness'] = df['total_activity'].apply(activity_to_brightness)
        df['traditional_brightness'] = 100
        
        return df

# Load data
df = load_traffic_data()

# Calculate Savings
def calculate_savings_metrics(df, num_lights, power_per_light, electricity_rate):
    """Calculate all savings metrics"""
    time_interval_hours = 5 / 60  # 5 minutes in hours
    
    # Traditional: always 100%
    traditional_kwh = (num_lights * power_per_light * len(df) * time_interval_hours) / 1000
    
    # Smart: variable brightness
    smart_kwh = (num_lights * power_per_light * 
                 (df['optimal_brightness'].sum() / 100) * time_interval_hours) / 1000
    
    # Savings
    kwh_saved = traditional_kwh - smart_kwh
    percentage_saved = (kwh_saved / traditional_kwh) * 100
    
    # Costs
    cost_saved_daily = kwh_saved * electricity_rate
    cost_saved_monthly = cost_saved_daily * 30
    cost_saved_yearly = cost_saved_daily * 365
    
    # CO2 (0.82 kg CO2 per kWh in India)
    co2_saved_daily = kwh_saved * 0.82
    co2_saved_yearly = co2_saved_daily * 365
    
    # Trees equivalent (1 tree absorbs ~20kg CO2/year)
    trees_equivalent = co2_saved_yearly / 20
    
    return {
        'traditional_kwh': traditional_kwh,
        'smart_kwh': smart_kwh,
        'kwh_saved': kwh_saved,
        'percentage_saved': percentage_saved,
        'cost_saved_daily': cost_saved_daily,
        'cost_saved_monthly': cost_saved_monthly,
        'cost_saved_yearly': cost_saved_yearly,
        'co2_saved_daily': co2_saved_daily,
        'co2_saved_yearly': co2_saved_yearly,
        'trees_equivalent': trees_equivalent
    }

savings = calculate_savings_metrics(df, num_lights, power_per_light, electricity_rate)

# Key Metrics Row
st.markdown("### 📊 Real-Time Impact Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="⚡ Energy Saved",
        value=f"{savings['percentage_saved']:.1f}%",
        delta=f"{savings['kwh_saved']:.1f} kWh/day",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="💰 Daily Savings",
        value=f"₹{savings['cost_saved_daily']:,.0f}",
        delta=f"₹{savings['cost_saved_yearly']:,.0f}/year",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="🌍 CO₂ Reduced",
        value=f"{savings['co2_saved_yearly']:,.0f} kg/yr",
        delta=f"{savings['trees_equivalent']:.0f} trees equivalent",
        delta_color="normal"
    )

with col4:
    st.metric(
        label="💡 Active Lights",
        value=f"{num_lights}",
        delta=f"{power_per_light}W each",
        delta_color="off"
    )

st.markdown("---")

# Main Content Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Live Analysis", 
    "💰 Cost Savings", 
    "📈 Traffic Patterns", 
    "⚡ System Status",
    "📋 Data Table"
])

# TAB 1: Live Analysis
with tab1:
    st.subheader("Real-Time Brightness Optimization")
    
    # Brightness comparison chart
    fig_brightness = go.Figure()
    
    fig_brightness.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['traditional_brightness'],
        name='Traditional System (100% Always)',
        line=dict(color='#e74c3c', width=2, dash='dash'),
        hovertemplate='Time: %{x}<br>Brightness: %{y}%<extra></extra>'
    ))
    
    fig_brightness.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['optimal_brightness'],
        name='Lumi-Node (Smart Adaptive)',
        fill='tonexty',
        fillcolor='rgba(39, 174, 96, 0.3)',
        line=dict(color='#27ae60', width=3),
        hovertemplate='Time: %{x}<br>Brightness: %{y}%<extra></extra>'
    ))
    
    fig_brightness.update_layout(
        height=450,
        xaxis_title="Time of Day",
        yaxis_title="Brightness Level (%)",
        hovermode='x unified',
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_brightness, use_container_width=True)
    
    st.info(f"💡 **Green shaded area** represents energy saved = **{savings['percentage_saved']:.1f}%** reduction")
    
    # Activity charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👥 Pedestrian & Vehicle Detection")
        fig_activity = go.Figure()
        
        fig_activity.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['people_count'],
            name='Pedestrians',
            fill='tozeroy',
            line=dict(color='#3498db', width=2)
        ))
        
        fig_activity.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['vehicle_count'],
            name='Vehicles',
            fill='tozeroy',
            line=dict(color='#e67e22', width=2)
        ))
        
        fig_activity.update_layout(
            height=350,
            xaxis_title="Time",
            yaxis_title="Count",
            template='plotly_white',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_activity, use_container_width=True)
    
    with col2:
        st.markdown("#### 🕐 Average Activity by Hour")
        df['hour'] = df['timestamp'].dt.hour
        hourly = df.groupby('hour')['total_activity'].mean().reset_index()
        
        fig_hourly = px.bar(
            hourly,
            x='hour',
            y='total_activity',
            color='total_activity',
            color_continuous_scale='Viridis',
            labels={'total_activity': 'Avg Activity', 'hour': 'Hour of Day'}
        )
        
        fig_hourly.update_layout(
            height=350,
            template='plotly_white',
            showlegend=False
        )
        
        st.plotly_chart(fig_hourly, use_container_width=True)

# TAB 2: Cost Savings
with tab2:
    st.subheader("Cost-Benefit Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚡ Energy Comparison")
        
        comparison_df = pd.DataFrame({
            'System': ['Traditional\n(Wasteful)', 'Lumi-Node\n(Smart)'],
            'kWh per Day': [savings['traditional_kwh'], savings['smart_kwh']]
        })
        
        fig_energy = px.bar(
            comparison_df,
            x='System',
            y='kWh per Day',
            color='System',
            color_discrete_map={
                'Traditional\n(Wasteful)': '#e74c3c',
                'Lumi-Node\n(Smart)': '#27ae60'
            },
            text='kWh per Day'
        )
        
        fig_energy.update_traces(texttemplate='%{text:.2f} kWh', textposition='outside')
        fig_energy.update_layout(height=400, showlegend=False, template='plotly_white')
        
        st.plotly_chart(fig_energy, use_container_width=True)
    
    with col2:
        st.markdown("#### 💰 Cost Savings Timeline")
        
        savings_timeline = pd.DataFrame({
            'Period': ['Daily', 'Monthly', 'Yearly', '5 Years'],
            'Savings (₹)': [
                savings['cost_saved_daily'],
                savings['cost_saved_monthly'],
                savings['cost_saved_yearly'],
                savings['cost_saved_yearly'] * 5
            ]
        })
        
        fig_savings = px.bar(
            savings_timeline,
            x='Period',
            y='Savings (₹)',
            color='Savings (₹)',
            color_continuous_scale='Greens',
            text='Savings (₹)'
        )
        
        fig_savings.update_traces(
            texttemplate='₹%{text:,.0f}',
            textposition='outside'
        )
        fig_savings.update_layout(height=400, showlegend=False, template='plotly_white')
        
        st.plotly_chart(fig_savings, use_container_width=True)
    
    # ROI Breakdown
    st.markdown("---")
    st.markdown("### 📈 5-Year Financial Projection")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        **💵 Total Savings**
        - 5 Years: ₹{savings['cost_saved_yearly'] * 5:,.0f}
        - 10 Years: ₹{savings['cost_saved_yearly'] * 10:,.0f}
        """)
    
    with col2:
        st.markdown(f"""
        **🌍 Environmental Impact**
        - CO₂ Saved: {savings['co2_saved_yearly'] * 5:,.0f} kg
        - Trees Equivalent: {int(savings['trees_equivalent'] * 5)} trees
        """)
    
    with col3:
        st.markdown(f"""
        **⚡ Energy Saved**
        - 5 Years: {savings['kwh_saved'] * 365 * 5:,.0f} kWh
        - Monthly: {savings['kwh_saved'] * 30:,.0f} kWh
        """)

# TAB 3: Traffic Patterns
with tab3:
    st.subheader("Traffic Pattern Analysis")
    
    # Heatmap
    st.markdown("#### 🗓️ Activity Heatmap (24 Hours)")
    
    df['hour'] = df['timestamp'].dt.hour
    df['minute_group'] = (df['timestamp'].dt.minute // 15) * 15
    
    pivot = df.pivot_table(
        values='total_activity',
        index='minute_group',
        columns='hour',
        aggfunc='mean'
    )
    
    fig_heatmap = px.imshow(
        pivot,
        labels=dict(x="Hour of Day", y="Minute", color="Activity"),
        color_continuous_scale='Viridis',
        aspect="auto"
    )
    
    fig_heatmap.update_layout(height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Peak hours analysis
    st.markdown("---")
    st.markdown("#### 🔥 Peak Activity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top 5 Busiest Hours:**")
        peak_hours = df.groupby('hour')['total_activity'].mean().nlargest(5)
        for idx, (hour, activity) in enumerate(peak_hours.items(), 1):
            st.write(f"{idx}. **{hour:02d}:00** — Avg: {activity:.0f} people/vehicles")
    
    with col2:
        st.markdown("**Top 5 Quietest Hours:**")
        quiet_hours = df.groupby('hour')['total_activity'].mean().nsmallest(5)
        for idx, (hour, activity) in enumerate(quiet_hours.items(), 1):
            st.write(f"{idx}. **{hour:02d}:00** — Avg: {activity:.0f} people/vehicles")

# TAB 4: System Status
with tab4:
    st.subheader("System Status & Control")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔋 System Health")
        st.metric("Status", "🟢 ACTIVE", delta="All systems operational")
        st.metric("Uptime", "99.8%", delta="Last 30 days")
    
    with col2:
        st.markdown("#### 💡 Lights Status")
        st.metric("Online", f"{num_lights}/{num_lights}", delta="100% operational")
        st.metric("Avg Response", "1.2 sec", delta="Command to action")
    
    with col3:
        st.markdown("#### ⏱️ Last Update")
        current_time = datetime.now().strftime("%H:%M:%S")
        st.metric("Time", current_time, delta="Live data")
        st.metric("Mode", "Automatic", delta="AI-controlled")
    
    st.markdown("---")
    
    # Manual Override Section
    st.markdown("### 🎛️ Manual Override (Demo Mode)")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        manual_brightness = st.slider(
            "Override Brightness Level",
            min_value=0,
            max_value=100,
            value=60,
            step=5,
            help="Manually set brightness for all lights"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("🚀 Apply Override", type="primary"):
            st.success(f"✅ All {num_lights} lights set to {manual_brightness}% brightness")
            st.warning("⚠️ Manual override active - automatic optimization disabled")
    
    st.info("💡 **Note:** In production, manual override would send real commands to streetlight controllers via IoT network")

# TAB 5: Data Table
with tab5:
    st.subheader("📋 Raw Data Explorer")
    
    # Add filters
    col1, col2 = st.columns(2)
    
    with col1:
        hour_filter = st.multiselect(
            "Filter by Hour",
            options=sorted(df['hour'].unique()),
            default=sorted(df['hour'].unique())[:5]
        )
    
    with col2:
        brightness_filter = st.multiselect(
            "Filter by Brightness Level",
            options=sorted(df['optimal_brightness'].unique()),
            default=sorted(df['optimal_brightness'].unique())
        )
    
    # Filter data
    if hour_filter and brightness_filter:
        filtered_df = df[
            (df['hour'].isin(hour_filter)) & 
            (df['optimal_brightness'].isin(brightness_filter))
        ]
    else:
        filtered_df = df
    
    # Display table
    st.dataframe(
        filtered_df[['timestamp', 'people_count', 'vehicle_count', 'total_activity', 'optimal_brightness']],
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f'lumi_node_data_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p><strong>Lumi-Node Smart Streetlight Network</strong> | Powered by AI & IoT</p>
    <p>Developed for Indian Smart Cities Initiative | Data updates every 5 minutes</p>
</div>
""", unsafe_allow_html=True)