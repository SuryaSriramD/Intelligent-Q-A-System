.PHONY: run crawl index ask test health clean install demo eval-build eval-run eval

install:
	pip install -r requirements.txt

run:
	uvicorn app.api:app --reload --port 8000

health:
	curl -s localhost:8000/health | python -m json.tool

# Example one-liners (replace values as needed)
# Note: /crawl now auto-indexes, so you can go straight to /ask after crawling
crawl:
	curl -X POST localhost:8000/crawl -H "content-type: application/json" \
	  -d '{"start_url":"https://example.com","max_pages":20,"max_depth":2,"crawl_delay_ms":400}' | python -m json.tool

index:
	curl -X POST localhost:8000/index -H "content-type: application/json" \
	  -d '{"chunk_size":800,"chunk_overlap":120}' | python -m json.tool

ask:
	curl -X POST localhost:8000/ask -H "content-type: application/json" \
	  -d '{"question":"What services does Example offer?","top_k":6}' | python -m json.tool

ask-refuse:
	curl -X POST localhost:8000/ask -H "content-type: application/json" \
	  -d '{"question":"What is the company revenue in 2025?","top_k":6}' | python -m json.tool

# One-shot: crawl and ask in a single request (real-time mode)
crawl-and-ask:
	curl -X POST localhost:8000/crawl-and-ask -H "content-type: application/json" \
	  -d '{"start_url":"https://example.com","question":"What is this domain about?","max_pages":10,"top_k":6}' | python -m json.tool

test:
	python test_api_flow.py

demo:
	python demo.py

eval-build:
	python evals/build_eval.py

eval-run:
	python evals/run_eval.py

eval: eval-build eval-run

clean:
	rm -rf data/*.jsonl data/*.index __pycache__ */__pycache__ evals/*.json

