"""
Shared cache and concurrency cap for yfinance `Ticker.info` lookups
(ST-15, BLG-OPS-217, EPIC-06, v9.17).

Why: production `api_call_log` (7 days to 2026-11-13) showed 86% of the week's
on-demand Yahoo failures in one two-minute burst (2026-11-09 15:37-15:38: 471
calls, 418 failed). A page that renders one earnings badge per row fires one
`GET /earnings/{ticker}` per row at once, each costing about four Yahoo calls
(getcrumb, quoteSummary, quote, timeseries). Yahoo then refuses the crumb and
the crumb-dependent calls fail. Quiet page loads succeeded. Research made
three `Ticker.info` calls for the same symbol per request (sector, market cap,
earnings), and each Positions load ran one per position for the sector.

What this module does:
  - `get_info(symbol, load)` returns a cached `Ticker.info` dict for `symbol`,
    or calls `load()` to fetch it. Only a usable result (one carrying
    `quoteType`, which every successful quoteSummary/quote answer has) is
    cached, for INFO_TTL_SECONDS. A failed or empty lookup is never cached, so
    a throttled answer is not kept as "no data".
  - At most MAX_CONCURRENT_LOOKUPS fetches run at once across the process; the
    rest wait up to SLOT_WAIT_SECONDS for a slot, then raise YahooInfoBusy,
    which callers treat like any failed lookup.
  - `TTLCache` is also used by earnings_service for its own results.

`load` is passed in, rather than this module calling yf.Ticker itself, so each
caller keeps its own `yf.Ticker` reference (and its existing test patches).

Trade-off: FastAPI runs sync endpoints on a worker thread pool (40 threads by
default). During a cold burst, waiting requests hold a thread while queued, so
other endpoints may wait too until the burst drains. A warm cache serves the
same page with no Yahoo call and no wait.
"""
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

MAX_CONCURRENT_LOOKUPS = 4
SLOT_WAIT_SECONDS = 30.0
INFO_TTL_SECONDS = 12 * 60 * 60

_MISSING = object()


class YahooInfoBusy(Exception):
    """No lookup slot came free within SLOT_WAIT_SECONDS."""


class TTLCache:
    """A small thread-safe key -> value cache with a per-entry expiry."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entries: Dict[Any, Tuple[float, Any]] = {}
        _CACHES.append(self)

    def get(self, key, default=None, now: Optional[float] = None):
        now = time.monotonic() if now is None else now
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return default
            expires, value = entry
            if now >= expires:
                del self._entries[key]
                return default
            return value

    def set(self, key, value, ttl_seconds: float, now: Optional[float] = None) -> None:
        now = time.monotonic() if now is None else now
        with self._lock:
            self._entries[key] = (now + ttl_seconds, value)

    def delete(self, key) -> None:
        with self._lock:
            self._entries.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()

    def __len__(self) -> int:
        with self._lock:
            return len(self._entries)


_CACHES: List[TTLCache] = []
_slots = threading.BoundedSemaphore(MAX_CONCURRENT_LOOKUPS)
_info_cache = TTLCache()


def clear_caches() -> None:
    """Empty every cache built on TTLCache (tests; never needed in production)."""
    for cache in list(_CACHES):
        cache.clear()


def is_usable_info(info) -> bool:
    return isinstance(info, dict) and bool(info.get("quoteType"))


def call_with_slot(load: Callable[[], Any]):
    """Run `load` while holding one of the MAX_CONCURRENT_LOOKUPS slots."""
    if not _slots.acquire(timeout=SLOT_WAIT_SECONDS):
        raise YahooInfoBusy(f"no Yahoo lookup slot free within {SLOT_WAIT_SECONDS:g}s")
    try:
        return load()
    finally:
        _slots.release()


def get_info(symbol: str, load: Callable[[], Dict]) -> Dict:
    """`Ticker.info` for a Yahoo symbol, from the cache or from `load()`.

    Raises whatever `load` raises, or YahooInfoBusy; callers already treat an
    exception as "no data".
    """
    key = symbol.upper()
    cached = _info_cache.get(key, _MISSING)
    if cached is not _MISSING:
        return cached

    def fetch():
        # Another request may have filled the cache while this one waited.
        again = _info_cache.get(key, _MISSING)
        if again is not _MISSING:
            return again
        info = load()
        if is_usable_info(info):
            _info_cache.set(key, info, INFO_TTL_SECONDS)
        return info

    return call_with_slot(fetch)
