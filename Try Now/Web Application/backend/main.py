"""
FitAI Backend — main.py
FastAPI server for upper-body virtual try-on using IDM-VTON.

Endpoints:
    GET  /api/health           — health check
    GET  /api/products         — list all products with image URLs
    POST /api/tryon            — run try-on by product_id (no file upload needed)
    POST /api/tryon/upload     — run try-on with custom garment upload
    GET  /api/result/{id}      — fetch a previously generated result
"""

import os
import uuid
import time
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from dotenv import load_dotenv
load_dotenv()

from tryon import run_upper_body_tryon, TryOnResult
from store import ResultStore
from products import PRODUCTS, get_product_by_id

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent
PRODUCTS_DIR = BASE_DIR / "static" / "products"
PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("fitai")

# ── App lifespan ───────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FitAI backend starting...")
    logger.info(f"  HF_TOKEN    : {'SET ✓' if os.environ.get('HF_TOKEN')    else 'NOT SET ✗'}")
    logger.info(f"  GROQ_API_KEY: {'SET ✓' if os.environ.get('GROQ_API_KEY') else 'NOT SET ✗'}")

    # Check product images exist
    missing = [p["img_file"] for p in PRODUCTS if not (PRODUCTS_DIR / p["img_file"]).exists()]
    if missing:
        logger.warning(f"  Missing product images: {missing}")
        logger.warning("  Run: python download_products.py")
    else:
        logger.info(f"  Product images: {len(PRODUCTS)} found ✓")
    yield
    logger.info("FitAI backend stopped.")

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="FitAI API",
    description="Upper-body virtual try-on powered by IDM-VTON",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Serve static product images at /static/products/<filename> ─────────────────
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# ── Result store ───────────────────────────────────────────────────────────────
store = ResultStore()


# ─────────────────────────────────────────────────────────────────────────────
# HEALTH
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    missing = [p["img_file"] for p in PRODUCTS if not (PRODUCTS_DIR / p["img_file"]).exists()]
    return {
        "status":          "ok",
        "model":           "yisol/IDM-VTON",
        "hf_token":        bool(os.environ.get("HF_TOKEN")),
        "groq_key":        bool(os.environ.get("GROQ_API_KEY")),
        "products_total":  len(PRODUCTS),
        "images_missing":  missing,
    }


# ─────────────────────────────────────────────────────────────────────────────
# PRODUCTS LIST
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/products")
def get_products():
    """Return all products with their local image URLs."""
    result = []
    for p in PRODUCTS:
        img_path = PRODUCTS_DIR / p["img_file"]
        result.append({
            **p,
            "img_url": f"/static/products/{p['img_file']}",
            "img_exists": img_path.exists(),
        })
    return JSONResponse(result)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN TRY-ON — by product_id (uses local saved image)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/tryon")
