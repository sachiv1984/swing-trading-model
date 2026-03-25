# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-03-25 (session — 1 new item added: BLG-BE-05)
**Last rebalance:** 2026-03-24 (cycle 2026-03-24__scheduled — DL-012)

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
**Priority:** P3 (Low)
**Type:** Observability
**Target release:** v2.3 (or when system becomes multi-user; updated from v2.2 — STEP 3 backlog health scan, cycle 2026-03-24__scheduled)

**Scope**
- Add `GET /metrics` Prometheus endpoint exposing:
  - Validation run count
  - Failure count by metric and severity
  - Validation duration
- Optional Grafana dashboard.

**Acceptance Criteria**
- Metrics scrape successfully in Prometheus format.
- Counters and histograms are correct.

---

## 2. Product Feature Backlog (User-Facing)

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

## 6. New Backlog Items — Cycle 2026-03-15__item-5.3 and Later

---

Items promoted to backlog from idea pool during roadmap rebalance cycle 2026-03-15__item-5.3, and items raised during v1.10 sprint execution and QA sign-off.

---

*BLG-SPEC-G6, BLG-SPEC-D10, BLG-SPEC-D11, BLG-SPEC-D12, BLG-SPEC-D13 — all shipped v2.1 (ST-16/ST-17) — retired to `claude/backlog/backlog_archive.md` 2026-03-21.*

---

### BLG-QA-01 — Playwright E2E automation for chart interactivity scenarios
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Source:** ST-11 post-merge staging sign-off — 2026-03-19 (two bugs found manually that Playwright would have caught automatically)
**Cycle added:** 2026-03-18__release-v2.1
**Effort:** M (~1–2 days)
**Target release:** v2.3
**Depends on:** ~~BLG-OPS-03~~ — resolved: BLG-OPS-03 (per-PR preview environments) shipped in v2.1 (ST-15). No outstanding blockers.

**Problem**
Post-merge staging sign-off for ST-11 found two bugs manually (zoom-out stuck at right edge; tooltip % of total missing). Both were fully automatable — they would have been caught pre-merge if Playwright tests existed. Manual DoQ testing is slow and error-prone for interaction-heavy UI (tooltips, zoom, drag, modals).

**Scope**
- Add Playwright to the repo (`npm install --save-dev @playwright/test`)
- Author E2E tests covering `docs/testing/chart_interactivity_scenarios.md` (SC-CHART-IX-01 through SC-CHART-IX-06):
  - Heatmap tile click → modal content assertions (trade count, P&L)
  - Zoom in/out via scroll and buttons → assert full range is restorable
  - Drag pan → assert window shifts
  - R-Multiple tooltip → assert all three fields (R range, count, % of total)
- Wire into CI as a new workflow step running against the per-PR preview URL
- Seed data prerequisite: same `seed_chart_test_data.sql` approach

**Acceptance Criteria**
- Playwright test suite covers all 16 SC-CHART-IX sub-scenarios
- CI runs tests against the per-PR preview environment on every PR
- Both ST-11 bugs (zoom-out edge, tooltip %) would be caught by the suite
- Test run time < 5 minutes
- DoQ can rely on Playwright pass as primary evidence for non-visual AC; visual AC (colours, ring) remain manual

---

### BLG-BE-04 — R-Multiple Analysis: stop price unavailable from trade_history
**Priority:** P3 (Low)
**Type:** Backend / Data
**Owner:** Head of Engineering
**Source:** ST-11 post-merge staging sign-off — 2026-03-19
**Cycle added:** 2026-03-18__release-v2.1
**Effort:** S (~2–3 hrs)
**Target release:** v2.3
**ID note:** Renumbered from BLG-BE-02 (2026-03-24 — duplicate ID with v2.0 closed item "Spec and implement GET /portfolio/prospective-heat" per backlog health scan GROOM-20260324-01)

**Problem**
`RMultipleAnalysis.js` filters trades using `t.stop_price`. The analytics page passes trades from `trade_history`, which does not carry `initial_stop` (stop price lives on `positions`). Result: the R-Multiple Analysis section shows "R-Multiple requires stop prices to be defined for all trades" even when all positions had stop prices set at entry. The R-Multiple Distribution histogram (which renders inside the same component) only shows when `tradesWithR.length >= 10`.

**Scope**
- Extend the analytics endpoint (or trade history endpoint) to JOIN `positions.initial_stop` into the `trade_history` response
- OR expose `initial_stop` as `stop_price` on the closed trade objects returned to the frontend
- Update `RMultipleAnalysis.js` filter if the field name changes
- Update `docs/specs/api_contracts/analytics_endpoints.md` and `openapi.yaml` if response shape changes

**Acceptance Criteria**
- Closed trades returned to the analytics page include a `stop_price` (or `initial_stop`) field where available
- R-Multiple Analysis section renders correctly for trades where stop prices were set at entry
- `RMultipleAnalysis.js` filter produces correct `tradesWithR` count
- `openapi.yaml` updated in same commit if response shape changes

---

*TEST-GAP-SIG-01, TEST-GAP-TAX-01, BLG-PROC-01 — all shipped v2.1 (ST-18/ST-19) — retired to `claude/backlog/backlog_archive.md` 2026-03-21.*

---

*BLG-FE-01 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-07 — Retired to `claude/backlog/backlog_archive.md`*

---

*BLG-BE-03 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-06 — Retired to `claude/backlog/backlog_archive.md`*

---

## Closed Items

Items archived in `claude/backlog/backlog_archive.md`. Listed most recent first.

