Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-24

# Delegation Log — 2026-05-22__release-v4.0

Append-only. All delegated tasks across Sprint 1 and Sprint 2.

---

## DEL-20260524-01

- **ST Item:** ST-05 — Validate ticker symbol on add
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #479
- **Branch:** exec/2026-05-22__release-v4.0/EPIC-02
- **Delegated at:** 2026-05-24T08:00:00Z
- **What is needed:** Add real-time Yahoo Finance symbol validation to `POST /ticker-universe`. When a user adds a ticker, the backend must verify the symbol exists and is tradeable using `yfinance` before inserting it into the universe.

  **Context:** The ticker universe is the sole authoritative source for screener and signal generation. Adding an invalid ticker (typo, delisted, or unknown symbol) silently corrupts the universe. This story adds a live lookup gate at the `POST /ticker-universe` endpoint. `yfinance` is already in `backend/requirements.txt`.

  **Note on staging-only AC:** The live Yahoo Finance lookup AC (`invalid ticker returns 422 with meaningful error`) requires a staging environment with internet access. This is a staging-only AC. A backlog item must be filed for staging verification before the PR opens (see notes in sprint_backlog.md). The unit test stub in `backend/routers/test.py` must mock `yfinance` — do not make live network calls in CI.

  **Change required:**
  - In `POST /ticker-universe` handler (file: `backend/routers/ticker_universe.py`):
    1. Before inserting, call `yfinance.Ticker(ticker).info` (or equivalent minimal fetch)
    2. If `info` is empty dict, `quoteType` is absent, or any `yfinance` exception is raised → return HTTP 422 with `{ "detail": "Ticker '<TICKER>' not found or not tradeable" }`
    3. If valid, proceed with existing insert logic
  - The validation must be skipped (or mocked) when `SKIP_TICKER_VALIDATION=true` env var is set — this allows the existing test suite to pass without live Yahoo Finance calls
  - `backend/routers/test.py`: add a test entry for `POST /ticker-universe` with a valid ticker (`AAPL`). The test should pass in CI using the `SKIP_TICKER_VALIDATION=true` env var or a `yfinance` mock in conftest.py
  - Staging-only AC: add `BLG-QA-xx` backlog item for live Yahoo Finance rejection path testing before PR opens

  **API contract reference:** `docs/specs/api_contracts/ticker_universe_api_contract.md#POST /ticker-universe`
  - Current spec shows `400` for invalid market/blank ticker. This story adds `422` for invalid Yahoo Finance symbol
  - Update the Error Responses table in the spec to add `422` row: `| 422 | Ticker not found or not tradeable via Yahoo Finance live lookup |`

  **Behaviour rules:**
  - Valid ticker → insert proceeds exactly as before (no change to happy path)
  - Invalid ticker → 422 with detail message
  - `SKIP_TICKER_VALIDATION=true` env var bypasses the yfinance call entirely (CI safety valve)
  - Yahoo Finance timeout (>5s) → treat as invalid, return 422 with detail "Ticker validation timed out — check symbol and retry"
  - Do not call yfinance for DELETE or GET operations — validation only on POST

  **Non-functional rules:**
  - No live Yahoo Finance calls in CI — must use env var bypass or mock
  - yfinance call must have a 5-second timeout
  - Staging-only AC must have a filed backlog item before PR opens

  **Expected outcome:** `POST /ticker-universe` rejects unknown/delisted tickers with HTTP 422. Valid tickers continue to be added as before. The yfinance call is bypassed in CI environments.

- **Spec reference:** `docs/specs/api_contracts/ticker_universe_api_contract.md#POST /ticker-universe`
- **Unblock criteria:** Commit `[EPIC-02][ST-05] ...` pushed to `exec/2026-05-22__release-v4.0/EPIC-02`; `backend/routers/test.py` updated; staging-only AC backlog item filed; `SKIP_TICKER_VALIDATION` env var implemented; API contract updated with 422 row; GitHub issue #479 closed automatically
- **Commit format required:** `[EPIC-02][ST-05] <description>` pushed to `exec/2026-05-22__release-v4.0/EPIC-02`
- **SLA:** Next available sprint cycle
- **Status:** Unblocked — commit 494eb022 pushed 2026-05-24; BLG-QA-30 filed; API contract v1.2 updated; SKIP_TICKER_VALIDATION bypass implemented

---
