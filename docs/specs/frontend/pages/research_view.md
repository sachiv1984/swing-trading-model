**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.4
**Last Updated:** 2026-08-16
**Story:** ST-09 (EPIC-03, v3.3) — BLG-SPEC-24
**§13 Compliance:** Confirmed — display-only. No automated recommendation generated. See §8.
**API contract:** docs/specs/api_contracts/research_endpoint.md
**Data provenance:** docs/specs/data_provenance/research_view_provenance.md
**UX spec:** docs/design/2026-05-09__release-v3.3/research-view/ux_spec.md
**Design Source:** docs/design/2026-05-09__release-v3.3/research-view/ux_spec.md
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# research_view.md — Research View

**Purpose:** The Research View (`/research/:ticker`) provides an aggregated pre-trade research snapshot for a single ticker. It consolidates price data, signal information, market regime, sector, screener presence, earnings proximity, and recent news into a single page for pre-entry review.

Shipped in v3.1 (PT-02). Spec formalised in v3.3 (ST-09, EPIC-03).

---

## 1. Purpose and User Goals

Users should be able to:

- Review all available pre-trade research for a given ticker on one page
- Assess market regime context before placing an entry
- See whether the ticker is currently in the screener results
- View upcoming earnings risk
- Read recent news headlines
- Navigate directly to create or view a trade plan for the ticker

---

## 2. Navigation and Routes

| Route | Purpose |
|-------|---------|
| `/research/:ticker` | Research view for the given ticker |
| `/research/:ticker?market=UK` | Research view with explicit market (optional) |

- Accessible from: Screener results ("Research" link), Watchlist ("Research" link), Trade Plan form ("Review research →" link)
- Page title: **"{TICKER} — Research"**

---

## 3. API Reference

| Endpoint | Purpose |
|----------|---------|
| `GET /research/{ticker}` | Aggregated research data |
| `GET /trade-plans?ticker={ticker}` | Active trade plan for the ticker (if any) |
| `GET /portfolio/prospective-heat?ticker={ticker}&...` | Prospective portfolio heat for sizing context |

Canonical API contract: `docs/specs/api_contracts/research_endpoint.md`

---

## 4. Data Fields Displayed

### 4.1 Price Panel

| Field | Source | Format | Null display |
|-------|--------|--------|-------------|
| Current price | `data.price` | Currency symbol + 2dp (USD/GBP) | `—` |
| Daily change % | `data.price_change_pct` | `+1.42%` or `-0.83%` with colour | `—` |
| Market cap | `data.market_cap` | `$2.8T`, `£450M` (abbreviated) | `—` |
| Sector | `data.sector.sector` | Plain text | `—` |
| Industry | `data.sector.industry` | Plain text | `—` |

### 4.2 Signal Panel

Displayed only when `data.signal` is non-null.

| Field | Source | Format |
|-------|--------|--------|
| Signal status | `data.signal.status` | Coloured badge: Active (green), Watch (amber), others (grey) |
| Setup type | `data.signal.signal_type` | Plain text (setup type slug, displayed as-is); `—` if null |
| Signal date | `data.signal.signal_date` | `"Signal: {YYYY-MM-DD}"` |
| ATR | `data.signal.atr` | `"{N} ATR"` |
| Entry price | `data.signal.entry_price` | Currency-formatted |
| Stop price | `data.signal.stop_price` | Currency-formatted |
| R-target | `data.signal.r_target` | `"{N}R"` |
| Rank | `data.signal.rank` | `"Rank #{N}"` |

**Playwright test coverage:** `tests/e2e/research-view-signal-type.spec.js` covers observable AC for `signal_type` display (label visible, value rendered). Filed per ST-10 AC-02 Playwright path.

When `data.signal` is null: display "No signal on file" placeholder.

### 4.3 Market Regime Panel

| Field | Source | Format |
|-------|--------|--------|
| Regime label | `data.regime.label` | Badge: "Risk On" (green), "Risk Off" (red), "Mixed" (amber) |
| SPY status | `data.regime.spy_risk_on` | Inline: "SPY ✓" or "SPY ✗" |
| FTSE status | `data.regime.ftse_risk_on` | Inline: "FTSE ✓" or "FTSE ✗" |

When `data.regime` is null: display "Regime unavailable".

**Regime label badge constraint (v3.6 — ST-08):** Badge must render on a single line. Apply `max-w-[120px] truncate` or equivalent to prevent two-line wrapping at standard viewport widths (1280px, 1440px). Typography must conform to `docs/frontend/design_system.md` chip/badge scale (`text-xs font-medium`). Long label values (e.g. future additions) must truncate with ellipsis rather than wrap.

### 4.4 Screener Panel

| State | Display |
|-------|---------|
| `data.screener` non-null | Score, ATR%, last run timestamp |
| `data.screener` null | "Not in latest screener results" |

### 4.5 Earnings Panel

| Field | Source | Format |
|-------|--------|--------|
| Next date | `data.earnings.next_earnings_date` | `"Earnings: {YYYY-MM-DD}"` |
| Days until | `data.earnings.days_until_earnings` | `"In {N} days"` |
| Fiscal quarter | `data.earnings.fiscal_quarter` | Plain text |

When `data.earnings` is null: display "No upcoming earnings data".

### 4.6 News Feed

- Up to 5 most recent headlines from `data.news_headlines`
- Each article: headline text (truncated to ~80 chars), source name, relative publication time
- Headline links to article URL (opens in new tab)
- Empty state: "No recent news for {ticker}"

