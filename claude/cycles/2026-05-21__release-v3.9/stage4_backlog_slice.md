Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v3.9
Cycle: 2026-05-21__release-v3.9
Last Updated: 2026-05-21

---

# Backlog Slice — v3.9

---

## EPIC-01 — Screener Data Quality & Reliability

**Maps to:** S2-01, S2-02
**Owner:** Head of Backend Engineering; Head of UX & Design
**Sprint:** Sprint 1
**Description:** Fix three live screener data quality bugs (P1/P2) that silently degrade screener output, and add a user-visible degraded-run warning when OHLCV failures exceed 20%.

---

### ST-01 — Fix Yahoo Finance crumb/401 rate-limiting in screener batch

**Epic:** EPIC-01
**Source:** BLG-TECH-10
**Effort:** M (~1–2 days)
**Type:** Backend Engineering

**Objective:** The screener batch service makes concurrent OHLCV requests to Yahoo Finance. Under load, YF returns 401 "Invalid Crumb" errors, causing the majority of US tickers to fail data fetch silently. Fix crumb refresh logic, add exponential backoff with jitter, and cap concurrent requests.

**Acceptance Criteria:**
- AC-01: A 401 response in screener batch triggers a crumb refresh and one retry before marking the ticker as failed
- AC-02: Per-request exponential backoff with jitter applied on 401/429 responses
- AC-03: Concurrent YF request cap configurable via environment variable (default: 5 in-flight)
- AC-04: Screener run against full ticker universe completes without >5% OHLCV failures under normal YF conditions
- AC-05: Crumb refresh events and consecutive failure counts visible in backend logs

**Test coverage:** Unit tests for crumb refresh trigger; integration test verifying backoff; Playwright: not required (backend-only)

---

### ST-02 — Fix sector/industry data silently dropped in screener batch

**Epic:** EPIC-01
**Source:** BLG-BE-10
**Effort:** XS (<1h)
**Type:** Backend Engineering

**Objective:** `screener_batch_service.py` extracts only the ticker string from the DB record, discarding sector/industry. Fix to retain the full ticker dict and pass sector/industry to `compute_screener_result()`.

**Acceptance Criteria:**
- AC-01: Screener results for tickers with sector/industry in `ticker_universe` have non-null sector and industry values
- AC-02: No change to screener result schema or API contract
- AC-03: Unit test confirms sector/industry propagation through batch → compute_screener_result

**Test coverage:** Unit test; Playwright: not required (backend data fix, display unchanged)

---

### ST-03 — Remove invalid DAY ticker and investigate PHNX.L from ticker universe

**Epic:** EPIC-01
**Source:** BLG-BE-11
**Effort:** XS (<1h)
**Type:** Backend Engineering

**Objective:** `DAY` (Dayforce Inc.) consistently returns Yahoo Finance HTTP 404 on historical data requests. Remove from ticker universe and CSV. Investigate PHNX.L status.

**Acceptance Criteria:**
- AC-01: `DAY` removed from `backend/tickers_full_list.csv`
- AC-02: `DAY` deactivated or deleted from `ticker_universe` table
- AC-03: No `OHLCV FAILED for DAY` log entries on subsequent screener runs
- AC-04: PHNX.L investigated — if consistently 404, same treatment applied; finding documented in commit message
- AC-05: If a valid Yahoo Finance symbol for Dayforce Inc. exists, add it back with correct symbol

**Test coverage:** Manual verification against screener run; Playwright: not required

---

### ST-04 — Add degraded-run warning banner to screener results page

**Epic:** EPIC-01
**Source:** BLG-FE-38
**Effort:** S (~0.5 days)
**Type:** Backend + Frontend

**Objective:** When >20% of tickers fail OHLCV fetch in a screener run, set `degraded_run: true` and `failure_rate` on the run record, expose it in the API response, and display a visible warning banner in the frontend.

