# 🎯 Quick Start Guide - For Non-Technical Users

## What is this?

This is an **Intelligent Q&A System** that:
1. Reads any website you give it
2. Understands the content
3. Answers your questions about it

**No coding required!** Just use your web browser.

---

## How to Use (3 Simple Steps)

### Step 1: Start the System

**Windows Users:**
1. Open PowerShell in the project folder
2. Type: `.\start.ps1`
3. Press Enter

**Mac/Linux Users:**
1. Open Terminal in the project folder
2. Type: `./start.sh`
3. Press Enter

You'll see:
```
╔══════════════════════════════════════════════════════════════════╗
║           RAG API - INTELLIGENT Q&A SYSTEM                       ║
╚══════════════════════════════════════════════════════════════════╝

Starting production server...
  • Web UI: http://localhost:8000
```

### Step 2: Open Your Browser

Go to: **http://localhost:8000**

You'll see a beautiful purple and white interface.

### Step 3: Use the System

#### A. Crawl a Website

1. **Enter a URL** in the first box
   - Example: `https://www.wikipedia.org`
   - Example: `https://www.news.com`
   - Any website works!

2. **Configure Settings** (optional)
   - **Max Pages**: How many pages to read (default: 40)
   - **Max Depth**: How deep to go into links (default: 2)
   - **Crawl Delay**: Time between requests (default: 500ms)

3. **Click the Purple Button**: "🚀 Start Crawling & Indexing"

4. **Wait 20-60 seconds** while it reads the website

5. **Success!** You'll see:
   - ✅ Pages crawled: 40
   - ✅ Chunks indexed: 120
   - ✅ Ready for questions!

#### B. Ask Questions

1. **Type your question** in the text box
   - "What is this website about?"
   - "What are the latest news topics?"
   - "Who is the CEO?"
   - Any question!

2. **Click**: "💬 Get Answer"

3. **Get instant answer** (1-5 milliseconds!)
   - See the answer
   - See the sources (URLs where info came from)
   - Click source URLs to verify

4. **Ask more questions!** As many as you want.

---

## Example Workflow

### Example 1: News Website

```
1. Enter URL: https://www.republicworld.com
2. Click "Start Crawling"
3. Wait 30 seconds
4. ✅ 40 pages crawled!

Questions to try:
- "What are the latest headlines?"
- "What world news is covered?"
- "What is the election news?"
```

### Example 2: Company Website

```
1. Enter URL: https://www.company.com
2. Click "Start Crawling"
3. Wait 45 seconds
4. ✅ 50 pages crawled!

Questions to try:
- "What products does this company offer?"
- "What is their pricing?"
- "Do they have an API?"
```

---

## What You'll See

### During Crawling
```
🔄 Crawling and indexing... This may take 20-60 seconds.
```

### After Success
```
✅ Success!

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Pages Crawled   │  │ Chunks Indexed  │  │ Pages Skipped   │
│      40         │  │      120        │  │       15        │
└─────────────────┘  └─────────────────┘  └─────────────────┘

🎉 Ready for questions! Start asking below.
```

### When You Ask a Question
```
💬 Answer:
Based on the crawled content, here are the relevant findings:

1. From 'About Us' (https://example.com/about):
   "We are a leading technology company..."

📚 Sources (3):
[1] About Us
    https://example.com/about
    We are a leading technology company that provides...

[2] Products
    https://example.com/products
    Our main products include cloud services...

⏱️ Response time: 2.34ms (retrieval: 2.10ms)
```

---

## Tips & Tricks

### ✅ DO:
- Use popular, well-structured websites
- Ask specific questions
- Try different questions to explore content
- Click source URLs to verify information
- Use 30-50 pages for good coverage

### ❌ DON'T:
- Ask questions the website doesn't cover (it will refuse)
- Use websites that require login
- Crawl too many pages (>100) - it takes time
- Set crawl delay too low (<300ms) - be polite!

---

## Common Questions

**Q: How long does crawling take?**
A: 20-60 seconds for 40 pages (depends on website speed)

**Q: Can I crawl multiple websites?**
A: Yes! Just crawl a new website. It replaces the previous one.

**Q: What if it says "Not found in crawled content"?**
A: The answer isn't on the website you crawled. Try a different question or crawl a different website.

**Q: Is this using AI?**
A: It uses smart search (BM25 + TF-IDF) to find relevant content. The answers are extracted directly from the website (no generation/hallucination).

**Q: Can I use this for my work?**
A: Yes! It's production-ready. Great for:
- Research
- Competitive analysis
- Customer support
- Documentation search
- Content discovery

---

## Troubleshooting

### Server Won't Start
- Make sure port 8000 is not in use
- Check if you installed dependencies: `pip install -r requirements.txt`

### Crawling Fails
- Check if the URL is correct
- Try a different website
- Check your internet connection

### No Answers
- Make sure crawling finished successfully
- Check if your question is about the crawled content
- Try rephrasing your question

### Slow Performance
- Reduce max_pages to 20-30
- Increase crawl_delay to 1000ms
- Close other applications

---

## Need Help?

1. Check the server is running (look for the message in terminal)
2. Visit http://localhost:8000 in your browser
3. Try the API docs: http://localhost:8000/docs
4. Check health: http://localhost:8000/health

---

## Stop the System

In the terminal where the server is running:
- Press `Ctrl + C`
- Wait for "Shutting down"
- Done!

---

**That's it! You're ready to explore any website with intelligent Q&A.** 🚀
