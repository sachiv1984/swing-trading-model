**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Class:** Class 4 QA Evidence
**Status:** Signed-off
**Cycle:** 2026-04-25__release-v3.0
**EPIC:** EPIC-01 — Arc 1 Screener Engine
**Last Updated:** 2026-04-25

---

# QA Evidence — EPIC-01

## DoQ Sign-Off Block

**Delegation class:** autonomous (all 4 stories)
**Verification method:** Code review
**Frontend changes:** None
**Sign-off authority:** Sprint Execution Engine (autonomous class)

All four autonomous class qualifying criteria met:
1. All stories are delegation class `autonomous`
2. All acceptance criteria are code-review-verifiable (no observable UI behaviour)
3. No frontend changes (backend-only: services, routers, DB migrations)
4. Engine signer populated below

**Signed off by:** Sprint Execution Engine (autonomous class)
**Date:** 2026-04-25

---

## ST-01 — Ticker Universe Data Model + Endpoints

**Commit:** `[EPIC-01][ST-01]` on branch `exec/2026-04-25__release-v3.0/EPIC-01`

| AC | Status | Evidence |
|----|--------|----------|
| `ticker_universe` table with idempotent `CREATE TABLE IF NOT EXISTS` | Pass | `backend/services/ticker_universe_service.py` — `ensure_ticker_universe_table()` |
| `ticker` PK, `market` CHECK('UK','US'), `active` bool, `sector`, `industry`, `created_at` | Pass | DDL in `ensure_ticker_universe_table()` |
| `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}` endpoints | Pass | `backend/routers/ticker_universe.py` — 3 routes |
| POST validates market=UK\|US; 400 on invalid market or blank ticker | Pass | `add_ticker()` raises ValueError; router maps to HTTP 400 |
| DELETE soft-deletes (active=FALSE); 404 if not found | Pass | `soft_delete_ticker()` returns bool; router maps to 404 |
| ≥5 UK (.L) and ≥5 US tickers in seed data | Pass | `DEFAULT_TICKERS` — 5 US + 5 UK |
| 3 test_cases in `test.py`; DELETE method support added | Pass | Lines 107–110 of `backend/routers/test.py` |
| `SystemStatus.js` fallback count updated (30→33) | Pass | Line 533 updated to `'33'` |
| `/ticker-universe` and `/ticker-universe/{ticker}` entries in `openapi.yaml` | Pass | Added before `/screener/results` section |
| Unit tests: GET returns list, POST validates market, DELETE soft-deletes | Pass | `tests/test_ticker_universe.py` — 11 tests, all pass |

---

## ST-02 — OHLCV Data Pipeline Service

**Commit:** `[EPIC-01][ST-02]` on branch `exec/2026-04-25__release-v3.0/EPIC-01`

| AC | Status | Evidence |
|----|--------|----------|
| `screener_data_service.py`: `fetch_ohlcv(ticker, market, days=30)` | Pass | `backend/services/screener_data_service.py` |
| US tickers: Alpaca primary; Yahoo Finance fallback | Pass | `fetch_ohlcv()` calls `get_ohlcv_bars()` first, falls back on None/empty |
| UK tickers (.L suffix): Yahoo Finance only | Pass | `market == "UK"` skips Alpaca entirely |
| Pence→GBP conversion (currency=GBp ÷ 100) | Pass | `_yahoo_fetch_ohlcv()` — `scale = 100.0 if pence else 1.0` |
| Returns normalised OHLCVRecord: date, open, high, low, close, volume | Pass | `_alpaca_bars_to_ohlcv()` and `_yahoo_fetch_ohlcv()` both emit this schema |
| Returns None on all-source failure | Pass | Both paths return None on error |
| All external calls mockable via BLG-QA-08 | Pass | `get_ohlcv_bars` patched in tests; Yahoo via `_yahoo_fetch_ohlcv` patch |
| Unit tests covering all paths | Pass | `tests/test_screener_data_service.py` — 9 tests, all pass |

