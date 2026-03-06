**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-03-06
**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9
**Sprint:** 1 of 2
**Sprint Goal:** Fully resolve all Risk Dashboard deviations from v1.8, establish reproducible test infrastructure that closes the v1.8 scenario coverage gap, and complete the documentation hygiene backlog — leaving the codebase defect-free and documentation-complete as the foundation for the feature sprint.

---

# Sprint Backlog — 2026-03-06__release-v1.9 Sprint 1

---

## Sprint Scope

---

### EPIC-04 — Risk Dashboard Defect Resolution

**Maps to:** S2-05 through S2-15
**Owner:** Head of Engineering (implementation); Head of Specs Team (ST-06 spec alignment)
**Estimated effort:** ~14.5 hours (mid; ST-06 pre-completed)
**Risk IDs:** RISK-05 (monitor), RISK-06 (resolved)
**Execution sequence:** Wave 1 (ST-06 done, ST-07, ST-10) → Wave 2 (ST-08, ST-09)

---

#### ST-06 — Drawdown Data Source Spec Alignment

**Owner:** Head of Specs Team
**Estimated effort:** N/A — **PRE-COMPLETED 2026-03-06**
**Delegation class:** autonomous

**Status:** COMPLETE. Head of Specs Team decision 2026-03-06:
- `current_drawdown_percent` → `GET /portfolio` (confirmed)
- `days_underwater` → `GET /analytics/metrics` (confirmed)
- `risk_dashboard.md §4.1` updated to v0.1.7; DEV-ST03-08 resolved; BLG-RD-08 closed.

**No execution work required.**

---

#### ST-07 — Risk Dashboard Backend: US Currency Conversion

**Owner:** Head of Engineering
**Estimated effort:** 3–6 hours
**Delegation class:** delegated_backend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `backend/services/portfolio_service.py` converts `entry_price` to GBP for US positions using stored `fx_rate` (same pattern as existing `current_price` conversion). `portfolio_service.py` converts `current_stop` to GBP for US positions using the same `fx_rate`. All position prices returned in GBP for both US and UK positions. Stop Distance % calculation uses matching currencies. |
| Quality | Golden output tests updated to include a US position with GBP-converted `entry_price` and `current_stop`. Golden output CI passes with no regression. Existing UK position values unchanged. Scenario: US position entry price and stop price display as GBP on Risk Dashboard. |
| Security | N/A — backend computation change only; no new endpoint, no new data exposure. |
| Verification | Director of Quality confirms golden output CI passes. SC-RD scenarios for US position currency display pass against live or seeded environment. |

**Dependencies:** None
**Notes:** Deploy before ST-08 and ST-09 frontend work, or provide mock. Key enabler for all remaining EPIC-04 frontend items.

---

#### ST-08 — Risk Dashboard Frontend: Error States & Entity Fallback

**Owner:** Head of Engineering / Base44 Frontend Prompt Owner
**Estimated effort:** 2–4 hours
**Delegation class:** delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Each Risk Dashboard component (HeatGauge, DrawdownSummary, GracePeriodPanel, PositionRiskTable, ProspectiveHeatPanel) renders its own error state independently when `GET /portfolio` fails. Entity store fallback (`base44.entities`) does not silently mask API failure — either error indicator shown while fallback active, or fallback removed. GracePeriodPanel renders a distinct error card (not empty state) when `portfolioError` is set. |
| Quality | Scenarios SC-RD-02 (portfolio API error → error state shown) and SC-RD-03 (GracePeriodPanel error vs empty state). Verified by simulating API failure (mock 500 or network error). Error indicator visually distinct from "no data" state. |
| Security | N/A — frontend display logic only. |
| Verification | Director of Quality executes SC-RD-02 and SC-RD-03 against seeded test environment. Confirms error state is visually distinct from empty state for GracePeriodPanel. |

**Dependencies:** ST-07 (soft — deploy backend first or use mock)
**Notes:** RISK-05 — Base44 entity store fallback approach to be confirmed at execution pre-alignment with Base44 Frontend Prompt Owner.

---

#### ST-09 — Risk Dashboard Frontend: Table and Column Fixes

