# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-03-21 (roadmap rebalance — cycle 2026-03-21__item-3.5 — 12 new backlog items added from DL-011 + BLG-FE-03)
**Last rebalance:** 2026-03-21 (cycle 2026-03-21__item-3.5 — DL-011)

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
**Target release:** v2.2 (or when system becomes multi-user)

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
**Target release:** v2.2
**Depends on:** BLG-OPS-03 (per-PR preview environment — Playwright needs a stable URL to run against)

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

### BLG-BE-02 — R-Multiple Analysis: stop price unavailable from trade_history
**Priority:** P3 (Low)
**Type:** Backend / Data
**Owner:** Head of Engineering
**Source:** ST-11 post-merge staging sign-off — 2026-03-19
**Cycle added:** 2026-03-18__release-v2.1
**Effort:** S (~2–3 hrs)
**Target release:** v2.2

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

### BLG-FE-01 — Slippage StatsCard uses unsupported gradient key (cosmetic)
**Priority:** P3 (Low)
**Type:** Frontend / Cosmetic
**Owner:** Base44 Frontend
**Source:** ST-14 DoQ review observation — 2026-03-20
**Cycle added:** 2026-03-18__release-v2.1
**Effort:** XS (<30 min)
**Target release:** v2.2

**Problem**
`TradeHistory.js` passes `color="cyan"` to the Avg Slippage `StatsCard`. The `StatsCard` gradient map has no `"cyan"` key — the card renders without the expected gradient background. All non-null slippage states (negative/emerald, positive/rose) use colour-coded values in the cell, so this is a cosmetic regression on the summary card only.

**Acceptance Criteria**
- Avg Slippage StatsCard renders with a supported gradient key (e.g. `"slate"` or `"violet"`) when slippage is null/zero
- No regression to the cell-level colour coding (emerald/rose) in `TradeHistoryTable.js`

---

### BLG-BE-03 — Latent CSV export import bug: wrong function name in trade_service.py
**Priority:** P2 (Medium)
**Type:** Backend / Defect
**Owner:** Head of Engineering
**Source:** ST-14 DoQ review observation — 2026-03-20
**Cycle added:** 2026-03-18__release-v2.1
**Effort:** XS (<15 min)
**Target release:** v2.1 (or earliest opportunity)

**Problem**
`backend/services/trade_service.py` imports `get_all_trade_history` from `database`, but the actual function in `database.py` is `get_all_closed_trades_for_csv_export`. The import will raise `ImportError` at runtime if the CSV export path (`GET /trades/export/csv`) is exercised. The bug is latent — the endpoint is defined but this code path is not covered by any current automated test.

This was introduced when BLG-FEAT-07 (CSV Export of Trade History) was shipped. It went undetected because the import error only fires when the function is called, not at module load time (the import is inside `trade_csv_service.py`).

**Acceptance Criteria**
- `trade_service.py` (or whichever service handles `/trades/export/csv`) imports the correct function name from `database.py`
- `GET /trades/export/csv` returns a valid CSV without error
- Regression confirmed: the incorrect import name is present before the fix

---

## Closed Items

Items archived in `claude/backlog/backlog_archive.md`. Listed most recent first.

| Item ID | Title | Shipped | Cycle | Story |
|---------|-------|---------|-------|-------|
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
**Target release:** v2.2

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

### BLG-GOV-04 — Roadmap engine writes Provisional-Target at backlog promotion
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Direct session architectural review — 2026-03-18
**Target release:** v2.2

**Problem**
When the roadmap engine promotes an idea to the backlog (STEP 8/9), it has full scoring context — horizon (Now/Next/Later), effort band, CPS alignment. None of this flows to the backlog item as a provisional release target. Release planning then evaluates candidates without this signal, duplicating capacity reasoning from scratch.

**Proposed change**
- Roadmap engine STEP 9: when writing a promoted item to `backlog.md`, include a `**Provisional-Target:**` field derived from the item's horizon placement (Now → next planned release, Next → +1 release, Later → unscheduled)
- This is a signal, not a commitment — release planning may override it during STEP 4 capacity check
- Addresses the capacity reasoning duplication problem together with BLG-GOV-05

