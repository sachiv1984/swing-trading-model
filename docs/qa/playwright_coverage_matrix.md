**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.5
**Last Updated:** 2026-09-16 (ST-18, BLG-QA-167, v9.5 — §2 Spec File Index fully re-derived, 39→104 files corrected); prior — 2026-09-09 (ST-05, BLG-QA-82, v9.3 — SignalCard rows consolidated to signal-card.spec.js; stale total-count gap filed as BLG-QA-167); prior history retained — see prior entries in version control.
**Cycle:** 2026-06-01__release-v4.8 (ST-06 — BLG-QA-39); 2026-09-09__release-v9.3 (ST-05 — BLG-QA-82); 2026-09-15__release-v9.5 (ST-18 — BLG-QA-167)

---

# Playwright Scenario Coverage Matrix

## 1. Purpose

This matrix maps delivered features and stories (v3.7–v4.2) to their Playwright E2E test coverage. It identifies features with zero automated coverage and flags staging-only ACs that are not amenable to Playwright automation.

---

## 2. Spec File Index

| Spec File | Scenarios | Primary Features Covered |
|-----------|----------|--------------------------|
| `accessibility-axe-scan.spec.js` | 4 | Standalone axe-core WCAG accessibility CI scan (ST-21, BLG-QA-83, v9.0) — 4 representative pages, serious/critical violations block |
| `ai-briefing-progressive-disclosure.spec.js` | 7 | AI daily briefing card expand/collapse progressive disclosure |
| `ai-usage-costs.spec.js` | 9 | AI cost view (single-provider Claude total) |
| `alert-nav-badge.spec.js` | 8 | Alert navigation badge |
| `alert-thresholds-empty-state.spec.js` | 13 | Alert thresholds empty state |
| `analytics-mobile-responsive.spec.js` | 7 | PerformanceAnalytics mobile responsive audit (ST-12, BLG-FE-94, v8.5) — against analytics.md §Responsive Behavior |
| `arc5-compliance-section.spec.js` | 16 | Arc 5 compliance UI section |
| `backtest-rule-change.spec.js` | 5 | Backtest Rule Change tab (ST-07, BLG-FEAT-89, v8.9) — in-app backtesting engine for strategy rule changes |
| `bulk-actions-toolbar.spec.js` | 12 | Bulk actions on list/table views (`BLG-FE-117`) |
| `chart-interactivity.spec.js` | 21 | Chart interaction behaviours |
| `command-palette.spec.js` | 16 | Global command palette / cross-page search (`BLG-FE-115`) |
| `compliance-panel.spec.js` | 7 | Compliance panel |
| `compliance-recheck.spec.js` | 11 | On-demand SI-01 compliance recheck for open positions |
| `custom-price-alerts.spec.js` | 11 | User-defined custom price alerts (`BLG-FE-116`) |
| `dialog-classname-override-fixes.spec.js` | 6 | Dialog className-override collision fixes |
| `earnings-calendar.spec.js` | 9 | Earnings calendar UI |
| `entry-checklist.spec.js` | 11 | Pre-entry checklist |
| `epic01-v34-lifecycle.spec.js` | 10 | v3.4 EPIC-01 lifecycle scenarios |
| `epic01-v62-stops-alerts.spec.js` | 16 | SignalCard exit_rebalance status / stops & alerts |
| `epic01-v70-grid-badge-parity.spec.js` | 9 | Grid View badge parity |
| `epic02-v34-risk-prompts.spec.js` | 10 | v3.4 EPIC-02 risk prompts |
| `epic02-v62-ai-briefing-chat.spec.js` | 11 | AI Daily Briefing card & AI Chat widget |
| `epic03-v34-frontend.spec.js` | 21 | v3.4 EPIC-03 frontend |
| `fee-drag-trade-history.spec.js` | 7 | Fee drag in trade history |
| `form-validation-error-color-fixes.spec.js` | 6 | Form-validation error text dark-token contrast fixes |
| `gap-risk-flag.spec.js` | 8 | Overnight/weekend gap risk flag |
| `gate-progress.spec.js` | 4 | Gate proximity indicator |
| `heading-light-theme-contrast.spec.js` | 4 | Dashboard/StrategyBenchmark heading contrast |
| `keyboard-shortcuts.spec.js` | 13 | Keyboard shortcuts |
| `loading-states.spec.js` | 13 | Loading state indicators |
| `market-correlation.spec.js` | 8 | Market correlation panel |
| `modal-theming-token-conversion.spec.js` | 6 | Modal theming token conversion (ST-06, BLG-FE-156, v8.7) — WatchlistModal/ExportModal/WidgetLibrary shadcn tokens |
| `monthly-pnl-avg-per-trade.spec.js` | 5 | Avg P&L/Trade column, Monthly P&L report |
| `monthly-pnl-csv-export.spec.js` | 5 | Monthly CSV export (alongside tax-year export) |
| `monthly-pnl-realized-unrealized.spec.js` | 5 | Unrealised P&L Card & Combined Total |
| `morning-briefing.spec.js` | 11 | Trader's Morning Briefing dashboard |
| `nav-notification-digest-consolidation.spec.js` | 7 | Nav duplication removal / digest-notification unification |
| `net-r-trade-history.spec.js` | 5 | Net-of-costs performance tracking |
| `notification-badge-contrast.spec.js` | 2 | Nav alert-badge contrast fix |
| `notifications.spec.js` | 12 | Notifications UI |
| `page-header-dark-gradient-contrast.spec.js` | 2 | PageHeader dark-mode gradient contrast fix |
| `paper-account.spec.js` | 5 | Paper trading account |
| `plan-vs-reality.spec.js` | 12 | Plan vs reality comparison |
| `position-review-cadence-nudge.spec.js` | 8 | Position review cadence nudge |
| `position-sizing-concentration.spec.js` | 3 | Concentration-aware position sizing display (ST-04, BLG-BE-104, v8.9) — correlation/sector-concentration-aware sizing |
| `position-stop-currency-basis.spec.js` | 4 | Trailing stop currency basis, card & table view (ST-02, BLG-BE-103, v8.9) — US-market position currency fix |
| `positions-pnl-columns.spec.js` | 4 | Positions P&L column display |
| `pre-entry-panel-badge.spec.js` | 3 | Pre-entry panel badge |
| `pre-trade-research.spec.js` | 16 | Pre-trade research view |
| `price-alert-trade-plan-linkage.spec.js` | 2 | Price-alert-to-trade-plan linkage round trip (ST-09, BLG-BE-84, v8.8) |
| `print-export-pdf.spec.js` | 6 | Print/PDF export — WeeklyDigest, TradePlan (`BLG-FE-119`) |
| `r-multiple-reflection.spec.js` | 5 | R-multiple display fix, Reflection page |
| `red-flag-journal-filter-persistence.spec.js` | 2 | Red Flag Journal filter-state persistence |
| `red-flag-journal.spec.js` | 6 | Red flag journal |
| `reports-performance-tab.spec.js` | 13 | Reports performance tab |
| `reports-realised-pnl-zero-colour-convention.spec.js` | 5 | Realised P&L exact-zero colour convention (ST-08, BLG-FE-144, v8.5) — Tax Year Trades Table |
| `reports-reconciliation.spec.js` | 5 | P&L / tax record reconciliation report |
| `reports-si02-gate-status.spec.js` | 11 | SI-02 gate visibility indicator, Reports page |
| `reports-theme-fix-si02-unrealised-pnl.spec.js` | 4 | SI-02 gate status section + unrealised P&L card light/dark theme fix (ST-04/ST-05, BLG-FE-151/152, v8.7) |
| `research-trade-plan-status-badge.spec.js` | 2 | Research page Trade Plan Status Badge (ST-14, BLG-FE-162, v8.8) — Trade Plan Panel |
| `research-typography.spec.js` | 5 | Research view typography |
| `research-view-signal-type.spec.js` | 4 | Research view signal type |
| `risk-dashboard.spec.js` | 17 | Risk dashboard |
| `saved-filters-calendar-view.spec.js` | 10 | Saved filter views and calendar view (`BLG-FE-118`) |
| `screener-quality.spec.js` | 5 | Screener data quality telemetry |
| `screener-uk-suffix.spec.js` | 4 | Screener UK suffix handling |
| `screener.spec.js` | 24 | Screener full suite |
| `secondary-text-contrast.spec.js` | 4 | Dark-theme secondary-text contrast fix |
| `sector-heatmap.spec.js` | 4 | Sector heat-map |
| `sector-regime-exposure-trend.spec.js` | 3 | Historical sector/regime exposure trend, Risk Dashboard |
| `settings-heading-order-and-aria-labelledby-regression.spec.js` | 4 | Settings heading-order and TradePlan/Settings aria-labelledby pinned regression tests (ST-08, BLG-QA-164, v9.4) |
| `setup-quality-score.spec.js` | 9 | Setup Quality Score display (Research/TradePlan) |
| `setup-thesis-digest.spec.js` | 4 | SetupThesisDigestPanel (ST-02, BLG-FEAT-56, v8.6) |
| `shadcn-token-remaining-families.spec.js` | 5 | Remaining shadcn token call-site families (ST-08/ST-17, BLG-FE-157/160, v8.7/v8.8) — coverage left untested by v8.6/ST-04 |
| `si01-si03-integration.spec.js` | 10 | SI-01/SI-03 integration |
| `si04-version-comparison.spec.js` | 5 | SI-04 strategy-version performance comparison |
| `sidebar-nav-groups.spec.js` | 8 | Sidebar navigation groups |
| `signal-card.spec.js` | 12 | SignalCard: watchlist add, cash balance, allocation-insufficient badge (consolidated v9.3, BLG-QA-82; was 3 files: signals-add-to-watchlist v5.3, signals-allocation-insufficient v5.0, signals-cash-balance v5.0). Runtime evidence: §"SignalCard Consolidation Runtime Evidence" below (v9.5, BLG-QA-169). |
| `slippage-tracking.spec.js` | 8 | Slippage tracking |
| `smoke-critical-paths.spec.js` | 3 | Smoke — critical paths |
| `staleness-indicator.spec.js` | 5 | Data staleness indicator |
| `standing-alert.spec.js` | 6 | Shared "standing alert" component |
| `strategy-benchmark.spec.js` | 18 | Strategy Benchmark page |
| `system-status.spec.js` | 21 | System status page |
| `tax-year-csv-export.spec.js` | 5 | Tax-year CSV export (Download CSV button order) |
| `theme-persistence.spec.js` | 4 | Theme-toggle persistence across sessions (ST-11, BLG-FE-93, v8.5) — audit-only story verifying already-correct behaviour |
| `ticker-universe.spec.js` | 31 | Ticker universe management |
| `trade-debrief.spec.js` | 6 | Automated AI post-trade debrief (ST-06, BLG-FEAT-90, v8.9) — §13 conditional review |
| `trade-history-ai-journal-summary.spec.js` | 3 | AI journal summary error states |
| `trade-plan-completion-rate.spec.js` | 9 | TradePlanCompletionRateSection (ST-01, BLG-FEAT-32, v8.6) |
| `trade-plan-invalidation-link-toast-ai-badge.spec.js` | 6 | Invalidation condition field, link-confirmation toast, AI-draft badge (ST-01/ST-02/ST-03, BLG-FEAT-84/BLG-FE-158/BLG-BE-95, v8.7) |
| `trade-plan-linkage-advisory.spec.js` | 3 | Trade Plan Linkage Advisory (ST-28, BLG-FEAT-95, v9.4) — per position_form.md §Trade Plan Linkage Advisory |
| `trade-plan-signal-context.spec.js` | 4 | Trade plan signal context |
| `trade-plan-tag-filter.spec.js` | 5 | Trade plan tagging & tag-based performance filtering |
| `trade-plan.spec.js` | 41 | Trade plan full suite |
| `trailing-stop-explainer-tooltip.spec.js` | 5 | "Why is my stop moving" explainer tooltip |
| `v7.2-dashboard-tradeplan-ux-hardening.spec.js` | 15 | Dashboard/trade-plan UX hardening |
| `visual-regression-baselines.spec.js` | 5 | First pixel-level toHaveScreenshot() baselines in this app (ST-18, BLG-QA-81, v9.0) |
| `visual-snapshots.spec.js` | 15 | Visual snapshot regression |
| `watchlist-staleness-review.spec.js` | 5 | Watchlist staleness tracking & Keep/Remove action |
| `watchlist.spec.js` | 6 | Watchlist.js baseline coverage |
| `weekly-digest.spec.js` | 5 | Weekly digest |
| `what-if-sizing-preview.spec.js` | 8 | What-If sizing preview (ST-05, BLG-FEAT-91, v8.9) — pre-commit what-if sizing/risk simulator on trade-plan form |
| `whats-new-panel.spec.js` | 6 | In-app "what's new" panel |

