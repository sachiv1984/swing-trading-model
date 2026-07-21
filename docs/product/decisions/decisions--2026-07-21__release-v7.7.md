Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v7.7
Cycle: 2026-07-21__release-v7.7
Last Updated: 2026-07-21

## Planning Decisions — v7.7 Strategy Intelligence Surfacing & Notification UX

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Exclude BLG-FEAT-73 (SI-02 frontend build) from firm scope | BLG-GOV-107 gate live-reconfirmed NOT MET 2026-07-21 (9th consecutive identical reading since 2026-07-12) — no movement since BLG-FE-109 shipped v7.3. LP-05 flag requires independent gate reconfirmation before scope entry; that reconfirmation failed. Remains a named roadmap anchor, unresolved. | Product Owner | 2026-07-21 |
| Exclude BLG-FEAT-74 (PO-05 Lightweight Replay Mode) from firm scope | No §13 determinism pre-clearance review exists on record for this item; effort (VH, >2 weeks) exceeds this release's realistic single-cycle capacity regardless of gate status. Recommend Strategy Rules & System Intent Owner schedule the §13 review as a distinct future action so a future release planning session has a clean input. | Product Owner | 2026-07-21 |
| No trade-volume gate required for BLG-FEAT-75 (SI-04) | Unlike SI-02, SI-04 compares performance across strategy-rule versions rather than needing an absolute closed-trade count; the version-tagged trade history foundation is already populated (since Arc 2) and unused. Proceeds as ungated. | Product Owner | 2026-07-21 |
| Fill remaining sprint capacity with 6 ready, ungated backlog items (BLG-OPS-108, BLG-GOV-28, BLG-QA-104, BLG-BE-63, BLG-OPS-110, BLG-QA-102) | Explicit user instruction to maximise release scope ("ensure you use full capacity"). The 5 ready named v7.7 anchors alone totalled only ~12.5 days (~45–50%) against a ~24–28 day capacity ceiling. Selected fill items favour correctness/QA/ops value (2 are P1 correctness/governance items overdue for pickup) over pure process/tooling debt, consistent with standing guidance to prioritise product/bug-fix value when a Product Value signal is not in Alert (currently 0.39 Advisory). | Product Owner | 2026-07-21 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (BLG-FEAT-75) sequenced first among design-gated items | Largest single item (H, >5 days) — starting first reduces risk of it slipping past sprint close. | Product Owner | 2026-07-21 |
| EPIC-09 (BLG-BE-63) sequenced before EPIC-10 (BLG-OPS-110) | Idempotency must be confirmed safe before building monitoring/alerting around the same nightly backtest job. | Product Owner | 2026-07-21 |
| EPIC-02/03/04 (all UI-facing) held pending Design Gate PASS | 4 of 11 items carry observable UI acceptance criteria — CLAUDE.md hard-gate requirement; Sprint Planning may not seal until Design Gate passes or a bypass is recorded. | Product Owner | 2026-07-21 |

### Accepted risks
None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-21__release-v7.7