**Owner:** Head of Engineering
**Estimated effort:** 2–4 hours
**Delegation class:** delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | PositionRiskTable sorted by stop distance ascending (tightest first = most at risk) within each state group per spec §6.4. Stop Price column (`current_stop`, GBP, 2 dp) present in PositionRiskTable per spec §6.2. Days in Grace (`holding_days`) column present in Grace Period table per spec §5.2. Threshold label badge present in ProspectiveHeatPanel result row, updating when boundary crossed, per spec §7.5. |
| Quality | Scenarios SC-RD-04 (sort ascending with 3+ positions), SC-RD-05 (Stop Price column present), SC-RD-07 (Days in Grace column present), SC-RD-08 (threshold label badge updates on boundary cross). |
| Security | N/A — frontend display only. |
| Verification | Director of Quality executes all four scenarios. Confirms sort direction, column presence, and threshold label behaviour. |

**Dependencies:** ST-07 (soft)
**Notes:** Four independent fixes; may be implemented in a single Base44 prompt session alongside ST-08.

---

#### ST-10 — Risk Dashboard Frontend: HeatGauge and Cosmetic Fixes

**Owner:** Head of Engineering
**Estimated effort:** 1–3 hours
**Delegation class:** delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | GRACE state badge colour is blue (not amber) per spec §6.3. GBP value at risk displayed below gauge percentage value per spec §3.2. |
| Quality | Scenarios SC-RD-05 (GRACE badge is blue), SC-RD-06 (GBP value at risk visible below gauge). Verified visually. |
| Security | N/A — cosmetic frontend changes only. |
| Verification | Director of Quality visually confirms badge colour is blue and GBP value at risk is displayed beneath gauge percentage. |

**Dependencies:** None (cosmetic; independent of ST-07 backend)
**Notes:** Can be delivered in Wave 1 alongside ST-07 — no backend dependency.

---

### EPIC-05 — QA & Test Infrastructure (Sprint 1 items)

**Maps to:** S2-16, S2-17
**Owner:** QA & Testing Owner (ST-11); Backend Engineering Patterns Owner (ST-13)
**Estimated effort:** ~13 hours (mid; ST-12 deferred to Sprint 2)
**Risk IDs:** RISK-07 (monitor)
**Execution sequence:** Wave 1 (ST-11 infra setup, ST-13 independent)

---

#### ST-11 — Canonical Test Scenario Library Phase 1 (Risk Dashboard)

**Owner:** QA & Testing Owner
**Estimated effort:** 6–10 hours
**Delegation class:** delegated_qa

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Seeded test infrastructure created — approach agreed at sprint start (seeded SQLite, mock/stub API layer, or test fixture API). Infrastructure supports: specific `portfolio_heat_percent` values, positions with specific `grace_days_remaining`, empty position state, controlled prospective heat API responses. "Test Infrastructure Preconditions" section added to `docs/testing/risk_dashboard_scenarios.md`. All 17 NOT EXECUTED Risk Dashboard scenarios (SC-RD-02–06, SC-RD-07–12, SC-RD-15, SC-RD-16–18, SC-RD-24–25) re-run against seeded environment. Results recorded in `risk_dashboard_scenarios.md`. |
| Quality | Infrastructure is reproducible — "Test Infrastructure Preconditions" section sufficient for independent replication. No scenario relies on live external data. |
| Security | N/A — test infrastructure only; no production data used. |
| Verification | Director of Quality confirms all 17 scenarios have a recorded result (PASS/FAIL/BLOCKED) in `risk_dashboard_scenarios.md`. Confirms "Test Infrastructure Preconditions" section present and sufficient. |

**Dependencies:** None
**Notes:** RISK-07 — approach decision (seeded DB vs mock layer) to be agreed with Head of Engineering at sprint start. Record chosen approach in "Test Infrastructure Preconditions" section.

---

