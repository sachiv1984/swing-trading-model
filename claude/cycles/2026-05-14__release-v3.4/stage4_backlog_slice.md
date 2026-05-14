**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.4
**Cycle:** 2026-05-14__release-v3.4
**Published:** 2026-05-14

---

# Backlog Slice — v3.4 Arc 3 In-Trade Risk Management (continued)

**Theme:** Arc 3 Frontend Completion + IT-04/05 Risk Prompts + Frontend Quick Wins + Spec/QA Debt
**Stories:** 14 | **EPICs:** 4 | **Sprints:** 2
**Capacity verdict:** WARN (11 days estimated vs ~10–13 available)

---

## EPIC-01 — Arc 3 Frontend Completion

**Maps to:** S2-01
**Sprint:** 2
**Owner:** Head of Engineering
**Dependency:** BLG-FE-31 (component library, EPIC-04 ST-11) recommended first; UX specs from v3.3 design gate available
**Sequencing:** Implement after Sprint 1 so component library reference (ST-11) is available

---

### ST-01 — Position lifecycle state: frontend display (IT-01)

**EPIC:** EPIC-01
**Sprint:** 2
**Priority:** P1
**Source:** Returned to backlog from v3.3 ST-03 (DEL-20260510-01); backed by `docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md`
**Effort:** M (~1–1.5 days)

**Context:**
Backend is complete: `position_lifecycle_service.py`, DS-05 migration, enriched `GET /positions` response, `arc3_lifecycle_display` feature flag all live on main. The React badge component displaying GRACE / PROFITABLE / LOSING / EXIT ZONE / UNKNOWN states is pending.

**Acceptance Criteria:**
- [ ] Positions page renders a lifecycle state badge per position row when `arc3_lifecycle_display` feature flag is ON
- [ ] Badge displays: GRACE (yellow), PROFITABLE (green), LOSING (red), EXIT ZONE (purple), UNKNOWN (grey)
- [ ] `days_in_state` displayed alongside GRACE state badge
- [ ] Feature flag OFF → no badge rendered (no regression to existing positions display)
- [ ] Playwright E2E scenarios present before PR merge: SC-LS-01, SC-LS-02, SC-LS-03, SC-LS-04 (from TEST-GAP-EPIC-01-v33 in backlog)
- [ ] No regression in positions page loading performance or existing columns

**Backend contract:** `GET /positions` returns `lifecycle_state`, `days_in_state` per position — already live
**UX spec:** `docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md`
**Feature flag:** `arc3_lifecycle_display`

---

### ST-02 — Grace Period Decision Support frontend (IT-02)

**EPIC:** EPIC-01
**Sprint:** 2
**Priority:** P1
**Source:** Returned to backlog from v3.3 ST-05 (DEL-20260510-02); §13 display-only alert card
**Effort:** M (~1 day)

**Context:**
Backend is complete: `GET /positions/grace-period-alerts` is live on main. The alert card UI (dismissible via localStorage, links to trade plan, display-only) is pending.

**Acceptance Criteria:**
- [ ] Alert card renders when a position is in GRACE state ≥ day 8 (returned by `GET /positions/grace-period-alerts`)
- [ ] Card displays: ticker, `days_in_state`, link to associated trade plan (if PT-01 exists)
- [ ] Dismiss button removes card for the session; on app reload, card re-appears if position still qualifies (localStorage used to persist dismissal until next day)
- [ ] §13 compliance: card is display-only — no automated action taken; user must confirm/dismiss
- [ ] Playwright E2E scenarios present before PR merge: SC-GP-01, SC-GP-02, SC-GP-03 (from TEST-GAP-EPIC-02-v33)
- [ ] No regression in positions page or trade plan navigation

**Backend contract:** `GET /positions/grace-period-alerts` — already live
**UX spec:** `docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md`

---

### ST-03 — Stop Management Workflow frontend (IT-03)

**EPIC:** EPIC-01
**Sprint:** 2
**Priority:** P1
**Source:** Returned to backlog from v3.3 ST-07 (DEL-20260510-03); §13 guided panel requiring user confirmation
**Effort:** M (~1 day)

**Context:**
Backend is complete: `GET /positions/{id}/stop-trail` is live on main. The guided panel with Trail Stop button, current stop / ATR trail stop / difference / R-terms display, and confirm/cancel interaction is pending.

