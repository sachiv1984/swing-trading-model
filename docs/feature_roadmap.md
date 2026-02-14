l# Feature Roadmap - Momentum Trading Assistant

**Last Updated:** February 14, 2026  
**Current Version:** 1.4 (Analytics in progress)

---

## ✅ Completed Features (v1.0 - v1.4)

### Core Trading Features
- ✅ Portfolio management
- ✅ Manual position entry with fractional shares
- ✅ Daily position analysis
- ✅ ATR-based trailing stops
- ✅ Grace period (10 days, no stop loss)
- ✅ Market regime detection (SPY/FTSE vs 200-day MA)
- ✅ Multi-currency support (USD/GBP)
- ✅ Live price fetching from Yahoo Finance
- ✅ Fee calculation (UK: commission + stamp duty, US: FX fees)

### Dashboard & UI
- ✅ Responsive dashboard with draggable widgets
- ✅ Portfolio value display
- ✅ Open positions summary
- ✅ Total P&L tracking
- ✅ Cash balance management
- ✅ Dark mode UI

### Cash Management (v1.1)
- ✅ Deposit/withdrawal tracking
- ✅ Transaction history
- ✅ Accurate P&L accounting
- ✅ Cash management modal UI

### Portfolio History (v1.1)
- ✅ Daily portfolio snapshots
- ✅ Historical performance data
- ✅ Performance chart visualization
- ✅ Automated snapshot creation (cron)

### Exit Features (v1.2)
- ✅ Partial exit support (specify shares to exit)
- ✅ Custom exit date (backdate for reconciliation)
- ✅ User-provided exit price (actual broker execution)
- ✅ User-provided FX rate for US stocks (from broker statement)
- ✅ Exit reason selection dropdown
- ✅ Detailed fee breakdown in exit response
- ✅ Proportional cost basis calculation for partial exits

### Backend Architecture (v1.2)
- ✅ Complete refactoring to service layer architecture
- ✅ 67% code reduction in main.py (1,439 → 470 lines)
- ✅ 5 service modules (position, portfolio, trade, cash, signal)
- ✅ 100% testable business logic
- ✅ Clean separation of concerns (HTTP → Service → Utils → Database)

### System Health & Monitoring (v1.3)
- ✅ Health check endpoint (`GET /health`) for load balancers
- ✅ Detailed system status (`GET /health/detailed`)
- ✅ Automated endpoint testing (`POST /test/endpoints`)
- ✅ Frontend status dashboard page
- ✅ Real-time system health monitoring
- ✅ Component-level health checks (Database, Yahoo Finance, Services, Config)
- ✅ One-click endpoint testing with pass/fail results
- ✅ Auto-refresh capability (5-second intervals)
- ✅ Response time tracking
- ✅ 100% success rate monitoring

### Trade Journal & Notes System (v1.4)
- ✅ Entry notes when creating positions
- ✅ Exit notes when closing positions
- ✅ Tags system for categorizing trades
- ✅ Tag filtering in trade history
- ✅ Expandable trade rows showing full journal entries
- ✅ Tag autocomplete from existing tags
- ✅ Journal view mode in Positions page
- ✅ Visual entry/exit note cards with color-coded headers
- ✅ Strategy tag pills with gradient styling
- ✅ Database schema updates (entry_note, exit_note, tags fields)
- ✅ Backend endpoints for note/tag management
- ✅ Full-width journal display in trade history

### Technical Infrastructure
- ✅ PostgreSQL database
- ✅ FastAPI backend with clean architecture
- ✅ React frontend with TanStack Query
- ✅ Real-time FX rate conversion
- ✅ Error handling and validation
- ✅ Production deployment on Render
- ✅ GitHub Pages frontend hosting

---

## 🎯 Planned Features

### Priority 1: High Value, Essential for Trading

#### 1. Performance Analytics Page ⏳ IN PROGRESS
**Status:** In Progress (v1.4)  
**Effort:** Medium (3-4 days)  
**Value:** High