**Acceptance Criteria**
- `roadmap_prompt.md` STEP 9 write instructions include `Provisional-Target` field on new backlog items
- Field format documented in `shared_standards.md`
- Release planning STEP 1 reads `Provisional-Target` as a candidate prioritisation input

---

### BLG-GOV-05 — Release planning loads scored_initiatives.md for effort band handoff
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Direct session architectural review — 2026-03-18
**Target release:** v2.2

**Problem**
`roadmap_prompt.md` (line 864) explicitly states that effort bands in `scored_initiatives.md` are recorded "to provide the release planning engine with sizing signal." However, release planning's STEP 0 load list includes `initiative_register.md` but not `scored_initiatives.md`. The sizing signal is never consumed. Together with BLG-GOV-04 this is the root cause of capacity reasoning being duplicated across the two engines.

**Proposed change**
- Add `claude/roadmap/scored_initiatives.md` to release planning STEP 0 load list
- Release planning STEP 4 capacity check references the effort band from this file rather than re-deriving sizing
- If `scored_initiatives.md` is absent or an item has no entry: fall back to STEP 4 estimate as today

**Acceptance Criteria**
- `release_planning_prompt.md` STEP 0 loads `scored_initiatives.md`
- STEP 4 capacity check references effort bands from the file where available
- `shared_standards.md` documents the handoff contract between the two engines

---

### BLG-GOV-06 — Structured lessons learnt carry-forward block across all engines
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Direct session architectural review — 2026-03-18
**Target release:** v2.2

**Problem**
Lessons learnt from post-ship closure currently produce either (a) deferred patches applied ad-hoc at the next roadmap STEP -1.5, or (b) advisory items that sit in `lessons_learnt_closure.md` and are only consulted if someone remembers to look. No engine reads lessons as a substantive planning input. Carry-forward of learnings is effectively lost after one cycle.

**Proposed change**
- Standardise a `## Carry-Forward` section in `lessons_learnt_closure.md` (3–5 items max, structured as: observation, implication, which engine should act)
- All engines (roadmap, release planning, sprint planning) read this section at STEP 0 and surface it to the operator before proceeding
- Items in Carry-Forward are acknowledged (ticked off) when the relevant engine acts on them, or explicitly deferred with rationale
- Post-ship closure engine writes the Carry-Forward section as part of its STEP output

**Acceptance Criteria**
- `lessons_learnt_closure.md` schema includes `## Carry-Forward` section (documented in `shared_standards.md`)
- `roadmap_prompt.md`, `release_planning_prompt.md`, `sprint_planning_prompt.md` STEP 0 each include a Carry-Forward read-and-acknowledge step
- `post_ship_closure.md` writes the Carry-Forward section as a mandatory STEP output
- At least one carry-forward item from a prior cycle demonstrably influences the next cycle's planning

---

### BLG-UX-01 — Sidebar navigation overflow: too many items to reach comfortably
**Priority:** P2 (Medium)
**Type:** UX / Frontend
**Owner:** Product Owner
**Source:** ST-10 DoQ staging sign-off — 2026-03-21
**Target release:** v2.2

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

### TEST-GAP-EPIC-02 — Watchlist test scenarios: formally execute notifications_scenarios.md on staging
**Priority:** P2 (Medium)
**Type:** QA Coverage
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-18__release-v2.1 — TSG-v21-01
**Target release:** v2.2 (before next sprint touching notifications domain)

SC-NOTIF-01 through SC-NOTIF-08 exist in `docs/testing/notifications_scenarios.md` but were not formally executed and referenced in qa_evidence_EPIC-02.md. QA & Testing Owner to execute on staging and record results. Remaining 3 alert types (stop_loss_approach, grace_period_warning, market_regime_change) require open positions to trigger — test data setup needed.

---

### TEST-GAP-EPIC-03 — Create watchlist test scenarios
**Priority:** P2 (Medium)
**Type:** QA Coverage
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-18__release-v2.1 — TSG-v21-02
**Target release:** v2.2

