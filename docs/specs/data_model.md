# Data Model - Momentum Trading Assistant

**Version:** 1.6
**Last Updated:** February 17, 2026

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
| fx_rate | DECIMAL(10,6) | YES | GBP/USD rate at time of entry (stored; for US stocks) |
| shares | DECIMAL(10,4) | NO | Number of shares (fractional allowed) |
| total_cost | DECIMAL(12,2) | NO | Total cost including fees in GBP |
| fees_paid | DECIMAL(10,2) | NO | Total fees (commission + stamp duty or FX fee). Zero-fee trades store `0`, never `null` |
| fee_type | VARCHAR(20) | YES | "stamp_duty" or "fx_fee" |
| initial_stop | DECIMAL(10,4) | YES | Initial stop loss level calculated at entry (`entry_price − (atr_multiplier_initial × ATR)`) in native currency |
| current_stop | DECIMAL(10,4) | YES | Current trailing stop level in native currency. **API name:** `stop_price` / `stop_price_native` |
| current_price | DECIMAL(10,4) | YES | Latest stored market price (GBP). **API also returns** `current_price_native` (computed at query time) |
| atr | DECIMAL(10,4) | YES | Average True Range value. **API name:** `atr_value` |
| holding_days | INTEGER | NO | Days held (updated daily by position analysis) |
| pnl | DECIMAL(12,2) | NO | Profit/Loss in GBP |
| pnl_pct | DECIMAL(10,2) | NO | Profit/Loss percentage. **API name:** `pnl_percent` (canonical in position responses); `pnl_pct` is the compatibility alias used in trade history |
| status | VARCHAR(20) | NO | "open" or "closed" |
| exit_date | DATE | YES | Position exit date. `null` while open |
| exit_price | DECIMAL(10,4) | YES | Exit price (user-provided). `null` while open |
| exit_reason | VARCHAR(50) | YES | Reason for exit (see exit reason values below). `null` while open |
| entry_note | TEXT | YES | Trade journal entry note (max 500 chars) |
| exit_note | TEXT | YES | Trade journal exit note (max 500 chars). Always `null` while status = 'open' |
| tags | TEXT[] | YES | Array of tags for categorization (max 10 tags; each max 20 chars; lowercase, numbers, hyphens only) |
| created_at | TIMESTAMP | NO | Record creation |
| updated_at | TIMESTAMP | NO | Last update |

### API field name mapping

The following fields are stored under one name but exposed via the API under a different name. Both refer to the same data:

| Stored column | API field name | Notes |
|---------------|----------------|-------|
| `atr` | `atr_value` | Renamed in API response for clarity |
| `current_stop` | `stop_price` / `stop_price_native` | API returns both GBP and native currency versions |
| `pnl_pct` | `pnl_percent` | `pnl_percent` is canonical in position responses; `pnl_pct` used in trade history for compatibility |

### API-computed fields (not stored columns)

These fields appear in `GET /positions` responses but are not stored in the database. They are computed at query time:

| API field | How computed |
|-----------|-------------|
| `current_price_native` | `current_price` converted to native currency using live FX rate |
| `stop_price_native` | `current_stop` converted to native currency using live FX rate |
| `live_fx_rate` | Fetched live from Yahoo Finance at query time |
| `display_status` | Derived from `holding_days`, `pnl`, and grace period threshold: `"GRACE"` (day 0–9), `"PROFITABLE"` (day 10+, pnl > 0), `"LOSING"` (day 10+, pnl ≤ 0) |
| `grace_period` | `holding_days < min_hold_days` (boolean) |
| `initial_stop` (GBP) | `initial_stop` stored in native currency, converted to GBP for the API response |

### Notes
- UK tickers are automatically appended with ".L" (e.g., "FRES.L").
- `total_cost` is always in GBP for portfolio tracking.
- `shares` supports fractional values (e.g., 5.5).
- `atr` is stored at entry and updated on each position analysis call.
- The `min_hold_days` setting defaults to `10`, meaning grace covers days 0–9 inclusive. Day 10 is the first day stop logic is active. In general, grace covers days `0` through `min_hold_days − 1`.

---

## 3. Cash Transactions Table

Tracks deposits and withdrawals for accurate P&L calculation.

