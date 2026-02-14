# Frontend Functional Specification (React SPA)

**Version:** 1.4  
**Last Updated:** February 14, 2026  
**Status:** Current

## Overview
This document defines the frontend requirements for the Position Manager Web App, a React Single Page Application (SPA).  
The frontend will connect to backend APIs (OpenAPI spec) to manage portfolio creation, position entry, daily monitoring, trade journaling, and trade history.

---

# 1. General Requirements

## 1.1 UI Framework
- React (SPA)
- Recommended: TypeScript
- UI library: TailwindCSS or Material UI (developer choice)
- State management: React Context or Redux (developer choice)
- Routing: React Router

## 1.2 Theme
- Default: **Dark Mode**
- Optional: Light Mode toggle
- Theme persistence: store user preference in `localStorage`

## 1.3 Authentication
- Initially no authentication required (local demo mode)
- Optionally add authentication later (OAuth or JWT)

## 1.4 Error Handling
- Global error banner for API failures
- Inline error messages for forms
- Retry button for failed API calls

---

# 2. Pages & Components

## 2.1 Global Layout
**Header**
- App name/logo
- Theme toggle (Dark/Light)
- Navigation links:
  - Dashboard
  - Positions
  - Trade Entry
  - Trade History
  - Settings

**Footer**
- Version
- Support link
- Link to documentation

---

# 3. Page Specifications

---

## 3.1 Dashboard (Home)

### Purpose
Show portfolio summary, risk status, and quick actions.

### Data Display
- Total portfolio value
- Cash balance (clickable - opens cash management modal)
- Open positions value
- Total P&L
- Market status (SPY / FTSE risk on/off)
- Performance chart (30-day history)

### Actions
- Button: "Go to Positions"
- Button: "Enter New Position"
- Button: "Daily Monitor" (run position manager)

### API Integration
- `GET /portfolio`
- `GET /portfolio/history?days=30`
- `GET /positions/analyze` (for daily monitor)

---

## 3.2 Positions Page

### Purpose
List open positions with current stop levels and P&L.

### UI Elements
- **View Switcher (NEW v1.4):**
  - Grid view (cards)
  - Table view (table)
  - Journal view (all positions with notes/tags) ⭐ NEW
  
- Table/List of positions:
  - Ticker
  - Market flag (🇺🇸 US / 🇬🇧 UK)
  - Entry price (in native currency)
  - Current price (in native currency)
  - Stop price (in native currency, shows £0.00/$0.00 during grace)
  - Shares (supports fractional display, e.g., "5.5")
  - P&L (in GBP)
  - P&L % 
  - Days held (with grace period indicator if < 10 days)
  - Status badge (GRACE/PROFITABLE/LOSING)
  - **Tags (NEW v1.4)** - displayed as colored pills
  - Action buttons:
    - "Exit" (opens exit modal)
    - "View Journal" (opens position modal with notes)

### Grace Period Display
- Show "Grace period (X/10 days)" instead of stop price when holding_days < 10
- Visual indicator (badge or icon) for positions in grace period
- Tooltip explaining grace period concept

### API Integration
- `GET /positions` (fetches live prices, includes notes/tags)
- `GET /positions/tags` (for tag filter in journal view)

---

## 3.3 Position Detail Modal

### Purpose
Show position detail, stop logic, and journal entries.

### UI Elements

**Position Details:**
- Entry details
  - Entry date
  - Entry price (native currency)
  - Shares (fractional)
  - Total cost (GBP)
  - Fees paid
  
- Current status
  - Current price (native currency)
  - Days held
  - Grace period indicator
  - Stop levels
  - Risk status
  
- P&L breakdown
  - Unrealized P&L (GBP)
  - P&L %

**Journal Section (NEW v1.4):**
- Entry Note card
  - Text display of entry_note
  - "Edit" button (opens inline editor)
  - Shows "No entry note" if empty
  - Character count when editing (500 max)
  
- Exit Note card (if position closed)
  - Text display of exit_note
  - "Edit" button (opens inline editor)
  - Shows "No exit note" if empty
  - Character count when editing (500 max)
  
- Tags section
  - Display tags as colored pills
  - "Edit Tags" button
  - Autocomplete when adding tags
  - Click X to remove tag
  - Max 10 tags indicator
  
