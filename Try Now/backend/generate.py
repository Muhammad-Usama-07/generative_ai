"""
backend/generate.py

Verified working Spaces (June 2025):
  Tops/Bottoms/Dresses → Nymbo/Virtual-Try-On  (OOTDiffusion-based, supports category param)
  Shoes               → franciszzz/virtual-try-on-shoe
  Accessories         → Kwai-Kolors/Kolors-Virtual-Try-On (fallback: IDM-VTON)

levihsu/OOTDiffusion Space is currently broken (runtime error) — do NOT use it.
OOTDiffusion/OOTDiffusion is a MODEL repo, not a Space — cannot be called via gradio_client.
"""

import os
import tempfile
import io
from PIL import Image
from backend.logger import (
    logger, log_tryon_request, log_model_selected,
    log_space_attempt, log_space_success, log_space_failure,
    log_result, log_error,
)


def bytes_to_pil(image_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(image_bytes))


def pil_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def _get_client(space: str):
    from gradio_client import Client
    hf_token = os.environ.get("HF_TOKEN", "").strip()
    logger.debug(f"Client → '{space}' | HF_TOKEN={'SET' if hf_token else 'NOT SET'}")
    if hf_token:
        return Client(space, hf_token=hf_token)
    return Client(space)


def _save_images(tmp, person_image, item_image):
    person_path = os.path.join(tmp, "person.jpg")
    item_path   = os.path.join(tmp, "item.jpg")
    person_image.convert("RGB").save(person_path, quality=95)
    item_image.convert("RGB").save(item_path, quality=95)
    logger.debug(f"Saved → person:{person_path} | item:{item_path}")
    return person_path, item_path


# ─────────────────────────────────────────────────────────────────────────────
# TOPS / BOTTOMS / DRESSES
# Primary: Nymbo/Virtual-Try-On (OOTDiffusion-based, category-aware, WORKING)
# Fallback: yisol/IDM-VTON (upper body only — only good for tops)
# ─────────────────────────────────────────────────────────────────────────────
CATEGORY_MAP = {
    "tops":    "Upper-body",
    "bottoms": "Lower-body",
    "dresses": "Dress",
}

