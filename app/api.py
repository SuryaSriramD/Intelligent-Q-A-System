from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schemas import (
    CrawlRequest, CrawlResponse, IndexRequest, IndexResponse, 
    AskRequest, AskResponse, CrawlAndAskRequest, CrawlAndAskResponse
)
from app.observability import with_timings, metrics_snapshot
from crawl.crawler import run_crawl
from index.chunk import build_chunks
from index.bm25 import BM25Store
from index.vector import TfidfVectorStore
from retrieve.hybrid import hybrid_search
import time
import os

app = FastAPI(title="RAG API - Intelligent Q&A System", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for the UI
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

bm25_store = BM25Store()
tfidf_store = TfidfVectorStore()

@app.get("/")
def read_root():
    """Serve the main UI"""
    static_file = os.path.join(static_dir, "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    return {"message": "RAG API is running. Visit /docs for API documentation."}

@app.get("/health")
def health():
    return {"status": "ok", "metrics": metrics_snapshot()}

@app.post("/crawl", response_model=CrawlResponse)
@with_timings
def crawl(req: CrawlRequest):
    """Crawl a website and automatically index it for question answering."""
    try:
        # Step 1: Crawl the website
        result = run_crawl(
            start_url=str(req.start_url),  # Convert Pydantic URL to string
            max_pages=req.max_pages,
            max_depth=req.max_depth,
            crawl_delay_ms=req.crawl_delay_ms,
        )
        
        # Step 2: Automatically index the crawled content
        # This makes the workflow seamless - crawl → immediately ready for questions
        indexed = False
        vector_count = 0
        if result["page_count"] > 0:
            chunks, errors = build_chunks(chunk_size=800, chunk_overlap=120)
            bm25_store.build(chunks)
            tfidf_store.build(chunks)
            indexed = True
            vector_count = len(chunks)
        
        return CrawlResponse(
            **result,
            indexed=indexed,
            vector_count=vector_count
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Crawl error: {e}")

@app.post("/index", response_model=IndexResponse)
@with_timings
def index(req: IndexRequest):
    try:
        chunks, errors = build_chunks(chunk_size=req.chunk_size, chunk_overlap=req.chunk_overlap)
        bm25_store.build(chunks)
        tfidf_store.build(chunks)
        return IndexResponse(vector_count=len(chunks), errors=errors)
    except Exception as e:
        raise HTTPException(500, f"Index error: {e}")

@app.post("/ask", response_model=AskResponse)
@with_timings
def ask(req: AskRequest):
    try:
        t_start = time.time()
        
        if not bm25_store.ready or not tfidf_store.ready:
            raise HTTPException(400, "Index not built. Call /index first.")
        
        # Retrieve documents with detailed timing
        t_retrieval_start = time.time()
        results, debug_info = hybrid_search(
            question=req.question, 
            bm25_store=bm25_store, 
            tfidf_store=tfidf_store, 
            top_k=req.top_k
        )
        retrieval_ms = (time.time() - t_retrieval_start) * 1000
        
        # Score threshold for refusal (tuned via evaluation)
        # Tuning history:
        # - 0.01: Too permissive (0% refusal rate on trap questions)
        # - 0.05: Too conservative (refused answerable questions)
        # - 0.03: Sweet spot for this dataset (balances precision/recall)
        REFUSAL_THRESHOLD = 0.03
        
        # Check if we have meaningful results
        # Refuse if: no results, score too low, or all results have same low score
        max_score = results[0].get("score", 0) if results else 0
        score_variance = (results[0].get("score", 0) - results[-1].get("score", 0)) if len(results) > 1 else 1.0
        
        should_refuse = (
            not results or 
            max_score < REFUSAL_THRESHOLD or
            (len(results) >= 2 and score_variance < 0.001 and max_score < 0.1)  # All chunks equally bad (only if multiple chunks)
        )
        
        if should_refuse:
            # Return closest matches for transparency
            closest = []
            for r in results[:2] if results else []:
                closest.append({
                    "url": r["url"],
                    "snippet": r["snippet"][:200] + "..." if len(r["snippet"]) > 200 else r["snippet"],
                    "title": r.get("title", "")
                })
            
            total_ms = (time.time() - t_start) * 1000
            return AskResponse(
                answer="Not found in crawled content.",
                sources=[],
                closest=closest,
                timings={
                    "retrieval_ms": round(retrieval_ms, 2), 
                    "generation_ms": 0, 
                    "total_ms": round(total_ms, 2)
                },
                retrieval_debug=debug_info
            )
        
        # Generate answer (extractive composition)
        t_gen_start = time.time()
        answer = _compose_grounded_answer(results, req.question)
        generation_ms = (time.time() - t_gen_start) * 1000
        
        # Build sources - only show the top source (most relevant)
        srcs = []
        if results:
            top_result = results[0]
            srcs.append({
                "url": top_result["url"],
                "snippet": top_result["snippet"],
                "start": top_result.get("start", 0),
                "end": top_result.get("end", 0),
                "title": top_result.get("title", ""),
            })
        
        total_ms = (time.time() - t_start) * 1000
        return AskResponse(
            answer=answer.strip(),
            sources=srcs,
            timings={
                "retrieval_ms": round(retrieval_ms, 2), 
                "generation_ms": round(generation_ms, 2), 
                "total_ms": round(total_ms, 2)
            },
            retrieval_debug=debug_info
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Ask error: {e}")


@app.post("/crawl-and-ask", response_model=CrawlAndAskResponse)
@with_timings
def crawl_and_ask(req: CrawlAndAskRequest):
    """
    One-shot endpoint: Crawl a URL and immediately answer a question about it.
    Perfect for real-time use cases where you want instant answers about a webpage.
    """
    try:
        # Step 1: Crawl (which now auto-indexes)
        crawl_result = crawl(CrawlRequest(
            start_url=req.start_url,
            max_pages=req.max_pages,
            max_depth=req.max_depth,
            crawl_delay_ms=req.crawl_delay_ms
        ))
        
        # Step 2: Ask question
        ask_result = ask(AskRequest(
            question=req.question,
            top_k=req.top_k
        ))
        
        return CrawlAndAskResponse(
            crawl=crawl_result,
            answer=ask_result
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Crawl-and-ask error: {e}")


def _compose_grounded_answer(results, question):
    """Compose an extractive answer from top results, grounded in source content."""
    if not results:
        return "No relevant information found."
    
    # Get the top result (most relevant)
    top_result = results[0]
    snippet = top_result["snippet"]
    
    # Check if this is a list-based question (top 10, top 5, etc.)
    question_lower = question.lower()
    is_list_question = any(word in question_lower for word in ['top', 'list', 'highest', 'best', 'most', 'which'])
    
    # Try to extract structured data if it looks like a numbered list
    if is_list_question and any(marker in snippet for marker in ['1/10:', '1.', '2.', '1)', '2/10:', '3/10:']):
        # Extract list items - handle format like "1/10:\nContent here"
        list_items = []
        
        # Split by numbered markers and process
        import re
        # Pattern matches "1/10:", "2/10:", ... "10/10:" or "1.", "2.", etc.
        pattern = r'(\d{1,2}/10:|\d{1,2}\.|\d{1,2}\))'
        parts = re.split(pattern, snippet)
        
        for i in range(1, len(parts), 2):  # Every odd index is a number, even is content
            if i+1 < len(parts):
                number = parts[i]
                content = parts[i+1].strip()
                
                # Skip metadata lines at the start
                if i == 1 and any(skip in content[:100] for skip in ['Updated', 'Published', 'IST', 
                                                                      'Galleries', 'Advertisement']):
                    # For first item, skip initial metadata
                    lines = content.split('\n')
                    content = '\n'.join([l for l in lines if l.strip() and not any(
                        skip in l for skip in ['Updated', 'Published', 'IST', 'Galleries', 'Advertisement', 'min read']
                    )])
                
                # Clean the content - take only the first line (the actual item)
                first_line = content.split('\n')[0].strip()
                
                # Remove image credits
                if '/ Image:' in first_line:
                    first_line = first_line.split('/ Image:')[0].strip()
                
                # Only add meaningful content
                if first_line and len(first_line) > 10:
                    list_items.append(f"{number} {first_line}")
        
        if list_items:
            # Return ONLY the list items, nothing else
            return "\n".join(list_items)
    
    # For non-list questions, extract the most relevant sentence or paragraph
    # Remove metadata, timestamps, and clutter
    lines = snippet.split('\n')
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        # Skip metadata and noise
        if any(skip in line for skip in ['Updated', 'Published', 'IST', 'Advertisement', 'min read', 
                                          'Add Republic', 'Trending', 'Show Quick Read']):
            continue
        if line and len(line) > 20:  # Only meaningful content
            clean_lines.append(line)
    
    # Return first meaningful paragraph (up to 3 sentences)
    result = ' '.join(clean_lines[:3]) if clean_lines else snippet
    
    # Limit length to avoid overwhelming the user
    if len(result) > 500:
        cutoff = result.rfind('. ', 0, 500)
        if cutoff > 300:
            result = result[:cutoff + 1]
        else:
            result = result[:500] + "..."
    
    return result