**Actions:**
- Edit Note button → Opens inline text editor
- Edit Tags button → Opens tag input
- Save button → PATCH /positions/{id}/note or /positions/{id}/tags
- Close button

### Graph (Optional)
- Price history chart

### API Integration
- `GET /positions/{ticker}` - Get position with notes/tags
- `PATCH /positions/{id}/note` - Update entry_note or exit_note ✅ NEW v1.4
- `PATCH /positions/{id}/tags` - Update tags ✅ NEW v1.4
- `GET /positions/tags` - Get autocomplete suggestions ✅ NEW v1.4

---

## 3.4 Trade Entry Page

### Purpose
Add a new position manually (manual entry).

### Inputs
- Ticker (required)
  - Text input
  - Auto-uppercase
  - Market auto-detected from .L suffix
  
- Entry date (required)
  - Date picker
  - Format: YYYY-MM-DD
  - Default: today
  
- Shares (required)
  - Number input
  - Supports fractional (e.g., 5.5)
  - Min: 0.0001
  
- Entry price (required)
  - Number input
  - In native currency (USD for US, GBP for UK)
  - Label adjusts based on market
  
- FX rate (conditional)
  - Number input
  - Only shown for US stocks
  - Auto-fetched from Yahoo Finance if not provided
  - User can override
  - Format: 1.XXXX (4 decimal places)
  
- ATR value (optional)
  - Number input
  - Auto-calculated from Yahoo Finance if not provided
  - User can override
  
- Stop price (optional)
  - Number input
  - Auto-calculated as entry_price - (5 × ATR) if not provided
  - User can override

- Entry note (optional) ✅ NEW v1.4
  - Text area input
  - Max 500 characters
  - Character counter displayed
  - Placeholder: "Document your entry reasoning, setup, risk/reward..."
  - Label: "Entry Note (Optional)"
  
- Tags (optional) ✅ NEW v1.4
  - Tag input component with autocomplete
  - Fetches existing tags from GET /positions/tags
  - Displays as colored pills
  - Click X to remove tag
  - Press Enter to add tag
  - Auto-lowercase conversion
  - Max 10 tags
  - Validation: lowercase, numbers, hyphens only
  - Label: "Tags (Optional)"

### Validation Rules
- Ticker: Not empty, max 10 characters
- Entry date: Valid date, not in future
- Shares: > 0, max 4 decimal places
- Entry price: > 0, max 2 decimal places
- FX rate: > 0 (if US stock), max 6 decimal places
- ATR: > 0 (if provided)
- Insufficient funds: total_cost > available cash → show error
- Entry note: max 500 characters ✅ NEW v1.4
- Tags: each tag max 20 chars, max 10 tags total, lowercase/numbers/hyphens only ✅ NEW v1.4

### Output
- Fee breakdown
  - UK: Commission (£9.95) + Stamp duty (0.5%)
  - US: FX fee (0.15%)
- Total cost (GBP)
- Initial stop level
- Entry note preview ✅ NEW v1.4
- Tags list ✅ NEW v1.4
- Confirmation button

### API Integration
- `POST /portfolio/position` - Accepts entry_note, tags (optional) ✅ UPDATED v1.4

### Error Handling
- Show inline error for validation failures
- Show error banner for API failures
- Display remaining cash in error message for insufficient funds

---

## 3.5 Exit Position Modal (v1.4)

### Purpose
Exit a position (full or partial) with detailed fee preview and journal notes.

### Inputs
- Shares to exit (optional)
  - Number input
  - Default: all shares
  - Max: total shares in position
  - Supports fractional
  - Label: "Shares to exit (Total: X.XX)"
  
- Exit price (REQUIRED)
  - Number input
  - In native currency
  - Pre-filled with current market price (user can edit)
  - Label: "Exit price (USD)" or "Exit price (GBP)"
  
- Exit date (optional)
  - Date picker
  - Format: YYYY-MM-DD
  - Default: today
  - Can backdate for reconciliation
  
- Exit reason (optional)
  - Dropdown
  - Options:
    - Manual Exit (default)
    - Stop Loss Hit
    - Target Reached
    - Risk-Off Signal
    - Trailing Stop
    - Partial Profit Taking
    
- FX rate (conditional - REQUIRED for US stocks)
  - Number input
  - Only shown for US stocks
  - Pre-filled with current FX rate (user can edit)
  - Label: "GBP/USD rate from broker"
  - Format: 1.XXXX (4+ decimal places)

