import { useState, useRef, useEffect } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function uniqueSources(sources) {
  const seen = new Set();
  return sources.filter((s) => {
    const key = `${s.section}-${s.page}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hello! I'm GlucoGuide. Ask me anything about Type 2 Diabetes (answers in English are more accurate).",
      sources: [],
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendQuestion(e) {
    e.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setMessages((prev) => [...prev, { role: "user", text: question, sources: [] }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Server error ${res.status}`);
      }
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: data.answer, sources: data.sources },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: `Error: ${err.message}`, sources: [] },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>GlucoGuide</h1>
        <p>RAG-based healthcare chatbot for Type 2 Diabetes</p>
      </header>

      <main className="chat">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            <div className="bubble">{m.text}</div>
            {m.sources.length > 0 && (
              <div className="sources">
                Sources:{" "}
                {uniqueSources(m.sources).map((s, j) => (
                  <span key={j} className="chip">
                    {s.section} · p.{s.page}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="msg bot">
            <div className="bubble typing">GlucoGuide thinking...</div>
          </div>
        )}
        <div ref={endRef} />
      </main>

      <form className="inputbar" onSubmit={sendQuestion}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Write your Question, like: What are the symptoms of diabetes?"
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </div>
  );
}