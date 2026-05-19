import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. DATABASE COMPONENT LAYER
# -----------------------------------------------------------------------------
WORLD_CUP_DATA = {
    "groups": {
        "Group A": [
            {"rank": 1, "team": "Netherlands", "played": 3, "won": 2, "drawn": 1, "lost": 0, "gf": 5, "ga": 1, "gd": 4, "pts": 7},
            {"rank": 2, "team": "Senegal", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 5, "ga": 4, "gd": 1, "pts": 6},
            {"rank": 3, "team": "Ecuador", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 4, "ga": 3, "gd": 1, "pts": 4},
            {"rank": 4, "team": "Qatar (H)", "played": 3, "won": 0, "drawn": 0, "lost": 3, "gf": 1, "ga": 7, "gd": -6, "pts": 0}
        ],
        "Group B": [
            {"rank": 1, "team": "England", "played": 3, "won": 2, "drawn": 1, "lost": 0, "gf": 9, "ga": 2, "gd": 7, "pts": 7},
            {"rank": 2, "team": "United States", "played": 3, "won": 1, "drawn": 2, "lost": 0, "gf": 2, "ga": 1, "gd": 1, "pts": 5},
            {"rank": 3, "team": "Iran", "played": 3, "won": 1, "drawn": 0, "lost": 2, "gf": 4, "ga": 7, "gd": -3, "pts": 3},
            {"rank": 4, "team": "Wales", "played": 3, "won": 0, "drawn": 1, "lost": 2, "gf": 1, "ga": 6, "gd": -5, "pts": 1}
        ],
        "Group C": [
            {"rank": 1, "team": "Argentina", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 5, "ga": 2, "gd": 3, "pts": 6},
            {"rank": 2, "team": "Poland", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 2, "ga": 2, "gd": 0, "pts": 4},
            {"rank": 3, "team": "Mexico", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 2, "ga": 3, "gd": -1, "pts": 4},
            {"rank": 4, "team": "Saudi Arabia", "played": 3, "won": 1, "drawn": 0, "lost": 2, "gf": 3, "ga": 5, "gd": -2, "pts": 3}
        ],
        "Group D": [
            {"rank": 1, "team": "France", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 6, "ga": 3, "gd": 3, "pts": 6},
            {"rank": 2, "team": "Australia", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 3, "ga": 4, "gd": -1, "pts": 6},
            {"rank": 3, "team": "Tunisia", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 1, "ga": 1, "gd": 0, "pts": 4},
            {"rank": 4, "team": "Denmark", "played": 3, "won": 0, "drawn": 1, "lost": 2, "gf": 1, "ga": 3, "gd": -2, "pts": 1}
        ],
        "Group E": [
            {"rank": 1, "team": "Japan", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 4, "ga": 3, "gd": 1, "pts": 6},
            {"rank": 2, "team": "Spain", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 9, "ga": 3, "gd": 6, "pts": 4},
            {"rank": 3, "team": "Germany", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 6, "ga": 5, "gd": 1, "pts": 4},
            {"rank": 4, "team": "Costa Rica", "played": 3, "won": 1, "drawn": 0, "lost": 2, "gf": 3, "ga": 11, "gd": -8, "pts": 3}
        ],
        "Group F": [
            {"rank": 1, "team": "Morocco", "played": 3, "won": 2, "drawn": 1, "lost": 0, "gf": 4, "ga": 1, "gd": 3, "pts": 7},
            {"rank": 2, "team": "Croatia", "played": 3, "won": 1, "drawn": 2, "lost": 0, "gf": 4, "ga": 1, "gd": 3, "pts": 5},
            {"rank": 3, "team": "Belgium", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 1, "ga": 2, "gd": -1, "pts": 4},
            {"rank": 4, "team": "Canada", "played": 3, "won": 0, "drawn": 0, "lost": 3, "gf": 2, "ga": 7, "gd": -5, "pts": 0}
        ],
        "Group G": [
            {"rank": 1, "team": "Brazil", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 3, "ga": 1, "gd": 2, "pts": 6},
            {"rank": 2, "team": "Switzerland", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 4, "ga": 3, "gd": 1, "pts": 6},
            {"rank": 3, "team": "Cameroon", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 4, "ga": 4, "gd": 0, "pts": 4},
            {"rank": 4, "team": "Serbia", "played": 3, "won": 0, "drawn": 1, "lost": 2, "gf": 5, "ga": 8, "gd": -3, "pts": 1}
        ],
        "Group H": [
            {"rank": 1, "team": "Portugal", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 6, "ga": 4, "gd": 2, "pts": 6},
            {"rank": 2, "team": "South Korea", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 4, "ga": 4, "gd": 0, "pts": 4},
            {"rank": 3, "team": "Uruguay", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 2, "ga": 2, "gd": 0, "pts": 4},
            {"rank": 4, "team": "Ghana", "played": 3, "won": 1, "drawn": 0, "lost": 2, "gf": 5, "ga": 7, "gd": -2, "pts": 3}
        ]
    },
    "bracket": {
        "r16": [
            {"match": "R16 1", "team1": "Netherlands", "score1": 3, "team2": "USA", "score2": 1, "winner": "Netherlands"},
            {"match": "R16 2", "team1": "Argentina", "score1": 2, "team2": "Australia", "score2": 1, "winner": "Argentina"},
            {"match": "R16 3", "team1": "Japan", "score1": 1, "team2": "Croatia (p)", "score2": 1, "winner": "Croatia"},
            {"match": "R16 4", "team1": "Brazil", "score1": 4, "team2": "South Korea", "score2": 1, "winner": "Brazil"},
            {"match": "R16 5", "team1": "England", "score1": 3, "team2": "Senegal", "score2": 0, "winner": "England"},
            {"match": "R16 6", "team1": "France", "score1": 3, "team2": "Poland", "score2": 1, "winner": "France"},
            {"match": "R16 7", "team1": "Morocco (p)", "score1": 0, "team2": "Spain", "score2": 0, "winner": "Morocco"},
            {"match": "R16 8", "team1": "Portugal", "score1": 6, "team2": "Switzerland", "score2": 1, "winner": "Portugal"}
        ],
        "qf": [
            {"match": "QF 1", "team1": "Netherlands", "score1": 2, "team2": "Argentina (p)", "score2": 2, "winner": "Argentina"},
            {"match": "QF 2", "team1": "Croatia (p)", "score1": 1, "team2": "Brazil", "score2": 1, "winner": "Croatia"},
            {"match": "QF 3", "team1": "England", "score1": 1, "team2": "France", "score2": 2, "winner": "France"},
            {"match": "QF 4", "team1": "Morocco", "score1": 1, "team2": "Portugal", "score2": 0, "winner": "Morocco"}
        ],
        "sf": [
            {"match": "SF 1", "team1": "Argentina", "score1": 3, "team2": "Croatia", "score2": 0, "winner": "Argentina"},
            {"match": "SF 2", "team1": "France", "score1": 2, "team2": "Morocco", "score2": 0, "winner": "France"}
        ],
        "third": [
            {"match": "Third Place", "team1": "Croatia", "score1": 2, "team2": "Morocco", "score2": 1, "winner": "Croatia"}
        ],
        "final": [
            {"match": "Final", "team1": "Argentina (p)", "score1": 3, "team2": "France", "score2": 3, "winner": "Argentina"}
        ]
    },
    "players": [
        {"id": "messi", "name": "Lionel Messi", "team": "Argentina", "role": "Forward / Playmaker", "stats": {"Pace": 83, "Shooting": 94, "Passing": 96, "Dribbling": 95, "Defending": 35, "Physical": 69}, "world_cup_stats": {"Goals": 7, "Assists": 3, "Key Passes": 18, "Shots on Target": 15, "Dribbles Comp": 15, "Distance (km)": 62.1}},
        {"id": "mbappe", "name": "Kylian Mbappé", "team": "France", "role": "Forward", "stats": {"Pace": 97, "Shooting": 92, "Passing": 80, "Dribbling": 92, "Defending": 36, "Physical": 77}, "world_cup_stats": {"Goals": 8, "Assists": 2, "Key Passes": 11, "Shots on Target": 16, "Dribbles Comp": 25, "Distance (km)": 58.4}},
        {"id": "griezmann", "name": "Antoine Griezmann", "team": "France", "role": "Midfielder / Central AM", "stats": {"Pace": 78, "Shooting": 83, "Passing": 91, "Dribbling": 85, "Defending": 68, "Physical": 74}, "world_cup_stats": {"Goals": 0, "Assists": 3, "Key Passes": 22, "Shots on Target": 4, "Dribbles Comp": 6, "Distance (km)": 66.8}},
        {"id": "modric", "name": "Luka Modrić", "team": "Croatia", "role": "Central Midfielder", "stats": {"Pace": 72, "Shooting": 78, "Passing": 92, "Dribbling": 88, "Defending": 74, "Physical": 72}, "world_cup_stats": {"Goals": 0, "Assists": 0, "Key Passes": 10, "Shots on Target": 3, "Dribbles Comp": 8, "Distance (km)": 72.4}},
        {"id": "fernandes", "name": "Bruno Fernandes", "team": "Portugal", "role": "Attacking Midfielder", "stats": {"Pace": 79, "Shooting": 86, "Passing": 90, "Dribbling": 83, "Defending": 64, "Physical": 77}, "world_cup_stats": {"Goals": 2, "Assists": 3, "Key Passes": 12, "Shots on Target": 5, "Dribbles Comp": 6, "Distance (km)": 44.2}},
        {"id": "hakimi", "name": "Achraf Hakimi", "team": "Morocco", "role": "Right Wingback", "stats": {"Pace": 92, "Shooting": 68, "Passing": 81, "Dribbling": 80, "Defending": 85, "Physical": 82}, "world_cup_stats": {"Goals": 0, "Assists": 1, "Key Passes": 7, "Shots on Target": 2, "Dribbles Comp": 11, "Distance (km)": 70.2}}
    ],
    "final_match": {
        "details": {
            "match": "2022 World Cup Final",
            "stadium": "Lusail Stadium, Qatar",
            "attendance": "88,966",
            "referee": "Szymon Marciniak (Poland)",
            "score": "Argentina 3-3 France (Penalties: 4-2)",
            "home": "Argentina",
            "away": "France"
        },
        "stats": {
            "Possession (%)": [54, 46],
            "Expected Goals (xG)": [3.28, 2.15],
            "Total Shots": [20, 10],
            "Shots on Target": [10, 5],
            "Passes Completed": [542, 421],
            "Pass Accuracy (%)": [85, 80],
            "Corners": [6, 5],
            "Fouls Committed": [26, 19],
            "Yellow Cards": [5, 3]
        },
        "events": [
            {"time": "23'", "team": "Argentina", "type": "goal", "player": "Lionel Messi", "desc": "Goal! Converted penalty after Dembélé fouled Di María.", "icon": "⚽"},
            {"time": "36'", "team": "Argentina", "type": "goal", "player": "Ángel Di María", "desc": "Goal! World-class counter-attack. Tapped home from Mac Allister's low cross.", "icon": "⚽"},
            {"time": "41'", "team": "France", "type": "sub", "player": "Thuram / Kolo Muani", "desc": "Tactical subs: Giroud & Dembélé replaced early.", "icon": "🔄"},
            {"time": "80'", "team": "France", "type": "goal", "player": "Kylian Mbappé", "desc": "Goal! Penalty kick drilled low after Otamendi fouled Kolo Muani.", "icon": "⚽"},
            {"time": "81'", "team": "France", "type": "goal", "player": "Kylian Mbappé", "desc": "Goal! Sensational volleyed finish from Rabiot's lofted pass. 2-2!", "icon": "⚽"},
            {"time": "108'", "team": "Argentina", "type": "goal", "player": "Lionel Messi", "desc": "Goal! Bundled home from close range after Lloris saved Lautaro's shot.", "icon": "⚽"},
            {"time": "118'", "team": "France", "type": "goal", "player": "Kylian Mbappé", "desc": "Goal! Penalty kick converted after Montiel handled in the box. Hat-trick!", "icon": "⚽"},
            {"time": "120+3'", "team": "France", "type": "shot", "player": "Randal Kolo Muani", "desc": "Incredible reflex save by Emi Martínez to deny France the trophy.", "icon": "🧤"}
        ],
        "coordinates": {
            "shots": [
                {"x": 88.5, "y": 50.0, "team": "Argentina", "player": "Lionel Messi", "outcome": "goal", "xG": 0.78, "desc": "Penalty Goal (23')"},
                {"x": 93.0, "y": 38.0, "team": "Argentina", "player": "Ángel Di María", "outcome": "goal", "xG": 0.62, "desc": "Di María Close Range (36')"},
                {"x": 92.0, "y": 50.0, "team": "Argentina", "player": "Lionel Messi", "outcome": "goal", "xG": 0.70, "desc": "Goal Rebound (108')"},
                {"x": 86.0, "y": 48.0, "team": "Argentina", "player": "Alexis Mac Allister", "outcome": "saved", "xG": 0.12, "desc": "Mac Allister shot saved"},
                {"x": 78.0, "y": 62.0, "team": "Argentina", "player": "Rodrigo De Paul", "outcome": "saved", "xG": 0.06, "desc": "De Paul volley saved"},
                {"x": 89.0, "y": 44.0, "team": "Argentina", "player": "Julián Álvarez", "outcome": "saved", "xG": 0.28, "desc": "Álvarez tight angle saved"},
                {"x": 85.0, "y": 54.0, "team": "Argentina", "player": "Lionel Messi", "outcome": "saved", "xG": 0.09, "desc": "Messi long range strike"},
                {"x": 74.0, "y": 38.0, "team": "Argentina", "player": "Enzo Fernández", "outcome": "missed", "xG": 0.04, "desc": "Fernández shot wide"},
                {"x": 11.5, "y": 50.0, "team": "France", "player": "Kylian Mbappé", "outcome": "goal", "xG": 0.78, "desc": "Penalty Goal (80')"},
                {"x": 14.0, "y": 68.0, "team": "France", "player": "Kylian Mbappé", "outcome": "goal", "xG": 0.15, "desc": "Volley Goal (81')"},
                {"x": 11.5, "y": 50.0, "team": "France", "player": "Kylian Mbappé", "outcome": "goal", "xG": 0.78, "desc": "Penalty Goal (118')"},
                {"x": 10.0, "y": 52.0, "team": "France", "player": "Randal Kolo Muani", "outcome": "saved", "xG": 0.65, "desc": "Muani 1v1 saved by Martinez"},
                {"x": 15.0, "y": 42.0, "team": "France", "player": "Kylian Mbappé", "outcome": "saved", "xG": 0.10, "desc": "Mbappé curler saved"},
                {"x": 22.0, "y": 35.0, "team": "France", "player": "Adrien Rabiot", "outcome": "saved", "xG": 0.08, "desc": "Rabiot snapshot saved"},
                {"x": 18.0, "y": 62.0, "team": "France", "player": "Marcus Thuram", "outcome": "missed", "xG": 0.05, "desc": "Thuram header wide"}
            ],
            "passes": [
                {"fromX": 54.0, "fromY": 50.0, "toX": 78.0, "toY": 25.0, "team": "Argentina", "playerFrom": "Enzo Fernández", "playerTo": "Alexis Mac Allister", "type": "progressive"},
                {"fromX": 78.0, "fromY": 25.0, "toX": 93.0, "toY": 38.0, "team": "Argentina", "playerFrom": "Alexis Mac Allister", "playerTo": "Ángel Di María", "type": "key"},
                {"fromX": 60.0, "fromY": 65.0, "toX": 82.0, "toY": 55.0, "team": "Argentina", "playerFrom": "Rodrigo De Paul", "playerTo": "Lionel Messi", "type": "progressive"},
                {"fromX": 82.0, "fromY": 55.0, "toX": 91.0, "toY": 65.0, "team": "Argentina", "playerFrom": "Lionel Messi", "playerTo": "Julián Álvarez", "type": "key"},
                {"fromX": 45.0, "fromY": 50.0, "toX": 25.0, "toY": 78.0, "team": "France", "playerFrom": "Adrien Rabiot", "playerTo": "Kylian Mbappé", "type": "key"},
                {"fromX": 35.0, "fromY": 30.0, "toX": 15.0, "toY": 58.0, "team": "France", "playerFrom": "Kingsley Coman", "playerTo": "Kolo Muani", "type": "progressive"},
                {"fromX": 40.0, "fromY": 60.0, "toX": 18.0, "toY": 74.0, "team": "France", "playerFrom": "Marcus Thuram", "playerTo": "Kylian Mbappé", "type": "progressive"}
            ],
            "heatmap": [
                {"x": 52.0, "y": 48.0, "value": 0.8}, {"x": 58.0, "y": 55.0, "value": 0.95}, {"x": 62.0, "y": 50.0, "value": 0.9},
                {"x": 66.0, "y": 38.0, "value": 0.85}, {"x": 74.0, "y": 32.0, "value": 0.9}, {"x": 80.0, "y": 25.0, "value": 0.95},
                {"x": 78.0, "y": 50.0, "value": 0.8}, {"x": 84.0, "y": 48.0, "value": 0.85}, {"x": 88.0, "y": 52.0, "value": 0.9},
                {"x": 65.0, "y": 70.0, "value": 0.65}, {"x": 72.0, "y": 78.0, "value": 0.72}, {"x": 80.0, "y": 80.0, "value": 0.6},
                {"x": 40.0, "y": 50.0, "value": 0.5}, {"x": 35.0, "y": 45.0, "value": 0.45},
                {"x": 48.0, "y": 50.0, "value": 0.75}, {"x": 42.0, "y": 68.0, "value": 0.85}, {"x": 32.0, "y": 75.0, "value": 0.95},
                {"x": 22.0, "y": 80.0, "value": 0.98}, {"x": 14.0, "y": 82.0, "value": 0.9}, {"x": 15.0, "y": 65.0, "value": 0.85},
                {"x": 25.0, "y": 50.0, "value": 0.7}, {"x": 30.0, "y": 25.0, "value": 0.6}, {"x": 18.0, "y": 22.0, "value": 0.75},
                {"x": 12.0, "y": 38.0, "value": 0.68}, {"x": 8.0, "y": 50.0, "value": 0.8}
            ]
        }
    },
    "simulation_teams": {
        "Argentina": {"attack": 92, "midfield": 90, "defense": 89, "star_player": "Lionel Messi"},
        "France": {"attack": 91, "midfield": 88, "defense": 90, "star_player": "Kylian Mbappé"},
        "Croatia": {"attack": 82, "midfield": 92, "defense": 85, "star_player": "Luka Modrić"},
        "Morocco": {"attack": 80, "midfield": 84, "defense": 88, "star_player": "Achraf Hakimi"},
        "Brazil": {"attack": 93, "midfield": 87, "defense": 89, "star_player": "Neymar Jr"},
        "England": {"attack": 89, "midfield": 88, "defense": 86, "star_player": "Harry Kane"},
        "Portugal": {"attack": 88, "midfield": 89, "defense": 85, "star_player": "Bruno Fernandes"},
        "Netherlands": {"attack": 85, "midfield": 86, "defense": 89, "star_player": "Virgil van Dijk"}
    }
}

