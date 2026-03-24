# Specs Index (Canonical)

**Owner:** Head of Specs Team
**Purpose:** Single map of canonical product truth
**Audience:** Product, Engineering, Analytics, Strategy
**Status:** Authoritative
**Last Updated:** 2026-03-24

---

## 1. Purpose of This Index

This document defines **where authoritative truth lives** across the system.

It answers:
- Which spec owns which decisions
- How specs relate to one another
- Which document prevails in case of conflict

If two specs disagree, **this index determines the escalation path**.

---

## 2. How to Use This Index

When asking:
- "Where is X defined?"
- "Which rules apply?"
- "Who owns this decision?"
- "Can I change this safely?"

Start here.

This index does **not** restate rules.
It points to the **single canonical source**.

---

## 3. Canonical Spec Domains

### 3.1 Strategy

**What it owns**
- Trading intent
- Risk philosophy
- Position lifecycle rules
- Strategy parameter governance

**Canonical Documents**
- `strategy_rules.md`

**Owner**
- Strategy Rules & System Intent Owner

---

### 3.2 Data Model

**What it owns**
- Meaning of fields (price, stop, P&L, value)
- Currency semantics
- Lifecycle and state representations

**Canonical Documents**
- `data_model.md`
- `data_model/settings_model.md` — Class 1 Canonical, v0.1, Active (created 2026-03-08, ST-17): all settings field names, types, validation rules, defaults, and semantics.

**Owner**
- Data Model & Domain Schema Owner

---

### 3.3 Metrics & Analytics

**What it owns**
- Definitions of performance metrics
- Canonical formulas and tolerances
- Data sufficiency and failure behavior

**Canonical Documents**
- `metrics_definitions.md`

**Owner**
- Metrics Definitions & Analytics Canonical Owner

---

### 3.4 API Contracts

**What it owns**
- Request/response schemas
- Field guarantees and defaults
- Idempotency and error semantics
- Backward compatibility rules

**Canonical Location**
- `docs/specs/api_contracts/`

**Canonical Documents**
- `README.md`
- `conventions.md` — includes §13 Error Response Standard (canonical error envelope, HTTP status mapping)
- `*_endpoints.md`
- `market_endpoints.md` — Class 1 Canonical, v0.1, Active (created 2026-03-08, ST-16): GET /market/status
- `reports_endpoints.md` — Class 1 Canonical, v0.1, Active (created 2026-03-17, ST-03): GET /reports/tax-year — UK tax-year P&L statement. Dual sign-off: Head of Specs Team + Financial Reporting & Records Owner (2026-03-17).
- `alerts_endpoints.md` — Class 1 Canonical, v0.3, Active (created 2026-03-20, ST-02; updated v0.3 2026-03-24, ST-05): Alert rules CRUD, alert evaluation, notification feed, notification preferences, alert history (GET /alerts/history). Architecture: FastAPI BackgroundTasks per ADR-003. Sign-off: Head of Specs Team (2026-03-20).
- `health_endpoints.md` — Class 1 Canonical, v1.0, Active (created 2026-03-18; spec update to v1.1 deferred to v2.3, BLG-SPEC-D14 — DEV-HEALTH-001 deviation accepted 2026-03-24): GET /health operational health check endpoint. Note: implementation schema differs from v1.0 spec; v1.1 update pending.
- `api_changelog.md` — *Running changelog; must be updated with every contract version increment*

**Supporting Reference**
- `docs/reference/openapi.yaml` — *Supporting reference only; must not diverge from canonical contracts*

**Owner**
- API Contracts & Documentation Owner

**Enforcement**
- Any pull request that changes canonical API contracts or backend API behavior **must** be reviewed inline against:
  - Canonical Markdown contracts **and**
  - `docs/reference/openapi.yaml`
- Approval is blocked if OpenAPI alignment is skipped for contract-affecting changes.

---

### 3.5 Frontend & UX Semantics

**What it owns**
- User-visible meanings and mental models
- Page-level user goals, states, and flows
- Reusable UI component behavior
- Cross-cutting UX patterns
- Visual and interaction consistency

**Canonical Location**
- `specs/frontend/`

**Canonical Documents**
- `frontend/README.md`
- `frontend/design_system.md`
- Page, component, and pattern specifications

**Owner**
- Frontend Specifications & UX Documentation Owner

---

### 3.5b Observability & Logging

**What it owns**
- Structured log format standards
- Log levels and usage policy
- Correlation ID generation and propagation scheme
- Async failure observability approach

**Canonical Documents**
- `docs/specs/structured_logging_standards.md` — Class 1 Canonical Specification, v0.1.0, Active (created 2026-03-02, EPIC-04)

**Owner**
- Head of Engineering

---

### 3.6 Glossary (System-Level Reference)

**What it owns**
- Shared terminology used across specs
- Cross-domain language consistency
- Canonical meanings of commonly referenced terms

