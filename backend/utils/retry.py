"""
Shared retry/backoff decorator for external data calls (ST-09, EPIC-09, v7.8, BLG-BE-71).

Proof-of-pattern extraction: prior to this module, retry logic for external
API calls was hand-rolled per call site (e.g. `services/alpaca_service.py`'s
inline exponential backoff loop), and the highest-traffic call site
(`utils/pricing.py`'s Yahoo Finance price fetch, used by every `get_current_price()`
call — US-ticker fallback and all UK tickers) had no retry logic at all.

RISK-02 (sprint_backlog.md, EPIC-09): scope is bounded to proof-of-pattern on
the single highest-traffic call site (Yahoo Finance) — no full retrofit of
every external call site (e.g. `alpaca_service.py`) this cycle. Remaining
call sites migrate incrementally in future cycles.
"""
import time
import logging
import functools

logger = logging.getLogger(__name__)


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    backoff_factor: float = 2.0,
    retryable_exceptions=(Exception,),
    sleep_fn=time.sleep,
):
    """
    Decorator: retries the wrapped function on the given exception type(s)
    using exponential backoff, then re-raises the final exception if every
    attempt is exhausted.

    Delay sequence: base_delay, base_delay*backoff_factor, base_delay*backoff_factor^2, ...
    capped at max_delay. No delay after the final (failing) attempt.

    Args:
        max_attempts: total attempts including the first (non-retry) call.
        base_delay: seconds to wait before the first retry.
        max_delay: upper bound on the backoff delay.
        backoff_factor: multiplier applied to the delay after each failed attempt.
        retryable_exceptions: exception type or tuple of types that trigger a retry.
            Exceptions not matching this filter propagate immediately (no retry) —
            e.g. a data-validation error should not be retried, only transient
            network/rate-limit errors should be.
        sleep_fn: injected sleep function (defaults to `time.sleep`); tests pass
            a no-op stand-in to avoid real wall-clock delay.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as exc:
                    if attempt >= max_attempts:
                        logger.warning(
                            "%s failed after %d attempt(s): %s", func.__name__, attempt, exc
                        )
                        raise
                    logger.info(
                        "%s attempt %d/%d failed (%s), retrying in %.1fs",
                        func.__name__, attempt, max_attempts, exc, delay,
                    )
                    sleep_fn(delay)
                    delay = min(delay * backoff_factor, max_delay)

        return wrapper

    return decorator
