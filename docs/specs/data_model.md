# Data Model - Momentum Trading Assistant

**Version:** 1.7
**Status:** Canonical
**Owner:** Data Model & Domain Schema Owner
**Last Updated:** 2026-02-19

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
CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cash DECIMAL(12, 2) NOT NULL DEFAULT 0,
    initial_cash DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| cash | DECIMAL(12,2) | Current cash balance (GBP) |
| initial_cash | DECIMAL(12,2) | Starting cash (**deprecated** — use `cash_transactions` table) |
| created_at | TIMESTAMP | Portfolio creation date |
| last_updated | TIMESTAMP | Last update timestamp |

### Notes
- `cash` is always in GBP.
- Updated on every position entry/exit.
- `initial_cash` is deprecated in favour of the `cash_transactions` table. Do not use for P&L calculations.

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
| created_at | TIMESTAMP | NO | Record creation timestamp |
| updated_at | TIMESTAMP | NO | Last update timestamp |

---

## 3. Trade History Table

Immutable record of closed trades. Written at exit time; never updated.

```sql
CREATE TABLE trade_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    position_id UUID REFERENCES positions(id),
    ticker VARCHAR(20) NOT NULL,
    market VARCHAR(5) NOT NULL,
    entry_date DATE NOT NULL,
    exit_date DATE NOT NULL,
    shares DECIMAL(10, 4) NOT NULL,
    entry_price DECIMAL(10, 4) NOT NULL,
    exit_price DECIMAL(10, 4) NOT NULL,
    total_cost DECIMAL(12, 2) NOT NULL,
    exit_proceeds DECIMAL(12, 2) NOT NULL,
    pnl DECIMAL(12, 2) NOT NULL,
    pnl_pct DECIMAL(10, 2) NOT NULL,
    holding_days INTEGER NOT NULL,
    exit_reason VARCHAR(50),
    entry_fx_rate DECIMAL(10, 6),
    exit_fx_rate DECIMAL(10, 6),
    entry_note TEXT,
    exit_note TEXT,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trade_history_portfolio ON trade_history(portfolio_id);
CREATE INDEX idx_trade_history_ticker ON trade_history(ticker);
CREATE INDEX idx_trade_history_exit_date ON trade_history(exit_date DESC);
CREATE INDEX idx_trade_history_tags ON trade_history USING GIN(tags);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| position_id | UUID | YES | FK to originating position |
| ticker | VARCHAR(20) | NO | Stock symbol |
| market | VARCHAR(5) | NO | "US" or "UK" |
| entry_date | DATE | NO | Original position entry date |
| exit_date | DATE | NO | Exit date |
| shares | DECIMAL(10,4) | NO | Shares exited |
| entry_price | DECIMAL(10,4) | NO | Entry price in native currency |
| exit_price | DECIMAL(10,4) | NO | Exit price in native currency |
| total_cost | DECIMAL(12,2) | NO | Entry cost in GBP (including fees) |
| exit_proceeds | DECIMAL(12,2) | NO | Exit value in GBP (after fees) |
| pnl | DECIMAL(12,2) | NO | Realised P&L in GBP |
| pnl_pct | DECIMAL(10,2) | NO | P&L as percentage of entry cost. API also returns as `pnl_percent` for compatibility |
| holding_days | INTEGER | NO | Calendar days from entry_date to exit_date inclusive |
| exit_reason | VARCHAR(50) | YES | Reason for exit. `null` normalised to `"Manual Exit"` by analytics service at read time |
| entry_fx_rate | DECIMAL(10,6) | YES | GBP/USD rate at entry (US stocks only) |
| exit_fx_rate | DECIMAL(10,6) | YES | GBP/USD rate at exit (US stocks only) |
| entry_note | TEXT | YES | Journal note copied from position at exit time |
| exit_note | TEXT | YES | Journal note entered at exit |
| tags | TEXT[] | YES | Tags copied from position at exit time |
| created_at | TIMESTAMP | NO | Record creation time |

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
        CHECK (status IN ('new', 'entered', 'dismissed', 'expired', 'already_held'))
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

---

## Planned Future Schema Changes

### v1.8 — Alerts (Planned)

```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID REFERENCES portfolios(id),
    type VARCHAR(50),
    message TEXT,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

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

**Document Version:** 1.7
**Maintained By:** Data Model & Domain Schema Owner
**Last Review:** 2026-02-19
