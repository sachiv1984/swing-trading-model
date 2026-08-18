# Data Model - Momentum Trading Assistant

**Owner:** Data Model & Domain Schema Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 2.30
**Last Updated:** 2026-08-18 (ST-10, EPIC-03, v8.9, BLG-BE-100 — transaction-isolation fix-or-accept decision documented for position_audit_log/position_state_history: audit-log write ordering); prior — 2026-08-14 (ST-09, EPIC-02, v8.8, BLG-BE-84 — DS-15 trade_plans.triggered_by_price_alert_id, reporting-treatment decision documented); prior — 2026-08-14 (ST-12, EPIC-02, v8.8, BLG-BE-94 — DS-14 signals functional index for UPPER(ticker), Head-of-Engineering-review correction); prior history retained — see prior entries in version control
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

This document describes the complete database schema and data structures used in the **Position Manager Web App**.

---

## Database Overview

**Database:** PostgreSQL 13+
**Schema:** Public (single schema)
**User Model:** Single user (multi-user planned for v2.0)

---

## 1. Portfolios Table

Primary portfolio container. Currently supports single portfolio per user.

```sql
CREATE TABLE public.portfolios (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    cash NUMERIC(12, 2) NOT NULL DEFAULT 20000.00,
    created_date DATE NOT NULL DEFAULT CURRENT_DATE,
    last_updated TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    CONSTRAINT portfolios_pkey PRIMARY KEY (id)
);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| cash | NUMERIC(12,2) | NO | Current cash balance (GBP). Default 20000.00. |
| created_date | DATE | NO | Portfolio creation date |
| last_updated | TIMESTAMP | NO | Last update timestamp |

### Notes
- `cash` is always in GBP. Updated on every position entry/exit.
- `initial_cash` does **not** exist in the deployed schema. Historical migration scripts (v1.2→v1.3) and earlier versions of `reset_staging_db.sql` referenced it — these are outdated. Do not add this column.
- `created_date` is a `DATE` (not `TIMESTAMP`). Earlier spec versions documented `created_at TIMESTAMP` which does not exist in the deployed DB.

**Schema verification (v2.2, 2026-04-02):** Confirmed against actual Supabase DB output (`CREATE TABLE public.portfolios` — provided by Product Owner 2026-04-02). Previous v2.1 note based on code inference was incorrect — direct DB confirmation supersedes it.

---

## 2. Positions Table

> **Lifecycle note:** This table serves both open and closed positions. All `exit_*` fields are `null` while `status = 'open'`. Queries must always filter by `status` unless intentionally spanning both lifecycle states — failure to do so is a common source of incorrect P&L aggregations.

```sql
CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    ticker VARCHAR(20) NOT NULL,
    market VARCHAR(5) NOT NULL CHECK (market IN ('US', 'UK')),
    entry_date DATE NOT NULL,
    entry_price DECIMAL(10, 4) NOT NULL,
    fill_price DECIMAL(10, 4),
    fill_currency VARCHAR(3),
    fx_rate DECIMAL(10, 6),
    shares DECIMAL(10, 4) NOT NULL,
    total_cost DECIMAL(12, 2) NOT NULL,
    fees_paid DECIMAL(10, 2) NOT NULL DEFAULT 0,
    fee_type VARCHAR(20),
    initial_stop DECIMAL(10, 4),
    current_stop DECIMAL(10, 4),
    current_price DECIMAL(10, 4),
    atr DECIMAL(10, 4),
    holding_days INTEGER DEFAULT 0,
    pnl DECIMAL(12, 2) DEFAULT 0,
    pnl_pct DECIMAL(10, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'closed')),
    exit_date DATE,
    exit_price DECIMAL(10, 4),
    exit_reason VARCHAR(50),
    entry_note TEXT,
    exit_note TEXT,
    tags TEXT[],
    user_fill_price DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    position_state VARCHAR(20),
    state_entered_at TIMESTAMP WITHOUT TIME ZONE,
    state_history JSONB NOT NULL DEFAULT '[]'::JSONB
);

CREATE INDEX idx_positions_portfolio ON positions(portfolio_id);
CREATE INDEX idx_positions_status ON positions(status);
CREATE INDEX idx_positions_ticker ON positions(ticker);
CREATE INDEX idx_positions_tags ON positions USING GIN(tags);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| ticker | VARCHAR(20) | NO | Stock symbol (e.g., "PLTR", "FRES.L") |
| market | VARCHAR(5) | NO | "US" or "UK" |
| entry_date | DATE | NO | Position entry date |
| entry_price | DECIMAL(10,4) | NO | Entry price in native currency (USD for US, GBP for UK) |
| fill_price | DECIMAL(10,4) | YES | Actual fill price in native currency |
| fill_currency | VARCHAR(3) | YES | "GBP" or "USD" |
| fx_rate | DECIMAL(10,6) | YES | GBP/USD rate at time of entry (US stocks) |
| shares | DECIMAL(10,4) | NO | Number of shares (fractional allowed) |
| total_cost | DECIMAL(12,2) | NO | Total cost including fees in GBP |
| fees_paid | DECIMAL(10,2) | NO | Total fees. NOT NULL as of v1.6 |
| fee_type | VARCHAR(20) | YES | Fee calculation method applied |
| initial_stop | DECIMAL(10,4) | YES | Stop price at entry |
| current_stop | DECIMAL(10,4) | YES | Current trailing stop price |
| current_price | DECIMAL(10,4) | YES | Last known price in native currency |
| atr | DECIMAL(10,4) | YES | ATR value at entry |
| holding_days | INTEGER | NO | Calendar days held (updated daily) |
| pnl | DECIMAL(12,2) | NO | Unrealised (open) or realised (closed) P&L in GBP |
| pnl_pct | DECIMAL(10,2) | NO | P&L as percentage of entry cost. Also returned as `pnl_percent` by the API |
| status | VARCHAR(20) | NO | `'open'` or `'closed'` |
| exit_date | DATE | YES | Exit date (null while open) |
| exit_price | DECIMAL(10,4) | YES | Exit price in native currency (null while open) |
| exit_reason | VARCHAR(50) | YES | Reason for exit (null while open) |
| entry_note | TEXT | YES | Journal note at entry |
| exit_note | TEXT | YES | Journal note at exit |
| tags | TEXT[] | YES | Strategy/classification tags |
| user_fill_price | DECIMAL(10,4) | YES | User-provided actual broker fill price in native currency (optional). Used to compute slippage. Null when not provided (pre-v2.1 trades). |
| created_at | TIMESTAMP | NO | Record creation timestamp |
| updated_at | TIMESTAMP | NO | Last update timestamp |
| position_state | VARCHAR(20) | YES | Lifecycle state: `GRACE`, `LOSING`, `PROFITABLE`, `EXIT ZONE`, `UNKNOWN`. Null for closed positions. Computed by `PositionLifecycleService`. Added v2.6. |
| state_entered_at | TIMESTAMP | YES | Timestamp when current `position_state` was assigned. Updated on each state transition. Null for closed positions. Added v2.6. |
| state_history | JSONB | NO | Ordered array of `{state, entered_at}` objects recording all state transitions. Default `[]`. Never truncated — full audit trail. Added v2.6. |

---

## 3. Trade History Table

Immutable record of closed trades. Written at exit time; never updated.

```sql
CREATE TABLE public.trade_history (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    portfolio_id UUID NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    ticker VARCHAR(20) NOT NULL,
    market VARCHAR(5) NULL,
    entry_date DATE NOT NULL,
    exit_date DATE NOT NULL,
    shares NUMERIC(10, 4) NOT NULL,
    entry_price NUMERIC(10, 4) NOT NULL,
    exit_price NUMERIC(10, 4) NOT NULL,
    total_cost NUMERIC(12, 2) NULL,
    gross_proceeds NUMERIC(12, 2) NULL,
    net_proceeds NUMERIC(12, 2) NULL,
    entry_fees NUMERIC(10, 2) NULL,
    exit_fees NUMERIC(10, 2) NULL,
    pnl NUMERIC(12, 2) NULL,
    pnl_pct NUMERIC(10, 2) NULL,
    holding_days INTEGER NULL,
    exit_reason VARCHAR(100) NULL,
    entry_fx_rate NUMERIC(10, 4) NULL,
    exit_fx_rate NUMERIC(10, 4) NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NULL DEFAULT now(),
    entry_note TEXT NULL,
    exit_note TEXT NULL,
    tags TEXT[] NULL,
    position_id UUID NULL REFERENCES positions(id),
    fill_price NUMERIC(10, 4) NULL,
    CONSTRAINT trade_history_pkey PRIMARY KEY (id)
);

CREATE INDEX idx_trade_history_portfolio ON public.trade_history USING btree (portfolio_id);
CREATE INDEX idx_trade_history_ticker ON public.trade_history USING btree (ticker);
CREATE INDEX idx_trade_history_tags ON public.trade_history USING gin (tags);
CREATE INDEX idx_trade_history_position_id ON public.trade_history USING btree (position_id);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | YES | FK to portfolios (ON DELETE CASCADE) |
| ticker | VARCHAR(20) | NO | Stock symbol |
| market | VARCHAR(5) | YES | "US" or "UK" |
| entry_date | DATE | NO | Original position entry date |
| exit_date | DATE | NO | Exit date |
| shares | NUMERIC(10,4) | NO | Shares exited |
| entry_price | NUMERIC(10,4) | NO | Entry price in native currency |
| exit_price | NUMERIC(10,4) | NO | Exit price in native currency |
| total_cost | NUMERIC(12,2) | YES | Entry cost in GBP (including fees) |
| gross_proceeds | NUMERIC(12,2) | YES | Exit value before fees in GBP |
| net_proceeds | NUMERIC(12,2) | YES | Exit value after exit fees in GBP |
| entry_fees | NUMERIC(10,2) | YES | Brokerage fees paid at entry (GBP) |
| exit_fees | NUMERIC(10,2) | YES | Brokerage fees paid at exit (GBP) |
| pnl | NUMERIC(12,2) | YES | Realised P&L in GBP (`net_proceeds − total_cost`) |
| pnl_pct | NUMERIC(10,2) | YES | P&L as percentage of entry cost. API also returns as `pnl_percent` for compatibility |
| holding_days | INTEGER | YES | Calendar days from entry_date to exit_date inclusive |
| exit_reason | VARCHAR(100) | YES | Reason for exit. `null` normalised to `"Manual Exit"` by analytics service at read time |
| entry_fx_rate | NUMERIC(10,4) | YES | GBP/USD rate at entry (US stocks only) |
| exit_fx_rate | NUMERIC(10,4) | YES | GBP/USD rate at exit (US stocks only) |
| created_at | TIMESTAMP | YES | Record creation time (defaults to now()) |
| entry_note | TEXT | YES | Journal note copied from position at exit time |
| exit_note | TEXT | YES | Journal note entered at exit |
| tags | TEXT[] | YES | Tags copied from position at exit time |
| position_id | UUID | YES | FK to originating position |
| fill_price | NUMERIC(10,4) | YES | Actual broker fill price copied from `positions.user_fill_price` at exit. Null when user did not provide a fill price at entry. Used to compute `slippage_pct` in the API response. Added by v1.9→v2.0 migration — confirmed present in Supabase DB (2026-04-02). |

### Exit Reason Values

| Value | Description |
|-------|-------------|
| `"Manual Exit"` | User-initiated exit outside of automated logic |
| `"Stop Loss Hit"` | Initial or trailing stop level breached |
| `"Trailing Stop"` | Trailing stop triggered after profitable period |
| `"Risk-Off Signal"` | Market regime turned risk-off |
| `"Target Reached"` | User defined profit target met |
| `"Partial Profit Taking"` | Partial exit to lock in gains |

> **Note:** `null` values in `exit_reason` are normalised to `"Manual Exit"` by the analytics service at read time. They are stored as `null` in this table.

---

## 4. Cash Transactions Table

Immutable ledger of all cash movements. Source of truth for cash balance history.

```sql
CREATE TABLE cash_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    type VARCHAR(20) NOT NULL CHECK (type IN ('deposit', 'withdrawal')),
    amount DECIMAL(12, 2) NOT NULL,
    date DATE NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cash_transactions_portfolio ON cash_transactions(portfolio_id);
CREATE INDEX idx_cash_transactions_date ON cash_transactions(date DESC);
```

---

## 5. Portfolio History Table

Daily portfolio value snapshots. Used for analytics (Sharpe ratio, drawdown). Written once per day via `POST /portfolio/snapshot`.

```sql
CREATE TABLE portfolio_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    snapshot_date DATE NOT NULL,
    total_value DECIMAL(12, 2) NOT NULL,
    cash_balance DECIMAL(12, 2) NOT NULL,
    positions_value DECIMAL(12, 2) NOT NULL,
    total_pnl DECIMAL(12, 2) NOT NULL,
    position_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (portfolio_id, snapshot_date)
);

