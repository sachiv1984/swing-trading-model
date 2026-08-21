Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v8.9
Cycle: 2026-08-17__release-v8.9
Last Updated: 2026-08-21

Superseded by: v8.9 ship — 2026-08-21
Changelog: docs/product/changelog.md#v8.9
Cycle: 2026-08-17__release-v8.9

## Planning Decisions — v8.9 Live Risk-Management Correctness & Trade Intelligence Expansion

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Widen scope to full ~24–28 day capacity band rather than a tight P0-only or moderate P0+P2-only scope | 2 P0 anchor items alone (~2.25 days) left significant headroom against confirmed capacity; widening pulls in the fresh P2 product-feature pool plus a curated P3 debt/coverage tail rather than leaving capacity idle | Product Owner | 2026-08-17 |
| Exclude `BLG-FEAT-92` from this cycle's scope | Item's own text names an unresolved scope-overlap dependency on gated `BLG-FEAT-30` requiring explicit reconciliation before entering sprint planning — not a Release Planning decision to make unilaterally | Product Owner (via Release Planning Engine, applying the item's own stated precondition) | 2026-08-17 |
| Exclude `BLG-GOV-105` from this cycle's scope | Already ✅ CLOSED (confirmed duplicate, 2026-07-12); stale entry, not live scope | Release Planning Engine (data-quality exclusion, not a scope trade-off) | 2026-08-17 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| `BLG-BE-103` (ST-02) sequenced after `BLG-BE-102` (ST-01) within EPIC-01 | Both fixes touch the same position stop-value data path; fixing the currency-display bug alone would still surface a correctly-labeled but stale number until the underlying ratchet bug is also fixed (per `BLG-BE-103`'s own `Depends on` field) | Head of Specs Team (release plan authoring) | 2026-08-17 |
| Regression test (per `BLG-BE-102`'s own AC) required before any live-position backfill/recompute | An incorrect fix to the nightly-scheduled trailing-stop path could itself misprice a live stop; verify correctness before touching production data | Head of Specs Team (release plan authoring, RISK-01) | 2026-08-17 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations raised this cycle | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-08-17__release-v8.9
