**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-14
**Cycle:** 2026-05-14__release-v3.4
**Source:** BLG-FE-22 (ST-12)
**Related specs:** docs/specs/frontend/pages/screener_results.md; docs/specs/frontend/pages/watchlist.md; docs/specs/frontend/pages/pre_trade_research.md
**Signed off by:** Frontend Specifications & UX Documentation Owner
**Sign-off date:** 2026-05-14

---

# Screener Morning Routine — UX Workflow Spec

**Purpose:** Define the step-by-step user workflow for the Arc 1 morning screening routine: from screener results through shortlisting to watchlist promotion and pre-trade research navigation. Specifies what data carries between views and how the user moves across pages.

---

## 1. Routine Overview

The morning routine is a 4-step workflow:

```
Step 1: Review screener results         /screener
Step 2: Shortlist candidates            (in-screener, filter + sort)
Step 3: Promote to watchlist            /screener → POST /watchlist
Step 4: Navigate to pre-trade research  /watchlist → /research/{ticker}
```

The user moves through these steps sequentially in a single session. No page requires a manual reload between steps — state carries via React navigation.

---

## 2. Step-by-Step Workflow

### Step 1 — Review Screener Results

**Entry point:** User navigates to `/screener` from the sidebar nav.

**Initial state:** Page loads the most recent screener results via `GET /screener/results`. The freshness badge (§6 of `screener_results.md`) shows when the last run completed.

**First-time scenario:** If no screener run has been completed, the empty state displays with a "Scan" button. User clicks Scan → `POST /screener/run` → polling begins → results populate on completion.

**Data visible at this step:**

| Column | Field | Purpose in morning routine |
|--------|-------|---------------------------|
| Ticker | `ticker` | Identifies the candidate |
| Price | `price` | Current price context |
| ATR | `atr` | Position sizing reference |
| Regime | `regime_status` | Quick pass/fail signal |
| Signal | `signal_score` | Ranking and urgency |
| Sector | `sector` | Concentration awareness |
| Entry Zone | `proximity_to_entry_zone` | Immediate opportunity flag |
| News badge | `news_headline_count` | Material event check |

---

### Step 2 — Shortlist Candidates

**Action:** User applies filters and sort controls within the screener page to reduce the list to actionable candidates.

**Recommended workflow sequence:**

1. Apply regime filter: "Risk-On only" — removes risk-off tickers
2. Review signal_score order (default descending) — highest momentum first
3. Check Entry Zone column — candidates "In zone" or "Near entry" are prioritised
4. Expand news panel for any candidate with ≥1 headline — quick material event scan
5. Optionally filter by sector if portfolio concentration is near threshold

**Shortlist result:** The user has a mental (or on-screen) list of 1–5 candidates to research further. No shortlist data structure is persisted server-side — the screener results page acts as a live shortlist view.

**Future scope (not in this spec):** A persistent session shortlist or "pin" mechanism is a candidate for a future sprint.

---

### Step 3 — Promote to Watchlist

**Trigger:** User clicks "Add to Watchlist" on a screener result row for a prioritised candidate.

**Confirmation flow:** Per `screener_results.md` §8:
1. Inline confirmation popover opens with ticker and price pre-populated
2. Optional: target entry price (pre-filled from screener price), notes
3. User clicks "Add to Watchlist" → `POST /watchlist` call
4. On success: row shows "Added ✓"; button disabled for session
5. On error: inline error message; user can retry

**Data carried from screener to watchlist record:**

| Screener field | Watchlist field | Carried? |
|---------------|-----------------|---------|
| `ticker` | `ticker` | Yes — always |
| `price` | `target_entry_price` | Yes — pre-populated in popover (editable) |
| `market` | `market` | Yes — implicitly from ticker suffix (.L = UK) |
| `sector` | *(not stored in watchlist)* | No — sector fetched on demand via research endpoint |
| `signal_score` | *(not stored)* | No — signal re-fetched when watchlist loads |
| `notes` | `notes` | Optional — user-authored in popover |

**Bulk promotion:** Not in scope for this spec. One-at-a-time promotion via inline popover is the canonical flow.

---

### Step 4 — Navigate to Pre-Trade Research

**Entry point for research:** User navigates to `/watchlist`, finds the promoted ticker, and clicks the Research button/link.

**Navigation path:**

```
/screener → Add to Watchlist → /watchlist → Research button → /research/{ticker}
```

Alternative fast-path from screener: The screener results table includes a "Research" link per row (per `screener_results.md` §4 Actions column). This navigates directly to `/research/{ticker}` without requiring watchlist promotion first.

**Navigation implementation:**

```js
// From screener row
navigate(`/research/${ticker}`);

// From watchlist row
navigate(`/research/${ticker}`);
```

Both use the same route. No additional query parameters needed.

---

## 3. Information Carry Across Views

### Screener → Research View

When the user navigates from the screener to `/research/{ticker}`, the research page fetches independently via `GET /research/{ticker}`. No screener data is passed via props or URL params.

**Data visible in both views (re-fetched independently):**

| Data item | Screener source | Research view source |
|-----------|-----------------|---------------------|
| Current price | `screener.price` | `research.price` |
| ATR (14d) | `screener.atr` | `research.signal.atr` |
| Momentum signal | `screener.regime_status` + `signal_score` | `research.signal.status` |
| Sector | `screener.sector` | `research.sector.sector` |
| News headlines | Expanded inline panel | `research.news_headlines` (up to 5) |

**Consistency note:** Price and ATR may differ between screener and research views if the screener run is older than the research data. The research view's freshness indicator (`Updated X ago`) signals this to the user.

**Data only in screener:** `signal_score` (numeric), `proximity_to_entry_zone`, `regime_status` enum.

**Data only in research view:** `market_cap`, `price_change_pct`, prospective heat (if signal has entry/stop prices), trade plan context (linked plans), full news list.

---

### Watchlist → Research View

The watchlist stores `ticker`, `target_entry_price`, `notes`, and research status indicator (ST-09, EPIC-03). None of these are passed to the research view — research always fetches from the API fresh.

---

## 4. Navigation Model

```
Sidebar
  ├── Screener (/screener)
  │     ├── Inline: Add to Watchlist [POST /watchlist]
  │     └── Research link → /research/{ticker}
  ├── Watchlist (/watchlist)
  │     └── Research button → /research/{ticker}
  └── Research (/research/:ticker)
        └── Back button → navigate(-1) [browser history]
```

**Back navigation:** The research page uses `navigate(-1)` (browser back). This returns the user to wherever they came from — screener or watchlist — without requiring explicit state management.

**No circular loops:** Research does not link back to screener. The user uses the browser back button or sidebar nav to return.

---

## 5. Error and Edge Cases

| Scenario | Behaviour |
|----------|-----------|
| Ticker promoted to watchlist but research API returns 404 | Research page shows error state with "Unable to load research data" + Retry button |
| Screener results stale (>24h) | Yellow warning badge on screener; user proceeds with stale data at their discretion |
| Ticker already on watchlist | "Add to Watchlist" popover: if `POST /watchlist` returns 409 Conflict, show "Already on watchlist" message; do not duplicate |
| No trade plan for ticker | Research page Trade Plan panel shows "No trade plan — Create Trade Plan" button navigating to `/TradePlan?ticker={ticker}` |

---

## 6. Out of Scope

- Wireframes or visual mockups (workflow spec only — see design gate deliverables for mockups)
- Session shortlist / pin mechanism (future sprint)
- Bulk watchlist promotion
- Screener result sharing or export
