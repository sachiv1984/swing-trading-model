# Implementation Notes - Recent Features

**Document Version:** 1.1  
**Last Updated:** February 1, 2026

This document provides technical implementation details for features added after the initial MVP.

---

## Cash Management System (v1.1)

**Implemented:** January 31, 2026  
**Status:** ✅ Complete

### Overview
Tracks deposits and withdrawals to calculate accurate portfolio P&L that accounts for cash flows.

### Database Schema

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
```

### Key Functions (database.py)

```python
def create_cash_transaction(portfolio_id: str, transaction_data: Dict)
def get_cash_transactions(portfolio_id: str, order_by: str = 'DESC')
def get_total_deposits_withdrawals(portfolio_id: str)
```

### API Endpoints (main.py)

- `POST /cash/transaction` - Create deposit/withdrawal
- `GET /cash/transactions` - List transactions
- `GET /cash/summary` - Get totals

### Frontend Components

- `CashManagementModal.js` - Modal UI for deposits/withdrawals
- `StatsWidgets.js` - Clickable cash balance widget
- `Dashboard.js` - Integration with modal

### P&L Calculation Change

**Old (Incorrect):**
```python
true_total_pnl = total_positions_value_gbp - total_cost_of_positions
```

**New (Correct):**
```python
net_cash_flow = total_deposits - total_withdrawals
true_total_pnl = total_value - net_cash_flow
```

### Critical Setup Step

**Must record initial deposit!**

```sql
INSERT INTO cash_transactions (portfolio_id, type, amount, date, note)
VALUES ('your-portfolio-id', 'deposit', 5000, '2026-01-23', 'Initial deposit');
```

Without this, P&L will be incorrect.

---

## Portfolio History & Charts (v1.1)

**Implemented:** January 31, 2026  
**Status:** ✅ Complete

### Overview
Daily snapshots of portfolio performance for historical tracking and chart visualization.

### Database Schema

```sql
CREATE TABLE portfolio_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    snapshot_date DATE NOT NULL,
    total_value DECIMAL(12, 2) NOT NULL,
    cash_balance DECIMAL(12, 2) NOT NULL,
    positions_value DECIMAL(12, 2) NOT NULL,
    total_pnl DECIMAL(12, 2) NOT NULL,
    position_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(portfolio_id, snapshot_date)
);
```

### Key Functions (database.py)

```python
def create_portfolio_snapshot(snapshot_data: Dict)
def get_portfolio_snapshots(portfolio_id: str, days: int = 30)
def get_latest_snapshot(portfolio_id: str)
```

### API Endpoints (main.py)

- `POST /portfolio/snapshot` - Create daily snapshot
- `GET /portfolio/history?days=30` - Get historical data

### Frontend Components

- `PortfolioChart.js` - Recharts visualization
- Updated to fetch from `/portfolio/history`
- Falls back to sample data if no history exists

### Automation

**GitHub Actions Workflow:**
```yaml
name: Daily Portfolio Snapshot
on:
  schedule:
    - cron: '0 16 * * 1-5'  # 4 PM UTC weekdays
  workflow_dispatch:

jobs:
  create-snapshot:
    runs-on: ubuntu-latest
    steps:
      - name: Create Snapshot
        env:
          API_URL: ${{ secrets.API_URL }}
        run: |
          curl -X POST "${API_URL}/portfolio/snapshot"
```

**Alternative: Render Cron Job**
- More reliable for hosted apps
- Configure in Render dashboard
- Command: `curl -X POST https://your-api.onrender.com/portfolio/snapshot`

---

## Multi-Currency Support (v1.1)

**Implemented:** January 30, 2026  
**Status:** ✅ Complete

### Overview
Handles USD and GBP positions with live FX conversion for accurate P&L.

### Key Concepts

1. **Stored FX Rate** - Rate at purchase time (in position record)
2. **Live FX Rate** - Current rate from Yahoo Finance
3. **Dual Prices** - GBP (calculations) + Native (display)

