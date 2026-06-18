**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-06-17
**Source:** BLG-QA-50 — v5.5 ST-09; refreshed v5.9 ST-10

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

**Total spec files:** 41 (42 after v5.9 ST-11 Playwright spec is merged)
**Total scenarios:** 391 (as of v5.9 pre-ST-11)

Source directory: `tests/e2e/`

| Spec File | Scenarios | Feature / Area | Introduced |
|-----------|-----------|----------------|------------|
| alert-nav-badge.spec.js | 8 | Alert navigation badge | v2.3 |
| alert-thresholds-empty-state.spec.js | 13 | Alert thresholds empty state | v2.3 |
| arc5-compliance-section.spec.js | 5 | Arc 5 compliance UI section | v4.0 |
| chart-interactivity.spec.js | 21 | Chart interaction behaviours | v3.0 |
| compliance-panel.spec.js | 7 | Compliance panel | v2.0 |
| earnings-calendar.spec.js | 9 | Earnings calendar UI | v3.1 |
| entry-checklist.spec.js | 7 | Pre-entry checklist | v3.1 |
| epic01-v34-lifecycle.spec.js | 10 | v3.4 EPIC-01 lifecycle scenarios | v3.4 |
| epic02-v34-risk-prompts.spec.js | 10 | v3.4 EPIC-02 risk prompts | v3.4 |
| epic03-v34-frontend.spec.js | 16 | v3.4 EPIC-03 frontend | v3.4 |
| fee-drag-trade-history.spec.js | 7 | Fee drag in trade history | v3.6 |
| keyboard-shortcuts.spec.js | 11 | Keyboard shortcuts | v3.0 |
| loading-states.spec.js | 13 | Loading state indicators | v2.5 |
| market-correlation.spec.js | 8 | Market correlation panel | v3.0 |
| notifications.spec.js | 9 | Notifications UI | v2.3 |
| paper-account.spec.js | 5 | Paper trading account | v3.5 |
| plan-vs-reality.spec.js | 12 | Plan vs reality comparison | v3.5 |
| positions-pnl-columns.spec.js | 4 | Positions P&L column display | v3.2 |
| pre-trade-research.spec.js | 16 | Pre-trade research view | v3.1 |
| red-flag-journal.spec.js | 4 | Red flag journal | v3.9 |
| reports-performance-tab.spec.js | 13 | Reports performance tab | v3.1 |
| research-typography.spec.js | 5 | Research view typography | v3.3 |
| research-view-signal-type.spec.js | 4 | Research view signal type | v3.3 |
| risk-dashboard.spec.js | 17 | Risk dashboard | v3.4 |
| screener-uk-suffix.spec.js | 4 | Screener UK suffix handling | v3.0 |
| screener.spec.js | 20 | Screener full suite | v3.0 |
| si01-si03-integration.spec.js | 10 | SI-01/SI-03 integration | v3.9 |
| si05-digest-delivery.spec.js | 4 | SI-05 digest delivery | v5.1 |
| sidebar-nav-groups.spec.js | 8 | Sidebar navigation groups | v3.3 |
| signals-add-to-watchlist.spec.js | 3 | Signal watchlist add | v5.3 |
| signals-allocation-insufficient.spec.js | 5 | Allocation insufficient signal flow | v5.0 |
| signals-cash-balance.spec.js | 4 | Signals cash balance display | v5.0 |
| slippage-tracking.spec.js | 8 | Slippage tracking | v3.6 |
| smoke-critical-paths.spec.js | 3 | Smoke — critical paths | v2.0 |
| staleness-indicator.spec.js | 5 | Data staleness indicator | v3.2 |
| system-status.spec.js | 16 | System status page | v2.5 |
| ticker-universe.spec.js | 21 | Ticker universe management | v3.0 |
| trade-plan-signal-context.spec.js | 4 | Trade plan signal context | v3.1 |
| trade-plan.spec.js | 23 | Trade plan full suite | v3.1 |
| visual-snapshots.spec.js | 14 | Visual snapshot regression | v3.4 |
| weekly-digest.spec.js | 5 | Weekly digest | v2.3 |

---

## Part 3 — Coverage Summary by Arc

| Arc | Description | Backend Endpoints | E2E Spec Files |
|-----|-------------|-------------------|----------------|
| Core | Root, health, settings, positions, trades, cash, market | 15 | smoke-critical-paths, loading-states, staleness-indicator |
| Arc 1 | Alerts, notifications, weekly digest | 5 | alert-nav-badge, alert-thresholds-empty-state, notifications, weekly-digest |
| Arc 2 | Analytics, compliance, PT plan vs reality | 9 | compliance-panel, arc5-compliance-section, reports-performance-tab, plan-vs-reality, positions-pnl-columns, chart-interactivity |
| Arc 3 | Position lifecycle, risk dashboard, red flag journal, IT-xx | 8 | epic01-v34-lifecycle, epic02-v34-risk-prompts, risk-dashboard, red-flag-journal, entry-checklist, trade-plan, trade-plan-signal-context |
| Arc 4 | Screener, ticker universe, pre-trade research, trade plans | 11 | screener, screener-uk-suffix, ticker-universe, pre-trade-research, research-typography, research-view-signal-type, earnings-calendar |
| Arc 5 | SI-01/02/03/05, signals, paper trading, AI | 12 | si01-si03-integration, si05-digest-delivery, signals-add-to-watchlist, signals-allocation-insufficient, signals-cash-balance, paper-account, keyboard-shortcuts, sidebar-nav-groups |
| Ops/QA | System status, validation, market correlation, visual regression | 6 | system-status, market-correlation, slippage-tracking, fee-drag-trade-history, visual-snapshots, epic03-v34-frontend |

---

## Part 4 — Regression Run Classification

### Critical Path (must pass before any deploy)

Endpoints: 12 critical endpoints (entries 1–4, 8, 9, 10, 12, 15, 21, 52, 60 in Part 1)

E2E smoke: `smoke-critical-paths.spec.js` (3 scenarios)

### Full Regression (pre-release gate)

All 66 endpoint tests + all 41 spec files (391 scenarios; 42 files/≥393 scenarios after v5.9 ST-11 merge)

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

---

## Change History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2026-06-11 | Initial baseline — 66 endpoints, 41 spec files, 387 scenarios as of v5.5 | Sprint Execution Engine (v5.5 ST-09) |
| 1.1 | 2026-06-17 | v5.9 refresh: scenario counts corrected (391 total; 3 spec files gained scenarios since v5.5 — si01-si03-integration +2, arc5-compliance-section +1, red-flag-journal +1); header count corrected; pending: v5.9 ST-11 spec to add 42nd file | Sprint Execution Engine (v5.9 ST-10) |

---

## Director of Quality Sign-Off (ST-10 AC-04)

- Signed off by: Director of Quality
- Date: 2026-06-18
- Comments: Regression baseline v1.1 reviewed. 66 backend endpoints mapped (AC-02 ✓), 41 Playwright spec files listed with scenario counts and feature mapping (AC-03 ✓). Known gaps section present and correctly caveated. No sealed artefacts modified. Document constitutes the authoritative regression baseline from v5.9.
