"""
Telecom Data Pipeline Dashboard - Enhanced Cloud Version
Premium UI with authentic graphs and detailed descriptions
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
import numpy as np
import time

# Page Configuration
st.set_page_config(
    page_title="Telecom Data Pipeline Dashboard",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-refresh every 30 seconds
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

current_time = time.time()
if current_time - st.session_state.last_refresh > 30:
    st.session_state.last_refresh = current_time
    st.rerun()

# Enhanced Custom CSS
st.markdown("""
<style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Headers with glow effect */
    h1, h2, h3 { 
        color: #00d4ff !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        color: #00ff88 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
    }
    
    [data-testid="stMetricLabel"] { 
        color: #ffffff !important;
        font-size: 1rem !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* Text colors - ensure visibility */
    .stMarkdown { color: #ffffff !important; }
    .stMarkdown p { color: #e0e0e0 !important; }
    .stMarkdown li { color: #e0e0e0 !important; }
    .stMarkdown strong { color: #ffffff !important; }
    
    /* Expander styling */
    .streamlit-expanderHeader { color: #ffffff !important; }
    .streamlit-expanderContent { color: #e0e0e0 !important; }
    
    /* Caption styling */
    .stCaption { color: #aaaaaa !important; }
    
    /* Info/Success boxes text */
    [data-testid="stAlert"] p { color: #ffffff !important; }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0, 0, 0, 0.3);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: white;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
        color: #000 !important;
    }
    
    /* Card styling */
    .info-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(0, 212, 255, 0.1), rgba(0, 255, 136, 0.05));
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        text-align: center;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, rgba(233, 69, 96, 0.2), rgba(255, 107, 107, 0.1));
        border-left: 4px solid #e94560;
        padding: 15px 20px;
        border-radius: 0 10px 10px 0;
        margin: 15px 0;
    }
    
    /* Pulse animation */
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .live-dot {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #00ff88;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse 1.5s infinite;
        box-shadow: 0 0 10px #00ff88;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
        color: #000;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Database connection function
def get_database_connection():
    """Try to connect to Supabase if credentials are available."""
    try:
        if 'SUPABASE_HOST' in st.secrets:
            import psycopg2
            conn = psycopg2.connect(
                host=st.secrets["SUPABASE_HOST"],
                port=st.secrets.get("SUPABASE_PORT", "5432"),
                database=st.secrets["SUPABASE_DB"],
                user=st.secrets["SUPABASE_USER"],
                password=st.secrets["SUPABASE_PASSWORD"]
            )
            # Test the connection
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM telecom_data")
            count = cursor.fetchone()[0]
            cursor.close()
            st.sidebar.success(f"✅ Connected! {count:,} rows in DB")
            return conn, "supabase"
    except Exception as e:
        st.sidebar.error(f"❌ Connection failed: {str(e)}")
        pass
    return None, "demo"

def generate_demo_data(n_records=200):
    """Generate realistic demo data."""
    np.random.seed(42)
    
    providers = ['Verizon', 'AT&T', 'T-Mobile', 'Sprint']
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Chris', 'Lisa', 
                   'James', 'Jennifer', 'Robert', 'Maria', 'William', 'Linda', 'Thomas',
                   'Jessica', 'Daniel', 'Ashley', 'Matthew', 'Amanda']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                  'Davis', 'Rodriguez', 'Martinez', 'Wilson', 'Anderson', 'Taylor', 'Thomas',
                  'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White']
    
    data = []
    base_time = datetime.now() - timedelta(hours=48)
    
    for i in range(n_records):
        caller = f"{random.choice(first_names)} {random.choice(last_names)}"
        receiver = f"{random.choice(first_names)} {random.choice(last_names)}"
        duration = random.randint(30, 1800)
        provider = random.choice(providers)
        amount = round((duration / 60) * 0.05, 2)
        
        start_time = base_time + timedelta(minutes=i * 14.4 + random.randint(0, 30))
        end_time = start_time + timedelta(seconds=duration)
        
        data.append({
            'caller_name': caller,
            'receiver_name': receiver,
            'caller_id': f'+1{random.randint(1000000000, 9999999999)}',
            'receiver_id': f'+1{random.randint(1000000000, 9999999999)}',
            'start_datetime': start_time,
            'end_datetime': end_time,
            'call_duration': duration,
            'network_provider': provider,
            'total_amount': amount
        })
    
    return pd.DataFrame(data)

def fetch_data_from_db(conn):
    """Fetch data from the database."""
    query = """
        SELECT caller_name, receiver_name, caller_id, receiver_id,
               start_datetime, end_datetime, call_duration,
               network_provider, total_amount
        FROM telecom_data
        ORDER BY start_datetime DESC
        LIMIT 5000
    """
    return pd.read_sql(query, conn)

# Sidebar
with st.sidebar:
    st.markdown("# 🎛️ Dashboard Control")
    st.markdown("---")
    
    conn, mode = get_database_connection()
    
    if mode == "supabase":
        st.markdown('<div class="metric-card"><span class="live-dot"></span><strong>LIVE DATA</strong><br><small>Connected to Supabase</small></div>', unsafe_allow_html=True)
    else:
        st.info("📊 Demo Mode")
    
    st.markdown("---")
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    
    # Get data for sidebar stats
    if mode == "supabase":
        df_stats = fetch_data_from_db(conn)
    else:
        df_stats = generate_demo_data(200)
    
    st.metric("Total Records", f"{len(df_stats):,}")
    st.metric("Avg Call Duration", f"{df_stats['call_duration'].mean()/60:.1f} min")
    
    st.markdown("---")
    st.markdown("### 👤 Created By")
    st.markdown("**Ratnesh Singh**")
    st.markdown("*Data Scientist*")
    st.markdown("[GitHub](https://github.com/Ratnesh-181998) | [LinkedIn](https://www.linkedin.com/in/ratneshkumar1998/)")

# Main Title with animation and author info
st.markdown("""
<div style="position: relative; text-align: center; padding: 20px 250px 20px 20px; min-height: 120px;">
    <div style="position: absolute; top: 10px; right: 20px; text-align: right; z-index: 10;">
        <div style="background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(0, 255, 136, 0.1)); 
                    backdrop-filter: blur(10px); 
                    border: 1px solid rgba(0, 212, 255, 0.3); 
                    border-radius: 12px; 
                    padding: 12px 20px;
                    box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2);
                    min-width: 200px;">
            <p style="margin: 0; font-size: 1.1rem; color: #00d4ff; font-weight: 700; letter-spacing: 0.5px; white-space: nowrap;">
                Ratnesh Singh
            </p>
            <p style="margin: 2px 0 0 0; font-size: 0.85rem; color: #00ff88; font-weight: 500; white-space: nowrap;">
                Data Scientist
            </p>
            <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: #aaa; font-style: italic; white-space: nowrap;">
                4+ Years Experience
            </p>
        </div>
    </div>
    <h1 style="font-size: 2.5rem; margin-bottom: 10px; max-width: calc(100% - 250px); margin-left: auto; margin-right: auto;">📞 Telecom Data Pipeline Using Kafka</h1>
    <p style="font-size: 1.1rem; color: #888;">Real-Time Streaming Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Create Tabs with icons
tab1, tab2, tab3 = st.tabs(["📊 Live Analytics", "🏗️ Architecture & Tech Stack", "ℹ️ Project Documentation"])

# Get data
conn, mode = get_database_connection()
if mode == "supabase":
    df = fetch_data_from_db(conn)
    data_source = "🟢 Live Supabase Data"
else:
    df = generate_demo_data(200)
    data_source = "📊 Demo Data"

# ==================== TAB 1: LIVE ANALYTICS ====================
with tab1:
    # Calculate time until next refresh
    time_since_refresh = int(current_time - st.session_state.last_refresh)
    time_until_refresh = 30 - time_since_refresh
    
    st.markdown(f'''
    <div style="text-align: center; background: rgba(0,212,255,0.1); padding: 10px; border-radius: 10px; margin-bottom: 20px;">
        <span class="live-dot"></span>
        <strong>{data_source}</strong> | 
        Last updated: {datetime.now().strftime("%H:%M:%S")} | 
        Total Records: {len(df):,} | 
        <span style="color: #00ff88;">Auto-refresh in {time_until_refresh}s</span>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("")
    
    # Calculate statistics
    total_calls = len(df)
    total_revenue = df['total_amount'].sum()
    avg_duration = df['call_duration'].mean() / 60
    total_minutes = df['call_duration'].sum() / 60
    
    # Top Metrics with enhanced styling
    st.markdown("### 📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #00ff88; margin: 0;">📞</h2>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Total Calls", f"{total_calls:,}")
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #00d4ff; margin: 0;">💰</h2>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #ff6b6b; margin: 0;">⏱️</h2>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Avg Duration", f"{avg_duration:.1f} min")
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #ffd93d; margin: 0;">📊</h2>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Total Minutes", f"{total_minutes:,.0f}")
    
    st.markdown("---")
    
    # Provider Statistics
    provider_stats = df.groupby('network_provider').agg({
        'caller_name': 'count',
        'total_amount': 'sum',
        'call_duration': 'mean'
    }).rename(columns={'caller_name': 'Calls', 'total_amount': 'Revenue', 'call_duration': 'Avg Duration'}).reset_index()
    provider_stats.columns = ['Provider', 'Calls', 'Revenue', 'Avg Duration']
    provider_stats['Avg Duration'] = provider_stats['Avg Duration'] / 60
    
    st.markdown("### 📊 Network Provider Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Donut Chart
        fig = go.Figure(data=[go.Pie(
            labels=provider_stats['Provider'],
            values=provider_stats['Calls'],
            hole=0.6,
            marker=dict(colors=['#00d4ff', '#00ff88', '#ff6b6b', '#ffd93d']),
            textinfo='label+percent',
            textfont=dict(size=14, color='white'),
            hovertemplate="<b>%{label}</b><br>Calls: %{value:,}<br>Share: %{percent}<extra></extra>"
        )])
        fig.update_layout(
            title=dict(text="📱 Call Distribution by Provider", font=dict(size=18, color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=12)),
            annotations=[dict(text=f'{total_calls:,}<br>Total', x=0.5, y=0.5, 
                            font=dict(size=20, color='white'), showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Enhanced Bar Chart with gradient colors
        fig = go.Figure(data=[go.Bar(
            x=provider_stats['Provider'],
            y=provider_stats['Revenue'],
            marker=dict(
                color=provider_stats['Revenue'],
                colorscale=[[0, '#00d4ff'], [0.5, '#00ff88'], [1, '#ffd93d']],
                line=dict(width=0)
            ),
            text=[f'${x:,.2f}' for x in provider_stats['Revenue']],
            textposition='outside',
            textfont=dict(color='white', size=14),
            hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>"
        )])
        fig.update_layout(
            title=dict(text="💵 Revenue by Provider", font=dict(size=18, color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=14)),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=12)),
            bargap=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Time Series Analysis
    st.markdown("### 📈 Call Activity Timeline")
    
    df_sorted = df.sort_values('start_datetime')
    df_sorted['hour'] = pd.to_datetime(df_sorted['start_datetime']).dt.floor('h')
    hourly_data = df_sorted.groupby('hour').agg({
        'caller_name': 'count',
        'total_amount': 'sum'
    }).reset_index()
    hourly_data.columns = ['Hour', 'Calls', 'Revenue']
    
    # Create dual-axis chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=hourly_data['Hour'], y=hourly_data['Calls'], 
                   name="Calls", line=dict(color='#00d4ff', width=3),
                   fill='tozeroy', fillcolor='rgba(0, 212, 255, 0.2)',
                   hovertemplate="Time: %{x}<br>Calls: %{y}<extra></extra>"),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=hourly_data['Hour'], y=hourly_data['Revenue'], 
                   name="Revenue ($)", line=dict(color='#00ff88', width=3, dash='dot'),
                   hovertemplate="Time: %{x}<br>Revenue: $%{y:.2f}<extra></extra>"),
        secondary_y=True
    )
    
    fig.update_layout(
        title=dict(text="Hourly Call Volume & Revenue Trend", font=dict(size=18, color='white')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    fig.update_yaxes(title_text="Number of Calls", secondary_y=False, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(title_text="Revenue ($)", secondary_y=True, gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Distribution Charts
    st.markdown("### 📊 Data Distribution Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Call Duration Histogram
        fig = go.Figure(data=[go.Histogram(
            x=df['call_duration'] / 60,
            nbinsx=25,
            marker=dict(color='#00d4ff', line=dict(color='#00ff88', width=1)),
            hovertemplate="Duration: %{x:.1f} min<br>Count: %{y}<extra></extra>"
        )])
        fig.update_layout(
            title=dict(text="⏱️ Call Duration Distribution", font=dict(size=16, color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(title="Duration (minutes)", gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="Frequency", gridcolor='rgba(255,255,255,0.1)'),
            bargap=0.1
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Box Plot by Provider
        fig = go.Figure()
        colors = ['#00d4ff', '#00ff88', '#ff6b6b', '#ffd93d']
        for i, provider in enumerate(df['network_provider'].unique()):
            provider_data = df[df['network_provider'] == provider]['call_duration'] / 60
            fig.add_trace(go.Box(
                y=provider_data,
                name=provider,
                marker_color=colors[i % len(colors)],
                boxpoints='outliers'
            ))
        fig.update_layout(
            title=dict(text="📦 Duration by Provider (Box Plot)", font=dict(size=16, color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            yaxis=dict(title="Duration (minutes)", gridcolor='rgba(255,255,255,0.1)'),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recent Calls Table
    st.markdown("### 📋 Recent Call Records")
    st.markdown(f"*Showing latest 20 of {len(df):,} records*")
    
    display_df = df.head(20)[['caller_name', 'receiver_name', 'call_duration', 
                              'network_provider', 'total_amount', 'start_datetime']].copy()
    display_df['call_duration'] = display_df['call_duration'].apply(lambda x: f"{x//60}m {x%60}s")
    display_df['total_amount'] = display_df['total_amount'].apply(lambda x: f"${x:.2f}")
    display_df.columns = ['📞 Caller', '📱 Receiver', '⏱️ Duration', '📡 Provider', '💰 Amount', '🕐 Time']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ==================== TAB 2: ARCHITECTURE ====================
with tab2:
    st.markdown("## 🏗️ System Architecture & Technology Stack")
    st.markdown("---")
    
    # Visual Architecture Diagram
    st.markdown("### 📐 Data Flow Architecture")
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px; margin: 20px 0;">
        <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px 30px; border-radius: 15px; min-width: 150px;">
                <span style="display: block; font-size: 1.5rem; color: black; font-weight: 800; margin-bottom: 8px;">📝 Producer</span>
                <span style="display: block; font-size: 0.85rem; color: black; font-weight: 600; margin-bottom: 4px;">kafka_producer.py</span>
                <span style="display: block; font-size: 0.75rem; color: black; font-weight: 500;">Generates CDRs</span>
            </div>
            <span style="font-size: 2rem; color: white; font-weight: bold;">➜</span>
            <div style="background: linear-gradient(135deg, #f093fb, #f5576c); padding: 20px 30px; border-radius: 15px; min-width: 150px;">
                <span style="display: block; font-size: 1.5rem; color: black; font-weight: 800; margin-bottom: 8px;">📨 Kafka</span>
                <span style="display: block; font-size: 0.85rem; color: black; font-weight: 600; margin-bottom: 4px;">Message Broker</span>
                <span style="display: block; font-size: 0.75rem; color: black; font-weight: 500;">Topic: telecom-data</span>
            </div>
            <span style="font-size: 2rem; color: white; font-weight: bold;">➜</span>
            <div style="background: linear-gradient(135deg, #4facfe, #00f2fe); padding: 20px 30px; border-radius: 15px; min-width: 150px;">
                <span style="display: block; font-size: 1.5rem; color: black; font-weight: 800; margin-bottom: 8px;">🔄 Consumer</span>
                <span style="display: block; font-size: 0.85rem; color: black; font-weight: 600; margin-bottom: 4px;">kafka_to_postgres.py</span>
                <span style="display: block; font-size: 0.75rem; color: black; font-weight: 500;">Process & Save</span>
            </div>
            <span style="font-size: 2rem; color: white; font-weight: bold;">➜</span>
            <div style="background: linear-gradient(135deg, #43e97b, #38f9d7); padding: 20px 30px; border-radius: 15px; min-width: 150px;">
                <span style="display: block; font-size: 1.5rem; color: black; font-weight: 800; margin-bottom: 8px;">🗄️ Database</span>
                <span style="display: block; font-size: 0.85rem; color: black; font-weight: 600; margin-bottom: 4px;">PostgreSQL/Supabase</span>
                <span style="display: block; font-size: 0.75rem; color: black; font-weight: 500;">Data Warehouse</span>
            </div>
        </div>
        <div style="margin-top: 30px; font-size: 3rem; color: white;">⬇️</div>
        <div style="background: linear-gradient(135deg, #fa709a, #fee140); padding: 25px 40px; border-radius: 15px; display: inline-block; margin-top: 10px;">
            <span style="display: block; font-size: 1.5rem; color: black; font-weight: 800; margin-bottom: 8px;">📊 This Dashboard</span>
            <span style="display: block; font-size: 0.85rem; color: black; font-weight: 600; margin-bottom: 4px;">Streamlit + Plotly</span>
            <span style="display: block; font-size: 0.75rem; color: black; font-weight: 500;">Real-time Visualization</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technology Stack Cards
    st.markdown("### 🛠️ Technology Stack Details")
    
    col1, col2, col3, col4 = st.columns(4)
    
    tech_stack = [
        {"icon": "🐍", "name": "Python 3.11", "desc": "Core Language", 
         "tools": ["kafka-python-ng", "psycopg2", "pandas", "Faker", "PySpark"]},
        {"icon": "📨", "name": "Apache Kafka", "desc": "Stream Processing", 
         "tools": ["Zookeeper", "Kafka Broker", "Schema Registry", "Control Center"]},
        {"icon": "🐘", "name": "PostgreSQL", "desc": "Data Storage", 
         "tools": ["Supabase (Cloud)", "Docker (Local)", "JDBC Driver", "SQL Queries"]},
        {"icon": "🐳", "name": "Docker", "desc": "Containerization", 
         "tools": ["Docker Compose", "Multi-container", "Network Isolation", "Volume Mounts"]}
    ]
    
    for i, tech in enumerate(tech_stack):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="info-card" style="text-align: center; min-height: 280px;">
                <div style="font-size: 3rem;">{tech['icon']}</div>
                <h3 style="color: #00d4ff; margin: 10px 0;">{tech['name']}</h3>
                <p style="color: #888;">{tech['desc']}</p>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <ul style="text-align: left; padding-left: 20px; font-size: 0.9rem;">
                    {''.join([f'<li>{t}</li>' for t in tech['tools']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step by Step Process
    st.markdown("### 🔄 Data Processing Pipeline Steps")
    
    steps = [
        {"num": "01", "title": "Data Generation", "icon": "📝",
         "desc": "Python script generates realistic telecom Call Detail Records (CDRs) using the Faker library. Each record contains caller info, receiver info, duration, provider, and billing amount."},
        {"num": "02", "title": "Kafka Publishing", "icon": "📤",
         "desc": "Generated records are serialized to JSON and published to the 'telecom-data' Kafka topic. Kafka provides fault-tolerant, distributed message queuing."},
        {"num": "03", "title": "Stream Consumption", "icon": "📥",
         "desc": "Consumer application subscribes to the Kafka topic and reads messages in real-time. Data validation ensures only quality records are processed."},
        {"num": "04", "title": "Database Storage", "icon": "💾",
         "desc": "Valid records are inserted into PostgreSQL (locally) or Supabase (cloud). The database schema is optimized for analytics queries."},
        {"num": "05", "title": "Visualization", "icon": "📊",
         "desc": "This Streamlit dashboard queries the database and renders interactive Plotly charts. Auto-refresh keeps data current."}
    ]
    
    for step in steps:
        st.markdown(f"""
        <div class="info-card" style="display: flex; align-items: center; gap: 20px;">
            <div style="background: linear-gradient(135deg, #00d4ff, #00ff88); color: #000; font-size: 1.5rem; font-weight: bold; 
                        width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                {step['num']}
            </div>
            <div style="flex: 1;">
                <h4 style="margin: 0; color: #00d4ff;">{step['icon']} {step['title']}</h4>
                <p style="margin: 5px 0; color: #ccc;">{step['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How to Run
    st.markdown("### 🚀 How to Run This Project")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚙️ Prerequisites")
        st.markdown("""
        - ✅ **Docker Desktop** - For Kafka & PostgreSQL containers
        - ✅ **Python 3.8+** - For running scripts
        - ✅ **Java 11/17** - Required for Spark (optional)
        - ✅ **Git** - For version control
        """)
        
        st.markdown("#### 📦 Installation")
        st.code("""# Clone repository
git clone https://github.com/Ratnesh-181998/kafka-streaming.git
cd kafka-streaming

# Install dependencies
pip install -r requirements.txt

# Start Docker containers
docker-compose up -d

# Wait for services to be healthy
docker-compose ps""", language="bash")
    
    with col2:
        st.markdown("#### ▶️ Running the Pipeline")
        st.code("""# Terminal 1: Start Kafka Producer
python kafka_producer.py

# Terminal 2: Start Consumer
python kafka_to_postgres.py

# Terminal 3: Start Dashboard
streamlit run streamlit_app.py

# Open browser: http://localhost:8501""", language="bash")
        
        st.markdown("#### 🔍 Verify Data")
        st.code("""# Check database
python postgres_connect.py

# Query directly
docker exec -it postgres psql -U admin -d telecom_db \\
  -c "SELECT COUNT(*) FROM telecom_data;" """, language="bash")

# ==================== TAB 3: ABOUT ====================
with tab3:
    st.markdown("## ℹ️ Project Documentation")
    st.markdown("*A complete guide to understanding this project - written for everyone!*")
    st.markdown("---")
    
    # Simple Introduction
    st.markdown("### 📚 What is This Project? (Simple Explanation)")
    
    st.markdown("""
    <div class="info-card">
        <p style="font-size: 1.2rem; line-height: 2;">
            Imagine you run a <strong>telephone company</strong> 📞. Every time someone makes a call, 
            you need to know: <em>Who called? Who did they call? How long was the call? How much to charge?</em>
        </p>
        <p style="font-size: 1.2rem; line-height: 2;">
            With <strong>millions of calls happening every minute</strong>, you can't wait until the end of 
            the day to process this data. You need to see it <strong>RIGHT NOW</strong> - in real-time!
        </p>
        <p style="font-size: 1.2rem; line-height: 2;">
            <strong>This project shows how to build such a system.</strong> It captures call data as it happens, 
            processes it instantly, stores it safely, and shows beautiful charts - all in real-time! 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Real World Analogy
    st.markdown("### 🍕 Understanding With a Pizza Shop Analogy")
    
    st.markdown("**Let's understand this with a simple example!** 🍕")
    st.markdown("")
    
    st.markdown("**Imagine a busy pizza shop:**")
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 2, 1, 2, 1, 2])
    with col1:
        st.markdown("**👨‍🍳 Pizza Orders**")
        st.caption("Customers placing orders")
    with col2:
        st.markdown("### →")
    with col3:
        st.markdown("**📝 Order Tickets**")
        st.caption("Written on paper slips")
    with col4:
        st.markdown("### →")
    with col5:
        st.markdown("**👨‍🍳 Kitchen**")
        st.caption("Cooks make the pizza")
    with col6:
        st.markdown("### →")
    with col7:
        st.markdown("**📊 Sales Report**")
        st.caption("Manager sees all orders")
    
    st.markdown("")
    st.markdown("**Now in our project:**")
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 2, 1, 2, 1, 2])
    with col1:
        st.info("**📞 Phone Calls**\n\nPeople making calls")
    with col2:
        st.markdown("### →")
    with col3:
        st.info("**📨 Kafka**\n\nMessage queue")
    with col4:
        st.markdown("### →")
    with col5:
        st.info("**🔄 Consumer**\n\nProcesses the data")
    with col6:
        st.markdown("### →")
    with col7:
        st.success("**📊 Dashboard**\n\nYou see live charts!")
    
    st.markdown("---")
    
    # Step by Step Journey
    st.markdown("### 🚶 Follow the Data Journey (Step by Step)")
    st.markdown("**🎬 Let's follow one phone call through our system:**")
    
    steps_simple = [
        ("1️⃣", "📞 A Call is Made", 
         "John calls his friend Sarah. They talk for 5 minutes.",
         "The producer script creates a record with all details."),
        ("2️⃣", "📝 Record is Created", 
         "The system writes down: 'John → Sarah, 5 minutes, Verizon, $0.25'",
         "A JSON object is created with caller_name, receiver_name, duration, etc."),
        ("3️⃣", "📨 Sent to Kafka", 
         "Like putting a letter in a mailbox - Kafka safely holds the message.",
         "The record is published to the 'telecom-data' Kafka topic."),
        ("4️⃣", "📥 Consumer Picks It Up", 
         "Like a mailman - the consumer collects and delivers the message.",
         "The consumer reads from Kafka and validates the data."),
        ("5️⃣", "💾 Saved to Database", 
         "The call record is filed away in a giant filing cabinet (database).",
         "Data is inserted into the PostgreSQL/Supabase database."),
        ("6️⃣", "📊 Shown on Dashboard", 
         "You see John's call appear in the charts - instantly!",
         "Streamlit queries the database and updates the Plotly visualizations.")
    ]
    
    for num, title, simple, technical in steps_simple:
        with st.expander(f"{num} {title}", expanded=True):
            st.markdown(f"**🗣️ Simple:** {simple}")
            st.caption(f"🔧 Technical: {technical}")
    
    st.markdown("---")
    
    # Components Explained Simply
    st.markdown("### 🧩 What Does Each Part Do? (Super Simple!)")
    
    components_simple = [
        {
            "icon": "📝",
            "name": "Kafka Producer",
            "analogy": "Like a news reporter",
            "simple": "It creates fake phone call data. In real life, this would be connected to actual phone towers!",
            "example": "Creates: 'John called Sarah for 5 minutes on Verizon'"
        },
        {
            "icon": "📨",
            "name": "Apache Kafka", 
            "analogy": "Like a post office",
            "simple": "It safely holds messages until someone picks them up. Even if the database is busy, no message is lost!",
            "example": "Holds the message until the consumer is ready"
        },
        {
            "icon": "🔄",
            "name": "Consumer",
            "analogy": "Like a mailman + secretary",
            "simple": "It picks up messages from Kafka, checks if they're valid, and files them in the database.",
            "example": "Reads the message, checks 'Is duration > 0?', then saves it"
        },
        {
            "icon": "🗄️",
            "name": "PostgreSQL Database",
            "analogy": "Like a giant filing cabinet",
            "simple": "Stores all the call records permanently. You can search, filter, and analyze millions of records!",
            "example": "Stores 'John → Sarah, 5 min, $0.25' in a table"
        },
        {
            "icon": "📊",
            "name": "Streamlit Dashboard",
            "analogy": "Like a TV news screen",
            "simple": "Shows beautiful charts and graphs so you can understand the data at a glance!",
            "example": "Shows pie charts, bar graphs, and tables - like this page!"
        }
    ]
    
    for comp in components_simple:
        with st.expander(f"{comp['icon']} {comp['name']} - {comp['analogy']}", expanded=False):
            st.markdown(f"""
            **🎯 What it does:** {comp['simple']}
            
            **📍 Example:** {comp['example']}
            """)
    
    st.markdown("---")
    
    # Why This Matters
    st.markdown("### 🤔 Why Should You Care About This?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>🌍 This Technology is Everywhere!</h4>
            <p>Every time you:</p>
            <ul style="line-height: 2;">
                <li>📱 <strong>Use Uber/Lyft</strong> - Real-time driver tracking</li>
                <li>🎬 <strong>Watch Netflix</strong> - Recommendations update instantly</li>
                <li>💳 <strong>Swipe your card</strong> - Fraud detection in milliseconds</li>
                <li>📦 <strong>Track a package</strong> - Live location updates</li>
                <li>🎮 <strong>Play online games</strong> - Real-time leaderboards</li>
            </ul>
            <p><strong>All use streaming technology like this!</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>💼 Why Companies Need This</h4>
            <p>Without real-time processing:</p>
            <ul style="line-height: 2;">
                <li>❌ Fraud goes undetected for hours</li>
                <li>❌ Customers wait for slow reports</li>
                <li>❌ Business decisions are delayed</li>
                <li>❌ Competitive disadvantage</li>
            </ul>
            <p><strong>With real-time processing:</strong></p>
            <ul style="line-height: 2;">
                <li>✅ Instant alerts and actions</li>
                <li>✅ Happy customers</li>
                <li>✅ Better decisions</li>
                <li>✅ More money! 💰</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # FAQ for Beginners
    st.markdown("### ❓ Common Questions (Beginner-Friendly)")
    
    faqs = [
        ("What is 'streaming' data?", 
         "Think of it like a river 🌊 - data flows continuously, not in buckets. Instead of waiting to collect a day's worth of data, we process each piece as it arrives!"),
        ("What is Kafka?", 
         "Kafka is like a super-reliable post office 📮. It receives messages, stores them safely, and delivers them to the right place. Even if the recipient is busy, the message won't be lost!"),
        ("Why not just save directly to the database?", 
         "Imagine a restaurant 🍽️ - you don't have waiters run directly to the kitchen. They put orders on a ticket system. Kafka is that ticket system - it handles busy times smoothly!"),
        ("What is Docker?", 
         "Docker is like a shipping container 📦 for software. Instead of installing Kafka, Postgres, etc. separately, Docker packages everything together so it works the same everywhere!"),
        ("Is this used in real companies?", 
         "Absolutely! Netflix processes billions of events/day with Kafka. Uber uses it for real-time pricing. LinkedIn uses it for activity feeds. This is industry-standard technology! 🏢"),
        ("Can I learn this too?", 
         "Yes! This project is a great starting point. Start by understanding the flow (Producer → Kafka → Consumer → Database → Dashboard), then dive deeper into each part. 📚")
    ]
    
    for q, a in faqs:
        with st.expander(f"🤔 {q}"):
            st.markdown(f"**Answer:** {a}")
    
    st.markdown("---")
    
    # Skills Summary
    st.markdown("### 🎓 What Skills Does This Project Show?")
    
    st.markdown("""
    <div class="info-card">
        <table style="width: 100%;">
            <tr>
                <td style="padding: 15px; vertical-align: top;">
                    <h4>👨‍💻 Programming</h4>
                    <ul>
                        <li>Python scripting</li>
                        <li>Working with JSON data</li>
                        <li>Error handling</li>
                        <li>Clean code practices</li>
                    </ul>
                </td>
                <td style="padding: 15px; vertical-align: top;">
                    <h4>🔧 Data Engineering</h4>
                    <ul>
                        <li>Building data pipelines</li>
                        <li>Stream processing</li>
                        <li>Data validation</li>
                        <li>ETL (Extract, Transform, Load)</li>
                    </ul>
                </td>
                <td style="padding: 15px; vertical-align: top;">
                    <h4>☁️ DevOps</h4>
                    <ul>
                        <li>Docker containers</li>
                        <li>Docker Compose</li>
                        <li>Cloud deployment</li>
                        <li>Environment management</li>
                    </ul>
                </td>
                <td style="padding: 15px; vertical-align: top;">
                    <h4>📊 Visualization</h4>
                    <ul>
                        <li>Dashboard design</li>
                        <li>Interactive charts</li>
                        <li>Streamlit framework</li>
                        <li>User experience</li>
                    </ul>
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About Author
    st.markdown("### 👨‍💻 About the Creator")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="width: 150px; height: 150px; background: linear-gradient(135deg, #00d4ff, #00ff88); 
                        border-radius: 50%; margin: 0 auto; display: flex; align-items: center; 
                        justify-content: center; font-size: 4rem; box-shadow: 0 0 30px rgba(0,212,255,0.5);">
                👨‍💻
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### Ratnesh Singh
        **Data Scientist** 
        
        I'm passionate about making complex data systems understandable and accessible. 
        This project demonstrates how real companies handle massive amounts of data in real-time.
        
        **Want to connect?**
        - 🔗 [LinkedIn](https://www.linkedin.com/in/ratneshkumar1998/) - Let's network!
        - 💻 [GitHub](https://github.com/Ratnesh-181998) - See more projects
        - 📧 rattudacsit2021gate@gmail.com - Say hello!
        
        *Feel free to reach out if you have questions about this project or data engineering in general!*
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 30px;'>
    <p style="font-size: 1.2rem;">🚀 <strong>Real-Time Telecom Data Pipelin Using Kafkae,Spark and Redshift</strong></p>
    <p>From phone calls to beautiful charts - in milliseconds!</p>
    <p style='font-size: 0.9rem; margin-top: 15px;'>
        Built with ❤️ by <strong>Ratnesh Singh</strong> | Data Scientist
    </p>
</div>
""", unsafe_allow_html=True)