**Acceptance Criteria:**
- AC-01: `degraded_run: true` set on screener run record when >20% of tickers returned no OHLCV data
- AC-02: `GET /screener/results` response includes `degraded_run` boolean and `failure_rate` float
- AC-03: Screener results page shows a warning banner when `degraded_run` is true: "Results may be incomplete — {N}% of tickers failed data fetch"
- AC-04: Clean runs (failure rate ≤20%) show no banner
- AC-05: Playwright test verifies banner appears when `degraded_run: true` in mocked API response
- AC-06: Playwright test verifies banner absent when `degraded_run: false`

**Test coverage:** Unit test for degraded_run calculation; Playwright SC-SCR-DEG-01 (banner present), SC-SCR-DEG-02 (banner absent)

---

## EPIC-02 — Ticker Universe Management Enhancements

**Maps to:** S2-03
**Owner:** Head of Backend Engineering; Head of UX & Design
**Sprint:** Sprint 1
**Description:** Two quality-of-life improvements to the Ticker Universe page shipped in v3.8: strip .L suffix from display labels and add company name to the management page.

---

### ST-05 — Strip .L suffix from Ticker Universe page display labels

**Epic:** EPIC-02
**Source:** BLG-FE-37
**Effort:** XS (<1h)
**Type:** Frontend

**Objective:** LSE tickers display with `.L` suffix on the Ticker Universe page. Strip suffix from display label only; underlying API calls and DB values unchanged.

**Acceptance Criteria:**
- AC-01: LSE tickers on the Ticker Universe page display without `.L` suffix in the label
- AC-02: Ticker symbol sent in API requests (add, delete, toggle) still includes `.L` suffix unchanged
- AC-03: US tickers are unaffected
- AC-04: Playwright test verifies LSE ticker displayed without `.L`

**Test coverage:** Playwright SC-TU-DISP-01 (LSE suffix stripped in display)

---

### ST-06 — Add company_name column to ticker universe and display on management page

**Epic:** EPIC-02
**Source:** BLG-BE-12
**Effort:** S (~0.5 days)
**Type:** Backend + Frontend

**Objective:** `ticker_universe` table lacks company name. Add `company_name TEXT` column, backfill from `tickers_full_list.csv`, include in API response, and display alongside ticker symbol on the management page.

**Acceptance Criteria:**
- AC-01: `company_name TEXT` column added to `ticker_universe` table via `ensure_company_name_column()` on startup
- AC-02: `company_name` backfilled from `tickers_full_list.csv` for all existing rows on startup
- AC-03: `company_name` populated when syncing new tickers from CSV
- AC-04: `GET /ticker-universe` response includes `company_name` field
- AC-05: Ticker Universe page shows company name next to each ticker symbol
- AC-06: Tickers not in CSV have `company_name = null`; page displays gracefully (shows ticker only, no error)
- AC-07: Playwright test verifies company name renders on the page for a known ticker

**Test coverage:** Unit test for backfill logic; Playwright SC-TU-COMP-01 (company name visible)

---

## EPIC-03 — Arc 5 Red Flag Journal (SI-03)

**Maps to:** S2-04
**Owner:** Head of Backend Engineering; Head of UX & Design
**Sprint:** Sprint 2
**Description:** Auto-populated log of every instance where the operator's behaviour deviated from their stated strategy — pre-entry rule validation override, checklist item skipped, stop management prompt dismissed. Separate from the trade journal. SI-01 (v3.8) provides the override acknowledgement infrastructure; this EPIC adds persistent logging and the Red Flag Journal display.

**§13 compliance note:** Red Flag Journal is a display-only audit log of operator-confirmed deviations. No automated decisions. Fully §13 compliant.

---

### ST-07 — Red Flag Journal — data model and backend

**Epic:** EPIC-03
**Effort:** M (~1.5–2 days)
**Type:** Backend

**Objective:** Persist override events from SI-01 and other deviation triggers to a `red_flag_events` table. Add `GET /portfolio/red-flag-journal` endpoint returning a paginated log of deviation events with type, timestamp, ticker, and context.

