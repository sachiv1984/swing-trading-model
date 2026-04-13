# Product Roadmap — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-13 (post-ship closure 2026-04-11__release-v2.6 — v2.6 marked ✅ Complete; §1, §3, and §8 updated)
**Last rebalance:** 2026-04-05 (cycle 2026-04-05__scheduled — scheduled run; Standard tier; DL-017 to DL-019)

> ⚠️ **Standing Notice:** This document records product intent and prioritisation thinking. All implementation detail (formulas, schemas, endpoint paths) is illustrative and indicative only. Before any feature moves to implementation, the relevant canonical specifications must be authored or updated by the appropriate domain owner. This document must not be cited as canonical intent.

---

## 1. Current Version

**v2.6** — Backend Integration Completion, Test Automation & Governance Hardening — Shipped 2026-04-13
**Next planned release:** **v2.7** (TBD)

---

## 2. Strategic Scope

### This system is
- A deterministic, human-in-the-loop decision support tool for momentum trading
- A risk-managed framework built around ATR-based trailing stops and regime detection
- A single-user portfolio tracker with journalling and analytics

### Strategic exclusions (canonical — see `docs/specs/strategy_rules.md §13`)

These are not deferred features. They are formally recorded as system boundaries in the Strategy Rules canonical spec and prevail over any planning document:

- **Not an automated trading bot.** All exits require manual confirmation.
- **Not a configurable strategy builder.** The strategy is a fixed, versioned behavioural contract.
- **Not an ML-based prediction system.** The system is explicitly deterministic.

### Product scope exclusions (deferred, not strategically excluded)

These may be revisited in future versions without any canonical spec change:

- Broker API integration
- Real-time streaming prices
- Social / community features
- Options and futures trading support

---

## 3. Delivery Plan — Horizon: Now

*v2.6 shipped 2026-04-13 (Verified_with_deviations). RA:v2.6 annotation retired to roadmap_archive.md 2026-04-13. Next release v2.7 — planning not yet opened.*

---

## 5. Priority 3 — Horizon: Later (v2.1 / v3.0)

| Feature | Effort | Rationale for deferral |
|---------|--------|------------------------|
| Position Correlation Analysis | High | Value confirmed; not urgent for single-user system |
| Backtesting Module | Very High | High value for validation; significant scope |
| Multi-Portfolio Support | High | Low value at current scale |
| Mobile App | Very High | Web experience sufficient |
| Full Compliance Scoring | High | Requires more trade history; lightweight version ships in v1.9 |
| BLG-TECH-05 — Prometheus metrics endpoint | Low–Medium | Defer until operational need or multi-user |
| Market Correlation Analysis | High | Gate cleared 2026-04-04 — Yahoo Finance pipeline confirmed sufficient (PO + HoE). Backlog item BLG-FEAT-17 filed. See Priority 2 — Next Phase in `initiative_register.md`. |
| AI Journal Summarisation | Medium | Gate cleared 2026-04-04 — SRB-v1.7 CONDITIONALLY COMPLIANT (PO). Backlog item BLG-FEAT-16 filed. See Priority 2 — Next Phase in `initiative_register.md`. |
| New Technical Indicators | Low–Medium | Gate cleared 2026-04-04 — display-only scope approved by Strategy Rules owner. Backlog item BLG-BE-10 filed. See Priority 2 — Next Phase in `initiative_register.md`. |
| Customisable Dashboard Layout | High | High build cost, low current priority. Defer indefinitely at current scale |

---

## 6. Gated Features — Awaiting Pre-Conditions

These features have been discussed and provisionally agreed but may not enter pre-alignment until the stated pre-condition is met. They are not deferred — they are waiting on an explicit gate.

| Feature | Gate condition | Gate owner |
|---------|---------------|------------|
| ~~Signal parameter exposure (4.3)~~ | ~~`strategy_rules.md` updated to formally define `top_n` and `lookback_days` as user-configurable~~ | ~~Strategy Rules owner + Product Owner~~ |
| AI Journal Summarisation | §13 boundary decision documented: does non-deterministic AI output conflict with the deterministic system principle? | Product Owner + Strategy Rules owner |
| New Technical Indicators | Strategy rules review: which indicators, if any, are canonical to this strategy? | Strategy Rules owner |
| Market Correlation | External data pipeline decision: do we ingest benchmark prices (SPY, FTSE)? | Product Owner + Head of Engineering |

