# 🚀 Quick Start Guide - RAG FastAPI

## ✅ Setup Complete!

Dependencies are installed. You're ready to run the API!

## 🎯 Two-Terminal Setup (Recommended)

### Terminal 1: Start Server
```powershell
cd d:\rag-fastapi
.\.venv\Scripts\Activate
uvicorn app.api:app --port 8000
```

Wait for: `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2: Test the API

#### Test 1: Health Check
```powershell
Invoke-RestMethod -Uri http://localhost:8000/health | ConvertTo-Json
```

Expected: Status "ok" with metrics

#### Test 2: Crawl
```powershell
$body = @{
    start_url = "https://example.com"
    max_pages = 5
    max_depth = 1
    crawl_delay_ms = 300
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/crawl -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 10
```

Expected: page_count > 0, list of URLs

#### Test 3: Index
```powershell
$body = @{
    chunk_size = 800
    chunk_overlap = 120
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/index -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json
```

Expected: vector_count > 0

#### Test 4: Ask (Answerable)
```powershell
$body = @{
    question = "What is this website about?"
    top_k = 6
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/ask -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 10
```

Expected: Answer with sources and URLs

#### Test 5: Ask (Refusal)
```powershell
$body = @{
    question = "What is the company revenue in 2025?"
    top_k = 6
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/ask -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 10
```

Expected: "Not found in crawled content." with closest matches

## 🎨 Using Make Commands

If you have `make` installed, you can use these shortcuts:

```bash
# Terminal 1
make run

# Terminal 2
make health
make crawl
make index
make ask
make ask-refuse
```

## 🔍 Run Full Demo

```powershell
# Terminal 1: Start server first
uvicorn app.api:app --port 8000

# Terminal 2: Run demo script
cd d:\rag-fastapi
.\.venv\Scripts\python.exe demo.py
```

This will:
1. Check health
2. Crawl 5 pages from example.com
3. Build search indexes
4. Ask answerable question
5. Test refusal mechanism

## 📊 Expected Output

### Answerable Question
```
Answer:
Based on the crawled content, here are the relevant findings:

1. From 'Example Domain' (https://example.com):
   "This domain is for use in illustrative examples..."

Performance:
  Retrieval: 42.3ms
  Generation: 8.1ms
  Total: 52.4ms
```

### Refusal (Unanswerable)
```
Answer: Not found in crawled content.

Closest matches shown for transparency:
  1. Example Domain
     This domain is for use in illustrative examples...

Performance:
  Retrieval: 41.2ms
  Total: 42.5ms
```

## 🐛 Troubleshooting

### Port already in use
```powershell
# Use different port
uvicorn app.api:app --port 8001

# Then adjust URLs to localhost:8001
```

### Server won't start
```powershell
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
.\.venv\Scripts\pip.exe install -r requirements.txt
```

### Can't connect to server
```powershell
# Check if server is running
netstat -ano | findstr :8000

# Test health endpoint
curl http://localhost:8000/health
```

## 🎯 Success Checklist

- [ ] Server starts without errors
- [ ] `/health` returns 200 OK
- [ ] `/crawl` fetches pages successfully
- [ ] `/index` creates chunks
- [ ] `/ask` returns grounded answers
- [ ] `/ask` refuses unanswerable questions gracefully
- [ ] Timings are present in responses
- [ ] Sources include URLs

## 📚 Next Steps

Once everything works:
- Review [README.md](README.md) for full API documentation
- Check [PHASE_2-4_COMPLETE.md](PHASE_2-4_COMPLETE.md) for architecture details
- See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing
- Proceed to Phase 5: Build evaluation suite

---

**🎉 You're all set! Happy testing!**
