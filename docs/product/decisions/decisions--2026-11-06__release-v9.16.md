Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.16
Cycle: 2026-11-06__release-v9.16
Last Updated: 2026-11-11

Superseded by: v9.16 ship — 2026-11-11
Changelog: docs/product/changelog.md#v9.16
Verification report: claude/cycles/2026-11-06__release-v9.16/verification_report.md
Cycle: 2026-11-06__release-v9.16

## Planning Decisions — v9.16

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Use full capacity: fill to 27.95 of the 28.00-day ceiling of the confirmed ~24–28 day band | Explicit user instruction: "plan release v9.16 use full capacity". 0.05d was left, and no remaining item fits. | Product Owner (direct user instruction) | 2026-11-06 |
| Seat `BLG-OPS-214` (P1) and `BLG-OPS-213` (P2) | The Anthropic key rotation (overdue since 2026-08-25) and the key copy in the public Pages build, accepted post-merge at v9.15 ST-29. v9.15 closure Carry-Forward #1. The P1 and P2 tiers seat both. | Release Planning Engine (Product Owner role) | 2026-11-06 |
| Seat the five Phase 2 P2 items and `BLG-FE-271` | `BLG-FE-250`, `254`, `255`, `256`, `264` (Phase 2) and `BLG-FE-271` (accepted v9.15 P2 gap, ruled at `ESC-CLOSE-20261106-01`) are ready P2. §1.4c step 1 seats them in ascending ID order. | Release Planning Engine (Product Owner role) | 2026-11-06 |
| Seat the three Phase 2 P3 items (§1.4c override) | `BLG-FE-251`, `252`, `253` (3.50d). The Product Owner named v9.16 "Site Structure & Usability, Phase 2". The oldest-first round-robin would not reach these items, which were filed 2026-11-03, so Phase 2 would have finished in v9.17 alongside Phase 3. Asked in session with two options, seating all of Phase 2 or the mechanical rule only; the Product Owner chose to seat all of Phase 2. Displaces 7 round-robin items (3.55d). | Product Owner (user decision in session) | 2026-11-06 |
| Hold Phase 3 under §1.4c step 0 | First use of `ESC-CLOSE-20261106-02`'s ruling (v2.72). The 8 Phase 3 items (20.50d), including P2 `BLG-FE-260`, are provisional for v9.17. No dated Product Owner reason to seat any of them early was given. | Release Planning Engine (Head of Specs Team role), per `release_planning_prompt.md` §1.4c step 0 | 2026-11-06 |
| Seat `BLG-GOV-413` under §1.4c step 1a | v9.15's deferred lessons-learnt patch (`LL-v9.15-Closure-01`), targeted at v9.16. | Release Planning Engine (Head of Specs Team role) | 2026-11-06 |
| Clear five gating-item-shipped gates in place (§1.3a, disposition (a)) | `BLG-FE-39`, `BLG-QA-21`, `BLG-QA-22`, `BLG-QA-23`, `BLG-GOV-26`. Each gate named only PT-04 shipped, and for three also Arc 2 complete. `current_roadmap.md` records PT-04 ✅ Shipped v6.1 and "Arc 2 ✅ Fully Complete". Bounded edits under ST-45/`ESC-EXEC-20261102-01` and `ESC-CLOSE-20261007-01`. The round-robin then seated all five as the oldest-filed items in the pool. | Release Planning Engine (Head of Specs Team role) | 2026-11-06 |
| Exclude `BLG-OPS-48` and `BLG-AI-23` (split-achievability) | Both were seated at v9.15, and their unmet ACs are tracked by follow-ups (`BLG-OPS-214`/`213`/`BLG-SPEC-223`; `BLG-AI-27`). Seating them again would track each AC twice. `BLG-GOV-413` (ST-28) fixes the pattern at Post-Ship Closure. | Release Planning Engine (Head of Specs Team role) | 2026-11-06 |
| Exclude `BLG-GOV-178`, `BLG-GOV-192`, `BLG-GOV-408` | `BLG-GOV-178`'s remainder is `BLG-GOV-399`. `BLG-GOV-192` is already met (v9.15 finding). `BLG-GOV-408` is a `run roadmap` input. | Release Planning Engine (Head of Specs Team role) | 2026-11-06 |
| Defer `BLG-TECH-21` (P2) despite P2-first ordering | Dedicated-release constraint in its own scope; `Provisional-Target: v10.0`. Standing §1.4c override, as at v9.10–v9.15. | Release Planning Engine (Product Owner role) | 2026-11-06 |
| Classify `BLG-OPS-197` and `BLG-OPS-198` as conditional (§1.4b) | Their production-data dates (2026-11-09; about 2026-11-12, after 10 nightly runs) fall inside the sprint window. `BLG-OPS-197` returned once at v9.15. | Release Planning Engine (PMO Lead role) | 2026-11-06 |
| Ship ST-06's Today list without the "Stops moved" group | `BLG-BE-205` is not seated (capacity). `dashboard.md` §1B already says the group is not rendered until those fields exist. The AC is restated to exclude TL-09/TL-10. | Release Planning Engine (Head of Specs Team role) | 2026-11-06 |
| Apply the STEP 4 calibration to the whole pool before selection, reading Scope and AC text | 6 raises, +2.85d, none seated (`BLG-BE-205` and `BLG-QA-250` new; 4 carried from v9.15). `BLG-FE-223` held with its count named. | Release Planning Engine (Head of Specs Team role) | 2026-11-06 |
| Restate missing, stale or out-of-slice ACs | Cleared-gate ACs: `BLG-FE-39`, `BLG-QA-21`, `BLG-QA-22`, `BLG-QA-23`, `BLG-GOV-26`. AC met by a ruling: `BLG-FE-271` AC 1 and AC 2's condition, plus a case (c) closure AC for its Known deviation. Spec data dependency: `BLG-FE-254`. No AC: `BLG-GOV-198`. Unqualified ST references: `BLG-AI-28`. Post-merge marker: `BLG-GOV-413` AC 2. Each is marked *(restated)* in the slice. | Release Planning Engine (Head of Specs Team role) | 2026-11-06 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ST-11 first in the sprint, run with ST-12 | P1 security item. ST-12 removes the Pages build's use of the secret, so the old key is revoked once. | Head of Specs Team | 2026-11-06 |
| ST-01 first in EPIC-01; ST-02 and ST-03 after it | Parent and onward links sit in `navigation.md` v2's areas, which ST-01 builds. | Head of Specs Team | 2026-11-06 |
| ST-07 → ST-08 | Both change the Trade Plan entry path; ST-08 edits `TradePlan.js` after "Plan this" pre-fills it. | Head of Specs Team | 2026-11-06 |
| EPIC-03 merges after EPIC-01 and EPIC-02 | ST-09 regenerates visual baselines for both themes, which must include the other UI changes. | Head of Specs Team | 2026-11-06 |
| ST-26 and ST-27 after ST-07/ST-08; ST-26 → ST-24 | The lifecycle test and journey map should reflect the new Trade Plan path. The QA protocol reuses the lifecycle test. | Head of Specs Team | 2026-11-06 |
| ST-16 → ST-17; ST-19 → ST-20 | Same fallback code path; the collision ruling may apply to the production tokens found in ST-19. | Head of Specs Team | 2026-11-06 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
