Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-05

# QA Evidence Log — EPIC-06

**EPIC:** EPIC-06 — Frontend & UX Debt
**Cycle:** 2026-09-30__release-v9.9
**Sprint goal:** Ship a single canonical ATR/stop-recalculation implementation with timestamp visibility on `GET /positions` (`BLG-BE-135`), while clearing the queued backend, security, QA, governance, spec, and frontend debt items that make up the rest of v9.9's full-capacity scope.
**Test scenarios used:** `tests/e2e/recent-trades-zero-pnl-badge.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-35 | `docs/specs/frontend/design_system.md#Data States` (zero renders in the neutral tone: green > 0, red < 0, neutral = 0), `tests/e2e/recent-trades-zero-pnl-badge.spec.js` | `RecentTradesWidget`'s icon badge now uses the same three-way split as the adjacent P&L text: `bg-emerald-500/20 text-emerald-400` above 0, `bg-rose-500/20 text-rose-400` below 0, and `bg-slate-500/20 text-slate-300` at exactly 0 (and for a missing `pnl`, which the widget already treats as 0). Badge colour only; the icon glyph logic is unchanged, as BLG-FE-192 scopes it. A `data-testid` was added for the test. | AC-01 zero-P&L badge neutral → SC-RTB-01 (plus SC-RTB-04 for `pnl: null`); AC-02 winner emerald / loser rose unchanged → SC-RTB-02, SC-RTB-03; AC-03 Playwright test passes in CI → SC-RTB-01..04 all ✓ in `Playwright E2E Acceptance Tests` run 37285970680 (head `7013c331`, shard 5/8) | Pass | None |

**Frontend testing gate (CLAUDE.md §2, LL-v3.1-EX-01):** every observable AC (badge colour per P&L sign) has Playwright coverage, so none is "code review only".
- `tests/e2e/recent-trades-zero-pnl-badge.spec.js` SC-RTB-01..04, mocked `GET /positions` and `/#/Dashboard`
- **Observed passing in real GitHub Actions CI:** run https://github.com/sachiv1984/swing-trading-model/actions/runs/37285970680 on head `7013c331`. All 8 acceptance shards succeeded, and SC-RTB-01, 02, 03 and 04 each show ✓ in shard 5/8 (job 111684832810). The run's advisory pixel-baseline job showed diffs on DashboardHome, TradePlan and PerformanceAnalytics. Those are pages this change does not touch, and the latest `main` run of the same workflow (34971448238, `1f0f4201`) shows the same diffs, including DashboardHome's 1608→1612px height. They predate this change. The job concluded success and is advisory.
- Local runs: 4/4 passed on two consecutive runs. One earlier run had a single SC-RTB-01 failure on a cold `npm start` dev server, which passed on immediate re-run; CI uses a production build.
- Regression proof: with the original `>= 0` logic restored temporarily, SC-RTB-01 and SC-RTB-04 fail
- The environment-parity sub-clause (focus/interaction timing) does not apply; this is a static class/colour AC.

**QA test coverage:**
- Scenarios run: `tests/e2e/recent-trades-zero-pnl-badge.spec.js` (4 scenarios)
- Regression areas checked: Dashboard Recent Trades widget. Cross-spec selector check: no existing Playwright spec targets this badge (the `bg-emerald-500/20` assertions in `compliance-recheck`, `research-trade-plan-status-badge` and `market-correlation` are other components).
- Known deviations: None found — ST-35's deviation check completed with nothing to file (the change brings the widget into line with `design_system.md`).

---

## Standard Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):** Criterion 3 unmet — ST-35 modifies `src/components/dashboard/widgets/RecentTradesWidget.js` (BLG-GOV-135 detection rule). Standard Sign-Off Block applies.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no URL construction in this change
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-10-05
- Comments: Agent-mediated Director of Quality review per execution_prompt.md §5.3, by an independent reviewer subagent working read-only against `claude/agents/director_of_quality.md`. **Verdict: Approved**, with 3 non-blocking findings: (1) the CI shard number was corrected to 5/8 (job 111684832810, "121 passed (1.9m)" with SC-RTB-01..04 ✓); (2) the icon glyph still uses `>= 0`, which is acceptable because the AC and BLG-FE-192 are colour-only; (3) the local mutation claim is consistent on static analysis. The frontend testing gate is met by the real CI Playwright run 37285970680, all 10 jobs successful. The reviewer verified the pixel-baseline diffs are pre-existing on `main`. This block does not satisfy the always-human merge-gate rows: a Director of Quality comment on the PR and Product Owner acceptance are still required.
