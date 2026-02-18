# Feature Backlog — Momentum Trading Assistant

**Owner:** Product Owner  
**Class:** Planning Document (Class 4)  
**Status:** Active  
**Last Updated:** 2026-02-18

> ⚠️ **Standing Notice:** This document records backlog thinking and quick-win candidates. Items here are not committed and have not been reviewed against canonical specifications. Before any item moves to implementation, the relevant canonical specifications must be authored or updated by the appropriate domain owner.

---

## 1. Quick Wins (Low Effort, High Return)

These items can be slotted between major features. Each is estimated at 30 minutes to 2 hours unless otherwise noted.

### 1.1 Current Drawdown Widget
**Effort:** ~30 minutes  
**Value:** High visibility — surfaces risk posture immediately on dashboard  

Dashboard display showing current drawdown from peak and days underwater. Example: "Drawdown: −8.2%, 12 days underwater".

> Metrics Definitions owner must confirm the drawdown calculation before implementation.

---

### 1.2 R-Multiple Column in Trade History
**Effort:** ~1 hour  
**Value:** Medium — makes strategy edge visible in the trade list  

Add an R-multiple column to the trade history table. Calculated as `(Exit Price − Entry Price) / (Entry Price − Stop Price)`.

> Formula is indicative. Metrics Definitions owner must confirm before implementation. Note: R-multiple may be frontend-only for display — confirm with API Contracts owner whether this should be server-side or client-side.

---

### 1.3 Slippage Tracking
**Effort:** 1–2 hours  
**Value:** Medium — useful for execution quality monitoring  

Add a slippage field to the trade history table. Show average slippage in the analytics summary.

> Indicative formula: `(Fill Price − Market Price) / Market Price`. Metrics Definitions owner must define this before implementation. Requires data model update for the slippage field.

---

### 1.4 Best / Worst Trades Widget
**Effort:** ~1 hour  
**Value:** Medium — supports review and pattern recognition  

Dashboard or analytics widget showing top 3 and bottom 3 trades by R-multiple or P&L.

---

### 1.5 Win Rate Chart
**Effort:** ~1 hour  
**Value:** Medium  

Simple bar chart showing win rate by calendar month. Can be delivered as part of the Performance Analytics page or as a standalone dashboard widget.

---

### 1.6 Grace Period Indicator
**Effort:** ~1 hour  
**Value:** Medium — reduces manual counting  

Visual countdown in the open positions table showing remaining days in the grace period (e.g. "Day 6 of 10").

---

### 1.7 CSV Export Button
**Effort:** ~1 hour  
**Value:** Medium (tax preparation)  

One-click export of the trade history table as a CSV file. Simple implementation, high practical value.

---

### 1.8 Basic Compliance Metrics
**Effort:** ~1 day  
**Value:** Medium (discipline monitoring)  

Lightweight metrics tracking process discipline rather than performance: journal completion rate (% of trades with notes), stop-based exit rate (% of exits that were stop-triggered), average position size as % of portfolio.

> Definitions must be confirmed in Metrics Definitions before implementation.

---

## 2. Removed Items

Items explicitly removed from consideration with rationale.

| Item | Decision | Rationale |
|---|---|---|
| Gap Risk Monitor | Removed | Not actionable for this strategy. The trailing stop framework handles gap risk implicitly. Adding a monitor would create noise without enabling a different decision. |
| Full Compliance Scoring System | Deferred to v2.0 | Meaningful only with sufficient trade history. Lightweight compliance metrics (see 1.8 above) cover the immediate need. |

---

## 3. Deferred Items (not current priority)

Items with confirmed value that are not being pursued now.

| Item | Target | Notes |
|---|---|---|
| Daily email summary | v2.0 | Cron job sending daily portfolio status. Useful but not urgent. |
| FX rate history tracking | v2.0 | Track GBP/USD changes over time. Low priority. |

---

## 4. Out of Scope (product level)

These are product decisions — not strategic constraints. They may be revisited.

- Broker API integration
- Real-time streaming prices  
- Social / community features
- Options trading support
- Futures trading support
- Multi-portfolio support (deferred to v2.0)
- Mobile app (deferred to v2.0)

For strategic constraints (automated execution, strategy builder, ML predictions), see `docs/specs/strategy_rules.md §13`. Those cannot be revisited without a canonical spec change.

---

*For committed priorities and phasing, see `docs/product/roadmap.md`.*  
*For delivery history, see `docs/product/changelog.md`.*
