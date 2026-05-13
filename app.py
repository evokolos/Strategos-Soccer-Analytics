import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Strategos Soccer Analytics", layout="wide")

# Custom UI Styling for instructional prominence
st.markdown("""
    <style>
    .stMetric { background-color: #1a1c24; padding: 20px; border-radius: 10px; border: 1px solid #2e313d; }
    .main { background-color: #0e1117; }
    .instruction-header { color: #00d4ff; font-weight: bold; font-size: 1.2rem; }
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
    st.title("Strategos Scout")
    st.write("---")
    
    all_matches = get_data()
    selected_match = st.selectbox("📅 Choose Fixture", all_matches['label'])
    m_id = all_matches[all_matches['label'] == selected_match]['match_id'].values[0]
    
    passes = get_events(m_id)
    team = st.selectbox("🛡️ Analyze Team", passes['team'].unique())
    
    st.divider()
    tactical_filter = st.radio("🔬 Tactical Focus", ["All Passes", "Under Pressure", "Progressive (>15y)"])
    view = st.radio("🎨 Visual Style", ["Tactical Lines", "Heatmap Density"])

# --- 4. ANALYTICS LOGIC ---
df_filtered = passes[passes['team'] == team].copy()
if tactical_filter == "Under Pressure":
    df_filtered = df_filtered[df_filtered['under_pressure'] == True]
elif tactical_filter == "Progressive (>15y)":
    df_filtered = df_filtered[df_filtered['progression'] > 15]

# --- 5. THE MAIN INTERFACE ---
st.title("⚽ Strategos Tactical Intelligence Suite")

# --- THOROUGH USER INSTRUCTIONS ---
st.info("### 📋 OPERATIONAL GUIDE")
guide_col1, guide_col2, guide_col3 = st.columns(3)

with guide_col1:
    st.markdown("<p class='instruction-header'>1. Filter Selection</p>", unsafe_allow_html=True)
    st.write("""
    Use the **Sidebar** to set your context. 
    - **Under Pressure:** Analyzes passes made while an opponent is actively closing down the player.
    - **Progressive:** Filters for 'Verticality'—passes that moved the ball at least 15 yards toward the goal.
    """)

with guide_col2:
    st.markdown("<p class='instruction-header'>2. Interpreting the Map</p>", unsafe_allow_html=True)
    st.write("""
    - 🔵 **Cyan Lines:** Successful high-progression passes.
    - 🟢 **Green Lines:** Successful standard completions.
    - 🔴 **Red Lines:** Turnovers or failed attempts.
    - **Heatmap:** Concentrated color shows where the team initiates their plays.
    """)

with guide_col3:
    st.markdown("<p class='instruction-header'>3. Glossary of Terms</p>", unsafe_allow_html=True)
    st.write("""
    - **Danger Zone:** Total successful passes ending in the final 20% of the field.
    - **Avg Yards:** The mean distance a pass moved forward (negative value means backward passing).
    """)

# KPI Metric Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("Pass Volume", len(df_filtered))
acc = (len(df_filtered[df_filtered['pass_outcome'] == 'Complete']) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
m2.metric("Accuracy", f"{acc:.1f}%")
m3.metric("Danger Zone", len(df_filtered[df_filtered['end_x'] > 100]))
m4.metric("Avg Yards", f"{df_filtered['progression'].mean():.1f}y")

st.divider()

# --- 6. PROMINENT DUAL-PANE VIEW ---
col_rank, col_map = st.columns([1, 1.5])

with col_rank:
    st.header("📈 Player Rankings")
    leaders = df_filtered.groupby('player')['progression'].sum().sort_values(ascending=False).head(10)
    
    if not leaders.empty:
        st.bar_chart(leaders, color="#00d4ff")
        st.write("#### Scout's Data View")
        disp = df_filtered[['player', 'pass_outcome', 'progression']].copy()
        disp.columns = ['Player', 'Outcome', 'Yards']
        st.dataframe(disp.groupby('Player')['Yards'].sum().sort_values(ascending=False), use_container_width=True)
    else:
        st.warning("No data found for this specific filter.")

with col_map:
    st.header("🎯 Spatial Analysis")
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0e1117', line_color='#3e424b', goal_type='box')
    fig, ax = pitch.draw(figsize=(10, 7))
    
    if view == "Tactical Lines":
        for i, row in df_filtered.iterrows():
            color = "#ff4b4b" if row['pass_outcome'] != 'Complete' else ("#00d4ff" if row['progression'] > 15 else "#2ecc71")
            pitch.lines(row['start_x'], row['start_y'], row['end_x'], row['end_y'], 
                        lw=2, color=color, comet=True, ax=ax, alpha=0.5)
    else:
        if not df_filtered.empty:
            pitch.kdeplot(df_filtered['start_x'], df_filtered['start_y'], ax=ax, fill=True, levels=100, cmap='magma')
    st.pyplot(fig)