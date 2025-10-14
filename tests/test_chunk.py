from index.chunk import build_chunks

print("Testing chunking...")
chunks, errors = build_chunks(800, 120)
print(f"Chunks created: {len(chunks)}")
print(f"Errors: {errors}")

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i}:")
    print(f"  URL: {chunk['url']}")
    print(f"  Title: {chunk['title']}")
    print(f"  Text length: {len(chunk['text'])} chars")
    print(f"  Text: {chunk['text'][:100]}...")
