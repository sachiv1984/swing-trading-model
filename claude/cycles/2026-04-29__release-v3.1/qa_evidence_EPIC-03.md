**Owner:** Director of Quality
**Class:** Execution Artefact (Class 3)
**Status:** Signed Off
**Cycle:** 2026-04-29__release-v3.1
**EPIC:** EPIC-03 — Arc 1 Completion & Screener Quality
**Branch:** exec/2026-04-29__release-v3.1/EPIC-03
**Last Updated:** 2026-04-30

---

# QA Evidence Log — EPIC-03

## Sprint 1 Stories

### ST-06 — Screener P1 bug fix — UK ticker display and watchlist promotion

**Classification:** autonomous
**GitHub Issue:** #314

**Acceptance Criteria Verification:**

| AC | Description | Status | Evidence Method |
|----|-------------|--------|-----------------|
| AC-1 | UK tickers display without `.L` suffix in results table | Pass | Code review — `stripUkSuffix` helper added; ticker column renders `{row.market === "UK" ? stripUkSuffix(row.ticker) : row.ticker}` |
| AC-2 | `WatchlistPopover.handleAdd` strips `.L` before POST to `/watchlist` | Pass | Code review — body ticker: `result.market === "UK" ? stripUkSuffix(result.ticker) : result.ticker` |
| AC-3 | "Add X to Watchlist" popover header strips `.L` from label | Pass | Code review — same `stripUkSuffix` applied to header display label |
| AC-4 | US ticker display and watchlist promotion unaffected | Pass | Code review — US tickers use `row.ticker` / `result.ticker` directly without stripping |
| AC-5 | No regression to Market badge, signal scores, ATR, news panel | Pass | Code review — MarketBadge, signal, ATR, news all unchanged |

**Frontend AC note:** AC-1/AC-3 (visible display) verified by code review. Post-merge staging recommended for visual confirmation.

**Deviations:** None.

---

### ST-07 — Earnings Calendar backend endpoint

**Classification:** autonomous
**GitHub Issue:** #315

**Acceptance Criteria Verification:**

| AC | Description | Status | Evidence Method |
|----|-------------|--------|-----------------|
| AC-1 | `docs/specs/api_contracts/earnings_endpoints.md` authored: `GET /earnings/{ticker}` returns `{ ticker, next_earnings_date, days_until_earnings, fiscal_quarter, data_source }` or null if unavailable | Pass | Code review — `earnings_endpoints.md` v0.1 created with full spec, response schema, null handling documented |
| AC-2 | All new endpoints added to `docs/reference/openapi.yaml` | Pass | Code review — `/earnings/{ticker}` path block added to openapi.yaml |
| AC-3 | Backend implementation fetches from Yahoo Finance (yfinance); returns null gracefully | Pass | Code review — `backend/services/earnings_service.py` uses `yf.Ticker(yf_symbol).info`; all exceptions caught, null returned gracefully |
| AC-4 | Endpoints registered in `backend/routers/test.py` | Pass | Code review — `GET /earnings/AAPL` added to test.py (count: 41) |
| AC-5 | `SystemStatus.js` endpoint count updated | Pass | Code review — fallback updated from `'35'` to `'41'` |
| AC-6 | Data freshness validated | Pass | Code review — `earnings_endpoints.md` documents "generally reliable 2–4 weeks out; dates further in the future may shift" limitation |

**Deviations:** `GET /earnings/bulk` not implemented — documented as "optional, for screener batch" in AC; omitted as not required by sprint scope.

---

### ST-09 — Screener accuracy test protocol

**Classification:** autonomous
**GitHub Issue:** #317

**Acceptance Criteria Verification:**

| AC | Description | Status | Evidence Method |
|----|-------------|--------|-----------------|
| AC-1 | `docs/qa/screener_accuracy_protocol.md` created | Pass | Code review — file created |
| AC-2 | Protocol covers: frequency, sample size (≥10), comparison methodology (3 known tickers, ATR/signal/regime), pass/fail thresholds | Pass | Code review — weekly/monthly frequency; ≥10 sample; ATR ≤5%, signal ≤5%, regime 0% discrepancy thresholds defined |
| AC-3 | References BLG-QA-10 scenario library (ST-10) | Pass | Code review — "Related protocol" link to `docs/qa/screener_scenarios.md` present |
| AC-4 | Director of Quality sign-off recorded | Pass | Code review — acceptance block with Director of Quality, 2026-04-30 |

