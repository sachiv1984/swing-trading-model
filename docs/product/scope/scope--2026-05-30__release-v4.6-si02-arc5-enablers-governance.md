**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.6
**Cycle:** 2026-05-30__release-v4.6
**Last Updated:** 2026-05-30
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Scope Document — v4.6 SI-02 Behavioural Drift Detection & Arc 5 Completion

---

## Release

**Version:** v4.6
**Theme:** SI-02 Behavioural Drift Detection, Arc 5 Enablers & Governance Debt Clearance
**Cycle:** 2026-05-30__release-v4.6
**Plan published:** 2026-05-30
**Planned sprints:** 2

---

## Cycle

**Sprint 1:** EPIC-04 (governance/OA) + EPIC-01 (SI-02 backend)
**Sprint 2:** EPIC-03 (Arc 5 enablers) + EPIC-02 (SI-02 frontend, data density gate conditional)
**Capacity:** double (~24–28 days/sprint; 2× standard solo-dev baseline)

---

## Items in Scope

| ID | Scope Item | EPIC | Priority | Status |
|----|-----------|------|----------|--------|
| S2-01 | SI-02 Behavioural Drift Detection — Backend (DS-07 migration, drift service, GET /analytics/behavioural-drift, POST /trade-plans capture, unit tests) | EPIC-01 | P1 | Firm |
| S2-02 | SI-02 Behavioural Drift Detection — Frontend (BehaviouralDriftPanel, PerformanceAnalytics integration, Playwright tests) | EPIC-02 | P1 | Firm (gate: data density ≥20 trades) |
| S2-03 | Arc 5 Enablers: red_flag_events severity field, Arc 5 hosting cost projection, Arc 5 nav cohesion review, Red Flag Journal design review scope, SI-05 Phase 1 (conditional) | EPIC-03 | P2 | Firm (4) + Conditional (1) |
| S2-04 | Governance, Spec Debt & OA Resolution: OA-01, BLG-GOV-32/33/34/41/43/45/52, BLG-SPEC-32, OA-02 | EPIC-04 | P1–P3 | Firm |

**Total stories:** 22 (21 firm + 1 conditional)
**EPICs:** 4

---

## Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-25 — PT-04 Setup Quality Score | Gate: 20+ closed trades (ST-16 audit confirms) | TBD gate-conditional |
| BLG-GOV-62 — SI-04 §13 pre-assessment | Gate: SI-04 sprint planning imminent | v4.7+ |
| BLG-SPEC-35 — PO-02 §13 review | Gate: PO-02 sprint planning imminent | TBD |
| BLG-OPS-28 — Staging deploy live verification | Requires live Render environment | v4.7 |
| BLG-FE-43 — SI-05 frontend spec | Gate: SI-05 sprint planning imminent | v4.7 |
| BLG-QA-26 — Arc 5 QA protocol | Gate: all 5 Arc 5 features shipped | Post-v4.6 |
| BLG-GOV-30/31/55 | Already resolved; archive pending next groom backlog | Archive |

---

## Supersession Note

*(To be completed at Post-Ship Closure. This document will be superseded by the v4.6 verification report and changelog entry.)*
