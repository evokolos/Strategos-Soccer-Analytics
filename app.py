import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

st.set_page_config(page_title="Strategos Soccer Analytics", layout="wide")
st.title("⚽ Strategos Soccer Analytics")

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
    return df

passes = get_events(m_id)
team = st.sidebar.selectbox("Select Team", passes['team'].unique())
view = st.sidebar.radio("Analysis Type", ["Pass Lines", "Activity Heatmap"])

df_filtered = passes[passes['team'] == team]

m1, m2 = st.columns(2)
m1.metric("Total Passes", len(df_filtered))
m2.metric("Success Rate", f"{(len(df_filtered[df_filtered['pass_outcome'] == 'Complete']) / len(df_filtered) * 100):.1f}%")

st.write("---")
col1, col2 = st.columns([1.5, 1])

with col1:
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1a1a', line_color='#7c7c7c')
    fig, ax = pitch.draw(figsize=(10, 7))
    if view == "Pass Lines":
        for i, row in df_filtered.iterrows():
            color = "cyan" if row['progression'] > 15 else "green"
            pitch.lines(row['start_x'], row['start_y'], row['end_x'], row['end_y'], 
                        lw=2, color=color, comet=True, ax=ax, alpha=0.6)
    else:
        pitch.kdeplot(df_filtered['start_x'], df_filtered['start_y'], ax=ax, fill=True, levels=100, cmap='hot')
    st.pyplot(fig)

with col2:
    st.write("### Progressive Leaders")
    st.bar_chart(df_filtered.groupby('player')['progression'].sum().sort_values(ascending=False).head(10))