import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Strategos Soccer Analytics", layout="wide")

# Custom UI Styling for larger text
st.markdown("""
    <style>
    .stMetric { background-color: #1a1c24; padding: 20px; border-radius: 10px; border: 1px solid #2e313d; }
    .main { background-color: #0e1117; }
    /* Making the Info/Warning text larger */
    .st-ae { font-size: 1.1rem !important; } 
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINES (Cached) ---
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

# --- HIGH-VISIBILITY COMMAND CENTER ---
# We use a header inside the info box to make it "pop"
st.info(f"""
### 🚀 COMMAND CENTER: HOW TO ANALYZE {team.upper()}
1. **FILTER:** Use the sidebar to toggle **Under Pressure** to see which players handle stress best.
2. **MAP:** Switch to **Heatmap Density** to see if the team is attacking primarily through the wings or the center.
3. **SCOUT:** Head to the **Player Rankings** tab to see who leads the team in vertical yardage.
""")

st.warning("""
### 🕵️ TACTICAL VISUAL KEY
* 🔵 **CYAN LINES:** High-impact **Progressive Passes** (Moved ball >15 yards forward).
* 🟢 **GREEN LINES:** Standard successful completions that kept possession.
* 🔴 **RED LINES:** Failed passes, interceptions, or out-of-bounds turnovers.
""")

# KPI Metric Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("Pass Volume", len(df_filtered))
acc = (len(df_filtered[df_filtered['pass_outcome'] == 'Complete']) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
m2.metric("Accuracy", f"{acc:.1f}%")
m3.metric("Danger Zone", len(df_filtered[df_filtered['end_x'] > 100]))
m4.metric("Avg Yards", f"{df_filtered['progression'].mean():.1f}y")

st.divider()

# --- 6. TABS ---
tab_map, tab_rank = st.tabs(["🎯 SPATIAL ANALYSIS", "📈 PLAYER RANKINGS"])

with tab_map:
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0e1117', line_color='#3e424b', goal_type='box')
    fig, ax = pitch.draw(figsize=(12, 8))
    
    if view == "Tactical Lines":
        for i, row in df_filtered.iterrows():
            color = "#ff4b4b" if row['pass_outcome'] != 'Complete' else ("#00d4ff" if row['progression'] > 15 else "#2ecc71")
            pitch.lines(row['start_x'], row['start_y'], row['end_x'], row['end_y'], 
                        lw=2, color=color, comet=True, ax=ax, alpha=0.5)
    else:
        if not df_filtered.empty:
            pitch.kdeplot(df_filtered['start_x'], df_filtered['start_y'], ax=ax, fill=True, levels=100, cmap='magma')
    st.pyplot(fig)

with tab_rank:
    st.subheader("Top Impact Players")
    leaders = df_filtered.groupby('player')['progression'].sum().sort_values(ascending=False).head(10)
    if not leaders.empty:
        st.bar_chart(leaders, color="#00d4ff")
        st.write("### Data Snapshot")
        disp = df_filtered[['player', 'pass_outcome', 'progression']].copy()
        disp.columns = ['Player', 'Outcome', 'Yards']
        st.dataframe(disp.tail(15), use_container_width=True)