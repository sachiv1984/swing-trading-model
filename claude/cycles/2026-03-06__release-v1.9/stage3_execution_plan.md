# Stage 3 — Execution Plan

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9
**Last Updated:** 2026-03-06

---

## EPIC Structure Overview

| EPIC | Theme | S2 Items | Sequencing |
|------|-------|----------|------------|
| EPIC-01 | Trade Reflection & Compliance Metrics | S2-01, S2-02 | S2-02 must complete before S2-01 (metrics definitions gate) |
| EPIC-02 | Analytics Enhancements | S2-03, S2-18 | S2-18 after BLG-FEAT-08 metrics defs (same constraint as S2-01) |
| EPIC-03 | Dashboard Homepage | S2-04 | Independent |
| EPIC-04 | Risk Dashboard Defect Resolution | S2-05–S2-15 | S2-12 (spec alignment) must complete first; S2-14 and S2-15 share root cause — implement together |
| EPIC-05 | QA & Test Infrastructure | S2-16, S2-17 | S2-16 Phase 1 before new feature scenarios (Phase 2); S2-17 independent |
| EPIC-06 | Documentation Hygiene & Governance | S2-19–S2-30 | S2-22 (settings_model) after existing EPIC-03 v1.8 deliverables confirmed stable; S2-21 and S2-23 can run in parallel |

**Recommended execution sequence:**
1. EPIC-04 (Risk Dashboard defects — clears known deviations; backend changes inform subsequent QA)
2. EPIC-05 Phase 1 (seeded test infrastructure — enables scenario execution for EPIC-04 defects)
3. EPIC-01 (compliance metrics definitions → reflection template)
4. EPIC-02 (cohort analysis + R-multiple distribution, share metrics defs capacity with EPIC-01)
5. EPIC-03 (dashboard homepage — independent, uses existing endpoints)
6. EPIC-06 (documentation hygiene — can run in parallel with above, no code dependencies)
7. EPIC-05 Phase 2 (new feature scenario authoring — after above features delivered)

---

## EPIC-01 — Trade Reflection & Compliance Metrics

**Maps to:** S2-01, S2-02
**Owner:** Head of Specs Team (spec); Head of Engineering (implementation)
**Domain:** Backend + Frontend + Canonical Spec update

### Scope

**S2-02 — Basic Compliance Metrics (pre-work)**
- Metrics Definitions & Analytics Owner canonicalises 3 metrics in `metrics_definitions.md`:
  - Journal completion rate
  - Stop-based exit rate
  - Average position size (% of portfolio)
- Backend: compute and expose metrics via appropriate endpoint (existing or new analytics extension)
- Frontend: display on analytics page or settings/compliance panel
- Acceptance gate: definitions canonical before any frontend or backend implementation begins

**S2-01 — Structured Trade Reflection Template**
- Frontend: post-trade reflection form at trade close
- Pre-populated from trade record: hold time, R-multiple, exit reason, position state history
- Structured prompts: trade rationale, what worked, what didn't, discipline assessment
- No AI — deterministic and testable
- Spec document required: `docs/specs/frontend/pages/trade_reflection.md` (new)

### Sequencing Constraint
S2-02 must be complete (metrics definitions canonical) before S2-01 implementation begins.

### Acceptance Gate
- metrics_definitions.md updated and canonical (Class 1, version incremented)
- All 3 compliance metrics computable from existing data
- Reflection form renders pre-populated trade data
- Reflection entries stored and retrievable
- All new endpoints documented in API contracts

### Risks

**RISK-01 — Metrics Definitions owner capacity (LL-05)**
Relates to: EPIC-01
The roadmap explicitly flags (LL-05) that the Metrics Definitions & Analytics Owner must be confirmed available before BLG-FEAT-08 enters pre-alignment. This owner was committed to EPIC-03 in v1.7. Mitigation: FinOps & Resource Architect confirms availability in Stage 4.5.
Priority: Medium — does not block planning; must confirm before sprint planning.

