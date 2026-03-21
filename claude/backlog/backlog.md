# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-03-21 (post-ship closure 2026-03-18__release-v2.1 — 10 backlog items closed; BLG-TECH-05 target updated to v2.2)
**Last rebalance:** 2026-03-17 (cycle 2026-03-17__item-v1.10 — DL-009)

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
