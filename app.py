import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# ==========================================
# 1. PAGE SETUP & GLOBAL CONFIG
# ==========================================
st.set_page_config(
    page_title="Strategós Analytics", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Set up standard pitch sizing for background grids
PITCH_BG = "#111111"
LINE_COLOR = "#2a2a2a"

# ==========================================
# 2. BRANDED HEADER BANNER
# ==========================================
header_logo, header_text = st.columns([1, 8])

with header_logo:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/e/e5/2022_FIFA_World_Cup_official_logo.svg",
        width=85
    )

with header_text:
    st.markdown("<h2 style='margin-bottom: 0px;'>Strategós Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888888; margin-top: 0px;'>World Cup Qatar Hub — Pro Scouting Suite</p>", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px; border-color: #222222;'>", unsafe_allow_html=True)

# ==========================================
# 3. GLOBAL MATCH CONTROLS (Sidebar)
# ==========================================
st.sidebar.title("Global Match Filter")
selected_match = st.sidebar.selectbox(
    "Select Tournament Fixture:",
    options=["Argentina vs France (Final)", "Croatia vs Morocco", "England vs France"]
)
st.sidebar.info(f"Analyzing spatial tracking frames for: {selected_match}")

# ==========================================
# 4. PRIMARY NAVIGATION MULTI-TABS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Shot Map & xG Plotter", 
    "🕸️ Playmaker Passing Network", 
    "📈 Player Radar Profiler", 
    "⏱️ Game State Timeline"
])

# ------------------------------------------
# TAB 1: SHOT MAP & xG PLOTTER
# ------------------------------------------
with tab1:
    st.subheader("Shot Map Analysis")
    st.caption("Visualizes shot locations, expected goals value (size), and match outcomes.")
    
    # Simple Mock Shot Data (Right-Attack Orientation)
    shots_df = pd.DataFrame({
        "x": [108, 95, 112, 88, 104, 115, 98],
        "y": [40, 52, 36, 25, 44, 41, 60],
        "xG": [0.65, 0.12, 0.45, 0.04, 0.78, 0.18, 0.08],
        "Outcome": ["Goal", "Saved", "Blocked", "Missed", "Goal", "Saved", "Missed"]
    })
    
    # Filters specific to shots
    outcome_filter = st.multiselect("Filter by Shot Outcome:", options=["Goal", "Saved", "Blocked", "Missed"], default=["Goal", "Saved", "Missed"])
    filtered_shots = shots_df[shots_df["Outcome"].isin(outcome_filter)]
    
    # Plotly Canvas
    fig_shots = go.Figure()
    fig_shots.update_layout(xaxis=dict(range=[60, 125], visible=False), yaxis=dict(range=[-5, 85], visible=False), height=450, plot_bgcolor=PITCH_BG, paper_bgcolor=PITCH_BG, margin=dict(l=0,r=0,t=0,b=0), showlegend=True)
    
    # Add half-pitch lines
    fig_shots.add_shape(type="rect", x0=60, y0=0, x1=120, y1=80, line=dict(color=LINE_COLOR, width=2))
    fig_shots.add_shape(type="rect", x0=102, y0=18, x1=120, y1=62, line=dict(color=LINE_COLOR, width=1.5))
    
    # Map outcome colors
    color_map = {"Goal": "#00CC96", "Saved": "#FECB52", "Blocked": "#636EFA", "Missed": "#EF553B"}
    
    for outcome in outcome_filter:
        subset = filtered_shots[filtered_shots["Outcome"] == outcome]
        fig_shots.add_trace(go.Scatter(
            x=subset["x"], y=subset["y"], mode="markers", name=outcome,
            marker=dict(size=subset["xG"] * 40, color=color_map[outcome], line=dict(color="#ffffff", width=1)),
            hovertemplate="<b>xG:</b> %{text}<br><b>Location:</b> (%{x}, %{y})<extra></extra>",
            text=subset["xG"]
        ))
        
    st.plotly_chart(fig_shots, use_container_width=True)