---

## ST-03 — ATR + Regime Detection + Signal Scoring Engine

**Commit:** `[EPIC-01][ST-03]` on branch `exec/2026-04-25__release-v3.0/EPIC-01`

| AC | Status | Evidence |
|----|--------|----------|
| `screener_engine.py`: `compute_screener_result(ticker, market, ohlcv_data, ...)` | Pass | `backend/services/screener_engine.py` |
| ATR: 14-period Wilder's ATR; returns float | Pass | `compute_atr()` — seeded average + Wilder smoothing |
| Regime gate: `risk_off` → exclusion (returns None) | Pass | Gate 1 in `compute_screener_result()` |
| Data gate: minimum 15 bars (ATR_PERIOD + 1) | Pass | Gate 2 in `compute_screener_result()` |
| ATR gate: ATR < 0.5% of price → exclusion | Pass | Gate 3 (`MIN_ATR_PCT = 0.005`) |
| Signal score: RSI (40%) + MACD histogram (40%) + volume surge (20%); 0.0–1.0 | Pass | `compute_signal_score()` — 3 components normalised and capped |
| Signal gate: score < 0.25 → exclusion | Pass | Gate 4 (`MIN_SIGNAL_SCORE = 0.25`) |
| Returns ScreenerResultRecord with all schema fields when passing | Pass | 19-field dict per `screener_results_schema.md §1.1` |
| Results deterministic for given OHLCV input | Pass | `test_atr_is_deterministic`, `test_signal_score_deterministic` |
| BLG-QA-09 test data used (no live API calls) | Pass | Fixtures loaded from `tests/mock_harness/fixtures/` |
| Unit tests: ATR correctness, regime gate, signal bounds, data gate | Pass | `tests/test_screener_engine.py` — 16 tests, all pass |

---

## ST-04 — Screener Batch Engine + API Endpoints

**Commit:** `[EPIC-01][ST-04]` on branch `exec/2026-04-25__release-v3.0/EPIC-01`

| AC | Status | Evidence |
|----|--------|----------|
| `screener_batch_service.py`: `run_screener()` loops all active tickers, persists results | Pass | `backend/services/screener_batch_service.py` |
| `screener_results` table with all required columns + JSONB news_headlines | Pass | `ensure_screener_results_table()` DDL |
| `GET /screener/results`: latest run results; market/run_id filter; pagination | Pass | `backend/routers/screener.py` — `screener_results()` |
| `GET /screener/results`: 404 if no runs; 400 if limit > 200 | Pass | `get_screener_results()` raises ValueError; router maps 404/400 |
| `POST /screener/run`: triggers run; returns run_id | Pass | `trigger_screener_run()` → 202 with run_id |
| `POST /screener/run`: 409 if run in progress | Pass | `RuntimeError("RUN_IN_PROGRESS")` → HTTP 409 |
| Both endpoints registered in test suite | Pass | Lines 113–115 of `backend/routers/test.py` (35 total) |
| `SystemStatus.js` fallback updated (33→35) | Pass | Line 533 updated to `'35'` |
| Integration test with BLG-QA-08 mock harness | Pass | `tests/test_screener_batch_service.py` — 9 tests, all pass |
| UK tickers routed to FTSE regime | Pass | `test_run_screener_routes_uk_ticker_to_uk_regime` |

---

## Consolidation Summary

| Story | AC Count | Pass | Fail | Notes |
|-------|----------|------|------|-------|
| ST-01 | 10 | 10 | 0 | — |
| ST-02 | 8 | 8 | 0 | — |
| ST-03 | 11 | 11 | 0 | — |
| ST-04 | 10 | 10 | 0 | Sprint 1 gate deliverable ✅ |
| **Total** | **39** | **39** | **0** | — |

**Test count:** 45 new tests (11 + 9 + 16 + 9); all pass. Pre-existing test_alpaca_integration.py ordering failures (6) confirmed pre-existing — not introduced by EPIC-01.