**Acceptance Criteria:**
- AC-01: `red_flag_events` table created with fields: id, event_type (ENUM: pre_entry_override, checklist_skipped, stop_prompt_dismissed, drawdown_prompt_dismissed), ticker, position_id (nullable), context (JSON), created_at
- AC-02: SI-01 pre-entry validation override acknowledgement writes a `pre_entry_override` event to `red_flag_events` at confirmation time
- AC-03: `GET /portfolio/red-flag-journal` returns paginated events (page, page_size, total, items[])
- AC-04: Response includes: event_type, ticker, context (summary), created_at for each event
- AC-05: Filter query params supported: `event_type`, `ticker`, `since` (ISO date)
- AC-06: Endpoint registered in `backend/routers/test.py` and `docs/reference/openapi.yaml`
- AC-07: Unit tests: empty journal, pagination, filter by event_type, filter by ticker
- AC-08: SI-01 override path confirmed to write to `red_flag_events` in integration test

**Test coverage:** Unit tests per AC-07; integration test for SI-01 event write path

---

### ST-08 — Red Flag Journal — frontend display

**Epic:** EPIC-03
**Effort:** M (~1.5 days)
**Type:** Frontend

**Objective:** Add a Red Flag Journal view surfacing the paginated event log from `GET /portfolio/red-flag-journal`. Display event type with icon, ticker, context summary, and date. Accessible from the main navigation.

**Acceptance Criteria:**
- AC-01: `/red-flag-journal` route added to `src/App.js` and `createPageUrl` map
- AC-02: `RedFlagJournal.js` component renders a paginated list of events from the API
- AC-03: Each event row shows: event type icon, event type label, ticker, context summary, date
- AC-04: Filter controls: event type dropdown, ticker text input, date range
- AC-05: Empty state displayed when no events exist: "No strategy deviations recorded yet"
- AC-06: Nav link added to main navigation (sidebar / top nav)
- AC-07: Playwright: SC-RFJ-01 — page renders with mocked events list
- AC-08: Playwright: SC-RFJ-02 — empty state renders when API returns 0 events
- AC-09: Playwright: SC-RFJ-03 — filter by event_type narrows results in mocked response

**Test coverage:** Playwright SC-RFJ-01, SC-RFJ-02, SC-RFJ-03

---

## EPIC-04 — Governance & Process Patches

**Maps to:** S2-05
**Owner:** Head of Specs Team; Director of Quality
**Sprint:** Sprint 2
**Description:** Four governance patches addressing v3.8 carry-forward items and BLG-GOV-25 dry-run support. All are governance prompt or template modifications; no product code changes.

---

### ST-09 — execution_prompt.md patches — test_scenarios guidance and createPageUrl delegation note

**Epic:** EPIC-04
**Source:** CF item 4 (test_scenarios population guidance) + CF item 2 (createPageUrl delegation template)
**Effort:** S (~1h)
**Type:** Governance

**Objective:** Two patches to `execution_prompt.md`: (1) test_scenarios should only reference spec files containing scenarios exercised for that EPIC's AC — stale cross-file references inflate traceability check; (2) when creating a new frontend page, the delegation template must include a `createPageUrl` map update requirement.

**Acceptance Criteria:**
- AC-01: `execution_prompt.md` §9.1 spec_references guidance updated: test_scenarios lists only spec files whose scenarios directly exercise an AC of this EPIC
- AC-02: `execution_prompt.md` delegation template section includes note: "New frontend page stories must include `createPageUrl` map update in delegation scope"
- AC-03: `execution_prompt.md` version bumped; OPERATIONAL_GUIDE §14 table updated; `prompt_change_log.md` entry appended
- AC-04: All four governance file changes committed together (CLAUDE.md §6 checklist)

**Test coverage:** Governance prompt — no automated test; verified by governance-drift skill post-commit

---

### ST-10 — sprint_planning_prompt.md patch — planning-deferred items in execution_state.json