> **Gate cleared (2026-03-04):** Signal parameter exposure (4.3) gate cleared by PoG POG-20260304-01. Item promoted to active v2.0 planning. See 4.3 entry in §3 above.

---

## 7. Decision Framework

When evaluating new features:

1. Does it help make better trading decisions?
2. Will it be used daily or weekly?
3. Can it be implemented in under a week?
4. Does it require external dependencies?
5. Does it conflict with system boundaries in `strategy_rules.md §13`? If yes, do not proceed without a canonical spec change.
6. Does it require pre-work (spec definitions, canonical updates, decision records) that isn't yet complete? If yes, add the pre-work as an explicit roadmap item before the feature.

---

## 8. Release Summary

| Release | Theme | Key deliveries |
|---------|-------|----------------|
| **v1.5** | Performance Analytics | Unified analytics endpoint, validation endpoint — ✅ Shipped *(retired to archive 2026-03-15)* |
| **v1.6** | Position Sizing | Calculator, settings default risk % — ✅ Shipped |
| **v1.6.1** | Correctness & Quick Wins | Quick Wins Bundle (6 features) — ✅ Shipped 2026-03-01 |
| **v1.7** | Foundation | CI/CD gate, §13 boundary review, metrics definitions, observability, API versioning decision — ✅ Shipped 2026-03-03 |
| **v1.8** | Risk Dashboard | Full risk page — heat, drawdown, grace period, position-level risk — ✅ Shipped 2026-03-06 |
| **v1.9** | User Value & Insight | ✅ Fully Shipped 2026-03-13 — all items retired to archive |
| **v1.10** | Operations & Quality | Staging environment, CI/CD auto-deploy, CohortAnalysis refactor, integration tests, v1.7 QA scenario gaps — ✅ Shipped 2026-03-16 *(retired to archive 2026-03-16)* |
| **v2.0** | Reporting & Alerts | Tax-year P&L statement, signal exposure controls (top_n, lookback_days) — ✅ Shipped 2026-03-17. Alerts & notifications deferred to v2.1 (pending BLG-TECH-08 ADR). |
| **v2.1** | Alerts, Watchlists & Enhancements | ADR-003 (async notification), Alerts & Notifications (Telegram delivery), Watchlists & Screening, Chart Interactivity, Tax-Year PDF/CSV Export, Slippage Tracking, Spec Debt & QA Coverage — ✅ Shipped 2026-03-21 |
| **v2.2** | Security, Alert Maturity & Quality | Security hardening (API Key Auth, CSP), Alert system maturity (scheduling, thresholds, history), Bug fixes & operational quick wins, QA coverage, Governance process enhancements — ✅ Shipped 2026-03-24 |
| **v2.3** | Quality Automation & User Insight | Strategy Compliance Panel, Metrics Staleness Indicator, Alert Nav Badge, Health Database endpoint, QA automation, Governance tooling — ✅ Shipped 2026-03-30 (Verified_with_deviations) |
| **v2.4** | Correctness, Insight & Governance Hardening | ATR fix, alert deduplication, stop price join, P&L GBP column, error mapping, data model reconciliation, weekly digest, operational readiness, governance patches — ✅ Shipped 2026-04-03 (Verified_with_deviations) |
| **v2.5** | Integration Baseline, Quick Wins & Governance Debt | System Status reliability (26 endpoints, auth fix, categories), backend integration docs, latency investigation, Fee Drag % metric, governance prompt patches (CF-2), governance_sync.yml fix, test scenarios — ✅ Shipped 2026-04-10 (Verified_with_deviations) |
| **v2.6** | Backend Integration Completion, Test Automation & Governance Hardening | Base44 SDK eliminated (Reports + Signals pages), CI pytest suite live (129 tests), fee drag Playwright + pytest specs, Trade History UX polish (7-card stats, column sort, header styling), CF-1/CF-2 governance patches closed — ✅ Shipped 2026-04-13 (Verified_with_deviations) |

---

*For delivery history, see `docs/product/changelog.md`.*
*For backlog and quick wins, see `claude/backlog/backlog.md`.*
*For strategic constraints and system boundaries, see `docs/specs/strategy_rules.md`.*
