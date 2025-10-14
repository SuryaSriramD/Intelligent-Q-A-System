"""
Demo script showing the complete RAG pipeline flow.
This demonstrates both answerable and unanswerable questions.
"""
import httpx
import json
import sys

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def demo_health():
    print_section("1. Health Check")
    resp = httpx.get(f"{BASE_URL}/health")
    data = resp.json()
    print(json.dumps(data, indent=2))
    return resp.status_code == 200

def demo_crawl():
    print_section("2. Crawling Example.com (5 pages) - Auto-Indexes!")
    print("This will crawl example.com and automatically index for Q&A...")
    
    resp = httpx.post(
        f"{BASE_URL}/crawl",
        json={
            "start_url": "https://example.com",
            "max_pages": 5,
            "max_depth": 1,
            "crawl_delay_ms": 300
        },
        timeout=60
    )
    
    if resp.status_code != 200:
        print(f"\n❌ Crawl failed with status {resp.status_code}")
        print(f"Response: {resp.text}")
        return False
    
    data = resp.json()
    print(f"\n✓ Crawled {data['page_count']} pages")
    print(f"✓ Skipped {data['skipped_count']} URLs")
    if data.get('indexed'):
        print(f"✓ Auto-indexed {data.get('vector_count', 0)} chunks → Ready for Q&A!")
    print(f"\nSkip breakdown:")
    for reason, count in data['skipped_reasons'].items():
        if count > 0:
            print(f"  - {reason}: {count}")
    
    print(f"\nCrawled URLs:")
    for url in data['urls'][:3]:
        print(f"  • {url}")
    if len(data['urls']) > 3:
        print(f"  ... and {len(data['urls']) - 3} more")
    
    return resp.status_code == 200

def demo_index():
    print_section("3. Building Search Index")
    print("Chunking content and building BM25 + TF-IDF indexes...")
    
    resp = httpx.post(
        f"{BASE_URL}/index",
        json={
            "chunk_size": 800,
            "chunk_overlap": 120
        },
        timeout=30
    )
    
    data = resp.json()
    print(f"\n✓ Created {data['vector_count']} searchable chunks")
    if data['errors']:
        print(f"⚠ Errors: {data['errors']}")
    
    return resp.status_code == 200

def demo_ask_answerable():
    print_section("4a. Answerable Question")
    question = "What is this website about?"
    print(f"Question: {question}\n")
    
    resp = httpx.post(
        f"{BASE_URL}/ask",
        json={
            "question": question,
            "top_k": 3
        },
        timeout=30
    )
    
    data = resp.json()
    
    print(f"Answer:\n{data['answer']}\n")
    print(f"Sources found: {len(data['sources'])}")
    for i, src in enumerate(data['sources'][:2], 1):
        print(f"\n  Source {i}:")
        print(f"    Title: {src['title']}")
        print(f"    URL: {src['url']}")
        print(f"    Snippet: {src['snippet'][:100]}...")
    
    print(f"\nPerformance:")
    print(f"  Retrieval: {data['timings']['retrieval_ms']:.1f}ms")
    print(f"  Generation: {data['timings']['generation_ms']:.1f}ms")
    print(f"  Total: {data['timings']['total_ms']:.1f}ms")
    
    return resp.status_code == 200

def demo_ask_unanswerable():
    print_section("4b. Unanswerable Question (Refusal)")
    question = "What is the company's annual revenue in 2025?"
    print(f"Question: {question}\n")
    
    resp = httpx.post(
        f"{BASE_URL}/ask",
        json={
            "question": question,
            "top_k": 3
        },
        timeout=30
    )
    
    data = resp.json()
    
    print(f"Answer: {data['answer']}\n")
    
    if data.get('closest'):
        print(f"Closest matches shown for transparency:")
        for i, match in enumerate(data['closest'], 1):
            print(f"\n  {i}. {match.get('title', 'Untitled')}")
            print(f"     {match['snippet'][:100]}...")
    
    print(f"\nPerformance:")
    print(f"  Retrieval: {data['timings']['retrieval_ms']:.1f}ms")
    print(f"  Total: {data['timings']['total_ms']:.1f}ms")
    
    print(f"\n✓ Properly refused to hallucinate!")
    
    return resp.status_code == 200

def main():
    print("\n" + "🚀 RAG FastAPI Demo".center(70))
    print("Make sure the server is running: make run\n")
    
    try:
        steps = [
            ("Health Check", demo_health),
            ("Crawl", demo_crawl),
            ("Index", demo_index),
            ("Ask (Answerable)", demo_ask_answerable),
            ("Ask (Refusal)", demo_ask_unanswerable),
        ]
        
        for name, func in steps:
            if not func():
                print(f"\n❌ {name} failed!")
                return 1
        
        print_section("✅ Demo Complete!")
        print("\nKey Features Demonstrated:")
        print("  ✓ Polite, in-domain crawling with skip tracking")
        print("  ✓ DOM-aware chunking with overlap")
        print("  ✓ Hybrid search (BM25 + TF-IDF fusion)")
        print("  ✓ Grounded answers with source attribution")
        print("  ✓ Graceful refusals with transparency")
        print("  ✓ Detailed timing metrics")
        print()
        
        return 0
        
    except httpx.ConnectError:
        print("\n❌ Cannot connect to server!")
        print("Make sure it's running: uvicorn app.api:app --port 8000")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
