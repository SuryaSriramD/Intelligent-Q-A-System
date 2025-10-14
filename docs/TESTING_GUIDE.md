# Testing Guide

## Quick Test Commands

### 1. Health Check
```bash
curl http://localhost:8000/health
```

Expected: `{"status": "ok", "metrics": {...}}`

### 2. Crawl Test
```powershell
# Windows PowerShell
Invoke-RestMethod -Uri http://localhost:8000/crawl -Method POST -ContentType "application/json" -Body '{"start_url":"https://example.com","max_pages":5,"max_depth":1,"crawl_delay_ms":300}' | ConvertTo-Json -Depth 10
```

Expected output:
- `page_count` > 0
- `skipped_reasons` breakdown
- List of `urls`

### 3. Index Test
```powershell
Invoke-RestMethod -Uri http://localhost:8000/index -Method POST -ContentType "application/json" -Body '{"chunk_size":800,"chunk_overlap":120}' | ConvertTo-Json -Depth 10
```

Expected:
- `vector_count` > 0
- Empty `errors` array

### 4. Ask Test (Answerable)
```powershell
Invoke-RestMethod -Uri http://localhost:8000/ask -Method POST -ContentType "application/json" -Body '{"question":"What is this website about?","top_k":6}' | ConvertTo-Json -Depth 10
```

Expected:
- Non-empty `answer`
- Multiple `sources` with URLs
- Timing breakdown in `timings`
- Debug info in `retrieval_debug`

### 5. Ask Test (Refusal)
```powershell
Invoke-RestMethod -Uri http://localhost:8000/ask -Method POST -ContentType "application/json" -Body '{"question":"What is the company revenue in 2025?","top_k":6}' | ConvertTo-Json -Depth 10
```

Expected:
- `answer` = "Not found in crawled content."
- Empty `sources`
- Non-empty `closest` array
- Timing info still present

## Automated Testing

### Run Full Test Suite
```bash
python test_api_flow.py
```

### Run Demo
```bash
python demo.py
```

## Manual Verification Checklist

- [ ] Server starts without errors
- [ ] `/health` returns 200 OK
- [ ] `/crawl` successfully fetches pages
- [ ] `/crawl` respects `max_pages` limit
- [ ] `/crawl` tracks skip reasons correctly
- [ ] `/index` creates chunks
- [ ] `/index` builds both indexes (BM25 + TF-IDF)
- [ ] `/ask` returns grounded answer for valid questions
- [ ] `/ask` shows sources with URLs
- [ ] `/ask` includes timing breakdown
- [ ] `/ask` provides debug info
- [ ] `/ask` refuses unanswerable questions
- [ ] `/ask` shows closest matches on refusal
- [ ] Metrics (p50/p95) are tracked
- [ ] All responses are valid JSON

## Performance Testing

### Measure Request Times
```powershell
# Time a single request
Measure-Command { 
    Invoke-RestMethod -Uri http://localhost:8000/ask -Method POST -ContentType "application/json" -Body '{"question":"What is this?","top_k":6}' 
}
```

### Expected Performance
- Health check: <10ms
- Crawl (5 pages): ~2-5 seconds
- Index (20 chunks): ~200-500ms
- Ask: <100ms

## Common Issues

### Issue: "Index not built"
**Solution:** Run `/index` endpoint after crawling

### Issue: Empty sources
**Cause:** Question not found in content (working as designed)
**Expected:** Should see refusal message and closest matches

### Issue: Slow retrieval
**Check:** Number of chunks (should be <1000 for good performance)
**Solution:** Reduce `max_pages` in crawl or increase `chunk_size`

### Issue: Connection refused
**Check:** Is server running? `netstat -ano | findstr :8000`
**Solution:** Start server with `make run` or `uvicorn app.api:app`

## Debugging

### Enable Verbose Logging
Add to `app/api.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Data Files
```powershell
# Pages crawled
Get-Content data\pages.jsonl | Measure-Object

# Chunks created
Get-Content data\chunks.jsonl | Measure-Object
```

### Inspect Retrieval Scores
Look at `retrieval_debug` in response:
```json
{
  "bm25": [{"idx": 12, "score": 2.45}],
  "tfidf": [{"idx": 12, "score": 0.82}],
  "fusion": [{"idx": 12, "score": 0.04}]
}
```

Low scores (<0.01) trigger refusals.

## Test Different Sites

### Small Static Site
```json
{
  "start_url": "https://example.com",
  "max_pages": 5,
  "max_depth": 1
}
```

### Documentation Site
```json
{
  "start_url": "https://docs.python.org/3/",
  "max_pages": 20,
  "max_depth": 2
}
```

### Blog
```json
{
  "start_url": "https://blog.example.com",
  "max_pages": 30,
  "max_depth": 1
}
```

## Expected Behavior by Scenario

### Scenario 1: Answerable Question
**Input:** "What is X?"
**Output:**
- Structured answer with quotes
- 3-6 sources with URLs
- Retrieval < 50ms
- Non-zero generation time

### Scenario 2: Partially Answerable
**Input:** Question where some info exists
**Output:**
- Answer with available info
- Sources for what was found
- May have lower scores in debug

### Scenario 3: Unanswerable
**Input:** Question about uncrawled content
**Output:**
- "Not found in crawled content."
- Empty sources
- Closest 1-2 matches shown
- generation_ms = 0

### Scenario 4: Empty Index
**Input:** Ask before indexing
**Output:**
- 400 error
- "Index not built. Call /index first."

## Success Criteria

✅ All endpoints return valid JSON
✅ No 500 errors on valid input
✅ Timings are present and reasonable
✅ Sources always include URLs
✅ Refusals are graceful
✅ Metrics accumulate over time
✅ Debug info is present

## Report Template

Use this when testing:

```
Test Date: [DATE]
Server: localhost:8000

ENDPOINTS TESTED:
[ ] GET /health - Status: ___ Response time: ___ms
[ ] POST /crawl - Status: ___ Pages: ___ Time: ___s
[ ] POST /index - Status: ___ Chunks: ___ Time: ___ms
[ ] POST /ask (answerable) - Status: ___ Sources: ___ Time: ___ms
[ ] POST /ask (refusal) - Status: ___ Refused: [Y/N]

OBSERVATIONS:
- 
- 

ISSUES:
- 

PERFORMANCE:
- p50 latency: ___ms
- p95 latency: ___ms
- Retrieval speed: ___ms average
```
