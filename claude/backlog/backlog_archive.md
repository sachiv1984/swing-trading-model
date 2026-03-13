**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-13 (GROOM-20260313-01: 27 v1.9 items archived)

# Backlog Archive — Momentum Trading Assistant

Permanent record of completed and killed backlog items retired from `claude/backlog/backlog.md`. Listed in retirement order, most recent first. Append-only — do not edit existing entries.

---

### BLG-FEAT-08 — Basic Compliance Metrics

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 2
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-01 | ST-02 | verification_report_sprint2.md

### BLG-FEAT-08 — Basic Compliance Metrics ✅ COMPLETE
**Priority:** P2
**Effort:** ~1 day
**Target release:** v1.9 (pre-work gate for Structured Trade Reflection Template)
**Status:** ✅ COMPLETE — 2026-03-13 (v1.9 Sprint 2, EPIC-01, ST-02)

Lightweight discipline metrics:
- Journal completion rate
- Stop-based exit rate
- Average position size (% of portfolio)

Definitions must be canonicalised in `metrics_definitions.md` first.

---

### BLG-NEW-09 — R-Multiple Distribution Report

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 2
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-02 | ST-05 | verification_report_sprint2.md

### BLG-NEW-09 — R-Multiple Distribution Report ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Analytics / User Value
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-analytics-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Sequence constraint:** After BLG-FEAT-08 metrics definitions (Metrics Definitions owner capacity — LL-05 check applies)
**Status:** ✅ COMPLETE — 2026-03-13 (v1.9 Sprint 2, EPIC-02, ST-05)

**Problem**
No visualisation of R-multiple distribution exists. R-multiple (profit in units of initial risk) is the canonical trade quality measure in this strategy — users cannot see whether trades are systematically achieving R > 1 on winners or not.

**Scope**
- Add R-multiple distribution chart/panel to the Performance Analytics page (extends existing §3.1 delivery)
- Backend: compute R-multiple per closed trade from existing trade data
- Metrics Definitions owner must define R-multiple formula in metrics_definitions.md before implementation

**Acceptance Criteria**
- R-multiple formula defined and canonicalised in metrics_definitions.md
- Distribution visualisation present on analytics page showing frequency of R-multiple values across closed trades
- Values computed from canonical backend formula; no client-side derivation

---

### BLG-NEW-10 — Canonical Test Scenario Library

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1 (Phase 1) + Sprint 2 (Phase 2)
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-05 | ST-11 (Phase 1), ST-12 (Phase 2)

### BLG-NEW-10 — Canonical Test Scenario Library ✅ COMPLETE
**Priority:** P1 (High)
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Scope constraint:** Risk Dashboard components first (resolves TEST-GAP-EPIC-01 infrastructure dependency); new v1.9 feature scenarios added at release time; no retroactive full-coverage mandate
**Status:** Phase 1 ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-05, ST-11). Phase 2 ✅ COMPLETE — 2026-03-13 (v1.9 Sprint 2, EPIC-05, ST-12). Full item complete.

**Problem**
Test scenarios are ad-hoc per feature. TEST-GAP-EPIC-01 identified that 17/27 Risk Dashboard scenarios cannot be executed without a seeded test infrastructure. A systematic canonical library with documented infrastructure preconditions prevents this gap recurring in every release.

**Scope**
- Phase 1: Create seeded test infrastructure and resolve TEST-GAP-EPIC-01 (17 unexecuted Risk Dashboard scenarios)
- Phase 2: Add test scenarios for each new feature delivered in v1.9 at time of delivery
- Document infrastructure preconditions per scenario group

**Acceptance Criteria**
- TEST-GAP-EPIC-01: all 17 unexecuted Risk Dashboard scenarios run against seeded environment and results recorded
- Infrastructure preconditions documented in risk_dashboard_scenarios.md
- v1.9 feature scenarios added to scenario library as each feature is delivered
- No retroactive full-coverage mandate

---

### TEST-GAP-EPIC-01 — Risk Dashboard scenario execution infrastructure gap

**Status at retirement:** ✅ Complete — closed
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-05 | ST-11

### TEST-GAP-EPIC-01 — Risk Dashboard scenario execution infrastructure gap ✅ COMPLETE
**Priority:** P2
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-04__release-v1.8 — Director of Quality recommendation
**Cycle added:** 2026-03-04__release-v1.8
**Target release:** v1.9
**Status:** CLOSED — resolved in v1.9 ST-11 (2026-03-09)

17 of 27 Risk Dashboard acceptance scenarios (SC-RD-02–06, SC-RD-07–12, SC-RD-15, SC-RD-16–18, SC-RD-24–25) cannot be executed in the v1.8 environment due to the absence of a test data injection mechanism.

**Resolution:** Playwright mock layer delivered. All 17 scenarios automated in `tests/e2e/risk-dashboard.spec.js`. CI gate at `.github/workflows/playwright.yml`. Mock data in `tests/e2e/mocks/portfolio-mock-data.js`. Scenario document updated to v1.1.

