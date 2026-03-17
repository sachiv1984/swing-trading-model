Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v2.0
Cycle: 2026-03-17__release-v2.0
Last Updated: 2026-03-17

---

## Planning Decisions — v2.0 Reporting & Alerts

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-BE-01 (P1 GET /portfolio fix) in v2.0 Sprint 1 as guaranteed first story | P1 defect from v1.10 QA open since 2026-03-16; v1.11 patch release avoided to eliminate duplicate governance overhead; guarantee enforced by making it Sprint 1 item 1 | Product Owner | 2026-03-17 |
| Include BLG-BE-02 (prospective-heat endpoint) as Sprint 1 stretch | P3 but small scope; natural pairing with BLG-BE-01 backend work | Product Owner | 2026-03-17 |
| Include BLG-GOV-01 + BLG-GOV-02 in v2.0 | Governance prep needed before next roadmap cycle; grouping with v2.0 execution window keeps them from drifting indefinitely | Product Owner | 2026-03-17 |
| EPIC-03 (3.5 Alerts) treated as conditional scope | QA gate 3 (DL-003) is still pending; 3.5 cannot enter sprint execution until gate clears; if uncleared at sprint planning seal, 3.5 defers to v2.1 | Product Owner | 2026-03-17 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ST-12 (BLG-BE-01 P1 fix) is Sprint 1 item 1 | P1 defect; earliest possible resolution required | Product Owner | 2026-03-17 |
| ST-03 (4.1b spec) must precede ST-04 (backend) and ST-05 (frontend) | Tax-year P&L has no endpoint spec; cannot implement before spec is authored and signed off | Head of Specs Team | 2026-03-17 |
| ST-16 (migration governance standard) should precede EPIC-02 schema work | 4.1b may require a new table or schema change; migration governance standard should exist before a migration is run | Head of Engineering | 2026-03-17 |
| EPIC-05 and EPIC-06 run as parallel track | Documentation and governance items are independent of product delivery; do not block product EPICs | PMO Lead | 2026-03-17 |

### Accepted risks

None.

### Supersession note

Superseded by: v2.0 ship — 2026-03-17
Changelog: docs/product/changelog.md#v20--reporting--alerts--2026-03-17
Verification report: claude/cycles/2026-03-17__release-v2.0/verification_report.md
Cycle: 2026-03-17__release-v2.0
