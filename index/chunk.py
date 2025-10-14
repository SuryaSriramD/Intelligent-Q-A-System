import os, json, re
from typing import List, Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PAGES_PATH = os.path.join(DATA_DIR, "pages.jsonl")
CHUNKS_PATH = os.path.join(DATA_DIR, "chunks.jsonl")

def split_into_paragraphs(text: str) -> List[str]:
    # Normalize and split on blank lines
    text = re.sub(r'\r\n', '\n', text)
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    return paras

def window_subchunks(paras: List[str], chunk_size: int, overlap: int) -> List[str]:
    chunks = []
    buf = ""
    for p in paras:
        if len(buf) + len(p) + 1 <= chunk_size:
            buf = (buf + "\n" + p).strip()
        else:
            if buf:
                chunks.append(buf)
            # start new buffer with overlap from end of previous buffer
            tail = buf[-overlap:] if overlap > 0 else ""
            buf = (tail + "\n" + p).strip()
    
    # Always add remaining buffer, even if smaller than chunk_size
    # This ensures short documents still get indexed
    if buf:
        chunks.append(buf)
    
    return chunks

def build_chunks(chunk_size: int = 800, chunk_overlap: int = 120):
    os.makedirs(DATA_DIR, exist_ok=True)
    errors = []
    count = 0
    with open(CHUNKS_PATH, "w", encoding="utf-8") as out:
        try:
            with open(PAGES_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    rec = json.loads(line)
                    text = rec.get("text", "")
                    url = rec.get("url", "")
                    title = rec.get("title", "")
                    paras = split_into_paragraphs(text)
                    subs = window_subchunks(paras, chunk_size, chunk_overlap)
                    for s in subs:
                        out.write(json.dumps({
                            "url": url,
                            "title": title,
                            "text": s
                        }, ensure_ascii=False) + "\n")
                        count += 1
        except FileNotFoundError:
            errors.append("No pages found. Run /crawl first.")
    return load_chunks(), errors

def load_chunks():
    items = []
    try:
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            for line in f:
                items.append(json.loads(line))
    except FileNotFoundError:
        pass
    return items
