**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.6
**Cycle:** 2026-05-30__release-v4.6
**Published:** 2026-05-30

---

# Stage 4 Backlog Slice — v4.6

---

## EPIC-01 — SI-02 Behavioural Drift Detection: Backend (S2-01)

**Owner:** Head of Backend Engineering; Data Model & Domain Schema Owner
**Maps to:** S2-01
**Sprint:** Sprint 1
**Sequencing:** Before EPIC-02; data density audit (ST-16 in EPIC-04) must confirm ≥20 closed trades before EPIC-02 sprint planning seals
**Description:** Full backend implementation of SI-02 Behavioural Drift Detection. Covers the DS-07 data migration (5 columns + 3 indexes), POST /trade-plans capture updates, drift detection service (4 metrics per si02_drift_score.md v1.0), the GET /analytics/behavioural-drift endpoint, and the full unit test suite. §13 PASS confirmed (9 binding conditions). All pre-planning docs present.

---

### ST-01 — DS-07 data migration: add SI-02 columns to trade_plans

**Backlog ref:** si02_data_schema.md v1.0 (EPIC-03 ST-08 v4.5)
**Priority:** P1 (High)
**Effort:** M (~3–4 hrs)
**Owner:** Data Model & Domain Schema Owner; Head of Backend Engineering
**EXECUTION:** autonomous
**VERIFICATION:** staging (migration runs cleanly; 5 columns present in trade_plans; indexes created)

**References:** `docs/specs/data_model/si02_data_schema.md §4–§6`

**Acceptance Criteria:**
- [ ] AC-01: Migration file created: adds 5 nullable columns to `trade_plans` — `signal_id UUID REFERENCES signals(id) ON DELETE SET NULL`, `risk_percent_used NUMERIC(4,2)`, `portfolio_value_at_entry NUMERIC(12,2)`, `pre_entry_validation_snapshot JSONB`, `effective_settings_snapshot JSONB`
- [ ] AC-02: P1 index created within the same migration (inside transaction): `CREATE INDEX CONCURRENTLY idx_trade_plans_signal ON trade_plans(signal_id) WHERE signal_id IS NOT NULL` — or split into separate file if migration runner requires CONCURRENTLY outside transaction (per data schema §6 note)
- [ ] AC-03: Separate migration file for P2 indexes (outside transaction, CONCURRENTLY): `idx_trade_history_exit_date ON trade_history(portfolio_id, exit_date DESC)` and `idx_trade_history_entry_date ON trade_history(portfolio_id, entry_date DESC)`
- [ ] AC-04: Migration is fully reversible (DROP COLUMN, DROP INDEX documented in comment)
- [ ] AC-05: Migration applied cleanly on staging; all 5 columns present in trade_plans; `\d trade_plans` confirms schema; all 3 indexes created
- [ ] AC-06: No existing records broken (nullable columns, zero-row backfill)
- [ ] AC-07: Data Model & Domain Schema Owner sign-off recorded in QA evidence

---

### ST-02 — POST /trade-plans: capture 5 new SI-02 fields at plan creation

**Backlog ref:** si02_data_schema.md §7 (Capture Responsibility Summary)
**Priority:** P1 (High)
**Effort:** M (~3–4 hrs)
**Owner:** Head of Backend Engineering
**EXECUTION:** autonomous
**VERIFICATION:** unit test + staging (new fields persisted in trade_plans on plan creation)

**References:** `docs/specs/data_model/si02_data_schema.md §7`

**Acceptance Criteria:**
- [ ] AC-01: `POST /trade-plans` handler updated — backend captures `risk_percent_used` from the sizing calculator result in the request body (if provided)
- [ ] AC-02: Backend captures `portfolio_value_at_entry` — queries `portfolio_history` for most recent `total_value` at plan creation time and stores in trade plan record
- [ ] AC-03: Backend captures `effective_settings_snapshot` — at plan creation, reads current `settings` row and stores JSONB: `{default_risk_percent, atr_multiplier_initial, atr_multiplier_trailing, min_hold_days, captured_at}`
- [ ] AC-04: Frontend is expected to pass `signal_id` and `pre_entry_validation_snapshot` in the POST body when available; backend persists both without validation (nullable — may be absent from body)
- [ ] AC-05: All capture is additive and backward-compatible — existing plan creation flows with missing fields succeed without error
- [ ] AC-06: Unit test: `POST /trade-plans` with all 5 fields in body → verify all stored in DB
- [ ] AC-07: Unit test: `POST /trade-plans` with no new fields → verify plan created successfully (backwards compat)
- [ ] AC-08: Head of Backend Engineering sign-off recorded in QA evidence

