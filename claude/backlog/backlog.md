# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-05-21 (session — 1 new item added: BLG-GOV-25)
**Last rebalance:** 2026-05-15 (cycle 2026-05-15__scheduled — DL-029 backlog add × 1 BLG-QA-19)

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

> 📋 Placement Rule
> New items must be appended to the correct existing type section (§1–§8). Do not create new numbered session sections. The backlog is organised by type, not by session date.
> **Ephemeral sections** (Release Slice tables, Test Scenario Gap sections, and "Returned to Backlog" sections appended by governance engines) are temporary. They must be removed during the next `groom backlog` run after the cycle closes. Any still-open items within them must be promoted to the appropriate §1–§8 type section before the ephemeral section is removed.

*Completed and killed items are recorded in `claude/backlog/backlog_archive.md`.*

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

*BLG-TECH-05 deferred to §9 (DL-023, 2026-04-24).*

---

### BLG-TECH-10 — Fix Yahoo Finance crumb/401 rate-limiting in screener batch
**Priority:** P1 (High)
**Type:** Platform / Technical Debt
**Owner:** Head of Backend Engineering
**Source:** Screener render log analysis — 2026-05-20
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.9

**Problem**
The screener batch service makes concurrent OHLCV requests to Yahoo Finance. Under load, YF returns heavy 401 "Invalid Crumb" and "User is unable to access this feature" errors, causing the majority of US tickers to fail data fetch in a single run. This silently produces degraded screener results — only the tickers whose requests happened to succeed appear. The root cause is that the crumb auth token expires and is not refreshed between requests, and concurrent request volume exceeds YF's tolerance.

**Scope**
- Implement crumb refresh logic: detect 401 responses and re-fetch the crumb before retrying
- Add per-request exponential backoff with jitter on 401/429 responses
- Cap concurrent YF requests to a safe limit (e.g. 5 in-flight at a time)
- Log crumb refresh events and consecutive failure counts for observability

**Acceptance Criteria**
- Screener run against full ticker universe completes without >5% OHLCV failures under normal YF conditions
- A 401 response triggers a crumb refresh and one retry before marking the ticker as failed
- Concurrent request cap is configurable via environment variable
- Crumb refresh events visible in backend logs

---

## 2. Product Feature Backlog (User-Facing)

---

*BLG-FEAT-18 (Consecutive losing streak metric) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-FEAT-19 (Monthly P&L summary report) — ✅ COMPLETE v3.1 — archived to backlog_archive.md 2026-05-05*

---

### BLG-FEAT-20 — Net-of-costs performance tracking
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260321-02 — promoted cycle 2026-05-05__scheduled (DL-024)
**Effort:** M (~2–3 days)
**Provisional-Target:** Arc 3/4 context (deliver alongside Arc 3 or Arc 4 data model work — not a standalone sprint item)

**Problem**
Performance metrics (R-multiple, win rate, expectancy) use gross P&L figures. When evaluating edge in Arc 4/6, R-multiples that ignore transaction costs overstate performance and may mask a genuinely unprofitable strategy. The Fee Drag % metric (v2.4) surfaces aggregate cost impact but per-trade R-multiples remain gross.

**Scope**
- Add brokerage cost fields per trade (commission, spread cost in GBP) — optional capture, not mandatory
- Recalculate R-multiple as net-of-costs where cost data is present
- Surface net-of-costs vs gross R-multiple on trade records and performance reports
- Sequence alongside Arc 3/4 data model work to avoid standalone migration overhead

**Acceptance Criteria**
- Brokerage cost fields capturable per trade (optional — not all trades will have explicit cost data)
- Net-of-costs R-multiple calculated and displayed where cost data exists
- Performance report breakdowns show gross vs net comparison where material
- No impact to existing R-multiple calculations where cost data is absent

---

