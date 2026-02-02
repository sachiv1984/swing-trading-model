# Data Model - Momentum Trading Assistant

**Version:** 1.1  
**Last Updated:** February 1, 2026

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
| initial_cash | DECIMAL(12,2) | Starting cash (deprecated - use cash_transactions) |
| created_at | TIMESTAMP | Portfolio creation date |
| last_updated | TIMESTAMP | Last update timestamp |

### Notes
- `cash` is always in GBP
- Updated on every position entry/exit
- `initial_cash` deprecated in favor of cash_transactions table

---

## 2. Positions Table

Tracks all positions (open and closed).

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
    fees_paid DECIMAL(10, 2) DEFAULT 0,
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_positions_portfolio ON positions(portfolio_id);
CREATE INDEX idx_positions_status ON positions(status);
CREATE INDEX idx_positions_ticker ON positions(ticker);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| portfolio_id | UUID | NO | FK to portfolios |
| ticker | VARCHAR(20) | NO | Stock symbol (e.g., "PLTR", "FRES.L") |
| market | VARCHAR(5) | NO | "US" or "UK" |
| entry_date | DATE | NO | Position entry date |
| entry_price | DECIMAL(10,4) | NO | Entry price (GBP for UK, USD for US) |
| fill_price | DECIMAL(10,4) | YES | Actual fill price in native currency |
| fill_currency | VARCHAR(3) | YES | "GBP" or "USD" |
| fx_rate | DECIMAL(10,6) | YES | GBP/USD rate at entry (for US stocks) |
| shares | DECIMAL(10,4) | NO | Number of shares (fractional allowed) |
| total_cost | DECIMAL(12,2) | NO | Total cost including fees (GBP) |
| fees_paid | DECIMAL(10,2) | NO | Total fees (commission + stamp duty/FX) |
| fee_type | VARCHAR(20) | YES | "stamp_duty" or "fx_fee" |
| initial_stop | DECIMAL(10,4) | YES | Initial stop loss level |
| current_stop | DECIMAL(10,4) | YES | Current trailing stop level |
| current_price | DECIMAL(10,4) | YES | Latest market price |
| atr | DECIMAL(10,4) | YES | Average True Range value |
| holding_days | INTEGER | NO | Days held (updated daily) |
| pnl | DECIMAL(12,2) | NO | Profit/Loss in GBP |
| pnl_pct | DECIMAL(10,2) | NO | Profit/Loss percentage |
| status | VARCHAR(20) | NO | "open" or "closed" |
| exit_date | DATE | YES | Position exit date |
| exit_price | DECIMAL(10,4) | YES | Exit price |
| exit_reason | VARCHAR(50) | YES | Reason for exit |
| created_at | TIMESTAMP | NO | Record creation |
| updated_at | TIMESTAMP | NO | Last update |

### Notes
- UK tickers automatically appended with ".L" (e.g., "FRES.L")
- `entry_price` is in native currency for display
- `total_cost` always in GBP for portfolio tracking
- `shares` supports fractional values (e.g., 5.5)
- `atr` stored for trailing stop calculations

---

## 3. Cash Transactions Table (New in v1.1)

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
- **Critical:** Initial deposit must be recorded for correct P&L
- Amount always positive; type determines add/subtract
- Used to calculate: `net_cash_flow = deposits - withdrawals`
- Portfolio P&L = `total_value - net_cash_flow`

---

## 4. Portfolio History Table (New in v1.1)

Daily snapshots of portfolio performance for historical tracking.

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
| total_value | DECIMAL(12,2) | NO | Total portfolio value (GBP) |
| cash_balance | DECIMAL(12,2) | NO | Cash balance (GBP) |
| positions_value | DECIMAL(12,2) | NO | Total positions value (GBP) |
| total_pnl | DECIMAL(12,2) | NO | Total P&L (GBP) |
| position_count | INTEGER | NO | Number of open positions |
| created_at | TIMESTAMP | NO | Snapshot creation time |

### Notes
- UNIQUE constraint prevents duplicate snapshots per day
- Idempotent: Can run multiple times per day (updates existing)
- Should be automated via cron (4 PM weekdays recommended)
- Used for performance charts and historical analysis

---

## 5. Trade History Table

Historical record of closed positions.

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trade_history_portfolio 
ON trade_history(portfolio_id, exit_date DESC);
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| portfolio_id | UUID | FK to portfolios |
| ticker | VARCHAR(20) | Stock symbol |
| market | VARCHAR(5) | "US" or "UK" |
| entry_date | DATE | Entry date |
| exit_date | DATE | Exit date |
| shares | DECIMAL(10,4) | Number of shares |
| entry_price | DECIMAL(10,4) | Entry price |
| exit_price | DECIMAL(10,4) | Exit price |
| total_cost | DECIMAL(12,2) | Total cost (GBP) |
| gross_proceeds | DECIMAL(12,2) | Proceeds before fees (GBP) |
| net_proceeds | DECIMAL(12,2) | Proceeds after fees (GBP) |
| entry_fees | DECIMAL(10,2) | Fees paid on entry |
| exit_fees | DECIMAL(10,2) | Fees paid on exit |
| pnl | DECIMAL(12,2) | Realized P&L (GBP) |
| pnl_pct | DECIMAL(10,2) | P&L percentage |
| holding_days | INTEGER | Days held |
| exit_reason | VARCHAR(50) | Reason for exit |
| entry_fx_rate | DECIMAL(10,6) | GBP/USD at entry |
| exit_fx_rate | DECIMAL(10,6) | GBP/USD at exit |
| created_at | TIMESTAMP | Record creation |