---

### ST-03 — SI-02 behavioural drift detection service (4 metrics)

**Backlog ref:** Arc 5 SI-02 (roadmap); `docs/specs/metrics/si02_drift_score.md` v1.0
**Priority:** P1 (High)
**Effort:** H (~1–1.5 days)
**Owner:** Head of Backend Engineering
**EXECUTION:** autonomous
**VERIFICATION:** unit tests pass; staging health check confirms endpoint responds
**§13 gate:** PASS (9 binding conditions; `docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md`)

**References:** `docs/specs/metrics/si02_drift_score.md §2–§4`

**Acceptance Criteria:**
- [ ] AC-01: `behavioural_drift_service.py` created in `backend/services/` — computes 4 drift metrics: `entry_timing_drift`, `sizing_adherence`, `consecutive_loss_sizing`, `regime_context`
- [ ] AC-02: Analysis window: 90-day rolling window; minimum trade threshold: 10 closed trades (returns `status: "insufficient_data"` with no metric values if below)
- [ ] AC-03: `entry_timing_drift` — AVG(positions.entry_date - signals.signal_date) for trades with `signal_id IS NOT NULL` in the 90-day window; unit: days; thresholds: green ≤0.80, amber 0.80–1.00, red >1.00; advisory note counts excluded trades
- [ ] AC-04: `sizing_adherence` — AVG(trade_plans.risk_percent_used) for trades in the 90-day window; reference: `settings.default_risk_percent` (or `effective_settings_snapshot` if present); thresholds: green ≤plan_max×0.80, amber plan_max×0.80–plan_max, red >plan_max; under-sizing advisory (<plan_max×0.50) as separate note
- [ ] AC-05: `consecutive_loss_sizing` — AVG(risk_percent_used) for trades entered after ≥2 consecutive closed losing trades in the 90-day window; minimum 3 qualifying trades required (null + insufficient_data for metric if below); thresholds: green ≤plan_max×0.80, amber plan_max×0.80–plan_max, red >plan_max
- [ ] AC-06: `regime_context` — pct of trades entered with `regime_context_at_entry IN ('risk_on', 'neutral', null)` in the 90-day window; direction: gte (higher is better); thresholds: green ≥95%, amber 90–95%, red <90%
- [ ] AC-07: Each metric returns: `metric_id`, `label`, `measured_value`, `unit`, `status` (ok/approaching/breached/insufficient_data), `threshold_value`, `deviation_pct`, `advisory_note` (nullable)
- [ ] AC-08: Top-level endpoint status: `insufficient_data` if <10 trades; `no_drift` if all metrics ok; `drift_detected` if any metric approaching/breached; `error` on computation failure
- [ ] AC-09: §13 binding conditions enforced: output is display-only metrics; no automated recommendations; no ML inference; all formulas deterministic
- [ ] AC-10: Head of Backend Engineering sign-off recorded in QA evidence

---

### ST-04 — GET /analytics/behavioural-drift endpoint, openapi.yaml, API contract

**Backlog ref:** Arc 5 SI-02; CLAUDE.md §2 (same-commit endpoint documentation rule)
**Priority:** P1 (High)
**Effort:** M (~3–4 hrs)
**Owner:** Head of Backend Engineering; API Contracts Documentation Owner
**EXECUTION:** autonomous
**VERIFICATION:** unit test returns 200 with correct schema; openapi.yaml updated; API contract doc present

**Acceptance Criteria:**
- [ ] AC-01: `GET /analytics/behavioural-drift` endpoint added to `backend/routers/analytics.py` (or equivalent analytics router) — calls `behavioural_drift_service.py`; returns full drift response for the authenticated portfolio
- [ ] AC-02: Response schema: `{status, analysis_window_days: 90, trade_count_in_window, metrics: [{metric_id, label, measured_value, unit, status, threshold_value, deviation_pct, advisory_note}], computed_at}`
- [ ] AC-03: `GET /analytics/behavioural-drift` added to `docs/reference/openapi.yaml` in the same commit as the endpoint (CLAUDE.md §2 requirement)
- [ ] AC-04: API contract document created or updated in `docs/specs/api_contracts/` covering `GET /analytics/behavioural-drift` with all response fields documented (CLAUDE.md §2 same-sprint contract requirement) — `## GET /analytics/behavioural-drift` heading at `##` level
- [ ] AC-05: Endpoint registered in `backend/routers/test.py` (hardcoded count updated + SC-SS-01b updated in `tests/e2e/system-status.spec.js` if applicable per CLAUDE.md §2)
- [ ] AC-06: Returns `200` with `status: "insufficient_data"` when <10 trades; returns `200` with `status: "no_drift"` or `"drift_detected"` with metrics when data is sufficient
- [ ] AC-07: Returns `401` if unauthenticated
- [ ] AC-08: API Contracts Documentation Owner sign-off recorded in QA evidence

