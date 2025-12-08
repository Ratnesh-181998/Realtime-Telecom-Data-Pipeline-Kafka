"""
Telecom Data Pipeline Dashboard
Real-time visualization of streaming telecom data from Kafka to Postgres
"""
import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Page Configuration
st.set_page_config(
    page_title="Telecom Data Pipeline Dashboard",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e94560 !important;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #00d9ff !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
    }
    
    /* Cards */
    .css-1r6slb0, .css-12w0qpk {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f3460 100%) !important;
    }
    
    /* Text */
    .stMarkdown {
        color: #ffffff !important;
    }
    
    /* DataFrame */
    .dataframe {
        color: #ffffff !important;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
    }
    
    /* Pulse animation for live indicator */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #00ff00;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "port": "5438",
    "database": "telecom_db",
    "user": "admin",
    "password": "password"
}

@st.cache_resource
def get_connection():
    """Create database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def fetch_data():
    """Fetch all telecom data from Postgres."""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                caller_name, receiver_name, caller_id, receiver_id,
                start_datetime, end_datetime, call_duration,
                network_provider, total_amount
            FROM telecom_data
            ORDER BY start_datetime DESC
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def fetch_stats():
    """Fetch aggregate statistics."""
    conn = get_connection()
    if conn is None:
        return {}
    
    try:
        cursor = conn.cursor()
        
        # Total calls
        cursor.execute("SELECT COUNT(*) FROM telecom_data")
        total_calls = cursor.fetchone()[0]
        
        # Total revenue
        cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM telecom_data")
        total_revenue = cursor.fetchone()[0]
        
        # Average duration
        cursor.execute("SELECT COALESCE(AVG(call_duration), 0) FROM telecom_data")
        avg_duration = cursor.fetchone()[0]
        
        # Calls by provider
        cursor.execute("""
            SELECT network_provider, COUNT(*) as count, SUM(total_amount) as revenue
            FROM telecom_data
            GROUP BY network_provider
            ORDER BY count DESC
        """)
        provider_stats = cursor.fetchall()
        
        cursor.close()
        
        return {
            "total_calls": total_calls,
            "total_revenue": float(total_revenue),
            "avg_duration": float(avg_duration),
            "provider_stats": provider_stats
        }
    except Exception as e:
        st.error(f"Error fetching stats: {e}")
        return {}

# Sidebar
with st.sidebar:
    st.markdown("# 🎛️ Control Panel")
    st.markdown("---")
    
    # Auto-refresh toggle
    auto_refresh = st.toggle("🔄 Auto Refresh", value=True)
    refresh_rate = st.slider("Refresh Rate (seconds)", 5, 60, 10)
    
    st.markdown("---")
    st.markdown("### 📊 Data Pipeline Status")
    
    # Check connection
    conn = get_connection()
    if conn:
        st.markdown('<span class="live-indicator"></span> **Database Connected**', unsafe_allow_html=True)
        st.success("PostgreSQL: Online")
    else:
        st.error("PostgreSQL: Offline")
    
    st.markdown("---")
    st.markdown("### 🔧 Pipeline Components")
    st.info("📡 Kafka Producer → Broker → Consumer → PostgreSQL")
    
    st.markdown("---")
    st.markdown("### 👤 Created By")
    st.markdown("**Ratnesh Singh**")
    st.markdown("*Data Engineer*")

# Main Content
st.markdown("# 📞 Telecom Data Pipeline Dashboard")
st.markdown('<span class="live-indicator"></span> **LIVE** - Real-time Kafka Streaming Data', unsafe_allow_html=True)
st.markdown("---")

# Fetch data
stats = fetch_stats()
df = fetch_data()

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📱 Total Calls",
        value=f"{stats.get('total_calls', 0):,}",
        delta=None
    )

with col2:
    st.metric(
        label="💰 Total Revenue",
        value=f"${stats.get('total_revenue', 0):,.2f}",
        delta=None
    )

with col3:
    avg_min = stats.get('avg_duration', 0) / 60
    st.metric(
        label="⏱️ Avg Duration",
        value=f"{avg_min:.1f} min",
        delta=None
    )

with col4:
    st.metric(
        label="📡 Data Points",
        value=f"{len(df):,}",
        delta=None
    )

st.markdown("---")

# Charts Row
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Calls by Network Provider")
    if stats.get('provider_stats'):
        provider_df = pd.DataFrame(
            stats['provider_stats'],
            columns=['Provider', 'Calls', 'Revenue']
        )
        
        fig = px.pie(
            provider_df,
            values='Calls',
            names='Provider',
            color_discrete_sequence=px.colors.sequential.Plasma,
            hole=0.4
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available yet")

with col2:
    st.markdown("### 💵 Revenue by Provider")
    if stats.get('provider_stats'):
        fig = px.bar(
            provider_df,
            x='Provider',
            y='Revenue',
            color='Revenue',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available yet")

st.markdown("---")

# Call Duration Distribution
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⏱️ Call Duration Distribution")
    if not df.empty:
        fig = px.histogram(
            df,
            x='call_duration',
            nbins=30,
            color_discrete_sequence=['#00d9ff']
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title="Duration (seconds)",
            yaxis_title="Count",
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available yet")

with col2:
    st.markdown("### 💰 Revenue Distribution")
    if not df.empty:
        fig = px.box(
            df,
            x='network_provider',
            y='total_amount',
            color='network_provider',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False,
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available yet")

st.markdown("---")

# Recent Calls Table
st.markdown("### 📋 Recent Call Records")
if not df.empty:
    # Display last 20 records
    display_df = df.head(20)[['caller_name', 'receiver_name', 'call_duration', 'network_provider', 'total_amount', 'start_datetime']]
    display_df.columns = ['Caller', 'Receiver', 'Duration (s)', 'Provider', 'Amount ($)', 'Time']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("📭 No call records yet. Start the Kafka producer to generate data!")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p>🚀 <strong>Kafka-Spark-PostgreSQL Streaming Pipeline</strong></p>
    <p>Real-time data visualization powered by Streamlit</p>
    <p style='font-size: 0.8em;'>Built by <strong>Ratnesh Singh</strong> | Data Engineer Portfolio Project</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
