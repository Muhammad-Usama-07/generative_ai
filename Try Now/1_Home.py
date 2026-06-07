"""
1_Home.py
Main entry point for FitAI multi-page app.
set_page_config() lives HERE ONLY — never in child pages.
"""
import streamlit as st

# ── Must be FIRST Streamlit call, in the main file only ───────────────────────
st.set_page_config(
    page_title="FitAI · Virtual Try-On",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 👗 FitAI")
st.markdown("### AI-Powered Virtual Try-On")
st.markdown("---")
st.markdown("Welcome to **FitAI** — virtually try on tops, bottoms, shoes, dresses and accessories.")

if st.button("✨ Go to Virtual Try-On"):
    st.switch_page("pages/2_Try_On.py")