*BLG-FEAT-21 (Trade plan abandonment status field) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FEAT-23 (Setup type classification field on trade plans) — ✅ COMPLETE v3.8 — ST-06, cycle: 2026-05-19__release-v3.8 — archived to backlog_archive.md 2026-05-21*

---

*BLG-FEAT-24 (AI-assisted setup thesis generation) — ✅ COMPLETE v3.8 — ST-08, cycle: 2026-05-19__release-v3.8 — archived to backlog_archive.md 2026-05-21*

---

*BLG-FEAT-22 (Ticker Universe Management page) — ✅ COMPLETE v3.8 — ST-09, cycle: 2026-05-19__release-v3.8 — archived to backlog_archive.md 2026-05-21*

---

### BLG-FEAT-25 — PT-04 Setup Quality Score (backend + frontend)
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Head of Backend Engineering; Metrics & Analytics Owner; Head of UX & Design
**Source:** Arc 2 roadmap — deferred from v3.8 (ST-04/ST-05, EPIC-02) — gate not met 2026-05-19: < 20 closed trades. Traceability entry added by delivery verification engine 2026-05-20.
**Effort:** L (~2–4 days, backend + frontend)
**Provisional-Target:** v3.9 (conditional — 20+ closed trades gate must be confirmed by Product Owner before sprint planning seals)

**Problem**
A deterministic setup quality score (0–100) based on own trade history cannot be computed until sufficient closed trades exist. When the user has entered with similar regime/signal/ATR conditions before, the score reflects historical win rate under those conditions. The gate condition (20+ closed trades) was not met at v3.8 sprint planning (PO confirmed 2026-05-19).

**Scope (Backend — ST-04)**
- `GET /trade-plans/setup-quality-score?ticker={ticker}` endpoint
- Score (0–100) computed from closed trade history matching current regime/signal/ATR conditions
- Gate response: `{"gate_not_met": true, "min_trades_required": 20}` when fewer than 20 closed trades
- Score factors: matching_trades count, win_rate, average_R, score_explanation
- Endpoint registered in backend/routers/test.py and openapi.yaml

**Scope (Frontend — ST-05)**
- Setup Quality Score displayed in Pre-Trade Research View and Trade Plan form
- Score badge with numeric value (0–100) and qualitative label (Excellent/Good/Fair/Low)
- "Insufficient trade history (< 20 trades)" message when gate not met
- Tooltip/expandable: matching_trades, win_rate, average_R

**Acceptance Criteria**
- Backend: endpoint implemented, gate enforced, unit tests cover gate_not_met, gate_met mixed, perfect history
- Frontend: score renders in Pre-Trade Research View and Trade Plan form; gate-not-met state clearly displayed; score updates when ticker changes
- Playwright: score renders; gate-not-met message renders; score updates on ticker change

---

## 3. Frontend & UX Backlog

---

*BLG-FE-16 (React component inventory) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*


---

*BLG-FE-19 (Keyboard shortcuts) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*
*BLG-FE-18 (Screener news panel attachment) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-FE-21 (Design system document) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

