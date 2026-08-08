**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.4
**Last Updated:** 2026-08-08
**Design Source (v1.4):** docs/design/2026-08-08__release-v8.5/regime-distribution-panel/decision_record.md
**Design Source (v1.3):** docs/design/2026-06-19__release-v6.0/screener-quality-telemetry/ux_spec.md
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

- `GET /screener/results` — fetch screener result records (paginated); response envelope includes run quality fields: `tickers_requested` (int), `tickers_loaded` (int), `tickers_failed` (string[]), `last_full_run_utc` (ISO 8601), `run_quality` (FULL|DEGRADED|FAILED). Legacy fields `degraded_run` (boolean) and `failure_rate` (float) are deprecated in v6.0 — replaced by the run quality panel (§12)
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
| Actions | — | "Research" link + "Add to Watchlist" button (see §8 and §11) |

**Column ordering is fixed.** The frontend must not reorder columns without a spec update.

**Responsive behaviour:** On mobile viewport (<768px), hide the Sector and Entry Zone columns. Show Ticker, Price, Signal, and a "Details" expand.

---

## 5. Sort and Filter Controls

### 5.0 Regime History Panel (v1.4 — ST-21, BLG-FEAT-29)

A compact panel showing how the market regime has distributed across screener runs over time, distinct from the per-row `Regime` column (§4, which shows only the current run's status). Rendered above the Sort and Filter Controls (§5.1–5.2) — page-level context for interpreting the whole result set, shown before the user scans individual rows.

**Window selector:** Segmented button (same control pattern as the Market filter, §5.2) — **30d / 60d / All**.

**Breakdown display:** a two-segment horizontal percentage bar — green segment = % of screener runs in the selected window with `regime_status = risk_on`, red segment = % with `risk_off`, reusing the same chip colours as the per-row Regime column (§4) so the aggregate reads as the same concept scaled up. A single-line numeric readout beneath the bar, e.g. `"Risk-On 72% · Risk-Off 28% (30d)"`.

**Empty state:** if the selected window contains zero screener runs, render `DataState`'s `empty` branch (`docs/specs/frontend/design_system.md` §Data States) rather than a `0%/0%` bar, which would misleadingly imply data exists and split evenly.

**Data source:** aggregated from existing screener run history (`regime_status` per run) — no new backend concept beyond the aggregate query itself.

Design source: `docs/design/2026-08-08__release-v8.5/regime-distribution-panel/decision_record.md`.

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

## 11. Research Navigation (v3.2 — ST-04)

Each ticker row in the screener results table has a **"Research"** action (text link or secondary button) in the Actions column, adjacent to "Add to Watchlist".

| Attribute | Specification |
|-----------|---------------|
| Label | "Research" |
| Placement | Actions column, adjacent to "Add to Watchlist" |
| Target | `/research/{ticker}` |
| Context carry | None — ticker in URL path is sufficient |

**Back navigation:** User clicking `← Back` on the research view returns to `/screener` via browser back.

**Design source:** `docs/design/2026-05-05__release-v3.2/screener-to-research-navigation/ux_spec.md`

---

## 12. Run Quality Panel (v6.0 — ST-04)

**Design source:** `docs/design/2026-06-19__release-v6.0/screener-quality-telemetry/ux_spec.md`

Supersedes the v3.9 degraded-run banner (`degraded_run: boolean`). Displays a structured quality panel below the page header, above the data freshness indicator (§6) and results table, covering three distinct states driven by `run_quality`.

### FULL State

| Attribute | Specification |
|-----------|---------------|
| Badge | Green — "✓ FULL" |
| Content | Loaded ratio: "{tickers_loaded} / {tickers_requested}" |
| Stale advisory | Amber sub-line "Last full run: {N} hours ago" when `last_full_run_utc` > 24h ago |

### DEGRADED State

| Attribute | Specification |
|-----------|---------------|
| Badge | Amber — "⚠ DEGRADED" |
| Content | Loaded ratio + "Results may be incomplete — {N} tickers failed to load" |
| Expandable | Chevron "Show failed tickers ▾" → expands `tickers_failed` list; collapses on new run |
| Stale advisory | As per FULL state |

### FAILED State

| Attribute | Specification |
|-----------|---------------|
| Badge | Red — "✗ FAILED" |
| Content | "Screener run failed — no results available" |
| Retry | "Retry Run" button (secondary) — fires `POST /screener/run`; spinner while running |

**§13 Compliance:** Display-only quality telemetry. No automated decisions.

**Playwright tests:** SC-SQT-01a (FULL state badge + ratio), SC-SQT-01b (FULL + stale advisory), SC-SQT-01c (DEGRADED badge + ratio + message + toggle), SC-SQT-01d (DEGRADED expand/collapse ticker list), SC-SQT-01e (FAILED badge + retry button), SC-SQT-01f (backward-compat: old response without new fields gracefully handled)

---

## 13. AC Coverage Summary (DS-02 Interaction Patterns)

This spec covers all DS-02 interaction patterns:

| DS-02 / v3.9 Interaction | Spec section |
|--------------------------|-------------|
| Column layout | §4 |
| Sort/filter controls | §5 |
| Data freshness indicator | §6 |
| Manual refresh trigger | §6 |
| Empty states | §7 |
| Watchlist promotion flow | §8 |
| News panel | §9 |
| Skeleton/progressive loading | §10 |
| Research navigation (v3.2) | §11 |
| Run quality panel — FULL/DEGRADED/FAILED states (v6.0) | §12 |

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

---

## Known Deviations

| ID | Description | Canonical requirement | Priority | Target resolution | Owner | Backlog reference |
|----|-------------|----------------------|----------|------------------|-------|------------------|
| DEV-01 | News panel not displayed on screener results page (DS-02 portion of DS-06 AC-1). The `GET /news/{ticker}` backend endpoint is available; UI attachment to the screener results page is deferred pending DS-02 page implementation in v3.0. | §9 News Panel: "display on screener results page" (ST-07 AC-1). DS-02 implementation is a prerequisite. | P3 | v3.0 (DS-02 — screener results page implementation) | Backend Engineering Patterns Owner + Frontend Specifications & UX Documentation Owner | BLG-FE-18 |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.4 | 2026-08-08 | v8.5 design gate — ST-21 (EPIC-06, BLG-FEAT-29): added §5.0 Regime History Panel — rolling 30d/60d/All window selector (Segmented button, reusing the Market filter pattern) and a two-segment percentage breakdown bar (risk-on/risk-off), reusing the per-row Regime column's chip colours. Design source: `regime-distribution-panel/decision_record.md`. Approved: Head of UX & Design + Product Owner 2026-08-08. Head of Specs Team confirmed. |
| 1.3 | 2026-06-19 | v6.0 design gate — §12 replaced: Degraded Run Warning Banner (v3.9) superseded by Run Quality Panel with FULL/DEGRADED/FAILED states, loaded ratio, expandable failed ticker list, stale advisory, and retry prompt. §3 API reference updated: new response fields (tickers_requested, tickers_loaded, tickers_failed, last_full_run_utc, run_quality); legacy degraded_run/failure_rate deprecated. Design source: screener-quality-telemetry/ux_spec.md. Approved: Product Owner 2026-06-19. Head of Specs Team confirmed. |
| 1.2 | 2026-05-21 | v3.9 design gate — added §12 Degraded Run Warning Banner (ST-04: banner when degraded_run: true, percentage text, amber style, SC-SCR-DEG-01/02). §3 API reference updated to note degraded_run and failure_rate fields. Design source: degraded-run-banner/ux_spec.md. Approved: Product Owner 2026-05-21. Head of Specs Team confirmed. |
| 1.1 | 2026-05-05 | v3.2 design gate — added §11 Research Navigation (ST-04); added Actions column to §4 column layout. Design source: screener-to-research-navigation/ux_spec.md. |
| 1.0 | 2026-04-23 | Initial spec. |
