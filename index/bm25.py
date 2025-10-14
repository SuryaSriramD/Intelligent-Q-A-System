from rank_bm25 import BM25Okapi
from typing import List, Dict, Any
import re

def _tokenize(text: str):
    return re.findall(r"[A-Za-z0-9]+", text.lower())

class BM25Store:
    def __init__(self):
        self.bm25 = None
        self.docs = []  # raw
        self.chunks = []
        self.ready = False

    def build(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        self.docs = [c["text"] for c in chunks]
        corpus = [_tokenize(t) for t in self.docs]
        if corpus:
            self.bm25 = BM25Okapi(corpus)
            self.ready = True
        else:
            self.ready = False

    def search(self, query: str, k: int = 10):
        if not self.ready:
            return []
        q = _tokenize(query)
        scores = self.bm25.get_scores(q)
        # top k indices
        idxs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [{"idx": i, "score": float(scores[i])} for i in idxs]