*BLG-FE-31 (Research view component library) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-22 (Screener morning routine UX spec) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-23 (Research page UK ticker suffix not stripped) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-24 (Negative earnings days display for past earnings dates) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-25 (Signals page: default to most recent day's signals) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-26 (Research page UX review: regime lozenge and font consistency) — ✅ COMPLETE v3.6 — archived to backlog_archive.md 2026-05-17*

---

### BLG-FE-27 — Nav bar redesign exploration
**Priority:** P3 (Low)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design
**Source:** v3.2 delivery verification — user feedback 2026-05-06
**Effort:** M (~1–2 days design + spec)
**Provisional-Target:** Arc 3 (design exploration — not urgent; no current blocking workflow)

**Problem**
The current nav bar occupies a fixed portion of the visible screen area. As the application grows in Arc 2 and beyond, the navigation structure may benefit from a redesign to reclaim vertical space. Options to evaluate: Sticky/Fixed Header (current pattern, optimised), mega menu (grouped sections), or breadcrumb navigation (context-sensitive, minimal footprint).

**Scope**
- Head of UX & Design to evaluate the three navigation patterns in the context of current and Arc 2 page inventory
- Produce a design recommendation with rationale (no implementation required at this stage)
- If redesign is recommended, produce a UX spec and create a follow-on implementation backlog item

**Acceptance Criteria**
- Design recommendation document produced (one of: maintain current, redesign to pattern X)
- Rationale covers: screen real-estate impact, mobile responsiveness, Arc 2 page count
- If redesign: UX spec produced and implementation backlog item filed

---

*BLG-FE-28 (Pre-Trade Research View UX spec) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-FE-29 (Watchlist research status indicator) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-30 (Trade plan status badges) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-34 (Trade plan form signal context panel — SignalContextPanel.js with entry_rationale/confirmation pre-population) — ✅ COMPLETE v3.7 — ST-03, cycle: 2026-05-18__release-v3.7*

---

*BLG-FE-33 (Signals page Add to Watchlist CTA — watchlisted status backend + SignalCard CTA replacement) — ✅ COMPLETE v3.7 — ST-01 + ST-02, cycle: 2026-05-18__release-v3.7*

---

*BLG-FE-32 (Research view SC-RV-18/SC-RV-19 Playwright coverage) — ✅ COMPLETE v3.6 — archived to backlog_archive.md 2026-05-17*

---

*BLG-FE-35 (ST-08 AC-02: Research page font conformance staging) — ✅ COMPLETE v3.7 — staging run performed 2026-05-18 (Head of UX & Design); conformant; Playwright SC-RV-TYP-01 added for CI regression; archived to backlog_archive.md 2026-05-18*

---

*BLG-FE-36 (Add news context panel to trade plan form) — ✅ COMPLETE v3.8 — ST-07, cycle: 2026-05-19__release-v3.8 — archived to backlog_archive.md 2026-05-21*

---

### BLG-FE-37 — Strip .L suffix from Ticker Universe page display labels
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** Post-sprint QA observation — 2026-05-20
**Effort:** XS (<1h)
**Provisional-Target:** v3.9

**Problem**
The Ticker Universe page displays LSE ticker symbols with the `.L` suffix (e.g. `BATS.L`) because that is how they are stored in the database for identification. This is correct internally but looks unpolished to users — LSE tickers are conventionally displayed without the suffix in UI contexts (e.g. `BATS`). The suffix is meaningful to data sources but irrelevant to a trader reading the page.

**Scope**
- In `TickerUniverse.js`, strip `.L` from the displayed ticker label (not from the underlying value used for API calls)
- DB storage and API payloads remain unchanged

**Acceptance Criteria**
- LSE tickers on the Ticker Universe page display without `.L` suffix
- Ticker symbol sent in API requests (add, delete, toggle) is unchanged (still includes `.L`)
- US tickers are unaffected

---

### BLG-FE-38 — Add degraded-run warning to screener when OHLCV failure rate exceeds 20%
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Head of Backend Engineering; Head of UX & Design
**Source:** Screener render log analysis — 2026-05-20
**Effort:** S (~0.5 days)
**Provisional-Target:** v3.9

**Problem**
When Yahoo Finance rate-limits during a screener run, the majority of US tickers fail OHLCV fetch silently. The screener returns results with no indication that coverage was degraded — a trader sees UK-only or partial results and may act on them without realising most of the universe was excluded. There is currently no way to distinguish a clean full-coverage run from a heavily degraded one.

**Scope**
- In the screener batch service, calculate `ohlcv_failure_rate = failed_tickers / total_tickers` at run completion
- If `ohlcv_failure_rate > 0.20`, set `degraded_run: true` and `failure_rate: <float>` on the screener run record
- Expose `degraded_run` and `failure_rate` in `GET /screener/results` response
- In the screener frontend, display a visible warning banner when `degraded_run` is true: "Results may be incomplete — {N}% of tickers failed data fetch"

**Acceptance Criteria**
- `degraded_run: true` is set on any screener run where >20% of tickers returned no OHLCV data
- `GET /screener/results` response includes `degraded_run` boolean and `failure_rate` float
- Screener results page shows a warning banner when `degraded_run` is true, citing the failure rate
- Clean runs (failure rate ≤20%) show no banner

---

## 4. Backend & Data Backlog


---

*BLG-AI-02 (Model version contract for AI Journal) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-AI-03 (AI Journal Summarisation quarterly review cadence) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

### BLG-BE-10 — Fix sector/industry data dropped in screener batch
**Priority:** P1 (High)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** Post-sprint QA observation — 2026-05-20
**Effort:** XS (<1h)
**Provisional-Target:** v3.9

**Problem**
`screener_batch_service.py` fetches full ticker records from `ticker_universe` (including `sector` and `industry`) but immediately extracts only the ticker string into a list, silently discarding the sector/industry fields. These fields are never passed to `compute_screener_result()`, so screener results are stored with NULL sector and industry for every ticker. Sector/industry-based filtering and display in screener results is therefore always empty.

**Scope**
- In `screener_batch_service.py`, retain the full ticker dict instead of extracting the ticker string only
- Pass `sector` and `industry` from the ticker record when calling `compute_screener_result()`
- Verify screener results now persist non-null sector/industry for tickers that have this data in `ticker_universe`

**Acceptance Criteria**
- Screener results for tickers with sector/industry in `ticker_universe` have non-null sector and industry values
- No change to screener result schema or API contract

---

### BLG-BE-11 — Remove DAY from ticker universe (invalid Yahoo Finance symbol)
**Priority:** P2 (Medium)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** Screener render log — Yahoo Finance 404 for DAY (range=30d) — 2026-05-20
**Effort:** XS (<1h)
**Provisional-Target:** v3.9

**Problem**
The ticker `DAY` (Dayforce Inc., formerly Ceridian) is in `tickers_full_list.csv` and is synced into `ticker_universe` as active. Yahoo Finance returns HTTP 404 for `DAY` on historical data requests (30d range), meaning it consistently fails OHLCV fetch on every screener run, wasting processing time and appearing in the active ticker list despite producing no usable data. Also investigate whether `PHNX.L` is a permanent YF 404 or a transient issue.

**Scope**
- Remove `DAY` from `backend/tickers_full_list.csv`
- Deactivate or delete `DAY` from the `ticker_universe` table via migration or startup cleanup
- Investigate the correct YF symbol for Dayforce Inc. and add back if a valid symbol exists
- Confirm `PHNX.L` status — if consistently 404, apply same treatment

**Acceptance Criteria**
- `DAY` no longer appears in `ticker_universe` active tickers
- No `OHLCV FAILED for DAY` log entries on screener runs
- `tickers_full_list.csv` does not contain `DAY`

---

### BLG-BE-12 — Add company_name column to ticker universe
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering; Head of UX & Design
**Source:** Post-sprint QA observation — 2026-05-20
**Effort:** S (~0.5 days)
**Provisional-Target:** v3.9

**Problem**
The `ticker_universe` table stores only ticker symbol, market, sector, industry, and active status — no company name. `tickers_full_list.csv` already contains company names (e.g. `HOLX,NASDAQ,Hologic`), so the data is available at source. The Ticker Universe management page therefore shows only bare ticker symbols with no human-readable company name, making the list harder to scan for non-technical users.

**Scope**
- Add `company_name TEXT` column to `ticker_universe` table via `ensure_company_name_column()` in `ticker_universe_service.py`
- Backfill `company_name` from `tickers_full_list.csv` for all existing rows on startup
- Populate `company_name` from CSV when syncing new tickers
- Include `company_name` in `GET /ticker-universe` response
- Display company name alongside ticker symbol on the Ticker Universe page

**Acceptance Criteria**
- `ticker_universe` rows have non-null `company_name` for all tickers present in the CSV
- `GET /ticker-universe` response includes `company_name` field
- Ticker Universe page shows company name next to each ticker symbol

---

## 5. QA & Test Automation Backlog

---

*BLG-QA-18 (Screener accuracy test protocol) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-QA-14 (Author Playwright E2E test suite for entry checklist) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*TEST-GAP-ST14 (AI audit service unit tests) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-QA-15 (PT-02 research view acceptance test protocol) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-QA-16 (Research endpoint integration test coverage) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-QA-17 (Research view test scenario library) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*TEST-GAP-EPIC-03-v33 (SC-RV-18 and SC-RV-19 Playwright coverage) — ✅ COMPLETE v3.6 — archived to backlog_archive.md 2026-05-17*

---

*BLG-QA-19 (Research view regression test protocol) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-QA-20 (Consolidate database stub files into shared pytest conftest fixture — session-scoped stub) — ✅ COMPLETE v3.7 — ST-09, cycle: 2026-05-18__release-v3.7*

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add new v2.8/v2.9/v3.0/v3.4 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 (3 endpoints); v3.0 post-ship closure 2026-04-28 OA-v30-01 (5 additional endpoints); v3.1 post-ship closure 2026-05-05 (10 additional endpoints); v3.4 post-ship closure 2026-05-14 (2 additional endpoints); v3.5 post-ship closure 2026-05-15 (2 additional endpoints)
**Effort:** M (~2 days — 22 endpoints total)
**Provisional-Target:** Before next performance baseline review

**Problem**
Twenty-two endpoints shipped in v2.8/v2.9/v3.0/v3.1/v3.4/v3.5 are absent from `docs/ops/api_performance_baseline.md`. Performance re-runs require a live environment and human coordination — baseline updates cannot be automated.

**Scope (updated 2026-05-15):**
- v2.8/v2.9 endpoints (3): `POST /ai/journal-summary`, `GET /ai/journal-summary/history`, `GET /v1beta1/news`
- v3.0 endpoints (5): `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}`, `GET /screener/results`, `POST /screener/run`
- v3.1 endpoints (10): `POST /trade-plans`, `GET /trade-plans/{id}`, `PUT /trade-plans/{id}`, `DELETE /trade-plans/{id}`, `GET /trade-plans/by-position/{position_id}`, `GET /trade-plans/by-ticker/{ticker}`, `GET /research/{ticker}`, `GET /earnings/{ticker}`, `GET /reports/monthly-pnl`, plus any additional v3.1 routes
- v3.4 endpoints (2): `GET /portfolio/drawdown-status`, `GET /portfolio/concentration-status`
- v3.5 endpoints (2): `GET /portfolio/paper-positions`, `GET /trades/{trade_id}/plan-vs-reality`
- Run each against staging to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- All 22 endpoints have p50 and p95 latency entries in the baseline document
- Entries consistent with existing baseline measurement methodology

---

*BLG-OPS-14 (AI Journal monitoring metrics) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*
*BLG-OPS-12 (External API health check extension) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-OPS-15 (Research endpoint latency monitoring) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-OPS-16 (Remove tracked backend/__pycache__ files from git + .gitignore) — ✅ COMPLETE v3.7 — ST-10, cycle: 2026-05-18__release-v3.7*

---

*BLG-SEC-06 (Trade plan data sensitivity classification) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SEC-05 (Alpaca API key rotation policy and credential audit) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

## 7. Spec Debt Backlog

*BLG-SPEC-20 deferred to §9 (DL-023, 2026-04-24).*

---

*BLG-SPEC-24 (PT-02 research view canonical spec) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SPEC-25 (PT-02 research endpoint API contract) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SPEC-26 (Research view data source provenance spec) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SPEC-27 (Research endpoint HTTP error code differentiation) — ✅ COMPLETE v3.6 — archived to backlog_archive.md 2026-05-17*

---

*BLG-SPEC-28 (Update trade_plan.md §6.2 entry checklist field references) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-SPEC-29 (Correct grace-period-alert ux_spec.md §5 dismiss storage to sessionStorage) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-SPEC-30 (Correct stop-management-workflow ux_spec.md §4.4 stop-update HTTP verb to PATCH) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-SPEC-31 (Review React Query v5 onSuccess migration impact across codebase) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

## 8. Governance Backlog

*BLG-GOV-23 (scored_initiatives.md Arc 3–6 comprehensive refresh — OA-RP-05 resolved) — ✅ COMPLETE v3.7 — ST-11, cycle: 2026-05-18__release-v3.7*

---

*BLG-GOV-24 (Add gh_issue_template.md to §14 governance table) — ✅ COMPLETE v3.8 — ST-10, cycle: 2026-05-19__release-v3.8 — archived to backlog_archive.md 2026-05-21*

---

*BLG-GOV-19 (PT-05 entry checklist §13 compliance review) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-GOV-20 (Trade plan field extension governance) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-GOV-21 (Arc 4 data requirements capture) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-GOV-22 (sprint_planning_prompt.md patch: shared execution_state.json ownership + multi-EPIC Positions.js conflict guidance) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-GOV-18 (External API dependency risk register) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

*BLG-GOV-11 (Cycle artefact inventory and maintenance review) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

### BLG-GOV-25 — Add --dry-run support to plan release and run delivery verification engines
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Audit AUD-2026-05-21-004 — 2026-05-21
**Effort:** M (~1–2d)
**Provisional-Target:** v3.9

**Problem**
`plan release` and `run delivery verification` are both absent from the §13 dry-run capability table in `shared_standards.md`. `plan release` is the highest-cost engine at approximately 8,232 tokens/run; a failed run that a dry-run could have caught wastes full context and requires a complete re-execution. `run delivery verification` cross-checks all cycle artefacts and similarly has no safe preview mode. Without dry-run support, there is no low-cost way to validate pre-conditions before committing to full engine execution.

**Scope**
- Add `--dry-run` flag handling to `release_planning_prompt.md`: validate inputs, check artefact availability, report what would be created — no writes
- Add `--dry-run` flag handling to `delivery_verification_prompt.md`: validate inputs, report which checks would run — no writes
- Add two rows to `shared_standards.md` §13 dry-run table for `plan release` and `run delivery verification`
- Bump versions on all three files per §6 governance checklist

**Acceptance Criteria**
- `plan release --version vX.Y --dry-run` exits cleanly with a preflight summary and no artefact writes
- `run delivery verification --cycle <id> --dry-run` exits cleanly with a check inventory and no artefact writes
- Both commands appear in the §13 dry-run table in `shared_standards.md`
- All three modified files have bumped version headers and `prompt_change_log.md` entries

---

## 9. Deferred / Future Candidates

- Daily email portfolio summary
- FX rate history tracking
- **BLG-TECH-05 — Prometheus metrics endpoint** (P3, M effort — permanently deferred at single-user scale; DL-023 2026-04-24)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system
- **BLG-SPEC-20 — Machine-readable spec front-matter standard** (P3, S effort — deferred; Arc 1 specs shipped without requiring this standard; DL-023 2026-04-24)

---

## 10. Explicitly Out of Scope (Product-Level)

These are deliberate product decisions, not deferrals:

- Broker API integration
- Automated trading execution
- Configurable strategy builder
- ML-based predictions
- Social / community features
- Options and futures trading support

---

## 11. Lifecycle Governance Notes

- This backlog is not canonical and must never override: strategy rules, metrics definitions, API contracts

---


