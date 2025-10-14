"""
Real-time RAG example: Ask questions about any URL instantly!
"""
import httpx
import json

BASE_URL = "http://localhost:8000"

def example_separate_calls():
    """Example 1: Traditional workflow (crawl → ask)"""
    print("\n" + "="*70)
    print("  Example 1: Separate Calls (Crawl → Ask)")
    print("="*70)
    
    # Step 1: Crawl (now auto-indexes!)
    print("\n1. Crawling https://example.com...")
    crawl_resp = httpx.post(
        f"{BASE_URL}/crawl",
        json={
            "start_url": "https://example.com",
            "max_pages": 10,
            "max_depth": 2
        },
        timeout=60
    )
    crawl_data = crawl_resp.json()
    print(f"   ✓ Crawled {crawl_data['page_count']} pages")
    print(f"   ✓ Indexed {crawl_data.get('vector_count', 0)} chunks")
    
    # Step 2: Ask question
    print("\n2. Asking: 'What is this domain about?'")
    ask_resp = httpx.post(
        f"{BASE_URL}/ask",
        json={
            "question": "What is this domain about?",
            "top_k": 6
        },
        timeout=30
    )
    ask_data = ask_resp.json()
    print(f"\n   Answer: {ask_data['answer']}")
    print(f"   Sources: {len(ask_data['sources'])} chunks")
    print(f"   Timing: {ask_data['timings']['total_ms']:.2f}ms")


def example_one_shot():
    """Example 2: One-shot endpoint (crawl + ask in one request)"""
    print("\n" + "="*70)
    print("  Example 2: One-Shot Call (Instant Answer!)")
    print("="*70)
    
    print("\nCrawling + Asking in a single request...")
    print("URL: https://example.com")
    print("Question: What is this website for?")
    
    resp = httpx.post(
        f"{BASE_URL}/crawl-and-ask",
        json={
            "start_url": "https://example.com",
            "question": "What is this website for?",
            "max_pages": 10,
            "top_k": 6
        },
        timeout=90
    )
    
    data = resp.json()
    
    # Show crawl results
    print(f"\n✓ Crawled: {data['crawl']['page_count']} pages")
    print(f"✓ Indexed: {data['crawl'].get('vector_count', 0)} chunks")
    
    # Show answer
    print(f"\n✓ Answer: {data['answer']['answer']}")
    print(f"✓ Sources: {len(data['answer']['sources'])} chunks")
    print(f"✓ Total time: {data['answer']['timings']['total_ms']:.2f}ms")


def example_different_url():
    """Example 3: Try a different URL to show real-time capability"""
    print("\n" + "="*70)
    print("  Example 3: Different URL - Real-Time Context Switch")
    print("="*70)
    
    # This demonstrates that each crawl replaces the previous context
    print("\nNow asking about a DIFFERENT website...")
    print("This shows each crawl creates fresh context")
    
    resp = httpx.post(
        f"{BASE_URL}/crawl-and-ask",
        json={
            "start_url": "https://www.iana.org/domains/reserved",
            "question": "What domains are reserved?",
            "max_pages": 5,
            "top_k": 6
        },
        timeout=90
    )
    
    data = resp.json()
    print(f"\n✓ Crawled: {data['crawl']['page_count']} pages from iana.org")
    print(f"✓ Answer: {data['answer']['answer'][:200]}...")


if __name__ == "__main__":
    print("\n🚀 Real-Time RAG API Demo")
    print("="*70)
    
    try:
        # Check health
        health = httpx.get(f"{BASE_URL}/health", timeout=5)
        if health.status_code != 200:
            print("❌ Server not running! Start with: uvicorn app.api:app --port 8000")
            exit(1)
        
        print("✓ Server is running")
        
        # Run examples
        example_separate_calls()
        example_one_shot()
        
        # Uncomment to try different URL (takes longer due to crawling)
        # example_different_url()
        
        print("\n" + "="*70)
        print("✓ All examples completed successfully!")
        print("="*70 + "\n")
        
    except httpx.ConnectError:
        print("\n❌ Cannot connect to server!")
        print("Start server: uvicorn app.api:app --port 8000\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
