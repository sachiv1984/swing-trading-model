**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.7
**Cycle:** 2026-04-13__release-v2.7
**Last Updated:** 2026-04-13

---

# Sprint Backlog Slice — v2.7

**Theme:** Performance, Governance Hardening & Market Intelligence
**Sprint Goal:** Ship v2.7: eliminate connection pooling latency, harden governance process gates, resolve Playwright test infrastructure, deliver market correlation analysis and supplementary signal indicators, and close spec/governance documentation debt.

**Total Stories:** 11
**Sprints:** 2

---

## EPIC-01 — Performance & Connection Infrastructure

**Maps to:** S2-01, S2-02
**Sprint:** Sprint 1
**Owner:** Head of Engineering + Infrastructure & Operations Owner
**Branch:** exec/2026-04-13__release-v2.7/EPIC-01

### ST-01 — Enable Supabase Supavisor connection pooling

**Backlog item:** BLG-OPS-14
**Priority:** P1
**Effort:** XS (<1 hour — env var change + test)
**Delegation class:** delegated (requires human to update environment variables on Render)

**Description:** Switch `DATABASE_URL` on staging and production Render services to the Supabase Supavisor pooler connection string (port 6543, `?pgbouncer=true`). No code changes required. Projects p50 improvements of 1–4s for DB-heavy endpoints.

**Acceptance Criteria:**
- [ ] Supavisor pooler connection string in use on staging and production
- [ ] Baseline re-run shows p50 ≤ 500ms for at least the fast cluster endpoints; GET /portfolio and GET /notifications/preferences projected to improve by ≥1.5s
- [ ] No regression to DB correctness (reads and writes verified)
- [ ] `docs/ops/api_performance_baseline.md` updated to v1.2 with new measurements

**Sequencing:** Must complete and verify before ST-02 is implemented.

---

### ST-02 — Refactor get_portfolio_summary() to use a single DB connection

**Backlog item:** BLG-BE-07-FIX
**Priority:** P2
**Effort:** M (~half day)
**Delegation class:** autonomous
**Depends on:** ST-01 (Supavisor must be enabled first for independent measurement)

**Description:** Refactor `get_portfolio_summary()` in `backend/services/portfolio_service.py` to accept or create a single DB connection and pass it to all 4 internal calls (`get_portfolio()`, `get_positions()`, `get_total_deposits_withdrawals()`, `get_drawdown_fields()`).

**Acceptance Criteria:**
- [ ] `GET /portfolio` makes 1 DB connection per request, not 4
- [ ] P50 for GET /portfolio after fix (with Supavisor enabled) ≤ 400ms
- [ ] No regression to portfolio data correctness (all fields return correct values)
- [ ] Unit test coverage for the refactored function exists or is extended

---

## EPIC-02 — Governance Process Hardening

**Maps to:** S2-03, S2-04, S2-05
**Sprint:** Sprint 1
**Owner:** Director of Quality + Head of Specs Team + Infrastructure & Operations Owner
**Branch:** exec/2026-04-13__release-v2.7/EPIC-02

### ST-03 — Require QA evidence sign-off block to be complete before PR is raised

**Backlog item:** BLG-GOV-18
**Priority:** P2
**Effort:** XS (<1 hour)
**Delegation class:** autonomous

**Description:** Add explicit gate to `execution_prompt.md §3.2.B` (Open PR step): "Do not open the PR until `qa_evidence_EPIC-xx.md` DoQ sign-off block contains a non-blank Date field." Update `commit-check` skill pre-commit checklist to flag blank sign-off Date.

**Acceptance Criteria:**
- [ ] `execution_prompt.md §3.2.B` explicitly gates PR creation on a non-blank DoQ sign-off Date in `qa_evidence_EPIC-xx.md`
- [ ] `commit-check` skill pre-commit checklist raises a warning if any in-scope EPIC's `qa_evidence` has a blank Date field
- [ ] Version bump: `execution_prompt.md` bumped; OPERATIONAL_GUIDE §14 updated; `prompt_change_log.md` entry appended
- [ ] §6 checklist applied per CLAUDE.md

---

### ST-04 — Define formal autonomous DoQ sign-off class for code-review-only EPICs

**Backlog item:** BLG-GOV-19
**Priority:** P2
**Effort:** S (~0.5d)
**Delegation class:** autonomous

**Description:** Define "autonomous DoQ" sign-off class in `execution_prompt.md §3.2.A` with qualifying criteria (checklist or table). Update `delivery_verification_prompt.md` STEP -1.3 Tier 2 check to recognise the class as a compliant sign-off.

**Qualifying criteria (draft for Director of Quality review):**
1. All stories in the EPIC have `delegation_class: autonomous`
2. All AC verified by code review — no observable UI behaviour, no staging run required
3. No frontend-visible change in this EPIC
4. Engine signer field populated as "Sprint Execution Engine (autonomous class)"

