# User Guide — A Day in the Life of a Swing Trader

This guide walks through how a typical trading day flows inside the system — from the morning market check to closing the session. Every section maps to a real screen you can navigate to.

---

## Morning — Before the Market Opens

### 1. Start at Home

Open the app. The **Home** screen gives you an at-a-glance snapshot of where things stand:

- **Open Positions** — how many positions you currently hold
- **Portfolio Heat** — the percentage of your portfolio at risk right now (your stop-loss exposure)
- **Grace Period** — any positions in their first 10 days (handled with extra care)
- **Signal Status** — whether new momentum signals are waiting for you
- **Recent Activity** — latest trades and changes logged

If anything looks off — a position hit its stop overnight, heat is unusually high — you know immediately.

---

### 2. Check Your Risk Dashboard

Navigate to **Analytics → Risk Dashboard**.

This is your morning health check:

- **Portfolio Heat Gauge** — is your total risk within your target band (typically under 20%)?
- **Drawdown Summary** — how far are you from your peak portfolio value?
- **Grace Period Panel** — which positions need careful handling today?
- **Position Risk Table** — per-position breakdown of current stop-loss exposure
- **Prospective Heat** — if all open positions move against you to their stops simultaneously, what does your heat look like?

If heat is too high before the market opens, you know to look for positions to reduce before trading.

---

### 3. Review Your Positions

Navigate to **Trading → Positions**.

For each open position, you can see:

- Current lifecycle state: **GRACE** (< 10 days), **LOSING**, **PROFITABLE**, **EXIT ZONE**
- Whether an earnings announcement is approaching (earns date warning)
- Notes you wrote when you entered the trade

This is the moment to ask: *are any of these approaching my exit criteria?* If a position is in the EXIT ZONE, it may be time to act today.

---

### 4. Review Active Signals

Navigate to **Analytics → Signals**.

The system shows you the top momentum signals ranked by strength. Each signal card shows:

- The stock ticker and market (US or UK)
- Signal rank and strength score
- A suggested entry point

You can filter by market (All / US / UK) and configure the lookback period (default is 252 trading days — one year). Signals that are old or that you've already reviewed can be dismissed.

If a signal looks interesting, you don't act on it yet — first, you do research.

---

## Mid-Morning — Research and Planning

### 5. Research a Signal

Navigate to **Tools → Watchlist** and find the stock, or click through from the Signals page.

From the Watchlist, click **Research** on any entry to open the Research View. This aggregates:

- Current price and technicals
- Sector context
- Recent news
- Screener results for this stock

Read the news. Understand the setup. If the stock passes your criteria, you move to planning.

---

### 6. Create a Trade Plan

Navigate to **Trading → Trade Plans**, then click **New Trade Plan**.

A trade plan is your pre-commitment document. Fill in:

- **Ticker and market**
- **Setup thesis** — why does this trade make sense?
- **Entry rationale** — what specific condition triggers your entry?
- **Regime context** — what is the broader market doing?
- **R-target** — what is your profit target in R-multiples?
- **Early exit conditions** — what would make you abandon the trade before it triggers?
- **Confirmation criteria** — what must you see before pressing the button?
- **Pre-entry checklist** — use the built-in checklist to verify you've covered your bases

The plan status starts as **Draft** and progresses: *Research Pending → Research Complete → Entry Ready → Active*.

You should not enter a trade without a plan. The plan is your defence against impulse.

---

### 7. Run the Screener (Weekly or as Needed)

Navigate to **Tools → Screener**.

The screener scans your ticker universe against fundamental and technical criteria. Click **Run Screener** to trigger a fresh run (it runs asynchronously — results appear when complete).

Use screener results to:

- Discover stocks that meet your base criteria
- Add promising tickers to your Watchlist for further research
- Filter by US or UK markets

The screener is not a buy signal — it is a candidate list.

---

## When the Market Opens — Trade Execution

### 8. Enter a Trade

When a plan reaches **Entry Ready** status and your entry condition triggers, navigate to **Trading → Trade Entry**.

Fill in:

- **Ticker and market** (US or UK)
- **Entry date**
- **Shares, entry price, fill price**
- **Stop price** — your loss limit
- **ATR value** — the stock's average true range (used for stop calculations)
- **FX rate** — for UK trades in GBP
- **Entry note/thesis** — a brief summary of why you entered right now
- **Tags** — categorise the trade for later analysis (e.g. `momentum`, `breakout`, `earnings-play`)

The **Position Sizing Widget** calculates your recommended position size based on your account size, risk percentage per trade, and the distance to your stop. Use it — do not size by feel.

