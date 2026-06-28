"""
FitAI Backend — main.py
FastAPI server for upper-body virtual try-on using IDM-VTON.

Endpoints:
    POST /api/tryon        — run try-on, returns base64 result image
    GET  /api/health       — health check
    GET  /api/result/{id}  — fetch a previously generated result
"""

import os
import uuid
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from dotenv import load_dotenv
load_dotenv()

from tryon import run_upper_body_tryon, TryOnResult
from store import ResultStore

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
    logger.info("FitAI backend starting up...")
    hf = os.environ.get("HF_TOKEN", "")
    groq = os.environ.get("GROQ_API_KEY", "")
    logger.info(f"  HF_TOKEN   : {'SET ✓' if hf   else 'NOT SET ✗'}")
    logger.info(f"  GROQ_API_KEY: {'SET ✓' if groq else 'NOT SET ✗'}")
    yield
    logger.info("FitAI backend shutting down.")

# ── FastAPI app ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="FitAI API",
    description="Upper-body virtual try-on powered by IDM-VTON",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS — allow your HTML frontend ───────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory result store ────────────────────────────────────────────────────
store = ResultStore()


# ── HEALTH ────────────────────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model": "yisol/IDM-VTON",
        "category": "upper-body",
        "hf_token": bool(os.environ.get("HF_TOKEN")),
        "groq_key": bool(os.environ.get("GROQ_API_KEY")),
    }


# ── MAIN TRY-ON ENDPOINT ──────────────────────────────────────────────────────
@app.post("/api/tryon")
async def tryon(
    person_image: UploadFile = File(..., description="Full/upper-body photo of the person"),
    garment_image: UploadFile = File(..., description="Clothing item to try on"),
    garment_description: str = "",
    denoise_steps: int = 30,
    seed: int = 42,
):
    """
    Run upper-body virtual try-on.

    - **person_image**       : JPG/PNG of the person (full or upper body)
    - **garment_image**      : JPG/PNG of the clothing item
    - **garment_description**: Optional text description of the garment
    - **denoise_steps**      : 20–50, higher = better quality (default 30)
    - **seed**               : Reproducibility seed (default 42)

    Returns JSON with:
    - result_id      : unique ID to fetch result later
    - result_b64     : base64-encoded PNG of try-on result
    - person_b64     : base64-encoded PNG of input person
    - garment_b64    : base64-encoded PNG of input garment
    - duration_sec   : how long generation took
    """

    # ── Validate file types ──────────────────────────────────────────────────
    allowed = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
    for f, name in [(person_image, "person_image"), (garment_image, "garment_image")]:
        ct = (f.content_type or "").lower()
        if ct not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"{name} must be JPEG/PNG/WEBP, got '{ct}'"
            )

    # ── Validate steps range ─────────────────────────────────────────────────
    if not (10 <= denoise_steps <= 100):
        raise HTTPException(status_code=400, detail="denoise_steps must be 10–100")

    # ── Read image bytes ─────────────────────────────────────────────────────
    logger.info(f"TRY-ON REQUEST | person={person_image.filename} | garment={garment_image.filename}")
    person_bytes  = await person_image.read()
    garment_bytes = await garment_image.read()
    logger.info(f"  Person bytes : {len(person_bytes):,}")
    logger.info(f"  Garment bytes: {len(garment_bytes):,}")
    logger.info(f"  Description  : '{garment_description}'")
    logger.info(f"  Steps/Seed   : {denoise_steps}/{seed}")

    # ── Run try-on ───────────────────────────────────────────────────────────
    t0 = time.time()
    try:
        result: TryOnResult = run_upper_body_tryon(
            person_bytes=person_bytes,
            garment_bytes=garment_bytes,
            garment_description=garment_description,
            denoise_steps=denoise_steps,
            seed=seed,
        )
    except Exception as e:
        logger.error(f"Try-on failed: {e}", exc_info=True)
        err = str(e)

        # User-friendly quota error
        if "quota" in err.lower() or "zerogpu" in err.lower():
            import re
            wait = re.search(r"Try again in (\d+:\d+:\d+)", err)
            msg = "HuggingFace ZeroGPU quota exceeded."
            if wait:
                msg += f" Try again in {wait.group(1)}."
            msg += " Add HF_TOKEN to .env for more quota."
            raise HTTPException(status_code=429, detail=msg)

        raise HTTPException(status_code=500, detail=f"Try-on failed: {err}")

    duration = round(time.time() - t0, 2)
    logger.info(f"TRY-ON COMPLETE | duration={duration}s")

    # ── Store + return ───────────────────────────────────────────────────────
    result_id = str(uuid.uuid4())
    store.save(result_id, result)

    return JSONResponse({
        "result_id":    result_id,
        "result_b64":   result.result_b64,
        "person_b64":   result.person_b64,
        "garment_b64":  result.garment_b64,
        "duration_sec": duration,
        "model":        "yisol/IDM-VTON",
        "category":     "upper-body",
    })


# ── FETCH RESULT BY ID ────────────────────────────────────────────────────────
@app.get("/api/result/{result_id}")
def get_result(result_id: str):
    """Fetch a previously generated result by its ID."""
    result = store.get(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found or expired.")
    return JSONResponse({
        "result_id":  result_id,
        "result_b64": result.result_b64,
        "person_b64": result.person_b64,
        "garment_b64": result.garment_b64,
    })


# ── RUN ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)