- Exit note (optional) ✅ NEW v1.4
  - Text area input
  - Max 500 characters
  - Character counter displayed
  - Placeholder: "Document exit reasoning, lessons learned, emotions..."
  - Label: "Exit Note (Optional)"
  - Pre-filled with reflection prompts

### Validation Rules
- Shares: > 0, <= position.shares
- Exit price: > 0 (REQUIRED)
- Exit date: Valid date, >= entry_date
- Exit reason: One of valid options
- FX rate: > 0 (REQUIRED for US stocks)
- Exit note: max 500 characters ✅ NEW v1.4

### Preview Display (Before Confirmation)
Calculate and show:
- Entry cost (from position.total_cost proportional to shares)
- Gross proceeds (native currency)
- Fee breakdown:
  - Commission (if applicable)
  - FX fee (if applicable)
  - Total fees
- Net proceeds (native currency)
- Net proceeds (GBP with FX conversion shown)
- Realized P&L (GBP)
- Realized P&L %

### Confirmation Flow
1. User fills form
2. Real-time preview updates as they type
3. User clicks "Confirm Exit"
4. API call with all data
5. Success: Close modal, refresh positions
6. Error: Show error message, keep modal open

### API Integration
- `POST /positions/{position_id}/exit` - Accepts exit_note (optional) ✅ UPDATED v1.4

### Error Handling
- "Insufficient shares" → show error
- "FX rate required" → highlight FX rate field
- "Exit price required" → highlight exit price field
- API errors → show in modal with retry option

---

## 3.6 Trade History Page

### Purpose
View closed trades, performance metrics, and trade journals.

### UI Elements
- Summary stats:
  - Total trades
  - Win rate %
  - Total P&L (GBP)
  - Average winner
  - Average loser
  
- **Tag Filter (NEW v1.4):**
  - Dropdown showing all available tags
  - Multi-select (can choose multiple tags)
  - Filters trades showing ANY selected tag (OR logic)
  - Selected tags shown as removable pills
  - Only appears if trades have tags
  
- Table of trade history:
  - Ticker
  - Market flag
  - Entry date
  - Exit date
  - Shares (fractional display)
  - Entry price (native)
  - Exit price (native)
  - P&L (GBP)
  - P&L %
  - Days held
  - Exit reason
  - **Click row to expand journal (NEW v1.4)**
  
- **Expandable Journal Row (NEW v1.4):**
  - Full-width card spanning entire table row
  - "Trade Journal" header with gradient accent
  - Three sections:
    - 📘 Entry Analysis (cyan header) - shows entry_note
    - 📕 Exit Reflection (rose header) - shows exit_note
    - 🏷️ Strategy Tags (violet header) - shows tags as pills
  - Beautiful color-coded layout
  - Displays "No entry note" / "No exit note" if empty
  
- Filters:
  - Date range
  - Win/Loss
  - Market (US/UK)
  - Exit reason
  - **Tags (multi-select) ✅ NEW v1.4**

### API Integration
- `GET /trades` - Returns trades with entry_note, exit_note, tags fields ✅ UPDATED v1.4
- `GET /positions/tags` - Get all available tags for filter dropdown ✅ NEW v1.4

---

## 3.7 Cash Management Modal (v1.1)

### Purpose
Record deposits and withdrawals for accurate P&L tracking.

### Inputs
- Transaction type (required)
  - Radio buttons: Deposit / Withdrawal
  
- Amount (required)
  - Number input (GBP)
  - Min: 0.01
  
- Date (required)
  - Date picker
  - Format: YYYY-MM-DD
  - Default: today
  
- Note (optional)
  - Text input
  - Max 200 characters

### Transaction History Display
- List of all transactions
- Sortable by date
- Filter by type
- Running total display

### API Integration
- `POST /cash/transaction`
- `GET /cash/transactions`
- `GET /cash/summary`

---

## 3.8 Settings Page

### Purpose
Configure strategy parameters and portfolio settings.

### Settings
- Strategy Parameters:
  - Minimum hold days (grace period)
  - ATR multiplier (initial) - for losing positions
  - ATR multiplier (trailing) - for profitable positions
  - ATR period
  
- Trading Fees:
  - UK commission (GBP)
  - US commission (GBP)
  - Stamp duty rate (%)
  - FX fee rate (%)
  
- UI Preferences:
  - Default currency (GBP)
  - Theme preference (Dark/Light)

