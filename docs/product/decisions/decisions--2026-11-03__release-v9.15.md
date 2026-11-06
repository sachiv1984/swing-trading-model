Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.15
Cycle: 2026-11-03__release-v9.15
Last Updated: 2026-11-06

Superseded by: v9.15 ship — 2026-11-06
Changelog: docs/product/changelog.md#v9.15
Verification report: claude/cycles/2026-11-03__release-v9.15/verification_report.md
Cycle: 2026-11-03__release-v9.15

## Planning Decisions — v9.15

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Use full capacity: fill to 28.00 of the 28.00-day ceiling of the confirmed ~24–28 day band | Explicit user instruction: "plan release v9.15 use full capacity". | Product Owner (direct user instruction) | 2026-11-03 |
| Seat all 10 items committed to v9.15 by DL-088, first | Roadmap rebalance `2026-11-03__scheduled` commits them to this release. They include both ready P1 items: `BLG-FE-244` (pre-entry checks on every route into Trade Entry) and `BLG-FE-245` (live FX pre-fill), Correctness Fast-Track promotions. | Release Planning Engine (Product Owner role), per DL-088 | 2026-11-03 |
| Hold the ungated Site Structure & Usability Phase 2/3 items to v9.16/v9.17 (§1.4c override) | DL-088 calls the later phases provisional, so §1.4c's P2-first step would have seated `BLG-FE-255`, `256`, `260` and `264` (8.5d). The Product Owner chose to keep the programme's phasing, so Phase 2 builds from this release's specs. The override also covers their P3 siblings (`BLG-FE-253`, `257`, `259`, `261`, `262`, `263`). The 10 items total 20.00d. | Product Owner (user decision in session) | 2026-11-03 |
| Seat `BLG-FE-239`, `BLG-FE-240`, `BLG-FE-243` | The three accepted v9.14 P2 found defects (closure Carry-Forward #2). All are ready P2, so the P2-first step seats them. | Release Planning Engine (Product Owner role) | 2026-11-03 |
| Seat `BLG-GOV-404` and `BLG-QA-240` under §1.4c step 1a | v9.14's deferred lessons-learnt script patches, both targeted at v9.15 (closure §6 row 3, `ESC-CLOSE-20261103-02` option (a)). This is the first use of step 1a. | Release Planning Engine (Head of Specs Team role) | 2026-11-03 |
| Clear `BLG-OPS-48`'s gate (§1.3a date-lapsed, option (a)) | The whole condition is met: the gating item `BLG-OPS-36` shipped at v4.2, and the gate's only other limb, "no earlier than 2026-11-01", has passed. A bounded edit under `ESC-CLOSE-20261007-01`. The item is then seated as a ready P2. | Release Planning Engine (Head of Specs Team role) | 2026-11-03 |
| Exclude `BLG-GOV-185` and `BLG-GOV-192` as already met | `BLG-GOV-185`: its AC is met by `metrics_definitions.md` Appendix D (Change Log), the reason v9.14 deferred it at planning (ST-51), but it was never bannered. `BLG-GOV-192`: its proposed every-3-cycle §14 drift check has been in `run audit` since 2026-03-13, before the item was filed, and AUD-2026-11-03 ran it (TABLE 3). Both were first selected by the round-robin, then removed on reading, and the selection was rerun. Left for `groom backlog` to archive. | Release Planning Engine (Head of Specs Team role) | 2026-11-03 |
| Exclude `BLG-GOV-178` and `BLG-GOV-400`; record `BLG-GOV-400`'s evidence | `BLG-GOV-178`'s remaining scope is `BLG-GOV-399` (v9.14 closure §6 row 4). `BLG-GOV-400`'s check runs in this run (see `run_manifest.md`): no item whose whole gate is a shipped item is re-listed without a named reason. | Release Planning Engine (Head of Specs Team role) | 2026-11-03 |
| Defer `BLG-TECH-21` (P2) despite P2-first ordering | Dedicated-release constraint in its own scope; `Provisional-Target: v10.0`. Standing §1.4c override, as at v9.10–v9.14. | Release Planning Engine (Product Owner role) | 2026-11-03 |
| Classify `BLG-OPS-197` as conditional (§1.4b); treat `BLG-OPS-195` as not ready | `BLG-OPS-197` needs 7 days of production data after v9.14 EPIC-05 deployed (merged 2026-11-02), so its earliest clear date is 2026-11-09, inside the sprint. `BLG-OPS-195` alerts against the §4 baseline that only `BLG-OPS-197` fills (it reads "Pending"), so it is not ready while that item is unshipped. | Release Planning Engine (PMO Lead role) | 2026-11-03 |
| Apply the STEP 4 calibration to the whole pool before selection | 6 raises, +2.70d (v9.14 precedents, plus `BLG-OPS-205`'s seed sweep and staging write). 2 are seated (`BLG-SPEC-196`, `BLG-SPEC-197`). `BLG-FE-243` and `BLG-FE-246` are held, with counts named. | Release Planning Engine (Head of Specs Team role) | 2026-11-03 |
| Restate missing, stale or out-of-slice ACs | No AC: `BLG-GOV-193`, `BLG-GOV-194`, `BLG-GOV-195`, `BLG-GOV-196`. §13 citations: `BLG-SPEC-216`, `BLG-GOV-194`. Stale endpoint list: `BLG-OPS-48`. "Above" pointing at the source Problem: `BLG-AI-24`, `BLG-AI-25`, `BLG-AI-26`, `BLG-GOV-404`. Post-merge markers: `BLG-OPS-197`, `BLG-SPEC-196`. Each is marked *(restated)* in the slice. | Release Planning Engine (Head of Specs Team role) | 2026-11-03 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ST-01 and ST-02 lead EPIC-01; ST-03 after ST-02 | P1 correctness on the Trade Entry page. ST-03 relabels the FX field that ST-02 changes. | Head of Specs Team | 2026-11-03 |
| ST-08 first in EPIC-02; ST-11 after ST-08 is approved | `BLG-FE-248` takes its labels from `BLG-SPEC-214`'s glossary section. | Head of Specs Team | 2026-11-03 |
| ST-16 (EPIC-03) before ST-12 (EPIC-02) | `BLG-FE-247` must confirm that `BLG-FE-240`'s fix lands on `DashboardHome`, not the legacy page it removes. | Head of Specs Team | 2026-11-03 |
| ST-25 → ST-27 | One AI Compliance & Governance Officer ruling can cover both journal-summary check changes. | Head of Specs Team | 2026-11-03 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
