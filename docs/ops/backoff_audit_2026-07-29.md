**Owner:** Backend Engineering Patterns Owner
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-29
**Cycle:** 2026-07-28__release-v7.10 (ST-02 — BLG-BE-75)

---

# Retry/Backoff Audit — Yahoo Finance, Gemini, and Claude Call Sites

## Purpose

`BLG-BE-57` audited retry/backoff behaviour for Alpaca call sites only. ST-02 (BLG-BE-75) extends the same methodology to the three remaining named providers — Yahoo Finance, Gemini, and Claude — confirming each external call site either uses the shared `retry_with_backoff` decorator (`backend/utils/retry.py`, BLG-BE-71) or has a documented rationale for not using it.

## Scope Note — "Gemini" and "Claude" are the same provider

Per `database.py::get_monthly_claude_cost()`'s own docstring (ST-07, EPIC-07, v7.6, reframed under `ESC-EXEC-20260720-01`): **Claude is the only AI provider integrated in this codebase.** There is no `google-generativeai` package installed and no `GEMINI_API_KEY` anywhere in the environment or config. `backend/services/gemini_service.py` is a legacy-named module (predates the provider switch) whose `_call_claude()` helper calls the Anthropic API exclusively. This audit therefore treats "Gemini" and "Claude" as one provider (Anthropic) with two call-site groups (`gemini_service.py` and `ai_service.py`), not four distinct external systems.

## Method

Full enumeration via `grep` of all `yf.Ticker`/`requests.get`/`requests.post` calls to Yahoo Finance domains and all `anthropic.Anthropic(...)` client instantiations across `backend/services/*.py`, `backend/routers/*.py`, and `backend/utils/*.py`, cross-referenced against `backend/utils/retry.py` decorator usage.

## Findings — Yahoo Finance (9 call sites)

| # | Call site | Decorator? | Disposition |
|---|-----------|:---:|-------------|
| 1 | `utils/pricing.py::_yahoo_fetch_price` (via `get_current_price`) | ✅ Yes | Compliant — highest-traffic site, `retry_with_backoff(max_attempts=3)` |
| 2 | `utils/pricing.py::get_live_fx_rate` | ❌ No | Accepted exception — 5-min TTL cache already absorbs failures; single-attempt with hardcoded `DEFAULT_FX_RATE` fallback is intentional graceful-degradation, not an oversight |
| 3 | `utils/pricing.py::check_market_regime` (inner `get_ma200`) | ❌ No | Gap — filed as `BLG-BE-79` |
| 4 | `services/screener_batch_service.py::_fetch_index_regime` | ❌ No | Gap — filed as `BLG-BE-79` (same regime-check pattern as #3, single follow-up covers both) |
| 5 | `services/earnings_service.py` (`yf.Ticker(...)`) | ❌ No | Accepted exception — enrichment-only (next earnings date), caller already tolerates `None`, low call frequency |
| 6 | `services/gap_risk_service.py` (`yf.Ticker(...).history`) | ❌ No | Accepted exception — same enrichment-only rationale as #5 |
| 7 | `services/sector_service.py`, `services/ticker_universe_service.py`, `services/watchlist_service.py`, `routers/ticker_universe.py`, `routers/research.py` (`yf.Ticker(...).info` / company-name lookups) | ❌ No | Accepted exception — all are best-effort metadata enrichment (sector, company name) with existing try/except-and-continue callers; not on any pricing/trading hot path |

## Findings — Claude / Anthropic (5 call sites)

| # | Call site | Decorator? | Disposition |
|---|-----------|:---:|-------------|
| 1 | `services/gemini_service.py::_call_claude` (used by `generate_full_plan`, `generate_setup_thesis`) | ❌ No | Accepted exception — see rationale below |
| 2 | `services/ai_service.py` — journal summary, daily briefing, chat (3 call sites) | ❌ No | Accepted exception — same rationale |

**Rationale (documented here per ST-02 AC, formalising a previously-implicit pattern):** all 4 Claude call sites are invoked synchronously within a live user-facing HTTP request/response cycle (chat, daily briefing, thesis generation). Unlike a background price fetch, adding `retry_with_backoff` here would directly multiply client-facing latency on every retry attempt (each backoff delay is added to the response the user is waiting on). Every call site already: (a) sits behind its own per-endpoint rate limiter (`_ai_limiter`, `services/rate_limiter.py`) bounding request volume, (b) catches all exceptions and degrades gracefully (`available: False` / an informational message, never a 500), and (c) is cost-tracked with a daily-spend alert (`check_and_alert_daily_cost`). A single-attempt-with-graceful-degradation pattern is the correct trade-off for synchronous LLM calls in this codebase; this audit formalises that as the documented exception rather than leaving it implicit.

## Findings — Alpaca (out of primary scope, cross-checked for consistency)

`services/alpaca_service.py::get_ohlcv_bars` already has its own hand-rolled, status-code-aware retry (429 → up to 5 attempts exponential, 5xx → up to 3, 403 → no retry) — more granular than the generic decorator supports, so it is correctly left as a documented exception (`BLG-BE-57`'s own finding, unchanged).

`services/alpaca_paper_sync_service.py` (paper-trading order mirror, `IT-06`) has **no retry at all** on its `POST /v2/orders` and `DELETE /v2/positions/{ticker}` calls. This was not in `BLG-BE-57`'s original Alpaca scope (that audit covered the market-data client only) but surfaced during this pass. Blind retry is unsafe here — a retried `POST /v2/orders` without a client-supplied idempotency key risks a duplicate paper order. Filed as `BLG-BE-80` (P3 — paper-trading mirror only, no real-money risk) recommending Alpaca's `client_order_id` field rather than the generic backoff decorator.

## Summary

| Provider | Call sites | Compliant (decorator) | Accepted exception | Gaps filed |
|----------|:---:|:---:|:---:|:---:|
| Yahoo Finance | 9 | 1 | 6 | 2 (via `BLG-BE-79`) |
| Claude (incl. "Gemini") | 5 | 0 | 5 | 0 |
| Alpaca (cross-check) | 2 | 1 | 0 | 1 (`BLG-BE-80`) |

All 4 providers named in ST-02's scope are accounted for: every call site either uses the shared decorator or has a documented, reasoned exception recorded above. 2 genuine gaps (regime-check retry, paper-sync idempotent retry) filed as P3 follow-ups per the same "gaps filed as follow-up items" convention `BLG-BE-57` established — neither blocks this story per its acceptance criteria.

## Sign-off

**Backend Engineering Patterns Owner:** Confirmed — all 4 providers' call sites reviewed; decorator usage or documented exception recorded for each; 2 gaps filed as follow-up items. 2026-07-29.
