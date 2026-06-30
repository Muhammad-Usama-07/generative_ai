"""
FitAI Backend — tryon.py
Core upper-body try-on logic using IDM-VTON via gradio_client.

KEY FIX vs previous version:
  - Client is now created ONCE at module load (matches the working notebook
    pattern: `client = Client(...)` at top level), not recreated per-request.
    Recreating the Client object on every call re-triggers the full Gradio
    handshake (config fetch, queue join, heartbeat negotiation) which is
    slower and more failure-prone under FastAPI's threaded request handling.
  - Full exception traceback is logged BEFORE any cleanup runs, so the real
    error is visible instead of being masked by a generic 500.
  - session_dir cleanup no longer touches the Gradio-returned result_path
    (that file lives in Gradio's own temp cache, not our session_dir) —
    the previous version's `finally: shutil.rmtree(session_dir)` was safe,
    but we now copy the result bytes into memory FIRST, before any cleanup,
    so a slow/failed cleanup can never affect the response.
"""

import os
import io
import base64
import logging
import traceback
import uuid
import shutil
from dataclasses import dataclass
from pathlib import Path
from PIL import Image
from gradio_client import Client, handle_file

logger = logging.getLogger("fitai.tryon")

UPLOADS_DIR = Path(__file__).parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


# ── Result dataclass ───────────────────────────────────────────────────────────
@dataclass
class TryOnResult:
    result_img:  Image.Image
    person_img:  Image.Image
    garment_img: Image.Image
    result_b64:  str
    person_b64:  str
    garment_b64: str


# ── Helpers ────────────────────────────────────────────────────────────────────
def _bytes_to_pil(b: bytes) -> Image.Image:
    return Image.open(io.BytesIO(b)).convert("RGB")


def _pil_to_b64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


# ── MODULE-LEVEL CLIENT — created once, matches working notebook pattern ──────
_client: Client | None = None


def _get_client() -> Client:
    """
    Return a singleton IDM-VTON client, creating it once on first use.
    This matches the pattern in the working notebook script, where
    `client = Client(...)` is created once at the top of the file and
    reused for every call — avoiding repeated handshake/queue overhead.
    """
    global _client
    if _client is None:
        hf_token = os.environ.get("HF_TOKEN", "").strip()
        space = "yisol/IDM-VTON"
        logger.info(f"Creating IDM-VTON client (once) for space='{space}' | HF_TOKEN={'SET' if hf_token else 'NOT SET'}")
        if hf_token:
            _client = Client(space, hf_token=hf_token)
        else:
            logger.warning("No HF_TOKEN set — limited ZeroGPU quota")
            _client = Client(space)
    return _client


# ── Main try-on function ───────────────────────────────────────────────────────
def run_upper_body_tryon(
    person_bytes: bytes,
    garment_bytes: bytes,
    garment_description: str = "",
    denoise_steps: int = 30,
    seed: int = 42,
) -> TryOnResult:
    """
    Run upper-body try-on using IDM-VTON. Mirrors the exact working
    notebook call signature and flow.
    """

    person_img  = _bytes_to_pil(person_bytes)
    garment_img = _bytes_to_pil(garment_bytes)

    logger.info(f"Person image  : {person_img.size[0]}x{person_img.size[1]} px")
    logger.info(f"Garment image : {garment_img.size[0]}x{garment_img.size[1]} px")
    logger.info(f"Description   : '{garment_description}'")
    logger.info(f"Denoise steps : {denoise_steps} | Seed: {seed}")

    session_id  = str(uuid.uuid4())
    session_dir = UPLOADS_DIR / session_id
    session_dir.mkdir(exist_ok=True)

    person_path  = str(session_dir / "person.jpg")
    garment_path = str(session_dir / "garment.jpg")

    try:
        person_img.save(person_path, format="JPEG", quality=95)
        garment_img.save(garment_path, format="JPEG", quality=95)
        logger.info(f"Saved person  → {person_path}")
        logger.info(f"Saved garment → {garment_path}")

        client = _get_client()

        logger.info("Calling IDM-VTON /tryon ...")
        try:
            result = client.predict(
                dict={"background": handle_file(person_path)},
                garm_img=handle_file(garment_path),
                garment_des=garment_description,
                is_checked=True,
                is_checked_crop=False,
                denoise_steps=denoise_steps,
                seed=seed,
                api_name="/tryon",
            )
        except Exception as predict_err:
            # Log the FULL traceback right here — this is the real failure point
            logger.error("client.predict() raised an exception:")
            logger.error(traceback.format_exc())
            raise RuntimeError(f"IDM-VTON predict() failed: {predict_err}") from predict_err

        logger.info(f"Raw result from IDM-VTON: {result}")

        if not result or len(result) < 1:
            raise RuntimeError(f"IDM-VTON returned unexpected result: {result!r}")

        result_path = result[0]
        mask_path   = result[1] if len(result) > 1 else None
        logger.info(f"Result path: {result_path}")
        logger.info(f"Mask path  : {mask_path} (ignored)")

        if not result_path or not os.path.exists(result_path):
            raise RuntimeError(f"Result image path does not exist on disk: {result_path}")

        # ── Load result image and immediately encode to bytes/base64 ─────────
        # This happens BEFORE any cleanup, so cleanup can never corrupt the response.
        result_img = Image.open(result_path).convert("RGB")
        result_img.load()  # force full decode into memory now, while file still exists
        logger.info(f"Result image size: {result_img.size[0]}x{result_img.size[1]} px")

        result_b64  = _pil_to_b64(result_img)
        person_b64  = _pil_to_b64(person_img)
        garment_b64 = _pil_to_b64(garment_img)

        return TryOnResult(
            result_img=result_img,
            person_img=person_img,
            garment_img=garment_img,
            result_b64=result_b64,
            person_b64=person_b64,
            garment_b64=garment_b64,
        )

    except Exception:
        # Log full traceback for ANY failure in this function, not just predict()
        logger.error("run_upper_body_tryon() failed:")
        logger.error(traceback.format_exc())
        raise

    finally:
        # Clean up our own session dir (person.jpg/garment.jpg we created).
        # This never touches result_path, which lives in Gradio's own cache.
        try:
            if session_dir.exists():
                shutil.rmtree(session_dir, ignore_errors=True)
                logger.info(f"Cleaned up session dir: {session_id}")
        except Exception as cleanup_err:
            logger.warning(f"Session cleanup failed (non-fatal): {cleanup_err}")