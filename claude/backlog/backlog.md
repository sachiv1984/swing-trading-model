# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-03-09 (ST-11: TEST-GAP-EPIC-01 closed; BLG-API-01 added)
**Last rebalance:** 2026-03-06 (cycle 2026-03-06__item-3.4 — DL-006)

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

*Completed and killed items are recorded in `claude/backlog/backlog_archive.md`.*

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

These items ensure analytical correctness, validation integrity, and operational safety.
They are not user-facing, but they directly affect trust in outputs and release confidence.

---

### BLG-TECH-05 — Prometheus metrics endpoint
**Priority:** P3 (Low — v2.1 candidate)
**Type:** Observability

**Scope**
- Add `GET /metrics` Prometheus endpoint exposing:
  - Validation run count
  - Failure count by metric and severity
  - Validation duration
- Optional Grafana dashboard.

**Acceptance Criteria**
- Metrics scrape successfully in Prometheus format.
- Counters and histograms are correct.

**Target**
- v2.1 or when system becomes multi-user.

---

## 2. Product Feature Backlog (User-Facing)

---

### BLG-FEAT-03 — Slippage Tracking
**Priority:** P2
**Effort:** 1-2 hours

> ⚠️ **Orphan Notice:** No roadmap home or cycle activity detected. Review at next Roadmap Rebalance.

Track and display trade slippage and average slippage summary.

**Indicative Formula**

`(Fill Price - Market Price) / Market Price`

Requires data model update.

---

### BLG-FEAT-08 — Basic Compliance Metrics
**Priority:** P2
**Effort:** ~1 day
**Target release:** v1.9 (pre-work gate for Structured Trade Reflection Template)

Lightweight discipline metrics:
- Journal completion rate
- Stop-based exit rate
- Average position size (% of portfolio)

Definitions must be canonicalised in `metrics_definitions.md` first.

---

## 3. Deferred / v2.1 Candidates

- Daily email portfolio summary
- FX rate history tracking
- Prometheus validation observability (BLG-TECH-05)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system

---

## 4. Explicitly Out of Scope (Product-Level)

These are deliberate product decisions, not deferrals:

- Broker API integration
- Automated trading execution
- Configurable strategy builder
- ML-based predictions
- Social / community features
- Options and futures trading support

---

## 5. Lifecycle Governance Notes

- This backlog is not canonical and must never override:
  - Strategy rules
  - Metrics definitions
  - API contracts
- Any shipped feature must be backed by:
  - Canonical specification
  - Updated validation where applicable
- Once implemented, backlog items are superseded by canonical documentation.

---

## 6. Test Coverage Gaps (from Delivery Verification)

> ⚠️ **Orphan Notice:** No BLG-ID assigned; no explicit roadmap home or cycle activity. Assign a BLG-ID and roadmap home at next Roadmap Rebalance, or close if addressed.

- [TEST-GAP-EPIC-06] Test scenario coverage gap from 2026-03-02__release-v1.7: QA & Testing Owner to create scenarios per verification_report.md §6 (Test Coverage Assessment). Gaps: no scenarios asserting sharpe_ratio_trade_method presence in /validate/calculations response (14 metrics); no scenario asserting portfolio_endpoints.md field alignment; no scenario asserting holding_days in GET /trades. Target: pre-next sprint on analytics, portfolio, or trade endpoint domains.

---

## 7. Spec & Documentation Debt (Head of Specs Review — 2026-03-03)

Review performed: 2026-03-03 by Head of Specs Team.
Scope: all docs/specs/, docs/reference/, docs/governance/, docs/product/, claude/roadmap/, claude/backlog/, backend/main.py cross-referenced against live contracts.

Items are classified as **DRIFT** (spec and implementation/document diverged) or **GAP** (spec section required but absent).

---

### DRIFT Items

---

