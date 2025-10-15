## 🤖 Intelligent Q&A System# 🤖 Intelligent Q&A System



**Production-ready RAG API with web UI** — Crawl any website, index content automatically, and get instant answers with source citations.> **Production-ready RAG API with web UI** — Crawl any website, index content automatically, and get instant answers with source citations. No hallucinations, no GPU required.



[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



---## ✨ Features



## ✨ Features- 🌐 **Web UI** — Beautiful interface for non-technical users

- 🔍 **Smart Search** — Hybrid BM25 + TF-IDF retrieval with relevance filtering

- 🌐 **Web UI** — Beautiful gradient interface for non-technical users- 📚 **Source Citations** — Every answer includes clickable source URLs

- 🔍 **Smart Search** — Hybrid BM25 + TF-IDF retrieval with relevance filtering  - 🚫 **No Hallucinations** — Refuses to answer when information isn't found

- 📚 **Source Citations** — Every answer includes clickable URLs to original sources- ⚡ **Fast** — 1-5ms query latency after indexing

- 🚫 **No Hallucinations** — Refuses to answer when information isn't found- 🎯 **Grounded** — All answers extracted from crawled content

- ⚡ **Fast** — 1-5ms query latency after indexing- 📊 **Observable** — Full timing breakdowns and debug info

- 🎯 **Grounded** — All answers extracted from actual crawled content

- 📊 **Observable** — Complete timing breakdowns and debug information## 🚀 Quick Start



---### Option 1: Use the Web UI (Recommended)



## 🚀 Quick Start```powershell

# Windows

### Web UI (Recommended).\start.ps1



```bash# Linux/Mac

# Windows./start.sh

.\start.ps1```



# Linux/MacThen open your browser to **http://localhost:8000**

./start.sh

```That's it! You now have a beautiful web interface where you can:

1. Paste any website URL

Then open **http://localhost:8000** in your browser.2. Click "Start Crawling & Indexing"

3. Ask questions and get instant answers!

### REST API

### Option 2: Use the REST API

**Start server:**

```bash**1. Start the server:**

uvicorn app.api:app --port 8000```powershell

```uvicorn app.api:app --port 8000

```

**Crawl a website** (auto-indexes):

```bash**2. Crawl a website** (automatically indexes):

curl -X POST http://localhost:8000/crawl \```bash

  -H "Content-Type: application/json" \curl -X POST http://localhost:8000/crawl \

  -d '{  -H "Content-Type: application/json" \

    "start_url": "https://www.example.com",  -d '{

    "max_pages": 40,    "start_url": "https://www.republicworld.com",

    "max_depth": 2,    "max_pages": 40,

    "crawl_delay_ms": 500    "max_depth": 2,

  }'    "crawl_delay_ms": 500

```  }'

```

**Ask questions:**

```bash**3. Ask questions:**

curl -X POST http://localhost:8000/ask \```bash

  -H "Content-Type: application/json" \curl -X POST http://localhost:8000/ask \

  -d '{  -H "Content-Type: application/json" \

    "question": "What are the top 10 products?",  -d '{

    "top_k": 6    "question": "What are the top 10 SUVs with highest sales?",

  }'    "top_k": 6

```  }'

```

---

## 📋 Installation

## 📦 Installation

### Prerequisites

### Prerequisites- Python 3.8 or higher

- Python 3.8 or higher- pip (Python package manager)

- pip (Python package manager)

### Setup

### Setup Steps

**1. Clone the repository:**

**1. Clone the repository:**```bash

```bashgit clone <your-repo-url>

git clone https://github.com/SuryaSriramD/Intelligent-Q-A-System.gitcd rag-fastapi

cd Intelligent-Q-A-System```

```

**2. Create virtual environment:**

**2. Create virtual environment:**```bash

```bashpython -m venv .venv

python -m venv .venv

# Activate it:

# Activate:# Windows:

# Windows:.\.venv\Scripts\Activate.ps1

.\.venv\Scripts\Activate.ps1

# Linux/Mac:

# Linux/Mac:source .venv/bin/activate

source .venv/bin/activate```

```

**3. Install dependencies:**

**3. Install dependencies:**```bash

```bashpip install -r requirements.txt

pip install -r requirements.txt```

```

**4. Run the server:**

**4. Run the server:**```bash

```bash.\start.ps1  # Windows

.\start.ps1  # Windows./start.sh   # Linux/Mac

./start.sh   # Linux/Mac```

```

That's it! Open http://localhost:8000 to use the web interface.

Open **http://localhost:8000** to use the web interface.

## 🏗️ Architecture

---

```

