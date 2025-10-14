# 🤖 Intelligent Q&A System

> **Production-ready RAG API with web UI** — Crawl any website, index content automatically, and get instant answers with source citations. No hallucinations, no GPU required.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

- 🌐 **Web UI** — Beautiful interface for non-technical users
- 🔍 **Smart Search** — Hybrid BM25 + TF-IDF retrieval with relevance filtering
- 📚 **Source Citations** — Every answer includes clickable source URLs
- 🚫 **No Hallucinations** — Refuses to answer when information isn't found
- ⚡ **Fast** — 1-5ms query latency after indexing
- 🎯 **Grounded** — All answers extracted from crawled content
- 📊 **Observable** — Full timing breakdowns and debug info

## 🚀 Quick Start

### Option 1: Use the Web UI (Recommended)

```powershell
# Windows
.\start.ps1

# Linux/Mac
./start.sh
```

Then open your browser to **http://localhost:8000**

That's it! You now have a beautiful web interface where you can:
1. Paste any website URL
2. Click "Start Crawling & Indexing"
3. Ask questions and get instant answers!

### Option 2: Use the REST API

**1. Start the server:**
```powershell
uvicorn app.api:app --port 8000
```

**2. Crawl a website** (automatically indexes):
```bash
curl -X POST http://localhost:8000/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "start_url": "https://www.republicworld.com",
    "max_pages": 40,
    "max_depth": 2,
    "crawl_delay_ms": 500
  }'
```

**3. Ask questions:**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the top 10 SUVs with highest sales?",
    "top_k": 6
  }'
```

## 📋 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

**1. Clone the repository:**
```bash
git clone <your-repo-url>
cd rag-fastapi
```

**2. Create virtual environment:**
```bash
python -m venv .venv

# Activate it:
# Windows:
.\.venv\Scripts\Activate.ps1

# Linux/Mac:
source .venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the server:**
```bash
.\start.ps1  # Windows
./start.sh   # Linux/Mac
```

That's it! Open http://localhost:8000 to use the web interface.

## 🏗️ Architecture

```
┌─────────────┐
│   Web UI    │ ← Beautiful gradient interface
└──────┬──────┘
       │
┌──────▼──────────────────────────────────────┐
│          FastAPI REST API                    │
│  /crawl  /ask  /health  /docs               │
└──────┬──────────────────────────────────────┘
       │
       ├─► Crawler (httpx) → Content Cleaner (trafilatura)
       │
       ├─► Chunker (800 chars, 15% overlap) → JSONL Storage
       │
       ├─► Indexer → BM25 + TF-IDF Vectors
       │
       └─► Hybrid Search → Reciprocal Rank Fusion
                         → Relevance Filtering (50% threshold)
                         → Smart List Extraction
                         → Grounded Answers + Source Citations
```

### Key Design Principles

✅ **Grounded Answers** — Every answer extracted from actual crawled content  
✅ **Source Attribution** — All facts include clickable URLs  
✅ **Smart Refusals** — Refuses to answer when confidence is low  
✅ **Relevance Filtering** — Only shows truly relevant sources (50% threshold)  
✅ **List Intelligence** — Automatically formats top-N lists cleanly  
✅ **No GPU Required** — Works on any machine, no expensive hardware

## 📖 API Endpoints

### 🏠 GET `/`
Serves the web UI (production interface).

### ❤️ GET `/health`
Health check with performance metrics.

**Response:**
```json
{
  "status": "ok",
  "metrics": {
    "count": 10,
    "p50_ms": 2.5,
    "p95_ms": 8.3
  }
}
```

