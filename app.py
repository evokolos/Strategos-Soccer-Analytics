import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Strategós Analytics", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Sleek Top Header Layout (Logo next to title text)
header_logo, header_text = st.columns([1, 8])

with header_logo:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/e/e5/2022_FIFA_World_Cup_official_logo.svg",
        width=85
    )

with header_text:
    st.markdown("<h2 style='margin-bottom: 0px;'>Strategós Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888888; margin-top: 0px;'>World Cup Qatar Hub</p>", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px; border-color: #222222;'>", unsafe_allow_html=True)

# 3. Streamlined Workspace Layout
control_col, display_col = st.columns([1, 3.5])

with control_col:
    st.markdown("<h4 style='color: #ffffff;'>Overlay Controls</h4>", unsafe_allow_html=True)
    
    # Clean tracking checkboxes
    show_def = st.checkbox("🔴 Defensive Chain", value=True)
    show_mid = st.checkbox("🟡 Midfield Block", value=True)
    show_att = st.checkbox("🟢 Attacking Unit", value=False)
    show_heat = st.checkbox("🔥 Spatial Density (Heatmap)", value=True)
    
    st.markdown("<hr style='border-color: #222222;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #ffffff;'>Live Frame Data</h4>", unsafe_allow_html=True)
    st.metric(label="Backline Depth", value="30.25 m")
    st.metric(label="Block Area", value="435 m²")

with display_col:
    st.info("The advanced matrix rendering layers have been removed. Ready for new visualization or data structures.")