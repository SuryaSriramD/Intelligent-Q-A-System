from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any

class CrawlRequest(BaseModel):
    start_url: HttpUrl
    max_pages: int = Field(ge=1, le=1000, default=40)
    max_depth: int = Field(ge=0, le=10, default=2)
    crawl_delay_ms: int = Field(ge=0, le=5000, default=400)

class CrawlResponse(BaseModel):
    page_count: int
    skipped_count: int
    urls: List[str]
    skipped_reasons: Dict[str, int]
    indexed: bool = False  # Whether content was automatically indexed
    vector_count: int = 0  # Number of chunks indexed

class IndexRequest(BaseModel):
    chunk_size: int = Field(ge=200, le=4000, default=800)
    chunk_overlap: int = Field(ge=0, le=1000, default=120)

class IndexResponse(BaseModel):
    vector_count: int
    errors: List[str] = []

class Source(BaseModel):
    url: str
    snippet: str
    start: int
    end: int
    title: str = ""

class AskRequest(BaseModel):
    question: str
    top_k: int = Field(ge=1, le=20, default=6)

class AskResponse(BaseModel):
    answer: str
    sources: List[Source]
    timings: Dict[str, Any]
    retrieval_debug: Dict[str, Any]
    closest: Optional[List[Dict[str, str]]] = []

class CrawlAndAskRequest(BaseModel):
    """One-shot: crawl a URL and immediately answer a question about it."""
    start_url: HttpUrl
    question: str
    max_pages: int = Field(ge=1, le=1000, default=10)
    max_depth: int = Field(ge=0, le=10, default=2)
    crawl_delay_ms: int = Field(ge=0, le=5000, default=400)
    top_k: int = Field(ge=1, le=20, default=6)

class CrawlAndAskResponse(BaseModel):
    """Response with both crawl stats and the answer."""
    crawl: CrawlResponse
    answer: AskResponse