### 🕷️ POST `/crawl`
Crawls a website and **automatically indexes** the content.

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
  "page_count": 25,
  "skipped_count": 15,
  "indexed": true,
  "vector_count": 50,
  "urls": ["https://example.com", ...],
  "skipped_reasons": {
    "off_domain": 8,
    "duplicate": 5,
    "error": 2
  }
}
```

### 💬 POST `/ask`
Ask questions and get grounded answers with sources.

**Request:**
```json
{
  "question": "What are the top 10 SUVs with highest sales?",
  "top_k": 6
}
```

**Response:**
```json
{
  "answer": "1/10: Hyundai Creta - 18,861 units (+19% YoY)\n2/10: Mahindra Scorpio - 18,372 units (+27% YoY)\n...",
  "sources": [
    {
      "url": "https://example.com/suv-sales",
      "title": "Top 10 SUVs with Highest Sales",
      "snippet": "Updated 14 October 2025... (1500 chars)"
    }
  ],
  "timings": {
    "retrieval_ms": 2.3,
    "generation_ms": 0.8,
    "total_ms": 3.1
  }
}
```

### 📚 GET `/docs`
Interactive API documentation (Swagger UI).

Visit http://localhost:8000/docs for full API exploration.

## 🎯 How It Works

### 1. Crawling
- Starts from a URL and follows links within the same domain
- Respects crawl delays (default: 500ms) for politeness
- Cleans HTML using Trafilatura (removes ads, nav, footers)
- Configurable max pages (1-1000) and depth (0-10)

### 2. Indexing (Automatic)
- Splits content into 800-character chunks with 15% overlap
- Builds BM25 index (keyword search)
- Builds TF-IDF vectors (semantic similarity)
- Stores in JSONL files for fast access

### 3. Retrieval
- **Hybrid Search**: Combines BM25 + TF-IDF results
- **Reciprocal Rank Fusion**: Merges rankings intelligently (c=30)
- **Relevance Filtering**: Only shows sources scoring ≥50% of top result
- **Smart Snippets**: Top result gets 1500 chars, others get 800/400 chars

### 4. Answer Generation
- **List Detection**: Auto-formats top-N questions (e.g., "top 10 SUVs")
- **Clean Extraction**: Removes metadata, timestamps, image credits
- **Source Attribution**: Every answer linked to original URLs
- **Refusal Logic**: Returns "Not found" when confidence < 0.03

## ⚙️ Configuration

### Default Settings
- **Max Pages**: 40 (configurable 1-1000)
- **Crawl Delay**: 500ms (configurable 100-5000ms)
- **Chunk Size**: 800 characters
- **Chunk Overlap**: 120 characters (15%)
- **Top-K Results**: 6
- **Refusal Threshold**: 0.03
- **Relevance Threshold**: 50% of top score

### Performance
- **Query Speed**: 1-5ms after indexing
- **Crawl Speed**: 20-60 seconds for 30-50 pages
- **Memory**: Low (no GPU required)
- **Storage**: ~1MB per 50 pages crawled

## 📁 Project Structure

```
rag-fastapi/
├── app/
│   ├── api.py              # FastAPI endpoints
│   ├── schemas.py          # Pydantic models
│   └── observability.py    # Metrics & timing
├── crawl/
│   └── crawler.py          # Web crawler
├── index/
│   ├── chunk.py            # Text chunking
│   ├── bm25.py             # BM25 search
│   └── vector.py           # TF-IDF vectors
├── retrieve/
│   └── hybrid.py           # Hybrid search + RRF
├── static/
│   └── index.html          # Web UI
├── data/                   # Auto-generated
│   ├── pages.jsonl         # Crawled pages
│   ├── chunks.jsonl        # Indexed chunks
│   └── indexes/            # BM25 + TF-IDF indexes
├── start.ps1 / start.sh    # Production startup
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## 📚 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** — Step-by-step guide for non-technical users
- **[DEPLOYMENT.md](DEPLOYMENT.md)** — How to deploy to production
- **[README_PRODUCTION.md](README_PRODUCTION.md)** — Technical deep-dive
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** — Quick reference card

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) — Modern, fast web framework
- [Trafilatura](https://github.com/adbar/trafilatura) — Content extraction
- [rank-bm25](https://github.com/dorianbrown/rank_bm25) — BM25 search
- [scikit-learn](https://scikit-learn.org/) — TF-IDF vectors

---

**Questions?** Open an issue or check the [documentation](docs/).

**Ready to use?** Run `.\start.ps1` and open http://localhost:8000 🚀
#   I n t e l l i g e n t - Q - A - S y s t e m  
 