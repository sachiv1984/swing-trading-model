Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v2.8
Cycle: 2026-04-17__release-v2.8
Last Updated: 2026-04-20
Superseded by: v2.8 ship — 2026-04-20
Changelog: docs/product/changelog.md#v2.8
Cycle: 2026-04-17__release-v2.8

## Planning Decisions — v2.8 Frontend Completion, Test Quality & AI Journal Feature

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-FE-14 (Market Correlation frontend) | Directly completes v2.7 deferred AC-6; backend live and fully spec'd in analytics_endpoints.md v2.1.0; carry-forward obligation | Product Owner | 2026-04-17 |
| Include BLG-QA-13 (test scenario coverage) | Known test gap from v2.7 delivery verification; SC-CORR and SC-SIG-IND scenarios needed for endpoint coverage | Product Owner | 2026-04-17 |
| Include CF-1 and CF-2 governance patches (S2-03, S2-04) | Carry-forward obligations from v2.7 closure; governance hardening; S effort each | Product Owner | 2026-04-17 |
| Include BLG-GOV-13 (backlog archive deduplication) | S effort quick win; ID uniqueness scan has been returning FAIL since v2.4; PO confirmation of deduplication approach required before execution | Product Owner | 2026-04-17 |
| Include BLG-FEAT-16 (AI Journal Summarisation) | Gate-cleared initiative (SRB-v1.7); Priority 2 in initiative register; first AI feature aligned with system scope; mandatory SRB conditions in AC | Product Owner | 2026-04-17 |
| Defer BLG-GOV-08 (engine prompt compression) to v2.9 as final deferral | L effort; 4 consecutive deferrals (v2.4–v2.7); prompts functional as-is; if not actioned in v2.9, PO will retire from backlog at v2.9 planning | Product Owner | 2026-04-17 |
| Defer BLG-GOV-11 (cycle artefact inventory) to v2.9 | M effort governance housekeeping; lower urgency given other governance items in scope | Product Owner | 2026-04-17 |
| Defer BLG-FEAT-13 (feature flag rollout) to v2.9+ | M effort; not needed at current single-user scale; no active use case requiring staged rollout | Product Owner | 2026-04-17 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Sprint 1: EPIC-02 (test scenarios) + EPIC-03 (governance patches + deduplication) | Independent of design decisions; establishes quality baseline before frontend and AI work; EPIC-03 governance changes should be early to avoid conflicts | PMO Lead | 2026-04-17 |
| Sprint 2: EPIC-01 (frontend) + EPIC-04 (AI Journal) | EPIC-01 requires UX placement decision (pre-sprint); EPIC-04 requires Strategy Rules sign-off in-sprint; both can proceed in parallel once pre-conditions met | PMO Lead | 2026-04-17 |
| EPIC-04 Strategy Rules sign-off is an in-sprint AC — not a planning blocker | SRB-v1.7 conditional compliance already established; sign-off at implementation time is a merge gate, not a pre-condition for sprint planning | Product Owner | 2026-04-17 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations raised; no AR/SRB records required | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-04-17__release-v2.8
