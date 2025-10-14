import httpx, time, urllib.parse, os, json
from bs4 import BeautifulSoup
import trafilatura

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PAGES_PATH = os.path.join(DATA_DIR, "pages.jsonl")

def same_domain(a, b):
    return urllib.parse.urlparse(a).netloc.split(':')[0].endswith(
        urllib.parse.urlparse(b).netloc.split(':')[0]
    )

def clean_url(u):
    parsed = urllib.parse.urlparse(u)
    # remove fragments and common tracking params
    query = urllib.parse.parse_qs(parsed.query)
    for k in list(query.keys()):
        if k.startswith("utm_") or k in {"gclid", "fbclid"}:
            query.pop(k, None)
    new_q = urllib.parse.urlencode({k:v[0] for k,v in query.items()})
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', new_q, ''))

def extract_main(html, url):
    downloaded = trafilatura.extract(html, include_comments=False, favor_recall=True, include_links=False, url=url)
    if downloaded: 
        return downloaded
    # fallback: basic text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n")

def run_crawl(start_url: str, max_pages: int = 40, max_depth: int = 2, crawl_delay_ms: int = 400):
    os.makedirs(DATA_DIR, exist_ok=True)
    seen = set()
    frontier = [(start_url, 0)]
    saved = 0
    skipped = {"off_domain":0, "duplicate":0, "non_http":0, "error":0}
    urls = []

    host = urllib.parse.urlparse(start_url).netloc

    with httpx.Client(follow_redirects=True, timeout=10) as client, open(PAGES_PATH, "w", encoding="utf-8") as f:
        while frontier and saved < max_pages:
            url, depth = frontier.pop(0)
            url = clean_url(url)
            if url in seen:
                skipped["duplicate"] += 1
                continue
            seen.add(url)
            if depth > max_depth:
                continue
            if urllib.parse.urlparse(url).scheme not in {"http", "https"}:
                skipped["non_http"] += 1
                continue
            if not same_domain(start_url, url):
                skipped["off_domain"] += 1
                continue
            try:
                resp = client.get(url, headers={"User-Agent": "rag-starter/0.1 (+https://example.com)"})
                if resp.status_code >= 400:
                    skipped["error"] += 1
                    continue
                html = resp.text
                text = extract_main(html, url)
                rec = {"url": url, "title": "", "text": text}
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html, "html.parser")
                    if soup.title and soup.title.string:
                        rec["title"] = soup.title.string.strip()
                    # enqueue links
                    for a in soup.find_all("a", href=True):
                        href = urllib.parse.urljoin(url, a["href"])
                        frontier.append((href, depth+1))
                except Exception:
                    pass
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                saved += 1
                urls.append(url)
                time.sleep(crawl_delay_ms/1000.0)
            except Exception:
                skipped["error"] += 1
                continue

    return {"page_count": saved, "skipped_count": sum(skipped.values()), "urls": urls, "skipped_reasons": skipped}
