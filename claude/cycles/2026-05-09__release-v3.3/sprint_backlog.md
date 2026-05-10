**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-10
**Cycle:** 2026-05-09__release-v3.3
**Release:** v3.3
**Sprint Goal:** Establish the Arc 3 in-trade risk management foundation by shipping a deterministic position lifecycle state machine with visible state display, two §13-compliant decision-support prompts (grace period alert and ATR trail stop management), comprehensive research view spec and QA closure, and all outstanding governance patches.
**Backlog Slice Source:** original `claude/cycles/2026-05-09__release-v3.3/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-05-09__release-v3.3

---

## Sprint Scope

---

### Sprint 1

Sprint 1 delivers the Arc 3 data foundation (EPIC-01), research view spec and QA closure (EPIC-03), and all governance patches (EPIC-04 ST-13/14/15). Target: ~10 stories, ~9–13d effort.

---

#### EPIC-01 — Arc 3 Foundation: Position Lifecycle Manager

**Maps to:** S2-01
**Owner:** Head of Engineering
**Estimated effort:** ~2.5–5d
**Risk IDs:** RISK-01
**Execution sequence:** Sprint 1 (items 4, 6, 11 — after ST-13/14/15 governance and parallel with EPIC-03)

##### ST-01 — Positions data model: add lifecycle state fields and migration

**Owner:** Head of Engineering
**Estimated effort:** XS–S (~0.5–1d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None
**Notes:** RISK-01 mitigated — back-fill strategy resolved: GRACE if within last 10 trading days; UNKNOWN otherwise. Both are valid display states (ST-03 UX spec §6 covers UNKNOWN). Migration must be reversible (down migration required per AC).

---

##### ST-02 — Position lifecycle state machine backend service

**Owner:** Head of Engineering
**Estimated effort:** S–M (~1–2d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** ST-01 (data model fields must be present)
**Notes:** Service callable on demand; no automatic state mutation (§13 compliant). 5 state paths: GRACE, LOSING, PROFITABLE, EXIT ZONE, UNKNOWN. Unit tests cover all 5 paths.

---

##### ST-03 — Position lifecycle state: frontend display

**Owner:** Head of Engineering
**Estimated effort:** S–M (~1–2d)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** ST-02 (backend service must be complete); design gate UX spec locked — `docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md`; frontend spec: `docs/specs/frontend/pages/positions.md` v1.5
**Notes:** Feature flag proof-of-concept — `arc3_lifecycle_display` flag wraps lifecycle badge per BLG-FEAT-13 (ST-16 provides the flag infrastructure; ST-03 implements the badge behind it). Playwright E2E scenario required. Human staging sign-off required for badge states not covered by Playwright. Test scenario gap flag: EPIC-01 test_scenarios pending — QA & Testing Owner to author before Sprint 2.

---

#### EPIC-03 — Research View Spec & QA Closure

**Maps to:** S2-03
**Owner:** Head of Specs Team
**Estimated effort:** ~4.5–9d
**Risk IDs:** RISK-03
**Execution sequence:** Sprint 1 (items 5, 7, 8, 9, 10 — starts day 1 in parallel with EPIC-01)

##### ST-08 — PT-02 research API contract (BLG-SPEC-25) + data source provenance spec (BLG-SPEC-26)

**Owner:** Head of Specs Team (SPEC-25: API Contracts & Documentation Owner; SPEC-26: Head of Specs Team)
**Estimated effort:** S–M (~1–2d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** None
**Notes:** Spec-first: start day 1 of Sprint 1. RISK-03 mitigation — must complete before ST-09, which must complete before EPIC-02 frontend designs finalise (Sprint 2).

---

##### ST-09 — PT-02 canonical research view spec (BLG-SPEC-24) + UX spec (BLG-FE-28)

**Owner:** Head of Specs Team (canonical spec); Frontend UX Documentation Owner (UX spec)
**Estimated effort:** S–M (~1–2d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** ST-08 (canonical spec references provenance spec for source attribution)
**Notes:** Design gate classification: Design Not Applicable — this story IS the design and spec work. No pre-gate artefact required. UX spec output location: `docs/design/2026-05-09__release-v3.3/research-view/ux_spec.md`. Canonical spec: `docs/specs/frontend/pages/research_view.md`.

---

##### ST-10 — Research view test scenario library (BLG-QA-17) + acceptance test protocol (BLG-QA-15)

**Owner:** Director of Quality
**Estimated effort:** XS–S (~0.5–1d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** ST-09 (test scenarios reference canonical spec field list and UX spec)
**Notes:** Both documents reviewed by Director of Quality before Sprint 2 begins (QA readiness gate for EPIC-02 sign-off).

---

##### ST-11 — Entry checklist Playwright E2E tests (BLG-QA-14)

**Owner:** QA & Testing Owner
**Estimated effort:** S–M (~1–2d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** None (entry checklist shipped v3.2; tests are additive)
**Notes:** 7 scenarios SC-CL-01 through SC-CL-07. Scenarios registered in execution_state.json test_scenarios for EPIC-02 (v3.2 trade plan domain). All scenarios must pass in CI.

---

##### ST-12 — Research endpoint integration tests (BLG-QA-16) + latency baseline (BLG-OPS-15) + trade plan sensitivity classification (BLG-SEC-06) + field extension governance (BLG-GOV-20)

**Owner:** QA & Testing Owner (QA-16); Infrastructure & Operations Owner (OPS-15); Cybersecurity & Trust Lead (SEC-06); Data Model Domain & Schema Owner (GOV-20)
**Estimated effort:** S–M (~1–2d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** ST-08, ST-09 (integration test references /research/{ticker} endpoint contract; latency baseline references spec)
**Notes:** Addresses OA-06 (endpoint coverage gap). Cybersecurity & Trust Lead sign-off required for SEC-06 doc. Data Model owner sign-off required for GOV-20 doc.

---

#### EPIC-04 — Governance Patches + Mandatory Quick Wins (Sprint 1 stories)

**Maps to:** S2-04
**Owner:** PMO Lead + Head of Specs Team
**Sprint 1 items:** ST-13, ST-14, ST-15
**Estimated effort Sprint 1:** ~1.25d
**Risk IDs:** RISK-04 (ST-16 only — in Sprint 2)
**Execution sequence:** Sprint 1 (items 1, 2, 3 — earliest priority; unblocked)

##### ST-13 — execution_prompt.md governance patches: sealed-file check (OA-01/CF-01) + mock payload advisory (OA-02/CF-02)

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.5d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** None
**Notes:** CLAUDE.md §6 checklist mandatory in same commit: version bump (execution_prompt.md → next version), OPERATIONAL_GUIDE §14 update, prompt_change_log.md PREPENDED row. Resolves OA-01 (CF-01) and OA-02 (CF-02) from v3.2 closure.

---

##### ST-14 — Governance policy patches: design gate "before sprint planning" check (OA-05) + backlog 3-cycle deferral policy (OA-03/CF-03)

**Owner:** Head of Specs Team (sprint_planning_prompt.md); PMO Lead (backlog_management_prompt.md)
**Estimated effort:** XS (~0.5d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** None
**Notes:** CLAUDE.md §6 checklist mandatory for both prompt files in same commit. Policy document `docs/governance/backlog_deferral_policy.md` created as standalone reference. Resolves OA-03 (CF-03) and OA-05.

---

##### ST-15 — PT-05 entry checklist §13 compliance review (BLG-GOV-19)

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** XS (~0.25d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`
**Dependencies:** None
**Notes:** Strategy Rules & System Intent Owner sign-off recorded in doc. Document referenced in trade plan spec. Contingency: if Sprint 1 is capacity-constrained, ST-15 can move to Sprint 2 without impacting sequencing.