**Features:**
- Monthly/quarterly returns table
- Best/worst trades leaderboard
- Win rate by month chart
- Average profit vs average loss
- **Max drawdown tracking** (critical for risk management)
- **Underwater chart** (% drawdown from peak over time)
- Sharpe ratio calculation
- **R-multiple distribution chart** (strategy effectiveness)
- **Expectancy per trade** (edge validation)
- **Average R-multiple** (by tag, by outcome)

**Metrics to Display:**
- Total return %
- Annualized return
- **Max drawdown** (emphasize this)
- **Current drawdown** (prominent display)
- **Time underwater** (days from peak)
- Win rate (by month, quarter, year, tag)
- Average winner / Average loser
- Profit factor
- Expectancy per trade
- **R-multiple by tag** (which setups work best)

**API Endpoints:**
- `GET /analytics/summary` - Overall statistics
- `GET /analytics/monthly` - Monthly breakdown
- `GET /analytics/trades/best` - Top performers
- `GET /analytics/trades/worst` - Biggest losses
- `GET /analytics/drawdown` - Drawdown history
- `GET /analytics/r-multiples` - R-multiple distribution

---

#### 2. Position Sizing Calculator 🚀 PROMOTED TO P1
**Status:** Planned for v1.4  
**Effort:** Low (1-2 days)  
**Value:** **HIGH** (daily workflow improvement)

**Features:**
- Input: Risk per trade (% of portfolio)
- Input: Stop loss distance
- Output: Optimal share count
- **Integrated into position entry modal** (not separate page)
- Pre-populate shares field automatically
- Real-time calculation as user types
- Validates against available cash
- Shows warning if position would exceed cash

**Formula:**
```
Risk Amount = Portfolio Value × Risk %
Position Size = Risk Amount / Stop Distance
```

**Example:**
- Portfolio: £10,000
- Risk per trade: 2% = £200
- Stop distance: £5
- Position size: 40 shares
- Cost: 40 × £100 = £4,000

**UI Integration:**
- **Embedded widget in position entry modal**
- Shows: "To risk 2% (£200), buy X shares at £Y"
- Auto-fills shares field
- Updates live as entry price or stop changes
- Validates against available cash

**Why Promoted:**
- Daily value (used every time you enter a position)
- Prevents sizing errors
- Enforces risk discipline
- Quick to implement (1-2 days)

---

#### 3. Portfolio Heat Gauge ⭐ NEW - P1
**Status:** Planned for v1.4  
**Effort:** Low-Medium (2-3 days)  
**Value:** **HIGH** (risk management)

**Features:**
- Calculate total capital at risk across all positions
- Display as % of portfolio
- Color-coded risk indicator
- Shows risk per position
- Integrated into Position Sizing Calculator
- Dashboard widget showing current heat

**Calculation:**
```
For each open position:
  Position Risk = (Entry Price - Stop Price) × Shares

Total Portfolio Heat = Sum of all Position Risks / Portfolio Value
```

**Example:**
```
Position 1: £10k, stop at -5% = £500 risk
Position 2: £8k, stop at -8% = £640 risk
Position 3: £12k, stop at -3% = £360 risk

Total Heat = £1,500 / £50,000 = 3% portfolio heat
```

**UI Display:**

Dashboard Widget:
```
┌────────────────────────────────┐
│ Portfolio Heat                 │
├────────────────────────────────┤
│ [████████░░] 3.2%             │
│                                │
│ Total Risk: £1,600            │
│ If all stops hit: -3.2%       │
│                                │
│ 5 positions open              │
│ Max recommended: 10% heat      │
└────────────────────────────────┘
```

Position Entry Modal Integration:
```
Current heat: 3.2%
After adding position: 5.2% ✓ (safe)
```