**Acceptance Criteria:**
- [ ] Autonomous DoQ sign-off class formally defined with qualifying criteria in `execution_prompt.md`
- [ ] Director of Quality sign-off on qualifying criteria recorded in QA evidence before merge
- [ ] `delivery_verification_prompt.md` STEP -1.3 Tier 2 check does not fire for EPICs with a valid autonomous DoQ sign-off
- [ ] Version bumps: both prompts bumped; OPERATIONAL_GUIDE §14 updated; `prompt_change_log.md` entries appended
- [ ] §6 checklist applied per CLAUDE.md for both files

---

### ST-05 — Extend governance_sync.yml to trigger on push to main

**Backlog item:** BLG-GOV-16
**Priority:** P2
**Effort:** XS (<1 hour)
**Delegation class:** autonomous

**Description:** Add `main` to the `on.push.branches` trigger list in `.github/workflows/governance_sync.yml`. Verify the workflow fires on merge to main and closes correct issues. Existing `--state open` filter prevents double-close errors.

**Acceptance Criteria:**
- [ ] `.github/workflows/governance_sync.yml` `on.push.branches` includes `main`
- [ ] After merging a PR to `main`, GitHub Issues with titles matching `[ST-xx]` commits in the merge are automatically closed
- [ ] Issues already closed (from exec branch push) are not errored — workflow skips them cleanly
- [ ] Manual issue closure after EPIC merges is no longer required

---

## EPIC-03 — Test Infrastructure

**Maps to:** S2-06, S2-07
**Sprint:** Sprint 1
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Branch:** exec/2026-04-13__release-v2.7/EPIC-03

### ST-06 — Fix Playwright page.route() intercepts not firing in local test environment

**Backlog item:** BLG-QA-11
**Priority:** P2
**Effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Description:** Investigate root cause of Playwright page.route() intercept failures affecting all e2e specs. Fix the intercept mechanism so at least one spec passes end-to-end. Apply fix pattern to all existing specs. Document the working approach.

**Suspected root causes (investigate in priority order):**
1. React Query bypassing Playwright's intercept layer (CSP or service worker)
2. `REACT_APP_API_URL` env var not resolving to `http://localhost:8000`
3. Route registration timing — may need `page.addInitScript` rather than `page.route()`

**Acceptance Criteria:**
- [ ] Root cause of intercept failure identified and documented
- [ ] `reports-performance-tab.spec.js` — all 11 tests pass in headless Chromium
- [ ] `slippage-tracking.spec.js` — all 8 tests pass in headless Chromium
- [ ] `fee-drag-trade-history.spec.js` — all 7 tests pass in headless Chromium
- [ ] `signals-cash-balance.spec.js` — all 4 tests pass in headless Chromium
- [ ] Fix pattern documented so future specs follow the working approach

**Note:** ST-07 is gated on this story. If root cause cannot be fixed in this sprint, ST-07 is descoped and BLG-QA-12 re-deferred to v2.8.

---

### ST-07 — System Status Playwright spec

**Backlog item:** BLG-QA-12
**Priority:** P3
**Effort:** M (~1 day)
**Delegation class:** autonomous
**Depends on:** ST-06 (intercept fix must be in place)

**Description:** Write `tests/e2e/system-status.spec.js` asserting category routing and endpoint count display using the fixed page.route() pattern from ST-06.

**Acceptance Criteria:**
- [ ] `tests/e2e/system-status.spec.js` exists covering category routing and count display
- [ ] Mock `POST /test/endpoints` response with controlled endpoint results covering `/alerts/rules`, `/notifications`, `/digest/weekly` (at minimum)
- [ ] Assert: Alerts category section visible; Notifications section visible; Digest section visible
- [ ] Assert: total endpoint count shown is ≥ 26 (or exact 26 if count is hardcoded in placeholder)
- [ ] Assert: none of the alert/notification/digest endpoints appear under "Other"
- [ ] All assertions pass in headless Chromium using the ST-06 fix pattern

---

## EPIC-04 — Market Intelligence

**Maps to:** S2-08, S2-09
**Sprint:** Sprint 2
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Branch:** exec/2026-04-13__release-v2.7/EPIC-04

### ST-08 — Market Correlation Analysis

**Backlog item:** BLG-FEAT-17
**Priority:** P2
**Effort:** M (~1–2 days)
**Delegation class:** autonomous

**Description:** New `GET /analytics/market-correlation` endpoint returning per-position and portfolio-level Pearson correlation coefficients vs. benchmark (SPY for US, FTSE for UK) over 252-day default lookback. Response cached TTL-based (minimum one trading day). Frontend displays on Analytics/Reports page with colour-coded severity.

