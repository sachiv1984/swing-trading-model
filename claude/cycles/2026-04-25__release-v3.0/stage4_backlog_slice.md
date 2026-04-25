Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v3.0
Cycle: 2026-04-25__release-v3.0
Last Updated: 2026-04-25

---

# Backlog Slice — v3.0 Arc 1 Remainder: Screener Engine & Results Page

**Sprint plan:** 2 sprints | **Total stories:** 16 | **EPICs:** 4

---

## EPIC-01 — Arc 1 Screener Engine

**Maps to:** S2-01 (DS-01)
**Sprint:** 1
**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Theme:** Implement the strategy-rules screener engine: ticker universe management, OHLCV data pipeline, ATR + regime + signal scoring computation, batch orchestration, and API endpoints.

**Pre-conditions:**
- BLG-SPEC-21 (screener engine spec) ✅ available
- BLG-SPEC-22 (Alpaca API contract) ✅ available
- BLG-SPEC-23 (screener internal API contract) ✅ available
- alpaca_service.py ✅ operational (v2.9)
- sector_service.py ✅ operational (v2.9)
- BLG-QA-08 mock harness ✅ operational (v2.9)
- BLG-QA-09 screener test data library ✅ available (v2.9)

---

### ST-01 — Ticker Universe Data Model + Endpoints

**EPIC:** EPIC-01 | **Sprint:** 1 | **Effort:** S | **Maps to:** S2-01

**Description:** Create the ticker universe DB schema and management endpoints. This is the foundational data layer for DS-01 — the screener engine operates on a configurable list of tickers.

**Acceptance Criteria:**
- `ticker_universe` table created: `ticker`, `market` (UK/US), `active` (bool), `sector`, `industry`, `created_at`
- DB migration script provided and runs idempotently
- `GET /ticker-universe` returns all active tickers with market and sector fields
- `POST /ticker-universe` adds a ticker (validation: market must be UK or US; ticker must be non-empty)
- `DELETE /ticker-universe/{ticker}` marks ticker inactive (soft delete)
- Default seed data: at least 5 UK (.L) and 5 US tickers from BLG-QA-09 test data library
- Endpoint registered in test suite (backend/routers/test.py); SystemStatus.js count updated
- OpenAPI spec entry added for all new endpoints (openapi.yaml)
- Unit tests covering: GET returns list, POST validates market, DELETE soft-deletes
- DoQ sign-off with Date field populated

---

### ST-02 — OHLCV Data Pipeline Service

**EPIC:** EPIC-01 | **Sprint:** 1 | **Effort:** M | **Maps to:** S2-01

**Description:** Implement the screener data pipeline service that fetches OHLCV price history for a ticker using Alpaca (US) or Yahoo Finance (UK) per BLG-SPEC-22, and stores/caches the result for use by the computation engine.

**Acceptance Criteria:**
- `screener_data_service.py` (or equivalent): `fetch_ohlcv(ticker, market, days=30)` returns price history
- US tickers: fetched via alpaca_service.py; UK tickers (.L suffix): fetched via yahoo_finance_service.py
- Returns at minimum: date, open, high, low, close, volume per BLG-SPEC-21 §3 data model
- Graceful error handling: if Alpaca unavailable, falls back to Yahoo Finance for US (per BLG-SPEC-22 §6 fallback spec); if both unavailable, returns empty result with error flag
- Rate limit compliance per BLG-SPEC-22 §4
- All external calls mockable via BLG-QA-08 mock harness in CI
- Unit tests covering: UK fetch, US fetch, Alpaca fallback, empty result on total failure
- DoQ sign-off with Date field populated

---

### ST-03 — ATR + Regime Detection + Signal Scoring Engine

**EPIC:** EPIC-01 | **Sprint:** 1 | **Effort:** M | **Maps to:** S2-01

**Description:** Implement the computation engine: ATR calculation, regime detection (trending/choppy), and signal scoring for a given ticker's OHLCV history per BLG-SPEC-21 §4–§6.