**Color Coding:**
- 0-5%: Green (conservative)
- 5-10%: Yellow (moderate)
- 10-15%: Orange (aggressive)
- 15%+: Red (danger - too concentrated)

**API Endpoints:**
- `GET /portfolio/heat` - Current portfolio heat calculation
- Returns: total_heat_pct, positions_risk_breakdown, recommendations

**Why Added:**
- Critical for position sizing discipline
- Prevents overexposure
- Answers: "Can I add this position safely?"
- Complements Position Sizing Calculator perfectly

---

#### 4. Alerts & Notifications
**Status:** Planned for v1.4  
**Effort:** Medium-High (4-5 days)  
**Value:** High

**Features:**
- Email alerts for:
  - Stop loss hit
  - Position exits grace period ending (day 8-9 warning)
  - Market regime change (risk-off signal)
  - Daily portfolio summary
- SMS alerts (via Twilio) - optional
- In-app notifications
- Configurable alert preferences

**Database Changes:**
```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    user_id UUID,
    type VARCHAR(50),
    message TEXT,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP
);

CREATE TABLE alert_preferences (
    id UUID PRIMARY KEY,
    user_id UUID,
    email_enabled BOOLEAN DEFAULT true,
    sms_enabled BOOLEAN DEFAULT false,
    alert_types TEXT[]
);
```

**API Endpoints:**
- `GET /alerts` - Get unread alerts
- `POST /alerts/{id}/read` - Mark as read
- `GET /alerts/preferences` - Get alert settings
- `PUT /alerts/preferences` - Update alert settings

---

### Priority 2: Medium Value, Good ROI

#### 5. Export & Reporting
**Status:** Planned for v1.4  
**Effort:** Low-Medium (2-3 days)  
**Value:** Medium (tax necessity)

**Features:**
- Export trades to CSV (for taxes)
- Export portfolio snapshots to CSV
- Generate monthly PDF report
- Export performance metrics
- Tax loss harvesting report

**Export Formats:**
- CSV for Excel/Google Sheets
- PDF for sharing/printing
- JSON for backup

**API Endpoints:**
- `GET /exports/trades.csv` - Trade history CSV
- `GET /exports/portfolio.pdf` - Portfolio report PDF
- `GET /exports/tax-report` - Tax document

---

#### 6. Watchlist & Screening
**Status:** Planned for v1.4  
**Effort:** Medium (3-4 days)  
**Value:** Medium

**Features:**
- Add tickers to watchlist
- Monitor for entry signals
- Quick-add from watchlist to positions
- Price alerts on watchlist items
- Technical indicators on watchlist

**Database Changes:**
```sql
CREATE TABLE watchlist (
    id UUID PRIMARY KEY,
    user_id UUID,
    ticker VARCHAR(10),
    market VARCHAR(5),
    added_date DATE,
    notes TEXT,
    target_entry DECIMAL(10,2),
    target_stop DECIMAL(10,2)
);
```

**API Endpoints:**
- `GET /watchlist` - Get all watchlist items
- `POST /watchlist` - Add ticker
- `DELETE /watchlist/{ticker}` - Remove ticker
- `GET /watchlist/signals` - Check for entry signals

---

### Priority 3: Nice to Have (v2.0)

#### 7. Position Correlation Analysis
**Status:** Planned for v2.0  
**Effort:** High (5-6 days)  
**Value:** Medium

**Features:**
- Show correlation between positions
- Warn if portfolio too concentrated
- Diversification score
- Sector exposure breakdown

---

#### 8. Backtesting Module
**Status:** Planned for v2.0  
**Effort:** Very High (2-3 weeks)  
**Value:** High (for validation)

**Features:**
- Test strategy on historical data
- Compare different ATR multipliers
- Optimize parameters
- Walk-forward analysis

---

#### 9. Multi-Portfolio Support
**Status:** Planned for v2.0  
**Effort:** High (1 week)  
**Value:** Low (single user system)