**Total: 104 spec files, 874 test scenarios** (re-derived 2026-09-16, ST-18, BLG-QA-167, v9.5 — full re-inventory against `tests/e2e/` directly, `test(`/`test.only(`/`test.skip(` occurrence counting convention matching `regression_test_suite_baseline.md`'s established method)

---

## 3. Feature-to-Coverage Matrix (v3.7–v4.2)

### v3.7 — Signals Workflow

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| Add signal to watchlist (IT-02 partial) | ✅ Covered | `signal-card.spec.js` (consolidated v9.3) | 3 | None |
| Signals cash balance display | ✅ Covered | `signal-card.spec.js` (consolidated v9.3) | 4 | None |
| Screener (signals integration) | ✅ Covered | `screener.spec.js` | 20 | None |

### v3.8 — (No new Playwright coverage added — primarily backend/governance cycle)

| Feature/Story | Playwright Coverage | Notes |
|---------------|--------------------|----|
| No frontend-visible changes delivered in v3.8 | N/A | Governance-only cycle |

### v3.9 — Screener P1 Fixes + SI-03 Red Flag Journal

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| Screener P1 fixes (BLG-FE-20) | ✅ Covered | `screener.spec.js`, `screener-uk-suffix.spec.js` | 24 | None |
| Red Flag Journal page (SI-03 read) | ✅ Covered | `red-flag-journal.spec.js` | 3 | None |
| Staleness indicator | ✅ Covered | `staleness-indicator.spec.js` | 5 | None |

### v4.0 — Arc 5 Analytics + SI Pipeline

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| Arc5ComplianceSection (SI-03 metrics) | ✅ Covered | `arc5-compliance-section.spec.js` | 4 | None |
| SI-01→SI-03 integration path | ✅ Covered | `si01-si03-integration.spec.js` | 8 | None |
| Ticker universe management | ⚠️ File exists, count uncertain | `ticker-universe.spec.js` | — | AC: live Yahoo Finance validation |
| Pre-trade research (IT-01/02) | ✅ Covered | `pre-trade-research.spec.js` | 16 | None (mocked) |
| Risk dashboard (PO-01 Arc 4) | ✅ Covered | `risk-dashboard.spec.js` | 17 | None |
| Paper trading account display | ✅ Covered | `paper-account.spec.js` | 5 | None |

### v4.1 — AI Thesis Generation + Governance

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| AI thesis generation ("Improve with AI" button) | ✅ Covered | `trade-plan.spec.js` | (within 23) | AC-01/02/03 staging-only (BLG-QA-29, deferred ST-06) |
| Ticker validation (Yahoo Finance rejection path) | ⚠️ File exists | `ticker-universe.spec.js` | — | AC-01/02 staging-only (BLG-QA-30, deferred ST-07) |
| Claude daily cost alert | ❌ No Playwright coverage | N/A | 0 | AC-01/02 staging-only (BLG-QA-35, deferred ST-08) |

### v4.2 — Claude Audit Log + Trade Plan Fixes

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| Reports performance tab | ✅ Covered | `reports-performance-tab.spec.js` | 13 | None |
| Pre-entry validation fixes (entry_price) | ✅ Covered | `trade-plan.spec.js` (SC-TP-21) | (within 23) | None |
| Trade plan plan-vs-reality | ✅ Covered | `plan-vs-reality.spec.js` | 12 | None |
| Claude AI copy audit (provider-agnostic text) | ✅ Covered | `trade-plan.spec.js` (SC-TP-22) | (within 23) | None |

### v4.3 — Trade Plan Enhancements + Performance Reports

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| Monthly P&L compliance section (v4.3 ST-18 — strategy_compliance) | ✅ Covered | `reports-performance-tab.spec.js` | (within 13 — SC-REP-01–04) | None |
| Risk prompt framework (v3.4 carry) | ✅ Covered | `epic01-v34-lifecycle.spec.js`, `epic02-v34-risk-prompts.spec.js` | 20 | None |

### v4.4–v4.6 — (No new Playwright coverage added)

| Feature/Story | Playwright Coverage | Notes |
|---------------|--------------------|----|
| Governance-only cycles (v4.4) | N/A | No frontend-visible changes |
| IT-04/IT-05 risk prompt framework patches (v4.4) | N/A | Backend/governance only |
| Arc 5 SI-02 data layer (v4.5–v4.6) | N/A | Backend only; no new UI components |
| SI-02 drift panel §20 (v4.6 conditional — deferred) | N/A | EPIC-02 deferred — gate NOT MET |

### v4.7 — Compliance Summary Field Rename (ST-03)

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| `compliance_summary` field (renamed from `strategy_compliance`; GET /reports/monthly-pnl v0.6) | ✅ Covered | `reports-performance-tab.spec.js` | SC-REP-05 | None |

**Note on SC-REP-05:** The compliance_summary field is covered by SC-REP-05 in `reports-performance-tab.spec.js`. This scenario validates the response shape from `GET /reports/monthly-pnl` including the renamed `compliance_summary` field. Scenario added as part of v4.7 ST-03 contract verification.

**Regression checkpoint:** Any change to the `compliance_summary` field shape, key names, or nesting must be validated against SC-REP-05 before merge.

---

## 3A. Shared Mock Fixture Pattern (ST-05, EPIC-05, v7.6, BLG-QA-114)

**Preferred pattern for new Playwright tests:** `tests/e2e/fixtures/api-mocks.js` — a shared, OpenAPI-derived mock payload factory library. Before hand-rolling an inline mock JSON literal in a new spec file, check whether the endpoint is already covered here.

Rationale: prior to this item, every spec file inlined its own ad hoc mock objects per endpoint (e.g. `custom-price-alerts.spec.js`, `bulk-actions-toolbar.spec.js`, `saved-filters-calendar-view.spec.js` each independently defined `PriceAlert`/`SavedFilter`/bulk-result shapes). A contract change in `openapi.yaml` then required hunting down every spec's inline copy rather than updating one factory. Per `shared_standards.md §18`'s mock-payload advisory (mocks must match the canonical response shape; nested objects must not be flattened), fixture shapes here are derived directly from `docs/reference/openapi.yaml` component schemas (`SavedFilter`, `PriceAlert`, `BulkActionResult`).

**Current coverage:** the endpoints touched by `BLG-SPEC-95`'s v7.4 UI-heavy release readiness bundle — `GET/POST /saved-filters`, `DELETE /saved-filters/{id}`, `GET/POST /price-alerts`, `DELETE /price-alerts/{id}`, `POST /watchlist/bulk-tag`, `DELETE /watchlist/bulk`, `POST /trade-plans/bulk-tag`, `PUT /trade-plans/bulk-archive`, `DELETE /trade-plans/bulk`. Command palette (`BLG-FE-115`) has no fixtures here — v1 introduces no backend endpoint (client-side only, confirmed by that feature's own readiness pass).

