Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.17
Cycle: 2026-11-11__release-v9.17
Last Updated: 2026-11-11

## Planning Decisions — v9.17

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Use full capacity: fill to 27.95 of the 28.00-day ceiling of the confirmed ~24–28 day band | Explicit user instruction: "plan release v9.17 use full capacity". 0.05d was left, and no remaining item fits (the smallest is 0.15d). | Product Owner (direct user instruction) | 2026-11-11 |
| Seat the five accepted v9.16 P2 found defects | `BLG-BE-211`, `BLG-FE-278`, `BLG-FE-281`, `BLG-FE-282`, `BLG-OPS-217`. v9.16 Carry-Forward #1. The P2 tier seats all five in ascending ID order, so no dated reason to leave one out is needed. | Release Planning Engine (Product Owner role) | 2026-11-11 |
| Seat `BLG-FE-260` (Phase 3, P2) in the P2 tier | Phase 3's provisional release is v9.17, so §1.4c step 0 no longer holds it. | Release Planning Engine (Head of Specs Team role) | 2026-11-11 |
| Seat Phase 3's 7 P3 items and `BLG-BE-205` under §1.4c step 1b | First use of `ESC-CLOSE-20261111-01`'s ruling (v2.74). `BLG-FE-257`, `258`, `259`, `261`, `262`, `263`, `265` are listed in Phase 3. `BLG-BE-205` is named in the Phase 2 row, and Phase 2 is unfinished while `BLG-FE-254` waits on it ("items in an earlier, unfinished phase qualify too"). 19.50d. No Product Owner override was needed, unlike v9.16. | Release Planning Engine (Head of Specs Team role), per `release_planning_prompt.md` §1.4c step 1b | 2026-11-11 |
| Seat `BLG-FE-254`'s remainder only, at 0.5 days | v9.16 ST-06 shipped every Today list AC except TL-09/TL-10, which wait on `BLG-BE-205` (closure §6 row 3; Carry-Forward #4). The item's own L estimate covered the whole list. The remainder is two Playwright ACs and the group's render. | Release Planning Engine (Head of Specs Team role) | 2026-11-11 |
| Seat `BLG-GOV-419` under §1.4c step 1a | v9.16's deferred lessons-learnt patch (`LL-v9.16-Release-03`), targeted at v9.17. | Release Planning Engine (Head of Specs Team role) | 2026-11-11 |
| Round-robin: `BLG-BE-178`, `BLG-QA-223`, `BLG-OPS-195`, `BLG-SPEC-202` | One pass of the category-balanced, oldest-first round-robin filled the last 1.40d. `BLG-OPS-195`'s dependency is now met (`data_pipeline_cost_baseline.md` §4 recorded 2026-11-11). | Release Planning Engine (PMO Lead role) | 2026-11-11 |
| Exclude 8 ungated items as not ready | `BLG-FEAT-73` (re-check needs a production read), `BLG-FEAT-76` (blocked on `BLG-FEAT-73`), `BLG-TECH-21` (standing override), `BLG-GOV-178` (remainder is `BLG-GOV-399`), `BLG-GOV-200`/`201` (no ACs, closure §6 row 5), `BLG-GOV-408` (a `run roadmap` input), `BLG-OPS-201` (not before 2026-12-01). | Release Planning Engine (Head of Specs Team role) | 2026-11-11 |
| Clear no gates | 0 date-lapsed items; all 14 gating-item-shipped items keep an unmet limb (each read; same 14 as v9.16). | Release Planning Engine (Head of Specs Team role) | 2026-11-11 |
| Apply the STEP 4 calibration to the whole pool before selection | 9 raises, +4.35d. Three new: `BLG-BE-211` (backfill, seated), `BLG-OPS-217` (production diagnosis, seated), `BLG-BE-210` (production count and migration). Six carried, one seated (`BLG-BE-205`). `BLG-FE-265` held at L with its count named. | Release Planning Engine (Head of Specs Team role) | 2026-11-11 |
| Restate ACs | `BLG-FE-254` (remainder TL-09/TL-10), `BLG-FE-259` (KPI confirmation recorded), `BLG-FE-282` (close `DEV-v9.16-ST27-01`), `BLG-OPS-217` and `BLG-GOV-419` (post-merge markers). Each is marked *(restated)* or *(post-merge)* in the slice. | Release Planning Engine (Head of Specs Team role) | 2026-11-11 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ST-01 first in EPIC-01; ST-02, ST-03 after it; ST-04 last | All four rewrite `Positions.js`. ST-02 reuses ST-01's urgency order; ST-04 changes the grace entry ST-03 builds. | Head of Specs Team | 2026-11-11 |
| ST-05 and ST-06 merge one after the other | Both add redirects and change `navigation.md` v2's areas and the command palette. | Head of Specs Team | 2026-11-11 |
| EPIC-03 merges last | ST-08 sweeps colour classes across every page and regenerates both themes' visual baselines. | Head of Specs Team | 2026-11-11 |
| ST-09 → ST-10 | TL-09/TL-10 need `stop_last_moved_date` and `previous_stop`. | Head of Specs Team | 2026-11-11 |
| ST-15 → ST-16 | The 2× alert should compare against post-fix failure counts where available. | Head of Specs Team | 2026-11-11 |
| ST-12 and ST-19 decisions before the build | Each needs the Strategy Rules & System Intent Owner's choice (RISK-05). | Head of Specs Team | 2026-11-11 |

### Accepted risks

None. No escalation was raised this run.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-11-11__release-v9.17