**Reference Document**
- `docs/reference/glossary.md` — Class 2 Supporting, v1.1, Active (updated 2026-03-08, ST-14): lifecycle-compliant header; terms added: portfolio heat, stop distance, cohort, journal completion rate, stop-based exit rate

**Authority**
- Language only — canonical definitions, formulas, and rules live in domain specs

**Owner**
- Head of Specs Team

**Notes**
- The glossary must not introduce new behavior or override domain specifications
- In case of conflict, the relevant domain canonical spec prevails

---

## 4. Conflict Resolution Order

In case of conflict, precedence is resolved in the following order:

1. **Specs Index**
2. Domain Canonical Spec
3. Supporting Specs
4. Reference Artifacts (e.g. OpenAPI, Glossary)
5. Code
6. UI behavior
7. Tribal knowledge

No downstream system may override upstream intent.

---

## 5. Change Governance & Enforcement

- Changes to **domain canonical specs** require domain owner approval
- Changes affecting multiple domains require Head of Specs Team review
- **Supporting reference artifacts must be reviewed inline with their canonical specs**
- Silent divergence between specs and behavior is treated as a **system bug**
- All documentation must comply with the lifecycle rules defined in:
  - `claude/charter/document_lifecycle_guide.md`

---

## 6. Pending Spec Work — Named Owner Assignments

This section tracks canonical spec gaps that have been identified but not yet filled. Items here block the features or releases noted. No feature may enter pre-alignment until its upstream spec gap is closed.

---

### 6.1 Settings Canonical Specification *(v1.6.1 pre-work gate)*

**Status:** RESOLVED — 2026-03-09 (v1.9 Sprint 1, ST-17). See §3.2 for registration.
**Backlog item:** BLG-SPEC-G1 — COMPLETE
**Resolved by:** `docs/specs/data_model/settings_model.md` Class 1 Canonical v0.1, Active — created 2026-03-08. All settings field names, types, validation rules, defaults, and semantics. Registered in §3.2 above. Cross-referenced from `settings_endpoints.md`.

~~Gap description: Settings behaviour was defined only within `settings_endpoints.md`. No standalone canonical document owned the settings model independently of the API layer.~~

---

### 6.2 Error Response Standard *(v1.6.1 pre-work gate)*

**Status:** RESOLVED — 2026-03-09 (v1.9 Sprint 1, ST-18). See §3.4 for registration.
**Backlog item:** BLG-SPEC-G2 — COMPLETE
**Resolved by:** `docs/specs/api_contracts/conventions.md` §13 Error Response Standard added — canonical error envelope shape, all error codes, HTTP status mapping, rule distinguishing HTTP 400 (malformed input) from HTTP 200 with `valid: false` (business rule failure). Registered in §3.4 above.

~~Gap description: Error response shapes were partially covered but not canonically defined for all failure modes.~~

---

### 6.3 GET /portfolio/prospective-heat endpoint — spec and implementation gap

**Status:** RESOLVED — 2026-03-17 (v2.0 Sprint, ST-13, cycle 2026-03-17__release-v2.0)
**Deviation:** DEV-ST05-01 (P3) — v1.10 sprint execution
**Backlog item:** BLG-BE-02 (P3) — COMPLETE
**Owner:** Head of Engineering + Head of Specs Team
**Resolution:** ST-13 (v2.0 EPIC-04) spec authored in `portfolio_endpoints.md v2.0.0 §GET /portfolio/prospective-heat`; endpoint implemented in backend; `@unittest.skip` removed from `TestProspectiveHeat`; all integration tests pass. Commit 279e832.

~~`GET /portfolio/prospective-heat` endpoint is not defined in `docs/specs/api_contracts/portfolio_endpoints.md` and has no backend implementation. Referenced by the ProspectiveHeatPanel frontend component. Integration tests written in `tests/test_portfolio_integration.py` are currently skipped (`@unittest.skip`) pending spec authoring.~~

---

## 7. Open Compliance Issues

This section records known lifecycle or governance compliance gaps that have been identified and are pending resolution. Items here do not block current work but must be resolved by the owner before the document is next updated.

---

### 7.1 `docs/operations/validation_system.md` — Owner field non-compliant

**Identified:** 2026-02-21
**Status:** RESOLVED — 2026-03-09 (v1.9 Sprint 1, ST-19)
**Backlog item:** BLG-SPEC-G5 — COMPLETE
**Resolution:** `Owner: Platform Team` updated to a named governance role per `claude/charter/document_lifecycle_guide.md §7`. Resolved by Infrastructure & Operations Documentation Owner in ST-19.

---

### 7.2 `GET /portfolio` — 4 required fields missing from API response vs `portfolio_endpoints.md`

**Identified:** 2026-03-16 (GAP-03 staging execution — v1.10 sprint QA)
**Status:** RESOLVED — 2026-03-17 (v2.0 Sprint, ST-12)
**Backlog item:** BLG-BE-01 (P1) — COMPLETE
**Owner:** Head of Engineering
**Resolution:** ST-12 (v2.0) added `initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value` to `GET /portfolio` response. GAP-03 scenario passes. Commit 04ed5e8.