### Live FX Rate Fetching

```python
def get_live_fx_rate():
    """Fetch GBP/USD from Yahoo Finance"""
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GBPUSD=X"
    # ... implementation
    return fx_rate  # e.g., 1.3685
```

### Position Price Fields

- `current_price` - GBP (for Dashboard calculations)
- `current_price_native` - USD or GBP (for display)
- `stop_price` - GBP (for calculations, 0 during grace)
- `stop_price_native` - USD or GBP (for display, 0 during grace)

### Currency Conversion Logic

**US Stocks:**
```python
# Yahoo returns USD
current_price_native = live_price  # USD
current_price_gbp = live_price / live_fx_rate  # GBP

# P&L calculation
entry_price_usd = pos['fill_price']  # USD
pnl_usd = (current_price_native - entry_price_usd) * shares
pnl_gbp = pnl_usd / live_fx_rate
```

**UK Stocks:**
```python
# Yahoo returns pence
current_price_native = live_price / 100  # Convert to pounds
current_price_gbp = current_price_native  # Already GBP

# P&L calculation
pnl_gbp = (current_price_native - entry_price) * shares
```

### Frontend Display

**PositionCard.js & Positions.js:**
```javascript
const displayCurrentPrice = position.current_price_native || position.current_price;
const displayStopPrice = position.stop_price_native || position.stop_price;
```

Shows prices in native currency (what trader sees in broker).

---

## Grace Period & Stop Loss Logic (v1.0)

**Implemented:** January 27, 2026  
**Status:** ✅ Complete

### Grace Period Rules

- **Duration:** 10 days from entry
- **Purpose:** Prevent premature stop-outs
- **Behavior:** Stop loss displayed as £0.00 / $0.00

### Stop Calculation After Grace Period

**Profitable Positions (P&L > 0):**
```python
atr_multiplier = 2  # Tight trailing stop
new_stop = current_price - (2 × ATR)
```

**Losing Positions (P&L ≤ 0):**
```python
atr_multiplier = 5  # Wide stop
new_stop = current_price - (5 × ATR)
```

**Trailing Logic:**
```python
# Stop only moves up, never down
trailing_stop = max(current_stop, new_stop)
```

### Implementation

**Backend (main.py - /positions/analyze):**
```python
holding_days = (datetime.now() - entry_date).days
grace_period = holding_days < 10

if grace_period:
    current_stop_gbp = 0
    stop_price_native = 0
    display_stop = 0
    stop_reason = f"Grace period ({holding_days}/10 days)"
else:
    # Calculate trailing stop based on profitability
    # ...
```

### Frontend Display

```javascript
// In PositionCard/Positions table
{grace_period ? (
  <span className="text-slate-400">Grace period ({holding_days}/10)</span>
) : (
  <span>£{stop_price.toFixed(2)}</span>
)}
```

---

## Fractional Shares Support (v1.0)

**Implemented:** January 27, 2026  
**Status:** ✅ Complete

### Changes

**Request Model (main.py):**
```python
class AddPositionRequest(BaseModel):
    shares: float  # Changed from int
```

**Database:**
```sql
ALTER TABLE positions ALTER COLUMN shares TYPE DECIMAL(10, 4);
```

### Use Cases

- UK stocks often require fractional shares due to high prices
- Allows precise position sizing
- Example: 5.5 shares of WDC at $243

---

## Live Price Fetching (v1.0)

**Implemented:** January 29, 2026  
**Status:** ✅ Complete

### Implementation

```python
def get_current_price(ticker: str) -> float:
    """Fetch from Yahoo Finance API"""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    # ... implementation with retries and error handling
```

### Key Features

1. **No library dependencies** - Direct API calls
2. **Rate limiting protection** - 300ms delay between calls
3. **Fallback logic** - Uses stored price if fetch fails
4. **Pence conversion** - Handles UK stocks (divides by 100)

### When Prices Are Fetched