| Item ID | Title | Shipped | Cycle | Story |
|---------|-------|---------|-------|-------|
| BLG-GOV-07 | Reinforce backend branch discipline in execution prompt | v2.3 target | 2026-03-21__release-v2.2 (filed) | — |
| BLG-FE-04 | Alert Thresholds empty state: add "Add alert rule" CTA button | v2.3 target | 2026-03-21__release-v2.2 (filed) | — |
| BLG-SPEC-D14 | Update health_endpoints.md to document actual GET /health response schema | v2.3 Sprint 1 | 2026-03-21__release-v2.2 (filed) | — |
| BLG-GOV-06 | Structured lessons learnt carry-forward block | v2.2 | 2026-03-21__release-v2.2 | EPIC-05/ST-15 |
| BLG-GOV-05 | Release planning loads scored_initiatives.md | v2.2 | 2026-03-21__release-v2.2 | EPIC-05/ST-14 |
| BLG-GOV-04 | Roadmap engine Provisional-Target field | v2.2 | 2026-03-21__release-v2.2 | EPIC-05/ST-13 |
| BLG-SPEC-T01 | Spec-to-Test Traceability Matrix | v2.2 | 2026-03-21__release-v2.2 | EPIC-04/ST-12 |
| BLG-QA-02 | Test Automation Readiness Assessment | v2.2 | 2026-03-21__release-v2.2 | EPIC-04/ST-11 |
| TEST-GAP-EPIC-03 | Create watchlist test scenarios | v2.2 | 2026-03-21__release-v2.2 | EPIC-04/ST-10 |
| TEST-GAP-NOTIF-01 | Execute notifications_scenarios.md on staging | v2.2 | 2026-03-21__release-v2.2 | EPIC-04/ST-09 |
| BLG-OPS-06 | Health Check Endpoint | v2.2 | 2026-03-21__release-v2.2 | EPIC-03/ST-08 |
| BLG-FE-01 | Slippage StatsCard gradient key fix | v2.2 | 2026-03-21__release-v2.2 | EPIC-03/ST-07 |
| BLG-BE-03 | CSV export function name import bug fix | v2.2 | 2026-03-21__release-v2.2 | EPIC-03/ST-06 |
| BLG-FEAT-12 | Alert History Table | v2.2 | 2026-03-21__release-v2.2 | EPIC-02/ST-05 |
| BLG-FEAT-10 | Alert Threshold Customisation | v2.2 | 2026-03-21__release-v2.2 | EPIC-02/ST-04 |
| BLG-OPS-04 | Alert scheduling design | v2.2 | 2026-03-21__release-v2.2 | EPIC-02/ST-03 |
| BLG-SEC-02 | Content Security Policy Headers | v2.2 | 2026-03-21__release-v2.2 | EPIC-01/ST-02 |
| BLG-SEC-01 | API Key Authentication for Render Deployment | v2.2 | 2026-03-21__release-v2.2 | EPIC-01/ST-01 |
| BLG-PROC-01 | Cross-EPIC process compliance check | v2.1 | 2026-03-18__release-v2.1 | EPIC-06/ST-19 |
| TEST-GAP-TAX-01 | Tax Year P&L report test scenarios | v2.1 | 2026-03-18__release-v2.1 | EPIC-06/ST-18 |
| TEST-GAP-SIG-01 | Signals page controls test scenarios | v2.1 | 2026-03-18__release-v2.1 | EPIC-06/ST-18 |
| BLG-SPEC-D11 | data_model.md §501 trade_reflections section | v2.1 | 2026-03-18__release-v2.1 | EPIC-06/ST-17 |
| BLG-SPEC-D10 | api_dependencies.md v2.0 additions | v2.1 | 2026-03-18__release-v2.1 | EPIC-06/ST-17 |
| BLG-SPEC-G6 | total_return_pct not returned by GET /analytics/metrics | v2.1 | 2026-03-18__release-v2.1 | EPIC-06/ST-17 |
| BLG-SPEC-D13 | metrics_definitions.md Owner field non-compliant | v2.1 | 2026-03-18__release-v2.1 | EPIC-06/ST-17 |
| BLG-SPEC-D12 | Bulk lifecycle header remediation (28 docs) | v2.1 | 2026-03-18__release-v2.1 | EPIC-06/ST-16 |
| BLG-OPS-03 | Pre-merge frontend preview environments | v2.1 | 2026-03-18__release-v2.1 | EPIC-05/ST-15 |
| BLG-FR-01 | Tax Year P&L Report PDF Export | v2.1 | 2026-03-18__release-v2.1 | EPIC-05/ST-12 |
| BLG-FEAT-03 | Slippage Tracking | v2.1 | 2026-03-18__release-v2.1 | EPIC-05/ST-14 |
| BLG-FR-02 | Tax Year P&L Report CSV Export | v2.1 | 2026-03-18__release-v2.1 | EPIC-05/ST-13 |
| BLG-TECH-08 | Async notification delivery ADR | v2.1 (pre-sprint) | 2026-03-18__release-v2.1 | EPIC-01/ST-01 |
| BLG-GOV-01 | Roadmap stage document consolidation | v2.0 | 2026-03-17__release-v2.0 | EPIC-06/ST-18 |
| BLG-GOV-02 | Ideas register (replace per-file idea submissions) | v2.0 | 2026-03-17__release-v2.0 | EPIC-06/ST-19 |
| TEST-GAP-EPIC-02 | CohortAnalysis backend integration regression scenario | v2.0 | 2026-03-17__release-v2.0 | EPIC-05/ST-20 |
| BLG-BE-02 | Spec and implement GET /portfolio/prospective-heat | v2.0 | 2026-03-17__release-v2.0 | EPIC-04/ST-13 |
| BLG-NEW-13 | Spec Coverage Inventory | v2.0 | 2026-03-17__release-v2.0 | EPIC-05/ST-17 |
| BLG-BE-01 | GET /portfolio missing 4 required fields (GAP-03) | v2.0 | 2026-03-17__release-v2.0 | EPIC-04/ST-12 |
| BLG-OPS-02 | Production Deployment Runbook | v2.0 | 2026-03-17__release-v2.0 | EPIC-05/ST-14 |
| BLG-DATA-01 | Positions Table Data Dictionary | v2.0 | 2026-03-17__release-v2.0 | EPIC-05/ST-15 |
| BLG-TECH-07 | Database Migration Governance Standard | v2.0 | 2026-03-17__release-v2.0 | EPIC-05/ST-16 |
| BLG-OPS-01 | Provision development environment | v1.10 | 2026-03-15__release-v1.10 | EPIC-01/ST-01–ST-03 |
| BLG-TECH-06 | Fix CohortAnalysis client-side computation | v1.10 | 2026-03-15__release-v1.10 | EPIC-02/ST-04 |
| BLG-API-01 | Backend API integration tests (FastAPI TestClient) | v1.10 | 2026-03-15__release-v1.10 | EPIC-03/ST-05–ST-06 |
| TEST-GAP-EPIC-06 | v1.7 test scenario coverage gap (BLG-QA-01) | v1.10 | 2026-03-15__release-v1.10 | EPIC-03/ST-07 |
| BLG-FEAT-08 | Basic Compliance Metrics | v1.9 Sprint 2 | 2026-03-06__release-v1.9 | EPIC-03/ST-01 |
| BLG-NEW-09 | R-Multiple Distribution Report | v1.9 Sprint 2 | 2026-03-06__release-v1.9 | EPIC-02/ST-04 |
| BLG-NEW-10 | Canonical Test Scenario Library | v1.9 | 2026-03-06__release-v1.9 | EPIC-05/ST-11, ST-12 |
| BLG-RD-01 | Entity store fallback masks API error states | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-08 |
| BLG-RD-02 | GracePeriodPanel empty vs error state | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-08 |
| BLG-RD-03 | PositionRiskTable sorted descending | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-04 | Stop Price column absent | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-05 | GRACE badge colour amber instead of blue | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-10 |
| BLG-RD-06 | GBP value at risk absent from HeatGauge | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-10 |
| BLG-RD-07 | Days in Grace column absent | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-08 | Drawdown data source resolved | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-06 |
| BLG-RD-09 | ProspectiveHeatPanel missing threshold label | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-10 | US entry prices in USD not GBP | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-07 |
| BLG-RD-11 | current_stop in USD for US positions | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-07 |
| TEST-GAP-EPIC-01 | Risk Dashboard scenario execution infrastructure gap | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-11 |
| BLG-NEW-04 | AI-Assisted Workflow Governance Policy | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-15 |
| BLG-NEW-11 | Canonical Terms Glossary | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-14 |
| BLG-NEW-12 | Service Layer Test Coverage Standard | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-13 |
| BLG-SPEC-D1 | API Contracts README version frozen | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D3 | GET /market/status undocumented | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-16 |
| BLG-SPEC-D4 | GET /positions/search/tags undocumented | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D8 | System_status_report.md missing header | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D9 | Broken cross-references to lifecycle guide | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G1 | settings_model.md missing | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-17 |
| BLG-SPEC-G2 | Error Response Standard not defined | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-18 |
| BLG-SPEC-G3 | structured_logging_standards.md not in Specs Index | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G4 | ADR-002 in wrong location | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G5 | validation_system.md owner field non-compliant | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
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