**Working example:** `custom-price-alerts.spec.js` was refactored to consume `priceAlertsListOk()`/`priceAlert()` from the shared library in place of its previous inline `EMPTY_PRICE_ALERTS`/`POPULATED_PRICE_ALERTS` literals (byte-identical output verified; all 11 scenarios still pass). Other pre-existing specs (`bulk-actions-toolbar.spec.js`, `saved-filters-calendar-view.spec.js`) were not migrated in this item — migrating a passing spec is optional cleanup, not required; the library is additive and new specs should use it going forward.

**Extending the library:** when a new endpoint needs mocking in a future spec, add a factory function here following the same pattern (defaults matching the OpenAPI example/schema, `...overrides` for scenario-specific fields) rather than inlining another ad hoc object.

---

## 4. Features with Zero Automated Coverage

| Feature | Release | Reason | Recommendation |
|---------|---------|--------|---------------|
| Claude API daily cost alert (POST /ai/check-daily-cost threshold notification) | v4.1 | Telegram integration — cannot mock in Playwright | Manual staging run only (deferred ST-08) |
| Claude audit log page/display | v4.2 | No UI component delivering this to user — API endpoint only | N/A — no frontend rendering |
| Claude AI audit log endpoint (`GET /ai/claude-audit-log`) | v4.2 | Backend API only — data consumed internally | Backend unit test sufficient |