**BLG-SPEC-D1** — API Contracts README.md version frozen at v1.8.4
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/specs/api_contracts/README.md` header and changelog list contract version as 1.8.4 / 1.8.2.
Three contracts were incremented to v1.9.0 during EPIC-06 (analytics_endpoints.md, portfolio_endpoints.md, trade_endpoints.md).
README.md was not updated.

**Acceptance Criteria**
- README.md version header reflects v1.9.0
- Changelog includes a v1.9.0 entry referencing EPIC-06 changes (sharpe_ratio_trade_method, portfolio field alignment, holding_days)

---

**BLG-SPEC-D3** — GET /market/status completely undocumented live endpoint
**Priority:** P2 (Medium)
**Type:** Documentation Gap / Drift
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`GET /market/status` is implemented in `backend/main.py` (router tag: `market`), called by the frontend MarketStatusBar component, and appears in `docs/System_status_report.md` test results.
No spec document exists. No entry in Specs_Index.md. No openapi.yaml path.

**Scope**
- Create `docs/specs/api_contracts/market_endpoints.md` (or equivalent) documenting GET /market/status: request, response schema (SPY/FTSE regime, live FX rate), error behaviour
- Register in Specs_Index.md §3
- Add to openapi.yaml

**Acceptance Criteria**
- GET /market/status has a canonical spec section
- Response schema matches live implementation
- Registered in Specs_Index.md

---

**BLG-SPEC-D4** — GET /positions/search/tags undocumented
**Priority:** P3 (Low)
**Type:** Documentation Gap
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`GET /positions/search/tags` is implemented in `backend/main.py` (router: positions).
Not documented in `docs/specs/api_contracts/position_endpoints.md`.

**Acceptance Criteria**
- position_endpoints.md includes GET /positions/search/tags with request parameters and response schema

---

**BLG-SPEC-D8** — docs/System_status_report.md missing governance lifecycle header
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Drift
**Owner:** Director of Quality
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/System_status_report.md` has no governance lifecycle header (Owner, Class, Status, Version, Last Updated).
Per `document_lifecycle_guide.md`, all documents must carry a compliant header.
Current document begins directly with `# System Status Verification Report` with no metadata block.

**Acceptance Criteria**
- Lifecycle header added to docs/System_status_report.md: Owner, Class, Status, Version, Last Updated fields
- Class and Status assigned consistently with document_lifecycle_guide.md definitions

---

**BLG-SPEC-D9** — process_index.md and Specs_Index.md reference wrong path for document_lifecycle_guide.md
**Priority:** P3 (Low)
**Type:** Documentation Drift / Broken Cross-Reference
**Owner:** Head of Specs Team
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/governance/process_index.md` references `docs/governance/document_lifecycle_guide.md`.
`docs/specs/Specs_Index.md` §5 references `docs/governance/document_lifecycle_guide.md`.
Actual file location: `claude/charter/document_lifecycle_guide.md`.
The docs/governance/ path does not exist.

**Acceptance Criteria**
- process_index.md updated to reference `claude/charter/document_lifecycle_guide.md`
- Specs_Index.md §5 updated to reference `claude/charter/document_lifecycle_guide.md`

---

### GAP Items

---

**BLG-SPEC-G1** — settings_model.md missing (Specs_Index §6.1, open since 2026-02-21)
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** Head of Specs Team
**Raised:** Specs_Index §6.1, 2026-02-21 (carried forward to 2026-03-03 review)

**Problem**
`docs/specs/data_model/settings_model.md` is listed as an open gap in Specs_Index.md §6.1 since 2026-02-21.
The settings schema is referenced by settings_endpoints.md but no canonical model document exists.
This gap pre-dates v1.7 and remains unresolved.

**Acceptance Criteria**
- settings_model.md created in docs/specs/data_model/ covering: settings schema, field names, types, validation rules, defaults
- Registered in Specs_Index.md §3
- Cross-referenced from settings_endpoints.md

**Note**
Resolution of BLG-SPEC-D2 (PUT vs PATCH method drift) should be decided first, as the resolved API shape will determine the model document scope.

---

**BLG-SPEC-G2** — Error Response Standard not defined (Specs_Index §6.2, open since 2026-02-21)
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** API Contracts & Documentation Owner
**Raised:** Specs_Index §6.2, 2026-02-21 (carried forward to 2026-03-03 review)

**Problem**
No canonical Error Response Standard exists.
Specs_Index.md §6.2 has listed this as an open gap since 2026-02-21.
Without a standard, error shapes across endpoints are inconsistent and untestable against a single schema.

**Acceptance Criteria**
- Error Response Standard document created (or section added to an existing canonical spec)
- Covers: standard error envelope shape, required fields (status_code, error_code, message, detail), HTTP status code mapping
- All existing API contract docs updated to reference the Error Response Standard for their error sections
- Registered in Specs_Index.md

---

**BLG-SPEC-G3** — structured_logging_standards.md not registered in Specs_Index.md
**Priority:** P3 (Low)
**Type:** Index Gap
**Owner:** Head of Specs Team
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/specs/structured_logging_standards.md` was created in EPIC-04 (2026-03-02) as a Class 1 Canonical Specification.
It is not registered in `docs/specs/Specs_Index.md` §3 (Domain Specifications).
New canonical specs must be registered in Specs_Index.md per document_lifecycle_guide.md.

