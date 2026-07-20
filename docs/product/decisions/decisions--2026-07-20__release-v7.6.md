Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v7.6
Cycle: 2026-07-20__release-v7.6
Last Updated: 2026-07-20

## Planning Decisions — v7.6 PDF / Print-Friendly Export

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Anchor v7.6 on `BLG-FE-119` alone (single EPIC, single item) | Now horizon was empty at invocation (RA:v7.5 retired in full 2026-07-20); `BLG-FE-119` is the strongest ready, unblocked, standalone P1 candidate — no dependencies, previously stale-targeted twice (v7.3, v7.4) without ever being named anchor scope. Favours product value over process-debt fill per standing PO guidance. | Product Owner | 2026-07-20 |
| Formalize v7.6 on the roadmap via direct-write bypass rather than a full `run roadmap` rebalance | A compliant `run roadmap --reason "scheduled"` path exists and was recommended first; PO explicitly directed the established low-overhead direct-write pattern instead (see `decision_log.md` DL-072) | Product Owner | 2026-07-20 |
| Add `BLG-QA-112` as companion scope (EPIC-02/S2-02) | Its gate condition ("any of BLG-FE-115–119 enters a release scope") fired the moment `BLG-FE-119` was scoped into v7.6. Trivial size (Effort S, ~1 day), directly triggered by this exact release — resolving a fired gate immediately is the compliant default. PO confirmed inclusion explicitly. | Product Owner | 2026-07-20 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| No sequencing constraints — EPIC-01 is standalone | Single EPIC, no dependencies on other in-flight work | Product Owner | 2026-07-20 |

### Accepted risks
None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-20__release-v7.6