```sql
CREATE TABLE cash_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    type VARCHAR(20) NOT NULL CHECK (type IN ('deposit', 'withdrawal')),
    amount DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
    date DATE NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cash_transactions_portfolio
ON cash_transactions(portfolio_id, date DESC);

CREATE INDEX idx_cash_transactions_date
ON cash_transactions(date DESC);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| type | VARCHAR(20) | NO | "deposit" or "withdrawal" |
| amount | DECIMAL(12,2) | NO | Amount (always positive) |
| date | DATE | NO | Transaction date |
| note | TEXT | YES | Optional description |
| created_at | TIMESTAMP | NO | Record creation |
| updated_at | TIMESTAMP | NO | Last update |

### Notes
- **Critical:** The initial deposit must be recorded for correct P&L calculations.
- `amount` is always positive; `type` determines whether it is added or subtracted.
- `net_cash_flow = total deposits − total withdrawals`
- Portfolio P&L = `total_value − net_cash_flow`

---

## 4. Portfolio History Table

Daily snapshots of portfolio performance for historical tracking and Sharpe ratio calculation.

```sql
CREATE TABLE portfolio_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    snapshot_date DATE NOT NULL,
    total_value DECIMAL(12, 2) NOT NULL,
    cash_balance DECIMAL(12, 2) NOT NULL,
    positions_value DECIMAL(12, 2) NOT NULL,
    total_pnl DECIMAL(12, 2) NOT NULL,
    position_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(portfolio_id, snapshot_date)
);

CREATE INDEX idx_portfolio_history_date
ON portfolio_history(portfolio_id, snapshot_date DESC);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| snapshot_date | DATE | NO | Date of snapshot |
| total_value | DECIMAL(12,2) | NO | Total portfolio value in GBP |
| cash_balance | DECIMAL(12,2) | NO | Cash balance in GBP |
| positions_value | DECIMAL(12,2) | NO | Total positions value in GBP |
| total_pnl | DECIMAL(12,2) | NO | Total P&L in GBP |
| position_count | INTEGER | NO | Number of open positions at snapshot time |
| created_at | TIMESTAMP | NO | Snapshot creation time |

### Notes
- `UNIQUE(portfolio_id, snapshot_date)` prevents duplicate snapshots per day. The upsert pattern makes snapshot creation idempotent.
- Should be automated via cron (4 PM weekdays recommended).
- Used for performance charts and historical analysis.
- The analytics service uses 30+ snapshots to compute the portfolio-method Sharpe ratio. Fewer than 30 snapshots falls back to the trade-method Sharpe calculation.

---

## 5. Trade History Table

Immutable historical record of closed positions. Records are written once on exit and never updated.