# -----------------------------------------------------------------------------
# 2. RUNTIME GRAPHICS CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Strategós World Cup Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #0f172a; color: #f8fafc;}
    div[data-testid="stMetricValue"] {font-size: 2rem; font-weight: 700; color: #38bdf8;}
    div.stButton > button:first-child {
        background-color: #0284c7; color: white; border-radius: 6px; border: none; width: 100%; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Strategós Python Analytics Dashboard")
st.subheader("2022 FIFA World Cup Comprehensive Analysis Suite")
st.write("---")

navigation_view = st.sidebar.radio(
    "Select Dashboard Suite",
    ["Standings & Tournament Path", "Final Match Tactical Pitch", "Player Comparison Radar", "Predictive Match Simulator"]
)

# -----------------------------------------------------------------------------
# INTERFACE SUITE 1: STANDINGS
# -----------------------------------------------------------------------------
if navigation_view == "Standings & Tournament Path":
    st.header("🏆 Group Stage Standings & Knockout Matrix")
    selected_group = st.selectbox("Filter Group Table", list(WORLD_CUP_DATA["groups"].keys()))
    group_df = pd.DataFrame(WORLD_CUP_DATA["groups"][selected_group]).set_index("rank")
    
    st.dataframe(group_df.style.background_gradient(subset=["pts", "gd"], cmap="Blues"), use_container_width=True)
    
    st.write("### 🪜 Knockout Stage Progression Tree")
    bracket_level = st.selectbox("Select Tournament Round", ["Round of 16 (r16)", "Quarter-Finals (qf)", "Semi-Finals (sf)", "Final (final)"])
    bracket_key = bracket_level.split("(")[-1].replace(")", "").strip()
    st.table(pd.DataFrame(WORLD_CUP_DATA["bracket"][bracket_key])[["match", "team1", "score1", "team2", "score2", "winner"]])

# -----------------------------------------------------------------------------
# INTERFACE SUITE 2: SPATIAL PITCH OVERLAYS
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# INTERFACE SUITE 2: SPATIAL PITCH OVERLAYS (WITH ADVANCED FILTERS)
# -----------------------------------------------------------------------------
elif navigation_view == "Final Match Tactical Pitch":
    st.header("🎯 Final Match Spatial Event Mapping")
    details = WORLD_CUP_DATA["final_match"]["details"]
    coords = WORLD_CUP_DATA["final_match"]["coordinates"]
    
    # Meta Information Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Score", details["score"])
    with col2: st.metric("Venue", details["stadium"])
    with col3: st.metric("Attendance", details["attendance"])
    with col4: st.metric("Official", details["referee"].split("(")[0])

    st.write("---")
    
    # --- SIDEBAR FILTERS CRADLE ---
    st.sidebar.markdown("### 🛠️ Tactical Canvas Filters")
    
    # Filter 1: Team Selection
    team_filter = st.sidebar.multiselect(
        "Filter by Team", 
        options=["Argentina", "France"], 
        default=["Argentina", "France"]
    )
    
    # Filter 2: Event Type Toggles
    st.sidebar.markdown("**Display Layers**")
    show_shots = st.sidebar.checkbox("Show Shot Overlay Maps", value=True)
    show_passes = st.sidebar.checkbox("Show Passing Vectors", value=True)
    
    # Filter 3: Sub-category metrics (Conditional options)
    shot_outcome_filter = []
    pass_type_filter = []
    
    if show_shots:
        shot_outcome_filter = st.sidebar.multiselect(
            "Shot Outcomes", 
            options=["goal", "saved", "missed"], 
            default=["goal", "saved", "missed"]
        )
        
    if show_passes:
        pass_type_filter = st.sidebar.multiselect(
            "Pass Dynamics", 
            options=["key", "progressive"], 
            default=["key", "progressive"]
        )

    # --- CANVAS GENERATION LOGIC ---
    def generate_pitch_base():
        fig = go.Figure()
        # Draw Field Outer Boundaries
        fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, line=dict(color="rgba(255,255,255,0.3)", width=2), fillcolor="rgba(16, 185, 129, 0.08)")
        # Halfway Line
        fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, line=dict(color="rgba(255,255,255,0.3)", width=2))
        # Center Circle
        fig.add_shape(type="circle", x0=40, y0=35, x1=60, y1=65, line=dict(color="rgba(255,255,255,0.3)", width=2))
        # Left Penalty Box (France attacking side / Argentina defense zone)
        fig.add_shape(type="rect", x0=0, y0=20, x1=16.5, y1=80, line=dict(color="rgba(255,255,255,0.3)", width=2))
        # Right Penalty Box (Argentina attacking side / France defense zone)
        fig.add_shape(type="rect", x0=83.5, y0=20, x1=100, y1=80, line=dict(color="rgba(255,255,255,0.3)", width=2))
        return fig

    fig_pitch = generate_pitch_base()

    # --- PLOT SHOTS IF ACTIVATED ---
    if show_shots and shot_outcome_filter:
        shot_df = pd.DataFrame(coords["shots"])
        # Apply filters based on UI state inputs
        filtered_shots = shot_df[
            (shot_df["team"].isin(team_filter)) & 
            (shot_df["outcome"].isin(shot_outcome_filter))
        ]
        
        if not filtered_shots.empty:
            filtered_shots["marker_size"] = filtered_shots["xG"] * 45 + 10
            color_map = {"goal": "#10b981", "saved": "#3b82f6", "missed": "#ef4444"}
            
            for outcome, group in filtered_shots.groupby("outcome"):
                fig_pitch.add_trace(go.Scatter(
                    x=group["x"], y=group["y"], mode="markers",
                    marker=dict(size=group["marker_size"], color=color_map[outcome], line=dict(width=1, color="white")),
                    name=f"SHOT: {outcome.upper()}",
                    text=group["player"] + "<br>" + group["desc"] + "<br>xG: " + group["xG"].astype(str),
                    hoverinfo="text"
                ))

    # --- PLOT PASS LINES IF ACTIVATED ---
    if show_passes and pass_type_filter:
        pass_df = pd.DataFrame(coords["passes"])
        filtered_passes = pass_df[
            (pass_df["team"].isin(team_filter)) & 
            (pass_df["type"].isin(pass_type_filter))
        ]
        
        colors = {"Argentina": "#38bdf8", "France": "#f43f5e"}
        
        for idx, row in filtered_passes.iterrows():
            # Adjust styling details depending on key vs progressive markers
            is_key = row["type"] == "key"
            fig_pitch.add_trace(go.Scatter(
                x=[row["fromX"], row["toX"]], y=[row["fromY"], row["toY"]],
                mode="lines+markers",
                line=dict(
                    color=colors[row["team"]], 
                    width=4 if is_key else 2, 
                    dash="solid" if is_key else "dash"
                ),
                marker=dict(size=[4, 8], color=colors[row["team"]]),
                name=f"{row['team']} {row['type'].upper()} Pass",
                text=f"{row['playerFrom']} -> {row['playerTo']}<br>Type: {row['type']}",
                hoverinfo="text",
                showlegend=True if idx == filtered_passes.index[0] or row['type'] == 'key' else False 
            ))

    # Clean layout properties
    fig_pitch.update_xaxes(visible=False, range=[-2, 102])
    fig_pitch.update_yaxes(visible=False, range=[-2, 102])
    fig_pitch.update_layout(
        template="plotly_dark", 
        height=650, 
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(30, 41, 59, 0.7)")
    )
    
    st.plotly_chart(fig_pitch, use_container_width=True)

