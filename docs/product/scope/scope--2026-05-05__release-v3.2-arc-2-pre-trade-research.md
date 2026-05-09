Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v3.2
Cycle: 2026-05-05__release-v3.2
Last Updated: 2026-05-08
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

## Release Scope — v3.2 Arc 2 Pre-Trade Research & Planning

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Pre-Trade Research View frontend (PT-02) — ticker fundamentals, news, and momentum signals from GET /research/{ticker} |
| S2-02 | EPIC-01 | Prospective Heat at Entry integration (PT-03) — surface GET /portfolio/prospective-heat result in research view |
| S2-03 | EPIC-02 | Pre-Trade Entry Checklist (PT-05) — checklist component in Trade Plan flow, pre-population and persistence |
| S2-04 | EPIC-03 | Governance & process prompt hardening — D-01 to D-04 deferred LL items from v3.1 (OA-02 to OA-05) |
| S2-05 | EPIC-03 | Test scenario gap remediation — TEST-GAP-EPIC-01 and TEST-GAP-EPIC-03 from v3.1 delivery verification |
| S2-06 | EPIC-04 | Documentation & security quick wins — BLG-FE-16, BLG-FE-21, BLG-SEC-05, BLG-GOV-18, BLG-GOV-11 |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-13 — Gated feature rollout | Capacity trade-off; Arc 2 is primary. 2nd consecutive deferral — mandatory in v3.3 | v3.3 |
| BLG-FEAT-20 — Net-of-costs performance tracking | Target changed to Arc 3/4 data model context; not standalone sprint item | Arc 3/4 |
| BLG-FE-22 — Screener morning routine UX spec | Design gate prerequisite deliverable — must be completed before sprint planning seals, not a sprint story | Design gate |

### Supersession note
Superseded by: v3.2 ship — 2026-05-08
Changelog: docs/product/changelog.md#v3.2
Verification report: claude/cycles/2026-05-05__release-v3.2/verification_report.md
Cycle: 2026-05-05__release-v3.2