```sql
CREATE TABLE trade_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    ticker VARCHAR(20) NOT NULL,
    market VARCHAR(5) NOT NULL,
    entry_date DATE NOT NULL,
    exit_date DATE NOT NULL,
    shares DECIMAL(10, 4) NOT NULL,
    entry_price DECIMAL(10, 4) NOT NULL,
    exit_price DECIMAL(10, 4) NOT NULL,
    total_cost DECIMAL(12, 2) NOT NULL,
    gross_proceeds DECIMAL(12, 2) NOT NULL,
    net_proceeds DECIMAL(12, 2) NOT NULL,
    entry_fees DECIMAL(10, 2),
    exit_fees DECIMAL(10, 2),
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

CREATE INDEX idx_trade_history_portfolio
ON trade_history(portfolio_id, exit_date DESC);
CREATE INDEX idx_trade_history_tags ON trade_history USING GIN(tags);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| ticker | VARCHAR(20) | NO | Stock symbol |
| market | VARCHAR(5) | NO | "US" or "UK" |
| entry_date | DATE | NO | Entry date |
| exit_date | DATE | NO | Exit date |
| shares | DECIMAL(10,4) | NO | Number of shares |
| entry_price | DECIMAL(10,4) | NO | Entry price in native currency |
| exit_price | DECIMAL(10,4) | NO | Exit price in native currency (user-provided) |
| total_cost | DECIMAL(12,2) | NO | Total cost in GBP |
| gross_proceeds | DECIMAL(12,2) | NO | Proceeds before fees in GBP |
| net_proceeds | DECIMAL(12,2) | NO | Proceeds after fees in GBP |
| entry_fees | DECIMAL(10,2) | YES | Fees paid on entry |
| exit_fees | DECIMAL(10,2) | YES | Fees paid on exit |
| pnl | DECIMAL(12,2) | NO | Realized P&L in GBP |
| pnl_pct | DECIMAL(10,2) | NO | P&L percentage. The API also returns this as `pnl_percent` for compatibility |
| holding_days | INTEGER | NO | Calendar days from `entry_date` to `exit_date` inclusive |
| exit_reason | VARCHAR(50) | YES | Reason for exit (see exit reason values below). `null` values are normalised to `"Manual Exit"` by the analytics service at read time |
| entry_fx_rate | DECIMAL(10,6) | YES | GBP/USD rate at entry (US stocks only) |
| exit_fx_rate | DECIMAL(10,6) | YES | GBP/USD rate at exit (US stocks only) |
| entry_note | TEXT | YES | Journal note copied from position at exit time |
| exit_note | TEXT | YES | Journal note entered at exit |
| tags | TEXT[] | YES | Tags copied from position at exit time |
| created_at | TIMESTAMP | NO | Record creation time |

### Exit Reason Values

Valid exit reason strings used across the system:

| Value | Description |
|-------|-------------|
| `"Manual Exit"` | User-initiated exit outside of automated logic |
| `"Stop Loss Hit"` | Initial or trailing stop level breached |
| `"Trailing Stop"` | Trailing stop triggered after profitable period |
| `"Risk-Off Signal"` | Market regime turned risk-off (SPY or FTSE below 200-day MA) |
| `"Target Reached"` | User defined profit target met |
| `"Partial Profit Taking"` | Partial exit to lock in gains |

> **Note:** `null` values in `exit_reason` are normalised to `"Manual Exit"` by the analytics service at read time. They are stored as `null` in this table.

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
| default_currency | VARCHAR(3) | GBP | Portfolio base currency. GBP only — multi-currency is position-level, not portfolio-level |
| theme | VARCHAR(20) | dark | UI theme preference ("dark" or "light") |
| uk_commission | DECIMAL(10,2) | 9.95 | Fixed commission per UK trade in GBP |
| us_commission | DECIMAL(10,2) | 0.00 | Fixed commission per US trade (zero-commission brokers) |
| stamp_duty_rate | DECIMAL(6,5) | 0.005 | UK stamp duty rate on purchases (0.5%) |
| fx_fee_rate | DECIMAL(6,5) | 0.0015 | FX conversion fee rate for USD trades (0.15%) |
| min_trades_for_analytics | INTEGER | 10 | Minimum number of closed trades required before analytics metrics are computed |
| created_at | TIMESTAMP | NOW | Record creation |
| updated_at | TIMESTAMP | NOW | Last update |

### Strategy parameter context
The default values for `min_hold_days`, `atr_multiplier_initial`, and `atr_multiplier_trailing` are backtest-optimised and produced 26.37% CAGR, 1.29 Sharpe Ratio, and −25.38% maximum drawdown. Changes affect all future stop calculations; existing open positions are not retroactively affected.

---

## 7. Signals Table

Stores generated momentum signals produced by `POST /signals/generate`. Each signal represents a ranked entry candidate for a given ticker on a given date. For endpoint behaviour see `signal_endpoints.md`.

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

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| ticker | VARCHAR(20) | NO | Stock symbol |
| market | VARCHAR(5) | NO | "US" or "UK" |
| signal_date | DATE | NO | Date the signal was generated |
| rank | INTEGER | NO | Momentum rank within the generation batch (1 = strongest) |
| momentum_percent | NUMERIC(10,2) | NO | Momentum percentage over the lookback period |
| current_price | NUMERIC(10,4) | NO | Price in native currency at signal generation time (point-in-time) |
| price_gbp | NUMERIC(10,4) | NO | Price converted to GBP at signal generation time (point-in-time) |
| atr_value | NUMERIC(10,4) | NO | ATR at signal generation time |
| volatility | NUMERIC(10,6) | NO | Volatility measure used for inverse-volatility position sizing |
| initial_stop | NUMERIC(10,4) | NO | Suggested initial stop in native currency: `current_price − (atr_multiplier_initial × ATR)` |
| suggested_shares | INTEGER | NO | Whole-share position size based on available cash and volatility weighting. Integer only — fractional shares are not supported in signal generation |
| allocation_gbp | NUMERIC(12,2) | NO | Capital allocated to this signal in GBP |
| total_cost | NUMERIC(12,2) | NO | Estimated total cost including fees in GBP |
| status | VARCHAR(20) | YES | Signal lifecycle status. Defaults to `'new'`. See status values below |
| position_id | UUID | YES | FK to positions — set only when `status = 'entered'`; links signal to the resulting position |
| created_at | TIMESTAMP | YES | Record creation time |
| updated_at | TIMESTAMP | YES | Last update time |

### Signal Status Values

| Value | Description |
|-------|-------------|
| `new` | Generated and not yet acted upon |
| `entered` | User entered a position based on this signal; `position_id` is populated |
| `dismissed` | User dismissed this signal without acting |
| `expired` | Signal is more than 7 days old without action |
| `already_held` | A matching open position existed when the signal was generated |

### Constraints & Design Notes
- `UNIQUE(portfolio_id, ticker, signal_date)` prevents duplicate signals for the same ticker on the same day. Re-running `POST /signals/generate` on the same day does not create duplicate records for already-generated tickers.
- `position_id` is nullable and only set when `status = 'entered'`. It provides traceability from signal to the position that resulted from it.
- `suggested_shares` is `INTEGER`. Signal generation does not support fractional share sizing. Actual position entry via `POST /portfolio/position` supports fractional shares.
- `current_price`, `price_gbp`, `atr_value`, `initial_stop`, and `volatility` are all point-in-time values captured at generation. They will diverge from live values as time passes and must not be used as live market data.

---

## Data Relationships

```
portfolios (1) ──┬── (N) positions
                 ├── (N) cash_transactions
                 ├── (N) portfolio_history
                 ├── (N) trade_history
                 └── (N) signals ──── (0..1) positions (via position_id)