async def tryon_by_product(
    person_image: UploadFile = File(..., description="Person photo (JPG/PNG/WEBP)"),
    product_id:   str        = Form(..., description="Product ID from /api/products"),
    denoise_steps: int       = Form(30),
    seed:          int       = Form(42),
):
    """
    Run upper-body try-on using a saved local product image.
    Frontend sends: person photo file + product_id string.
    Backend looks up the local garment image from static/products/.
    """

    # ── Validate person image ────────────────────────────────────────────────
    allowed_types = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
    ct = (person_image.content_type or "").lower()
    if ct not in allowed_types:
        raise HTTPException(400, f"person_image must be JPG/PNG/WEBP, got '{ct}'")

    # ── Look up product ──────────────────────────────────────────────────────
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(404, f"Product '{product_id}' not found. Check /api/products")

    garment_path = PRODUCTS_DIR / product["img_file"]
    if not garment_path.exists():
        raise HTTPException(
            404,
            f"Garment image not found: {product['img_file']}. "
            f"Run: python download_products.py"
        )

    logger.info(f"TRY-ON REQUEST | person={person_image.filename} | product_id={product_id}")
    logger.info(f"  Product : {product['name']} ({product['category']})")
    logger.info(f"  Garment : {garment_path}")
    logger.info(f"  Steps   : {denoise_steps} | Seed: {seed}")

    # ── Read person bytes ────────────────────────────────────────────────────
    person_bytes  = await person_image.read()
    garment_bytes = garment_path.read_bytes()

    logger.info(f"  Person bytes : {len(person_bytes):,}")
    logger.info(f"  Garment bytes: {len(garment_bytes):,}")

    # ── Run try-on (in a thread — client.predict() blocks for 30-60s) ────────
    t0 = time.time()
    try:
        import anyio
        result: TryOnResult = await anyio.to_thread.run_sync(
            lambda: run_upper_body_tryon(
                person_bytes=person_bytes,
                garment_bytes=garment_bytes,
                garment_description=product["name"],
                denoise_steps=denoise_steps,
                seed=seed,
            )
        )
    except Exception as e:
        logger.error(f"Try-on failed: {e}", exc_info=True)
        err = str(e)
        if "quota" in err.lower() or "zerogpu" in err.lower():
            import re
            wait = re.search(r"Try again in (\d+:\d+:\d+)", err)
            msg = "HuggingFace ZeroGPU quota exceeded."
            if wait:
                msg += f" Try again in {wait.group(1)}."
            msg += " Add HF_TOKEN to .env for more quota."
            raise HTTPException(429, msg)
        raise HTTPException(500, f"Try-on failed: {err}")

    duration = round(time.time() - t0, 2)
    logger.info(f"TRY-ON COMPLETE | {duration}s")

    result_id = str(uuid.uuid4())
    store.save(result_id, result)

    return JSONResponse({
        "result_id":    result_id,
        "result_b64":   result.result_b64,
        "person_b64":   result.person_b64,
        "garment_b64":  result.garment_b64,
        "product_name": product["name"],
        "product_id":   product_id,
        "duration_sec": duration,
        "model":        "yisol/IDM-VTON",
    })


# ─────────────────────────────────────────────────────────────────────────────
# TRYON WITH CUSTOM UPLOAD (for future use)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/tryon/upload")
async def tryon_by_upload(
    person_image:  UploadFile = File(...),
    garment_image: UploadFile = File(...),
    garment_description: str  = Form(""),
    denoise_steps: int        = Form(30),
    seed:          int        = Form(42),
):
    """Try-on with a custom uploaded garment (not from catalog)."""
    allowed = {"image/jpeg","image/jpg","image/png","image/webp"}
    for f, n in [(person_image,"person_image"),(garment_image,"garment_image")]:
        if (f.content_type or "").lower() not in allowed:
            raise HTTPException(400, f"{n}: must be JPG/PNG/WEBP")

    person_bytes  = await person_image.read()
    garment_bytes = await garment_image.read()
    logger.info(f"CUSTOM UPLOAD TRY-ON | desc='{garment_description}'")

    t0 = time.time()
    try:
        result = run_upper_body_tryon(
            person_bytes=person_bytes,
            garment_bytes=garment_bytes,
            garment_description=garment_description,
            denoise_steps=denoise_steps,
            seed=seed,
        )
    except Exception as e:
        logger.error(f"Try-on failed: {e}", exc_info=True)
        raise HTTPException(500, f"Try-on failed: {str(e)}")

    duration = round(time.time() - t0, 2)
    result_id = str(uuid.uuid4())
    store.save(result_id, result)

    return JSONResponse({
        "result_id":   result_id,
        "result_b64":  result.result_b64,
        "person_b64":  result.person_b64,
        "garment_b64": result.garment_b64,
        "duration_sec": duration,
    })


# ─────────────────────────────────────────────────────────────────────────────
# FETCH RESULT BY ID
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/result/{result_id}")
def get_result(result_id: str):
    result = store.get(result_id)
    if not result:
        raise HTTPException(404, "Result not found or expired (results expire after 1 hour).")
    return JSONResponse({
        "result_id":   result_id,
        "result_b64":  result.result_b64,
        "person_b64":  result.person_b64,
        "garment_b64": result.garment_b64,
    })


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)