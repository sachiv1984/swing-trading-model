Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v2.2
Cycle: 2026-03-21__release-v2.2
Last Updated: 2026-03-24

Superseded by: v2.2 ship — 2026-03-24
Changelog: docs/product/changelog.md#v22
Verification report: claude/cycles/2026-03-21__release-v2.2/verification_report.md
Cycle: 2026-03-21__release-v2.2

## Release Scope — v2.2 Security, Alert Maturity & Quality

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Security Hardening — API Key Authentication (BLG-SEC-01) + Content Security Policy Headers (BLG-SEC-02) |
| S2-02 | EPIC-02 | Alert System Maturity — Scheduling design and trigger mechanism (BLG-OPS-04) + Alert Threshold Customisation (BLG-FEAT-10) + Alert History Table (BLG-FEAT-12) |
| S2-03 | EPIC-03 | Bug Fixes & Operational Quick Wins — CSV export import bug fix (BLG-BE-03) + Slippage StatsCard cosmetic fix (BLG-FE-01) + Health Check Endpoint (BLG-OPS-06) |
| S2-04 | EPIC-04 | QA Coverage — Execute notifications_scenarios.md on staging (TEST-GAP-EPIC-02) + Create watchlist test scenarios (TEST-GAP-EPIC-03) + Test Automation Readiness Assessment (BLG-QA-02) + Spec-to-Test Traceability Matrix (BLG-SPEC-T01) |
| S2-05 | EPIC-05 | Governance Process Enhancements — Roadmap engine Provisional-Target field (BLG-GOV-04) + Release planning scored_initiatives.md handoff (BLG-GOV-05) + Structured lessons learnt carry-forward block (BLG-GOV-06) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-11 — Strategy Compliance Score (Display-Only) | SPS=4 boundary-adjacent; requires formal Strategy Rules & System Intent Owner review and §13.3 scope constraint documentation before sprint planning | v2.3 |
| BLG-UX-01 — Sidebar navigation overflow | Product Owner design decision (grouping/pattern) needed before spec can be authored | v2.3 |
| BLG-QA-01 — Playwright E2E automation | Sequenced after BLG-QA-02 readiness assessment (in v2.2); natural implementation in v2.3 | v2.3 |
| BLG-FE-02 — Loading State Standardisation | P3; deprioritised in favour of security and alert maturity | v2.3 |
| BLG-FE-03 — User-Facing Error Message Mapping Layer | P3; deprioritised | v2.3 |
| BLG-FEAT-09 — Metrics Staleness Indicator | P2; deprioritised to keep v2.2 focused | v2.3 |
| BLG-OPS-05 — API Endpoint Performance Baseline | P3; deprioritised | v2.3 |
| BLG-GOV-03 — Simplify cycle artefact sealing | P3; governance-internal only | v2.3 |
| BLG-BE-02 (active) — R-Multiple Analysis stop price | P3; note: ID conflict with closed BLG-BE-02 (v2.0) — recommend backlog ID rename before v2.3 promotion | v2.3 |
| BLG-TECH-05 — Prometheus metrics endpoint | P3; conditional on multi-user or operational need | v3.0+ |
| TEST-GAP-EPIC-05-SLIP — Slippage tracking test scenarios | P3 | v2.3 |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-03-21__release-v2.2