settings (1 global)
```

---

## Example Data Flow

### 1. Creating a Position

```sql
-- User deposits £5000
INSERT INTO cash_transactions (portfolio_id, type, amount, date, note)
VALUES ('portfolio-id', 'deposit', 5000, '2026-01-23', 'Initial deposit');

-- User buys 5.5 shares of WDC at $243
INSERT INTO positions (
    portfolio_id, ticker, market, entry_date, entry_price,
    fill_price, fill_currency, fx_rate, shares, total_cost, fees_paid
) VALUES (
    'portfolio-id', 'WDC', 'US', '2026-01-23', 243.00,
    243.00, 'USD', 1.3528, 5.5, 986.70, 1.48
);

-- Update portfolio cash
UPDATE portfolios
SET cash = cash - 986.70
WHERE id = 'portfolio-id';
```

### 2. Daily Position Analysis

```sql
-- Update position with live price (note: column is 'atr', API returns 'atr_value')
UPDATE positions
SET
    current_price = 250.38,
    holding_days = 8,
    pnl = 29.06,
    pnl_pct = 2.98,
    atr = 3.15,
    current_stop = 236.85,
    updated_at = NOW()
WHERE id = 'position-id';
```

### 3. Creating Daily Snapshot

```sql
INSERT INTO portfolio_history (
    portfolio_id, snapshot_date, total_value, cash_balance,
    positions_value, total_pnl, position_count
) VALUES (
    'portfolio-id', '2026-01-31', 5133.52, 532.62,
    4600.90, 133.52, 5
)
ON CONFLICT (portfolio_id, snapshot_date)
DO UPDATE SET
    total_value = EXCLUDED.total_value,
    cash_balance = EXCLUDED.cash_balance,
    positions_value = EXCLUDED.positions_value,
    total_pnl = EXCLUDED.total_pnl,
    position_count = EXCLUDED.position_count;
```

### 4. Signal Lifecycle

```sql
-- Signal generated for NVDA
INSERT INTO signals (
    portfolio_id, ticker, market, signal_date, rank,
    momentum_percent, current_price, price_gbp, atr_value,
    volatility, initial_stop, suggested_shares,
    allocation_gbp, total_cost, status
) VALUES (
    'portfolio-id', 'NVDA', 'US', '2026-02-17', 1,
    45.2, 850.00, 623.00, 18.50,
    0.021800, 757.50, 1,
    986.00, 996.00, 'new'
);

-- User enters position based on signal
UPDATE signals
SET
    status = 'entered',
    position_id = 'new-position-id',
    updated_at = NOW()
WHERE id = 'signal-id';
```

---

## Query Examples

### Get Portfolio Summary
```sql
SELECT
    p.cash,
    COUNT(pos.id) FILTER (WHERE pos.status = 'open') AS open_positions,
    SUM(pos.total_cost) FILTER (WHERE pos.status = 'open') AS invested,
    SUM(pos.pnl) FILTER (WHERE pos.status = 'open') AS unrealized_pnl
