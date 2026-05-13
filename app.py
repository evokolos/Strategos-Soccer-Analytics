import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Strategos Soccer Analytics", layout="wide")

# Custom CSS to make the UI feel "Premium"
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 10px; border: 1px solid #2e313d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
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

# --- 3. SIDEBAR (The Control Center) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/e/e3/2022_FIFA_World_Cup.svg", width=100)
    st.title("Strategos Analytics")
    st.write("Professional Scouting Suite")
    st.divider()
    
    all_matches = get_data()
    selected_match = st.selectbox("📅 Match Selection", all_matches['label'])
    m_id = all_matches[all_matches['label'] == selected_match]['match_id'].values[0]
    
    passes = get_events(m_id)
    team = st.selectbox("🛡️ Select Team", passes['team'].unique())
    
    st.divider()
    tactical_filter = st.radio("🔬 Tactical Focus", ["All Passes", "Under Pressure", "Progressive"])
    view = st.radio("🎨 Visual Style", ["Pass Lines", "Activity Heatmap"])

# --- 4. DATA PROCESSING ---
df_filtered = passes[passes['team'] == team]
if tactical_filter == "Under Pressure":
    df_filtered = df_filtered[df_filtered['under_pressure'] == True]
elif tactical_filter == "Progressive":
    df_filtered = df_filtered[df_filtered['progression'] > 15]

# --- 5. THE CLEAN UI LAYOUT ---
st.title(f"📊 {team} vs {all_matches[all_matches['match_id']==m_id]['away_team' if team == all_matches[all_matches['match_id']==m_id]['home_team'].values[0] else 'home_team'].values[0]}")