**Acceptance Criteria:**
- [ ] Trail Stop button appears per PROFITABLE or EXIT ZONE position row where `current_stop` is set
- [ ] Clicking Trail Stop opens a guided panel showing: current stop, ATR trail stop (calculated), difference in price terms, difference in R-terms
- [ ] Panel has explicit Confirm and Cancel buttons — §13 compliance: no automatic stop update; user must click Confirm
- [ ] On Confirm, executes the stop update (or navigates to stop update flow) — scoped to guided confirmation only
- [ ] Playwright E2E scenarios present before PR merge: SC-TS-01, SC-TS-02, SC-TS-03 (from TEST-GAP-EPIC-02-v33)
- [ ] No regression in positions table or stop price display

**Backend contract:** `GET /positions/{id}/stop-trail` — already live
**UX spec:** `docs/design/2026-05-09__release-v3.3/stop-trail-panel/ux_spec.md`

---

## EPIC-02 — Arc 3 Risk Prompts: Drawdown Review & Concentration Limits

**Maps to:** S2-02, S2-03
**Sprint:** 2
**Owner:** Head of Engineering
**Dependency:** Design gate clearance required (Phase 1.5) — IT-04/05 UX specs must exist before sprint planning seals
**Sequencing:** Sprint 2; design gate produces UX specs before sprint planning

---

### ST-04 — Drawdown-Triggered Review Prompt backend (IT-04)

**EPIC:** EPIC-02
**Sprint:** 2
**Priority:** P2
**Source:** Arc 3 roadmap IT-04; no existing backend
**Effort:** M (~1.5 days)

**Acceptance Criteria:**
- [ ] `GET /portfolio/drawdown-status` endpoint returns: current drawdown % from portfolio peak, threshold (default 10%, configurable per user settings), `threshold_breached` boolean
- [ ] Drawdown % calculated as: `(portfolio_peak_value - current_value) / portfolio_peak_value * 100`; portfolio peak = highest recorded total value in last 30 trading days
- [ ] Threshold configurable via existing settings infrastructure; default 10%; valid range 5–50%
- [ ] When threshold breached, endpoint also returns: open positions by lifecycle state (counts), current portfolio heat %, current regime status (bull/bear/neutral if available)
- [ ] Endpoint registered in `backend/routers/test.py`; hardcoded fallback count in `SystemStatus.js` updated
- [ ] Endpoint added to `docs/reference/openapi.yaml` in same commit as contract

---

### ST-05 — Drawdown-Triggered Review Prompt frontend (IT-04)

**EPIC:** EPIC-02
**Sprint:** 2
**Priority:** P2
**Source:** Arc 3 roadmap IT-04; §13 compliant — structured prompt, no automated action
**Effort:** M (~1 day)
**Design gate dependency:** UX spec required from Phase 1.5 before implementation

**Acceptance Criteria:**
- [ ] Structured review prompt visible on positions page or portfolio summary when `GET /portfolio/drawdown-status` returns `threshold_breached: true`
- [ ] Prompt displays: current drawdown %, breach threshold, open positions by state (counts), portfolio heat %, regime status
- [ ] §13 compliance: prompt is display-only — no automated position changes; user reviews and dismisses
- [ ] Dismissal persists until next drawdown recalculation exceeds threshold again (not localStorage — server-side acknowledgement or session-scoped)
- [ ] Playwright E2E test coverage or human staging sign-off recorded in DoQ before PR merge
- [ ] UX spec from design gate referenced in PR description

---

### ST-06 — Position Concentration Limits (IT-05 — backend + frontend)

**EPIC:** EPIC-02
**Sprint:** 2
**Priority:** P2
**Source:** Arc 3 roadmap IT-05; uses DS-03 sector data (shipped v2.9)
**Effort:** S (~1 day combined backend + frontend)
**Design gate dependency:** UX spec for warning UI required from Phase 1.5

**Acceptance Criteria:**
- [ ] Backend: `GET /portfolio/concentration-status` returns: per-position heat % of portfolio, sector concentration % per sector (using DS-03 sector field), any positions/sectors exceeding configurable thresholds
- [ ] Single-position threshold: configurable, default 15% of portfolio heat; sector concentration threshold: configurable, default 30%
- [ ] Frontend: warning indicator on positions page or portfolio summary when any threshold is breached; lists breaching positions/sectors
- [ ] DS-03 sector data used where available; graceful degradation when sector data absent (no warning for positions without sector)
- [ ] Thresholds configurable via settings; validated range 5–50% for single-position; 10–80% for sector
- [ ] Playwright E2E test coverage or human staging sign-off recorded before PR merge
- [ ] New endpoints registered in `backend/routers/test.py` and `openapi.yaml`