CREATE INDEX idx_portfolio_history_portfolio ON portfolio_history(portfolio_id);
CREATE INDEX idx_portfolio_history_date ON portfolio_history(snapshot_date DESC);
```

### Notes
- The `UNIQUE (portfolio_id, snapshot_date)` constraint makes `POST /portfolio/snapshot` an idempotent upsert.
- A minimum of 30 snapshots is required for the portfolio-method Sharpe ratio calculation.
- The most recent snapshot's `total_value` is the `PortfolioValue` used by the Position Sizing Calculator (`strategy_rules.md §4.1.1`).

---

## 6. Settings Table

Global configuration for trading strategy, fee parameters, and UI preferences. Single row per deployment.

```sql
CREATE TABLE settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    min_hold_days INTEGER DEFAULT 10,
    atr_multiplier_initial DECIMAL(4, 2) DEFAULT 5.0,
    atr_multiplier_trailing DECIMAL(4, 2) DEFAULT 2.0,
    atr_period INTEGER DEFAULT 14,
    default_currency VARCHAR(3) DEFAULT 'GBP',
    theme VARCHAR(20) DEFAULT 'dark',
    uk_commission DECIMAL(10, 2) DEFAULT 9.95,
    us_commission DECIMAL(10, 2) DEFAULT 0.00,
    stamp_duty_rate DECIMAL(6, 5) DEFAULT 0.005,
    fx_fee_rate DECIMAL(6, 5) DEFAULT 0.0015,
    min_trades_for_analytics INTEGER DEFAULT 10,
    default_risk_percent DECIMAL(4, 2) NOT NULL DEFAULT 1.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT settings_risk_percent_check
        CHECK (default_risk_percent > 0 AND default_risk_percent <= 100)
);
```

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | UUID | — | Primary key |
| min_hold_days | INTEGER | 10 | Grace period in days. Stop losses not enforced during days 0–(n-1). With default `10`, grace covers days 0–9 inclusive; day 10 is the first day stop logic is active |
| atr_multiplier_initial | DECIMAL(4,2) | 5.0 | ATR multiplier for **losing** positions (wide stop, room to recover) |
| atr_multiplier_trailing | DECIMAL(4,2) | 2.0 | ATR multiplier for **profitable** positions (tight trailing stop to protect gains) |
| atr_period | INTEGER | 14 | ATR calculation lookback window in days |
| default_currency | VARCHAR(3) | GBP | Portfolio base currency. Display only — position-level currency is determined by market |
| theme | VARCHAR(20) | dark | UI theme preference (`'dark'` or `'light'`) |
| uk_commission | DECIMAL(10,2) | 9.95 | Fixed commission per UK trade in GBP |
| us_commission | DECIMAL(10,2) | 0.00 | Fixed commission per US trade in GBP (zero-commission brokers) |
| stamp_duty_rate | DECIMAL(6,5) | 0.005 | UK stamp duty rate on purchases (0.5%) |
| fx_fee_rate | DECIMAL(6,5) | 0.0015 | FX conversion fee rate for USD trades (0.15%) |
| min_trades_for_analytics | INTEGER | 10 | Minimum closed trades required before analytics metrics are computed |
| default_risk_percent | DECIMAL(4,2) | 1.00 | Default risk percentage pre-populated in the Position Sizing Calculator widget on the Trade Entry page. Represents percentage of portfolio value to risk per position (e.g. `1.00` = 1%). NOT NULL. Constraint: > 0 and ≤ 100. This is a user preference default, not an enforced position limit — users may override per trade. Added in v1.7. |
| created_at | TIMESTAMP | now | Record creation timestamp |
| updated_at | TIMESTAMP | now | Last update timestamp |

### Strategy parameter context

The default values (`min_hold_days: 10`, `atr_multiplier_initial: 5.0`, `atr_multiplier_trailing: 2.0`) reflect backtest-optimised parameters. Changes take effect on the next call to `GET /positions/analyze` and do not retroactively affect open positions.

### `default_risk_percent` design note

`DECIMAL(4,2)` supports values from `0.01` to `99.99`, covering the full practical range for risk percentage inputs. `NOT NULL DEFAULT 1.00` ensures the widget always has a value to pre-populate. The check constraint enforces the validity rule that `RiskPercent <= 0` is invalid (`strategy_rules.md §4.1.4`) and adds a safety ceiling at 100.

---

## 7. Signals Table

Generated trade signals from momentum screening. Each signal represents a candidate position for manual evaluation.

```sql
CREATE TABLE signals (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    market VARCHAR(5) NOT NULL,
    signal_date DATE NOT NULL,
    rank INTEGER NOT NULL,
    momentum_percent NUMERIC(10, 2) NOT NULL,
    current_price NUMERIC(10, 4) NOT NULL,
    price_gbp NUMERIC(10, 4) NOT NULL,
    atr_value NUMERIC(10, 4) NOT NULL,
    volatility NUMERIC(10, 6) NOT NULL,
    initial_stop NUMERIC(10, 4) NOT NULL,
    suggested_shares INTEGER NOT NULL,
    allocation_gbp NUMERIC(12, 2) NOT NULL,
    total_cost NUMERIC(12, 2) NOT NULL,
    status VARCHAR(20) NULL DEFAULT 'new',
    position_id UUID NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT signals_pkey PRIMARY KEY (id),
    CONSTRAINT signals_portfolio_id_ticker_signal_date_key
        UNIQUE (portfolio_id, ticker, signal_date),
    CONSTRAINT signals_portfolio_id_fkey
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(id),
    CONSTRAINT signals_position_id_fkey
        FOREIGN KEY (position_id) REFERENCES positions(id),
    CONSTRAINT signals_market_check
        CHECK (market IN ('US', 'UK')),
    CONSTRAINT signals_status_check
        CHECK (status IN ('new', 'entered', 'dismissed', 'expired', 'already_held', 'watchlisted'))
) TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_signals_portfolio
    ON signals USING btree (portfolio_id) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS idx_signals_status
    ON signals USING btree (status) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS idx_signals_date
    ON signals USING btree (signal_date DESC) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS idx_signals_ticker
    ON signals USING btree (ticker) TABLESPACE pg_default;
```

> **Note:** `suggested_shares` in the signals table is always an integer (whole shares). This differs from the Position Sizing Calculator which returns shares to 4 decimal places (`strategy_rules.md §4.1.3`). Signal generation does not support fractional shares.

---

## 8. Alert Rules Table

Configurable alert rule settings per portfolio. One row per alert type. Seeded automatically on first `GET /alerts/rules` call.

```sql
CREATE TABLE alert_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    type VARCHAR(50) NOT NULL CHECK (type IN (
        'stop_loss_approach',
        'grace_period_warning',
        'market_regime_change',
        'daily_portfolio_summary'
    )),
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    threshold_percent DECIMAL(5, 2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_alert_rules_portfolio_type UNIQUE (portfolio_id, type)
);

CREATE INDEX idx_alert_rules_portfolio ON alert_rules(portfolio_id);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| type | VARCHAR(50) | NO | Alert type key. One of the four valid values. |
| enabled | BOOLEAN | NO | Whether this rule is evaluated during alert evaluation. Default `true`. |
| threshold_percent | DECIMAL(5,2) | YES | Trigger threshold for `stop_loss_approach` only — fire when stop is within this % of current price. `null` for all other types. |
| created_at | TIMESTAMPTZ | NO | Rule creation timestamp |
| updated_at | TIMESTAMPTZ | NO | Last update timestamp |

### Constraints

- `UNIQUE (portfolio_id, type)` — one rule per type per portfolio.
- `threshold_percent` is not constrained at the DB level; the API layer validates `> 0 AND ≤ 100`.

### Default seeded values

| Type | enabled | threshold_percent |
|------|---------|-------------------|
| `stop_loss_approach` | `true` | `5.0` |
| `grace_period_warning` | `true` | `null` |
| `market_regime_change` | `true` | `null` |
| `daily_portfolio_summary` | `true` | `null` |

---

## 9. Notifications Table

Log of triggered alert instances. Written by `POST /alerts/evaluate`. Includes delivery tracking fields per ADR-003 retry model.

```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN (
        'stop_loss_approach',
        'grace_period_warning',
        'market_regime_change',
        'daily_portfolio_summary'
    )),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    context JSONB,
    read BOOLEAN NOT NULL DEFAULT FALSE,
    delivered BOOLEAN NOT NULL DEFAULT FALSE,
    delivery_attempted_at TIMESTAMPTZ,
    delivery_attempts INTEGER NOT NULL DEFAULT 0,
    delivery_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notifications_portfolio ON notifications(portfolio_id);
CREATE INDEX idx_notifications_created ON notifications(created_at DESC);
CREATE INDEX idx_notifications_read ON notifications(portfolio_id, read);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| alert_type | VARCHAR(50) | NO | Alert type key |
| title | string | NO | Human-readable alert title (e.g. `"Stop Loss Approach — AAPL"`) |
| message | TEXT | NO | One-line description of the event |
| context | JSONB | YES | Supplemental structured data (e.g. `{"ticker": "AAPL", "stop_price": 210.00, "current_price": 219.05, "proximity_percent": 4.2}`). Shape varies by alert type. |
| read | BOOLEAN | NO | `false` until marked read via API. |
| delivered | BOOLEAN | NO | `true` after successful email delivery. |
| delivery_attempted_at | TIMESTAMPTZ | YES | Timestamp of most recent delivery attempt. |
| delivery_attempts | INTEGER | NO | Count of delivery attempts (success or failure). Incremented on each attempt. |
| delivery_error | TEXT | YES | Error message from last failed delivery attempt. Cleared on success. |
| created_at | TIMESTAMPTZ | NO | Notification creation timestamp |
| updated_at | TIMESTAMPTZ | NO | Last update timestamp |

### Delivery retry model (ADR-003)

- On each `POST /alerts/evaluate`: notifications with `delivered = false` and `delivery_attempts < 3` have delivery re-enqueued.
- After 3 failed attempts: no further retries. `delivery_error` reflects the last failure reason.
- `daily_portfolio_summary`: at most one notification per `portfolio_id` per calendar day (UTC). Evaluation must not create a duplicate same-day summary.

### `context` field shapes by type

| Type | Context keys |
|------|-------------|
| `stop_loss_approach` | `ticker`, `stop_price`, `current_price`, `proximity_percent` |
| `grace_period_warning` | `ticker`, `holding_days`, `grace_days_remaining` |
| `market_regime_change` | `regime` (value: `"risk_off"`) |
| `daily_portfolio_summary` | `portfolio_value_gbp`, `open_position_count`, `unrealised_pnl_gbp` |

---

## 10. Notification Preferences Table

Per-alert-type email delivery preferences. One row per alert type per portfolio. Seeded automatically on first `GET /notifications/preferences` call.

```sql
CREATE TABLE notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN (
        'stop_loss_approach',
        'grace_period_warning',
        'market_regime_change',
        'daily_portfolio_summary'
    )),
    email_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_notification_preferences_portfolio_type UNIQUE (portfolio_id, alert_type)
);

CREATE INDEX idx_notification_preferences_portfolio ON notification_preferences(portfolio_id);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| alert_type | VARCHAR(50) | NO | Alert type key |
| email_enabled | BOOLEAN | NO | `true` = send email when this type triggers. Default `true`. |
| created_at | TIMESTAMPTZ | NO | Record creation timestamp |
| updated_at | TIMESTAMPTZ | NO | Last update timestamp |

### Constraints

- `UNIQUE (portfolio_id, alert_type)` — one preference row per type per portfolio.

### Channel scope (v2.1)

Email is the only delivery channel in v2.1. SMS is not implemented. The schema supports future channel columns (e.g. `sms_enabled`) without migration impact.

---

## 11. Price Alerts Table

User-created ticker/condition/threshold alerts. Many rows per portfolio, unconstrained by open positions. Evaluated as a step inside `POST /alerts/evaluate`. Introduced ST-02 (BLG-FE-116, EPIC-02, v7.5); schema pre-designed in `docs/specs/blg_fe_116_pre_implementation_readiness_pass.md` AC-01.

