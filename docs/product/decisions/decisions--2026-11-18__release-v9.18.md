Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.18
Cycle: 2026-11-18__release-v9.18
Last Updated: 2026-11-18 (created)

## Planning Decisions — v9.18

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Use full capacity: fill to 27.95 of the 28.00-day ceiling of the confirmed ~24–28 day band | Explicit user instruction: "plan release v9.18 use full capacity". 0.05d was left, and no remaining item fits (the smallest is 0.15d). | Product Owner (direct user instruction) | 2026-11-18 |
| Seat all 12 ready P2 items | `BLG-BE-208`, `BLG-BE-213`, `BLG-BE-223`, `BLG-FE-294`, `BLG-FE-311`, `BLG-FE-312`, `BLG-GOV-420`, `BLG-GOV-421`, `BLG-GOV-422`, `BLG-OPS-217` (remainder), `BLG-QA-262`, `BLG-SEC-46`. §1.4c step 1 in ascending ID order. Includes v9.17 Carry-Forward #1's two P2 items and #2's `BLG-FE-294`. | Release Planning Engine (Product Owner role) | 2026-11-18 |
| Hold Phase 4 stages 3–4 (20 items, 16.25d) | §1.4c step 0: their provisional release in the DL-089 programme plan is v9.19. | Release Planning Engine (Head of Specs Team role) | 2026-11-18 |
| Seat Phase 4 stages 1–2's 12 P3 items under §1.4c step 1b | `BLG-FE-308`, `318`, `320`, `323`, `BLG-FEAT-103`, `BLG-QA-271`, `BLG-UX-11`, `12`, `13`, `15`, `19`, `21`; 11.90d. Stages 1–2's provisional release is v9.18. | Release Planning Engine (Head of Specs Team role), per `release_planning_prompt.md` §1.4c step 1b | 2026-11-18 |
| Seat `BLG-QA-268` and `BLG-OPS-220` under §1.4c step 1a | `BLG-QA-268` tracks `LL-v9.17-P3-01` (b), targeted at v9.18. `BLG-OPS-220` tracks `LL-v9.17-P3-03`, assigned to "v9.18 Release Planning" by v9.17's closure, but its own `Source`/`Provisional-Target` were not set to match; seated by the rule's purpose, for the Product Owner to confirm. | Release Planning Engine (Head of Specs Team role) | 2026-11-18 |
| Seat `BLG-QA-260` (P3) by override | Product Owner direction of 2026-11-12 (with `BLG-GOV-422` and `BLG-QA-262`), committed in the roadmap's v9.18 section (DL-089). §1.4c has no tier for it, so it is recorded as an override. | Product Owner (direction 2026-11-12; recorded by Release Planning) | 2026-11-18 |
| Extend `BLG-GOV-422`'s ACs | Product Owner scope extension of 2026-11-13 (v9.17 `execution_state.json` process_note, `a207af77`): writer check, time-boundary worked examples, dry run on `dashboard.md` v4.0 §1B. Restated in the slice; effort 0.5d → 0.75d. | Product Owner (direction 2026-11-13); Head of Specs Team | 2026-11-18 |
| Seat `BLG-OPS-217`'s remainder only, at 0.25 days, as conditional | AC 1 met in v9.17 ST-15; AC 2–3 need a post-fix production weekly report, not before 2026-11-20 (PR #2259 merged 2026-11-13T15:11:51Z). §1.4b: within-sprint date gate → conditional. | Release Planning Engine (Head of Specs Team role) | 2026-11-18 |
| Round-robin: 13 items, 5.70d | Two passes of the category-balanced, oldest-first round-robin: `BLG-BE-179`, `BLG-QA-225`, `BLG-OPS-205`, `BLG-SPEC-203`, `BLG-GOV-378`, `BLG-FE-225`, `BLG-AI-29`, `BLG-BE-181`, `BLG-QA-226`, `BLG-OPS-206`, `BLG-SPEC-204`, `BLG-GOV-388`, `BLG-FE-228`. | Release Planning Engine (PMO Lead role) | 2026-11-18 |
| Exclude 9 ungated items as not ready | `BLG-FEAT-73` (re-check needs a production read), `BLG-FEAT-76` (blocked on `BLG-FEAT-73`), `BLG-TECH-21` (standing override), `BLG-GOV-178` (remainder is `BLG-GOV-399`), `BLG-GOV-200`/`201` (no ACs), `BLG-GOV-408` (✅ COMPLETE), `BLG-GOV-419` (remainder needs a gate clearance), `BLG-OPS-201` (not before 2026-12-01). | Release Planning Engine (Head of Specs Team role) | 2026-11-18 |
| Clear no gates | 0 date-lapsed items; all 13 gating-item-shipped items keep an unmet limb (each read). | Release Planning Engine (Head of Specs Team role) | 2026-11-18 |
| Apply the STEP 4 calibration to the whole pool before selection | 9 raises, +5.35d. Seated: `BLG-BE-223` (M → L, price-consumer sweep), `BLG-GOV-422` (PO extension), `BLG-SPEC-203` (staging verification), `BLG-OPS-205` (carried). Five carried on unselected items. | Release Planning Engine (Head of Specs Team role) | 2026-11-18 |
| Restate ACs | `BLG-UX-21` (decision half met by DL-089), `BLG-UX-12` (link target if ST-14 relabels the figure), `BLG-GOV-422` (PO extension), `BLG-QA-268` (v9.17 commit references), `BLG-BE-223` (rule approval first), `BLG-OPS-217` (remainder), `BLG-AI-29` and `BLG-GOV-378` (§13 clause citations). Each is marked *(restated)* in the slice. | Release Planning Engine (Head of Specs Team role) | 2026-11-18 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ST-07 first in EPIC-02 | `navigation.md` and `design_system.md` revisions govern ST-08's moves and the Dashboard builds. | Head of Specs Team | 2026-11-18 |
| ST-09 → ST-10 → ST-11 | All three change `dashboard.md` and the Dashboard cards and baselines. | Head of Specs Team | 2026-11-18 |
| ST-14 → ST-15 + ST-16 → ST-17 | ST-14 renames the field the rewrite lays out and links; ST-17 adds a section to the rewritten page. | Head of Specs Team | 2026-11-18 |
| ST-18 early in the sprint | v9.19's design gate is the first real use of the new checks. | Head of Specs Team | 2026-11-18 |
| ST-34 early | EPIC-01–03 regenerate visual baselines; the workflow should be able to push them. | Head of Specs Team | 2026-11-18 |
| ST-25 → ST-26; ST-29 → ST-38; ST-32 → ST-33 | Shared code paths (native entry; settings change log; the on-demand Yahoo failures). | Head of Specs Team | 2026-11-18 |
| ST-27 rule approval before the build | A `strategy_rules.md` §12.3 change (RISK-05). | Head of Specs Team | 2026-11-18 |

### Accepted risks

None. No escalation was raised this run.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-11-18__release-v9.18
