import json
from pathlib import Path

import faiss
import numpy as np

STORE_DIR = Path(__file__).parent / "faiss_store"
INDEX_FILE = STORE_DIR / "index.faiss"
META_FILE = STORE_DIR / "chunks.json"


def reset_and_store(chunks, embeddings):
    """Vectors ko FAISS index mein, aur chunk text/metadata ko JSON mein save karo."""
    STORE_DIR.mkdir(exist_ok=True)

    vectors = np.array(embeddings, dtype="float32")
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, str(INDEX_FILE))
    META_FILE.write_text(json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
    return index.ntotal


def search(query_embedding, k=4):
    """Sawal ke vector se sabse milte-julte k chunks dhoondo."""
    if not INDEX_FILE.exists() or not META_FILE.exists():
        raise FileNotFoundError("FAISS index nahi mila. Pehle /ingest chalayein.")

    index = faiss.read_index(str(INDEX_FILE))
    chunks = json.loads(META_FILE.read_text(encoding="utf-8"))

    q = np.array([query_embedding], dtype="float32")
    faiss.normalize_L2(q)
    scores, ids = index.search(q, k)

    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx == -1:
            continue
        c = chunks[idx]
        results.append({
            "text": c["text"],
            "section": c["section"],
            "page": c["page"],
            "score": round(float(score), 3),
        })
    return results