*BLG-OPS-03, BLG-FR-01 — shipped v2.1 (ST-15/ST-12) — retired to `claude/backlog/backlog_archive.md` 2026-03-21.*

---

### BLG-GOV-03 — Simplify cycle artefact sealing (remove SHA-256, retain sealed flag)
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Direct session architectural review — 2026-03-18
**Target release:** v2.3

**Problem**
The current release planning engine computes and verifies SHA-256 hashes for sealed artefacts on every run. For a 2-person team, the primary threat (accidental writes by Claude) is already covered by write scope restrictions in STEP 5. Hash recomputation adds schema complexity and verification overhead for a failure mode that `git diff` would catch anyway.

**Proposed change**
- Remove `sealed_hashes` and `artifact_hashes` fields from `state.json` schema
- Remove hash computation and drift detection steps from the release planning engine
- Retain the `sealed: true` flag as the sole sealing mechanism — write gate checks this flag before any modification
- Retain `state_snapshot_hash` on `state.json` only (single lightweight checksum)

**Acceptance Criteria**
- Release planning engine no longer computes or verifies per-artefact SHA-256 hashes
- `state.json` schema updated; `sealed_hashes` and `artifact_hashes` blocks removed
- `sealed: true` flag check remains and is enforced as a hard gate
- All references to hash drift detection removed from prompt and shared_standards

---

*BLG-GOV-04 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-13 — Retired to `claude/backlog/backlog_archive.md`*

---

*BLG-GOV-05 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-14 — Retired to `claude/backlog/backlog_archive.md`*

---

*BLG-GOV-06 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-15 — Retired to `claude/backlog/backlog_archive.md`*

---

### BLG-UX-01 — Sidebar navigation overflow: too many items to reach comfortably
**Priority:** P2 (Medium)
**Type:** UX / Frontend
**Owner:** Product Owner
**Source:** ST-10 DoQ staging sign-off — 2026-03-21
**Target release:** v2.3

**Problem**
The left sidebar now has 13 navigation items. On shorter screens items near the bottom (Settings, Notifications) are hard to reach without scrolling. As the product grows this will worsen.

**Options to consider**
- Group items into collapsible sections (e.g. Trading, Analytics, System)
- Move low-frequency items (System Status, Settings) to a footer strip or icon-only secondary nav
- Sticky scroll within the nav with a visible scrollbar
- Collapse sidebar to icon-only mode on smaller desktop viewports

**Proposed next step**
Product Owner to decide preferred grouping/pattern. Engineering to spec and implement.

---

*TEST-GAP-NOTIF-01 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-09 — Retired to `claude/backlog/backlog_archive.md` — (ID note: renumbered from TEST-GAP-EPIC-02 per GROOM-20260324-01 duplicate scan — original TEST-GAP-EPIC-02 is v2.0 item "CohortAnalysis backend integration regression scenario")*

---

*TEST-GAP-EPIC-03 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-10 — Retired to `claude/backlog/backlog_archive.md`*

---

### TEST-GAP-EPIC-05-SLIP — Create slippage tracking test scenarios
**Priority:** P3 (Low)
**Type:** QA Coverage
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-18__release-v2.1 — TSG-v21-03
**Target release:** v2.3

No scenario file covers slippage tracking (ST-14). QA & Testing Owner to add SC-SLIP-01 through SC-SLIP-04 covering: fill price input on trade entry, slippage % column display (colour-coded), avg slippage StatsCard update, null fill price shows "—". May be added to `docs/testing/reports_scenarios.md` or a new `slippage_scenarios.md`.

---

*BLG-OPS-04 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-03 — Retired to `claude/backlog/backlog_archive.md`*

---

## 7. New Backlog Items — Cycle 2026-03-21__item-3.5

*Added from roadmap rebalance cycle 2026-03-21__item-3.5 (completion event: 3.5 Alerts & Notifications). Ideas window IW-20260321-01 and stale idea clearing.*

---

*BLG-SEC-01 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-01 — Retired to `claude/backlog/backlog_archive.md`*

---

*BLG-FEAT-12 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-05 — Retired to `claude/backlog/backlog_archive.md`*

---

*BLG-FEAT-10 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-04 — Retired to `claude/backlog/backlog_archive.md`*

---

### BLG-FEAT-11 — Strategy Compliance Score (Display-Only)
**Priority:** P2 (Medium)
**Type:** Feature (boundary-adjacent — SPS=4)
**Owner:** Strategy Rules & System Intent Owner + Backend Engineering + Base44 Frontend
**Source:** IW-20260321-01 (IDEA-strategy-owner-20260321-01)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** M–L (~3–5 days)
**Target release:** v2.3

> ⚠️ **Scope constraint (from STEP 5 debate):** This item is display-only. No automated enforcement, no alerts generated by the score, no blocking behaviour. The score surfaces raw ATR/stop data in a compliance-framed summary. Any extension toward automated enforcement or notifications requires a new SPS≥4 review and explicit §13.3 sign-off from Strategy Rules & System Intent Owner.

**Problem**
Users have no dashboard view showing whether their open positions respect ATR-based stop discipline rules. A compliance panel could surface: positions where stop distance exceeds ATR ratio, stops not updated within N days, position sizes that deviate significantly from ATR-derived recommendations.

**Scope**
- Display-only compliance summary panel on the portfolio or positions page
- Per-position scores: stop distance vs ATR, stop update recency, position size vs ATR recommendation
- No automated actions — user reads score and decides
- Backend: new computation endpoint or extend existing positions endpoint
- Update strategy_rules.md cross-reference if new derived fields are introduced

**Acceptance Criteria**
- Compliance panel visible on portfolio/positions page
- Per-position breakdown shows: ATR-based stop compliance flag, days since last stop update, size deviation from ATR recommendation
- No automated notification, alert, or action generated by this panel
- Strategy Rules & System Intent Owner DoQ sign-off required (SPS=4 item) at delivery verification
- §13.3 scope constraint documented in AC and reflected in implementation

---

