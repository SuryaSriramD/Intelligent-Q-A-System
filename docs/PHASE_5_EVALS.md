# 🎯 Phase 5: Build Evaluation Suite

## What We're Building

A **tiny but real** evaluation system that:
1. **Auto-generates** questions from crawled content
2. **Measures retrieval quality** (recall@k, keyword matching)
3. **Validates refusal behavior** (unanswerable questions)
4. **Tracks performance** (timing metrics)

## Files Created

```
evals/
├── build_eval.py        # Auto-generate Q&A eval set
├── run_eval.py          # Run evaluation & measure metrics
├── eval_questions.json  # Generated questions (after build)
└── eval_report.json     # Results (after run)
```

## How to Run

### Step 1: Build Evaluation Set

This auto-generates questions from your crawled content:

```powershell
python evals/build_eval.py
```

**What it does:**
- Analyzes crawled pages
- Extracts ~10-15 answerable questions (from headings, sentences)
- Adds 5 "trap" questions (unanswerable)
- Saves to `evals/eval_questions.json`

**Expected output:**
```
=== Building Evaluation Set ===

Loaded 5 pages

✓ Generated 17 questions:
  - 12 answerable
  - 5 unanswerable (trap questions)

Saved to: D:\rag-fastapi\evals\eval_questions.json
```

### Step 2: Run Evaluation

This runs all questions through your API and measures quality:

```powershell
python evals/run_eval.py
```

**What it measures:**

**For Answerable Questions:**
- Keyword Recall: Are expected keywords in retrieved chunks?
- URL Found Rate: Is the expected source URL retrieved?
- Has Answer Rate: Does it provide a real answer?
- Has Sources Rate: Are sources cited?

**For Unanswerable Questions:**
- Correct Refusal Rate: Does it refuse appropriately?
- Provided Closest Rate: Does it show closest matches?

**For Performance:**
- Avg retrieval time
- Avg total time

**Expected output:**
```
=== Running Evaluation ===

Loaded 17 questions

[1/17] answerable: What is this domain about?...
[2/17] answerable: What information is available about 'Example'?...
...
[17/17] unanswerable: What is the stock price today?...

✓ Evaluation complete!
Saved to: D:\rag-fastapi\evals\eval_report.json

=== Evaluation Summary ===

Total questions: 17
Successful: 17
Errors: 0

Answerable Questions:
  • Count: 12
  • Keyword Recall: 75.00%
  • URL Found Rate: 83.33%
  • Has Answer Rate: 91.67%
  • Has Sources Rate: 100.00%
  • Avg Sources: 3.5

Unanswerable Questions (Refusals):
  • Count: 5
  • Correct Refusal Rate: 100.00%
  • Provided Closest Matches: 100.00%

Performance:
  • Avg Retrieval: 45.2ms
  • Avg Total: 58.7ms
```

### Step 3: Review Results

```powershell
# View the full report
Get-Content evals\eval_report.json | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

## Make Commands

Quick shortcuts:

```bash
make eval-build    # Generate eval questions
make eval-run      # Run evaluation
make eval          # Build + Run (full eval)
```

## What Good Results Look Like

### ✅ Strong Performance

```
Answerable Questions:
  • Keyword Recall: >70%      ← Good retrieval
  • URL Found Rate: >80%       ← Finding right sources
  • Has Answer Rate: >90%      ← Providing answers
  • Has Sources Rate: 100%     ← Always citing

Unanswerable Questions:
  • Correct Refusal Rate: 100% ← Never hallucinates
  • Provided Closest: >80%     ← Transparent refusals

Performance:
  • Avg Retrieval: <100ms      ← Fast
  • Avg Total: <200ms          ← Responsive
```

### ⚠️ Needs Improvement

- **Low Keyword Recall (<50%)**: Chunking might be too aggressive
- **Low URL Found Rate (<60%)**: Retrieval not finding right sources
- **Low Has Answer Rate (<70%)**: Too many refusals (threshold too high)
- **Refusal Rate <100%**: Hallucinating on unanswerable questions! ⚠️

## Troubleshooting

### "No pages found"
```powershell
# Run crawl first
Invoke-RestMethod -Uri http://localhost:8000/crawl -Method POST -Body '{"start_url":"https://example.com","max_pages":10,"max_depth":2}' -ContentType "application/json"
```

### "Server not running"
```powershell
# Start server
.\.venv\Scripts\uvicorn.exe app.api:app --port 8000
```

### Few questions generated
- Normal if you only crawled a few pages
- Crawl more pages (increase `max_pages`) for more eval questions

## What to Do with Results

### 1. Document in README
Add a section showing your eval results:
```markdown
## Evaluation Results

Ran automated evaluation on 17 questions (12 answerable, 5 trap):
- Keyword Recall: 75%
- Correct Refusals: 100%
- Avg Retrieval: 45ms
```

### 2. Tune if Needed
- **Low recall?** Adjust chunk size/overlap
- **Slow?** Reduce top_k
- **Too many refusals?** Lower refusal threshold

### 3. Include in Report
- Copy `eval_report.json` to your submission
- Shows you validated the system empirically

## Next Steps

After running evals:

1. ✅ Review `eval_report.json`
2. ✅ Document results in README
3. ➡️ **Proceed to Phase 6: Polish README**
   - Add architecture diagram
   - Add trade-offs section
   - Add limitations
   - Add extensions

## Time Investment

- **Build eval script**: Already done! ✅
- **Run evaluation**: ~2-3 minutes
- **Review results**: ~5 minutes
- **Document findings**: ~5 minutes

**Total: ~10-15 minutes**

---

**Status: Phase 5 infrastructure complete! Run the evals now.** 🎯
