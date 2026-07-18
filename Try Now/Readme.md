# 👗 FitAI — AI Virtual Try-On

> Upload your photo. Pick any item. See it on **you** — before you buy.

FitAI is a full-stack AI virtual try-on web application. Users upload a personal photo, browse a product catalog, and see AI-generated results showing exactly how a garment looks on their body — powered entirely by free, open-source models with zero paid APIs.

---

## ✨ Features

- **Virtual Try-On** — AI composites any clothing item onto the user's photo in seconds
- **Product Catalog** — Browse tops, bottoms, shoes and caps with real product images
- **Category-aware model routing** — Dedicated AI model per category for accurate region masking
- **Multi-select with smart validation** — Prevents invalid combinations (e.g. multiple tops at once)
- **Before/After comparison** — Interactive drag slider + 3-panel Original + Product = Result view
- **Full outfit upsell block** — After upper-body try-on, prompts user to try the complete outfit
- **Sign-up gate** — Bottoms, shoes, and caps require an account (upper-body try-on is free)
- **FastAPI backend** — REST API with product catalog, result caching, health check, Swagger UI
- **9-step pipeline debugger** — `debug_tryon.py` isolates and validates every layer independently
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

## 🛠️ Tech Stack

### Backend
`Python 3.11` · `FastAPI` · `Uvicorn` · `gradio_client` · `Pillow` · `httpx` · `anyio` · `python-dotenv` · `Groq SDK`

### AI Models
`IDM-VTON` · `OOTDiffusion` · `ShoeVTON` · `Kolors VTO` · `Llama 3.2 Vision` · `HuggingFace ZeroGPU`

### Frontend
`HTML5` · `CSS3` · `Vanilla JavaScript (ES2022)` · `Fetch API` · `FormData` · `AbortController` · `FileReader API`

---

## 🗂️ Project Structure

```
FitAI/
│
├── frontend/                       ← open in browser (never double-click)
│   ├── index.html                  ← landing page — catalog, before/after slider, how it works
│   ├── tryon.html                  ← try-on page — photo upload, product picker, result view
│   └── serve_frontend.py           ← serves frontend at http://localhost:5500
│
└── backend/                        ← Python FastAPI server
    ├── main.py                     ← FastAPI app, all endpoints
    ├── tryon.py                    ← IDM-VTON core logic, singleton client, retry logic
    ├── products.py                 ← product catalog (single source of truth)
    ├── store.py                    ← thread-safe in-memory result store with TTL expiry
    ├── download_products.py        ← downloads all 11 product images (run once)
    ├── debug_tryon.py              ← 9-step end-to-end pipeline debugger
    ├── test_tryon.py               ← CLI test tool (no server needed)
    ├── requirements.txt
    ├── .env                        ← your API keys (created from .env.example)
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
- Free HuggingFace account — [huggingface.co](https://huggingface.co)
- Free Groq account — [console.groq.com](https://console.groq.com)

---

### Step 1 — Install dependencies

```cmd
cd FitAI/backend
pip install -r requirements.txt
```

---

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

> `HF_TOKEN` is required. Without it, HuggingFace's anonymous ZeroGPU quota is exhausted in ~60 seconds/day. A logged-in token gives significantly more free GPU time.

---

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

---

### Step 4 — Verify the pipeline (recommended before first run)

```cmd
:: Copy any person photo here first
copy path\to\any_photo.jpg static\test_person.jpg

:: Run all 9 diagnostic steps
python debug_tryon.py
```

All 9 steps should pass and a `debug_result.jpg` will appear in `backend/`. Open it to confirm the AI result looks correct before starting the server.

---

## 🚀 Running the App

Open **two terminals** and keep both running:

**Terminal 1 — Backend**
```cmd
cd FitAI/backend
python main.py
```

Expected startup output:
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

Expected output:
```
Open in browser: http://localhost:5500/tryon.html
```

**Open in browser:**

```
http://localhost:5500/tryon.html
```

> ⚠️ **Never open `tryon.html` by double-clicking it.** The `file://` URL origin blocks `fetch()` calls to the backend in modern browsers. Always use `http://localhost:5500/tryon.html`.

---

## 🌐 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Server status, token check, missing image list |
| `GET` | `/api/products` | All 11 products with local image URLs |
| `POST` | `/api/tryon` | Run try-on by `product_id` (uses saved local garment image) |
| `POST` | `/api/tryon/upload` | Run try-on with a custom uploaded garment image |
| `GET` | `/api/result/{id}` | Fetch a previously generated result by UUID |
| `GET` | `/docs` | Interactive Swagger UI |

### POST `/api/tryon` — Main endpoint

**Request (`multipart/form-data`):**

| Field | Type | Description |
|---|---|---|
| `person_image` | File | JPG/PNG/WEBP photo of the person |
| `product_id` | string | Product ID from `/api/products` e.g. `"white_tee"` |
| `denoise_steps` | int | 20–50, default 30. Higher = better quality, slower |
| `seed` | int | Reproducibility seed, default 42 |

**Response (`application/json`):**

```json
{
  "result_id":    "550e8400-e29b-41d4-a716-446655440000",
  "result_b64":   "iVBORw0KGgo...",
  "person_b64":   "iVBORw0KGgo...",
  "garment_b64":  "iVBORw0KGgo...",
  "product_name": "Classic White Tee",
  "product_id":   "white_tee",
  "duration_sec": 117.4,
  "model":        "yisol/IDM-VTON"
}
```