If you created a Trade Plan, link the trade to it here.

Once submitted, the position appears in **Positions** with a **GRACE** badge for the first 10 days.

---

## During the Day — Monitoring

### 9. Monitor Open Positions

Positions don't need constant watching — that is the point of having a stop. But you should check in periodically.

From **Trading → Positions**, look for:

- **EXIT ZONE** badges — the position has reached your target area
- **Earnings date warnings** — an announcement is approaching; you may want to reduce size or exit before it
- **LOSING** state with grace period expired — time to reassess

You can add journal notes to any position at any time.

---

### 10. Check Notifications

Navigate to **Alerts → Notifications** (the bell icon shows a badge count when you have unread alerts).

The alert system fires automatically when:

- A position's stop loss is approaching
- A grace period is ending
- The market regime changes
- Your daily portfolio summary is ready

Mark alerts as read once you've reviewed them. You can configure which alert types you receive and set custom thresholds in **Notification Preferences**.

---

## Closing the Session — Exits and Review

### 11. Exit a Position

When your exit condition is met (price target, stop hit, rule-based exit), go to **Trading → Positions**, find the position, and click **Exit**.

Confirm the exit with:

- Exit date
- Exit price
- Exit reason: **STOP**, **MANUAL**, **TARGET**, or **REGIME**

After exit, the system prompts you to complete a **Trade Reflection**.

---

### 12. Complete a Trade Reflection

This is non-optional if you want to improve.

The reflection captures:

- What worked and what didn't
- Whether you followed your plan
- What you'd do differently

Reflections are stored and searchable from **Trading → Reflections**. Over time, patterns emerge — you'll see which setups produce your best R-multiples and which you consistently mismanage.

---

## End of Week — Performance Review

### 13. Weekly Digest

Navigate to **Analytics → Weekly Digest**.

This gives you the 7-day summary:

- Realised P&L
- Unrealised P&L delta
- Alerts fired and dismissed
- Compliance score — how well did you follow your own rules?

Use this to calibrate the next week, not to celebrate or punish yourself.

---

### 14. Performance Analytics

Navigate to **Analytics → Analytics** for the deeper view.

Choose your time period (7 days, 1 month, 1 quarter, 1 year, all-time) and review:

- **Win rate, profit factor, Sharpe ratio**
- **R-multiple distribution** — are your wins meaningfully larger than your losses?
- **Monthly heatmap** — are you consistent across months or volatile?
- **Exit reason breakdown** — are most exits at your stop, or at target?
- **Tag performance** — which trade categories perform best?
- **Discipline compliance metrics** — are you following your rules?

This is where patterns become visible. A win rate of 40% with a 2:1 average win-to-loss ratio is profitable. A win rate of 60% with a 0.8:1 ratio is not.

---

### 15. Tax Report (End of Tax Year)

Navigate to **Analytics → Reports**.

Select the tax year and generate a report in PDF or CSV format. The report shows every trade in the year with entry/exit dates, prices, and P&L — ready to hand to an accountant or file with HMRC.

UK tax year runs **6 April to 5 April**.

---

## Configuration — Set It Once, Review Occasionally

### Settings

Navigate to **System → Settings**.

Key parameters to configure when you first start:

| Setting | What It Controls |
|---|---|
| Default risk % per trade | Drives the position sizing calculator |
| ATR multiplier (initial) | Sets your initial stop distance |
| ATR multiplier (trailing) | Sets your trailing stop distance |
| ATR period | Lookback for ATR calculation |
| Min hold days | Minimum days before a position can exit (grace period) |
| UK / US commission | Used in P&L calculations |
| Stamp duty | Applied to UK trades automatically |
| FX fee rate | Applied to currency conversion on UK trades |

These values underpin every sizing and P&L calculation in the system. Set them correctly and leave them alone unless your rules change.

---

## Quick Reference — Where to Go for What

| I want to… | Go to… |
|---|---|
| See my current risk exposure | Risk Dashboard |
| Find new trade ideas | Signals, Screener, Watchlist |
| Research a specific stock | Watchlist → Research |
| Document a trade before entry | Trade Plans |
| Enter a trade | Trade Entry |
| Check my open positions | Positions |
| Exit a trade | Positions → Exit |
| Review past trades | Trade History |
| Read my reflections | Reflections |
| See overall performance | Performance Analytics |
| Get my weekly summary | Weekly Digest |
| Download my tax report | Reports |
| Manage alerts | Notifications / Notification Preferences |
| Change trading parameters | Settings |
| Check the system is working | System Status |
