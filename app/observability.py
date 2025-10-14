import time, statistics
from functools import wraps
from structlog import get_logger

_log = get_logger()
_latencies = []  # rolling ms

def with_timings(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        try:
            return fn(*args, **kwargs)
        finally:
            ms = (time.time() - t0) * 1000.0
            _latencies.append(ms)
            if len(_latencies) > 500:
                del _latencies[:200]  # keep window bounded
            _log.info("timing", handler=fn.__name__, ms=ms)
    return wrapper

def metrics_snapshot():
    if not _latencies:
        return {"count": 0}
    return {
        "count": len(_latencies),
        "p50_ms": statistics.quantiles(_latencies, n=2)[0],
        "p95_ms": quantile(_latencies, 0.95),
    }

def quantile(xs, q):
    xs = sorted(xs)
    idx = int((len(xs)-1) * q)
    return xs[idx]
