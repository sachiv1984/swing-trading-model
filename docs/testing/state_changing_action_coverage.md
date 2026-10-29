**Owner:** Director of Quality
**Class:** Class 2
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-28 (ST-24, EPIC-04, v9.13, BLG-QA-227 — first inventory of state-changing primary actions with Playwright coverage status)
**Sprint Item:** ST-24 (BLG-QA-227, EPIC-04, v9.13)

---

# State-Changing Action Coverage

Every frontend action that sends a POST, PUT, PATCH or DELETE to the app's API, and whether a Playwright test exercises it. The Daily Position Monitor sent `PATCH /positions/{id}` to a route that does not exist (BLG-FE-226), and no test noticed. This inventory, together with the suite-wide API status guard (`tests/e2e/fixtures/api-status-guard.js`), is what stops that happening silently again.

## How This Was Produced

1. **Call sites.** `scripts/check_frontend_api_calls.py` (ST-23) extracts every `doFetch`/`apiFetch` call in `src/` with its method and path. Its state-changing calls are the rows below: 58 call sites, 52 distinct routes, in 21 files.
2. **UI action.** Each call site was traced to the control that triggers it. A client method in `src/api/base44Client.js` was traced through its callers. Seven methods have no caller and are listed separately.
3. **Coverage.** The full Playwright suite was run against a production build with `API_CALL_LOG=<file>`. The guard fixture then records every state-changing request the app sends to the API origin, mocked or not, with the spec and test that sent it. An action counts as **covered** when at least one test sent its request from that action's control. A route reached from several controls was attributed per control from the test titles. A `{param}` route does not count a request to a literal sibling route (e.g. `DELETE /watchlist/bulk` is not `DELETE /watchlist/{id}`).

Run: 2026-10-28, branch `exec/2026-10-16__release-v9.13/EPIC-04`, 1,142 tests.

To regenerate: build as in `playwright.config.js`, then run `API_CALL_LOG=/tmp/calls.jsonl npx playwright test` and repeat steps 2 and 3.

## Defects the Guard Exposed

None. The first full run with the guard failed 20 tests in 5 specs. Every 404 was a response the API contract documents ("no plan linked", "no debrief yet", "no reflection saved", `version_not_found`, "plan not found"). Each of those specs now declares its 404 with `allowApiErrors(...)`. No 405 occurred.

## Primary Actions

