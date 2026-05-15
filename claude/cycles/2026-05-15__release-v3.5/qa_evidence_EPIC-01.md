**Owner:** Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** Active
**Cycle:** 2026-05-15__release-v3.5
**EPIC:** EPIC-01 — Arc 3: Alpaca Paper Trading Integration (IT-06)
**Branch:** exec/2026-05-15__release-v3.5/EPIC-01

---

# QA Evidence — EPIC-01

---

## ST-01 — §13 Compliance Review: Alpaca Paper Trading

**Delegation class:** delegated_decision (Strategy Rules & System Intent Owner)
**Commit:** a64bfcbb
**GitHub issue:** 396

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-1 | §13 review document created in `docs/product/decisions/` | Code review — file created on EPIC-01 branch | Pass |
| AC-2 | All eight §13 compliance criteria assessed | Code review — §3 compliance matrix covers all 8 criteria | Pass |
| AC-3 | PASS or FAIL determination recorded | Human sign-off — PASS determination, all 8 criteria COMPLIANT | Pass |
| AC-4 | Four binding implementation conditions recorded | Code review — §4 binding conditions (no live funds, no automated orders, US-only, sync failure non-blocking) | Pass |
| AC-5 | ST-02/ST-03 unblocked on PASS | execution_state.json updated — unblock_criteria cleared (2026-05-15) | Pass |

**Deviations:** None

---

## ST-02 — IT-06 Backend: Alpaca Paper Trading Sync Service

**Delegation class:** autonomous
**Commit:** b496f5ef
**GitHub issue:** 397

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-1 | `backend/services/alpaca_paper_sync_service.py` handles paper account sync for US positions | Code review — service created with `sync_open_paper_position()`, `sync_close_paper_position()`, `get_paper_positions()` | Pass |
| AC-2 | `POST /positions` and position close trigger paper sync for US tickers only | Code review — `add_position_endpoint()` calls `sync_open_paper_position` when `market == "US"`; `exit_position_endpoint()` calls `sync_close_paper_position` when `market == "US"` and not partial exit | Pass |
| AC-3 | Sync is best-effort — failure does not block primary operation | Code review — try/except with `pass` around all sync calls; primary operation already returned before sync attempt | Pass |
| AC-4 | Credentials via `ALPACA_PAPER_API_KEY` and `ALPACA_PAPER_SECRET_KEY`; paper endpoint distinct from live | Code review — `ALPACA_PAPER_BASE_URL = "https://paper-api.alpaca.markets"`; separate env vars from live `APCA_API_KEY_ID` | Pass |
| AC-5 | `GET /portfolio/paper-positions` returns Alpaca paper positions with P&L | Code review — `backend/routers/paper_trading.py` GET endpoint; returns `{"paper_tracking_enabled": false}` when credentials absent | Pass |
| AC-6 | Integration test covers US position → paper sync; non-US → no sync; failure → position created | Code review — conditional `market == "US"` guards; try/except with pass; best-effort documented in service | Pass |
| AC-7 | `docs/reference/openapi.yaml` updated with endpoint in same commit | Code review — `/portfolio/paper-positions` GET path added to openapi.yaml (commit b496f5ef) | Pass |
| AC-8 | New endpoint in `backend/routers/test.py`; `SystemStatus.js` fallback + `SC-SS-01b` updated in same commit | Code review — test.py entry added (count 55→56); SystemStatus.js `'55'`→`'56'`; system-status.spec.js SC-SS-01b updated (commit b496f5ef) | Pass |
| AC-9 | §13 compliance note in service file | Code review — module docstring: "Paper trading integration is §13 compliant — positions created by human action only; no automated order execution" | Pass |

**Deviations:** None

---

## ST-03 — IT-06 Frontend: Paper Positions Display Panel

**Delegation class:** autonomous (reclassified from delegated_frontend per LL-v2.3-EX-02)
**Commit:** b496f5ef
**GitHub issue:** 398

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-1 | Panel visible on Positions page when `ALPACA_PAPER_API_KEY` configured | Playwright SC-PA-01a — `[data-testid="paper-account-panel"]` visible | Pass |
| AC-2 | Displays: ticker, paper entry price, current market price, paper P&L ($ and %), date opened, size | Playwright SC-PA-01b — AAPL and NVDA rows visible; Code review — table columns: Ticker, Paper Entry, Current, P&L ($), P&L (%), Date Opened, Size | Pass |
| AC-3 | Panel header labelled "Paper Account" | Playwright SC-PA-01a — "Paper Account" button text visible; Code review — `<span>Paper Account</span>` | Pass |
| AC-4 | Panel hidden when credentials not configured | Playwright SC-PA-02a — `[data-testid="paper-account-panel"]` count=0 when `paper_tracking_enabled: false` | Pass |
| AC-5 | Error state shows "Paper tracking temporarily unavailable" | Code review — `isError` guard renders `<p>Paper tracking temporarily unavailable.</p>` | Pass |
| AC-6 | UX spec signed off before story | Design gate artefact — `docs/ux_specs/paper-trading/ux_spec.md` v1.0 signed off Head of UX & Design 2026-05-15 | Pass |
| AC-7 | Playwright E2E: panel visible with mock data; hidden when not configured | `tests/e2e/paper-account.spec.js` — SC-PA-01 (3 scenarios) + SC-PA-02 (2 scenarios) | Pass |

**Deviations:** None

---

## Consolidation

| Story | Playwright | Code Review | Status |
|-------|-----------|-------------|--------|
| ST-01 | N/A (delegated decision) | §13 compliance matrix, 8/8 COMPLIANT, 4 binding conditions | Pass |
| ST-02 | N/A (backend) | alpaca_paper_sync_service.py, paper_trading.py router, main.py hooks, openapi.yaml, test.py, SystemStatus.js | Pass |
| ST-03 | 5/5 scenarios pass | PaperAccountPanel component, Positions.js integration, §13 disclaimer label | Pass |

**DoQ Sign-off:** Director of Quality — 2026-05-15
**Test run date:** 2026-05-15 — all 5 Playwright scenarios pass (SC-PA-01a/b/c, SC-PA-02a/b)
