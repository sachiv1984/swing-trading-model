**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-02

---

# QA Evidence Log — EPIC-06: Spec Debt Resolution

**EPIC:** EPIC-06 — Spec Debt Resolution (S2-06, S2-07, S2-08)
**Cycle:** 2026-03-02__release-v1.7
**Sprint goal:** Establish foundational governance, quality, and specification artefacts to unlock v1.8 and v2.0 pre-alignment, and resolve spec debt.
**Test scenarios used:** docs/testing/QWB-quick-wins-bundle-test-scenarios.md

---

## Evidence Table

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| TASK-21 | docs/specs/api_contracts/analytics_endpoints.md#Validated Metrics | sharpe_ratio_trade_method added to validated metrics table with severity, formula, tolerance fields; total metric count now 14 | sharpe_ratio_trade_method in validated metrics table; total: 14 | Pass | None |
| TASK-22 | docs/specs/api_contracts/analytics_endpoints.md#POST /validate/calculations | Response example updated to show 14 results; by_severity.critical.total: 4 | Response example shows 14 results; critical.total: 4 | Pass | None |
| TASK-23 | docs/specs/api_contracts/analytics_endpoints.md | Version incremented 1.8.1 → 1.9.0; OBS-01 resolved | Version incremented; OBS-01 resolved | Pass | None |
| TASK-24 | docs/specs/api_contracts/analytics_endpoints.md | OBS-01 formally resolved and signed off | OBS-01 formally resolved | Pass | None |
| TASK-25 | docs/specs/api_contracts/portfolio_endpoints.md | Decision documented: Option (a) spec update chosen | Decision documented | Pass | None |
| TASK-26 | docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio | portfolio_endpoints.md positions summary field list corrected to match live API response (S2-07); OBS-QWB-R1-01 resolved | Spec matches live API for /portfolio positions objects | Pass | None |
| TASK-27 | docs/specs/api_contracts/portfolio_endpoints.md | Version incremented 1.8.2 → 1.9.0; signed off | Version incremented; sign-off recorded | Pass | None |
| TASK-28 | docs/specs/api_contracts/trade_endpoints.md | Decision documented: backend fix chosen for holding_days | Decision documented | Pass | None |
| TASK-29 | docs/specs/api_contracts/trade_endpoints.md#GET /trades | backend/services/trade_service.py updated: holding_days added to formatted_trades dict; GET /trades response now includes holding_days; OBS-QWB-R3-01 resolved | GET /trades includes holding_days; no discrepancy between spec and implementation | Pass | None |
| TASK-30 | docs/specs/api_contracts/trade_endpoints.md | Version incremented 1.8.4 → 1.9.0; holding_days added to changelog | Version incremented; OBS-QWB-R3-01 resolved | Pass | None |

---

## QA Test Coverage

- **Scenarios run:** docs/testing/QWB-quick-wins-bundle-test-scenarios.md (referenced — manual execution against live API)
- **Regression areas checked:** /validate/calculations endpoint metric count; /portfolio positions field alignment; /trades holding_days field presence; spec version consistency
- **Known deviations filed:** None

---

## QA Sign-off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked

Signed off by: Director of Quality
Date: 2026-03-02
Comments: EPIC-06 fully delivered. All three spec debt items resolved: OBS-01 (analytics_endpoints.md now lists 14 validated metrics including sharpe_ratio_trade_method, v1.9.0), OBS-QWB-R1-01 (portfolio_endpoints.md corrected to match live API, v1.9.0), OBS-QWB-R3-01 (holding_days added to trade_service.py and trade_endpoints.md, v1.9.0). QWB test scenarios referenced.
