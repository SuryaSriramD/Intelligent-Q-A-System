# Real-Time RAG API

## What Changed

The API now supports **real-time workflows** where users can:
1. Provide a URL and get it crawled + indexed immediately
2. Ask questions about that specific URL's content
3. Switch to different URLs to create fresh contexts

## Updated Endpoints

### 1. POST /crawl (Enhanced)
**Now auto-indexes after crawling!**

```bash
curl -X POST http://localhost:8000/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "start_url": "https://example.com",
    "max_pages": 10,
    "max_depth": 2,
    "crawl_delay_ms": 400
  }'
```

**Response:**
```json
{
  "page_count": 1,
  "skipped_count": 0,
  "urls": ["https://example.com/"],
  "skipped_reasons": {...},
  "indexed": true,        ← NEW
  "vector_count": 1       ← NEW
}
```

### 2. POST /ask (Unchanged)
Works on the most recently crawled/indexed content.

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this domain about?",
    "top_k": 6
  }'
```

### 3. POST /crawl-and-ask (NEW!)
**One-shot endpoint: Crawl + Answer in a single request**

```bash
curl -X POST http://localhost:8000/crawl-and-ask \
  -H "Content-Type: application/json" \
  -d '{
    "start_url": "https://example.com",
    "question": "What is this website for?",
    "max_pages": 10,
    "top_k": 6
  }'
```

**Response:**
```json
{
  "crawl": {
    "page_count": 1,
    "skipped_count": 0,
    "urls": ["https://example.com/"],
    "indexed": true,
    "vector_count": 1
  },
  "answer": {
    "answer": "Example Domain is used...",
    "sources": [...],
    "timings": {...}
  }
}
```

### 4. POST /index (Still Available)
Optional - for manual re-indexing with different chunk parameters.

## Workflow Examples

### Traditional Workflow (2 steps)
```python
# Step 1: Crawl (auto-indexes)
POST /crawl {
  "start_url": "https://example.com",
  "max_pages": 10
}

# Step 2: Ask questions
POST /ask {
  "question": "What is this domain about?"
}
```

### One-Shot Workflow (1 step)
```python
# Crawl + Ask in one request
POST /crawl-and-ask {
  "start_url": "https://example.com",
  "question": "What is this domain about?",
  "max_pages": 10
}
```

## Use Cases

### Real-Time Research Assistant
```python
# User provides URL → Get instant answer
POST /crawl-and-ask
{
  "start_url": "https://docs.python.org/3/",
  "question": "How do I use async/await?",
  "max_pages": 20
}
```

### Multi-Turn Conversation
```python
# 1. Crawl once
POST /crawl {"start_url": "https://company.com", "max_pages": 50}

# 2. Ask multiple questions
POST /ask {"question": "What products do they offer?"}
POST /ask {"question": "What's their pricing?"}
POST /ask {"question": "Do they have an API?"}
```

### Context Switching
```python
# Each crawl creates fresh context
POST /crawl {"start_url": "https://site-a.com"}
POST /ask {"question": "About site A..."}

POST /crawl {"start_url": "https://site-b.com"}
POST /ask {"question": "About site B..."}
```

## Key Features

✅ **Auto-Indexing**: No manual /index call needed  
✅ **Separate Endpoints**: Each endpoint remains independent  
✅ **One-Shot Option**: Convenience endpoint for instant answers  
✅ **Context Management**: Each crawl replaces previous context  
✅ **Full Observability**: Timings, debug info, source citations  

## Testing

Run the demo:
```bash
python demo.py
```

Run real-time examples:
```bash
python example_realtime.py
```

Test one-shot endpoint:
```bash
make crawl-and-ask
```

## Implementation Notes

- `/crawl` automatically calls chunking + indexing after successful crawl
- Each crawl replaces the in-memory index (fresh context)
- `/index` endpoint still available for manual re-indexing with different parameters
- `/crawl-and-ask` internally calls `/crawl` then `/ask`
- All endpoints maintain backward compatibility