---

### BLG-NEW-11 — Canonical Terms Glossary

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-14

### BLG-NEW-11 — Canonical Terms Glossary ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Governance / Spec Quality
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Class constraint:** Document must be Class 2 (Supporting) — cross-reference index only; no new canonical rules
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-14)

**Problem**
Terms like "portfolio heat", "grace period", "stop distance", "R-multiple" are used across multiple specs without a single cross-reference point. Term drift causes ambiguity (e.g., BLG-RD-08 — drawdown data source ambiguity).

**Scope**
- Create a canonical terms glossary as a Class 2 Supporting document
- Each term: definition + link to Class 1 canonical source (metrics_definitions.md, strategy_rules.md, etc.)
- No new canonical definitions — only cross-references
- Register in Specs_Index.md

**Acceptance Criteria**
- Glossary exists as Class 2 Supporting document with compliant header
- All key trading and system terms defined with canonical source links
- Registered in Specs_Index.md
- No duplicate or conflicting definitions introduced

---

### BLG-NEW-12 — Service Layer Test Coverage Standard

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-05 | ST-13

### BLG-NEW-12 — Service Layer Test Coverage Standard ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Engineering Quality / CI
**Owner:** Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Prerequisite:** BLG-NEW-01 (golden output baseline) — COMPLETE
**CI constraint:** Standard must include a minimum coverage threshold enforceable via CI (pytest-cov or equivalent)
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-05, ST-13)

**Problem**
The golden output baseline (BLG-NEW-01, COMPLETE) covers end-to-end calculation correctness. The service layer (portfolio_service.py, trade_service.py, analytics_service.py) has no documented test coverage standard. Logic errors at the service layer may not be caught by golden tests if they produce correct outputs on golden inputs.

**Scope**
- Author a Service Layer Test Coverage Standard
- Define minimum unit test coverage threshold for services/ directory
- Add CI step that enforces coverage threshold on every PR

**Acceptance Criteria**
- Coverage standard documented with named threshold (agreed at pre-alignment)
- CI step adds pytest-cov (or equivalent) coverage check on services/ directory
- Build fails if coverage falls below threshold
- Standard integrated with or referenced from backend_engineering_patterns.md

---

### BLG-NEW-04 — AI-Assisted Workflow Governance Policy

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-15

### BLG-NEW-04 — AI-Assisted Workflow Governance Policy ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Governance
**Owner:** Product Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-15)

**Problem**
The project uses AI-assisted workflows (Claude Code) for governed routines. There is no documented policy governing: which decisions may be taken by AI, which require human override, and how AI output is reviewed before it becomes a canonical record.

**Scope**
- Author an AI-Assisted Workflow Governance Policy document
- Define: AI authority scope, human-in-the-loop requirements, escalation triggers, record-keeping obligations

**Acceptance Criteria**
- Policy document authored and filed under appropriate governance path
- Policy covers: scope of AI authority, mandatory human review checkpoints, record-keeping requirements

---

### BLG-SPEC-G5 — validation_system.md owner field non-compliant

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-19

### BLG-SPEC-G5 — validation_system.md owner field non-compliant ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Gap
**Owner:** Infrastructure & Operations Owner
**Raised:** Specs_Index §7.1, 2026-02-21 (carried forward to 2026-03-03 review)
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-19)

`docs/specs/validation_system.md` owner field updated from "Platform Team" to named governance role per document_lifecycle_guide.md. Specs_Index.md §7.1 marked RESOLVED.

---

### BLG-SPEC-G4 — ADR-002 in wrong location

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-19

### BLG-SPEC-G4 — ADR-002 in wrong location ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Governance Organisation Gap
**Owner:** Head of Specs Team
**Raised:** 2026-03-03 — Head of Specs Team review
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-19)

ADR-002 moved to `docs/product/decisions/`. Cross-references updated.

---

### BLG-SPEC-G3 — structured_logging_standards.md not registered in Specs_Index.md

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-19

### BLG-SPEC-G3 — structured_logging_standards.md not registered in Specs_Index.md ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Index Gap
**Owner:** Head of Specs Team
**Raised:** 2026-03-03 — Head of Specs Team review
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-19)

`docs/specs/structured_logging_standards.md` registered in Specs_Index.md §3.5b with Owner, Class, Status, Version.

---

### BLG-SPEC-G2 — Error Response Standard not defined

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-18

### BLG-SPEC-G2 — Error Response Standard not defined ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** API Contracts & Documentation Owner
**Raised:** Specs_Index §6.2, 2026-02-21 (carried forward to 2026-03-03 review)
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-18)

Error Response Standard added as §13 of `docs/specs/api_contracts/conventions.md`. Canonical error envelope shape, all error codes, HTTP status mapping. Registered in Specs_Index.md §3.4.

---

### BLG-SPEC-G1 — settings_model.md missing

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-17

### BLG-SPEC-G1 — settings_model.md missing ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** Head of Specs Team
**Raised:** Specs_Index §6.1, 2026-02-21 (carried forward to 2026-03-03 review)
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-17)