### API Integration
- `GET /settings`
- `PUT /settings`

---

## 3.9 Journal View (NEW v1.4)

### Purpose
Dedicated view for reviewing all positions with journal entries (open + closed).

### Access
- Positions page → View switcher → Journal button
- Shows book icon (📖)
- Alternative to Grid/Table views

### UI Elements

**Header:**
- Title: "Trade Journal"
- Description: "Review your trading decisions and learn from past trades"
- Tag filter dropdown
- Search bar (future)

**Position Cards:**
- Shows ALL positions (open and closed)
- Card layout similar to Grid view
- Displays:
  - Ticker and market flag
  - Entry/Exit dates
  - P&L (color coded)
  - Entry note (truncated, click to expand)
  - Exit note (if closed, truncated)
  - Tags as pills
  - "View Full Journal" button

**Filtering:**
- Filter by tags (same as Trade History)
- Filter by open/closed status
- Sort by:
  - Date (newest first)
  - P&L (best/worst)
  - Holding period

**Expandable View:**
- Click card to expand
- Shows full entry and exit notes
- All tags displayed
- Position metrics (P&L, days held, etc.)

### API Integration
- `GET /positions` - Fetches ALL positions (not just open)
- `GET /positions/tags` - Get available tags for filter

### Use Cases
- Monthly review of trades
- Pattern discovery in journals
- Learning from mistakes
- Celebrating wins

---

# 4. UI State & Flow

## 4.1 Portfolio Load Flow
1. App loads
2. Fetch portfolio data
3. If no portfolio exists → prompt user to create one
4. Redirect to Dashboard

## 4.2 Daily Monitor Flow
1. User clicks "Daily Monitor"
2. Fetch current prices + market regime
3. Display list of HOLD vs EXIT recommendations
4. User can click "Exit" on any EXIT recommendation
5. Opens exit modal pre-filled with current price
6. User confirms
7. App updates portfolio

## 4.3 Position Entry Flow
1. User navigates to "Trade Entry"
2. User enters ticker
3. Market auto-detected (.L = UK, else US)
4. For US stocks: FX rate auto-fetched (editable)
5. ATR auto-calculated (editable)
6. Stop auto-calculated from ATR
7. User adds entry note (optional)
8. User adds tags (optional, autocomplete from existing)
9. Fee preview shown
10. User confirms
11. Position created, redirect to Positions page

## 4.4 Exit Flow (Full)
1. User clicks "Exit" on position
2. Modal opens with form
3. All shares pre-selected
4. Current price pre-filled
5. Today's date pre-filled
6. For US: Current FX rate pre-filled
7. User adds exit note (optional)
8. User reviews fee breakdown
9. User confirms
10. Position closed, trade history created
11. Modal closes, positions refresh

## 4.5 Exit Flow (Partial)
1. User clicks "Exit" on position
2. Modal opens
3. User changes shares (e.g., 2.5 of 5 shares)
4. Preview updates for partial exit
5. User confirms
6. Position updated (2.5 shares remain)
7. Trade history created for exited shares
8. Modal closes, positions refresh

## 4.6 Journal Entry Flow (NEW v1.4)

1. **During Position Entry:**
   - User fills position details
   - User adds entry note (optional)
   - User adds tags (optional)
   - Tags autocomplete from existing
   - Character counter shows 500 max
   - Position created with journal data

2. **During Position Exit:**
   - User initiates exit
   - Modal pre-fills exit data
   - User adds exit note (optional)
   - Character counter shows 500 max
   - Exit confirmed
   - Journal data preserved in trade_history

3. **Editing Notes After Entry:**
   - User opens position modal
   - Clicks "Edit Note" button
   - Inline editor appears
   - User updates note
   - PATCH /positions/{id}/note
   - Note saved

4. **Managing Tags:**
   - User opens position modal
   - Clicks "Edit Tags" button
   - Tag input appears with autocomplete
   - User adds/removes tags
   - PATCH /positions/{id}/tags
   - Tags saved

5. **Filtering by Tags:**
   - User goes to Trade History
   - Clicks tag filter dropdown
   - Selects one or more tags
   - Trades filtered (OR logic)
   - Selected tags shown as pills
   - Click X to remove filter

6. **Reviewing Journal:**
   - User goes to Positions → Journal view
   - Sees all positions with journals
   - Filters by tags
   - Expands cards to read full notes
   - Identifies patterns

