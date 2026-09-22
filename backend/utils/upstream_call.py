"""
Shared upstream-call configuration (ST-13, EPIC-03, v9.6, BLG-BE-122).

Single source of truth for external-API timeout and retry-budget values,
built on top of utils/retry.py's retry_with_backoff decorator (BLG-BE-71,
v7.8) rather than replacing it — this module is the "configured in one
place" layer the ST-13 acceptance criteria ask for, not a new retry
mechanism.

Before this module, `timeout=` was set ad hoc at ~25 call sites across 8+
backend modules (Yahoo Finance/yfinance, Alpaca, Anthropic), and retry
coverage was inconsistent: some call sites (gemini_service.py's and
debrief_service.py's Anthropic calls, utils/pricing.py's
_yahoo_fetch_price, screener_batch_service.py's regime fetch) were already
migrated to retry_with_backoff by earlier stories (BLG-BE-71, BLG-BE-89);
others (utils/pricing.py's get_live_fx_rate, ai_service.py's 3 Anthropic
call sites) had none.

Scope (BLG-BE-122's own Scope section): migrates the nightly stop-update
path (yfinance + Alpaca, both feeding services.position_service.
run_nightly_trailing_stop_update via utils/pricing.py and
services/alpaca_service.py) and the yfinance-specific timeouts on the
screener path first. Deliberately NOT migrated this story (listed as
follow-ups instead, per BLG-BE-122's own "list remaining call sites as
follow-ups" instruction):
  - screener_data_service.py's Stooq and Twelve Data fallback tiers (not
    one of the 3 named providers; each has its own existing
    rate-limit/cooldown bookkeeping that a blind retry wrap risks
    interacting with poorly without a dedicated review)
  - live_trading_assistant.py, news_service.py, si05_digest_service.py,
    ai_endpoint_anomaly_service.py, routers/research.py, database.py,
    health_service.py, ticker_universe.py (no live-capital path urgency)
  - alpaca_service.py::get_ohlcv_bars's own status-code-aware retry
    bounds (429 up to 5 attempts, 5xx up to 3) are left as-is — already
    bounded and more sophisticated than the generic decorator (it
    distinguishes rate-limit vs. server-error vs. auth-failure); only its
    timeout value is migrated to this module's config, not its retry
    shape
"""
from typing import Dict, Tuple, Type

# Timeout, in seconds, applied per provider. Call sites that build their
# own request (requests.get(..., timeout=...), anthropic.Anthropic(timeout=...))
# read this via get_timeout(provider) at the point the request/client is
# constructed — this decorator module does not (and cannot, in general)
# inject a timeout transparently into an arbitrary wrapped call.
UPSTREAM_TIMEOUTS: Dict[str, float] = {
    "yfinance": 10,
    # Longer-range chart pulls (e.g. 1-year history for a 200-day moving
    # average) return a materially larger payload than a single-day quote
    # lookup and were already given a longer timeout (15s) at every such
    # call site before this migration — kept as its own key rather than
    # flattened into "yfinance" so this migration doesn't silently shrink
    # that timeout and introduce new spurious failures on slower large
    # responses.
    "yfinance_history": 15,
    "alpaca": 10,
    "anthropic": 60,
}

# Retry budget per provider: max_attempts (including the first, non-retry
# attempt) and base_delay in seconds (utils.retry.retry_with_backoff's
# exponential backoff starts here). Anthropic's budget is deliberately the
# same shape already proven safe by gemini_service.py/debrief_service.py
# (BLG-BE-89, v8.7) — max_attempts=3, base_delay=1.0 — not a larger budget
# borrowed from yfinance/Alpaca, because a retry re-issues paid inference
# and must stay within the existing AI cost gating (sprint_backlog.md
# ST-13 design-gate note). Keeping it identical to the already-shipped
# budget, rather than inventing a new number, is itself the conservative
# choice here.
UPSTREAM_RETRY_BUDGETS: Dict[str, Dict] = {
    "yfinance": {"max_attempts": 3, "base_delay": 0.5},
    "alpaca": {"max_attempts": 3, "base_delay": 0.5},
    "anthropic": {"max_attempts": 3, "base_delay": 1.0},
}


def get_timeout(provider: str) -> float:
    """Return the configured timeout (seconds) for `provider`.

    Raises KeyError for an unconfigured provider — deliberately not
    defaulted, so a typo'd provider name fails loudly at call time rather
    than silently reverting to some implicit default timeout.
    """
    return UPSTREAM_TIMEOUTS[provider]


def get_retry_budget(provider: str) -> Dict:
    """Return the configured {max_attempts, base_delay} dict for `provider`."""
    return UPSTREAM_RETRY_BUDGETS[provider]


def bounded_upstream_call(
    provider: str,
    retryable_exceptions: Tuple[Type[BaseException], ...] = (Exception,),
):
    """Decorator: apply `provider`'s configured retry budget via
    utils.retry.retry_with_backoff.

    Timeout is intentionally NOT applied by this decorator — it wraps
    whatever the function does internally, which may or may not accept a
    timeout kwarg the decorator could inject. Call get_timeout(provider)
    separately at the point the request/client is constructed, same as
    every migrated call site in this story does.
    """
    from utils.retry import retry_with_backoff

    budget = get_retry_budget(provider)
    return retry_with_backoff(
        max_attempts=budget["max_attempts"],
        base_delay=budget["base_delay"],
        retryable_exceptions=retryable_exceptions,
    )


def anthropic_retryable_exceptions() -> Tuple[Type[BaseException], ...]:
    """Lazily resolve the Anthropic SDK exception classes worth retrying:
    timeout, connection error, rate-limit, and transient 5xx
    (InternalServerError). NOT retried: 4xx client errors
    (BadRequestError, AuthenticationError, PermissionDeniedError,
    NotFoundError, etc.) — retrying those just repeats the same failure
    with added latency and, for Anthropic specifically, added cost.

    This is the same exception set gemini_service.py and debrief_service.py
    each independently derived (BLG-BE-89, v8.7) — centralised here so a
    third and fourth call site (this story's ai_service.py migration, and
    any future one) don't re-derive it again. Falls back to an empty tuple
    (retries nothing, i.e. today's pre-migration behaviour) if the
    `anthropic` package is ever absent, matching this codebase's existing
    lazy-import graceful-degradation convention.
    """
    try:
        import anthropic
        return (
            anthropic.APITimeoutError,
            anthropic.APIConnectionError,
            anthropic.RateLimitError,
            anthropic.InternalServerError,
        )
    except ImportError:
        return ()