`docs/specs/data_model/settings_model.md` created. All settings field names, types, validation rules, defaults, and semantics. Registered in Specs_Index.md §3.2. Cross-referenced from settings_endpoints.md.

---

### BLG-SPEC-D9 — process_index.md and Specs_Index.md reference wrong path for document_lifecycle_guide.md

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-19

### BLG-SPEC-D9 — process_index.md and Specs_Index.md reference wrong path ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Drift / Broken Cross-Reference
**Owner:** Head of Specs Team
**Raised:** 2026-03-03 — Head of Specs Team review
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-19)

Both documents updated to reference `claude/charter/document_lifecycle_guide.md` (correct path).

---

### BLG-SPEC-D8 — docs/System_status_report.md missing governance lifecycle header

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-19

### BLG-SPEC-D8 — docs/System_status_report.md missing governance lifecycle header ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Drift
**Owner:** Director of Quality
**Raised:** 2026-03-03 — Head of Specs Team review
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-19)

Lifecycle header added to docs/System_status_report.md: Owner, Class, Status, Version, Last Updated fields.

---

### BLG-SPEC-D4 — GET /positions/search/tags undocumented

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-19

### BLG-SPEC-D4 — GET /positions/search/tags undocumented ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Gap
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-19)

`GET /positions/search/tags` documented in position_endpoints.md.

---

### BLG-SPEC-D3 — GET /market/status completely undocumented live endpoint

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-16

### BLG-SPEC-D3 — GET /market/status completely undocumented live endpoint ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Documentation Gap / Drift
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-16)

`docs/specs/api_contracts/market_endpoints.md` created (Class 1 Canonical v0.1). GET /market/status documented. Registered in Specs_Index.md §3.4. Added to openapi.yaml.

---

### BLG-SPEC-D1 — API Contracts README.md version frozen at v1.8.4

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06 | ST-19

### BLG-SPEC-D1 — API Contracts README.md version frozen at v1.8.4 ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-06, ST-19)

README.md version header updated to v1.9.0. Changelog includes v1.9.0 entry.

---

### BLG-RD-11 — current_stop in USD for US positions causes incorrect Stop Distance %

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04 | ST-07

### BLG-RD-11 — current_stop in USD for US positions (DEV-ST03-12) ✅ COMPLETE
**Priority:** P2
**Type:** Backend + Frontend Defect — Currency Conversion
**Owner:** Head of Engineering
**Source:** DEV-ST03-12 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-04, ST-07)

`portfolio_service.py` converts `current_stop` to GBP for US positions. Stop Distance % calculation uses matching currencies.

---

### BLG-RD-10 — US entry prices in USD not GBP

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04 | ST-07

### BLG-RD-10 — US entry prices in USD not GBP (DEV-ST03-11) ✅ COMPLETE
**Priority:** P2
**Type:** Backend + Frontend Defect — Currency Conversion
**Owner:** Head of Engineering
**Source:** DEV-ST03-11 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-04, ST-07)

`portfolio_service.py` converts `entry_price` to GBP for US positions. Frontend Risk Dashboard displays entry prices in GBP for all positions.

---

### BLG-RD-09 — ProspectiveHeatPanel missing threshold label

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04 | ST-09

### BLG-RD-09 — ProspectiveHeatPanel missing threshold label (DEV-ST03-09) ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Display Element
**Owner:** Head of Engineering
**Source:** DEV-ST03-09 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-04, ST-09)

Threshold label badge added to ProspectiveHeatPanel result row per spec §7.5.

---

### BLG-RD-08 — Drawdown data source needs Head of Specs Team verification

**Status at retirement:** ✅ Resolved
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1 (pre-sprint resolution 2026-03-06)
**Evidence:** Head of Specs Team decision 2026-03-06; risk_dashboard.md §4.1 v0.1.7

### BLG-RD-08 — Drawdown data source needs Head of Specs Team verification (DEV-ST03-08) ✅ RESOLVED
**Priority:** P2
**Type:** Spec Alignment — Requires Owner Decision
**Owner:** Head of Specs Team
**Source:** DEV-ST03-08 — Delivery verification 2026-03-04__release-v1.8
**Status:** RESOLVED — 2026-03-06

Split-source data model confirmed: `current_drawdown_percent` from `drawdown_service.py` via `GET /portfolio`; `days_underwater` from `analytics_service.py` via `GET /analytics/metrics`. `risk_dashboard.md §4.1` updated to v0.1.7. Head of Specs Team decision 2026-03-06.

---

### BLG-RD-07 — Days in Grace column absent from GracePeriodPanel

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04 | ST-09

### BLG-RD-07 — Days in Grace column absent from GracePeriodPanel (DEV-ST03-07) ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Column
**Owner:** Head of Engineering
**Source:** DEV-ST03-07 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-04, ST-09)

`holding_days` column added to Grace Period table per spec §5.2.

---

