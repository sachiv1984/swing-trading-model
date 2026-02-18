# Product Roadmap — Momentum Trading Assistant

**Owner:** Product Owner  
**Class:** Planning Document (Class 4)  
**Status:** Active  
**Last Updated:** 2026-02-18

> ⚠️ **Standing Notice:** This document records product intent and prioritisation thinking. All implementation detail (formulas, schemas, endpoint paths) is illustrative and indicative only. Before any feature moves to implementation, the relevant canonical specifications must be authored or updated by the appropriate domain owner. This document must not be cited as canonical intent.

---

## 1. Current Version

**v1.4** — Trade Journal complete. Performance Analytics in progress.  
**Next planned release:** v1.5

---

## 2. Strategic Scope

### This system is

- A deterministic, human-in-the-loop decision support tool for momentum trading
- A risk-managed framework built around ATR-based trailing stops and regime detection
- A single-user portfolio tracker with journalling and analytics

### Strategic exclusions (canonical — see `docs/specs/strategy_rules.md §13`)

These are not deferred features. They are formally recorded as system boundaries in the Strategy Rules canonical spec and prevail over any planning document:

- **Not an automated trading bot.** All exits require manual confirmation. This is a core design constraint.
- **Not a configurable strategy builder.** The strategy is a fixed, versioned behavioral contract. User-defined rule systems contradict the determinism principle.
- **Not an ML-based prediction system.** The system is explicitly deterministic. Non-deterministic signals are architecturally incompatible.

### Product scope exclusions (deferred, not strategically excluded)

These may be revisited in future versions without any canonical spec change:

- Broker API integration
- Real-time streaming prices
- Social / community features
- Options and futures trading support

---

## 3. Priority 1 — Current Focus (v1.4 completing / v1.5)

### 3.1 Performance Analytics Page
**Status:** In Progress  
**Effort:** Medium (3–4 days)  
**Value:** High

Full view of trading performance over time.

Intended outputs: monthly and quarterly returns, win rate by month, profit factor, max drawdown, current drawdown, time underwater (days from peak), Sharpe ratio, R-multiple distribution chart, expectancy per trade, R-multiple breakdown by tag.

> **Before implementation:** All metric formulas must be defined or confirmed in `docs/specs/metrics_definitions.md`. All analytics API endpoints must be specified in `docs/specs/api_contracts/` before frontend integration begins.

---

### 3.2 Position Sizing Calculator
**Status:** Planned — next after Analytics  
**Effort:** Low (1–2 days)  
**Value:** High (daily workflow improvement)

Embedded widget inside the position entry modal. Takes risk percentage and stop distance as inputs. Outputs optimal share count. Auto-fills the shares field. Validates against available cash in real time.

> **Before implementation:** The sizing formula must be canonicalized in `docs/specs/strategy_rules.md`. Indicative logic: `Risk Amount = Portfolio Value × Risk %`, `Position Size = Risk Amount / Stop Distance`. These are illustrative only until confirmed by the Strategy Rules owner.

---

### 3.3 Portfolio Heat Gauge
**Status:** Planned  
**Effort:** Low–Medium (2–3 days)  
**Value:** High (risk management)

Dashboard widget showing total capital at risk across all open positions as a percentage of portfolio value. Integrates with the Position Sizing Calculator to show the heat impact of a prospective new position.

> **Before implementation:** The heat formula and display thresholds must be defined in `docs/specs/metrics_definitions.md`. Indicative formula: `Position Risk = (Entry Price − Stop Price) × Shares`; `Portfolio Heat = Sum of Position Risks / Portfolio Value`. Indicative thresholds (0–5% green, 5–10% yellow, 10–15% orange, 15%+ red) are illustrative — the Metrics Definitions owner must confirm them.

---

### 3.4 Alerts & Notifications
**Status:** Planned  
**Effort:** Medium–High (4–5 days)  
**Value:** High

Email alerts for: stop loss approach, grace period ending (days 8–9 warning), market regime change to risk-off, daily portfolio summary. Optional SMS. In-app notification feed. Configurable per-user preferences.

> **Before implementation:** Database schema must be defined in `docs/specs/data_model.md`. API endpoints must be specified in `docs/specs/api_contracts/`. Schema sketches in the legacy roadmap file are illustrative only.

---

## 4. Priority 2 — Next Phase (v1.5)

### 4.1 Export & Reporting
**Status:** Planned  
**Effort:** Low–Medium (2–3 days)  
**Value:** Medium (tax necessity)

CSV export of trade history. PDF monthly portfolio report. JSON backup export.

---

### 4.2 Watchlist & Screening
**Status:** Planned — may defer to v2.0  
**Effort:** Medium (3–4 days)  
**Value:** Medium

Monitor tickers for entry signals. Target entry and stop fields. Quick-add to position entry modal.

> **Before implementation:** Schema and API endpoints must be defined in canonical specs. Illustrative sketches existed in legacy planning — do not treat as canonical.

---

## 5. Priority 3 — Deferred (v2.0)

| Feature | Effort | Rationale for deferral |
|---|---|---|
| Position Correlation Analysis | High | Value confirmed; not urgent for single-user system |
| Backtesting Module | Very High | High value for validation; significant scope |
| Multi-Portfolio Support | High | Low value at current scale |
| Mobile App | Very High | Web experience sufficient |
| Full Compliance Scoring | High | Requires more trade history to be meaningful |

---

## 6. Decision Framework

When evaluating new features:

1. Does it help make better trading decisions?
2. Will it be used daily or weekly?
3. Can it be implemented in under a week?
4. Does it require external dependencies?
5. Does it conflict with system boundaries in `strategy_rules.md §13`? If yes, do not proceed without a canonical spec change.

---

*For delivery history, see `docs/product/changelog.md`.*  
*For backlog and quick wins, see `docs/product/feature_backlog.md`.*  
*For strategic constraints and system boundaries, see `docs/specs/strategy_rules.md`.*
