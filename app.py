import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# ==========================================
# 1. GLOBAL CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="Strategós Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

TACTICAL_COLORS = {
    "Defensive Line": "#EF553B",      # Crimson Red
    "Midfield Block": "#FECB52",      # Amber Yellow
    "Attacking Line": "#00CC96",      # Emerald Green
    "Passing Lane/Link": "#636EFA",    # Electric Blue
    "Pressing/Cover Line": "#AB63FA", # Royal Purple
    "Width/Flank Unit": "#19D3F3"     # Cyan
}

# ==========================================
# 2. DATA ENGINE (StatsBomb 120x80 Scale)
# ==========================================
@st.cache_data
def load_mock_tactical_data():
    lines = {
        "Defensive Line": {"x": [28, 30, 34, 29], "y": [15, 35, 55, 68]},
        "Midfield Block": {"x": [52, 55, 58, 54], "y": [12, 32, 50, 70]},
        "Attacking Line": {"x": [82, 88, 84],     "y": [20, 40, 60]},
        "Passing Lane/Link": {"x": [30, 55],       "y": [35, 32]},
        "Pressing/Cover Line": {"x": [88, 95, 92], "y": [35, 50, 65]},
        "Width/Flank Unit": {"x": [34, 58, 84],    "y": [72, 74, 76]}
    }
    
    np.random.seed(42)
    heatmap_events = pd.DataFrame({
        "x": np.random.normal(loc=82, scale=12, size=200),
        "y": np.random.normal(loc=58, scale=10, size=200)
    })
    heatmap_events["x"] = heatmap_events["x"].clip(0, 120)
    heatmap_events["y"] = heatmap_events["y"].clip(0, 80)
    
    return lines, heatmap_events

computed_lines, heatmap_df = load_mock_tactical_data()

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
st.sidebar.title("Strategós Control Panel")
st.sidebar.write("Configure layers for professional match-shape analysis.")
st.sidebar.markdown("---")

st.sidebar.subheader("Structural Overlays")
selected_lines = st.sidebar.multiselect(
    "Select Structural Units:",
    options=list(TACTICAL_COLORS.keys()),
    default=["Defensive Line", "Midfield Block"]
)

st.sidebar.markdown("---")

st.sidebar.subheader("Territorial Dominance")
enable_heatmap = st.sidebar.checkbox("Enable Player Heatmap", value=True)
if enable_heatmap:
    target_player = st.sidebar.selectbox(
        "Target Player Vector:",
        options=["Winger (Right-Flank Inverted)", "Deep Playmaker", "Striker"]
    )
    heatmap_opacity = st.sidebar.slider("Heatmap Intensity Opacity", 0.1, 1.0, 0.45, step=0.05)

# ==========================================
# 4. PITCH RENDERING ENGINE (Plotly)
# ==========================================
def draw_tactical_pitch():
    fig = go.Figure()

    fig.update_layout(
        xaxis=dict(range=[-5, 125], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-5, 85], showgrid=False, zeroline=False, visible=False),
        width=950,
        height=630,
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(color="#aaaaaa", size=12)
        )
    )

    pitch_line_color = "#2a2a2a"
    fig.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80, line=dict(color=pitch_line_color, width=2))
    fig.add_shape(type="line", x0=60, y0=0, x1=60, y1=80, line=dict(color=pitch_line_color, width=2, dash="dash"))
    fig.add_shape(type="rect", x0=0, y0=18, x1=18, y1=62, line=dict(color=pitch_line_color, width=1.5))
    fig.add_shape(type="rect", x0=102, y0=18, x1=120, y1=62, line=dict(color=pitch_line_color, width=1.5))
    fig.add_shape(type="circle", x0=50, y0=30, x1=70, y1=50, line=dict(color=pitch_line_color, width=1.5))

    if enable_heatmap:
        fig.add_trace(go.Histogram2dContour(
            x=heatmap_df["x"],
            y=heatmap_df["y"],
            name="Spatial Density",
            colorscale="YlOrRd",
            reversescale=False,
            showscale=False,
            ncontours=24,
            line=dict(width=0),
            opacity=heatmap_opacity,
            hoverinfo="skip"
        ))

    for line_name, coords in computed_lines.items():
        if line_name in selected_lines:
            is_abstract_link = "Lane" in line_name or "Link" in line_name
            
            fig.add_trace(go.Scatter(
                x=coords["x"],
                y=coords["y"],
                mode="lines+markers",
                name=line_name,
                line=dict(
                    color=TACTICAL_COLORS[line_name],
                    width=4 if not is_abstract_link else 2,
                    dash="dash" if is_abstract_link else "solid"
                ),
                marker=dict(
                    size=8,
                    color="#ffffff",
                    line=dict(color=TACTICAL_COLORS[line_name], width=2)
                ),
                hoverinfo="name"
            ))

    return fig

# ==========================================
# 5. UI LAYOUT ARCHITECTURE
# ==========================================
header_logo_col, header_text_col = st.columns([1, 7])

with header_logo_col:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/4/4b/FIFA_World_Cup_2026_Logo.svg",
        width=100
    )

with header_text_col:
    st.title("Strategós Analytics — World Cup Edition")
    st.caption("Advanced Spatial Data Engine | Elite Scouting & Tactical Performance Framework")

main_pitch_fig = draw_tactical_pitch()
st.plotly_chart(main_pitch_fig, use_container_width=True)

st.markdown("---")
metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

with metrics_col1:
    st.metric(label="Defensive Line Average Height", value="30.25 m")
with metrics_col2:
    st.metric(label="Midfield Compactness Area", value="435 m²")
with metrics_col3:
    st.metric(label="Half-Space Entry Infiltrations", value="14")