**Acceptance Criteria**
- Specs_Index.md §3 updated to include structured_logging_standards.md with Owner (Head of Engineering), Class (1), Status (Active), Version (0.1.0)

---

**BLG-SPEC-G4** — ADR-002 in wrong location
**Priority:** P3 (Low)
**Type:** Governance Organisation Gap
**Owner:** Head of Specs Team
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
ADR-002 (if it exists) is located in `docs/decisions/` rather than `docs/product/decisions/` where all other decision records are filed (e.g., SRB-v1.7-*.md, api-versioning-v1.7.md).
Inconsistent location breaks navigation and cross-reference from Specs_Index.md.

**Acceptance Criteria**
- ADR-002 moved or copied to `docs/product/decisions/`
- Any cross-references updated
- `docs/decisions/` directory removed or documented if intentionally separate

---

**BLG-SPEC-G5** — validation_system.md owner field non-compliant (Specs_Index §7.1, open since 2026-02-21)
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Gap
**Owner:** Infrastructure & Operations Owner
**Raised:** Specs_Index §7.1, 2026-02-21 (carried forward to 2026-03-03 review)

**Problem**
`docs/specs/validation_system.md` lists owner as `Platform Team` — a team name, not a named role.
Specs_Index.md §7.1 has flagged this as open since 2026-02-21.
Per document_lifecycle_guide.md, Owner must be a named governance role (e.g., Head of Engineering, Director of Quality).

**Acceptance Criteria**
- validation_system.md owner field updated to a named governance role consistent with document_lifecycle_guide.md
- Specs_Index.md §7.1 notation updated to reflect resolved

---

**Review Summary (active items — updated 2026-03-06 groom)**
- Active items: 5 DRIFT (D1, D3, D4, D8, D9), 5 GAP (G1–G5) = 10 total
- Archived this run: D2 (✅ ST-09), D7 (✅ ST-10)
- P2: 3 (D3, G1, G2)
- P3: 7 (D1, D4, D8, D9, G3, G4, G5)
- Oldest open items: G1, G2, G5 — open since 2026-02-21 (3 cycles; ⚠️ priority upgrade review recommended at v1.9 pre-alignment)
- Recommended resolution order: G1 → D3 → G2

---

## 8. New Backlog Items — IW-20260304-01 (Cycle 2026-03-04__item-3.4)

Items promoted to backlog from Idea Intake Window IW-20260304-01 (2026-03-04). Decision log: DL-005.
All items compete within v1.8 release capacity. Release planning engine determines v1.8 backlog slice.

---

### BLG-NEW-04 — AI-Assisted Workflow Governance Policy
**Priority:** P2 (Medium)
**Type:** Governance
**Owner:** Product Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day

**Problem**
The project uses AI-assisted workflows (Claude Code) for governed routines. There is no documented policy governing: which decisions may be taken by AI, which require human override, and how AI output is reviewed before it becomes a canonical record.

**Scope**
- Author an AI-Assisted Workflow Governance Policy document
- Define: AI authority scope, human-in-the-loop requirements, escalation triggers, record-keeping obligations

**Acceptance Criteria**
- Policy document authored and filed under appropriate governance path
- Policy covers: scope of AI authority, mandatory human review checkpoints, record-keeping requirements

---

**Section Summary (IW-20260304-01 active items — updated 2026-03-06 groom)**
- Active: 1 (BLG-NEW-04)
- P2: 1 (BLG-NEW-04)
- Archived this run: BLG-NEW-01 (✅ ST-05), BLG-NEW-02 (✅ ST-06), BLG-NEW-03 (✅ ST-11), BLG-NEW-05 (✅ ST-07), BLG-NEW-07 (✅ ST-12), BLG-NEW-08 (✅ ST-08)
- Archived prior: BLG-NEW-06 (merged into 4.1b — see backlog_archive.md)

---

## v1.8 Release Slice — 2026-03-04

<!-- release-plan-marker: RP:v1.8:2026-03-04__release-v1.8 -->

**Cycle:** 2026-03-04__release-v1.8
**Release:** v1.8 — Risk Dashboard
**Planned:** 2026-03-04
**Backlog slice:** `claude/cycles/2026-03-04__release-v1.8/stage4_backlog_slice.md`

