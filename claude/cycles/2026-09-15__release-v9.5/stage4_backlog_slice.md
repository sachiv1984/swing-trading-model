Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-15
Cycle: 2026-09-15__release-v9.5
Release: v9.5

# Backlog Slice — v9.5

<!-- release-plan-marker: RP:v9.5:2026-09-15__release-v9.5 -->

43 stories across 6 grouped EPICs, 27.99 estimated days. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope set to the top of the confirmed ~24-28 day/sprint capacity band per explicit user "use full capacity" instruction (2026-09-15). Ready pool: 62 items / ~43.79 days (after excluding 3 substantively gate-blocked items with no formal Gate field — BLG-FEAT-73/74/76). Selection method: P1 items first, then P2 items (ascending ID), then category-balanced round-robin oldest-first for remaining P3/P4 — per `release_planning_prompt.md` §1.4c Canonical Over-Capacity Ready-Pool Selection Method. All 4 FE/UX items in EPIC-06 carry an observable UI acceptance criterion — `design_gate_required: true`.

---

## EPIC-01 — Backend & Platform Engineering Debt

**Maps to:** S2-01
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Head of Engineering

### ST-01 — CI-blocking test_changelog_service.py failure on every PR
**Source:** BLG-BE-117
**Priority:** P1
**Effort:** S (~0.5–1d, pending root cause)
**Acceptance Criteria:**
- `test_real_changelog_is_parseable` passes against the real `docs/product/changelog.md`
- A clean PR shows CI green with no dependency on this fix

### ST-02 — Backend logging output does not conform to structured_logging_standards.md's mandatory JSON Lines format
**Source:** BLG-BE-112
**Priority:** P3
**Effort:** M (~2-3 days)
**Acceptance Criteria:**
- Backend log output is valid JSON Lines matching the canonical example in `structured_logging_standards.md`, OR the spec is formally revised to match accepted practice
- No regression to existing log-based monitoring/alerting that depends on the current plain-text format

### ST-03 — Validate limit/offset are non-negative on screener endpoints
**Source:** BLG-BE-113
**Priority:** P3
**Effort:** S (~0.5 day)
**Acceptance Criteria:**
- A negative `limit` or `offset` on either endpoint returns HTTP 400 `INVALID_PARAMS`, not a 500
- Any other paginated endpoint found with the same gap is either fixed or filed as a follow-up item

### ST-04 — Consolidate duplicated ATR trailing-stop recalculation logic
**Source:** BLG-BE-114
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- Single shared implementation exists; all 3 call sites use it
- Existing trailing-stop tests still pass unchanged

---

## EPIC-02 — Operations & Security Debt

**Maps to:** S2-02
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect

### ST-05 — nightly-stop-update and rebalance-exit appear to have no live scheduled trigger
**Source:** BLG-OPS-160
**Priority:** P1
**Effort:** S (investigation/confirmation) — remediation effort TBD pending confirmation
**Acceptance Criteria:**
- Render dashboard checked and outcome documented (dashboard-cron found, or confirmed absent)
- If absent: both endpoints wired into a live schedule; live confirmation that `GET /health/scheduler` shows a recent `last_run` for all three affected job names
- `scheduler_architecture_review_v6.3.md` corrected to match the confirmed live trigger mechanism

### ST-06 — AI audit log cost-monitoring follow-ons: storage projection, per-feature trend, silent-purge-failure visibility
**Source:** BLG-OPS-153
**Priority:** P3
**Effort:** M (~2 days, 3 small sub-items)
**Acceptance Criteria:**
- All 3 sub-items addressed (or explicitly re-scoped/split into separate items at grooming time)
- FinOps & Resource Architect sign-off

### ST-07 — New `api_call_log` table has no retention/purge policy
**Source:** BLG-OPS-154
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `api_call_log` has a documented retention window and a scheduled purge function
- Infrastructure & Operations Owner sign-off

