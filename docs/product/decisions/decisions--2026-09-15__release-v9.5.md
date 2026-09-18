Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.5
Cycle: 2026-09-15__release-v9.5
Last Updated: 2026-09-18

Superseded by: v9.5 ship — 2026-09-18
Changelog: docs/product/changelog.md#v95
Cycle: 2026-09-15__release-v9.5

## Planning Decisions — v9.5 Full-Capacity Debt Clearance III

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Selected a 43-item / 27.99-day subset from the 62-item / ~43.79-day ungated ready pool via the codified §1.4c method: P1 items first, then P2 items (ascending ID), then category-balanced round-robin oldest-first for the remaining P3/P4 | Full-capacity instruction; first citable application of §1.4c since it was codified at v9.4 post-ship closure; extended to seat ready P1 items ahead of P2 (§1.4c's text did not anticipate a ready P1 item existing) | Release Planning Engine (Head of Specs Team authority) | 2026-09-15 |
| `BLG-SPEC-56`, `BLG-SPEC-57`, `BLG-QA-59` re-included in the ready pool and selected into scope, reversing v9.3/v9.4's exclusion of these 3 items | Direct re-read found each item describes legitimate pre-authoring work performable ahead of the PO-02 gate, not work blocked by it — the scripted gate-scan's own docstring confirms a data-quality warning "does not mark the item gated" | Release Planning Engine | 2026-09-15 |
| `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76` excluded from the ready pool | Each explicitly states in its own body text that it may not enter sprint planning yet (unmet re-check condition or unrun §13 pre-clearance), despite carrying no formal `Gate` field | Release Planning Engine | 2026-09-15 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| `ST-01` (`BLG-BE-117`) sequenced first within EPIC-01, and recommended first across the whole cycle | It is CI-blocking on every open and future PR — every other story's own PR inherits the red CI state until this lands | Release Planning Engine | 2026-09-15 |
| EPIC-06 (all 4 items) flagged design-gate-triggering; `run design-gate` must pass before `plan sprint` can seal | All 4 selected items carry an observable UI acceptance criterion or UI-shipping Scope text | Release Planning Engine | 2026-09-15 |
| Within EPIC-05, sequence `ST-37` (`BLG-GOV-322`) and `ST-38` (`BLG-GOV-323`) rather than editing `workforce_capacity.md` in parallel commits | Both items add new sections to the same shared file in the same cycle | Release Planning Engine | 2026-09-15 |
| No cross-EPIC sequencing dependency otherwise — all 6 EPICs may proceed independently | No shared-file or shared-owner conflict identified across EPIC-01 through EPIC-06 beyond the two notes above | Release Planning Engine | 2026-09-15 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations raised during this release-planning session | — | — |

### Supersession note

Superseded by: v9.5 ship — 2026-09-18
Changelog: docs/product/changelog.md#v95
Cycle: 2026-09-15__release-v9.5