Items in v1.8 sprint: EPIC-01 (ST-01–ST-04), EPIC-02 (ST-05–ST-08), EPIC-03 (ST-09–ST-10), EPIC-04 (ST-11–ST-12)

---

## 9. Risk Dashboard Deviation Backlog (from 2026-03-04__release-v1.8)

Deviation backlog items from EPIC-01 delivery. All accepted for v1.8 by Product Owner (2026-03-05). All target v1.9 resolution unless noted. Source: `docs/specs/frontend/pages/risk_dashboard.md §11`.

---

### BLG-RD-01 — Entity store fallback masks API error states (DEV-ST03-01)
**Priority:** P2
**Type:** Frontend Defect — Error State Coverage
**Owner:** Head of Engineering
**Source:** DEV-ST03-01 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9

When `GET /portfolio` fails, the Base44 entity store fallback (`base44.entities.Position/Portfolio`) activates and supplies stale data, preventing the error state from being rendered. The spec (§8) requires each component to render its own error state independently on API failure.

**Acceptance Criteria**
- Each Risk Dashboard component renders its own error state when `GET /portfolio` fails
- The entity fallback does not silently mask the failure
- Error indicator displayed while fallback data is active (or fallback removed entirely)

---

### BLG-RD-02 — GracePeriodPanel empty vs error state indistinguishable (DEV-ST03-02)
**Priority:** P3
**Type:** Frontend Defect — Error State UX
**Owner:** Head of Engineering
**Source:** DEV-ST03-02 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9

On API failure, `positions` is `[]` and "No positions in grace period" is displayed — indistinguishable from a valid empty state. Spec §5.5 requires an error state when the API fails.

**Acceptance Criteria**
- GracePeriodPanel renders a visible error card when `portfolioError` is set, distinct from the empty state

---

### BLG-RD-03 — PositionRiskTable sorted descending (DEV-ST03-03)
**Priority:** P2
**Type:** Frontend Defect — Sort Direction
**Owner:** Head of Engineering
**Source:** DEV-ST03-03 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9

The PositionRiskTable is sorted by stop distance descending (largest first). Spec §6.4 requires ascending sort (tightest/smallest stop distance first = most at risk positions shown first).

**Acceptance Criteria**
- PositionRiskTable sorts by stop distance ascending within each state group

---

### BLG-RD-04 — Stop Price column absent from PositionRiskTable (DEV-ST03-04)
**Priority:** P2
**Type:** Frontend Defect — Missing Column
**Owner:** Head of Engineering
**Source:** DEV-ST03-04 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9

The Stop Price column (`current_stop`, GBP, 2 dp) required by spec §6.2 is absent. Stop Distance % is shown instead (presentational derivation only).

**Acceptance Criteria**
- Stop Price column present in PositionRiskTable alongside Stop Distance %
- Stop Price displayed in GBP to 2 decimal places per §6.2

---

### BLG-RD-05 — GRACE badge colour amber instead of blue (DEV-ST03-05)
**Priority:** P3
**Type:** Frontend Defect — Cosmetic
**Owner:** Head of Engineering
**Source:** DEV-ST03-05 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9

GRACE badge is rendered in amber. Spec §6.3 requires blue.

**Acceptance Criteria**
- GRACE state badge colour is blue per spec §6.3

---

### BLG-RD-06 — GBP value at risk absent from HeatGauge (DEV-ST03-06)
**Priority:** P3
**Type:** Frontend Defect — Missing Metric
**Owner:** Head of Engineering
**Source:** DEV-ST03-06 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9

The "GBP value at risk" tertiary metric required by spec §3.2 is absent from the Heat Gauge.

**Acceptance Criteria**
- GBP value at risk displayed below the gauge value per spec §3.2

---

### BLG-RD-07 — Days in Grace column absent from GracePeriodPanel (DEV-ST03-07)
**Priority:** P3
**Type:** Frontend Defect — Missing Column
**Owner:** Head of Engineering
**Source:** DEV-ST03-07 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9

The "Days in Grace" (`holding_days`) column required by spec §5.2 is absent from the Grace Period table.

**Acceptance Criteria**
- Days in Grace (`holding_days`) column present in Grace Period table per spec §5.2

---

### BLG-RD-08 — Drawdown data source needs Head of Specs Team verification (DEV-ST03-08)
**Priority:** P2
**Type:** Spec Alignment — Requires Owner Decision
**Owner:** Head of Specs Team
**Source:** DEV-ST03-08 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9
**Status:** RESOLVED — 2026-03-06