No test scenario file exists for the watchlist feature. QA & Testing Owner to create `docs/testing/watchlist_scenarios.md` covering: SC-WATCH-01 (add), SC-WATCH-02 (edit), SC-WATCH-03 (delete), SC-WATCH-04 (Add to Position removes from watchlist), SC-WATCH-05 (duplicate 409), SC-WATCH-06 (sort order with mixed signal statuses). SC-WATCH-06 also satisfies deferred AC-6 from ST-10 DoQ sign-off.

---

### TEST-GAP-EPIC-05-SLIP — Create slippage tracking test scenarios
**Priority:** P3 (Low)
**Type:** QA Coverage
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-18__release-v2.1 — TSG-v21-03
**Target release:** v2.2

No scenario file covers slippage tracking (ST-14). QA & Testing Owner to add SC-SLIP-01 through SC-SLIP-04 covering: fill price input on trade entry, slippage % column display (colour-coded), avg slippage StatsCard update, null fill price shows "—". May be added to `docs/testing/reports_scenarios.md` or a new `slippage_scenarios.md`.

---

### BLG-OPS-04 — Alert evaluation scheduling: trigger mechanism and rule behaviour design
**Priority:** P1 (High)
**Type:** Product Design Gap
**Owner:** Product Owner
**Source:** Post-delivery review — 2026-03-20
**Target release:** v2.2

**Problem**
`POST /alerts/evaluate` must be called explicitly to evaluate rules and fire notifications. There is no scheduler — alerts are dormant unless manually triggered. Additionally, the behaviour of each alert rule under real conditions (e.g. frequency, cooldown, what constitutes a `market_regime_change` trigger in practice) has not been fully designed. Without a trigger mechanism and clear rule behaviour, the alert system cannot operate autonomously.

**Outstanding questions for Product Owner**
- How often should evaluation run? (e.g. daily at market close, intraday, on-demand only?)
- Should `stop_loss_approach` and `grace_period_warning` have a cooldown to avoid repeat notifications on consecutive evaluations?
- What is the source of truth for `market_regime_change`? (currently reads `GET /market/status` — is this sufficient?)
- Trigger mechanism preference: external cron (e.g. cron-job.org hitting the staging URL), Render cron job (paid), or a scheduled task within the app?

**Proposed next step**
Product Owner to answer outstanding questions above. Engineering to then spec and implement the scheduler and any cooldown logic as a follow-on story.

---

## 7. New Backlog Items — Cycle 2026-03-21__item-3.5

*Added from roadmap rebalance cycle 2026-03-21__item-3.5 (completion event: 3.5 Alerts & Notifications). Ideas window IW-20260321-01 and stale idea clearing.*

---

### BLG-SEC-01 — API Key Authentication for Render Deployment
**Priority:** P1 (High)
**Type:** Security
**Owner:** Backend Engineering Patterns Owner
**Source:** IW-20260321-01 (IDEA-backend-engineering-20260321-01 + IDEA-cybersecurity-20260321-02)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** M (~1 day)
**Target release:** v2.2

**Problem**
The system is deployed on Render with publicly accessible URLs. There is no authentication on the API. Financial data (portfolio, trades, P&L, tax reports) is readable by anyone who knows the Render URL. HTTPS + unguessable URL is obscurity, not security.

**Scope**
- Add `X-API-Key` header requirement to all non-public API endpoints
- Single hard-coded API key (environment variable) for single-user system
- Return 401 on missing or invalid key
- Document in `docs/specs/api_contracts/` (note: this must follow the OpenAPI Drift Detection rules — all endpoints must remain in openapi.yaml)
- Frontend must include the API key in all requests (environment config)

**Acceptance Criteria**
- All endpoints require a valid X-API-Key header
- Missing or invalid key returns HTTP 401
- Frontend includes key from environment variable on all API calls
- No regression to existing functionality

---

### BLG-FEAT-12 — Alert History Table
**Priority:** P2 (Medium)
**Type:** Feature / Data Model
**Owner:** Data Model & Domain Schema Owner + Backend Engineering
**Source:** IW-20260321-01 (IDEA-data-model-owner-20260321-01)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** M (~2–3 days)
**Target release:** v2.2
**Depends on:** BLG-OPS-04 (alert scheduling design — best sequenced together)