---

## 5. Staging-Only ACs Summary

| AC | Feature | Story | Deferred to |
|----|---------|-------|------------|
| Thesis generation on live staging | v4.1 AI thesis | ST-06 (v4.3 EPIC-02) | Staging run when ST-13 clears |
| Yahoo Finance ticker rejection on staging | v4.0 ticker validation | ST-07 (v4.3 EPIC-02) | Staging run when ST-13 clears |
| Telegram alert fires on daily cost threshold | v4.1 cost alert | ST-08 (v4.3 EPIC-02) | Staging run when ST-13 clears |
| claude-audit-log p50 latency on staging | v4.2 audit log | ST-14 (v4.3 EPIC-03) | Staging run — DEL-20260529-05 |

---

## 6. Review Sign-Off

```
Director of Quality (agent-mediated, QA & Testing Owner role — §5.3)
Date: 2026-09-16

ST-18 (BLG-QA-167, EPIC-03, v9.5): §2 Spec File Index fully re-derived against
tests/e2e/ directly (ls tests/e2e/*.spec.js, 104 files — the stale table
claimed 39). Scenario counts re-counted per file (test(/test.only(/test.skip(
occurrences, same convention as regression_test_suite_baseline.md) — total
874 scenarios. Descriptions sourced from regression_test_suite_baseline.md's
own Part 2 where already present (most files), this document's own
pre-existing descriptions where regression_test_suite_baseline.md lacked an
entry, and freshly derived from each file's own header comment for the 20
files present in neither source (accessibility-axe-scan, analytics-mobile-
responsive, backtest-rule-change, and 17 others — see §2 for the full list).
Running total corrected from 39 to 104. Version bumped 1.4->1.5.

Signed: Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3) — 2026-09-16
```

