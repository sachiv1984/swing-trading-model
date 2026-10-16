Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.13
Cycle: 2026-10-16__release-v9.13
Last Updated: 2026-10-16

## Planning Decisions — v9.13

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Use full capacity: fill to 28.00 of the 28.00-day ceiling of the confirmed ~24–28 day band | Explicit user instruction: "plan release v9.13 use full capacity." | Product Owner (direct user instruction) | 2026-10-16 |
| Seat the three roadmap-committed items: `BLG-FE-226` (P1, ST-01), `BLG-FE-227` and `BLG-BE-182` (P2, ST-03, ST-04) | Committed to v9.13 by rebalance `2026-10-16__scheduled` (DL-086): STEP 8.0 Correctness Fast-Track and the §7.1 sustained-failure pull-forward. All three also seat mechanically in §1.4c's P1 and P2 passes, so no override was needed. | Release Planning Engine (Product Owner role) | 2026-10-16 |
| Treat 5 Ops items as ungated because their only gate is a shipped item | First run of the §1.3a gating-item-shipped check (ST-40, v9.12). `BLG-OPS-18`/`-19` (`BLG-OPS-17`, v9.3), `BLG-OPS-23` (`BLG-OPS-13`, v8.8), `BLG-OPS-77` (`BLG-OPS-71`, v6.8), `BLG-OPS-85` (`BLG-OPS-74`, v6.8). No gate text was edited; that goes to `groom backlog`. The other 20 listed items keep an unmet limb or are delivered (`BLG-FE-195`). | Release Planning Engine (Head of Specs Team role) | 2026-10-16 |
| Raise 8 effort estimates under the STEP 4 calibration check, before selection | Live migrations, a live backfill, a Render dashboard step and a 59-call sweep (see `release_plan.md` Capacity Check). The raises seated `BLG-GOV-387` in place of `BLG-BE-164`. | Release Planning Engine (Head of Specs Team role) | 2026-10-16 |
| Defer `BLG-TECH-21` (P2) despite P2-first ordering | Dedicated-release constraint in its own scope; `Provisional-Target: v10.0`. §1.4c override, as at v9.10–v9.12. | Release Planning Engine (Product Owner role) | 2026-10-16 |
| Exclude `BLG-GOV-142`, `BLG-GOV-360`, `BLG-SPEC-199`, `BLG-GOV-368`, `BLG-GOV-361`, `BLG-GOV-374` as done or resolved | Resolution banners, a ✅ COMPLETE banner, a met scope, or delivered by the 2026-10-16 action-now patch (`ready_pool_history.md`, `roadmap_prompt.md` v9.35). Left for `groom backlog`. | Release Planning Engine (Head of Specs Team role) | 2026-10-16 |
| Keep the 17 items with a literal `Gate criteria: None` out of the ready pool | Same treatment as prior cycles, which keeps pools comparable. `BLG-GOV-390` (ST-35) fixes the scan in this release. | Release Planning Engine (Head of Specs Team role) | 2026-10-16 |
| Restate stale, untestable or out-of-release-dependent ACs | `BLG-SPEC-186`, `BLG-GOV-391`, `BLG-AI-18`: Scope steps made testable. `BLG-QA-228`: its AC waited on the unseated `BLG-FE-230`. `BLG-QA-227`: exposed defects filed, not fixed in-story. `BLG-OPS-18`/`-19`/`-23`: gate checks moved to Release Planning. `BLG-GOV-373`: tested by fixture (empty date-lapsed list). Each is marked *(restated)* in the slice. | Release Planning Engine (Head of Specs Team role) | 2026-10-16 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ST-01 leads EPIC-01, then ST-02 → ST-03 | P1 anchor. ST-03's module takes each reason's §8 category from ST-02. | Head of Specs Team | 2026-10-16 |
| ST-23 and ST-24 (EPIC-04) after ST-01 (EPIC-01) | Both checks fail while `PATCH /positions/{id}` is still called. | Head of Specs Team | 2026-10-16 |
| RISK-02's `strategy_rules.md` route decided before the sprint planning seal | Up to five stories in three EPICs may write a file Sprint Execution may not write without authorisation. | Head of Specs Team | 2026-10-16 |
| ST-35 → ST-36; ST-38 → ST-39 | Same script; one `strategy_rules.md` version bump. | Head of Specs Team | 2026-10-16 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
