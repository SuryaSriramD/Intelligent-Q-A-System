"""
Run evaluation on the RAG system.
Measures recall@k and answer quality.
"""
import json
import os
import httpx
import time
from typing import Dict, Any, List

EVAL_QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "eval_questions.json")
EVAL_REPORT_PATH = os.path.join(os.path.dirname(__file__), "eval_report.json")
BASE_URL = "http://localhost:8000"


def load_eval_questions() -> List[Dict[str, Any]]:
    """Load evaluation questions."""
    try:
        with open(EVAL_QUESTIONS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("questions", [])
    except FileNotFoundError:
        print("❌ Eval questions not found. Run: python evals/build_eval.py")
        return []


def check_retrieval_recall(question: Dict, response: Dict, k: int = 6) -> Dict[str, Any]:
    """Check if relevant chunks were retrieved."""
    sources = response.get("sources", [])
    expected_url = question.get("expected_url", "")
    expected_keywords = question.get("expected_keywords", [])
    
    # Check if expected URL is in sources
    url_found = any(expected_url in src.get("url", "") for src in sources)
    
    # Check if keywords appear in retrieved snippets
    snippets_text = " ".join([src.get("snippet", "").lower() for src in sources])
    keywords_found = sum(1 for kw in expected_keywords if kw in snippets_text)
    keyword_recall = keywords_found / len(expected_keywords) if expected_keywords else 0
    
    return {
        "url_found": url_found,
        "keyword_recall": keyword_recall,
        "num_sources": len(sources),
        "retrieved": len(sources) > 0
    }


def check_answer_quality(question: Dict, response: Dict) -> Dict[str, Any]:
    """Check if the answer is appropriate."""
    answer = response.get("answer", "")
    q_type = question.get("type", "")
    
    if q_type == "unanswerable":
        # Should refuse
        refused = "not found in crawled content" in answer.lower()
        has_closest = len(response.get("closest", [])) > 0
        return {
            "correct_refusal": refused,
            "provided_closest": has_closest,
            "answer_length": len(answer)
        }
    else:
        # Should answer
        has_answer = len(answer) > 50 and "not found" not in answer.lower()
        has_sources = len(response.get("sources", [])) > 0
        expected_keywords = question.get("expected_keywords", [])
        keywords_in_answer = sum(1 for kw in expected_keywords if kw in answer.lower())
        
        return {
            "has_answer": has_answer,
            "has_sources": has_sources,
            "keywords_in_answer": keywords_in_answer,
            "answer_length": len(answer)
        }


def run_single_eval(question: Dict, top_k: int = 6) -> Dict[str, Any]:
    """Run evaluation for a single question."""
    try:
        resp = httpx.post(
            f"{BASE_URL}/ask",
            json={"question": question["question"], "top_k": top_k},
            timeout=30
        )
        
        if resp.status_code != 200:
            return {
                "error": f"HTTP {resp.status_code}",
                "question": question
            }
        
        response = resp.json()
        
        # Evaluate retrieval
        retrieval_metrics = check_retrieval_recall(question, response, top_k)
        
        # Evaluate answer quality
        quality_metrics = check_answer_quality(question, response)
        
        return {
            "question": question["question"],
            "type": question["type"],
            "difficulty": question.get("difficulty", "unknown"),
            "retrieval": retrieval_metrics,
            "quality": quality_metrics,
            "timings": response.get("timings", {}),
            "response": {
                "answer_preview": response.get("answer", "")[:200],
                "num_sources": len(response.get("sources", [])),
                "num_closest": len(response.get("closest", []))
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "question": question
        }


def compute_aggregate_metrics(results: List[Dict]) -> Dict[str, Any]:
    """Compute aggregate metrics across all results."""
    answerable = [r for r in results if r.get("type") == "answerable" and "error" not in r]
    unanswerable = [r for r in results if r.get("type") == "unanswerable" and "error" not in r]
    
    metrics = {
        "total_questions": len(results),
        "successful": len([r for r in results if "error" not in r]),
        "errors": len([r for r in results if "error" in r]),
    }
    
    # Answerable questions metrics
    if answerable:
        metrics["answerable"] = {
            "count": len(answerable),
            "avg_keyword_recall": sum(r["retrieval"]["keyword_recall"] for r in answerable) / len(answerable),
            "url_found_rate": sum(1 for r in answerable if r["retrieval"]["url_found"]) / len(answerable),
            "has_answer_rate": sum(1 for r in answerable if r["quality"]["has_answer"]) / len(answerable),
            "has_sources_rate": sum(1 for r in answerable if r["quality"]["has_sources"]) / len(answerable),
            "avg_sources": sum(r["retrieval"]["num_sources"] for r in answerable) / len(answerable),
        }
    
    # Unanswerable questions metrics
    if unanswerable:
        metrics["unanswerable"] = {
            "count": len(unanswerable),
            "correct_refusal_rate": sum(1 for r in unanswerable if r["quality"]["correct_refusal"]) / len(unanswerable),
            "provided_closest_rate": sum(1 for r in unanswerable if r["quality"]["provided_closest"]) / len(unanswerable),
        }
    
    # Timing metrics
    all_timings = [r["timings"] for r in results if "timings" in r and r["timings"]]
    if all_timings:
        metrics["performance"] = {
            "avg_retrieval_ms": sum(t.get("retrieval_ms", 0) for t in all_timings) / len(all_timings),
            "avg_total_ms": sum(t.get("total_ms", 0) for t in all_timings) / len(all_timings),
        }
    
    return metrics


def run_evaluation(top_k: int = 6) -> Dict[str, Any]:
    """Run full evaluation."""
    print("\n=== Running Evaluation ===\n")
    
    # Check if server is running
    try:
        httpx.get(f"{BASE_URL}/health", timeout=5)
    except Exception:
        print("❌ Server not running. Start it first:")
        print("   uvicorn app.api:app --port 8000")
        return {}
    
    questions = load_eval_questions()
    if not questions:
        return {}
    
    print(f"Loaded {len(questions)} questions\n")
    
    # Run evaluations
    results = []
    for i, question in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] {question['type']}: {question['question'][:60]}...")
        result = run_single_eval(question, top_k)
        results.append(result)
        time.sleep(0.1)  # Be nice to the server
    
    # Compute metrics
    metrics = compute_aggregate_metrics(results)
    
    # Build report
    report = {
        "config": {
            "top_k": top_k,
            "base_url": BASE_URL,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "metrics": metrics,
        "results": results
    }
    
    # Save report
    with open(EVAL_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Evaluation complete!")
    print(f"Saved to: {EVAL_REPORT_PATH}\n")
    
    return report


def print_summary(report: Dict):
    """Print evaluation summary."""
    metrics = report.get("metrics", {})
    
    print("=== Evaluation Summary ===\n")
    print(f"Total questions: {metrics.get('total_questions', 0)}")
    print(f"Successful: {metrics.get('successful', 0)}")
    print(f"Errors: {metrics.get('errors', 0)}\n")
    
    if "answerable" in metrics:
        ans = metrics["answerable"]
        print("Answerable Questions:")
        print(f"  • Count: {ans['count']}")
        print(f"  • Keyword Recall: {ans['avg_keyword_recall']:.2%}")
        print(f"  • URL Found Rate: {ans['url_found_rate']:.2%}")
        print(f"  • Has Answer Rate: {ans['has_answer_rate']:.2%}")
        print(f"  • Has Sources Rate: {ans['has_sources_rate']:.2%}")
        print(f"  • Avg Sources: {ans['avg_sources']:.1f}\n")
    
    if "unanswerable" in metrics:
        unans = metrics["unanswerable"]
        print("Unanswerable Questions (Refusals):")
        print(f"  • Count: {unans['count']}")
        print(f"  • Correct Refusal Rate: {unans['correct_refusal_rate']:.2%}")
        print(f"  • Provided Closest Matches: {unans['provided_closest_rate']:.2%}\n")
    
    if "performance" in metrics:
        perf = metrics["performance"]
        print("Performance:")
        print(f"  • Avg Retrieval: {perf['avg_retrieval_ms']:.1f}ms")
        print(f"  • Avg Total: {perf['avg_total_ms']:.1f}ms")


if __name__ == "__main__":
    report = run_evaluation(top_k=6)
    if report:
        print_summary(report)
        
        print("\n=== Next Steps ===")
        print("1. Review eval_report.json for detailed results")
        print("2. Check which questions failed and why")
        print("3. Tune retrieval parameters if needed")
        print("4. Proceed to Phase 6: Polish README")