### BLG-RD-06 — GBP value at risk absent from HeatGauge

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04 | ST-10

### BLG-RD-06 — GBP value at risk absent from HeatGauge (DEV-ST03-06) ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Metric
**Owner:** Head of Engineering
**Source:** DEV-ST03-06 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-04, ST-10)

GBP value at risk SVG text added below gauge percentage per spec §3.2.

---

### BLG-RD-05 — GRACE badge colour amber instead of blue

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04 | ST-10

### BLG-RD-05 — GRACE badge colour amber instead of blue (DEV-ST03-05) ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Cosmetic
**Owner:** Head of Engineering
**Source:** DEV-ST03-05 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-04, ST-10)

GRACE badge colour corrected to blue per spec §6.3.

---

### BLG-RD-04 — Stop Price column absent from PositionRiskTable

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04 | ST-09

### BLG-RD-04 — Stop Price column absent from PositionRiskTable (DEV-ST03-04) ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Missing Column
**Owner:** Head of Engineering
**Source:** DEV-ST03-04 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-04, ST-09)

Stop Price column (current_stop, GBP, 2dp) added to PositionRiskTable per spec §6.2.

---

### BLG-RD-03 — PositionRiskTable sorted descending

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04 | ST-09

### BLG-RD-03 — PositionRiskTable sorted descending (DEV-ST03-03) ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Sort Direction
**Owner:** Head of Engineering
**Source:** DEV-ST03-03 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-04, ST-09)

Sort corrected to ascending (tightest stop distance first) per spec §6.4.

---

### BLG-RD-02 — GracePeriodPanel empty vs error state indistinguishable

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04 | ST-08

### BLG-RD-02 — GracePeriodPanel empty vs error state indistinguishable (DEV-ST03-02) ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Error State UX
**Owner:** Head of Engineering
**Source:** DEV-ST03-02 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-04, ST-08)

GracePeriodPanel now renders a visible error card on API failure, distinct from the empty state.

---

### BLG-RD-01 — Entity store fallback masks API error states

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-13
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04 | ST-08

### BLG-RD-01 — Entity store fallback masks API error states (DEV-ST03-01) ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Error State Coverage
**Owner:** Head of Engineering
**Source:** DEV-ST03-01 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** ✅ COMPLETE — 2026-03-09 (v1.9 Sprint 1, EPIC-04, ST-08)

Each Risk Dashboard component now renders its own error state independently. Entity store fallback does not silently mask failures.

---

### BLG-NEW-08 — Automated OpenAPI Drift Detection in CI

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-08

### BLG-NEW-08 — Automated OpenAPI Drift Detection in CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** CI / Governance
**Owner:** Engineering (CI)
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-08

**Problem**
`docs/reference/openapi.yaml` was not updated during EPIC-06 when three contracts were bumped to v1.9.0 (BLG-SPEC-D7). There is no CI check that detects drift between the markdown API contracts and openapi.yaml. Drift will recur without an automated gate.

**Scope**
- Add a CI step that detects drift between `openapi.yaml` and the markdown API contracts
- Approach: either (a) generate openapi.yaml from contracts and compare, or (b) run a custom lint/diff check against known contract fields
- Block merge on detected drift

**Acceptance Criteria**
- CI step detects drift between openapi.yaml and markdown contracts
- Merge blocked if drift is detected
- Approach documented (generation vs diff) — approach decision to be made in pre-alignment

---

### BLG-NEW-07 — Running API Changelog Document

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-12

### BLG-NEW-07 — Running API Changelog Document ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Documentation / Governance
**Owner:** API Contracts & Documentation Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-12

**Problem**
There is no single running changelog document for API contract changes. Changes to endpoint contracts (new fields, removed fields, version bumps) are recorded in individual spec files but there is no centralised, human-readable history of API evolution across versions.

**Scope**
- Create a running API Changelog document that summarises contract changes per version
- Cover all contracts under `docs/specs/api_contracts/`
- Backfill from v1.8.x → v1.9.0 changes (EPIC-06 scope)
- Document maintainer obligation: must be updated alongside every contract version bump

**Acceptance Criteria**
- API Changelog document exists and is registered in Specs_Index.md
- All v1.9.0 contract changes (EPIC-06) are backfilled
- Maintenance obligation documented alongside contract spec authoring workflow

---

### BLG-NEW-05 — Dependency Vulnerability Scanning in CI

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-07

### BLG-NEW-05 — Dependency Vulnerability Scanning in CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Security / CI
**Owner:** Engineering (CI)
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-07

**Problem**
There is no automated scanning of Python dependencies for known vulnerabilities in the CI pipeline. A compromised or vulnerable dependency could be introduced silently.

**Scope**
- Add a CI step that scans Python dependencies (e.g., using `pip-audit` or `safety`) for known CVEs
- Block merge (or warn at configurable severity) on high/critical vulnerabilities
- Integrate with existing `.github/workflows/` structure