### ST-08 — `get_api_session_report()` anomaly baseline is self-inclusive
**Source:** BLG-OPS-155
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Anomaly baseline is no longer inflated by the session(s) it is evaluating
- Infrastructure & Operations Owner sign-off

### ST-09 — Add 1 new endpoint to api_performance_baseline.md re-run
**Source:** BLG-OPS-156
**Priority:** P3
**Effort:** XS (<1h, plus a live measurement re-run)
**Acceptance Criteria:**
- `api_performance_baseline.md` has a row for `GET /positions/{id}`
- Infrastructure & Operations Owner sign-off

### ST-10 — Recurring quarterly hosting-cost trend review
**Source:** BLG-OPS-157
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Cadence documented
- First cadence-driven review completed with results recorded

### ST-11 — Synthetic uptime monitor for /health independent of hosting dashboard
**Source:** BLG-OPS-158
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Monitor configured and confirmed firing on a deliberate test failure
- Notification path confirmed working

### ST-12 — Document the dashboard-only deploy path-filter gotcha in the ops runbook
**Source:** BLG-OPS-159
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- Note added to the ops runbook
- Cross-referenced from the deploy-troubleshooting doc

### ST-13 — claude_audit_log has no latency column; no real-data source for AI endpoint latency anomaly checks
**Source:** BLG-OPS-161
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- `claude_audit_log` carries a populated latency column for new rows
- `POST /ai/check-endpoint-anomalies` reports real (non-simulated) `latency_anomalies` with `latency_data_source` no longer `"not_available_pending_BLG-OPS-161"`

### ST-14 — Provision read-only staging `DATABASE_URL` for sprint-execution sessions
**Source:** BLG-OPS-162
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- A read-only staging DB credential exists and is scoped so it cannot mutate any table
- The credential is injected into sprint-execution sessions via environment configuration, never appearing as chat text or in git history
- A sprint-execution session can successfully run a real read-only query against staging data end-to-end as a smoke test

---

## EPIC-03 — QA & Test Coverage Debt

**Maps to:** S2-03
**Owner:** QA & Testing Owner; Director of Quality

### ST-15 — Arc 4 E2E test strategy pre-design (PO-02/03/04)
**Source:** BLG-QA-59
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Arc 4 E2E test strategy document produced
- Mocking approach for PO-02/03/04 AI calls defined and consistent with existing BLG-QA-37 Playwright mock strategy
- Reviewed by Director of Quality

### ST-16 — Extract governance_sync.yml's embedded bash logic into a shared, sourced script
**Source:** BLG-QA-165
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `governance_sync.yml`'s diff-detection and close-gate logic each live in exactly one place (a sourced script), not duplicated between the workflow and its tests
- Both existing regression test scripts still pass, now by exercising the real extracted functions rather than hand-maintained copies
- QA & Testing Owner sign-off

### ST-17 — Add unit test coverage for check_contract_example_freshness.py
**Source:** BLG-QA-166
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- New test file exists and passes
- QA & Testing Owner sign-off

### ST-18 — Playwright coverage matrix file-inventory count is stale (39 vs actual ~100+ spec files)
**Source:** BLG-QA-167
**Priority:** P3
**Effort:** S (~1 day)
**Acceptance Criteria:**
- Per-file table matches the actual `tests/e2e/` directory contents
- Running total corrected
- Doc Version/Last Updated bumped per the doc's own convention

### ST-19 — ST-09 cross-browser evaluation cites stale pre-sharding CI baseline
**Source:** BLG-QA-168
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Document cites the current CI baseline, not the superseded pre-sharding one
- QA & Testing Owner sign-off

### ST-20 — ST-05 SignalCard spec consolidation lacks before/after runtime evidence
**Source:** BLG-QA-169
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A real before/after runtime number is recorded substantiating (or correcting) the "runtime reduced" claim
- QA & Testing Owner sign-off

### ST-21 — `qa_evidence_EPIC-03.md` test-count claim inaccurate (30 vs. actual 28)
**Source:** BLG-QA-170
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Test count in `qa_evidence_EPIC-03.md` matches the actual number of tests in `tests/test_cost_monitoring.py`
- QA & Testing Owner sign-off

