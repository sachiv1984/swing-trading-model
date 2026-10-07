Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.10
Cycle: 2026-10-06__release-v9.10
Last Updated: 2026-10-07

Superseded by: v9.10 ship — 2026-10-07 — see docs/product/changelog.md#v9.10, cycle 2026-10-06__release-v9.10

## Planning Decisions — v9.10

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Use full capacity: fill to 27.90 of the 28.00-day ceiling of the confirmed ~24–28 day band | Explicit user instruction: "plan release v9.10 use full capacity." | Product Owner (direct user instruction) | 2026-10-06 |
| Seat the three roadmap-committed v9.10 items: `BLG-BE-138` (ST-01), `BLG-FE-193` (ST-06), `BLG-FE-198` (ST-08) | Committed by rebalance `2026-10-06__scheduled` (DL-083). All three also seat mechanically under §1.4c's P1-then-P2 ordering, so no override was needed. | Release Planning Engine (Product Owner role) | 2026-10-06 |
| Treat `BLG-FE-193` and `BLG-OPS-92` as ready (date-lapsed gates whose conditions are met) | `BLG-FE-193`: `BLG-BE-135` shipped v9.9, and the gate text already says met. `BLG-OPS-92`: quarterly cadence date (~2026-10-06) reached, and a new advisory signal surfaced (issue #1885). | Release Planning Engine (Head of Specs Team role) | 2026-10-06 |
| Defer `BLG-TECH-21` (P2) despite P2-first ordering | Its own scope requires a dedicated single-EPIC release (scoping document §6), and it carries `Provisional-Target: v10.0`. Recorded as a §1.4c override. | Release Planning Engine (Product Owner role) | 2026-10-06 |
| Do not seat `BLG-GOV-368`, `BLG-GOV-142` or `BLG-GOV-360` | Already done or resolved (v9.9 closure carry-forward item 3; ST-19/ST-20 resolution banners). Re-seating would re-plan finished work. | Release Planning Engine (Head of Specs Team role) | 2026-10-06 |
| Keep the 17 items with a literal `Gate criteria: None` out of the ready pool | Same treatment as prior cycles, which keeps pools comparable. Flagged for correction (`lessons_learnt.md` Friction Item 1). | Release Planning Engine (Head of Specs Team role) | 2026-10-06 |
| Restate stale ACs in the slice for `BLG-GOV-140`/`141` (past 2026-09-24 dates) and `BLG-FE-193` (satisfied dependency AC); point `BLG-GOV-357`'s output at `docs/ops/` | These ACs could not be met as written, or would touch the `ESC-CLOSE-20261006-01` boundary. Each restatement is marked *(restated)* in `stage4_backlog_slice.md`. | Release Planning Engine (Head of Specs Team role) | 2026-10-06 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (stop-parameter correctness) leads, and ST-01's parameter-authority ruling is the release's first sub-step | ST-01 is the P1 Correctness Fast-Track item. Its ruling decides the parameter source that ST-03 (contract text), ST-06 (displayed multiplier) and ST-07 (Trade Entry fallback) depend on. | Head of Specs Team | 2026-10-06 |
| ST-13 (gap-risk §13.3 ruling) precedes ST-14 (gap-risk rework); ST-11 (lifecycle ruling) ideally precedes ST-12's post-grace work | Each ruling item's output is folded into the paired build item. | Head of Specs Team | 2026-10-06 |
| ST-08 before ST-09 | Both need the same "post-grace stop breach or risk-off" predicate. Build it once. | Head of Specs Team | 2026-10-06 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: v9.10 ship — 2026-10-07
Changelog: docs/product/changelog.md#v9.10
Cycle: 2026-10-06__release-v9.10