**RISK-02 — Trade reflection data model**
Relates to: EPIC-01
Reflection entries require storage. If the existing notes/journal schema cannot accommodate structured fields, a data model change is required. Mitigation: Data Model & Domain Schema Owner reviews at pre-alignment. If schema change needed, add to data_model.md before sprint planning.
Priority: Low — likely solvable with existing notes structure; needs confirmation.

---

## EPIC-02 — Analytics Enhancements

**Maps to:** S2-03, S2-18
**Owner:** Head of Engineering
**Domain:** Backend + Frontend + Canonical Spec update

### Scope

**S2-03 — Cohort Analysis**
- Group closed trade performance by entry period (month, quarter, year)
- Derivable from existing trade data — no new data dependencies
- Backend: new query or analytics endpoint extension
- Frontend: new chart component on Performance Analytics page (cohort analysis tab/panel)
- Spec: cohort metric definitions added to `metrics_definitions.md`; frontend spec updated

**S2-18 — R-Multiple Distribution Report**
- Backend: compute R-multiple per closed trade from existing trade data
- Metrics Definitions & Analytics Owner defines R-multiple formula in `metrics_definitions.md`
- Frontend: distribution chart/panel on Performance Analytics page
- No client-side derivation; values from canonical backend formula

### Sequencing Constraint
S2-18 shares the BLG-FEAT-08 metrics definitions dependency: Metrics Definitions owner must be available. Recommend batching metric definition work (S2-02, S2-03 cohort defs, S2-18 R-multiple def) into a single metrics_definitions.md update.

### Acceptance Gate
- Cohort metric definitions and R-multiple formula canonical in metrics_definitions.md
- Cohort analysis renders on analytics page with period selector
- R-multiple distribution chart renders on analytics page
- Values consistent with canonical backend formula
- All endpoints documented

### Risks

**RISK-03 — Metrics definition batching risk**
Relates to: EPIC-02
If Metrics Definitions owner updates are batched across EPIC-01 and EPIC-02, sequencing dependency tightens. Mitigation: confirm single metrics_definitions.md update sprint covers all three (compliance metrics, cohort defs, R-multiple).
Priority: Low.

---

## EPIC-03 — Dashboard Homepage

**Maps to:** S2-04
**Owner:** Head of Engineering (implementation); Frontend Specs & UX Documentation Owner (spec)
**Domain:** Backend (optional composite endpoint) + Frontend

### Scope

**S2-04 — Dashboard Homepage / Session Summary**
- Home page displaying: open positions count, total portfolio heat, positions in grace period today, today's signal status, recent trade activity summary
- All data from existing endpoints: `GET /portfolio`, `GET /positions`, `GET /signals`
- Optional composite endpoint (`GET /dashboard/summary` or equivalent) — engineering decision at pre-alignment
- Frontend spec required: `docs/specs/frontend/pages/dashboard_home.md` (new)

### Acceptance Gate
- Dashboard home page renders on load with all 5 data categories
- All values sourced from existing canonical endpoints
- If composite endpoint added: documented in API contracts and openapi.yaml
- Frontend spec filed and canonical

### Risks

**RISK-04 — Composite endpoint scope creep**
Relates to: EPIC-03
A composite endpoint could expand to aggregate business logic not currently in scope. Constraint: composite endpoint must only aggregate — no new computations. Any new computation requires metrics_definitions.md update.
Priority: Low.

---

## EPIC-04 — Risk Dashboard Defect Resolution

**Maps to:** S2-05, S2-06, S2-07, S2-08, S2-09, S2-10, S2-11, S2-12, S2-13, S2-14, S2-15
**Owner:** Head of Engineering (implementation); Frontend Specs & UX Documentation Owner (spec alignment)
**Domain:** Backend + Frontend

### Scope (grouped by root cause)