---

```
Director of Quality
Date: 2026-06-09

v5.3 update (ST-20, BLG-QA-54): Coverage matrix updated with v5.2+v5.3 feature coverage.
41 spec files total. New SI-05 digest delivery spec (4 scenarios, ST-19).
Tax year P&L boundary validation via Python unittest (6 scenarios, ST-18).
System-status fallback count updated '62'→'65' (ST-07 watchlist endpoints).
EPIC-01 new contract docs (ST-04–07) have no frontend UI — coverage N/A.
EPIC-03 governance docs have no frontend rendering — coverage N/A.
2 coverage gaps identified (API contract docs, governance docs) — both intentional.

Prior sign-off (2026-05-29): 39 spec files, v3.7–v4.2 features, 3 zero-coverage features.

Signed: Sprint Execution Engine (autonomous class) — 2026-06-09
```

---

### v5.2 Coverage

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Notes |
|---------------|--------------------|-----------|-----------|----|
| SI-05 Weekly Digest delivery (v5.2) | ✅ N/A | — | — | Backend-only endpoint; no frontend page; coverage added in v5.3 (ST-19) |
| system-status.spec.js SC-SS-01b fallback count update (v5.2 ST-01) | ✅ Covered | `system-status.spec.js` | SC-SS-01b | Updated '59'→'62' for new endpoints |