| # | Action (UI) | Request | Call site | Status | Evidence / tracking |
|---|-------------|---------|-----------|--------|---------------------|
| 1 | Exit selected positions (Daily Position Monitor) | `POST /positions/{id}/exit` | `pages/Dashboard.js` → `base44Client.js:291` | Covered | `monitor-exit-queue.spec.js` SC-MEQ-01..04 |
| 2 | Confirm exit (Positions page Exit modal) | `POST /positions/{id}/exit` | `pages/Positions.js` → `base44Client.js:291` | Not covered | BLG-QA-230 (2026-10-28) |
| 3 | Add position (Trade Entry) | `POST /portfolio/position` | `base44Client.js:400` | Covered | `smoke-critical-paths.spec.js`, `trade-entry-system-stop.spec.js` |
| 4 | Calculate position size | `POST /portfolio/size` | `base44Client.js:411` | Covered | `position-sizing-widget-behaviours.spec.js`, `smoke-critical-paths.spec.js` |
| 5 | Mark reviewed (Positions table view) | `PATCH /positions/{id}/mark-reviewed` | `pages/Positions.js:606` | Covered | `position-review-cadence-nudge.spec.js` SC-RCN-06 |
| 6 | Mark reviewed (position card, grid view) | `PATCH /positions/{id}/mark-reviewed` | `components/positions/PositionCard.js:114` | Not covered | BLG-QA-230 (2026-10-28) |
| 7 | Save position note | `PATCH /positions/{id}/note` | `pages/Positions.js:773` → `base44Client.js:228` | Not covered | BLG-QA-230 (2026-10-28) |
| 8 | Save position tags | `PATCH /positions/{id}/tags` | `pages/Positions.js:778` → `base44Client.js:235` | Not covered | BLG-QA-230 (2026-10-28) |
| 9 | Deposit / withdraw cash | `POST /cash/transaction` | `components/cash/CashManagementModal.js` → `base44Client.js:508` | Covered | `cash-management-global-trigger.spec.js` |
| 10 | Save settings (existing record) | `PATCH /settings/{id}` | `pages/Settings.js:78` → `base44Client.js:499` | Covered | `settings-last-change.spec.js`, `settings-strategy-parameters-fixed.spec.js` |
| 11 | Save settings (first save, no record yet) | `POST /settings` | `pages/Settings.js:80` → `base44Client.js:493` | Not covered | BLG-QA-230 (2026-10-28) |
| 12 | Update signal status (Signals page) | `PATCH /signals/{id}` | `pages/Signals.js` → `base44Client.js:346` | Covered | `signal-card.spec.js` |
| 13 | Add signal to watchlist (Signals page) | `POST /watchlist` | `pages/Signals.js:116` | Covered | `signal-card.spec.js` |
| 14 | Add result to watchlist (Screener) | `POST /watchlist` | `pages/Screener.js:284` | Covered | `screener.spec.js` SC-SCR-11..13, `screener-uk-suffix.spec.js` SC-UK-04 |
| 15 | Run screener | `POST /screener/run` | `pages/Screener.js:742` | Covered | `screener.spec.js`, `empty-state-next-action.spec.js` SC-ESN-03 |
| 16 | Add watchlist entry (Watchlist modal) | `POST /watchlist` | `hooks/useWatchlistEntryForm.js:27` | Not covered | BLG-QA-230 (2026-10-28) |
| 17 | Edit watchlist entry (Watchlist modal) | `PATCH /watchlist/{id}` | `hooks/useWatchlistEntryForm.js:16` | Not covered | BLG-QA-230 (2026-10-28) |
| 18 | Keep stale watchlist entry | `PATCH /watchlist/{id}` | `hooks/useWatchlistModal.js:24` | Covered | `watchlist-staleness-review.spec.js` SC-WLS-04 |
| 19 | Delete watchlist entry (Watchlist modal) | `DELETE /watchlist/{id}` | `hooks/useWatchlistEntryForm.js:82` | Not covered | BLG-QA-230 (2026-10-28) |
| 20 | Bulk tag watchlist entries | `POST /watchlist/bulk-tag` | `pages/Watchlist.js:84` | Covered | `bulk-actions-toolbar.spec.js` |
| 21 | Bulk remove watchlist entries | `DELETE /watchlist/bulk` | `pages/Watchlist.js:99` | Covered | `bulk-actions-toolbar.spec.js` SC-BAT-06 |
| 22 | Save new trade plan | `POST /trade-plans` | `pages/TradePlan.js:599` | Covered | `trade-plan-clone.spec.js`, `entry-checklist.spec.js` |
| 23 | Save existing trade plan | `PUT /trade-plans/{id}` | `pages/TradePlan.js:616` | Covered | `trade-plan.spec.js` SC-TP-30 |
| 24 | Abandon trade plan (submit) | `PUT /trade-plans/{id}` | `pages/TradePlan.js:633` | Not covered | BLG-QA-230 (2026-10-28) |
| 25 | Improve plan with AI | `POST /trade-plans/generate-plan` | `pages/TradePlan.js:1063` | Covered | `trade-plan.spec.js` |
| 26 | Delete one trade plan | `DELETE /trade-plans/{id}` | `pages/TradePlans.js:88` | Not covered | BLG-QA-230 (2026-10-28) |
| 27 | Bulk tag trade plans | `POST /trade-plans/bulk-tag` | `pages/TradePlans.js:169` | Covered | `bulk-actions-toolbar.spec.js` |
| 28 | Bulk archive trade plans | `PUT /trade-plans/bulk-archive` | `pages/TradePlans.js:184` | Covered | `bulk-actions-toolbar.spec.js` |
| 29 | Bulk delete trade plans | `DELETE /trade-plans/bulk` | `pages/TradePlans.js:198` | Covered | `bulk-actions-toolbar.spec.js` SC-BAT-10 |
| 30 | Save trade reflection | `POST /trades/{id}/reflection` | `components/trades/TradeReflectionModal.js:89` → `base44Client.js:441` | Not covered | BLG-QA-230 (2026-10-28) |
| 31 | Generate / regenerate post-trade debrief | `POST /trades/{id}/debrief` | `components/trades/TradeDebrief.js:74` | Covered | `trade-debrief.spec.js` SC-DBF-02a, 07a..09b |
| 32 | Generate AI journal summary | `POST /ai/journal-summary` | `pages/TradeHistory.js:179` | Covered | `trade-history-ai-journal-summary.spec.js` |
| 33 | Save filter preset | `POST /saved-filters` | `components/trades/SavedFiltersControl.js:43` | Covered | `saved-filters-calendar-view.spec.js` SC-SFC-03 |
| 34 | Delete filter preset | `DELETE /saved-filters/{id}` | `components/trades/SavedFiltersControl.js:72` | Not covered | BLG-QA-230 (2026-10-28) |
| 35 | Ask the AI chat | `POST /ai/chat` | `components/AiChatWidget.js` → `base44Client.js:533` | Covered | `epic02-v62-ai-briefing-chat.spec.js`, `chat-answer-rating.spec.js` |
| 36 | Rate a chat answer | `POST /ai/chat/{answer_id}/rating` | `components/AiChatWidget.js` → `base44Client.js:540` | Covered | `chat-answer-rating.spec.js` SC-CAR-01..05 |
| 37 | Load AI daily briefing | `POST /ai/daily-briefing` | `components/dashboard/home/AiDailyBriefing.js` → `base44Client.js:531` | Covered | `ai-briefing-progressive-disclosure.spec.js` |
| 38 | Create alert threshold rule | `POST /alerts/rules` | `components/notifications/AlertThresholdsSection.js:82` | Covered | `alert-thresholds-empty-state.spec.js` |
| 39 | Edit or toggle alert threshold rule | `PATCH /alerts/rules/{id}` | `components/notifications/AlertThresholdsSection.js:179` | Not covered | BLG-QA-230 (2026-10-28) |
| 40 | Create price alert | `POST /price-alerts` | `components/notifications/CustomPriceAlertsSection.js:104` | Covered | `custom-price-alerts.spec.js` |
| 41 | Delete price alert | `DELETE /price-alerts/{id}` | `components/notifications/CustomPriceAlertsSection.js:211` | Covered | `custom-price-alerts.spec.js` |
| 42 | Save notification preferences | `PATCH /notifications/preferences` | `pages/NotificationPreferences.js:84` | Covered | `notifications.spec.js` |
| 43 | Mark notification read | `PATCH /notifications/{id}` | `pages/Notifications.js:82` | Covered | `notifications.spec.js` |
| 44 | Mark all notifications read | `POST /notifications/mark-all-read` | `pages/Notifications.js:104` | Covered | `notifications.spec.js` |
| 45 | Add ticker to universe | `POST /ticker-universe` | `pages/TickerUniverse.js:62` | Covered | `ticker-universe.spec.js` SC-TU-02b/c |
| 46 | Reactivate ticker | `POST /ticker-universe` | `pages/TickerUniverse.js:257` | Not covered | BLG-QA-230 (2026-10-28) |
| 47 | Deactivate ticker | `DELETE /ticker-universe/{ticker}` | `pages/TickerUniverse.js:247` | Covered | `ticker-universe.spec.js` |
| 48 | Run replay | `POST /replay/run` | `pages/Replay.js:109` | Covered | `replay-mode.spec.js`, `accessibility-axe-scan.spec.js` |
| 49 | Generate monthly P&L narrative | `POST /reports/monthly-pnl/narrative` | `components/reports/MonthlyNarrativeCard.js:88` | Covered | `monthly-pnl-narrative.spec.js` |
| 50 | Run rule-change backtest | `POST /strategy/backtest-rule-change/run` | `pages/StrategyBenchmark.js` → `base44Client.js:595` | Covered | `backtest-rule-change.spec.js` |
| 51 | Test all endpoints (System Status) | `POST /test/endpoints` | `pages/SystemStatus.js:210` | Covered | `system-status.spec.js` |
| 52 | Run calculation validation (System Status) | `POST /validate/calculations` | `pages/SystemStatus.js:238` | Not covered | BLG-QA-230 (2026-10-28) |