**Group A — Spec alignment required first**
- **S2-12 (BLG-RD-08)** — Head of Specs Team verifies drawdown data source (GET /portfolio vs GET /analytics/metrics). Must complete before other defects are confirmed against spec. This is a documentation task only.

**Group B — Currency conversion (shared root cause: BLG-RD-10 + BLG-RD-11)**
- **S2-14 (BLG-RD-10)** — portfolio_service.py converts entry_price to GBP for US positions
- **S2-15 (BLG-RD-11)** — portfolio_service.py converts current_stop to GBP for US positions
  - Implement together: same FX conversion pattern; same file; affects Stop Distance % display

**Group C — Backend: none; Frontend fixes**
- **S2-05 (BLG-RD-01)** — Remove/correct entity store fallback; each component renders own error state
- **S2-07 (BLG-RD-03)** — PositionRiskTable: sort ascending by stop distance
- **S2-08 (BLG-RD-04)** — PositionRiskTable: add Stop Price column
- **S2-10 (BLG-RD-06)** — HeatGauge: add GBP value at risk
- **S2-11 (BLG-RD-07)** — GracePeriodPanel: add Days in Grace column
- **S2-13 (BLG-RD-09)** — ProspectiveHeatPanel: add threshold label badge

**Group D — Small cosmetic fixes**
- **S2-06 (BLG-RD-02)** — GracePeriodPanel: distinct error vs empty state
- **S2-09 (BLG-RD-05)** — GRACE badge: amber → blue

### Sequencing Within EPIC-04
1. S2-12 (spec alignment) — Head of Specs Team decision; parallelisable with everything else but must close before final verification
2. S2-14 + S2-15 (backend) — implement together, deploy first to unblock frontend currency display
3. Groups C and D (frontend) — after backend currency fix deployed or mocked

### Acceptance Gate
- S2-12: risk_dashboard.md §4.1 updated with confirmed data source
- S2-14 + S2-15: all position prices in GBP on Risk Dashboard for US and UK positions
- All 11 deviation items (BLG-RD-01–11) resolved and corresponding DEV-ST03-xx closed
- Golden output tests pass (no regression on existing CI)
- risk_dashboard.md §11 deviations section updated to mark each item resolved

### Risks

**RISK-05 — Entity store fallback (BLG-RD-01) — frontend-only or requires Base44 config change**
Relates to: EPIC-04
The Base44 entity store fallback is a platform-level behaviour. Removing it may require Base44 platform configuration or prompt changes. The Base44 Frontend Prompt Owner may need to update the frontend prompt. Mitigation: confirm at pre-alignment whether entity store can be disabled per component.
Priority: Medium.

**RISK-06 — S2-12 spec alignment may reveal additional backend/frontend misalignment**
Relates to: EPIC-04
If Head of Specs Team confirms GET /analytics/metrics (not GET /portfolio) as the canonical drawdown source, additional backend and frontend work is required beyond the current EPIC-04 scope. Mitigation: S2-12 decision must be made before sprint planning seal.
Priority: High — escalate immediately if decision not available at pre-alignment.

---

## EPIC-05 — QA & Test Infrastructure

**Maps to:** S2-16, S2-17
**Owner:** QA & Testing Owner (S2-16); Backend Engineering Patterns Owner (S2-17)
**Domain:** QA Infrastructure + CI

### Scope

**S2-16 — Canonical Test Scenario Library (Phase 1 + Phase 2)**
*Phase 1 — Resolve TEST-GAP-EPIC-01:*
- Create seeded test infrastructure (database seed or mock/stub API layer)
- Infrastructure must support: specific portfolio_heat_percent values, positions with specific grace_days_remaining, empty position state, controlled prospective heat API responses
- Re-run all 17 NOT EXECUTED Risk Dashboard scenarios against seeded environment
- Record results in risk_dashboard_scenarios.md
- Add "Test Infrastructure Preconditions" section to risk_dashboard_scenarios.md

*Phase 2 — v1.9 feature scenarios:*
- Author test scenarios for each new feature delivered in v1.9 at time of delivery
- Scenarios added to canonical library as each feature completes