---

## EPIC-03 — Frontend Quick Wins

**Maps to:** S2-04
**Sprint:** 1
**Owner:** Head of Engineering
**Sequencing:** Sprint 1 — independent quick wins; front-loaded per LL-v3.3 carry-forward item 1

---

### ST-07 — Research page UK suffix strip + negative earnings days display (BLG-FE-23 + BLG-FE-24)

**EPIC:** EPIC-03
**Sprint:** 1
**Priority:** P3
**Source:** BLG-FE-23 (DEV-E01-03, v3.2 staging), BLG-FE-24 (v3.2 staging) — bundled as both are XS effort
**Effort:** XS (~0.5 day combined)

**Acceptance Criteria (BLG-FE-23):**
- [ ] Research page title/header strips `.L` suffix from UK tickers using existing `stripUkSuffix` utility
- [ ] `MTLN.L` displays as `MTLN` in the Research page header
- [ ] No regression in screener or watchlist UK suffix stripping

**Acceptance Criteria (BLG-FE-24):**
- [ ] When `days_until_earnings` is negative (past earnings date), display `—` in all earnings columns (screener, watchlist, research, positions)
- [ ] When `days_until_earnings` is zero: display `Today`
- [ ] When `days_until_earnings` is positive: display the number (unchanged from current behaviour)
- [ ] No regression in earnings proximity warning (≤5 days amber)

---

### ST-08 — Signals page: default to most recent day's signals (BLG-FE-25)

**EPIC:** EPIC-03
**Sprint:** 1
**Priority:** P2
**Source:** BLG-FE-25 (v3.2 staging observation)
**Effort:** S (~0.5 day)

**Acceptance Criteria:**
- [ ] Signals page defaults to displaying only the most recent trading day's signals on load
- [ ] A control exists to view older signals (e.g. date picker or "Show all" toggle)
- [ ] If this is a regression, root cause identified and documented in PR description
- [ ] No regression in signal data accuracy or existing Playwright tests

---

### ST-09 — Watchlist research status indicator (BLG-FE-29)

**EPIC:** EPIC-03
**Sprint:** 1
**Priority:** P2
**Source:** BLG-FE-29 (DL-025, 2026-05-08)
**Effort:** XS (~0.5 day)

**Acceptance Criteria:**
- [ ] Watchlist table includes a Research Status indicator per ticker row (icon or badge — not text label)
- [ ] Done = research record exists for this ticker in the research data store
- [ ] Not Done = no research record found
- [ ] Binary only — no research quality score, no freshness signal (scope constraint)
- [ ] No regression in watchlist loading performance or existing columns

---

### ST-10 — Trade plan status badges + abandonment UI (BLG-FE-30 + BLG-FEAT-21 frontend)

**EPIC:** EPIC-03
**Sprint:** 1
**Priority:** P2
**Source:** BLG-FE-30 (DL-025, 2026-05-08); BLG-FEAT-21 frontend (v3.3 ST-17 partial — backend DS-06 + abandonment API live)
**Effort:** S (~1 day combined)

**Context:**
Trade plan abandonment backend is live (DS-06 migration + `PUT /trade-plans/{id}` abandonment guard shipped v3.3 ST-17). This story delivers the frontend: abandonment UI + status badges for all states.

**Acceptance Criteria (BLG-FE-30 — status badges):**
- [ ] Status badges rendered in trade plan list view and trade plan detail view header for all states: Draft, Research Pending, Research Complete, Entry Conditions Set, Active, Closed, Abandoned
- [ ] Colour coding: grey (Draft), amber (Research Pending), blue (Research Complete), purple (Entry Conditions Set), green (Active), muted (Closed), red (Abandoned)
- [ ] Each status has distinct, accessible colour (contrast ratio ≥ 4.5:1)
- [ ] Colours aligned with design system tokens (`docs/frontend/design_system.md`)
- [ ] No regression in trade plan list rendering performance

**Acceptance Criteria (BLG-FEAT-21 frontend — abandonment UI):**
- [ ] Trade plan can be set to Abandoned status via UI with a required reason (free text input)
- [ ] Abandoned plans appear in plan history with abandonment reason displayed
- [ ] Active positions linked to a plan cannot be abandoned (guard enforced — backend already blocks via `PUT /trade-plans/{id}`)
- [ ] No regression in existing plan status transitions (Draft → Research Pending → ... → Active → Closed)

