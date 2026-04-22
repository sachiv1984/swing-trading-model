Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v2.9
Cycle: 2026-04-22__release-v2.9
Last Updated: 2026-04-22

---

# Backlog Slice — v2.9 Arc 1 Foundation

**Theme:** Arc 1 Foundation — Stock Discovery & Screening Spec & Infrastructure

---

## EPIC-01 — Arc 1 Specification Foundation

**Purpose:** Author the three canonical specs and one UX spec that are prerequisites for Arc 1 implementation. These artefacts gate DS-01, DS-02, and DS-05 execution.

**Maps to:** S2-04, S2-05, S2-06, S2-07

**Sprint:** 1

---

### ST-01 — Screener results schema spec (BLG-SPEC-21)

**Source:** BLG-SPEC-21
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team

**Acceptance Criteria:**
1. New Class 2 canonical document created at `docs/specs/screener_results_schema.md` (or equivalent path under docs/specs/)
2. Document specifies all screener output fields: ticker, market, ATR, regime status, signal score, sector, proximity to entry zone — with type and derivation source for each
3. Document explicitly references `docs/specs/strategy_rules.md §11` as the parameter source for regime gate, ATR multiplier, and signal threshold fields
4. Logging requirement section included: screener runs must log the parameter set used (§11 version + field values) for audit trail purposes
5. DoQ sign-off with Date field populated
6. Document added to `docs/specs/Specs_Index.md`

---

### ST-02 — Alpaca API integration contract (BLG-SPEC-22)

**Source:** BLG-SPEC-22
**Effort:** S (~1 day)
**Owner:** API Contracts & Documentation Owner

**Acceptance Criteria:**
1. New Class 2 canonical document created at `docs/specs/api_contracts/alpaca_integration_contract.md`
2. All DS-05 Alpaca endpoints documented at `##` heading level with request/response schemas (OHLCV bars endpoint at minimum)
3. Rate limits, error codes, and retry strategy documented
4. Fallback strategy explicitly defined: Yahoo Finance fallback vs explicit error (not left implicit)
5. API version pinned (Alpaca API version documented)
6. Corresponding OpenAPI entries added to `docs/reference/openapi.yaml` for any new endpoints (per CLAUDE.md §1 rule)
7. DoQ sign-off with Date field populated
8. Document added to `docs/specs/Specs_Index.md`

---

### ST-03 — Screener internal API contract (BLG-SPEC-23)

**Source:** BLG-SPEC-23
**Effort:** S (~0.5 day)
**Owner:** API Contracts & Documentation Owner

**Acceptance Criteria:**
1. New Class 2 canonical document created at `docs/specs/api_contracts/screener_api_contract.md`
2. `GET /screener/results` and `POST /screener/run` endpoints documented at `##` heading level
3. Request/response schemas defined with field names, types, and pagination for GET
4. Error codes and authentication requirements documented
5. Corresponding OpenAPI entries added to `docs/reference/openapi.yaml` (per CLAUDE.md §1 rule)
6. DoQ sign-off with Date field populated
7. Document added to `docs/specs/Specs_Index.md`

---

### ST-04 — Screener results page UX spec (BLG-FE-17)

**Source:** BLG-FE-17
**Effort:** M (~2 days)
**Owner:** Frontend Specifications & UX Documentation Owner

**Acceptance Criteria:**
1. UX spec created as Class 2 or Class 5 document at appropriate path under `docs/specs/` or `docs/design/`
2. Column layout, sort/filter controls, and candidate card design documented
3. Data freshness indicator specified: last updated timestamp + manual refresh trigger
4. Empty states designed and documented: no results, no market data, stale data
5. Watchlist promotion confirmation flow documented (DS-07 interaction detail)
6. Progressive loading pattern (skeleton UI) specified
7. All DS-02 interaction patterns covered
8. DoQ sign-off with Date field populated

---

## EPIC-02 — Arc 1 Implementation Start

**Purpose:** Deliver first three Arc 1 features: sector enrichment (DS-03), Alpaca data integration (DS-05), and Alpaca news panel (DS-06). These are the infrastructure items that enable the screener engine (DS-01) in v3.0.

**Maps to:** S2-01, S2-02, S2-03

**Sprint:** 2

**Sequencing constraint:** ST-06 (DS-05) requires ST-02 (BLG-SPEC-22) to be complete. ST-07 (DS-06) requires ST-08 (BLG-GOV-16) sign-off to be complete.

---

### ST-05 — Sector & Industry Classification (DS-03)

**Source:** DS-03 (Arc 1 roadmap feature)
**Effort:** S (~1 day)
**Owner:** Backend Engineering Patterns Owner