**S2-17 — Service Layer Test Coverage Standard**
- Author Service Layer Test Coverage Standard
- Define minimum unit test coverage threshold for services/ directory
- Add CI step: pytest-cov (or equivalent) coverage check on services/ directory
- Build fails if coverage falls below threshold
- Standard integrated with / referenced from backend_engineering_patterns.md

### Acceptance Gate
- S2-16 Phase 1: all 17 NOT EXECUTED scenarios re-run and results recorded
- S2-16 Phase 2: new scenarios present in library for each v1.9 feature
- S2-17: coverage standard documented, CI step enforced, threshold agreed
- No reduction in existing CI gate coverage

### Risks

**RISK-07 — Seeded test infrastructure implementation approach**
Relates to: EPIC-05
Multiple implementation options exist: seeded SQLite, mock layer, test fixture API. Choice has implications for maintenance and CI integration time. Mitigation: QA & Testing Owner and Head of Engineering agree approach at pre-alignment; document in sprint backlog.
Priority: Medium.

---

## EPIC-06 — Documentation Hygiene & Governance

**Maps to:** S2-19, S2-20, S2-21, S2-22, S2-23, S2-24, S2-25, S2-26, S2-27, S2-28, S2-29, S2-30
**Owner:** Head of Specs Team (S2-19, S2-20, S2-21, S2-22, S2-23, S2-24, S2-25, S2-26, S2-27, S2-28, S2-29, S2-30)
**Domain:** Documentation only — no code changes

### Scope

**S2-19 (BLG-NEW-11) — Canonical Terms Glossary**
- Class 2 Supporting document
- Key terms: portfolio heat, grace period, stop distance, R-multiple, cohort, etc.
- Each term: definition + link to Class 1 canonical source
- Register in Specs_Index.md

**S2-20 (BLG-NEW-04) — AI-Assisted Workflow Governance Policy**
- Policy document governing which decisions may be taken by AI vs require human override
- Define: AI authority scope, mandatory human review checkpoints, record-keeping requirements
- File under appropriate governance path (claude/charter/ or docs/governance/)

**S2-21 (BLG-SPEC-D3) — Document GET /market/status**
- Create `docs/specs/api_contracts/market_endpoints.md`
- Document: request, response schema (SPY/FTSE regime, live FX rate), error behaviour
- Register in Specs_Index.md §3
- Add to openapi.yaml

**S2-22 (BLG-SPEC-G1) — settings_model.md**
- Create `docs/specs/data_model/settings_model.md`
- Cover: settings schema, field names, types, validation rules, defaults
- Register in Specs_Index.md §3
- Cross-reference from settings_endpoints.md
- Note: BLG-SPEC-D2 (PUT vs PATCH method drift) was resolved in v1.8 (ST-09) — no dependency blocker

**S2-23 (BLG-SPEC-G2) — Error Response Standard**
- Create or add section to canonical spec: standard error envelope shape, required fields, HTTP status code mapping
- Update all existing API contract docs to reference Error Response Standard
- Register in Specs_Index.md

**S2-24–S2-30 — Small fixes**
- S2-24: Update API Contracts README to v1.9.0 (Changelog + header)
- S2-25: Add GET /positions/search/tags to position_endpoints.md
- S2-26: Add lifecycle header to docs/System_status_report.md
- S2-27: Fix broken cross-references to document_lifecycle_guide.md (process_index.md + Specs_Index.md)
- S2-28: Register structured_logging_standards.md in Specs_Index.md §3
- S2-29: Move/copy ADR-002 to docs/product/decisions/
- S2-30: Fix validation_system.md owner field to a named governance role

### Acceptance Gate
- All EPIC-06 documents created/updated with lifecycle-compliant headers
- Specs_Index.md updated for new/moved documents
- openapi.yaml updated for S2-21 (GET /market/status)
- All documents pass lifecycle compliance check

### Risks