```sql
CREATE TABLE price_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    ticker VARCHAR(10) NOT NULL,
    condition VARCHAR(10) NOT NULL CHECK (condition IN ('above', 'below')),
    threshold_price NUMERIC(10, 4) NOT NULL CHECK (threshold_price > 0),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    triggered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_price_alerts_portfolio_active ON price_alerts(portfolio_id, active);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| ticker | VARCHAR(10) | NO | Not constrained to open positions or watchlist — any ticker accepted by `utils.pricing.get_current_price(ticker)`. |
| condition | VARCHAR(10) | NO | `above` or `below` — direction of the threshold crossing. |
| threshold_price | NUMERIC(10,4) | NO | Same precision as `positions.current_price`. Must be `> 0`. |
| active | BOOLEAN | NO | `true` until triggered (single-fire, not repeating) or explicitly deactivated by the user. |
| triggered_at | TIMESTAMPTZ | YES | `null` until fired. |
| created_at | TIMESTAMPTZ | NO | Alert creation timestamp |
| updated_at | TIMESTAMPTZ | NO | Last update timestamp |

### Constraints

- Per-portfolio active-alert cap of 50 enforced at the API layer (not the DB) — see `docs/specs/api_contracts/alerts_endpoints.md §POST /price-alerts`.

---

## Migration History

### Migration from v1.1 to v1.2

```sql
BEGIN;
ALTER TABLE positions ADD COLUMN fill_price DECIMAL(10, 4);
ALTER TABLE positions ADD COLUMN fill_currency VARCHAR(3);
ALTER TABLE positions ADD COLUMN fee_type VARCHAR(20);
COMMIT;
```

### Migration from v1.2 to v1.3

```sql
BEGIN;
CREATE TABLE cash_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    type VARCHAR(20) NOT NULL CHECK (type IN ('deposit', 'withdrawal')),
    amount DECIMAL(12, 2) NOT NULL,
    date DATE NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE portfolio_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    snapshot_date DATE NOT NULL,
    total_value DECIMAL(12, 2) NOT NULL,
    cash_balance DECIMAL(12, 2) NOT NULL,
    positions_value DECIMAL(12, 2) NOT NULL,
    total_pnl DECIMAL(12, 2) NOT NULL,
    position_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (portfolio_id, snapshot_date)
);
ALTER TABLE positions ALTER COLUMN shares TYPE DECIMAL(10, 4);
INSERT INTO cash_transactions (portfolio_id, type, amount, date, note)
SELECT id, 'deposit', initial_cash, created_at::date, 'Initial deposit (migration)'
FROM portfolios;
COMMIT;
```

### Migration from v1.3 to v1.4

```sql
BEGIN;
ALTER TABLE positions ADD COLUMN entry_note TEXT;
ALTER TABLE positions ADD COLUMN exit_note TEXT;
ALTER TABLE positions ADD COLUMN tags TEXT[];
ALTER TABLE trade_history ADD COLUMN entry_note TEXT;
ALTER TABLE trade_history ADD COLUMN exit_note TEXT;
ALTER TABLE trade_history ADD COLUMN tags TEXT[];
CREATE INDEX idx_positions_tags ON positions USING GIN(tags);
CREATE INDEX idx_trade_history_tags ON trade_history USING GIN(tags);
COMMIT;
```

### Migration from v1.4 to v1.5

```sql
BEGIN;
ALTER TABLE settings ADD COLUMN min_trades_for_analytics INTEGER DEFAULT 10;
COMMIT;
```

### Migration from v1.5 to v1.6

```sql
BEGIN;
ALTER TABLE positions ALTER COLUMN fees_paid SET NOT NULL;
CREATE TABLE signals (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    market VARCHAR(5) NOT NULL,
    signal_date DATE NOT NULL,
    rank INTEGER NOT NULL,
    momentum_percent NUMERIC(10, 2) NOT NULL,
    current_price NUMERIC(10, 4) NOT NULL,
    price_gbp NUMERIC(10, 4) NOT NULL,
    atr_value NUMERIC(10, 4) NOT NULL,
    volatility NUMERIC(10, 6) NOT NULL,
    initial_stop NUMERIC(10, 4) NOT NULL,
    suggested_shares INTEGER NOT NULL,
    allocation_gbp NUMERIC(12, 2) NOT NULL,
    total_cost NUMERIC(12, 2) NOT NULL,
    status VARCHAR(20) NULL DEFAULT 'new',
    position_id UUID NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT signals_pkey PRIMARY KEY (id),
    CONSTRAINT signals_portfolio_id_ticker_signal_date_key UNIQUE (portfolio_id, ticker, signal_date),
    CONSTRAINT signals_portfolio_id_fkey FOREIGN KEY (portfolio_id) REFERENCES portfolios(id),
    CONSTRAINT signals_position_id_fkey FOREIGN KEY (position_id) REFERENCES positions(id),
    CONSTRAINT signals_market_check CHECK (market IN ('US', 'UK')),
    CONSTRAINT signals_status_check CHECK (status IN ('new', 'entered', 'dismissed', 'expired', 'already_held'))
);
CREATE INDEX IF NOT EXISTS idx_signals_portfolio ON signals USING btree (portfolio_id);
CREATE INDEX IF NOT EXISTS idx_signals_status ON signals USING btree (status);
CREATE INDEX IF NOT EXISTS idx_signals_date ON signals USING btree (signal_date DESC);
CREATE INDEX IF NOT EXISTS idx_signals_ticker ON signals USING btree (ticker);
COMMIT;
```

### Migration from v1.6 to v1.7

**Purpose:** Add `default_risk_percent` to the settings table to support Position Sizing Calculator widget pre-population (roadmap item 3.2, Decision 5).

**Safety:** Safe to apply without downtime. `NOT NULL DEFAULT 1.00` means all existing rows receive `1.00` automatically at migration time. The check constraint is evaluated post-default so no existing row will violate it.

```sql
BEGIN;

ALTER TABLE settings
    ADD COLUMN default_risk_percent DECIMAL(4, 2) NOT NULL DEFAULT 1.00,
    ADD CONSTRAINT settings_risk_percent_check
        CHECK (default_risk_percent > 0 AND default_risk_percent <= 100);

COMMIT;
```

**Verification query (run after migration):**

```sql
SELECT id, default_risk_percent
FROM settings;
-- Expected: all rows show 1.00
```

### Migration from v1.9 to v2.0

**Purpose:** Add slippage tracking. `positions.user_fill_price` captures the user's actual broker fill at entry time (optional). `trade_history.fill_price` is copied from `user_fill_price` at exit and used to compute `slippage_pct` in the API response.

**Safety:** Both columns are nullable — no existing row will violate any constraint. Safe to apply without downtime.

```sql
BEGIN;
ALTER TABLE positions ADD COLUMN user_fill_price DECIMAL(10, 4);
ALTER TABLE trade_history ADD COLUMN fill_price DECIMAL(10, 4);
COMMIT;
```

---

## Deprecated Tables

**Documentation backfill — no new migration applied.** Added retroactively (v2.19, ST-04, EPIC-01, v7.10, BLG-BE-41 deprecated-table read-path audit) — this table's deprecation predates this section's existence and was previously undocumented here, discoverable only via `claude/backlog/backlog_archive.md`'s `BLG-BE-40` record. Recorded now so future deprecated-table audits (per `BLG-BE-41`'s own acceptance criteria — "cross-check against `data_model.md` migration history for tables marked deprecated") have a canonical entry to check against instead of re-deriving it from backlog history each time.

### `tickers` — superseded by `ticker_universe`

**Deprecated:** 2026-07-02 (v6.4, `BLG-BE-40`). **Superseded by:** `ticker_universe` (created via `services/ticker_universe_service.py::ensure_ticker_universe_table()`, not tracked as a numbered migration in this document since it is created idempotently at call time rather than via a one-off `ALTER`/`CREATE` migration script, consistent with this codebase's `ensure_*` convention).

`signal_service.py` read `tickers` directly until v6.4, when it was switched to `services.ticker_universe_service.get_all_tickers(active_only=True)` (`BLG-BE-40`, P1 production-correctness fix). A second, unused read of `tickers` was found in `database.py::get_all_tickers()` during this audit (`BLG-BE-41`) — confirmed to have zero callers anywhere in the codebase (dead code, not a live correctness bug) and removed in the same commit as this note.

Do not add new reads of `tickers`. All ticker-universe lookups must go through `services.ticker_universe_service`.

---

## Planned Future Schema Changes

### v1.8 — Trade Reflections (implemented — v1.9 Sprint 1)

One reflection record per closed trade. Upsert model — a reflection may be saved once and updated; skip leaves no record. Linked to `trade_history` by UUID.

```sql
CREATE TABLE trade_reflections (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trade_id              UUID NOT NULL REFERENCES trade_history(id) ON DELETE CASCADE,
    trade_rationale       TEXT,
    what_worked           TEXT,
    what_didnt_work       TEXT,
    discipline_assessment TEXT,
    key_takeaway          TEXT,
    created_at            TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_trade_reflections_trade UNIQUE (trade_id)
);

CREATE INDEX idx_trade_reflections_trade ON trade_reflections(trade_id);
```

#### Field definitions

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| trade_id | UUID | NO | FK to `trade_history.id`. Unique — one reflection per trade. |
| trade_rationale | TEXT | YES | "Why did you enter this trade? What was the setup?" |
| what_worked | TEXT | YES | "What did the trade do well?" |
| what_didnt_work | TEXT | YES | "What went wrong or was unexpected?" |
| discipline_assessment | TEXT | YES | "Did you follow your rules?" |
| key_takeaway | TEXT | YES | "One lesson from this trade." |
| created_at | TIMESTAMP | NO | First save timestamp |
| updated_at | TIMESTAMP | NO | Last save timestamp (equals created_at on first save) |

#### Design decisions

- **1:1 via UNIQUE constraint** — `UNIQUE (trade_id)` enforces one reflection per trade at the DB level. Backend should use `INSERT … ON CONFLICT (trade_id) DO UPDATE SET …, updated_at = NOW()`.
- **All five reflection fields nullable** — spec §6 permits submission with any subset, including all empty.
- **No portfolio FK** — derivable via `trade_history.portfolio_id`; omitted to keep the table lean.
- **`ON DELETE CASCADE`** — if the trade history record is deleted, its reflection is deleted with it.
- **Max lengths not enforced at DB level** — spec §5 states 500 chars per field; enforce at API validation layer to avoid migration overhead if limits change.

#### Required endpoints (to be documented in `docs/specs/api_contracts/trade_endpoints.md`)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/trades/{trade_id}/reflection` | Create or update reflection (upsert). |
| GET | `/trades/{trade_id}/reflection` | Retrieve existing reflection. Returns 404 if none saved yet. |

---

### v2.0 — Multi-User (Planned)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP
);

ALTER TABLE portfolios ADD COLUMN user_id UUID REFERENCES users(id);
```

---

### Migration from v1.8 to v1.9

**Purpose:** Introduce alert rules, notifications, and notification preferences tables for EPIC-02 Alerts & Notifications (v2.1). Replaces the placeholder v1.9 planned schema.

**Safety:** Safe to apply without downtime. All new tables — no changes to existing tables.

```sql
BEGIN;

CREATE TABLE alert_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    type VARCHAR(50) NOT NULL CHECK (type IN (
        'stop_loss_approach',
        'grace_period_warning',
        'market_regime_change',
        'daily_portfolio_summary'
    )),
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    threshold_percent DECIMAL(5, 2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_alert_rules_portfolio_type UNIQUE (portfolio_id, type)
);

CREATE INDEX idx_alert_rules_portfolio ON alert_rules(portfolio_id);

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN (
        'stop_loss_approach',
        'grace_period_warning',
        'market_regime_change',
        'daily_portfolio_summary'
    )),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    context JSONB,
    read BOOLEAN NOT NULL DEFAULT FALSE,
    delivered BOOLEAN NOT NULL DEFAULT FALSE,
    delivery_attempted_at TIMESTAMPTZ,
    delivery_attempts INTEGER NOT NULL DEFAULT 0,
    delivery_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notifications_portfolio ON notifications(portfolio_id);
CREATE INDEX idx_notifications_created ON notifications(created_at DESC);
CREATE INDEX idx_notifications_read ON notifications(portfolio_id, read);

CREATE TABLE notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN (
        'stop_loss_approach',
        'grace_period_warning',
        'market_regime_change',
        'daily_portfolio_summary'
    )),
    email_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_notification_preferences_portfolio_type UNIQUE (portfolio_id, alert_type)
);

CREATE INDEX idx_notification_preferences_portfolio ON notification_preferences(portfolio_id);

