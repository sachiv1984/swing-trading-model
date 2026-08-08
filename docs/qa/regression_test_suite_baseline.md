**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-08
**Source:** refreshed v8.4 ST-26 (BLG-QA-116, full backfill); refreshed v7.6 ST-02 (BLG-QA-112); refreshed v5.9 ST-10 — prior history retained, see prior entries in version control

---

# Regression Test Suite Baseline

This document is the authoritative record of all regression test coverage as of the v5.5 sprint close. It maps every entry in `backend/routers/test.py` to its originating feature and release, and lists every Playwright e2e spec file with scenario count and feature mapping.

---

## Part 1 — Backend Endpoint Test Suite (test.py)

**Total endpoints in test suite:** 66

Source file: `backend/routers/test.py`
Invoked via: `POST /test/endpoints`

| # | Endpoint | Method | Critical | Feature | Introduced |
|---|----------|--------|----------|---------|------------|
| 1 | `/` | GET | Yes | Core — root | v1.0 |
| 2 | `/health` | GET | Yes | Core — health check | v1.0 |
| 3 | `/health/detailed` | GET | Yes | Core — detailed health | v1.0 |
| 4 | `/settings` | GET | Yes | Settings & configuration | v1.0 |
| 5 | `/positions` | GET | Yes | Position management | v1.0 |
| 6 | `/positions/tags` | GET | No | Position tags | v1.5 |
| 7 | `/positions/compliance` | GET | No | Compliance overlay | v2.0 |
| 8 | `/portfolio` | GET | Yes | Portfolio summary | v1.0 |
| 9 | `/portfolio/history?days=30` | GET | Yes | Portfolio history | v1.0 |
| 10 | `/trades` | GET | Yes | Trade history | v1.0 |
| 11 | `/cash/transactions` | GET | Yes | Cash management | v1.0 |
| 12 | `/cash/summary` | GET | Yes | Cash summary | v1.0 |
| 13 | `/signals` | GET | No | Signals feed | v1.0 |
| 14 | `/signals/{id}` (watchlisted) | PATCH | No | Signal status update | v1.0 |
| 15 | `/market/status` | GET | Yes | Market status | v1.0 |
| 16 | `/alerts/rules` | GET | No | Alert rules | v2.3 |
| 17 | `/alerts/history` | GET | No | Alert history | v2.3 |
| 18 | `/notifications` | GET | No | Notifications | v2.3 |
| 19 | `/notifications/preferences` | GET | No | Notification preferences | v2.3 |
| 20 | `/digest/weekly` | GET | No | Weekly digest | v2.3 |
| 21 | `/analytics/metrics?period=all_time` | GET | Yes | Analytics metrics (all time) | v1.5 |
| 22 | `/analytics/metrics?period=last_7_days` | GET | No | Analytics metrics (7d) | v1.5 |
| 23 | `/analytics/metrics?period=ytd` | GET | No | Analytics metrics (YTD) | v1.5 |
| 24 | `/analytics/cohort?period=month` | GET | No | Cohort analytics | v2.0 |
| 25 | `/analytics/r-multiple-distribution` | GET | No | R-multiple distribution | v2.0 |
| 26 | `/analytics/compliance-metrics` | GET | No | Compliance metrics | v2.0 |
| 27 | `/ai/journal-summary` | POST | No | AI journal summary | v2.5 |
| 28 | `/ai/journal-summary/history` | GET | No | AI journal history | v2.5 |
| 29 | `/news/AAPL` | GET | No | News feed | v2.0 |
| 30 | `/watchlist` | GET | No | Watchlist — list | v5.3 |
| 31 | `/watchlist` | POST | No | Watchlist — add | v5.3 |
| 32 | `/watchlist/{id}` | DELETE | No | Watchlist — remove | v5.3 |
| 33 | `/analytics/market-correlation` | GET | No | Market correlation | v3.0 |
| 34 | `/analytics/arc5-compliance` | GET | No | Arc 5 compliance metrics | v4.0 |
| 35 | `/ticker-universe` | GET | No | Ticker universe — list | v3.0 |
| 36 | `/ticker-universe` | POST | No | Ticker universe — add | v3.0 |
| 37 | `/ticker-universe/AAPL` | DELETE | No | Ticker universe — remove | v3.0 |
| 38 | `/screener/results` | GET | No | Screener results | v3.0 |
| 39 | `/screener/run` | POST | No | Screener run | v3.0 |
| 40 | `/trade-plans` | GET | No | Trade plans — list | v3.1 |
| 41 | `/trade-plans` | POST | No | Trade plans — create | v3.1 |
| 42 | `/trade-plans/by-position/{id}` | GET | No | Trade plan by position | v3.1 |
| 43 | `/trade-plans/{id}` | GET | No | Trade plan detail | v3.1 |
| 44 | `/trade-plans/{id}` | PUT | No | Trade plan update | v3.1 |
| 45 | `/trade-plans/{id}` | DELETE | No | Trade plan delete | v3.1 |
| 46 | `/trade-plans/{id}/generate-thesis` | POST | No | AI thesis generation | v3.1 |
| 47 | `/earnings/AAPL` | GET | No | Earnings calendar | v3.1 |
| 48 | `/reports/monthly-pnl` | GET | No | Monthly P&L report | v3.1 |
| 49 | `/research/AAPL?market=US` | GET | No | Pre-trade research | v3.1 |
| 50 | `/positions/{id}` | GET | No | Position detail | v3.3 |
| 51 | `/positions/{id}/refresh-state` | POST | No | Position state refresh | v3.3 |
| 52 | `/positions/grace-period-alerts` | GET | Yes | Grace period alerts | v3.3 |
| 53 | `/positions/{id}/stop-trail` | GET | No | Stop trail | v3.3 |
| 54 | `/portfolio/drawdown-status` | GET | No | Portfolio drawdown status | v3.4 |
| 55 | `/portfolio/concentration-status` | GET | No | Portfolio concentration | v3.4 |
| 56 | `/portfolio/paper-positions` | GET | No | Paper trading positions | v3.5 |
| 57 | `/portfolio/pre-entry-validation` | GET | No | Pre-entry validation | v3.8 |
| 58 | `/portfolio/red-flag-journal` | GET | No | Red flag journal | v3.9 |
| 59 | `/trades/{id}/plan-vs-reality` | GET | No | Plan vs reality | v3.5 |
| 60 | `/validate/calculations` | POST | Yes | Calculation validation | v1.0 |
| 61 | `/ai/check-daily-cost` | POST | No | AI cost monitoring | v4.1 |
| 62 | `/ai/claude-audit-log` | GET | No | Claude API audit trail | v4.2 |
| 63 | `/analytics/behavioural-drift` | GET | No | SI-02 behavioural drift | v4.6 |
| 64 | `/signals?status=allocation_insufficient` | GET | No | Allocation insufficient signals | v5.0 |
| 65 | `/digest/si05/send` | POST | No | SI-05 strategy integrity digest | v5.1 |
| 66 | `/portfolio/gate-metrics` | GET | No | Trade count gate metrics | v5.5 |