# -----------------------------------------------------------------------------
# INTERFACE SUITE 3: RADAR ENGINES
# -----------------------------------------------------------------------------
elif navigation_view == "Player Comparison Radar":
    st.header("📊 Profile Attributes Side-by-Side Radar Matrix")
    player_dict = {p["name"]: p for p in WORLD_CUP_DATA["players"]}
    
    c1, c2 = st.columns(2)
    with c1: p1_selection = st.selectbox("Select Player A", list(player_dict.keys()), index=0)
    with c2: p2_selection = st.selectbox("Select Player B", list(player_dict.keys()), index=1)
    
    p1, p2 = player_dict[p1_selection], player_dict[p2_selection]
    categories = list(p1["stats"].keys())
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=list(p1["stats"].values()), theta=categories, fill='toself', name=p1["name"], line=dict(color="#38bdf8")))
    fig_radar.add_trace(go.Scatterpolar(r=list(p2["stats"].values()), theta=categories, fill='toself', name=p2["name"], line=dict(color="#f43f5e")))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100]), bgcolor="#1e293b"), template="plotly_dark", height=500)
    st.plotly_chart(fig_radar, use_container_width=True)
    
    st.dataframe(pd.DataFrame([{"Player": p["name"], "Team": p["team"], **p["world_cup_stats"]} for p in [p1, p2]]).set_index("Player"), use_container_width=True)

