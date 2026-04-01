# Product Roadmap — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-31 (roadmap rebalance — cycle 2026-03-31__scheduled — scheduled run; Standard tier; DL-013 to DL-016)
**Last rebalance:** 2026-03-31 (cycle 2026-03-31__scheduled — scheduled run; Standard tier; DL-013 to DL-016)

> ⚠️ **Standing Notice:** This document records product intent and prioritisation thinking. All implementation detail (formulas, schemas, endpoint paths) is illustrative and indicative only. Before any feature moves to implementation, the relevant canonical specifications must be authored or updated by the appropriate domain owner. This document must not be cited as canonical intent.

---

## 1. Current Version

**v2.3** — Quality Automation & User Insight — Shipped 2026-03-30
**Next planned release:** **v2.4** (TBD)

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

*v2.3 shipped 2026-03-30. v2.4 release plan published 2026-03-31 — 17 stories across 6 EPICs (Correctness, Insight & Governance Hardening). Sprint planning pending.*

<!-- roadmap-annotation-marker: RA:v2.4:2026-03-31__release-v2.4 -->

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-03-31__release-v2.4
- Plan published: 2026-03-31
- Cycle folder: claude/cycles/2026-03-31__release-v2.4/
- Backlog slice: claude/cycles/2026-03-31__release-v2.4/stage4_backlog_slice.md
- Status at annotation: Validated

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
| Market Correlation Analysis | High | Blocked: requires external benchmark data pipeline (SPY, FTSE daily prices). Revisit when/if that pipeline is introduced |
| AI Journal Summarisation | Unknown | Blocked: requires §13 boundary decision (determinism principle). Not on active roadmap until that decision is documented |
| New Technical Indicators | Low–Medium | Blocked: requires strategy rules review. Not in scope without formal §13 confirmation |
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

---

*For delivery history, see `docs/product/changelog.md`.*
*For backlog and quick wins, see `claude/backlog/backlog.md`.*
*For strategic constraints and system boundaries, see `docs/specs/strategy_rules.md`.*
