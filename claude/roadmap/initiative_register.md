# Initiative Register

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-01

> ⚠️ Standing Notice: This register is a planning inventory only. It does not constitute canonical specification. All implementation detail is indicative until confirmed in canonical specs.

---

## Purpose

This register provides a canonical inventory of all roadmap initiatives with current status and decision log references. It is the single place to determine whether an initiative is active, gated, deferred, or killed.

---

## Active Initiatives

| ID | Initiative | Release | Status | Decision log ref |
|----|-----------|---------|--------|-----------------|
| BLG-TECH-04 | CI/CD GitHub Actions Validation Workflow | v1.7 | Planned — unblocked | — |
| §13-BR | Strategy Rules §13 Boundary Review | v1.7 | Planned | — |
| HEAT-DEF | Metrics Definitions — Portfolio Heat Formula & Thresholds | v1.7 | Planned | — |
| LOG-STD | Structured Logging / Observability Standards | v1.7 | Planned | — |
| API-VER | API Versioning Strategy Decision Record | v1.7 | Planned | — |
| 3.4 | Risk Dashboard | v1.8 | Planned — pre-req: HEAT-DEF | — |
| BLG-FEAT-08 | Basic Compliance Metrics | v1.9 | Planned — pre-req gate for 5.1 | — |
| 5.1 | Structured Trade Reflection Template | v1.9 | Planned — pre-req: BLG-FEAT-08 | — |
| 5.2 | Cohort Analysis | v1.9 | Planned | — |
| 5.3 | Dashboard Homepage / Session Summary | v1.9 | Planned | — |
| 3.5 | Alerts & Notifications | v2.0 | Planned — hard gates apply (see DL-002) | DL-002 |
| 4.1b | Tax-Year P&L Statement | v2.0 | Planned | — |
| 4.1c | Server-Side PDF Report | v2.0 | Planned | — |

---

## Gated Initiatives (not consuming resources until gate clears)

| ID | Initiative | Gate condition | Gate owner |
|----|-----------|---------------|------------|
| 4.3 | Signal Exposure Enhancement | `strategy_rules.md` §13 boundary review confirms `top_n` and `lookback_days` are user-configurable | Strategy Rules owner + Product Owner |
| AI-SUM | AI Journal Summarisation | §13 boundary decision: non-deterministic AI vs determinism principle | Product Owner + Strategy Rules owner |
| TECH-IND | New Technical Indicators | Strategy rules review confirms which indicators are in scope | Strategy Rules owner |
| MKT-COR | Market Correlation Analysis | External data pipeline decision (SPY/FTSE ingestion) | Product Owner + Head of Engineering |

---

## Priority 2 — Next Phase (post v2.0)

| ID | Initiative | Status |
|----|-----------|--------|
| 4.2 | Watchlists & Screening | Planned — do not pull forward |
| CHART-IX | Chart Interactivity Enhancements | Planned — do not pull forward |

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

---

## Completed

| ID | Initiative | Shipped | Release |
|----|-----------|---------|---------|
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
