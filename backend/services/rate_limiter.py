"""
In-memory sliding-window rate limiter.

ST-03 (BLG-OPS-81, EPIC-01, v6.3) — AI endpoint per-endpoint rate limiting.
Thread-safe. No external dependencies. Single-process scope (sufficient for
single-instance Render deployment).
"""

from collections import defaultdict
from threading import Lock
from time import time


class RateLimiter:
    def __init__(self):
        self._windows: dict = defaultdict(list)
        self._lock = Lock()

    def is_allowed(self, key: str, limit: int, window_secs: int = 60) -> tuple[bool, int]:
        """
        Sliding-window check. Returns (allowed, retry_after_secs).
        retry_after_secs is 0 when allowed.
        """
        now = time()
        with self._lock:
            window = self._windows[key]
            cutoff = now - window_secs
            window[:] = [t for t in window if t > cutoff]
            if len(window) >= limit:
                retry_after = int(window[0] + window_secs - now) + 1
                return False, retry_after
            window.append(now)
            return True, 0

    def reset(self, key: str) -> None:
        """Remove all timestamps for a key. Used in tests only."""
        with self._lock:
            self._windows.pop(key, None)


_ai_limiter = RateLimiter()

# ST-08 (EPIC-08, v7.8, BLG-SEC-21) — rate-limiting audit remediation: a
# separate limiter instance for endpoints that are NOT gated by X-API-Key
# (currently only GET /health, the app's sole unauthenticated surface).
# Kept distinct from _ai_limiter so AI-endpoint traffic and public-endpoint
# traffic never share a sliding window under the same key namespace.
_public_limiter = RateLimiter()