**Acceptance Criteria**
- Dependency vulnerability scan runs on every PR
- High/critical CVEs block merge (or produce a required review comment)
- Scan tool and severity threshold documented

---

### BLG-NEW-03 — Define and Document Unavailability Failure Mode

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-11

### BLG-NEW-03 — Define and Document Unavailability Failure Mode ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Policy / Governance
**Owner:** Infrastructure & Operations Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-11

**Problem**
There is no documented policy for what happens when the system is unavailable during a trading session (e.g., backend down, market data feed unavailable). The system has no documented failure modes or fallback procedures for the user.

**Scope**
- Define and document the unavailability failure mode: what the user should do, what the system state is, and any manual fallback procedures
- Document where this policy lives (e.g., OPERATIONAL_GUIDE.md or a new docs/ops/ document)

**Acceptance Criteria**
- Unavailability failure mode documented: system states covered, user action required, data integrity implications
- Document registered in appropriate governance index

---

### BLG-NEW-02 — Backtest vs Live Stop Reconciliation Report

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-06

### BLG-NEW-02 — Backtest vs Live Stop Reconciliation Report ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Quality / CI
**Owner:** Engineering + QA
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Dependency:** After BLG-NEW-01 (golden output baseline must be in place first)
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-06

**Problem**
There is no automated verification that the trailing stop formula used in backtests and the formula used in the live system produce identical results for the same inputs. Silent divergence between backtest and live logic is a category of defect that cannot be caught by either gate independently.

**Scope**
- Report or CI assertion that compares backtest stop calculations vs live system stop calculations for a set of known inputs
- Output: reconciliation result confirming parity or flagging divergence

**Acceptance Criteria**
- Automated check exists that verifies backtest and live stop logic produce identical results for all golden inputs
- Any divergence between backtest and live calculation fails the check

---

### BLG-NEW-01 — Golden Output Regression Baseline for CI

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-05

### BLG-NEW-01 — Golden Output Regression Baseline for CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Quality / CI
**Owner:** Engineering + QA
**Source:** IDEA-director-of-quality-20260304-02 — Director of Quality, IW-20260304-01
**Cycle added:** 2026-03-04__item-3.4
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-05

**Problem**
The current CI gate (`POST /validate/calculations`, EPIC-01) checks only that `critical_failed > 0` blocks the merge. It does not verify that specific calculations return the correct numeric values. A change that silently alters the trailing stop formula from `CurrentPrice - (2 × ATR)` to `CurrentPrice - (2.1 × ATR)` would pass the current gate. Numeric regressions are the highest-risk defect class in a trading system.

**Scope**
- Define a set of deterministic golden test cases: known inputs (entry_price, ATR, risk_percent, etc.) with expected output values derived directly from the canonical strategy spec
- Store as `tests/golden_outputs.json` — treated as a canonical artefact; updated only via spec-linked PR
- Scope limited to stop/sizing calculations only (per STEP 5 scoping from IW-20260304-01)
- Add a CI step that calls the backend with each golden input and asserts output matches to required precision
- Any numeric divergence from golden values fails the build

**Acceptance Criteria**
- `tests/golden_outputs.json` exists with spec-derived golden values for stop and sizing calculations
- CI step added that runs golden output assertions on every PR
- Build fails on any numeric deviation from golden values
- Precision tolerance documented (e.g., 4 decimal places for share counts)
- Golden values derived from canonical spec, not from current implementation

**Dependencies**
- None (prerequisite: BLG-NEW-02 must follow, not precede)

---

### BLG-SPEC-D7 — openapi.yaml frozen at v1.8.1

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-10

### BLG-SPEC-D7 — openapi.yaml frozen at v1.8.1; not updated for v1.9.0 contracts ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Documentation Drift / Reference Artefact Staleness
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-10 — openapi.yaml updated to v1.9.0

**Problem**
`docs/reference/openapi.yaml` is at version 1.8.1 (1193 lines).
Three contracts were bumped to v1.9.0 in EPIC-06:
- `sharpe_ratio_trade_method` absent from /validate/calculations validated metrics list
- portfolio positions response schema not aligned to v1.9.0 field list
- `holding_days` absent from GET /trades trade object schema
Specs_Index.md §4 states: "openapi.yaml must be reviewed inline with every contract change; markdown contracts take precedence on conflict."
This was not done during EPIC-06.

**Acceptance Criteria**
- openapi.yaml version field updated to 1.9.0
- /validate/calculations response includes sharpe_ratio_trade_method (14 validated metrics total)
- GET /trades trade object includes holding_days (integer)
- GET /portfolio positions objects reflect v1.9.0 field list
- No conflicts between openapi.yaml and markdown contracts

---

### BLG-SPEC-D2 — settings_endpoints.md spec/implementation mismatch

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-09

### BLG-SPEC-D2 — settings_endpoints.md spec/implementation mismatch ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Spec–Implementation Drift
**Owner:** API Contracts & Documentation Owner + Head of Engineering
**Raised:** 2026-03-03 — Head of Specs Team review
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-09 — settings_endpoints.md v1.1.0 published; PATCH/POST documented as canonical