### 4.7 Trade Plan Panel

- Fetched via `GET /trade-plans?ticker={ticker}`
- When active plan exists: shows plan status, stop level, R/R notes, and read-only pre-entry checklist
- When no plan: CTA button "Create Trade Plan" → navigates to `/trade-plans/new?ticker={ticker}`
- **Status badge source (v1.3 — ST-14, BLG-FE-162):** the plan status badge renders via the shared `TradePlanStatusBadge`/`STATUS_CONFIG` exported from `TradePlans.js` — the single canonical source for all 6 statuses (plus `abandoned`) app-wide. This page must not maintain its own local status→label/colour map. Design source: `docs/design/2026-08-14__release-v8.8/research-status-badge-single-source/decision_record.md`.
- **Plan selection precedence (v1.3 — ST-14, BLG-FE-162):** when `GET /trade-plans?ticker={ticker}` returns more than one plan for the ticker, exactly one is shown. Precedence (first match wins): `active` → `entry_conditions_set` → `research_complete` → `research_pending` → `draft` → `closed`, i.e. most-currently-relevant-in-the-plan-lifecycle first. Prior to this story the selection only checked `active`/`entry_conditions_set`/`draft`, so a ticker whose only plan was `research_pending`, `research_complete`, or `closed` silently fell through to the no-plan CTA — found and fixed via this story's own Playwright coverage (`tests/e2e/research-trade-plan-status-badge.spec.js`), not a pre-existing design-time AC.

---

## 5. Data Freshness Policy

| Data type | Max acceptable age | Staleness display |
|-----------|-------------------|--------------------|
| Price, change% | Live (fetched on page load) | Show "(stale)" after 5 min without refresh |
| Market cap | Live | Same as price |
| Regime | Live (recalculated on load) | No staleness indicator |
| Signal | From last screener run | Show screener run timestamp |
| Screener results | From last screener run | Show `latest_run_timestamp` |
| Earnings | Static (yfinance) | No staleness indicator |
| News | Live on load | No staleness indicator |

**Staleness indicator:** After 5 minutes on page without refresh, display a pill or notice: "Data may be stale — Refresh". Clicking triggers re-fetch.

---

## 6. Error States

| Scenario | Display |
|----------|---------|
| `GET /research/{ticker}` 404 | Full-page error: "Ticker not found." — ticker does not exist in any data source. No retry button. |
| `GET /research/{ticker}` 503 | Full-page error: "Research data temporarily unavailable." + Retry button — critical source (Yahoo Finance) entirely unavailable. |
| `GET /research/{ticker}` 500 | Full-page error: "Unable to load research data." + Retry button |
| Individual field null | Per-field null display per §4 |
| No price data | Price section shows `—` for all price fields |
| All fields null | Full-page degraded state: each section shows its null display; no error page |

---

## 7. Source Attribution

Per `docs/specs/data_provenance/research_view_provenance.md`:
- Each data section displays muted source attribution text beneath the section header
- Format: `Source: {source name} · Updated {HH:MM}` (where timestamp applies)
- Full attribution spec in provenance doc

---

## 8. §13 Compliance

This feature is **§13 compliant — display-only**:
- The system aggregates and presents data from multiple sources
- No automated recommendation, signal, or action is generated by the page itself
- Signal data (when present) originates from a prior screener run and is labelled accordingly
- The human reviews all displayed information and makes all decisions independently

---

## Known Deviations

None.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.4 | 2026-08-16 | Sprint execution `2026-08-14__release-v8.8` EPIC-03/ST-14: §4.7 gains a documented plan-selection precedence rule (`active → entry_conditions_set → research_complete → research_pending → draft → closed`). Root cause found via this story's own new Playwright coverage: `Research.js`'s `activePlan` derivation only matched 3 of 6 statuses (`active`/`entry_conditions_set`/`draft`), so a ticker whose only plan was `research_pending`/`research_complete`/`closed` silently fell through to the no-plan CTA instead of showing the (now-correct) badge — fixed in the same commit as the badge-source change. Authority: Sprint Execution Engine (ST-14, 2026-08-16). |
| 1.3 | 2026-08-14 | v8.8 design gate (ST-14, BLG-FE-162): §4.7 Trade Plan Panel — documented that the status badge must render via the shared `TradePlanStatusBadge`/`STATUS_CONFIG` (`TradePlans.js`), not a page-local map; closes the 3-of-6-statuses-fall-back-to-raw-snake_case defect. No new colours or component. Design source: `docs/design/2026-08-14__release-v8.8/research-status-badge-single-source/decision_record.md`. Head of UX & Design confirmed 2026-08-14. |
| 1.2 | 2026-05-27 | v4.1 ST-10 (BLG-FE-44): §4.2 Signal Panel — added `signal_type` field (`data.signal.signal_type`, plain text, null → `—`). Playwright test coverage note added. Playwright coverage in tests/e2e/research-view-signal-type.spec.js. |
| 1.1 | 2026-05-16 | v3.6 design gate: (ST-07) §6 Error States — added 404 (ticker not found) and 503 (source unavailable) display rules; (ST-08) §4.3 regime label badge — single-line constraint added (`max-w-[120px] truncate`), typography conformance note referencing design_system.md chip/badge scale. Head of UX & Design confirmed 2026-05-16. |
| 1.0 | 2026-05-10 | Initial creation — ST-09 (EPIC-03, v3.3). Formalises PT-02 (v3.1) shipped feature. Full data fields, freshness policy, error states, §13 confirmation, source attribution references. |
