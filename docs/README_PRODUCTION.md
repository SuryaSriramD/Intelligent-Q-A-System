# 🤖 RAG API - Intelligent Q&A System

A production-ready Retrieval-Augmented Generation (RAG) system that crawls websites and answers questions about their content using hybrid retrieval (BM25 + TF-IDF).

## 🌟 Features

- **Real-Time Web Crawling**: Crawl 30-50 pages from any website with politeness controls
- **Automatic Indexing**: DOM-aware chunking with 800-character chunks and 15% overlap
- **Hybrid Retrieval**: BM25 + TF-IDF with reciprocal rank fusion for better accuracy
- **Smart Refusals**: Refuses to answer when evidence is insufficient (prevents hallucination)
- **Grounded Answers**: All answers cite sources with URLs and snippets
- **Web UI**: Clean, professional interface for non-technical users
- **Full Observability**: Request timings, p50/p95 latency, debug information
- **REST API**: OpenAPI/Swagger documentation at `/docs`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

**Windows:**
```powershell
.\start.ps1
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### 3. Open the Web UI

Visit **http://localhost:8000** in your browser

## 💻 Web UI Usage

1. **Enter a URL** (e.g., `https://www.example.com`)
2. **Configure crawl parameters** (default: 40 pages, depth 2)
3. **Click "Start Crawling & Indexing"** (takes 20-60 seconds)
4. **Ask questions** about the crawled content
5. **Get answers** with source citations in real-time

## 📡 API Endpoints

### POST /crawl
Crawl a website and automatically index it for Q&A.

**Request:**
```json
{
  "start_url": "https://example.com",
  "max_pages": 40,
  "max_depth": 2,
  "crawl_delay_ms": 500
}
```

**Response:**
```json
{
  "page_count": 40,
  "skipped_count": 15,
  "urls": ["https://example.com/", "..."],
  "skipped_reasons": {"off_domain": 10, "duplicate": 5},
  "indexed": true,
  "vector_count": 120
}
```

### POST /ask
Ask questions about the indexed content.

**Request:**
```json
{
  "question": "What is this website about?",
  "top_k": 6
}
```

**Response:**
```json
{
  "answer": "Based on the crawled content...",
  "sources": [
    {
      "url": "https://example.com/about",
      "snippet": "Relevant text excerpt...",
      "title": "About Us",
      "start": 0,
      "end": 800
    }
  ],
  "timings": {
    "retrieval_ms": 3.2,
    "generation_ms": 0.5,
    "total_ms": 3.7
  },
  "retrieval_debug": {...}
}
```

### POST /crawl-and-ask
One-shot endpoint: crawl a URL and immediately answer a question.

**Request:**
```json
{
  "start_url": "https://example.com",
  "question": "What is this website about?",
  "max_pages": 10
}
```

**Response:**
```json
{
  "crawl": { "page_count": 10, "vector_count": 30, ... },
  "answer": { "answer": "...", "sources": [...], ... }
}
```

### GET /health
Check API health and metrics.