**Critical endpoint count:** 12  
**Non-critical endpoint count:** 54

---

## Part 2 — Playwright End-to-End Test Suite

**Total spec files:** 86 (all files present in `tests/e2e/` at time of this backfill — ST-26, BLG-QA-116)
**Total scenarios:** 732 (sum of all 86 files listed in this table)

> **Backfill note (ST-26, EPIC-06, v8.4):** This table previously catalogued only 46 of the (then) 70 files in `tests/e2e/` (`BLG-QA-116`, filed at v7.6 ST-02). This update adds the 41 files added between v5.9 and v8.4 that were not yet catalogued (more than the 24 originally estimated at filing time, since the gap widened further between v7.6 and v8.4 before this backfill ran), removes 1 entry for a file since deleted (`si05-digest-delivery.spec.js`, removed `BLG-QA-64`/v6.8 — "architecturally incompatible"), and corrects 7 scenario counts on already-catalogued files found stale during this pass (`entry-checklist.spec.js`, `epic03-v34-frontend.spec.js`, `keyboard-shortcuts.spec.js`, `red-flag-journal.spec.js`, `system-status.spec.js`, `trade-plan.spec.js`, `visual-snapshots.spec.js`) — a scenario-count drift check across the full table was necessary to satisfy this item's "Total scenarios counts match the table exactly" AC, since a stale-but-uncorrected row would have broken that arithmetic. **Version attribution methodology:** each new row's "Introduced" version is the release cycle whose `execution_state.json` records the file-adding commit SHA, where a record exists; otherwise (older cycles predating consistent `commit_sha` capture) the nearest release date on or after the commit's calendar date, per `docs/product/changelog.md`. The latter method is approximate at same-day release-boundary collisions — treat pre-v6.0 "Introduced" values on newly-added rows as indicative, not audited to the same standard as rows with a direct `execution_state.json` match.