**Totals:** 52 primary actions; 37 covered; 15 not covered, all tracked in BLG-QA-230 (dated 2026-10-28).

## Client Methods With No Caller

These methods send a state-changing request but nothing in `src/` calls them, so they are not user actions. ST-23's check allow-lists the three whose route is missing from `openapi.yaml`.

| Method | Request | Call site | Tracking |
|--------|---------|-----------|----------|
| `Signal.create` | `POST /signals` (no route) | `base44Client.js:340` | BLG-FE-230 |
| `exchangeCodeForToken` | `POST /auth/callback` (no route) | `base44Client.js:161` | BLG-FE-230 |
| `getPublicSettingsById` | `GET /apps/public/prod/public-settings/by-id/{id}` (no route; not state-changing) | `base44Client.js:87` | BLG-FE-230 |
| `Signal.delete` | `DELETE /signals/{id}` | `base44Client.js:352` | BLG-FE-235 (2026-10-28) |
| `Signal.generate` | `POST /signals/generate` | `base44Client.js:357` | BLG-FE-235 (2026-10-28) |
| `createSnapshot` | `POST /portfolio/snapshot` | `base44Client.js:398` | BLG-FE-235 (2026-10-28) |
| `trades.updateCosts` | `PATCH /trades/{id}/costs` | `base44Client.js:445` | BLG-FE-235 (2026-10-28) |
| `importData` (strategy benchmark) | `POST /strategy/benchmark/import` | `base44Client.js:570` | BLG-FE-235 (2026-10-28) |

## Notes

- **Unanswered request in an existing test.** `position-review-cadence-nudge.spec.js` SC-RCN-06 mocks `**/positions*`, a glob that does not match `/positions/{id}/mark-reviewed`. The PATCH is sent and the test passes on `waitForRequest`, but no mock answers it. The action counts as covered (the request is asserted). The missing response is recorded in BLG-QA-230's scope.
- **Related:** `scripts/check_frontend_api_calls.py` (ST-23) is the static half of this control: it fails CI on a call to a route missing from `openapi.yaml`. The guard fixture is the runtime half.