*BLG-SPEC-T01 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-12 — Retired to `claude/backlog/backlog_archive.md`*

---

### BLG-FEAT-09 — Metrics Staleness Indicator
**Priority:** P2 (Medium)
**Type:** Feature / UX
**Owner:** Metrics Definitions & Analytics Canonical Owner + Base44 Frontend
**Source:** IW-20260321-01 (IDEA-metrics-analytics-20260304-02 — gate cleared: BLG-FEAT-03 slippage tracking shipped)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** S–M (~1–2 days)
**Target release:** v2.3

**Problem**
Analytics metrics can be based on stale data (last portfolio/trade sync may be hours old). No indicator shows the user when data was last refreshed — they may be making decisions based on outdated P&L figures.

**Scope**
- Add "data as of: <timestamp>" indicator to analytics and portfolio pages
- Backend: expose `last_sync_at` or similar field on relevant endpoints
- Frontend: display indicator with relative time ("Updated 2h ago") and absolute time on hover
- Configurable staleness threshold: warn visually if data is >N hours old

**Acceptance Criteria**
- Data freshness indicator visible on analytics and portfolio pages
- Shows relative time (e.g. "Updated 2h ago") and absolute time on hover
- Visual warning (amber) if data is stale beyond a configurable threshold
- openapi.yaml updated if new field added to response

---

*BLG-QA-02 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-11 — Retired to `claude/backlog/backlog_archive.md`*

---

### BLG-FE-02 — Loading State Standardisation
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend Prompt Owner
**Source:** IW-20260321-01 (IDEA-base44-frontend-20260304-01 — gate cleared: BLG-TECH-08 async ADR shipped v2.1)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** M (~1–2 days)
**Target release:** v2.3

**Problem**
API-backed interactions (portfolio load, watchlist load, alert evaluation) show inconsistent loading states — some show a spinner, some flash an empty state, some silently error. Users cannot reliably distinguish "loading" from "empty" from "error".

**Scope**
- Audit all API-backed component interactions for loading, empty, and error state handling
- Establish a standard pattern: loading spinner, empty-state message, error-state message
- Apply pattern consistently across: portfolio, positions, watchlist, alerts, analytics pages
- Document the pattern in the frontend specs

**Acceptance Criteria**
- All API-backed components have consistent loading, empty, and error states
- Spinner shown while awaiting API response on all listed pages
- Empty-state message shown when API returns empty data (distinct from error)
- Error-state message shown on API failure (distinct from empty)
- No regression to existing page layouts

---

### BLG-OPS-05 — API Endpoint Performance Baseline
**Priority:** P3 (Low)
**Type:** Operational / Observability
**Owner:** Head of Engineering + Infrastructure & Operations Owner
**Source:** IW-20260321-01 (IDEA-head-of-engineering-20260304-02 — gate cleared: API surface stable post-v2.1)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** S (~0.5–1 day)
**Target release:** v2.3

**Problem**
No baseline exists for endpoint response times. As features are added (alert evaluation, chart queries), performance regressions cannot be detected. The alert evaluation endpoint and analytics queries are the most likely candidates for slowdown.

**Scope**
- Instrument and document p50/p95 response times for all currently active API endpoints
- Use existing integration test infrastructure or a simple timing script
- Produce a baseline document in `docs/` or as a test artefact
- Identify any endpoint already outside acceptable thresholds

**Acceptance Criteria**
- Response time baseline documented for all endpoints defined in openapi.yaml
- p50 and p95 values recorded
- Any endpoint with p95 > 500ms flagged for investigation

---

*BLG-OPS-06 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-08 — Retired to `claude/backlog/backlog_archive.md`*

---

*BLG-SEC-02 — ✅ COMPLETE — Shipped v2.2 — 2026-03-24 — Cycle: 2026-03-21__release-v2.2 — Story: ST-02 — Retired to `claude/backlog/backlog_archive.md`*

---

### BLG-FE-03 — User-Facing Error Message Mapping Layer
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend Prompt Owner
**Source:** IW-20260304-01 (IDEA-base44-frontend-20260304-02 — gate cleared: BLG-SPEC-G2 Error Response Standard shipped v2.1)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** S–M (~1–2 days)
**Target release:** v2.3
**Depends on:** BLG-SPEC-G2 (✅ shipped v2.1)

**Problem**
Backend API errors surface as raw status codes or technical error messages in the UI. Users see "500" or "undefined" instead of actionable guidance. The Error Response Standard (BLG-SPEC-G2) defines the error envelope — this item consumes it on the frontend.

**Scope**
- Create a frontend error mapping layer: HTTP status code + error code → user-readable message
- Cover all known error codes defined in BLG-SPEC-G2 Error Response Standard
- Apply consistently across all API-consuming components
- Log raw error details to console for debugging; surface friendly message to user

**Acceptance Criteria**
- API errors display a user-readable message rather than a raw code or "undefined"
- Error mapping covers all error codes defined in the Error Response Standard
- Raw technical details logged to console (not shown to user)
- No regression to existing error display behaviour

---

### BLG-SPEC-D14 — Update health_endpoints.md to document actual GET /health response schema
**Priority:** P2 (Medium)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** DEV-HEALTH-001 — ST-08 (v2.2) implementation diverged from spec v1.0 schema
**Cycle added:** 2026-03-21__release-v2.2 (verification run 2026-03-24)
**Effort:** XS (< 1 hour)
**Target release:** v2.3 Sprint 1

**Problem**
`docs/specs/api_contracts/health_endpoints.md` v1.0 specifies `GET /health` returns `{"status": "healthy", "timestamp": "<ISO>", "version": "<string>"}`. The v2.2 ST-08 implementation returns `{"status": "ok"|"error", "db": "connected"|"error", "last_market_status_check": "<ISO or null>", "last_alert_evaluation": "<ISO or null>"}`. The spec must be updated to document the actual canonical schema.

**Acceptance Criteria**
- `health_endpoints.md` updated to v1.1 documenting the current response schema from ST-08
- openapi.yaml OperationalHealthResponse schema matches v1.1 spec
- No functional changes required

---

### BLG-FE-04 — Alert Thresholds empty state: add "Add alert rule" CTA button
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend Prompt Owner
**Source:** DEV-EPIC02-ST04-01 — ST-04 (v2.2) omitted CTA button from AlertThresholdsSection empty state
**Cycle added:** 2026-03-21__release-v2.2 (verification run 2026-03-24)
**Effort:** XS (< 1 hour)
**Target release:** v2.3

**Problem**
`AlertThresholdsSection` renders empty state icon, heading, and body text but omits the "Add alert rule" CTA button specified in `notifications.md §Section 2`. State is effectively unreachable in production (rules are auto-seeded), but spec compliance requires the button.

**Acceptance Criteria**
- "Add alert rule" CTA button present in empty state
- Button opens create form on click (per §Section 2 form spec)
- No regression to populated state

---