**RISK-08 — settings_model.md scope uncertainty**
Relates to: EPIC-06
S2-22 notes that BLG-SPEC-G1 says "resolution of BLG-SPEC-D2 (PUT vs PATCH) should be decided first." BLG-SPEC-D2 was resolved in v1.8 (ST-09: PATCH /settings/{id} canonical). The resolved API shape is now known. This dependency is therefore clear; no blocker.
Priority: Low — no issue.

**RISK-09 — ADR-002 missing or moved**
Relates to: EPIC-06
S2-29 assumes ADR-002 exists in `docs/decisions/`. If the file does not exist or has already been moved, the fix is trivially different (create or verify location). Mitigation: Head of Specs Team checks at sprint start.
Priority: Low.

---

## Risk Register Summary

| Risk ID | EPIC | Description | Priority | Mitigation |
|---------|------|-------------|----------|------------|
| RISK-01 | EPIC-01 | Metrics Definitions owner capacity (LL-05) | Medium | FinOps confirms at Stage 4.5 |
| RISK-02 | EPIC-01 | Trade reflection data model change needed | Low | Data Model owner reviews at pre-alignment |
| RISK-03 | EPIC-02 | Metrics definition batching dependency | Low | Batch into single metrics_definitions.md sprint |
| RISK-04 | EPIC-03 | Composite endpoint scope creep | Low | Aggregation only constraint enforced |
| RISK-05 | EPIC-04 | Entity store fallback requires Base44 config | Medium | Confirm approach at pre-alignment |
| RISK-06 | EPIC-04 | S2-12 spec alignment may widen scope | High | Decision required before sprint planning seal |
| RISK-07 | EPIC-05 | Seeded test infrastructure implementation approach | Medium | Agree approach at pre-alignment |
| RISK-08 | EPIC-06 | settings_model.md scope (BLG-SPEC-D2 resolved) | Low | No blocker; BLG-SPEC-D2 closed in v1.8 |
| RISK-09 | EPIC-06 | ADR-002 existence/location | Low | Check at sprint start |

---

## Dependency Map

```
BLG-FEAT-08 metrics defs (EPIC-01/S2-02)
  ├── S2-01 Structured Trade Reflection (EPIC-01)
  ├── S2-18 R-Multiple Distribution (EPIC-02)
  └── S2-03 Cohort defs (EPIC-02) [parallel to above]

S2-12 Drawdown spec alignment (EPIC-04)
  └── EPIC-04 verification completeness

S2-14 + S2-15 Backend FX conversion (EPIC-04)
  └── EPIC-04 frontend currency display fixes

EPIC-05 Phase 1 (seeded infra)
  └── EPIC-05 Phase 2 (new feature scenarios)
  └── EPIC-04 defect verification (17 Risk Dashboard scenarios)

EPIC-06 Documentation (no code dependencies)
```

---

## Verification Approach

| EPIC | Verification method |
|------|-------------------|
| EPIC-01 | Functional: trade close flow triggers reflection form; compliance metrics correct per definitions |
| EPIC-02 | Functional: cohort panel renders; R-multiple values match backend formula |
| EPIC-03 | Functional: dashboard home loads; all 5 data categories present |
| EPIC-04 | Functional: all 11 deviation items verified against risk_dashboard_scenarios.md; golden output regression passes |
| EPIC-05 | QA: all 17 NOT EXECUTED scenarios executed; CI coverage gate enforced |
| EPIC-06 | Lifecycle compliance audit: all documents have compliant headers; Specs_Index.md updated; openapi.yaml updated |

---

## Out-of-Scope Confirmation (Challenger-reviewed)

The following were considered and explicitly excluded:
- No new strategy parameters (§13 boundary unchanged)
- No automated trading execution
- No AI/ML features
- No broker API integration
- No v2.0 items pulled forward
- BLG-FEAT-03 (Slippage Tracking): no confirmed v1.9 roadmap home — excluded pending next rebalance
