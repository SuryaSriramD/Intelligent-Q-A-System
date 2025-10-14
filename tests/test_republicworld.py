"""
Test the real-time RAG API with Republic World news site.
Demonstrates crawling, indexing, and answering questions about real content.
"""
import httpx
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def test_crawl_and_index():
    """Step 1: Crawl and auto-index Republic World"""
    print_section("STEP 1: Crawling Republic World (auto-indexes)")
    
    print("\n📰 Crawling https://www.republicworld.com/")
    print("   This will take a moment (respecting crawl delay)...")
    
    start_time = time.time()
    
    try:
        resp = httpx.post(
            f"{BASE_URL}/crawl",
            json={
                "start_url": "https://www.republicworld.com/",
                "max_pages": 20,  # Reasonable number for testing
                "max_depth": 2,
                "crawl_delay_ms": 500  # Be polite to the server
            },
            timeout=120  # Give it time to crawl
        )
        
        elapsed = time.time() - start_time
        
        if resp.status_code != 200:
            print(f"\n❌ Crawl failed: {resp.status_code}")
            print(f"Response: {resp.text}")
            return False
        
        data = resp.json()
        
        print(f"\n✓ Crawl completed in {elapsed:.1f}s")
        print(f"✓ Pages crawled: {data['page_count']}")
        print(f"✓ Pages skipped: {data['skipped_count']}")
        print(f"✓ Auto-indexed: {data.get('indexed', False)}")
        print(f"✓ Chunks created: {data.get('vector_count', 0)}")
        
        if data['skipped_count'] > 0:
            print(f"\nSkip reasons:")
            for reason, count in data.get('skipped_reasons', {}).items():
                if count > 0:
                    print(f"  - {reason}: {count}")
        
        print(f"\nCrawled URLs (first 5):")
        for url in data.get('urls', [])[:5]:
            print(f"  • {url}")
        
        if data.get('vector_count', 0) > 0:
            print(f"\n✅ Ready for questions! ({data['vector_count']} chunks indexed)")
            return True
        else:
            print("\n❌ No chunks indexed - cannot answer questions")
            return False
            
    except httpx.TimeoutException:
        print("\n❌ Request timed out - try reducing max_pages")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def ask_question(question, show_sources=True):
    """Ask a question and display the answer"""
    print(f"\n❓ Question: {question}")
    
    try:
        resp = httpx.post(
            f"{BASE_URL}/ask",
            json={
                "question": question,
                "top_k": 6
            },
            timeout=30
        )
        
        if resp.status_code != 200:
            print(f"❌ Request failed: {resp.status_code}")
            return False
        
        data = resp.json()
        answer = data.get('answer', '')
        sources = data.get('sources', [])
        timings = data.get('timings', {})
        
        print(f"\n💬 Answer:")
        print(f"   {answer[:500]}{'...' if len(answer) > 500 else ''}")
        
        if sources:
            print(f"\n📚 Sources: {len(sources)} chunks found")
            if show_sources:
                for i, src in enumerate(sources[:3], 1):  # Show first 3
                    print(f"\n   [{i}] {src['title']}")
                    print(f"       URL: {src['url']}")
                    print(f"       Snippet: {src['snippet'][:150]}...")
        else:
            print(f"\n⚠️  No sources found (refusal)")
            closest = data.get('closest', [])
            if closest:
                print(f"\n   Closest match:")
                print(f"   • {closest[0].get('snippet', '')[:200]}")
        
        print(f"\n⏱️  Timing: {timings.get('total_ms', 0):.2f}ms")
        return len(sources) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_multiple_questions():
    """Step 2: Ask multiple questions about the content"""
    print_section("STEP 2: Asking Questions About Republic World")
    
    questions = [
        "What is Republic World?",
        "What are the latest news topics covered?",
        "What entertainment news is available?",
        "What sports news is covered?",
        "What is the company's annual revenue?",  # Should refuse - not in content
    ]
    
    results = []
    for question in questions:
        answered = ask_question(question, show_sources=True)
        results.append((question, answered))
        time.sleep(0.5)  # Brief pause between questions
    
    return results


def test_one_shot():
    """Step 3: Test the one-shot endpoint"""
    print_section("BONUS: One-Shot Endpoint (Crawl + Ask in one call)")
    
    print("\n🚀 Testing /crawl-and-ask with a focused question...")
    print("   Crawling + asking: 'What is Republic World about?'")
    
    try:
        resp = httpx.post(
            f"{BASE_URL}/crawl-and-ask",
            json={
                "start_url": "https://www.republicworld.com/",
                "question": "What is Republic World about?",
                "max_pages": 10,
                "top_k": 6
            },
            timeout=120
        )
        
        if resp.status_code != 200:
            print(f"❌ Request failed: {resp.status_code}")
            return False
        
        data = resp.json()
        
        print(f"\n✓ Crawl: {data['crawl']['page_count']} pages")
        print(f"✓ Indexed: {data['crawl'].get('vector_count', 0)} chunks")
        print(f"\n💬 Answer: {data['answer']['answer'][:300]}...")
        print(f"📚 Sources: {len(data['answer']['sources'])} chunks")
        print(f"⏱️  Total time: {data['answer']['timings']['total_ms']:.2f}ms")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("\n" + "="*80)
    print("  🌐 REAL-TIME RAG API TEST - REPUBLIC WORLD")
    print("="*80)
    
    # Check server health
    try:
        health = httpx.get(f"{BASE_URL}/health", timeout=5)
        if health.status_code != 200:
            print("\n❌ Server not running!")
            print("Start with: uvicorn app.api:app --port 8000\n")
            return
        print("\n✓ Server is running")
    except:
        print("\n❌ Cannot connect to server!")
        print("Start with: uvicorn app.api:app --port 8000\n")
        return
    
    # Step 1: Crawl and index
    if not test_crawl_and_index():
        print("\n❌ Crawl failed - cannot proceed with questions")
        return
    
    # Step 2: Ask multiple questions
    results = test_multiple_questions()
    
    # Summary
    print_section("SUMMARY")
    answered = sum(1 for _, ans in results if ans)
    refused = len(results) - answered
    
    print(f"\nQuestions answered: {answered}/{len(results)}")
    print(f"Questions refused: {refused}/{len(results)}")
    
    print("\nResults:")
    for question, answered in results:
        status = "✓ Answered" if answered else "✗ Refused"
        print(f"  {status}: {question[:60]}...")
    
    # Bonus: Test one-shot endpoint
    # Uncomment if you want to test it (will crawl again)
    # test_one_shot()
    
    print("\n" + "="*80)
    print("  ✓ Real-time RAG test completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
