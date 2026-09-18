Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-18

---

## Consolidation Block

**EPIC:** EPIC-06 — Frontend & UX Debt
**Cycle:** 2026-09-15__release-v9.5
**Sprint goal:** Clear the full v9.5 debt-reduction scope — 43 items across 6 EPICs — at the top of confirmed sprint capacity, resolving the cycle's two genuine ungated P1 items first. See `sprint_goal.md`.
**Test scenarios used:** `tests/e2e/arc5-compliance-section.spec.js`, `tests/e2e/system-status.spec.js`, `tests/e2e/reports-performance-tab.spec.js`, `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js`, `tests/e2e/watchlist.spec.js`, `tests/e2e/settings-heading-order-and-aria-labelledby-regression.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-40 | `docs/specs/frontend/pages/trade_plan.md#9`, `src/pages/TradePlans.js#STATUS_CONFIG` | `TradeEntry.js`'s trade-plan-link select now uses the canonical `STATUS_CONFIG` label instead of the raw snake_case `plan.status` value. | Human-readable formatted text, no underscores, linkage functionality unaffected | Pass | None |
| ST-41 | `docs/specs/frontend/design_system.md#Motion-vs-contrast guideline`, `docs/design/2026-09-14__release-v9.4/motion-timing-target-release/decision_record.md` | All 4 known motion-timing non-compliant components (`SystemStatus.js` ×2, `Signals.js`, `Reports.js`, `RecentTradesWidget.js`) brought under the 500ms `delay + duration` ceiling; explicit `duration: 0.3` added throughout, verified against `framer-motion`'s actual source rather than assumed; removed from `design_system.md`'s known-non-compliant list. | All 4 verified against own current `duration`; removed from list in same commit; no visual regression beyond timing | Pass | None |
| ST-42 | `docs/specs/frontend/design_system.md#Toast Notification Timing`, `docs/design/2026-09-14__release-v9.4/toast-timing-standard/decision_record.md` | All 9 non-conforming toast call sites (`Layout.js`, `Settings.js` ×2, `Signals.js` ×2, `Positions.js` ×2, `PositionCard.js`, `useWatchlistModal.js`) brought into line with the severity-based duration table; non-conforming-screens table marked historical. | All 9 sites conform; table updated; no visual regression beyond timing | Pass | `BLG-QA-180` filed for future Playwright duration-assertion coverage (no existing test asserted these specific sites' timing) |
| ST-43 | `docs/specs/frontend/components/arc5_compliance_section.md#Low-Trade-Volume Advisory`, `docs/design/2026-09-15__release-v9.5/arc5-low-volume-advisory-placement/decision_record.md` | Advisory copy extended with the reliability/remaining-count clause; banner moved above the 4-card stat grid; 2 new Playwright assertions added (`SC-ARC5-13a/b`). | Placement/copy decision recorded; spec updated same commit; existing Playwright coverage still passes | Pass | None |

**QA test coverage:**
- Scenarios run (all local, sandboxed — see CI-confirmation note below):
  - `tests/e2e/arc5-compliance-section.spec.js` — 18/18 passed (16 pre-existing + 2 new, ST-43)
  - `tests/e2e/system-status.spec.js` — 34/34 passed (combined run with reports-performance-tab.spec.js, ST-41)
  - `tests/e2e/reports-performance-tab.spec.js` — included in the above 34/34 (ST-41)
  - `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js` — 15/15 passed (ST-40, RecentActivityCard timing for ST-41)
  - `tests/e2e/watchlist.spec.js` + `tests/e2e/settings-heading-order-and-aria-labelledby-regression.spec.js` — 10/10 passed (ST-42 adjacent-regression check)
- Regression areas checked: trade-plan linkage, dashboard/reports/system-status rendering, watchlist/settings toast paths, Arc 5 compliance advisory (all boundary/singular-plural cases)
- Known deviations: None found — all 4 stories' deviation checks completed with nothing to file, beyond the `BLG-QA-180` coverage-gap filing noted in ST-42's row above (a filed follow-up, not an unresolved deviation)

**Environment-parity sub-clause (LL-v8.3-P3-02) — disclosed, not yet satisfied:** ST-41 and ST-42 are interaction-timing ACs. All Playwright runs above were executed locally/sandboxed in this session — **no real GitHub Actions CI run has yet been observed for any commit in this EPIC**, since the PR is not yet open at the time this evidence was first written. Per the sub-clause, sandboxed-pass alone is not sufficient for this AC sub-class; **this must be re-checked against the real CI run once the PR is open and CI has completed, before this EPIC's sign-off is treated as final.** See the Sign-Off Block's own pending-confirmation note below.

---

## Frontend Testing Gate

This EPIC introduces frontend-visible changes (all 4 stories modify files under `src/pages/**` or `src/components/**`) — the **BLG-GOV-19 Autonomous Class Sign-Off Block is unavailable** (Criterion 3 fails per the `src/components/**`/`src/pages/**` detection rule). Standard Sign-Off Block used below.

For each observable AC:
1. **ST-40** (wording-only, no layout/colour/interaction claim) — FI-P3-02 exception applies; code review of the static JSX substitutes for staging/Playwright, per `sprint_backlog.md`'s own scoping. Confirmed via re-running `v7.2-dashboard-tradeplan-ux-hardening.spec.js` (15/15) that linkage functionality itself is unaffected.
2. **ST-41** (timing) — Playwright coverage exists and passes locally (`system-status.spec.js`, `reports-performance-tab.spec.js`, `v7.2-dashboard-tradeplan-ux-hardening.spec.js`); real-CI confirmation pending (see environment-parity note above).
3. **ST-42** (timing) — no dedicated Playwright coverage exists for these 9 exact call sites; `BLG-QA-180` filed before the PR opened, per the hard gate. Adjacent-regression suites re-run clean.
4. **ST-43** (copy + layout/placement) — new Playwright coverage added directly (`SC-ARC5-13a/b`) rather than deferred; 18/18 passed locally; real-CI confirmation pending (see environment-parity note above).

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no new URL construction introduced by this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-18
- Comments: All 4 stories' AC verified by code review + local Playwright runs (77 total local test executions across 4 suites plus the new arc5 suite run, 0 failures). **Pending confirmation before this sign-off is final:** the environment-parity sub-clause (LL-v8.3-P3-02) requires ST-41/ST-42's timing ACs to be observed passing in a real GitHub Actions CI run, not merely a sandboxed local pass — this has not yet occurred (PR not yet open at time of writing). Must be re-checked and this block updated once the EPIC-06 PR's CI run completes, before merge.

---

## Change Log

| Date | Change |
|------|--------|
| 2026-09-18 | Initial publication — EPIC-06, 4 stories (ST-40–ST-43), Standard Sign-Off Block (agent-mediated), CI confirmation pending per environment-parity sub-clause. |