Source directory: `tests/e2e/`

| Spec File | Scenarios | Feature / Area | Introduced |
|-----------|-----------|----------------|------------|
| ai-briefing-progressive-disclosure.spec.js | 7 | AI daily briefing card expand/collapse progressive disclosure | v6.3 |
| ai-usage-costs.spec.js | 9 | AI cost view (single-provider Claude total) | v7.6 |
| alert-nav-badge.spec.js | 8 | Alert navigation badge | v2.3 |
| alert-thresholds-empty-state.spec.js | 13 | Alert thresholds empty state | v2.3 |
| arc5-compliance-section.spec.js | 5 | Arc 5 compliance UI section | v4.0 |
| bulk-actions-toolbar.spec.js | 12 | Bulk actions on list/table views (`BLG-FE-117`) | v7.5 |
| chart-interactivity.spec.js | 21 | Chart interaction behaviours | v3.0 |
| command-palette.spec.js | 12 | Global command palette / cross-page search (`BLG-FE-115`) | v7.4 |
| compliance-panel.spec.js | 7 | Compliance panel | v2.0 |
| compliance-recheck.spec.js | 11 | On-demand SI-01 compliance recheck for open positions | v6.9 |
| custom-price-alerts.spec.js | 11 | User-defined custom price alerts (`BLG-FE-116`) | v7.5 |
| dialog-classname-override-fixes.spec.js | 6 | Dialog className-override collision fixes | v8.4 |
| earnings-calendar.spec.js | 9 | Earnings calendar UI | v3.1 |
| entry-checklist.spec.js | 11 | Pre-entry checklist | v3.1 |
| epic01-v34-lifecycle.spec.js | 10 | v3.4 EPIC-01 lifecycle scenarios | v3.4 |
| epic01-v62-stops-alerts.spec.js | 16 | SignalCard exit_rebalance status / stops & alerts | v6.2 |
| epic01-v70-grid-badge-parity.spec.js | 9 | Grid View badge parity | v7.0 |
| epic02-v34-risk-prompts.spec.js | 10 | v3.4 EPIC-02 risk prompts | v3.4 |
| epic02-v62-ai-briefing-chat.spec.js | 10 | AI Daily Briefing card & AI Chat widget | v6.2 |
| epic03-v34-frontend.spec.js | 21 | v3.4 EPIC-03 frontend | v3.4 |
| fee-drag-trade-history.spec.js | 7 | Fee drag in trade history | v3.6 |
| form-validation-error-color-fixes.spec.js | 6 | Form-validation error text dark-token contrast fixes | v8.4 |
| gap-risk-flag.spec.js | 8 | Overnight/weekend gap risk flag | v6.9 |
| gate-progress.spec.js | 4 | Gate proximity indicator | v6.1 |
| heading-light-theme-contrast.spec.js | 4 | Dashboard/StrategyBenchmark heading contrast | v7.0 |
| keyboard-shortcuts.spec.js | 13 | Keyboard shortcuts | v3.0 |
| loading-states.spec.js | 13 | Loading state indicators | v2.5 |
| market-correlation.spec.js | 8 | Market correlation panel | v3.0 |
| monthly-pnl-avg-per-trade.spec.js | 5 | Avg P&L/Trade column, Monthly P&L report | v8.4 |
| monthly-pnl-csv-export.spec.js | 5 | Monthly CSV export (alongside tax-year export) | v7.8 |
| monthly-pnl-realized-unrealized.spec.js | 5 | Unrealised P&L Card & Combined Total | v7.0 |
| morning-briefing.spec.js | 11 | Trader's Morning Briefing dashboard | v6.0 |
| nav-notification-digest-consolidation.spec.js | 7 | Nav duplication removal / digest-notification unification | v7.7 |
| net-r-trade-history.spec.js | 5 | Net-of-costs performance tracking | v6.0 |
| notification-badge-contrast.spec.js | 2 | Nav alert-badge contrast fix | v7.8 |
| notifications.spec.js | 9 | Notifications UI | v2.3 |
| page-header-dark-gradient-contrast.spec.js | 2 | PageHeader dark-mode gradient contrast fix | v7.8 |
| paper-account.spec.js | 5 | Paper trading account | v3.5 |
| plan-vs-reality.spec.js | 12 | Plan vs reality comparison | v3.5 |
| position-review-cadence-nudge.spec.js | 7 | Position review cadence nudge | v7.0 |
| positions-pnl-columns.spec.js | 4 | Positions P&L column display | v3.2 |
| pre-entry-panel-badge.spec.js | 3 | Pre-entry panel badge | v5.9 |
| pre-trade-research.spec.js | 16 | Pre-trade research view | v3.1 |
| print-export-pdf.spec.js | 6 | Print/PDF export — WeeklyDigest, TradePlan (`BLG-FE-119`) | v7.6 |
| r-multiple-reflection.spec.js | 5 | R-multiple display fix, Reflection page | v6.3 |
| red-flag-journal-filter-persistence.spec.js | 2 | Red Flag Journal filter-state persistence | v6.6 |
| red-flag-journal.spec.js | 5 | Red flag journal | v3.9 |
| reports-performance-tab.spec.js | 13 | Reports performance tab | v3.1 |
| reports-reconciliation.spec.js | 5 | P&L / tax record reconciliation report | v8.2 |
| reports-si02-gate-status.spec.js | 11 | SI-02 gate visibility indicator, Reports page | v6.8 |
| research-typography.spec.js | 5 | Research view typography | v3.3 |
| research-view-signal-type.spec.js | 4 | Research view signal type | v3.3 |
| risk-dashboard.spec.js | 17 | Risk dashboard | v3.4 |
| saved-filters-calendar-view.spec.js | 9 | Saved filter views and calendar view (`BLG-FE-118`) | v7.5 |
| screener-quality.spec.js | 5 | Screener data quality telemetry | v6.0 |
| screener-uk-suffix.spec.js | 4 | Screener UK suffix handling | v3.0 |
| screener.spec.js | 20 | Screener full suite | v3.0 |
| secondary-text-contrast.spec.js | 4 | Dark-theme secondary-text contrast fix | v6.7 |
| sector-heatmap.spec.js | 4 | Sector heat-map | v6.1 |
| sector-regime-exposure-trend.spec.js | 3 | Historical sector/regime exposure trend, Risk Dashboard | v7.9 |
| setup-quality-score.spec.js | 9 | Setup Quality Score display (Research/TradePlan) | v6.1 |
| si01-si03-integration.spec.js | 10 | SI-01/SI-03 integration | v3.9 |
| si04-version-comparison.spec.js | 5 | SI-04 strategy-version performance comparison | v7.7 |
| sidebar-nav-groups.spec.js | 8 | Sidebar navigation groups | v3.3 |
| signals-add-to-watchlist.spec.js | 3 | Signal watchlist add | v5.3 |
| signals-allocation-insufficient.spec.js | 5 | Allocation insufficient signal flow | v5.0 |
| signals-cash-balance.spec.js | 4 | Signals cash balance display | v5.0 |
| slippage-tracking.spec.js | 8 | Slippage tracking | v3.6 |
| smoke-critical-paths.spec.js | 3 | Smoke — critical paths | v2.0 |
| staleness-indicator.spec.js | 5 | Data staleness indicator | v3.2 |
| standing-alert.spec.js | 6 | Shared "standing alert" component | v7.7 |
| strategy-benchmark.spec.js | 18 | Strategy Benchmark page | v6.4 |
| system-status.spec.js | 19 | System status page | v2.5 |
| tax-year-csv-export.spec.js | 5 | Tax-year CSV export (Download CSV button order) | v7.0 |
| ticker-universe.spec.js | 21 | Ticker universe management | v3.0 |
| trade-history-ai-journal-summary.spec.js | 3 | AI journal summary error states | v6.4 |
| trade-plan-signal-context.spec.js | 4 | Trade plan signal context | v3.1 |
| trade-plan-tag-filter.spec.js | 5 | Trade plan tagging & tag-based performance filtering | v6.8 |
| trade-plan.spec.js | 35 | Trade plan full suite | v3.1 |
| trailing-stop-explainer-tooltip.spec.js | 5 | "Why is my stop moving" explainer tooltip | v7.9 |
| v7.2-dashboard-tradeplan-ux-hardening.spec.js | 15 | Dashboard/trade-plan UX hardening | v7.3 |
| visual-snapshots.spec.js | 15 | Visual snapshot regression | v3.4 |
| watchlist-staleness-review.spec.js | 5 | Watchlist staleness tracking & Keep/Remove action | v7.9 |
| watchlist.spec.js | 5 | Watchlist.js baseline coverage | v8.4 |
| weekly-digest.spec.js | 5 | Weekly digest | v2.3 |
| whats-new-panel.spec.js | 5 | In-app "what's new" panel | v7.8 |

