import re
import pymupdf


def load_pdf(pdf_path):
    """Load a PDF and return a list of pages: [{"page": 1, "text": "..."}, ...]"""
    pages = []
    doc = pymupdf.open(pdf_path)

    for page_number, page in enumerate(doc, start=1):
        text = page.get_text()
        # PDF ke footer wali "Page 1" jaisi lines hata do
        text = re.sub(r"^Page \d+\s*$", "", text, flags=re.MULTILINE).strip()
        if text:
            pages.append({"page": page_number, "text": text})

    doc.close()
    return pages