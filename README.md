# 🤖 Intelligent Q&A System

**Production-ready RAG API with Web UI** — Crawl any website, index content automatically, and get instant, grounded answers with source citations. No hallucinations, no GPU required.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Features

* 🌐 **Web UI** — Beautiful, simple interface for non-technical users
* 🔍 **Smart Search** — Hybrid **BM25 + TF-IDF** retrieval with relevance filtering
* 📚 **Source Citations** — Every answer includes clickable URLs
* 🚫 **No Hallucinations** — Refuses to answer when information isn’t found
* ⚡ **Fast** — Millisecond-level query latency after indexing
* 🎯 **Grounded** — Answers extracted from actually crawled content
* 📊 **Observable** — Full timing breakdowns and debug info

---

## 🚀 Quick Start

### Option 1: Web UI (Recommended)

```powershell
# Windows
.\start.ps1
```

```bash
# Linux / macOS
./start.sh
```

Then open **[http://localhost:8000](http://localhost:8000)** in your browser.

You can:

1. Paste any website URL
2. Click **Start Crawling & Indexing**
3. Ask questions and get instant answers with citations

### Option 2: REST API

**1) Start the server**

```bash
uvicorn app.api:app --port 8000
```

**2) Crawl a website (auto-indexes)**

```bash
curl -X POST http://localhost:8000/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "start_url": "https://example.com",
    "max_pages": 40,
    "max_depth": 2,
    "crawl_delay_ms": 500
  }'
```

**3) Ask a question**

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the top 10 SUVs with highest sales?",
    "top_k": 6
  }'
```

---

## 📦 Installation

### Prerequisites

* Python **3.8+**
* `pip`

### Setup

```bash
# 1) Clone
git clone https://github.com/SuryaSriramD/Intelligent-Q-A-System.git
cd Intelligent-Q-A-System

# 2) Create & activate venv
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

# 3) Install deps
pip install -r requirements.txt

# 4) Run
# Windows
.\start.ps1
# Linux/macOS
./start.sh
```

Open **[http://localhost:8000](http://localhost:8000)** to use the web interface.

---

## 🏗️ Architecture

```
┌─────────────┐
│   Web UI    │  ← Simple, gradient interface
└──────┬──────┘
       │
┌──────▼───────────────────────────────────────────┐
│                   FastAPI API                    │
│            /crawl   /ask   /health   /docs       │
└──────┬───────────────────────────────────────────┘
       │
       ├─► Crawler (httpx) → Content Cleaner (trafilatura)
       │
       ├─► Chunker (800 chars, 15% overlap) → JSONL Storage
       │
       ├─► Indexer → BM25 (keyword) + TF-IDF (vectors)
       │
       └─► Hybrid Search → Reciprocal Rank Fusion (RRF)
            → Relevance Filtering (≥50% of top)
            → Smart Snippets → Grounded Answers + Citations
