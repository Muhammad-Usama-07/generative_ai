"""
backend/analyze_cloth.py
Groq Llama 3.2 Vision — analyzes fashion items with full logging.
"""

import base64
import os
import json
import re
from groq import Groq
from backend.logger import logger, log_groq_analysis, log_error


def encode_image(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def analyze_clothing(image_bytes: bytes, mime_type: str = "image/jpeg",
                     custom_prompt: str = None) -> dict:

    logger.info(f"GROQ ANALYSIS START | mime='{mime_type}' | image_size={len(image_bytes)} bytes")
    logger.info(f"  Custom prompt: {custom_prompt or 'None (using default)'}")

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    img_b64 = encode_image(image_bytes)

    analysis_instruction = custom_prompt or "Describe this clothing or fashion item for virtual try-on."

    system_prompt = """You are a fashion expert AI. Analyze the given fashion item image
and return a JSON object with EXACTLY these keys:
- description: one detailed sentence describing the item
- category: one of [top, bottom, dress, shoes, accessory, jacket, outerwear]
- color: primary color(s)
- fit: one of [slim, regular, relaxed, oversized, tailored, n/a]
- fabric: guessed material (e.g. cotton, leather, canvas, suede, synthetic)
- prompt: a 20-30 word natural language description optimized for virtual try-on AI models

Return ONLY valid JSON. No markdown fences, no explanation, no extra text."""

    logger.info(f"  Sending to Groq model: meta-llama/llama-4-scout-17b-16e-instruct")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        max_tokens=400,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "image_url",
                     "image_url": {"url": f"data:{mime_type};base64,{img_b64}"}},
                    {"type": "text", "text": analysis_instruction},
                ],
            },
        ],
    )

    raw = response.choices[0].message.content.strip()
    logger.debug(f"  Groq raw response: {raw}")

    clean = re.sub(r"```json|```", "", raw).strip()

    try:
        parsed = json.loads(clean)
        log_groq_analysis("detected", raw, parsed)

        # ── Sanity check: warn if Groq category doesn't match UI category
        logger.info(f"  Groq detected category: '{parsed.get('category')}'")
        logger.info(f"  Final prompt for try-on model: '{parsed.get('prompt')}'")
        return parsed

    except json.JSONDecodeError as e:
        log_error("analyze_clothing JSON parse", e)
        logger.warning(f"  JSON parse failed, using fallback dict")
        return {
            "description": raw[:200],
            "category": "item",
            "color": "unknown",
            "fit": "regular",
            "fabric": "unknown",
            "prompt": raw[:100],
        }