---

## EPIC-04 — Spec & Documentation Debt

**Maps to:** S2-04
**Owner:** Head of Specs Team; API Contracts & Documentation Owner; Data Model & Domain Schema Owner; Frontend Specifications & UX Documentation Owner

### ST-22 — data_model.md `positions` table (DS-17 addition) not confirmed against live deployed schema
**Source:** BLG-SPEC-D18
**Priority:** P2
**Effort:** XS (confirmation only, once DB access is available)
**Acceptance Criteria:**
- Live schema confirmed to match spec (or discrepancies filed as their own follow-on items)
- Schema verification note added to `data_model.md`'s Positions Table section

### ST-23 — Arc 4 API contract pre-authoring (PO-02/03/04)
**Source:** BLG-SPEC-56
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Stub contract files exist for PO-02, PO-03, PO-04 endpoint groups in `docs/specs/api_contracts/`
- Each stub includes at minimum: endpoint path, HTTP method, brief description, key request/response fields
- BLG-SPEC-35 §13 pre-assessment reviewed or updated if new boundary questions arise

### ST-24 — Data model v3 pre-definition for Arc 4 journal intelligence
**Source:** BLG-SPEC-57
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Data model pre-definition document produced covering Arc 4 schema additions
- BLG-SPEC-56 Arc 4 API contracts reference the pre-defined model where applicable
- Reviewed by Head of Specs Team and Infrastructure & Operations Owner

### ST-25 — position_endpoints.md example JSON: current_trailing_stop_native doesn't reconcile with current_trailing_stop × live_fx_rate
**Source:** BLG-SPEC-133
**Priority:** P4
**Effort:** XS (~15min)
**Acceptance Criteria:**
- Example JSON block in `docs/specs/api_contracts/position_endpoints.md` is internally consistent (`current_trailing_stop × live_fx_rate == current_trailing_stop_native`, within rounding)
- API Contracts & Documentation Owner sign-off (or Head of Specs Team, per standard doc-fix delegation)

### ST-26 — Triage contract example-payload freshness check findings
**Source:** BLG-SPEC-139
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Every one of the 40 baseline findings has a recorded disposition (fixed, or documented as a resolver artifact)
- `python3 scripts/check_contract_example_freshness.py` re-run and its updated finding count recorded
- API Contracts & Documentation Owner sign-off

### ST-27 — Make check_orphaned_specs.py path-aware to resolve duplicate-basename blind spots
**Source:** BLG-SPEC-140
**Priority:** P3
**Effort:** M (~2 days)
**Acceptance Criteria:**
- Detector distinguishes path-qualified references to same-named files in different directories
- A duplicate-basename pair with only one member referenced (unambiguous path-qualified reference) correctly flags the other as orphaned
- Existing 10 unit tests in `tests/test_check_orphaned_specs.py` still pass; new tests added for path-aware resolution and the ambiguity-flagging fallback

### ST-28 — Spec debt dashboard sort key mishandles same-day-filed items
**Source:** BLG-SPEC-141
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A same-day-filed item sorts as the newest item in its priority tier, not as undated
- API Contracts & Documentation Owner sign-off

### ST-29 — Canonical position/trade lifecycle state diagram
**Source:** BLG-SPEC-142
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- Diagram exists in `data_model.md`
- All 3 source files cross-reference it

### ST-30 — Consolidate divergent empty-state copy patterns
**Source:** BLG-SPEC-143
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Confirmed status against v9.1 ST-29's prior consolidation recorded
- Canonical pattern documented if a genuine remaining gap is confirmed

---

## EPIC-05 — Governance Process Debt

**Maps to:** S2-05
**Owner:** Head of Specs Team; PMO Lead; FinOps & Resource Architect; Director of HR; Director of Quality

