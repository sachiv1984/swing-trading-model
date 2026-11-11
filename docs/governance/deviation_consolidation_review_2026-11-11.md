**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Report Date:** 2026-11-11
**Filed:** 2026-11-11
**Cycle:** 2026-11-06__release-v9.16 (post-ship closure STEP 5.1, cadence-triggered — 3rd Post-Ship Closure invocation since last run)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cross-EPIC Deviation (DEV-*) Consolidation Review — Ninth Run

## Objective

Ninth periodic run of the cross-cycle `DEV-*` consolidation review established by `ST-12` (EPIC-04, `2026-08-03__release-v8.1`, `BLG-QA-129`). Cadence: every 3rd Post-Ship Closure invocation. Prior run: `docs/governance/deviation_consolidation_review_2026-10-29.md` (eighth run, 27 records, commit `486e5cf2`).

## Method

Covered the three cycles since the last review: `2026-10-29__release-v9.14`, `2026-11-03__release-v9.15` and `2026-11-06__release-v9.16`.

- Diffed `docs/` and `claude/strategy/` from `486e5cf2` to `HEAD` (108 files) for added `DEV-*` identifiers and for added "Known deviation" text. The text search catches records with no `DEV-*` ID, such as `strategy_rules.md` entries and `metrics_definitions.md` Appendix E items.
- Read every record found in the diff at its current position in its spec.
- For every open record, checked that its backlog reference still resolves to an active `claude/backlog/backlog.md` item, not an archived one.
- Re-verified the eighth run's Recommendations 1 and 2, and continued the target-release-elapsed check.

## Consolidated Register

**Five new records in the window: four `DEV-*` records from v9.16 and two `metrics_definitions.md` Appendix E items from v9.14 closure.** One of the `DEV-*` records, `DEV-v9.16-ST27-01`, was added by this closure's STEP 5. The diff also shows three `strategy_rules.md` known-deviation changes and two `DEV-*` IDs that changed only in header text (`DEV-EPIC02-ST03-01` in `analytics.md` and `DEV-REPORTS-ST06-01` in `reports.md`). Neither of those two records changed status.

Status changes since the eighth run:
- ‡ `strategy_rules.md` §4.1.5 US sizing FX inversion: the entry was added (v1.19, `ESC-CLOSE-20261029-01`) and then **Resolved in v1.21** (v9.14 ST-09, `BLG-BE-190`).
- ‡ `strategy_rules.md` §8.4: its Priority, Target, Owner and backlog ID were completed (v1.19). It is still Open, and `BLG-BE-187` is active.
- ‡ `strategy_rules.md` §4.2.1 plan-linked Trade Entry: the entry was added (v1.26, `ESC-CLOSE-20261106-01`) and then **Resolved in v1.27** (v9.16 ST-05, `BLG-FE-271`).

The register now holds **34 records**: the 27 from the eighth run, the §4.2.1 entry, the two Appendix E items and the four v9.16 `DEV-*` records. The table lists the new and changed records. The 25 unchanged records are in the eighth run's register.

| DEV ID | Spec File | Priority | Status | Target/Resolved Release |
|--------|-----------|----------|--------|--------------------------|
| DEV-NAV-ST01-01 | `frontend/pages/navigation.md` | P3 | Open (`BLG-SPEC-226`, active) | TBD |
| DEV-v9.16-ST05-01 | `frontend/pages/trade_plan.md` | P3 | Open (`BLG-FE-277`, active) | v9.17 |
| DEV-v9.16-ST12-01 | `frontend/pages/trade_plan.md` | P3 | Open (`BLG-SPEC-229`, active) | v9.17 or later |
| DEV-v9.16-ST27-01 | `frontend/pages/trade_plan.md` | P2 (accepted PO + DoQ, 2026-11-11) | Open (`BLG-FE-282`, active). Added this closure, STEP 5 | v9.17 |
| *(no ID)* Appendix E Item 3, break-even win | `metrics_definitions.md` Appendix E | P2 | Resolved (v9.15, ST-15, `BLG-FE-239`) | v9.15 |
| *(no ID)* Appendix E Item 4, Dashboard win-rate widgets | `metrics_definitions.md` Appendix E | P2 | **Still marked Open, but its tracking item was closed and archived** (Finding 1) | v9.15 (elapsed) |
| *(no ID)* ‡ §4.1.5 US sizing FX inversion | `claude/strategy/strategy_rules.md` | P2 | **Resolved (v1.21, v9.14 ST-09)**, changed this run | v9.14 |
| *(no ID)* ‡ §8.4 live month-end calendar | `claude/strategy/strategy_rules.md` | P3 | Open. Fields completed (v1.19) (`BLG-BE-187`, active) | TBD |
| *(no ID)* ‡ §4.2.1 plan-linked Trade Entry | `claude/strategy/strategy_rules.md` | P2 | **Resolved (v1.27, v9.16 ST-05)** | v9.16 |

