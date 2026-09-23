Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-23
Cycle: 2026-09-23__release-v9.7
Release: v9.7

# Backlog Slice — v9.7

<!-- release-plan-marker: RP:v9.7:2026-09-23__release-v9.7 -->

29 stories across 7 grouped EPICs, 28.00 estimated days. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope set to the top of the confirmed ~24-28 day/sprint capacity band per explicit user "use full capacity" instruction (2026-09-23). Ready pool: 68 items / 61.35 days (after excluding 2 substantively gate-blocked items with no formal Gate field — BLG-FEAT-73/76 — and 1 item already resolved same-session — BLG-FE-189). Selection method: sole ready P1 item (BLG-FEAT-74, §13-cleared this week) seated first per §1.4c, then all 6 ready P2 items, then category-balanced round-robin oldest-first for remaining P3/P4 — per `release_planning_prompt.md` §1.4c. EPIC-01 leads the table as this cycle's flagship build-and-ship item. EPIC-01 and EPIC-02 items carry an observable UI acceptance criterion — `design_gate_required: true`.

---

## EPIC-01 — PO-05 Lightweight Replay Mode

**Maps to:** S2-01
**Owner:** Head of Engineering; Product Owner; Strategy Rules & System Intent Owner

### ST-01 — PO-05 Lightweight Replay Mode
**Source:** BLG-FEAT-74
**Priority:** P1
**Effort:** VH (>2 weeks)
**Notes:** VH effort (12.0d PO estimate) — phase as scope-confirmation sub-story (§13 binding conditions), then backend replay mechanics, then frontend selector/output view. See RISK-01.
**Acceptance Criteria:**
- User can select a historical date range or trade set and run it through paper-trading mechanics under current strategy rules
- Output is clearly labelled as retrospective/deterministic, not predictive
- §13 pre-clearance review completed and documented before sprint planning begins
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

---

## EPIC-02 — Frontend & UX Correctness

**Maps to:** S2-02, S2-03, S2-04, S2-05, S2-06, S2-07
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner

### ST-02 — Cloned trade plan can silently get the wrong Setup Type
**Source:** BLG-FE-186
**Priority:** P2
**Effort:** S (~0.5-1d)
**Acceptance Criteria:**
- A clone of a plan with Setup Type X shows X, including when the ticker has a watchlisted signal
- The design record and `trade_plan.md` state which fields a clone copies
- The new Playwright scenario passes in CI
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-03 — Monthly P&L's NULL-fee audit flag has no frontend surfacing
**Source:** BLG-FE-187
**Priority:** P2
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- A month with `null_fee_trade_count > 0` shows a visible indicator on the Monthly P&L page; a month with `0` does not
- Playwright test covering the above passes in CI
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-04 — Month-end P&L restatement diff has no frontend surfacing
**Source:** BLG-FE-188
**Priority:** P2
**Effort:** S (~1d)
**Acceptance Criteria:**
- A restated month shows its diff on the Monthly P&L page
- A tax year with `restated_month_count > 0` shows the notice on its summary bar
- Playwright tests covering both pass in CI
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-05 — AlertThresholdsSection.js empty-state heading has a trailing period, violating the empty-state microcopy pattern
**Source:** BLG-FE-178
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Empty-state heading renders `"No alert rules configured"` (no trailing period)
- Playwright coverage or a recorded staging run confirms the rendered heading, per CLAUDE.md's frontend-visible-change rule (wording-only — code review may substitute per the FI-P3-02 exception if genuinely no visual/layout change results)
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-06 — NotificationsHistory.js empty-state heading has a trailing period, violating the empty-state microcopy pattern
**Source:** BLG-FE-179
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Empty-state heading renders `"No alert history yet"` (no trailing period)
- Playwright coverage or a recorded staging run confirms the rendered heading, per CLAUDE.md's frontend-visible-change rule (wording-only — code review may substitute per the FI-P3-02 exception if genuinely no visual/layout change results)
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-07 — CI lint of static UI copy for forbidden predictive or advice-crossing phrases
**Source:** BLG-FE-183
**Priority:** P3
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- CI fails on a disallowed phrase in a new string literal
- Allow-list entries require a justification
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