**Acceptance Criteria:**
1. Yahoo Finance sector/industry data enrichment implemented for all screened tickers
2. Sector and industry classification exposed on existing open positions as well as screened candidates
3. New `sector` and `industry` fields added to relevant data model (position and/or screener result)
4. `GET /positions` (or relevant endpoint) returns sector/industry fields for each position
5. Data model change documented with migration script if schema change required
6. Unit tests cover sector enrichment for known tickers
7. No regression to existing position data

---

### ST-06 — Alpaca US Market Data Integration (DS-05)

**Source:** DS-05 (Arc 1 roadmap feature)
**Effort:** M (~2 days)
**Owner:** Backend Engineering Patterns Owner

**Prerequisite:** ST-02 (BLG-SPEC-22 Alpaca API contract) complete.

**Acceptance Criteria:**
1. Alpaca Markets API replaces Yahoo Finance as the OHLCV data source for US tickers
2. All endpoint calls implemented per BLG-SPEC-22 (ST-02) contract — no deviation from contract
3. Fallback strategy per BLG-SPEC-22 implemented and tested
4. ATR calculation and signal generation use Alpaca data for US market tickers
5. UK tickers continue to use Yahoo Finance (US-only change)
6. Integration tests cover Alpaca API call, response parsing, and fallback trigger
7. No regression to UK ticker data or existing analytics
8. API version pinned per BLG-SPEC-22 contract

---

### ST-07 — Alpaca News Panel (DS-06)

**Source:** DS-06 (Arc 1 roadmap feature)
**Effort:** S (~1 day)
**Owner:** Backend Engineering Patterns Owner + Frontend Specifications & UX Documentation Owner

**Prerequisite:** ST-08 (BLG-GOV-16 §13 sign-off) complete.

**Acceptance Criteria:**
1. Ticker-level news context panel implemented on screener results and watchlist pages
2. Display-only: headline count + headline list surfaced; no sentiment scoring, no automated advisory generated
3. Scope strictly per BLG-GOV-16 sign-off conditions (display-only, no sentiment analysis)
4. Alpaca News API endpoint used per BLG-SPEC-22 (ST-02) contract
5. Panel renders correctly when no news available (empty state)
6. §13 compliance verified: panel is read-only context, not an input to automated decision
7. No regression to screener results or watchlist rendering

---

## EPIC-03 — Arc 1 Governance & QA Foundation

**Purpose:** Complete the governance gate for DS-06 and establish the CI/test infrastructure for Arc 1 screener testing.

**Maps to:** S2-08, S2-09, S2-10

**Sprint:** 1

---

### ST-08 — §13 review record for DS-06 (BLG-GOV-16)

**Source:** BLG-GOV-16
**Effort:** S (~0.5 day)
**Owner:** Strategy Rules & System Intent Owner

**Acceptance Criteria:**
1. Class 3 Operational Record (or Class 5 Decision Record) created at `docs/product/decisions/` or equivalent path documenting §13 review of DS-06
2. Document explicitly states: DS-06 compliance conditioned on display-only headlines with no sentiment scoring and no automated advisory generation
3. Strategy Rules & System Intent Owner sign-off recorded with date
4. Gate marked complete in `claude/roadmap/current_roadmap.md` Arc 1 DS-06 row (or equivalent gate tracking)
5. Document references `docs/specs/strategy_rules.md §13` directly

---

### ST-09 — External API mock harness for CI (BLG-QA-08)

**Source:** BLG-QA-08
**Effort:** M (~2 days)
**Owner:** Director of Quality + QA & Testing Owner

**Acceptance Criteria:**
1. Test harness mocking Alpaca Markets API and Yahoo Finance API responses operational in CI
2. Mock responses are configurable per test scenario (not hard-coded to a single fixture)
3. Screener CI tests pass deterministically when mock harness is active (no live API calls)
4. Works in conjunction with BLG-QA-09 (ST-10) test data library
5. CI configuration updated to use mock harness for screener-related tests
6. DoQ sign-off with Date field populated

---

### ST-10 — Screener test data library (BLG-QA-09)

**Source:** BLG-QA-09
**Effort:** M (~2 days)
**Owner:** QA & Testing Owner

**Acceptance Criteria:**
1. Test data library created with minimum 10 synthetic tickers covering key screener filter scenarios
2. Edge cases documented and covered: passes all filters, fails regime gate, fails ATR threshold, fails signal threshold, market=UK vs market=US
3. Each synthetic ticker has: ticker symbol, market, price history, ATR values, regime state, signal score, sector
4. Library is compatible with BLG-QA-08 (ST-09) mock harness format
5. DoQ sign-off with Date field populated

---

