**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.1
**Cycle:** 2026-03-18__release-v2.1
**Last Updated:** 2026-03-18

---

# Cycle Summary — v2.1 Release Planning

**Release theme:** Alerts, Watchlists & Enhancements
**Cycle ID:** 2026-03-18__release-v2.1
**Date:** 2026-03-18
**Mode:** standard
**Status:** Published

---

## Release Overview

v2.1 is the next delivery horizon following v2.0 (shipped 2026-03-17). The release carries forward the deferred Alerts & Notifications EPIC (3.5 — Now horizon on roadmap) along with the Priority 2 Watchlists and Chart Interactivity initiatives, financial reporting export enhancements from v2.0 staging feedback, and a batch of spec debt and QA coverage items.

**Key constraint:** EPIC-02 (Alerts) is gated on EPIC-01 (BLG-TECH-08 ADR) completion. The notification delivery architecture decision must be made and signed off by Head of Engineering before any Alerts story can be sealed in the sprint backlog.

---

## Scope Summary

| EPIC | Theme | Stories | Effort | Sprint |
|------|-------|---------|--------|--------|
| EPIC-01 | Notification Architecture ADR | ST-01 | S (4–6 hrs) | 1 |
| EPIC-02 | Alerts & Notifications (deferred) | ST-02–ST-07 | M–H (34–60 hrs) | 2–3 (conditional on EPIC-01) |
| EPIC-03 | Watchlists & Screening | ST-08–ST-10 | M (20–36 hrs) | 3 |
| EPIC-04 | Chart Interactivity | ST-11 | S–M (5–10 hrs) | 1 |
| EPIC-05 | Financial Reporting & Enhancements | ST-12–ST-15 | M (18–32 hrs) | 1–2 |
| EPIC-06 | Spec Debt & QA Coverage | ST-16–ST-19 | S–M (13–23 hrs) | 1 |
| **Total** | | **19 stories** | **~93–167 hrs (mid: ~129 hrs)** | **3 sprints** |

**Capacity outcome:** WARN — 3-sprint release. See Phasing Recommendation in `release_plan.md §Capacity Check`.

---

## Risks Carried Forward to Sprint Planning

| RISK-ID | Description | Sprint Planning Action |
|---------|-------------|----------------------|
| RISK-01 | BLG-TECH-08 ADR not yet authored — EPIC-02 cannot be specced until complete | Sprint Planning must verify ST-01 Complete before sealing any EPIC-02 story |
| RISK-02 | EPIC-02 large effort (~47 hrs mid) — dominates Sprint 2 and 3 | Sprint 1 capacity must be preserved for EPIC-01 delivery; phasing plan should be adopted |

---

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] BLG-TECH-08 ADR complete — notification delivery architecture decided and signed off by Head of Engineering. Sprint planning must confirm `ST-01` is marked Complete with sign-off before sealing any EPIC-02 story in the sprint backlog. If ST-01 is not complete at sprint planning time, EPIC-02 stories (ST-02–ST-07) must be deferred to a later sprint.

---

## Deferred Items

| Item | Reason | Target |
|------|--------|--------|
| BLG-TECH-05 Prometheus | P3, below priority threshold | v2.2 |
| BLG-GOV-03/04/05/06 | Governance improvements, v2.2 target set | v2.2 |

---

## Next Command

```
run design-gate --cycle 2026-03-18__release-v2.1
```
or, if design gate is not required for this release:
```
plan sprint --cycle 2026-03-18__release-v2.1
```

Sprint Planning Engine STEP -1 must verify RISK-01 Pre-sprint Required Decision before sealing.
