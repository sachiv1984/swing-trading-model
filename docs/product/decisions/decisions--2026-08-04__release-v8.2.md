Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v8.2
Cycle: 2026-08-04__release-v8.2
Last Updated: 2026-08-05

Superseded by: v8.2 ship — 2026-08-05
Changelog: docs/product/changelog.md#v8.2
Cycle: 2026-08-04__release-v8.2

## Planning Decisions — v8.2 User-Feature Push (continued) & Full-Capacity Debt Clearance

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Lead scope with 5 user-facing/user-adjacent items (`BLG-FEAT-88`, `BLG-FE-105`, `BLG-FE-67`, `BLG-FE-138`, `BLG-FEAT-86`) | Exhaustive scan of all `BLG-FEAT-*`/`BLG-FE-*` candidates found these 5 genuinely ready and ungated — a materially larger pool than the single item found at each of the last two cycles; honours the explicit "focus on user features first" instruction | Product Owner | 2026-08-04 |
| Defer `BLG-FEAT-73`/`BLG-FEAT-74` and the Arc 5 UX-prep cluster for a 3rd consecutive cycle — Option (a), keep conditional | STEP 1.4a Perennial-Return Check mandates an explicit active disposition; no materially new gate-clearance path exists since `v8.1`'s assessment; per STEP 1.4a.1 this is the last cycle before the mandatory 4-consecutive sunset trigger | Product Owner | 2026-08-04 |
| Exclude `BLG-FEAT-45` from firm scope despite its 2026-08-05 gate date falling inside this cycle's execution window | STEP 1.4b (mandatory): within-sprint date gates may never be classified firm regardless of proximity | Product Owner | 2026-08-04 |
| Size scope to ~26.2 days midpoint, top of the confirmed ~24-28 day capacity band | Explicit user instruction this session: "Use full sprint capacity" | Product Owner | 2026-08-04 |
| Fill remaining capacity with a curated set of highest-priority ready (ungated) items — all P1/P2 ungated candidates plus 4 highest-value P3 QA/Spec/Backend debt items — rather than exhaustively padding to the exact ceiling | No further ungated user-facing scope exists beyond the 5 selected; filling capacity with genuinely valuable ready work is preferable both to leaving capacity unused and to indiscriminate low-value padding; 3 of the included items (`BLG-SEC-27`, `BLG-OPS-128`, `BLG-GOV-285`) already carried `Provisional-Target: v8.2` from their filing session | Product Owner | 2026-08-04 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Sequence `BLG-SEC-27` (staging API key rotation) before or alongside `BLG-OPS-128` (deploy-staleness detection) | Both touch staging environment configuration; uncoordinated sequencing risks a false-positive staleness reading during the key-rotation window | Product Owner | 2026-08-04 |
| EPIC-03's 11 items carry no cross-dependency and may execute in any order | Each is an independent governance-process document/checklist change with a distinct owner role | Product Owner | 2026-08-04 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations were raised this cycle (capacity outcome `pass`, no gate failures requiring risk acceptance) | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-08-04__release-v8.2
