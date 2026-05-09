**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.3
**Cycle:** 2026-05-09__release-v3.3
**Last Updated:** 2026-05-09

---

# Backlog Slice — v3.3 Arc 3 In-Trade Risk Management

**Theme:** Arc 3 Start — Position Lifecycle + Decision Support + Research View Spec Closure + Governance Patches

**Sprints:** 2 | **EPICs:** 4 | **Stories:** 17

---

## EPIC-01 — Arc 3 Foundation: Position Lifecycle Manager

**Maps to:** S2-01
**Owner:** Head of Engineering
**Sprint:** 1
**Theme:** IT-01 — Position state machine: data model, backend service, frontend display

IT-01 is the Arc 3 data foundation. Positions currently have no explicit lifecycle state. This EPIC introduces a deterministic state machine (GRACE → LOSING → PROFITABLE → EXIT ZONE) persisted in the database, computed and updated by a backend service, and displayed in the frontend positions view.

### ST-01 — Positions data model: add lifecycle state fields and migration

**EPIC:** EPIC-01
**Sprint:** 1
**Type:** Backend / Data Model
**Source:** IT-01 (Arc 3)

**Acceptance Criteria:**
- `positions` table has new fields: `position_state` (varchar, nullable initially), `state_entered_at` (timestamp, nullable), `state_history` (JSONB — array of {state, entered_at} for audit)
- Alembic migration created and tested
- Back-fill logic: existing positions assigned `position_state = 'GRACE'` if opened within last 10 trading days; `'UNKNOWN'` otherwise (UNKNOWN is a valid display state handled gracefully)
- Migration reversible (down migration provided)
- No regression in existing position endpoints

---

### ST-02 — Position lifecycle state machine backend service

**EPIC:** EPIC-01
**Sprint:** 1
**Type:** Backend / Service
**Source:** IT-01 (Arc 3)

**Acceptance Criteria:**
- `PositionLifecycleService` class implements state transition logic:
  - `GRACE`: days since open ≤ 10 trading days and position has not moved outside entry zone
  - `LOSING`: position below entry price by more than 0.5 ATR
  - `PROFITABLE`: position above entry price by more than 0.5 ATR
  - `EXIT ZONE`: position above entry price by ≥ 2R (R-target reached)
  - `UNKNOWN`: insufficient data to determine state (no stop or R-target on plan)
- State computed from existing position data (current price, entry price, ATR, stop level, R-target from trade plan if linked)
- Service callable on demand; no automatic state mutation (human-in-the-loop)
- `GET /positions` and `GET /positions/{id}` return `position_state`, `state_entered_at`, `days_in_state` in response
- State updated when `GET /positions` is called (lazy recalculation) OR via explicit `POST /positions/{id}/refresh-state`
- Unit tests covering all 5 state transition paths

---

### ST-03 — Position lifecycle state: frontend display

**EPIC:** EPIC-01
**Sprint:** 1
**Type:** Frontend
**Source:** IT-01 (Arc 3)
**Design gate dependency:** UX spec for position state display required from design gate before implementation

**Acceptance Criteria:**
- Positions page displays `position_state` as a coloured badge per row: GRACE (blue), LOSING (red), PROFITABLE (green), EXIT ZONE (purple), UNKNOWN (grey)
- `days_in_state` displayed alongside badge (e.g. "GRACE — 3d")
- "Next state trigger" tooltip or subtitle displayed per state (e.g. GRACE: "Exits grace in 7d if no move > 0.5 ATR")
- No regression in existing positions page columns
- Playwright E2E scenario: positions page loads with state badge visible for at least one position
- Human staging sign-off if Playwright cannot cover all badge states (document which states require staging)

---

## EPIC-02 — Arc 3 Decision Support: Grace Period + Stop Management

**Maps to:** S2-02
**Owner:** Head of Engineering
**Sprint:** 2
**Theme:** IT-02 + IT-03 — Grace period day-8 alert + ATR trail stop management guided UI

Depends on EPIC-01: uses `position_state` and lifecycle service infrastructure. Both features are structured prompts requiring human confirmation — §13 COMPLIANT.

### ST-04 — Grace Period Decision Support backend (IT-02)

**EPIC:** EPIC-02
**Sprint:** 2
**Type:** Backend
**Source:** IT-02 (Arc 3)

**Acceptance Criteria:**
- `GET /positions/grace-period-alerts` returns positions in GRACE state where `days_in_state ≥ 8`
- Response includes: position_id, ticker, days_in_state, trade_plan_id (if linked), trade_plan_summary (thesis excerpt, entry zone, stop level, R-target)
- If no linked trade plan: trade_plan fields returned as null
- Endpoint registered in `backend/routers/test.py` with representative value in same commit
- Endpoint registered in `docs/reference/openapi.yaml` in same commit

