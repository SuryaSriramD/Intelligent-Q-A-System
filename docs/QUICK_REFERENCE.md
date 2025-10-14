# ⚡ Quick Reference Card

## 🚀 Start the System

```powershell
# Windows
.\start.ps1

# Linux/Mac
./start.sh
```

**Then open:** http://localhost:8000

---

## 📍 Important URLs

| What | URL |
|------|-----|
| **Web UI** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health |

---

## 🎯 Quick Workflow

1. **Enter URL** → https://example.com
2. **Click** → "Start Crawling & Indexing"
3. **Wait** → 20-60 seconds
4. **Ask** → Type your question
5. **Get** → Answer with sources in 1-5ms

---

## 🔌 API Quick Reference

### Crawl Website
```bash
POST /crawl
{
  "start_url": "https://example.com",
  "max_pages": 40,
  "max_depth": 2,
  "crawl_delay_ms": 500
}
```

### Ask Question
```bash
POST /ask
{
  "question": "What is this website about?",
  "top_k": 6
}
```

### One-Shot (Crawl + Ask)
```bash
POST /crawl-and-ask
{
  "start_url": "https://example.com",
  "question": "What is this website about?",
  "max_pages": 10
}
```

---

## ⚙️ Default Settings

| Setting | Default | Range |
|---------|---------|-------|
| Max Pages | 40 | 1-1000 |
| Max Depth | 2 | 0-10 |
| Crawl Delay | 500ms | 100-5000ms |
| Chunk Size | 800 chars | 200-4000 |
| Top K | 6 | 1-20 |

---

## 🏗️ Architecture at a Glance

```
User → Web UI → FastAPI
              ↓
         Crawler → Index (BM25 + TF-IDF)
              ↓
         Retrieval → Hybrid Search
              ↓
         Answer → Sources + Citations
```

---

## 📊 Performance

- **Crawl:** 2-3 pages/sec (with delays)
- **Index:** ~50ms per 100 chunks
- **Query:** 1-5ms (p95)
- **Throughput:** 200+ queries/sec

---

## 🛠️ Common Commands

### Check Health
```bash
curl http://localhost:8000/health
```

### View Logs
```bash
# If running with systemd
journalctl -u rag-api -f
```

### Stop Server
```bash
# In terminal where server is running
Ctrl + C
```

### Restart Server
```bash
# Stop first, then:
.\start.ps1  # Windows
./start.sh   # Linux/Mac
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Server won't start | Check if port 8000 is free |
| UI won't load | Verify server is running on port 8000 |
| Crawl fails | Check URL is valid and accessible |
| No answers | Ensure crawl completed successfully |
| Slow performance | Reduce max_pages or increase delay |

---

## 📚 Documentation

- **Technical:** README_PRODUCTION.md
- **Users:** USER_GUIDE.md
- **Deploy:** DEPLOYMENT.md

---

## 🎯 Example Websites to Try

1. **News:** https://www.republicworld.com
2. **Tech:** https://www.python.org
3. **Docs:** https://fastapi.tiangolo.com
4. **Company:** Any company website
5. **Blog:** Any blog or content site

---

## 💡 Pro Tips

- Use 30-50 pages for good coverage
- Keep crawl delay at 500ms+ (be polite!)
- Ask specific questions for best results
- Click source URLs to verify answers
- System refuses when uncertain (feature!)

---

**Need help?** Check the full docs or visit /docs for API reference.