**Features:**
- Multiple portfolios per user
- Paper trading portfolio
- Real money portfolio
- Switch between portfolios

---

#### 10. Mobile App
**Status:** Planned for v2.0  
**Effort:** Very High (4-6 weeks)  
**Value:** Medium

**Features:**
- React Native app
- Push notifications
- Quick position entry
- View-only dashboard

---

## 📊 Updated Feature Priority Matrix

| Feature | Effort | Value | Priority | Version | Status |
|---------|--------|-------|----------|---------|--------|
| ~~API Health & Status~~ | ~~Low~~ | ~~Very High~~ | ~~P1~~ | ✅ v1.3 | DONE |
| ~~Trade Journal~~ | ~~Medium~~ | ~~High~~ | ~~P1~~ | ✅ v1.4 | DONE |
| Performance Analytics | Medium | High | P1 | v1.4 | ⏳ IN PROGRESS |
| Position Sizing Calculator | Low | **High** | P1 | v1.4 | 🚀 PROMOTED |
| Portfolio Heat Gauge | Low-Med | **High** | P1 | v1.4 | ⭐ NEW |
| Alerts & Notifications | Medium-High | High | P1 | v1.4 | Planned |
| Export & Reporting | Low-Medium | Medium | P2 | v1.4 | Planned |
| Watchlist | Medium | Medium | P2 | v1.4 | Planned |
| Correlation Analysis | High | Medium | P3 | v2.0 | Deferred |
| Backtesting | Very High | High | P3 | v2.0 | Deferred |
| Multi-Portfolio | High | Low | P3 | v2.0 | Deferred |
| Mobile App | Very High | Medium | P3 | v2.0 | Deferred |

---

## 🎯 Updated Implementation Order

### Phase 1 (v1.4) - Q2 2026

1. ⏳ **Performance Analytics** (3-4 days) - **IN PROGRESS**
   - Finish current work
   - Emphasize R-multiples and drawdown tracking
   - Add underwater chart
   - R-multiple by tag analysis

2. 🚀 **Position Sizing Calculator** (1-2 days) - **DO NEXT**
   - Integrate into position entry modal
   - Auto-calculate optimal shares
   - Real-time validation

3. ⭐ **Portfolio Heat Gauge** (2-3 days)
   - Dashboard widget
   - Integration with Position Sizing
   - Risk warnings

4. **Alerts & Notifications** (4-5 days)
   - Stop hit alerts
   - Grace period warnings
   - Risk-off signals
   - Daily summaries

### Phase 2 (v1.4) - Q2 2026

5. **Export & Reporting** (2-3 days)
   - CSV export for taxes
   - PDF reports

6. **Watchlist** (3-4 days) - **OPTIONAL**
   - Can defer to v2.0 if time-constrained

### Phase 3 (v2.0) - Q3 2026
7. **Correlation Analysis** (5-6 days)
8. **Backtesting** (2-3 weeks) - If needed for validation

---

## 💡 Quick Wins (Can slot between major features)

### High Priority Quick Wins
1. ~~**API Health Check**~~ ✅ COMPLETED
2. ~~**Position notes field**~~ ✅ COMPLETED (Trade Journal v1.4)
3. **Slippage calculation** (1-2 hours) ⭐ NEW
   - Add to trade history table
   - Show: "Avg slippage: -0.12%"
   - Formula: (Fill Price - Market Price) / Market Price
4. **Current drawdown widget** (30 mins) ⭐ NEW
   - Dashboard display
   - "Drawdown: -8.2%, 12 days underwater"
5. **R-multiple column** in trade history (1 hour) ⭐ NEW

### Medium Priority Quick Wins
6. **Best/worst trades widget** - Add to dashboard
7. **Win rate chart** - Simple bar chart by month
8. **CSV export button** - Download trades as CSV
9. **Grace period indicator** - Visual countdown in UI
10. **Compliance metrics** (1 day) ⭐ NEW
    - Journal completion rate
    - Stop-based exit rate
    - Avg position size