**Epic:** EPIC-04
**Source:** CF item 5
**Effort:** S (~1h)
**Type:** Governance

**Objective:** Update `sprint_planning_prompt.md` to record planning-deferred items in `execution_state.json` with `status: deferred_at_planning` and a `gate_condition` note. Enables execution engine to distinguish items that were never in scope vs items that were deferred at planning time.

**Acceptance Criteria:**
- AC-01: `sprint_planning_prompt.md` STEP 5 or equivalent section updated: when an item is deferred at planning (gate not met, capacity, etc.), add it to `execution_state.json` with `status: deferred_at_planning` and `gate_condition: "<reason>"`
- AC-02: `sprint_planning_prompt.md` version bumped; OPERATIONAL_GUIDE §14 table updated; `prompt_change_log.md` entry appended
- AC-03: All four governance file changes committed together (CLAUDE.md §6 checklist)

**Test coverage:** Governance prompt — no automated test

---

### ST-11 — BLG-GOV-25 — Add --dry-run support to plan release and run delivery verification

**Epic:** EPIC-04
**Source:** BLG-GOV-25; Audit AUD-2026-05-21-004
**Effort:** M (~1–2 days)
**Type:** Governance

**Objective:** Add `--dry-run` flag support to `release_planning_prompt.md` and `delivery_verification_prompt.md`. When `--dry-run` is specified: validate inputs, check artefact availability, report what would be created — no writes. Add both engines to `shared_standards.md` §13 dry-run capability table.

**Acceptance Criteria:**
- AC-01: `release_planning_prompt.md` STEP -1: if `--dry-run` is detected, execute preflight and scope extraction only, report what would be created, make no file writes, exit cleanly
- AC-02: `delivery_verification_prompt.md` STEP -1: if `--dry-run` is detected, report which checks would run (list all STEP checks with their precondition sources), make no file writes, exit cleanly
- AC-03: `shared_standards.md` §13 dry-run table gains two rows: `plan release --dry-run` and `run delivery verification --dry-run` with their respective outputs
- AC-04: All three modified files have bumped version headers; OPERATIONAL_GUIDE §14 table updated for all three; `prompt_change_log.md` entries appended (one per file, same commit)
- AC-05: CLAUDE.md §6 governance checklist fully satisfied for all modified files

**Test coverage:** Governance prompt — no automated test; manual dry-run invocation to verify no writes

---

### ST-12 — QA evidence pre-merge enforcement — PR template checklist item

**Epic:** EPIC-04
**Source:** CF item 3 (2-cycle escalation — Director of Quality); lessons_learnt_closure.md Phase 4 LL item 1
**Effort:** S (~1h)
**Type:** Governance
**Authority:** Director of Quality

**Objective:** Add a mandatory checklist item to the PR template requiring QA evidence to exist before requesting merge. This is a 2-cycle escalation — the pattern of retroactive QA evidence recurred in v3.7 Phase 3, v3.8 Phase 3, and v3.8 Phase 4. Director of Quality must implement this before v3.9 execution begins.

**Acceptance Criteria:**
- AC-01: PR template (`.github/pull_request_template.md` or equivalent) gains a checklist item: `[ ] QA evidence file exists and DoQ sign-off date is populated before this PR is opened`
- AC-02: The checklist item is marked as required (cannot be unchecked without reviewer noting reason)
- AC-03: Commit message notes: "Closes CF-3 DoQ QA enforcement escalation (2-cycle recurrence v3.7 → v3.8)"

**Test coverage:** Manual review of PR template; no automated test

---

## Conditional Scope — EPIC-05 (PT-04 Setup Quality Score)

**Maps to:** S2-06
**Owner:** Head of Backend Engineering; Metrics & Analytics Owner; Head of UX & Design
**Sprint:** Sprint 2 (conditional — gate must be confirmed before sprint planning seals)
**Gate:** Product Owner confirms 20+ closed trades at sprint planning

