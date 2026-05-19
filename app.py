import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Strategós Soccer Analytics", layout="wide")

# CUSTOM CSS: High Contrast & Professional Typography
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
    .concept-box { background-color: #1a1c24; padding: 15px; border-radius: 10px; border-left: 5px solid #00d4ff; margin-bottom: 10px; }
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

# --- DETAILED CONCEPT GUIDE ---
with st.container():
    st.info("### 📘 STRATEGÓS OPERATIONAL GUIDE & CONCEPTS")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("<div class='concept-box'><strong>📍 What is High-Progression?</strong><br>This identifies 'Spatial Gravity'. It measures if the team is actually dangerous or just passing in circles. Lighter heatmap zones in the final third indicate successful penetration into scoring areas.</div>", unsafe_allow_html=True)
        st.markdown("<div class='concept-box'><strong>📐 The Danger Zone Scale</strong><br>Measured on a 120-yard pitch. The Danger Zone is the final 24 yards (x > 100). Successful entries here are the highest-value actions in football.</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='concept-box'><strong>📈 What are Vertical Yards?</strong><br>This measures 'Directness'. It only counts distance gained toward the opponent's goal. A 40-yard sideways pass counts as 0 yards, while a 15-yard forward pass counts as 15.</div>", unsafe_allow_html=True)
        st.markdown("<div class='concept-box'><strong>🛡️ Under Pressure Filter</strong><br>Isolates moments where defenders are actively closing down the player. Use this to scout technical composure and decision-making speed.</div>", unsafe_allow_html=True)

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

with map_col2:
    st.subheader("Tactical Lines")
    pitch2 = Pitch(pitch_type='statsbomb', pitch_color='#0e1117', line_color='#3e424b', goal_type='box')
    fig2, ax2 = pitch2.draw(figsize=(8, 6))
    ax2.axvspan(100, 120, color='#00d4ff', alpha=0.1)
    
    for i, row in df_filtered.iterrows():
        color = "#ff4b4b" if row['pass_outcome'] != 'Complete' else ("#00d4ff" if row['progression'] > 15 else "#2ecc71")
        pitch2.lines(row['start_x'], row['start_y'], row['end_x'], row['end_y'], 
                    lw=2, color=color, comet=True, ax=ax2, alpha=0.5)
    st.pyplot(fig2)

st.divider()

# --- 7. THE ELITE 11 PLAYER RANKINGS ---
st.header("📈 The Elite 11: Impact Rankings")
st.write("Top 11 players ranked by total vertical yards progressed toward the goal.")

# Force exactly 11 players
leaders = df_filtered.groupby('player')['progression'].sum().sort_values(ascending=False).head(11)

if not leaders.empty:
    st.bar_chart(leaders, color="#00d4ff")
    
    # Detailed Table for the Elite 11
    disp = df_filtered.groupby('player')['progression'].sum().sort_values(ascending=False).reset_index()
    disp.columns = ['Scouted Player', 'Total Vertical Yards']
    st.table(disp.head(11)) # Using st.table for a more 'static/professional' look
else:
    st.warning("No performance data available for this filter.")
    import streamlit as st
import plotly.graph_objects as go

# 1. Define your tactical color palette
TACTICAL_COLORS = {
    "Defensive Line": "#EF553B",    # Crimson Red
    "Midfield Block": "#FECB52",    # Amber Yellow
    "Attacking Line": "#00CC96",    # Emerald Green
    "Passing Lane/Link": "#636EFA"  # Electric Blue
}

st.title("Strategós Analytics — Tactical Line Filter")

# 2. Sidebar Filters
st.sidebar.header("Tactical Visualization Filters")

# Allow user to toggle specific lines on/off
selected_lines = st.sidebar.multiselect(
    "Select Tactical Lines to Display:",
    options=list(TACTICAL_COLORS.keys()),
    default=list(TACTICAL_COLORS.keys())
)

# 3. Base Pitch Setup (Simplified for example)
fig = go.Figure()

# Pitch boundaries (StatsBomb coords: 120 x 80)
fig.update_layout(
    xaxis=dict(range=[0, 120], showgrid=False, zeroline=False),
    yaxis=dict(range=[0, 80], showgrid=False, zeroline=False),
    width=800,
    height=533,
    plot_bgcolor="#1e1e1e", # Dark mode pitch background
    paper_bgcolor="#1e1e1e"
)

# 4. Mock Tracking Data for Tactical Lines
# In production, this would be computed from your StatsBomb event/tracking data
line_data = [
    {"type": "Defensive Line", "x": [30, 32, 35, 30], "y": [15, 35, 55, 70]},
    {"type": "Midfield Block", "x": [55, 58, 60, 56], "y": [10, 32, 50, 72]},
    {"type": "Attacking Line", "x": [85, 90, 88],     "y": [20, 40, 60]},
    {"type": "Passing Lane/Link", "x": [32, 58],       "y": [35, 32]}
]

# 5. Render Filtered Lines
for line in line_data:
    if line["type"] in selected_lines:
        fig.add_trace(go.Scatter(
            x=line["x"],
            y=line["y"],
            mode="lines+markers",
            name=line["type"],
            line=dict(
                color=TACTICAL_COLORS[line["type"]], 
                width=3, 
                dash="dash" if "Link" in line["type"] else "solid"
            ),
            marker=dict(size=6, color="#ffffff"),
            hoverinfo="name"
        ))

st.plotly_chart(fig, use_container_width=True)