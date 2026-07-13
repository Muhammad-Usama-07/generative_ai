# llm.py
from groq import Groq
from config import MODEL, TEMPERATURE, MAX_TOKENS, SYSTEM_PROMPT
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_model(prompt: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content