**Acceptance Criteria:**
- `screener_engine.py` (or equivalent): `compute_screener_result(ticker, ohlcv_data)` returns a `ScreenerResult` object
- ATR computation: 14-period ATR per BLG-SPEC-21 §4 formula; result in absolute and % terms
- Regime detection: EMA-based trending/choppy classification per BLG-SPEC-21 §5; returns `trending` or `choppy`
- Signal scoring: RSI, MACD, volume score per BLG-SPEC-21 §6; returns composite signal score 0–100
- Regime gate: choppy regime results in screener exclusion (signal_score = null, regime_gate = failed) per BLG-SPEC-21 §7
- Results deterministic for given OHLCV input (no randomness)
- Uses BLG-QA-09 synthetic test data for all unit tests (no live API calls in tests)
- Unit tests covering: ATR calculation correctness, trending/choppy regime detection, signal score bounds, regime gate exclusion
- DoQ sign-off with Date field populated

---

### ST-04 — Screener Batch Engine + API Endpoints

**EPIC:** EPIC-01 | **Sprint:** 1 | **Effort:** S | **Maps to:** S2-01

**Description:** Implement screener batch orchestration (loop over ticker universe, call data pipeline + engine, persist results) and expose the screener API endpoints per BLG-SPEC-23.

**Acceptance Criteria:**
- `screener_batch_service.py` (or equivalent): runs screener computation for all active tickers; persists results to `screener_results` table
- `screener_results` table: `ticker`, `market`, `atr`, `atr_pct`, `regime`, `signal_score`, `sector`, `run_timestamp`
- `GET /screener/results` returns all screener results from latest run; supports `?market=UK|US` filter per BLG-SPEC-23
- `POST /screener/run` triggers a batch run; returns `{status: "running", run_id: <id>}` or `{status: "completed", count: N}`; idempotent if run already in progress
- Both endpoints registered in test suite and openapi.yaml
- Integration test using BLG-QA-08 mock harness: POST /screener/run completes and GET /screener/results returns results
- DoQ sign-off with Date field populated

---

## EPIC-02 — Arc 1 Screener Frontend

**Maps to:** S2-02, S2-03, S2-04 (DS-02, DS-07, BLG-FE-18)
**Sprint:** 2
**Owner:** Base44 Frontend Prompt Owner
**Theme:** Implement the screener results page, watchlist promotion flow, and news panel attachment per screener_results.md.

**Pre-conditions:**
- EPIC-01 ST-04 merged to main (GET /screener/results endpoint available) ✅ (Sprint 1 deliverable)
- Design gate passed ✅ (required before Sprint 2 opens)
- screener_results.md UX spec ✅ available (v2.9 BLG-FE-17)
- BLG-GOV-16 §13 sign-off (BLG-FE-18 display-only boundary) confirmed

---

### ST-05 — Screener Results Page

**EPIC:** EPIC-02 | **Sprint:** 2 | **Effort:** M | **Maps to:** S2-02

**Description:** Implement the screener results page per screener_results.md. Main table view with all required columns, sorting, filters, regime tags, and empty/error states.

**Acceptance Criteria:**
- Screener results page accessible via `/screener` route (or per createPageUrl pattern)
- Table displays per screener_results.md §4: ticker, market, ATR (% and absolute), regime badge, signal score, sector, entry zone proximity
- Regime badge: green "Trending" / grey "Choppy" per screener_results.md §5
- Sort by signal score (default descending) per screener_results.md §6
- Market filter: UK / US / All per screener_results.md §6
- Empty state: "No screener results" with "Run screener" CTA per screener_results.md §7
- Loading state: skeleton rows while fetching per screener_results.md §8
- Error state: API error message per screener_results.md §7
- "Last updated" timestamp visible per screener_results.md §3
- Manual refresh button per screener_results.md §3
- DoQ sign-off with local run or staging evidence; frontend-visible AC requires explicit evidence method statement

---

### ST-06 — Watchlist Promotion Flow

