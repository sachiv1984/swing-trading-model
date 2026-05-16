**Owner:** Director of Quality
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-05-16
**Story:** ST-10 (EPIC-03, v3.3) — BLG-QA-17
**Cross-reference:** `docs/qa/acceptance_protocols/research_view_protocol.md`
**Spec ref:** `docs/specs/frontend/pages/research_view.md`
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Test Scenario Library — Research View (PT-02)

---

## 1. Data Field Rendering

### SC-RV-01 — Price field renders when API returns price

**Precondition:** `GET /research/AAPL` returns `data.price = 178.50`, `data.market = "US"`
**Action:** Navigate to `/research/AAPL`
**Expected result:** Price displayed as `$178.50` (or equivalent currency format)

---

### SC-RV-02 — Price change renders with correct direction styling

**Precondition:** `data.price_change_pct = 0.0142`
**Action:** Navigate to research page
**Expected result:** Change displayed as `+1.42%` in green styling

**Variant:** `data.price_change_pct = -0.0083` → `-0.83%` in red styling

---

### SC-RV-03 — Market cap renders in abbreviated format

**Precondition:** `data.market_cap = 2800000000000`
**Action:** Navigate to research page
**Expected result:** Displayed as `$2.8T` or equivalent abbreviated form

---

### SC-RV-04 — ATR from signal renders in signal panel

**Precondition:** `data.signal.atr = 4.20`
**Action:** Navigate to research page, locate Signal panel
**Expected result:** ATR shown as `4.20` with appropriate label

---

### SC-RV-05 — Regime badge renders correctly for each regime value

**Precondition A:** `data.regime.label = "risk_on"`
**Expected result A:** "Risk On" badge in green

**Precondition B:** `data.regime.label = "risk_off"`
**Expected result B:** "Risk Off" badge in red

**Precondition C:** `data.regime.label = "mixed"`
**Expected result C:** "Mixed" badge in amber

---

### SC-RV-06 — Earnings panel renders next date and countdown

**Precondition:** `data.earnings = { next_earnings_date: "2026-07-25", days_until_earnings: 76, fiscal_quarter: "Q3 2026" }`
**Action:** Navigate to research page
**Expected result:** Earnings panel shows "2026-07-25" and "76 days" (or equivalent phrasing)

---

## 2. Source Attribution Display

### SC-RV-07 — Price source attribution shows "Yahoo Finance"

**Precondition:** Research endpoint returns price data
**Action:** Navigate to research page
**Expected result:** Muted attribution text beneath or adjacent to price shows "Yahoo Finance"

---

### SC-RV-08 — Screener panel shows run timestamp when screener data present

**Precondition:** `data.screener.latest_run_timestamp = "2026-05-09T06:00:00Z"`
**Action:** Navigate to research page, locate screener panel
**Expected result:** Run timestamp displayed as relative time (e.g. "Last run: yesterday" or ISO date)

---

### SC-RV-09 — Signal panel shows attribution as "Screener"

**Precondition:** `data.signal` is non-null
**Action:** Locate signal panel
**Expected result:** Attribution label or tooltip references "Screener" as source

---

## 3. News Feed Scenarios

### SC-RV-10 — News headlines render when present

**Precondition:** `data.news_headlines` contains 3+ items, each with `title`, `source`, `published_at`
**Action:** Navigate to research page, locate news section
**Expected result:** At least 3 headline items visible; each shows title and source/time

---

### SC-RV-11 — News empty state shown when no headlines

**Precondition:** `data.news_headlines = []`
**Action:** Navigate to research page
**Expected result:** News section shows "No recent news" empty state; no list items rendered

---

### SC-RV-12 — News renders gracefully when Alpaca is unavailable

**Precondition:** News service fails — `data.news_headlines = []` (API still returns 200)
**Action:** Navigate to research page
**Expected result:** News section shows empty state; no crash or error for the news section specifically; other panels unaffected

---

## 4. Freshness Indicator

### SC-RV-13 — Freshness indicator appears after 5 minutes without refresh

**Precondition:** Page loaded successfully; no user interaction for 5 minutes (simulate by mocking Date or fast-forward timer)
**Action:** Wait / advance timer
**Expected result:** Amber pill or notice appears: "Data may be stale" with refresh option

---

### SC-RV-14 — Clicking refresh re-fetches data

**Precondition:** Freshness indicator is visible
**Action:** Click "Refresh" or equivalent
**Expected result:** API call made to `GET /research/{ticker}`; panels update; indicator disappears

---

## 5. Error States

### SC-RV-15 — Full-page error when research endpoint returns 5xx

**Precondition:** `GET /research/AAPL` returns HTTP 500
**Action:** Navigate to research page
**Expected result:** Full-page error state with heading "Unable to load research data" and Retry button; no partial data shown

---

### SC-RV-16 — Retry button re-fetches after error

**Precondition:** Research endpoint returns 500; error state displayed
**Action:** Click "Retry"
**Expected result:** New request sent to `GET /research/AAPL`; if successful, page loads normally

---

### SC-RV-17 — Price null does not crash the page

**Precondition:** `data.price = null`, `data.price_change_pct = null`
**Action:** Navigate to research page
**Expected result:** Price panel renders with `—` placeholders; no JS error; other panels unaffected

---

### SC-RV-18 — Regime null does not crash the page

**Precondition:** `data.regime = null`
**Action:** Navigate to research page
**Expected result:** Regime panel shows "Regime unavailable"; no crash

---

### SC-RV-19 — All fields null — degraded state renders without crash

**Precondition:** All optional fields null: `price: null, signal: null, regime: null, screener: null, earnings: null`
**Action:** Navigate to research page
**Expected result:** Each panel renders its specific null display; no JS crash; Back button accessible

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-05-16 | ST-06 (EPIC-03, v3.6): SC-RV-18 and SC-RV-19 Playwright coverage confirmed — tests added to `tests/e2e/pre-trade-research.spec.js`. Closes BLG-FE-32. |
| 1.0 | 2026-05-10 | Initial creation — ST-10 (EPIC-03, v3.3). 19 scenarios covering field rendering, source attribution, news feed, freshness, and error states. |
