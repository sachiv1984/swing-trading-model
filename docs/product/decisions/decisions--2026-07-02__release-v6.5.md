Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v6.5
Cycle: 2026-07-02__release-v6.5
Last Updated: 2026-07-03

Superseded by: v6.5 ship — 2026-07-03
Changelog: docs/product/changelog.md#v6.5
Cycle: 2026-07-02__release-v6.5

## Planning Decisions — v6.5 Audit Debt Clearance, Backlog Debt Clearance & AI Thesis Feedback Loop

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Draw v6.5 scope from ungated backlog/audit debt rather than any Now-horizon Arc feature | No Arc 4/5/6 feature item is unblocked this cycle — SI-02 gate last checked 6/11 closed trades vs 20 required (2026-06-09, stale); PO-02/PO-04 further out | Product Owner; Head of Specs Team | 2026-07-02 |
| Include EPIC-01 (BLG-GOV-157/158/159, filed this session) covering the 10 still-open AUD-2026-07-01 findings | v6.4 closed only 7 of 17 audit findings (BLG-GOV-150–153); one remaining finding (AUD-006) is flagged in the audit's own SLA section as a P0-escalation risk if still open at the next audit | Head of Specs Team | 2026-07-02 |
| Include EPIC-02 (BLG-OPS-83, TEST-GAP-EPIC-03-v64, BLG-QA-61) | First two carry explicit `Provisional-Target: v6.5`; BLG-QA-61 is a 3-cycle carry-forward item requiring an active disposition per `2026-07-02__release-v6.4` lessons_learnt_closure.md Carry-Forward #1 | PMO Lead; Head of Specs Team | 2026-07-02 |
| Include EPIC-03 (BLG-FE-46, BLG-FEAT-41) — 2 user-facing items | `2026-07-02__scheduled` rebalance found the Skill-Silo rolling-3-cycle average worsened to 64.8% despite a single U-item pull-forward in v6.4, and explicitly instructed v6.5 to prioritise more than one user-facing item | Product Owner | 2026-07-02 |
| Exclude BLG-SPEC-35 (PO-02 §13 boundary pre-work) | Gate condition ("PO-02 sprint planning imminent") not met — PO-02 remains blocked on the Arc 4 6-months-AI-journal-entries data-density gate | Strategy Rules & System Intent Owner; Product Owner | 2026-07-02 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01, EPIC-02, EPIC-03 have no cross-EPIC dependency and may run in any order or in parallel | No shared files or data-model dependency between the three EPICs | Head of Specs Team | 2026-07-02 |
| Design gate must complete before sprint planning seals, specifically for EPIC-03 | BLG-FE-46 has an observable UI acceptance criterion (feedback UI) — CLAUDE.md §2 hard gate | Head of Specs Team | 2026-07-02 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|--------------|-----------|
| None | — | No escalations raised this cycle | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-02__release-v6.5
