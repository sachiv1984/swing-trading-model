Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.12
Cycle: 2026-10-12__release-v9.12
Last Updated: 2026-10-12

## Planning Decisions — v9.12

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Use full capacity: fill to 27.95 of the 28.00-day ceiling of the confirmed ~24–28 day band | Explicit user instruction: "plan release v9.12 - use full capacity." | Product Owner (direct user instruction) | 2026-10-12 |
| Seat `BLG-BE-162` at P1 (ST-01) | Committed to v9.12 by Product Owner direction (DL-085), as the condition of v9.11's verification P1 acceptance. It also seats mechanically as the only ready P1 item under §1.4c, so no override was needed. | Release Planning Engine (Product Owner role) | 2026-10-12 |
| Raise three effort estimates under the STEP 4 calibration check | `BLG-BE-162` (live migration plus staging verification, 0.5→1.0d), `BLG-SEC-41` (new table, 1.0→1.5d) and `BLG-OPS-182` (live staging divergence, XS→S). The raises changed the round-robin's final picks: `BLG-FE-210` seated in place of `BLG-FE-208`. | Release Planning Engine (Head of Specs Team role) | 2026-10-12 |
| Defer `BLG-TECH-21` (P2) despite P2-first ordering | Dedicated-release constraint in its own scope; `Provisional-Target: v10.0`. §1.4c override, as at v9.10 and v9.11. | Release Planning Engine (Product Owner role) | 2026-10-12 |
| Exclude `BLG-GOV-142`, `BLG-GOV-360`, `BLG-GOV-361`, `BLG-GOV-368` as done or resolved | Already-resolved banners or a met scope; left for `groom backlog`. | Release Planning Engine (Head of Specs Team role) | 2026-10-12 |
| Keep the 17 items with a literal `Gate criteria: None` out of the ready pool | Same treatment as prior cycles, which keeps pools comparable. Still tracked by `BLG-GOV-373` (unselected). | Release Planning Engine (Head of Specs Team role) | 2026-10-12 |
| Do not add an aged spec item over capacity | `BLG-SPEC-180`/`184`/`186`/`188` trip the §1.1 advisory. Seating one would displace a round-robin pick, which needs an explicit Product Owner override; none was given. Recommended for v9.13. | Release Planning Engine (Product Owner role) | 2026-10-12 |
| Restate stale, untestable or boundary-touching ACs | `BLG-BE-162`, `BLG-AI-10`, `BLG-AI-13`, `BLG-BE-159`, `BLG-BE-149`, `BLG-FE-202`, `BLG-BE-146`, `BLG-OPS-184`, `BLG-SEC-41`, `BLG-GOV-363`: Scope steps made testable. `BLG-BE-148`, `BLG-SPEC-182`: §13 clause citation (§13.3, §13.5) per the v2.61 rule. `BLG-GOV-369`: lint AC no longer waits on items already shipped. `BLG-FE-200`: both outcomes of its light-mode decision covered. `BLG-GOV-367`: the method-break note's home named as `roadmap_prompt.md` §7.1, not `decision_log.md`. `BLG-OPS-182`: dependency met. Each is marked *(restated)* in the slice. | Release Planning Engine (Head of Specs Team role) | 2026-10-12 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ST-01 leads EPIC-01 | P1 and the release anchor. | Head of Specs Team | 2026-10-12 |
| ST-23's light-mode decision before the sprint planning seal | The decision changes the largest story's work (RISK-03). | Head of Specs Team | 2026-10-12 |
| ST-16 (EPIC-02) and ST-20/ST-21 (EPIC-03) before ST-26 (EPIC-04) | All three EPICs edit the Settings path (RISK-05). | Head of Specs Team | 2026-10-12 |
| ST-39 first in EPIC-06; governance prompt bumps (ST-40 → ST-41 → ST-42 → ST-43) sequential on one branch | ST-39 closes the merge-splice gap other EPICs' merges depend on (RISK-07). Sequential bumps avoid the same-version collisions CLAUDE.md §8 step 2a guards against. | Head of Specs Team | 2026-10-12 |
| ST-17 → ST-18 → ST-19 on Trade Entry | The Playwright coverage in ST-19 should test the changed page. | Head of Specs Team | 2026-10-12 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