---

# 5. Accessibility
- Use semantic HTML
- Ensure keyboard navigation
- Color contrast for dark theme (WCAG AA)
- ARIA labels for tables & buttons
- Focus management in modals
- Screen reader announcements for dynamic content

---

# 6. Responsive Design
- Mobile-first layout
- Breakpoints: 640px, 768px, 1024px, 1280px
- Table collapses into cards on mobile
- Sidebar navigation becomes hamburger menu
- Modals are full-screen on mobile
- Forms stack vertically on mobile

---

# 7. Form Validation Summary

## Position Entry Form
```javascript
const validate = {
  ticker: (v) => v.length > 0 && v.length <= 10,
  entry_date: (v) => isValidDate(v) && !isFuture(v),
  shares: (v) => v > 0 && countDecimals(v) <= 4,
  entry_price: (v) => v > 0 && countDecimals(v) <= 2,
  fx_rate: (v, market) => market === 'UK' || v > 0,
  total_cost: (v, cash) => v <= cash,
  entry_note: (v) => !v || v.length <= 500,  // NEW v1.4
  tags: (arr) => arr.length <= 10 && arr.every(t => t.length <= 20 && /^[a-z0-9-]+$/.test(t))  // NEW v1.4
}
```

## Exit Position Form
```javascript
const validate = {
  shares: (v, max) => v > 0 && v <= max,
  exit_price: (v) => v > 0,  // REQUIRED
  exit_date: (v, entry) => isValidDate(v) && v >= entry,
  exit_fx_rate: (v, market) => market === 'UK' || v > 0,  // REQUIRED for US
  exit_note: (v) => !v || v.length <= 500  // NEW v1.4
}
```

## Cash Transaction Form
```javascript
const validate = {
  type: (v) => ['deposit', 'withdrawal'].includes(v),
  amount: (v) => v >= 0.01,
  date: (v) => isValidDate(v)
}
```

## Journal Entry Validation (NEW v1.4)
```javascript
const validate = {
  entry_note: (v) => {
    if (!v) return true;  // Optional
    if (v.length > 500) return false;
    return true;
  },
  exit_note: (v) => {
    if (!v) return true;  // Optional
    if (v.length > 500) return false;
    return true;
  },
  tag: (t) => {
    if (t.length > 20) return false;
    if (!/^[a-z0-9-]+$/.test(t)) return false;
    return true;
  },
  tags: (arr) => {
    if (arr.length > 10) return false;
    return arr.every(validate.tag);
  }
}
```

---

# 8. API Integration Map

| Page | API Endpoint | Purpose | Response Data |
|------|--------------|---------|---------------|
| Dashboard | `GET /portfolio` | Get portfolio summary | cash, total_value, total_pnl, positions |
| Dashboard | `GET /portfolio/history?days=30` | Get chart data | historical snapshots |
| Positions | `GET /positions` | Get open positions | positions with live prices |
| Position Detail | `GET /positions/{ticker}` | Get position details | detailed position info with notes/tags ✅ UPDATED v1.4 |
| Trade Entry | `POST /portfolio/position` | Create new position | confirmation with fees, accepts entry_note/tags ✅ UPDATED v1.4 |
| Trade Exit | `POST /positions/{position_id}/exit` | Exit position | proceeds, P&L, new balance, accepts exit_note ✅ UPDATED v1.4 |
| Trade History | `GET /trades` | Get completed trades | trade history with stats, notes, tags ✅ UPDATED v1.4 |
| Cash Management | `POST /cash/transaction` | Record deposit/withdrawal | new balance |
| Cash Management | `GET /cash/transactions` | List transactions | transaction history |
| Settings | `GET /settings` | Get config | all settings |
| Settings | `PUT /settings` | Update config | updated settings |
| Daily Monitor | `GET /positions/analyze` | Analyze positions | HOLD/EXIT recommendations |
| **Position Notes** | **`PATCH /positions/{id}/note`** | **Update notes** | **updated notes** ✅ **NEW v1.4** |
| **Position Tags** | **`PATCH /positions/{id}/tags`** | **Update tags** | **updated tags** ✅ **NEW v1.4** |
| **Tag Autocomplete** | **`GET /positions/tags`** | **Get all tags** | **unique tags list** ✅ **NEW v1.4** |

---

