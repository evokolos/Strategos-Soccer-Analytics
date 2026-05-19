import streamlit as st
import plotly.graph_objects as go

# 1. Global Tactical Color Configuration
TACTICAL_COLORS = {
    "Defensive Line": "#EF553B",      # Crimson Red
    "Midfield Block": "#FECB52",      # Amber Yellow
    "Attacking Line": "#00CC96",      # Emerald Green
    "Passing Lane/Link": "#636EFA",    # Electric Blue
    "Pressing/Cover Line": "#AB63FA", # Royal Purple
    "Width/Flank Unit": "#19D3F3"     # Cyan
}

st.set_page_config(layout="wide")
st.title("Strategós Analytics — Tactical Shape Engine")

# 2. Sidebar Filters
st.sidebar.header("Tactical Overlay Control")
st.sidebar.write("Toggle structural layers to analyze team compactness and spatial gaps.")

selected_lines = st.sidebar.multiselect(
    "Select Tactical Lines to Display:",
    options=list(TACTICAL_COLORS.keys()),
    default=["Defensive Line", "Midfield Block"]  # Focus on defensive stability by default
)

# 3. Dynamic Coordinate Data Pipeline
# In production, these coordinates are derived dynamically from player positional tracking frames
computed_tactical_data = {
    "Defensive Line": {"x": [28, 30, 34, 29], "y": [15, 35, 55, 68]},
    "Midfield Block": {"x": [52, 55, 58, 54], "y": [12, 32, 50, 70]},
    "Attacking Line": {"x": [82, 88, 84],     "y": [20, 40, 60]},
    "Passing Lane/Link": {"x": [30, 55],       "y": [35, 32]},
    "Pressing/Cover Line": {"x": [88, 95, 92], "y": [35, 50, 65]},
    "Width/Flank Unit": {"x": [34, 58, 84],    "y": [72, 74, 76]}
}

# 4. Initialize Plotly Pitch (StatsBomb dimensions)
fig = go.Figure()

# Base pitch setup with subtle tactical dark-mode styling
fig.update_layout(
    xaxis=dict(range=[0, 120], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[0, 80], showgrid=False, zeroline=False, visible=False),
    width=900,
    height=600,
    plot_bgcolor="#141414",  # Ultra-dark canvas to make colors pop
    paper_bgcolor="#141414",
    margin=dict(l=20, r=20, t=20, b=20),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color="#ffffff")
    )
)

# Subtle Pitch Outline & Halfway Line for reference
fig.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80, line=dict(color="#333333", width=2))
fig.add_shape(type="line", x0=60, y0=0, x1=60, y1=80, line=dict(color="#333333", width=2, dash="dash"))

# 5. The Combined Filter & Rendering Loop
for line_name, line_coords in computed_tactical_data.items():
    if line_name in selected_lines:
        
        # Style logic: Abstract connections (Passing Lanes) get dashed formatting
        is_link = "Lane" in line_name or "Link" in line_name
        
        fig.add_trace(go.Scatter(
            x=line_coords['x'],
            y=line_coords['y'],
            mode="lines+markers",
            name=line_name,
            line=dict(
                color=TACTICAL_COLORS[line_name],
                width=3.5 if not is_link else 2,
                dash="dash" if is_link else "solid"
            ),
            marker=dict(
                size=8, 
                color="#ffffff", 
                line=dict(color=TACTICAL_COLORS[line_name], width=2)
            ),
            hoverinfo="name"
        ))

# 6. Streamlit Layout Distribution
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Match Insights")
    st.info("💡 **Scouting Note:** Toggle the 'Defensive Line' and 'Midfield Block' concurrently to observe the vertical compression of the space between the lines.")
    
    # Contextual readout based on what user has selected
    if "Defensive Line" in selected_lines:
        st.write("🔴 **Defensive Line Status:** Average depth measured at **30.25m**. Medium-high block deployment detected.")
    if "Midfield Block" in selected_lines:
        st.write("🟡 **Midfield Block Status:** Lateral horizontal coverage spanning **58m**. Wide structural shifting.")