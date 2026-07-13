# state.py
import streamlit as st

def init_state():
    defaults = {
        "step": 0,              # 0=config, 1=per-slide, 2=done
        "topic": "",
        "category": "",
        "no_of_slides": 3,
        "current_slide": 1,
        "titles": [],           # 3 title options for current slide
        "selected_title": None,
        "contents": (),         # (v1, v2) for current slide
        "selected_content": None,
        "presen_titles": [],    # finalized titles so far
        "presen_content": [],   # finalized content so far
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val