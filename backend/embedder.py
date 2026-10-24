from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts):
    """Text ki list ko vectors (numbers ki list) mein badlo."""
    return get_model().encode(texts, show_progress_bar=False).tolist()