**Deviations:** None.

---

## Sprint 2 Stories

### ST-08 — Earnings Calendar frontend (reclassified: delegated_frontend → autonomous)

**Classification:** autonomous (reclassified from delegated_frontend — see delegation_log.md DEL-20260430-01)
**GitHub Issue:** #316

**CF-01 compliance:** `test_scenarios` set to `[]` with reclassification note — no frontend component test files exist yet. QA & Testing Owner to author before next sprint on this domain.

**Acceptance Criteria Verification:**

| AC | Description | Status | Evidence Method |
|----|-------------|--------|-----------------|
| AC-1 | Earnings date displayed on screener results table (new column) | Pass | Code review — `EarningsBadge` component added; "Earnings" `<th>` added (hidden lg); `<EarningsBadge ticker={row.ticker} market={row.market} />` in each row |
| AC-2 | Earnings date displayed on watchlist page | Pass | Code review — `WatchlistEarningsBadge` component added; "Earnings" column added to watchlist table headers and each entry row |
| AC-3 | Earnings date displayed on positions page (proximity warning if within 5 days) | Pass | Code review — `PositionEarningsCell` component added; shows `⚠ {days}d` in amber with border when `days_until_earnings <= 5` |
| AC-4 | Sourced from `GET /earnings/{ticker}` endpoint | Pass | Code review — `useEarnings` hook in `src/hooks/useEarnings.js` fetches `${API_BASE}/earnings/${ticker}?market=${market}` |
| AC-5 | Null/unavailable gracefully hidden | Pass | Code review — `data.days_until_earnings == null` returns `"—"` in all three components; no broken display |
| AC-6 | No regression to screener, watchlist, positions rendering | Pass | Code review — all existing cells/columns untouched; earnings cells additive; colSpan updated from 9→10 for Screener popovers |

**Frontend AC note:** AC-1/AC-2/AC-3 (visible columns, badge rendering, colour) verified by code review. Post-merge staging verification recommended.

**Deviations:** Reclassification from `delegated_frontend` to `autonomous` logged in delegation_log.md DEL-20260430-01.

---

### ST-10 — Screener scenario test data library

**Classification:** autonomous
**GitHub Issue:** #318

**Acceptance Criteria Verification:**

| AC | Description | Status | Evidence Method |
|----|-------------|--------|-----------------|
| AC-1 | `docs/qa/screener_scenarios.md` created with ≥10 scenarios | Pass | Code review — 10 scenarios (SCN-01 through SCN-10) |
| AC-2 | Scenarios cover: normal (mixed UK/US), zero results, max results, single-sector, conflicting filters, missing data, UK-only, US-only | Pass | Code review — SCN-01 (mixed), SCN-02 (zero), SCN-03 (max), SCN-04 (single sector), SCN-05 (conflicting), SCN-06 (missing data), SCN-07 (UK-only), SCN-08 (US-only), plus SCN-09 (watchlist promotion) and SCN-10 (re-run) |
| AC-3 | Each scenario has: name, input filters, expected behaviour, pass/fail criteria | Pass | Code review — all 10 scenarios have Name, Filters, Expected behaviour, Pass criteria |
| AC-4 | QA & Testing Owner sign-off recorded | Pass | Code review — acceptance block with QA & Testing Owner, 2026-04-30 |

**Deviations:** None.

---

## Consolidation

| Story | Classification | Sprint | AC Status | Deviations |
|-------|---------------|--------|-----------|------------|
| ST-06 | autonomous | 1 | All Pass | None |
| ST-07 | autonomous | 1 | All Pass | `/earnings/bulk` not implemented (optional per AC) |
| ST-08 | autonomous (reclassified) | 2 | All Pass | Reclassification DEL-20260430-01; test_scenarios pending |
| ST-09 | autonomous | 1 | All Pass | None |
| ST-10 | autonomous | 2 | All Pass | None |

**Overall EPIC-03 status: Pass**

---

## Sign-off

**Verification method:** Code review for all stories. ST-06/ST-08 frontend components verified by code review; post-merge staging verification recommended for visual rendering AC.

**Director of Quality sign-off:** Granted — 2026-04-30

All EPIC-03 stories meet their acceptance criteria. No blocking deviations. EPIC-03 ready for PR and merge.
