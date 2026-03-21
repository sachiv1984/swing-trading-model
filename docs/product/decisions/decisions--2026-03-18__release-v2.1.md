Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Superseded: 2026-03-21 (post-ship closure — v2.1 shipped, cycle closed)
Release: v2.1
Cycle: 2026-03-18__release-v2.1
Last Updated: 2026-03-21

## Planning Decisions — v2.1 Alerts, Watchlists & Enhancements

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-TECH-08 (Notification ADR) as EPIC-01 — first story | ADR is a prerequisite for all EPIC-02 (Alerts) stories; must be resolved before sprint planning seals EPIC-02 items | Product Owner + Head of Engineering | 2026-03-18 |
| Carry forward all 6 deferred v2.0 EPIC-03 Alerts stories into v2.1 | These stories were deferred from v2.0 specifically to v2.1; they remain the highest-priority Now-horizon roadmap item after ADR is complete | Product Owner | 2026-03-18 |
| Include BLG-FR-01/02 (PDF + CSV export) in v2.1 EPIC-05 | Promoted from staging feedback (v2.0); P2 backlog items with clear user need (HMRC filing); format-param extension of existing endpoint — low risk | Product Owner | 2026-03-18 |
| Defer BLG-TECH-05 (Prometheus) to v2.2 | P3, no current operational need at single-user scale; v2.1 already 3-sprint scope | Product Owner | 2026-03-18 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (ADR) must complete before any EPIC-02 sprint story is sealed | Without the architecture decision, the notification spec (ST-02) cannot be written to a stable baseline; premature spec = wasted rework | Product Owner + Head of Engineering | 2026-03-18 |
| EPIC-04 (Chart Interactivity) and EPIC-06 (Spec Debt) in Sprint 1 | Both are low-risk, independent tracks that use frontend/spec capacity not needed for the ADR; quick wins to keep Sprint 1 productive | Product Owner | 2026-03-18 |
| EPIC-03 (Watchlists) scheduled to Sprint 3 — after EPIC-02 Alerts Phase 1 | Alerts is Now-horizon (higher priority); Watchlists is Next-horizon per roadmap §4; ADR and alert infrastructure are pre-work that benefits the full roadmap | Product Owner | 2026-03-18 |

### Accepted risks

None. No escalations raised in this cycle.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-03-18__release-v2.1
