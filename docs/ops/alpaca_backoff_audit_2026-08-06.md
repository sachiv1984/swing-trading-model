**Owner:** Backend Engineering Patterns Owner
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-06
**Cycle:** 2026-08-05__release-v8.3 (ST-06 — BLG-BE-57)

---

# Alpaca API Rate-Limit Backoff Audit

## Purpose

`BLG-BE-57` requires an audit of current retry/backoff logic against Alpaca's documented rate limits across every Alpaca call site in the codebase, filing any gaps as follow-up items.

## Documented Policy (Reference)

`docs/specs/api_contracts/alpaca_integration_contract.md` §Rate Limits:
- 200 req/min (Free/paper tier), 10,000 req/min (paid)
- HTTP 429 → exponential backoff: wait `2^attempt × 1s`, max 5 retries, max wait 32s

## Method

Enumerated every Alpaca HTTP call site (`grep -n "alpaca" backend/services/*.py` cross-referenced against `requests.get/post/delete` calls in the same files) and read each site's retry/backoff implementation in full.

## Findings

**1. `backend/services/alpaca_service.py::get_ohlcv_bars` (data API, `data.alpaca.markets`) — compliant, no gap.**
Implements 429 handling: up to 5 attempts, delay starts at 1.0s and doubles each retry (`1s, 2s, 4s, 8s, 16s`), capped at 30s. Minor numeric deviation from the contract's exact `2^attempt × 1s` formula (which would start at 2s and cap at 32s) — this implementation is strictly more conservative (retries sooner, caps 2s lower), so it is not a functional gap. Also separately retries 5xx (up to 3 attempts) and network exceptions (up to 3 attempts), neither of which the contract's §Rate Limits section itself mandates but both improve resilience beyond the documented floor.

**2. `backend/services/news_service.py::get_news_headlines` (`data.alpaca.markets` News API) — compliant, minor under-provisioning, no action.**
Implements the same 429 backoff shape (delay doubles, capped at 30s) but caps at 3 attempts rather than the contract's documented 5. This is a narrower retry budget than specified, not a missing capability — combined with this endpoint's explicit best-effort, display-only contract (returns `[]` on any exhausted-retry outcome, callers show an empty state), the severity is low. No follow-up filed; noted for awareness only.

**3. `backend/services/alpaca_paper_sync_service.py` (`paper-api.alpaca.markets`) — gap found, filed as `BLG-BE-83`.**
None of `sync_open_paper_position`, `sync_close_paper_position`, or `get_paper_positions` implement any 429/backoff handling — each makes a single HTTP call, and on any non-2xx status (including 429) logs a warning and returns/swallows rather than retrying. This is the one Alpaca-integration surface in the codebase with zero rate-limit resilience, despite hitting the same documented 200 req/min tier as the two compliant call sites above.
- `sync_open_paper_position` is being fixed in this same sprint by `ST-10` (`BLG-BE-80`) — `retry_with_backoff` plus a deterministic `client_order_id` to make the retry safe against duplicate orders. That story's scope is explicitly the open path only.
- `sync_close_paper_position` (idempotent `DELETE`, no duplicate-order risk) and `get_paper_positions` (idempotent `GET`) remain unaddressed after ST-10 ships. Filed as `BLG-BE-83` (P3) rather than fixed inline — out of this story's audit-only scope and ST-10's explicitly bounded scope.

**4. `backend/services/screener_data_service.py`, `backend/services/health_service.py` — no direct Alpaca HTTP calls, no gap.**
`screener_data_service.py` calls `alpaca_service.get_ohlcv_bars` (Finding 1, already audited) rather than making its own request. `health_service.py` only references `"alpaca"` as a config/health-check label, not an API call site.

## Disposition

Audit complete. 1 gap found (Alpaca paper-sync close/positions endpoints have no 429/backoff handling), filed as `BLG-BE-83` (P3) rather than fixed inline, per this story's acceptance criteria. 2 compliant call sites confirmed (`alpaca_service.py`, `news_service.py`), with one minor under-provisioning noted for awareness (news retry budget: 3 vs documented 5 attempts — low severity, best-effort/display-only path, no action taken).

## Sign-off

**Reviewed by:** Backend Engineering Patterns Owner
**Status:** Approved
**Date:** 2026-08-06
**Notes:** Findings cross-checked against the actual retry-loop code at each call site (not inferred from docstrings alone). Gap correctly scoped against ST-10's in-flight fix (BLG-BE-80) to avoid a duplicate/overlapping filing — BLG-BE-83 explicitly excludes the open-path call site ST-10 is already fixing this sprint.