**Quick checks:**
```
http://localhost:8000/api/health      ← token status + missing images
http://localhost:8000/api/products    ← full product catalog JSON
http://localhost:8000/docs            ← Swagger interactive docs
```

---

## 🧪 Testing Without the UI

```cmd
:: Full 9-step pipeline diagnostic — run this first
python debug_tryon.py

:: Quick CLI test with your own images
python test_tryon.py --person static\test_person.jpg --garment static\products\white_tee.jpg

:: Custom description
python test_tryon.py --person me.jpg --garment shirt.jpg --desc "white cotton t-shirt" --output result.jpg
```

---

## 🐛 Troubleshooting

### `ReadTimeout: The read operation timed out`

The model finished generating but downloading the result image from HuggingFace CDN timed out — a transient network issue, not a code bug.

- The backend auto-retries twice before giving up
- Try again — it often succeeds on the second attempt
- If persistent: try a different network, disable VPN, or run during off-peak hours

---

### `ZeroGPU quota exceeded`

```
You have exceeded your ZeroGPU quota (60s requested vs. 79s left)
```

- Ensure `HF_TOKEN` is set in `.env` — logged-in tokens have far higher quota
- Wait 24 hours for quota to reset
- Lower `denoise_steps` to `20` to use less GPU time per generation

---

### `person_image must be JPG/PNG/WEBP, got 'image/octet-stream'`

The browser is sending the file with an unrecognized MIME type. Rename the file to `.jpg` or `.png` and try again.

---

### `Product not found`

The `data-id` attribute in `tryon.html` doesn't match a product `id` in `products.py`. Values are case-sensitive — check they match exactly.

---

### Result image doesn't appear in the UI

1. Open browser DevTools (F12) → **Network** tab
2. Click the failed `tryon` request → **Response** tab
3. The `"detail"` field in the JSON shows the actual Python error
4. Run `python debug_tryon.py` — if all 9 steps pass, the backend is fine and the issue is in JavaScript

---

### Images not showing in product grid

Product images are served by the backend at `http://localhost:8000/static/products/`. Make sure the backend is running and `python download_products.py` has been run.

---

### `set_page_config() can only be called once` (Streamlit version only)

`set_page_config()` must only exist in `1_Home.py`. Never add it to files inside `pages/`.

---

## ⏱️ Performance Notes

Generation time depends on HuggingFace ZeroGPU queue load and your network speed for downloading the result image.

| Operation | Free tier estimate |
|---|---|
| IDM-VTON — tops (30 steps) | ~60–120 seconds |
| OOTDiffusion — bottoms / dresses | ~30–60 seconds |
| ShoeVTON — shoes | ~20–45 seconds |
| Groq clothing analysis | ~1–2 seconds |
| Backend overhead | < 1 second |

The frontend uses a **3-minute `AbortController` timeout** on the `fetch()` call to accommodate the longest possible generation time without the browser silently dropping the connection.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `fastapi` | ≥0.111.0 | Web framework |
| `uvicorn[standard]` | ≥0.29.0 | ASGI server |
| `python-multipart` | ≥0.0.9 | Multipart file upload parsing |
| `gradio_client` | ≥0.16.0 | HuggingFace Space API calls |
| `Pillow` | ≥10.0.0 | Image loading, conversion, base64 encoding |
| `python-dotenv` | ≥1.0.0 | `.env` file loading |
| `groq` | ≥0.9.0 | Llama 3.2 Vision API client |
| `httpx` | (auto) | HTTP client used by gradio_client |
| `anyio` | (auto) | Async thread runner for blocking AI calls |

---

## 💡 Key Engineering Decisions

**Singleton Gradio client** — The `Client("yisol/IDM-VTON")` is created once at module load and reused across all requests. Recreating it per-request re-triggers the full Gradio handshake (config fetch, queue negotiation) adding ~5-10s of overhead and causing intermittent failures under concurrent load.

**Thread offloading with anyio** — `client.predict()` blocks for 60–120 seconds. Calling it directly inside an `async def` FastAPI route blocks the entire event loop. `anyio.to_thread.run_sync()` moves it to a background thread so the server remains responsive.

**Product-ID based try-on** — Instead of having the frontend fetch the garment image from Unsplash and re-upload it, it sends a `product_id` string and the backend reads the locally saved image from `static/products/`. This avoids CORS issues, external network dependency, and ensures the exact same image the user sees in the catalog is what gets sent to the AI model.

**AbortController with 3-minute timeout** — Browser `fetch()` has no built-in timeout. Without `AbortController`, a dropped connection after 60s would silently fail with no error shown to the user. The 3-minute window safely covers IDM-VTON's worst-case generation time.

---

## 🗺️ Roadmap

- [ ] Full-body outfit try-on (shirt + pants simultaneously)
- [ ] User accounts with saved try-on history
- [ ] Background removal for cleaner garment images
- [ ] Mobile app (React Native / Expo)
- [ ] More product categories (jackets, outerwear, accessories)
- [ ] Admin panel to add/remove products without touching code

---

## 📄 License

Open-source models used under their respective licenses:

- **IDM-VTON** — [CC BY-NC-SA 4.0](https://huggingface.co/yisol/IDM-VTON)
- **OOTDiffusion** — [CC BY-NC-SA 4.0](https://huggingface.co/OOTDiffusion/OOTDiffusion)
- **Kolors** — [Kolors Community License](https://huggingface.co/Kwai-Kolors/Kolors)

---

*Built with FastAPI · Gradio Client · IDM-VTON · OOTDiffusion · Groq · Pillow*