# 9. Data Flow Examples

## Position Entry Data Flow
```
Frontend Form → Validation → API Call
{
  ticker: "FRES",
  market: "UK",
  entry_date: "2026-01-31",
  shares: 27.25,
  entry_price: 40.98,
  fx_rate: null,
  atr_value: 2.58,
  stop_price: null
}

← Backend Response
{
  ticker: "FRES.L",
  total_cost: 1116.70,  // GBP
  fees_paid: 9.95,
  entry_price: 40.98,
  initial_stop: 28.08,
  remaining_cash: 4383.30
}
```

## Exit Position Data Flow
```
Frontend Modal → Validation → API Call
{
  position_id: "uuid",
  shares: 5.5,  // All shares
  exit_price: 242.67,  // User-entered from broker
  exit_date: "2026-02-07",
  exit_reason: "Stop Loss Hit",
  exit_fx_rate: 1.3611  // User-entered from broker
}

← Backend Response
{
  ticker: "NVDA",
  market: "US",
  exit_price: 242.67,
  shares: 5.5,
  gross_proceeds: 980.59,  // GBP
  exit_fees: 1.47,
  fee_breakdown: {
    commission: 0,
    stamp_duty: 0,
    fx_fee: 2.00  // USD
  },
  net_proceeds: 979.12,
  realized_pnl: -10.29,
  realized_pnl_pct: -1.04,
  new_cash_balance: 4153.35
}
```

## Journal Entry Data Flow (NEW v1.4)

### Creating Position with Journal
```
Frontend Form → Validation → API Call
{
  ticker: "NVDA",
  entry_date: "2026-02-14",
  shares: 10,
  entry_price: 850.00,
  entry_note: "Breakout above $800 resistance on heavy volume. RSI trending up. Stop at $820.",
  tags: ["momentum", "breakout"]
}

← Backend Response
{
  ticker: "NVDA",
  total_cost: 6256.25,  // GBP
  fees_paid: 9.38,
  entry_price: 850.00,  // USD
  initial_stop: 773.40,
  remaining_cash: 3743.75,
  entry_note: "Breakout above $800...",
  tags: ["momentum", "breakout"]
}
```

### Updating Notes
```
Frontend Modal → Edit Note → API Call
{
  position_id: "uuid",
  entry_note: "Updated: Added position after Fed decision. Market risk-on confirmed."
}

← Backend Response
{
  id: "uuid",
  ticker: "NVDA",
  entry_note: "Updated: Added position...",
  exit_note: null,
  updated_at: "2026-02-14T10:30:00"
}
```

### Filtering Trades by Tags
```
Frontend TradeHistory → Select Tags → Filter Client-Side
Selected Tags: ["momentum", "winner"]

Filtered Trades = trades.filter(t => 
  t.tags && selectedTags.some(tag => t.tags.includes(tag))
)

Result: Shows all trades tagged with "momentum" OR "winner"
```

---

# 10. Error States & Messages

## Insufficient Funds
```
Error: Insufficient funds
Total cost: £986.70
Available cash: £800.00
Shortfall: £186.70
```

## Invalid Exit Shares
```
Error: Insufficient shares
Position has 5.5 shares
Exit requested: 10.0 shares
```

## Missing FX Rate (US Stock)
```
Error: FX rate required for US stock exits
Please provide the GBP/USD rate from your broker statement.
```

## Invalid Date
```
Error: Exit date cannot be before entry date
Entry: 2026-01-23
Exit: 2026-01-20
```

## Journal Validation Errors (NEW v1.4)
```
Error: Entry note exceeds 500 character limit
Current: 523 characters
```

```
Error: Invalid tag format
Tag: "My Tag!"
Allowed: lowercase letters, numbers, and hyphens only
```

```
Error: Too many tags
Maximum: 10 tags per position
Current: 12 tags
```

---

# 11. Future Enhancements
- Authentication
- Real-time price updates (websockets)
- Advanced charts & visualizations
- Email/SMS notifications
- Export to CSV / PDF
- Multi-portfolio support
- Performance analytics dashboard
- **Full-text search in journal notes** ✅ NEW
- **Note edit history/versioning** ✅ NEW
- **Tag analytics (win rate by tag)** ✅ NEW
- **Collaborative journaling features** ✅ NEW

---

**Version:** 1.4  
**Last Updated:** February 14, 2026  
**Status:** Current
