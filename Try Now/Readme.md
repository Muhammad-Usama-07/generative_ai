# 👗 FitAI — AI Virtual Try-On

> Upload your photo. Pick any item. See it on **you** — before you buy.

FitAI is a full-stack AI virtual try-on web application. Users upload a personal photo, browse a product catalog, and see AI-generated results showing exactly how a garment looks on their body — powered entirely by free, open-source models.

---

## ✨ Features

- **Virtual Try-On** — AI composites any clothing item onto the user's photo
- **Product Catalog** — Browse tops, bottoms, shoes and caps with real product images
- **Category-aware routing** — Dedicated AI models per category for accurate results
- **Multi-select with smart validation** — Prevents invalid combinations (e.g. multiple tops)
- **Before/After comparison** — Interactive drag slider + 3-panel Original + Product = Result view
- **Full outfit upsell** — After upper-body try-on, prompts user to try complete outfit
- **Sign-up gate** — Non-top categories (bottoms, shoes, caps) require account to try on
- **FastAPI backend** — Clean REST API with product catalog endpoint, result caching, health check
- **Zero paid APIs** — HuggingFace free tier + Groq free tier only

---

## 🤖 AI Stack (100% Free & Open Source)

| Category | Model | HuggingFace Space |
|---|---|---|
| 👕 **Tops** | IDM-VTON | `yisol/IDM-VTON` |
| 👖 **Bottoms** | OOTDiffusion (Lower-body) | `Nymbo/Virtual-Try-On` |
| 👗 **Dresses** | OOTDiffusion (Dress) | `Nymbo/Virtual-Try-On` |
| 👟 **Shoes** | ShoeVTON | `franciszzz/virtual-try-on-shoe` |
| 🧢 **Caps** | Kolors Virtual Try-On | `Kwai-Kolors/Kolors-Virtual-Try-On` |
| 🤖 **Vision Analysis** | Llama 3.2 Vision | Groq API (free tier) |

> **Note:** IDM-VTON takes ~60–120 seconds per generation on the free ZeroGPU tier. This is normal — the model runs on shared GPU hardware.

---

## 🗂️ Project Structure

```
FitAI/
│
├── frontend/                       ← open in browser (never double-click)
│   ├── index.html                  ← landing page with catalog, before/after slider
│   ├── tryon.html                  ← virtual try-on page
│   └── serve_frontend.py           ← serves frontend at http://localhost:5500
│
└── backend/                        ← Python FastAPI server
    ├── main.py                     ← FastAPI app, all endpoints
    ├── tryon.py                    ← IDM-VTON core logic, singleton client
    ├── products.py                 ← product catalog (single source of truth)
    ├── store.py                    ← in-memory result store with TTL expiry
    ├── download_products.py        ← downloads all 11 product images (run once)
    ├── debug_tryon.py              ← end-to-end pipeline debugger (no server needed)
    ├── test_tryon.py               ← CLI test tool
    ├── requirements.txt
    ├── .env                        ← API keys (you create from .env.example)
    ├── .env.example                ← template
    │
    └── static/
        └── products/               ← auto-created by download_products.py
            ├── white_tee.jpg
            ├── oxford_shirt.jpg
            ├── denim_overshirt.jpg
            ├── slim_jeans.jpg
            ├── khaki_chinos.jpg
            ├── black_trousers.jpg
            ├── white_sneakers.jpg
            ├── runners.jpg
            ├── chukka_boots.jpg
            ├── baseball_cap.jpg
            └── snapback_cap.jpg
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- pip
- A free HuggingFace account — [huggingface.co](https://huggingface.co)
- A free Groq account — [console.groq.com](https://console.groq.com)

### Step 1 — Install dependencies

```cmd
cd FitAI/backend
pip install -r requirements.txt
```

### Step 2 — Configure API keys

```cmd
copy .env.example .env
notepad .env
```

Paste your keys:

```env
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

| Key | Where to get it | Cost |
|---|---|---|
| `HF_TOKEN` | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) → New token → **Read** | Free |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) | Free |

> `HF_TOKEN` is required. Without it, HuggingFace's ZeroGPU quota is exhausted almost immediately (~60s/day). A logged-in token gives significantly more free GPU time.

### Step 3 — Download product images (run once)

```cmd
python download_products.py
```

Expected output:
```
Downloading 11 product images...
  ✓ white_tee.jpg (37 KB)
  ✓ oxford_shirt.jpg (52 KB)
  ...
11/11 images ready in static/products/
```

### Step 4 — Verify the pipeline works (debug script)

Before running the server, verify end-to-end:

```cmd
:: Copy any person photo first
copy path\to\any_photo.jpg static\test_person.jpg

:: Run all 9 diagnostic steps
python debug_tryon.py
```

All 9 steps should pass and a `debug_result.jpg` will appear in `backend/` — open it to confirm the AI result looks correct.

---

## 🚀 Running the App

Open **two terminals**:

**Terminal 1 — Backend**
```cmd
cd FitAI/backend
python main.py
```
Expected:
```
FitAI backend starting...
  HF_TOKEN    : SET ✓
  GROQ_API_KEY: SET ✓
  Product images: 11 found ✓
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 — Frontend**
```cmd
cd FitAI/frontend
python serve_frontend.py
```
Expected:
```
Serving frontend from: ...
Open in browser: http://localhost:5500/tryon.html
```

**Browser:**

Open **`http://localhost:5500/tryon.html`**

