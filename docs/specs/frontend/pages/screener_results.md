**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-23
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Schema reference:** docs/specs/screener_results_schema.md
**API contract:** docs/specs/api_contracts/screener_api_contract.md
**Strategy reference:** claude/strategy/strategy_rules.md §11

---

# screener_results.md — Screener Results Page

**Purpose:** The Screener Results page surfaces the output of the Arc 1 strategy-rules screener engine (DS-01). It shows which tickers currently pass the user's strategy filters, ranked by momentum signal strength. The page enables the user to review candidates and promote them to the watchlist.

**Implementation status:** DS-02 (page implementation) is deferred to v3.0. This spec is the UX prerequisite for DS-02 — authoritative before implementation begins.

---

## 1. Purpose and User Goals

Users should be able to:

- See which tickers pass their strategy filters right now (regime gate, ATR gate, signal gate)
- Understand why a ticker passes (regime status, ATR, signal score)
- See sector/industry context for concentration awareness
- Check recent news headlines for each candidate (display-only)
- Understand how fresh the results are and trigger a manual refresh
- Promote a candidate to the watchlist for deeper research (DS-07)

---

## 2. Navigation and Route

- Top-level nav item: **"Screener"**
- Route: `/screener`
- Page title: **"Screener"**

---

## 3. API Reference

- `GET /screener/results` — fetch screener result records (paginated)
- `POST /screener/run` — trigger a new screener run
- Canonical contract: `docs/specs/api_contracts/screener_api_contract.md`
- Schema: `docs/specs/screener_results_schema.md`

---

## 4. Column Layout

The screener results are displayed in a table/list with the following columns:

| Column | Field | Description |
|--------|-------|-------------|
| Ticker | `ticker` | Ticker symbol |
| Market | `market` | US or UK |
| Price | `price` | Last close price in `currency` |
| ATR | `atr` | 14-day ATR. Displayed with currency suffix (e.g. `$18.50` or `£0.85`) |
| Regime | `regime_status` | `risk_on` → green chip "Risk On"; `risk_off` → red chip "Risk Off" |
| Signal | `signal_score` | Numeric score 0.0–1.0 displayed as percentage or bar indicator |
| Sector | `sector` | Sector classification text (or em dash `—` if null) |
| Entry Zone | `proximity_to_entry_zone` | Displayed as "Near entry" / "In zone" / "—" based on proximity value |
| News | `news_headline_count` | Headline count badge (e.g. "3") clicking expands inline panel |

**Column ordering is fixed.** The frontend must not reorder columns without a spec update.

**Responsive behaviour:** On mobile viewport (<768px), hide the Sector and Entry Zone columns. Show Ticker, Price, Signal, and a "Details" expand.

---

## 5. Sort and Filter Controls

### 5.1 Sort

Default sort: `signal_score` descending. This matches the API's default order.

User-selectable sort columns:
- Signal Score (default, descending)
- Price (ascending or descending)
- ATR (ascending or descending)

Sort state is not persisted across page refreshes.

### 5.2 Filter Controls

| Filter | Type | Options |
|--------|------|---------|
| Market | Segmented button | All / US / UK |
| Regime | Toggle | Show all / Risk-On only |
| Sector | Dropdown multiselect | All sectors + individual sector values from current result set |

Filter state is not persisted across page refreshes.

---

## 6. Data Freshness Indicator

The screener results page must show the user how fresh the data is.

**Freshness badge:**
- Location: top-right of results section, below the page header
- Format: "Last screened: [relative time]" (e.g. "Last screened: 12 minutes ago")
- Derived from: `run_timestamp` field from `GET /screener/results` response
- If no run has completed: show "No screener run yet"

**Manual refresh trigger:**
- A "Refresh" button adjacent to the freshness badge
- Clicking triggers `POST /screener/run`
- While a run is in progress: button shows "Scanning..." with a spinner; button is disabled
- On run completion (poll `GET /screener/results?run_id={run_id}`): results table updates; freshness badge updates
- On error: show inline error message "Screener run failed — try again"