ST-06 investigation confirmed split-source data model: `current_drawdown_percent` is computed by `drawdown_service.py` and returned on `GET /portfolio` (confirmed in portfolio_service.py and openapi.yaml). `days_underwater` is computed by `analytics_service.py` and returned on `GET /analytics/metrics`. `risk_dashboard.md §4.1` updated to v0.1.7 to reflect correct split sources. DEV-ST03-08 marked resolved. Head of Specs Team decision 2026-03-06.

---

### BLG-RD-09 — ProspectiveHeatPanel missing threshold label (DEV-ST03-09)
**Priority:** P3
**Type:** Frontend Defect — Missing Display Element
**Owner:** Head of Engineering
**Source:** DEV-ST03-09 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9

`ProspectiveHeatPanel.js` renders projected heat % and delta only. The threshold label (which changes when hypothetical position crosses a boundary) required by spec §7.5 is absent.

**Acceptance Criteria**
- Threshold label badge present in prospective heat result row, updating when boundary is crossed per §7.5

---

### BLG-RD-10 — US entry prices in USD not GBP (DEV-ST03-11)
**Priority:** P2
**Type:** Backend + Frontend Defect — Currency Conversion
**Owner:** Head of Engineering
**Source:** DEV-ST03-11 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9

US position entry prices display in native USD ($) in the Risk Dashboard. Spec §6.2 requires GBP (£) for all positions. The backend returns `entry_price` in native currency without GBP conversion for US positions.

**Acceptance Criteria**
- `portfolio_service.py` converts `entry_price` to GBP for US positions (using stored FX rate)
- Frontend Risk Dashboard displays entry prices in GBP (£) for all positions per §6.2

---

### BLG-RD-11 — current_stop in USD for US positions causes incorrect Stop Distance % (DEV-ST03-12)
**Priority:** P2
**Type:** Backend + Frontend Defect — Currency Conversion
**Owner:** Head of Engineering
**Source:** DEV-ST03-12 — Delivery verification 2026-03-04__release-v1.8
**Target:** v1.9

`current_stop` is returned in native USD for US positions while `current_price` is in GBP. The Stop Distance % display derivation `(current_price − current_stop) / current_price × 100` therefore mixes currencies, producing an incorrect result for all US positions. (Related to BLG-RD-10 — same root cause: native USD not converted to GBP.)

**Acceptance Criteria**
- `portfolio_service.py` converts `current_stop` to GBP for US positions (FX conversion consistent with `current_price`)
- Stop Distance % calculation uses matching currencies for both values per §6.2

---

## 10. Test Coverage Gaps (from 2026-03-04__release-v1.8)

---

### TEST-GAP-EPIC-01 — Risk Dashboard scenario execution infrastructure gap
**Priority:** P2
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-04__release-v1.8 — Director of Quality recommendation
**Cycle added:** 2026-03-04__release-v1.8
**Target release:** v1.9
**Status:** CLOSED — resolved in v1.9 ST-11 (2026-03-09)

17 of 27 Risk Dashboard acceptance scenarios (SC-RD-02–06, SC-RD-07–12, SC-RD-15, SC-RD-16–18, SC-RD-24–25) cannot be executed in the v1.8 environment due to the absence of a test data injection mechanism.

**Resolution:** Playwright mock layer delivered. All 17 scenarios automated in `tests/e2e/risk-dashboard.spec.js`. CI gate at `.github/workflows/playwright.yml`. Mock data in `tests/e2e/mocks/portfolio-mock-data.js`. Scenario document updated to v1.1.

**Last Updated:** 2026-03-09

---

## 11. New Backlog Items — Cycle 2026-03-06__item-3.4

Items promoted to backlog from IW-20260304-01 parked carry-forwards. Decision log: DL-006.
Release planning engine determines v1.9 backlog slice.

---

### BLG-NEW-09 — R-Multiple Distribution Report
**Priority:** P2 (Medium)
**Type:** Analytics / User Value
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-analytics-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Sequence constraint:** After BLG-FEAT-08 metrics definitions (Metrics Definitions owner capacity — LL-05 check applies)

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
**Priority:** P1 (High)
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Scope constraint:** Risk Dashboard components first (resolves TEST-GAP-EPIC-01 infrastructure dependency); new v1.9 feature scenarios added at release time; no retroactive full-coverage mandate

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
- No retroactive full-endpoint coverage required

---

