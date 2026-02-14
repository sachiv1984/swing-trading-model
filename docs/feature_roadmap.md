# Feature Roadmap - Momentum Trading Assistant

**Last Updated:** February 14, 2026  
**Current Version:** 1.4

---

## ✅ Completed Features (v1.0 - v1.3)

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

### Trade Journal & Notes System (v1.4) ⭐ NEW
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

### Priority 1: High Value, Quick Wins

#### 1. Performance Analytics Page
**Status:** Planned for v1.4  
**Effort:** Medium (3-4 days)  
**Value:** High

**Features:**
- Monthly/quarterly returns table
- Best/worst trades leaderboard
- Win rate by month chart
- Average profit vs average loss
- Max drawdown tracking
- Sharpe ratio calculation
- R-multiple distribution chart

**Metrics to Display:**
- Total return %
- Annualized return
- Max drawdown
- Win rate (by month, quarter, year)
- Average winner / Average loser
- Profit factor
- Expectancy per trade

**API Endpoints:**
- `GET /analytics/summary` - Overall statistics
- `GET /analytics/monthly` - Monthly breakdown
- `GET /analytics/trades/best` - Top performers
- `GET /analytics/trades/worst` - Biggest losses
- `GET /analytics/drawdown` - Drawdown history

---

#### 2. Alerts & Notifications
**Status:** Planned for v1.4  
**Effort:** Medium-High (4-5 days)  
**Value:** High

**Features:**
- Email alerts for:
  - Stop loss hit
  - Position exits grace period
  - Market regime change
  - Daily summary report
- SMS alerts (via Twilio)
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

#### 3. Position Sizing Calculator
**Status:** Planned for v1.4  
**Effort:** Low (1-2 days)  
**Value:** Medium

**Features:**
- Input: Risk per trade (% of portfolio)
- Input: Stop loss distance
- Output: Optimal share count
- Visual risk calculator in UI
- Pre-populate position entry form

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

**UI Integration:**
- Widget on position entry page
- Shows: "To risk 2% (£200), buy X shares at £Y"
- Validates against available cash

---

#### 4. Watchlist & Screening
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

#### 5. Export & Reporting
**Status:** Planned for v1.4  
**Effort:** Low-Medium (2-3 days)  
**Value:** Medium

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

### Priority 3: Nice to Have

#### 6. Position Correlation Analysis
**Status:** Planned for v2.0  
**Effort:** High (5-6 days)  
**Value:** Medium

**Features:**
- Show correlation between positions
- Warn if portfolio too concentrated
- Diversification score
- Sector exposure breakdown

---

#### 7. Backtesting Module
**Status:** Planned for v2.0  
**Effort:** Very High (2-3 weeks)  
**Value:** High (for validation)

**Features:**
- Test strategy on historical data
- Compare different ATR multipliers
- Optimize parameters
- Walk-forward analysis

---

#### 8. Multi-Portfolio Support
**Status:** Planned for v2.0  
**Effort:** High (1 week)  
**Value:** Low (single user system)

**Features:**
- Multiple portfolios per user
- Paper trading portfolio
- Real money portfolio
- Switch between portfolios

---

#### 9. Mobile App
**Status:** Planned for v2.0  
**Effort:** Very High (4-6 weeks)  
**Value:** Medium

**Features:**
- React Native app
- Push notifications
- Quick position entry
- View-only dashboard

---

## 📊 Feature Priority Matrix

| Feature | Effort | Value | Priority | Version |
|---------|--------|-------|----------|---------|
| ~~API Health & Status Page~~ | ~~Low~~ | ~~Very High~~ | ~~P1~~ | ✅ v1.3 |
| ~~Trade Journal~~ | ~~Medium~~ | ~~High~~ | ~~P1~~ | ✅ v1.4 |
| Performance Analytics | Medium | High | P1 | v1.4 |
| Alerts & Notifications | Medium-High | High | P1 | v1.4 |
| Position Sizing | Low | Medium | P2 | v1.4 |
| Watchlist | Medium | Medium | P2 | v1.4 |
| Export & Reporting | Low-Medium | Medium | P2 | v1.4 |
| Correlation Analysis | High | Medium | P3 | v2.0 |
| Backtesting | Very High | High | P3 | v2.0 |
| Multi-Portfolio | High | Low | P3 | v2.0 |
| Mobile App | Very High | Medium | P3 | v2.0 |

---

## 🎯 Recommended Implementation Order

### Phase 1 (v1.4) - Q2 2026

1. **Performance Analytics** (3-4 days)
   - Understand what's working
   - Data already available
   - Visual insights

2. **Alerts & Notifications** (4-5 days)
   - Stay informed without checking constantly
   - Professional feature
   - Good user experience

### Phase 2 (v1.4) - Q2 2026

4. **Position Sizing Calculator** (1-2 days)
   - Quick win
   - Improves risk management
   - Easy to implement

5. **Export & Reporting** (2-3 days)
   - Practical necessity (taxes)
   - Low effort
   - High utility

6. **Watchlist & Screening** (3-4 days)

### Phase 3 (v2.0) - Q3 2026
7. **Correlation Analysis** (5-6 days)
8. Consider **Backtesting** if needed for validation

---

## 💡 Quick Wins (Can be done in 1-2 days each)

1. ~~**API Health Check**~~ ✅ COMPLETED
2. ~~**Position notes field**~~ ✅ COMPLETED (Trade Journal v1.4)
3. **Best/worst trades widget** - Add to dashboard
4. **Win rate chart** - Simple bar chart by month
5. **CSV export button** - Download trades as CSV
6. **Daily email summary** - Cron job to send portfolio status
7. **Stop loss alert** - Email when stop is hit
8. **Grace period indicator** - Visual countdown in UI
9. **FX rate history** - Track GBP/USD changes

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

### Completed in v1.4 (February 2026) ⭐ NEW
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

**Next Review:** May 2026