---

## 8. Coverage Inventory

The Coverage Inventory is the authoritative cross-domain record of spec-to-implementation coverage, lifecycle compliance status, and open documentation gaps. It is refreshed every 3 cycles (at `run audit`) and at the start of each major release.

- `docs/specs/spec_coverage_inventory.md` — Class 3 Operational Record, v1.0, Filed 2026-03-17 (ST-17, EPIC-05). 38 documents audited; 7 actions identified.

---

## 9. Test Coverage Gaps — v2.1 (2026-03-18__release-v2.1)

Identified during delivery verification (verification_report.md §6 — TSG-v21-01 through TSG-v21-03). All three gaps have backlog items and are tracked for resolution before the next sprint touching the relevant domain.

### 9.1 TSG-v21-01 — EPIC-02: notifications_scenarios.md not formally executed

**Identified:** 2026-03-21 (delivery verification 2026-03-18__release-v2.1)
**Status:** RESOLVED — 2026-03-24 (v2.2, ST-09, cycle 2026-03-21__release-v2.2)
**Owner:** QA & Testing Owner
**Gap:** `docs/testing/notifications_scenarios.md` (SC-NOTIF-01 through SC-NOTIF-08) exists but was not formally executed and referenced in `qa_evidence_EPIC-02.md`. Remaining 3 alert types require test data with open positions.
**Resolution:** SC-NOTIF-01 through SC-NOTIF-08 executed on staging; 9 Playwright tests pass; results recorded in `qa_evidence_EPIC-04.md` (ST-09). Backlog item TEST-GAP-EPIC-02 closed.

### 9.2 TSG-v21-02 — EPIC-03: no watchlist test scenario file exists

**Identified:** 2026-03-21 (delivery verification 2026-03-18__release-v2.1)
**Status:** RESOLVED — 2026-03-24 (v2.2, ST-10, cycle 2026-03-21__release-v2.2)
**Owner:** QA & Testing Owner
**Gap:** No test scenario file exists for the watchlist feature (EPIC-03, ST-08/09/10). Spec refs: `docs/specs/api_contracts/watchlist_endpoints.md`, `docs/specs/frontend/pages/watchlist.md`.
**Resolution:** `docs/testing/watchlist_scenarios.md` created covering SC-WATCH-01 through SC-WATCH-06 (including deferred ST-10 AC-6 sort order). Backlog item TEST-GAP-EPIC-03 closed.

### 9.3 TSG-v21-03 — EPIC-05: no slippage tracking test scenarios exist

**Identified:** 2026-03-21 (delivery verification 2026-03-18__release-v2.1)
**Status:** Open — backlog item TEST-GAP-EPIC-05-SLIP
**Owner:** QA & Testing Owner
**Gap:** No scenario file covers slippage tracking (ST-14). Spec ref: `docs/specs/frontend/pages/trade_history.md`.
**Required action:** Author SC-SLIP-01 through SC-SLIP-04 in `docs/testing/reports_scenarios.md` or a new `slippage_scenarios.md`.
**Resolution target:** v2.3 (slippage scenarios not included in v2.2 sprint; TEST-GAP-EPIC-05-SLIP remains open).

---

## 10. Test Coverage Gaps — v2.2 (2026-03-21__release-v2.2)

Identified during delivery verification (verification_report.md §6 — TSG-v22-01 through TSG-v22-03). Gaps are tracked for resolution per stated disposition.

### 10.1 TSG-v22-01 — EPIC-01: no scenario for API key authentication

**Identified:** 2026-03-24 (delivery verification 2026-03-21__release-v2.2)
**Status:** Open — backlog item BLG-QA-01 Phase 4
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Gap:** No automated test scenario covers X-API-Key authentication (401 path, frontend header injection, exempt endpoints). Core security control; zero scenario coverage. Manual acceptance only at ship.
**Required action:** Add API auth integration tests (401 path, valid key, exempt endpoints) to CI as part of BLG-QA-01 Phase 4.
**Resolution target:** BLG-QA-01 Phase 4 (Playwright E2E automation cycle)

### 10.2 TSG-v22-02 — EPIC-03: no scenario for GET /health operational health response schema

**Identified:** 2026-03-24 (delivery verification 2026-03-21__release-v2.2)
**Status:** Open — deferred to v2.3 Sprint 1 alongside BLG-SPEC-D14 spec update
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Gap:** New endpoint; response schema not validated by any automated test (status, db, last_* fields). Manual code review only at ship.
**Required action:** Add SC-HEALTH-01 scenario validating operational health response fields in v2.3 Sprint 1.
**Resolution target:** v2.3 Sprint 1 (aligned with BLG-SPEC-D14 spec update)

---

## 11. Guiding Principle

> Specs explain decisions.
> This index ensures those decisions form a coherent system.