COMMIT;
```

**Verification query (run after migration):**

```sql
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('alert_rules', 'notifications', 'notification_preferences');
-- Expected: 3 rows
```

---

---

## DS-03 — Sector & Industry Enrichment (v2.4, 2026-04-24)

**Story:** ST-05 (EPIC-02, v2.9)

`sector` and `industry` are **virtual fields** returned by `GET /positions` (and future screener result endpoints). They are derived on-request from Yahoo Finance (`yfinance.Ticker.info`) and are not stored in the `positions` table.

**No database migration is required.** These fields are enriched at API response time via `services/sector_service.py`. Fields will be `null` when Yahoo Finance does not carry classification for a ticker (common for some UK-listed stocks).

| Field | Source | Type | Nullable | Description |
|-------|--------|------|----------|-------------|
| `sector` | `yfinance.Ticker.info['sector']` | String | YES | Yahoo Finance sector classification (e.g. "Technology") |
| `industry` | `yfinance.Ticker.info['industry']` | String | YES | Yahoo Finance industry classification (e.g. "Semiconductors") |

These fields appear in the `GET /positions` API response on each open position and in the screener result schema (`docs/specs/screener_results_schema.md §1.1`).

---

---

## DS-04 — Trade Plan Object (v2.5, 2026-04-30)

**Story:** ST-01 (EPIC-01, v3.1)

The `trade_plans` table stores structured pre-trade reasoning documents linked optionally to a position.

### Table: trade_plans

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS trade_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    position_id UUID REFERENCES positions(id) ON DELETE SET NULL,
    ticker VARCHAR(20) NOT NULL,
    market VARCHAR(10) NOT NULL CHECK (market IN ('US', 'UK')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    setup_thesis TEXT,
    entry_rationale TEXT,
    regime_context_at_entry VARCHAR(50),
    r_target NUMERIC(8,2),
    early_exit_conditions TEXT,
    confirmation_criteria TEXT,
    checklist_completed BOOLEAN NOT NULL DEFAULT FALSE,
    checklist_items JSONB NOT NULL DEFAULT '[]'::JSONB,
    status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'closed'))
);

CREATE INDEX idx_trade_plans_portfolio ON trade_plans(portfolio_id);
CREATE INDEX idx_trade_plans_position ON trade_plans(position_id) WHERE position_id IS NOT NULL;
CREATE INDEX idx_trade_plans_ticker_upper ON trade_plans (UPPER(ticker));
CREATE INDEX idx_trade_plans_status ON trade_plans(status);

COMMIT;
```

**Verification query (run after migration):**

```sql
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public' AND table_name = 'trade_plans';
-- Expected: 1 row
```

### Field Reference

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | UUID | NO | Primary key |
| `portfolio_id` | UUID | NO | Foreign key to `portfolios` |
| `position_id` | UUID | YES | Foreign key to `positions` — null if plan exists before position is opened |
| `ticker` | VARCHAR(20) | NO | Ticker symbol |
| `market` | VARCHAR(10) | NO | `US` or `UK` |
| `created_at` | TIMESTAMPTZ | NO | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | NO | Last update timestamp |
| `setup_thesis` | TEXT | YES | High-level setup thesis |
| `entry_rationale` | TEXT | YES | Specific entry rationale |
| `regime_context_at_entry` | VARCHAR(50) | YES | Regime status at time of plan creation (e.g. `risk_on`, `risk_off`) |
| `r_target` | NUMERIC(8,2) | YES | Target R-multiple for the trade |
| `early_exit_conditions` | TEXT | YES | Conditions that would prompt early exit |
| `confirmation_criteria` | TEXT | YES | Criteria needed before executing entry |
| `checklist_completed` | BOOLEAN | NO | Whether pre-entry checklist is signed off |
| `checklist_items` | JSONB | NO | Array of checklist items `[{item, checked}]` |
| `status` | VARCHAR(20) | NO | `draft`, `active`, `closed`, or `abandoned` |
| `abandonment_reason` | VARCHAR(500) | YES | Required when status=`abandoned`; enforced at API layer |

### Down Migration

```sql
BEGIN;
DROP TABLE IF EXISTS trade_plans;
COMMIT;
```

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-04-30
- Head of Specs Team: Accepted — 2026-04-30

---

## Trade Plan to Position Linkage

No schema change — this section formalises the `trade_plans.position_id` → `positions.id` relationship already in production, referenced by SI-02's linked-trade-plan gate condition (`current_roadmap.md`). Behaviour below reflects `BLG-BE-46` (v6.8) and `BLG-FE-109` (v7.3); see `docs/specs/data_model.md` change history for those migrations' schema entries.

### Relationship

- `trade_plans.position_id` is a nullable foreign key to `positions.id` (`ON DELETE SET NULL` — see Trade Plan Object above).
- Cardinality is one trade plan to zero-or-one positions. The FK has no database-level uniqueness constraint, but application logic (`position_service.add_position()`) only ever assigns a currently-unlinked plan (`position_id IS NULL`) to a new position, and never re-parents a plan that is already linked.
- `positions` carries no reverse `trade_plan_id` column. The reverse lookup (position → its plan) is a query against `trade_plans` filtered by `position_id` (`get_trade_plans_by_position()`).
- `trade_history` (closed-trade rows) links to `positions` via its own `position_id` FK — not directly to `trade_plans`. A closed trade's linked plan, if any, is therefore reached via a two-hop join: `trade_history.position_id = positions.id` AND `trade_plans.position_id = positions.id`.

### When the link is set

`position_service.add_position()` sets `trade_plans.position_id` at position-creation time, via one of two paths:
1. **Explicit** — the caller passes `trade_plan_id` (the "Start Trade from Plan" flow, `BLG-FE-109`/v7.3): the named plan is looked up directly via `get_trade_plan_by_id()`.
2. **Best-effort match** — no `trade_plan_id` supplied: `get_unlinked_trade_plan_for_entry()` looks for the most recent plan with `position_id IS NULL` matching the new position's ticker and market (`BLG-BE-46`/v6.8 forward-fix).

In both cases the link is written only if a matching plan is found and its `position_id` is still `NULL` — this makes the write idempotent and prevents re-parenting an already-linked plan.

### Nullability and backfill posture

- `position_id` is nullable by design: a plan can be drafted before any position exists (`status = 'draft'`), and plans never tied to an actual trade (abandoned, exploratory) are expected to remain unlinked indefinitely.
- The 11 `trade_plans` rows created before the `BLG-BE-46` fix (v6.8) have `position_id = NULL` and were **not backfilled** — a ticker/date-proximity match against `trade_history` was assessed at the time and judged unreliable (decision recorded in `claude/cycles/2026-07-08__release-v6.8/qa_evidence_EPIC-01.md` and `lessons_learnt_closure.md` LP-12). These rows remain permanently unlinked; only trade plans created after the v6.8 fix accrue toward SI-02's linked-trade-plan count.

### Known deviation — roadmap gate query

`current_roadmap.md`'s SI-02 gate condition (1) documents the linked-trade-plan check as `SELECT COUNT(*) FROM trade_history th JOIN trade_plans tp ON th.id = tp.position_id WHERE th.pnl IS NOT NULL`. Per the relationship above, `trade_plans.position_id` references `positions.id`, not `trade_history.id` — the correct join is a two-hop join through `positions` (`trade_history.position_id = positions.id AND trade_plans.position_id = positions.id`), not a direct `trade_history.id = trade_plans.position_id` comparison. This is a pre-existing inaccuracy in the roadmap note's ad hoc SQL, not a schema issue introduced here. Correcting `current_roadmap.md` is outside this routine's write scope (`claude/roadmap/*` — execution_prompt.md §7); flagged here for the Roadmap Rebalance Engine or Head of Specs Team to correct at the next roadmap touch, citing this section as the canonical reference.

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-07-27 (agent-mediated; documentation-only, no schema change, behaviour verified against `backend/services/position_service.py` and `tests/test_position_trade_plan_link.py`)

---

## DS-05 — Position Lifecycle State Fields (v2.6, 2026-05-10)

**Story:** ST-01 (EPIC-01, v3.3)

Three columns added to `positions` to support the Arc 3 position lifecycle state machine (IT-01). State is computed by `PositionLifecycleService` — never set by direct DB writes from other services.

### Up Migration (v2.5 → v2.6)

```sql
BEGIN;

ALTER TABLE positions
    ADD COLUMN position_state VARCHAR(20),
    ADD COLUMN state_entered_at TIMESTAMP WITHOUT TIME ZONE,
    ADD COLUMN state_history JSONB NOT NULL DEFAULT '[]'::JSONB;

-- Back-fill open positions: GRACE if opened within last 10 trading days (Mon–Fri),
-- UNKNOWN otherwise. Closed positions remain NULL (no active lifecycle state).
WITH computed AS (
    SELECT
        id,
        CASE
            WHEN (
                SELECT COUNT(*)
                FROM generate_series(
                    entry_date::date + INTERVAL '1 day',
                    CURRENT_DATE,
                    INTERVAL '1 day'
                ) AS d
                WHERE EXTRACT(DOW FROM d) NOT IN (0, 6)
            ) <= 10 THEN 'GRACE'
            ELSE 'UNKNOWN'
        END AS new_state
    FROM positions
    WHERE status = 'open'
)
UPDATE positions p
SET
    position_state = c.new_state,
    state_entered_at = NOW(),
    state_history = jsonb_build_array(
        jsonb_build_object('state', c.new_state, 'entered_at', NOW()::text)
    )
FROM computed c
WHERE p.id = c.id;

COMMIT;
```

**Verification query (run after migration):**

```sql
SELECT position_state, COUNT(*) FROM positions WHERE status = 'open' GROUP BY position_state;
-- Expected: rows for GRACE and/or UNKNOWN; no NULLs for open positions
SELECT COUNT(*) FROM positions WHERE status = 'open' AND state_history = '[]'::jsonb;
-- Expected: 0
```

### Down Migration (v2.6 → v2.5)

```sql
BEGIN;
ALTER TABLE positions
    DROP COLUMN IF EXISTS position_state,
    DROP COLUMN IF EXISTS state_entered_at,
    DROP COLUMN IF EXISTS state_history;
COMMIT;
```

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-05-10
- Head of Specs Team: Accepted — 2026-05-10

### Known Deviations

| Field | Detail |
|-------|--------|
| Description | ST-01 AC specified "Alembic migration script"; implementation used project-standard direct SQL migration (documented in this section). Alembic is not used in this project — direct SQL migrations are the canonical project pattern. |
| Canonical requirement | ST-01 acceptance criteria (sprint_backlog.md v3.3): "Alembic migration script created and applied" |
| Priority | P3 — cosmetic spec wording mismatch; implementation is correct for project |
| Target resolution release | v3.4 — update sprint backlog template to specify "direct SQL migration" instead of "Alembic migration" for future stories |
| Owner | Data Model Domain & Schema Owner |
| Backlog reference | No separate backlog item filed — accepted as correct project pattern per Data Model owner sign-off 2026-05-10; documented as DEV-v33-01 in verification_report.md §4 (cycle 2026-05-09__release-v3.3) |

---

## DS-06 — Add abandonment_reason to trade_plans (v2.7, 2026-05-10)

**Story:** ST-17 (EPIC-04, v3.3)

Adds `abandonment_reason` as a nullable VARCHAR column to support the trade plan abandonment feature (BLG-FEAT-21). The column is enforced non-null at the API layer when `status = 'abandoned'`; no DB constraint is applied so that existing rows and programmatic transitions are unaffected.

### Up Migration (v2.6 → v2.7)

```sql
BEGIN;
ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS abandonment_reason VARCHAR(500) NULL;
COMMIT;
```

### Verification

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'trade_plans' AND column_name = 'abandonment_reason';
-- Expected: 1 row, data_type character varying, is_nullable YES
```

### Down Migration (v2.7 → v2.6)

```sql
BEGIN;
ALTER TABLE trade_plans DROP COLUMN IF EXISTS abandonment_reason;
COMMIT;
```

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-05-10 (agent-mediated, v3.3 sprint execution)

---

---

## DS-07 — Add watchlisted to signals_status_check (v2.8, 2026-05-18)

**Story:** ST-01 (EPIC-01, v3.7)

Extends the `signals_status_check` CHECK constraint to include `'watchlisted'` status. This supports the signal-to-watchlist workflow (BLG-FE-33): when a user adds a ticker to the watchlist from a signal card, the signal is transitioned to `status = 'watchlisted'`. The existing statuses (`new`, `entered`, `dismissed`, `expired`, `already_held`) are unchanged.

### Up Migration (v2.7 → v2.8)

```sql
BEGIN;
ALTER TABLE signals DROP CONSTRAINT IF EXISTS signals_status_check;
ALTER TABLE signals ADD CONSTRAINT signals_status_check
    CHECK (status IN ('new', 'entered', 'dismissed', 'expired', 'already_held', 'watchlisted'));
COMMIT;
```

### Verification

```sql
SELECT constraint_name, check_clause
FROM information_schema.check_constraints
WHERE constraint_name = 'signals_status_check';
-- Expected: 1 row with check_clause containing 'watchlisted'
```

### Down Migration (v2.8 → v2.7)

```sql
BEGIN;
ALTER TABLE signals DROP CONSTRAINT IF EXISTS signals_status_check;
ALTER TABLE signals ADD CONSTRAINT signals_status_check
    CHECK (status IN ('new', 'entered', 'dismissed', 'expired', 'already_held'));
