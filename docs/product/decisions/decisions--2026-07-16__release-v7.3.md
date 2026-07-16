Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v7.3
Cycle: 2026-07-16__release-v7.3
Last Updated: 2026-07-16

## Planning Decisions — v7.3 Dashboard/Trade-Plan/Navigation UX Continuation

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include `BLG-FE-109/110/111` as firm scope | Already unblocked and design-gate-approved (under v7.2); simply carried forward unbuilt — no reason to re-litigate scope | Product Owner | 2026-07-16 |
| Include `BLG-SPEC-91/92/93/94` (readiness passes) as firm scope, exclude their paired `BLG-FE-115/116/117/118` implementation items | Mirrors the v7.2 precedent exactly (`BLG-SPEC-89`/`BLG-SPEC-90` shipped before `BLG-FE-109/110/111`); each `BLG-FE-11x` item explicitly depends on its own readiness pass completing first, per that item's own backlog entry | Product Owner | 2026-07-16 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (S2-01–03) has no dependency on EPIC-02–05 and may proceed independently | The 3 UI items' own readiness passes already shipped in v7.2; the 4 new readiness passes are for a different, later feature set | Head of Specs Team | 2026-07-16 |
| EPIC-02–05 may run in any order or in parallel | No item depends on another within this release — each is an independent readiness pass for a different v7.4 candidate | Head of Specs Team | 2026-07-16 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | 0 escalations raised this cycle | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-16__release-v7.3
