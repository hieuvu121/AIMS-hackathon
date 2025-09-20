import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np

# Page configuration
st.set_page_config(
    page_title="World Modern Slavery Index",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --primary-color: #3b82f6;
    --secondary-color: #1e40af;
    --accent-color: #f59e0b;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --error-color: #ef4444;
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-tertiary: #334155;
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --border-color: #475569;
}

.stApp {
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
}

    .main-header {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    padding: 2.5rem;
    border-radius: 20px;
    color: white;
        text-align: center;
        margin-bottom: 2rem;
    box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.main-header h1 {
    font-size: 3.2rem;
    font-weight: 900;
    margin: 0;
    background: linear-gradient(45deg, #ffffff, #e2e8f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
}

.main-header p {
    font-size: 1.3rem;
    margin: 1rem 0 0 0;
    opacity: 0.95;
    position: relative;
    z-index: 1;
}

.dashboard-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.dashboard-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.6s ease;
}

.dashboard-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
    border-color: var(--primary-color);
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
}

.dashboard-card:hover::before {
    left: 100%;
}

    .metric-card {
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
    padding: 2rem;
    border-radius: 16px;
    border-left: 6px solid var(--primary-color);
    margin: 1rem 0;
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, transparent 0%, rgba(59, 130, 246, 0.05) 100%);
    pointer-events: none;
    transition: all 0.4s ease;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
    transition: left 0.6s ease;
}

.metric-card:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 16px 48px rgba(59, 130, 246, 0.4);
    border-left-color: var(--accent-color);
    background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
}

.metric-card:hover::before {
    background: linear-gradient(135deg, transparent 0%, rgba(59, 130, 246, 0.15) 100%);
}

.metric-card:hover::after {
    left: 100%;
}

.company-info-card {
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
    border: 2px solid var(--primary-color);
    border-radius: 20px;
    padding: 2.5rem;
    margin: 1rem 0;
    color: var(--text-primary);
    box-shadow: 0 12px 48px rgba(59, 130, 246, 0.2);
    position: relative;
    overflow: hidden;
}

.company-info-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
    pointer-events: none;
}

.chart-container {
    background: var(--bg-secondary);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    border: 1px solid var(--border-color);
}

.recommendation-box {
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
    border: 2px solid var(--accent-color);
    border-radius: 16px;
    padding: 2rem;
    margin: 1rem 0;
    color: var(--text-primary);
    box-shadow: 0 8px 32px rgba(245, 158, 11, 0.15);
}

.alert-card {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    border: 2px solid var(--error-color);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: #991b1b;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.8; }
    100% { opacity: 1; }
}

.success-card {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    border: 2px solid var(--success-color);
    border-radius: 12px;
        padding: 1.5rem;
    margin: 1rem 0;
    color: #065f46;
}

.score-excellent { 
    border-left: 6px solid var(--success-color); 
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, var(--bg-secondary) 100%); 
}
.score-good { 
    border-left: 6px solid #0891b2; 
    background: linear-gradient(90deg, rgba(8, 145, 178, 0.1) 0%, var(--bg-secondary) 100%); 
}
.score-developing { 
    border-left: 6px solid var(--accent-color); 
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.1) 0%, var(--bg-secondary) 100%); 
}
.score-needs-improvement { 
    border-left: 6px solid var(--error-color); 
    background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, var(--bg-secondary) 100%); 
}

.progress-bar {
    background: var(--bg-tertiary);
    border-radius: 10px;
    overflow: hidden;
    height: 20px;
    margin: 0.5rem 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    transition: width 1s ease-in-out;
        border-radius: 10px;
}

.floating-action {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4);
    cursor: pointer;
    z-index: 1000;
    transition: all 0.3s ease;
}

.floating-action:hover {
    transform: scale(1.1);
    box-shadow: 0 12px 48px rgba(59, 130, 246, 0.6);
}

    .slavery-type-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .slavery-type-title {
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        color: #fff;
    }

    .sidebar .sidebar-content {
        background-color: #2c3e50;
    }

/* Streamlit specific overrides */
.stSelectbox > div > div {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
}

.stSelectbox label {
    color: var(--text-primary);
    font-weight: 600;
}

.stSlider > div > div {
    background-color: var(--bg-secondary);
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
}

.stMultiSelect > div > div {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
}

.stMultiSelect label {
    color: var(--text-primary);
    font-weight: 600;
}

.stDataFrame {
    background-color: var(--bg-secondary);
    border-radius: 8px;
    overflow: hidden;
}

.stExpander > div {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
}

.stExpander > div > div {
    color: var(--text-primary);
}

.stInfo {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(30, 64, 175, 0.1));
    border: 1px solid var(--primary-color);
    border-radius: 8px;
}

.stSuccess {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
    border: 1px solid var(--success-color);
    border-radius: 8px;
}

.stWarning {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1));
    border: 1px solid var(--warning-color);
    border-radius: 8px;
}

