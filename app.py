import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 1. Page Configuration (Ensures the app looks wide and professional)
st.set_page_config(
    page_title="Strategós Analytics", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Sleek Top Header Layout (Logo tucked cleanly next to title text)
header_logo, header_text = st.columns([1, 8])

with header_logo:
    # Keeps the asset narrow and proportional instead of massive and centered
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/e/e5/2022_FIFA_World_Cup_official_logo.svg",
        width=85
    )

with header_text:
    st.markdown("<h2 style='margin-bottom: 0px;'>Strategós Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888888; margin-top: 0px;'>World Cup Qatar Hub — Advanced Team Shape Matrix</p>", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px; border-color: #222222;'>", unsafe_allow_html=True)

# 3. Simple Mock Data Data Pipeline (StatsBomb 120x80 Scale)
lines_data = {
    "Defensive Line": {"x": [28, 30, 34, 29], "y": [15, 35, 55, 68], "color": "#EF553B"},
    "Midfield Block": {"x": [52, 55, 58, 54], "y": [12, 32, 50, 70], "color": "#FECB52"},
    "Attacking Line": {"x": [82, 88, 84],     "y": [20, 40, 60], "color": "#00CC96"}
}

np.random.seed(42)
hx = np.random.normal(loc=85, scale=10, size=150).clip(0, 120)
hy = np.random.normal(loc=60, scale=8, size=150).clip(0, 80)

# 4. Two-Column Workspace (Saves vertical space so nothing is pushed down)
control_col, pitch_col = st.columns([1, 3.5])

with control_col:
    st.markdown("<h4 style='color: #ffffff;'>Overlay Controls</h4>", unsafe_allow_html=True)
    
    # Intuitive controls next to the field
    show_def = st.checkbox("🔴 Defensive Chain", value=True)
    show_mid = st.checkbox("🟡 Midfield Block", value=True)
    show_att = st.checkbox("🟢 Attacking Unit", value=False)
    show_heat = st.checkbox("🔥 Spatial Density (Heatmap)", value=True)
    
    st.markdown("<hr style='border-color: #222222;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #ffffff;'>Live Frame Data</h4>", unsafe_allow_html=True)
    st.metric(label="Backline Depth", value="30.25 m")
    st.metric(label="Block Area", value="435 m²")

with pitch_col:
    # Build the clean dark-mode Plotly soccer field
    fig = go.Figure()
    
    fig.update_layout(
        xaxis=dict(range=[-5, 125], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-5, 85], showgrid=False, zeroline=False, visible=False),
        height=580,
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    
    # Precise field boundary markings
    fig.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80, line=dict(color="#2a2a2a", width=2))
    fig.add_shape(type="line", x0=60, y0=0, x1=60, y1=80, line=dict(color="#2a2a2a", width=2, dash="dash"))
    fig.add_shape(type="rect", x0=0, y0=18, x1=18, y1=62, line=dict(color="#2a2a2a", width=1.5))
    fig.add_shape(type="rect", x0=102, y0=18, x1=120, y1=62, line=dict(color="#2a2a2a", width=1.5))
    fig.add_shape(type="circle", x0=50, y0=30, x1=70, y1=50, line=dict(color="#2a2a2a", width=1.5))

    # Heatmap Layer
    if show_heat:
        fig.add_trace(go.Histogram2dContour(
            x=hx, y=hy, colorscale="YlOrRd", showscale=False, ncontours=18, line=dict(width=0), opacity=0.45
        ))

    # Tactical Lines Layers
    if show_def:
        fig.add_trace(go.Scatter(x=lines_data["Defensive Line"]["x"], y=lines_data["Defensive Line"]["y"], mode="lines+markers", line=dict(color=lines_data["Defensive Line"]["color"], width=4), marker=dict(size=8, color="#ffffff")))
    
    if show_mid:
        fig.add_trace(go.Scatter(x=lines_data["Midfield Block"]["x"], y=lines_data["Midfield Block"]["y"], mode="lines+markers", line=dict(color=lines_data["Midfield Block"]["color"], width=4), marker=dict(size=8, color="#ffffff")))
        
    if show_att:
        fig.add_trace(go.Scatter(x=lines_data["Attacking Line"]["x"], y=lines_data["Attacking Line"]["y"], mode="lines+markers", line=dict(color=lines_data["Attacking Line"]["color"], width=4), marker=dict(size=8, color="#ffffff")))

    # Output pitch graphic cleanly
    st.plotly_chart(fig, use_container_width=True)