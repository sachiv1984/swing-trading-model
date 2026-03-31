# Initiative Register

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-31 (roadmap rebalance — cycle 2026-03-31__scheduled; active initiatives remain zero; no Now-horizon initiatives added; 4 backlog items added (DL-013 to DL-016))

> ⚠️ Standing Notice: This register is a planning inventory only. It does not constitute canonical specification. All implementation detail is indicative until confirmed in canonical specs.

---

## Purpose

This register provides a canonical inventory of all roadmap initiatives with current status and decision log references. It is the single place to determine whether an initiative is active, gated, deferred, or killed.

---

## Active Initiatives

*No active initiatives as of 2026-03-31. v2.3 shipped 2026-03-30. v2.4 scope TBD — pending release planning. Standard-tier horizon review (cycle 2026-03-31__scheduled) confirmed no movements warranted for any Later or Gated item. 4 new items added to backlog candidate pool (BLG-FEAT-14, BLG-OPS-10, BLG-BE-06, BLG-GOV-09).*

---

## Gated Initiatives (not consuming resources until gate clears)

| ID | Initiative | Gate condition | Gate owner |
|----|-----------|---------------|------------|
| ~~4.3~~ | ~~Signal Exposure Enhancement~~ | ~~Gate cleared 2026-03-04 (PoG POG-20260304-01)~~ | ~~Strategy Rules owner + Product Owner~~ |
| AI-SUM | AI Journal Summarisation | §13 boundary decision: non-deterministic AI vs determinism principle | Product Owner + Strategy Rules owner |
| TECH-IND | New Technical Indicators | Strategy rules review confirms which indicators are in scope | Strategy Rules owner |
| MKT-COR | Market Correlation Analysis | External data pipeline decision (SPY/FTSE ingestion) | Product Owner + Head of Engineering |

---

## Priority 2 — Next Phase (post v2.1)

*No items currently in Next Phase. v2.2 scope will be determined by release planning engine from enriched backlog.*

---

## Priority 3 — Deferred

| Initiative | Rationale |
|-----------|-----------|
| Position Correlation Analysis | Not urgent; single-user scale |
| Backtesting Module | High value; significant scope |
| Multi-Portfolio Support | Low value at current scale |
| Mobile App | Web experience sufficient |
| Full Compliance Scoring | Lightweight version in v1.9 |
| BLG-TECH-05 Prometheus | Defer until multi-user or operational need |
| Customisable Dashboard Layout | High build cost; low current priority |

---

## Killed

| ID | Initiative | Date | Decision | Decision log ref |
|----|-----------|------|----------|-----------------|
| 4.1a | CSV Export of Trade History | 2026-03-01 | Superseded by BLG-FEAT-07 (shipped v1.6.1) | DL-001 |
| 4.1c | Server-Side PDF Report | 2026-03-15 | Displaced by BLG-OPS-01 (Dev Environment). Standing displacement candidate since DL-005. Browser-print functional; structural QA gap is higher priority. | DL-008 |

---

## Completed

| ID | Initiative | Shipped | Release |
|----|-----------|---------|---------|
| 3.5 | Alerts & Notifications | 2026-03-21 | v2.1 |
| 4.2 | Watchlists & Screening | 2026-03-21 | v2.1 |
| CHART-IX | Chart Interactivity Enhancements | 2026-03-21 | v2.1 |
| 4.1b | Tax-Year P&L Statement | 2026-03-17 | v2.0 |
| 4.3 | Signal Exposure Enhancement | 2026-03-17 | v2.0 |
| BLG-OPS-01 | Development Environment (staging) | 2026-03-16 | v1.10 |
| 3.1 | Performance Analytics Page | — | v1.5 |
| 3.2 | Position Sizing Calculator | 2026-02-20 | v1.6 |
| BLG-TECH-01 | Fix Sharpe Variance + Capital Efficiency | 2026-02-21 | v1.6.1 |
| BLG-TECH-02 | Validation Severity Model | 2026-02-21 | v1.6.1 |
| BLG-TECH-03 | ValidationService Consolidation | 2026-02-21 | v1.6.1 |
| BLG-FEAT-01 | Current Drawdown Widget | 2026-03-01 | v1.6.1 |
| BLG-FEAT-02 | R-Multiple Column | 2026-03-01 | v1.6.1 |
| BLG-FEAT-04 | Best / Worst Trades Widget | 2026-03-01 | v1.6.1 |
| BLG-FEAT-05 | Win Rate by Month Chart | 2026-03-01 | v1.6.1 |
| BLG-FEAT-06 | Grace Period Indicator | 2026-03-01 | v1.6.1 |
| BLG-FEAT-07 | CSV Export of Trade History | 2026-03-01 | v1.6.1 |
| BLG-TECH-04 | CI/CD GitHub Actions Validation Workflow | 2026-03-03 | v1.7 |
| §13-BR | Strategy Rules §13 Boundary Review | 2026-03-03 | v1.7 |
| HEAT-DEF | Metrics Definitions — Portfolio Heat Formula & Thresholds | 2026-03-03 | v1.7 |
| LOG-STD | Structured Logging / Observability Standards | 2026-03-03 | v1.7 |
| API-VER | API Versioning Strategy Decision Record | 2026-03-03 | v1.7 |
| BLG-TECH-06 | Canonicalise sharpe_ratio_trade_method | 2026-03-03 | v1.7 |
| BLG-TECH-08 | Align portfolio_endpoints.md positions summary | 2026-03-03 | v1.7 |
| BLG-TECH-09 | Add holding_days to GET /trades | 2026-03-03 | v1.7 |
| BLG-FEAT-08 | Basic Compliance Metrics | 2026-03-13 | v1.9 Sprint 2 |
| 5.1 | Structured Trade Reflection Template | 2026-03-13 | v1.9 Sprint 2 |
| 5.2 | Cohort Analysis | 2026-03-13 | v1.9 Sprint 2 |
| 5.3 | Dashboard Homepage / Session Summary | 2026-03-13 | v1.9 Sprint 2 |