.stError {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
    border: 1px solid var(--error-color);
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Sample data for Australian states
@st.cache_data
def load_australia_data():
    # Sample modern slavery data by Australian state
    data = {
        'State': ['New South Wales', 'Victoria', 'Queensland', 'Western Australia', 
                  'South Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory'],
        'State_Code': ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT', 'ACT'],
        'Population': [8166369, 6681297, 5206400, 2675797, 1771703, 541965, 246561, 431215],
        'Modern_Slavery_Cases': [12500, 9800, 7200, 3800, 2100, 650, 420, 580],
        'Human_Trafficking': [2.1, 1.8, 1.9, 1.6, 1.4, 1.2, 2.8, 1.3],
        'Forced_Labour': [3.2, 2.8, 3.1, 2.4, 2.1, 1.8, 3.5, 2.0],
        'Debt_Bondage': [1.8, 1.5, 1.7, 1.3, 1.1, 0.9, 2.1, 1.0],
        'Forced_Marriage': [0.9, 0.7, 0.8, 0.6, 0.5, 0.4, 1.2, 0.8],
        'Servitude': [1.4, 1.2, 1.3, 1.0, 0.8, 0.7, 1.6, 0.9],
        'Child_Labour': [0.6, 0.5, 0.7, 0.4, 0.3, 0.2, 0.9, 0.3],
        'Deceptive_Recruiting': [2.3, 2.0, 2.2, 1.7, 1.5, 1.3, 2.7, 1.6],
        'Sexual_Exploitation': [1.1, 0.9, 1.0, 0.8, 0.7, 0.5, 1.4, 0.7]
    }
    
    df = pd.DataFrame(data)
    
    # Calculate slavery rate per 1000 people
    df['Slavery_Rate_Per_1000'] = (df['Modern_Slavery_Cases'] / df['Population']) * 1000
    
    # Calculate total modern slavery index (sum of all types)
    slavery_columns = ['Human_Trafficking', 'Forced_Labour', 'Debt_Bondage', 'Forced_Marriage',
                      'Servitude', 'Child_Labour', 'Deceptive_Recruiting', 'Sexual_Exploitation']
    df['Modern_Slavery_Index'] = df[slavery_columns].sum(axis=1)
    
    return df

# Load data
df = load_australia_data()

# Main header
st.markdown('<h1 class="main-header">Modern Slavery Index</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Navigation")
    view_option = st.selectbox(
        "Select View:",
        ["World Map", "Country Details", "State Comparison", "Slavery Types Analysis"]
    )
    
    st.markdown("### Country Selection")
    country_option = st.selectbox(
        "Select Country:",
        ["World", "Australia", "United States", "United Kingdom", "Canada", "Germany", "France", "Japan", "China", "India", "Brazil", "Russia", "South Africa", "Mexico", "Indonesia", "Thailand", "Philippines", "Vietnam", "Bangladesh", "Pakistan", "Nigeria"]
    )
    
    st.markdown("### Filters")
    if country_option == "Australia":
        selected_states = st.multiselect(
            "Select Australian States:",
            df['State'].tolist(),
            default=df['State'].tolist()
        )
    elif country_option == "United States":
        us_states = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania', 'Illinois', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']
        selected_states = st.multiselect(
            "Select US States:",
            us_states,
            default=us_states
        )
    elif country_option == "United Kingdom":
        uk_cities = ['London', 'Birmingham', 'Manchester', 'Glasgow', 'Liverpool', 'Leeds', 'Sheffield', 'Edinburgh', 'Bristol', 'Cardiff', 'Belfast', 'Newcastle', 'Nottingham', 'Leicester', 'Coventry', 'Bradford', 'Stoke-on-Trent', 'Wolverhampton', 'Plymouth', 'Southampton']
        selected_states = st.multiselect(
            "Select UK Cities:",
            uk_cities,
            default=uk_cities[:10]  # Default to first 10 cities
        )
    else:
        selected_states = []
    
    metric_option = st.selectbox(
        "Display Metric:",
        ["Modern_Slavery_Index", "Slavery_Rate_Per_1000", "Modern_Slavery_Cases"]
    )
    
    st.markdown("### Modern Slavery Types")
    slavery_type_options = {
        "All Types": "All Types",
        "Human Trafficking": "Human_Trafficking",
        "Forced Labour": "Forced_Labour", 
        "Debt Bondage": "Debt_Bondage",
        "Forced Marriage": "Forced_Marriage",
        "Servitude": "Servitude",
        "Child Labour": "Child_Labour",
        "Deceptive Recruiting": "Deceptive_Recruiting",
        "Sexual Exploitation": "Sexual_Exploitation"
    }
    
    selected_display = st.selectbox(
        "Filter by Slavery Type:",
        list(slavery_type_options.keys())
    )
    
    # Get the internal value for processing
    slavery_type_option = slavery_type_options[selected_display]
    
    # Add threshold filter for slavery type
    if slavery_type_option != "All Types":
        st.markdown("### Filter Threshold")
        threshold = st.slider(
            f"Minimum {selected_display} Value:",
            min_value=0.0,
            max_value=5.0,
            value=0.0,
            step=0.1,
            help=f"Filter to show only regions with {selected_display} values above this threshold"
        )
    else:
        threshold = 0.0

# Filter data based on selection
filtered_df = df[df['State'].isin(selected_states)]

# Apply slavery type filter if not "All Types"
if slavery_type_option != "All Types":
    # Filter data based on slavery type threshold
    filtered_df = filtered_df[filtered_df[slavery_type_option] >= threshold].copy()
    
    # Create a new column for the selected slavery type
    filtered_df['Filtered_Metric'] = filtered_df[slavery_type_option]
    
    # Update metric_option to use the filtered metric
    original_metric = metric_option
    metric_option = 'Filtered_Metric'
else:
    # Keep original metric
    original_metric = metric_option
    # Ensure Filtered_Metric column exists for consistency
    if 'Filtered_Metric' not in filtered_df.columns:
        filtered_df['Filtered_Metric'] = filtered_df[metric_option]

# Ensure original_metric is always defined
if 'original_metric' not in locals():
    original_metric = metric_option

# Display current filter selections
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"### View: {view_option}")