### v5.3 Coverage (new this sprint)

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Notes |
|---------------|--------------------|-----------|-----------|----|
| ST-08 API key auth (POST /digest/si05/send) | ✅ Covered via unit test | `tests/test_api_contracts.py::TestDigestEndpoints` | 2 scenarios (401, 200) | FastAPI TestClient; not Playwright |
| SI-05 digest delivery E2E (ST-19) | ✅ Covered | `si05-digest-delivery.spec.js` | SC-SI05-01, SC-SI05-02, SC-SI05-03 + contract shape | ≥3 scenarios; Telegram mocked |
| Tax year P&L boundary (ST-18) | ✅ Covered via unit test | `tests/test_tax_year_pnl_boundary.py` | 6 scenarios | Python pytest; not Playwright |
| system-status.spec.js SC-SS-01b (ST-07 watchlist +3) | ✅ Covered | `system-status.spec.js` | SC-SS-01b | Updated '62'→'65' |

**New spec files this sprint:** `si05-digest-delivery.spec.js` (3 describe blocks, 4 scenarios)

**Total spec files post-v5.3:** 41

### Coverage Gaps — v5.3

| Feature | Reason | Recommendation |
|---------|--------|---------------|
| API contract doc pages (ST-04–07) | No frontend UI for contract docs | N/A — documentation only |
| Governance document pages (EPIC-03 stories) | No frontend rendering | N/A — backend governance only |

