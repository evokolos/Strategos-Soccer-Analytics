import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# --- UI SETUP ---
st.set_page_config(page_title="Strategos Scout", layout="wide")
st.title("⚽ Strategos Scout: World Cup 2022 Analytics")

# --- DATA INGESTION ---
@st.cache_data
def get_data():
    matches = sb.matches(competition_id=43, season_id=106)
    matches['label'] = matches['home_team'] + " vs " + matches['away_team']
    return matches

all_matches = get_data()

# --- SIDEBAR ---
st.sidebar.header("📅 Selection")
selected_match = st.sidebar.selectbox("Match", all_matches['label'])
m_id = all_matches[all_matches['label'] == selected_match]['match_id'].values[0]

@st.cache_data
def get_events(match_id):
    events = sb.events(match_id=match_id)
    passes = events[events['type'] == 'Pass'].copy()
    passes['pass_outcome'] = passes['pass_outcome'].fillna('Complete')
    passes['start_x'] = passes['location'].str[0]
    passes['start_y'] = passes['location'].str[1]
    passes['end_x'] = passes['pass_end_location'].str[0]
    passes['end_y'] = passes['pass_end_location'].str[1]
    passes['progression'] = passes['end_x'] - passes['start_x']
    return passes

passes = get_events(m_id)
team = st.sidebar.selectbox("Team", passes['team'].unique())
view = st.sidebar.radio("View", ["Pass Lines", "Heatmap"])

# --- FILTERING ---
df = passes[passes['team'] == team]

# --- DASHBOARD ---
st.metric("Total Passes", len(df))

col1, col2 = st.columns([1.5, 1])

with col1:
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1a1a', line_color='#7c7c7c')
    fig, ax = pitch.draw(figsize=(10, 7))
    if view == "Pass Lines":
        for i, row in df.iterrows():
            color = "cyan" if row['progression'] > 15 else "green"
            pitch.lines(row['start_x'], row['start_y'], row['end_x'], row['end_y'], 
                        lw=2, color=color, comet=True, ax=ax, alpha=0.6)
    else:
        pitch.kdeplot(df['start_x'], df['start_y'], ax=ax, fill=True, levels=100, cmap='hot')
    st.pyplot(fig)

with col2:
    st.write("### Progressive Leaders")
    st.bar_chart(df.groupby('player')['progression'].sum().sort_values(ascending=False).head(10))