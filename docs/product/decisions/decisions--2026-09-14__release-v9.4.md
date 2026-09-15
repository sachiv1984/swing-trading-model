Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.4
Cycle: 2026-09-14__release-v9.4
Last Updated: 2026-09-15

Superseded by: v9.4 ship — 2026-09-15
Changelog: docs/product/changelog.md#v9.4
Cycle: 2026-09-14__release-v9.4

## Planning Decisions — v9.4 Full-Capacity Debt Clearance II

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Selected a 28-item / 27.55-day subset from the 74-item / ~65.05-day ungated ready pool via round-robin, category-balanced, P2-first, oldest-id-first selection | Full-capacity instruction; consistent with the same informal method used at v9.1–v9.3 (not yet codified — see v9.3 lessons learnt Friction Item 1, carried in `prompt_change_log.md`) | Release Planning Engine (Head of Specs Team authority) | 2026-09-14 |
| `BLG-GOV-178` excluded from the ready pool and not re-selected as new scope | Its literal AC already shipped at ST-22/v9.3; only retained un-archived for escalation visibility (`ESC-EXEC-20260910-01`) | Release Planning Engine | 2026-09-14 |
| `BLG-FEAT-95` selected into scope (EPIC-06); `Priority` corrected `P3`→`P2` in `backlog.md` at this document-touch | Satisfies the `2026-09-14__scheduled` rebalance's Skill-Silo mandatory-pull-forward directive — named as the sole genuine ungated build-and-ship U-item candidate; same escalation-recording pattern as `BLG-FEAT-32`/DL-078 | Release Planning Engine, per Product Owner's prior rebalance disposition | 2026-09-14 |
| `BLG-AI-06` selected into scope (EPIC-05) | Filed this session (AI Compliance & Governance Officer) as the concrete remediation for the `Deferred` `ESC-EXEC-20260910-01`; qualified on its own P2 priority and category-balanced round-robin position, not by special-casing | Release Planning Engine | 2026-09-14 |
| 6 data-quality-flagged items (`BLG-FEAT-73/74/76`, `BLG-SPEC-56/57`, `BLG-QA-59`) excluded from the ready pool | Embedded gate-like free text in `Provisional-Target` with no formal `Gate` field — semantically not ready despite the scripted gate-scan not hard-flagging them; consistent with how 3 of these 6 were already excluded at v9.3 | Release Planning Engine | 2026-09-14 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-06 (and `BLG-AI-05` within EPIC-05) flagged design-gate-triggering; `run design-gate` must pass before `plan sprint` can seal | 3 selected items carry an observable UI acceptance criterion — first design-gate-triggering release since v9.0 | Release Planning Engine | 2026-09-14 |
| Within EPIC-05, sequence `BLG-AI-06` and `BLG-AI-05` to avoid colliding on the same AI-response call sites if both touch a shared wrapper | Both items touch AI-generation code paths; avoid double-editing the same integration point in parallel | Release Planning Engine | 2026-09-14 |
| No cross-EPIC sequencing dependency otherwise — all 6 EPICs may proceed independently | No shared-file or shared-owner conflict identified across EPIC-01 through EPIC-06 beyond the EPIC-05 internal note above | Release Planning Engine | 2026-09-14 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations raised during this release-planning session; `ESC-EXEC-20260910-01` was dispositioned `Deferred` (not Accepted Risk — prohibited for its Strategy-boundary trigger type) in a prior session turn, outside this cycle's own record | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-09-14__release-v9.4