---

### ST-05 — SI-02 unit test suite

**Backlog ref:** Arc 5 SI-02; §13 binding conditions
**Priority:** P1 (High)
**Effort:** M (~4 hrs)
**Owner:** QA Lead; Head of Backend Engineering
**EXECUTION:** autonomous
**VERIFICATION:** all unit tests pass in CI

**Acceptance Criteria:**
- [ ] AC-01: Unit tests created for `behavioural_drift_service.py` covering all 4 metrics in isolation
- [ ] AC-02: Test cases: sufficient data returns correct metric values; insufficient data (< 10 trades) returns `status: "insufficient_data"`; `entry_timing_drift` excludes trades without signal_id and counts exclusions in advisory_note; `sizing_adherence` correct for over-sizing (red), approaching (amber), and within (green)
- [ ] AC-03: `consecutive_loss_sizing` test: correctly identifies trades after ≥2 consecutive losses; insufficient post-loss trades returns null for this metric only (not the full endpoint)
- [ ] AC-04: `regime_context` test: correctly counts risk_on + neutral as valid; risk_off as drift; null regime_context_at_entry counted as neutral (not a violation)
- [ ] AC-05: §13 binding condition tests: verify no automated recommendations in response; output contains only display values; `error` status on computation failure does not expose internal details
- [ ] AC-06: If new `database` functions imported in `backend/services/position_service.py` or related: `_DB_STUB_FUNCTIONS` list in `tests/conftest.py` updated (CLAUDE.md §2 rule)
- [ ] AC-07: All tests pass in CI; coverage ≥17 test cases total for SI-02 service
- [ ] AC-08: QA Lead sign-off recorded in QA evidence

---

## EPIC-02 — SI-02 Behavioural Drift Detection: Frontend (S2-02)

**Owner:** Base44 Frontend; QA Lead
**Maps to:** S2-02
**Sprint:** Sprint 2
**Sequencing:** After EPIC-01 merged to main; data density gate (ST-16 result) confirmed by Product Owner before Sprint 2 EPIC-02 planning seals
**Gate condition:** Product Owner confirms ≥20 closed trades with linked trade_plans (per ST-16 BLG-GOV-33 audit result) before EPIC-02 sprint planning seals. If gate not met, EPIC-02 is deferred and Sprint 2 closes with EPIC-03 only.
**Description:** Frontend implementation of SI-02. BehaviouralDriftPanel component displaying all 4 drift metrics with ok/approaching/breached visual treatment, integrated into PerformanceAnalytics or Arc 5 compliance section. Playwright test coverage. Design informed by BLG-FE-52/53 pre-design (v4.4); `si02_fe_component_predesign.md` is the authoritative frontend spec.

---

### ST-06 — BehaviouralDriftPanel component

**Backlog ref:** BLG-FE-52 (component pre-design, v4.4); BLG-FE-53 (v4.4); `si02_fe_component_predesign.md`
**Priority:** P1 (High)
**Effort:** H (~4–6 hrs)
**Owner:** Base44 Frontend
**EXECUTION:** autonomous
**VERIFICATION:** staging visual (panel renders with all 4 metrics, correct colour coding, advisory notes display)