**Problem**
`docs/specs/api_contracts/settings_endpoints.md` specifies `PUT /settings` (replace all settings).
Live implementation in `backend/main.py` uses `PATCH /settings/{settings_id}` (update single setting by ID).
Additionally, `POST /settings` is implemented but not documented anywhere.
This is a P1 drift: clients relying on the spec will call the wrong method and path.

**Decision Required**
Product Owner + API Contracts owner to choose:
(a) Update spec to document `PATCH /settings/{settings_id}` and `POST /settings` as the canonical interface, or
(b) Align backend to implement `PUT /settings` as specced (breaking change to existing frontend).

**Acceptance Criteria**
- settings_endpoints.md accurately documents the live HTTP method, path, and request/response schema
- No divergence between spec and implementation
- Decision record filed if option (b) chosen (breaking change)

---

### §6 v1.7 Release Slice — 2026-03-02__release-v1.7

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** All 6 EPICs shipped 2026-03-03; verified 2026-03-03 — `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

<!-- release-plan-marker: RP:v1.7:2026-03-02__release-v1.7 -->

**Cycle:** 2026-03-02__release-v1.7
**Planning Date:** 2026-03-02
**Status:** ✅ Complete — all 6 EPICs shipped 2026-03-03; verified 2026-03-03
**Reference:** claude/cycles/2026-03-02__release-v1.7/stage4_backlog_slice.md

| S2 ID | Item | Epic | Priority | Effort |
|-------|------|------|----------|--------|
| S2-01 | BLG-TECH-04 — CI/CD GitHub Actions Validation Workflow | EPIC-01 | P2 | ~1 day |
| S2-02 | Strategy Rules §13 Boundary Review | EPIC-02 | P1 | ~0.5 day |
| S2-03 | Metrics Definitions — Portfolio Heat Formula & Thresholds | EPIC-03 | P1 | ~0.5 day |
| S2-04 | Structured Logging / Observability Standards | EPIC-04 | P2 | ~1 day |
| S2-05 | API Versioning Strategy Decision Record | EPIC-05 | P2 | ~0.5 day |
| S2-06 | BLG-TECH-06 — Canonicalise sharpe_ratio_trade_method | EPIC-06 | P2 | ~30 min–1 hr |
| S2-07 | BLG-TECH-08 — Align portfolio_endpoints.md positions summary | EPIC-06 | P3 | ~30 min + decision |
| S2-08 | BLG-TECH-09 — Add holding_days to GET /trades | EPIC-06 | P3 | ~30 min + decision |

**Total estimated effort:** ~3.5–4 days
**Capacity assessment:** PASS (workforce_capacity.md — no constraints violated)
**Key gates unlocked by this release:**
- EPIC-02 → §13-gated features may enter pre-alignment
- EPIC-03 → v1.8 Risk Dashboard pre-alignment
- EPIC-04 + EPIC-05 → v2.0 Alerts pre-alignment (2 of 3 gates)

---

### BLG-SPEC-D6 — changelog.md has no v1.7 entry

**Status at retirement:** ✅ Complete — Resolved
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** N/A — documentation fix
**Evidence:** v1.7 entry confirmed present in `docs/product/changelog.md` (verified 2026-03-04)

**BLG-SPEC-D6** — changelog.md has no v1.7 entry
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** Product Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/product/changelog.md` last entry is v1.6.1 (2026-03-01).
v1.7 Foundation & Governance sprint was fully delivered and verified (2026-03-03).
No entry exists for v1.7.

**Acceptance Criteria**
- v1.7 changelog entry added covering: CI/CD merge gate (EPIC-01), §13 boundary review (EPIC-02), Portfolio Heat metrics (EPIC-03), Structured Logging Standards (EPIC-04), API Versioning Decision Record (EPIC-05), Spec Debt Resolution — analytics/portfolio/trade endpoints v1.9.0 (EPIC-06)

---

### BLG-SPEC-D5 — current_roadmap.md v1.7 section not closed out

**Status at retirement:** ✅ Complete — Resolved
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** N/A — documentation fix
**Evidence:** Resolved by `manage roadmap` run 2026-03-04 — v1.7 section retired to `claude/roadmap/roadmap_archive.md`; release summary updated; footer already referenced correct backlog path

**BLG-SPEC-D5** — current_roadmap.md v1.7 section not closed out
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** Product Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`claude/roadmap/current_roadmap.md` v1.7 section items still show "Status: Planned".
Release Summary table has no ✅ for v1.7.
v1.7 was fully delivered (2026-03-02) and verified (2026-03-03).
Additionally, footer references `docs/product/feature_backlog.md` which does not exist (actual backlog: `claude/backlog/backlog.md`).

**Acceptance Criteria**
- v1.7 section marked Complete with delivery date
- Release Summary table updated (✅ v1.7)
- Footer corrected to reference correct backlog path

---

### BLG-NEW-06 — Realised vs Unrealised P&L Labelling

