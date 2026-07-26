Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-26

# QA Evidence — EPIC-09 (v7.8)

**EPIC:** EPIC-09 — Shared retry/backoff decorator for external data calls
**Cycle:** 2026-07-24__release-v7.8
**Sprint goal:** Ship all 12 v7.8 EPICs with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_retry_backoff.py`

## ST-09 — Extract shared retry/backoff decorator and migrate highest-traffic call site

**Spec reference:** `backend/utils/retry.py` (new artefact, Case B — the module itself is the governing spec per `execution_prompt.md` STEP 3.1.A)
**Commit:** `473472a4` (implementation `a3db2612`)

**What was built:** `backend/utils/retry.py` — a `retry_with_backoff` decorator with configurable `max_attempts`, `base_delay`, `max_delay`, `backoff_factor`, a `retryable_exceptions` filter (so non-transient errors propagate immediately instead of wasting retries), and an injectable `sleep_fn` for test determinism. Per RISK-02's scope bound (proof-of-pattern on the single highest-traffic call site, no full retrofit), migrated `utils/pricing.py`'s `_yahoo_get_current_price` — confirmed the higher-traffic of the two candidates (Yahoo Finance vs Alpaca) by call-site count (9 consumer files vs Alpaca's 2) and by the fact that, unlike Alpaca's existing hand-rolled retry loop, Yahoo Finance previously had **no retry logic at all**. Restructured into an inner `_yahoo_fetch_price` (decorated, raises `requests.exceptions.RequestException` subtypes on transient failure or `ValueError` on a well-formed-but-empty response) wrapped by the original `_yahoo_get_current_price` (catches, logs, returns `None`) — the external contract for all callers is unchanged.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-09 | `backend/utils/retry.py` | `retry_with_backoff` decorator | Shared retry/backoff decorator or helper added with unit tests | Pass | None |
| ST-09 | (same) | Migrated `_yahoo_get_current_price` (via `_yahoo_fetch_price`) | At least the highest-traffic external call site migrated as proof of pattern | Pass | None |
| ST-09 | (same) | (same) | No full retrofit required — remaining call sites migrate incrementally | Pass — `alpaca_service.py` and other call sites explicitly left for future cycles per RISK-02 | None |

**QA test coverage:**
- Scenarios run: `tests/test_retry_backoff.py` — 9 tests: decorator behaviour (first-attempt success, retry-then-succeed, exhaustion/re-raise, max-delay capping, non-retryable-exception passthrough) and the migrated call site (first-try success, retry-then-succeed on `ConnectionError`, gives-up-after-3-attempts returning `None`, well-formed-empty-response not retried). All 9 pass (`backend/.venv/bin/python3 -m pytest tests/test_retry_backoff.py -v`).
- Regression areas checked: ran the 7 existing test files that consume `get_current_price`/pricing (`test_alerts_service.py`, `test_alpaca_integration.py`, `test_api_contracts.py`, `test_compliance_recheck.py`, `test_portfolio_integration.py`, `test_pre_entry_validation.py`, `test_price_alerts_service.py`, `test_trade_service.py`) — 193 tests total, all pass, no behavioural regression.
- Known deviations filed: None.

## Autonomous class eligibility check (BLG-GOV-19)

- Criterion 1 (all stories autonomous): ✓ — ST-09 is the only story, classified `autonomous`.
- Criterion 2 (all AC verifiable by code review alone, no observable UI/staging required): ✓ — verified entirely via unit tests, no UI surface.
- Criterion 3 (no frontend-visible change): ✓ — only `backend/utils/retry.py`, `backend/utils/pricing.py`, and `tests/test_retry_backoff.py` were touched; no file under `src/components/**` or `src/pages/**`.
- Criterion 4 (engine signer field populated): ✓ — see below.

**All four criteria met — autonomous class applies.**

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-26
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review/test-verifiable, no frontend changes, engine signer populated). 9 new unit tests pass; 193-test regression suite across all pricing consumers confirms no behavioural change.