**Acceptance Criteria:**
- [ ] AC-01: `BehaviouralDriftPanel.js` component created — calls `GET /analytics/behavioural-drift`; displays overall status badge (`no_drift` / `drift_detected` / `insufficient_data`)
- [ ] AC-02: Each of the 4 metrics displayed as a card or row: label, measured value + unit, status indicator (green/amber/red), deviation_pct display, threshold value reference
- [ ] AC-03: Status visual treatment: green (`ok`) = green indicator; amber (`approaching`) = amber/yellow indicator; red (`breached`) = red indicator — consistent with existing Arc 5 SI-01 PreEntryValidationPanel colour pattern
- [ ] AC-04: `advisory_note` displayed when status is `approaching` or `breached` (inline text below the metric row)
- [ ] AC-05: `insufficient_data` state: panel displays "Insufficient data — drift analysis requires 10 or more closed trades in the last 90 days. Currently X trades recorded." with the trade_count_in_window from the response
- [ ] AC-06: Loading state displayed while API call in progress; error state on API failure
- [ ] AC-07: `computed_at` timestamp displayed in panel footer (e.g., "Drift analysed as of: [date]")
- [ ] AC-08: Component design aligns with `si02_fe_component_predesign.md §5` (percentage deviation display format confirmed in metric spec §2.3)
- [ ] AC-09: Head of UX & Design sign-off or staging visual QA recorded in QA evidence

---

### ST-07 — BehaviouralDriftPanel integration into PerformanceAnalytics

**Backlog ref:** Arc 5 SI-02 frontend integration
**Priority:** P1 (High)
**Effort:** S (~2 hrs)
**Owner:** Base44 Frontend
**EXECUTION:** autonomous
**VERIFICATION:** staging visual (panel renders on PerformanceAnalytics page; nav link present)

**Acceptance Criteria:**
- [ ] AC-01: `BehaviouralDriftPanel` integrated into `PerformanceAnalytics.js` (or equivalent analytics page) as a new section — after `Arc5ComplianceSection` or in a dedicated "Behavioural Drift" section
- [ ] AC-02: Navigation: "Drift" or "Behavioural Drift" link added to the Trading or Analytics nav section — consistent with existing Arc 5 nav pattern
- [ ] AC-03: Panel is hidden or shows `insufficient_data` state gracefully when API returns insufficient_data (not a blank/broken page)
- [ ] AC-04: Section heading: "Behavioural Drift" — human-readable, no story IDs in heading (CLAUDE.md §2 rule)
- [ ] AC-05: Base44 Frontend sign-off recorded in QA evidence

---

### ST-08 — SI-02 Playwright test coverage

**Backlog ref:** BLG-QA-31 (Playwright pre-design, v4.4)
**Priority:** P1 (High)
**Effort:** S (~2–3 hrs)
**Owner:** QA Lead
**EXECUTION:** autonomous
**VERIFICATION:** all Playwright scenarios pass in CI

**References:** `docs/specs/si02/si02_playwright_predesign.md` (BLG-QA-31 v4.4 output)

**Acceptance Criteria:**
- [ ] AC-01: Playwright scenario SC-BD-01: `GET /analytics/behavioural-drift` called; BehaviouralDriftPanel renders on PerformanceAnalytics page; overall status badge present
- [ ] AC-02: Playwright scenario SC-BD-02: all 4 metric cards render with labels and status indicators
- [ ] AC-03: Playwright scenario SC-BD-03: `insufficient_data` state — panel displays the correct message including trade count from the API response
- [ ] AC-04: Playwright scenario SC-BD-04: nav link to Behavioural Drift (or enclosing page) navigates correctly
- [ ] AC-05: Playwright mocks the API response (no live database calls in CI per BLG-QA-37 mock strategy from v4.2)
- [ ] AC-06: All 4 scenarios pass in CI
- [ ] AC-07: QA Lead sign-off recorded in QA evidence

---

## EPIC-03 — Arc 5 Enablers & Gate-Cleared Items (S2-03)

**Owner:** Head of Backend Engineering; Infrastructure & Operations Owner; Head of UX & Design; Frontend Specs & UX Documentation Owner
**Maps to:** S2-03
**Sprint:** Sprint 2
**Sequencing:** Parallel to EPIC-02; no dependency on EPIC-01 (Arc 5 enablers are independent)
**Description:** Gate-cleared backlog items unlocked by SI-02 sprint planning imminence. Includes severity field for red_flag_events, Arc 5 hosting cost projection, Arc 5 nav cohesion review, Red Flag Journal design review scope document. SI-05 Phase 1 is conditional on 2026-06-21 gate.

---

### ST-09 — BLG-BE-16: red_flag_events severity field

**Backlog ref:** BLG-BE-16
**Priority:** P2 (Medium)
**Effort:** M (~3–4 hrs)
**Owner:** Data Model & Domain Schema Owner; Head of Backend Engineering
**EXECUTION:** autonomous
**VERIFICATION:** staging (severity field present in red_flag_journal API response; filter parameter works)
**Gate:** SI-02 sprint planning imminent → CLEARED

