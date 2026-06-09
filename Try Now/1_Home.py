# """
# 1_Home.py
# Main entry point for FitAI multi-page app.
# set_page_config() lives HERE ONLY — never in child pages.
# """
# import streamlit as st

# # ── Must be FIRST Streamlit call, in the main file only ───────────────────────
# st.set_page_config(
#     page_title="FitAI · Virtual Try-On",
#     page_icon="👗",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# st.markdown("""
# <style>
# #MainMenu, footer, header { visibility: hidden; }
# [data-testid="stDecoration"] { display: none; }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("# 👗 FitAI")
# st.markdown("### AI-Powered Virtual Try-On")
# st.markdown("---")
# st.markdown("Welcome to **FitAI** — virtually try on tops, bottoms, shoes, dresses and accessories.")

# if st.button("✨ Go to Virtual Try-On"):
#     st.switch_page("pages/2_Try_On.py")
"""
1_Home.py
Landing page for FitAI — converted from index.html into Streamlit.
set_page_config() lives HERE ONLY.
"""
import streamlit as st

st.set_page_config(
    page_title="FitAI · Virtual Try-On",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Route to try-on page if button was clicked ─────────────────────────────────
if st.session_state.get("goto_tryon"):
    st.session_state.goto_tryon = False
    st.switch_page("pages/2_Try_On.py")

# ── Inject full landing page HTML ──────────────────────────────────────────────
st.markdown("""
<style>
/* Hide all Streamlit chrome so it looks like a pure website */
#MainMenu, footer, header, [data-testid="stDecoration"],
[data-testid="stToolbar"], [data-testid="stSidebarNav"] { display:none !important; visibility:hidden !important; }
[data-testid="stAppViewContainer"] { padding:0 !important; }
[data-testid="block-container"] { padding:0 !important; max-width:100% !important; }
.stButton { display:none; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  :root{
    --cream:#faf7f2;--ink:#1a1714;--warm:#c8a96e;--warm-light:#e8d9bb;
    --rust:#b85c38;--sage:#4a6741;--slate:#2d3748;
    --card-bg:#ffffff;--muted:#6b6560;
  }
  html{scroll-behavior:smooth}
  body{font-family:'Outfit',sans-serif;background:var(--cream);color:var(--ink);overflow-x:hidden}

  nav{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:1rem 3rem;background:rgba(250,247,242,.92);backdrop-filter:blur(12px);border-bottom:1px solid rgba(200,169,110,.2)}
  .nav-logo{font-family:'Playfair Display',serif;font-size:1.6rem;color:var(--ink);letter-spacing:.04em}
  .nav-logo span{color:var(--warm)}
  .nav-links{display:flex;gap:2rem;list-style:none}
  .nav-links a{text-decoration:none;color:var(--muted);font-size:.85rem;letter-spacing:.1em;text-transform:uppercase;font-weight:500;transition:color .2s}
  .nav-links a:hover{color:var(--warm)}
  .nav-cta{background:var(--ink);color:var(--cream);padding:.55rem 1.4rem;border-radius:40px;font-size:.82rem;font-weight:500;letter-spacing:.08em;text-decoration:none;text-transform:uppercase;transition:background .2s;cursor:pointer;border:none;font-family:'Outfit',sans-serif}
  .nav-cta:hover{background:var(--warm)}

  .hero{min-height:100vh;display:grid;grid-template-columns:1fr 1fr;align-items:center;padding:8rem 3rem 4rem;gap:4rem;position:relative;overflow:hidden}
  .hero::before{content:'';position:absolute;top:-20%;right:-10%;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(200,169,110,.12) 0%,transparent 70%);pointer-events:none}
  .hero-badge{display:inline-flex;align-items:center;gap:.5rem;background:var(--warm-light);color:var(--rust);padding:.35rem 1rem;border-radius:40px;font-size:.75rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin-bottom:1.5rem}
  .hero-badge::before{content:'✦';font-size:.6rem}
  .hero h1{font-family:'Playfair Display',serif;font-size:clamp(2.8rem,5vw,4.2rem);line-height:1.1;margin-bottom:1.5rem;color:var(--ink)}
  .hero h1 em{font-style:italic;color:var(--warm)}
  .hero p{color:var(--muted);font-size:1.05rem;line-height:1.7;max-width:480px;margin-bottom:2.5rem;font-weight:300}
  .hero-btns{display:flex;gap:1rem;flex-wrap:wrap}
  .btn-primary{background:var(--ink);color:var(--cream);padding:.8rem 2rem;border-radius:40px;font-size:.9rem;font-weight:500;text-decoration:none;letter-spacing:.06em;transition:all .25s;cursor:pointer;border:none;font-family:'Outfit',sans-serif}
  .btn-primary:hover{background:var(--warm);transform:translateY(-2px)}
  .btn-outline{background:transparent;color:var(--ink);padding:.8rem 2rem;border-radius:40px;font-size:.9rem;font-weight:500;text-decoration:none;letter-spacing:.06em;border:1.5px solid rgba(26,23,20,.25);transition:all .25s}
  .btn-outline:hover{border-color:var(--warm);color:var(--warm)}
  .hero-visual{position:relative;height:540px}
  .hero-img-grid{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:16px;height:100%}
  .h-card{border-radius:20px;overflow:hidden;position:relative}
  .h-card:nth-child(1){border-radius:20px 20px 4px 20px;background:linear-gradient(135deg,#dde8d8,#c5d9be)}
  .h-card:nth-child(2){border-radius:20px 20px 20px 4px;margin-top:40px;background:linear-gradient(135deg,#e8ddd0,#d4c5b0)}
  .h-card:nth-child(3){border-radius:4px 20px 20px 20px;margin-top:-40px;background:linear-gradient(135deg,#d8dde8,#b0c5d4)}
  .h-card:nth-child(4){border-radius:20px 4px 20px 20px;background:linear-gradient(135deg,#e8d8dd,#d4b0be)}
  .h-card-inner{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1rem;gap:.5rem}
  .h-icon{font-size:2.5rem}
  .h-label{font-size:.75rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:rgba(26,23,20,.5)}
  .hero-stats{display:flex;gap:2rem;margin-top:2.5rem}
  .stat{text-align:center}
  .stat-num{font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:var(--ink)}
  .stat-label{font-size:.72rem;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;margin-top:.1rem}

  section{padding:6rem 3rem}
  .section-tag{display:inline-block;font-size:.72rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--warm);margin-bottom:.75rem}
  .section-title{font-family:'Playfair Display',serif;font-size:clamp(2rem,3.5vw,2.8rem);line-height:1.2;margin-bottom:1rem;color:var(--ink)}
  .section-title em{font-style:italic;color:var(--warm)}
  .section-sub{color:var(--muted);font-size:1rem;line-height:1.7;max-width:540px;font-weight:300}

  .products-header{text-align:center;margin-bottom:4rem}
  .products-header .section-sub{margin:0 auto}
  .cat-tabs{display:flex;gap:.5rem;justify-content:center;margin-bottom:3rem;flex-wrap:wrap}
  .cat-tab{padding:.5rem 1.4rem;border-radius:40px;font-size:.82rem;font-weight:500;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;border:1.5px solid rgba(26,23,20,.15);background:transparent;color:var(--muted);transition:all .2s}
  .cat-tab.active,.cat-tab:hover{background:var(--ink);color:var(--cream);border-color:var(--ink)}
  .grid-items{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.5rem}
  .product-item{display:none}
  .product-item.visible{display:block}
  .product-card{background:var(--card-bg);border-radius:18px;overflow:hidden;border:1px solid rgba(200,169,110,.15);transition:transform .25s,box-shadow .25s;cursor:pointer}
  .product-card:hover{transform:translateY(-6px);box-shadow:0 20px 50px rgba(26,23,20,.1)}
  .product-thumb{height:240px;display:flex;align-items:center;justify-content:center;font-size:5rem;position:relative}
  .product-thumb.green{background:linear-gradient(135deg,#dde8d8,#c5d9be)}
  .product-thumb.sand{background:linear-gradient(135deg,#e8e0d0,#d4c8b0)}
  .product-thumb.blue{background:linear-gradient(135deg,#d8dde8,#b0c5d4)}
  .product-thumb.blush{background:linear-gradient(135deg,#e8d8dd,#d4b0be)}
  .product-thumb.charcoal{background:linear-gradient(135deg,#d5d5d5,#b8b8b8)}
  .product-thumb.amber{background:linear-gradient(135deg,#e8e0c8,#d4c8a0)}
  .product-badge{position:absolute;top:12px;left:12px;background:var(--rust);color:#fff;padding:.25rem .75rem;border-radius:20px;font-size:.68rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
  .product-info{padding:1.2rem}
  .product-name{font-weight:500;font-size:.95rem;margin-bottom:.3rem;color:var(--ink)}
  .product-meta{font-size:.8rem;color:var(--muted)}
  .product-price{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--ink);margin-top:.5rem}

  .men-section{background:var(--ink);color:var(--cream)}
  .men-section .section-tag{color:var(--warm)}
  .men-section .section-title{color:var(--cream)}
  .men-section .section-title em{color:var(--warm)}
  .men-section .section-sub{color:rgba(250,247,242,.6)}
  .men-layout{display:grid;grid-template-columns:1fr 1.5fr;gap:5rem;align-items:center}
  .men-products{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
  .men-card{background:rgba(255,255,255,.05);border:1px solid rgba(200,169,110,.2);border-radius:16px;padding:1.5rem;transition:all .25s;cursor:pointer}
  .men-card:hover{background:rgba(200,169,110,.1);border-color:var(--warm);transform:translateY(-3px)}
  .men-icon{font-size:2.5rem;margin-bottom:.75rem}
  .men-name{font-weight:500;font-size:.92rem;color:var(--cream);margin-bottom:.25rem}
  .men-price{font-size:.82rem;color:var(--warm);font-weight:600}
  .men-featured{border-radius:24px;overflow:hidden;height:420px;background:linear-gradient(135deg,#2a3528,#1e2b1c);display:flex;align-items:center;justify-content:center;font-size:8rem;position:relative}
  .men-featured-label{position:absolute;bottom:20px;left:20px;right:20px;background:rgba(26,23,20,.8);border-radius:12px;padding:1rem;backdrop-filter:blur(8px)}
  .men-featured-label h3{font-family:'Playfair Display',serif;color:var(--cream);margin-bottom:.25rem;font-size:1.1rem}
  .men-featured-label p{font-size:.8rem;color:rgba(250,247,242,.6)}

  .tryon-section{background:linear-gradient(135deg,#1a1714 0%,#2d2520 50%,#1a1714 100%);position:relative;overflow:hidden;text-align:center}
  .tryon-section::before{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:800px;height:800px;border-radius:50%;background:radial-gradient(circle,rgba(200,169,110,.08) 0%,transparent 70%);pointer-events:none}
  .tryon-section .section-tag{color:var(--warm)}
  .tryon-section .section-title{color:var(--cream);margin:0 auto 1rem;max-width:700px}
  .tryon-section .section-sub{color:rgba(250,247,242,.55);margin:0 auto 3rem;max-width:520px}
  .tryon-showcase{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;max-width:700px;margin:0 auto 3.5rem;position:relative;z-index:1}
  .tryon-card{border-radius:20px;overflow:hidden;border:1px solid rgba(200,169,110,.15);background:rgba(255,255,255,.04);transition:all .3s}
  .tryon-card:hover{border-color:var(--warm);background:rgba(200,169,110,.08);transform:scale(1.03)}
  .tryon-thumb{height:180px;display:flex;align-items:center;justify-content:center;font-size:4rem}
  .tryon-thumb.t1{background:linear-gradient(135deg,#2a3528,#1e2b1c)}
  .tryon-thumb.t2{background:linear-gradient(135deg,#2a2420,#1e1a16)}
  .tryon-thumb.t3{background:linear-gradient(135deg,#1e2a2a,#141e1e)}
  .tryon-info{padding:1rem;text-align:left}
  .tryon-info p{font-size:.82rem;font-weight:500;color:rgba(250,247,242,.8);margin-bottom:.2rem}
  .tryon-info span{font-size:.72rem;color:var(--warm);text-transform:uppercase;letter-spacing:.08em}
  .tryon-cta-wrap{position:relative;z-index:1}
  .btn-tryon{display:inline-flex;align-items:center;gap:.75rem;background:linear-gradient(120deg,var(--warm),#e8a84a);color:var(--ink);padding:1.1rem 2.8rem;border-radius:60px;font-size:1rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;border:none;transition:all .3s;box-shadow:0 8px 30px rgba(200,169,110,.3);font-family:'Outfit',sans-serif}
  .btn-tryon:hover{transform:translateY(-3px) scale(1.03);box-shadow:0 16px 50px rgba(200,169,110,.45)}
  .btn-tryon-arrow{font-size:1.3rem;transition:transform .25s}
  .btn-tryon:hover .btn-tryon-arrow{transform:translateX(5px)}
  .tryon-note{margin-top:1.2rem;font-size:.78rem;color:rgba(250,247,242,.35);letter-spacing:.06em;text-transform:uppercase}

  .how-section{background:var(--cream)}
  .how-section .section-title,.how-section .section-sub{text-align:center;margin-left:auto;margin-right:auto}
  .how-section .section-sub{margin-bottom:4rem}
  .steps{display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;position:relative}
  .steps::before{content:'';position:absolute;top:40px;left:12.5%;right:12.5%;height:1px;background:linear-gradient(90deg,transparent,var(--warm-light),var(--warm-light),transparent);z-index:0}
  .step-item{text-align:center;position:relative;z-index:1}
  .step-num{width:80px;height:80px;border-radius:50%;background:var(--card-bg);border:2px solid var(--warm-light);display:flex;align-items:center;justify-content:center;margin:0 auto 1.2rem;font-size:2rem;box-shadow:0 4px 20px rgba(200,169,110,.15)}
  .step-title{font-weight:600;font-size:.9rem;letter-spacing:.05em;color:var(--ink);margin-bottom:.5rem;text-transform:uppercase}
  .step-desc{font-size:.83rem;color:var(--muted);line-height:1.6;font-weight:300}

  footer{background:var(--ink);color:rgba(250,247,242,.5);padding:3rem;text-align:center;font-size:.8rem;letter-spacing:.06em;text-transform:uppercase}
  footer strong{color:var(--warm)}
</style>
</head>
<body>

<nav>
  <div class="nav-logo">Fit<span>AI</span></div>
  <ul class="nav-links">
    <li><a href="#products">Collections</a></li>
    <li><a href="#men">Men</a></li>
    <li><a href="#tryon">Try-On</a></li>
    <li><a href="#how">How it works</a></li>
  </ul>
  <button class="nav-cta" onclick="goToTryOn()">Try it free</button>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-left">
    <div class="hero-badge">AI-Powered Fashion</div>
    <h1>Wear it before<br>you <em>buy it.</em></h1>
    <p>Browse hundreds of styles, accessories, and outfits — then virtually try them on using your own photo. Powered by open-source AI.</p>
    <div class="hero-btns">
      <button class="btn-primary" onclick="goToTryOn()">Try it now — free</button>
      <a href="#products" class="btn-outline">Browse collection</a>
    </div>
    <div class="hero-stats">
      <div class="stat"><div class="stat-num">500+</div><div class="stat-label">Styles</div></div>
      <div class="stat"><div class="stat-num">12k+</div><div class="stat-label">Try-ons daily</div></div>
      <div class="stat"><div class="stat-num">Free</div><div class="stat-label">Always</div></div>
    </div>
  </div>
  <div class="hero-visual">
    <div class="hero-img-grid">
      <div class="h-card"><div class="h-card-inner"><div class="h-icon">👗</div><div class="h-label">Dresses</div></div></div>
      <div class="h-card"><div class="h-card-inner"><div class="h-icon">👜</div><div class="h-label">Bags</div></div></div>
      <div class="h-card"><div class="h-card-inner"><div class="h-icon">👟</div><div class="h-label">Footwear</div></div></div>
      <div class="h-card"><div class="h-card-inner"><div class="h-icon">💍</div><div class="h-label">Jewelry</div></div></div>
    </div>
  </div>
</section>

<!-- PRODUCTS -->
<section id="products" style="background:#fff;padding:6rem 3rem">
  <div class="products-header">
    <div class="section-tag">Collections</div>
    <h2 class="section-title">Shop the <em>lookbook</em></h2>
    <p class="section-sub">From everyday staples to statement pieces — all virtually try-onable.</p>
  </div>
  <div class="cat-tabs">
    <button class="cat-tab active" onclick="filterCat('all',this)">All</button>
    <button class="cat-tab" onclick="filterCat('clothing',this)">Clothing</button>
    <button class="cat-tab" onclick="filterCat('accessories',this)">Accessories</button>
    <button class="cat-tab" onclick="filterCat('footwear',this)">Footwear</button>
    <button class="cat-tab" onclick="filterCat('bags',this)">Bags</button>
  </div>
  <div class="grid-items" id="productGrid">
    <div class="product-item visible" data-cat="clothing"><div class="product-card"><div class="product-thumb green"><span>🧥</span><span class="product-badge">New</span></div><div class="product-info"><div class="product-name">Linen Blazer</div><div class="product-meta">Sage · Relaxed fit</div><div class="product-price">Rs. 8,500</div></div></div></div>
    <div class="product-item visible" data-cat="accessories"><div class="product-card"><div class="product-thumb amber"><span>👒</span></div><div class="product-info"><div class="product-name">Straw Sun Hat</div><div class="product-meta">Natural · One size</div><div class="product-price">Rs. 3,200</div></div></div></div>
    <div class="product-item visible" data-cat="clothing"><div class="product-card"><div class="product-thumb blush"><span>👗</span><span class="product-badge">Hot</span></div><div class="product-info"><div class="product-name">Midi Floral Dress</div><div class="product-meta">Blush · Regular</div><div class="product-price">Rs. 6,900</div></div></div></div>
    <div class="product-item visible" data-cat="footwear"><div class="product-card"><div class="product-thumb charcoal"><span>👟</span></div><div class="product-info"><div class="product-name">Minimal Sneakers</div><div class="product-meta">White/Grey · Unisex</div><div class="product-price">Rs. 12,000</div></div></div></div>
    <div class="product-item visible" data-cat="bags"><div class="product-card"><div class="product-thumb sand"><span>👜</span></div><div class="product-info"><div class="product-name">Structured Tote</div><div class="product-meta">Camel · Leather</div><div class="product-price">Rs. 18,500</div></div></div></div>
    <div class="product-item visible" data-cat="accessories"><div class="product-card"><div class="product-thumb blue"><span>💍</span><span class="product-badge">Sale</span></div><div class="product-info"><div class="product-name">Pearl Ring Set</div><div class="product-meta">Silver · Adjustable</div><div class="product-price">Rs. 2,800</div></div></div></div>
    <div class="product-item visible" data-cat="clothing"><div class="product-card"><div class="product-thumb blue"><span>👔</span></div><div class="product-info"><div class="product-name">Oxford Shirt</div><div class="product-meta">Sky blue · Slim fit</div><div class="product-price">Rs. 5,500</div></div></div></div>
    <div class="product-item visible" data-cat="footwear"><div class="product-card"><div class="product-thumb blush"><span>👠</span></div><div class="product-info"><div class="product-name">Block Heel Mule</div><div class="product-meta">Blush · Comfort sole</div><div class="product-price">Rs. 9,200</div></div></div></div>
  </div>
</section>

<!-- MEN ACCESSORIES -->
<section id="men" class="men-section" style="padding:6rem 3rem">
  <div class="men-layout">
    <div>
      <div class="section-tag">Men's Edit</div>
      <h2 class="section-title">Sharp <em>accessories</em><br>for every occasion</h2>
      <p class="section-sub" style="margin-bottom:2.5rem">From boardroom to weekend — curated accessories that complete any look.</p>
      <div class="men-products">
        <div class="men-card"><div class="men-icon">⌚</div><div class="men-name">Classic Timepiece</div><div class="men-price">Rs. 45,000</div></div>
        <div class="men-card"><div class="men-icon">👓</div><div class="men-name">Aviator Frames</div><div class="men-price">Rs. 7,500</div></div>
        <div class="men-card"><div class="men-icon">🎩</div><div class="men-name">Wool Fedora</div><div class="men-price">Rs. 6,800</div></div>
        <div class="men-card"><div class="men-icon">💼</div><div class="men-name">Leather Briefcase</div><div class="men-price">Rs. 32,000</div></div>
        <div class="men-card"><div class="men-icon">🧣</div><div class="men-name">Cashmere Scarf</div><div class="men-price">Rs. 8,200</div></div>
        <div class="men-card"><div class="men-icon">👞</div><div class="men-name">Derby Oxfords</div><div class="men-price">Rs. 22,000</div></div>
      </div>
    </div>
    <div class="men-featured"><span>🧥</span>
      <div class="men-featured-label"><h3>Merino Overcoat</h3><p>Charcoal · Tailored cut · Winter collection</p></div>
    </div>
  </div>
</section>

<!-- TRY-ON CTA -->
<section id="tryon" class="tryon-section" style="padding:7rem 3rem">
  <div class="section-tag">✦ AI Virtual Try-On</div>
  <h2 class="section-title">See it on <em>you.</em><br>Before you decide.</h2>
  <p class="section-sub">Upload your photo, pick any item from our collection, and our AI will show you exactly how it looks — in seconds.</p>
  <div class="tryon-showcase">
    <div class="tryon-card"><div class="tryon-thumb t1"><span>🧥</span></div><div class="tryon-info"><p>Linen Blazer</p><span>Try it on →</span></div></div>
    <div class="tryon-card"><div class="tryon-thumb t2"><span>👗</span></div><div class="tryon-info"><p>Midi Dress</p><span>Try it on →</span></div></div>
    <div class="tryon-card"><div class="tryon-thumb t3"><span>🧣</span></div><div class="tryon-info"><p>Cashmere Scarf</p><span>Try it on →</span></div></div>
  </div>
  <div class="tryon-cta-wrap">
    <button class="btn-tryon" onclick="goToTryOn()">
      Try it on yourself <span class="btn-tryon-arrow">→</span>
    </button>
    <p class="tryon-note">No account needed · Free · Powered by open-source AI</p>
  </div>
</section>

<!-- HOW IT WORKS -->
<section id="how" class="how-section">
  <div class="section-tag" style="display:block;text-align:center">How it works</div>
  <h2 class="section-title">From browse to <em>virtually dressed</em> in 4 steps</h2>
  <p class="section-sub">Powered by Groq + Nymbo/Virtual-Try-On. No GPU required.</p>
  <div class="steps">
    <div class="step-item"><div class="step-num">📸</div><div class="step-title">Upload Photo</div><div class="step-desc">A full-body shot gives the best results — any background works.</div></div>
    <div class="step-item"><div class="step-num">👗</div><div class="step-title">Pick Category</div><div class="step-desc">Choose tops, bottoms, shoes, dresses, or accessories.</div></div>
    <div class="step-item"><div class="step-num">🤖</div><div class="step-title">AI Processes</div><div class="step-desc">Groq analyzes the garment, the right model composites it onto your photo.</div></div>
    <div class="step-item"><div class="step-num">✨</div><div class="step-title">See & Download</div><div class="step-desc">View the result instantly and download or share your try-on image.</div></div>
  </div>
</section>

<footer>Built with <strong>Streamlit · Groq · OOTDiffusion · IDM-VTON</strong> — 100% open source</footer>

<script>
function filterCat(cat, btn) {
  document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.product-item').forEach(item => {
    if (cat === 'all' || item.dataset.cat === cat) {
      item.classList.add('visible');
    } else {
      item.classList.remove('visible');
    }
  });
}

function goToTryOn() {
  // Post message to Streamlit to trigger page switch
  window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
}
</script>
</body>
</html>
""", unsafe_allow_html=True)

# ── Hidden Streamlit button triggered by JS postMessage ───────────────────────
# Streamlit can't directly receive JS postMessage, so we use a form + query param approach
st.markdown("""
<style>
.tryon-form { position:fixed; bottom:20px; right:20px; z-index:9999; }
.tryon-form button {
  background: linear-gradient(120deg,#c8a96e,#e8a84a);
  color: #1a1714; border: none; border-radius: 40px;
  padding: .7rem 1.6rem; font-size:.85rem; font-weight:600;
  letter-spacing:.08em; text-transform:uppercase; cursor:pointer;
  box-shadow: 0 4px 20px rgba(200,169,110,.35);
  font-family:'Outfit',sans-serif;
}
</style>
""", unsafe_allow_html=True)

# Floating "Go to Try-On" button using native Streamlit (always works)
with st.container():
    st.markdown('<div style="position:fixed;bottom:24px;right:24px;z-index:9999">', unsafe_allow_html=True)
    if st.button("✨ Open Try-On", key="floating_tryon"):
        st.switch_page("pages/2_Try_On.py")
    st.markdown('</div>', unsafe_allow_html=True)