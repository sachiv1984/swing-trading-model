Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v3.1
Cycle: 2026-04-29__release-v3.1
Last Updated: 2026-04-29

## Planning Decisions — v3.1 Arc 2 Start: Trade Plan Object & Pre-Trade Research Foundation

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Defer PT-02 frontend to v3.2 | Design gate is a structural requirement before new frontend pages; PT-02 is a complex unified research view with UX considerations. Delivering backend foundation in v3.1 and frontend in v3.2 ensures quality. | Product Owner | 2026-04-29 |
| Defer PT-03, PT-05 to v3.2 | Both depend logically on PT-02 frontend being live — no value without the research view UI. | Product Owner | 2026-04-29 |
| Defer PT-04 to v3.2+ | Gate condition (20+ closed trades) is a data precondition, not a scope decision. Cannot be pulled forward without the gate being met. | Product Owner | 2026-04-29 |
| Include CF-01, CF-02 as sprint stories | Carry-forward items from v3.0 have recurring process impact (2-cycle recurrence for CF-01). Conversion to sprint stories ensures they are formally tracked and completed. | PMO Lead | 2026-04-29 |
| Combine BLG-SEC-04 + BLG-GOV-17 into one story (ST-12) | Both are XS-effort documentation/audit items with related subject matter (external API credentials and dependency risk). Combined effort is S-class, manageable in a single story. | Product Owner | 2026-04-29 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 ST-01 (spec) before ST-02 (backend) before ST-03 (frontend) | Trade Plan data model must be spec-authored and reviewed before backend implementation; backend must exist before frontend integration. Standard spec-first sequencing. | Head of Specs Team | 2026-04-29 |
| BLG-FE-20 (P1 bug) in Sprint 1 | P1 bug with user-visible impact (watchlist promotion fails for UK tickers). Should be first-in-sprint to unblock users. | Product Owner | 2026-04-29 |
| EPIC-02 in Sprint 2 only | PT-02 backend depends on EPIC-01 completing the Trade Plan data model. Sprint 2 placement respects this dependency. | PMO Lead | 2026-04-29 |
| Design gate between Release Planning and Sprint Planning | Trade Plan frontend (ST-03) and Earnings Calendar frontend (ST-08) are new UI surfaces. Design gate Phase 1.5 must run before sprint planning seals to ensure design sign-off precedes frontend implementation. | Head of UX & Design + Product Owner | 2026-04-29 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No Accepted Risk escalations required — all blockers resolved via scope deferral or sequencing constraints within the release. | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-04-29__release-v3.1
