Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-20

# QA Evidence — EPIC-04 (v7.5)

## Consolidation Block

**EPIC:** EPIC-04 — Saved filter presets & calendar view
**Cycle:** 2026-07-17__release-v7.5
**Sprint goal:** Ship all four v7.5 UI feature expansions — global command palette, user-defined price alerts, bulk actions, and saved filters/calendar view — each fully wired to its now-locked design artefact and observable in the running app.
**Test scenarios used:** tests/e2e/saved-filters-calendar-view.spec.js (SC-SFC-01 through SC-SFC-09); tests/test_saved_filters_and_daily_pnl.py (13 unit test scenarios)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-04 | docs/design/2026-07-17__release-v7.5/saved-filters-calendar-view/ux_spec.md; docs/specs/frontend/pages/trade_history.md v1.11 §Saved Filter Presets & Calendar View; docs/specs/blg_fe_118_pre_implementation_readiness_pass.md; docs/specs/api_contracts/saved_filters_endpoints.md v1.0; docs/specs/api_contracts/reports_endpoints.md v0.9; docs/specs/data_model.md v2.13 | New `saved_filters` table (migration v2.12→v2.13); `GET/POST /saved-filters`, `DELETE /saved-filters/{id}`; `GET /reports/daily-pnl` (day-granularity sibling of the existing monthly-pnl report); `SavedFiltersControl.js` (save/apply/delete named presets, inline confirmation) and `CalendarView.js` (react-day-picker month grid with realised-P&L day indicators, unrealised-P&L banner, day-click navigation) mounted on Trade History behind a Table/Calendar toggle; BLG-FE-40 localStorage-envelope pattern added for Trade History's ephemeral active-filter state (previously unpersisted) | AC: User can save a filter combination by name and reapply it in a later session | Pass | None |
| ST-04 | (same as above) | (same as above) | AC: A calendar view renders trade plan dates and key dates, navigable by month | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/e2e/saved-filters-calendar-view.spec.js` — SC-SFC-01/02 ("Save current filters as…" hidden/visible based on active-filter state), SC-SFC-03 (save fires `POST /saved-filters` with correct name/filter_state), SC-SFC-04 (applying a preset overwrites active filters), SC-SFC-05 (Table/Calendar toggle, Table remains default), SC-SFC-06 (day-with-exits shows coloured indicator + tooltip with exact figure), SC-SFC-07 (clicking a day with exits switches to Table view with the date filter set to that day), SC-SFC-08 (month navigation fires a new `GET /reports/daily-pnl` request), SC-SFC-09 (zero closed trades in the account shows the full-page empty state). All 9 run live against `npm start` (real dev server, `page.route()` API interception) — 9/9 pass.
- `tests/test_saved_filters_and_daily_pnl.py` — 13 unit scenarios covering `create_saved_filter` validation (missing/oversized name, non-dict `filter_state`, duplicate-name rejection, successful creation), `delete_saved_filter` (not-found + success), `get_saved_filters` serialisation, and `get_daily_pnl_report` (no-portfolio path, day-bucketed shape, empty-month path). All mocked — no live DB calls.
- Regression areas checked: `tests/e2e/trade-history-ai-journal-summary.spec.js` (3/3), `tests/e2e/tax-year-csv-export.spec.js` (5/5), `tests/e2e/slippage-tracking.spec.js` (8/8), `tests/e2e/trade-plan-tag-filter.spec.js` (5/5 — Performance Analytics page unaffected), `tests/e2e/net-r-trade-history.spec.js` (5/5 — see regression note below), `tests/e2e/system-status.spec.js` (16/16, incl. updated SC-SS-01b fallback-count assertion for the new 93-endpoint total), `tests/e2e/smoke-critical-paths.spec.js` (3/3). Backend: full `pytest` suite 686 passed, 2 skipped (pre-existing), 0 failed. Full e2e suite re-run end-to-end after the regression fix below — all green.
- Known deviations filed: None.

**Implementation notes (not filed deviations — intent matches spec, per LL-v3.4-P3-03):**
1. **`react-day-picker` DayPicker interactivity gap.** The pre-existing `src/components/ui/calendar.js` scaffold was written against an older DayPicker API (v8/v9-style `classNames`/`IconLeft`/`IconRight`) but the actually-installed version is v10.0.1 (already present in `package.json`/`node_modules` — the readiness pass's flagged dependency gap was already resolved before this story started, confirmed via direct `node_modules` check). Rather than reconcile the mismatched wrapper, built a purpose-specific `CalendarView.js` using `DayPicker` directly with v10-correct `classNames`/`components` keys (verified against the installed package's own `.d.ts` files). Discovered during live verification that DayPicker only renders a custom `DayButton` component when interactive (`mode` or `onDayClick` set) — added a no-op `onDayClick` to force this without introducing an actual selection state, since day-click handling is implemented inside the custom `DayButton` itself.
2. **Ephemeral active-filter persistence added to Trade History.** `ux_spec.md` §2.5 / `trade_history.md`'s "Persistence Distinction" locks in that the page's active filter state should follow the existing BLG-FE-40 versioned-localStorage-envelope pattern (already implemented for `RedFlagJournal.js`), coexisting with but distinct from the new named server-side presets. Trade History had no such persistence before this story; added it in the same commit per the locked design, reusing the identical envelope shape/versioning/corrupt-state-recovery behaviour.

**Regression caught and fixed during verification:** the first full-suite run surfaced a real crash in `tests/e2e/net-r-trade-history.spec.js` (5 scenarios) — that pre-existing spec file's generic catch-all mock (`{status:'ok', data:{}}`, an object rather than an array, for any endpoint it doesn't explicitly stub) is now also hit by the newly-mounted `SavedFiltersControl`/`CalendarView` components' `GET /saved-filters`/`GET /reports/daily-pnl` calls, and `presets.map(...)`/`dailyPnl.map(...)` crashed on the non-array `data` value. Fixed by guarding both fetches with `Array.isArray(json.data) ? json.data : []` instead of the weaker `json.data || []` (which only handles `null`/`undefined`, not a non-array truthy value). Re-ran the full e2e suite after the fix to confirm the crash is resolved and no other tests were affected.

**Frontend testing gate (CLAUDE.md / LL-v3.1-EX-01):** Both ACs are observable UI behaviour (save/apply/delete presets; calendar rendering, navigation, day-click) — sprint_backlog.md's ST-04 entry lists no staging-only ACs, and all are Playwright-covered in CI (`tests/e2e/saved-filters-calendar-view.spec.js`), satisfying the hard gate without a staging run.

**Autonomous class eligibility check (BLG-GOV-19):** Not applicable — this EPIC creates `src/components/trades/SavedFiltersControl.js` and `src/components/trades/CalendarView.js`, and modifies `src/pages/TradeHistory.js` (frontend-visible change under `src/components/**` and `src/pages/**`), so Criterion 3 is automatically unmet per the BLG-GOV-135 detection rule. Standard Sign-Off Block below applies; Playwright coverage evidence is recorded above per the fail-path instruction.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — `SavedFiltersControl.js` and `CalendarView.js` use `API_BASE_URL`/`apiFetch` from `src/api/base44Client.js`, the same pattern as sibling components in this domain.
- Signed off by: Director of Quality
- Date:
- Comments: Awaiting Director of Quality review. Engine-side verification complete: 9/9 new Playwright scenarios pass, 13/13 new backend unit scenarios pass, full regression suite (trade-history-ai-journal-summary, tax-year-csv-export, slippage-tracking, trade-plan-tag-filter, system-status, smoke-critical-paths e2e specs + full backend pytest suite) green. Per `execution_prompt.md` §3.2.A/§5.3, DoQ sign-off is an always-human gate — halting here pending human review, not an escalation requiring an authority decision.