FROM portfolios p
LEFT JOIN positions pos ON p.id = pos.portfolio_id
WHERE p.id = 'portfolio-id'
GROUP BY p.id, p.cash;
```

### Get Win Rate
```sql
SELECT
    COUNT(*) FILTER (WHERE pnl > 0) * 100.0 / COUNT(*) AS win_rate,
    AVG(pnl) FILTER (WHERE pnl > 0) AS avg_winner,
    AVG(pnl) FILTER (WHERE pnl < 0) AS avg_loser
FROM trade_history
WHERE portfolio_id = 'portfolio-id';
```

### Get Net Cash Flow
```sql
SELECT
    SUM(amount) FILTER (WHERE type = 'deposit') AS total_deposits,
    SUM(amount) FILTER (WHERE type = 'withdrawal') AS total_withdrawals,
    SUM(CASE WHEN type = 'deposit' THEN amount ELSE -amount END) AS net_cash_flow
FROM cash_transactions
WHERE portfolio_id = 'portfolio-id';
```

### Search Positions by Tag
```sql
SELECT * FROM positions
WHERE portfolio_id = 'portfolio-id'
AND tags && ARRAY['momentum', 'breakout']  -- Contains any of these tags
ORDER BY entry_date DESC;
```

### Get All Unique Tags
```sql
SELECT DISTINCT unnest(tags) AS tag
FROM positions
WHERE portfolio_id = 'portfolio-id'
ORDER BY tag;
```

### Get Trades with Notes
```sql
SELECT
    ticker, entry_date, exit_date, pnl,
    entry_note, exit_note, tags
FROM trade_history
WHERE portfolio_id = 'portfolio-id'
AND (entry_note IS NOT NULL OR exit_note IS NOT NULL)
ORDER BY exit_date DESC;
```

### Get Active Signals with Position Linkage
```sql
SELECT
    s.ticker,
    s.market,
    s.rank,
    s.momentum_percent,
    s.current_price,
    s.status,
    p.pnl AS position_pnl
FROM signals s
LEFT JOIN positions p ON s.position_id = p.id
WHERE s.portfolio_id = 'portfolio-id'
AND s.status IN ('new', 'already_held')
ORDER BY s.rank ASC;
```

---

## Migration from v1.0 to v1.1

### Required Changes

1. Add `cash_transactions` table
2. Add `portfolio_history` table
3. Alter `positions.shares` to `DECIMAL(10,4)`
4. Record initial deposit

```sql
BEGIN;

CREATE TABLE cash_transactions ( -- schema above );
CREATE TABLE portfolio_history ( -- schema above );

ALTER TABLE positions ALTER COLUMN shares TYPE DECIMAL(10, 4);

-- Record initial deposit (CRITICAL!)
INSERT INTO cash_transactions (portfolio_id, type, amount, date, note)
SELECT id, 'deposit', initial_cash, created_at::date, 'Initial deposit (migration)'
FROM portfolios;

COMMIT;
```

---

## Migration from v1.3 to v1.4

### Required Changes — Trade Journal

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

All fields are nullable. No data migration required. GIN indexes enable fast tag-based queries.

---

## Migration from v1.4 to v1.5

### Required Changes — Analytics Threshold

```sql
BEGIN;

ALTER TABLE settings ADD COLUMN min_trades_for_analytics INTEGER DEFAULT 10;

COMMIT;
```

Existing settings rows will receive the default value of `10`, which matches the pre-existing hardcoded threshold in the analytics service.

---

## Migration from v1.5 to v1.6

### Required Changes — Signals Table + positions.fees_paid constraint

```sql
BEGIN;

-- Formalise NOT NULL on positions.fees_paid.
-- Safe: DEFAULT 0 was always enforced at the application layer; no rows have null values.
ALTER TABLE positions ALTER COLUMN fees_paid SET NOT NULL;

-- Add signals table (full DDL in Section 7 above).
-- Note: this table already exists in the live database.
-- This migration formalises it in the documentation for the first time.
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

COMMIT;
```

---

## Planned Future Schema Changes

### v1.7 — Alerts (Planned)
```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    portfolio_id UUID REFERENCES portfolios(id),
    type VARCHAR(50),
    message TEXT,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP,
    updated_at TIMESTAMP  -- consistent with all other tables; add at formal design time
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

**Document Version:** 1.6
**Maintained By:** Development Team
**Last Review:** February 17, 2026