### BLG-GOV-07 — Reinforce backend branch discipline in execution prompt
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** DEV-EPIC02-ST05-02 — ST-05 (v2.2) backend commits landed on main rather than EPIC-02 branch
**Cycle added:** 2026-03-21__release-v2.2 (verification run 2026-03-24)
**Effort:** XS
**Target release:** v2.3 (governance update)

**Problem**
When a delegated_frontend story requires backend implementation (new DB migration + endpoint), the backend commits should land on the EPIC branch alongside the frontend, not directly on main. This creates a process deviation (P2) even when functionality is correct. execution_prompt §9 invariants should be reinforced with explicit guidance.

**Acceptance Criteria**
- execution_prompt.md §9 invariants updated to note: "Backend commits tightly coupled to a delegated_frontend story must land on the same EPIC branch unless explicitly authorised as direct-to-main by PMO Lead"
- §6 checklist applied per CLAUDE.md

---

### BLG-GOV-08 — Engine prompt compression: roadmap_prompt and release_planning_prompt
**Priority:** P3 (Low)
**Type:** Governance Process / Technical Debt
**Owner:** Head of Specs Team
**Source:** AUD-2026-03-21 Tier 3 — engine prompt compression deferred (roadmap_prompt 1,581 lines; release_planning_prompt 1,534 lines)
**Cycle added:** 2026-03-24
**Effort:** L
**Target release:** v2.3

**Problem**
`claude/system/roadmap_prompt.md` (1,581 lines) and `claude/system/release_planning_prompt.md` (1,534 lines) are the two largest engine prompts in the governance system. Audit AUD-2026-03-21 flagged both as candidates for compression to reduce per-run token cost. Current inline schemas, repeated examples, and verbose explanatory prose are opportunities for extraction to `shared_standards.md` or for prose tightening without removing instructional precision.

**Acceptance Criteria**
- Both files reduced by at least 10% in line count without removing governance intent or hard gate logic
- Any extracted schemas or reference material moved to `shared_standards.md` with cross-reference added in-engine
- §6 checklist applied per CLAUDE.md for both files
- OPERATIONAL_GUIDE §14 and §6/§6B source prompt headers updated accordingly

---

---

## 10. New Backlog Items — Cycle 2026-03-24__scheduled

*Added from roadmap rebalance cycle 2026-03-24__scheduled (scheduled run, Extended tier). 8 items promoted from ideas pool. Decision log: DL-012.*

---

### BLG-OPS-07 — System Health Check Playbook
**Priority:** P3 (Low)
**Type:** Operational Documentation
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260304-02 (IW-20260304-01 — stale cycle-5; gate cleared: BLG-OPS-06 health endpoint shipped v2.2)
**Cycle added:** 2026-03-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.3

**Problem**
`GET /health` endpoint (BLG-OPS-06) shipped in v2.2 and provides DB connectivity, last market check, and last alert evaluation signals. No operational runbook documents how to respond to those signals — what to do when DB connectivity is "error", how to diagnose and recover, who to contact and what to check. Operators cannot act on monitoring output without documented procedures.

**Scope**
- Document: how to interpret each health signal (`status`, `db`, `last_market_status_check`, `last_alert_evaluation`)
- Provide diagnosis steps for each failure mode (DB error, alert evaluation stalled, market status stale)
- Cover recovery actions for each failure mode
- Reference `GET /health` response schema (health_endpoints.md v1.1)

**Acceptance Criteria**
- Playbook document present in `docs/` covering all health signals from the `GET /health` response
- Each failure mode has a diagnosis + recovery path documented
- Document references health_endpoints.md v1.1 schema

---

### BLG-QA-03 — Canonical Test Execution Report Template
**Priority:** P3 (Low)
**Type:** QA Process Governance
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260304-01 (IW-20260304-01 — stale cycle-5; gate cleared: BLG-QA-02 automation readiness assessment shipped v2.2)
**Cycle added:** 2026-03-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.3

**Problem**
BLG-QA-02 (Test Automation Readiness Assessment) shipped in v2.2 and established a quality baseline, but there is no standard structure for reporting test execution results. Each sprint produces ad-hoc QA notes. A canonical template ensures consistent, comparable QA evidence across cycles and makes DoQ sign-off against it straightforward.

**Scope**
- Define a standard test execution report template covering: sprint/cycle reference, test scenarios run, pass/fail counts, deviations, coverage gaps, DoQ sign-off block
- Template should be usable for both manual and automated test runs
- Template stored in `docs/testing/` or `docs/governance/`

**Acceptance Criteria**
- Template document present and usable
- Template includes all mandatory fields (scenario list, pass/fail, deviation notes, DoQ block)
- Template referenced in QA governance documentation

---

### BLG-QA-04 — Integration Test Coverage Report
**Priority:** P3 (Low)
**Type:** QA / CI Engineering
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260321-01 (IW-20260321-01 — gate cleared: BLG-QA-02 shipped v2.2)
**Cycle added:** 2026-03-24__scheduled
**Effort:** M (~1 day)
**Provisional-Target:** v2.3
**Displacement:** BLG-FE-03 deprioritised in priority queue (broader governance value over error message polish)

**Problem**
The CI pipeline runs integration tests but produces no report showing which API endpoints have coverage vs. which are untested. As endpoints are added, coverage gaps accumulate silently. The DoQ sign-off is made with partial visibility — reviewers cannot see at a glance what is and is not covered.

**Scope**
- Generate a coverage report (or annotated list) showing: each endpoint in openapi.yaml, whether an integration test exists covering it, and test file reference
- Output should be produced by CI on every PR and viewable as a CI artefact or in the test results
- May leverage the existing integration test infrastructure (FastAPI TestClient)

**Acceptance Criteria**
- CI produces an endpoint coverage report on every PR
- Report shows each endpoint with covered / not-covered status
- Coverage gaps are visible to DoQ during sign-off
- Report format machine-readable or human-readable (either acceptable)

---

### BLG-QA-05 — Critical-path Smoke Test (Playwright)
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260321-02 (IW-20260321-01 — gate cleared: BLG-QA-02 shipped v2.2)
**Cycle added:** 2026-03-24__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** v2.3
**Depends on:** BLG-OPS-08 (staging reset — prerequisite for reproducible Playwright runs), BLG-QA-06 (seed scripts)
**Displacement:** BLG-FE-02 deprioritised in priority queue (quality safety net over UX polish)

> ⚠️ **§3 Scope constraint (from STEP 5 debate):** Playwright pass is supporting evidence for non-visual AC only — not a replacement for DoQ human sign-off. Flaky test failures (infrastructure outage, missing seed data) must not block human review. Visual AC (colours, ring indicators) remain manual. This scope constraint must be reflected in the AC and implementation.

**Problem**
BLG-QA-02 identified that three critical paths (add trade, view portfolio, view alerts) have no automated test coverage. Manual testing on every PR is slow and error-prone. BLG-QA-01 (Playwright for chart scenarios) is already in the backlog; this item adds coverage for the three most-used non-chart flows.