### ST-31 — Require resolving commits to update the canonical spec's own Known Deviation fields when closing a deviation
**Source:** BLG-GOV-332
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A named governed-routine step requires resolving-commit-updates-canonical-entry discipline, mirroring the existing filing-time discipline
- Next Cross-EPIC Deviation Consolidation Review confirms 0 new resolution-status-drift instances found after this rule lands
- Head of Specs Team sign-off

### ST-32 — Wire the wall-clock cost logging convention (§22) into an engine's STEP list
**Source:** BLG-GOV-316
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- At least one engine's STEP list explicitly instructs capturing `Session start (UTC)`/`Session end (UTC)`
- A real session record demonstrates the convention in use

### ST-33 — Codify whether opportunistic in-file fixes found mid-story need their own backlog entry
**Source:** BLG-GOV-318
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Rule documented in a governance source file
- Product Owner sign-off

### ST-34 — record-visual-qa skill's documented output format has drifted ~5 months from actual staging sign-off practice
**Source:** BLG-GOV-319
**Priority:** P3
**Effort:** S (~1 day)
**Acceptance Criteria:**
- Skill documentation matches actual current staging sign-off practice, confirmed against a sample of recent `qa_evidence_EPIC-*.md` entries
- Director of Quality sign-off on the reconciled approach

### ST-35 — File a Product Owner decision record for ST-20's trade-tagging "no closed taxonomy" call
**Source:** BLG-GOV-320
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Decision record filed and cross-referenced
- Product Owner sign-off

### ST-36 — Lightweight role-retirement process for inactive agent charters
**Source:** BLG-GOV-321
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Process documented (likely a short addition to `team_charter.md` or a new §)
- Applied at least once to confirm it runs end to end (may find 0 qualifying roles — that is a valid outcome)

### ST-37 — Cross-role pairing rotation note in workforce_capacity.md
**Source:** BLG-GOV-322
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Note added and cross-referenced from `roadmap_prompt.md` §7.1's pull-forward step

### ST-38 — Cost-per-cycle wall-clock rollup in workforce_capacity.md
**Source:** BLG-GOV-323
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Rollup table added and populated with available historical figures
- Refresh cadence documented

### ST-39 — Formalise the STEP 8.0.5 / STEP 8.2 candidate-verification pattern as one subroutine
**Source:** BLG-GOV-324
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Subroutine extracted; version bump + `prompt_change_log.md` entry per the Governance File Edit Checklist
- Both steps reference the shared subroutine with no behavioural change

---

## EPIC-06 — Frontend & UX Debt

**Maps to:** S2-06
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design

### ST-40 — Fix trade plan link display to use formatted text instead of snake_case
**Source:** BLG-FE-177
**Priority:** P2
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Trade plan link/reference on trade entry displays human-readable formatted text, not snake_case
- No underscores visible in the rendered trade plan link text
- Existing trade plan linkage functionality (click-through/navigation) unaffected

### ST-41 — Bring the 4 known motion-timing non-compliant components under the 500ms ceiling
**Source:** BLG-FE-175
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- All 4 components verified against their own actual current `duration` value and brought to `max(delay) + duration ≤ 500ms`
- Each component removed from `design_system.md`'s known-non-compliant list in the same commit that fixes it
- No visual regression beyond the timing change itself — existing Playwright coverage, if any, still passes

### ST-42 — Bring 9 non-conforming toast call sites into line with the Toast Notification Timing standard
**Source:** BLG-FE-176
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- All 9 call sites named in the inventory conform to `design_system.md` v1.17's Toast Notification Timing table
- `design_system.md`'s non-conforming-screens table updated to reflect the fix (or the table removed/marked historical if all sites now conform)
- No visual regression beyond the timing change itself

### ST-43 — Arc 5 low-trade-volume advisory: surface the 20-trade threshold and remaining-trades count, reconsider placement above the stat grid
**Source:** BLG-UX-05
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Placement and copy decision recorded (keep as-is, or specify the change)
- If changed: `arc5_compliance_section.md` updated in the same commit as the implementation, existing Playwright coverage (`tests/e2e/arc5-compliance-section.spec.js`) still passes

---