---

### ST-05 — Grace Period Decision Support frontend (IT-02)

**EPIC:** EPIC-02
**Sprint:** 2
**Type:** Frontend
**Source:** IT-02 (Arc 3)
**Design gate dependency:** UX spec for grace period prompt required from design gate

**Acceptance Criteria:**
- Grace period alert surfaced on positions page or dashboard when any position is in GRACE state with days_in_state ≥ 8
- Alert card displays: ticker, days_in_state, trade plan context (thesis excerpt, entry zone, stop, R-target if available)
- Dismissible: user can acknowledge and dismiss the alert (dismissed state stored in localStorage or session — no backend persistence required)
- Link to original trade plan detail view (if trade_plan_id present)
- §13 display-only: no automated recommendation generated; system prompts review, human decides
- Playwright scenario: alert renders when position in GRACE state ≥ day 8

---

### ST-06 — Stop Management Workflow backend (IT-03)

**EPIC:** EPIC-02
**Sprint:** 2
**Type:** Backend
**Source:** IT-03 (Arc 3)

**Acceptance Criteria:**
- `GET /positions/{id}/stop-trail` returns:
  - `current_stop`: stop price from position record (from stop price join shipped v2.4)
  - `atr_trail_stop`: calculated as `current_price - (ATR × trail_multiplier)` where trail_multiplier defaults to 2.0 (configurable per strategy_rules.md)
  - `trail_difference`: `atr_trail_stop - current_stop` (positive = trail raises stop)
  - `trail_r_terms`: difference expressed as R-multiples (using R from linked trade plan or 1×ATR if no plan)
  - `recommendation`: string "Raise stop to {atr_trail_stop}" — display-only per §13
- If `current_stop` is null: return trail calculation with `current_stop: null` and `trail_difference: null`; frontend disables trail action
- Endpoint registered in `backend/routers/test.py` and `openapi.yaml` in same commit

---

### ST-07 — Stop Management Workflow frontend (IT-03)

**EPIC:** EPIC-02
**Sprint:** 2
**Type:** Frontend
**Source:** IT-03 (Arc 3)
**Design gate dependency:** UX spec for stop management guided UI required from design gate

**Acceptance Criteria:**
- Positions page has "Trail Stop" action button per row (visible for PROFITABLE or EXIT ZONE state positions with a current stop set)
- Clicking opens a guided panel/modal showing:
  - Current stop (price)
  - ATR trail stop (calculated price)
  - Difference (in price and R-terms)
  - Confirmation button: "Update stop to {trail_stop}" — user must click to proceed
  - Cancel/dismiss option
- On confirmation: calls existing stop update mechanism (PUT /positions/{id} or equivalent) to update stop_price
- If current_stop is null: "Trail Stop" button disabled with tooltip "No current stop set"
- §13: system presents recommendation; human confirms; no automated action
- Playwright scenario: trail stop panel opens and confirm button is present

---

## EPIC-03 — Research View Spec & QA Closure

**Maps to:** S2-03
**Owner:** Head of Specs Team
**Sprint:** 1
**Theme:** Close spec, QA, and governance gaps for the shipped PT-02 research view

All 6 "Before v3.3 sprint planning" items are in this EPIC. These are high priority — spec authorship starts day 1 of Sprint 1 and must complete before EPIC-02 frontend designs begin.

### ST-08 — PT-02 research API contract (BLG-SPEC-25) + data source provenance spec (BLG-SPEC-26)

**EPIC:** EPIC-03
**Sprint:** 1
**Type:** Specification
**Source:** BLG-SPEC-25, BLG-SPEC-26

**Acceptance Criteria:**
- `docs/specs/api_contracts/research_endpoint.md` (Class 2) created covering:
  - Request: ticker format, market auto-detection behaviour
  - Response schema: all fields with types, nullable flags, and source attribution fields
  - Error codes: 404 (ticker not found), 503 (external source unavailable), 429 (rate limit)
  - Rate limit policy per external source
- `docs/specs/data_provenance/research_view_provenance.md` (Class 2) created covering:
  - Per data field: named source (Yahoo Finance, Alpaca, internal), retrieval timestamp display requirement
  - Display format for source attribution (tooltip, label, or icon — specified, not left to implementation)
  - Retrieval timestamp: format and placement per field or panel
