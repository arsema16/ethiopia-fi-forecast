# Task 5: Interactive Dashboard - CORRECTED
# Forecasting Financial Inclusion in Ethiopia

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Forecast",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🇪🇹 Ethiopia Financial Inclusion Forecast</div>', unsafe_allow_html=True)
st.markdown("*2025-2027 Forecast Dashboard | Selam Analytics*")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["📊 Overview", "📈 Trends", "🎯 Forecasts", "📋 Insights", "ℹ️ About"]
)

# Load data
@st.cache_data
def load_data():
    """Load all data for the dashboard."""
    # Load enriched dataset
    df = pd.read_csv('data/raw/ethiopia_fi_unified_data.csv')
    df['observation_date'] = pd.to_datetime(df['observation_date'])
    
    # Try to load forecasts
    try:
        forecast_base = pd.read_csv('data/processed/forecast_base_2025_2027.csv', index_col=0)
        forecast_base.index = pd.to_datetime(forecast_base.index)
    except:
        forecast_base = pd.DataFrame()
    
    try:
        forecast_optimistic = pd.read_csv('data/processed/forecast_optimistic_2025_2027.csv', index_col=0)
        forecast_optimistic.index = pd.to_datetime(forecast_optimistic.index)
    except:
        forecast_optimistic = pd.DataFrame()
    
    try:
        forecast_pessimistic = pd.read_csv('data/processed/forecast_pessimistic_2025_2027.csv', index_col=0)
        forecast_pessimistic.index = pd.to_datetime(forecast_pessimistic.index)
    except:
        forecast_pessimistic = pd.DataFrame()
    
    return df, forecast_base, forecast_optimistic, forecast_pessimistic

df, forecast_base, forecast_optimistic, forecast_pessimistic = load_data()

# Helper functions
def get_latest_observations(df):
    """Get latest observations for key indicators."""
    observations = df[df['record_type'] == 'observation']
    
    # Get all available indicators
    indicators = observations['indicator_code'].unique()
    latest = {}
    
    for indicator in indicators:
        data = observations[observations['indicator_code'] == indicator]
        if len(data) > 0:
            latest_row = data.iloc[-1]
            latest[indicator] = {
                'value': latest_row['value_numeric'],
                'date': latest_row['observation_date'],
                'year': latest_row['observation_date'].year
            }
    
    return latest

latest = get_latest_observations(df)

# Page: Overview
if page == "📊 Overview":
    st.markdown('<div class="sub-header">📊 Overview Dashboard</div>', unsafe_allow_html=True)
    
    # Key Metrics - show all available indicators
    cols = st.columns(min(4, len(latest)))
    for idx, (indicator, data) in enumerate(latest.items()):
        if idx < 4:
            with cols[idx]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{data['value']:.1f}%</div>
                    <div class="metric-label">{indicator} ({data['year']})</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Historical Trends
    st.markdown("### Historical Trends")
    
    # Get observation data for plotting
    obs_data = df[df['record_type'] == 'observation']
    
    if len(obs_data) > 0:
        fig = make_subplots(rows=1, cols=1, subplot_titles=("Financial Inclusion Indicators"))
        
        # Plot each indicator
        for indicator in obs_data['indicator_code'].unique():
            data = obs_data[obs_data['indicator_code'] == indicator].sort_values('observation_date')
            fig.add_trace(
                go.Scatter(x=data['observation_date'], y=data['value_numeric'],
                          mode='lines+markers', name=indicator),
                row=1, col=1
            )
        
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No observation data available")
    
    # Event Timeline
    st.markdown("### Recent Events")
    events = df[df['record_type'] == 'event'].sort_values('observation_date', ascending=False).head(5)
    
    if len(events) > 0:
        # Find the correct column for event name
        event_name_col = None
        for col in events.columns:
            if 'indicator' in col.lower() or 'name' in col.lower() or 'description' in col.lower():
                if col != 'indicator_code' or len(events['indicator_code'].unique()) > 1:
                    event_name_col = col
                    break
        
        if event_name_col is None:
            event_name_col = events.columns[0]  # Fallback to first column
        
        for _, event in events.iterrows():
            event_name = event[event_name_col] if pd.notna(event[event_name_col]) else "Unnamed Event"
            category = event.get('category', 'N/A')
            year = event['observation_date'].year
            st.info(f"**{event_name}** - {category} ({year})")
    else:
        st.info("No events found in dataset")
    
    # Key Insight
    st.markdown("---")
    st.markdown("### 🔑 Key Insight")
    st.markdown("""
    <div class="insight-box">
        <b>Growth Deceleration Paradox:</b> Ethiopia's financial inclusion shows significant growth 
        potential despite recent slowdown. The gap between account ownership and active usage 
        represents a major opportunity for targeted interventions.
    </div>
    """, unsafe_allow_html=True)

