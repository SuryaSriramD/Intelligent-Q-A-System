"""
Quick test script to verify the API flow end-to-end
"""
import httpx
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n=== Testing /health ===")
    resp = httpx.get(f"{BASE_URL}/health")
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")
    assert resp.status_code == 200

def test_crawl():
    print("\n=== Testing /crawl ===")
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
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Pages crawled: {data['page_count']}")
    print(f"Skipped: {data['skipped_count']}")
    print(f"Skipped reasons: {json.dumps(data['skipped_reasons'], indent=2)}")
    print(f"URLs: {data['urls'][:3]}...")
    assert resp.status_code == 200
    assert data['page_count'] > 0

def test_index():
    print("\n=== Testing /index ===")
    resp = httpx.post(
        f"{BASE_URL}/index",
        json={
            "chunk_size": 800,
            "chunk_overlap": 120
        },
        timeout=30
    )
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Vector count: {data['vector_count']}")
    print(f"Errors: {data['errors']}")
    assert resp.status_code == 200
    assert data['vector_count'] > 0

def test_ask_answerable():
    print("\n=== Testing /ask (answerable question) ===")
    resp = httpx.post(
        f"{BASE_URL}/ask",
        json={
            "question": "What is this website about?",
            "top_k": 6
        },
        timeout=30
    )
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Answer: {data['answer'][:200]}...")
    print(f"Sources: {len(data['sources'])}")
    print(f"Timings: {json.dumps(data['timings'], indent=2)}")
    print(f"Debug info: {json.dumps(data['retrieval_debug'], indent=2)}")
    assert resp.status_code == 200

def test_ask_unanswerable():
    print("\n=== Testing /ask (unanswerable question) ===")
    resp = httpx.post(
        f"{BASE_URL}/ask",
        json={
            "question": "What is the company's annual revenue in 2025?",
            "top_k": 6
        },
        timeout=30
    )
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Answer: {data['answer']}")
    print(f"Sources: {len(data['sources'])}")
    print(f"Closest matches: {len(data.get('closest', []))}")
    if data.get('closest'):
        print(f"Closest: {data['closest'][0]['snippet'][:100]}...")
    print(f"Timings: {json.dumps(data['timings'], indent=2)}")
    assert resp.status_code == 200

if __name__ == "__main__":
    try:
        print("Starting API tests...")
        print("Make sure the server is running: uvicorn app.api:app --port 8000")
        time.sleep(1)
        
        test_health()
        test_crawl()
        test_index()
        test_ask_answerable()
        test_ask_unanswerable()
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