## 🏗️ Architecture┌─────────────┐

│   Web UI    │ ← Beautiful gradient interface

```└──────┬──────┘

┌─────────────┐       │

│   Web UI    │ ← Beautiful purple gradient interface┌──────▼──────────────────────────────────────┐

└──────┬──────┘│          FastAPI REST API                    │

       ││  /crawl  /ask  /health  /docs               │

┌──────▼──────────────────────────────────────┐└──────┬──────────────────────────────────────┘

│          FastAPI REST API                    │       │

│  /crawl  /ask  /health  /docs               │       ├─► Crawler (httpx) → Content Cleaner (trafilatura)

└──────┬──────────────────────────────────────┘       │

       │       ├─► Chunker (800 chars, 15% overlap) → JSONL Storage

       ├─► Crawler (httpx + trafilatura)       │

       │   • Polite crawling with delays       ├─► Indexer → BM25 + TF-IDF Vectors

       │   • Content extraction & cleaning       │

       │       └─► Hybrid Search → Reciprocal Rank Fusion

       ├─► Chunker (800 chars, 15% overlap)                         → Relevance Filtering (50% threshold)

       │   • DOM-aware text splitting                         → Smart List Extraction

       │   • JSONL storage                         → Grounded Answers + Source Citations

       │```

       ├─► Indexer

       │   • BM25 (keyword search)### Key Design Principles

       │   • TF-IDF (semantic vectors)

       │✅ **Grounded Answers** — Every answer extracted from actual crawled content  

       └─► Hybrid Search✅ **Source Attribution** — All facts include clickable URLs  

           • Reciprocal Rank Fusion (RRF)✅ **Smart Refusals** — Refuses to answer when confidence is low  

           • Relevance filtering (50% threshold)✅ **Relevance Filtering** — Only shows truly relevant sources (50% threshold)  

           • Smart list extraction✅ **List Intelligence** — Automatically formats top-N lists cleanly  

           • Grounded answers + citations✅ **No GPU Required** — Works on any machine, no expensive hardware

```

## 📖 API Endpoints

### Key Design Principles

### 🏠 GET `/`

✅ **Grounded Answers** — Every answer extracted from crawled content  Serves the web UI (production interface).

✅ **Source Attribution** — All facts include clickable URLs  

✅ **Smart Refusals** — Refuses when confidence < 0.03  ### ❤️ GET `/health`

✅ **Relevance Filtering** — Only shows truly relevant sources  Health check with performance metrics.

✅ **List Intelligence** — Auto-formats top-N questions  

✅ **No GPU Required** — Works on any machine**Response:**

```json

---{

  "status": "ok",

## 📖 API Endpoints  "metrics": {

    "count": 10,

### 🏠 `GET /`    "p50_ms": 2.5,

Serves the web UI.    "p95_ms": 8.3

  }

### ❤️ `GET /health`}

Health check with metrics.```



**Response:**### 🕷️ POST `/crawl`

```jsonCrawls a website and **automatically indexes** the content.

{

  "status": "ok",**Request:**

  "metrics": {```json

    "count": 10,{

    "p50_ms": 2.5,  "start_url": "https://example.com",

    "p95_ms": 8.3  "max_pages": 40,

  }  "max_depth": 2,

}  "crawl_delay_ms": 500

```}

```

### 🕷️ `POST /crawl`

Crawls website and auto-indexes content.**Response:**

```json

**Request:**{

```json  "page_count": 25,

{  "skipped_count": 15,

  "start_url": "https://example.com",  "indexed": true,

  "max_pages": 40,  "vector_count": 50,

  "max_depth": 2,  "urls": ["https://example.com", ...],

  "crawl_delay_ms": 500  "skipped_reasons": {

}    "off_domain": 8,

```    "duplicate": 5,

    "error": 2

**Response:**  }

```json}

{```

  "page_count": 25,

  "skipped_count": 15,### 💬 POST `/ask`

  "indexed": true,Ask questions and get grounded answers with sources.

  "vector_count": 50

}**Request:**

``````json

{

### 💬 `POST /ask`  "question": "What are the top 10 SUVs with highest sales?",

Ask questions, get grounded answers.  "top_k": 6

}

**Request:**```

```json