- Both documents cross-reference each other
- Signed off by API Contracts & Documentation Owner (SPEC-25) and Head of Specs Team (SPEC-26)

---

### ST-09 — PT-02 canonical research view spec (BLG-SPEC-24) + UX spec (BLG-FE-28)

**EPIC:** EPIC-03
**Sprint:** 1
**Type:** Specification + UX
**Source:** BLG-SPEC-24, BLG-FE-28

**Acceptance Criteria:**
- `docs/specs/frontend/pages/research_view.md` (Class 2 canonical) created covering:
  - Data fields displayed: price, % change, market cap, ATR, regime, news, earnings
  - Data sources per field (references ST-08 provenance spec)
  - Data freshness policy: maximum acceptable data age per field, staleness display behaviour
  - Display rules: formatting, units, empty/null handling
  - §13 compliance confirmed in spec front-matter
  - References openapi.yaml for GET /research/{ticker}
- `docs/design/2026-05-09__release-v3.3/research-view/ux_spec.md` (UX spec) created covering:
  - Layout: panel arrangement, data field hierarchy
  - Data field placement and visual hierarchy
  - Source attribution display format (aligned with ST-08 provenance spec)
  - News feed design: article format, truncation, link behaviour
  - Freshness indicator: placement, format, staleness threshold
  - Empty and error states explicitly specified
- Head of Specs Team sign-off on canonical spec; Frontend UX Documentation Owner sign-off on UX spec

---

### ST-10 — Research view test scenario library (BLG-QA-17) + acceptance test protocol (BLG-QA-15)

**EPIC:** EPIC-03
**Sprint:** 1
**Type:** QA
**Source:** BLG-QA-17, BLG-QA-15

**Acceptance Criteria:**
- Test scenario library document exists at `docs/qa/test_scenarios/research_view_scenarios.md` covering:
  - Data field rendering (price, change, market cap, ATR, regime, earnings)
  - Source attribution display (Yahoo Finance vs Alpaca)
  - News feed scenarios: articles present, none, Alpaca unavailable
  - Freshness indicator: fresh, stale (threshold exceeded)
  - Error states: ticker not found, Yahoo unavailable, all sources unavailable
  - Each scenario: precondition, action, expected result
- Acceptance test protocol document at `docs/qa/acceptance_protocols/research_view_protocol.md` covering:
  - Each PT-02 observable AC mapped to: Playwright (automated) or human staging sign-off
  - Freshness indicator acceptance threshold specified
  - Source attribution acceptance criteria specified
  - Error state test scenarios enumerated
- Both documents reviewed by Director of Quality before Sprint 2 begins

---

### ST-11 — Entry checklist Playwright E2E tests (BLG-QA-14)

**EPIC:** EPIC-03
**Sprint:** 1
**Type:** QA / Test Automation
**Source:** BLG-QA-14

**Acceptance Criteria:**
- `tests/e2e/entry-checklist.spec.js` created with 7 scenarios SC-CL-01 through SC-CL-07:
  - SC-CL-01: Checklist renders in Trade Plan form with 4 default items
  - SC-CL-02: Items can be toggled (checked/unchecked)
  - SC-CL-03: State persists on save
  - SC-CL-04: Pre-population — `stop_defined` pre-checked when `early_exit_conditions` present
  - SC-CL-05: Pre-population — `research_reviewed` pre-checked when `r_target` set
  - SC-CL-06: Review research link navigates to `/research/{ticker}`
  - SC-CL-07: Read-only checklist renders correctly in Research view trade plan panel
- All 7 scenarios pass in CI
- Scenarios registered in `execution_state.json test_scenarios` for EPIC-02 (v3.2 trade plan domain)
- No regression in existing test suite

---

### ST-12 — Research endpoint integration tests (BLG-QA-16) + latency baseline (BLG-OPS-15) + trade plan sensitivity classification (BLG-SEC-06) + field extension governance (BLG-GOV-20)

**EPIC:** EPIC-03
**Sprint:** 1
**Type:** QA + Operations + Governance
**Source:** BLG-QA-16, BLG-OPS-15, BLG-SEC-06, BLG-GOV-20

**Acceptance Criteria:**
- `backend/routers/test.py` includes test entry for `GET /research/{ticker}` (representative value: `AAPL`)
  - Scenarios: success, partial source failure, full failure
  - `SystemStatus.js` endpoint count updated if changed
- `docs/ops/api_performance_baseline.md` includes research endpoint latency entry:
  - p50/p95 values recorded (staging measurement or placeholder with methodology note)
  - Latency target documented: p95 ≤ 3s (multi-source external API aggregation rationale)
