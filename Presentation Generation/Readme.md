# 🎯 AI-Powered Presentation Generator

A **Streamlit web application** that leverages **Groq's LLaMA 3.1 70B** model to interactively generate professional PowerPoint presentations — slide by slide, with user-guided title and content selection.

---

## Features

- **AI-generated slide titles** — 3 variations per slide to choose from
- **AI-generated slide content** — 2 content versions per slide (detail + bullet points)
- **15 presentation categories** — Business, Motivational, Academic, Sales, Storytelling, and more
- **Interactive Streamlit UI** — step-by-step guided flow through topic setup, slide building, and download
- **Progress tracking** — visual progress bar and sidebar summary as you build each slide
- **PPTX download** — one-click download of the generated `.pptx` file directly from the browser
- **Powered by Groq API** — fast inference via `llama-3.1-70b-versatile`

---

## Tech Stack

| Component | Library/Tool |
|-----------|-------------|
| UI Framework | `streamlit` |
| LLM Backend | Groq API (`llama-3.1-70b-versatile`) |
| Presentation | `python-pptx` |
| Environment | `python-dotenv` |

---

## Installation

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd <repo-folder>
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your Groq API key**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

---

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

**Step-by-step walkthrough:**

1. **Config screen** — enter a topic, select a presentation category, and choose the number of slides
2. **Slide screens (repeated per slide)** — for each slide:
   - Pick one of 3 AI-generated title options
   - Optionally enter a description to guide content
   - Click **Generate Content** to get 2 content versions
   - Pick your preferred version
   - Click **Next Slide** (or **Finish** on the last slide)
3. **Download screen** — preview the slide list and download the `.pptx` file directly from the browser

---

## Presentation Categories

| # | Category |
|---|----------|
| 1 | Business |
| 2 | Motivational |
| 3 | Persuasive |
| 4 | Demonstrative |
| 5 | Informative |
| 6 | Storytelling |
| 7 | Academic |
| 8 | Sales |
| 9 | Instructional |
| 10 | Progress |
| 11 | Coach Style |
| 12 | Connector Style |
| 13 | Decision-Making |
| 14 | Instructor Style |
| 15 | Problem Solving |

---

## Project Structure

```
.
├── app.py              # Streamlit UI — screen router and all screen functions
├── generator.py        # Core logic — title/content generation and PPTX creation
├── llm.py              # Groq API client and call_model() function
├── state.py            # Session state initialization
├── config.py           # Constants — model, font sizes, categories, system prompt
├── requirements.txt    # Python dependencies
├── .env                # Groq API key (not committed)
└── README.md
```

---

## Configuration

All constants are defined in `config.py`:

```python
MODEL = "llama-3.1-70b-versatile"   # Groq model
TEMPERATURE = 0                      # Deterministic output
MAX_TOKENS = 4096                    # Max response length
TITLE_FONT_SIZE = Pt(30)             # Slide title font size
SLIDE_FONT_SIZE = Pt(16)             # Slide body font size
```

---

## App Flow (State Machine)

The UI is driven by `st.session_state.step`:

```
step = 0  →  Config screen      (topic, category, slide count)
step = 1  →  Slide screen       (repeated for each slide)
step = 2  →  Download screen    (preview + .pptx download)
```

Key session state keys:

| Key | Purpose |
|-----|---------|
| `step` | Current screen (0, 1, or 2) |
| `current_slide` | Which slide is being built |
| `titles` | 3 AI-suggested titles for the current slide |
| `contents` | 2 AI-generated content versions for the current slide |
| `presen_titles` | Accumulated finalized titles |
| `presen_content` | Accumulated finalized content |

---

## Notes

- The PPTX is generated in memory (`BytesIO`) — no files are written to disk.
- Topic input is sanitized to remove non-alphabetical characters.
- A **Start Over** button is available at any point to reset session state.

---

## Future Improvements

- [ ] Custom slide themes and color schemes
- [ ] Image insertion per slide (via stock photo API)
- [ ] Local LLM support via `ctransformers` (LLaMA GGUF)
- [ ] RAG-based content generation from uploaded documents
- [ ] Export to Google Slides
- [ ] Multi-language presentation support

---