def run_garment_tryon(person_image, cloth_image, cloth_description,
                      category="tops", denoise_steps=30, seed=42):
    from gradio_client import handle_file

    ootd_category = CATEGORY_MAP.get(category, "Upper-body")
    logger.info(f"GARMENT TRYON | ui_category='{category}' → ootd_category='{ootd_category}'")
    logger.info(f"  Description: '{cloth_description}'")

    with tempfile.TemporaryDirectory() as tmp:
        person_path, cloth_path = _save_images(tmp, person_image, cloth_image)
        last_err = None

        # ── Primary: Nymbo/Virtual-Try-On (OOTDiffusion, category-aware) ──
        space = "Nymbo/Virtual-Try-On"
        log_space_attempt(space, 1)
        try:
            client = _get_client(space)
            logger.info(f"  Calling {space}")
            logger.info(f"    person_path   = {person_path}")
            logger.info(f"    cloth_path    = {cloth_path}")
            logger.info(f"    category      = '{ootd_category}'  ← controls which body region")
            logger.info(f"    n_samples     = 1")
            logger.info(f"    n_steps       = {denoise_steps}")
            logger.info(f"    image_scale   = 2.0")
            logger.info(f"    seed          = {seed}")

            result = client.predict(
                handle_file(person_path),   # person image
                handle_file(cloth_path),    # garment image
                ootd_category,              # "Upper-body" / "Lower-body" / "Dress"
                1,                          # n_samples
                denoise_steps,              # n_steps
                2.0,                        # image_scale
                seed,                       # seed
                api_name="/process_dc",
            )

            logger.info(f"  Raw result: {result}")

            # Result can be list of dicts [{"image": path}] or list of paths
            if isinstance(result, (list, tuple)) and len(result) > 0:
                r = result[0]
                path = r.get("image") if isinstance(r, dict) else r
            else:
                path = result

            out = Image.open(path).copy()
            log_space_success(space)
            log_result(out.size)
            return out

        except Exception as e:
            log_space_failure(space, e)
            last_err = e
            logger.warning(f"  Nymbo/Virtual-Try-On failed, trying IDM-VTON fallback")

        # ── Fallback: IDM-VTON (upper body only — warn if not tops) ──
        if category != "tops":
            logger.warning(
                f"  IDM-VTON fallback does NOT support '{category}' correctly. "
                f"It will apply to upper body regardless. Result may be wrong."
            )

        space = "yisol/IDM-VTON"
        log_space_attempt(space, 2)
        try:
            client = _get_client(space)
            logger.info(f"  Calling {space} (fallback)")
            result = client.predict(
                dict(background=handle_file(person_path), layers=[], composite=None),
                handle_file(cloth_path),
                cloth_description,
                True, True,
                denoise_steps, seed,
                api_name="/tryon",
            )
            logger.info(f"  Raw result: {result}")
            out = Image.open(result[0]).copy()
            log_space_success(space)
            log_result(out.size)
            return out

        except Exception as e:
            log_space_failure(space, e)
            last_err = e

        log_error("run_garment_tryon", last_err)
        raise RuntimeError(
            f"All garment spaces failed for category='{category}'. Last error: {last_err}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# SHOES
# Primary: franciszzz/virtual-try-on-shoe
# Fallback: Kwai-Kolors/Kolors-Virtual-Try-On
# ─────────────────────────────────────────────────────────────────────────────
def run_shoe_tryon(person_image, shoe_image, shoe_description, denoise_steps=30, seed=42):
    from gradio_client import handle_file

    logger.info(f"SHOE TRYON | desc='{shoe_description}'")

    with tempfile.TemporaryDirectory() as tmp:
        person_path, shoe_path = _save_images(tmp, person_image, shoe_image)
        last_err = None

        # ── Primary: dedicated shoe space ──
        space = "franciszzz/virtual-try-on-shoe"
        log_space_attempt(space, 1)
        try:
            client = _get_client(space)
            logger.info(f"  Calling shoe-specific space: {space}")
            result = client.predict(
                handle_file(person_path),
                handle_file(shoe_path),
                api_name="/predict",
            )
            logger.info(f"  Raw result: {result}")
            out = Image.open(result).copy()
            log_space_success(space)
            log_result(out.size)
            return out

        except Exception as e:
            log_space_failure(space, e)
            last_err = e

        # ── Fallback: Kolors Virtual Try-On ──
        space = "Kwai-Kolors/Kolors-Virtual-Try-On"
        log_space_attempt(space, 2)
        try:
            client = _get_client(space)
            logger.info(f"  Calling Kolors fallback: {space}")
            result = client.predict(
                handle_file(person_path),
                handle_file(shoe_path),
                seed,
                api_name="/try_on",
            )
            logger.info(f"  Raw result: {result}")
            path = result[0] if isinstance(result, (list, tuple)) else result
            out = Image.open(path).copy()
            log_space_success(space)
            log_result(out.size)
            return out

        except Exception as e:
            log_space_failure(space, e)
            last_err = e

        log_error("run_shoe_tryon", last_err)
        raise RuntimeError(f"Shoe try-on failed: {last_err}")


# ─────────────────────────────────────────────────────────────────────────────
# ACCESSORIES
# Primary: Kwai-Kolors/Kolors-Virtual-Try-On
# Fallback: yisol/IDM-VTON
# ─────────────────────────────────────────────────────────────────────────────
def run_accessory_tryon(person_image, accessory_image, accessory_description,
                        denoise_steps=30, seed=42):
    from gradio_client import handle_file

    logger.info(f"ACCESSORY TRYON | desc='{accessory_description}'")

    with tempfile.TemporaryDirectory() as tmp:
        person_path, acc_path = _save_images(tmp, person_image, accessory_image)
        last_err = None

        space = "Kwai-Kolors/Kolors-Virtual-Try-On"
        log_space_attempt(space, 1)
        try:
            client = _get_client(space)
            logger.info(f"  Calling {space}")
            result = client.predict(
                handle_file(person_path),
                handle_file(acc_path),
                seed,
                api_name="/try_on",
            )
            logger.info(f"  Raw result: {result}")
            path = result[0] if isinstance(result, (list, tuple)) else result
            out = Image.open(path).copy()
            log_space_success(space)
            log_result(out.size)
            return out

        except Exception as e:
            log_space_failure(space, e)
            last_err = e

        # Fallback: IDM-VTON
        space = "yisol/IDM-VTON"
        log_space_attempt(space, 2)
        try:
            client = _get_client(space)
            result = client.predict(
                dict(background=handle_file(person_path), layers=[], composite=None),
                handle_file(acc_path),
                accessory_description,
                True, True, denoise_steps, seed,
                api_name="/tryon",
            )
            logger.info(f"  Raw result: {result}")
            out = Image.open(result[0]).copy()
            log_space_success(space)
            log_result(out.size)
            return out

        except Exception as e:
            log_space_failure(space, e)
            last_err = e

        log_error("run_accessory_tryon", last_err)
        raise RuntimeError(f"Accessory try-on failed: {last_err}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────────────────────
def run_tryon(person_image, cloth_image, cloth_description,
              category="tops", denoise_steps=30, seed=42):

    log_tryon_request(
        category=category,
        person_size=person_image.size,
        item_size=cloth_image.size,
        description=cloth_description,
        denoise_steps=denoise_steps,
        seed=seed,
    )

    router = {
        "tops":        ("Nymbo/Virtual-Try-On (Upper-body)", "Nymbo/Virtual-Try-On"),
        "bottoms":     ("Nymbo/Virtual-Try-On (Lower-body)", "Nymbo/Virtual-Try-On"),
        "dresses":     ("Nymbo/Virtual-Try-On (Dress)",      "Nymbo/Virtual-Try-On"),
        "shoes":       ("ShoeVTON",                          "franciszzz/virtual-try-on-shoe"),
        "accessories": ("Kolors-Virtual-Try-On",             "Kwai-Kolors/Kolors-Virtual-Try-On"),
    }

    model_name, space = router.get(category, router["tops"])
    log_model_selected(category, model_name, space)

    if category in ("tops", "bottoms", "dresses"):
        return run_garment_tryon(person_image, cloth_image, cloth_description,
                                 category, denoise_steps, seed)
    elif category == "shoes":
        return run_shoe_tryon(person_image, cloth_image, cloth_description,
                              denoise_steps, seed)
    else:
        return run_accessory_tryon(person_image, cloth_image, cloth_description,
                                   denoise_steps, seed)