**Status at retirement:** ❌ Killed — merged into 4.1b pre-work scope
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** N/A — merged
**Evidence:** DL-005 (2026-03-04); merged into roadmap item 4.1b Tax-Year P&L Statement pre-work scope

**BLG-NEW-06** — Realised vs Unrealised P&L Labelling
**Status:** Merged into 4.1b pre-work scope — not a standalone backlog item
**Source:** IW-20260304-01
**Cycle added:** 2026-03-04__item-3.4

This item (clear distinction of realised vs unrealised P&L amounts in the tax-year P&L statement) has been merged into the 4.1b Tax-Year P&L Statement scope as pre-work. See current_roadmap.md §4.1b scope note (2026-03-04). No standalone delivery required.

---

### BLG-TECH-09 — Add holding_days to GET /trades

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-28–30; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-09** — Add holding_days to GET /trades
**Priority:** P3
**Effort:** ~1 hour
**Target release:** v1.7
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-28–30; backend fix path chosen)
**Source:** OBS-QWB-R3-01 — QA Lead observation, QWB verification, 2026-03-01
holding_days is absent from trade objects in the GET /trades response.
trade_endpoints.md v1.8.4 lists it as a required field. Pre-existing behaviour,
not introduced by QWB.
Decision required: Either (a) add holding_days to the backend GET /trades
response (the spec-compliant fix); or (b) remove holding_days from trade_endpoints.md
documented schema. Product Owner + API Contracts owner to decide.
Acceptance Criteria

GET /trades trade objects include holding_days (integer), OR
trade_endpoints.md schema is corrected to remove the field, with a note explaining
its absence and where the value can be sourced (e.g. trades_for_charts)

**Owner:** API Contracts & Documentation Owner
Raised by: QA Lead, 2026-03-01

---

### BLG-TECH-08 — Align portfolio_endpoints.md positions summary field list

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-25–27; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-08** — Align portfolio_endpoints.md positions summary field list
**Priority:** P3
**Effort:** ~30 min
**Target release:** v1.7
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-25–27; spec update path chosen)
**Source:** OBS-QWB-R1-01 — QA Lead observation, QWB verification, 2026-03-01
GET /portfolio positions summary objects omit current_price_native, stop_price,
stop_price_native, and pnl_percent — fields listed in R-01 test scenario step 3
and in portfolio_endpoints.md. Pre-existing behaviour, not introduced by QWB.
Decision required: Either (a) update portfolio_endpoints.md to accurately document
the lightweight summary shape, explicitly distinguishing it from the full position object
on GET /positions; or (b) add the missing fields to the backend response. Product Owner

API Contracts owner to decide.

**Acceptance Criteria**

portfolio_endpoints.md positions summary field list matches the live API response
No discrepancy between spec and implementation for /portfolio positions objects

Owner: API Contracts & Documentation Owner
Raised by: QA Lead, 2026-03-01

---

### BLG-TECH-06 — Canonicalise sharpe_ratio_trade_method as 14th validation metric

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-21–24; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-06** — Canonicalise sharpe_ratio_trade_method as 14th validation metric in analytics_endpoints.md
**Priority:** P2 (Medium)
**Type:** Spec Accuracy / Governance
**Target release:** v1.7 *(updated from v1.6.1 — v1.6.1 has shipped; DL-001 cycle 2026-03-01__item-3.2)*
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-21–24)
**Problem**
POST /validate/calculations returns 14 validation results. analytics_endpoints.md v1.8.1
describes 13 metrics and does not document sharpe_ratio_trade_method.
The 14th metric was introduced under BLG-TECH-01 Addendum 1 (PMO-confirmed scope, 2026-02-20)
to exercise the trade-based Sharpe fallback path. The implementation is correct and the result
passes. The spec is incomplete.
This was recorded as OBS-01 by the QA Lead during BLG-TECH-02/03 re-verification
(2026-02-21T21:25:00Z) and formally acknowledged by the Product Owner (2026-02-21).
Per document_lifecycle_guide.md v2.2 — deviation must have priority, target release,
and owner at time of documentation. These are recorded here.
Scope

Update analytics_endpoints.md to add sharpe_ratio_trade_method as a formally
documented 14th validation metric
Add to the validated metrics table with: severity critical, formula, tolerance
Update the response example to show 14 results and correct by_severity.critical.total: 4
No code change required — implementation is correct

**Acceptance Criteria**

analytics_endpoints.md validated metrics table includes sharpe_ratio_trade_method
Response schema example reflects 14 results
by_severity.critical.total shown as 4 in example (not 3)
No deviation exists between the spec and the live POST /validate/calculations response

**Owner**

API Contracts & Documentation Owner

**Source**

OBS-01 — QA Lead, BLG-TECH-02/03 re-verification, 2026-02-21T21:25:00Z
Product Owner disposition: backlog item, v1.6.1 target, 2026-02-21

---

### BLG-TECH-04 — CI/CD validation workflow (GitHub Actions)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-01; PR #11 merged; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