**Acceptance Criteria:**
- [ ] `GET /analytics/market-correlation` (or equivalent path) returns correlation coefficients for all open positions vs. relevant benchmark (SPY/FTSE)
- [ ] Portfolio-level weighted average correlation included in response
- [ ] Correlation computed as Pearson coefficient over 252-day lookback (or available history); lookback is a query parameter
- [ ] Response cached with TTL of minimum one trading day — repeated calls return cached result
- [ ] SPY/FTSE historical data fetched on-demand; no index time-series persisted to database
- [ ] Frontend displays per-position correlation and portfolio average on Analytics page with colour-coded severity (high >0.7, moderate 0.3–0.7, low <0.3)
- [ ] `openapi.yaml` updated in the same commit as the new endpoint
- [ ] If Yahoo Finance unavailable, endpoint returns graceful error (not 500); cached data served if available
- [ ] Engineer notes in QA evidence: if Yahoo Finance reliability becomes a problem, a formal data source review is required before any further correlation-dependent features

---

### ST-09 — Add supplementary indicator fields to signal generation

**Backlog item:** BLG-BE-10
**Priority:** P3
**Effort:** M (~1–2 days)
**Delegation class:** autonomous
**§13 Status:** COMPLIANT (display-only) — SRB-v1.7 Feature 3

**Description:** Add 4 new display-only fields to `POST /signals/generate` response per signal: `relative_strength_pct`, `week52_high_proximity_pct`, `avg_daily_volume_20d`, `price_vs_50d_ma`. Frontend displays as supplementary context columns on Signals page.

**Acceptance Criteria:**
- [ ] `POST /signals/generate` response includes all four new fields per signal object
- [ ] `relative_strength_pct` computed as stock momentum minus benchmark momentum over same `lookback_days`; US stocks benchmark SPY, UK stocks benchmark FTSE
- [ ] `relative_strength_pct` labelled "vs. benchmark (informational)" in UI and does not affect `rank` field or signal ordering
- [ ] `week52_high_proximity_pct`, `avg_daily_volume_20d`, and `price_vs_50d_ma` displayed as supplementary context; display does not alter signal rank
- [ ] `signal_endpoints.md` updated to document the four new response fields
- [ ] `openapi.yaml` updated in the same commit as the contract change
- [ ] Strategy Rules owner confirms no scoring logic was modified (sign-off in QA evidence before merge)
- [ ] Documented in QA evidence: any future proposal to incorporate these fields into signal ranking requires a new §13 review and strategy_rules.md version bump before pre-alignment

---

## EPIC-05 — Spec & Governance Documentation

**Maps to:** S2-10, S2-11
**Sprint:** Sprint 2
**Owner:** Head of Specs Team + PMO Lead + Director of Quality
**Branch:** exec/2026-04-13__release-v2.7/EPIC-05

### ST-10 — Spec Dependency Map

**Backlog item:** BLG-SPEC-D17
**Priority:** P3
**Effort:** M (~1–2 days)
**Delegation class:** autonomous

**Description:** Create `docs/specs/spec_dependency_map.md` mapping all canonical spec cross-references. Document is read-only reference with explicit staleness acknowledgement. Head of Specs Team signs off on completeness at authoring time.

**Acceptance Criteria:**
- [ ] Reference document exists at `docs/specs/spec_dependency_map.md` listing all canonical specs and their known dependencies
- [ ] Document labelled as read-only reference with staleness acknowledgement (explicit header note: "Point-in-time reference — last updated [date]. Accuracy not guaranteed after spec creation/revision without a manual update.")
- [ ] All currently known cross-spec dependencies captured at time of authoring
- [ ] Head of Specs Team sign-off on completeness recorded in QA evidence

---

### ST-11 — Governance Health Score

**Backlog item:** BLG-GOV-14
**Priority:** P3
**Effort:** M (~1–2 days)
**Delegation class:** autonomous

**Description:** Define governance health score formula (3 components: header compliance %, deferred patch indicator, outstanding action count). Document canonically in OPERATIONAL_GUIDE.md or dedicated spec. Implement as advisory check at STEP -1 of each roadmap rebalance.

**Formula components:**
1. **Header compliance %** = Class 4/5 docs with compliant headers / total checked
2. **Deferred patch indicator** = count of open deferred patches by age band (<1 cycle / 1–2 cycles / >2 cycles)
3. **Outstanding action count** = count of open outstanding actions

**Acceptance Criteria:**
- [ ] Governance health score formula documented canonically with all three components defined (OPERATIONAL_GUIDE §N or dedicated spec)
- [ ] Score is computed and surfaced at STEP -1 of each roadmap rebalance as an advisory indicator
- [ ] Score labelled as advisory — cannot halt or gate the routine
- [ ] Head of Specs Team sign-off on formula definition recorded in QA evidence
- [ ] §6 checklist applied per CLAUDE.md for any prompt files modified