COMMIT;
```

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-05-18 (agent-mediated, v3.7 sprint execution)

---

---

## DS-08 — Add commission and spread cost columns to trade_history (v2.9, 2026-06-19)

**Story:** ST-03 (EPIC-02, v6.0) — BLG-FEAT-20

Adds two optional cost columns to `trade_history` to support net-of-costs performance tracking. Both columns are nullable; existing rows are unaffected. The migration is idempotent (`ADD COLUMN IF NOT EXISTS`).

### Up Migration (v2.8 → v2.9)

```sql
BEGIN;
ALTER TABLE trade_history ADD COLUMN IF NOT EXISTS commission_gbp NUMERIC(10, 2);
ALTER TABLE trade_history ADD COLUMN IF NOT EXISTS spread_cost_gbp NUMERIC(10, 2);
COMMIT;
```

### Verification

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'trade_history'
  AND column_name IN ('commission_gbp', 'spread_cost_gbp');
-- Expected: 2 rows, data_type=numeric, is_nullable=YES
```

### Down Migration (v2.9 → v2.8)

```sql
BEGIN;
ALTER TABLE trade_history DROP COLUMN IF EXISTS commission_gbp;
ALTER TABLE trade_history DROP COLUMN IF EXISTS spread_cost_gbp;
COMMIT;
```

### New computed field: net_r_multiple

`net_r_multiple` is not stored in the database. It is computed at query time in `trade_service.get_trade_history_with_stats()` using the formula:

```
net_r = (pnl - commission_gbp - spread_cost_gbp) / initial_risk_gbp
```

where `initial_risk_gbp = (entry_price - stop_price_at_entry) × shares / fx_rate` (USD-denominated positions are converted to GBP). Returns `null` when cost data or stop data is absent.

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-06-19 (agent-mediated, v6.0 sprint execution)

---

## DS-09 — Add thesis_feedback to trade_plans (v2.10, 2026-07-03)

**Story:** ST-07 (EPIC-03, v6.5) — BLG-FE-46

Adds one nullable column to `trade_plans` to persist the Claude thesis generation feedback control (`docs/design/2026-07-02__release-v6.5/thesis-feedback-mechanism/ux_spec.md`). Feeds ST-08's `thesis_adoption_rate` metric (`docs/specs/metrics_definitions.md#Thesis Adoption Rate`).

### Up Migration (v2.9 → v2.10)

```sql
BEGIN;
ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS thesis_feedback VARCHAR(20)
    CHECK (thesis_feedback IN ('useful', 'not_useful'));
COMMIT;
```

### Verification

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'trade_plans' AND column_name = 'thesis_feedback';
-- Expected: 1 row, data_type=character varying, is_nullable=YES
```

### Down Migration (v2.10 → v2.9)

```sql
BEGIN;
ALTER TABLE trade_plans DROP COLUMN IF EXISTS thesis_feedback;
COMMIT;
```

**Persistence approach note:** the UX spec recommended a `thesis_feedback` field on `claude_audit_log` (attributed to the specific generation call). That table has no `plan_id` column (see `docs/specs/metrics_definitions.md#Thesis Adoption Rate` Query Approach note for the same finding at ST-08), so attributing feedback to a specific `claude_audit_log` row was not viable without a schema change to that table too. Storing on `trade_plans` directly avoids a second migration, requires no new endpoint (feedback rides the existing `POST /trade-plans` / `PUT /trade-plans/{id}` payload), and is sufficient for AC-02 ("feedback data persisted") — the spec's own wording frames the `claude_audit_log` approach as "a recommendation, not a hard constraint."

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-07-03 (agent-mediated, v6.5 sprint execution)

---

## DS-10 — Backfill: plan_vs_reality (trade_history) and planned_stop_price (trade_plans) (v2.11, 2026-07-03)

**Story:** ST-05 (EPIC-02, v3.5) — PO-01 Plan vs Reality

**Documentation backfill — no new migration applied.** These two columns were migrated into production on 2026-05-15 (v3.5) via `ensure_plan_vs_reality_columns()` at startup, but were only ever documented in `docs/data_model.md` — a non-canonical Class 2 (Supporting) file that had drifted into an independent fork rather than pointing at this document as its canonical source. That file is now marked Deprecated; this entry backfills the gap so the schema is documented in one place.

### Schema (already live since v3.5)

```sql
ALTER TABLE trade_history ADD COLUMN IF NOT EXISTS plan_vs_reality JSONB;
ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS planned_stop_price NUMERIC(20, 6);
```

### Field Reference

| Table | Field | Type | Description |
|-------|-------|------|-------------|
| `trade_history` | `plan_vs_reality` | JSONB | Plan vs Reality comparison record (PO-01). Populated by `plan_vs_reality_service` on trade close. NULL if no trade plan was linked. |
| `trade_plans` | `planned_stop_price` | NUMERIC(20,6) | Planned stop price at plan creation. Optional; NULL for plans created before v3.5. Per `docs/product/arc4_data_requirements.md` §3.1 Decision 1. |

#### `plan_vs_reality` JSONB structure

| Key | Type | Description |
|-----|------|-------------|
| plan_linked | boolean | Whether a trade plan was linked |
| trade_plan_id | uuid | ID of the linked trade plan |
| r_achieved | float \| null | Actual R-multiple achieved: (exit - entry) / (entry - initial_stop) |
| r_target | float \| null | Planned R target from trade plan |
| r_delta | float \| null | r_achieved - r_target |
| entry_delta_pct | float \| null | Entry timing accuracy: (actual - planned) / planned * 100. Null until planned_entry_price snapshot is implemented. |
| stop_discipline | string | "on_plan" / "minor_deviation" / "deviation" / "not_captured" |
| exit_reason_actual | string \| null | Actual exit reason |
| exit_reason_planned | string \| null | Planned early exit conditions (free text) |
| lifecycle_state_at_exit | string \| null | Position lifecycle state at time of exit |
| plan_adherence_flag | string | "on_plan" / "entry_deviation" / "stop_deviation" / "early_exit" |
| deviation_note | string \| null | User-authored deviation note (populated via ST-06 frontend view) |

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-07-03 (backfill, agent-mediated)

---

### Migration from v2.11 to v2.12

ST-15 (BLG-FEAT-68, EPIC-03, v7.0) — position review cadence nudge.

```sql
BEGIN;
ALTER TABLE positions ADD COLUMN IF NOT EXISTS last_reviewed_at TIMESTAMP WITH TIME ZONE;
COMMIT;
```

| Field | Type | Description |
|-------|------|--------------|
| `last_reviewed_at` | timestamptz \| null | Nullable; null means the position has never been marked reviewed. Set to `NOW()` by `PATCH /positions/{id}/mark-reviewed`. Drives the "Last Reviewed" column/card-footer nudge (`positions.md` §Last Reviewed Column) — flagged amber when `days_since_review >= 14`, suppressed while the position is already surfaced by the Grace Period Alert Zone or the portfolio-level Drawdown Review Prompt. |

Reversible: `ALTER TABLE positions DROP COLUMN IF EXISTS last_reviewed_at;`

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-07-13 (agent-mediated, single nullable column addition, no backfill required)

---

## Saved Filters Table

Named, server-side Trade History filter presets (ST-04, BLG-FE-118, EPIC-04, v7.5). A user may create an arbitrary number of presets — a many-rows-per-portfolio table, structurally distinct from the singleton `settings` row (per readiness pass AC-01, same rationale already applied to `alert_rules`/`price_alerts` and `saved_filters`'s own readiness pass). Distinct from the page's ephemeral, device-local active-filter state (BLG-FE-40 localStorage-envelope pattern) — these rows persist across devices/sessions until explicitly deleted.

```sql
CREATE TABLE saved_filters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    name VARCHAR(100) NOT NULL,
    filter_state JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_saved_filters_portfolio_name UNIQUE (portfolio_id, name)
);

CREATE INDEX idx_saved_filters_portfolio ON saved_filters(portfolio_id);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| name | VARCHAR(100) | NO | Preset name, unique per portfolio |
| filter_state | JSONB | NO | Serialised filter selection (market, result, date range, tags) — shape owned by the frontend, opaque to the backend |
| created_at | TIMESTAMPTZ | NO | Preset creation timestamp |
| updated_at | TIMESTAMPTZ | NO | Last update timestamp |

### Constraints

- `UNIQUE (portfolio_id, name)` — one preset per name per portfolio; `POST /saved-filters` returns `400` on collision.

---

### Migration from v2.12 to v2.13

ST-02 (BLG-FE-116, EPIC-02, v7.5) — custom price alerts (`price_alerts` table + `notifications.alert_type` CHECK extension per readiness pass AC-01).

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS price_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    ticker VARCHAR(10) NOT NULL,
    condition VARCHAR(10) NOT NULL CHECK (condition IN ('above', 'below')),
    threshold_price NUMERIC(10, 4) NOT NULL CHECK (threshold_price > 0),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    triggered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_price_alerts_portfolio_active ON price_alerts(portfolio_id, active);

ALTER TABLE notifications DROP CONSTRAINT IF EXISTS notifications_alert_type_check;
ALTER TABLE notifications ADD CONSTRAINT notifications_alert_type_check CHECK (alert_type IN (
    'stop_loss_approach',
    'grace_period_warning',
    'market_regime_change',
    'daily_portfolio_summary',
    'custom_price_alert'
));

COMMIT;
```

Reversible:
```sql
BEGIN;
ALTER TABLE notifications DROP CONSTRAINT IF EXISTS notifications_alert_type_check;
ALTER TABLE notifications ADD CONSTRAINT notifications_alert_type_check CHECK (alert_type IN (
    'stop_loss_approach',
    'grace_period_warning',
    'market_regime_change',
    'daily_portfolio_summary'
));
DROP TABLE IF EXISTS price_alerts;
COMMIT;
```

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-07-17 (agent-mediated, schema pre-designed and PASS-reviewed in readiness pass `blg_fe_116_pre_implementation_readiness_pass.md` AC-01/§13, no deviation from pre-scoped shape)

---

### Migration from v2.13 to v2.14

ST-03 (BLG-FE-117, EPIC-03, v7.5) — bulk actions toolbar: adds a `tags` column to `watchlist` for the new Bulk Tag action (`bulk-actions-toolbar/ux_spec.md` §2.4). No single-item tag UI is introduced — bulk-tag only. **Note:** the `watchlist` table itself predates a canonical schema section in this document (created via `watchlist_service.py`'s idempotent bootstrap, migration v2.0→v2.1 per that service's module docstring); this entry documents only the incremental `tags` column addition, not a full backfill of the missing canonical section (tracked as spec debt, out of scope for ST-03). **Renumbered during cross-EPIC merge conflict resolution (CLAUDE.md §8):** originally authored as "v2.12→v2.13" on the EPIC-03 branch in parallel with EPIC-02's own v2.12→v2.13 migration; since EPIC-02 merged first, this entry is renumbered v2.13→v2.14 to keep migration numbering sequential — no schema content change.

```sql
BEGIN;
ALTER TABLE watchlist ADD COLUMN IF NOT EXISTS tags TEXT[] NOT NULL DEFAULT '{}';
COMMIT;
```

| Field | Type | Description |
|-------|------|--------------|
| `tags` | text[] | Not null, defaults to `{}`. Populated only via `POST /watchlist/bulk-tag` (union with existing tags, not replace) — no single-item create/edit UI sets this field. |

Reversible: `ALTER TABLE watchlist DROP COLUMN IF EXISTS tags;`

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-07-17 (agent-mediated, single nullable-equivalent array column with a safe default, no backfill required, no existing data affected)

---

### Migration from v2.14 to v2.15

ST-04 (BLG-FE-118, EPIC-04, v7.5) — saved filter presets (`saved_filters` table, per readiness pass AC-01). **Renumbered during cross-EPIC merge conflict resolution (CLAUDE.md §8):** originally authored as "v2.12→v2.13" on the EPIC-04 branch in parallel with EPIC-02's and EPIC-03's own migrations; since EPIC-02 and EPIC-03 merged first (claiming v2.13 and v2.14 respectively), this entry is renumbered v2.14→v2.15 to keep migration numbering sequential — no schema content change.

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS saved_filters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    name VARCHAR(100) NOT NULL,
    filter_state JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_saved_filters_portfolio_name UNIQUE (portfolio_id, name)
);

CREATE INDEX IF NOT EXISTS idx_saved_filters_portfolio ON saved_filters(portfolio_id);

COMMIT;
```

Reversible: `DROP TABLE IF EXISTS saved_filters;`

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — 2026-07-20 (agent-mediated, schema pre-designed and reasoned in readiness pass `blg_fe_118_pre_implementation_readiness_pass.md` AC-01, no deviation from pre-scoped shape)

---

### Migration from v2.16 to v2.17

ST-06 (BLG-BE-73, EPIC-06, v7.9) — audit trail for manual position overrides. Financial Reporting & Records Owner scope decision (recorded in `execution_state.json` for this story): "manual position overrides" covers the three genuinely user-initiated, manual PATCH endpoints that sit outside the automated trade lifecycle — note edit, tag edit, mark-reviewed — not a new core-trade-field override feature (no such endpoint exists in this product). Distinct from `BLG-SEC-14`'s AI-journal-generation audit trail (a different write path). No "who" column — single-user product, same precedent as `claude_audit_log` (§ above), which also carries no per-user identity field.

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS position_audit_log (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    position_id  UUID NOT NULL,
    source       TEXT NOT NULL,
    field        TEXT NOT NULL,
    before_value TEXT,
    after_value  TEXT,
    changed_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_position_audit_log_position_id ON position_audit_log(position_id);

COMMIT;
```

