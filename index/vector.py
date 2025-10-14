from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfidfVectorStore:
    def __init__(self):
        self.vec = None
        self.mat = None
        self.chunks: List[Dict[str, Any]] = []
        self.ready = False

    def build(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        texts = [c["text"] for c in chunks]
        if not texts:
            self.ready = False
            return
        self.vec = TfidfVectorizer(stop_words="english", max_features=50000)
        self.mat = self.vec.fit_transform(texts)
        self.ready = True

    def search(self, query: str, k: int = 10):
        if not self.ready:
            return []
        qv = self.vec.transform([query])
        sims = cosine_similarity(qv, self.mat).ravel()
        idxs = sims.argsort()[::-1][:k]
        return [{"idx": int(i), "score": float(sims[i])} for i in idxs]
