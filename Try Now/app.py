import streamlit as st
from PIL import Image
import io

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitAI · Virtual Try-On",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0a;
    color: #f0ece4;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,200,80,.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(220,120,60,.06) 0%, transparent 55%),
        #0a0a0a;
}

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Typography ── */
h1, h2, h3, .display { font-family: 'Bebas Neue', sans-serif; letter-spacing: .04em; }
body, p, label, span, div { font-family: 'DM Sans', sans-serif; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
}
.hero .logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem, 8vw, 6rem);
    letter-spacing: .12em;
    background: linear-gradient(120deg, #f5c842 0%, #ff7b3a 55%, #f5c842 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.hero .tagline {
    font-size: .95rem;
    color: #888;
    letter-spacing: .25em;
    text-transform: uppercase;
    margin-top: .5rem;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245,200,66,.35), transparent);
    margin: 0 auto 2.5rem;
    max-width: 600px;
}

/* ── Upload card ── */
.upload-card {
    background: rgba(255,255,255,.032);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 20px;
    padding: 2rem 1.5rem;
    backdrop-filter: blur(8px);
    transition: border-color .3s;
    height: 100%;
}
.upload-card:hover { border-color: rgba(245,200,66,.3); }

.card-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.35rem;
    letter-spacing: .08em;
    color: #f5c842;
    margin-bottom: .25rem;
}
.card-sub {
    font-size: .78rem;
    color: #666;
    letter-spacing: .15em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

/* ── File uploader overrides ── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed rgba(245,200,66,.25) !important;
    border-radius: 14px !important;
    background: rgba(245,200,66,.03) !important;
    transition: all .3s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(245,200,66,.55) !important;
    background: rgba(245,200,66,.06) !important;
}
[data-testid="stFileUploaderDropzone"] { padding: 1.8rem !important; }
[data-testid="stFileUploaderDropzoneInstructions"] { color: #888 !important; }

/* ── Preview image ── */
.preview-wrap {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.08);
    margin-top: .75rem;
    position: relative;
}
.preview-wrap img { display: block; width: 100%; }
.preview-badge {
    position: absolute;
    bottom: 10px; right: 10px;
    background: rgba(0,0,0,.65);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: .7rem;
    color: #aaa;
    letter-spacing: .1em;
    backdrop-filter: blur(6px);
}

/* ── CTA button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    padding: 1rem 2rem;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: .18em;
    color: #0a0a0a;
    background: linear-gradient(120deg, #f5c842 0%, #ff7b3a 100%);
    border: none;
    border-radius: 14px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: transform .2s, box-shadow .2s;
    box-shadow: 0 4px 28px rgba(245,200,66,.25);
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 40px rgba(245,200,66,.4);
}
div[data-testid="stButton"] > button:active { transform: translateY(0); }

/* ── Status / info boxes ── */
[data-testid="stInfo"] {
    background: rgba(245,200,66,.07) !important;
    border-left: 3px solid #f5c842 !important;
    border-radius: 10px !important;
    color: #c8ad5a !important;
}
[data-testid="stSuccess"] {
    background: rgba(60,220,130,.07) !important;
    border-left: 3px solid #3cdc82 !important;
    border-radius: 10px !important;
}
[data-testid="stWarning"] {
    background: rgba(255,123,58,.07) !important;
    border-left: 3px solid #ff7b3a !important;
    border-radius: 10px !important;
}

/* ── Result panel ── */
.result-panel {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 1.5rem;
    text-align: center;
}
.result-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: .12em;
    color: #3cdc82;
    margin-bottom: 1rem;
}

/* ── Steps row ── */
.steps-row {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin: 2rem 0 3rem;
    flex-wrap: wrap;
}
.step {
    display: flex;
    align-items: center;
    gap: .55rem;
    font-size: .78rem;
    color: #666;
    letter-spacing: .08em;
    text-transform: uppercase;
}
.step .num {
    width: 26px; height: 26px;
    border-radius: 50%;
    border: 1px solid rgba(245,200,66,.35);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: .9rem;
    color: #f5c842;
}
.step-arrow { color: #333; font-size: .85rem; }
</style>
""", unsafe_allow_html=True)


# ── Hero ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="logo">FIT AI</div>
    <div class="tagline">Virtual Try-On &nbsp;·&nbsp; Powered by Generative AI</div>
</div>
<div class="divider"></div>

<div class="steps-row">
    <div class="step"><div class="num">1</div> Upload your photo</div>
    <div class="step-arrow">→</div>
    <div class="step"><div class="num">2</div> Upload clothing</div>
    <div class="step-arrow">→</div>
    <div class="step"><div class="num">3</div> Generate try-on</div>
    <div class="step-arrow">→</div>
    <div class="step"><div class="num">4</div> Download result</div>
</div>
""", unsafe_allow_html=True)


# ── Upload columns ──────────────────────────────────────────────────────────────
col1, col_gap, col2 = st.columns([1, 0.08, 1])

# -- Person photo
with col1:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Your Photo</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">Full-body shot works best</div>', unsafe_allow_html=True)

    person_file = st.file_uploader(
        "Drop your photo here",
        type=["jpg", "jpeg", "png", "webp"],
        key="person_upload",
        label_visibility="collapsed",
    )

    if person_file:
        img = Image.open(person_file)
        st.markdown('<div class="preview-wrap">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown('<div class="preview-badge">✓ LOADED</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.success(f"Photo ready — {img.size[0]}×{img.size[1]} px")

    st.markdown('</div>', unsafe_allow_html=True)

# -- Clothing image
with col2:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Clothing Item</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">T-shirt, jacket, dress …</div>', unsafe_allow_html=True)

    cloth_file = st.file_uploader(
        "Drop the clothing image here",
        type=["jpg", "jpeg", "png", "webp"],
        key="cloth_upload",
        label_visibility="collapsed",
    )

    if cloth_file:
        img_c = Image.open(cloth_file)
        st.markdown('<div class="preview-wrap">', unsafe_allow_html=True)
        st.image(img_c, use_container_width=True)
        st.markdown('<div class="preview-badge">✓ LOADED</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.success(f"Clothing ready — {img_c.size[0]}×{img_c.size[1]} px")

    st.markdown('</div>', unsafe_allow_html=True)


# ── CTA Button ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
btn_col = st.columns([1, 2, 1])[1]

with btn_col:
    if not person_file or not cloth_file:
        st.info("Upload both images above to enable the try-on")

    generate = st.button(
        "✦  UPDATE CLOTHES",
        disabled=(not person_file or not cloth_file),
        use_container_width=True,
    )

# ── Generation placeholder ──────────────────────────────────────────────────────
if generate:
    with st.spinner("Generating your virtual try-on …"):
        import time
        time.sleep(2)          # ← replace with your AI call

    st.markdown("""
    <div class="result-panel">
        <div class="result-label">✓ Try-On Generated</div>
    </div>
    """, unsafe_allow_html=True)

    res_col = st.columns([1, 2, 1])[1]
    with res_col:
        # Placeholder: show the person photo back as a stand-in for the AI result
        st.image(
            Image.open(person_file),
            caption="🔮 AI result will appear here",
            use_container_width=True,
        )
        buf = io.BytesIO()
        Image.open(person_file).save(buf, format="PNG")
        st.download_button(
            "⬇  Download Result",
            data=buf.getvalue(),
            file_name="tryon_result.png",
            mime="image/png",
            use_container_width=True,
        )