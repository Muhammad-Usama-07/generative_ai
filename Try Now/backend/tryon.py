"""
FitAI Backend — tryon.py
Core upper-body try-on logic using IDM-VTON via gradio_client.
Uses the exact API signature provided.
"""

import os
import io
import base64
import logging
import tempfile
from dataclasses import dataclass
from PIL import Image
from gradio_client import Client, handle_file

logger = logging.getLogger("fitai.tryon")


# ── Result dataclass ───────────────────────────────────────────────────────────
@dataclass
class TryOnResult:
    result_img:  Image.Image   # AI try-on result
    person_img:  Image.Image   # original person image
    garment_img: Image.Image   # garment image
    result_b64:  str           # base64 PNG of result
    person_b64:  str           # base64 PNG of person
    garment_b64: str           # base64 PNG of garment


# ── Helpers ────────────────────────────────────────────────────────────────────
def _bytes_to_pil(b: bytes) -> Image.Image:
    return Image.open(io.BytesIO(b)).convert("RGB")


def _pil_to_b64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def _get_client() -> Client:
    """Create IDM-VTON client with HF token if available."""
    hf_token = os.environ.get("HF_TOKEN", "").strip()
    space = "yisol/IDM-VTON"
    if hf_token:
        logger.info(f"Connecting to {space} with HF_TOKEN")
        return Client(space, hf_token=hf_token)
    logger.warning(f"Connecting to {space} WITHOUT HF_TOKEN (limited quota)")
    return Client(space)


# ── Main try-on function ───────────────────────────────────────────────────────
def run_upper_body_tryon(
    person_bytes: bytes,
    garment_bytes: bytes,
    garment_description: str = "",
    denoise_steps: int = 30,
    seed: int = 42,
) -> TryOnResult:
    """
    Run upper-body try-on using IDM-VTON.

    Args:
        person_bytes       : Raw bytes of the person image
        garment_bytes      : Raw bytes of the garment image
        garment_description: Text description of the garment (improves accuracy)
        denoise_steps      : Diffusion steps (20–50, higher = better quality)
        seed               : Random seed for reproducibility

    Returns:
        TryOnResult with result image + both inputs as PIL images and base64 strings
    """

    # ── Convert bytes → PIL ──────────────────────────────────────────────────
    person_img  = _bytes_to_pil(person_bytes)
    garment_img = _bytes_to_pil(garment_bytes)

    logger.info(f"Person image  : {person_img.size[0]}x{person_img.size[1]} px")
    logger.info(f"Garment image : {garment_img.size[0]}x{garment_img.size[1]} px")
    logger.info(f"Description   : '{garment_description}'")
    logger.info(f"Denoise steps : {denoise_steps} | Seed: {seed}")

    with tempfile.TemporaryDirectory() as tmp:
        # ── Save images to disk (gradio_client needs file paths) ─────────────
        person_path  = os.path.join(tmp, "person.jpg")
        garment_path = os.path.join(tmp, "garment.jpg")

        person_img.save(person_path, format="JPEG", quality=95)
        garment_img.save(garment_path, format="JPEG", quality=95)
        logger.info(f"Saved person  → {person_path}")
        logger.info(f"Saved garment → {garment_path}")

        # ── Connect to IDM-VTON ───────────────────────────────────────────────
        client = _get_client()

        # ── Call IDM-VTON (exact API signature as provided) ──────────────────
        logger.info("Calling IDM-VTON /tryon ...")
        result = client.predict(
            dict={"background": handle_file(person_path)},  # person image dict
            garm_img=handle_file(garment_path),             # garment image
            garment_des=garment_description,                # garment description
            is_checked=True,                                # auto-mask
            is_checked_crop=False,                          # no auto-crop
            denoise_steps=denoise_steps,                    # diffusion steps
            seed=seed,                                      # seed
            api_name="/tryon"
        )
        logger.info(f"Raw result from IDM-VTON: {result}")

        # ── Extract result paths from tuple ──────────────────────────────────
        # result is a tuple: (result_path, mask_path)
        result_path = result[0]   # try-on result image
        mask_path   = result[1]   # segmentation mask (not used)
        logger.info(f"Result path: {result_path}")
        logger.info(f"Mask path  : {mask_path} (ignored)")

        # ── Load result image ─────────────────────────────────────────────────
        result_img = Image.open(result_path).convert("RGB")
        logger.info(f"Result image size: {result_img.size[0]}x{result_img.size[1]} px")

        # ── Encode all three to base64 for API response ───────────────────────
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