#### ST-13 — Service Layer Test Coverage Standard

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 3–6 hours
**Delegation class:** delegated_backend + delegated_qa

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Service Layer Test Coverage Standard authored in `docs/specs/backend_engineering_patterns.md` (version incremented) or as a referenced document. Includes: named coverage threshold (% agreed at sprint start), scope definition (`backend/services/` directory), tool (pytest-cov or equivalent). CI workflow step added: runs pytest-cov on `backend/services/`; build fails if coverage falls below threshold. |
| Quality | CI run with current test suite confirms threshold is enforced. Coverage at or above threshold: build passes. Behaviour below threshold confirmed to fail build (demonstrated by controlled test). |
| Security | N/A — CI/quality tooling addition only. |
| Verification | Director of Quality confirms CI workflow YAML contains the coverage step and threshold is named. `backend_engineering_patterns.md` version confirmed incremented. |

**Dependencies:** None
**Notes:** Threshold value to be agreed between Backend Engineering Patterns Owner and Head of Engineering at sprint start. Record in standard document.

---

### EPIC-06 — Documentation Hygiene & Governance

**Maps to:** S2-19 through S2-30
**Owner:** Head of Specs Team (coordinator)
**Estimated effort:** ~18 hours (mid)
**Risk IDs:** RISK-08 (closed), RISK-09 (monitor)
**Execution sequence:** Wave 1 — all items autonomous, fully parallelisable

---

#### ST-14 — Canonical Terms Glossary

**Owner:** Head of Specs Team
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Glossary created as Class 2 Supporting document with lifecycle-compliant header. Minimum terms defined: portfolio heat, grace period, stop distance, R-multiple, cohort, journal completion rate, stop-based exit rate. Each term: definition + link to Class 1 canonical source. No new canonical definitions introduced. Registered in `docs/specs/Specs_Index.md`. |
| Quality | Lifecycle compliance check passes (all required header fields present). Spot-check: 3 terms — definitions match referenced Class 1 source. |
| Security | N/A — documentation only. |
| Verification | Head of Specs Team confirms lifecycle compliance. Director of Quality spot-checks 3 terms. |

**Dependencies:** None

---

#### ST-15 — AI-Assisted Workflow Governance Policy

**Owner:** Product Owner / AI Compliance & Governance Officer
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Policy document created in `docs/governance/` or `claude/charter/` with lifecycle-compliant header. Covers all 4 areas: (a) AI authority scope; (b) mandatory human review checkpoints; (c) escalation triggers; (d) record-keeping obligations. |
| Quality | Lifecycle compliance check passes. Content spot-check: all 4 policy areas present and non-empty. |
| Security | N/A — governance document. |
| Verification | Product Owner confirms policy covers all 4 required areas and is filed in correct path. |

**Dependencies:** None

---

#### ST-16 — Document GET /market/status Endpoint

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `docs/specs/api_contracts/market_endpoints.md` created (Class 1 Canonical, v0.1). Covers: GET /market/status request, response schema (SPY/FTSE regime, live FX rate), error behaviour. Registered in `docs/specs/Specs_Index.md §3`. `docs/reference/openapi.yaml` updated with GET /market/status schema. |
| Quality | openapi-drift CI passes after openapi.yaml update. Lifecycle compliance check passes. Response schema consistent with backend implementation. |
| Security | N/A — documentation of existing endpoint; no code change. |
| Verification | Director of Quality confirms openapi-drift CI passes. Head of Specs Team confirms Specs_Index.md updated. |

**Dependencies:** None

---

#### ST-17 — Create settings_model.md

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `docs/specs/data_model/settings_model.md` created (Class 1 Canonical, v0.1). Covers: all settings field names, types, validation rules, defaults per confirmed PATCH /settings/{settings_id} + POST /settings shape. Registered in `docs/specs/Specs_Index.md §3`. Cross-referenced from `docs/specs/api_contracts/settings_endpoints.md`. |
| Quality | Lifecycle compliance check passes. Field list spot-checked against settings endpoint. |
| Security | N/A — data model documentation; no code change. |
| Verification | Head of Specs Team confirms field list matches implementation. Specs_Index.md and settings_endpoints.md cross-references confirmed. |

**Dependencies:** None

---

#### ST-18 — Define Error Response Standard

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Error Response Standard created as Class 1 Canonical document or new section in an existing API contracts document. Covers: standard error envelope shape, required fields (status_code, error_code, message, detail), HTTP status code mapping. All existing API contract docs updated to reference the standard for their error sections. Registered in `docs/specs/Specs_Index.md`. |
| Quality | Lifecycle compliance check passes for the new standard. Spot-check: at least 2 existing API contract error sections reference the standard. |
| Security | N/A — documentation only. |
| Verification | Head of Specs Team confirms all existing API contract docs reference the standard. Director of Quality spot-checks 2 cross-references. |