---

### Sprint 2

Sprint 2 delivers EPIC-02 Arc 3 decision-support prompts (depends on EPIC-01 complete) and EPIC-04 mandatory feature flag + quick wins. Target: ~7 stories, ~7–10d effort.

---

#### EPIC-02 — Arc 3 Decision Support: Grace Period + Stop Management

**Maps to:** S2-02
**Owner:** Head of Engineering
**Estimated effort:** ~3–6d
**Risk IDs:** RISK-02
**Execution sequence:** Sprint 2 (after EPIC-01 complete)
**Prerequisite:** EPIC-01 all stories done; EPIC-03 ST-08/09 complete (spec alignment for frontend)

##### ST-04 — Grace Period Decision Support backend (IT-02)

**Owner:** Head of Engineering
**Estimated effort:** XS–S (~0.5–1d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** EPIC-01 complete (position_state and lifecycle service infrastructure)
**Notes:** Endpoint `GET /positions/grace-period-alerts` must be registered in backend/routers/test.py AND openapi.yaml in same commit (CLAUDE.md §2 non-negotiables). §13 compliant: display-only endpoint.

---

##### ST-05 — Grace Period Decision Support frontend (IT-02)

**Owner:** Head of Engineering
**Estimated effort:** S–M (~1–2d)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** ST-04 (backend endpoint); design gate UX spec locked — `docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md`; frontend spec: `docs/specs/frontend/pages/positions.md` v1.5
**Notes:** §13 display-only: no automated recommendation generated. Dismissed state in localStorage (no backend persistence). Playwright scenario required. Test scenario gap flag: EPIC-02 test_scenarios pending.

---

##### ST-06 — Stop Management Workflow backend (IT-03)

**Owner:** Head of Engineering
**Estimated effort:** XS–S (~0.5–1d)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** EPIC-01 complete (position_state infrastructure; stop price join shipped v2.4)
**Notes:** Endpoint `GET /positions/{id}/stop-trail` must be registered in backend/routers/test.py AND openapi.yaml in same commit. Null-safe: if current_stop is null, return trail calculation with null stop/difference; frontend disables trail button. trail_multiplier defaults to 2.0 (configurable per strategy_rules.md).

---

##### ST-07 — Stop Management Workflow frontend (IT-03)

**Owner:** Head of Engineering
**Estimated effort:** S–M (~1–2d)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** ST-06 (backend endpoint); design gate UX spec locked — `docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md`; frontend spec: `docs/specs/frontend/pages/positions.md` v1.5
**Notes:** §13: system presents recommendation; human confirms; no automated action. "Trail Stop" button visible only for PROFITABLE/EXIT ZONE state positions with current stop set. Playwright scenario required. Test scenario gap flag: EPIC-02 test_scenarios pending (combined with ST-05).

---

#### EPIC-04 — Governance Patches + Mandatory Quick Wins (Sprint 2 stories)

**Sprint 2 items:** ST-16, ST-17
**Estimated effort Sprint 2:** ~3–5d
**Risk IDs:** RISK-04 (ST-16)
**Execution sequence:** Sprint 2 (ST-16 after ST-03; ST-17 independent, can run parallel to ST-04/06)

##### ST-16 — Feature flag rollout (BLG-FEAT-13) — mandatory

**Owner:** Head of Engineering
**Estimated effort:** S–M (~1–2d)
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`
**Dependencies:** ST-03 complete (proof-of-concept flag `arc3_lifecycle_display` wraps the lifecycle badge from ST-03)
**Notes:** BLG-FEAT-13 is mandatory for v3.3 — 3rd consecutive deferral. Scope strictly controlled: env-var or config-file only (no external service dependency). Pattern doc `docs/specs/platform/feature_flags.md` created as AC deliverable. No regression when flag disabled. RISK-04 mitigation: tight scope enforcement.

---

##### ST-17 — Trade plan abandonment + status badges (BLG-FEAT-21 + BLG-FE-30) + frontend quick wins (BLG-FE-23, BLG-FE-24, BLG-FE-25, BLG-FE-29)

**Owner:** Head of Engineering (implementation); Product Owner (feature sign-off)
**Estimated effort:** M–L (~2–3d)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`
**Dependencies:** None (self-contained; UX spec locked — `docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md`)
**Notes:** Multiple frontend specs updated: `docs/specs/frontend/pages/trade_plan.md` v0.3, `docs/specs/frontend/pages/watchlist.md` v0.3, `docs/specs/frontend/pages/signals.md` v0.2. Active position guard: cannot abandon plan with active positions (400 response). `abandonment_reason` field added to trade_plans table (nullable, required at API layer when status=abandoned). Contrast ratio ≥ 4.5:1 for all badge colours. Test scenario gap flag: EPIC-04 test_scenarios pending.

---

## Capacity Summary

| Metric | Sprint 1 | Sprint 2 | Cycle Total |
|--------|----------|----------|-------------|
| Total confirmed capacity | ~8–12d | ~8–12d | ~16–24d |
| Mid-point capacity | ~10d | ~10d | ~20d |
| Total estimated effort (in-scope) | ~9.5–14d | ~6.5–11d | ~16–25d |
| Mid-point estimated effort | ~10.75d | ~8.75d | ~19.5d |
| Utilisation (mid-point) | ~107% | ~87.5% | ~97.5% |
| Over-allocation | ⚠ Sprint 1 borderline — contingency: ST-15 can move to Sprint 2 | No | Product Owner must acknowledge |

---

## Items Deferred This Sprint

None — all 17 backlog slice items are included in sprint scope.

---

## Deferred Execution Blockers Accepted

*(Section omitted — deferred_execution_blockers was empty in state.json)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Product Owner: explicitly acknowledge capacity WARN (⚠ Sprint 1 borderline; cycle mid-point ~97.5% utilisation) | Product Owner | Yes |
| Product Owner: confirm sprint goal statement | Product Owner | Yes |
| Product Owner: confirm scope (all 17 stories across 2 sprints) | Product Owner | Yes |
| QA & Testing Owner: author test scenarios for EPIC-01, EPIC-02, EPIC-04 delegated_frontend items before respective sprint closes | QA & Testing Owner | No (before sprint close) |
| EPIC-04 ST-13/14 execution: CLAUDE.md §6 checklist for governance prompt edits (version bump + OPERATIONAL_GUIDE + prompt_change_log.md PREPENDED) | Head of Specs Team / PMO Lead | No (execution phase) |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** approved
**Scope confirmed (17 stories / 4 EPICs / 2 sprints):** approved
**Capacity WARN acknowledged (Sprint 1 borderline; cycle ~97.5% mid-point utilisation; contingency: ST-15 to Sprint 2 if constrained):** approved
**Deferred execution blockers accepted:** N/A
**Signed off by:** Product Owner
**Date:** 2026-05-10