---

## EPIC-03 — Backend Reliability & Financial Correctness

**Maps to:** S2-08, S2-09, S2-10, S2-11, S2-12, S2-13
**Owner:** Head of Engineering; Financial Reporting & Records Owner

### ST-08 — UK stamp duty / US FX fee rounding uses float `round()` instead of Decimal, under-rounding ~0.18%/0.02% of half-penny-boundary gross costs by £0.01
**Source:** BLG-BE-127
**Priority:** P2
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- All four fee functions round via `Decimal`/`ROUND_HALF_UP` instead of float `round()`
- The previously-documented discrepancy class (`tests/test_money_arithmetic_golden.py::TestKnownFloatDecimalDiscrepancies`) no longer reproduces — those tests are updated to assert the corrected value
- Full existing fee/sizing test suite still passes unchanged elsewhere (no other rounding behaviour regresses)

### ST-09 — Reflection reminder step: over-reported summary after a rollback, and NULL-portfolio trades never get a reminder
**Source:** BLG-BE-123
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- After a forced mid-loop failure the returned summary shows 0 created and 0 enqueued, and nothing was scheduled for rolled-back rows
- The NULL-portfolio behaviour is stated in `alerts_endpoints.md` and asserted by a test

### ST-10 — Generic alert re-delivery ignores read state
**Source:** BLG-BE-124
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A read notification is never re-enqueued for delivery, asserted by a test
- Unread, undelivered notifications are still retried up to 3 times (existing behaviour unchanged)

### ST-11 — Month-closure check and Monthly P&L's own SQL window use different clock sources
**Source:** BLG-BE-125
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A test asserts the same (year, month) tuple is used for both the SQL window and the closed-month check regardless of server timezone setting

### ST-12 — Monthly P&L snapshot lookup opens one DB connection per closed month
**Source:** BLG-BE-126
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `GET /reports/monthly-pnl` opens at most one additional connection (beyond the existing `get_monthly_pnl` call) regardless of how many closed months are in the response

### ST-13 — `latency_ms`/`elapsed_ms` recorded around retried Anthropic calls includes backoff sleep time, not just the final call's duration
**Source:** BLG-BE-129
**Priority:** P4
**Effort:** XS (<1h) — or "won't fix, document as intentional" is also a valid disposition
**Acceptance Criteria:**
- Either: a documented decision that the current combined-latency semantics are intentional and acceptable (no code change), or: `latency_ms` is split into a final-attempt-only figure and a total-including-retries figure, applied consistently across `ai_service.py`, `gemini_service.py`, and `debrief_service.py`

---

## EPIC-04 — QA & Test Coverage

**Maps to:** S2-14, S2-15, S2-16, S2-17, S2-18
**Owner:** Director of Quality

### ST-14 — The backend test suite can connect to a real database when DATABASE_URL is set to one
**Source:** BLG-QA-188
**Priority:** P2
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Running `backend/.venv/bin/python3 -m pytest tests/` with a real-looking `DATABASE_URL` and no opt-in makes zero real connections
- Phase B CI still runs `tests/test_schema.py` against its real Postgres with the opt-in set

### ST-15 — CI check flagging merged `.skip()`/`.only()` Playwright specs
**Source:** BLG-QA-174
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- CI check added and fires on a deliberately-introduced test case
- Exception mechanism documented

