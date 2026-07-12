Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v7.0
Cycle: 2026-07-12__release-v7.0
Last Updated: 2026-07-12

## Planning Decisions — v7.0 Positions Grid View Parity, Carryover Fixes & Feature Enhancements

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Maximise release scope to 15 stories / 3 EPICs (~9.5-10 estimated days) rather than the 2 named-mandatory pull-forwards alone | v6.9 used only ~4-6 of its ~12-14 day sprint capacity on 2 stories, incurring full governance overhead for minimal output; PO explicitly directed this release be maximised, and v6.9's own lessons-learnt carry-forward recommended surfacing capacity headroom as a question | Product Owner | 2026-07-12 |
| Favour ungated, product/bug-fix-value items over additional P3 governance/tooling backlog debt when filling capacity | Backlog carries an active 🔴 3rd-consecutive Product Value Alert (ratio 0.21, below the 0.30 floor); adding more governance/process debt items would worsen that ratio | Product Owner (delegated to Release Planning Engine) | 2026-07-12 |
| Include both named mandatory pull-forwards (`BLG-FE-102`, `BLG-FE-97`) as scope anchor | Named at the `2026-07-12__scheduled` rebalance's 3rd-consecutive Product Value Alert disposition | Product Owner (rebalance cycle) | 2026-07-12 |
| Deferred `BLG-FEAT-66`/`BLG-FEAT-67` (ungated, ready) to next release | Already-selected scope provides coherent, well-utilised capacity without them; not added purely to inflate story count | Product Owner (delegated to Release Planning Engine) | 2026-07-12 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 internal order: `BLG-SPEC-80` → `BLG-FE-102` → `BLG-FE-97` → `BLG-QA-95` → `BLG-FE-104` | Spec backfill should land before/alongside the fix it documents; Playwright parity coverage needs both badges rendered first; design review needs both badges rendered together | Head of Specs Team | 2026-07-12 |
| Design Gate required before Sprint Planning seals | 8 of 15 items carry observable UI acceptance criteria (RISK-04) | Head of Specs Team | 2026-07-12 |

### Accepted risks
None this cycle.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-12__release-v7.0