- `docs/specs/security/trade_plan_data_sensitivity.md` created covering:
  - Classification of all `trade_plans` fields: Public (ticker), Internal (dates, status), Private (entry zone, stop, R-target, thesis, checklist)
  - Access control principles per classification level
  - Referenced as input for any Arc 3/4 feature involving trade plan data exposure
  - Cybersecurity & Trust Lead sign-off
- `docs/governance/trade_plan_field_extension_policy.md` created covering:
  - Field addition criteria for trade_plans table vs separate table
  - Migration strategy requirement (when migration script required vs nullable add)
  - Backwards compatibility rules
  - Authority: Data Model owner + Product Owner approval for schema changes
  - Changelog format for schema changes
  - Data Model owner sign-off

---

## EPIC-04 — Governance Patches + Mandatory Quick Wins

**Maps to:** S2-04
**Owner:** PMO Lead + Head of Specs Team
**Sprint:** 1 (governance patches), 2 (BLG-FEAT-13 + quick wins)
**Theme:** OA resolution, mandatory feature flag, and UI quick wins

### ST-13 — execution_prompt.md governance patches: sealed-file check (OA-01/CF-01) + mock payload advisory (OA-02/CF-02)

**EPIC:** EPIC-04
**Sprint:** 1
**Type:** Governance / Prompt Engineering
**Source:** OA-01, OA-02, CF-01, CF-02 (v3.2 closure)

**Acceptance Criteria:**
- `execution_prompt.md` STEP 0 gains sealed-file integrity check:
  - At each EPIC session start, run `git diff --name-only HEAD` against sealed files (stage4_backlog_slice.md, release_plan.md, state.json for this cycle)
  - If any sealed file has staged or unstaged changes: halt with "[HALT] Sealed file modified: {filename}. Do not modify sealed artefacts. Revert changes before proceeding."
  - Hard gate — no bypass
- `execution_prompt.md` §14 Playwright Test Authoring Standard gains mock payload advisory:
  - "Mock payloads must match the canonical API spec response shape. Before authoring mocks, read the relevant openapi.yaml path and use the documented response schema. Nested objects (e.g. `{data: {field: value}}`) must not be flattened in mocks. Mismatch = silent test failure in prod."
- `OPERATIONAL_GUIDE.md` §14 version updated for execution_prompt
- `prompt_change_log.md` entry added (same commit)
- Version bump follows CLAUDE.md §6 checklist

---

### ST-14 — Governance policy patches: design gate "before sprint planning" check (OA-05) + backlog 3-cycle deferral policy (OA-03/CF-03)

**EPIC:** EPIC-04
**Sprint:** 1
**Type:** Governance / Prompt Engineering
**Source:** OA-03, OA-05, CF-03 (v3.2 closure)

**Acceptance Criteria:**
- `sprint_planning_prompt.md` STEP -1 (preflight) gains check for open "before sprint planning" backlog items:
  - Read active backlog for items with `Provisional-Target: Before vX.Y sprint planning` where vX.Y = current release
  - For each found item: surface as advisory — "⚠ Advisory: [N] 'before sprint planning' items found in backlog. These must be sprint stories (EPIC-03 or equivalent) before sprint planning seals."
  - Advisory only (not hard gate); recorded in sprint_planning_notes.md
- `backlog_management_prompt.md` gains 3-cycle deferral policy rule:
  - STEP 3.x added: during health check, flag any item deferred ≥ 3 consecutive cycles without a release assignment or named PO re-deferral
  - Named re-deferral format: "PO re-deferral YYYY-MM-DD: [reason]" appended to backlog item
  - Items without named re-deferral after 3rd consecutive deferral surfaced as health-check blockers
- Policy document `docs/governance/backlog_deferral_policy.md` created as a standalone reference (one page — criteria, re-deferral format, PO authority)
- `OPERATIONAL_GUIDE.md` §14 versions updated; `prompt_change_log.md` entry added; version bumps per CLAUDE.md §6

---

### ST-15 — PT-05 entry checklist §13 compliance review (BLG-GOV-19)

**EPIC:** EPIC-04
**Sprint:** 1
**Type:** Governance / §13 Compliance
**Source:** BLG-GOV-19

**Acceptance Criteria:**
- `docs/specs/compliance/pt05_entry_checklist_s13_review.md` created as a §13 boundary review document:
  - Confirms: entry checklist is display-only (user confirms each condition manually)
  - Confirms: no automated condition evaluation or recommendation generated
  - Confirms: system presents checklist items; human checks each one; system records checked state
  - Confirms: §13 boundary: the system does not determine whether entry conditions are met
  - Strategy Rules & System Intent Owner sign-off recorded in document