**Scope**
- Critical path 1: Add a trade (navigate to add trade form → fill required fields → submit → verify trade appears in portfolio)
- Critical path 2: View portfolio (load portfolio page → assert positions visible, key stats present)
- Critical path 3: View alerts (load alerts page → assert alert rules visible, history table present)
- Run in CI against the staging environment (or per-PR preview if available)
- Seed data: requires BLG-OPS-08 reset script and BLG-QA-06 seed scripts

**Acceptance Criteria**
- Playwright test suite covers all 3 critical paths
- Tests run in CI on every PR
- Run time < 2 minutes for smoke test suite
- Playwright pass is recorded as supporting evidence for non-visual AC — explicit in DoQ sign-off template
- Visual AC (colours, badges, chart rendering) remain DoQ manual review items
- Flaky test failures must not block the PR or human review — failures are advisory

---

### BLG-OPS-08 — Staging Data Reset Script
**Priority:** P3 (Low)
**Type:** Infrastructure / DevOps
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260321-02 (IW-20260321-01 — gate cleared: BLG-QA-02 shipped v2.2)
**Cycle added:** 2026-03-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.3
**Displacement:** TEST-GAP-EPIC-05-SLIP deprioritised in priority queue

**Problem**
Staging DB accumulates state between QA runs, causing test pollution where one session's data affects the next. BLG-QA-02 specifically identified reproducible test execution as a gap. Without a reset script, QA runs on staging produce inconsistent results and DoQ sign-off is less reliable. This item is a prerequisite for BLG-QA-05 (smoke test) and BLG-QA-04 (coverage report).

**Scope**
- Create a script (SQL or shell) that resets the staging DB to a known seed state
- Script idempotent — safe to run multiple times
- Documents minimum required seed data for smoke test scenarios (add trade, view portfolio, view alerts)
- Integration with staging environment Render deployment (manual invocation; not auto-run)

**Acceptance Criteria**
- Script present in repo (`scripts/` or `tools/`)
- Script resets staging DB to reproducible baseline
- Script is documented with usage instructions
- Smoke test scenarios in BLG-QA-05 can be run reliably after executing the reset script

---

### BLG-OPS-09 — Database Size Monitoring Alert
**Priority:** P2 (Medium)
**Type:** Infrastructure / Operational Safety
**Owner:** FinOps & Resource Architect + Backend Engineering
**Source:** IDEA-finops-20260321-02 (IW-20260321-01 — gate cleared: BLG-OPS-06 health endpoint shipped v2.2)
**Cycle added:** 2026-03-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.3
**Displacement:** BLG-TECH-05 deprioritised in priority queue (active data safety risk over deferred observability)

**Problem**
The system runs on Render free tier with a Postgres DB size limit. Without monitoring, the DB could silently fill to the limit, causing data loss with no warning. BLG-OPS-06 (health endpoint) shipped in v2.2 and provides a monitoring hook; this item adds DB size alerting to the existing monitoring infrastructure. Per §3: the alert surfaces a risk condition for human action — no automated response is triggered.

**Scope**
- Add DB size check to the health endpoint or as a separate scheduled check
- Alert mechanism: warning email or Telegram notification when DB size exceeds N% of limit
- Alert threshold configurable (e.g. 80% of Render free tier limit)
- Display current DB size in `GET /health` response or a dedicated admin endpoint

**Acceptance Criteria**
- DB size monitoring configured and active
- Alert sent to user when DB exceeds configured threshold
- Alert is notification-only — no automated cleanup or action triggered (§3 compliance)
- Current DB size queryable (via health endpoint or admin endpoint)

---

### BLG-FE-05 — Alert Notification Badge in Nav
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260321-02 (IW-20260321-01 — gate cleared: BLG-FEAT-12 alert history table shipped v2.2)
**Cycle added:** 2026-03-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.3
**Displacement:** BLG-FE-04 deprioritised in priority queue (higher daily-use value)

**Problem**
BLG-FEAT-12 (alert history table) shipped in v2.2 — the system now persists a record of all fired alerts. Without a visible nav badge, users must actively navigate to the Alerts page to discover unacknowledged alerts. A persistent badge provides ambient awareness without requiring proactive navigation. Per §3: the badge displays existing alert state to the human — no automated action is triggered.

**Scope**
- Add a badge/counter to the Alerts nav item showing unacknowledged alert count
- Badge shows count of alerts since last visit to Alerts page (or all unacknowledged alerts)
- Badge disappears or resets when user navigates to Alerts page
- Reads from the alert history data (BLG-FEAT-12 backend — already available)

**Acceptance Criteria**
- Badge visible on Alerts nav item when unacknowledged alerts exist
- Badge count accurate (reflects unacknowledged alert count)
- Badge clears on navigation to Alerts page
- No automated action triggered by badge — display only
- No regression to existing nav layout

---

### BLG-QA-06 — Test Data Seed Script Library
**Priority:** P2 (Medium)
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner + Backend Engineering
**Source:** IDEA-director-of-quality-20260321-02 (IW-20260321-01 — gate cleared: BLG-QA-02 shipped v2.2)
**Cycle added:** 2026-03-24__scheduled
**Effort:** S–M (~1 day)
**Provisional-Target:** v2.3
**Depends on:** BLG-OPS-08 (staging reset — prerequisite; seed scripts are invoked post-reset)
**Displacement:** BLG-OPS-05 deprioritised in priority queue (seed scripts prerequisite for smoke test work)

**Problem**
BLG-QA-02 (automation readiness assessment) identified test data reproducibility as a prerequisite for any automation investment. Ad-hoc seed data in each test author's environment means tests cannot be run by others or in CI without environment-specific setup. BLG-QA-05 (smoke test) and BLG-QA-04 (coverage report) both depend on a reliable shared seed state.

**Scope**
- Versioned collection of SQL seed scripts per test domain:
  - Alerts domain: seed alert rules + evaluation history
  - Watchlists domain: seed watchlist + symbols
  - Portfolio/trades domain: seed positions + trade history (for critical-path smoke test)
- Scripts scoped to three domains; not unbounded QA infrastructure investment
- Scripts compatible with the BLG-OPS-08 reset workflow
- Stored in `scripts/seeds/` or similar

**Acceptance Criteria**
- Seed scripts present for all three domains (alerts, watchlists, portfolio/trades)
- Scripts runnable independently for each domain
- Compatible with BLG-OPS-08 staging reset workflow
- BLG-QA-05 smoke test scenarios can run end-to-end after executing relevant seed scripts

---

## 12. New Backlog Items — Session 2026-03-25

*User-raised items from session review. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

### BLG-BE-05 — Fix ATR pence→GBP conversion for all UK (.L) tickers
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Bug Fix
**Owner:** Head of Engineering
**Source:** V-PATH1-04 staging test failure — server log ATR=-48.69 for LGEN at £2.45 — 2026-03-25
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.4