**EPIC:** EPIC-02 | **Sprint:** 2 | **Effort:** S | **Maps to:** S2-03

**Description:** Implement one-click watchlist promotion from screener results per DS-07 / screener_results.md §10.

**Acceptance Criteria:**
- "Add to Watchlist" button visible on each screener result row per screener_results.md §10
- Clicking button: calls watchlist API (`POST /watchlist`) with ticker; shows loading indicator; shows success confirmation
- Promoted rows show "In Watchlist" indicator (greyed button or badge) per screener_results.md §10
- Already-in-watchlist tickers show "In Watchlist" state on page load (pre-populated from watchlist API)
- Error handling: if watchlist API fails, show inline error; row state not changed
- No duplicate promotions: POST /watchlist returns graceful response if ticker already in watchlist; UI reflects existing state
- DoQ sign-off with evidence of promotion flow (local run or staging)

---

### ST-07 — Screener News Panel Attachment

**EPIC:** EPIC-02 | **Sprint:** 2 | **Effort:** S | **Maps to:** S2-04

**Description:** Wire the existing `GET /news/{ticker}` backend endpoint to the screener results page news panel per screener_results.md §9 and BLG-FE-18.

**Acceptance Criteria:**
- News count badge visible on US ticker rows per screener_results.md §9 (badge shows article count; absent if 0)
- Clicking news badge: expands inline news panel below the row showing last 5 headlines per screener_results.md §9
- UK tickers (.L suffix): news column shows "—", no badge, no panel per screener_results.md §9
- Empty news state per screener_results.md §7: "No news available" inline message
- Implementation display-only per BLG-GOV-16 §13 sign-off conditions; no new data sources
- Strategy Rules Owner counter-sign required at DoQ (BLG-FE-18 display-only boundary)
- DoQ sign-off with local run evidence of panel toggle; evidence method stated explicitly (code review insufficient for toggle behaviour)

---

## EPIC-03 — Operations, Observability & Test Quality

**Maps to:** S2-05, S2-06, S2-07, S2-08
**Sprint:** 2
**Owner:** Infrastructure & Operations Owner + QA & Testing Owner
**Theme:** Health check extensions for external APIs and AI Journal, AI audit unit tests, and keyboard shortcut UX quick win.

---

### ST-08 — External API Health Check Extension

**EPIC:** EPIC-03 | **Sprint:** 2 | **Effort:** S | **Maps to:** S2-05

**Description:** Extend `GET /health` to include Alpaca and Yahoo Finance API connectivity status per BLG-OPS-12.

**Acceptance Criteria:**
- `GET /health` response includes `external_apis` section with entries for `alpaca` and `yahoo_finance`
- Each entry: `last_successful_call` (ISO timestamp or null), `error_rate` (rolling window, 0.0–1.0), `p95_latency_ms` (int or null)
- Health endpoint does not fail if external API is down — returns `"status": "degraded"` in the external API section, overall health may remain ok
- External API check uses cached/lightweight ping (not a full data fetch) — does not consume rate limit quota
- Endpoint registered in test suite (if not already); openapi.yaml updated
- Unit tests covering: healthy response, degraded response when API unreachable
- DoQ sign-off with Date field populated

---

### ST-09 — AI Journal Monitoring Metrics

**EPIC:** EPIC-03 | **Sprint:** 2 | **Effort:** S | **Maps to:** S2-06

**Description:** Extend `GET /health` to include AI Journal monitoring metrics sourced from the BLG-AI-01 audit log table per BLG-OPS-14.

**Acceptance Criteria:**
- `GET /health` response includes `ai_journal` section with: `usage_rate` (summaries/day rolling 7d, float), `error_rate` (last 24h, 0.0–1.0), `p95_latency_ms` (last 24h, int or null)
- Metrics sourced from `ai_audit_log` table (BLG-AI-01)
- Non-blocking: if AI audit data absent or table empty, `ai_journal` section returns `{"status": "unavailable"}` — health endpoint does not fail
- Unit tests covering: populated metrics, empty audit table graceful handling
- DoQ sign-off with evidence of response format (code review + response sample sufficient)

