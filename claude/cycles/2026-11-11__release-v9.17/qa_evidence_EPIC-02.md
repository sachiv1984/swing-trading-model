Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-16

# QA Evidence — EPIC-02: Journal & Performance Consolidation

**EPIC:** EPIC-02 — Site Structure & Usability Phase 3: Journal & Performance Consolidation (build-and-ship)
**Cycle:** 2026-11-11__release-v9.17
**Sprint goal:** Ship Site Structure & Usability Phase 3 complete (decision-first Positions page with narrow-screen cards, one warning strip and one grace view; the single Journal area; one Performance page; section indexes on Trade Plan and Strategy Benchmark; the semantic colour token sweep), finish Phase 2's Stops moved group, and close the v9.16 Trade Plan and market-data carry-forwards.
**Test scenarios used:** `tests/e2e/journal.spec.js`, `tests/e2e/section-index.spec.js`, `tests/e2e/performance.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-05 | `journal.md` v1.1 (JA-01..JA-21) | One `/Journal` page (Reflections, Red flags, Position notes tabs, shared ticker filter); `/TradeReflection` and `/RedFlagJournal` redirect; Positions journal view replaced by a "Position notes" link. Three build-time rulings (2026-11-16, Frontend Specifications & UX Documentation Owner / Head of UX & Design) recorded in `journal.md` v1.1: closed positions from `GET /trades`; a filtered-empty Reflections message; P&L badge in GBP. Commits `617dc36b`, `45243887`. | "Every observable AC in the Journal spec has Playwright coverage that passes; old routes redirect" — JA-01..JA-21 covered by SC-JNL-01, 02, 03, 04, 05, 06, 06b, 06c, 07, 07b, 08, 08b, 09, 09b, 10, 11, 12, 13, 15, 17, 17b, 19, 20 (`journal.spec.js`) and, for JA-14's sidebar and palette parts, SC-SNV-08 (`sidebar-nav-groups.spec.js`) and SC-PL-01/02 (`page-labels-single-source.spec.js`); redirects SC-JNL-12. CI on `45243887`: all 9 workflows success, Playwright E2E Acceptance Tests run 43851366613. | Pass | None |
| ST-06 | `performance.md` v1.1 (PF-01..PF-14); `performance-page-brief/decision_record.md` §2 | One `/Performance` page (Summary, Reports, Analytics, Compliance; shared section index); one home per period-level KPI; KPIs read from the server's `GET /analytics/metrics`; `/Reports` and `/PerformanceAnalytics` redirect (digest `?section=strategy-compliance` → Compliance). Commits `2d739631`, `68b0418b`. | AC 1: "One Performance page; old routes redirect; each KPI appears once; Playwright coverage passes" — SC-PERF-01, 02, 03, 05, 06, 06b, 07, 08, 09, 10, 11, 13, 14 (`performance.spec.js`); PF-04 in SC-SNV-08 and SC-PL-01/02; PF-12 in SC-ESN-11 (`empty-state-next-action.spec.js`), SC-ONW-05 (`onward-links.spec.js`), SC-MB-07b (`morning-briefing.spec.js`) and `tests/test_si05_digest_service.py`. Redirects SC-PERF-03, one home SC-PERF-05. AC 2: "The Metrics Definitions & Analytics Canonical Owner's confirmation that each KPI keeps its canonical definition is recorded with a date in the QA evidence" — **confirmed 2026-11-16** by the user acting as Metrics Definitions & Analytics Canonical Owner (ESC-EXEC-20261116-01; `performance.md` §11): every KPI keeps its canonical definition, read from its server source (§5.2). Addendum gate: `performance.md` approved by the Head of UX & Design, 2026-11-16, before the build. CI on `68b0418b` (fix for SC-MB-07b after run 43893990317): all 8 triggered workflows success, Playwright E2E Acceptance Tests run 43894993795; Frontend Production Build success on `2d739631` (43893990465). | Pass | None (BLG-FE-299 filed, pre-existing — see notes) |
| ST-07 | `trade_plan.md` v1.28 §5g; `strategy_benchmark.md` v0.11 §3a; `long-page-section-index/decision_record.md` | Shared `SectionIndex` (sticky column at `lg`, sticky 44 px pill row below); Trade Plan in seven `<section>`s; Strategy Benchmark's Benchmark tab with four panels; `?section=` deep links. Commits `a7af866b`, `44736ed8`. | "Each page shows its sections as tabs or an index; each section is reachable in one click; Playwright coverage passes" (index, not tabs, per the addendum) — SC-SIX-01, 02, 03, 04, 05, 06, 06b, 07, 08, 09, 09b (`section-index.spec.js`). CI on `44736ed8`: all 9 workflows success, Playwright run 43871300660. | Pass | None |

**AC coverage:** ST-05 and ST-07 have one AC each; ST-06 has two. Every AC is named in its row. No AC was marked staging-only or post-merge at the seal.

**Frontend testing gate (CLAUDE.md §2, LL-v3.1-EX-01):** every observable slice AC, and every spec AC ID (JA-01..JA-21, PF-01..PF-14), has a Playwright assertion that passed in real GitHub Actions CI (run IDs above). After DoQ round 1, assertions were added for the parts the review found only partly asserted: PF-05 (every §5.1 label, incl. Compliance KPIs), PF-07 (the Reports section is not refetched on a period change), PF-13 (Export PDF produces the report), PF-14 (header controls; the Export button's app-wide gradient primary style is excluded), JA-16 (partial match in Position notes) and JA-08 (next-page pagination). No AC is "code review only". Interaction-timing ACs (JA-17 300 ms debounce; section-index focus on jump) were observed passing in real CI: SC-JNL-17 and SC-SIX-02/03 in runs 43851366613 / 43871300660; SC-PERF-02 in run 43894993795. Contrast: axe on the Journal tabs (SC-JNL-04, light and dark), the section index (SC-SIX-08, SC-PERF-14) and the Reports section (accessibility-axe-scan, scoped to `section#reports`) requires no violation and no unrated colour contrast.

