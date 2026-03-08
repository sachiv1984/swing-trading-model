**Owner:** Data Model & Domain Schema Owner
**Class:** Canonical Specification (Class 1)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-03-08
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Settings Model

## 1. Purpose

This document defines the **Settings** data model: all field names, types, validation rules, and default values for the settings domain. It owns the model — what each field means and its constraints. The API contract (`docs/specs/api_contracts/settings_endpoints.md`) owns the request/response shape.

## 2. Relationship to API Contract

- **This document:** canonical field definitions, types, defaults, constraints, and semantics.
- **`docs/specs/api_contracts/settings_endpoints.md`:** canonical request/response shape for `GET /settings`, `POST /settings`, `PATCH /settings/{settings_id}`.

In case of conflict between this document and the API contract on field naming or type, this document prevails. For request/response shape questions, the API contract prevails.

---

## 3. Settings Schema

### 3.1 Storage

Settings are stored as a single global row in the database. There is exactly one settings record per installation.

| Attribute | Value |
|-----------|-------|
| Table | `settings` |
| Cardinality | Singleton (one row) |
| Identifier | UUID (`id`) |
| Created by | `POST /settings` |
| Updated by | `PATCH /settings/{settings_id}` |

### 3.2 Field Definitions

| Field | Type | Default | Constraint | Semantics |
|-------|------|---------|-----------|-----------|
| `id` | string (UUID) | — (generated) | Unique, immutable | System-generated identifier for the settings record |
| `min_hold_days` | integer | `10` | ≥ 1 | Grace period duration in calendar days. Stop-loss enforcement is suspended for positions held fewer than this many days. Affects position display status ("GRACE"). This is the `min_hold_days` strategy parameter. |
| `atr_multiplier_initial` | float | `5.0` | > 0 | ATR multiplier applied when setting the initial stop price for a new position. Wider multiplier allows more room to recover. Canonical parameter documented in `docs/claude/strategy/strategy_rules.md`. |
| `atr_multiplier_trailing` | float | `2.0` | > 0 | ATR multiplier applied when trailing stops for profitable positions. Tighter multiplier protects gains. Canonical parameter documented in `docs/claude/strategy/strategy_rules.md`. |
| `atr_period` | integer | `14` | ≥ 1 | Rolling window in calendar days for Average True Range (ATR) calculation. Standard value: 14. |
| `default_currency` | string | `"GBP"` | `"GBP"` only | Portfolio base currency for display. Multi-currency support exists at position level (GBP/USD); the portfolio-level base currency is always GBP. |
| `theme` | string | `"dark"` | `"dark"` or `"light"` | UI display theme preference. User-configurable. No system behaviour depends on this value. |
| `uk_commission` | float | `9.95` | ≥ 0 | Fixed commission fee in GBP applied per UK trade (both entry and exit). Included in cost basis and P&L calculations. |
| `us_commission` | float | `0.00` | ≥ 0 | Fixed commission fee applied per US trade (in USD, zero for zero-commission brokers). Included in cost basis and P&L calculations. |
| `stamp_duty_rate` | float | `0.005` | ≥ 0 and ≤ 1 | UK stamp duty rate applied as a fraction of trade value on UK stock purchases (0.5% = 0.005). Does not apply to US stocks. |
| `fx_fee_rate` | float | `0.0015` | ≥ 0 and ≤ 1 | FX conversion fee rate applied to USD transactions as a fraction (0.15% = 0.0015). Applied at entry and exit for US positions. |
| `min_trades_for_analytics` | integer | `10` | ≥ 1 | Minimum number of closed trades required before analytics metrics are computed and returned. Prevents statistically meaningless results on small datasets. |
| `default_risk_percent` | float | `1.00` | > 0 and ≤ 100 | Default risk percentage pre-populated in the Position Sizing Calculator widget on the Trade Entry page. Represents the percentage of portfolio value to risk per new position (e.g., `1.00` = 1%). This is a user preference, not an enforced position limit — users may override per trade. |

### 3.3 Immutable Fields

| Field | Mutability |
|-------|------------|
| `id` | Immutable — set at creation, never updated |

All other fields are mutable via `PATCH /settings/{settings_id}`.

### 3.4 Strategic Parameter Context

The default values reflect the backtest-optimised parameters that produced:
- 26.37% CAGR
- 1.29 Sharpe Ratio
- −25.38% maximum drawdown

Changing `min_hold_days` or ATR multipliers affects all future stop calculations. Changes do not retroactively affect open positions or closed trade history.

### 3.5 Fee Parameter Semantics

Fee parameters (`uk_commission`, `us_commission`, `stamp_duty_rate`, `fx_fee_rate`) affect:
- Position cost basis calculations (applied at entry)
- P&L calculations on exit
- They do not affect existing closed trade history — changes apply to new transactions only.

---

## 4. Field Validation Rules (Canonical)

The following validation rules are enforced by the backend and are canonical regardless of how the API contract documents them:

| Field | Rule | Error on violation |
|-------|------|--------------------|
| `min_hold_days` | Must be ≥ 1 | HTTP 400 |
| `atr_multiplier_initial` | Must be > 0 | HTTP 400 |
| `atr_multiplier_trailing` | Must be > 0 | HTTP 400 |
| `atr_period` | Must be ≥ 1 | HTTP 400 |
| `default_currency` | Must be `"GBP"` | HTTP 400 |
| `theme` | Must be `"dark"` or `"light"` | HTTP 400 |
| `uk_commission` | Must be ≥ 0 | HTTP 400 |
| `us_commission` | Must be ≥ 0 | HTTP 400 |
| `stamp_duty_rate` | Must be ≥ 0 and ≤ 1 | HTTP 400 |
| `fx_fee_rate` | Must be ≥ 0 and ≤ 1 | HTTP 400 |
| `min_trades_for_analytics` | Must be ≥ 1 | HTTP 400 |
| `default_risk_percent` | Must be > 0 and ≤ 100 | HTTP 400 |

---

## 5. Cross-References

| Domain | Document | Relationship |
|--------|----------|-------------|
| API Contract | `docs/specs/api_contracts/settings_endpoints.md` | Canonical request/response shape for settings endpoints |
| Strategy Rules | `docs/claude/strategy/strategy_rules.md` | Canonical governance of strategy parameters (`min_hold_days`, ATR multipliers) |
| Position Sizing | `docs/specs/api_contracts/portfolio_endpoints.md §POST /portfolio/size` | `default_risk_percent` pre-populates the position sizing calculator |

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-08 | Initial canonical specification. Created per ST-17 (v1.9 Sprint 1, EPIC-06). Field definitions derived from `settings_endpoints.md v1.1.0` — the confirmed canonical interface shape following ESC-20260304-01 resolution. |
