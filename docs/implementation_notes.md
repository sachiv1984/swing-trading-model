# Implementation Notes - Recent Features

**Document Version:** 1.2  
**Last Updated:** February 8, 2026

This document provides technical implementation details for features added after the initial MVP.

---

## Partial Exit & Exit Flexibility (v1.2)

**Implemented:** February 7, 2026  
**Status:** ✅ Complete

### Overview
Complete exit flexibility with partial exits, custom dates, user-provided prices and FX rates. This enables accurate P&L reconciliation with broker statements and flexible position management.

### Key Features

#### 1. Partial Exit
- Specify number of shares to exit
- Position remains open with reduced shares
- Cost basis proportionally reduced
- Stops remain unchanged
- Example: Exit 2.5 of 5.5 shares → 3 shares remain open

#### 2. User-Provided Exit Price (CRITICAL)
- **REQUIRED** field (no longer fetches live price)
- User enters actual broker execution price
- Ensures P&L matches broker statement exactly
- Accounts for slippage, execution quality
- For US stocks: user enters price in USD (their trading currency)
- For UK stocks: user enters price in GBP

**Why this matters:**
- Live market price ≠ actual execution price
- Slippage can be significant (±0.5%)
- Reconciliation requires exact broker prices
- Trust: user sees exact fees/proceeds before confirmation

#### 3. User-Provided FX Rate (CRITICAL for US stocks)
- **REQUIRED** for US stock exits
- User enters GBP/USD rate from broker statement
- Ensures cash conversion matches broker exactly
- Prevents discrepancies from live FX rate differences
- Typical variance: 0.1-0.3% between live rate and broker rate

**Why this matters:**
```
Example: Exit $1,000 position
Live FX rate: 1.3650
Broker FX rate: 1.3611 (0.29% difference)
Cash difference: £732.60 vs £735.02 = £2.42 discrepancy

Over 50 trades: ~£120 cumulative error!
```

#### 4. Custom Exit Date
- Optional field (defaults to today)
- Allows backdating for reconciliation
- Format: YYYY-MM-DD
- Holding days calculated from entry to exit date
- Use case: Position exited in broker, now recording in app

#### 5. Exit Reason Selection
- Dropdown with predefined options
- Tracked in trade history for analysis
- Options:
  - Manual Exit (default)
  - Stop Loss Hit
  - Target Reached
  - Risk-Off Signal
  - Trailing Stop
  - Partial Profit Taking

### Backend Implementation

**File:** `backend/main.py` lines 737-930

**Request Model:**
```python
class ExitPositionRequest(BaseModel):
    shares: Optional[float] = None  # None = all shares
    exit_price: float  # REQUIRED
    exit_date: Optional[str] = None  # YYYY-MM-DD
    exit_reason: Optional[str] = None
    exit_fx_rate: Optional[float] = None  # REQUIRED for US stocks
```

**Key Logic Changes:**

1. **FX Rate Validation (lines 752-761):**
```python
if position['market'] == 'US':
    if request.exit_fx_rate and request.exit_fx_rate > 0:
        exit_fx_rate = request.exit_fx_rate
    else:
        raise HTTPException(
            status_code=400,
            detail="FX rate is required for US stock exits. Please provide the GBP/USD rate from your broker statement."
        )
else:
    exit_fx_rate = 1.0
```

2. **Proportional Cost Calculation (lines 812-820):**
```python
total_cost = float(position['total_cost'])
cost_per_share = total_cost / total_shares
exit_total_cost = cost_per_share * exit_shares

entry_fees = float(position.get('fees_paid', 0))
entry_fees_per_share = entry_fees / total_shares
exit_entry_fees = entry_fees_per_share * exit_shares
```

3. **GBP Conversion with User FX Rate (lines 800-805):**
```python
if market == 'US':
    gross_proceeds_gbp = gross_proceeds_native / exit_fx_rate
    net_proceeds_gbp = net_proceeds_native / exit_fx_rate
    exit_fees_gbp = exit_fees_native / exit_fx_rate
else:
    gross_proceeds_gbp = gross_proceeds_native
    net_proceeds_gbp = net_proceeds_native
```

4. **Exit Date Handling (lines 827-836):**
```python
if request.exit_date:
    exit_date = datetime.strptime(request.exit_date, '%Y-%m-%d')
    exit_date_str = request.exit_date
else:
    exit_date = datetime.now()
    exit_date_str = exit_date.strftime('%Y-%m-%d')

holding_days = (exit_date - entry_date).days
```

5. **Partial vs Full Exit (lines 880-917):**
```python
is_partial_exit = exit_shares < total_shares

if is_partial_exit:
    remaining_shares = total_shares - exit_shares
    remaining_cost = total_cost - exit_total_cost
    
    updated_position = update_position(position_id, {
        'shares': remaining_shares,
        'total_cost': remaining_cost,
        'fees_paid': entry_fees - exit_entry_fees
    })
else:
    updated_position = update_position(position_id, {
        'status': 'closed',
        'exit_date': exit_date_str,
        'exit_price': exit_price_native,
        'exit_reason': exit_reason
    })
```

### Frontend Requirements

**ExitModal Component Must:**

1. **Validate inputs:**
   - `exit_price > 0` (required)
   - `shares > 0 and shares <= position.shares`
   - `exit_fx_rate > 0` (required for US stocks only)
   - `exit_date` format YYYY-MM-DD, not before entry_date

