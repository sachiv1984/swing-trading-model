**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Draft — awaiting Head of UX & Design approval (build gated, `stage4_backlog_slice_addendum.md` ST-06)
**Version:** 1.0
**Last Updated:** 2026-11-16 (ST-06, EPIC-02, v9.17, BLG-FE-259 — initial draft: one Performance page from Reports and Analytics, against the `performance-page-brief` decision record §2)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-11-11__release-v9.17/performance-page-brief/decision_record.md §2
**Builds on:** `reports.md` v0.26, `analytics.md` v2.3, `navigation.md` v2.3, `glossary.md` v1.4, `docs/specs/metrics_definitions.md` v1.35.0, the shared `SectionIndex` (`long-page-section-index` decision record §2; `trade_plan.md` §5g)
**Built by:** `BLG-FE-259` (ST-06, EPIC-02, v9.17)

---

# Frontend Specification — Performance

## 1. Purpose

Results are split across two Review pages today:

- **Reports** (`Reports.js`, `/Reports`): a Performance tab (period headline cards, portfolio growth chart, performance summary, trade breakdown), plus Tax Year P&L, Monthly P&L and Reconciliation tabs.
- **Analytics** (`PerformanceAnalytics.js`, `/PerformanceAnalytics`): 21 components on one long scroll, from executive cards to compliance.

Several KPIs appear on both, and some are computed differently (§5). This spec merges them into one **Performance** page with four sections, gives each KPI one home, and reads each headline KPI from its canonical source. It does not change report generation, tax-year boundaries, exports or any server calculation (brief §2.8). Each moved component keeps its existing spec for content and states (`reports.md`, `analytics.md`) except where this spec says otherwise.

## 2. Route, Label and Placement

- **Route:** `/Performance`. **Label:** "Performance" everywhere — sidebar, page heading, palette and tab title `Performance · Position Manager` — from `src/lib/pageLabels.js` (`PAGE_LABELS.Performance`).
- **Placement:** Review area, in the slot Analytics holds today (`navigation.md` §Page Placement, position 2). The Reports and Analytics entries are removed.
- The same story updates: `navigation.md` (§Page Placement, §Onward Links, "Later merges" note), `glossary.md` §UI Labels (one "Performance" row; "Reports" and "Analytics" rows to legacy), `pageLabels.js` (`PAGE_LABELS`, `PALETTE_PAGE_KEYS`), every in-app link to the old routes (§7), and `reports.md` / `analytics.md` (a "Superseded by `performance.md`" header, brief §4).

## 3. Layout

```
Performance                                               (h1)
How your closed trades performed, with tax-year reports and rule compliance.
[ Period: Last Month ▾ ]  [ Export ]  [ Export PDF ]      ← header actions
Metrics staleness indicator
┌ content ─────────────────────────────────┐ ┌ On this page ┐
│ Summary                                   │ │ Summary      │
│ Reports  [Tax year | Monthly | Reconcil.] │ │ Reports      │
│ Analytics                                 │ │ Analytics    │
│ Compliance                                │ │ Compliance   │
└───────────────────────────────────────────┘ └──────────────┘
```