### Field Reference

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | UUID | NO | Primary key |
| `position_id` | UUID | NO | The position edited. No FK constraint (audit rows must survive a position's own lifecycle; matches `trade_history.position_id`'s pattern of not cascading) |
| `source` | TEXT | NO | Which manual action triggered the entry: `note`, `tags`, or `mark-reviewed` |
| `field` | TEXT | NO | The specific field changed (`entry_note`, `tags`, `last_reviewed_at`) |
| `before_value` | TEXT | YES | Value before the edit, stringified |
| `after_value` | TEXT | YES | Value after the edit, stringified |
| `changed_at` | TIMESTAMPTZ | NO | When the edit was recorded |

Reversible: `DROP TABLE IF EXISTS position_audit_log;`

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-07-27 (agent-mediated; single new append-only table, no existing schema touched, no backfill applicable — table did not previously exist)
- Financial Reporting & Records Owner: Accepted — 2026-07-27 (agent-mediated; scope decision recorded above)

**Transaction isolation decision (ST-10, BLG-BE-100, EPIC-03, v8.9):** `position_audit_log` and `position_state_history` (DS-13 below) writes are never in the same DB transaction as the primary state update they record — each uses its own independent `get_db()` connection. Reviewed both call sites for the resulting risk ("does the audit row get written when the primary write fails, or omitted when it shouldn't be"):
- **`position_audit_log` — accept, no change.** All 3 call sites (`services/position_service.py::update_note`/`mark_position_reviewed`/`update_tags`) already call the primary write first and the audit write only after it returns successfully; if the primary write raises, execution never reaches the audit call. Safe by construction (call ordering), without needing literal transactional atomicity across the two connections. No fix required.
- **`position_state_history` — fixed, not accepted.** Unlike `position_audit_log`, `refresh_position_lifecycle()` (`services/position_lifecycle_service.py`) called the audit write (`create_position_state_history_entry`) *before* the primary write (`update_position_lifecycle_state`) — a primary-write failure immediately after a successful audit insert would leave a `position_state_history` row recording a transition that never actually landed on `positions.position_state`. Reordered to primary-then-audit, matching `position_audit_log`'s already-safe pattern. Regression coverage: `tests/test_position_state_history.py::test_primary_write_runs_before_audit_write`, `test_audit_write_not_reached_when_primary_write_raises`.
- Data Model & Domain Schema Owner: Accepted (position_audit_log ordering) / Confirmed fix (position_state_history reorder) — 2026-08-18 (agent-mediated; no schema change, ordering-only code fix, both audit tables' own fail-open non-blocking convention is unchanged)

---

### Migration from v2.17 to v2.18

ST-02 (BLG-FEAT-67, EPIC-02, v7.9) — historical sector/regime exposure trend. **Data-dependency correction (Metrics Definitions & Analytics Owner amendment, agent-mediated, 2026-07-27):** the backlog item and its UX spec both stated this feature was "purely a historical view of data already captured" requiring "no new data collection." Investigation found this false — neither `GET /portfolio/sector-weights` nor `GET /market/status` ever persisted their live-computed figures anywhere; `portfolio_history` (§5 above) has no per-sector or per-regime granularity. This table introduces new data collection, **going forward only** — no retroactive backfill was attempted (there is no reliable way to reconstruct past sector allocations or regime status from current live-computed data without fabricating history).

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS sector_regime_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    snapshot_date DATE NOT NULL,
    sectors JSONB NOT NULL DEFAULT '[]',
    regime_us BOOLEAN,
    regime_uk BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (portfolio_id, snapshot_date)
);

CREATE INDEX IF NOT EXISTS idx_sector_regime_history_portfolio_date
    ON sector_regime_history (portfolio_id, snapshot_date DESC);

COMMIT;
```

### Field Reference

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | UUID | NO | Primary key |
| `portfolio_id` | UUID | NO | FK to `portfolios` |
| `snapshot_date` | DATE | NO | Date this row was captured. One row per portfolio per day (upsert, same idempotency pattern as `portfolio_history`) |
| `sectors` | JSONB | NO | Array of `{sector_name, position_count, exposure_pct}` — same shape as `GET /portfolio/sector-weights`'s live response, captured at snapshot time |
| `regime_us` | BOOLEAN | YES | SPY-based US regime status that day (`true` = risk-on), from `utils.pricing.check_market_regime()` |
| `regime_uk` | BOOLEAN | YES | FTSE-based UK regime status that day (`true` = risk-on), from the same function |
| `created_at` | TIMESTAMP | YES | Row creation/update timestamp |

Populated by `portfolio_service.create_daily_snapshot()` (the existing daily job, triggered by `POST /portfolio/snapshot` — same nightly cadence as `portfolio_history`), best-effort/fail-open — a capture failure here never blocks the main portfolio snapshot.

Reversible: `DROP TABLE IF EXISTS sector_regime_history;`

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-07-27 (agent-mediated; single new table, no existing schema touched, no backfill possible or attempted — see data-dependency correction above)
- Metrics Definitions & Analytics Owner: Accepted — 2026-07-27 (agent-mediated; confirmed going-forward-only capture is the correct approach over fabricating retroactive history — see full decision recorded in `execution_state.json` for this story)

---

## DS-11 — Add strategy_version_at_entry to trade_plans and positions (v2.20, 2026-07-30)

**Story:** ST-01 (EPIC-01, v8.0) — BLG-SPEC-78

Adds one nullable column to each of `trade_plans` and `positions`, stamped at row-creation time with the currently active strategy version label (`backend/strategy_version_registry.py::get_current_strategy_version()`, which returns the last entry of `STRATEGY_VERSION_REGISTRY` — maintained in the same commit as any new `strategy_rules.md` Change Log row). This is a direct, unambiguous version tag on newly created rows, distinct from the derived-window attribution approach `strategy_version_registry.resolve_version_window()` provides for historical `trade_history` rows that predate this field (SI-04, v7.7 ST-01) — that derivation remains the only attribution mechanism for pre-v8.0 rows.

### Up Migration (v2.19 → v2.20)

```sql
BEGIN;
ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS strategy_version_at_entry VARCHAR(10);
ALTER TABLE positions ADD COLUMN IF NOT EXISTS strategy_version_at_entry VARCHAR(10);
COMMIT;
```

### Verification

```sql
SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name IN ('trade_plans', 'positions') AND column_name = 'strategy_version_at_entry';
-- Expected: 2 rows, data_type=character varying, is_nullable=YES
```

### Down Migration (v2.20 → v2.19)

```sql
BEGIN;
ALTER TABLE trade_plans DROP COLUMN IF EXISTS strategy_version_at_entry;
ALTER TABLE positions DROP COLUMN IF EXISTS strategy_version_at_entry;
COMMIT;
```

### Field Reference

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `strategy_version_at_entry` | VARCHAR(10) | YES | Strategy version label (e.g. `"1.4"`) active at the moment this `trade_plans` / `positions` row was created. Populated forward-only — existing rows created before this migration remain `NULL`, and no backfill was attempted (their attribution, where needed, still goes through `resolve_version_window()`'s derived-window approach against `entry_date`). |

**Population points:** `backend/routers/trade_plans.py::create_plan()` (trade_plans) and `backend/services/position_service.py::add_position()` (positions), both via `get_current_strategy_version()` immediately before the row is written — mirrors the existing `portfolio_value_at_entry` / `effective_settings_snapshot` "capture-at-creation" pattern already used on `trade_plans` (DS-07/SI-02).

Reversible: see Down Migration above.

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-07-30 (agent-mediated; two nullable columns, no existing schema touched, no backfill attempted — forward-only by design per AC)
- Financial Reporting & Records Owner: Accepted — 2026-07-30 (agent-mediated; no impact to existing P&L/reporting computations, additive field only)

---

## Backtest Trades Table

Imported backtest results from `production_strategy.py` CSV outputs, used to compare historical backtest performance against live trade history on the Strategy Benchmark page (ST-11, EPIC-03, v6.3, BLG-FEAT-53). Two sibling tables, `backtest_yearly_performance` and `backtest_open_positions`, are created by the same idempotent function and documented alongside it below.

```sql
CREATE TABLE IF NOT EXISTS backtest_trades (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    entry_date DATE NOT NULL,
    exit_date DATE NOT NULL,
    holding_days INTEGER,
    entry_price NUMERIC(12, 4),
    exit_price NUMERIC(12, 4),
    pnl_gbp NUMERIC(12, 2),
    pnl_pct NUMERIC(8, 4),
    market VARCHAR(10) NOT NULL DEFAULT 'US',
    exit_reason VARCHAR(50),
    was_profitable BOOLEAN,
    entry_year INTEGER NOT NULL,
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (ticker, entry_date, exit_date)
);

CREATE TABLE IF NOT EXISTS backtest_yearly_performance (
    id SERIAL PRIMARY KEY,
    entry_year INTEGER NOT NULL,
    num_trades INTEGER,
    avg_pnl_gbp NUMERIC(12, 2),
    total_pnl_gbp NUMERIC(12, 2),
    avg_hold_days NUMERIC(8, 2),
    win_rate_pct NUMERIC(5, 2),
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (entry_year)
);

CREATE TABLE IF NOT EXISTS backtest_open_positions (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    entry_date DATE NOT NULL,
    entry_price NUMERIC(12, 4),
    current_price NUMERIC(12, 4),
    unrealized_pnl_gbp NUMERIC(12, 2),
    unrealized_pnl_pct NUMERIC(8, 4),
    market VARCHAR(10) NOT NULL DEFAULT 'US',
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (ticker, entry_date)
);
```

### Fields — `backtest_trades`

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | SERIAL | NO | Primary key |
| ticker | VARCHAR(20) | NO | Ticker symbol |
| entry_date | DATE | NO | Backtest entry date |
| exit_date | DATE | NO | Backtest exit date |
| holding_days | INTEGER | YES | Days held |
| entry_price | NUMERIC(12,4) | YES | Entry price (backtest currency) |
| exit_price | NUMERIC(12,4) | YES | Exit price |
| pnl_gbp | NUMERIC(12,2) | YES | Realised P&L in GBP |
| pnl_pct | NUMERIC(8,4) | YES | Realised P&L percentage |
| market | VARCHAR(10) | NO | `US` or `UK`, default `US` |
| exit_reason | VARCHAR(50) | YES | Backtest exit trigger label |
| was_profitable | BOOLEAN | YES | Convenience flag, `pnl_gbp > 0` |
| entry_year | INTEGER | NO | Entry year, used for yearly rollups |
| imported_at | TIMESTAMPTZ | NO | Import timestamp, default `NOW()` |

**Constraints:** `UNIQUE (ticker, entry_date, exit_date)` on `backtest_trades`; `UNIQUE (entry_year)` on `backtest_yearly_performance`; `UNIQUE (ticker, entry_date)` on `backtest_open_positions`.

**Purpose:** provides the historical baseline that the Strategy Benchmark page (`strategy_benchmark_endpoints.md`) compares against live trade history — answers "is the live system tracking the backtested strategy's expected performance."

**Populating function:** `backend/database.py::ensure_backtest_tables()` (idempotent DDL) + `upsert_backtest_data()` (writes), invoked from `POST /strategy/benchmark/import` (`backend/routers/strategy_benchmark.py::import_backtest()`). Reads via `get_backtest_trades()`, `get_backtest_open_positions()`, `get_backtest_summary()`.

---

## Idempotency Keys Table

Generic, additive, opt-in cache for state-mutating `POST` endpoints that supply a client-generated idempotency key, preventing duplicate side effects on retry (RISK-02 mitigation).

```sql
CREATE TABLE IF NOT EXISTS idempotency_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    endpoint VARCHAR(100) NOT NULL,
    idempotency_key VARCHAR(200) NOT NULL,
    response_body JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (portfolio_id, endpoint, idempotency_key)
);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | Portfolio the cached request belongs to |
| endpoint | VARCHAR(100) | NO | The endpoint path the idempotency key was issued for |
| idempotency_key | VARCHAR(200) | NO | Caller-supplied key (opaque string) |
| response_body | JSONB | NO | The cached response returned on replay |
| created_at | TIMESTAMPTZ | NO | Cache write timestamp, default `NOW()` |

**Constraints:** `UNIQUE (portfolio_id, endpoint, idempotency_key)` — a repeat request with the same key against the same endpoint/portfolio replays the cached `response_body` instead of re-executing.

**Purpose:** only touched when a caller supplies an `idempotency_key` — endpoints that never receive one never call this table's functions, so behaviour is unchanged when the key is absent.