2. **Display real-time preview:**
   - Entry cost calculation (from `position.total_cost`)
   - Exit proceeds calculation
   - Fee breakdown (commission, FX fee)
   - Net proceeds in GBP (show FX conversion)
   - Realized P&L preview
   - All calculations in native currency for clarity

3. **Pre-fill sensible defaults:**
   - Shares: all shares
   - Exit price: current_price_native
   - Exit date: today
   - Exit reason: "Manual Exit"
   - FX rate: live_fx_rate (user should verify against broker)

4. **Show clear labels:**
   - US stock: "Exit price (USD)", "GBP/USD rate from broker"
   - UK stock: "Exit price (GBP)"

### API Endpoint

**POST /positions/{position_id}/exit**

**Request:**
```json
{
  "shares": 5.5,
  "exit_price": 242.67,
  "exit_date": "2026-02-07",
  "exit_reason": "Stop Loss Hit",
  "exit_fx_rate": 1.3611
}
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "ticker": "WDC",
    "market": "US",
    "exit_price": 242.67,
    "shares": 5.5,
    "gross_proceeds": 980.59,
    "exit_fees": 1.47,
    "fee_breakdown": {
      "commission": 0,
      "stamp_duty": 0,
      "fx_fee": 2.00
    },
    "net_proceeds": 979.12,
    "realized_pnl": -10.29,
    "realized_pnl_pct": -1.04,
    "new_cash_balance": 4153.35,
    "exit_fx_rate": 1.3611,
    "exit_date": "2026-02-07",
    "is_partial_exit": false,
    "remaining_shares": 0
  }
}
```

### Database Impact

**No schema changes required!**

All fields already existed in schema:
- `positions.shares` (DECIMAL - supports fractional)
- `positions.exit_date` (DATE)
- `positions.exit_price` (DECIMAL)
- `positions.exit_reason` (VARCHAR)
- `trade_history.exit_fx_rate` (DECIMAL)

### Example Usage

**Full Exit:**
```javascript
const exitPayload = {
  position_id: "f9516f4e-698d-43ec-8dde-c55ef7496657",
  shares: null,  // null = all shares
  exit_price: 242.67,
  exit_date: "2026-02-07",
  exit_reason: "Stop Loss Hit",
  exit_fx_rate: 1.3611  // Required for US stocks
};
```

**Partial Exit:**
```javascript
const exitPayload = {
  position_id: "f9516f4e-698d-43ec-8dde-c55ef7496657",
  shares: 2.5,  // Exit 2.5 of 5.5 shares
  exit_price: 250.00,
  exit_date: "2026-02-07",
  exit_reason: "Partial Profit Taking",
  exit_fx_rate: 1.3611
};
```

### Testing Checklist

- [x] Full exit US stock with user FX rate
- [x] Full exit UK stock (no FX rate needed)
- [x] Partial exit (2.5 of 5.5 shares)
- [x] Custom exit date (backdated)
- [x] All exit reasons from dropdown
- [x] Validation: missing FX rate for US stock
- [x] Validation: shares > position total
- [x] Validation: exit_price = 0
- [x] P&L matches ExitModal preview
- [x] Trade history shows correct FX rate
- [x] Remaining shares calculated correctly
- [x] Cost basis proportionally reduced

### Common Issues & Solutions

**Issue:** P&L doesn't match broker statement  
**Solution:** User must enter exact broker execution price and FX rate

**Issue:** FX rate validation error  
**Solution:** Ensure exit_fx_rate is provided for US stocks (check market field)

**Issue:** Partial exit leaves wrong shares  
**Solution:** Verify shares calculation: remaining = total - exited

**Issue:** Exit date validation fails  
**Solution:** Ensure exit_date >= entry_date format

### Migration Notes

**Breaking Change from v1.1:**
- Previously: Backend fetched live price (optional user override)
- Now: User MUST provide exit price (required field)
- Frontend must be updated to always provide exit_price
- Old API calls without exit_price will fail with 400 error

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

### 6. User-Provided Data for Reconciliation (v1.2)
- Exit price from broker (not live price)
- FX rate from broker (not live rate)
- Allows exact reconciliation
- Small differences compound over time

---

## Migration Checklist

When deploying these features:

### Backend
- [ ] Run database migrations (if needed)
- [ ] Add cash transaction functions to database.py
- [ ] Deploy updated main.py
- [ ] Test all endpoints with curl

### Frontend  
- [ ] Install Radix UI dependencies
- [ ] Create/update ExitModal with all fields
- [ ] Update Positions.js to pass position_id
- [ ] Test exit modal with US and UK stocks
- [ ] Verify FX rate validation

### Data Setup
- [ ] Record initial deposit transaction
- [ ] Create first portfolio snapshot
- [ ] Set up GitHub Actions or Render cron
- [ ] Verify P&L is correct

### Validation
- [ ] Check portfolio P&L matches expected
- [ ] Verify cash transactions appear
- [ ] Confirm charts show data
- [ ] Test full and partial exits
- [ ] Verify trade history records correct FX rate

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

### Issue: Exit validation fails (v1.2)
**Solution:** Check exit_fx_rate is provided for US stocks, verify parameter name is `exit_fx_rate` not `fx_rate`

### Issue: Trade history shows wrong FX rate (v1.2)
**Solution:** Run SQL fix script to update existing trades with correct broker FX rates

---

## Future Considerations

### When Adding Trade Journal
- Add `entry_note` and `exit_note` to positions table
- Update position entry form
- Update exit modal
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
**Version:** 1.2  
**Last Updated:** February 8, 2026