**Acceptance Criteria:**
- [ ] AC-01: `severity` column added to `red_flag_events` table: enum or VARCHAR (info/warning/critical); migration created
- [ ] AC-02: Default severity for existing event types: SI-01 override events → `warning`; future SI-02 drift events → `critical` (establish convention in migration or service layer)
- [ ] AC-03: Backfill: existing red_flag_events updated with default severity (`warning` for SI-01 override events, `info` for other types)
- [ ] AC-04: `GET /portfolio/red-flag-journal` updated — accepts optional `severity` query parameter for filtering (e.g. `?severity=warning`)
- [ ] AC-05: `openapi.yaml` updated: severity field added to red_flag_event schema; severity filter parameter documented on `GET /portfolio/red-flag-journal`
- [ ] AC-06: API contract in `docs/specs/api_contracts/` updated with severity field and filter (existing contract updated, not a new `##` heading unless endpoint heading does not already exist at `##` level)
- [ ] AC-07: Unit test: `GET /portfolio/red-flag-journal?severity=warning` returns only warning events
- [ ] AC-08: Data Model & Domain Schema Owner sign-off recorded in QA evidence

---

### ST-10 — BLG-OPS-40: Arc 5 hosting cost projection assessment

**Backlog ref:** BLG-OPS-40
**Priority:** P2 (Medium)
**Effort:** S (~1–2 hrs)
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**EXECUTION:** delegated_decision (FinOps & Resource Architect)
**VERIFICATION:** document inspection (assessment document produced)
**Gate:** SI-02 sprint planning initiated → CLEARED

**Acceptance Criteria:**
- [ ] AC-01: Assessment document produced: `docs/ops/arc5_hosting_cost_projection.md`
- [ ] AC-02: Estimate of additional compute load from SI-02 background queries (if background job pattern adopted) or inline query load per endpoint call
- [ ] AC-03: Comparison against current Render compute tier headroom (using existing ops baselines from api_performance_baseline.md v1.5)
- [ ] AC-04: Recommendation stated: current Render tier adequate for SI-02 load / upgrade recommended before SI-02 ships (with quantified rationale)
- [ ] AC-05: FinOps & Resource Architect sign-off recorded in document and QA evidence

---

### ST-11 — BLG-FE-42: Arc 5 nav cohesion review

**Backlog ref:** BLG-FE-42
**Priority:** P2 (Medium)
**Effort:** M (~3–4 hrs)
**Owner:** Head of UX & Design
**EXECUTION:** delegated_decision (Head of UX & Design)
**VERIFICATION:** document inspection (cohesion review document produced)
**Gate:** SI-02 sprint planning → CLEARED

**Acceptance Criteria:**
- [ ] AC-01: Cohesion review document produced covering current Trading nav structure against projected Arc 5 complete state (SI-01, SI-02, SI-03, SI-04, SI-05 all shipped)
- [ ] AC-02: Review covers: navigability, grouping logic, naming clarity, page depth for the full Arc 5 nav inventory including BehaviouralDriftPanel (SI-02)
- [ ] AC-03: Recommendation stated: maintain current nav structure OR specific structural changes proposed
- [ ] AC-04: If changes recommended: UX spec produced and implementation backlog item filed
- [ ] AC-05: Head of UX & Design sign-off recorded in QA evidence

---

### ST-12 — BLG-FE-47: Red Flag Journal design review scope document

**Backlog ref:** BLG-FE-47
**Priority:** P2 (Medium)
**Effort:** S (~1 hr)
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (scope document produced)

**Acceptance Criteria:**
- [ ] AC-01: Design review scope document produced for RedFlagJournal.js: `docs/specs/fe/rfj_design_review_scope.md`
- [ ] AC-02: Scope document defines what is reviewable: presentation (layout, filters, pagination UI, empty state, severity colour coding if severity field shipped in ST-09) and what is out of scope (data structure, backend API contract)
- [ ] AC-03: Document flags gate date for BLG-FE-41 (gate clears 2026-06-21 — SI-03 live ≥30 days)
- [ ] AC-04: Reviewed by Product Owner and Head of UX & Design before filing
- [ ] AC-05: Frontend Specs & UX Documentation Owner sign-off recorded in QA evidence

---

### ST-13 — BLG-GOV-67: SI-05 Phase 1 implementation — Conditional