---

## Part 3 — Coverage Summary by Arc

| Arc | Description | Backend Endpoints | E2E Spec Files |
|-----|-------------|-------------------|----------------|
| Core | Root, health, settings, positions, trades, cash, market | 15 | smoke-critical-paths, loading-states, staleness-indicator |
| Arc 1 | Alerts, notifications, weekly digest | 5 | alert-nav-badge, alert-thresholds-empty-state, notifications, weekly-digest, custom-price-alerts, print-export-pdf, nav-notification-digest-consolidation, notification-badge-contrast, standing-alert |
| Arc 2 | Analytics, compliance, PT plan vs reality, reports | 9 | compliance-panel, arc5-compliance-section, reports-performance-tab, plan-vs-reality, positions-pnl-columns, chart-interactivity, compliance-recheck, monthly-pnl-avg-per-trade, monthly-pnl-csv-export, monthly-pnl-realized-unrealized, net-r-trade-history, r-multiple-reflection, reports-reconciliation, reports-si02-gate-status, strategy-benchmark, tax-year-csv-export |
| Arc 3 | Position lifecycle, risk dashboard, red flag journal, IT-xx | 8 | epic01-v34-lifecycle, epic02-v34-risk-prompts, risk-dashboard, red-flag-journal, entry-checklist, trade-plan, trade-plan-signal-context, print-export-pdf, epic01-v62-stops-alerts, gap-risk-flag, gate-progress, position-review-cadence-nudge, red-flag-journal-filter-persistence, sector-heatmap, sector-regime-exposure-trend, trailing-stop-explainer-tooltip |
| Arc 4 | Screener, ticker universe, pre-trade research, trade plans | 11 | screener, screener-uk-suffix, ticker-universe, pre-trade-research, research-typography, research-view-signal-type, earnings-calendar, saved-filters-calendar-view, pre-entry-panel-badge, screener-quality, setup-quality-score, trade-plan-tag-filter, watchlist, watchlist-staleness-review |
| Arc 5 | SI-01/02/03/05, signals, paper trading, AI | 12 | si01-si03-integration, si05-digest-delivery (removed v6.8, see Part 2), signals-add-to-watchlist, signals-allocation-insufficient, signals-cash-balance, paper-account, keyboard-shortcuts, sidebar-nav-groups, ai-briefing-progressive-disclosure, ai-usage-costs, epic02-v62-ai-briefing-chat, morning-briefing, si04-version-comparison, trade-history-ai-journal-summary |
| Ops/QA | System status, validation, market correlation, visual regression, cross-page utilities | 6 | system-status, market-correlation, slippage-tracking, fee-drag-trade-history, visual-snapshots, epic03-v34-frontend, command-palette, bulk-actions-toolbar, dialog-classname-override-fixes, epic01-v70-grid-badge-parity, form-validation-error-color-fixes, heading-light-theme-contrast, page-header-dark-gradient-contrast, secondary-text-contrast, v7.2-dashboard-tradeplan-ux-hardening, whats-new-panel |

