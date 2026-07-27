Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v7.8
Cycle: 2026-07-24__release-v7.8
Last Updated: 2026-07-27

Superseded by: v7.8 ship — 2026-07-27
Changelog: docs/product/changelog.md#v7.8
Cycle: 2026-07-24__release-v7.8

## Planning Decisions — v7.8 Release Visibility & Engineering Hardening

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Scope v7.8 around 12 ungated items drawn from the `IW-20260724-01` idea-intake backlog addition (34 standalone items), rather than waiting for a formally roadmap-named anchor set. | `2026-07-24__scheduled` rebalance's own STEP 8.1 Option (b) rationale explicitly named this path: "let `plan release` make that call... scope a release around ungated backlog items." No P0/P1 production-correctness items existed to fast-track (STEP 8.0 found 0 this rebalance). | Product Owner | 2026-07-24 |
| Selection favoured P2 items and user-facing/accessibility value (`BLG-FE-128`, `BLG-FEAT-84`, `BLG-FE-127`, `BLG-FE-125`, `BLG-FEAT-81`, `BLG-FEAT-82`) alongside security/engineering hardening (`BLG-SEC-20/21`, `BLG-BE-71`, `BLG-QA-117/119`, `BLG-OPS-117`). | Product Value Ratio remains Advisory (0.42, improving from 0.39 but below the healthy band) per `2026-07-24__scheduled` rebalance — favouring user-facing items this cycle supports continued improvement without abandoning overdue engineering hardening. | Product Owner | 2026-07-24 |
| `BLG-FEAT-73` and `BLG-FEAT-74` excluded from v7.8 scope; PO disposition Option (b) — remove from horizon (per STEP 1.4a Perennial-Return Check, 2nd consecutive return for both). | SI-02 gate (`BLG-FEAT-73`) remains NOT MET with no new evidence; `BLG-FEAT-74` has never had §13 pre-clearance and its VH effort exceeds single-cycle sizing regardless. Continuing to re-list either as "conditional" each cycle with no changed facts is exactly the backlog-churn pattern STEP 1.4a exists to prevent. | Product Owner | 2026-07-24 |
| `BLG-QA-122` excluded (not "deferred" in the perennial-return sense) — gate-conditional at the item level, no broker import mechanism exists yet. | Item's own gate criteria unmet; not eligible for scope entry regardless of return count. | Product Owner | 2026-07-24 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| UI-facing EPICs (EPIC-01, 03, 04, 05, 06) sequenced after Design Gate pass; all other EPICs (02, 07–12) may execute in parallel with no cross-dependency. | 5 of 12 items carry observable UI acceptance criteria (visible rendering, contrast, interaction) — `CLAUDE.md` §2 Playwright/staging-sign-off requirement applies; Design Gate is the standing hard prerequisite before Sprint Planning seals per `design_gate_prompt.md`. | Product Owner / Head of Specs Team | 2026-07-24 |
| EPIC-09 (`BLG-BE-71` retry/backoff decorator) scoped to proof-of-pattern on the single highest-traffic external call site only, not a full retrofit. | Matches the backlog item's own Acceptance Criteria; bounds regression risk (RISK-02) on a shared decorator touching live Yahoo Finance/Alpaca call paths. | Product Owner | 2026-07-24 |

### Accepted risks
None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-24__release-v7.8