**Dependencies:** None

---

#### ST-19 — Spec/Doc Debt Small Fixes (7 items)

**Owner:** Head of Specs Team (coordinator)
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | All 7 items complete: (BLG-SPEC-D1) `docs/specs/api_contracts/README.md` header + changelog updated to v1.9.0. (BLG-SPEC-D4) `position_endpoints.md` includes GET /positions/search/tags with parameters + response schema. (BLG-SPEC-D8) `docs/System_status_report.md` lifecycle header added. (BLG-SPEC-D9) `docs/governance/process_index.md` and `docs/specs/Specs_Index.md §5` reference `claude/charter/document_lifecycle_guide.md`. (BLG-SPEC-G3) `docs/specs/Specs_Index.md §3` includes structured_logging_standards.md. (BLG-SPEC-G4) ADR-002 confirmed present in `docs/product/decisions/`; cross-references updated. (BLG-SPEC-G5) `docs/specs/validation_system.md` owner field updated to a named governance role. |
| Quality | Lifecycle compliance check passes for all 7 documents. Head of Specs Team spot-checks each item. |
| Security | N/A — documentation only; no code changes. |
| Verification | Head of Specs Team confirms all 7 items complete. |

**Dependencies:** None
**Notes:** RISK-09 — verify ADR-002 location before attempting BLG-SPEC-G4. ~30 min per item; can be batched as a single commit.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Confirmed capacity (sprint, 1–2 weeks) | ~15–25 hours |
| Sprint 1 items in scope | 12 (ST-06 pre-completed; 11 remaining + ST-06) |
| Sprint 1 estimated effort (mid) | ~42 hours |
| Sprint 1 utilisation | ~170–280% (over-allocated; ~3–4 weeks elapsed at current pace) |
| Over-allocation | Yes — accepted by Product Owner (Option B phased approach, 2026-03-06) |
| Sprint 2 deferred effort (mid) | ~49 hours |

---

## Items Deferred to Sprint 2

| Item | EPIC | Title | Reason |
|------|------|-------|--------|
| ST-01 | EPIC-01 | Canonicalise Basic Compliance Metrics | Product Owner phased approach decision — Sprint 2 |
| ST-02 | EPIC-01 | Structured Trade Reflection Template | Product Owner phased approach decision — Sprint 2 |
| ST-03 | EPIC-02 | Cohort Analysis | Product Owner phased approach decision — Sprint 2 |
| ST-04 | EPIC-02 | R-Multiple Distribution Report | Product Owner phased approach decision — Sprint 2 |
| ST-05 | EPIC-03 | Dashboard Homepage / Session Summary | Product Owner phased approach decision — Sprint 2 |
| ST-12 | EPIC-05 | Canonical Test Scenario Library Phase 2 | Depends on Sprint 2 feature delivery |

Sprint 2 items remain in the release planning backlog slice. A new sprint planning run (`plan sprint --cycle 2026-03-06__release-v1.9`) will be required to seal Sprint 2 once Sprint 1 is verified.

---

## Outstanding Actions at Sprint Start (non-blockers)

| Action | Owner | Blocker? |
|--------|-------|---------|
| Agree ST-11 test infra approach (seeded DB vs mock layer) | QA & Testing Owner + Head of Engineering | No — decide at ST-11 start |
| Agree ST-13 coverage threshold % | Backend Engineering Patterns Owner + Head of Engineering | No — decide at ST-13 start |
| Verify ADR-002 location (RISK-09) before ST-19/BLG-SPEC-G4 | Head of Specs Team | No — check at ST-19 start |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** confirmed — 2026-03-06
**Scope confirmed:** confirmed — Option B (phased approach, Sprint 1 of 2), 2026-03-06
**Capacity over-allocation explicitly accepted:** confirmed — ~42 hrs (~3–4 weeks elapsed at current pace), 2026-03-06
**Signed off by:** Product Owner
**Date:** 2026-03-06