# Page: Trends
elif page == "📈 Trends":
    st.markdown('<div class="sub-header">📈 Trends Analysis</div>', unsafe_allow_html=True)
    
    # Get available indicators
    obs_data = df[df['record_type'] == 'observation']
    indicators = obs_data['indicator_code'].unique().tolist()
    
    if len(indicators) > 0:
        # Indicator selector
        selected_indicator = st.selectbox("Select Indicator:", indicators)
        
        # Filter data
        data = obs_data[obs_data['indicator_code'] == selected_indicator].sort_values('observation_date')
        
        if len(data) > 0:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=data['observation_date'],
                y=data['value_numeric'],
                mode='lines+markers',
                name=selected_indicator,
                line=dict(width=2, color='#1f77b4'),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                title=f"{selected_indicator} Trend",
                xaxis_title="Year",
                yaxis_title="Value (%)",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Growth rates
            st.markdown("### Growth Rates")
            data['growth_pp'] = data['value_numeric'].diff()
            
            col1, col2 = st.columns(2)
            with col1:
                total_growth = data['growth_pp'].sum()
                st.metric(
                    "Total Growth",
                    f"{total_growth:.1f} pp",
                    delta=f"{data['growth_pp'].iloc[-1]:.1f} pp (latest)"
                )
            with col2:
                avg_growth = data['growth_pp'].mean()
                st.metric(
                    "Average Annual Growth",
                    f"{avg_growth:.1f} pp/year"
                )
        else:
            st.warning("No data available for selected indicator")
    else:
        st.warning("No indicators available in dataset")

# Page: Forecasts
elif page == "🎯 Forecasts":
    st.markdown('<div class="sub-header">🎯 Forecasts (2025-2027)</div>', unsafe_allow_html=True)
    
    if len(forecast_base) > 0:
        # Scenario selector
        scenario = st.selectbox(
            "Select Scenario:",
            ["Base", "Optimistic", "Pessimistic"]
        )
        
        # Get forecast data
        if scenario == "Base":
            forecast_data = forecast_base
        elif scenario == "Optimistic":
            forecast_data = forecast_optimistic if len(forecast_optimistic) > 0 else forecast_base
        else:
            forecast_data = forecast_pessimistic if len(forecast_pessimistic) > 0 else forecast_base
        
        # Get available indicators from forecast
        forecast_indicators = forecast_data.columns.tolist()
        
        if forecast_indicators:
            selected_forecast = st.multiselect(
                "Select Indicators:",
                forecast_indicators,
                default=forecast_indicators[:2] if len(forecast_indicators) >= 2 else forecast_indicators
            )
            
            if selected_forecast:
                # Create forecast plot
                fig = go.Figure()
                
                # Add each selected indicator
                for indicator in selected_forecast:
                    if indicator in forecast_data.columns:
                        # Get historical data for comparison
                        hist_data = obs_data[obs_data['indicator_code'] == indicator].sort_values('observation_date')
                        
                        if len(hist_data) > 0:
                            fig.add_trace(go.Scatter(
                                x=hist_data['observation_date'],
                                y=hist_data['value_numeric'],
                                mode='lines+markers',
                                name=f"{indicator} (Historical)",
                                line=dict(color='lightgray', dash='solid')
                            ))
                        
                        # Add forecast
                        fig.add_trace(go.Scatter(
                            x=forecast_data.index,
                            y=forecast_data[indicator],
                            mode='lines',
                            name=f"{indicator} ({scenario})",
                            line=dict(width=2)
                        ))
                
                fig.update_layout(
                    title=f"Forecast: {scenario} Scenario",
                    xaxis_title="Year",
                    yaxis_title="Value (%)",
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Forecast Table
                st.markdown("### Forecast Summary")
                
                # Create summary table
                summary_data = []
                for year in [2025, 2026, 2027]:
                    year_end = pd.Timestamp(f'{year}-12-31')
                    if year_end in forecast_data.index:
                        row = {'Year': year}
                        for indicator in selected_forecast:
                            if indicator in forecast_data.columns:
                                row[indicator] = f"{forecast_data.loc[year_end, indicator]:.1f}%"
                        summary_data.append(row)
                
                if summary_data:
                    summary_df = pd.DataFrame(summary_data)
                    st.dataframe(summary_df, use_container_width=True)
                
                # Target Progress
                st.markdown("### Progress Toward Targets")
                if 'ACC_OWNERSHIP' in forecast_data.columns:
                    last_value = forecast_data['ACC_OWNERSHIP'].iloc[-1]
                    target = 60
                    progress = min(last_value / target * 100, 100)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "2027 Projection",
                            f"{last_value:.1f}%",
                            delta=f"{last_value - 49:.1f} pp from 2024"
                        )
                    with col2:
                        st.metric(
                            "Target Progress",
                            f"{progress:.1f}%",
                            delta=f"{target - last_value:.1f} pp remaining"
                        )
                    
                    # Progress bar
                    st.progress(progress / 100)
        else:
            st.warning("No forecast indicators available")
    else:
        st.warning("Forecast data not available. Please run Task 4 first.")