**Populating function:** `backend/database.py::ensure_idempotency_keys_table()` (idempotent DDL) + `get_idempotency_record()` / the write path in `backend/utils/idempotency.py::replay_or_create()`, which callers invoke directly.

---

## Gemini Audit Log Table

AI compliance audit trail (ST-07) recording model/prompt provenance for every AI-generated trade plan thesis — retained under `claude_api_log_hygiene_policy.md`. **Naming note:** the table and function names predate the switch from Gemini to the Anthropic Claude API (see `docs/specs/api_contracts/gemini_thesis_generation.md`'s own disclosed naming note) — the table stores audit records for the current AI provider regardless of the legacy `gemini_` prefix.

```sql
CREATE TABLE IF NOT EXISTS gemini_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID,
    model_version TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    input_hash TEXT NOT NULL,
    output_hash TEXT NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    estimated_cost_usd NUMERIC(12, 8)
);

CREATE INDEX IF NOT EXISTS idx_gal_generated_at ON gemini_audit_log (generated_at DESC);
CREATE INDEX IF NOT EXISTS idx_gal_plan_id ON gemini_audit_log (plan_id);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| plan_id | UUID | YES | FK-like reference to the `trade_plans` row this generation was for (not a DB-enforced FK) |
| model_version | TEXT | NO | AI model + version string (ST-12, EPIC-03, v8.4 extends this pattern to thesis/summary text generally) |
| prompt_version | TEXT | NO | Prompt template version used |
| input_hash | TEXT | NO | Hash of the prompt input, for reproducibility/audit |
| output_hash | TEXT | NO | Hash of the generated output |
| generated_at | TIMESTAMPTZ | NO | Generation timestamp, default `NOW()` |
| prompt_tokens | INTEGER | YES | Input token count |
| completion_tokens | INTEGER | YES | Output token count |
| total_tokens | INTEGER | YES | `prompt_tokens + completion_tokens` |
| estimated_cost_usd | NUMERIC(12,8) | YES | Estimated cost of this generation call |

**Indexes:** `idx_gal_generated_at` (DESC, for recency queries), `idx_gal_plan_id` (for per-plan lookups).

**Purpose:** AI Compliance & Governance Officer audit trail — every AI-generated thesis/summary logs its model version, prompt version, and content hashes here, independent of where the generated text itself is stored.

**Populating function:** `backend/database.py::ensure_gemini_audit_log_table()` (idempotent DDL) + `create_gemini_audit_entry()`, called from the thesis-generation pipeline (`docs/specs/api_contracts/gemini_thesis_generation.md`).

---

## AI Journal Entries Table

**Externally-provisioned — not created, migrated, or schema-owned by this codebase.** No `CREATE TABLE ai_journal_entries` statement exists anywhere in `backend/`. Every read is preceded by an `information_schema.tables` existence check before querying (`backend/database.py::get_ai_journal_review_status()`), so behaviour degrades gracefully (`ai_journal_entry_count: null`) when the table is absent — consistent with `docs/ops/db_index_audit_arc4_2026-08-06.md` Finding 4, which scoped this table out of its index audit for the same reason.

**Known columns (inferred from the one query this codebase issues against it):**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| portfolio_id | UUID (assumed) | — | Filter column used in the only query this codebase runs: `SELECT COUNT(*) FROM ai_journal_entries WHERE portfolio_id = %s` |

No other columns are known to this codebase — the full schema is owned by whatever external system provisions this table. If/when this codebase begins writing to `ai_journal_entries` directly (e.g. as part of Arc 4 journal intelligence features, see `ST-24`/`docs/operations/arc4_ai_cost_model.md`), this section must be replaced with a full `CREATE TABLE` schema and populating-function reference at that time.

**Purpose (as consumed here):** `get_ai_journal_review_status()` reports `ai_journal_entry_count` as an optional enrichment field alongside trade/position counts — read-only, best-effort, never blocks on the table's absence.

**Populating function:** none — this codebase never writes to `ai_journal_entries`.

---

**Sign-off (ST-08, EPIC-02, v8.4, BLG-SPEC-109):**
- Data Model & Domain Schema Owner: Accepted — 2026-08-07 (agent-mediated; documentation backfill only, no schema change; all 4 sections cross-checked against `backend/database.py`'s actual `CREATE TABLE`/`ensure_*` statements; `ai_journal_entries` correctly scoped as externally-provisioned per the standing `db_index_audit_arc4_2026-08-06.md` finding)

---

### Migration from v2.21 to v2.22

ST-10 (BLG-BE-82, EPIC-03, v8.4) — index correction, not a column change. `ensure_trade_plans_table()`'s idempotent create-path never actually created the plain `idx_trade_plans_ticker ON trade_plans(ticker)` this document's DS-04 schema block previously (incorrectly) documented — and even if it had, a plain index is not used by `get_trade_plans()`'s actual `WHERE UPPER(ticker)=%s` predicate. Found by `docs/ops/db_index_audit_arc4_2026-08-06.md` Finding 1. Replaced with a functional index matching the real predicate, following the same pattern already used by the sibling table `red_flag_events` (`idx_rfe_ticker ON red_flag_events (UPPER(ticker))`).

```sql
BEGIN;
DROP INDEX IF EXISTS idx_trade_plans_ticker;
CREATE INDEX IF NOT EXISTS idx_trade_plans_ticker_upper ON trade_plans (UPPER(ticker));
COMMIT;
```

**Verification query (run after migration):**

```sql
EXPLAIN SELECT * FROM trade_plans WHERE portfolio_id = '<uuid>' AND UPPER(ticker) = 'NVDA';
-- Expected: Bitmap Index Scan (or Index Scan) on idx_trade_plans_ticker_upper appears in the plan
```

Reversible:
```sql
BEGIN;
DROP INDEX IF EXISTS idx_trade_plans_ticker_upper;
CREATE INDEX IF NOT EXISTS idx_trade_plans_ticker ON trade_plans(ticker);
COMMIT;
```

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-08-07 (agent-mediated; index-only change, no column added/removed, corrects a doc/live-code mismatch found by the Arc 4 index audit)
- Backend Engineering Patterns Owner: Accepted — 2026-08-07 (agent-mediated; matches the existing `red_flag_events` functional-index precedent)

---

### Migration from v2.22 to v2.23

ST-12 (BLG-BE-70, EPIC-03, v8.4) — AI compliance/audit provenance. `gemini_service.py`'s `generate_full_plan()`/`generate_setup_thesis()` already return `model_version`/`prompt_version` to the caller and log them to `gemini_audit_log` keyed by `plan_id`, but the *stored* `trade_plans` row itself carried no provenance field — retroactive audit required a fragile join via `plan_id` (often null at generate-plan time, before a plan exists). Adds two nullable columns, populated only when the frontend saves narrative fields (`setup_thesis`, `entry_rationale`, etc.) as-received from a generate-plan/generate-thesis response, without user edits.

```sql
BEGIN;
ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS thesis_model_version VARCHAR(50);
ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS thesis_prompt_version VARCHAR(20);
COMMIT;
```

### Down Migration (v2.23 → v2.22)

```sql
BEGIN;
ALTER TABLE trade_plans DROP COLUMN IF EXISTS thesis_model_version;
ALTER TABLE trade_plans DROP COLUMN IF EXISTS thesis_prompt_version;
COMMIT;
```

### Field Reference

| Field | Type | Nullable | Description |
|-------|------|----------|--------------|
| `thesis_model_version` | VARCHAR(50) | YES | AI model identifier (e.g. `"claude-haiku-4-5"`) that produced this plan's narrative fields, if saved as-received from a generate-plan/generate-thesis response. Null when written/edited manually. Forward-only — no backfill. |
| `thesis_prompt_version` | VARCHAR(20) | YES | Companion prompt-template version (e.g. `"v3.0"`), saved the same way. |

**Population points:** `backend/routers/trade_plans.py`'s `TradePlanCreate`/`TradePlanUpdate` request models (frontend-passed, persisted without validation — same pattern as `signal_id`/`risk_percent_used`, SI-02 DS-07). Backend does not itself infer AI-origin; the frontend is expected to populate these two fields from the generate-plan/generate-thesis response's own `model_version`/`prompt_version` fields when saving unedited AI output. **Known residual gap:** this cycle (v8.4) delivers the backend storage capability only — actual end-to-end population depends on a frontend change (out of this backend-only story's scope) to pass these values through on save; filed as a follow-up backlog item (see `qa_evidence_EPIC-03.md`).

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-08-07 (agent-mediated; two nullable columns, no existing schema touched, no backfill attempted — forward-only by design)
- AI Compliance & Governance Officer: Accepted — 2026-08-07 (agent-mediated; closes the BLG-BE-70 retroactive-audit gap for newly-created records once frontend wiring lands; backend capability alone does not yet populate the field end-to-end — tracked as a residual gap, not silently treated as complete)

---

### Migration from v2.23 to v2.24

ST-13 (BLG-BE-77, EPIC-03, v8.4) — audit trail for trade plan edits post-entry, extending the `position_audit_log` pattern (`BLG-BE-73`, §Migration v2.16→v2.17 above) to `trade_plans`. "Post-entry" means the plan is linked to a position (`position_id` set, either before or after the edit) at the time of the edit — pre-entry edits to a still-draft plan are ordinary iterative authoring, not logged. Same schema shape, same no-"who"-column rationale (single-user product), same fail-open non-blocking write convention as `position_audit_log`.

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS trade_plan_audit_log (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trade_plan_id UUID NOT NULL,
    source        TEXT NOT NULL,
    field         TEXT NOT NULL,
    before_value  TEXT,
    after_value   TEXT,
    changed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trade_plan_audit_log_trade_plan_id ON trade_plan_audit_log(trade_plan_id);

COMMIT;
```

### Field Reference

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | UUID | NO | Primary key |
| `trade_plan_id` | UUID | NO | The trade plan edited. No FK constraint (audit rows must survive the plan's own lifecycle; matches `position_audit_log.position_id`'s pattern of not cascading) |
| `source` | TEXT | NO | Always `post-entry-edit` in this version — a single source, unlike `position_audit_log`'s 3 (`note`/`tags`/`mark-reviewed`), because `update_trade_plan()` is one generic PUT endpoint covering all editable fields, not 3 separate single-purpose endpoints |
| `field` | TEXT | NO | The specific field changed (any of `update_trade_plan()`'s allowed fields — `setup_thesis`, `status`, `r_target`, etc.) |
| `before_value` | TEXT | YES | Value before the edit, stringified |
| `after_value` | TEXT | YES | Value after the edit, stringified |
| `changed_at` | TIMESTAMPTZ | NO | When the edit was recorded |

Reversible: `DROP TABLE IF EXISTS trade_plan_audit_log;`

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-08-07 (agent-mediated; single new append-only table, no existing schema touched, no backfill applicable — table did not previously exist; mirrors the already-accepted `position_audit_log` shape)

---

## DS-12 — trade_plans active-status-requires-position CHECK constraint (v2.25, 2026-08-11)

**Story:** ST-03 (EPIC-02, v8.6) — BLG-BE-91

DB-level safeguard against new orphaned `trade_plans` rows going forward. `position_id` remains nullable by design (a plan may legitimately exist pre-entry, or be abandoned, with no position ever attached) — a hard `NOT NULL` constraint is not viable. The precise integrity risk closed here: `status = 'active'` is meant to mean "this plan backs a live position" — `position_service.py::add_position()`'s auto-link step is the only code path that ever sets `status = 'active'` as part of the intended flow, and it always sets `position_id` in the same write — but both `POST /trade-plans` (`create_plan()`) and `PUT /trade-plans/{id}` (`update_plan()`) previously accepted an arbitrary `status` string with no such guard, so a client could set `status = 'active'` directly with no `position_id` at either creation or edit time, producing exactly the orphaned-active-plan state this story exists to prevent. Closed at two layers in the same commit: router-level 400 guards in both `create_plan()` and `update_plan()` (primary defense — see `trade_plan_endpoints.md`'s `POST /trade-plans` and `PUT /trade-plans/{id}` Errors sections), and this CHECK constraint (defense-in-depth, in case a future code path bypasses the router — e.g. a direct DB write, or a new endpoint that omits the check).

Added `NOT VALID` deliberately — enforces the rule on rows inserted/updated going forward only (matching this story's own "going forward" framing), without retroactively validating the 11 legacy pre-`BLG-BE-46` (v6.8) `trade_plans` rows already known to carry `position_id IS NULL` (§"Trade Plan to Position Linkage" → §"Nullability and backfill posture" below). Avoids a migration failure risk from historical data not directly inspected as part of this change — **open risk, flagged not resolved:** if any of those 11 rows happen to also carry `status = 'active'` (plausible, since the `POST`/`PUT` gap this story closes existed for their entire pre-fix history), any future `UPDATE` touching that specific row will fail against this constraint until corrected; no live-DB query confirming or ruling this out was run as part of this change (sandboxed execution, no database access). A future `VALIDATE CONSTRAINT` pass can retroactively confirm the full table if ever needed; not required for this story's AC.

### Up Migration (v2.24 → v2.25)

```sql
BEGIN;
ALTER TABLE trade_plans DROP CONSTRAINT IF EXISTS trade_plans_active_requires_position_check;
ALTER TABLE trade_plans ADD CONSTRAINT trade_plans_active_requires_position_check
  CHECK (status != 'active' OR position_id IS NOT NULL) NOT VALID;
COMMIT;
```

### Verification

```sql
SELECT conname, convalidated
FROM pg_constraint
WHERE conrelid = 'trade_plans'::regclass AND conname = 'trade_plans_active_requires_position_check';
-- Expected: 1 row, convalidated=false (NOT VALID — enforced going forward, not backfilled)
```

### Down Migration (v2.25 → v2.24)

```sql
BEGIN;
ALTER TABLE trade_plans DROP CONSTRAINT IF EXISTS trade_plans_active_requires_position_check;
COMMIT;
```

Reversible: drops the constraint only; no column/table changes to reverse.

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-08-12 (agent-mediated; single new CHECK constraint, `NOT VALID` so no risk to existing rows, no existing column/table structure touched)
- Product Owner (design + risk acceptance): Accepted — 2026-08-12. Explicitly accepts the `NOT VALID`/going-forward-only design and the disclosed staging-verification gap (`BLG-BE-96`, elevated P1) as a reasonable trade-off, not a silently-ignored risk — full reasoning in `qa_evidence_EPIC-02.md`'s Product Owner Decision block. **This is not the same thing as the PR's merge-gate Product Owner acceptance** (`CLAUDE.md` §2, always-human, satisfied only by an actual human clicking accept on the PR) — that remains outstanding. (This entry briefly and incorrectly stated a bare "Accepted" for the merge-gate sense on 2026-08-11; corrected 2026-08-12 after an independent agent-mediated review of PR #1362 flagged the discrepancy, before being re-recorded here in its narrower, correct sense.)

### Verification note (ST-07, EPIC-02, v8.7, BLG-BE-96 — best-available-proxy execution)

No new migration. `BLG-BE-96` (ST-07) required staging/production verification of the linkage default and this constraint's live state; staging/live-Postgres access remains unavailable in this sandbox (unchanged since v8.6 — no `DATABASE_URL`, no `psql`, no outbound reachability to a live Postgres host). Product Owner (agent-mediated, 2026-08-12, `sprint_planning_notes.md`) authorised proceeding via best-available proxy rather than deferring again. Findings:

- **AC-01 (linkage-by-default) — confirmed via code path + test suite, not live staging.** `position_service.py::add_position()`'s auto-link step is the sole code path that ever sets `trade_plans.status = 'active'`, and it always sets `position_id` in the same `UPDATE` (see this section's own description above). Regression coverage: `tests/test_position_trade_plan_link.py` (447 lines, `TestAddPositionExplicitTradePlanLink` and ticker/market best-effort match cases). Proxy confidence: High — this is the same code path DS-12 itself was written to backstop, already reviewed at v8.6 ST-03.
- **AC-03 (constraint present on live table) — confirmed via startup-invocation code path, not a live `pg_constraint` query.** `ensure_trade_plans_active_requires_position_constraint()` (this section's Up Migration) is invoked unconditionally on every backend boot (`backend/main.py` startup sequence), with a startup log line on success and an error log on failure — i.e. the constraint is (re)applied idempotently on every deploy, and a failure to apply it would be visible in boot logs. Proxy confidence: High for "the migration runs on every deploy"; **not equivalent** to running the `### Verification` query above against the live table, which was not executed.
- **AC-02 (legacy orphaned-row audit) — not proxyable; residual gap, disclosed not silently met.** No mechanism in this sandbox can substitute for the live query (`SELECT ... WHERE status='active' AND position_id IS NULL`) against the 11 known pre-`BLG-BE-46` legacy rows. This AC is **not** verified this cycle. The v8.6-established escalation condition carries forward unchanged and remains the operative safeguard: **if a future live check of those 11 rows finds any with `status='active'`, that finding escalates to its own P0 immediately**, independent of this story's own timeline.

**Residual gap:** AC-02 remains open pending genuine staging/production database access. `BLG-BE-96` is not closed by this proxy execution — see `qa_evidence_EPIC-02.md` for the disposition and backlog carry-forward.

**Sign-off:**
- Signed off by: Sprint Execution Engine (agent-mediated, Head of Engineering role — §5.3) — 2026-08-13. Code-path and startup-invocation evidence for AC-01/AC-03 reviewed and found sufficient as best-available proxy; AC-02 correctly left unproxied rather than asserted met.
- Signed off by: Sprint Execution Engine (agent-mediated, Data Model & Domain Schema Owner role — §5.3) — 2026-08-13. Confirms no schema/migration change accompanies this note; DS-12's `NOT VALID` posture and its documented open risk (above) are unchanged by this verification pass.

---

## DS-13 — position_state_history table (v2.27, 2026-08-14)

**Story:** ST-08 (EPIC-02, v8.8) — BLG-BE-58

Append-only normalized log of position lifecycle state transitions, extending the `position_audit_log` pattern (§Migration v2.16→v2.17 above) to lifecycle state changes specifically. Complements — does not replace — the existing `state_history` JSONB column on `positions` (DS-05, v2.6): that column is untouched, `compute_position_state()` and the rest of the lifecycle state machine are unchanged (no behavioural change), and this table is written alongside the JSONB column on every genuine transition (`refresh_position_lifecycle()`, `services/position_lifecycle_service.py`). Rationale for a separate table rather than only the JSONB column: independently queryable/indexable history (e.g. `SELECT * FROM position_state_history WHERE position_id = ...`) without deserializing the JSONB blob, and a durable audit trail that survives even if the parent `positions` row's `state_history` column were ever reset. Same no-"who"-column rationale as `position_audit_log` (single-user product), same fail-open non-blocking write convention (a write failure never blocks the underlying lifecycle state update).

**Write-ordering fix (ST-10, BLG-BE-100, EPIC-03, v8.9):** `refresh_position_lifecycle()` now calls the primary write (`update_position_lifecycle_state()`) *before* this table's audit write (`create_position_state_history_entry()`), not after — see the "Transaction isolation decision" note under §Migration v2.16→v2.17 above for the full rationale (a primary-write failure right after a successful audit insert previously left a phantom transition record here).

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS position_state_history (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    position_id  UUID NOT NULL,
    from_state   VARCHAR(20),
    to_state     VARCHAR(20) NOT NULL,
    entered_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_position_state_history_position_id ON position_state_history(position_id);

COMMIT;
```

### Field Reference

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | UUID | NO | Primary key |
| `position_id` | UUID | NO | The position that transitioned. No FK constraint (audit rows must survive the position's own lifecycle; matches `position_audit_log.position_id`'s pattern of not cascading) |
| `from_state` | VARCHAR(20) | YES | The prior `position_state` value. NULL for a position's first-ever computed state (no prior state to record) |
| `to_state` | VARCHAR(20) | NO | The new `position_state` value (`EXIT ZONE` / `PROFITABLE` / `LOSING` / `GRACE` / `UNKNOWN`) |
| `entered_at` | TIMESTAMPTZ | NO | When the transition was recorded — same value written to `positions.state_entered_at` for this transition |

Reversible: `DROP TABLE IF EXISTS position_state_history;`

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-08-14 (agent-mediated; single new append-only table, no existing schema touched, `state_history` JSONB column and state machine logic unchanged, no backfill applicable — table did not previously exist; mirrors the already-accepted `position_audit_log`/`trade_plan_audit_log` shape)

---

## DS-14 — signals functional index for UPPER(ticker) (v2.28, 2026-08-14)

**Story:** ST-12 (EPIC-02, v8.8) — BLG-BE-94 (Head-of-Engineering-review correction, agent-mediated §5.3)

`database.get_signals_for_ticker()` (this story's own query-latency fix, `docs/ops/pre_trade_research_query_latency_review_2026-08-14.md`) queries `WHERE portfolio_id = %s AND UPPER(ticker) = UPPER(%s)`. The existing `idx_signals_ticker` (plain btree on the bare `ticker` column) cannot serve a predicate that wraps the column in `UPPER()` — a plain index is not usable by a functional predicate. Same class of gap already identified and fixed for `trade_plans`/`red_flag_events` (ST-10, BLG-BE-82, EPIC-03, v8.4 — `idx_trade_plans_ticker_upper` above). Missed on this story's first pass; caught by agent-mediated Head of Engineering review before merge, not after.

```sql
BEGIN;
CREATE INDEX IF NOT EXISTS idx_signals_ticker_upper ON signals (UPPER(ticker));
COMMIT;
```

### Verification

```sql
EXPLAIN SELECT * FROM signals WHERE portfolio_id = '...' AND UPPER(ticker) = UPPER('AAPL') ORDER BY signal_date DESC, rank ASC;
-- Expected: index scan referencing idx_signals_ticker_upper (or a bitmap plan combining it with idx_signals_portfolio), not a sequential/filter scan on UPPER(ticker)
```

### Down Migration (v2.28 → v2.27)

```sql
BEGIN;
DROP INDEX IF EXISTS idx_signals_ticker_upper;
COMMIT;
```

Reversible: drops the index only; no column/table changes to reverse. `get_signals_for_ticker()`'s query remains correct without it, just slower (row-filtered scan instead of index scan).

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-08-14 (agent-mediated; single new index, no existing schema touched, matches the accepted `idx_trade_plans_ticker_upper`/`idx_rfe_ticker` precedent exactly)

---

## DS-15 — trade_plans.triggered_by_price_alert_id (v2.29, 2026-08-14)

**Story:** ST-09 (EPIC-02, v8.8) — BLG-BE-84

Real alert-to-trade provenance, tracked since `BLG-FEAT-78`/ST-31 (v8.4) found no such linkage existed and shipped a different distinction instead (`trade_origin: "Signal"/"Manual"`, derived from `signal_id` — see `reports_endpoints.md`'s Known Deviations, `ESC-EXEC-20260807-01`, which explicitly notes `trade_origin` is "**Not** a price-alert indicator"). This story closes the original gap: `POST /trade-plans` now accepts an optional `triggered_by_price_alert_id`, set by the frontend when a plan is created via the alert-notification-to-trade-plan UI path (`NotificationRow.js` → `TradePlan.js`, see `docs/specs/api_contracts/trade_plan_endpoints.md` and `alerts_endpoints.md`'s `GET /notifications` `context.price_alert_id`). Null for plans created any other way (default UI flow, generate-plan, etc.) — no other code path sets it.

**Reporting treatment (decided per this story's own AC, before implementation):** a separate field, not a third `trade_origin` value. Reasoning:
1. `trade_origin` was deliberately scoped to `signal_id` only at v8.4, with an explicit note that it is *not* a price-alert indicator — overloading it now would silently change what an already-shipped, tax-relevant export field (`GET /reports/tax-year`) means, for existing consumers who read `trade_origin` today expecting exactly "Signal" or "Manual".
2. The two provenance signals are not mutually exclusive in principle (a plan could theoretically carry both a `signal_id` and a `triggered_by_price_alert_id` if the product ever allowed converting a fired alert into a signal-sourced plan) — a single enum can't represent that; two independent nullable columns can.
3. `signal_id` (system-generated momentum signal) and a price alert (a user-configured threshold the user chose to act on) are genuinely different provenance dimensions — one records what generated the *idea*, the other what triggered the *user's action* — not different values of the same taxonomy.

Extending `GET /reports/tax-year`'s CSV export to surface `triggered_by_price_alert_id` (or a derived label) is out of this story's scope — not requested by its AC, and would be its own follow-on story if wanted (`reports_endpoints.md`'s `trade_origin` field note would need its own update at that point).

```sql
BEGIN;
ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS triggered_by_price_alert_id UUID;
COMMIT;
```

### Field Reference

| Field | Type | Nullable | Description |
|-------|------|----------|--------------|
| `triggered_by_price_alert_id` | UUID | YES | The `price_alerts` row that triggered creation of this plan, via the alert-notification-to-trade-plan UI path. NULL for plans created any other way. No FK constraint — matches `signal_id`'s existing pattern of not cascading, so a plan's provenance record survives independently of the `price_alerts` row's own lifecycle (a `price_alerts` row is never deleted, only deactivated on trigger, but the same non-cascading convention is kept for consistency). |

Reversible: `ALTER TABLE trade_plans DROP COLUMN IF EXISTS triggered_by_price_alert_id;`

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-08-14 (agent-mediated; single new nullable column, no existing schema touched, matches the accepted `signal_id` shape and non-cascading convention exactly, no backfill applicable — column did not previously exist)

---

**Document Version:** 2.29
**Maintained By:** Data Model & Domain Schema Owner
**Last Review:** 2026-08-14
