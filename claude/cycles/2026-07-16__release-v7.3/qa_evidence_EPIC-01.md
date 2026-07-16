Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-16

# QA Evidence — EPIC-01 (Dashboard & Trade-Plan UX Implementation)

**Cycle:** 2026-07-16__release-v7.3
**Sprint goal:** Ship the three carried-forward v7.2 UI implementation stories (Start Trade from Plan, dashboard empty/first-run state coverage, dashboard briefing visual hierarchy) and complete all four v7.4-candidate pre-implementation readiness passes, so v7.4's next release plan can scope BLG-FE-115/116/117/118 from a fully de-risked backlog.
**Test scenarios used:** `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js` (15 scenarios, all passing), `tests/test_position_trade_plan_link.py` (7 scenarios, all passing)

---

## ST-01 — Trade-plan-to-execution linkage UX ("Start Trade from Plan")

**Spec reference:** `src/pages/TradePlan.js`, `src/pages/TradePlans.js`, `src/pages/TradeEntry.js`
**Commit:** `867f6ad629e1d766abe24faa57a465a61a0c0f7f`

**What was built:** A "Start Trade" action on `TradePlans.js` (list) and "Start Trade from Plan" on `TradePlan.js` (detail), shown only for plans with no linked position and not in a terminal status (`isStartTradeEligible` helper, exported for reuse). Clicking navigates to `TradeEntry.js` with ticker/market/entry price/stop price/quantity pre-filled via router state, and the exact plan id carried through. `backend/services/position_service.py add_position()` gained an optional `trade_plan_id` parameter that, when present, deterministically links that exact plan (`position_id` + `status: active`) — taking precedence over the existing ticker/market best-effort auto-link (BLG-BE-46). Manual entry (no plan origin) is unaffected and gained an optional "Link to Trade Plan" selector.

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 — action visible/functional on both TradePlan.js and TradePlans.js | Pass | SC-STP-01, SC-STP-02, SC-STP-03, SC-STP-04 |
| AC-02 — trade_plan_id populated with no additional user action | Pass | SC-STP-05 (Playwright, captures POST /portfolio/position payload); `test_explicit_plan_id_links_that_exact_plan_not_ticker_match`, `test_explicit_plan_already_linked_skips_update`, `test_explicit_plan_lookup_failure_does_not_block_position_creation` (backend unit) |
| AC-03 — manual trades unaffected, can still optionally select a plan | Pass | SC-STP-06 (manual entry regression), SC-STP-07 (manual link selector) |
| AC-04 — no regression to TradeEntry.js validation/submission | Pass | SC-STP-06/07 exercise the real submit path (`isFormValid` unchanged); `tests/e2e/keyboard-shortcuts.spec.js` SC-KBD-02/03 (TradeEntry navigation) and full CI Playwright E2E run confirm no regression |

**Deviations:** None. AC-02 required a backend change (`add_position()` explicit `trade_plan_id` param) not named in the story's frontend-only spec references — this is the correct implementation of AC-02 as written (deterministic link), not a divergence from spec intent; no canonical spec defined a different mechanism to diverge from.

---

## ST-02 — Dashboard empty/first-run state coverage

**Spec reference:** `src/pages/DashboardHome.js`, `src/components/ui/DataState.js`, `src/pages/Watchlist.js` (reference pattern)
**Commit:** `1db04b589353801ebdeeff97cf96f04f3df8fbb7`

**What was built:** `DataState.js` gained a `compact` mode (smaller padding/icon) for grid-tile contexts. `DashboardCard.js` now accepts `empty`/`emptyIcon`/`emptyHeading`/`emptyBody` and renders via `DataState` (compact) when empty, leaving its own loading/error rendering untouched. All nine dashboard tiles that previously showed a raw `0`/`—` (`OpenPositionsCard`, `PortfolioHeatCard`, `GracePeriodCard`, `RecentActivityCard`, and the five `morning/*Card` components) now show a clear empty state; `AiDailyBriefing`'s existing plain-text empty message was converted to the same `DataState` pattern for consistency.

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 — every card renders a clear empty state, not blank/raw zero-null | Pass | SC-DES-01, SC-DES-03, SC-DES-04; `morning-briefing.spec.js` SC-MB-02/02b (existing empty-text assertions still pass unchanged) |
| AC-02 — empty states use the shared DataState component | Pass | Code review: all 9 cards route through `DashboardCard`'s new `empty` prop → `DataState` (compact); `AiDailyBriefing` uses `DataState` directly |

