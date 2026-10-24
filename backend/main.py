from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from loader import load_pdf
from chunker import chunk_pages
from embedder import embed_texts
from vector_db import reset_and_store, search
from llm import generate_answer

PDF_PATH = str(Path(__file__).parent / "data" / "type2_diabetes_review.pdf")

app = FastAPI(
    title="GlucoGuide API",
    description="RAG-based healthcare chatbot for Type 2 Diabetes",
)

# React frontend ko backend se baat karne ki ijazat
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok", "app": "GlucoGuide"}


@app.post("/ingest")
def ingest():
    """Data Loading -> Chunking -> Embedding -> Vector DB."""
    pages = load_pdf(PDF_PATH)
    chunks = chunk_pages(pages)
    embeddings = embed_texts([c["text"] for c in chunks])
    count = reset_and_store(chunks, embeddings)
    return {"pages": len(pages), "chunks_stored": count}


@app.post("/ask")
def ask(body: Question):
    """Sawal -> Embedding -> Search -> LLM -> Answer + Sources."""
    q_embedding = embed_texts([body.question])[0]
    try:
        results = search(q_embedding, k=4)
    except Exception:
        raise HTTPException(status_code=400, detail="Pehle POST /ingest chalayein.")
    answer = generate_answer(body.question, results)
    sources = [
        {"section": r["section"], "page": r["page"], "score": r["score"]}
        for r in results
    ]
    return {"answer": answer, "sources": sources}