---

## 7. Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.5 | 2026-09-16 | Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3) | ST-18 (EPIC-03, v9.5, BLG-QA-167): §2 Spec File Index fully re-derived against `tests/e2e/` directly — corrected from the stale 39-file claim to the actual 104 files, 874 total scenarios. See §6 sign-off for sourcing methodology. |
| 1.3 | 2026-07-20 | Sprint Execution Engine | ST-05 (EPIC-05, v7.6, BLG-QA-114): Added §3A documenting `tests/e2e/fixtures/api-mocks.js`, the new shared OpenAPI-derived mock fixture library, as the preferred pattern for new Playwright tests. Covers the 9 endpoints touched by `BLG-SPEC-95`'s v7.4 UI-heavy release readiness bundle. `custom-price-alerts.spec.js` refactored as the working example (byte-identical mock output verified, all 11 scenarios still passing). |
| 1.2 | 2026-06-09 | Sprint Execution Engine | v5.3 ST-20 (BLG-QA-54): v5.2+v5.3 coverage sections added. SI-05 digest delivery spec (ST-19, 4 scenarios) + tax year P&L unit tests (ST-18, 6 scenarios) + system-status SC-SS-01b updated ('62'→'65'). Total: 41 spec files. Coverage gaps identified. Director of Quality sign-off. |
| 1.1 | 2026-06-01 | Sprint Execution Engine | v4.8 ST-06 (BLG-QA-39): Added v4.3–v4.7 feature coverage sections. Added compliance_summary field (v4.7 ST-03, SC-REP-05 reference). Confirmed GET /reports/monthly-pnl v0.6 contract present in reports_endpoints.md. No contract gaps found. |
| 1.0 | 2026-05-29 | Sprint Execution Engine | Initial coverage matrix (ST-12, v4.3 EPIC-02, BLG-QA-32). 39 spec files, v3.7–v4.2 features. |