**Backlog ref:** BLG-GOV-67
**Priority:** P2 (Medium)
**Effort:** M (~1.5–2 days)
**Owner:** Head of Backend Engineering; Base44 Frontend; QA Lead
**EXECUTION:** autonomous
**VERIFICATION:** staging (weekly digest renders with SI-01 + SI-03 metrics; Telegram delivery confirmed)
**Gate condition:** SI-01 + SI-03 live ≥30 days (gate clears 2026-06-21). Product Owner must confirm gate met before EPIC-03 Sprint 2 planning seals with ST-13. If gate not met by Sprint 2 seal, ST-13 is deferred and Sprint 2 closes with ST-09–ST-12 only.

**Acceptance Criteria:**
- [ ] AC-01: SI-05 Phase 1 weekly digest implemented using SI-01 + SI-03 data only (no SI-02 dependency in Phase 1)
- [ ] AC-02: Digest metrics: `validation_pass_rate` (from GET /analytics/arc5-compliance), `override_count` (from GET /portfolio/red-flag-journal count), `red_flag_frequency_trend` (week-over-week event count)
- [ ] AC-03: Digest delivered via existing Telegram notification infrastructure (v2.4 weekly digest pattern — consistent with POST /ai/check-daily-cost Telegram alert from v4.1)
- [ ] AC-04: Digest scheduled: weekly (existing digest schedule or new weekly trigger)
- [ ] AC-05: No SI-02 data referenced in Phase 1 output
- [ ] AC-06: Playwright test: digest trigger produces expected Telegram payload (mocked; no live Telegram call in CI)
- [ ] AC-07: Gate condition verified by Product Owner before sprint planning seals
- [ ] AC-08: Head of Specs Team sign-off recorded in QA evidence

---

## EPIC-04 — Governance, Spec Debt & OA Resolution (S2-04)

**Owner:** Head of Specs Team; PMO Lead; Product Owner; Strategy Rules & System Intent Owner; QA Lead
**Maps to:** S2-04
**Sprint:** Sprint 1
**Sequencing:** Parallel to EPIC-01; no dependencies on SI-02
**Description:** Resolution of v4.5 OA-01/OA-02, explicitly deferred BLG-GOV-32, aged governance items (BLG-GOV-33/34/41/43/45/52), spec template (BLG-SPEC-32 gate cleared), and OA-02 roadmap_prompt.md advisory. ST-15 combines BLG-GOV-32 + BLG-GOV-43 into a single release_planning_prompt.md patch.

---

### ST-14 — OA-01: System_status_report.md v4.4 stale status correction

**Backlog ref:** v4.5 closure_record.md OA-01
**Priority:** P2 (Medium)
**Effort:** XS (~15 min)
**Owner:** PMO Lead
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (v4.4 section updated)

**Acceptance Criteria:**
- [ ] AC-01: `docs/System_status_report.md` — v4.4 sprint section status updated from "Sprint_Complete — pending verification" to "Verified — 2026-05-29"
- [ ] AC-02: No other content changed in the document
- [ ] AC-03: PMO Lead sign-off recorded in QA evidence

---

### ST-15 — BLG-GOV-32 + BLG-GOV-43: release_planning_prompt.md gate scan + data density checkpoint

**Backlog ref:** BLG-GOV-32; BLG-GOV-43
**Priority:** P2 (Medium)
**Effort:** S (~2–3 hrs including §6 checklist)
**Owner:** Head of Specs Team; PMO Lead; Product Owner
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (release_planning_prompt.md updated; OPERATIONAL_GUIDE §14 updated; prompt_change_log.md entry appended)

**Acceptance Criteria:**
- [ ] AC-01: New advisory step added to `release_planning_prompt.md` STEP 1 — STEP 1.4 Gate-Condition Proximity Scan: "Scan all gate-conditional backlog items; flag items where gate is likely to clear within 30–60 days given current trajectory. Output gate proximity table in the run manifest."
- [ ] AC-02: STEP 1.4 includes Arc 4 data density sub-check: "Check current closed trade count, AI journal entry count, and trade plan creation rate. Surface projection: estimated gate-clearing dates for PO-02 (6+ months AI journals), PO-04 (50+ trades with plans), SI-02 (20+ trades with plans). PO to confirm or update projections."
- [ ] AC-03: Gate proximity table format documented: `| Item | Gate condition | Current trajectory | Projected clear date |`
- [ ] AC-04: release_planning_prompt.md version bumped; OPERATIONAL_GUIDE.md §14 updated to new version; prompt_change_log.md entry appended (CLAUDE.md §6 checklist — one version bump covers both BLG-GOV-32 and BLG-GOV-43 changes in the same commit)
- [ ] AC-05: Head of Specs Team sign-off recorded in QA evidence