# ------------------------------------------
# TAB 2: PLAYMAKER PASSING NETWORK
# ------------------------------------------
with tab2:
    st.subheader("Passing Distribution Network")
    st.caption("Maps pass frequency volumes and key circulation lanes between central anchors.")
    
    # Nodes (Player Avg Positions)
    players = {
        "Enzo Fernández": (55, 40), "Rodrigo de Paul": (68, 55), 
        "Alexis Mac Allister": (72, 25), "Lionel Messi": (85, 42), "Nicolás Otamendi": (35, 40)
    }
    
    # Direct Links (Pass Volumes)
    links = [
        ("Nicolás Otamendi", "Enzo Fernández", 22),
        ("Enzo Fernández", "Rodrigo de Paul", 18),
        ("Enzo Fernández", "Alexis Mac Allister", 15),
        ("Rodrigo de Paul", "Lionel Messi", 28),
        ("Alexis Mac Allister", "Lionel Messi", 19)
    ]
    
    min_volume = st.slider("Minimum Pass Volume Threshold:", 10, 30, 12)
    
    fig_net = go.Figure()
    fig_net.update_layout(xaxis=dict(range=[-5, 125], visible=False), yaxis=dict(range=[-5, 85], visible=False), height=450, plot_bgcolor=PITCH_BG, paper_bgcolor=PITCH_BG, margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
    fig_net.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80, line=dict(color=LINE_COLOR, width=2))
    fig_net.add_shape(type="line", x0=60, y0=0, x1=60, y1=80, line=dict(color=LINE_COLOR, width=2, dash="dash"))

    # Render Links
    for p1, p2, vol in links:
        if vol >= min_volume:
            x0, y0 = players[p1]
            x1, y1 = players[p2]
            fig_net.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1], mode="lines",
                line=dict(color="#636EFA", width=vol * 0.2), opacity=0.6
            ))
            
    # Render Nodes
    nx, ny, n_names = [], [], []
    for name, coords in players.items():
        nx.append(coords[0])
        ny.append(coords[1])
        n_names.append(name)
        
    fig_net.add_trace(go.Scatter(
        x=nx, y=ny, mode="markers+text", text=n_names, textposition="top center",
        marker=dict(size=14, color="#ffffff", line=dict(color="#636EFA", width=3)),
        textfont=dict(color="#ffffff")
    ))
    
    st.plotly_chart(fig_net, use_container_width=True)

# ------------------------------------------
# TAB 3: PLAYER RADAR PROFILER
# ------------------------------------------
with tab3:
    st.subheader("Scouting Attribute Profiler")
    st.caption("Compares individual performance metrics relative to positional tournament averages.")
    
    metrics = ["Pass %", "Progressive Carries", "Tackles Won", "Interceptions", "Key Passes", "Pressures"]
    
    # Target values vs Baselines
    player_vals = [88, 74, 62, 45, 81, 68]
    template_vals = [70, 50, 50, 50, 50, 50] # Benchmark
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=player_vals + [player_vals[0]], theta=metrics + [metrics[0]], fill='toself', name='Target Profile', line=dict(color="#00CC96")
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=template_vals + [template_vals[0]], theta=metrics + [metrics[0]], fill='toself', name='Tournament Avg', line=dict(color="#333333", dash="dash")
    ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100]), bgcolor="#141414"),
        paper_bgcolor=PITCH_BG, height=450, font=dict(color="#ffffff")
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

# ------------------------------------------
# TAB 4: GAME STATE TIMELINE
# ------------------------------------------
with tab4:
    st.subheader("Tactical Evolution Timeline")
    st.caption("Evaluate behavioral shape adjustments across shifting scorelines and minute cycles.")
    
    selected_phase = st.select_slider(
        "Match Phase Sequence:",
        options=["0'-15' (Opening Setup)", "15'-45' (Leading 1-0)", "45'-75' (Chasing Equalizer)", "75'-90' (Low Block Containment)"]
    )
    
    st.markdown("---")
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        if "Opening" in selected_phase:
            st.info("📋 **Tactical Posture: High Defensive Line**\n\nTeam is deployed in a balanced 4-3-3 shape, forcing high turnovers in the central third.")
        elif "Leading" in selected_phase:
            st.success("📋 **Tactical Posture: Controlled Midfield Block**\n\nPossession tempo slowed down by 14%. Focus shifted to horizontal ball circulation to draw out opponents.")
        elif "Chasing" in selected_phase:
            st.warning("📋 **Tactical Posture: High-Overload Pressing**\n\nFull-backs pushed into the final third. Transition structure shifted to an aggressive 2-3-5 blueprint.")
        elif "Low Block" in selected_phase:
            st.error("📋 **Tactical Posture: Deep Structural Containment**\n\nDefensive block depth dropped to 16.4m. Substitution utilized to introduce a 5-4-1 compact low-block layout.")
            
    with col_t2:
        st.markdown("**Phase Event Analysis Reading:**")
        st.write("- **Structural Compactness:** 92%")
        st.write("- **PPDA (Passes Per Defensive Action):** 8.4")
        st.write("- **Counter-Press Recovery Efficiency:** High")