**Problem**
Alert evaluation results are transient. There is no record of which rules fired, what values triggered them, when they fired, or whether a notification was sent. Users cannot review alert history, debug misconfigurations, or trust that the system behaved correctly while they were away.

**Scope**
- New `alert_evaluations` table: stores evaluation timestamp, rule type, symbol, triggered (bool), values compared, notification_sent (bool)
- `GET /alerts/history` endpoint returning recent evaluation records (last N days or N records)
- Frontend: alert history view (table or list, sortable by date/symbol)
- Schema migration with appropriate index on timestamp + rule_type
- Update `docs/specs/api_contracts/alerts_endpoints.md` + `openapi.yaml`

**Acceptance Criteria**
- Every `POST /alerts/evaluate` call persists a record per rule evaluated
- `GET /alerts/history` returns records with: timestamp, rule type, symbol, triggered flag, notification sent flag
- Frontend displays history; records are sortable and filterable by rule type
- Schema migration is reversible (down migration documented)
- openapi.yaml updated in same commit

---

### BLG-FEAT-10 — Alert Threshold Customisation
**Priority:** P2 (Medium)
**Type:** Feature
**Owner:** Product Owner + Backend Engineering Patterns Owner
**Source:** IW-20260321-01 (IDEA-product-owner-20260321-01)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** M (~2–3 days)
**Target release:** v2.2

**Problem**
Alert rules use fixed hardcoded thresholds (e.g. stop_loss_approach % trigger). A user monitoring a low-volatility stock needs different thresholds than one monitoring high-volatility stocks. No per-rule or per-symbol threshold customisation exists.

**Scope**
- User-configurable numeric thresholds per alert rule type (e.g. stop_loss_approach: notify when within N% of stop)
- Store thresholds in user settings or alert rule record
- Frontend: threshold input fields on alert creation/edit UI
- Backend: evaluation logic reads threshold from rule record, not hardcoded constant
- Update `docs/specs/api_contracts/alerts_endpoints.md` + `openapi.yaml` if schema changes

**Acceptance Criteria**
- User can set a custom threshold when creating or editing an alert rule
- Alert evaluation uses the per-rule threshold
- Default threshold (current hardcoded value) applies when no custom value is set
- Threshold visible on alert list view
- openapi.yaml updated if response/request shape changes

---

### BLG-FEAT-11 — Strategy Compliance Score (Display-Only)
**Priority:** P2 (Medium)
**Type:** Feature (boundary-adjacent — SPS=4)
**Owner:** Strategy Rules & System Intent Owner + Backend Engineering + Base44 Frontend
**Source:** IW-20260321-01 (IDEA-strategy-owner-20260321-01)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** M–L (~3–5 days)
**Target release:** v2.2

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

### BLG-SPEC-T01 — Spec-to-Test Traceability Matrix
**Priority:** P2 (Medium)
**Type:** Quality / Documentation
**Owner:** Director of Quality + Head of Specs Team
**Source:** IW-20260321-01 (IDEA-director-of-quality-20260304-01 — gate cleared: ST-17 shipped v2.1)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** M (~1–2 days)
**Target release:** v2.2
**Depends on:** ST-17 (Spec Coverage Inventory — ✅ shipped v2.1)

**Problem**
DoQ sign-offs cite test scenarios but there is no formal mapping from canonical spec ACs to specific test scenario IDs. AC coverage gaps are invisible — a scenario may exist that is not tied to any AC, or an AC may have no scenario covering it.

**Scope**
- For each canonical spec with test scenarios, create a traceability mapping: AC → scenario ID(s)
- Start with high-value specs: alert rules, portfolio, positions, trade history
- Document in `docs/testing/` as a reference alongside existing scenario files
- Review against Specs_Index.md §9 (Test Coverage Gaps — v2.1) to confirm gaps are tracked

**Acceptance Criteria**
- Traceability matrix exists for at least 3 canonical specs
- Each AC in covered specs maps to ≥1 scenario ID or is explicitly flagged as "No scenario — gap"
- Gaps are added to TEST-GAP tracking

---