with col2:
    if country_option == "Australia" and len(selected_states) > 0:
        st.markdown(f"### Regions Selected: {len(selected_states)} states")
    elif country_option == "United States" and len(selected_states) > 0:
        st.markdown(f"### Regions Selected: {len(selected_states)} states")
    elif country_option == "United Kingdom" and len(selected_states) > 0:
        st.markdown(f"### Regions Selected: {len(selected_states)} cities")
    else:
        st.markdown("### Regions Selected: None")

with col3:
    if slavery_type_option != "All Types":
        st.markdown(f"### Slavery Type: {selected_display} (≥{threshold})")
    else:
        st.markdown(f"### Metric: {metric_option.replace('_', ' ')}")

# Show filtering results
if slavery_type_option != "All Types":
    regions_after_filter = len(filtered_df)
    st.info(f"📊 Showing {regions_after_filter} regions with {selected_display} ≥ {threshold}")

st.markdown("---")

# Introduction Section - Only show for World Map view and World country
if view_option == "World Map" and country_option == "World":
    st.markdown("## About the Modern Slavery Index")
    
    # Create two columns for the main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card" style="height: 300px; display: flex; flex-direction: column;">
            <h3 style="color: #f59e0b; margin-bottom: 1.5rem; font-size: 1.8rem;">What is Modern Slavery?</h3>
            <p style="line-height: 1.6; color: #cbd5e1; font-weight: bold; font-size: 1.3rem; flex-grow: 1; display: flex; align-items: center;">
                Modern slavery is an umbrella term encompassing several types of exploitation, including forced labour, 
                human trafficking, forced marriage, debt bondage, forced commercial sexual exploitation, slavery-like 
                practices, and the sale and exploitation of children. It thrives in silence, making comprehensive 
                data collection and analysis crucial for understanding its scope and impact.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card" style="height: 300px; display: flex; flex-direction: column;">
            <h3 style="color: #f59e0b; margin-bottom: 1.5rem; font-size: 1.8rem;">Our Mission</h3>
            <p style="line-height: 1.6; color: #cbd5e1; font-weight: bold; font-size: 1.3rem; flex-grow: 1; display: flex; align-items: center;">
                This interactive dashboard provides real-time insights into modern slavery prevalence across countries 
                and regions using three key metrics: Modern Slavery Index, Slavery Rate Per 1000 people, and Modern Slavery Cases. 
                By visualizing data through maps, charts, and comparative analysis, we aim to support 
                evidence-based policy making and targeted interventions to combat modern slavery globally.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("###  Key Features")
    
    # Create three columns for the key features
    feat1, feat2, feat3 = st.columns(3)
    
    with feat1:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 2rem; margin-right: 1rem;"></span>
                <h4 style="margin: 0; color: #3b82f6;">Interactive World Maps</h4>
            </div>
            <p style="margin: 0; color: #cbd5e1; font-size: 0.9rem; font-weight: bold;">Explore global modern slavery data through interactive visualizations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat2:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 2rem; margin-right: 1rem;"></span>
                <h4 style="margin: 0; color: #3b82f6;">Regional Comparisons</h4>
            </div>
            <p style="margin: 0; color: #cbd5e1; font-size: 0.9rem; font-weight: bold;">Compare modern slavery metrics across different countries and regions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat3:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 2rem; margin-right: 1rem;"></span>
                <h4 style="margin: 0; color: #3b82f6;">Advanced Filtering</h4>
            </div>
            <p style="margin: 0; color: #cbd5e1; font-size: 0.9rem; font-weight: bold;">Filter data by slavery types, thresholds, and specific metrics</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Overview metrics for non-Australia countries
if country_option != "Australia":
    # Show country-specific metrics for other countries
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Selected Country", country_option)
    
    with col2:
        st.metric("View", view_option)
    
    with col3:
        if len(selected_states) > 0:
            st.metric("Regions Selected", len(selected_states))
        else:
            st.metric("Regions Selected", "None")

    with col4:
        st.metric("Metric", metric_option.replace("_", " "))

