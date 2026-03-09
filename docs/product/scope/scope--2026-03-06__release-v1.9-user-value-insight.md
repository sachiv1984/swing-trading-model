Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v1.9
Cycle: 2026-03-06__release-v1.9
Last Updated: 2026-03-09

## Release Scope — v1.9 User Value & Insight

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Structured Trade Reflection Template |
| S2-02 | EPIC-01 | Basic Compliance Metrics (pre-work gate for S2-01) |
| S2-03 | EPIC-02 | Cohort Analysis |
| S2-04 | EPIC-03 | Dashboard Homepage / Session Summary |
| S2-05 | EPIC-04 | Risk Dashboard: entity store fallback masks API errors (BLG-RD-01) |
| S2-06 | EPIC-04 | Risk Dashboard: GracePeriodPanel empty vs error state (BLG-RD-02) |
| S2-07 | EPIC-04 | Risk Dashboard: PositionRiskTable sort direction (BLG-RD-03) |
| S2-08 | EPIC-04 | Risk Dashboard: Stop Price column absent (BLG-RD-04) |
| S2-09 | EPIC-04 | Risk Dashboard: GRACE badge colour (BLG-RD-05) |
| S2-10 | EPIC-04 | Risk Dashboard: GBP value at risk absent from HeatGauge (BLG-RD-06) |
| S2-11 | EPIC-04 | Risk Dashboard: Days in Grace column absent (BLG-RD-07) |
| S2-12 | EPIC-04 | Risk Dashboard: Drawdown data source spec alignment (BLG-RD-08) |
| S2-13 | EPIC-04 | Risk Dashboard: ProspectiveHeatPanel threshold label (BLG-RD-09) |
| S2-14 | EPIC-04 | Risk Dashboard: US entry prices in USD not GBP (BLG-RD-10) |
| S2-15 | EPIC-04 | Risk Dashboard: current_stop in USD for US positions (BLG-RD-11) |
| S2-16 | EPIC-05 | Canonical Test Scenario Library + seeded test infrastructure (TEST-GAP-EPIC-01 / BLG-NEW-10) |
| S2-17 | EPIC-05 | Service Layer Test Coverage Standard + CI enforcement (BLG-NEW-12) |
| S2-18 | EPIC-02 | R-Multiple Distribution Report (BLG-NEW-09) |
| S2-19 | EPIC-06 | Canonical Terms Glossary (BLG-NEW-11) |
| S2-20 | EPIC-06 | AI-Assisted Workflow Governance Policy (BLG-NEW-04) |
| S2-21 | EPIC-06 | Document GET /market/status endpoint (BLG-SPEC-D3) |
| S2-22 | EPIC-06 | Create settings_model.md (BLG-SPEC-G1) |
| S2-23 | EPIC-06 | Define Error Response Standard (BLG-SPEC-G2) |
| S2-24 | EPIC-06 | Update API Contracts README to v1.9.0 (BLG-SPEC-D1) |
| S2-25 | EPIC-06 | Document GET /positions/search/tags (BLG-SPEC-D4) |
| S2-26 | EPIC-06 | Add lifecycle header to System_status_report.md (BLG-SPEC-D8) |
| S2-27 | EPIC-06 | Fix broken cross-references to document_lifecycle_guide.md (BLG-SPEC-D9) |
| S2-28 | EPIC-06 | Register structured_logging_standards.md in Specs_Index.md (BLG-SPEC-G3) |
| S2-29 | EPIC-06 | Move ADR-002 to correct location (BLG-SPEC-G4) |
| S2-30 | EPIC-06 | Fix validation_system.md owner field (BLG-SPEC-G5) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| 3.5 Alerts & Notifications | v2.0 QA gate pending | v2.0 |
| 4.1b Tax-Year P&L Statement | v2.0 scope | v2.0 |
| 4.1c Server-Side PDF Report | v2.0 scope | v2.0 |
| 4.3 Signal Exposure Enhancement | v2.0 scope (§13 gate cleared) | v2.0 |
| 4.2 Watchlists & Screening | Post v2.0 | v2.1+ |
| Chart Interactivity Enhancements | Post v2.0 | v2.1+ |
| BLG-TECH-05 Prometheus endpoint | v2.1 | v2.1+ |
| BLG-FEAT-03 Slippage Tracking | No confirmed v1.9 roadmap home | TBD |

### Supersession note
Superseded by: v1.9 Sprint 1 ship — 2026-03-09
Changelog: docs/product/changelog.md#v19---risk-dashboard-fixes--foundation---sprint-1-of-2-march-2026
Verification report: claude/cycles/2026-03-06__release-v1.9/verification_report.md
Cycle: 2026-03-06__release-v1.9
Sprint 1 scope (shipped): S2-05 through S2-30 (EPIC-04, EPIC-05 partial, EPIC-06)
Sprint 2 scope (pending): S2-01 through S2-04, S2-17 Phase 2 (EPIC-01, EPIC-02, EPIC-03, EPIC-05 ST-12)