### BLG-FEAT-09 — Metrics Staleness Indicator
**Priority:** P2 (Medium)
**Type:** Feature / UX
**Owner:** Metrics Definitions & Analytics Canonical Owner + Base44 Frontend
**Source:** IW-20260321-01 (IDEA-metrics-analytics-20260304-02 — gate cleared: BLG-FEAT-03 slippage tracking shipped)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** S–M (~1–2 days)
**Target release:** v2.2

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

### BLG-QA-02 — Test Automation Readiness Assessment
**Priority:** P2 (Medium)
**Type:** QA Process / Scoping
**Owner:** QA & Testing Owner + Director of Quality
**Source:** IW-20260321-01 (IDEA-qa-testing-20260304-02 — gate cleared: CI automation exists post-v1.10)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** XS–S (~0.5–1 day)
**Target release:** v2.2
**Sequencing:** Should precede BLG-QA-01 (Playwright E2E) to confirm scope

**Problem**
Before investing in broad test automation (Playwright, integration test suite expansion), a readiness assessment should confirm: what infrastructure exists, what gaps remain, what is the optimal sequencing and tooling. Without this, automation investment may be misdirected.

**Scope**
- Review current test infrastructure (pytest integration tests, golden output tests, existing Playwright setup if any)
- Map to BLG-QA-01 (Playwright E2E) and TEST-GAP items — confirm sequencing
- Produce a short readiness report (1–2 pages) with: current state, recommended investments, priority order
- Output: recommended scope for BLG-QA-01

**Acceptance Criteria**
- Readiness assessment document produced
- Current automation coverage quantified (% endpoints with integration tests)
- Recommended sequencing for BLG-QA-01 and other automation investments confirmed
- Director of Quality sign-off

---

### BLG-FE-02 — Loading State Standardisation
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend Prompt Owner
**Source:** IW-20260321-01 (IDEA-base44-frontend-20260304-01 — gate cleared: BLG-TECH-08 async ADR shipped v2.1)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** M (~1–2 days)
**Target release:** v2.2

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
**Target release:** v2.2

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

### BLG-OPS-06 — Health Check Endpoint
**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner + Backend Engineering
**Source:** IW-20260321-01 (IDEA-infra-ops-20260321-01 — direct backlog routing)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** XS (<1 hour)
**Target release:** v2.2

**Problem**
No `GET /health` endpoint exists. Monitoring tools, uptime checks, and alert schedulers have no way to verify system availability without parsing business logic responses.

**Scope**
- Add `GET /health` endpoint returning: HTTP 200, JSON with `{"status": "ok", "db": "connected" | "error", "last_market_status_check": "<ISO>", "last_alert_evaluation": "<ISO or null>"}`
- Add to openapi.yaml
- Wire into any future alert scheduler as a pre-flight check

**Acceptance Criteria**
- `GET /health` returns 200 with above JSON when system is healthy
- `db` field reflects actual DB connectivity
- openapi.yaml updated in same commit

---

### BLG-SEC-02 — Content Security Policy (CSP) Headers
**Priority:** P3 (Low)
**Type:** Security / Frontend
**Owner:** Cybersecurity & Trust Lead + Base44 Frontend
**Source:** IW-20260321-01 (IDEA-cybersecurity-20260321-01 — direct backlog routing)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** XS (<1 hour)
**Target release:** v2.2

**Problem**
The React frontend has no Content Security Policy (CSP) headers configured. CSP is a standard defence against XSS attacks that restricts which scripts, styles, and resources can be loaded by the browser.

**Scope**
- Configure CSP headers on the frontend (via meta tag or Render headers configuration)
- Appropriate policy: restrict scripts to same-origin + CDN sources used by the app; no inline scripts (or nonce-based if required)
- Verify no regression — ensure all current resources load correctly under the policy

**Acceptance Criteria**
- CSP header present on all frontend pages
- Browser console shows no CSP violations for normal application use
- No regression to existing page functionality

---

### BLG-FE-03 — User-Facing Error Message Mapping Layer
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend Prompt Owner
**Source:** IW-20260304-01 (IDEA-base44-frontend-20260304-02 — gate cleared: BLG-SPEC-G2 Error Response Standard shipped v2.1)
**Cycle added:** 2026-03-21__item-3.5
**Effort:** S–M (~1–2 days)
**Target release:** v2.2
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
