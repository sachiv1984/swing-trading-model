# Data Model - Momentum Trading Assistant

**Owner:** Data Model & Domain Schema Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 2.8
**Last Updated:** 2026-05-18
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
CREATE INDEX idx_trade_plans_ticker ON trade_plans(ticker);
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

**Document Version:** 2.9
**Maintained By:** Data Model & Domain Schema Owner
**Last Review:** 2026-06-19
