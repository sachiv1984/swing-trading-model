Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-12

# QA Evidence — EPIC-01: Positions Redesign

**EPIC:** EPIC-01 — Site Structure & Usability Phase 3: Positions Redesign (build-and-ship)
**Cycle:** 2026-11-11__release-v9.17
**Sprint goal:** Ship Site Structure & Usability Phase 3 complete (decision-first Positions page with narrow-screen cards, one warning strip and one grace view; the single Journal area; one Performance page; section indexes on Trade Plan and Strategy Benchmark; the semantic colour token sweep), finish Phase 2's Stops moved group, and fix the four v9.16 Trade Plan found defects.
**Test scenarios used:** `tests/e2e/positions-decision-first.spec.js`, `tests/e2e/positions-decision-cards.spec.js`, `tests/e2e/positions-warning-strip.spec.js`, `tests/e2e/positions-grace-view.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `positions.md` v2.25 §Decision-First Table; design record §2–§3 | Urgency-ordered Positions table: six data columns (Ticker, Price, Stop, To stop, P&L %, Action needed) plus expand and Actions; every other field in an expandable row; shared `src/lib/positionUrgency.js` | Default view shows about 6 columns in urgency order; expanding a row shows the rest; Playwright coverage passes | Pass — SC-POSDF-01..07; CI Playwright run 43257460636 on `6b475ae0` | None found. Review follow-ups BLG-SPEC-232, BLG-FE-289 (not AC gaps) |
| ST-02 | `positions.md` v2.25 §Responsive Behavior (Table v2.25 row); design record §4 | Below `md` the Table view renders decision cards in the same order and leading fields; Details opens the 2-column grid; 44 × 44 px footer actions | At 390px width, Positions shows cards with no horizontal page scroll; Playwright coverage passes | Pass — SC-POSDC-01..07 (SC-POSDC-02 asserts `scrollWidth ≤ 390`, collapsed, all details open, and Grid view); CI Playwright run 43286093150 on `540887b9` | None found. Review follow-ups BLG-FE-290, BLG-SPEC-233 (ST-01 code, not AC gaps) |
| ST-03 | `positions.md` v2.25 §Warning Strip; design record §6 | One `PositionsWarningStrip` ("Warnings" region) replaces the four banners; one entry per active warning in fixed order, each expanding to its existing content; `?grace=open` opens the grace entry | With all four conditions active, one strip shows four entries and each expands; Playwright coverage passes | Pass — SC-POSWS-01 (four entries, order, summaries), SC-POSWS-02 (each expands), SC-POSWS-03..08; CI Playwright run 43289954700 on `360bf177` (after the post-push SC-LBG-03 fix, see Comments) | None found |
| ST-04 | `positions.md` v2.26 §Grace Period View; `dashboard.md` v4.2 Card 3; `risk_dashboard.md` v0.1.16 §5.2; design record §5 | `GracePeriodView` is the only per-position grace detail (strip grace entry, every in-grace position, no dismiss); Dashboard Card 3 and the Risk Dashboard panel show a count and link to `/Positions?grace=open`; panel rows removed; `positions.md` §Grace Period Alert Zone made a "Superseded" stub | Grace detail renders in one component on one page; the other surfaces link to it; Playwright coverage passes | Pass_with_deviation — AC met: SC-POSGV-07 (the "Day n of 10" detail appears only inside `grace-period-view` on Dashboard, Risk Dashboard and Positions), SC-POSGV-05/06 (links), SC-POSGV-01..04, 08; CI Playwright run 43293797244 on `661cc4ee`. Spec shortfall: rows with more than 2 days left show no trade plan line | DEV-EPIC01-ST04-01 (P3, `positions.md` Known Deviations) — BLG-BE-215. Review follow-ups BLG-FE-291, BLG-SPEC-234 |

**AC coverage:** each story has one AC (stage4_backlog_slice.md#ST-01..ST-04, read with the addendum); every AC is a row above. No AC was marked staging-only or post-merge at the seal.

**Frontend testing gate (CLAUDE.md §2, LL-v3.1-EX-01):** every observable AC has Playwright coverage that passed in real GitHub Actions CI (run IDs above). No AC is "code review only". No focus-timing or interaction-timing AC is in this EPIC. Colour assertions: ST-01 "To stop" bands (SC-POSDF-03) and ST-04 amber accent (SC-POSGV-02) use theme tokens asserted by class. Contrast is checked by axe in light and dark mode for the warning strip with every entry open, including the grace view (SC-POSWS-07), and for the Risk Dashboard grace panel (SC-POSGV-08). The Positions axe scans in `accessibility-axe-scan.spec.js` also pass.

**Same-EPIC testing-gap consistency check:** no story in this EPIC filed a testing-gap backlog item. Nothing to align.

**Roll-up backstop (LL-v8.4-P4-01, LL-v9.0-P4-02):** the EPIC `test_scenarios` array in `execution_state.json` lists the four spec files above. That matches every test file in the stories' `spec_references` and every file named on this page.

**QA test coverage:**
- Scenarios run: SC-POSDF-01..07, SC-POSDC-01..07, SC-POSWS-01..08, SC-POSGV-01..08 (new). Existing specs updated to the new layout and run: SC-DD, SC-CC (`epic02-v34-risk-prompts`), SC-GP, SC-LS, SC-TS (`epic01-v34-lifecycle`), SC-LBG (`lifecycle-badge-grace-calendar-days`), SC-RD-07..12 (`risk-dashboard`, rewritten for the panel without rows), SC-GPL (`grace-panel-position-link`), SC-ESN (`empty-state-next-action`), SC-STALE, plus the 25 Positions specs whose selectors ST-01 updated. Full CI Playwright suite green on every story's final commit.
- Regression areas checked: Positions Table and Grid views, deep links (`?position=`, `?exit=`, `?grace=open`), Daily Monitor entry, compliance panel, Dashboard cards and Today list, Risk Dashboard grace panel and §6 table, Performance Analytics staleness indicator, axe scans of Positions, Dashboard and Risk Dashboard.
- Known deviations: DEV-EPIC01-ST04-01 (P3, BLG-BE-215). All four stories' deviation checks completed; ST-01 to ST-03 found nothing to file.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object. The strip reuses existing `API_BASE` and `API_URL` constants; there is no new URL base.
- [x] **Strategy values checked:** ST-01 — §6.3 (stop not enforced during grace, so in-grace rows never enter the stop tiers and show "Not enforced (grace)"), §7 (post-grace trailing-stop breach on the GBP basis, tier 2), §8 (exit condition met, tier 1 RISK OFF). ST-03 and ST-04 — §6.2 (grace length 10 calendar days; `GRACE_PERIOD_DAYS = 10`; "Day {min(11 − grace_days_remaining, 10)} of 10", entry day = Day 1). ST-02 displays ST-01's values with no new logic. The "near stop" ≤ 5% band is the Risk Dashboard display band (`risk_dashboard.md` §6), not a strategy parameter.
- Signed off by: [PENDING — awaiting Director of Quality sign-off]
- Date:
- Comments: Post-push CI fixes (LL-v8.5-P4-01, per story). ST-01: `b2d93f6d` failed SC-COMP-03/07 (run 43256379461); fixed in `6b475ae0`; final Playwright run 43257460636 green on head `6b475ae0`. ST-03: `99f16e6d` failed SC-LBG-03 (run 43288957471, shard 3/8); fixed in `360bf177`; final Playwright run 43289954700 green on head `360bf177`. ST-02 and ST-04 passed CI on their first push.