```

### Key Design Principles

* ✅ **Grounded Answers** — Extracted from crawled text
* ✅ **Source Attribution** — Clickable URLs for every fact
* ✅ **Smart Refusals** — Returns “Not found” when confidence < **0.03**
* ✅ **Relevance Filtering** — Only surfaces truly relevant sources
* ✅ **List Intelligence** — Auto-formats top-N lists
* ✅ **No GPU Required** — Runs anywhere

---

## 📖 API Endpoints

### 🏠 `GET /`

Serves the production Web UI.

### ❤️ `GET /health`

Health check + simple performance metrics.

**Example response**

```json
{
  "status": "ok",
  "metrics": { "count": 10, "p50_ms": 2.5, "p95_ms": 8.3 }
}
```

### 🕷️ `POST /crawl`

Crawl a site and automatically index content.

**Request**

```json
{
  "start_url": "https://example.com",
  "max_pages": 40,
  "max_depth": 2,
  "crawl_delay_ms": 500
}
```

**Response (example)**

```json
{
  "page_count": 25,
  "skipped_count": 15,
  "indexed": true,
  "vector_count": 50,
  "urls": ["https://example.com", "..."],
  "skipped_reasons": { "off_domain": 8, "duplicate": 5, "error": 2 }
}
```

### 💬 `POST /ask`

Ask questions and receive grounded answers with citations.

**Request**

```json
{
  "question": "What are the top 10 SUVs with highest sales?",
  "top_k": 6
}
```

**Response (example)**

```json
{
  "answer": "1/10: Hyundai Creta - 18,861 units (+19% YoY)\n2/10: Mahindra Scorpio - 18,372 units (+27% YoY)\n...",
  "sources": [
    {
      "url": "https://example.com/suv-sales",
      "title": "Top 10 SUVs with Highest Sales",
      "snippet": "Updated 14 October 2025..."
    }
  ],
  "timings": { "retrieval_ms": 2.3, "generation_ms": 0.8, "total_ms": 3.1 }
}
```

---

## 🎯 How It Works

1. **Crawling**

* Starts from a URL, follows in-domain links
* Respects crawl delays (default **500ms**)
* Cleans HTML via **trafilatura**
* Configurable **max_pages** (1–1000) and **max_depth** (0–10)

2. **Indexing (Automatic)**

* Splits content into **800-char** chunks with **15%** overlap
* Builds **BM25** (keyword) and **TF-IDF** (semantic) indexes
* Persists to **JSONL** for fast, simple storage

3. **Retrieval**

* **Hybrid Search**: BM25 + TF-IDF combined via **RRF (c=30)**
* **Relevance Filter**: keep sources scoring ≥ **50%** of the top result
* **Smart Snippets**: larger snippet for top source

4. **Answer Generation**

* Detects list-style prompts (e.g., “top 10 …”)
* Extracts clean text, removes boilerplate
* Links every fact to original sources
* Refuses when confidence < **0.03**

---

## ⚙️ Configuration (Defaults)

| Setting             | Default | Range       |
| ------------------- | ------- | ----------- |
| Max Pages           | 40      | 1–1000      |
| Crawl Delay         | 500 ms  | 100–5000 ms |
| Chunk Size          | 800     | —           |
| Chunk Overlap       | 120     | —           |
| Top-K Results       | 6       | —           |
| Relevance Threshold | 50%     | —           |
| Refusal Threshold   | 0.03    | —           |

### Performance (Typical)

* **Query Speed:** 1–5 ms after indexing
* **Crawl Speed:** ~20–60 s for 30–50 pages
* **Memory:** Low (CPU-only)
* **Storage:** ~1 MB per 50 pages

---

## 📁 Project Structure

```
Intelligent-Q-A-System/
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
│   ├── pages.jsonl         # Raw pages
│   ├── chunks.jsonl        # Indexed chunks
│   └── indexes/            # BM25 + TF-IDF indexes
├── start.ps1               # Windows startup
├── start.sh                # Linux/macOS startup
├── requirements.txt        # Dependencies
└── README.md               # This file
```

---

## 📚 Documentation

* **[USER_GUIDE.md](USER_GUIDE.md)** — Step-by-step guide for non-technical users
* **[DEPLOYMENT.md](DEPLOYMENT.md)** — How to deploy to production
* **[README_PRODUCTION.md](README_PRODUCTION.md)** — Technical deep-dive
* **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** — Quick reference card

---

## 🛠️ Technology Stack

* **FastAPI** — Modern, fast web framework
* **httpx** — Async HTTP client
* **Trafilatura** — Content extraction
* **rank-bm25** — BM25 search
* **scikit-learn** — TF-IDF vectors
* **Pydantic** — Data validation

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit: `git commit -m "Add AmazingFeature"`
4. Push: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see **[LICENSE](LICENSE)**.

---

## 📞 Contact

**Surya Sriram D**
GitHub: [@SuryaSriramD](https://github.com/SuryaSriramD)
Repository: [Intelligent-Q-A-System](https://github.com/SuryaSriramD/Intelligent-Q-A-System)

---

## 🚀 Ready to Use?

```bash
# Windows
.\start.ps1
# Linux/macOS
./start.sh
```

Open **[http://localhost:8000](http://localhost:8000)** and start asking questions! 🎉
