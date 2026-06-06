"""
generate.py
Runs virtual try-on using the FREE IDM-VTON HuggingFace Space
via the gradio_client library — no GPU, no paid API.
"""

import os
import tempfile
from pathlib import Path
from PIL import Image
import io


def run_tryon(
    person_image: Image.Image,
    cloth_image: Image.Image,
    cloth_description: str,
    denoise_steps: int = 30,
    seed: int = 42,
) -> Image.Image:
    """
    Call the IDM-VTON HuggingFace Space via Gradio Client (FREE).

    Args:
        person_image: PIL Image of the person (full body)
        cloth_image:  PIL Image of the clothing item
        cloth_description: Text description from Groq analysis
        denoise_steps: Denoising steps (20-40; higher = better quality, slower)
        seed: Random seed for reproducibility

    Returns:
        PIL Image — the try-on result
    """
    from gradio_client import Client, handle_file

    # Save images to temp files (gradio_client needs file paths)
    with tempfile.TemporaryDirectory() as tmp:
        person_path = os.path.join(tmp, "person.jpg")
        cloth_path  = os.path.join(tmp, "cloth.jpg")

        # Ensure RGB before saving
        person_image.convert("RGB").save(person_path, quality=95)
        cloth_image.convert("RGB").save(cloth_path, quality=95)

        client = Client("yisol/IDM-VTON")

        result = client.predict(
            # Human image dict (background = the person image, layers & composite = None)
            dict(
                background=handle_file(person_path),
                layers=[],
                composite=None,
            ),
            # Garment image
            handle_file(cloth_path),
            # Garment description (from Groq)
            cloth_description,
            # is_checked — use auto-mask
            True,
            # is_checked_crop — auto crop & resize
            True,
            # Denoising steps
            denoise_steps,
            # Seed
            seed,
            api_name="/tryon",
        )

        # result is a tuple: (output_image_path, masked_image_path)
        output_path = result[0]
        return Image.open(output_path).copy()


def bytes_to_pil(image_bytes: bytes) -> Image.Image:
    """Convert raw bytes to PIL Image."""
    return Image.open(io.BytesIO(image_bytes))


def pil_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    """Convert PIL Image to bytes for download."""
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()