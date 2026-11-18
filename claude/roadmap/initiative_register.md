# Initiative Register

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-18 (rebalance 2026-11-18__scheduled — DL-090: Position Correlation Analysis, Backtesting Module, Full Compliance Scoring and Customisable Dashboard Layout moved from Priority 3 — Deferred to Killed (ST-45 sunset review flags, BLG-GOV-408); 0 active initiatives (20th consecutive cycle); CPS=N/A; no displacement candidate named); prior — 2026-09-19 (rebalance 2026-09-19__scheduled — DL-080; no initiative changes; 0 active initiatives (13 consecutive cycles); CPS=N/A; no displacement candidate named (no initiatives); prior history retained — see prior entries in version control

> ⚠️ Standing Notice: This register is a planning inventory only. It does not constitute canonical specification. All implementation detail is indicative until confirmed in canonical specs.

---

## Purpose

This register provides a canonical inventory of all roadmap initiatives with current status and decision log references. It is the single place to determine whether an initiative is active, gated, deferred, or killed.

---

## Active Initiatives

*No active initiatives as of 2026-04-03. v2.4 shipped 2026-04-03 (Verified_with_deviations). v2.5 scope TBD — release planning not yet started. v2.4 was backlog-driven (no initiative rows required). Standard-tier horizon review (cycle 2026-03-31__scheduled) confirmed no movements warranted for any Later or Gated item.*

---

## Gated Initiatives (not consuming resources until gate clears)

| ID | Initiative | Gate condition | Gate owner |
|----|-----------|---------------|------------|
| ~~4.3~~ | ~~Signal Exposure Enhancement~~ | ~~Gate cleared 2026-03-04 (PoG POG-20260304-01)~~ | ~~Strategy Rules owner + Product Owner~~ |
| ~~AI-SUM~~ | ~~AI Journal Summarisation~~ | ~~Gate cleared 2026-04-04 — SRB-v1.7 (2026-03-02): CONDITIONALLY COMPLIANT. Backlog item BLG-FEAT-16 filed. Moved to Priority 2 — Next Phase.~~ | ~~Product Owner + Strategy Rules owner~~ |
| ~~TECH-IND~~ | ~~New Technical Indicators~~ | ~~Gate cleared 2026-04-04 — Strategy Rules owner scoping decision: display-only scope approved (52-week high %, volume, price vs 50-day MA flag, relative strength field). No scoring changes. No strategy_rules.md bump required. Backlog item BLG-BE-10 filed. Moved to Priority 2 — Next Phase.~~ | ~~Strategy Rules owner~~ |
| ~~MKT-COR~~ | ~~Market Correlation Analysis~~ | ~~Gate cleared 2026-04-04 — Yahoo Finance (existing pipeline) confirmed sufficient. SPY/FTSE already ingested via pricing.py check_market_regime(); extend to 2y range for correlation lookback. On-demand computation, no DB storage, caching required. Backlog item BLG-FEAT-17 filed. Moved to Priority 2 — Next Phase.~~ | ~~Product Owner + Head of Engineering~~ |

---

## Priority 2 — Next Phase

*No active Priority 2 initiatives as of 2026-05-09. v3.2 shipped Arc 2 continuation: PT-02 (Pre-Trade Research View frontend), PT-03 (Prospective Heat at Entry integration), PT-05 (Pre-Trade Entry Checklist) — Verified 2026-05-07. Arc 2 partially complete: PT-04 (Setup Quality Score, gate: 20+ closed trades) remains. Next phase: v3.3 — scope TBD at release planning.*

---

## Priority 3 — Deferred

| Initiative | Rationale |
|-----------|-----------|
| Multi-Portfolio Support | Low value at current scale |
| Mobile App | Web experience sufficient |
| BLG-TECH-05 Prometheus | Defer until multi-user or operational need |

---

## Killed

| ID | Initiative | Date | Decision | Decision log ref |
|----|-----------|------|----------|-----------------|
| 4.1a | CSV Export of Trade History | 2026-03-01 | Superseded by BLG-FEAT-07 (shipped v1.6.1) | DL-001 |
| 4.1c | Server-Side PDF Report | 2026-03-15 | Displaced by BLG-OPS-01 (Dev Environment). Standing displacement candidate since DL-005. Browser-print functional; structural QA gap is higher priority. | DL-008 |
| PC-DEF | Position Correlation Analysis | 2026-11-18 | Killed — ST-45 sunset review flag (v9.15). Market Correlation Analysis (MKT-COR, v2.7) covers the portfolio-level need; a per-position remainder has no evidence of use at single-user scale. | DL-090 |
| BT-DEF | Backtesting Module | 2026-11-18 | Killed — ST-45 sunset review flag (v9.15). Covered by PO-05 Lightweight Replay Mode (v9.7) and the strategy backtest engine (`backtest_rule_change` router, Strategy Benchmark). A future need for more is a new idea, not this initiative. | DL-090 |
| FCS-DEF | Full Compliance Scoring | 2026-11-18 | Killed — ST-45 sunset review flag (v9.15). Delivered in substance by the Arc 5 composite compliance score (v4.1, `metrics_definitions.md` v1.11), surfaced in Reports and the SI-05 digest. | DL-090 |
| CDL-DEF | Customisable Dashboard Layout | 2026-11-18 | Killed — ST-45 sunset review flag (v9.15). The adopted Phase 4 brief (DL-089, re-review §14.3) makes the Dashboard calmer and fixed by job, not configurable. | DL-090 |

---

## Completed

| ID | Initiative | Shipped | Release |
|----|-----------|---------|---------|
| TECH-IND | New Technical Indicators | 2026-04-16 | v2.7 |
| MKT-COR | Market Correlation Analysis | 2026-04-16 | v2.7 |
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
| AI-SUM | AI Journal Summarisation | 2026-04-20 | v2.8 |