---

## EPIC-04 — Spec, QA & Documentation Debt

**Maps to:** S2-05
**Sprint:** 1
**Owner:** Head of Specs Team
**Sequencing:** Sprint 1; ST-11 (component library) first — required before EPIC-01 implementation begins

---

### ST-11 — Research view component library (BLG-FE-31)

**EPIC:** EPIC-04
**Sprint:** 1
**Priority:** P3
**Source:** BLG-FE-31 (DL-028, 2026-05-13)
**Effort:** S (~0.5 day)

**Context:**
PT-02 research view shipped v3.2 with reusable UI components. Arc 3 frontend (EPIC-01 ST-01/02/03) will extend or reuse these. This story catalogues them before implementation begins.

**Acceptance Criteria:**
- [ ] Catalogue document covers all major PT-02 research view UI components: price card, regime/signal panel, news feed, source attribution row, freshness indicator
- [ ] Each entry includes: component name, file path, key props, known variants
- [ ] Reuse candidates for ST-01/02/03 (EPIC-01) explicitly noted
- [ ] Scope constraint: PT-02 research view components only — not a full application inventory
- [ ] Delivered (merged) before EPIC-01 sprint execution begins
- [ ] Document stored in appropriate location (e.g. `docs/frontend/component_library_research_view.md`)

---

### ST-12 — Screener morning routine UX spec (BLG-FE-22)

**EPIC:** EPIC-04
**Sprint:** 1
**Priority:** P2
**Source:** BLG-FE-22 (DL-024, 2026-05-05); Provisional-Target v3.2 then v3.4 — 2 cycles unassigned (age advisory triggered at §1.1)
**Effort:** S (~0.5 day)

**Acceptance Criteria:**
- [ ] UX workflow spec documents the step-by-step morning routine: screener results → shortlist → watchlist promotion → pre-trade research navigation
- [ ] Information-carry decisions documented: what data from screener is visible in research view
- [ ] Navigation model specified: how user moves between screener, watchlist, and research views
- [ ] Format: workflow and information-carry spec (not wireframes/mockups)
- [ ] Owner: Frontend Specifications & UX Documentation Owner sign-off in document header

---

### ST-13 — trade_plan.md §6.2 spec update + AI journal review cadence (BLG-SPEC-28 + BLG-AI-03)

**EPIC:** EPIC-04
**Sprint:** 1
**Priority:** P3
**Source:** BLG-SPEC-28 (v3.3 ST-11 deviation, P3), BLG-AI-03 (DL-025, 2026-05-08) — bundled as both are XS
**Effort:** XS (~0.5 day combined)

**Acceptance Criteria (BLG-SPEC-28):**
- [ ] `trade_plan.md` §6.2 entry checklist pre-population rules updated:
  - `stop_defined`: pre-checked when `early_exit_conditions` is present (not `stop_level`)
  - `research_reviewed`: pre-checked when `r_target` is set (not `risk_reward_notes`)
- [ ] Cross-reference to `entry-checklist.spec.js` test scenarios noted in spec
- [ ] Head of Specs Team sign-off recorded in document header

**Acceptance Criteria (BLG-AI-03):**
- [ ] Quarterly review process for AI Journal Summarisation defined and documented
- [ ] Review checklist specifies observable criteria: output quality sample, §13 compliance re-confirmation, BLG-AI-02 model version contract update, error rate review
- [ ] Process documented with named authority (AI Compliance & Governance Officer) and escalation path if §13 concerns arise
- [ ] Document stored in appropriate governance location; OPERATIONAL_GUIDE references the review process

---

### ST-14 — Screener accuracy test protocol (BLG-QA-18)

**EPIC:** EPIC-04
**Sprint:** 1
**Priority:** P2
**Source:** BLG-QA-18 (DL-027, 2026-05-13); before any sprint touching screener filter logic
**Effort:** S (~0.5 day)

**Acceptance Criteria:**
- [ ] Formal accuracy test protocol document produced (Owner: Director of Quality)
- [ ] Protocol specifies observable, measurable acceptance criteria
- [ ] Minimum sample: tickers with known regime, ATR, signal values — expected include/exclude outcome documented
- [ ] Protocol executable by QA & Testing Owner using BLG-QA-08 mock harness
- [ ] `strategy_rules.md §11` parameters (regime gate, ATR multipliers, signal threshold) explicitly referenced
- [ ] Boundary cases included: regime gate pass/fail, ATR threshold boundary, signal score threshold edge cases
