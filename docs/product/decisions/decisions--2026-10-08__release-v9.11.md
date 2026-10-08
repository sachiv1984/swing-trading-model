Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.11
Cycle: 2026-10-08__release-v9.11
Last Updated: 2026-10-08

## Planning Decisions — v9.11

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Run a scheduled roadmap rebalance before planning v9.11, with a reduced-roster idea window | §-1.2 halted: no `v9.11` roadmap section, and the only Option (b) record was used up by v9.10 (`ESC-CLOSE-20260928-02`). The user directed "do what is needed to make this work" and chose a 4-role user-facing idea window over a full 22-role one. | Product Owner (direct user instruction) | 2026-10-08 |
| Use full capacity: fill to 27.975 of the 28.00-day ceiling of the confirmed ~24–28 day band | Explicit user instruction: "plan release v9.11 use full capacity." | Product Owner (direct user instruction) | 2026-10-08 |
| Seat the four roadmap-committed v9.11 items: `BLG-BE-152` (ST-01), `BLG-BE-150` (ST-02), `BLG-BE-154` (ST-10), `BLG-FE-206` (ST-11) | Committed by rebalance `2026-10-08__scheduled` (DL-084). All four also seat mechanically under §1.4c's P1-then-P2 ordering, so no override was needed. | Release Planning Engine (Product Owner role) | 2026-10-08 |
| Re-gate the 6 date-lapsed items in place on their same conditions | First use of §7's gate-field carve-out (`ESC-CLOSE-20261007-01`). Two were satisfied-limb restatements (`BLG-FEAT-55`, `BLG-SPEC-65`). Four were false-positive dates (`BLG-GOV-121`, `BLG-FEAT-62`, `BLG-OPS-53`, `BLG-FEAT-92`). No condition was loosened, tightened or replaced, and no AC was edited. | Release Planning Engine (Head of Specs Team role) | 2026-10-08 |
| Treat `BLG-OPS-179` as ready; exclude `BLG-FE-195` as delivered | Both were gated on `BLG-BE-138`, which shipped in v9.10 with ruling (a). `BLG-FE-195`'s scope (§11 defaults, read-only panel) shipped with v9.10 ST-01; its remaining helper-text half is `BLG-FE-201`. | Release Planning Engine (Head of Specs Team role) | 2026-10-08 |
| Exclude `BLG-GOV-361` as met in-run | The `BLG-SPEC-65` re-gate is exactly its scope. | Release Planning Engine (Head of Specs Team role) | 2026-10-08 |
| Defer `BLG-TECH-21` (P2) despite P2-first ordering | Dedicated-release constraint in its own scope; `Provisional-Target: v10.0`. §1.4c override. | Release Planning Engine (Product Owner role) | 2026-10-08 |
| Keep the 17 items with a literal `Gate criteria: None` out of the ready pool | Same treatment as prior cycles, which keeps pools comparable. Still tracked by `BLG-GOV-373` (unselected). | Release Planning Engine (Head of Specs Team role) | 2026-10-08 |
| Restate stale or boundary-touching ACs | `BLG-FEAT-59`/`60`, `BLG-FE-84`, `BLG-FEAT-63`: gate ACs satisfied by the 2026-10-05 PO removal. `BLG-SPEC-174`: it targeted a removed gate. `BLG-GOV-366`, `BLG-BE-153`: they would edit existing backlog items. `BLG-FEAT-59`: §13 confirmation made testable. `BLG-FR-06`: migration home. `BLG-BE-150`: follow-up IDs mapped. Each is marked *(restated)* in the slice. | Release Planning Engine (Head of Specs Team role) | 2026-10-08 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 leads; ST-01's Condition 2 sign-off is its first sub-step | ST-01 is the P1 Correctness Fast-Track item. The sign-off decides what the prompt may carry. | Head of Specs Team | 2026-10-08 |
| ST-10 first in EPIC-02, then ST-11 and ST-13 | All three change `GET /portfolio` or the Position Risk table. ST-10 adds the first new field. | Head of Specs Team | 2026-10-08 |
| ST-23 (cost) and ST-24 (engagement metric) before ST-25 (AI narrative); ST-26 after ST-25 | Cost and the measurement baseline should exist before the feature (the `BLG-GOV-366` recommendation). | Head of Specs Team | 2026-10-08 |
| ST-16's grace ruling before ST-17 | The recorded parameter source may depend on it. | Head of Specs Team | 2026-10-08 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