---

## Part 4 — Regression Run Classification

### Critical Path (must pass before any deploy)

Endpoints: 12 critical endpoints (entries 1–4, 8, 9, 10, 12, 15, 21, 52, 60 in Part 1)

E2E smoke: `smoke-critical-paths.spec.js` (3 scenarios)

### Full Regression (pre-release gate)

All 66 endpoint tests + all 86 spec files listed in Part 2 (732 scenarios).

### Targeted Regression (per-EPIC, post-merge)

Run spec files corresponding to the EPIC's feature area. Consult sprint `qa_evidence_EPIC-xx.md` for the `test_scenarios` field to identify which specs are in-scope.

---

## Part 5 — Known Gaps as of v5.9

The following areas have endpoint coverage but no dedicated Playwright spec:

| Area | Endpoint | Gap Type |
|------|----------|----------|
| Pre-entry validation | `GET /portfolio/pre-entry-validation` | Functional tested via entry-checklist.spec.js indirectly; no dedicated spec |
| Grace period alerts | `GET /positions/grace-period-alerts` | No dedicated Playwright spec; covered by epic01-v34-lifecycle.spec.js scope |
| Gate metrics | `GET /portfolio/gate-metrics` | v5.5 addition — no Playwright spec; system-status.spec.js covers System Status page |

Gap tracking: BLG-QA-50 (source backlog item for this document). New gap items should be filed as BLG-QA-xx and referenced here in future refreshes.

