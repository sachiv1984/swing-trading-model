"""
External data-provider call attribution (ST-31, EPIC-05, v9.13, BLG-OPS-19)

Tags every outbound HTTP request to a market-data provider with the feature
that triggered it, and writes one api_call_log row per request with
service = the provider and feature = the trigger.

The feature is a ContextVar: api_attribution_middleware in main.py sets it
for each request to a resolver returning "<METHOD> <route template>" (e.g.
"POST /screener/run"). It is resolved when a call is recorded, because the
router only puts the matched route in the request scope after the
middleware runs. Every call made while handling that request, including its
background tasks, carries it. Outside a request it is "unattributed" unless code sets
one with feature_scope(). ThreadPoolExecutor workers do not inherit the
caller's context; submit them through contextvars.copy_context().run, as
screener_batch_service.run_screener does.

Calls are counted at the transport layer, not per call site: install()
wraps requests.Session.request (which requests.get/post go through) and
curl_cffi's Session.request (yfinance's transport). A request to a host not
in PROVIDER_HOSTS (Anthropic, Telegram, Supabase, Render) is not recorded;
Anthropic calls are already attributed per endpoint in claude_audit_log.
Each HTTP attempt is one row, so internal retries count, which is what a
provider's quota counts.

Rows are buffered in memory and written in one batch: at the end of each
request (middleware), at the end of a screener run, and whenever the
buffer reaches FLUSH_THRESHOLD. Writing a row per call would open a
database connection per call (external_api_dependency_register.md SFM-01).
A failed write drops the batch and logs a warning; attribution must never
break the request that made the call.

The service names here are distinct from the existing per-call-site rows
(service "alpaca" from alpaca_service._log_alpaca_call, "research" from
routers/research.py), so GET /ops/alpaca-call-report and
GET /ops/research-session-report keep their meaning.
"""
import contextlib
import contextvars
import logging
import threading
from datetime import datetime, timezone
from typing import Dict, Iterator, List, Optional, Tuple
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)

UNATTRIBUTED = "unattributed"
FLUSH_THRESHOLD = 100

# host -> service. data.alpaca.markets serves both bars and news; news is
# split out by path in classify().
PROVIDER_HOSTS: Dict[str, str] = {
    "data.alpaca.markets": "alpaca_data",
    "paper-api.alpaca.markets": "alpaca_paper",
    "api.alpaca.markets": "alpaca_trading",
    "query1.finance.yahoo.com": "yahoo",
    "query2.finance.yahoo.com": "yahoo",
    "finance.yahoo.com": "yahoo",
    "fc.yahoo.com": "yahoo",
    "guce.yahoo.com": "yahoo",
    "api.twelvedata.com": "twelve_data",
    "stooq.com": "stooq",
}
ALPACA_NEWS_PATH_PREFIX = "/v1beta1/news"
ALPACA_NEWS_SERVICE = "alpaca_news"

# USD per request. Every provider in use is free at current usage
# (docs/operations/data_provider_risk_assessment.md §1): Alpaca on the IEX
# feed, Yahoo with no key, Alpaca news, the Alpaca paper account. Change a
# value here if a provider starts charging per call; the attribution report
# multiplies call counts by it.
UNIT_COST_USD: Dict[str, float] = {
    "alpaca_data": 0.0,
    ALPACA_NEWS_SERVICE: 0.0,
    "alpaca_paper": 0.0,
    "alpaca_trading": 0.0,
    "yahoo": 0.0,
    "twelve_data": 0.0,
    "stooq": 0.0,
}
PROVIDER_SERVICES: Tuple[str, ...] = tuple(UNIT_COST_USD)

_feature_var: contextvars.ContextVar = contextvars.ContextVar("api_call_feature", default=UNATTRIBUTED)

_buffer: List[Tuple[str, str, str, bool, datetime]] = []
_buffer_lock = threading.Lock()
_installed = False


def get_feature() -> str:
    feature = _feature_var.get()
    return feature() if callable(feature) else feature


def set_feature(feature) -> contextvars.Token:
    """Set the feature: a string, or a zero-argument callable resolved at
    each recorded call."""
    return _feature_var.set(feature)


def reset_feature(token: contextvars.Token) -> None:
    _feature_var.reset(token)


@contextlib.contextmanager
def feature_scope(feature: str) -> Iterator[None]:
    """Attribute calls made inside the block to `feature`."""
    token = _feature_var.set(feature)
    try:
        yield
    finally:
        _feature_var.reset(token)