# Main content based on view selection
if view_option == "World Map":
    st.markdown("## Global Modern Slavery Index Map")
    
    # Create world map with sample data for demonstration
    world_data = {
        'Country': ['Australia', 'United States', 'United Kingdom', 'Canada', 'Germany', 'France', 'Japan', 'China', 'India', 'Brazil', 'Russia', 'South Africa', 'Mexico', 'Indonesia', 'Thailand', 'Philippines', 'Vietnam', 'Bangladesh', 'Pakistan', 'Nigeria'],
        'Modern_Slavery_Index': [filtered_df[metric_option].mean() if country_option == "Australia" and metric_option in filtered_df.columns and not filtered_df.empty else 2.1, 2.1, 1.8, 1.9, 1.6, 1.4, 1.2, 2.8, 3.1, 2.4, 2.1, 1.8, 3.5, 2.0, 2.3, 2.0, 2.2, 1.7, 1.5, 2.7],
        'Slavery_Rate_Per_1000': [1.5, 1.2, 1.0, 1.1, 0.9, 0.8, 0.7, 2.1, 2.3, 1.8, 1.5, 1.3, 2.8, 1.5, 1.7, 1.4, 1.6, 1.2, 1.1, 2.0],
        'Modern_Slavery_Cases': [12500, 45000, 12000, 8000, 15000, 10000, 8500, 120000, 180000, 38000, 20000, 8000, 35000, 40000, 12000, 15000, 15000, 20000, 18000, 35000]
    }
    
    world_df = pd.DataFrame(world_data)
    
    # Create choropleth world map
    # Update title based on slavery type filter
    if slavery_type_option != "All Types":
        title_text = f'Global {selected_display} Index'
    else:
        title_text = f'Global Modern Slavery Index - {metric_option.replace("_", " ")}'
    
    fig = px.choropleth(
        world_df,
        locations='Country',
        locationmode='country names',
        color='Modern_Slavery_Index',
        color_continuous_scale='Reds',
        title=title_text,
        labels={'Modern_Slavery_Index': selected_display if slavery_type_option != "All Types" else 'Modern Slavery Index'},
        hover_data={
            'Modern_Slavery_Index': True,
            'Slavery_Rate_Per_1000': True,
            'Modern_Slavery_Cases': True,
            'Country': True
        }
    )
    
    # Update layout for better world map display
    fig.update_geos(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    )
    
    fig.update_layout(
        height=600,
        coloraxis_colorbar=dict(
            title=dict(
                text="Modern Slavery Index",
                side="right"
            )
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add click instruction
    st.info("Select a country from the sidebar to view detailed state/region breakdowns!")

elif view_option == "Country Details":
    if country_option == "World":
        st.markdown("## Global Overview")
        st.info("Please select a specific country to view detailed breakdowns.")
    else:
        st.markdown(f"## {country_option} - Comprehensive Analysis")
        
        if country_option == "Australia":
            # Create a comprehensive Australia view with both country and state data
            
            # Australia Country Overview Section
            if slavery_type_option != "All Types":
                st.markdown(f"### 🇦🇺 Australia Country Overview - {slavery_type_option.replace('_', ' ')}")
            else:
                st.markdown("### 🇦🇺 Australia Country Overview")
            
            # Calculate Australia-wide metrics
            australia_total_cases = df['Modern_Slavery_Cases'].sum()
            australia_total_population = df['Population'].sum()
            australia_avg_index = df['Modern_Slavery_Index'].mean()
            australia_rate_per_1000 = (australia_total_cases / australia_total_population) * 1000
            
            # Display Australia metrics in columns
            col_a1, col_a2, col_a3, col_a4 = st.columns(4)
            
            with col_a1:
                st.metric("🇦🇺 Total Cases", f"{australia_total_cases:,}")
            with col_a2:
                st.metric("🇦🇺 Average Index", f"{australia_avg_index:.1f}")
            with col_a3:
                st.metric("🇦🇺 Rate per 1000", f"{australia_rate_per_1000:.2f}")
            with col_a4:
                st.metric("🇦🇺 Total Population", f"{australia_total_population:,}")
            
            # Australia Map Section
            if slavery_type_option != "All Types":
                st.markdown(f"### Australia State Map - {slavery_type_option.replace('_', ' ')}")
            else:
                st.markdown("### Australia State Map")
            
            if len(selected_states) > 0:
                filtered_df = df[df['State'].isin(selected_states)]
                
                # Create Australia state map using scatter plot with state boundaries
                # Since Plotly doesn't have built-in Australian state boundaries, we'll use a scatter plot
                # with larger circles positioned on each state to represent the state areas
                
                # Define coordinates for Australian states
                state_coords = {
                    'New South Wales': {'lat': -32.0, 'lon': 147.0, 'size': 60},
                    'Victoria': {'lat': -37.0, 'lon': 144.0, 'size': 50},
                    'Queensland': {'lat': -20.0, 'lon': 145.0, 'size': 70},
                    'Western Australia': {'lat': -26.0, 'lon': 121.0, 'size': 80},
                    'South Australia': {'lat': -30.0, 'lon': 135.0, 'size': 55},
                    'Tasmania': {'lat': -42.0, 'lon': 146.0, 'size': 30},
                    'Northern Territory': {'lat': -20.0, 'lon': 133.0, 'size': 65},
                    'Australian Capital Territory': {'lat': -35.0, 'lon': 149.0, 'size': 20}
                }
                
                # Prepare scatter data
                scatter_data = []
                for _, row in filtered_df.iterrows():
                    state_name = row['State']
                    if state_name in state_coords:
                        coords = state_coords[state_name]
                        # Get the value safely, fallback to original metric if Filtered_Metric doesn't exist
                        if metric_option in row and not pd.isna(row[metric_option]):
                            value = row[metric_option]
                        else:
                            value = row[original_metric] if original_metric in row else 0
                        
                        scatter_data.append({
                            'State': state_name,
                            'lat': coords['lat'],
                            'lon': coords['lon'],
                            'size': coords['size'],
                            'value': value,
                            'Modern_Slavery_Cases': row['Modern_Slavery_Cases'],
                            'Modern_Slavery_Index': row['Modern_Slavery_Index'],
                            'Slavery_Rate_Per_1000': row['Slavery_Rate_Per_1000']
                        })
                
                scatter_df = pd.DataFrame(scatter_data)
                
                # Create scatter plot on map
                fig = px.scatter_mapbox(
                    scatter_df,
                    lat='lat',
                    lon='lon',
                    size='size',
                    color='value',
                    hover_name='State',
                    hover_data={
                        'Modern_Slavery_Cases': True,
                        'Modern_Slavery_Index': True,
                        'Slavery_Rate_Per_1000': True,
                        'lat': False,
                        'lon': False,
                        'size': False
                    },
                    color_continuous_scale='Reds',
                    title=f'Australia - {metric_option.replace("_", " ")} by State (Circle size represents state area)',
                    mapbox_style="open-street-map",
                    zoom=4,
                    center=dict(lat=-25.2744, lon=133.7751)
                )
                
                # Add state labels
                for _, row in scatter_df.iterrows():
                    state_name = row['State']
                    value = row['value']
                    lat = row['lat']
                    lon = row['lon']
                    
                    fig.add_annotation(
                        x=lon,
                        y=lat,
                        text=f"<b>{state_name}</b><br>{value:.1f}",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="black",
                        font=dict(size=11, color="black"),
                        bgcolor="rgba(255,255,255,0.9)",
                        bordercolor="black",
                        borderwidth=2
                    )
                
                fig.update_layout(
                    height=600,
                    coloraxis_colorbar=dict(
                        title=dict(
                            text=metric_option.replace("_", " "),
                            side="right"
                        )
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Also show a horizontal bar chart for detailed comparison
                st.markdown("#### State Comparison Chart")
                bar_fig = px.bar(
                    filtered_df,
                    x=metric_option,
                    y='State',
                    orientation='h',
                    color=metric_option,
                    color_continuous_scale='Reds',
                    title=f'Detailed State Comparison - {metric_option.replace("_", " ")}',
                    labels={metric_option: metric_option.replace("_", " ")}
                )
                
                bar_fig.update_layout(
                    yaxis_title="State",
                    xaxis_title=metric_option.replace("_", " "),
                    showlegend=False,
                    height=max(400, len(selected_states) * 40)
                )
                
                st.plotly_chart(bar_fig, use_container_width=True)
            else:
                st.info("Please select Australian states to view the state breakdown.")
            
            # State Comparison Table
            if len(selected_states) > 0:
                st.markdown("### State-by-State Comparison")
                
                # Create detailed comparison table
                comparison_df = filtered_df[['State', 'Population', 'Modern_Slavery_Cases', 
                                          'Modern_Slavery_Index', 'Slavery_Rate_Per_1000']].copy()
                
                # Add percentage of total cases
                comparison_df['% of Total Cases'] = (comparison_df['Modern_Slavery_Cases'] / australia_total_cases * 100).round(2)
                
                # Add percentage of total population
                comparison_df['% of Total Population'] = (comparison_df['Population'] / australia_total_population * 100).round(2)
                
                # Rename columns for better display
                comparison_df.columns = ['State', 'Population', 'Cases', 'Index', 'Rate per 1000', '% of Total Cases', '% of Total Population']
                
                # Sort by the selected metric - map metric_option to the correct column name
                metric_column_map = {
                    'Modern_Slavery_Index': 'Index',
                    'Modern_Slavery_Cases': 'Cases', 
                    'Slavery_Rate_Per_1000': 'Rate per 1000'
                }
                sort_column = metric_column_map.get(metric_option, 'Index')
                comparison_df = comparison_df.sort_values(by=sort_column, ascending=False)
                
                st.dataframe(comparison_df, use_container_width=True)
                
                # Add insights
                st.markdown("### Key Insights")
                
                highest_state = comparison_df.iloc[0]['State']
                highest_value = comparison_df.iloc[0][sort_column]
                lowest_state = comparison_df.iloc[-1]['State']
                lowest_value = comparison_df.iloc[-1][sort_column]
                
                col_i1, col_i2 = st.columns(2)
                
                with col_i1:
                    st.success(f"**Highest {metric_option.replace('_', ' ')}**: {highest_state} ({highest_value})")
                
                with col_i2:
                    st.info(f"**Lowest {metric_option.replace('_', ' ')}**: {lowest_state} ({lowest_value})")
            
        elif country_option == "United States" and len(selected_states) > 0:
            # Create sample US states data
            us_data = {
                'State': selected_states,
                'Modern_Slavery_Index': [2.1, 2.3, 2.0, 1.8, 2.2, 1.9, 2.1, 2.4, 2.0, 2.2][:len(selected_states)],
                'Slavery_Rate_Per_1000': [1.5, 1.7, 1.4, 1.2, 1.6, 1.3, 1.5, 1.8, 1.4, 1.6][:len(selected_states)],
                'Modern_Slavery_Cases': [15000, 12000, 8000, 6000, 10000, 7000, 9000, 11000, 7500, 9500][:len(selected_states)]
            }
            us_df = pd.DataFrame(us_data)
            
            fig = px.bar(
                us_df,
                x='State',
                y=metric_option,
                color=metric_option,
                color_continuous_scale='Reds',
                title=f'{country_option} - {metric_option.replace("_", " ")} by State',
                labels={metric_option: metric_option.replace("_", " ")}
            )
            
            fig.update_layout(
                xaxis_title="State",
                yaxis_title=metric_option.replace("_", " "),
                showlegend=False,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif country_option == "United Kingdom" and len(selected_states) > 0:
            # Create sample UK cities data
            uk_cities_data = {
                'London': {'index': 2.1, 'rate': 1.5, 'cases': 12000, 'population': 8000000, 'lat': 51.5074, 'lon': -0.1278, 'size': 100},
                'Birmingham': {'index': 1.8, 'rate': 1.2, 'cases': 1500, 'population': 1250000, 'lat': 52.4862, 'lon': -1.8904, 'size': 80},
                'Manchester': {'index': 1.9, 'rate': 1.3, 'cases': 1200, 'population': 900000, 'lat': 53.4808, 'lon': -2.2426, 'size': 70},
                'Glasgow': {'index': 1.7, 'rate': 1.1, 'cases': 800, 'population': 700000, 'lat': 55.8642, 'lon': -4.2518, 'size': 60},
                'Liverpool': {'index': 1.6, 'rate': 1.0, 'cases': 600, 'population': 600000, 'lat': 53.4084, 'lon': -2.9916, 'size': 55},
                'Leeds': {'index': 1.5, 'rate': 0.9, 'cases': 500, 'population': 550000, 'lat': 53.8008, 'lon': -1.5491, 'size': 50},
                'Sheffield': {'index': 1.4, 'rate': 0.8, 'cases': 400, 'population': 500000, 'lat': 53.3811, 'lon': -1.4701, 'size': 45},
                'Edinburgh': {'index': 1.3, 'rate': 0.7, 'cases': 300, 'population': 450000, 'lat': 55.9533, 'lon': -3.1883, 'size': 40},
                'Bristol': {'index': 1.6, 'rate': 1.0, 'cases': 450, 'population': 450000, 'lat': 51.4545, 'lon': -2.5879, 'size': 45},
                'Cardiff': {'index': 1.5, 'rate': 0.9, 'cases': 350, 'population': 400000, 'lat': 51.4816, 'lon': -3.1791, 'size': 40},
                'Belfast': {'index': 1.4, 'rate': 0.8, 'cases': 250, 'population': 300000, 'lat': 54.5973, 'lon': -5.9301, 'size': 35},
                'Newcastle': {'index': 1.3, 'rate': 0.7, 'cases': 200, 'population': 300000, 'lat': 54.9783, 'lon': -1.6178, 'size': 35},
                'Nottingham': {'index': 1.2, 'rate': 0.6, 'cases': 180, 'population': 300000, 'lat': 52.9548, 'lon': -1.1581, 'size': 30},
                'Leicester': {'index': 1.1, 'rate': 0.5, 'cases': 150, 'population': 300000, 'lat': 52.6369, 'lon': -1.1398, 'size': 30},
                'Coventry': {'index': 1.0, 'rate': 0.4, 'cases': 120, 'population': 300000, 'lat': 52.4068, 'lon': -1.5197, 'size': 30},
                'Bradford': {'index': 1.2, 'rate': 0.6, 'cases': 140, 'population': 250000, 'lat': 53.7960, 'lon': -1.7594, 'size': 25},
                'Stoke-on-Trent': {'index': 1.1, 'rate': 0.5, 'cases': 100, 'population': 200000, 'lat': 53.0027, 'lon': -2.1794, 'size': 20},
                'Wolverhampton': {'index': 1.0, 'rate': 0.4, 'cases': 80, 'population': 200000, 'lat': 52.5869, 'lon': -2.1285, 'size': 20},
                'Plymouth': {'index': 0.9, 'rate': 0.3, 'cases': 60, 'population': 200000, 'lat': 50.3755, 'lon': -4.1427, 'size': 20},
                'Southampton': {'index': 1.1, 'rate': 0.5, 'cases': 90, 'population': 200000, 'lat': 50.9097, 'lon': -1.4044, 'size': 20}
            }
            
            # Create DataFrame with selected cities
            uk_data = []
            for city in selected_states:
                if city in uk_cities_data:
                    data = uk_cities_data[city]
                    uk_data.append({
                        'City': city,
                        'Modern_Slavery_Index': data['index'],
                        'Slavery_Rate_Per_1000': data['rate'],
                        'Modern_Slavery_Cases': data['cases'],
                        'Population': data['population'],
                        'lat': data['lat'],
                        'lon': data['lon'],
                        'size': data['size']
                    })
            
            uk_df = pd.DataFrame(uk_data)
            
            # Create UK cities map using scatter plot with circles
            st.markdown("### United Kingdom Cities Map")
            
            # Create scatter plot on map
            fig = px.scatter_mapbox(
                uk_df,
                lat='lat',
                lon='lon',
                size='size',
                color=metric_option,
                hover_name='City',
                hover_data={
                    'Modern_Slavery_Cases': True,
                    'Modern_Slavery_Index': True,
                    'Slavery_Rate_Per_1000': True,
                    'Population': True,
                    'lat': False,
                    'lon': False,
                    'size': False
                },
                color_continuous_scale='Reds',
                title=f'United Kingdom - {metric_option.replace("_", " ")} by City (Circle size represents city size)',
                mapbox_style="open-street-map",
                zoom=5,
                center=dict(lat=54.0, lon=-2.0)  # Center on UK
            )
            
            # Add city labels
            for _, row in uk_df.iterrows():
                city_name = row['City']
                # Get the value safely, fallback to original metric if Filtered_Metric doesn't exist
                if metric_option in row and not pd.isna(row[metric_option]):
                    value = row[metric_option]
                else:
                    value = row[original_metric] if original_metric in row else 0
                lat = row['lat']
                lon = row['lon']
                
                fig.add_annotation(
                    x=lon,
                    y=lat,
                    text=f"<b>{city_name}</b><br>{value:.1f}",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="black",
                    font=dict(size=11, color="black"),
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="black",
                    borderwidth=2
                )
            
            fig.update_layout(
                height=600,
                coloraxis_colorbar=dict(
                    title=dict(
                        text=metric_option.replace("_", " "),
                        side="right"
                    )
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Also show a horizontal bar chart for detailed comparison
            st.markdown("#### City Comparison Chart")
            bar_fig = px.bar(
                uk_df,
                x=metric_option,
                y='City',
                orientation='h',
                color=metric_option,
                color_continuous_scale='Reds',
                title=f'Detailed City Comparison - {metric_option.replace("_", " ")}',
                labels={metric_option: metric_option.replace("_", " ")}
            )
            
            bar_fig.update_layout(
                yaxis_title="City",
                xaxis_title=metric_option.replace("_", " "),
                showlegend=False,
                height=max(400, len(selected_states) * 40)
            )
            
            st.plotly_chart(bar_fig, use_container_width=True)
            
        else:
            st.info(f"Select states/regions for {country_option} to view detailed breakdowns.")
    
        # State/City details table
        if len(selected_states) > 0:
            st.markdown("### State/City Details")
            if country_option == "Australia":
                display_df = filtered_df[['State', 'Population', 'Modern_Slavery_Cases', 
                                         'Modern_Slavery_Index', 'Slavery_Rate_Per_1000']].copy()
                display_df.columns = ['State', 'Population', 'Cases', 'Index', 'Rate per 1000']
            elif country_option == "United States":
                display_df = us_df[['State', 'Modern_Slavery_Index', 'Slavery_Rate_Per_1000', 'Modern_Slavery_Cases']].copy()
                display_df.columns = ['State', 'Index', 'Rate per 1000', 'Cases']
            elif country_option == "United Kingdom":
                display_df = uk_df[['City', 'Population', 'Modern_Slavery_Cases', 'Modern_Slavery_Index', 'Slavery_Rate_Per_1000']].copy()
                display_df.columns = ['City', 'Population', 'Cases', 'Index', 'Rate per 1000']
            else:
                display_df = pd.DataFrame()
            
            if not display_df.empty:
                st.dataframe(display_df, use_container_width=True)

elif view_option == "State Comparison":
    if country_option == "Australia":
        st.markdown("## State Comparison")
        location_col = 'State'
        location_name = 'States'
    elif country_option == "United States":
        st.markdown("## State Comparison")
        location_col = 'State'
        location_name = 'States'
    elif country_option == "United Kingdom":
        st.markdown("## City Comparison")
        location_col = 'City'
        location_name = 'Cities'
    else:
        st.markdown("## Location Comparison")
        location_col = 'State'
        location_name = 'Locations'
    
    # Create comparison data based on country
    if country_option == "Australia":
        comparison_data = filtered_df
    elif country_option == "United States":
        # Create US data
        us_states = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania', 'Illinois', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']
        us_data = []
        for state in us_states:
            us_data.append({
                'State': state,
                'Modern_Slavery_Index': np.random.uniform(1.5, 2.5),
                'Slavery_Rate_Per_1000': np.random.uniform(0.8, 1.8),
                'Modern_Slavery_Cases': np.random.randint(200, 2000)
            })
        comparison_data = pd.DataFrame(us_data)
    elif country_option == "United Kingdom":
        # Create UK cities data
        uk_cities_data = {
            'London': {'index': 2.1, 'rate': 1.5, 'cases': 12000, 'population': 8000000},
            'Birmingham': {'index': 1.8, 'rate': 1.2, 'cases': 1500, 'population': 1250000},
            'Manchester': {'index': 1.9, 'rate': 1.3, 'cases': 1200, 'population': 900000},
            'Glasgow': {'index': 1.7, 'rate': 1.1, 'cases': 800, 'population': 700000},
            'Liverpool': {'index': 1.6, 'rate': 1.0, 'cases': 600, 'population': 600000},
            'Leeds': {'index': 1.5, 'rate': 0.9, 'cases': 500, 'population': 550000},
            'Sheffield': {'index': 1.4, 'rate': 0.8, 'cases': 400, 'population': 500000},
            'Edinburgh': {'index': 1.3, 'rate': 0.7, 'cases': 300, 'population': 450000},
            'Bristol': {'index': 1.6, 'rate': 1.0, 'cases': 450, 'population': 450000},
            'Cardiff': {'index': 1.5, 'rate': 0.9, 'cases': 350, 'population': 400000}
        }
        
        uk_data = []
        for city, data in uk_cities_data.items():
            uk_data.append({
                'City': city,
                'Modern_Slavery_Index': data['index'],
                'Slavery_Rate_Per_1000': data['rate'],
                'Modern_Slavery_Cases': data['cases'],
                'Population': data['population']
            })
        comparison_data = pd.DataFrame(uk_data)
    else:
        comparison_data = filtered_df
    
    # Bar chart comparison
    fig = px.bar(
        comparison_data, 
        x=location_col, 
        y=metric_option,
        title=f'{metric_option.replace("_", " ")} by {location_name}',
        color=metric_option,
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top 3 locations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### Highest Risk {location_name}")
        top_locations = comparison_data.nlargest(3, 'Modern_Slavery_Index')[[location_col, 'Modern_Slavery_Index']]
        for idx, row in top_locations.iterrows():
            st.markdown(f"**{row[location_col]}**: {row['Modern_Slavery_Index']:.1f}")
    
    with col2:
        st.markdown(f"### Lowest Risk {location_name}")
        low_locations = comparison_data.nsmallest(3, 'Modern_Slavery_Index')[[location_col, 'Modern_Slavery_Index']]
        for idx, row in low_locations.iterrows():
            st.markdown(f"**{row[location_col]}**: {row['Modern_Slavery_Index']:.1f}")

else:  # Slavery Types Analysis
    st.markdown("## Types of Modern Slavery Analysis")
    
    # Types of modern slavery information
    slavery_types = {
        'Human Trafficking': 'When a person uses coercion such as manipulation, control or violence, threats or lies to move someone across or within borders so they can be exploited.',
        'Forced Labour': 'When a person uses coercion such as manipulation, control or violence, threats or lies to make someone feel they cannot stop working or leave their place of work.',
        'Debt Bondage': 'When someone is forced to work to repay an excessive debt that they might never be able to pay off. The debt may be real or not.',
        'Forced Marriage': 'When a person is made to get married without their free and full consent. This means they did not agree to the marriage by their own choice. No child under 16 can legally agree to a marriage.',
        'Servitude': 'When a person uses coercion such as manipulation, control or violence, threats or lies so that a person feels they cannot stop working or leave their place of work.',
        'Child Labour': 'The worst forms of child labour is when children are in slavery or slavery-like practices such as forced labour, or do hazardous work.',
        'Deceptive Recruiting': 'When a person uses tricks or lies to recruit someone for a job involving exploitation.',
        'Sexual Exploitation': 'When someone is forced, coerced or deceived into prostitution or other sexual activities for the benefit of others.'
    }
    
    # Display slavery types cards
    col1, col2 = st.columns(2)
    
    slavery_columns = ['Human_Trafficking', 'Forced_Labour', 'Debt_Bondage', 'Forced_Marriage',
                      'Servitude', 'Child_Labour', 'Deceptive_Recruiting', 'Sexual_Exploitation']
    
    for i, col_name in enumerate(slavery_columns):
        formatted_name = col_name.replace('_', ' ')
        avg_rate = filtered_df[col_name].mean()
        
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="slavery-type-card">
                <div class="slavery-type-title">{formatted_name}</div>
                <div>Average Rate: {avg_rate:.1f} per 1000</div>
                <div style="margin-top: 0.5rem; font-size: 0.9rem;">
                    {slavery_types.get(formatted_name, 'Description not available')}
                </div>
            </div>
            """, unsafe_allow_html=True)
    ""
    # Heatmap of slavery types by state
    st.markdown("### Modern Slavery Types Heatmap")
    
    heatmap_data = filtered_df[['State'] + slavery_columns].set_index('State')
    
    fig = px.imshow(
        heatmap_data.T,
        labels=dict(x="State", y="Slavery Type", color="Rate per 1000"),
        x=heatmap_data.index,
        y=[col.replace('_', ' ') for col in slavery_columns],
        color_continuous_scale='Reds',
        aspect="auto"
    )
    
    fig.update_layout(
        title="Modern Slavery Types by State (Rate per 1000 people)",
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Modern Slavery Index | Data for educational purposes only</p>
    <p>Inspired by Walk Free's Global Slavery Index</p>
</div>
""", unsafe_allow_html=True)