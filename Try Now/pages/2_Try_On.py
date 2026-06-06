"""
pages/2_Try_On.py
Virtual Try-On page — Groq Vision (FREE) + IDM-VTON HuggingFace Space (FREE)
"""

import streamlit as st
import os
import io
import time
from PIL import Image
from dotenv import load_dotenv
load_dotenv()   # reads .env automatically — no manual set needed

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitAI · Try-On",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Outfit:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0e0c0a;
    color: #f0ece4;
    font-family: 'Outfit', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 70% 40% at 15% 0%, rgba(200,169,110,.06) 0%, transparent 55%),
        radial-gradient(ellipse 50% 30% at 85% 100%, rgba(184,92,56,.05) 0%, transparent 50%),
        #0e0c0a;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Back link ── */
.back-link { font-size:.8rem; color:#666; letter-spacing:.12em; text-transform:uppercase; margin-bottom:2rem; display:inline-block; text-decoration:none; transition:color .2s; }
.back-link:hover { color:#c8a96e; }

/* ── Page header ── */
.page-header { margin-bottom: 2.5rem; }
.page-header h1 { font-family:'Playfair Display',serif; font-size:clamp(2rem,4vw,3rem); color:#f0ece4; line-height:1.1; }
.page-header h1 em { font-style:italic; color:#c8a96e; }
.page-header p { color:#666; font-size:.9rem; margin-top:.5rem; font-weight:300; }

/* ── Upload cards ── */
.upload-card {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(200,169,110,.12);
    border-radius: 18px;
    padding: 1.8rem;
    height: 100%;
    transition: border-color .3s;
}
.upload-card:hover { border-color: rgba(200,169,110,.28); }
.card-label { font-size:.7rem; font-weight:600; letter-spacing:.18em; text-transform:uppercase; color:#c8a96e; margin-bottom:.4rem; }
.card-title { font-family:'Playfair Display',serif; font-size:1.2rem; color:#f0ece4; margin-bottom:1.2rem; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed rgba(200,169,110,.2) !important;
    border-radius: 12px !important;
    background: rgba(200,169,110,.03) !important;
    transition: all .3s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(200,169,110,.45) !important;
    background: rgba(200,169,110,.06) !important;
}

/* ── Preview ── */
.img-preview { border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,.07); margin-top:.75rem; }

/* ── Analysis badge ── */
.analysis-wrap {
    background: rgba(200,169,110,.07);
    border: 1px solid rgba(200,169,110,.18);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-top: 1rem;
}
.analysis-row { display:flex; gap:.6rem; align-items:center; flex-wrap:wrap; margin-bottom:.5rem; }
.a-badge { background:rgba(200,169,110,.15); color:#c8a96e; padding:.22rem .75rem; border-radius:20px; font-size:.72rem; font-weight:600; letter-spacing:.08em; text-transform:uppercase; }
.a-desc { font-size:.82rem; color:#aaa; line-height:1.5; }

/* ── Settings ── */
.settings-card {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 14px;
    padding: 1.4rem;
    margin-top:1rem;
}
.settings-title { font-size:.72rem; letter-spacing:.15em; text-transform:uppercase; color:#666; margin-bottom:1rem; }

/* ── Streamlit slider/number overrides ── */
[data-testid="stSlider"] > div > div { color: #c8a96e !important; }
[data-testid="stNumberInput"] input { background: rgba(255,255,255,.05) !important; border-color: rgba(200,169,110,.2) !important; color: #f0ece4 !important; border-radius: 8px !important; }

/* ── Generate button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    padding: 1rem 2rem;
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #0e0c0a;
    background: linear-gradient(120deg, #c8a96e 0%, #e8a84a 100%);
    border: none;
    border-radius: 14px;
    cursor: pointer;
    transition: transform .2s, box-shadow .2s;
    box-shadow: 0 4px 24px rgba(200,169,110,.22);
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 36px rgba(200,169,110,.38);
}
div[data-testid="stButton"] > button:disabled {
    background: rgba(255,255,255,.08) !important;
    color: #444 !important;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
}

/* ── Result panel ── */
.result-header {
    display:flex; align-items:center; gap:.75rem;
    margin-bottom:1.2rem;
}
.result-dot { width:10px; height:10px; border-radius:50%; background:#4caf7d; box-shadow:0 0 8px rgba(76,175,125,.5); }
.result-title { font-family:'Playfair Display',serif; font-size:1.4rem; color:#f0ece4; }
.result-card {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(76,175,125,.2);
    border-radius: 18px;
    padding: 1.8rem;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    width: 100%;
    background: transparent !important;
    border: 1.5px solid rgba(200,169,110,.35) !important;
    color: #c8a96e !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    letter-spacing:.06em;
    transition: all .2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(200,169,110,.1) !important;
    border-color: #c8a96e !important;
    transform: translateY(-1px) !important;
}

/* ── Status overrides ── */
[data-testid="stInfo"]    { background:rgba(200,169,110,.07)!important; border-left:3px solid #c8a96e!important; border-radius:10px!important; color:#c8a96e!important; }
[data-testid="stSuccess"] { background:rgba(76,175,125,.07)!important; border-left:3px solid #4caf7d!important; border-radius:10px!important; }
[data-testid="stError"]   { background:rgba(184,92,56,.07)!important; border-left:3px solid #b85c38!important; border-radius:10px!important; }
[data-testid="stWarning"] { background:rgba(200,169,110,.07)!important; border-left:3px solid #c8a96e!important; border-radius:10px!important; }

/* ── Progress steps ── */
.progress-steps { display:flex; gap:.5rem; align-items:center; margin:.75rem 0 1.5rem; }
.p-step { display:flex; align-items:center; gap:.4rem; font-size:.75rem; letter-spacing:.08em; text-transform:uppercase; }
.p-step .dot { width:8px; height:8px; border-radius:50%; }
.p-step.done .dot  { background:#4caf7d; }
.p-step.active .dot { background:#c8a96e; animation:pulse 1s infinite; }
.p-step.idle .dot  { background:#333; }
.p-step.done  { color:#4caf7d; }
.p-step.active { color:#c8a96e; }
.p-step.idle  { color:#444; }
.p-arrow { color:#333; font-size:.7rem; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

/* ── Divider ── */
.divider { height:1px; background:linear-gradient(90deg,transparent,rgba(200,169,110,.2),transparent); margin:2rem 0; }
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
for key in ["analysis", "result_img", "generating", "step"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "step" not in st.session_state or st.session_state.step is None:
    st.session_state.step = 0   # 0=idle, 1=analyzing, 2=generating, 3=done


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<a class="back-link" href="/">← Back to collection</a>', unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>Virtual <em>Try-On</em></h1>
    <p>Upload your photo + a clothing item → AI dresses you in seconds &nbsp;·&nbsp; Free &nbsp;·&nbsp; No GPU needed</p>
</div>
""", unsafe_allow_html=True)

# ── API key check ──────────────────────────────────────────────────────────────
groq_key = os.environ.get("GROQ_API_KEY", "")
if not groq_key:
    st.warning("⚠️  **GROQ_API_KEY** not set. Add it to your `.env` or environment variables. Get a free key at [console.groq.com](https://console.groq.com).")


# ── Progress indicator ─────────────────────────────────────────────────────────
def step_class(target):
    s = st.session_state.step
    if s > target:  return "done"
    if s == target: return "active"
    return "idle"

st.markdown(f"""
<div class="progress-steps">
    <div class="p-step {step_class(1)}"><div class="dot"></div>Analyze clothing</div>
    <div class="p-arrow">›</div>
    <div class="p-step {step_class(2)}"><div class="dot"></div>Generate try-on</div>
    <div class="p-arrow">›</div>
    <div class="p-step {step_class(3)}"><div class="dot"></div>Result ready</div>
</div>
""", unsafe_allow_html=True)


# ── Upload columns ─────────────────────────────────────────────────────────────
col_person, col_gap, col_cloth = st.columns([1, 0.06, 1])

# ---- Person photo
with col_person:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Step 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Your Photo</div>', unsafe_allow_html=True)

    person_file = st.file_uploader(
        "Full-body shot works best",
        type=["jpg", "jpeg", "png", "webp"],
        key="person_img",
        label_visibility="visible",
    )

    if person_file:
        person_pil = Image.open(person_file).convert("RGB")
        st.image(person_pil, use_column_width=True)
        st.success(f"✓ Photo loaded — {person_pil.size[0]}×{person_pil.size[1]} px")
    else:
        st.info("Upload a clear full-body photo for best results.")

    st.markdown('</div>', unsafe_allow_html=True)


# ---- Clothing image
with col_cloth:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Step 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Clothing Item</div>', unsafe_allow_html=True)

    cloth_file = st.file_uploader(
        "T-shirt, jacket, dress, trousers …",
        type=["jpg", "jpeg", "png", "webp"],
        key="cloth_img",
        label_visibility="visible",
    )

    if cloth_file:
        cloth_pil = Image.open(cloth_file).convert("RGB")
        st.image(cloth_pil, use_column_width=True)
        st.success(f"✓ Clothing loaded — {cloth_pil.size[0]}×{cloth_pil.size[1]} px")

        # ── Groq analysis (auto-triggers when cloth uploaded)
        if st.session_state.analysis is None or st.session_state.get("last_cloth") != cloth_file.name:
            if groq_key:
                with st.spinner("🤖 Groq is analyzing your clothing…"):
                    try:
                        from backend.analyze_cloth import analyze_clothing
                        cloth_file.seek(0)
                        ext = cloth_file.name.rsplit(".", 1)[-1].lower()
                        mime = f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"
                        analysis = analyze_clothing(cloth_file.read(), mime)
                        st.session_state.analysis = analysis
                        st.session_state.last_cloth = cloth_file.name
                        if st.session_state.step < 1:
                            st.session_state.step = 1
                    except Exception as e:
                        st.error(f"Groq analysis failed: {e}")
                        st.session_state.analysis = {
                            "description": "Clothing item",
                            "category": "top", "color": "unknown",
                            "fit": "regular", "fabric": "unknown",
                            "prompt": cloth_file.name,
                        }
            else:
                # No API key — use placeholder
                st.session_state.analysis = {
                    "description": "Clothing item (add GROQ_API_KEY for AI analysis)",
                    "category": "top", "color": "—", "fit": "regular",
                    "fabric": "—", "prompt": "clothing item for virtual try-on",
                }
                st.session_state.last_cloth = cloth_file.name

        # Show analysis result
        if st.session_state.analysis:
            a = st.session_state.analysis
            st.markdown(f"""
            <div class="analysis-wrap">
                <div class="analysis-row">
                    <span class="a-badge">{a.get('category','—')}</span>
                    <span class="a-badge">{a.get('color','—')}</span>
                    <span class="a-badge">{a.get('fit','—')}</span>
                    <span class="a-badge">{a.get('fabric','—')}</span>
                </div>
                <div class="a-desc">🤖 <strong>Groq:</strong> {a.get('description','—')}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Upload the clothing item you want to try on.")

    st.markdown('</div>', unsafe_allow_html=True)


# ── Settings + Generate ────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

set_col, btn_col = st.columns([2, 1])

with set_col:
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="settings-title">⚙ Generation settings</div>', unsafe_allow_html=True)

    s1, s2 = st.columns(2)
    with s1:
        denoise_steps = st.slider(
            "Denoising steps",
            min_value=20, max_value=50, value=30, step=5,
            help="Higher = better quality but slower. 30 is the sweet spot.",
        )
    with s2:
        seed = st.number_input(
            "Seed",
            min_value=0, max_value=9999, value=42, step=1,
            help="Change seed for different variations of the result.",
        )

    st.markdown('</div>', unsafe_allow_html=True)

with btn_col:
    st.markdown("<br>", unsafe_allow_html=True)
    both_uploaded = person_file is not None and cloth_file is not None
    generate_btn = st.button(
        "✦ Generate Try-On",
        disabled=not both_uploaded,
        use_container_width=True,
        key="generate",
    )

    if not both_uploaded:
        st.caption("Upload both images above to enable.")


# ── Generation logic ───────────────────────────────────────────────────────────
if generate_btn and both_uploaded:
    st.session_state.result_img = None
    st.session_state.step = 2

    cloth_desc = (st.session_state.analysis or {}).get("prompt", "clothing item for virtual try-on")

    with st.spinner("🔄 Connecting to IDM-VTON on HuggingFace…"):
        try:
            from backend.generate import run_tryon, pil_to_bytes

            person_file.seek(0)
            cloth_file.seek(0)
            person_pil_fresh = Image.open(person_file).convert("RGB")
            cloth_pil_fresh  = Image.open(cloth_file).convert("RGB")

            result_img = run_tryon(
                person_image=person_pil_fresh,
                cloth_image=cloth_pil_fresh,
                cloth_description=cloth_desc,
                denoise_steps=denoise_steps,
                seed=int(seed),
            )

            st.session_state.result_img = result_img
            st.session_state.step = 3

        except Exception as e:
            st.error(f"❌ Try-on generation failed: {e}")
            st.info("Make sure `gradio_client` is installed: `pip install gradio_client`")
            st.session_state.step = 0


# ── Result display ─────────────────────────────────────────────────────────────
if st.session_state.result_img is not None:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="result-header">
        <div class="result-dot"></div>
        <div class="result-title">Your Try-On Result</div>
    </div>
    """, unsafe_allow_html=True)

    res_img = st.session_state.result_img
    rc1, rc2, rc3 = st.columns([1, 2, 1])

    with rc2:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)

        # Side-by-side: original vs result
        cmp1, cmp2 = st.columns(2)
        with cmp1:
            st.caption("Original")
            person_file.seek(0)
            st.image(Image.open(person_file), use_column_width=True)
        with cmp2:
            st.caption("✨ With clothing")
            st.image(res_img, use_column_width=True)

        # Download button
        from backend.generate import pil_to_bytes
        result_bytes = pil_to_bytes(res_img, fmt="PNG")
        st.download_button(
            "⬇  Download Result (PNG)",
            data=result_bytes,
            file_name="fitai_tryon_result.png",
            mime="image/png",
            use_container_width=True,
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # Try another
    st.markdown("<br>", unsafe_allow_html=True)
    ta_col = st.columns([1, 2, 1])[1]
    with ta_col:
        if st.button("↺  Try Another Outfit", use_container_width=True):
            st.session_state.result_img = None
            st.session_state.analysis = None
            st.session_state.step = 0
            st.rerun()