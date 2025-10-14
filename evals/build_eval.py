"""
Auto-generate evaluation questions from crawled content.
Creates a small eval set with answerable and unanswerable questions.
"""
import json
import os
import re
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PAGES_PATH = os.path.join(DATA_DIR, "pages.jsonl")
EVAL_PATH = os.path.join(os.path.dirname(__file__), "eval_questions.json")


def extract_heading_questions(pages: List[Dict]) -> List[Dict[str, Any]]:
    """Generate questions from headings and first sentences."""
    questions = []
    
    for page in pages[:10]:  # Limit to first 10 pages
        text = page.get("text", "")
        url = page.get("url", "")
        title = page.get("title", "")
        
        # Extract potential facts from first few sentences
        sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 20][:5]
        
        # Generate "What is X" questions from sentences containing "is"
        for sent in sentences:
            if " is " in sent.lower() and len(sent) < 150:
                # Extract subject
                parts = sent.lower().split(" is ")
                if parts and len(parts[0].split()) <= 5:
                    subject = parts[0].strip()
                    question = f"What is {subject}?"
                    questions.append({
                        "question": question,
                        "type": "answerable",
                        "expected_url": url,
                        "expected_keywords": [subject.lower()],
                        "difficulty": "easy"
                    })
        
        # Generate questions from title
        if title and len(title.split()) <= 8:
            questions.append({
                "question": f"What information is available about '{title}'?",
                "type": "answerable",
                "expected_url": url,
                "expected_keywords": [title.lower()],
                "difficulty": "medium"
            })
    
    return questions[:12]  # Return up to 12 answerable questions


def generate_trap_questions() -> List[Dict[str, Any]]:
    """Generate questions that should NOT be answerable from crawled content."""
    trap_questions = [
        {
            "question": "What is the company's annual revenue in 2025?",
            "type": "unanswerable",
            "reason": "Financial data not in content",
            "difficulty": "easy"
        },
        {
            "question": "Who is the CEO of this organization?",
            "type": "unanswerable",
            "reason": "Personnel information not in content",
            "difficulty": "easy"
        },
        {
            "question": "What are the office hours on weekends?",
            "type": "unanswerable",
            "reason": "Specific operational details not in content",
            "difficulty": "medium"
        },
        {
            "question": "How many employees work at the company?",
            "type": "unanswerable",
            "reason": "Employee count not in content",
            "difficulty": "easy"
        },
        {
            "question": "What is the stock price today?",
            "type": "unanswerable",
            "reason": "Real-time financial data not in content",
            "difficulty": "easy"
        }
    ]
    return trap_questions[:5]


def build_eval_set() -> Dict[str, Any]:
    """Build a complete evaluation set."""
    print("Building evaluation set...")
    
    # Load crawled pages
    pages = []
    try:
        with open(PAGES_PATH, "r", encoding="utf-8") as f:
            for line in f:
                pages.append(json.loads(line))
    except FileNotFoundError:
        print("❌ No pages found. Run /crawl first.")
        return {"questions": [], "stats": {}}
    
    print(f"Loaded {len(pages)} pages")
    
    # Generate questions
    answerable = extract_heading_questions(pages)
    unanswerable = generate_trap_questions()
    
    all_questions = answerable + unanswerable
    
    # Build eval set
    eval_set = {
        "questions": all_questions,
        "stats": {
            "total": len(all_questions),
            "answerable": len(answerable),
            "unanswerable": len(unanswerable),
            "pages_analyzed": len(pages)
        },
        "metadata": {
            "generator": "build_eval.py",
            "version": "1.0"
        }
    }
    
    # Save to file
    with open(EVAL_PATH, "w", encoding="utf-8") as f:
        json.dump(eval_set, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Generated {len(all_questions)} questions:")
    print(f"  - {len(answerable)} answerable")
    print(f"  - {len(unanswerable)} unanswerable (trap questions)")
    print(f"\nSaved to: {EVAL_PATH}")
    
    return eval_set


if __name__ == "__main__":
    print("\n=== Building Evaluation Set ===\n")
    eval_set = build_eval_set()
    
    print("\n=== Sample Questions ===")
    for i, q in enumerate(eval_set["questions"][:3], 1):
        print(f"\n{i}. [{q['type']}] {q['question']}")
        if q['type'] == 'answerable':
            print(f"   Expected keywords: {q.get('expected_keywords', [])}")
    
    print("\n=== Next Step ===")
    print("Run: python evals/run_eval.py")
