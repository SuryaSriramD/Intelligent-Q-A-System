from typing import Dict, Any, List

def reciprocal_rank_fusion(bm25_hits, tfidf_hits, k=10, c=60):
    # Build score maps by rank
    def as_ranked(hits):
        return {h["idx"]: r+1 for r, h in enumerate(sorted(hits, key=lambda x: x["score"], reverse=True))}
    r1 = as_ranked(bm25_hits)
    r2 = as_ranked(tfidf_hits)
    all_idxs = set(r1.keys()) | set(r2.keys())
    fused = []
    for idx in all_idxs:
        s = (1.0 / (c + r1.get(idx, 1e9))) + (1.0 / (c + r2.get(idx, 1e9)))
        fused.append({"idx": idx, "score": s})
    fused.sort(key=lambda x: x["score"], reverse=True)
    return fused[:k]

def hybrid_search(question: str, bm25_store, tfidf_store, top_k: int = 6):
    """
    Hybrid search combining BM25 and TF-IDF with reciprocal rank fusion.
    Returns: (results, debug_info)
    """
    # Retrieve more candidates but be selective
    bm25_hits = bm25_store.search(question, k=top_k*2)  # Reduced from 3x to 2x
    tfidf_hits = tfidf_store.search(question, k=top_k*2)
    fused = reciprocal_rank_fusion(bm25_hits, tfidf_hits, k=top_k, c=30)  # Reduced c from 60 to 30 for stronger ranking

    # Build debug info
    debug_info = {
        "bm25": [{"idx": h["idx"], "score": round(h["score"], 4)} for h in bm25_hits[:5]],
        "tfidf": [{"idx": h["idx"], "score": round(h["score"], 4)} for h in tfidf_hits[:5]],
        "fusion": [{"idx": h["idx"], "score": round(h["score"], 4)} for h in fused],
        "rerank_scores": []  # Placeholder for future reranker
    }

    # assemble final results with snippets
    results = []
    for idx, h in enumerate(fused):
        c = bm25_store.chunks[h["idx"]]
        snippet = c["text"]
        
        # Better snippet extraction - show more for top results
        # Top result gets 2000 chars (enough for full top-10 lists), next 2 get 800, rest get 400
        if idx == 0:
            snippet_len = 2000  # Top result - show full content (handles top-10 lists)
        elif idx <= 2:
            snippet_len = 800   # Top 3 - show more
        else:
            snippet_len = 400   # Rest - show less
            
        if len(snippet) > snippet_len:
            # Try to cut at sentence boundary
            cutoff = snippet.rfind('. ', 0, snippet_len)
            if cutoff > snippet_len * 0.6:  # Don't cut too short
                snippet = snippet[:cutoff + 1]
            else:
                snippet = snippet[:snippet_len] + "..."
        
        results.append({
            "url": c.get("url", ""),
            "title": c.get("title", ""),
            "snippet": snippet,
            "start": 0,
            "end": len(snippet),
            "score": h["score"]
        })
    
    return results, debug_info