**Response:**
```json
{
  "status": "ok",
  "metrics": {
    "count": 150,
    "p50_ms": 3.2,
    "p95_ms": 8.5
  }
}
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Web UI / API                          │
│                    (FastAPI + HTML/JS)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Crawl Module                            │
│  • Polite crawler (respects robots.txt, delays)              │
│  • Domain boundaries (same registrable domain)               │
│  • DOM-aware content extraction                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Index Module                             │
│  • DOM-aware chunking (800 chars, 15% overlap)               │
│  • BM25 index (keyword search)                               │
│  • TF-IDF vectors (semantic search)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Retrieval Module                           │
│  • Hybrid search (BM25 + TF-IDF)                             │
│  • Reciprocal rank fusion (RRF)                              │
│  • Score-based refusal mechanism                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Answer Generation                           │
│  • Extractive composition from top chunks                    │
│  • Source citation with URLs and snippets                    │
│  • Grounded responses (no hallucination)                     │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Configuration

### Crawl Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `max_pages` | 40 | 1-1000 | Maximum pages to crawl |
| `max_depth` | 2 | 0-10 | Maximum link depth from start URL |
| `crawl_delay_ms` | 500 | 100-5000 | Delay between requests (politeness) |

### Index Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `chunk_size` | 800 | 200-4000 | Characters per chunk |
| `chunk_overlap` | 120 | 0-1000 | Overlap between chunks (15%) |

### Retrieval Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `top_k` | 6 | 1-20 | Number of chunks to retrieve |
| `refusal_threshold` | 0.03 | 0-1 | Minimum score to answer (higher = more conservative) |

## 📊 Performance

Tested with various websites:

| Metric | Value |
|--------|-------|
| Crawl speed | ~2-3 pages/second (with 500ms delay) |
| Index time | ~50ms for 100 chunks |
| Query latency | 1-5ms (p95) |
| Throughput | 200+ queries/second |

## 🛡️ Safety & Guardrails

### Refusal Mechanism
- Refuses to answer when retrieval score < 0.03
- Refuses when all chunks score equally low (no clear match)
- Provides closest matches for transparency on refusal

### Content Boundaries
- Only answers from crawled domain
- No off-site information
- Clear source attribution

### Prompt Hardening
- Extractive answers only (no generation)
- Ignores instructions in crawled pages
- No code execution from content

## 🧪 Testing

### Run Full Test Suite
```bash
pytest -v
```

### Test with Example Website
```bash
python test_republicworld.py
```

### Interactive Q&A
```bash
python interactive_qa.py
```

### Run Evaluation
```bash
python evals/build_eval.py
python evals/run_eval.py
```

## 📁 Project Structure

```
rag-fastapi/
├── app/
│   ├── api.py              # FastAPI application
│   ├── schemas.py          # Pydantic models
│   └── observability.py    # Metrics and logging
├── crawl/
│   └── crawler.py          # Web crawler
├── index/
│   ├── chunk.py            # Text chunking
│   ├── bm25.py             # BM25 index
│   └── vector.py           # TF-IDF vectors
├── retrieve/
│   └── hybrid.py           # Hybrid search
├── static/
│   └── index.html          # Web UI
├── evals/
│   ├── build_eval.py       # Generate eval questions
│   └── run_eval.py         # Run evaluation
├── data/                   # Runtime data (auto-created)
│   ├── pages.jsonl         # Crawled pages
│   └── chunks.jsonl        # Indexed chunks
├── start.ps1               # Windows start script
├── start.sh                # Linux/Mac start script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔄 Workflow

### Standard Workflow
1. User provides URL via Web UI
2. System crawls website (30-50 pages, ~20-60 seconds)
3. System auto-indexes content (chunking + BM25 + TF-IDF)
4. User asks questions
5. System retrieves relevant chunks (hybrid search)
6. System composes answer with source citations
7. User sees answer with clickable sources

### One-Shot Workflow
1. User provides URL + question via API
2. System crawls, indexes, and answers in one request
3. Returns both crawl stats and answer

## 🚦 Production Deployment

### Environment Variables
```bash
export HOST=0.0.0.0
export PORT=8000
export WORKERS=4
```

### Run with Gunicorn
```bash
gunicorn app.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)
```bash
docker build -t rag-api .
docker run -p 8000:8000 rag-api
```

## 🐛 Troubleshooting

### "Index not built" error
- Make sure to crawl a website first via UI or `/crawl` endpoint

### Slow crawling
- Reduce `max_pages` or increase `crawl_delay_ms`
- Check network connection

### No answers (always refuses)
- Check if content was actually crawled and indexed
- Try lowering `refusal_threshold` (default: 0.03)
- Ensure questions are about crawled content

### Server won't start
- Check if port 8000 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`

## 📝 License

This project is provided as-is for evaluation purposes.

## 🙏 Acknowledgments

Built with:
- FastAPI (web framework)
- HTTPX (HTTP client)
- BeautifulSoup4 (HTML parsing)
- Rank-BM25 (BM25 implementation)
- Scikit-learn (TF-IDF vectors)
