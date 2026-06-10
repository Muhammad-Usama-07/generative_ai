# 👗 FitAI — AI Virtual Try-On

> Browse fashion. Pick a style. See it on **you** — before you buy it.

FitAI is a multi-page Streamlit web app that lets users virtually try on clothing, shoes, and accessories using open-source AI models. No GPU required. No paid APIs. Completely free to run.

---

## ✨ Features

- **Category-aware try-on** — separate AI models for Tops, Bottoms, Dresses, Shoes, and Accessories
- **AI clothing analysis** — Groq (Llama 3.2 Vision) reads the uploaded garment and extracts color, fit, fabric, and category
- **Before/after comparison** — side-by-side view of original vs try-on result
- **Download result** — save the generated image as PNG
- **Live debug panel** — in-UI log viewer to inspect exactly what each model receives
- **Dark fashion-forward UI** — editorial aesthetic with warm gold accents
- **Landing page** — full product catalog with Men's accessories section and category filters

---

## 🧠 AI Stack (100% Free & Open Source)

| Category | Model | HuggingFace Space |
|---|---|---|
| 👕 Tops | IDM-VTON | `yisol/IDM-VTON` |
| 👖 Bottoms | OOTDiffusion (Lower-body) | `Nymbo/Virtual-Try-On` |
| 👗 Dresses | OOTDiffusion (Dress) | `Nymbo/Virtual-Try-On` |
| 👟 Shoes | ShoeVTON | `franciszzz/virtual-try-on-shoe` |
| 🧣 Accessories | Kolors Virtual Try-On | `Kwai-Kolors/Kolors-Virtual-Try-On` |
| 🤖 Vision Analysis | Llama 3.2 Vision | Groq API (free tier) |

---

## 🗂️ Project Structure

```
fitai/
├── 1_Home.py                   # Landing page (entry point)
├── pages/
│   └── 2_Try_On.py             # Virtual try-on page
├── backend/
│   ├── __init__.py
│   ├── analyze_cloth.py        # Groq vision analysis
│   ├── generate.py             # Model routing + HuggingFace calls
│   └── logger.py               # Centralized logging
├── .streamlit/
│   └── config.toml             # Dark theme + layout config
├── .env.example                # API key template
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone or download the project

```cmd
cd path\to\your\projects
```

### 2. Install dependencies

```cmd
pip install -r requirements.txt
```

### 3. Configure API keys

Copy the example env file and fill in your keys:

```cmd
copy .env.example .env
notepad .env
```

Your `.env` should look like this:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
```

**Getting your free API keys:**

| Key | Where to get it | Cost |
|---|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) | Free |
| `HF_TOKEN` | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) → New token → Read | Free |

> **Note:** `HF_TOKEN` is optional but highly recommended. Without it you hit HuggingFace's anonymous ZeroGPU quota much faster (~60s/day). A logged-in token gives significantly more free GPU time.

### 4. Run the app

```cmd
streamlit run 1_Home.py
```

Open your browser at `http://localhost:8501`

---

## 🚀 How to Use

1. Open the app and browse the landing page catalog
2. Click **"✨ Open Try-On"** (bottom-right floating button) or the **"Try it free"** nav button
3. On the Try-On page, select a **category** (Tops / Bottoms / Shoes / Dresses / Accessories)
4. Upload your **full-body photo**
5. Upload the **clothing/item image** you want to try on
6. Groq automatically analyzes the item (color, fit, fabric)
7. Adjust **denoising steps** and **seed** if desired
8. Click **"✦ Try On"** and wait for the result
9. View the **before/after comparison** and download the result

---

## 🐛 Troubleshooting

### `set_page_config() can only be called once`
`set_page_config()` must only exist in `1_Home.py`. Never add it to files inside `pages/`.

### `use_container_width` error on `st.image()`
Upgrade Streamlit or use `use_column_width=True` instead:
```cmd
pip install --upgrade streamlit
```

### ZeroGPU quota exceeded
```
You have exceeded your ZeroGPU quota (60s requested vs. 79s left)
```
- Add `HF_TOKEN` to your `.env` for more quota
- Lower denoising steps to `20`
- Wait 24 hours for quota reset

### `Repository Not Found` for OOTDiffusion
`OOTDiffusion/OOTDiffusion` is a **model repo**, not a Gradio Space. The correct Space is `Nymbo/Virtual-Try-On`. Do not change the space names in `generate.py`.

### Bottoms/Shoes applying to wrong body area
This happens when IDM-VTON is used for non-top categories. IDM-VTON only supports upper body. The routing in `generate.py` handles this automatically — verify the debug logs show the correct model being selected.

---

## 📋 Debug Logs

FitAI logs every AI call to two places:

- **In the UI** — scroll to the bottom of the Try-On page → click **"🛠️ Debug Logs"**
- **In the terminal** — live output where you ran `streamlit run`
- **In the file** — `fitai_debug.log` in the project root

Example log output:
```
[14:32:01] INFO  | TRY-ON REQUEST
[14:32:01] INFO  |   Category      : bottoms
[14:32:01] INFO  |   Description   : slim-fit black trousers, cotton, regular
[14:32:01] INFO  | MODEL SELECTED  : Nymbo/Virtual-Try-On (Lower-body)
[14:32:01] INFO  | SPACE ATTEMPT #1 : Nymbo/Virtual-Try-On
[14:32:01] INFO  |   category      = 'Lower-body'
[14:32:54] INFO  | SPACE SUCCESS   : Nymbo/Virtual-Try-On
[14:32:54] INFO  | RESULT IMAGE    : 398x600 px
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | ≥1.35.0 | Web UI framework |
| `groq` | ≥0.9.0 | Llama 3.2 Vision API client |
| `gradio_client` | ≥0.16.0 | HuggingFace Space API calls |
| `Pillow` | ≥10.0.0 | Image processing |
| `python-dotenv` | ≥1.0.0 | `.env` file loading |

---

## 🗺️ Roadmap

- [ ] Connect landing page product cards directly to try-on with pre-selected items
- [ ] Add men's category (separate male/female model routing)
- [ ] Result gallery — save and compare multiple try-ons
- [ ] Background removal for cleaner garment images
- [ ] Mobile-responsive layout

---

## 📄 License

This project uses open-source models under their respective licenses:
- IDM-VTON — [CC BY-NC-SA 4.0](https://huggingface.co/yisol/IDM-VTON)
- OOTDiffusion — [CC BY-NC-SA 4.0](https://huggingface.co/OOTDiffusion/OOTDiffusion)
- Kolors — [Kolors Community License](https://huggingface.co/Kwai-Kolors/Kolors)

---

*Built with Streamlit · Groq · OOTDiffusion · IDM-VTON · Kolors*