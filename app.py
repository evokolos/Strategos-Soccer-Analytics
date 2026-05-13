import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Strategós Soccer Analytics", layout="wide")

# CUSTOM CSS: Professional Contrast & Mobile Optimization
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #00d4ff !important;
        padding: 15px !important;
        border-radius: 12px !important;
    }
    [data-testid="stMetricLabel"] { color: #000000 !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #007bff !important; font-weight: 800 !important; }
    .main { background-color: #0e1117; }
    
    .mobile-hint {
        background-color: #ff4b4b;
        color: white;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
    }
    .guide-header { color: #00d4ff; font-weight: 800; font-size: 1.2rem; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINES ---
@st.cache_data
def get_data():
    matches = sb.matches(competition_id=43, season_id=106)
    matches['label'] = matches['home_team'] + " vs " + matches['away_team']
    return matches

@st.cache_data
def get_events(match_id):
    events = sb.events(match_id=match_id)
    df = events[events['type'] == 'Pass'].copy()
    df['pass_outcome'] = df['pass_outcome'].fillna('Complete')
    df['start_x'], df['start_y'] = df['location'].str[0], df['location'].str[1]
    df['end_x'], df['end_y'] = df['pass_end_location'].str[0], df['pass_end_location'].str[1]
    df['progression'] = df['end_x'] - df['start_x']
    df['under_pressure'] = df['under_pressure'].fillna(False)
    return df

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/e/e3/2022_FIFA_World_Cup.svg", use_container_width=True)
    st.title("Strategós Scout")
    st.write("---")
    all_matches = get_data()
    selected_match = st.selectbox("📅 Choose Fixture", all_matches['label'])
    m_id = all_matches[all_matches['label'] == selected_match]['match_id'].values[0]
    passes = get_events(m_id)
    team = st.selectbox("🛡️ Analyze Team", passes['team'].unique())
    st.divider()
    # Removed Visual Style filter as requested
    tactical_filter = st.radio("🔬 Tactical Focus", ["All Passes", "Under Pressure", "Progressive (>15y)"])

# --- 4. ANALYTICS LOGIC ---
df_filtered = passes[passes['team'] == team].copy()
if tactical_filter == "Under Pressure":
    df_filtered = df_filtered[df_filtered['under_pressure'] == True]
elif tactical_filter == "Progressive (>15y)":
    df_filtered = df_filtered[df_filtered['progression'] > 15]

# --- 5. THE MAIN INTERFACE ---
st.markdown('<div class="mobile-hint">📱 MOBILE USERS: Tap the ">>" arrow in the top-left for filters!</div>', unsafe_allow_html=True)
st.title("⚽ Strategós Tactical Intelligence")

# --- REFINED OPERATIONAL GUIDE ---
with st.container():
    st.info("### 📘 STRATEGÓS OPERATIONAL GUIDE")
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        st.markdown("<p class='guide-header'>1. Tactical Scale & Logic</p>", unsafe_allow_html=True)
        st.write("""
        - **The Field Scale:** Data is mapped on a **120-yard pitch**. 0 is your goal line; 120 is the opponent's.
        - **The Danger Zone:** Defined as the **final 20% of the field** (the last 24 yards). Successful entries here are the highest-value actions in soccer.
        - **Under Pressure:** Filters for moments of defensive duress to measure technical composure.
        """)
        
    with g_col2:
        st.markdown("<p class='guide-header'>2. Visual Legend</p>", unsafe_allow_html=True)
        st.write("""
        - **Heatmap (Left):** Identifies 'Spatial Gravity'—the specific zones where the team maintains possession.
        - **Tactical Lines (Right):** A vector-map of ball flight. 🔵 Cyan: High-Progression | 🟢 Green: Success | 🔴 Red: Turnovers.
        """)

# --- HIGH-CONTRAST METRICS ---
st.write("") 
m1, m2, m3, m4 = st.columns(4)
m1.metric("PASS VOLUME", len(df_filtered))
acc = (len(df_filtered[df_filtered['pass_outcome'] == 'Complete']) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
m2.metric("ACCURACY", f"{acc:.1f}%")
danger_zone_count = len(df_filtered[(df_filtered['pass_outcome'] == 'Complete') & (df_filtered['end_x'] > 100)])
m3.metric("DANGER ZONE", danger_zone_count)
m4.metric("AVG. YARDS", f"{df_filtered['progression'].mean():.1f}y")

st.divider()

# --- 6. SIMULTANEOUS PITCH ANALYSIS ---
st.header("🎯 Dual-Pitch Tactical Analysis")
map_col1, map_col2 = st.columns(2)

with map_col1:
    st.subheader("Spatial Heatmap")
    pitch1 = Pitch(pitch_type='statsbomb', pitch_color='#0e1117', line_color='#3e424b', goal_type='box')
    fig1, ax1 = pitch1.draw(figsize=(8, 6))
    if not df_filtered.empty:
        pitch1.kdeplot(df_filtered['start_x'], df_filtered['start_y'], ax=ax1, fill=True, levels=100, cmap='magma')
    st.pyplot(fig1)
    st.caption("Intensity of play: Lighter areas show where the team initiates play.")

with map_col2:
    st.subheader("Tactical Lines")
    pitch2 = Pitch(pitch_type='statsbomb', pitch_color='#0e1117', line_color='#3e424b', goal_type='box')
    fig2, ax2 = pitch2.draw(figsize=(8, 6))
    
    # Danger Zone visual highlight
    ax2.axvspan(100, 120, color='#00d4ff', alpha=0.1)
    
    for i, row in df_filtered.iterrows():
        color = "#ff4b4b" if row['pass_outcome'] != 'Complete' else ("#00d4ff" if row['progression'] > 15 else "#2ecc71")
        pitch2.lines(row['start_x'], row['start_y'], row['end_x'], row['end_y'], 
                    lw=2, color=color, comet=True, ax=ax2, alpha=0.5)
    st.pyplot(fig2)
    st.caption("Flow of play: Vectors showing individual pass success and threat.")

st.divider()

# --- 7. PLAYER RANKINGS ---
st.header("📈 Player Impact")
leaders = df_filtered.groupby('player')['progression'].sum().sort_values(ascending=False).head(10)
if not leaders.empty:
    st.bar_chart(leaders, color="#00d4ff")
    disp = df_filtered.groupby('player')['progression'].sum().sort_values(ascending=False).reset_index()
    disp.columns = ['Player', 'Vertical Yards Progressed']
    st.dataframe(disp.head(10), use_container_width=True)