# Product Roadmap — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-02-20
> ⚠️ **Standing Notice:** This document records product intent and prioritisation thinking. All implementation detail (formulas, schemas, endpoint paths) is illustrative and indicative only. Before any feature moves to implementation, the relevant canonical specifications must be authored or updated by the appropriate domain owner. This document must not be cited as canonical intent.

---

## 1. Current Version
**v1.5** — Performance Analytics complete. Position Sizing Calculator verified and in shipping closure.
**Next planned release:** **v1.6**

---

## 2. Strategic Scope

### This system is
- A deterministic, human-in-the-loop decision support tool for momentum trading
- A risk-managed framework built around ATR-based trailing stops and regime detection
- A single-user portfolio tracker with journalling and analytics

### Strategic exclusions (canonical — see `docs/specs/strategy_rules.md §13`)
These are not deferred features. They are formally recorded as system boundaries in the Strategy Rules canonical spec and prevail over any planning document:
- **Not an automated trading bot.** All exits require manual confirmation.
- **Not a configurable strategy builder.** The strategy is a fixed, versioned behavioral contract.
- **Not an ML-based prediction system.** The system is explicitly deterministic.

### Product scope exclusions (deferred, not strategically excluded)
These may be revisited in future versions without any canonical spec change:
- Broker API integration
- Real-time streaming prices
- Social / community features
- Options and futures trading support

---

## 3. Priority 1 — Current Focus (v1.6)

### 3.1 Performance Analytics Page
**Status:** ✅ Complete (shipped v1.5)
Delivered via a unified `GET /analytics/metrics?period=` endpoint. Includes a `POST /validate/calculations` endpoint for smoke-testing metric correctness against a known dataset.

---

### 3.2 Position Sizing Calculator (Primary Feature)
**Status:** ⚠️ Verification complete — shipping closure pending (DEF-006, F15)
**Effort:** Low–Medium (2–3 days) *(revised from 1–2 days — see scope note below)*
**Value:** High (daily workflow improvement)

Always-visible widget inside the position entry form, directly above the shares field. User provides risk percentage (pre-populated from settings default) and stop price; system calculates suggested share count. Auto-fills the shares field when empty; shows a "use this" affordance when the user has already entered a value. Validates against available cash in real time via debounced calculation (300ms).

> **Scope note (revised 2026-02-19):** Scope expanded during pre-alignment to include `default_risk_percent` field in the settings table, settings endpoint, and settings page UI. This is required to support widget pre-population and is in scope for v1.6 — not deferred. The original 1–2 day estimate did not account for the settings field, database migration, and additional spec updates across four documents. Revised estimate: 2–3 days. Full decision rationale: `docs/product/decisions/3.2-position-sizing-calculator.md`.

> **Canonical specifications:** Sizing formula, validity rules, FX handling, and cash constraint behaviour are canonicalised in `docs/specs/strategy_rules.md §4.1`. Endpoint contract at `docs/specs/api_contracts/portfolio_endpoints.md` (`POST /portfolio/size`). Data model at `docs/specs/data_model.md §6`. Settings field at `docs/specs/api_contracts/settings_endpoints.md`.

> **Verification status (updated 2026-02-20):** Phase 1 verification complete. Director of Quality sign-off granted at v1.1 (2026-02-19) and re-verification pass signed off at v1.2 (2026-02-20). Two items remain before shipping closure: DEF-006 (Low — Risk % session persistence, engineering assigned) and F15 (deferred — requires database access). Verification report: `docs/product/verification/3.2-position-sizing-calculator-verification.md`.

---

### 3.3 v1.6 Supporting Scope — Analytics Correctness & Validation Hardening (Scope Locked)

These items are intentionally included in v1.6 (alongside Position Sizing) because they are small enough to absorb into the release, but high enough impact that they must be explicit to avoid being dropped.

#### BLG-TECH-01 — Fix Sharpe variance method + Capital Efficiency currency basis (**Quality Gate**)
**Purpose:** Data correctness and validation trust.
**Release Gate:** v1.6 must not ship unless this item is complete and validation passes with signed-off expected values. This affects any user with enough trades to produce a non-zero Sharpe, which will be true of real usage.

Scope (summary):
- Sharpe uses sample variance (divide by n-1) for portfolio and trade methods
- Capital efficiency uses `total_cost (GBP)` from `trade_history`
- Update validation expected values and secure canonical owner sign-off

#### BLG-TECH-02 — Implement validation severity model
Add severity to each validation result and a by-severity breakdown to the validation summary. Update API contract first, then implement. This turns severity into an enforceable operational model rather than just documentation.

#### BLG-TECH-03 — Consolidate ValidationService stub into service layer
Migrate active validation logic into the service layer and keep the router thin. Do alongside BLG-TECH-02 to avoid double-touching validation code.

---

### 3.4 Portfolio Heat Gauge
**Status:** Planned
**Effort:** Low–Medium (2–3 days)
**Value:** High (risk management)

Dashboard widget showing total capital at risk across all open positions as a percentage of portfolio value. Integrates with Position Sizing Calculator to show the heat impact of a prospective new position.

> **Before implementation:** The heat formula and display thresholds must be defined in `docs/specs/metrics_definitions.md`. Indicative formula: `Position Risk = (Entry Price − Stop Price) × Shares`; `Portfolio Heat = Sum of Position Risks / Portfolio Value`. Thresholds are illustrative — confirm with the Metrics Definitions owner.

---

### 3.5 Alerts & Notifications
**Status:** Planned
**Effort:** Medium–High (4–5 days)
**Value:** High

Email alerts for: stop loss approach, grace period ending (days 8–9 warning), market regime change to risk-off, daily portfolio summary. Optional SMS. In-app notification feed. Configurable per-user preferences.

> **Before implementation:** Database schema must be defined in `docs/specs/data_model.md`. API endpoints must be specified in `docs/specs/api_contracts/`.

---

## 4. Priority 2 — Next Phase (post v1.6)

### 4.1 Export & Reporting
**Status:** Planned
**Effort:** Low–Medium (2–3 days)
**Value:** Medium (tax necessity)

CSV export of trade history. PDF monthly portfolio report. JSON backup export.

### 4.2 Watchlist & Screening
**Status:** Planned — may defer to v2.0
**Effort:** Medium (3–4 days)
**Value:** Medium

Monitor tickers for entry signals. Target entry and stop fields. Quick-add to position entry modal.

---

## 5. v1.7 — Process Improvement (Supporting Release)

### 5.1 BLG-TECH-04 — CI/CD: GitHub Actions validation workflow
**Purpose:** Process improvement (not user-facing)
Implement GitHub Actions workflow to run `POST /validate/calculations` on pull requests and branch pushes, block merge if any critical-severity validation fails, and post a results summary as a PR comment. Depends on validation severity.

---

## 6. Priority 3 — Deferred (v2.0)

Feature | Effort | Rationale for deferral
---|---|---
Position Correlation Analysis | High | Value confirmed; not urgent for single-user system
Backtesting Module | Very High | High value for validation; significant scope
Multi-Portfolio Support | High | Low value at current scale
Mobile App | Very High | Web experience sufficient
Full Compliance Scoring | High | Requires more trade history to be meaningful
BLG-TECH-05 — Prometheus metrics endpoint | Low–Medium | Observability; defer until operational need / multi-user

---

## 7. Decision Framework
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
