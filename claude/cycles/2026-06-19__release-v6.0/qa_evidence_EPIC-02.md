Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-19

---

# QA Evidence — EPIC-02: Trader's Morning Briefing and Net-of-Costs Performance Tracking

**EPIC:** EPIC-02 — Trader's Morning Briefing + Net-of-costs tracking
**Cycle:** 2026-06-19__release-v6.0
**Sprint goal:** Ship the P0 signal correctness fix and deliver the Trader's Morning Briefing and net-of-costs features to resolve the Product Value Alert, complete Screener data quality telemetry, and advance SI-05 effectiveness reviews as within-sprint gates clear.
**Test scenarios used:** tests/e2e/morning-briefing.spec.js (SC-MB-01 to SC-MB-07b); tests/e2e/net-r-trade-history.spec.js (SC-NR-01 to SC-NR-04b); tests/e2e/system-status.spec.js SC-SS-01b

---

## ST-02 — Trader's Morning Briefing dashboard

| AC | Spec AC | Evidence method | Result |
|----|---------|-----------------|--------|
| AC-01 | Morning Briefing section renders at top of DashboardHome | SC-MB-01: data-testid="morning-briefing" visible on page load | Pass |
| AC-02 | Screener hits card: count of new hits; links to Screener | SC-MB-03a: count=2 when 2 signals status=new; SC-MB-03b: link to Screener | Pass |
| AC-03 | Positions card: EXIT_ZONE/GRACE_PERIOD states with days-in-state; links to Positions | SC-MB-04: "in grace" text visible; link to /Positions | Pass |
| AC-04 | Red Flags card: count since last 7 days; links to RedFlagJournal | SC-MB-05a: total=3 shown; SC-MB-05b: link to /RedFlagJournal | Pass |
| AC-05 | Earnings card: positions with earnings within 7 days; links to Positions | SC-MB-06: card visible, link to /Positions | Pass |
| AC-06 | Compliance card: 7-day Arc 5 score with trend vs 30-day; links to PerformanceAnalytics | SC-MB-07a: score + "7-day compliance score" visible; SC-MB-07b: link | Pass |
| AC-07 | All 5 cards show empty state gracefully when no data | SC-MB-02: all card titles visible; SC-MB-02b: empty state text for each card | Pass |
| AC-08 | No blocking errors when any single card endpoint fails | Covered by SC-MB-02b mockFallback + specific empty-state responses | Pass |
| AC-09 | Playwright automated test coverage for all observable ACs | tests/e2e/morning-briefing.spec.js — 11 test scenarios | Pass |

**Deviations:** None

---

## ST-03 — Net-of-costs performance tracking

| AC | Spec AC | Evidence method | Result |
|----|---------|-----------------|--------|
| AC-01 | commission_gbp and spread_cost_gbp capturable via PATCH /trades/{id}/costs | PATCH endpoint added to main.py; registered in test.py (66→67), openapi.yaml, trade_endpoints.md v2.4.0 | Pass |
| AC-02 | net_r_multiple calculated and displayed where cost data exists | SC-NR-02: "+1.8xR" shown for trade with costs; SC-NR-04a/04b: green/red colouring; TradeHistoryTable.js "Net R" column | Pass |
| AC-03 | Performance report breakdowns show gross vs net comparison | R-Multiple column (gross) + Net R column (net) side-by-side in TradeHistoryTable — SC-NR-01 confirms header visible | Pass |
| AC-04 | No impact to existing R-multiple calculations where cost data absent | SC-NR-03: "—" shown (text-slate-600 span) for trades without cost data; backward-compatible | Pass |
| AC-05 | New fields optional; existing trades without cost data unaffected | database.py uses ADD COLUMN IF NOT EXISTS; service returns null for missing cost fields | Pass |

**Schema migration:** DS-08 (data_model.md v2.9) — ensure_trade_cost_columns() called in on_startup().
**New endpoint registered:** PATCH /trades/{trade_id}/costs → test.py count 66→67; SystemStatus.js + SC-SS-01b updated.
**conftest.py:** ensure_trade_cost_columns, update_trade_costs, get_trade_history_with_stops added to _DB_STUB_FUNCTIONS.
**Deviations:** None

---

## EPIC-02 Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-02 | stage4_backlog_slice.md#ST-02, BLG-FEAT-46 | MorningBriefing.js + 5 sub-cards (ScreenerHitsCard, ExitZoneCard, RedFlagsCard, EarningsAlertCard, ComplianceCard); DashboardHome.js integration; api.positions.gracePeriodAlerts, api.portfolio.redFlagJournal added to base44Client.js; 11 Playwright scenarios | All 9 ACs verified; Playwright AC-09 satisfied | Pass | None |
| ST-03 | stage4_backlog_slice.md#ST-03, BLG-FEAT-20 | database.py: ensure_trade_cost_columns, update_trade_costs, get_trade_history_with_stops; trade_service.py: get_trade_history_with_stats updated to use stops JOIN, _compute_net_r helper, cost fields in response; main.py: startup call + PATCH endpoint; test.py 66→67; SystemStatus.js 66→67; SC-SS-01b updated; conftest.py stubs; data_model.md DS-08; trade_endpoints.md v2.4.0; openapi.yaml PATCH path; base44Client.js updateCosts; TradeHistoryTable.js Net R column; 4 Playwright scenarios | All 5 ACs verified; Playwright AC-02 coverage satisfied | Pass | None |

**QA test coverage:**
- Scenarios run: tests/e2e/morning-briefing.spec.js (11 tests); tests/e2e/net-r-trade-history.spec.js (5 tests); tests/e2e/system-status.spec.js SC-SS-01b
- Regression areas checked: DashboardHome query key registration, base44Client.js new methods, trade endpoint registry (test.py 66→67), openapi.yaml drift gate, conftest.py stub completeness
- Known deviations filed: None

---

## BLG-GOV-19 Autonomous DoQ Sign-Off

Classification: Autonomous — all stories in this EPIC are `classification: autonomous`. DoQ sign-off is agent-mediated per BLG-GOV-19.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] Playwright coverage confirmed for all frontend-visible observable ACs
- Signed off by: Director of Quality (agent-mediated, BLG-GOV-19)
- Date: 2026-06-19
- Comments: ST-02 Morning Briefing — 11 Playwright scenarios covering all 5 cards, empty states, links, and data rendering. ST-03 Net-of-costs — 5 Playwright scenarios covering Net R column header, value display, backward compatibility (null→"—"), and positive/negative colour coding. Frontend testing gate satisfied for both stories. All CLAUDE.md §2 same-commit requirements met for ST-03 endpoint addition.
