**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.2
**Last Updated:** 2026-05-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-05-05__release-v3.2/pre-trade-research-view/ux_spec.md
**Design Source (v0.2 quality score):** docs/design/2026-05-18__release-v3.7/quality-score-display/ux_spec.md
**API contracts:** docs/specs/api_contracts/research_endpoints.md; docs/specs/api_contracts/portfolio_api_contract.md

---

# pre_trade_research.md — Pre-Trade Research View

**Purpose:** The Pre-Trade Research View surfaces research data for a specific ticker to support the pre-trade decision process. It consolidates momentum signal status, ATR, current price, prospective portfolio heat, trade plan context, and recent news in a single focused view. Introduced in v3.2 (Arc 2, PT-02 + PT-03).

---

## 1. Purpose and User Goals

Users should be able to:

- Review momentum signal status, ATR, and current price for a candidate ticker
- See what adding this ticker at entry would do to portfolio heat (prospective heat)
- Check or create a trade plan for the ticker without leaving the research context
- Read recent news headlines before committing to a trade plan

---

## 2. Navigation and Route

- Route: `/research/{ticker}`
- Ticker in path (uppercase for US, with `.L` suffix for UK tickers, e.g. `/research/AAPL`, `/research/BARC.L`)
- URL is shareable and bookmarkable
- Page title: **"{TICKER} — Research"**
- Back navigation: `← Back` (browser back — returns to referring screener or watchlist page)

---

## 3. API Reference

| Endpoint | Purpose |
|----------|---------|
| `GET /research/{ticker}` | Ticker fundamentals, momentum signal, ATR, price, news headlines |
| `GET /portfolio/prospective-heat?ticker={ticker}&quantity={n}` | Prospective heat if position entered |
| `GET /trade-plans?ticker={ticker}` | Fetch trade plan(s) for the researched ticker |

Canonical contracts:
- Research: `docs/specs/api_contracts/research_endpoints.md`
- Portfolio heat: `docs/specs/api_contracts/portfolio_api_contract.md`
- Trade plans: `docs/specs/api_contracts/trade_plan_endpoints.md`

---

## 4. Page Header

| Element | Source | Notes |
|---------|--------|-------|
| Ticker symbol | URL path param | Uppercase, large |
| Company name | `GET /research/{ticker}` → `name` | Subtitle |
| Sector | `GET /research/{ticker}` → `sector` | `—` if null |
| Market cap | `GET /research/{ticker}` → `market_cap` | Formatted (e.g. `$3.2T`); `—` if null |
| Last updated | API response timestamp | Relative time (e.g. "2m ago") |

---

## 5. Price and Signal Region

| Element | Source | Display |
|---------|--------|---------|
| Current price | `GET /research/{ticker}` → `price` | Native currency |
| Price change | `GET /research/{ticker}` → `price_change_pct` | `▲ +X.X%` (green) or `▼ -X.X%` (red) |
| Momentum signal status | `GET /research/{ticker}` → `signal_status` | Badge: `Active` (green) / `Watch` (amber) / `No Signal` (grey) — same badge conventions as watchlist |
| ATR (14d) | `GET /research/{ticker}` → `atr` | Currency-formatted (e.g. `$4.20` or `£0.85`) |
| Setup Quality Score *(v3.7, conditional EPIC-02 gate)* | `GET /trade-plans/{id}/quality-score` for most recent active/draft plan for this ticker | `{N}/100` or "N/A — insufficient history"; sub-label "Based on your trade history" (muted); omitted entirely if no trade plan exists for ticker |

**Setup Quality Score note (§13 compliance):** Display-only, labelled as historical reference. Not a prediction. If the EPIC-02 gate (20+ closed trades) is not confirmed, this row is omitted.

---

## 6. Prospective Heat at Entry Region

Calls `GET /portfolio/prospective-heat` with `ticker` and `quantity=1` (default minimum quantity).

| Element | Display |
|---------|---------|
| Current portfolio heat | Current heat percentage |
| Prospective heat if entered | Heat estimate with new position; colour-coded: green (<15%), amber (15–25%), red (>25%) |
| Label | "Prospective heat at entry" (explicit label) |

**Unavailable state:** If the endpoint returns an error, display "N/A" for the prospective heat value. Do not block the rest of the page.

---

## 7. Trade Plan Context Panel

Conditional display based on whether a plan exists for the ticker.

### 7.1 Plan exists (active or draft)

Data source: `GET /trade-plans?ticker={ticker}` — use the most recent active or draft plan.

| Element | Display |
|---------|---------|
| Status badge | Plan status (consistent with trade plan list conventions) |
| Stop level | Currency-formatted; `—` if null |
| Notes summary | First 100 characters of `risk_reward_notes`; truncated with "…" if longer |
| "View full plan" link | Links to `/trade-plans/{id}` |

Panel is read-only — no inline editing.

### 7.2 No plan exists

- Body: "No trade plan for {TICKER}."
- CTA: **"Create Trade Plan"** button — links to `/trade-plans/new?ticker={ticker}`

---

## 8. Recent News Region

| Element | Display |
|---------|---------|
| Headlines | Up to 5 headlines from `GET /research/{ticker}` → `news_headlines` |
| Per headline | Headline text + source name + relative timestamp |
| Empty state | "No recent news available." |

No sentiment labels or scores.

---

## 9. States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton placeholders for all four regions; page header visible immediately |
| Error (research endpoint) | Full-page error: "Unable to load research data. Please try again." + Retry button |
| Partial error (prospective heat) | "N/A" in heat region; rest of page renders normally |
| Partial error (trade plans) | Show "Create Trade Plan" CTA; do not block page |

---

## DoQ Sign-Off

- [x] Route and navigation model specified
- [x] All four page regions documented (price/signal, prospective heat, trade plan, news)
- [x] Colour conventions for heat aligned with existing conventions
- [x] All loading, error, and empty states specified
- [x] API references listed
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-05-05
- Comments: Autonomous class sign-off — design source approved by Product Owner 2026-05-05; all AC items code-review-verifiable.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.2 | 2026-05-18 | v3.7 design gate — added Setup Quality Score row to §5 Price and Signal Region (PT-04: conditional on EPIC-02 gate; shown if trade plan exists for ticker; "N/A — insufficient history" when < 20 closed trades). Design source: quality-score-display/ux_spec.md. Approved: Product Owner 2026-05-18. |
| 0.1 | 2026-05-05 | Initial spec. v3.2 design gate — EPIC-01 (ST-01, ST-02, ST-03). Design source: docs/design/2026-05-05__release-v3.2/pre-trade-research-view/ux_spec.md. |
