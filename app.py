import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

st.set_page_config(page_title="Strategos Soccer Analytics", layout="wide")
st.title("⚽ Strategos Soccer Analytics: Tactical Scout")

@st.cache_data
def get_data():
    matches = sb.matches(competition_id=43, season_id=106)
    matches['label'] = matches['home_team'] + " vs " + matches['away_team']
    return matches

all_matches = get_data()

st.sidebar.header("📅 Match Selection")
selected_match = st.sidebar.selectbox("Choose Match", all_matches['label'])
m_id = all_matches[all_matches['label'] == selected_match]['match_id'].values[0]

@st.cache_data
def get_events(match_id):
    events = sb.events(match_id=match_id)
    df = events[events['type'] == 'Pass'].copy()
    df['pass_outcome'] = df['pass_outcome'].fillna('Complete')
    df['start_x'] = df['location'].str[0]
    df['start_y'] = df['location'].str[1]
    df['end_x'] = df['pass_end_location'].str[0]
    df['end_y'] = df['pass_end_location'].str[1]
    df['progression'] = df['end_x'] - df['start_x']
    # Check if the pass was 'Under Pressure'
    df['under_pressure'] = df['under_pressure'].fillna(False)
    return df

passes = get_events(m_id)

# --- NEW SIDEBAR FILTERS ---
st.sidebar.header("🔬 Tactical Filters")
team = st.sidebar.selectbox("Select Team", passes['team'].unique())
tactical_filter = st.sidebar.radio("Focus Area", ["All Passes", "Under Pressure Only", "Progressive (>15y)"])
view = st.sidebar.radio("Visual Style", ["Pass Lines", "Activity Heatmap"])

# --- DATA FILTERING LOGIC ---
df_filtered = passes[passes['team'] == team]

if tactical_filter == "Under Pressure Only":
    df_filtered = df_filtered[df_filtered['under_pressure'] == True]
elif tactical_filter == "Progressive (>15y)":
    df_filtered = df_filtered[df_filtered['progression'] > 15]

# --- METRICS BAR ---
m1, m2, m3 = st.columns(3)
m1.metric("Passes Analyzed", len(df_filtered))
success_rate = (len(df_filtered[df_filtered['pass_outcome'] == 'Complete']) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
m2.metric("Success Rate", f"{success_rate:.1f}%")
danger_passes = len(df_filtered[df_filtered['end_x'] > 100])
m3.metric("Deep Completions", danger_passes)

st.write("---")

# --- VISUALIZATION ---
col1, col2 = st.columns([1.5, 1])

with col1:
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1a1a', line_color='#7c7c7c')
    fig, ax = pitch.draw(figsize=(10, 7))
    if view == "Pass Lines":
        for i, row in df_filtered.iterrows():
            # Cyan for successful progressive, Red for failed, Green for basic success
            if row['pass_outcome'] != 'Complete':
                color = "red"
            elif row['progression'] > 15:
                color = "cyan"
            else:
                color = "green"
            
            pitch.lines(row['start_x'], row['start_y'], row['end_x'], row['end_y'], 
                        lw=2, color=color, comet=True, ax=ax, alpha=0.6)
    else:
        if not df_filtered.empty:
            pitch.kdeplot(df_filtered['start_x'], df_filtered['start_y'], ax=ax, fill=True, levels=100, cmap='hot')
    
    st.pyplot(fig)

with col2:
    st.write("### Impact Leaders")
    st.write("Ranking players by total yardage gained for the team.")
    st.bar_chart(df_filtered.groupby('player')['progression'].sum().sort_values(ascending=False).head(10))
    
    if tactical_filter == "Under Pressure Only":
        st.info("💡 You are viewing players who maintain composure under defensive pressure.")