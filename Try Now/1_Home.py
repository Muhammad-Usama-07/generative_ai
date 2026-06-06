"""
1_Home.py  (or app.py)
Entry point — redirects to the landing page or renders it inline.
Place this in the root as: fitai/1_Home.py
"""
import streamlit as st

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

st.markdown("""
Welcome to **FitAI** — browse our collection and virtually try on any item.

Use the sidebar or click below to get started.
""")

if st.button("✨ Go to Virtual Try-On", use_container_width=False):
    st.switch_page("pages/2_Try_On.py")