{**Response:**

  "question": "What are the top 10 SUVs?",```json

  "top_k": 6{

}  "answer": "1/10: Hyundai Creta - 18,861 units (+19% YoY)\n2/10: Mahindra Scorpio - 18,372 units (+27% YoY)\n...",

```  "sources": [

    {

**Response:**      "url": "https://example.com/suv-sales",

```json      "title": "Top 10 SUVs with Highest Sales",

{      "snippet": "Updated 14 October 2025... (1500 chars)"

  "answer": "1/10: Hyundai Creta - 18,861 units\n2/10: Mahindra Scorpio...",    }

  "sources": [  ],

    {  "timings": {

      "url": "https://example.com/article",    "retrieval_ms": 2.3,

      "title": "Top 10 SUVs",    "generation_ms": 0.8,

      "snippet": "..."    "total_ms": 3.1

    }  }

  ],}

  "timings": {```

    "retrieval_ms": 2.3,

    "total_ms": 3.1### 📚 GET `/docs`

  }Interactive API documentation (Swagger UI).

}

```Visit http://localhost:8000/docs for full API exploration.



### 📚 `GET /docs`## 🎯 How It Works

Interactive API documentation (Swagger UI).

### 1. Crawling

---- Starts from a URL and follows links within the same domain

- Respects crawl delays (default: 500ms) for politeness

## 🎯 How It Works- Cleans HTML using Trafilatura (removes ads, nav, footers)

- Configurable max pages (1-1000) and depth (0-10)

### 1. Crawling

- Follows links within same domain### 2. Indexing (Automatic)

- Respects crawl delays (default: 500ms)- Splits content into 800-character chunks with 15% overlap

- Cleans HTML content (removes ads, nav, footers)- Builds BM25 index (keyword search)

- Configurable: max pages (1-1000), depth (0-10)- Builds TF-IDF vectors (semantic similarity)

- Stores in JSONL files for fast access

### 2. Indexing

- Splits into 800-char chunks with 15% overlap### 3. Retrieval

- Builds BM25 index (keyword search)- **Hybrid Search**: Combines BM25 + TF-IDF results

- Builds TF-IDF vectors (semantic similarity)- **Reciprocal Rank Fusion**: Merges rankings intelligently (c=30)

- Stores in JSONL format- **Relevance Filtering**: Only shows sources scoring ≥50% of top result

- **Smart Snippets**: Top result gets 1500 chars, others get 800/400 chars

### 3. Retrieval

- **Hybrid Search**: BM25 + TF-IDF fusion### 4. Answer Generation

- **RRF Algorithm**: Reciprocal Rank Fusion (c=30)- **List Detection**: Auto-formats top-N questions (e.g., "top 10 SUVs")

- **Relevance Filter**: Only shows sources ≥50% of top score- **Clean Extraction**: Removes metadata, timestamps, image credits

- **Smart Snippets**: Top result gets 2000 chars- **Source Attribution**: Every answer linked to original URLs

- **Refusal Logic**: Returns "Not found" when confidence < 0.03

### 4. Answer Generation

- **List Detection**: Auto-formats top-N questions## ⚙️ Configuration

- **Clean Extraction**: Removes metadata & timestamps

- **Source Attribution**: Links to original URLs### Default Settings

- **Refusal Logic**: Returns "Not found" when confidence < 0.03- **Max Pages**: 40 (configurable 1-1000)

- **Crawl Delay**: 500ms (configurable 100-5000ms)

---- **Chunk Size**: 800 characters

- **Chunk Overlap**: 120 characters (15%)

## ⚙️ Configuration- **Top-K Results**: 6

- **Refusal Threshold**: 0.03

### Default Settings- **Relevance Threshold**: 50% of top score

| Setting | Default | Range |

|---------|---------|-------|### Performance

| Max Pages | 40 | 1-1000 |- **Query Speed**: 1-5ms after indexing

| Crawl Delay | 500ms | 100-5000ms |- **Crawl Speed**: 20-60 seconds for 30-50 pages

| Chunk Size | 800 chars | - |- **Memory**: Low (no GPU required)

| Chunk Overlap | 120 chars (15%) | - |- **Storage**: ~1MB per 50 pages crawled

| Top-K Results | 6 | - |

| Refusal Threshold | 0.03 | - |## 📁 Project Structure

| Relevance Threshold | 50% of top | - |

```

### Performance Metricsrag-fastapi/

- **Query Speed**: 1-5ms after indexing├── app/

- **Crawl Speed**: 20-60 seconds for 30-50 pages│   ├── api.py              # FastAPI endpoints

- **Memory**: Low (no GPU required)│   ├── schemas.py          # Pydantic models

- **Storage**: ~1MB per 50 pages│   └── observability.py    # Metrics & timing

├── crawl/

---│   └── crawler.py          # Web crawler

├── index/

## 📁 Project Structure│   ├── chunk.py            # Text chunking

│   ├── bm25.py             # BM25 search

```│   └── vector.py           # TF-IDF vectors

rag-fastapi/├── retrieve/

├── app/│   └── hybrid.py           # Hybrid search + RRF

│   ├── api.py              # FastAPI endpoints├── static/

│   ├── schemas.py          # Pydantic models│   └── index.html          # Web UI

│   └── observability.py    # Metrics & timing├── data/                   # Auto-generated

├── crawl/│   ├── pages.jsonl         # Crawled pages

│   └── crawler.py          # Web crawler│   ├── chunks.jsonl        # Indexed chunks

├── index/│   └── indexes/            # BM25 + TF-IDF indexes

│   ├── chunk.py            # Text chunking├── start.ps1 / start.sh    # Production startup

│   ├── bm25.py             # BM25 search├── requirements.txt        # Dependencies

│   └── vector.py           # TF-IDF vectors└── README.md               # This file

├── retrieve/```

│   └── hybrid.py           # Hybrid search + RRF

├── static/## 📚 Documentation

│   └── index.html          # Web UI

├── data/                   # Auto-generated- **[USER_GUIDE.md](USER_GUIDE.md)** — Step-by-step guide for non-technical users

│   ├── pages.jsonl         # Crawled pages- **[DEPLOYMENT.md](DEPLOYMENT.md)** — How to deploy to production

│   ├── chunks.jsonl        # Indexed chunks- **[README_PRODUCTION.md](README_PRODUCTION.md)** — Technical deep-dive

│   └── indexes/            # Search indexes- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** — Quick reference card

├── start.ps1 / start.sh    # Startup scripts

├── requirements.txt        # Dependencies## 🤝 Contributing

└── README.md               # This file

```Contributions are welcome! Please feel free to submit a Pull Request.



---## 📄 License



## 📚 DocumentationThis project is licensed under the MIT License.



- **[USER_GUIDE.md](USER_GUIDE.md)** — Step-by-step user guide## 🙏 Acknowledgments

- **[DEPLOYMENT.md](DEPLOYMENT.md)** — Production deployment guide

- **[README_PRODUCTION.md](README_PRODUCTION.md)** — Technical deep-diveBuilt with:

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** — Quick reference card- [FastAPI](https://fastapi.tiangolo.com/) — Modern, fast web framework

- [Trafilatura](https://github.com/adbar/trafilatura) — Content extraction

---- [rank-bm25](https://github.com/dorianbrown/rank_bm25) — BM25 search

- [scikit-learn](https://scikit-learn.org/) — TF-IDF vectors

## 🎨 Screenshots

---

### Web UI

Beautiful purple gradient interface with real-time status updates:**Questions?** Open an issue or check the [documentation](docs/).

- Paste any URL

- Automatic crawling & indexing**Ready to use?** Run `.\start.ps1` and open http://localhost:8000 🚀

- Instant answers with source citations#   I n t e l l i g e n t - Q - A - S y s t e m 

 

### Example Query 
**Question:** "What are the top 10 SUVs with highest sales?"

**Answer:**
```
1/10: Hyundai Creta - 18,861 units (+19% YoY)
2/10: Mahindra Scorpio - 18,372 units (+27% YoY)
3/10: Mahindra XUV 700 - 9,764 units (+1% YoY)
... (complete list of 10 items)
```

**Source:** Links to original article with full context.

---

## 🛠️ Technology Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — Modern, fast web framework
- **[Trafilatura](https://github.com/adbar/trafilatura)** — Content extraction
- **[rank-bm25](https://github.com/dorianbrown/rank_bm25)** — BM25 search algorithm
- **[scikit-learn](https://scikit-learn.org/)** — TF-IDF vectors
- **[httpx](https://www.python-httpx.org/)** — Async HTTP client
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** — Data validation

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Special thanks to:
- FastAPI team for the excellent web framework
- Trafilatura for robust content extraction
- The open-source community for amazing tools

---

## 📞 Contact

**Surya Sriram D**  
GitHub: [@SuryaSriramD](https://github.com/SuryaSriramD)  
Repository: [Intelligent-Q-A-System](https://github.com/SuryaSriramD/Intelligent-Q-A-System)

---

## 🚀 Ready to Use?

```bash
.\start.ps1  # Windows
./start.sh   # Linux/Mac
```

Open **http://localhost:8000** and start asking questions! 🎉