**Same-EPIC testing-gap consistency check:** no story in this EPIC filed a testing-gap backlog item. Nothing to align.

**Roll-up backstop (LL-v8.4-P4-01, LL-v9.0-P4-02):** the EPIC `test_scenarios` array in `execution_state.json` lists the three spec files above, which matches every test file in the stories' `spec_references` and every file named here.

**Visual-regression baselines (advisory job, `continue-on-error`):** this EPIC changes the Trade Plan page (ST-07 section index) and replaces Performance Analytics (ST-06), so the advisory "Playwright Visual Regression Baselines" job reports 4 screenshot differences (Trade Plan and Performance Analytics, dark and light; first seen in run 43871300660 on `44736ed8`, 4 on run 43894993795 on `68b0418b`). `tests/e2e/visual-regression-baselines.spec.js` is retargeted to `/Performance?section=analytics` in this EPIC (setup verified locally to reach the screenshot step). The baselines themselves are regenerated by EPIC-03's ST-08, which re-baselines both themes after every other UI EPIC (`sprint_backlog.md` Merge Order, RISK-02). This was found by the agent-mediated DoQ review (round 1).

**`BLG-FE-237` (Reports tab bar and Monthly table overflow):** its AC is met by ST-06 (`performance.md` §9): at 375 px no page-level horizontal scroll on any Reports view and the Monthly Avg P&L/Trade column scrolls into view inside its card (SC-PERF-11 at 390 and 375 px). Recorded here for `groom backlog`.

**Found defects filed during this EPIC:** `BLG-FE-299` (P3) — the Discipline & Compliance section's endpoint takes no period, so it does not follow the Performance period selector; pre-existing on the old Analytics page. No P1 or P2 found defect was filed.

**QA test coverage:**
- Scenarios run (new): SC-JNL-01, 02, 03, 04, 05, 06, 06b, 06c, 07, 07b, 08, 08b, 09, 09b, 10, 11, 12, 13, 15, 17, 17b, 19, 20; SC-SIX-01, 02, 03, 04, 05, 06, 06b, 07, 08, 09, 09b; SC-PERF-01, 02, 03, 05, 06, 06b, 07, 08, 09, 10, 11, 13, 14. Existing specs retargeted to the new routes and run (every functional reference to the old routes; the advisory visual-regression spec is covered in the note below): red-flag-journal (3 files), si01-si03-integration, exit-reason-badges, r-multiple-reflection, dialog-classname-override-fixes, morning-briefing, empty-state-next-action, page-labels-single-source, sidebar-nav-groups, onward-links, browser-tab-title, and 30 Reports/Analytics specs (monthly-pnl-*, reports-*, tax-year-*, arc5-compliance-section, analytics-section-link (rewritten for `?section=compliance`), chart-interactivity, analytics-mobile-responsive, market-correlation, trade-plan-tag-filter, staleness-indicator, loading-states, accessibility-axe-scan, and others). Local E2E-env build: 341 Performance-related scenarios passed; Trade Plan and Strategy Benchmark specs 451 passed (2 skipped, existing). pytest: `test_red_flag_checklist_skipped.py`, `test_si05_digest_service.py`, `test_motion_timing_500ms_ceiling_regression.py`.
- Regression areas checked: Positions (journal view removed), Dashboard Red Flags and Signal Compliance card links, SI-05 digest links, Trade History `?ticker=`, Trade Plan form (all panels, print), Strategy Benchmark tabs, every Reports view and export, every Analytics component, compliance sections, sidebar and command palette, browser tab titles.
- Known deviations: none found — all three stories' deviation checks completed with nothing to file. Build-time rulings were recorded in the specs (`journal.md` v1.1, `performance.md` v1.1), not as deviations.

**Notes:** Each story ran a high-effort `/code-review` before commit; all findings were fixed in-commit (ST-05: 9, ST-07: 9, ST-06: 10). ST-05 and ST-07 each needed one post-push CI fix for font-dependent width at 375/390 px (`45243887`, `44736ed8`), and ST-06 one for a spec the route sweep missed (`68b0418b`); all three re-runs are green (runs above).

## Standard Sign-Off Block

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- [ ] **Strategy values checked:** N/A — no stop/grace/ATR/exit/sizing logic touched (the Journal, Performance and section-index changes display existing values only).
- Signed off by: Pending DoQ
- Date:
- Comments:

## Merge Gate Confirmations

*(Written when the merge is recorded — STEP 4.)*
