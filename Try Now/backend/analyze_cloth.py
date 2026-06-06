"""
analyze_cloth.py
Uses Groq (Llama 3.2 Vision - FREE) to analyze the uploaded clothing image
and return a structured description for the IDM-VTON model.
"""

import base64
import os
from groq import Groq


def encode_image(image_bytes: bytes) -> str:
    """Convert image bytes to base64 string."""
    return base64.b64encode(image_bytes).decode("utf-8")


def analyze_clothing(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    """
    Analyze clothing image using Groq Llama 3.2 Vision (FREE).

    Args:
        image_bytes: Raw image bytes
        mime_type: MIME type of the image (image/jpeg, image/png, etc.)

    Returns:
        dict with keys: description, category, color, fit, fabric, prompt
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    img_b64 = encode_image(image_bytes)

    system_prompt = """You are a fashion expert AI. When given a clothing image,
    analyze it and return a JSON object with these exact keys:
    - description: one detailed sentence describing the garment
    - category: one of [top, bottom, dress, jacket, outerwear, suit, accessory]
    - color: primary color(s) of the garment
    - fit: one of [slim, regular, relaxed, oversized, tailored]
    - fabric: guessed fabric (e.g. cotton, linen, denim, silk, wool)
    - prompt: a 20-30 word natural language prompt optimized for virtual try-on AI

    Return ONLY valid JSON. No markdown, no explanation."""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        max_tokens=400,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{img_b64}"
                        },
                    },
                    {
                        "type": "text",
                        "text": "Analyze this clothing item and return the JSON.",
                    },
                ],
            },
        ],
    )

    import json, re

    raw = response.choices[0].message.content.strip()
    # strip markdown fences if model wraps in ```json
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback if model returns unexpected format
        return {
            "description": raw[:200],
            "category": "top",
            "color": "unknown",
            "fit": "regular",
            "fabric": "unknown",
            "prompt": raw[:100],
        }