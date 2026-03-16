Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v1.10
Cycle: 2026-03-15__release-v1.10
Last Updated: 2026-03-16

Superseded by: v1.10 ship — 2026-03-16
Changelog: docs/product/changelog.md#v1.10
Verification report: claude/cycles/2026-03-15__release-v1.10/verification_report.md
Cycle: 2026-03-15__release-v1.10

---

## Release Scope — v1.10 Operations & Quality Foundation

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | BLG-OPS-01 — Provision staging/development environment: stable URL, CI/CD auto-deploy, governance QA sign-off process updated |
| S2-02 | EPIC-02 | BLG-TECH-06 — Fix CohortAnalysis.js client-side computation: refactor to call GET /analytics/cohort endpoint; remove buildCohorts() |
| S2-03 | EPIC-03 | BLG-API-01 — Backend API integration tests: FastAPI TestClient for GET /portfolio + GET /portfolio/prospective-heat; CI step added |
| S2-04 | EPIC-03 | BLG-QA-01 (TEST-GAP-EPIC-06) — Author missing v1.7 QA test scenarios: 3 scenarios per verification_report.md §6 |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| 3.5 Alerts & Notifications | v2.0 scope; QA gate still pending | v2.0 |
| 4.1b Tax-Year P&L Statement | v2.0 scope | v2.0 |
| 4.3 Signal Exposure Enhancement | v2.0 scope | v2.0 |
| 4.2 Watchlists & Screening | P2 — do not pull forward | v2.1+ |
| Chart Interactivity Enhancements | P2 — do not pull forward | v2.1+ |
| BLG-NEW-13 — Spec Coverage Inventory | v2.0 target | v2.0 |
| BLG-FEAT-03 — Slippage Tracking | v2.1 target | v2.1 |
| BLG-TECH-05 — Prometheus metrics endpoint | v2.1 target | v2.1 |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-03-15__release-v1.10
