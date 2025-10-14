# 🔍 Eval Results & Tuning

## Initial Evaluation Results

### ❌ Issue Found: Refusal Rate 0%

**Problem:** The system was answering ALL questions, including unanswerable ones!

```json
"unanswerable": {
  "count": 5,
  "correct_refusal_rate": 0.0,  ← PROBLEM!
  "provided_closest_rate": 0.0
}
```

**Root Cause:**
- Initial threshold was 0.01
- With only 1 page crawled (example.com), all questions matched the same chunk
- Fusion scores were 0.03-0.04 (above threshold)
- System couldn't distinguish unanswerable from answerable

**Example:**
Question: "What is the stock price today?"
- BM25 score: -0.2747
- TF-IDF score: 0.0
- **Fusion score: 0.0328** ← Above 0.01 threshold
- Result: Incorrectly answered instead of refusing

## ✅ Fix Applied

### Threshold Adjustment

**Changed:**
```python
REFUSAL_THRESHOLD = 0.01  # Old - too permissive
```

**To:**
```python
REFUSAL_THRESHOLD = 0.05  # New - more conservative

# Additional check: refuse when all chunks score equally (no clear winner)
should_refuse = (
    not results or 
    max_score < REFUSAL_THRESHOLD or
    (score_variance < 0.001 and max_score < 0.1)
)
```

### Reasoning

1. **Higher threshold (0.05)**: Requires stronger match to answer
2. **Score variance check**: If all chunks score about the same, likely no good match
3. **Conservative approach**: Better to refuse than hallucinate

## 🔄 Re-run Required

To apply the fix:

```powershell
# 1. Restart server (in uvicorn terminal, Ctrl+C then restart)
uvicorn app.api:app --port 8000

# 2. Re-run evaluation
.\.venv\Scripts\python.exe evals\run_eval.py
```

## Expected New Results

After fix:
```json
"unanswerable": {
  "count": 5,
  "correct_refusal_rate": 1.0,  ← Should be 100%!
  "provided_closest_rate": 1.0   ← With closest matches
}
```

## Key Learnings

### 1. **Threshold Tuning is Dataset-Dependent**
- Small dataset (1 page) → Need higher threshold
- Large dataset (100+ pages) → Can use lower threshold
- Monitor refusal rate and adjust

### 2. **Score Variance Matters**
- If all chunks score similarly → No clear winner → Should refuse
- If one chunk scores much higher → Confident match → Can answer

### 3. **Test with Trap Questions**
- Critical to include unanswerable questions in eval
- Caught the issue immediately
- 100% refusal rate on traps is non-negotiable

## Threshold Tuning Guide

| Dataset Size | Suggested Threshold | Rationale |
|--------------|-------------------|-----------|
| 1-5 pages | 0.05-0.10 | High false positive risk |
| 10-50 pages | 0.03-0.05 | Moderate diversity |
| 50-100 pages | 0.02-0.03 | Good diversity |
| 100+ pages | 0.01-0.02 | High diversity |

## Additional Improvements (Future)

1. **Dynamic thresholds** based on score distribution
2. **Confidence scores** in response
3. **Semantic similarity** check (not just keyword matching)
4. **Cross-encoder reranking** for better precision

## Documentation Updates Needed

After re-running with fix:

1. ✅ Update README with final eval results
2. ✅ Document threshold tuning process
3. ✅ Note the importance of trap questions
4. ✅ Add this as a design decision

---

**Status: Fix applied, awaiting re-run to verify 100% refusal rate**
