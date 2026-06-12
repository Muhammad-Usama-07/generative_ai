# 📧 Email Draft Generator API

A FastAPI-powered backend that uses **Groq's LLaMA 3** to auto-generate professional workplace emails (leave requests, permission letters, etc.) and answer general queries — all via a simple REST API.

---

## Features

- **`/submit/`** — Generate a formal email draft (e.g. leave request, half-day application) based on employee details and date range
- **`/ask_anything/`** — Send any free-form query to LLaMA 3 and get a response
- Powered by **Groq** inference (fast LLaMA 3 8B)
- Built with **FastAPI** + **Pydantic** for clean validation

---

## Tech Stack

| Layer | Tool |
|---|---|
| Framework | FastAPI |
| LLM Provider | Groq (`llama3-8b-8192`) |
| Validation | Pydantic |
| Server | Uvicorn |

---

## Getting Started

### 1. Install dependencies

```bash
pip install fastapi uvicorn groq pydantic
```

### 2. Set your Groq API key

In `main.py`, replace the empty string with your key:

```python
os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"
```

Or set it as an environment variable before running:

```bash
export GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

The API will be live at `http://localhost:8000`.

---

## API Reference

### `POST /submit/`

Generates a formal email based on employee form inputs.

**Form fields:**

| Field | Description | Example |
|---|---|---|
| `emp_name` | Employee full name | `Ali Hassan` |
| `request_type` | Type of email | `leave request` |
| `date_range_start` | Start date | `2024-06-10` |
| `date_range_end` | End date | `2024-06-12` |
| `request_day_type` | Full day / half day | `full day` |
| `Subj` | Email subject | `Family emergency` |

**Response:** Generated email string (trimmed to start from the subject line) + the prompt used.

---

### `POST /ask_anything/`

Send any query and get a plain-text LLM response.

**Form fields:**

| Field | Description |
|---|---|
| `query` | Any question or instruction |

**Response:** Plain text response from LLaMA 3.

---

## Example Usage (cURL)

```bash
# Generate a leave request email
curl -X POST http://localhost:8000/submit/ \
  -F "emp_name=Ali Hassan" \
  -F "request_type=leave request" \
  -F "date_range_start=2024-06-10" \
  -F "date_range_end=2024-06-12" \
  -F "request_day_type=full day" \
  -F "Subj=Family Emergency"

# Ask anything
curl -X POST http://localhost:8000/ask_anything/ \
  -F "query=Write a short professional bio for a software engineer"
```

---

## Interactive Docs

FastAPI auto-generates Swagger UI at:

```
http://localhost:8000/docs
```

---

## Notes

- The `/submit/` endpoint strips everything before the "Subj" line in the LLM response for a clean email output.
- LLM parameters: `temperature=1`, `max_tokens=1024`, `top_p=1`, streaming enabled.
- Make sure not to commit your `GROQ_API_KEY` to version control — use environment variables or a `.env` file in production.

---