**Polling behaviour:** After triggering `POST /screener/run`, the frontend polls `GET /screener/results?run_id={run_id}` every 5 seconds until the run appears in results. Maximum 60 seconds of polling; show error message on timeout.

---

## 7. Empty States

The screener results page must handle all empty states gracefully:

| Condition | Display |
|-----------|---------|
| No screener runs yet | Full-page empty state: "No screener results yet. Run your first screen." + Scan button |
| All tickers filtered (post-filter) | In-table empty state: "No tickers match your current filters. Adjust filters to see results." |
| No tickers pass strategy gates | Full-page empty state: "No tickers pass your current strategy filters. This may indicate a risk-off market regime." + link to Strategy Settings |
| No Alpaca data available (US tickers) | Inline data-source warning banner: "US market data using Yahoo Finance fallback — Alpaca data temporarily unavailable." Show results using fallback data |
| Stale data (last run >24 hours ago) | Yellow warning badge: "Results may be stale — last screened [time]" + Refresh button |

---

## 8. Watchlist Promotion Confirmation Flow (DS-07 interaction)

When the user clicks "Add to Watchlist" on a screener result row:

1. Show an inline confirmation popover (not a full modal) with:
   - Ticker and price pre-populated
   - Target entry price field (optional, pre-populated with screener price)
   - Notes field (optional)
   - "Add to Watchlist" confirm button
   - "Cancel" dismiss

2. On confirm: call `POST /watchlist` with ticker and optional target/notes

3. On success: row shows "Added ✓" chip; "Add to Watchlist" button becomes disabled for that row in the current session

4. On error: show inline error "Could not add to watchlist — try again"

**One-click scenario:** If the user has previously disabled confirmation (user preference setting, future scope), the confirmation popover is skipped. This preference is not in scope for v2.9 spec — document as a future enhancement.

---

## 9. News Panel (DS-06 Integration)

Each result row has a news headline count badge. Clicking the badge expands an inline news panel for that ticker.

**Expanded news panel:**
- Shows up to 10 recent headlines (from `news_headlines` array)
- Each headline: headline text + publication date (relative time, e.g. "2 hours ago")
- Source name displayed if available (`source` field)
- No sentiment labels, no sentiment scores, no advisory text — display-only per BLG-GOV-16 §13 review
- "Close" link at bottom of panel to collapse

**Empty state:** "No recent news available for [ticker]."

**UK tickers:** No Alpaca news data. Hide the news badge entirely for UK tickers (do not show a 0 badge).

---

## 10. Progressive Loading Pattern (Skeleton UI)

While `GET /screener/results` is loading:

1. Show the column header row with filter/sort controls (non-interactive, greyed out)
2. Show 8 skeleton rows — each row shows animated shimmer for ticker, price, ATR, signal, sector columns
3. Do not show "No results" state until response has been received

On response:
- Replace skeleton rows with real data
- Activate filter/sort controls

---

## 11. AC Coverage Summary (DS-02 Interaction Patterns)

This spec covers all DS-02 interaction patterns:

| DS-02 Interaction | Spec section |
|-------------------|-------------|
| Column layout | §4 |
| Sort/filter controls | §5 |
| Data freshness indicator | §6 |
| Manual refresh trigger | §6 |
| Empty states | §7 |
| Watchlist promotion flow | §8 |
| News panel | §9 |
| Skeleton/progressive loading | §10 |

---

## DoQ Sign-Off

- [x] Column layout, sort/filter controls, and candidate card design documented
- [x] Data freshness indicator specified (last updated timestamp + manual refresh trigger)
- [x] Empty states documented (no results, no market data, stale data)
- [x] Watchlist promotion confirmation flow documented
- [x] Progressive loading (skeleton UI) specified
- [x] All DS-02 interaction patterns covered
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-04-23
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable, no frontend implementation, engine signer populated). DS-02 implementation deferred to v3.0; this spec is the prerequisite.