---

### ST-10 — AI Audit Service Unit Tests

**EPIC:** EPIC-03 | **Sprint:** 2 | **Effort:** S | **Maps to:** S2-07

**Description:** Add unit tests for `ai_audit_service.py` (shipped v2.9 ST-14) covering all public functions per TEST-GAP-ST14.

**Acceptance Criteria:**
- Unit tests for `ensure_ai_audit_table`: idempotency (call twice, no error), table structure confirmed
- Unit tests for `log_ai_summary_run`: happy path row insertion, exception handling on DB error (graceful failure — does not propagate exception)
- Unit tests for `query_audit_log`: filter by trade_id, filter by date range, limit parameter, empty result
- No live DB required — use mock or TestClient pattern consistent with existing test suite
- Tests pass in CI
- DoQ sign-off with Date field populated

---

### ST-11 — Keyboard Shortcuts

**EPIC:** EPIC-03 | **Sprint:** 2 | **Effort:** S | **Maps to:** S2-08

**Description:** Add keyboard shortcuts for common trading actions per BLG-FE-19.

**Acceptance Criteria:**
- 'n' key: triggers new position flow (opens new position form/modal) on applicable pages
- 'w' key: triggers add-to-watchlist on applicable pages
- 'r' key: triggers page refresh/data reload on applicable pages
- Shortcuts do not fire when focus is inside a text input, textarea, or select element
- Keyboard shortcut reference visible to user (tooltip, help overlay, or footer hint)
- Shortcuts apply to screener results page (v3.0 new page) and any existing pages where the action is available
- No changes to business logic — display-layer event handlers only
- DoQ sign-off with local run evidence; state which pages were tested

---

## EPIC-04 — Governance, Deferred Patches & Quick Wins

**Maps to:** S2-09, S2-10, S2-11, S2-12, S2-13
**Sprint:** 1
**Owner:** Head of Specs Team + PMO Lead
**Theme:** Resolve v2.9 deferred patches (execution_prompt.md §2 + §3.1.A), close OA-v29-01, deliver BLG-FEAT-18 and BLG-AI-02.

---

### ST-12 — execution_prompt.md §2 Deferred Patch

**EPIC:** EPIC-04 | **Sprint:** 1 | **Effort:** S | **Maps to:** S2-09

**Description:** Apply v2.9 Friction Item 1 deferred patch: execution_prompt.md §2 EPIC execution order advisory — nominate a single EPIC branch as execution_state.json owner at sprint planning; other branches must check for its existence before creating their own version.

**Acceptance Criteria:**
- `claude/system/execution_prompt.md` §2 updated with EPIC execution_state.json owner designation rule
- Rule states: at sprint planning, the first EPIC branch to execute is designated execution_state.json owner; all other EPIC branches must check for existence of execution_state.json before creating their copy
- Merge order advisory note added: if execution_state.json conflict arises, CLAUDE.md §8 governs resolution
- Version bumped per CLAUDE.md §6 governance file edit checklist (version bump + OPERATIONAL_GUIDE.md update + prompt_change_log.md entry)
- OPERATIONAL_GUIDE.md §8 source prompt header and §14 execution engine version updated
- prompt_change_log.md entry appended
- DoQ sign-off with Date field populated

---

### ST-13 — execution_prompt.md §3.1.A Deferred Patch

**EPIC:** EPIC-04 | **Sprint:** 1 | **Effort:** S | **Maps to:** S2-10

**Description:** Apply v2.9 Friction Item 2 deferred patch: execution_prompt.md §3.1.A story completion checklist — add note to populate `test_scenarios` in execution_state.json with test file paths when tests are created.

