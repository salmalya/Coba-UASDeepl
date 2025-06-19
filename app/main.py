# app/main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.retriever import build_faiss_index, get_embedding
from app.kg_retriever import query_graph
import numpy as np
import requests
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Load .env untuk ambil HUGGINGFACE_API_KEY
load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = "HuggingFaceH4/zephyr-7b-beta"  # Model yang tersedia di API

app = FastAPI()


# Mount folder static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Endpoint untuk menampilkan halaman HTML
@app.get("/")
async def serve_homepage():
    return FileResponse("app/static/index.html")

# Baca data dari txt file
with open("data/bps_clean.txt", "r", encoding="utf-8") as f:
    texts = f.readlines()

# Bangun FAISS index dari embedding
index, texts, vectors = build_faiss_index(texts)

# Pydantic schema untuk input JSON
class QuestionRequest(BaseModel):
    question: str

@app.post("/query")
async def query(request: QuestionRequest):
    question = request.question

    # Embedding pertanyaan
    q_embed = get_embedding(question)

    # Cari top-3 context terdekat
    D, I = index.search(np.array([q_embed]).astype('float32'), k=3)
    context = "\n".join([texts[i] for i in I[0]])

    # Gabungkan ke prompt
    full_prompt = f"""
Berikut adalah informasi dari data statistik:
{context}

Jawab pertanyaan berikut hanya menggunakan informasi di atas.  
Jawaban maksimal 1 kalimat.  
Jika tidak ditemukan jawaban, balas: "Tidak ada informasi yang cukup untuk menjawab pertanyaan ini."

Pertanyaan:
{question}
"""

    # Kirim ke HuggingFace Inference API
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": full_prompt,
        "parameters": {"max_new_tokens": 100}
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return {"error": f"HuggingFace API error: {response.text}"}

    result = response.json()
    generated_text = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
    answer_line = ""
    import re

    # Coba ekstrak jawaban setelah kata "Jawaban:"
    match = re.search(r"Jawaban:\s*(.*)", generated_text, re.IGNORECASE)
    if match:
        answer_line = match.group(1).strip()
    else:
        # Fallback jika gagal
        lines = [l.strip() for l in generated_text.splitlines() if l.strip()]
        answer_line = lines[-1] if lines else "Tidak ada jawaban dari model."


    if not answer_line:
        answer_line = "Tidak ada jawaban dari model."

    return {
        "answer": answer_line,
        "context_used": context
    }

@app.post("/query-kg")
async def query_kg(request: QuestionRequest):
    question = request.question
    context, relasi = query_graph(question)

    prompt = f"""
Berikut adalah potongan struktur knowledge graph yang berisi fakta-fakta:
{chr(10).join(relasi)}

Jawablah pertanyaan berikut hanya berdasarkan fakta yang tersedia di atas.
Jawaban hanya berupa **angka dan satuan** yang persis ada di atas, misalnya '9.47 juta'.
**Jangan tambahkan interpretasi, konversi, atau bentuk angka lain.**
Jawaban maksimal 1 kalimat.

Pertanyaan:
{question}
    """

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 80}
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return {"error": f"HuggingFace API error: {response.text}"}

    result = response.json()
    generated_text = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "").strip()
    answer_line = ""

    # Ambil baris terakhir sebagai jawaban
    for line in reversed(generated_text.splitlines()):
        line = line.strip()
        if line and not line.lower().startswith("pertanyaan"):
            answer_line = line
            break

    if not answer_line:
        answer_line = "Tidak ada jawaban dari model."

    return {
        "answer": answer_line,
        "graph_relations": relasi,
        "raw_context": context
    }