**Problem**
`calculate_atr()` in `backend/utils/pricing.py` applies the pence→GBP conversion (`atr / 100`) only when `atr > 100`, but Yahoo Finance returns ATR in pence for all LSE `.L` tickers regardless of magnitude. For most UK stocks (ATR typically 5–30p), the guard is never triggered, leaving ATR in pence while all other price values are in GBP. This causes `calculate_initial_stop()` (multiplier=5.0) to produce deeply negative stop prices (e.g. -48.69 for LGEN at £2.45, ATR=10.23p), which the backend rejects and the position creation call fails.

**Scope**
- In `backend/utils/pricing.py` `calculate_atr()`, remove the `> 100` guard and always divide by 100 for `.L` tickers
- Verify `calculate_initial_stop()` produces a sane positive stop for LGEN (£2.45 entry, expected stop ≈ £1.94 at 5× ATR of ~10p)

**Acceptance Criteria**
- `calculate_atr('LGEN.L', ...)` returns ATR in GBP (e.g. ~0.10) not pence (e.g. ~10.23)
- `calculate_initial_stop(2.45, atr)` returns a positive value in the range £1.80–£2.40 for LGEN
- No regression: existing unit tests for ATR pass; high-ATR stocks (e.g. TSLA) are unaffected

---

<!-- release-plan-marker: RP:v2.3:2026-03-24__release-v2.3 -->

---

## 11. v2.3 Release Slice — Quality Automation & User Insight

*Planned: 2026-03-24 | Cycle: 2026-03-24__release-v2.3 | Backlog slice: claude/cycles/2026-03-24__release-v2.3/stage4_backlog_slice.md*

| EPIC | Story | Title | Priority | Effort | Conditional |
|------|-------|-------|----------|--------|-------------|
| EPIC-01 | ST-01 | BLG-FEAT-11: Strategy Compliance Score (Display-Only) | P2 | M–L | No — Sprint 2; SPS=4 sign-off required |
| EPIC-01 | ST-02 | BLG-FEAT-09: Metrics Staleness Indicator | P2 | S–M | No |
| EPIC-02 | ST-03 | BLG-OPS-08: Staging Data Reset Script | P3 | S | No — Sprint 1 prerequisite; gates ST-04/05 |
| EPIC-02 | ST-04 | BLG-QA-06: Test Data Seed Script Library | P2 | S–M | Yes — gated on ST-03 |
| EPIC-02 | ST-05 | BLG-QA-05: Critical-Path Smoke Test (Playwright) | P2 | M | Yes — gated on ST-03 + ST-04 |
| EPIC-02 | ST-06 | BLG-QA-01: Playwright E2E Chart Interactivity | P2 | M | No (independent) |
| EPIC-03 | ST-07 | BLG-SPEC-D14: Update health_endpoints.md to v1.1 | P2 | XS | No — Sprint 1; gates ST-09 |
| EPIC-03 | ST-08 | BLG-OPS-09: Database Size Monitoring Alert | P2 | S | No |
| EPIC-03 | ST-09 | BLG-OPS-07: System Health Check Playbook | P3 | S | Yes — after ST-07 |
| EPIC-04 | ST-10 | BLG-FE-05: Alert Notification Badge in Nav | P3 | S | No |
| EPIC-04 | ST-11 | BLG-FE-04: Alert Thresholds Empty State CTA Button | P3 | XS | No |
| EPIC-04 | ST-12 | BLG-FE-02: Loading State Standardisation | P3 | M | No |
| EPIC-04 | ST-13 | BLG-UX-01: Sidebar Navigation Overflow | P2 | M | Yes — Product Owner design decision required |
| EPIC-05 | ST-14 | BLG-GOV-07: Reinforce Backend Branch Discipline | P3 | XS | No — Sprint 1 governance quick win |
| EPIC-05 | ST-15 | BLG-QA-03: Canonical Test Execution Report Template | P3 | S | No |
| EPIC-05 | ST-16 | BLG-QA-04: Integration Test Coverage Report | P3 | M | No |
| EPIC-05 | ST-17 | BLG-GOV-08: Engine Prompt Compression | P3 | L | Yes — conditional/stretch Sprint 3 |

*Full acceptance criteria in stage4_backlog_slice.md. Capacity: WARN (~15–26 days estimated; 3 sprints phased). See release_plan.md §Capacity Check §Phasing Recommendation.*

---

<!-- release-plan-marker: RP:v2.2:2026-03-21__release-v2.2 -->

---

## 9. v2.2 Release Slice — Security, Alert Maturity & Quality ✅ Shipped 2026-03-24

*Planned: 2026-03-21 | Shipped: 2026-03-24 | Cycle: 2026-03-21__release-v2.2 | Backlog slice: claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md*
*All 15 items delivered. Verification: Verified_with_deviations. See verification_report.md for full traceability.*

| EPIC | Story | Title | Priority | Effort | Conditional |
|------|-------|-------|----------|--------|-------------|
| EPIC-01 | ST-01 | BLG-SEC-01: API Key Authentication for Render Deployment | P1 | M | No — Sprint 1 priority #1 |
| EPIC-01 | ST-02 | BLG-SEC-02: Content Security Policy Headers | P3 | XS | No — bundle with ST-01 |
| EPIC-02 | ST-03 | BLG-OPS-04: Alert scheduling — define trigger mechanism and rule behaviour | P1 | S | No — Sprint 1 design task; gates ST-04/ST-05 |
| EPIC-02 | ST-04 | BLG-FEAT-10: Alert Threshold Customisation | P2 | M | Yes — gated on ST-03 complete |
| EPIC-02 | ST-05 | BLG-FEAT-12: Alert History Table | P2 | M | Yes — gated on ST-03 complete |
| EPIC-03 | ST-06 | BLG-BE-03: Fix CSV export function name import bug | P2 | XS | No — bundle as quick wins PR |
| EPIC-03 | ST-07 | BLG-FE-01: Fix Slippage StatsCard gradient key | P3 | XS | No — bundle as quick wins PR |
| EPIC-03 | ST-08 | BLG-OPS-06: Health Check Endpoint | P3 | XS | No — bundle as quick wins PR |
| EPIC-04 | ST-09 | TEST-GAP-EPIC-02: Execute notifications_scenarios.md on staging | P2 | S | No |
| EPIC-04 | ST-10 | TEST-GAP-EPIC-03: Create watchlist test scenarios | P2 | S–M | No |
| EPIC-04 | ST-11 | BLG-QA-02: Test Automation Readiness Assessment | P2 | XS–S | No |
| EPIC-04 | ST-12 | BLG-SPEC-T01: Spec-to-Test Traceability Matrix | P2 | M | Yes — after ST-11 |
| EPIC-05 | ST-13 | BLG-GOV-04: Roadmap engine Provisional-Target field | P2 | M | No |
| EPIC-05 | ST-14 | BLG-GOV-05: Release planning loads scored_initiatives.md | P2 | M | No |
| EPIC-05 | ST-15 | BLG-GOV-06: Structured lessons learnt carry-forward block | P2 | M | No |