**Acceptance Criteria:**
- `claude/system/execution_prompt.md` §3.1.A updated with test_scenarios population instruction
- Instruction placed at the point of test creation: "populate test_scenarios in execution_state.json with the test file paths as tests are created"
- Instruction is non-blocking (advisory) — does not halt story execution
- Version bumped per CLAUDE.md §6 (this may be a combined commit with ST-12 if same version bump)
- OPERATIONAL_GUIDE.md §8 source prompt header and §14 execution engine version updated (if not already updated by ST-12)
- prompt_change_log.md entry appended
- DoQ sign-off with Date field populated

---

### ST-14 — prompt_change_log.md Retrospective Entries

**EPIC:** EPIC-04 | **Sprint:** 1 | **Effort:** S | **Maps to:** S2-11

**Description:** Close OA-v29-01 by adding retrospective prompt_change_log.md entries for sprint_planning_prompt.md v2.3→v2.4 and v2.4→v2.5 version increments (if gaps confirmed to exist).

**Acceptance Criteria:**
- `claude/system/prompt_change_log.md` scanned for sprint_planning_prompt.md entries
- If v2.3→v2.4 entry absent: add retrospective entry with date 2026-03-24, change summary from commit history or OPERATIONAL_GUIDE §14 diff, authority: Head of Specs Team (retrospective)
- If v2.4→v2.5 entry absent: add retrospective entry with date 2026-04-05, change summary, authority: Head of Specs Team (retrospective)
- If entries already present: record finding in delivery note and mark OA-v29-01 closed
- No other prompt_change_log.md modifications
- DoQ sign-off with Date field populated

---

### ST-15 — Consecutive Losing Streak Metric

**EPIC:** EPIC-04 | **Sprint:** 1 | **Effort:** S | **Maps to:** S2-12

**Description:** Add consecutive losing streak count to the analytics service and display it in the analytics dashboard per BLG-FEAT-18.

**Acceptance Criteria:**
- Consecutive losing streak count computed from closed trades (historical only; no reference to open positions)
- Metric visible in analytics/dashboard view alongside expectancy and win rate
- Metric definition added to canonical metrics definitions spec (as a new entry)
- Backend: new computed field in analytics service; no new endpoint required if existing analytics endpoint can be extended
- No regression to existing analytics metrics (win rate, expectancy, etc.)
- Endpoint registered in test suite if new endpoint added; openapi.yaml updated if applicable
- Unit tests covering: streak count computation (all wins → 0 streak, alternating → max streak, multiple consecutive losses → correct count)
- DoQ sign-off with Date field populated

---

### ST-16 — Model Version Contract for AI Journal

**EPIC:** EPIC-04 | **Sprint:** 1 | **Effort:** S | **Maps to:** S2-13

**Description:** Create the AI Journal model version contract document specifying which Claude model version executes summarisation per BLG-AI-02.

**Acceptance Criteria:**
- New document created: `docs/specs/ai_journal_model_contract.md` (or equivalent path per AI Compliance standards)
- Document specifies: current Claude model version in use, where model version is configured (environment variable or code constant), process for incrementing the contract when model version changes
- Document referenced in `ai_audit_service.py` or the AI journal summary endpoint (comment or docstring noting contract document)
- Class 2 or Class 3 per document_lifecycle_guide.md
- BLG-AI-02 acceptance criteria met: contract created, referenced in audit log implementation, change process documented
- DoQ sign-off with Date field populated

---

## Sprint Summary

| Sprint | EPICs | Stories | Estimated effort | Key deliverable |
|--------|-------|---------|-----------------|-----------------|
| Sprint 1 | EPIC-01, EPIC-04 | ST-01–ST-04, ST-12–ST-16 (9 stories) | ~6–9 days | Screener engine backend + governance patches |
| Sprint 2 | EPIC-02, EPIC-03 | ST-05–ST-11 (7 stories) | ~4–5 days | Screener frontend + ops/QA/shortcuts |
| **Total** | 4 | **16** | **~10–14 days** | v3.0 Arc 1 complete |

**Design gate required between Sprint 1 and Sprint 2** — must pass before EPIC-02 opens.

<!-- release-plan-marker: RP:v3.0:2026-04-25__release-v3.0 -->