> ⚠️ **Never open `tryon.html` by double-clicking.** The `file://` URL blocks `fetch()` calls to the backend. Always use `http://localhost:5500/tryon.html`.

---

## 🌐 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Server status, token check, missing images |
| `GET` | `/api/products` | All 11 products with image URLs |
| `POST` | `/api/tryon` | Try-on by `product_id` (uses local saved image) |
| `POST` | `/api/tryon/upload` | Try-on with custom uploaded garment |
| `GET` | `/api/result/{id}` | Fetch a previous result by UUID |

### POST `/api/tryon` — Main endpoint

**Request (multipart/form-data):**

| Field | Type | Description |
|---|---|---|
| `person_image` | File | JPG/PNG/WEBP photo of the person |
| `product_id` | string | Product ID from `/api/products` (e.g. `"white_tee"`) |
| `denoise_steps` | int | 20–50, default 30. Higher = better quality, slower |
| `seed` | int | Reproducibility seed, default 42 |

**Response (JSON):**

```json
{
  "result_id":    "uuid",
  "result_b64":   "base64-encoded PNG of try-on result",
  "person_b64":   "base64-encoded PNG of input person",
  "garment_b64":  "base64-encoded PNG of input garment",
  "product_name": "Classic White Tee",
  "product_id":   "white_tee",
  "duration_sec": 117.4,
  "model":        "yisol/IDM-VTON"
}
```

**Check health:**
```
http://localhost:8000/api/health
http://localhost:8000/api/products
http://localhost:8000/docs          ← Swagger UI
```

---

## 🧪 Testing Without the UI

```cmd
:: Quick CLI test
python test_tryon.py --person static\test_person.jpg --garment static\products\white_tee.jpg

:: Full pipeline diagnostic (recommended before first use)
python debug_tryon.py
```

---

## 🐛 Troubleshooting

### `ReadTimeout: The read operation timed out`

The model finished generating but downloading the result image from HuggingFace timed out. This is a transient network issue.

- Try again — it often succeeds on a second attempt
- The backend auto-retries twice before giving up
- If it happens consistently: try a different network, disable VPN, or try during off-peak hours

### `ZeroGPU quota exceeded`

```
You have exceeded your ZeroGPU quota (60s requested vs. 79s left)
```

- Make sure `HF_TOKEN` is in your `.env` — a logged-in token has much higher quota
- Wait 24 hours for quota to reset
- Lower `denoise_steps` to 20 to use less GPU time per run

### `person_image must be JPG/PNG/WEBP, got 'image/octet-stream'`

The browser sent the file with an unrecognized MIME type. Rename the file to `.jpg` or `.png` and try again.

### `Product not found`

The `data-id` attribute in `tryon.html` doesn't match a product `id` in `products.py`. Check that they match exactly (case-sensitive).

### Result image doesn't appear in the UI

1. Open DevTools (F12) → Network tab
2. Click the failed `tryon` request → Response tab
3. The JSON `"detail"` field shows the real Python error
4. Run `debug_tryon.py` — if all 9 steps pass, the backend is fine and the issue is JavaScript

### `set_page_config() can only be called once` (Streamlit version)

`set_page_config()` must only exist in `1_Home.py`, never in files inside `pages/`.

### Images not showing in product grid

Product images are served by the backend at `http://localhost:8000/static/products/`. Make sure the backend is running and `download_products.py` has been run first.

---

## ⏱️ Performance Notes

| Operation | Time (free tier) |
|---|---|
| IDM-VTON (tops, 30 steps) | ~60–120 seconds |
| OOTDiffusion (bottoms/dresses) | ~30–60 seconds |
| ShoeVTON (shoes) | ~20–45 seconds |
| Groq clothing analysis | ~1–2 seconds |
| Backend overhead | <1 second |

Generation time depends on HuggingFace ZeroGPU queue load. During peak hours it can be longer.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `fastapi` | ≥0.111.0 | Web framework |
| `uvicorn[standard]` | ≥0.29.0 | ASGI server |
| `python-multipart` | ≥0.0.9 | File upload parsing |
| `gradio_client` | ≥0.16.0 | HuggingFace Space API calls |
| `Pillow` | ≥10.0.0 | Image processing |
| `python-dotenv` | ≥1.0.0 | `.env` file loading |
| `groq` | ≥0.9.0 | Llama 3.2 Vision API |
| `httpx` | (auto) | HTTP client with timeout control |
| `anyio` | (auto) | Async thread runner for blocking calls |

---

## 🗺️ Roadmap

- [ ] Full-body outfit try-on (shirt + pants together)
- [ ] User accounts with saved try-on history
- [ ] Background removal for cleaner garment images
- [ ] Mobile app (React Native / Expo)
- [ ] More product categories (jackets, dresses, accessories)
- [ ] Admin panel to add/remove products without code changes

---

## 📄 License

Open-source models used under their respective licenses:

- **IDM-VTON** — [CC BY-NC-SA 4.0](https://huggingface.co/yisol/IDM-VTON)
- **OOTDiffusion** — [CC BY-NC-SA 4.0](https://huggingface.co/OOTDiffusion/OOTDiffusion)
- **Kolors** — [Kolors Community License](https://huggingface.co/Kwai-Kolors/Kolors)

---

*Built with FastAPI · Gradio Client · IDM-VTON · OOTDiffusion · Groq · Pillow*