**If gate confirmed:** ST-13 and ST-14 enter the sprint backlog with full AC. If gate not confirmed: ST-13 and ST-14 recorded as `deferred_at_planning` with gate_condition `"20+ closed trades not confirmed by PO"`.

---

### ST-13 — PT-04 Setup Quality Score — backend endpoint (conditional)

**Epic:** EPIC-05 (conditional)
**Source:** BLG-FEAT-25 §Scope Backend
**Effort:** M (~1–2 days)
**Type:** Backend
**Gate:** 20+ closed trades confirmed by Product Owner before sprint planning seals

**Acceptance Criteria:**
- AC-01: `GET /trade-plans/setup-quality-score?ticker={ticker}` endpoint implemented
- AC-02: Score (0–100) computed from closed trade history matching current regime/signal/ATR conditions for the ticker
- AC-03: Gate response: `{"gate_not_met": true, "min_trades_required": 20}` returned when fewer than 20 closed trades
- AC-04: Response fields when gate met: `score` (int 0–100), `matching_trades` (int), `win_rate` (float), `average_R` (float), `score_explanation` (string)
- AC-05: Endpoint registered in `backend/routers/test.py` and `docs/reference/openapi.yaml`
- AC-06: Unit tests: gate_not_met case, gate_met with mixed history, gate_met with high win rate

**Test coverage:** Unit tests per AC-06; API integration test

---

### ST-14 — PT-04 Setup Quality Score — frontend display (conditional)

**Epic:** EPIC-05 (conditional)
**Source:** BLG-FEAT-25 §Scope Frontend
**Effort:** M (~1–2 days)
**Type:** Frontend
**Gate:** ST-13 complete; 20+ closed trades gate confirmed

**Acceptance Criteria:**
- AC-01: Setup Quality Score displayed in Pre-Trade Research View
- AC-02: Setup Quality Score displayed in Trade Plan form (alongside existing fields)
- AC-03: Score badge shows numeric value (0–100) and qualitative label (Excellent ≥80 / Good 60–79 / Fair 40–59 / Low <40)
- AC-04: "Insufficient trade history (< 20 trades)" message shown when gate_not_met is true
- AC-05: Tooltip/expandable detail: matching_trades, win_rate, average_R
- AC-06: Score updates when ticker changes (React Query refetch on ticker param change)
- AC-07: Playwright: SC-SQS-01 — score badge renders with value and label
- AC-08: Playwright: SC-SQS-02 — gate-not-met message renders
- AC-09: Playwright: SC-SQS-03 — score updates on ticker change

**Test coverage:** Playwright SC-SQS-01, SC-SQS-02, SC-SQS-03

---

## Sprint Planning Notes

**Sprint 1 scope:** EPIC-01 (ST-01–ST-04) + EPIC-02 (ST-05–ST-06) = 6 stories
**Sprint 2 scope:** EPIC-03 (ST-07–ST-08) + EPIC-04 (ST-09–ST-12) = 6 stories (+ ST-13/ST-14 if gate confirmed)
**Total firm:** 12 stories | **Conditional:** +2 (PT-04)

**Merge order (Sprint 1):** EPIC-02 → EPIC-01
**Merge order (Sprint 2):** EPIC-04 → EPIC-03 → EPIC-05 (if in scope)

**Pre-sprint required decisions:**
- [ ] [RISK-03] SI-03 Red Flag Journal — verify SI-01 override event persistence model in v3.8 code before sprint planning seals; confirm DB table or schema for events — Owner: Head of Backend Engineering
- [ ] [RISK-05] PT-04 gate — Product Owner confirms 20+ closed trades gate met or not — Owner: Product Owner (decision required before sprint planning seals)

**Outstanding before sprint execution begins:**
- Director of Quality (ST-12 / CF-3 escalation) must confirm PR template item is live before EPIC-04 begins execution
- PMO Lead: audit and close duplicate GitHub issues created during v3.8 (housekeeping, not a sprint story)