### Exit Reasons

- "Stop Loss Hit"
- "Risk-Off Signal"
- "Manual Exit"
- "Profit Target"

---

## 6. Settings Table

Configuration for trading strategy and preferences.

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | UUID | - | Primary key |
| min_hold_days | INTEGER | 10 | Grace period (days) |
| atr_multiplier_initial | DECIMAL | 5.0 | Wide stop for losing positions |
| atr_multiplier_trailing | DECIMAL | 2.0 | Tight stop for profitable positions |
| atr_period | INTEGER | 14 | ATR calculation period |
| default_currency | VARCHAR | GBP | Portfolio base currency |
| theme | VARCHAR | dark | UI theme preference |
| uk_commission | DECIMAL | 9.95 | UK trading commission (£) |
| us_commission | DECIMAL | 0.00 | US trading commission |
| stamp_duty_rate | DECIMAL | 0.005 | UK stamp duty (0.5%) |
| fx_fee_rate | DECIMAL | 0.0015 | FX conversion fee (0.15%) |
| created_at | TIMESTAMP | NOW | Record creation |
| updated_at | TIMESTAMP | NOW | Last update |

---

## Data Relationships

```
portfolios (1) ──┬── (N) positions
                 ├── (N) cash_transactions
                 ├── (N) portfolio_history
                 └── (N) trade_history

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
-- Update position with live price
UPDATE positions 
SET 
    current_price = 250.38,
    holding_days = 8,
    pnl = 29.06,
    pnl_pct = 2.98,
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

---

## Query Examples

### Get Portfolio Summary
```sql
SELECT 
    p.cash,
    COUNT(pos.id) FILTER (WHERE pos.status = 'open') as open_positions,
    SUM(pos.total_cost) FILTER (WHERE pos.status = 'open') as invested,
    SUM(pos.pnl) FILTER (WHERE pos.status = 'open') as unrealized_pnl
FROM portfolios p
LEFT JOIN positions pos ON p.id = pos.portfolio_id
WHERE p.id = 'portfolio-id'
GROUP BY p.id, p.cash;
```

### Get Win Rate
```sql
SELECT 
    COUNT(*) FILTER (WHERE pnl > 0) * 100.0 / COUNT(*) as win_rate,
    AVG(pnl) FILTER (WHERE pnl > 0) as avg_winner,
    AVG(pnl) FILTER (WHERE pnl < 0) as avg_loser
FROM trade_history
WHERE portfolio_id = 'portfolio-id';
```

### Get Net Cash Flow
```sql
SELECT 
    SUM(amount) FILTER (WHERE type = 'deposit') as total_deposits,
    SUM(amount) FILTER (WHERE type = 'withdrawal') as total_withdrawals,
    SUM(CASE WHEN type = 'deposit' THEN amount ELSE -amount END) as net_cash_flow
FROM cash_transactions
WHERE portfolio_id = 'portfolio-id';
```

---

## Migration from v1.0 to v1.1

### Required Changes

1. **Add cash_transactions table**
2. **Add portfolio_history table**
3. **Alter positions.shares to DECIMAL(10,4)**
4. **Record initial deposit**

```sql
-- Migration script
BEGIN;

-- Add cash transactions table
CREATE TABLE cash_transactions (
    -- schema above
);

-- Add portfolio history table
CREATE TABLE portfolio_history (
    -- schema above
);

-- Allow fractional shares
ALTER TABLE positions ALTER COLUMN shares TYPE DECIMAL(10, 4);

-- Record initial deposit (CRITICAL!)
INSERT INTO cash_transactions (portfolio_id, type, amount, date, note)
SELECT 
    id,
    'deposit',
    initial_cash,
    created_at::date,
    'Initial deposit (migration)'
FROM portfolios;

COMMIT;
```

---

## Future Schema Changes (Planned)

### v1.2 - Trade Journal
```sql
ALTER TABLE positions ADD COLUMN entry_note TEXT;
ALTER TABLE positions ADD COLUMN tags TEXT[];
ALTER TABLE trade_history ADD COLUMN exit_note TEXT;
ALTER TABLE trade_history ADD COLUMN tags TEXT[];
```

### v1.3 - Alerts
```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    portfolio_id UUID REFERENCES portfolios(id),
    type VARCHAR(50),
    message TEXT,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP
);
```

### v2.0 - Multi-User
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

**Document Version:** 1.1  
**Maintained By:** Development Team  
**Last Review:** February 1, 2026