### BLG-NEW-11 — Canonical Terms Glossary
**Priority:** P2 (Medium)
**Type:** Governance / Spec Quality
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Class constraint:** Document must be Class 2 (Supporting) — cross-reference index only; no new canonical rules

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
**Priority:** P1 (High)
**Type:** Engineering Quality / CI
**Owner:** Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Prerequisite:** BLG-NEW-01 (golden output baseline) — COMPLETE
**CI constraint:** Standard must include a minimum coverage threshold enforceable via CI (pytest-cov or equivalent)

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

**Section 11 Summary**
- Active new items: 4 (BLG-NEW-09 through BLG-NEW-12)
- P1: 2 (BLG-NEW-10, BLG-NEW-12)
- P2: 2 (BLG-NEW-09, BLG-NEW-11)

---

## 12. New Backlog Items — Cycle 2026-03-06__release-v1.9

Items raised during sprint execution. Decision authority: Director of Quality (QA infrastructure), Head of Engineering (technical scope).

---

### BLG-API-01 — Backend API integration tests (FastAPI TestClient)
**Priority:** P2
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** ST-11 decision session 2026-03-09 — Head of Engineering and Director of Quality identified gap
**Cycle added:** 2026-03-06__release-v1.9
**Target release:** v1.10

**Problem**
The Playwright mock layer (ST-11) tests frontend rendering behaviour given known API payloads. It does not test whether the backend `GET /portfolio` and `GET /portfolio/prospective-heat` routers return correctly-shaped responses for real database rows. The golden output gate tests pure-math functions; it does not test the router-to-service pipeline end-to-end.

**Scope**
- Add FastAPI `TestClient` integration tests for `GET /portfolio` and `GET /portfolio/prospective-heat` endpoints
- Use fixture data (no live DB required — inject via dependency override or in-memory SQLite)
- Verify: response shape matches `portfolio_endpoints.md` contract, GBP conversion applies for US positions, heat formula produces correct output for known inputs
- Add as a CI step in a new workflow or extend `golden-outputs.yml`

**Acceptance Criteria**
- `TestClient` tests present in `tests/` covering at minimum: portfolio endpoint response shape, US position GBP conversion, heat formula output, prospective-heat endpoint calculation
- Tests are CI-safe (no live DB, no external calls)
- Director of Quality confirms CI step present and passing

**Last Updated:** 2026-03-09

---

## Closed Items

Items archived in `claude/backlog/backlog_archive.md`. Listed most recent first.

| Item ID | Title | Shipped | Cycle | Story |
|---------|-------|---------|-------|-------|
| BLG-NEW-08 | Automated OpenAPI Drift Detection in CI | v1.8 | 2026-03-04__release-v1.8 | ST-08 |
| BLG-NEW-07 | Running API Changelog Document | v1.8 | 2026-03-04__release-v1.8 | ST-12 |
| BLG-NEW-05 | Dependency Vulnerability Scanning in CI | v1.8 | 2026-03-04__release-v1.8 | ST-07 |
| BLG-NEW-03 | Define and Document Unavailability Failure Mode | v1.8 | 2026-03-04__release-v1.8 | ST-11 |
| BLG-NEW-02 | Backtest vs Live Stop Reconciliation Report | v1.8 | 2026-03-04__release-v1.8 | ST-06 |
| BLG-NEW-01 | Golden Output Regression Baseline for CI | v1.8 | 2026-03-04__release-v1.8 | ST-05 |
| BLG-SPEC-D7 | openapi.yaml frozen at v1.8.1 | v1.8 | 2026-03-04__release-v1.8 | ST-10 |
| BLG-SPEC-D2 | settings_endpoints.md spec/implementation mismatch | v1.8 | 2026-03-04__release-v1.8 | ST-09 |
| BLG-NEW-06 | Realised vs Unrealised P&L Labelling | N/A | 2026-03-04__item-3.4 | Merged into 4.1b |

---

## v1.9 Release Slice — 2026-03-06

<!-- release-plan-marker: RP:v1.9:2026-03-06__release-v1.9 -->

**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9 — User Value & Insight
**Planned:** 2026-03-06
**Backlog slice:** `claude/cycles/2026-03-06__release-v1.9/stage4_backlog_slice.md`

Items in v1.9 sprint: EPIC-01 (ST-01–ST-02), EPIC-02 (ST-03–ST-04), EPIC-03 (ST-05), EPIC-04 (ST-06–ST-10), EPIC-05 (ST-11–ST-13), EPIC-06 (ST-14–ST-19)