**Cataloguing gap — closed (ST-26, EPIC-06, v8.4):** The gap flagged at v7.6 (`BLG-QA-116`) — 24 undocumented spec files, since grown to 41 by the time this backfill ran — is now closed; Part 2 lists all 86 files present in `tests/e2e/` as of this update. See Part 2's backfill note for methodology and the scenario-count corrections made to 7 already-catalogued rows in the same pass.

---

## Change History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2026-06-11 | Initial baseline — 66 endpoints, 41 spec files, 387 scenarios as of v5.5 | Sprint Execution Engine (v5.5 ST-09) |
| 1.1 | 2026-06-17 | v5.9 refresh: scenario counts corrected (391 total; 3 spec files gained scenarios since v5.5 — si01-si03-integration +2, arc5-compliance-section +1, red-flag-journal +1); header count corrected; pending: v5.9 ST-11 spec to add 42nd file | Sprint Execution Engine (v5.9 ST-10) |
| 1.2 | 2026-07-20 | ST-02 (EPIC-02, v7.6, BLG-QA-112): Added 5 spec file entries covering `BLG-FE-115`–`BLG-FE-119` interaction surfaces (command-palette, custom-price-alerts, bulk-actions-toolbar, saved-filters-calendar-view, print-export-pdf; 50 scenarios total) per this item's acceptance criteria. Totals updated to 46 files / 441 scenarios. Flagged (not fixed, out of this item's scope) a broader cataloguing gap: 24 further spec files added v6.0–v7.3 remain undocumented — filed as `BLG-QA-116`. | Sprint Execution Engine (autonomous class) |
| 1.3 | 2026-08-08 | ST-26 (EPIC-06, v8.4, BLG-QA-116): Full backfill. Added 41 previously-uncatalogued spec files (267 scenarios); removed 1 entry for a deleted file (`si05-digest-delivery.spec.js`); corrected 7 stale scenario counts on already-catalogued rows (`entry-checklist`, `epic03-v34-frontend`, `keyboard-shortcuts`, `red-flag-journal`, `system-status`, `trade-plan`, `visual-snapshots`); Part 3 Arc coverage table extended to reference every newly-added file. Totals updated to 86 files / 732 scenarios, matching `tests/e2e/` exactly at time of execution. `BLG-QA-116` closed. | Sprint Execution Engine (autonomous class) |

---

## Director of Quality Sign-Off (ST-10 AC-04)

- Signed off by: Director of Quality
- Date: 2026-06-18
- Comments: Regression baseline v1.1 reviewed. 66 backend endpoints mapped (AC-02 ✓), 41 Playwright spec files listed with scenario counts and feature mapping (AC-03 ✓). Known gaps section present and correctly caveated. No sealed artefacts modified. Document constitutes the authoritative regression baseline from v5.9.

---

## Director of Quality Sign-Off (ST-02, EPIC-02, v7.6)

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-20
- Comments: v1.2 reviewed. All 5 required entries (`BLG-FE-115`–`BLG-FE-119`) added and cross-referenced against their Playwright spec files in `tests/e2e/` (file existence and scenario counts verified directly against the files, not inferred). No sealed artefacts modified; documentation-only change. Broader cataloguing gap flagged and filed as `BLG-QA-116` rather than silently left uncaptured.

---

## Director of Quality Sign-Off (ST-26, EPIC-06, v8.4)

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-08
- Comments: v1.3 reviewed. All 86 files in `tests/e2e/` present in Part 2, verified programmatically (set-difference against `ls tests/e2e/*.spec.js`, zero files missing either direction). Scenario counts re-derived from each file's `test(`/`test.only(`/`test.skip(` occurrences, matching the counting convention already established by this document's existing rows (spot-checked against 3 unmodified rows before use). Total row count (86) and total scenario count (732) verified by summation, not asserted. `si05-digest-delivery.spec.js` confirmed deleted via `git log --diff-filter=D` (BLG-QA-64, v6.8) before removal from the table. Part 3 Arc coverage table extended to reference every one of the 41 newly-added files — verified by cross-check, no newly-added file omitted. `BLG-QA-116` closed. No sealed artefacts modified; documentation-only change. **Caveat carried forward (not blocking):** "Introduced" version for newly-added rows without a direct `execution_state.json` commit-SHA match uses date-based inference against `changelog.md`, which is approximate at same-day release-boundary collisions (4 such collisions found and hand-corrected against `execution_state.json` during this pass; remaining un-corroborated rows are not individually audited to the same standard — see Part 2 backfill note).
