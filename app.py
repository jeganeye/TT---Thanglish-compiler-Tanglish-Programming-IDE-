"""
Tanglish Programming Language IDE - Streamlit Cloud Wrapper
Loads and renders the exact templates/index.html UI with full Dracula theme,
CodeMirror, pop-up Examples modal, pop-up Help modal, and Output Console.
"""
import os
import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Tanglish Programming IDE",
    page_icon="https://i.ibb.co/Ftydmrw/thanglish-logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Completely remove all Streamlit chrome (header, footer, sidebar, paddings)
st.markdown("""
<style>
    #MainMenu, header, footer, [data-testid="stSidebar"], [data-testid="collapsedControl"], .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 999999 !important;
    }
</style>
""", unsafe_allow_html=True)

# Read the exact templates/index.html
html_file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
with open(html_file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Render exact index.html in full screen
components.html(html_content, height=1200, scrolling=True)