### ST-16 — Recurring pre-sprint endpoint test coverage audit
**Source:** BLG-QA-175
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Audit method documented
- First run completed; any gap found filed as its own item (e.g. this cycle's own `BLG-OPS-156` is an example of the same class of gap, caught at post-ship instead — this item would catch it earlier)

### ST-17 — Backfill negative-path tests for the 3 newest v9.2/v9.3 routers
**Source:** BLG-QA-176
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- 3 routers identified
- Negative-path tests added and passing for each

### ST-18 — Validate `get_claude_endpoint_cost_windows()` SQL against a real Postgres instance
**Source:** BLG-QA-177
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- The query has been run at least once against a real or synthetic Postgres instance with confirmed-correct recent/baseline window boundaries, or a new test exists that executes the real (non-stubbed) `get_claude_endpoint_cost_windows()` and asserts its output shape/values

---

## EPIC-05 — Governance & Process Debt

**Maps to:** S2-19, S2-20, S2-21, S2-22
**Owner:** PMO Lead; Head of Specs Team

### ST-19 — Quarterly "governance overhead ratio" metric
**Source:** BLG-GOV-327
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- Metric defined in a canonical spec (likely `metrics_definitions.md`)
- First baseline reading recorded

### ST-20 — Review whether the SI-02 gate threshold should scale with observed trade cadence
**Source:** BLG-GOV-330
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Disposition recorded: re-examine (with new analysis) or confirm-closed (citing `BLG-GOV-237`, no new information)

### ST-21 — Document ensure_ascii=False convention for governance JSON writes
**Source:** BLG-GOV-331
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- Convention documented somewhere a future governance-JSON writer (agent or human) would see it before writing

### ST-22 — Reconcile sprint_planning_prompt.md STEP -1 status-vocabulary wording against shared_standards.md §10.1
**Source:** BLG-GOV-333
**Priority:** P3
**Effort:** XS (~0.5–1h)
**Acceptance Criteria:**
- STEP -1 Hard Gates 1–2 no longer contain a literal status enum independent of `shared_standards.md §10.1`
- Next `plan sprint` invocation's preflight reads cleanly with no drift advisory needed
- Head of Specs Team sign-off

---

## EPIC-06 — Spec & Data Model Debt

**Maps to:** S2-23, S2-24, S2-25, S2-26
**Owner:** Head of Specs Team; Data Model & Domain Schema Owner

### ST-23 — Formal definition of "linked trade plan" counting for the SI-02 gate
**Source:** BLG-SPEC-147
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Canonical definition exists
- `current_roadmap.md` SI-02 field cross-references it

### ST-24 — positions.exit_note documented in data_model.md does not exist on live table
**Source:** BLG-SPEC-149
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `data_model.md`'s Positions Table section no longer claims a live `exit_note` column that doesn't exist

### ST-25 — 4 orphaned, always-NULL, undocumented columns on live positions table
**Source:** BLG-SPEC-150
**Priority:** P3
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- Disposition recorded (drop vs document) with supporting evidence
- `data_model.md` and the live schema agree on every `positions` column, one way or the other

### ST-26 — positions.fees_paid documented as NOT NULL but live column is nullable
**Source:** BLG-SPEC-151
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `data_model.md` and the live schema agree on `fees_paid` nullability

---

## EPIC-07 — Ops, Security & Verification

**Maps to:** S2-27, S2-28, S2-29
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead

### ST-27 — Post-deploy staging verification of the reflection-reminder migration and SQL (never run against a live database)
**Source:** BLG-OPS-168
**Priority:** P2
**Effort:** XS (<1h)
**Notes:** Requires a real (non-mocked) DB/SQL run — route to Infrastructure & Operations Owner for a delegated staging slot; code review alone does not satisfy this AC. See RISK-03.
**Acceptance Criteria:**
- Both CHECK constraints and `uq_notifications_reflection_reminder_trade` are confirmed present on staging, with evidence recorded
- A second evaluation run creates 0 duplicate reminders
- The look-back and close-timestamp decisions are recorded

### ST-28 — External-dependency failure-mode matrix (yfinance, Alpaca, Anthropic, Supabase, Render)
**Source:** BLG-OPS-167
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- All 5 dependencies documented

### ST-29 — CI guard rejecting non-registry dependency specifiers (git+ssh, git+https, file:)
**Source:** BLG-SEC-38
**Priority:** P4
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A test PR adding a `git+ssh` dependency fails CI

---