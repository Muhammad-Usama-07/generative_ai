# 🎯 AI-Powered Presentation Generator

A CLI-based Python application that leverages **Groq's LLaMA 3.1 70B** model to interactively generate professional PowerPoint presentations — slide by slide, with user-guided title and content selection.

---

## Features

- **AI-generated slide titles** — 3 variations per slide to choose from
- **AI-generated slide content** — 2 content versions per slide (detail + bullet points)
- **15 presentation categories** — Business, Motivational, Academic, Sales, Storytelling, and more
- **Interactive CLI workflow** — user picks topics, categories, slide count, titles, content, and optional descriptions
- **PPTX output** — generates a `.pptx` file using `python-pptx`
- **Powered by Groq API** — fast inference via `llama-3.1-70b-versatile`

---

## Tech Stack

| Component | Library/Tool |
|-----------|-------------|
| LLM Backend | Groq API (`llama-3.1-70b-versatile`) |
| Presentation | `python-pptx` |
| Environment | `python-dotenv` |
| Embeddings (optional) | `fastembed` |
| Data utilities | `pandas`, `numpy` |

---

## Installation

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd <repo-folder>
```

**2. Install dependencies**
```bash
pip install groq python-pptx python-dotenv fastembed pandas numpy
```

**3. Set up your Groq API key**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Or set it directly in the script (not recommended for production):
```python
os.environ["GROQ_API_KEY"] = "your_key_here"
```

---

## Usage

Run the script from your terminal:
```bash
python app.py
```

**Step-by-step walkthrough:**

1. **Enter a topic** — e.g., `Artificial Intelligence in Healthcare`
2. **Select a category** — choose from 15 presentation styles (e.g., `5` for Informative)
3. **Enter number of slides** — e.g., `5`
4. **For each slide:**
   - Pick one of 3 AI-generated title options
   - Optionally enter a description to guide content
   - Pick one of 2 AI-generated content versions
5. **Output** — a file named `test_generated_presentation.pptx` is saved in the project directory

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
├── app.py                        # Main script
├── .env                          # Groq API key (not committed)
├── test_generated_presentation.pptx  # Output file (generated at runtime)
└── README.md
```

---

## Configuration

Key constants at the top of `app.py`:

```python
MODEL = "llama-3.1-70b-versatile"   # Groq model
TEMPERATURE = 0                      # Deterministic output
MAX_TOKENS = 4096                    # Max response length
TITLE_FONT_SIZE = Pt(30)             # Slide title font size
SLIDE_FONT_SIZE = Pt(16)             # Slide body font size
```

---

## Notes

- The last slide is always treated as the **"second last"** thematically — useful for conclusions/summaries.
- Topic input is sanitized to remove non-alphabetical characters.
- The `fastembed`, `ctransformers`, and `pandas`/`numpy` imports are present for future extensibility (e.g., local LLM, RAG-based content) but are not actively used in the current flow.

---

## Future Improvements

- [ ] Streamlit UI (interactive web front-end)
- [ ] Image insertion per slide
- [ ] Custom themes and color schemes
- [ ] Local LLM support via `ctransformers` (LLaMA GGUF)
- [ ] RAG-based content generation from uploaded documents
- [ ] Export to Google Slides

---