*Full acceptance criteria in stage4_backlog_slice.md. Capacity: WARN (~16 days estimated; 3 sprints phased). See release_plan.md §Capacity Check §Phasing Recommendation.*

---

<!-- release-plan-marker: RP:v2.1:2026-03-18__release-v2.1 -->

---

## 8. v2.1 Release Slice — Alerts, Watchlists & Enhancements ✅ Shipped 2026-03-21

*Planned: 2026-03-18 | Shipped: 2026-03-21 | Cycle: 2026-03-18__release-v2.1 | Backlog slice: claude/cycles/2026-03-18__release-v2.1/stage4_backlog_slice.md*
*All 19 items delivered. Verification: Verified_with_deviations. See verification_report.md for full traceability.*

| EPIC | Story | Title | Priority | Effort | Conditional |
|------|-------|-------|----------|--------|-------------|
| EPIC-01 | ST-01 | Author async notification delivery ADR (BLG-TECH-08) | P2 | S | No — Sprint 1 item 1 |
| EPIC-02 | ST-02 | Spec: alerts endpoint + notification preference model | P2 | M | Yes — gated on ST-01 complete |
| EPIC-02 | ST-03 | Backend: alert rules engine | P2 | M–H | Yes — gated on ST-02 |
| EPIC-02 | ST-04 | Backend: notification delivery (email) | P2 | M | Yes — gated on ST-02 + ST-01 ADR |
| EPIC-02 | ST-05 | Frontend: notification preferences page | P2 | S–M | Yes — gated on ST-02 |
| EPIC-02 | ST-06 | Frontend: in-app notification feed | P2 | S–M | Yes — gated on ST-02 |
| EPIC-02 | ST-07 | QA: notification delivery test scenarios | P2 | S | Yes — gated on ST-02 |
| EPIC-03 | ST-08 | Spec: watchlist data model + API endpoints | P2 | S–M | No |
| EPIC-03 | ST-09 | Backend: watchlist implementation | P2 | M | No (gated on ST-08) |
| EPIC-03 | ST-10 | Frontend: watchlist UI | P2 | M | No (gated on ST-08/09) |
| EPIC-04 | ST-11 | Implement chart interactivity enhancements (CHART-IX) | P2 | S–M | No |
| EPIC-05 | ST-12 | BLG-FR-01: Tax Year P&L PDF Export | P2 | M | No |
| EPIC-05 | ST-13 | BLG-FR-02: Tax Year P&L CSV Export | P2 | S | No |
| EPIC-05 | ST-14 | BLG-FEAT-03: Slippage Tracking | P2 | S–M | No (internal data model gate) |
| EPIC-05 | ST-15 | BLG-OPS-03: Render PR Preview Environments | P2 | S | No |
| EPIC-06 | ST-16 | BLG-SPEC-D12: Bulk lifecycle header remediation (28 docs) | P2 | S–M | No |
| EPIC-06 | ST-17 | Spec maintenance batch (D13 + G6 + D10 + D11) | P2–P3 | S | No |
| EPIC-06 | ST-18 | Author missing test scenario documents (SIG-01 + TAX-01) | P3 | S | No |
| EPIC-06 | ST-19 | BLG-PROC-01: Cross-EPIC process compliance check | P3 | S | No |

*Full acceptance criteria in stage4_backlog_slice.md.*

---

<!-- release-plan-marker: RP:v2.0:2026-03-17__release-v2.0 -->

---

## 7. v2.0 Release Slice — Reporting & Alerts

*Planned: 2026-03-17 | Cycle: 2026-03-17__release-v2.0 | Backlog slice: claude/cycles/2026-03-17__release-v2.0/stage4_backlog_slice.md*

| EPIC | Story | Title | Priority | Effort | Conditional |
|------|-------|-------|----------|--------|-------------|
| EPIC-01 | ST-01 | Author signals page frontend spec | P2 | S | No |
| EPIC-01 | ST-02 | Implement top_n + lookback_days controls on signals page | P2 | S | No |
| EPIC-02 | ST-03 | Author tax-year P&L report spec | P2 | S–M | No |
| EPIC-02 | ST-04 | Implement GET /reports/tax-year endpoint | P2 | M | No |
| EPIC-02 | ST-05 | Frontend: tax-year P&L report view | P2 | M | No |
| ~~EPIC-03~~ | ~~ST-06~~ | ~~Spec: alerts endpoint + notification preference model~~ | ~~P2~~ | ~~M~~ | **Deferred to v2.1** (DoQ session 2026-03-17) |
| ~~EPIC-03~~ | ~~ST-07~~ | ~~Backend: alert rules engine~~ | ~~P2~~ | ~~M–H~~ | **Deferred to v2.1** |
| ~~EPIC-03~~ | ~~ST-08~~ | ~~Backend: notification delivery (email)~~ | ~~P2~~ | ~~M~~ | **Deferred to v2.1** |
| ~~EPIC-03~~ | ~~ST-09~~ | ~~Frontend: notification preferences page~~ | ~~P2~~ | ~~S–M~~ | **Deferred to v2.1** |
| ~~EPIC-03~~ | ~~ST-10~~ | ~~Frontend: in-app notification feed~~ | ~~P2~~ | ~~S–M~~ | **Deferred to v2.1** |
| ~~EPIC-03~~ | ~~ST-11~~ | ~~QA: notification delivery test scenarios~~ | ~~P2~~ | ~~S~~ | **Deferred to v2.1** — DL-003 session complete; gate documented; prerequisite BLG-TECH-08 required |
| EPIC-04 | ST-12 | Fix GET /portfolio missing 4 fields (BLG-BE-01 P1) — **Sprint 1 item 1** | P1 | S | No |
| EPIC-04 | ST-13 | Spec + implement GET /portfolio/prospective-heat (BLG-BE-02 stretch) | P3 | M | No (stretch) |
| EPIC-05 | ST-14 | BLG-OPS-02: Production Deployment Runbook | P2 | S | No |
| EPIC-05 | ST-15 | BLG-DATA-01: Positions Table Data Dictionary | P2 | S | No |
| EPIC-05 | ST-16 | BLG-TECH-07: Database Migration Governance Standard | P2 | S | No |
| EPIC-05 | ST-17 | BLG-NEW-13: Spec Coverage Inventory | P2 | M | No |
| EPIC-06 | ST-18 | BLG-GOV-01: Roadmap stage document consolidation | P2 | M | No |
| EPIC-06 | ST-19 | BLG-GOV-02: Ideas register | P2 | M | No |
| EPIC-05 | ST-20 | TEST-GAP-EPIC-02: CohortAnalysis regression scenario (stretch) | P3 | S | No (stretch) |

*Full acceptance criteria in stage4_backlog_slice.md.*

---

*For delivery history, see `docs/product/changelog.md`.*
*For the active roadmap, see `claude/roadmap/current_roadmap.md`.*