def classify(url: str) -> Optional[Tuple[str, str]]:
    """Return (service, path) for a provider URL, or None for any other host."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return None
    host = (parts.hostname or "").lower()
    service = PROVIDER_HOSTS.get(host)
    if service is None:
        return None
    path = parts.path or "/"
    if service == "alpaca_data" and path.startswith(ALPACA_NEWS_PATH_PREFIX):
        service = ALPACA_NEWS_SERVICE
    return service, path


def record_call(url: str, success: bool) -> None:
    """Buffer one call if `url` is a provider; flush when the buffer is full."""
    classified = classify(url)
    if classified is None:
        return
    service, path = classified
    row = (service, path, get_feature(), success, datetime.now(timezone.utc))
    with _buffer_lock:
        _buffer.append(row)
        full = len(_buffer) >= FLUSH_THRESHOLD
    if full:
        flush()


def pending_count() -> int:
    with _buffer_lock:
        return len(_buffer)


def flush() -> int:
    """Write buffered rows to api_call_log in one batch. Returns rows written."""
    with _buffer_lock:
        rows = list(_buffer)
        _buffer.clear()
    if not rows:
        return 0
    try:
        from database import log_api_calls
        log_api_calls(rows)
    except Exception as exc:
        logger.warning("api_call_log attribution flush failed, %d rows dropped: %s", len(rows), exc)
        return 0
    return len(rows)


def _wrap_request(original):
    def request(self, method, url, *args, **kwargs):
        try:
            response = original(self, method, url, *args, **kwargs)
        except Exception:
            record_call(str(url), False)
            raise
        status = getattr(response, "status_code", 200) or 200
        record_call(str(url), status < 400)
        return response

    request._api_attribution_original = original
    return request


def install() -> None:
    """Wrap the HTTP clients' request methods. Idempotent."""
    global _installed
    if _installed:
        return
    import requests

    requests.Session.request = _wrap_request(requests.Session.request)
    try:
        from curl_cffi import requests as curl_requests

        curl_requests.Session.request = _wrap_request(curl_requests.Session.request)
    except ImportError:
        logger.info("curl_cffi not installed; yfinance calls made with it are not attributed")
    _installed = True


def build_attribution_report(rows: List[Dict], window: str) -> Dict:
    """Combine per-(feature, service) counts into a cost-by-feature report.

    rows: [{"feature", "service", "total_calls", "failure_count"}].
    Features are ranked by estimated cost, then by call count, so the top 3
    are meaningful while every provider is free.
    """
    by_feature: Dict[str, Dict] = {}
    by_service: Dict[str, Dict] = {}
    for row in rows:
        service = row["service"]
        calls = int(row["total_calls"])
        failures = int(row["failure_count"])
        cost = calls * UNIT_COST_USD.get(service, 0.0)
        feature = by_feature.setdefault(
            row["feature"] or UNATTRIBUTED,
            {"feature": row["feature"] or UNATTRIBUTED, "total_calls": 0, "failure_count": 0,
             "estimated_cost_usd": 0.0, "by_service": {}},
        )
        feature["total_calls"] += calls
        feature["failure_count"] += failures
        feature["estimated_cost_usd"] += cost
        feature["by_service"][service] = feature["by_service"].get(service, 0) + calls
        svc = by_service.setdefault(service, {"service": service, "total_calls": 0, "failure_count": 0,
                                              "estimated_cost_usd": 0.0})
        svc["total_calls"] += calls
        svc["failure_count"] += failures
        svc["estimated_cost_usd"] += cost

    features = sorted(by_feature.values(), key=lambda f: (-f["estimated_cost_usd"], -f["total_calls"], f["feature"]))
    for f in features:
        f["estimated_cost_usd"] = round(f["estimated_cost_usd"], 6)
    services = sorted(by_service.values(), key=lambda s: (-s["total_calls"], s["service"]))
    for s in services:
        s["estimated_cost_usd"] = round(s["estimated_cost_usd"], 6)
    return {
        "window": window,
        "total_calls": sum(f["total_calls"] for f in features),
        "estimated_cost_usd": round(sum(f["estimated_cost_usd"] for f in features), 6),
        "unit_cost_usd": dict(UNIT_COST_USD),
        "by_feature": features,
        "by_service": services,
        "top_contributors": [f["feature"] for f in features[:3]],
    }