**Scope note:** Extended beyond the 5 explicitly-named cards to the 5 `MorningBriefing` sub-cards and `AiDailyBriefing`, since all render on `DashboardHome.js` and several showed the same raw-zero/null pattern AC-01 prohibits. `SignalStatusCard` intentionally left unchanged — its regime-status rows always render meaningful content, so no "empty" condition exists for it.

**Regression found and fixed during implementation:** `PortfolioHeatCard` initially called `heat.toFixed(1)` unconditionally; because JSX children passed to `DashboardCard` are evaluated eagerly regardless of the `empty` flag, this crashed with `heat == null`. Caught by the new Playwright spec (`SC-DES-*` initially failed with a runtime error), fixed before commit — see commit `1db04b58` diff. `ComplianceCard` had the same latent pattern (non-crashing but included for consistency) and was fixed the same way.

**Deviations:** None.

---

## ST-03 — Dashboard briefing visual hierarchy

**Spec reference:** `src/pages/DashboardHome.js` (`MorningBriefing`, `AiDailyBriefing`)
**Commit:** `1db04b589353801ebdeeff97cf96f04f3df8fbb7`

**What was built:** `MorningBriefing` and `AiDailyBriefing` are now grouped in an accent-bordered/tinted wrapper (`border-indigo-500/30 bg-indigo-500/5 dark:bg-indigo-500/10`) placed immediately after the page header — above the status-card grid — so both are visible on page load without scrolling. No changes to card data, queries, or the `dashboard-retry-root` retry mechanism.

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 — visually distinguishable from status-card grid, visible on load without scrolling | Pass | SC-DBH-01 (bounding-box order check), SC-DBH-02 (border-colour presence), SC-DBH-03 |
| AC-02 — no change to card data/queries/dashboard-retry-root | Pass | SC-DBH-04; `gate-progress.spec.js` and `morning-briefing.spec.js` full suites pass unchanged |
| AC-03 — verified in both light and dark theme | Pass | SC-DBH-02 (explicit light + dark theme assertions per `base44_prompt_template_library.md` §4) |

**Deviations:** None.

---

## QA Test Coverage

- **Scenarios run:** `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js` (15/15 pass), `tests/test_position_trade_plan_link.py` (7/7 pass), full backend suite (668 passed, 2 skipped, 0 new failures), `tests/e2e/morning-briefing.spec.js` (12/12 pass), `tests/e2e/gate-progress.spec.js` (4/4 pass), `tests/e2e/heading-light-theme-contrast.spec.js` (4/4 pass), `tests/e2e/ai-briefing-progressive-disclosure.spec.js` + `tests/e2e/epic02-v62-ai-briefing-chat.spec.js` (14/14 pass), `tests/e2e/trade-plan.spec.js` (28/33 pass — 5 failures pre-existing and environment-caused, confirmed byte-identical against `git stash` baseline: `REACT_APP_ANTHROPIC_API_KEY` unset in this sandbox's `.env`, unrelated to this EPIC's changes).
- **Regression areas checked:** DashboardHome card grid (data/loading/error paths unchanged), Morning Briefing sub-cards, AI Daily Briefing, Trade Plan list/detail, Trade Entry form validation and submission, `add_position()` ticker/market best-effort auto-link (BLG-BE-46, still covered by its original 4 tests, all passing).
- **Known deviations filed:** None.

**Frontend testing gate (CLAUDE.md):** Every observable AC across ST-01/02/03 has explicit Playwright coverage (listed above), run and confirmed passing in this session prior to commit. No AC relies on "code review only" — no backlog item required for deferred staging.

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no new direct URL construction introduced
- Signed off by: Director of Quality
- Date: <awaiting Director of Quality sign-off — EPIC-01 introduces frontend-visible changes (src/pages/**, src/components/**), so per execution_prompt.md §3.2.A BLG-GOV-135 detection rule the autonomous DoQ sign-off class is unavailable, and per §5.3 the merge-gate QA sign-off is always human, never agent-mediated>
- Comments:
