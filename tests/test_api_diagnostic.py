"""Quick diagnostic to verify the real-time API is working correctly."""
import httpx
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n1. Testing /health endpoint...")
    try:
        resp = httpx.get(f"{BASE_URL}/health", timeout=5)
        if resp.status_code == 200:
            print("   ✓ Server is running")
            return True
        else:
            print(f"   ✗ Health check failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Cannot connect: {e}")
        return False


def test_crawl_with_auto_index():
    print("\n2. Testing /crawl (should auto-index)...")
    try:
        resp = httpx.post(
            f"{BASE_URL}/crawl",
            json={"start_url": "https://example.com", "max_pages": 1},
            timeout=60
        )
        data = resp.json()
        
        # Check required fields
        print(f"   Page count: {data.get('page_count')}")
        print(f"   Indexed: {data.get('indexed', 'MISSING!')}")
        print(f"   Vector count: {data.get('vector_count', 'MISSING!')}")
        
        if 'indexed' in data and 'vector_count' in data:
            if data['indexed'] and data['vector_count'] > 0:
                print("   ✓ Auto-indexing works!")
                return True
            else:
                print("   ✗ Auto-indexing failed (no chunks created)")
                return False
        else:
            print("   ✗ Response missing 'indexed' and 'vector_count' fields")
            print("   → Server needs restart to load updated code!")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_ask():
    print("\n3. Testing /ask endpoint...")
    try:
        resp = httpx.post(
            f"{BASE_URL}/ask",
            json={"question": "What is this domain about?", "top_k": 6},
            timeout=30
        )
        data = resp.json()
        
        answer = data.get('answer', '')
        sources = data.get('sources', [])
        
        print(f"   Answer length: {len(answer)} chars")
        print(f"   Sources: {len(sources)} chunks")
        
        if len(sources) > 0:
            print("   ✓ Found relevant sources!")
            return True
        else:
            print("   ✗ No sources found (might be a refusal)")
            print(f"   Answer: {answer[:100]}...")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_crawl_and_ask():
    print("\n4. Testing /crawl-and-ask endpoint...")
    try:
        resp = httpx.post(
            f"{BASE_URL}/crawl-and-ask",
            json={
                "start_url": "https://example.com",
                "question": "What is this website for?",
                "max_pages": 1
            },
            timeout=90
        )
        
        if resp.status_code == 404:
            print("   ✗ Endpoint not found - server needs restart!")
            return False
            
        data = resp.json()
        
        if 'crawl' in data and 'answer' in data:
            print(f"   Crawl: {data['crawl'].get('page_count')} pages")
            print(f"   Answer: {data['answer'].get('answer', '')[:80]}...")
            print("   ✓ One-shot endpoint works!")
            return True
        else:
            print("   ✗ Unexpected response structure")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


if __name__ == "__main__":
    print("="*70)
    print("  REAL-TIME API DIAGNOSTIC")
    print("="*70)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Auto-Index", test_crawl_with_auto_index()))
    results.append(("Ask Questions", test_ask()))
    results.append(("One-Shot", test_crawl_and_ask()))
    
    print("\n" + "="*70)
    print("  SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name:20s} {status}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n✓ All tests passed! Real-time API is working correctly.\n")
    else:
        print("\n✗ Some tests failed. Please restart the server and try again.\n")
        print("Restart command: uvicorn app.api:app --port 8000\n")