## Findings

**Finding 1: `metrics_definitions.md` Appendix E Item 4 still reads Open after its tracking item was closed as superseded.**
- **What happened.** Item 4 (Dashboard win-rate widgets fed from open positions only, P2, `BLG-FE-240`) still reads `Status: Open — Known Deviation (accepted P2, 2026-11-02)`. Its target, v9.15, has passed.
- **Why it is stale.** `BLG-FE-240` was bannered ✅ COMPLETE at the v9.15 post-ship closure under the new STEP 3.1 planning-deferred rule, and archived the same day. Both widgets existed only on the legacy `src/pages/Dashboard.js`, which v9.15 ST-12 removed, so the defect went with the page. `src/pages/Dashboard.js` is absent on `main`, and no `src/` file references `WinRateWidget` or `win_rate_chart`.
- **The pattern.** This is the resolution-status drift that the first run (2026-08-03) named. The tracking item was closed by a route that does not touch the spec: here, a supersession banner at closure, not a story. Item 3 was closed by its own story (ST-15), which updated the spec in the same commit (v1.34.3). Item 4 had no story, so nothing updated the spec.
- **Disposition.** Canonical spec status edits are outside Post-Ship Closure's STEP 5 write scope, which covers missing fields only. This is recorded as an Outstanding Action for the Metrics Definitions & Analytics Canonical Owner: mark Item 4 Resolved (superseded, v9.15 ST-12, legacy Dashboard removed). See the v9.16 closure record §6.

**Finding 2: the eighth run's recommendations are both closed.**
- Recommendation 1 (`ESC-CLOSE-20261029-01`): `strategy_rules.md` v1.19 added the §4.1.5 entry and completed the §8.4 entry's fields.
- Recommendation 2 (a path for `strategy_rules.md` known deviations): `ESC-CLOSE-20261029-02` ruled option (b), and the owner route is now in `post_ship_closure.md` STEP 5. The route worked at the next use: v9.15 closure routed the §4.2.1 entry through `ESC-CLOSE-20261106-01`, and it was applied the same day as v1.26.
- The second part of Recommendation 2, assigning `DEV-*` IDs to `strategy_rules.md` entries, was not taken up. The text search in this run's method still finds those entries. The watch stays narrowed to `strategy_rules.md`.

**Finding 3: same-story sync works for story-closed deviations.** `strategy_rules.md` §4.1.5 (v9.14 ST-09) and §4.2.1 (v9.16 ST-05) were each marked resolved by the story that fixed them. Appendix E Item 3 was too (v9.15 ST-15). All three used the sync rule (`BLG-GOV-315` / `BLG-GOV-332`). The one miss, Finding 1, is a deviation closed without a story.

**Finding 4: target-release-elapsed check (continued).**
- `DEV-ST04-01` (P2, Accepted) is still the only stale entry with a concrete target. Its precondition is unmet infrastructure, and the assessment has not changed across 9 runs.
- `DEV-REPORTS-ST06-01` (P3) has been open since v7.1 with target TBD. Its tracking item `BLG-SPEC-203` is active.
- Appendix E Item 4's v9.15 target has passed (Finding 1).

## Recommendations

1. **Mark `metrics_definitions.md` Appendix E Item 4 Resolved**, citing the v9.15 ST-12 supersession and `BLG-FE-240`'s banner. Owner: Metrics Definitions & Analytics Canonical Owner.
2. **Close the gap when a deviation is closed without a story.** When STEP 3.1 banners a planning-deferred item as superseded, and that item is the backlog reference of a Known Deviations entry, the closure should also flag the spec entry for its owner. Today the banner is the last step. Owner: Head of Specs Team. This is recorded as a v9.16 closure lessons-learnt item (`lessons_learnt_closure.md`).
3. **For the next run:**
   - Keep the broadened scan and the "Known deviation" text search.
   - Keep the active-backlog-reference check for every open record.
   - Re-verify Recommendation 1.
   - Continue the target-release-elapsed check, and check `DEV-v9.16-ST05-01` and `DEV-v9.16-ST27-01` against their v9.17 targets.

## Sign-off

- Signed off by: Post-Ship Closure Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-11-11
- Comments: Ninth consolidation review, cadence-triggered (3rd Post-Ship Closure invocation since 2026-10-29). Pending human confirmation.
  - The register grows from 27 to 34. Four new `DEV-*` records came from v9.16, including `DEV-v9.16-ST27-01`, added by this closure. The others are two `metrics_definitions.md` Appendix E items and one `strategy_rules.md` §4.2.1 entry.
  - Two `strategy_rules.md` deviations and Appendix E Item 3 were resolved by their own stories in the window.
  - Finding 1, a status drift on Appendix E Item 4, is routed to its spec owner.
