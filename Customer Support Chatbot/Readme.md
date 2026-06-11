# 🤖 Customer Support Chatbot

A RAG-based (Retrieval-Augmented Generation) customer support chatbot built with **Streamlit**, **Groq (LLaMA 3.1)**, and **FastEmbed**. The bot answers customer queries using knowledge extracted from a PDF document.

---

## 📋 Features

- 📄 **PDF Knowledge Base** — Extracts and indexes content from a PDF file
- 🔍 **Semantic Search** — Uses FastEmbed embeddings + cosine distance to retrieve relevant context
- 🧠 **LLM-Powered Responses** — Powered by Groq's `llama-3.1-70b-versatile` model
- 💬 **Chat UI** — Clean Streamlit interface with chat history
- ⚡ **Fast & Free** — Uses free-tier Groq API

---

## 🗂️ Project Structure

```
customer-support-chatbot/
│
├── app.py                  # Main Streamlit application
├── your_knowledge.pdf      # PDF knowledge base (add your own)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/customer-support-chatbot.git
cd customer-support-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Key

Get a free API key from [Groq Console](https://console.groq.com/) and set it in `app.py`:

```python
os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"
```

Or set it as an environment variable:

```bash
# Windows
set GROQ_API_KEY=your_groq_api_key_here

# Linux/macOS
export GROQ_API_KEY=your_groq_api_key_here
```

### 4. Add Your PDF

Place your knowledge base PDF in the project directory and update the path in `app.py`:

```python
pdf_text = read_pdf("your_knowledge.pdf")
```

Also update the website/business name in the system prompt:

```python
website_name = "Your Business Name"
```

### 5. Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📦 Requirements

```
streamlit
groq
fastembed
pymupdf
pandas
numpy
```

Install all at once:

```bash
pip install streamlit groq fastembed pymupdf pandas numpy
```

---

## 🔧 Configuration

| Variable | Description | Default |
|---|---|---|
| `MODEL` | Groq model to use | `llama-3.1-70b-versatile` |
| `TEMPERATURE` | Response creativity (0 = deterministic) | `0` |
| `MAX_TOKENS` | Max tokens in response | `4096` |
| `k` in `retrieve_context` | Number of context chunks retrieved | `3` |

---

## 🧠 How It Works

```
User Query
    │
    ▼
Embed Query (FastEmbed)
    │
    ▼
Nearest Neighbor Search (NumPy L2 Distance)
    │
    ▼
Retrieve Top-K Context from PDF
    │
    ▼
Build Prompt (System + Context + Query)
    │
    ▼
Groq LLaMA 3.1 → Response
    │
    ▼
Display in Streamlit Chat UI
```

---

## ⚠️ Known Limitations

- The entire PDF is treated as a single document chunk — for large PDFs, consider splitting into smaller chunks for better retrieval accuracy.
- Conversation history is not persisted across page refreshes.
- `website_name` must be defined before the `SYSTEM_PROMPT` is declared.

---

## 🛠️ Planned Improvements

- [ ] Chunk-based PDF splitting for better semantic search
- [ ] Multi-turn conversation memory
- [ ] Support for multiple PDF uploads
- [ ] Streaming responses
- [ ] Docker support

---

## 📄 License

MIT License. Feel free to use and modify.