---

### ST-16 — BLG-GOV-33: closed trade count audit (PT-04 + SI-02 data density gate)

**Backlog ref:** BLG-GOV-33
**Priority:** P2 (Medium)
**Effort:** XS (~30 min)
**Owner:** Product Owner; Challenger
**EXECUTION:** delegated_decision (Product Owner)
**VERIFICATION:** document inspection (count documented in QA evidence and PT-04 backlog item updated)

**Acceptance Criteria:**
- [ ] AC-01: Production database queried for current closed trade count: `SELECT COUNT(*) FROM trade_history WHERE pnl IS NOT NULL`
- [ ] AC-02: SI-02 gate query executed: `SELECT COUNT(*) FROM trade_history th JOIN trade_plans tp ON tp.position_id = th.position_id WHERE th.pnl IS NOT NULL`
- [ ] AC-03: Both counts documented in QA evidence for this story
- [ ] AC-04: PT-04 backlog item (BLG-FEAT-25) updated with current count and gate status
- [ ] AC-05: If count (AC-02) ≥ 20: Product Owner confirms SI-02 data density gate met; EPIC-02 Sprint 2 proceeds; note in QA evidence
- [ ] AC-06: If count (AC-02) < 20: Product Owner records gate not met; EPIC-02 deferred; projected clearing date estimated based on current trade frequency
- [ ] AC-07: Product Owner sign-off recorded in QA evidence

---

### ST-17 — BLG-GOV-34: Arc 4 data density risk trajectory assessment

**Backlog ref:** BLG-GOV-34
**Priority:** P2 (Medium)
**Effort:** S (~2–3 hrs)
**Owner:** Product Owner; Challenger
**EXECUTION:** delegated_decision (Product Owner)
**VERIFICATION:** document inspection (trajectory assessment document produced)

**Acceptance Criteria:**
- [ ] AC-01: Trajectory assessment document produced at `docs/product/decisions/arc4_data_density_trajectory_v4.6.md`
- [ ] AC-02: Current metrics assessed: trade frequency (trades/month), AI journal entry rate (summaries generated/month from BLG-FEAT-16), trade plan creation rate (plans/month)
- [ ] AC-03: Projected gate-clearing dates computed: PO-02 gate (6+ months AI journal entries), PO-04 gate (50+ trades with plans), PO-04 sub-gate (50+ closed trades)
- [ ] AC-04: Recommendation stated: (a) proceed on current trajectory, (b) revise gate conditions, or (c) re-scope/defer features — with rationale
- [ ] AC-05: Product Owner and Challenger sign-off recorded in QA evidence

---

### ST-18 — BLG-GOV-45: Arc 6 Monte Carlo §13 pre-assessment

**Backlog ref:** BLG-GOV-45
**Priority:** P2 (Medium)
**Effort:** S (~2–3 hrs)
**Owner:** Strategy Rules & System Intent Owner
**EXECUTION:** delegated_decision (Strategy Rules & System Intent Owner)
**VERIFICATION:** document inspection (§13 assessment document produced)

**Acceptance Criteria:**
- [ ] AC-01: §13 pre-assessment document produced for PS-03 (Monte Carlo Simulation, Arc 6): `docs/product/decisions/arc6_ps03_section13_preassessment.md`
- [ ] AC-02: Assessment confirms (or refutes): simulation is deterministic (no ML/probability model); uses own trade distribution data only (no external benchmarks); output is statistical context not a recommendation; gate condition ≥50 trades deterministic
- [ ] AC-03: Binding conditions documented (if PASS): "simulation uses actual trade distribution only", "output displays percentile ranges, not point predictions", and any additional conditions
- [ ] AC-04: PASS or CONDITIONAL determination documented with rationale
- [ ] AC-05: Strategy Rules & System Intent Owner sign-off recorded in document and QA evidence

---

### ST-19 — BLG-GOV-52: trade plan schema field count gate check

**Backlog ref:** BLG-GOV-52
**Priority:** P2 (Medium)
**Effort:** S (~1–2 hrs)
**Owner:** Data Model & Domain Schema Owner; Product Owner
**EXECUTION:** delegated_decision (Data Model & Domain Schema Owner)
**VERIFICATION:** document inspection (schema audit note produced)