# Page: Insights
elif page == "📋 Insights":
    st.markdown('<div class="sub-header">📋 Key Insights</div>', unsafe_allow_html=True)
    
    insights = [
        {
            "title": "1. Growth Deceleration",
            "description": "Account ownership growth slowed from +11pp (2017-2021) to +3pp (2021-2024) despite massive mobile money expansion.",
            "icon": "📉"
        },
        {
            "title": "2. Usage Gap",
            "description": "Significant gap exists between account ownership and active usage, representing a major opportunity for growth.",
            "icon": "📊"
        },
        {
            "title": "3. Event Impacts",
            "description": "Product launches like Telebirr and M-Pesa show 6-12 month lagged effects on usage indicators.",
            "icon": "🎯"
        },
        {
            "title": "4. Infrastructure Enablers",
            "description": "Mobile penetration and 4G coverage strongly correlate with digital payment adoption.",
            "icon": "🏗️"
        },
        {
            "title": "5. Ethiopia-Specific Dynamics",
            "description": "P2P dominates usage (used for commerce), mobile-only users are rare (~0.5%), and credit penetration is very low.",
            "icon": "🇪🇹"
        },
        {
            "title": "6. Forecast Drivers",
            "description": "M-Pesa expansion and EthSwitch Instant Pay are key drivers for 2025-2027 forecasts.",
            "icon": "🚀"
        },
        {
            "title": "7. Policy Recommendations",
            "description": "Focus on converting account ownership to active usage through targeted financial literacy programs.",
            "icon": "💡"
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for i, insight in enumerate(insights):
        with col1 if i % 2 == 0 else col2:
            with st.expander(f"{insight['icon']} {insight['title']}"):
                st.write(insight['description'])
    
    # Data Quality Assessment
    st.markdown("---")
    st.markdown("### Data Quality Assessment")
    
    if len(df) > 0:
        confidence_counts = df['confidence'].value_counts()
        
        if len(confidence_counts) > 0:
            quality_data = pd.DataFrame({
                "Category": confidence_counts.index.tolist(),
                "Percentage": (confidence_counts.values / len(df) * 100).round(1)
            })
            
            fig = px.bar(quality_data, x="Category", y="Percentage", 
                         title="Confidence Distribution",
                         color="Category",
                         color_discrete_sequence=["#2ecc71", "#f1c40f", "#e74c3c"])
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)

# Page: About
else:
    st.markdown('<div class="sub-header">ℹ️ About This Project</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Project Overview
    
    This dashboard is part of the **Ethiopia Financial Inclusion Forecasting System**, developed for 
    Selam Analytics as part of the 10 Academy AI Mastery Program (Week 11 Challenge).
    
    ### Stakeholders
    
    - **Development Finance Institutions**: Understanding investment effectiveness
    - **Mobile Money Operators** (Telebirr, M-Pesa): Strategic planning
    - **National Bank of Ethiopia**: Policy decision support
    
    ### Key Metrics
    
    - **Access**: Account Ownership Rate (Global Findex)
    - **Usage**: Digital Payment Adoption Rate (Global Findex)
    
    ### Methodology
    
    1. **Data Enrichment**: Unified schema with observations, events, impact_links
    2. **Exploratory Analysis**: Trend identification and pattern discovery
    3. **Event Impact Modeling**: Association matrix and impact estimation
    4. **Forecasting**: Linear trend models with event effects
    5. **Dashboard**: Interactive visualizations for stakeholders
    
    ### Forecasting Period
    
    **2025 - 2027** with three scenarios:
    - 🟢 Optimistic: Accelerated adoption
    - 🔵 Base: Expected outcomes
    - 🔴 Pessimistic: Slower adoption
    
    ### Data Sources
    
    - Global Findex Database
    - National Bank of Ethiopia
    - Ethio Telecom / EthSwitch
    - GSMA State of the Industry
    
    ### Repository
    
    [GitHub Repository](https://github.com/arsema16/ethiopia-fi-forecast)
    
    ### Team
    
    **Data Scientist**: ARSEMA TEFERA
    **Institution**: 10 Academy AI Mastery Program
    **Date**: July 2026
    
    ---
    
    *For more information, please refer to the project report.*
    """)

# Footer
st.markdown("---")
st.caption("© 2026 Selam Analytics | Ethiopia Financial Inclusion Forecast | 10 Academy AI Mastery Program")