- Document referenced in trade plan spec (`docs/specs/frontend/pages/trade_plan.md`) as §13 compliance evidence for PT-05

---

### ST-16 — Feature flag rollout (BLG-FEAT-13) — mandatory

**EPIC:** EPIC-04
**Sprint:** 2
**Type:** Platform Feature
**Source:** BLG-FEAT-13 (mandatory v3.3 — 3rd consecutive deferral)

**Acceptance Criteria:**
- Feature flag schema defined: flag name (string), enabled (boolean), optional scope (env/user — default all)
- Flag evaluation mechanism: environment variable or config file (no external service dependency)
  - Format: `FEATURE_FLAGS=flag1:true,flag2:false` env var OR `feature_flags.json` config file
  - Evaluation: `is_flag_enabled(flag_name)` utility function returns bool
- Proof-of-concept: at least one v3.3 Arc 3 UI feature (e.g. position lifecycle state badge, EPIC-01 ST-03) wrapped behind a feature flag `arc3_lifecycle_display`
- Flag state auditable: logged at application startup (`INFO: Feature flags: arc3_lifecycle_display=true`)
- Pattern documented in `docs/specs/platform/feature_flags.md` (Class 2) covering: flag definition, evaluation mechanism, usage pattern, proof-of-concept example
- No regression in existing features when flag is disabled

---

### ST-17 — Trade plan abandonment + status badges (BLG-FEAT-21 + BLG-FE-30) + frontend quick wins (BLG-FE-23, BLG-FE-24, BLG-FE-25, BLG-FE-29)

**EPIC:** EPIC-04
**Sprint:** 2
**Type:** Product Feature + Frontend
**Source:** BLG-FEAT-21, BLG-FE-30, BLG-FE-23, BLG-FE-24, BLG-FE-25, BLG-FE-29

**Acceptance Criteria:**

*BLG-FEAT-21 — Trade plan abandonment status:*
- Trade plan status can be set to `Abandoned` via UI with a required abandonment reason (free text input)
- Backend: `status = 'abandoned'` transition allowed from Draft/Research states; Active positions linked to a plan cannot be abandoned (guard enforced, returns 400)
- `abandonment_reason` field added to trade_plans table (nullable varchar, required when status = abandoned — enforced at API layer)
- Abandoned plans appear in plan history with abandonment reason displayed
- No regression in existing plan status transitions

*BLG-FE-30 — Trade plan status badges:*
- Visual status badges for all trade plan statuses including new Abandoned state
- Colour scheme: Draft (grey), Research Pending (amber), Research Complete (blue), Entry Conditions Set (purple), Active (green), Closed (muted), Abandoned (red)
- Contrast ratio ≥ 4.5:1 for all badge colours
- Applied in trade plan list and detail views

*BLG-FE-23 — Research page UK ticker suffix:*
- `stripUkSuffix` applied to Research page header/title so `MTLN.L` displays as `MTLN`
- No regression in screener or watchlist UK suffix stripping

*BLG-FE-24 — Negative earnings days display:*
- When `days_until_earnings` is negative, all earnings columns display `—` not a negative number
- When zero: display `Today`; positive: unchanged

*BLG-FE-25 — Signals page default to most recent day:*
- Signals page defaults to most recent trading day's signals on load
- Control exists to view older signals (date picker or "Show all" toggle)
- If regression identified, root cause documented

*BLG-FE-29 — Watchlist research status indicator:*
- Watchlist table includes binary research status indicator per ticker row
- Done = research record exists for this ticker; Not Done = no research record
- Icon or badge only (no text, no quality/freshness signal)
- No regression in watchlist loading performance

---

## Release Summary

| EPIC | Sprint | Stories | Theme |
|------|--------|---------|-------|
| EPIC-01 | Sprint 1 | ST-01, ST-02, ST-03 | Arc 3 Foundation — Position Lifecycle Manager (IT-01) |
| EPIC-02 | Sprint 2 | ST-04, ST-05, ST-06, ST-07 | Arc 3 Decision Support — Grace Period + Stop Management (IT-02, IT-03) |
| EPIC-03 | Sprint 1 | ST-08, ST-09, ST-10, ST-11, ST-12 | Research View Spec & QA Closure |
| EPIC-04 | Sprint 1+2 | ST-13, ST-14, ST-15, ST-16, ST-17 | Governance Patches + Mandatory Quick Wins |

**Total: 17 stories / 4 EPICs / 2 sprints**