- `/positions` endpoint - ALWAYS fetches live prices
- `/positions/analyze` endpoint - Fetches and updates database
- `/portfolio` endpoint - Fetches for all positions

### Error Handling

```python
if live_price:
    current_price = live_price
else:
    print(f"⚠️  Using stored price for {ticker}")
    current_price = pos.get('current_price', entry_price)
```

---

## Dashboard P&L Display Fix (v1.1)

**Implemented:** February 1, 2026  
**Status:** ✅ Complete

### Problem

Dashboard was recalculating P&L by summing individual position P&Ls:
```javascript
const totalPnL = openPositions.reduce((sum, p) => sum + (p.pnl || 0), 0);
```

This was wrong because:
1. Doesn't account for fees
2. Doesn't account for deposits/withdrawals

### Solution

Use pre-calculated P&L from portfolio endpoint:
```javascript
const totalPnL = portfolio?.total_pnl || 0;
```

### Why This Works

Backend calculates:
```python
net_cash_flow = total_deposits - total_withdrawals
true_total_pnl = total_value - net_cash_flow
```

This accounts for everything:
- Entry fees (commission, stamp duty, FX fees)
- Deposits and withdrawals
- Current market values
- Correct currency conversion

---

## Best Practices Learned

### 1. Never Recalculate on Frontend
- Always use backend-calculated values
- Frontend should display, not compute
- Prevents inconsistencies and bugs

### 2. Dual Price Fields Essential
- One for calculations (GBP)
- One for display (native currency)
- Impossible to do with single field

### 3. Always Record Cash Transactions
- Critical for accurate P&L
- Don't forget initial deposit!
- P&L meaningless without this

### 4. Grace Period UX
- Show "0" for stops during grace
- Display countdown: "8/10 days"
- Explain why no stop is active

### 5. Error Messages Matter
- "Insufficient funds" better than generic error
- Show current balance in error
- Validate before API call when possible

---

## Migration Checklist

When deploying these features:

### Backend
- [ ] Run database migrations
- [ ] Add cash transaction functions to database.py
- [ ] Deploy updated main.py
- [ ] Test all endpoints with curl

### Frontend  
- [ ] Install Radix UI dependencies
- [ ] Create cash modal component
- [ ] Update Dashboard.js
- [ ] Update StatsWidgets.js
- [ ] Test cash modal interaction

### Data Setup
- [ ] Record initial deposit transaction
- [ ] Create first portfolio snapshot
- [ ] Set up GitHub Actions or Render cron
- [ ] Verify P&L is correct

### Validation
- [ ] Check portfolio P&L matches expected
- [ ] Verify cash transactions appear
- [ ] Confirm charts show data
- [ ] Test deposit/withdrawal flows

---

## Common Issues & Solutions

### Issue: P&L is wrong after adding features
**Solution:** Make sure initial deposit is recorded in cash_transactions

### Issue: Chart shows sample data
**Solution:** Create snapshots with `POST /portfolio/snapshot`

### Issue: Radix UI errors
**Solution:** `npm install @radix-ui/react-tabs @radix-ui/react-dialog @radix-ui/react-label`

### Issue: Dashboard P&L doesn't match portfolio endpoint
**Solution:** Update Dashboard.js to use `portfolio?.total_pnl` instead of recalculating

### Issue: USD stocks showing GBP prices
**Solution:** Use `current_price_native` for display, not `current_price`

---

## Future Considerations

### When Adding Trade Journal
- Add `entry_note` and `exit_note` to positions table
- Update position entry form
- Create notes display component

### When Adding Alerts
- Create alerts table
- Set up email service (SendGrid, AWS SES)
- Add cron job to check conditions
- Create alert preferences UI

### When Adding Analytics
- Most data already exists in trade_history
- Just need aggregation endpoints
- Consider caching expensive calculations
- Use PostgreSQL window functions for efficiency

---

**Document maintained by:** Development Team  
**Review frequency:** After each feature release
