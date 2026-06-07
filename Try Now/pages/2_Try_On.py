"""
pages/2_Try_On.py
Virtual Try-On — Category selector (Tops, Bottoms, Shoes, Dresses, Accessories)
Groq Vision (FREE) + IDM-VTON HuggingFace Space (FREE)
"""

import streamlit as st
import os
import io
from PIL import Image

# ── Load .env ──────────────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Outfit:wght@300;400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0e0c0a; color: #f0ece4; font-family: 'Outfit', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 70% 40% at 15% 0%, rgba(200,169,110,.06) 0%, transparent 55%),
        radial-gradient(ellipse 50% 30% at 85% 100%, rgba(184,92,56,.05) 0%, transparent 50%),
        #0e0c0a;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

.back-link { font-size:.8rem; color:#666; letter-spacing:.12em; text-transform:uppercase;
    margin-bottom:2rem; display:inline-block; text-decoration:none; transition:color .2s; }
.back-link:hover { color:#c8a96e; }

.page-header { margin-bottom:1.5rem; }
.page-header h1 { font-family:'Playfair Display',serif; font-size:clamp(2rem,4vw,3rem);
    color:#f0ece4; line-height:1.1; }
.page-header h1 em { font-style:italic; color:#c8a96e; }
.page-header p { color:#666; font-size:.9rem; margin-top:.5rem; font-weight:300; }

/* ── Category selector ── */
.cat-selector-wrap { margin-bottom:2rem; }
.cat-selector-label { font-size:.7rem; font-weight:600; letter-spacing:.18em;
    text-transform:uppercase; color:#666; margin-bottom:.8rem; }
.cat-pills { display:flex; gap:.6rem; flex-wrap:wrap; }
.cat-pill {
    display:flex; align-items:center; gap:.5rem;
    padding:.55rem 1.2rem; border-radius:40px; cursor:pointer;
    border:1.5px solid rgba(255,255,255,.08); background:rgba(255,255,255,.03);
    color:#888; font-size:.82rem; font-weight:500; letter-spacing:.05em;
    transition:all .2s; user-select:none;
}
.cat-pill:hover { border-color:rgba(200,169,110,.35); color:#c8a96e; background:rgba(200,169,110,.06); }
.cat-pill.active {
    background:rgba(200,169,110,.15); border-color:#c8a96e;
    color:#c8a96e; box-shadow:0 0 16px rgba(200,169,110,.12);
}
.cat-pill .pill-icon { font-size:1.1rem; }

/* ── Hint banner ── */
.hint-banner {
    background:rgba(200,169,110,.06); border:1px solid rgba(200,169,110,.15);
    border-radius:12px; padding:.85rem 1.2rem; margin-bottom:1.5rem;
    font-size:.82rem; color:#a08858; display:flex; align-items:center; gap:.6rem;
}

/* ── Upload card ── */
.upload-card {
    background:rgba(255,255,255,.03); border:1px solid rgba(200,169,110,.12);
    border-radius:18px; padding:1.8rem; height:100%; transition:border-color .3s;
}
.upload-card:hover { border-color:rgba(200,169,110,.28); }
.card-label { font-size:.7rem; font-weight:600; letter-spacing:.18em;
    text-transform:uppercase; color:#c8a96e; margin-bottom:.4rem; }
.card-title { font-family:'Playfair Display',serif; font-size:1.2rem;
    color:#f0ece4; margin-bottom:1.2rem; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border:1.5px dashed rgba(200,169,110,.2) !important;
    border-radius:12px !important; background:rgba(200,169,110,.03) !important;
    transition:all .3s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color:rgba(200,169,110,.45) !important;
    background:rgba(200,169,110,.06) !important;
}

/* ── Analysis badge ── */
.analysis-wrap {
    background:rgba(200,169,110,.07); border:1px solid rgba(200,169,110,.18);
    border-radius:14px; padding:1.2rem 1.4rem; margin-top:1rem;
}
.analysis-row { display:flex; gap:.6rem; align-items:center; flex-wrap:wrap; margin-bottom:.5rem; }
.a-badge { background:rgba(200,169,110,.15); color:#c8a96e; padding:.22rem .75rem;
    border-radius:20px; font-size:.72rem; font-weight:600; letter-spacing:.08em; text-transform:uppercase; }
.a-desc { font-size:.82rem; color:#aaa; line-height:1.5; }

/* ── Settings card ── */
.settings-card {
    background:rgba(255,255,255,.025); border:1px solid rgba(255,255,255,.06);
    border-radius:14px; padding:1.4rem; margin-top:1rem;
}
.settings-title { font-size:.72rem; letter-spacing:.15em; text-transform:uppercase; color:#666; margin-bottom:1rem; }

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    width:100%; padding:1rem 2rem; font-family:'Outfit',sans-serif;
    font-size:1rem; font-weight:600; letter-spacing:.12em; text-transform:uppercase;
    color:#0e0c0a; background:linear-gradient(120deg,#c8a96e 0%,#e8a84a 100%);
    border:none; border-radius:14px; cursor:pointer;
    transition:transform .2s,box-shadow .2s;
    box-shadow:0 4px 24px rgba(200,169,110,.22);
}
div[data-testid="stButton"] > button:hover {
    transform:translateY(-2px); box-shadow:0 10px 36px rgba(200,169,110,.38);
}
div[data-testid="stButton"] > button:disabled {
    background:rgba(255,255,255,.08) !important; color:#444 !important;
    cursor:not-allowed; transform:none !important; box-shadow:none !important;
}

/* ── Result ── */
.result-header { display:flex; align-items:center; gap:.75rem; margin-bottom:1.2rem; }
.result-dot { width:10px; height:10px; border-radius:50%; background:#4caf7d;
    box-shadow:0 0 8px rgba(76,175,125,.5); }
.result-title { font-family:'Playfair Display',serif; font-size:1.4rem; color:#f0ece4; }
.result-card {
    background:rgba(255,255,255,.03); border:1px solid rgba(76,175,125,.2);
    border-radius:18px; padding:1.8rem;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    width:100%; background:transparent !important;
    border:1.5px solid rgba(200,169,110,.35) !important; color:#c8a96e !important;
    border-radius:10px !important; font-weight:500 !important; letter-spacing:.06em;
    transition:all .2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background:rgba(200,169,110,.1) !important; border-color:#c8a96e !important;
    transform:translateY(-1px) !important;
}

/* ── Status ── */
[data-testid="stInfo"]    { background:rgba(200,169,110,.07)!important; border-left:3px solid #c8a96e!important; border-radius:10px!important; color:#c8a96e!important; }
[data-testid="stSuccess"] { background:rgba(76,175,125,.07)!important; border-left:3px solid #4caf7d!important; border-radius:10px!important; }
[data-testid="stError"]   { background:rgba(184,92,56,.07)!important; border-left:3px solid #b85c38!important; border-radius:10px!important; }
[data-testid="stWarning"] { background:rgba(200,169,110,.07)!important; border-left:3px solid #c8a96e!important; border-radius:10px!important; }

/* ── Progress steps ── */
.progress-steps { display:flex; gap:.5rem; align-items:center; margin:.75rem 0 1.5rem; }
.p-step { display:flex; align-items:center; gap:.4rem; font-size:.75rem;
    letter-spacing:.08em; text-transform:uppercase; }
.p-step .dot { width:8px; height:8px; border-radius:50%; }
.p-step.done .dot   { background:#4caf7d; }
.p-step.active .dot { background:#c8a96e; animation:pulse 1s infinite; }
.p-step.idle .dot   { background:#333; }
.p-step.done   { color:#4caf7d; }
.p-step.active { color:#c8a96e; }
.p-step.idle   { color:#444; }
.p-arrow { color:#333; font-size:.7rem; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

.divider { height:1px; background:linear-gradient(90deg,transparent,rgba(200,169,110,.2),transparent); margin:2rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Category config ────────────────────────────────────────────────────────────
CATEGORIES = [
    {
        "key": "tops",
        "label": "Tops",
        "icon": "👕",
        "hint": "Upload a T-shirt, shirt, blouse, or jacket image.",
        "upload_label": "Top / Upper Garment",
        "upload_hint": "T-shirt, shirt, blouse, jacket, hoodie …",
        "body_hint": "Upper body or full body photo works best.",
        "groq_prompt": "Describe this top/upper garment for virtual try-on. Focus on style, fit, and color.",
    },
    {
        "key": "bottoms",
        "label": "Bottoms",
        "icon": "👖",
        "hint": "Upload trousers, jeans, shorts, or a skirt image.",
        "upload_label": "Bottom / Lower Garment",
        "upload_hint": "Jeans, trousers, shorts, skirt, joggers …",
        "body_hint": "Full-body or lower-body photo works best.",
        "groq_prompt": "Describe this bottom/lower garment for virtual try-on. Include style, cut, and color.",
    },
    {
        "key": "shoes",
        "label": "Shoes",
        "icon": "👟",
        "hint": "Upload any footwear — sneakers, heels, boots, sandals.",
        "upload_label": "Footwear",
        "upload_hint": "Sneakers, heels, boots, sandals, loafers …",
        "body_hint": "Full-body photo showing feet works best.",
        "groq_prompt": "Describe this footwear for virtual try-on. Include shoe type, color, sole, and style.",
    },
    {
        "key": "dresses",
        "label": "Dresses",
        "icon": "👗",
        "hint": "Upload a dress, jumpsuit, or full-length outfit.",
        "upload_label": "Dress / Full Outfit",
        "upload_hint": "Dress, jumpsuit, co-ord, saree …",
        "body_hint": "Full-body photo works best for dresses.",
        "groq_prompt": "Describe this dress or full outfit for virtual try-on. Include length, silhouette, and fabric.",
    },
    {
        "key": "accessories",
        "label": "Accessories",
        "icon": "🧣",
        "hint": "Upload a scarf, hat, bag, or jewellery item.",
        "upload_label": "Accessory",
        "upload_hint": "Scarf, hat, bag, belt, jewellery …",
        "body_hint": "Upper-body or full-body photo works best.",
        "groq_prompt": "Describe this fashion accessory for virtual try-on. Be specific about type, color, and material.",
    },
]
CAT_KEYS = [c["key"] for c in CATEGORIES]
CAT_MAP  = {c["key"]: c for c in CATEGORIES}

# ── Session state ──────────────────────────────────────────────────────────────
if "selected_cat" not in st.session_state:
    st.session_state.selected_cat = "tops"
for key in ["analysis", "result_img", "step", "last_item_key"]:
    if key not in st.session_state:
        st.session_state[key] = None
if st.session_state.step is None:
    st.session_state.step = 0

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<a class="back-link" href="/">← Back to collection</a>', unsafe_allow_html=True)
st.markdown("""
<div class="page-header">
    <h1>Virtual <em>Try-On</em></h1>
    <p>Pick a category · Upload your photo · Let AI dress you &nbsp;·&nbsp; Free &nbsp;·&nbsp; No GPU needed</p>
</div>
""", unsafe_allow_html=True)

groq_key = os.environ.get("GROQ_API_KEY", "")
if not groq_key:
    st.warning("⚠️ **GROQ_API_KEY** not set. Add it to `.env`. Get a free key at [console.groq.com](https://console.groq.com).")

# ── Category selector ──────────────────────────────────────────────────────────
st.markdown('<div class="cat-selector-wrap">', unsafe_allow_html=True)
st.markdown('<div class="cat-selector-label">What do you want to try on?</div>', unsafe_allow_html=True)
st.markdown('<div class="cat-pills">', unsafe_allow_html=True)

# Render pills as buttons in columns
pill_cols = st.columns(len(CATEGORIES))
for i, cat in enumerate(CATEGORIES):
    with pill_cols[i]:
        is_active = st.session_state.selected_cat == cat["key"]
        label = f"{cat['icon']}  {cat['label']}"
        if st.button(
            label,
            key=f"cat_btn_{cat['key']}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            if st.session_state.selected_cat != cat["key"]:
                # Reset analysis & result when switching categories
                st.session_state.selected_cat = cat["key"]
                st.session_state.analysis = None
                st.session_state.result_img = None
                st.session_state.step = 0
                st.session_state.last_item_key = None
                st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

# ── Active category info ───────────────────────────────────────────────────────
active_cat = CAT_MAP[st.session_state.selected_cat]

st.markdown(f"""
<div class="hint-banner">
    <span style="font-size:1.2rem">{active_cat['icon']}</span>
    <span><strong>{active_cat['label']} Try-On</strong> — {active_cat['hint']}</span>
</div>
""", unsafe_allow_html=True)

# ── Progress ───────────────────────────────────────────────────────────────────
# ── Model info banner ─────────────────────────────────────────────────────────
MODEL_INFO = {
    "tops":        ("Nymbo/Virtual-Try-On · Upper-body", "🟢", "OOTDiffusion-based, upper-body region"),
    "bottoms":     ("Nymbo/Virtual-Try-On · Lower-body", "🟢", "OOTDiffusion-based, lower-body region — pants, shorts, skirts"),
    "dresses":     ("Nymbo/Virtual-Try-On · Dress",      "🟢", "OOTDiffusion-based, full-body — dresses, jumpsuits"),
    "shoes":       ("ShoeVTON",                          "🟡", "Dedicated shoe model — full-body photo with feet visible"),
    "accessories": ("Kolors Virtual Try-On",             "🟡", "Kwai-Kolors model — works best with upper-body photo"),
}
m_name, m_dot, m_tip = MODEL_INFO[st.session_state.selected_cat]
st.markdown(f"""
<div style="display:flex;align-items:center;gap:.6rem;margin-bottom:1.2rem;
    background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);
    border-radius:10px;padding:.65rem 1rem;font-size:.78rem;color:#888;">
    <span>{m_dot}</span>
    <span>Using <strong style="color:#c8a96e">{m_name}</strong> — {m_tip}</span>
</div>
""", unsafe_allow_html=True)

def step_class(target):
    s = st.session_state.step or 0
    if s > target:  return "done"
    if s == target: return "active"
    return "idle"

st.markdown(f"""
<div class="progress-steps">
    <div class="p-step {step_class(1)}"><div class="dot"></div>Analyze item</div>
    <div class="p-arrow">›</div>
    <div class="p-step {step_class(2)}"><div class="dot"></div>Generate try-on</div>
    <div class="p-arrow">›</div>
    <div class="p-step {step_class(3)}"><div class="dot"></div>Result ready</div>
</div>
""", unsafe_allow_html=True)

# ── Upload columns ─────────────────────────────────────────────────────────────
col_person, col_gap, col_item = st.columns([1, 0.06, 1])

# ── Person photo ───────────────────────────────────────────────────────────────
with col_person:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Step 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Your Photo</div>', unsafe_allow_html=True)

    person_file = st.file_uploader(
        active_cat["body_hint"],
        type=["jpg", "jpeg", "png", "webp"],
        key="person_img",
        label_visibility="visible",
    )

    if person_file:
        person_pil = Image.open(person_file).convert("RGB")
        st.image(person_pil, use_column_width=True)
        st.success(f"✓ Photo loaded — {person_pil.size[0]}×{person_pil.size[1]} px")
    else:
        st.info("Upload a clear photo of yourself.")

    st.markdown('</div>', unsafe_allow_html=True)

# ── Item upload ────────────────────────────────────────────────────────────────
with col_item:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Step 2</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card-title">{active_cat["icon"]} {active_cat["upload_label"]}</div>', unsafe_allow_html=True)

    item_file = st.file_uploader(
        active_cat["upload_hint"],
        type=["jpg", "jpeg", "png", "webp"],
        key=f"item_img_{st.session_state.selected_cat}",
        label_visibility="visible",
    )

    if item_file:
        item_pil = Image.open(item_file).convert("RGB")
        st.image(item_pil, use_column_width=True)
        st.success(f"✓ {active_cat['label']} loaded — {item_pil.size[0]}×{item_pil.size[1]} px")

        # ── Groq analysis (auto-triggers on new upload)
        item_key = f"{st.session_state.selected_cat}_{item_file.name}_{item_file.size}"
        if st.session_state.last_item_key != item_key:
            if groq_key:
                with st.spinner(f"🤖 Groq is analyzing your {active_cat['label'].lower()}…"):
                    try:
                        from backend.analyze_cloth import analyze_clothing
                        item_file.seek(0)
                        ext  = item_file.name.rsplit(".", 1)[-1].lower()
                        mime = f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"
                        analysis = analyze_clothing(
                            item_file.read(), mime,
                            custom_prompt=active_cat["groq_prompt"]
                        )
                        st.session_state.analysis     = analysis
                        st.session_state.last_item_key = item_key
                        if (st.session_state.step or 0) < 1:
                            st.session_state.step = 1
                    except Exception as e:
                        st.error(f"Groq analysis failed: {e}")
                        st.session_state.analysis = {
                            "description": f"{active_cat['label']} item",
                            "category": active_cat["key"], "color": "unknown",
                            "fit": "regular", "fabric": "unknown",
                            "prompt": f"{active_cat['label']} for virtual try-on",
                        }
                        st.session_state.last_item_key = item_key
            else:
                st.session_state.analysis = {
                    "description": f"{active_cat['label']} item (add GROQ_API_KEY for AI analysis)",
                    "category": active_cat["key"], "color": "—", "fit": "—",
                    "fabric": "—", "prompt": f"{active_cat['label']} for virtual try-on",
                }
                st.session_state.last_item_key = item_key

        # Show analysis
        if st.session_state.analysis:
            a = st.session_state.analysis
            st.markdown(f"""
            <div class="analysis-wrap">
                <div class="analysis-row">
                    <span class="a-badge">{active_cat['icon']} {a.get('category', active_cat['key'])}</span>
                    <span class="a-badge">{a.get('color','—')}</span>
                    <span class="a-badge">{a.get('fit','—')}</span>
                    <span class="a-badge">{a.get('fabric','—')}</span>
                </div>
                <div class="a-desc">🤖 <strong>Groq:</strong> {a.get('description','—')}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"Upload the {active_cat['label'].lower()} you want to try on.")

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
            "Denoising steps", min_value=20, max_value=50, value=30, step=5,
            help="Higher = better quality but slower.",
        )
    with s2:
        seed = st.number_input(
            "Seed", min_value=0, max_value=9999, value=42, step=1,
            help="Change for a different result variation.",
        )
    st.markdown('</div>', unsafe_allow_html=True)

with btn_col:
    st.markdown("<br>", unsafe_allow_html=True)
    both_ready = person_file is not None and item_file is not None
    generate_btn = st.button(
        f"✦ Try On {active_cat['icon']}",
        disabled=not both_ready,
        use_container_width=True,
        key="generate",
    )
    if not both_ready:
        st.caption("Upload both images above to enable.")

# ── Generation ─────────────────────────────────────────────────────────────────
if generate_btn and both_ready:
    st.session_state.result_img = None
    st.session_state.step = 2
    cloth_desc = (st.session_state.analysis or {}).get(
        "prompt", f"{active_cat['label']} for virtual try-on"
    )

    with st.spinner(f"🔄 Generating {active_cat['label'].lower()} try-on via IDM-VTON…"):
        try:
            from backend.generate import run_tryon, pil_to_bytes
            person_file.seek(0)
            item_file.seek(0)
            result_img = run_tryon(
                person_image=Image.open(person_file).convert("RGB"),
                cloth_image=Image.open(item_file).convert("RGB"),
                cloth_description=cloth_desc,
                category=st.session_state.selected_cat,
                denoise_steps=denoise_steps,
                seed=int(seed),
            )
            st.session_state.result_img = result_img
            st.session_state.step = 3

        except Exception as e:
            err = str(e)
            st.session_state.step = 0

            if "quota" in err.lower() or "zerogpu" in err.lower():
                # Extract wait time if present
                import re
                wait = re.search(r"Try again in (\d+:\d+:\d+)", err)
                wait_str = f" Try again in **{wait.group(1)}**." if wait else ""
                st.error("⏱️ **HuggingFace ZeroGPU quota exceeded.**" + wait_str)
                st.markdown("""
<div style="background:rgba(200,169,110,.07);border:1px solid rgba(200,169,110,.2);
border-radius:12px;padding:1.2rem 1.4rem;margin-top:.5rem;font-size:.88rem;line-height:1.8;">
<strong style="color:#c8a96e">Fix options (pick any):</strong><br>
① <strong>Add HF token</strong> to your <code>.env</code> → <code>HF_TOKEN=xxx</code>
  &nbsp;→ get free token at <a href="https://huggingface.co/settings/tokens" target="_blank">huggingface.co/settings/tokens</a><br>
② <strong>Wait</strong> for quota to reset (resets every 24 hours)<br>
③ <strong>Lower denoising steps</strong> to 20 (uses less GPU time per run)<br>
④ <strong>Use a different Space</strong> by changing seed and retrying
</div>
                """, unsafe_allow_html=True)
            elif "gradio_client" in err.lower() or "modulenotfounderror" in err.lower():
                st.error("📦 Missing dependency.")
                st.code("pip install gradio_client", language="bash")
            else:
                st.error(f"❌ Generation failed: {err}")
                st.info("The HuggingFace Space may be temporarily down. Try again in a moment.")


# ── Result ─────────────────────────────────────────────────────────────────────
if st.session_state.result_img is not None:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-header">
        <div class="result-dot"></div>
        <div class="result-title">{active_cat['icon']} {active_cat['label']} Try-On Result</div>
    </div>
    """, unsafe_allow_html=True)

    res_img = st.session_state.result_img
    _, rc2, _ = st.columns([1, 2, 1])

    with rc2:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        cmp1, cmp2 = st.columns(2)
        with cmp1:
            st.caption("Original")
            person_file.seek(0)
            st.image(Image.open(person_file), use_column_width=True)
        with cmp2:
            st.caption(f"✨ With {active_cat['label'].lower()}")
            st.image(res_img, use_column_width=True)

        from backend.generate import pil_to_bytes
        st.download_button(
            "⬇  Download Result (PNG)",
            data=pil_to_bytes(res_img, fmt="PNG"),
            file_name=f"fitai_{active_cat['key']}_tryon.png",
            mime="image/png",
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, ta_col, _ = st.columns([1, 2, 1])
    with ta_col:
        if st.button("↺  Try Another Item", use_container_width=True):
            st.session_state.result_img  = None
            st.session_state.analysis    = None
            st.session_state.step        = 0
            st.session_state.last_item_key = None
            st.rerun()

# ── Debug log viewer ───────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
with st.expander("🛠️ Debug Logs — click to inspect what the AI is doing", expanded=False):
    log_col1, log_col2 = st.columns([3, 1])
    with log_col2:
        if st.button("🔄 Refresh logs", use_container_width=True):
            st.rerun()
        if st.button("🗑️ Clear logs", use_container_width=True):
            open("fitai_debug.log", "w").close()
            st.rerun()

    with log_col1:
        try:
            with open("fitai_debug.log", "r", encoding="utf-8") as f:
                lines = f.readlines()

            if lines:
                # Color-code log lines
                colored = []
                for line in lines[-80:]:  # last 80 lines
                    line = line.rstrip()
                    if "ERROR" in line:
                        colored.append(f"🔴 {line}")
                    elif "WARNING" in line or "FAILED" in line:
                        colored.append(f"🟡 {line}")
                    elif "SUCCESS" in line or "COMPLETE" in line:
                        colored.append(f"🟢 {line}")
                    elif "TRY-ON REQUEST" in line or "MODEL SELECTED" in line:
                        colored.append(f"🔵 {line}")
                    else:
                        colored.append(f"   {line}")

                st.code("\n".join(colored), language=None)

                # Summary box
                categories_logged = [l for l in lines if "Category" in l]
                models_logged     = [l for l in lines if "MODEL SELECTED" in l]
                errors_logged     = [l for l in lines if "ERROR" in l]

                if categories_logged:
                    last_cat = categories_logged[-1].strip().split(":")[-1].strip()
                    st.info(f"**Last category sent:** `{last_cat}`")
                if models_logged:
                    last_model = models_logged[-1].strip()
                    st.info(f"**Last model used:** `{last_model.split('|')[0].split(':')[-1].strip()}`")
                if errors_logged:
                    st.error(f"**{len(errors_logged)} error(s) found** — check logs above")
            else:
                st.info("No logs yet — generate a try-on first.")

        except FileNotFoundError:
            st.info("No log file yet — generate a try-on to start logging.")