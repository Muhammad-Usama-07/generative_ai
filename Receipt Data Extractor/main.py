import os, io, json, time, base64
import numpy as np
import easyocr
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from groq import Groq

app = FastAPI(title="Medical Receipt Extractor")

# Model names Groq console se verify kar lein, ye change hotay rehtay hain
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # yeh line zaroori hai

TEXT_MODEL = os.getenv("TEXT_MODEL", "llama-3.3-70b-versatile")
VISION_MODEL = os.getenv("VISION_MODEL", "qwen/qwen3.8-27b")

reader = easyocr.Reader(["en"], gpu=False)

SCHEMA_PROMPT = """You extract data from medical receipts.
Return ONLY valid JSON with this exact structure (use null if missing):
{
  "patient_name": null,
  "doctor_name": null,
  "hospital_or_clinic": null,
  "date": null,
  "receipt_number": null,
  "items": [{"description": null, "quantity": null, "price": null}],
  "total_amount": null,
  "currency": null
}
Do not guess values that are not present."""


def read_image(file_bytes: bytes) -> Image.Image:
    try:
        return Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(400, "Invalid image file")


@app.post("/extract/ocr")
async def extract_ocr(file: UploadFile = File(...)):
    img = read_image(await file.read())

    t0 = time.time()
    lines = reader.readtext(np.array(img), detail=0, paragraph=False)
    ocr_text = "\n".join(lines)
    t_ocr = time.time() - t0

    t1 = time.time()
    resp = client.chat.completions.create(
        model=TEXT_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SCHEMA_PROMPT},
            {"role": "user", "content": f"Receipt OCR text:\n{ocr_text}"},
        ],
    )
    t_llm = time.time() - t1

    return {
        "method": "ocr+llm",
        "raw_ocr_text": ocr_text,
        "data": json.loads(resp.choices[0].message.content),
        "timing_sec": {"ocr": round(t_ocr, 2), "llm": round(t_llm, 2),
                       "total": round(t_ocr + t_llm, 2)},
    }


@app.post("/extract/llm")
async def extract_llm(file: UploadFile = File(...)):
    raw = await file.read()
    img = read_image(raw)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    b64 = base64.b64encode(buf.getvalue()).decode()

    t0 = time.time()
    resp = client.chat.completions.create(
    model=VISION_MODEL,
    temperature=0,
    reasoning_format="hidden",   # thinking output response se hata deta hai
    response_format={"type": "json_object"},
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": SCHEMA_PROMPT},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ],
        }],
    )
    t_total = time.time() - t0

    return {
        "method": "vision-llm",
        "data": json.loads(resp.choices[0].message.content),
        "timing_sec": {"total": round(t_total, 2)},
    }