# Metric Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Volume", len(df_filtered))
success = (len(df_filtered[df_filtered['pass_outcome'] == 'Complete']) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
m2.metric("Completion %", f"{success:.1f}%")
m3.metric("Deep Completions", len(df_filtered[df_filtered['end_x'] > 100]))
m4.metric("Avg Progression", f"{df_filtered['progression'].mean():.1f}y")

st.write("") # Spacing

# Tabs for Organization
tab1, tab2 = st.tabs(["🎯 Spatial Analysis", "📈 Player Rankings"])

with tab1:
    col_a, col_b = st.columns([3, 1])
    with col_a:
        pitch = Pitch(pitch_type='statsbomb', pitch_color='#0e1117', line_color='#3e424b', goal_type='box')
        fig, ax = pitch.draw(figsize=(12, 8))
        
        if view == "Pass Lines":
            for i, row in df_filtered.iterrows():
                color = "cyan" if row['progression'] > 15 and row['pass_outcome'] == 'Complete' else ("#ff4b4b" if row['pass_outcome'] != 'Complete' else "#2ecc71")
                pitch.lines(row['start_x'], row['start_y'], row['end_x'], row['end_y'], 
                            lw=2, color=color, comet=True, ax=ax, alpha=0.5)
        else:
            if not df_filtered.empty:
                pitch.kdeplot(df_filtered['start_x'], df_filtered['start_y'], ax=ax, fill=True, levels=100, cmap='magma')
        st.pyplot(fig)
    
    with col_b:
        st.markdown("### **Legend**")
        st.write("🔵 **Cyan**: High Progression")
        st.write("🟢 **Green**: Basic Completion")
        st.write("🔴 **Red**: Turnover")
        st.divider()
        st.info("Heatmaps show pass origin density—the darker the 'heat', the more influence in that zone.")

with tab_rank:
    st.subheader("Progressive Yardage by Player")
    # Grouping by player to see who moved the ball forward the most
    leaders = df_filtered.groupby('player')['progression'].sum().sort_values(ascending=False).head(10)
    
    if not leaders.empty:
        st.bar_chart(leaders, color="#00d4ff")
        
        st.write("### Data Breakdown")
        # Cleaned up columns for a better user experience
        display_df = df_filtered[['player', 'pass_outcome', 'progression']].copy()
        display_df.columns = ['Player', 'Result', 'Yards Gained']
        st.dataframe(display_df.head(20), use_container_width=True)
    else:
        st.warning("No data available for the current filters.")

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Strategos Soccer Analytics", layout="wide")

# Custom CSS for a "Soft-Dark" user-friendly look
st.markdown("""
    <style>
    .stMetric { border-left: 5px solid #00d4ff; background-color: #1a1c24; padding: 20px; border-radius: 5px; }
    .main { color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE (Cached for speed) ---
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

# --- 3. THE USER-FRIENDLY SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Strategos Scout")
    st.info("Choose a match and team to begin your tactical analysis.")
    
    st.header("Step 1: Context")
    all_matches = get_data()
    selected_match = st.selectbox("Choose Match", all_matches['label'], help="Select a World Cup 2022 fixture.")
    m_id = all_matches[all_matches['label'] == selected_match]['match_id'].values[0]
    
    passes = get_events(m_id)
    team = st.selectbox("Choose Team", passes['team'].unique(), help="The analytics will focus on this team.")
    
    st.divider()
    st.header("Step 2: Analytics Filter")
    tactical_filter = st.radio("Focus Area", ["All Passes", "Under Pressure", "Progressive"], 
                               help="High Progression = Passes moving >15 yards toward goal.")
    
    view = st.segmented_control("Visual Style", ["Lines", "Heatmap"], default="Lines")

# --- 4. DATA PROCESSING ---
df_filtered = passes[passes['team'] == team]
if tactical_filter == "Under Pressure":
    df_filtered = df_filtered[df_filtered['under_pressure'] == True]
elif tactical_filter == "Progressive":
    df_filtered = df_filtered[df_filtered['progression'] > 15]

# --- 5. THE MAIN INTERFACE ---
# User-Friendly Greeting
st.title("📊 Tactical Intelligence Dashboard")
st.markdown(f"**Current Match:** `{selected_match}`")

# Helpful Onboarding for new users
with st.expander("📖 How to read this dashboard"):
    st.write("""
    *   **Pass Lines:** Successful passes are **Green**. High-impact (progressive) passes are **Cyan**. Turnovers are **Red**.
    *   **Activity Heatmap:** Darker areas show where the team 'lives' on the pitch.
    *   **Deep Completions:** Total passes successfully finished in the final 20% of the field.
    """)

# Metrics with context
m1, m2, m3, m4 = st.columns(4)
m1.metric("Pass Volume", len(df_filtered), help="Total number of passes matching your filters.")
success = (len(df_filtered[df_filtered['pass_outcome'] == 'Complete']) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
m2.metric("Accuracy", f"{success:.1f}%")
m3.metric("Danger Zone", len(df_filtered[df_filtered['end_x'] > 100]), help="Passes that reached the final attacking zone.")
m4.metric("Avg Yards", f"{df_filtered['progression'].mean():.1f}y", help="Average forward progression per pass.")

st.divider()

# Layout with a focus on the Pitch
tab_map, tab_rank = st.tabs(["🎯 Spatial View", "📈 Player Impact"])

with tab_map:
    col_main, col_legend = st.columns([4, 1])
    with col_main:
        pitch = Pitch(pitch_type='statsbomb', pitch_color='#0e1117', line_color='#3e424b', goal_type='box')
        fig, ax = pitch.draw(figsize=(12, 8))
        
        if view == "Lines":
            for i, row in df_filtered.iterrows():
                color = "cyan" if row['progression'] > 15 and row['pass_outcome'] == 'Complete' else ("#ff4b4b" if row['pass_outcome'] != 'Complete' else "#2ecc71")
                pitch.lines(row['start_x'], row['start_y'], row['end_x'], row['end_y'], 
                            lw=2, color=color, comet=True, ax=ax, alpha=0.5)
        else:
            if not df_filtered.empty:
                pitch.kdeplot(df_filtered['start_x'], df_filtered['start_y'], ax=ax, fill=True, levels=100, cmap='magma')
        st.pyplot(fig)
    
    with col_legend:
        st.write("#### Legend")
        st.write("🔵 Cyan: Attack")
        st.write("🟢 Green: Success")
        st.write("🔴 Red: Loss")

with tab_rank:
    st.subheader("Progressive Yardage by Player")
    leaders = df_filtered.groupby('player')['progression'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(leaders, color="#00d4ff")
    st.dataframe(df_filtered[['player', 'pass_outcome', 'progression']].tail(10), use_container_width=True)