**Acceptance Criteria:**
- [ ] AC-01: Trade plan schema audit note produced: `docs/specs/data_model/trade_plan_schema_audit_v4.6.md`
- [ ] AC-02: All current `trade_plans` fields enumerated (including post-DS-07 migration fields from ST-01)
- [ ] AC-03: Each field cross-referenced with roadmap feature descriptions (PT-01/02/03/04/05, Arc 4 plan_vs_reality, SI-02 capture fields)
- [ ] AC-04: Orphaned fields identified (present in table but not surfaced in any feature) — with remediation recommendation (keep/remove)
- [ ] AC-05: Missing fields identified (needed by roadmap features but absent) — with recommended sprint to add
- [ ] AC-06: Data Model & Domain Schema Owner sign-off recorded in QA evidence

---

### ST-20 — BLG-GOV-41: sprint close automation failure investigation

**Backlog ref:** BLG-GOV-41
**Priority:** P2 (Medium)
**Effort:** S (~1–2 hrs)
**Owner:** PMO Lead; Infrastructure & Operations Owner
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (investigation findings produced)
**Gate:** sprint_close_reminder.yml failure mechanism identified → investigation IS the gate resolution

**Acceptance Criteria:**
- [ ] AC-01: GitHub Actions run logs reviewed for the failing cycle (2026-05-22__release-v4.0 per BLG-GOV-41 description)
- [ ] AC-02: Root cause identified and documented: timing issue / environment issue / logic error / workflow not triggered
- [ ] AC-03: Resolution proposed and implemented OR workflow retired: (a) fix applied to `sprint_close_reminder.yml` and committed; OR (b) workflow retired with documented rationale (e.g., "manual trigger sufficient; automation overhead not warranted at current scale")
- [ ] AC-04: Findings documented in `docs/ops/sprint_close_reminder_investigation_v4.6.md`
- [ ] AC-05: PMO Lead sign-off recorded in QA evidence

---

### ST-21 — BLG-SPEC-32: external API integration spec template

**Backlog ref:** BLG-SPEC-32
**Priority:** P3 (Low)
**Effort:** S (~2–3 hrs)
**Owner:** Head of Specs Team; API Contracts Documentation Owner
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (template produced; at minimum Anthropic API contract conforms)
**Gate:** ≥2 external API integrations → CLEARED (Alpaca, Yahoo Finance, Anthropic = 3 integrations)

**Acceptance Criteria:**
- [ ] AC-01: Template document produced: `docs/specs/api_contracts/_external_api_template.md`
- [ ] AC-02: Template includes required sections: authentication model, rate limits, error taxonomy, cost attribution, data model mapping, retry policy
- [ ] AC-03: Anthropic API contract (`docs/specs/api_contracts/ai_thesis_contract.md` or equivalent) reviewed against template; any conformance gaps noted as advisory (sealed artefacts not modified retroactively without a new version)
- [ ] AC-04: Template reviewed by API Contracts Documentation Owner and Head of Specs Team
- [ ] AC-05: Head of Specs Team sign-off recorded in QA evidence

---

### ST-22 — OA-02: roadmap_prompt.md advisory — set next_release after DL decision

**Backlog ref:** v4.5 closure_record.md OA-02; v4.5 lessons_learnt_closure.md carry-forward item 1
**Priority:** P3 (Low)
**Effort:** XS (~1 hr including §6 checklist)
**Owner:** Head of Specs Team
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (roadmap_prompt.md patched; version bumped; change log entry appended)

**Acceptance Criteria:**
- [ ] AC-01: `roadmap_prompt.md` STEP 11 (or appropriate post-DL decision step) updated with advisory: "After the DL decision sets the next planned release label, update `next_release` in `.claude_current_state.json` to the projected version label (e.g., `v4.6`) if determinable. This reduces the 'version not on roadmap' annotation requirement at the next release planning invocation."
- [ ] AC-02: Patch is advisory text only — no hard gate added; no required action change
- [ ] AC-03: roadmap_prompt.md version bumped; OPERATIONAL_GUIDE.md §14 roadmap engine source updated; prompt_change_log.md entry appended (CLAUDE.md §6 checklist)
- [ ] AC-04: Head of Specs Team sign-off recorded in QA evidence

---

<!-- release-plan-marker: RP:v4.6:2026-05-30__release-v4.6 -->