### Lower Priority Quick Wins
11. **Daily email summary** - Cron job to send portfolio status
12. **FX rate history** - Track GBP/USD changes

---

## 🚫 Explicitly Out of Scope

- Automated trading / trade execution
- Broker API integration
- Real-time streaming prices
- Social/community features
- Strategy builder (drag-and-drop)
- Machine learning predictions
- Options trading support
- Futures trading support
- **Gap risk monitor** (not actionable for this strategy) ❌ NEW
- **Full compliance scoring system** (defer to v2.0 until more data) 🤔 NEW

---

## 📝 Decision Framework

When evaluating new features, ask:

1. **Does it help me make better trading decisions?**
   - Yes → High value
   - No → Low value

2. **Can I implement it in < 1 week?**
   - Yes → Quick win
   - No → Long-term project

3. **Does it require external dependencies?**
   - No → Preferred
   - Yes → Consider alternatives

4. **Will I use it daily/weekly?**
   - Yes → High priority
   - No → Low priority

---

## 🆕 Recent Changes

### In Progress (February 2026) ⏳
- ⏳ Performance Analytics Page
  - Adding R-multiple tracking
  - Emphasizing drawdown analysis
  - Underwater chart visualization

### Roadmap Updates (February 2026) 🔄
- 🚀 Promoted Position Sizing Calculator to P1 (from P2)
- ⭐ Added Portfolio Heat Gauge as new P1 feature
- ⭐ Added Slippage Tracking as quick win
- ⭐ Added Basic Compliance Metrics as quick win
- ❌ Removed Gap Risk Monitor (not actionable)
- 🤔 Deferred Full Compliance Score to v2.0

### Completed in v1.4 (February 2026)
- ✅ Trade Journal & Notes System
- ✅ Entry and exit note fields (500 char limit)
- ✅ Tag system with autocomplete
- ✅ Tag filtering in trade history
- ✅ Expandable trade rows with journal display
- ✅ Journal view mode in Positions page
- ✅ Full-width responsive journal cards
- ✅ Backend API endpoints (updateNote, updateTags, getTags)
- ✅ Database schema updates for notes and tags

### Completed in v1.3 (February 2026)
- ✅ API Health & Status Page
- ✅ Health check endpoint for load balancers
- ✅ Detailed system health monitoring
- ✅ Automated endpoint testing (11 endpoints)
- ✅ Frontend status dashboard with real-time monitoring
- ✅ Component-level health checks
- ✅ 100% test pass rate verification

### Completed in v1.2 (February 2026)
- ✅ Partial exit functionality
- ✅ Custom exit dates
- ✅ User-provided exit prices
- ✅ User-provided FX rates
- ✅ Exit reason tracking
- ✅ Detailed fee breakdowns
- ✅ Complete backend refactoring to service layer architecture
- ✅ 67% code reduction (1,439 → 470 lines)
- ✅ 5 production-ready service modules
- ✅ 100% testable business logic

---

## 📋 Summary of Key Changes

### Priority Changes
- **Position Sizing Calculator**: P2 → P1 (daily workflow value)
- **Portfolio Heat Gauge**: NEW P1 feature (risk management)

### New Features Added
- Portfolio Heat Gauge (P1)
- Slippage Tracking (Quick Win)
- Basic Compliance Metrics (Quick Win)
- Current Drawdown Widget (Quick Win)
- R-multiple Column (Quick Win)

### Features Removed/Deferred
- Gap Risk Monitor (removed - not actionable)
- Full Compliance Score (deferred to v2.0)

### Analytics Enhancements
- Emphasize R-multiple tracking
- Emphasize drawdown analysis
- Add underwater chart
- R-multiple by tag analysis

---

**Next Review:** May 2026  
**Current Focus:** Complete Analytics → Position Sizing → Portfolio Heat