# -----------------------------------------------------------------------------
# INTERFACE SUITE 4: POISSON PROJECTIONS
# -----------------------------------------------------------------------------
elif navigation_view == "Predictive Match Simulator":
    st.header("🧮 Weighted Multi-Factor Prediction Simulator")
    teams = WORLD_CUP_DATA["simulation_teams"]
    
    col1, col2 = st.columns(2)
    with col1: team_a_name = st.selectbox("Designated Home Team", list(teams.keys()), index=0)
    with col2: team_b_name = st.selectbox("Designated Away Team", list(teams.keys()), index=1)
    
    if team_a_name != team_b_name and st.button("Execute Match Simulation"):
        tA, tB = teams[team_a_name], teams[team_b_name]
        score_a = np.random.poisson((tA["attack"] / tB["defense"]) * 1.45)
        score_b = np.random.poisson((tB["attack"] / tA["defense"]) * 1.35)
        
        st.markdown(f"<h2 style='text-align: center;'>{team_a_name}  {score_a}  -  {score_b}  {team_b_name}</h2>", unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        with m1: st.metric(f"{team_a_name} Ball Possession", f"{int((tA['midfield']/(tA['midfield']+tB['midfield']))*100)}%")
        with m2: st.metric("Simulated Match State", "FT (After Extra Time)" if score_a == score_b else "Full-Time (FT)")
        with m3: st.metric(f"{team_b_name} Ball Possession", f"{100 - int((tA['midfield']/(tA['midfield']+tB['midfield']))*100)}%")
        # ==========================================
# 5. UI LAYOUT ARCHITECTURE (Safe Top Banner)
# ==========================================
# Ensure these lines start completely at the far left edge of your file!
header_logo_col, header_text_col = st.columns([1, 6])

with header_logo_col:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/4b/FIFA_World_Cup_2026_Logo.svg", width=120)

with header_text_col:
    st.title("Strategós Analytics — World Cup Edition")
    st.caption("Advanced Spatial Data Engine | Elite Scouting & Tactical Performance Framework")

# Render primary pitch interface directly below the branded banner
main_pitch_fig = draw_tactical_pitch()
st.plotly_chart(main_pitch_fig, use_container_width=True)

# Contextual metrics panel below pitch
st.markdown("---")
metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

with metrics_col1:
    st.metric(label="Defensive Line Average Height", value="30.25 m", delta="+1.40 m vs Last Match")
with metrics_col2:
    st.metric(label="Midfield Compactness Area", value="435 m²", delta="-22 m² (More Compact)", delta_color="inverse")
with metrics_col3:
    st.metric(label="Half-Space Entry Infiltrations", value="14", delta="Optimal Zone Saturation")