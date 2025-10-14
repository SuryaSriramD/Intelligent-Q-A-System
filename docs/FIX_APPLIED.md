# 🔧 Quick Fix Applied

## Issue Found
When running the demo, the `/crawl` endpoint threw an error:
```
'pydantic_core._pydantic_core.Url' object has no attribute 'decode'
```

## Root Cause
Pydantic's `HttpUrl` type returns a URL object, not a plain string. When this object was passed to `urllib.parse.urlparse()` in the crawler, it caused an error.

## Fix Applied
Updated `app/api.py` to convert the Pydantic URL to a string:

```python
result = run_crawl(
    start_url=str(req.start_url),  # Convert Pydantic URL to string
    max_pages=req.max_pages,
    max_depth=req.max_depth,
    crawl_delay_ms=req.crawl_delay_ms,
)
```

Also added better error handling to the demo script.

## How to Apply

**⚠️ You need to restart the server for the fix to take effect!**

### Step 1: Stop Current Server
In the server terminal, press `Ctrl+C`

### Step 2: Restart Server
```powershell
.\.venv\Scripts\uvicorn.exe app.api:app --port 8000
```

Wait for:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 3: Run Demo Again
```powershell
.\.venv\Scripts\python.exe demo.py
```

## Expected Result

After restarting, the demo should work completely:

```
======================================================================
  1. Health Check
======================================================================
✓ Status: ok

======================================================================
  2. Crawling Example.com (5 pages)
======================================================================
✓ Crawled 1 pages
✓ Skipped X URLs

======================================================================
  3. Building Search Index
======================================================================
✓ Created 5 searchable chunks

======================================================================
  4a. Answerable Question
======================================================================
Answer with sources and URLs...

======================================================================
  4b. Unanswerable Question (Refusal)
======================================================================
Answer: Not found in crawled content.
✓ Properly refused to hallucinate!

======================================================================
  ✅ Demo Complete!
======================================================================
```

## Status

- [x] Issue identified
- [x] Fix applied to code
- [ ] **Server needs restart** ← Do this now!
- [ ] Test with demo

Once you restart the server, everything should work perfectly! 🎉