### BLG-TECH-04 — CI/CD validation workflow (GitHub Actions)
**Priority:** P2 (Medium)
**Type:** Delivery Quality / Automation
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-01)
**Target release:** v1.7

**Problem**
- Validation is manual and not enforced at merge time.

**Scope**
- Add `.github/workflows/validate-analytics.yml`.
- Run `POST /validate/calculations` on:
  - Pull requests
  - Pushes to `main` and `develop`
- Block merge if any **critical-severity** validation fails.
- Post validation summary as PR comment.

**Acceptance Criteria**
- Workflow reliably runs on all PRs.
- Merge is blocked only for critical severity failures.
- Clear PR feedback is visible.

**Dependencies**
- BLG-TECH-02 (severity model must exist).

**Owners**
- Engineering
- QA

---

### BLG-FEAT-07 — CSV Export of Trade History

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-07 — CSV Export of Trade History
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

One-click CSV export for tax and analysis use.

---

### BLG-FEAT-06 — Grace Period Indicator

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-06 — Grace Period Indicator
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Show remaining grace period days in open positions table.
Example: "Day 6 of 10"

---

### BLG-FEAT-05 — Win Rate by Month Chart

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-05 — Win Rate by Month Chart
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Bar chart of win rate grouped by calendar month.

---

### BLG-FEAT-04 — Best / Worst Trades Widget

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-04 — Best / Worst Trades Widget
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Show top 3 and bottom 3 trades by R-multiple or P&L.

---

### BLG-FEAT-02 — R-Multiple Column in Trade History

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-02 — R-Multiple Column in Trade History
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Add R-multiple column to trade history table.

**Indicative Formula**

`(Exit Price - Entry Price) / (Entry Price - Stop Price)`

**Notes**
- Formula must be confirmed by Metrics Definitions owner.
- Decide server-side vs frontend-only calculation.

---

### BLG-FEAT-01 — Current Drawdown Widget

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-01 — Current Drawdown Widget
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Display current drawdown from peak and days underwater.
Example: "Drawdown: -8.2%, 12 days underwater"

**Dependency**
- Metrics Definitions owner must confirm drawdown calculation before implementation.

---

### BLG-TECH-03 — Consolidate ValidationService into service layer

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-04
**Shipped in:** v1.6.1 (co-delivered with BLG-TECH-02)
**Evidence:** Director of Quality sign-off 2026-02-21T21:30:00Z; `docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md`

BLG-TECH-03 — Consolidate ValidationService into service layer
Priority: P1 (High)
Type: Architecture / Maintainability
Status: ✅ COMPLETE — 2026-02-21
Closed

All validation logic moved from routers/validation.py into services/validation_service.py
Router thinned to HTTP in/out only — delegates entirely to ValidationService.validate_all()
Stub replaced with full 13-metric + trade-Sharpe implementation
Delivered in same branch as BLG-TECH-02 per co-delivery constraint
Director of Quality sign-off: 2026-02-21T21:30:00Z
Phase Gate Document filed: docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md

---

### BLG-TECH-02 — Implement validation severity model

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** Director of Quality sign-off 2026-02-21T21:30:00Z; `docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md`

BLG-TECH-02 — Implement validation severity model
Priority: P1 (High)
Type: Governance / Operational Control
Status: ✅ COMPLETE — 2026-02-21
Closed

severity field added to every validation result object (critical / high / medium / low)
by_severity aggregation added to summary — all four tiers always present
Severity mapping implemented in ValidationService per analytics_endpoints.md v1.8.1
Director of Quality sign-off: 2026-02-21T21:30:00Z
Phase Gate Document filed: docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md

---

### BLG-TECH-01 — Fix Sharpe variance method + Capital Efficiency currency basis

**Status at retirement:** ✅ Complete
**Priority at retirement:** P0
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** Canonical Owner sign-off 2026-02-21; 13/13 pass at 2026-02-21T00:24:41Z; `metrics_definitions.md` v1.5.7; `analytics_endpoints.md` v1.8.1

### BLG-TECH-01 — Fix Sharpe variance method + Capital Efficiency currency basis
**Priority:** P0 (Critical)
**Type:** Metrics Correctness / Validation Integrity
**Status:** ✅ COMPLETE — 2026-02-21

**Closed**
- `_calculate_sharpe()` updated to use sample variance (÷ n−1) for portfolio and trade-level Sharpe methods
- Capital efficiency updated to use `Mean(total_cost)` in GBP from `trade_history`
- `validation_data.py` expected values updated: `capital_efficiency` 0.17 → 0.22; `total_cost` fields added
- Validation: 13/13 pass confirmed at 2026-02-21T00:24:41Z
- Canonical Owner sign-off: 2026-02-21
- `metrics_definitions.md` v1.5.7 — Appendix E both items marked resolved
- `analytics_endpoints.md` v1.8.1 — resolved known limitations removed
- v1.6 quality gate: satisfied
