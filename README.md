# GlucoGuide

**A RAG-Based Healthcare Chatbot for Type 2 Diabetes Question Answering**

GlucoGuide answers questions about Type 2 Diabetes using only the content of a
PDF document. Every answer is grounded in retrieved text and shows its sources
(section and page number), which reduces hallucination.

> Educational project. Not a substitute for professional medical advice.

## How It Works (RAG Pipeline)

```
PDF -> Load (PyMuPDF) -> Sections -> Chunks -> Embeddings (Sentence Transformers)
    -> FAISS index

Question -> Embedding -> FAISS top-4 chunks -> Ollama LLM (context only) -> Answer + Sources
```

| Stage | File | Tool |
|---|---|---|
| Data loading | `backend/loader.py` | PyMuPDF |
| Chunking (sections, then 120-word chunks, 25-word overlap) | `backend/chunker.py` | Python |
| Embedding (384-dim vectors) | `backend/embedder.py` | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector store and retrieval (cosine similarity) | `backend/vector_db.py` | FAISS |
| Answer generation | `backend/llm.py` | Ollama (`llama3.2`, local) |
| API | `backend/main.py` | FastAPI |
| UI | `frontend/` | React (Vite) |

## Project Structure

```
ResearchMate/
├── backend/
│   ├── data/type2_diabetes_review.pdf
│   ├── loader.py  chunker.py  embedder.py
│   ├── vector_db.py  llm.py  main.py
├── frontend/          (React app)
└── README.md
```

## Run Locally

1. Install Ollama and run `ollama pull llama3.2`.
2. Backend (from `backend/`, with the virtual environment active):
   ```
   uvicorn main:app --reload
   ```
3. Open `http://127.0.0.1:8000/docs`, run `POST /ingest` once.
4. Frontend (from `frontend/`):
   ```
   npm run dev
   ```
5. Open `http://localhost:5173`.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check that the server is running |
| POST | `/ingest` | Load PDF, chunk, embed, build FAISS index |
| POST | `/ask` | Body: `{"question": "..."}`. Returns answer and sources |

## Limitations and Future Improvements

- Embedding model works best with English questions.
- Top-4 chunks are always shown as sources, even if some are less relevant.
  A similarity threshold can filter them.
- Single document only. Multi-PDF upload can be added.
- Chunking is word-based. Sentence-aware chunking can improve quality.