## EPIC-04 — Governance Debt & Quick Wins

**Purpose:** Apply two deferred execution_prompt.md patches (CF-1, CF-2 from v2.8), a quick cosmetic fix, and address AI governance debt from v2.8 (audit log + test coverage).

**Maps to:** S2-11, S2-12, S2-13, S2-14, S2-15

**Sprint:** Sprint 1 (ST-11, ST-12, ST-13) + Sprint 2 (ST-14, ST-15)

---

### ST-11 — execution_prompt.md §3.2 patches (BLG-GOV-14)

**Source:** BLG-GOV-14 (OA-v28-03)
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team

**Acceptance Criteria:**
1. `claude/system/execution_prompt.md` §3.2.A contains note: when a `delegated_frontend` story is reclassified to `autonomous` per LL-v2.3-EX-02 but the EPIC contains frontend-visible changes, Director of Quality counter-sign is required at STEP 5 sprint close in addition to engine sign-off
2. `claude/system/execution_prompt.md` §3.2 DoQ sign-off block template contains explicit note: EPIC-level DoQ consolidation block required in qa_evidence when story-level sign-offs involve domain-specific authorities (Strategy Rules, Security, etc.)
3. CLAUDE.md §6 checklist applied: version bump (v3.8→v3.9), OPERATIONAL_GUIDE.md §14 updated, phase section header updated, `claude/system/prompt_change_log.md` entry appended
4. Head of Specs Team sign-off on both patches

---

### ST-12 — execution_prompt.md STEP 5.1.B (BLG-GOV-15)

**Source:** BLG-GOV-15 (AUD-2026-04-20-001)
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team

**Acceptance Criteria:**
1. `claude/system/execution_prompt.md` STEP 5.1 contains STEP 5.1.B advisory immediately after the "QA Evidence File Existence Check": before writing Sprint_Complete, open `docs/System_status_report.md` and verify SC-* scenario count cells match actual entries; if cells were set at sprint planning and not updated post-execution, correct now; also verify execution_prompt.md version reference matches actual current version; record corrections in sprint_close.md notes; non-blocking
2. CLAUDE.md §6 checklist applied: version bump, OPERATIONAL_GUIDE.md §14 updated, phase section header updated, prompt_change_log.md entry appended
3. Head of Specs Team sign-off

*Note: If ST-11 is done in the same commit, the version bump after ST-11 is the base; ST-12 bumps again from that version.*

---

### ST-13 — SystemStatus.js /ai prefix fix (BLG-FE-15)

**Source:** BLG-FE-15 (OA-v28-02)
**Effort:** S (~0.5 day)
**Owner:** Frontend Specifications & UX Owner

**Acceptance Criteria:**
1. `/ai` prefix case added to `categorizeEndpoint()` in `SystemStatus.js`
2. `POST /api/ai/journal-summary` and `GET /api/ai/journal-summary/history` appear in a named category (not `'Other'`) in the System Status page
3. No regression to categorisation of existing endpoints
4. Verified by code review (no observable UI behaviour change beyond category label)

---

### ST-14 — AI Journal summary audit log (BLG-AI-01)

**Source:** BLG-AI-01
**Effort:** S (~1 day)
**Owner:** AI Compliance & Governance Officer + Backend Engineering Patterns Owner

**Sprint:** 2

**Acceptance Criteria:**
1. Persistent audit log implemented recording each AI summary run: timestamp, trade_ids included, model version, output hash
2. Log stored in queryable/durable storage (database table, not just application logs)
3. Log is queryable by trade_id and date range via a backend endpoint or direct DB query
4. Model version recorded per run (references BLG-AI-02 scope — document model version in audit log even without full BLG-AI-02 contract)
5. Integration with existing `POST /api/ai/journal-summary` endpoint — audit record created on each invocation
6. DoQ sign-off with Date field populated

---

### ST-15 — AI Journal test scenario coverage (TEST-GAP-EPIC-04)

**Source:** TEST-GAP-EPIC-04
**Effort:** S (~0.5 day)
**Owner:** QA & Testing Owner

**Sprint:** 2

**Acceptance Criteria:**
1. `docs/testing/ai_scenarios.md` created with minimum 4 scenarios:
   - AI summary happy path: `POST /api/ai/journal-summary` with valid trade_ids returns summarised text
   - AI summary graceful LLM failure: LLM unreachable → HTTP 200 with `summary: null`
   - Frontend: AI summary section collapsed by default on page load
   - Frontend: Disclaimer always visible when section is expanded (all expanded states)
2. All scenarios reference `docs/specs/api_contracts/ai_endpoints.md` and `trade_history.md v1.7` as canonical specs
3. DoQ sign-off with Date field populated
