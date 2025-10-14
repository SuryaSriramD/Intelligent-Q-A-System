# Phase 2-4 Complete: API Build Summary

## What We Built

### 1. Enhanced API Endpoints ✅

#### `/health`
- Returns system status and performance metrics
- Shows p50/p95 latencies from rolling window
- Useful for monitoring and debugging

#### `/crawl`
- Polite, in-domain web crawling
- Detailed skip tracking (off_domain, duplicate, error, non_http)
- Returns URLs crawled and skip reasons breakdown

#### `/index`
- DOM-aware chunking with configurable size/overlap
- Builds BM25 and TF-IDF indexes
- Returns vector count and any errors

#### `/ask` (Enhanced)
- **Hybrid retrieval** with BM25 + TF-IDF fusion
- **Smart refusals** with score threshold (< 0.01)
- **Detailed timings** (retrieval_ms, generation_ms, total_ms)
- **Debug info** showing BM25, TF-IDF, and fusion scores
- **Closest matches** shown on refusals for transparency
- **Grounded answers** with source attribution

### 2. Refusal Mechanism ✅

Key features:
- Score threshold of 0.01 (tunable)
- Returns "Not found in crawled content" when below threshold
- Shows 1-2 closest matches for transparency
- No hallucination - never generates content outside sources

### 3. Enhanced Observability ✅

**Timing Breakdown:**
- `retrieval_ms`: Time spent searching indexes
- `generation_ms`: Time spent composing answer
- `total_ms`: End-to-end request time

**Debug Info:**
- Top BM25 hits with scores
- Top TF-IDF hits with scores
- Fused results with scores
- Placeholder for future reranker scores

**Metrics:**
- Rolling window of latencies (last 500 requests)
- P50 and P95 latencies calculated
- Available via `/health` endpoint

### 4. Better Answer Composition ✅

- Extractive approach (no generation model needed)
- Clear source attribution with title and URL
- Proper sentence-boundary snippet extraction
- Structured format for readability

### 5. Supporting Files ✅

**`app/prompts.py`:**
- Hardened system prompts for future LLM integration
- Context building utilities
- Refusal reason generators

**`demo.py`:**
- Complete end-to-end demo script
- Shows answerable and unanswerable questions
- Pretty-printed output

**`test_api_flow.py`:**
- Automated test suite
- Tests all endpoints
- Verifies refusal mechanism

**Enhanced Makefile:**
- `make health` - Check system health
- `make crawl` - Crawl example site
- `make index` - Build indexes
- `make ask` - Ask answerable question
- `make ask-refuse` - Test refusal mechanism
- `make demo` - Run complete demo
- `make test` - Run test suite
- `make clean` - Clean data files

### 6. Enhanced README ✅

Added comprehensive sections:
- **API Reference** with request/response examples
- **Design Decisions** explaining all choices
- **Retrieval Strategy** rationale
- **Chunking Strategy** explanation
- **Refusal Mechanism** details
- **Observability** features

## Key Design Decisions

1. **Hybrid Search (BM25 + TF-IDF)**
   - BM25 catches exact keywords
   - TF-IDF catches semantic similarity
   - Reciprocal rank fusion combines both

2. **Chunking (800 chars, 15% overlap)**
   - Balances context preservation with granularity
   - Paragraph-aware to maintain semantic coherence
   - Overlap prevents context loss at boundaries

3. **Score Threshold (0.01)**
   - Empirically chosen for demo data
   - Should be tuned per dataset
   - Prevents low-quality matches from appearing as answers

4. **Extractive Answers**
   - No LLM generation = no hallucinations
   - Every statement traceable to source
   - Can add LLM layer later without changing API

## How to Use

```bash
# Terminal 1: Start server
make run

# Terminal 2: Run demo
make demo

# Or manually:
make health
make crawl
make index
make ask
make ask-refuse
```

## What's Next (Phase 5-6)

Based on the plan, next steps are:

1. **Phase 5: Tiny Evals**
   - Create `evals/build_eval.py` to auto-generate questions
   - Create `evals/run_eval.py` to measure recall@k
   - Generate `eval_report.json`

2. **Phase 6: README Polish**
   - Add architecture diagram
   - Add limitations section
   - Add extensions/future work
   - Add attribution

3. **Phase 7: Tests**
   - Expand `tests/test_basic.py`
   - Add unit tests for each component

4. **Phase 8: Optional Power-ups**
   - Add cross-encoder reranker
   - Add sitemap fast-path
   - Add Dockerfile

## Files Modified/Created

### Modified:
- `app/api.py` - Enhanced /ask endpoint with timings and refusals
- `app/schemas.py` - Added closest field to AskResponse
- `retrieve/hybrid.py` - Return debug info, better snippet extraction
- `Makefile` - Added new targets
- `README.md` - Comprehensive API docs and design decisions

### Created:
- `app/prompts.py` - Hardened prompts for future LLM use
- `demo.py` - Complete demo script
- `test_api_flow.py` - Automated test suite
- `API_BUILD_SUMMARY.md` - This file

## Verification

To verify everything works:

```bash
# 1. Install dependencies
make install

# 2. Start server (terminal 1)
make run

# 3. Run demo (terminal 2)
make demo
```

Expected output:
- ✅ Health check passes
- ✅ Crawls 5 pages from example.com
- ✅ Creates ~10-20 chunks
- ✅ Answers question with sources
- ✅ Refuses unanswerable question gracefully
- ✅ Shows timing metrics

## Quality Checklist

- [x] API matches spec exactly
- [x] Refusal mechanism works
- [x] Timings tracked per request
- [x] Debug info exposed
- [x] No hallucinations (extractive only)
- [x] Sources always attributed
- [x] README is comprehensive
- [x] Demo script works end-to-end
- [x] Makefile has helpful commands
- [ ] Evals built (Phase 5)
- [ ] Tests expanded (Phase 7)
