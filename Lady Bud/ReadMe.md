# 🌸 Female Health Care Chatbot

A focused AI-powered chatbot built with **Streamlit** and **Groq** that answers female health-related questions in a kind, concise, and respectful manner.

---

## Overview

This app uses the **LLaMA 3.1 70B** model via the Groq API to provide quick, accurate responses to female health queries. The assistant is scoped strictly to female health topics — any off-topic questions are gracefully declined.

---

## Features

- 💬 Conversational Q&A on female health topics
- ⚡ Fast inference powered by Groq's LPU backend
- 🛡️ Topic-scoped system prompt — won't go off-topic
- 🖥️ Clean, minimal Streamlit UI

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| LLM | LLaMA 3.1 70B (via Groq) |
| Embeddings | FastEmbed |
| PDF Parsing | PyMuPDF (fitz) |
| Data Handling | Pandas, NumPy |

---

## Project Structure

```
female-health-chatbot/
├── app.py          # Main Streamlit application
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- A [Groq API key](https://console.groq.com/)

### Installation

```bash
git clone https://github.com/your-username/female-health-chatbot.git
cd female-health-chatbot
pip install -r requirements.txt
```

### Configuration

Open `app.py` and set your Groq API key:

```python
os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"
```

> **Note:** For production use, store your API key in a `.env` file or environment variable instead of hardcoding it.

### Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Usage

1. Type your female health-related question in the input box.
2. Hit Enter and wait briefly for the response.
3. The bot will answer concisely — or politely decline if the question is out of scope.

---

## Configuration

Key parameters in `app.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL` | `llama-3.1-70b-versatile` | Groq model to use |
| `TEMPERATURE` | `0` | Response determinism (0 = most consistent) |
| `MAX_TOKENS` | `4096` | Maximum response length |

---

## Requirements

```
streamlit
groq
fastembed
pymupdf
pandas
numpy
```

---

## Notes

- The chatbot maintains a fresh conversation context per query (stateless per submission).
- The system prompt enforces topic boundaries and sets a respectful, empathetic tone.
- PyMuPDF and FastEmbed are included as dependencies for potential RAG extensions (e.g., ingesting health documents).

---

