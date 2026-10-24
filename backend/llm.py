import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

SYSTEM_PROMPT = (
    "You are GlucoGuide, a healthcare assistant for Type 2 Diabetes. "
    "Answer ONLY using the provided context. "
    "If the answer is not in the context, reply exactly: "
    "'This information is not available in the document.' "
    "Keep the answer clear and short. Do not invent facts."
)


def generate_answer(question, chunks):
    context = "\n\n".join(
        f"[Section: {c['section']} | Page {c['page']}]\n{c['text']}" for c in chunks
    )
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "stream": False,
                "options": {"temperature": 0.2},
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            },
            timeout=300,
        )
        if resp.status_code != 200:
            return f"Ollama error {resp.status_code}: {resp.text[:300]}"
        return resp.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "Ollama chal nahi raha. Ollama app kholein aur dobara try karein."
    except Exception as e:
        return f"LLM call fail hui: {e}"