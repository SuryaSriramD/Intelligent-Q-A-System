"""
Interactive Q&A with the currently indexed content.
Ask any question about the crawled website!
"""
import httpx
import json

BASE_URL = "http://localhost:8000"

def ask(question):
    """Ask a question and display the answer"""
    try:
        resp = httpx.post(
            f"{BASE_URL}/ask",
            json={"question": question, "top_k": 6},
            timeout=30
        )
        
        if resp.status_code != 200:
            print(f"❌ Error: {resp.status_code}")
            return
        
        data = resp.json()
        answer = data.get('answer', '')
        sources = data.get('sources', [])
        
        print(f"\n💬 Answer:")
        print(f"{answer}\n")
        
        if sources:
            print(f"📚 Sources ({len(sources)} chunks):")
            for i, src in enumerate(sources[:3], 1):
                print(f"\n[{i}] {src['title']}")
                print(f"    {src['url']}")
                print(f"    {src['snippet'][:150]}...")
        else:
            print("⚠️  No sources found (refusal)")
            closest = data.get('closest', [])
            if closest:
                print(f"\nClosest match:")
                print(f"  {closest[0].get('snippet', '')[:200]}")
        
        print(f"\n⏱️  Timing: {data['timings']['total_ms']:.2f}ms")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print("\n" + "="*70)
    print("  🤖 Interactive RAG Q&A")
    print("="*70)
    print("\nCurrently indexed: Republic World content")
    print("Type your question or 'quit' to exit\n")
    
    # Check if server is running
    try:
        httpx.get(f"{BASE_URL}/health", timeout=5)
    except:
        print("❌ Server not running! Start with: uvicorn app.api:app --port 8000\n")
        return
    
    while True:
        try:
            question = input("\n❓ Your question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            ask(question)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except EOFError:
            print("\n\n👋 Goodbye!\n")
            break


if __name__ == "__main__":
    main()