- **Section index:** the shared `SectionIndex` with ids `summary`, `reports`, `analytics`, `compliance`, in that order. Same behaviour as `trade_plan.md` §5g (instant jump, focus to the section `<h2>`, `?section=` by replace, honoured on load once the page's data is ready, `aria-current`). Each section is a `<section>` with a visible `<h2>`: "Summary", "Reports", "Analytics", "Compliance".
- **Period selector** (header): one selector, the Analytics options and keys (`last_7_days`, `last_month` default, `last_quarter`, `last_year`, `ytd`, `all_time`), held in `?period=` (replace). It drives Summary, Analytics and the Discipline & Compliance component. The Reports section keeps its own tax-year and month selectors and ignores it.
- **Exports** (header): Reports' **Export** (the existing `ExportModal`, period-filtered) and Analytics' **Export PDF** (the existing print report). Both unchanged.
- **Reports sub-views:** inside the Reports section, a tablist **Tax year · Monthly · Reconciliation** (the existing three tabs, unchanged content), held in `?report=tax-year|monthly|reconciliation` (replace; default `tax-year`). The tablist scrolls sideways inside itself at narrow widths (§9).
- **Markup:** new markup (page shell, section headings, the period bar, the Reports tablist) uses the `app-*` tokens (`design_system.md` §Semantic Colour Tokens, brief §2.10). Moved components keep their markup; ST-08 sweeps them.

## 4. Sections and What Lands Where

| Section (`id`) | Content, in order | From |
|----------------|-------------------|------|
| **Summary** (`summary`) | Headline cards: Total P&L (with W/L split subtitle on Win Rate), Win Rate, Total Trades (with "N still open"), Profit Factor, Expectancy. Then Portfolio Growth chart. Then Key Insights. | Reports Performance tab cards (Total P&L, Win Rate, Profit Factor, Total Trades) and chart; Analytics Expectancy card (moved here) and Key Insights |
| **Reports** (`reports`) | Tax year (summary bar, trades table, Unrealised P&L card, SI-02 Gate Status, restated-months notice), Monthly (Monthly Realised P&L table, AI monthly narrative, Exit Condition Breakdown, monthly CSV export), Reconciliation | Reports tabs, unchanged except: the Monthly view's **Strategy Compliance** block moves to Compliance (§5 one-home rule) |
| **Analytics** (`analytics`) | Risk cards: Sharpe Ratio, Max Drawdown, Recovery Factor, Time Underwater. Advanced metrics: Risk/Reward Ratio, Win Streak, Loss Streak, Avg Hold (Winners), Avg Hold (Losers), Trade Frequency, Capital Efficiency. Then Performance Summary (Gross Profit, Gross Loss, Average Win, Average Loss, Total Fees, Net P&L), Monthly Performance Heatmap, Underwater Equity Curve, Market Comparison, Performance by Exit Reason, Time-Based Analysis, R-Multiple Analysis, R-Multiple Distribution, Win Rate by Month, Top Performers, Best / Worst Trades, Consistency Metrics, Trade Plan Tag Filter, Performance by Strategy Tag, Cohort Analysis, Market Correlation | Analytics §1 (less Profit Factor and Expectancy), §3 (less Profit Factor), §4–§16, §18; Reports Performance Summary (less Best Trade / Worst Trade) |
| **Compliance** (`compliance`) | Discipline & Compliance, Arc 5 Signal Compliance (keeps its `id="strategy-compliance"` anchor), Trade Plan Completion Rate | Analytics §17, §19, §21; absorbs Reports Monthly "Strategy Compliance" |

**Removed as duplicates:** Reports' **Trade Breakdown** card (its "By Market" and "By Exit Reason" counts are shown by Market Comparison and Performance by Exit Reason); the Best Trade / Worst Trade rows of Performance Summary (Best / Worst Trades lists them with detail); Profit Factor in Analytics §1 and §3; Expectancy in Analytics §1 (moved to Summary).

## 5. One Home per KPI

**Scope rule:** a KPI over the page period (the header selector) has exactly one home. The same KPI over a narrower, labelled scope — one tax year, one month, one market, one exit reason, one tag, one cohort — is a different figure and stays with its breakdown. *(Interpretation for Head of UX & Design approval.)*

### 5.1 Period-level KPIs

| KPI | Home | Removed from | Canonical definition | Source on the Performance page |
|-----|------|--------------|----------------------|--------------------------------|
| Total P&L | Summary | — | `metrics_definitions.md` §Realized / Unrealized P&L Split (realised) | `GET /analytics/metrics` `summary.total_pnl` |
| Win Rate | Summary | — | §Win Rate | `summary.win_rate` |
| Total Trades | Summary | — | §Win Rate (denominator) | `summary.total_trades` |
| Profit Factor | Summary | Analytics §1, §3 | §Profit Factor | `executive_metrics.profit_factor` |
| Expectancy | Summary | Analytics §1 | §Expectancy | `executive_metrics.expectancy` |
| Sharpe Ratio | Analytics | — | §Sharpe Ratio (incl. Lookback Window) | `executive_metrics.sharpe_ratio` |
| Max Drawdown | Analytics | — | §Max Drawdown | `executive_metrics.max_drawdown` |
| Recovery Factor | Analytics | — | §Recovery Factor | `executive_metrics.recovery_factor` |
| Time Underwater | Analytics | — | §Days Underwater | `advanced_metrics.days_underwater`, `portfolio_peak_equity` |
| Risk/Reward Ratio | Analytics | — | §Risk/Reward Ratio | `executive_metrics.risk_reward_ratio` |
| Win / Loss Streak | Analytics | — | §Win Streak / Loss Streak | `advanced_metrics.win_streak`, `loss_streak` |
| Avg Hold (Winners / Losers) | Analytics | — | §Average Holding Period (Winners vs Losers) | `advanced_metrics.avg_hold_winners`, `avg_hold_losers` |
| Trade Frequency | Analytics | — | §Trade Frequency | `advanced_metrics.trade_frequency` |
| Capital Efficiency | Analytics | — | §Capital Efficiency | `advanced_metrics.capital_efficiency` |
| Gross Profit, Gross Loss, Average Win, Average Loss, Total Fees, Net P&L | Analytics (Performance Summary) | — | §Profit Factor (gross terms), §Fee Drag (fees) | as today (`trades_for_charts` of the same response) |
| Best / Worst Trade | Analytics (Best / Worst Trades) | Reports Performance Summary | — (a trade record, not a metric) | as today |
| Consistency (months profitable, P&L volatility, win-rate consistency) | Analytics | — | §Consistency Metrics | `advanced_metrics.consecutive_profitable_months`, `pnl_std_dev`, `win_rate_std_dev` |
| Override Rate, Red Flag Events/Week, Top Rule Breach, Validation Pass Rate | Compliance (Arc 5 Signal Compliance) | Reports Monthly "Strategy Compliance" | §Arc 5 Compliance Metrics | `GET /analytics/arc5-compliance` |
| Compliance metrics (§17) | Compliance | — | `metrics_definitions.md` v1.7.0 compliance set (analytics.md §17) | `GET /analytics/compliance-metrics` |
| Trade Plan Completion Rate | Compliance | — | analytics.md §21 | `GET /analytics/trade-plan-completion-rate` |

### 5.2 KPIs the two pages compute differently today

The Analytics page computes its §1 and §3 metrics in the browser from `GET /trades` (`PerformanceAnalytics.js` `calculateMetrics()`), while Reports and `analytics.md` §1/§3 use the server's `GET /analytics/metrics`. `metrics_definitions.md` §Sharpe Ratio (Lookback Window) already records the browser Sharpe as non-canonical (per-trade returns, population variance, √252 scaling, no minimum sample). On the Performance page every KPI in §5.1 is read from the server response named in its row; the browser recomputation is removed.

| KPI | Analytics page today | Canonical (kept) | Effect a user may see |
|-----|----------------------|------------------|-----------------------|
| Sharpe Ratio | browser, per-trade `pnl_percent`, population SD × √252 | server, §Sharpe Ratio | value changes |
| Max Drawdown, Recovery Factor | browser, cumulative realised P&L in the order of the list as returned; percent shown positive | server, §Max Drawdown (portfolio snapshots; `percent` zero or negative) / §Recovery Factor | value and sign convention change; the card shows the server percent as returned |
| Expectancy, Profit Factor, Risk/Reward | browser, same formulas, browser period filter | server, same formulas, server period filter | changes only where the two period filters select different trades |
| Win/Loss Streak, Avg Hold, Trade Frequency, Capital Efficiency, Time Underwater, Consistency Metrics | browser (Consistency from the browser monthly grouping) | server `advanced_metrics` | may change |

This is the brief §2.4 case ("the canonical one is kept"). It is not a recalculation of any server figure. *(The Metrics Definitions & Analytics Canonical Owner confirms §5 with a date — slice ST-06 AC 2.)*

## 6. States

- **Page loading:** the header and section index render at once; each section shows its own loading state.
- **Summary / Analytics, too few trades:** when the period has fewer than `min_trades_for_analytics` closed trades (server `has_enough_data: false`), both sections show the existing Analytics empty state ("Not enough trades", with "Enter Your First Position"); Reports and Compliance are unaffected.
- **No closed trades at all:** Summary shows the same empty state; the Reports tabs show their existing empty states (`reports.md` §Empty State).
- **Errors:** a failed request shows the existing error state inside its own section only; the other sections keep working. A component that already has its own error state (Arc 5, Discipline, Completion Rate, Cohort, Market Correlation) keeps it.

## 7. Redirects and Links

| Old route | New behaviour (replace navigation; Back does not loop) |
|-----------|--------------------------------------------------------|
| `/Reports` | `/Performance?section=reports` |
| `/PerformanceAnalytics` | `/Performance?section=analytics` |
| `/PerformanceAnalytics?section=strategy-compliance` | `/Performance?section=compliance` (the SI-05 digest link) |

Any other query string is kept (e.g. `period`). In-app links change in the same commit: Dashboard Signal Compliance card (`/PerformanceAnalytics` → `/Performance?section=compliance`), Strategy Benchmark onward link (→ `/Performance?section=analytics`, label "Performance"), the SI-05 digest compliance link (`backend/services/si05_digest_service.py`), and any `createPageUrl("Reports" | "PerformanceAnalytics")`. **Onward link:** the page header links to Trade History (Analytics' current onward link).

## 8. §13 Note

Display of existing deterministic metrics only, rearranged. No new AI call, score, rule or recommendation. The existing AI monthly narrative (Reports Monthly, `reports.md` §AI Summary, roster as today) moves with the Monthly view unchanged; Key Insights stay observational (`analytics.md` §2). §5.2 changes which existing server computation a KPI is read from, not any formula.

## 9. Phone Width

At 390 px the page has no page-level horizontal scroll. The section index is the sticky pill row below `lg`. The Reports tablist scrolls inside itself, and the Monthly Realised P&L table scrolls inside its card (`overflow-x-auto`), so the Avg P&L/Trade column can be scrolled into view. This meets `BLG-FE-237`'s AC (its 375 px checks are run at 375 px too); `groom backlog` can close it on ST-06's evidence.

## 10. Testable Acceptance Criteria

*For `BLG-FE-259`.*

| ID | Behaviour | Test |
|----|-----------|------|
| PF-01 | `/Performance` shows h1 "Performance", the four sections in order Summary, Reports, Analytics, Compliance, each with a visible h2; tab title `Performance · Position Manager` | Playwright |
| PF-02 | The section index lists the four sections; each link reaches its heading in one click and sets `?section=`; `?section=compliance` opens there | Playwright |
| PF-03 | `/Reports` → `/Performance?section=reports`, `/PerformanceAnalytics` → `?section=analytics`, `/PerformanceAnalytics?section=strategy-compliance` → `?section=compliance`; all replace navigations; other params kept | Playwright |
| PF-04 | Sidebar and palette show one "Performance" entry and no "Reports" or "Analytics" entry | Playwright (`sidebar-nav-groups`, `page-labels-single-source`) |
| PF-05 | Each §5.1 KPI label appears exactly once on the page in the populated state (one home) | Playwright: count of each label within `main` |
| PF-06 | Summary, Analytics and Compliance KPIs show the server values from `GET /analytics/metrics` (mocked with values a browser recomputation would not produce); no Sharpe or Expectancy is derived from `GET /trades` | Playwright with mocked responses |
| PF-07 | The period selector updates `?period=` and refetches Summary, Analytics and Discipline & Compliance; the Reports section ignores it | Playwright request capture |
| PF-08 | Reports tablist Tax year / Monthly / Reconciliation, `?report=` by replace, each view as `reports.md` | Playwright (retargeted Reports scenarios) |
| PF-09 | Too few trades: Summary and Analytics show "Not enough trades"; Reports and Compliance still render | Playwright |
| PF-10 | A failed `GET /analytics/arc5-compliance` affects only Compliance | Playwright |
| PF-11 | At 390 px and 375 px no page-level horizontal scroll on every Reports view; the Monthly Avg P&L/Trade column scrolls into view inside its card | Playwright |
| PF-12 | Dashboard Signal Compliance card, Strategy Benchmark onward link and the SI-05 digest link point at the new routes | Playwright + pytest (digest) |
| PF-13 | Both exports still open/produce as today | Playwright (retargeted export scenarios) |
| PF-14 | Axe: no violation on the page shell, section index and Reports tablist, light and dark | Playwright + axe |

## 11. Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-11-16 | Initial draft. ST-06 (EPIC-02, v9.17, BLG-FE-259) against the `performance-page-brief` §2 brief: route and label, four sections with the shared section index, one home per KPI with the scope rule, the browser-vs-server divergence list (§5.2), states, redirects incl. the SI-05 compliance link, §13 note, 390 px rule absorbing `BLG-FE-237`, ACs PF-01..PF-14. Head of UX & Design approval: *pending*. Metrics Definitions & Analytics Canonical Owner KPI confirmation (§5): *pending*. |
