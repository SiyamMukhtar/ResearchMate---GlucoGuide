import re

HEADING_RE = re.compile(r"^(Abstract|\d{1,2}\.\s+[A-Z][^.]{2,70})$")


def split_into_sections(pages):
    """Pages ko headings ke hisab se sections mein baanto."""
    sections = []
    current = {"title": "Title", "words": []}

    for p in pages:
        for line in p["text"].splitlines():
            line = line.strip()
            if not line:
                continue
            if HEADING_RE.match(line):
                if current["words"]:
                    sections.append(current)
                current = {"title": line, "words": []}
            else:
                for w in line.split():
                    current["words"].append((w, p["page"]))
    if current["words"]:
        sections.append(current)
    return sections


def chunk_pages(pages, chunk_size=120, overlap=25):
    """Har section ko overlap ke saath chhote chunks mein todo."""
    chunks = []
    step = chunk_size - overlap

    for sec in split_into_sections(pages):
        words = sec["words"]
        for start in range(0, len(words), step):
            piece = words[start:start + chunk_size]
            if len(piece) < 15 and start > 0:
                break
            chunks.append({
                "id": f"chunk_{len(chunks)}",
                "text": " ".join(w for w, _ in piece),
                "section": sec["title"],
                "page": piece[0][1],
            })
            if start + chunk_size >= len(words):
                break
    return chunks