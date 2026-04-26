**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-26
**Cycle:** 2026-04-25__release-v3.0
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Delegation Log — 2026-04-25__release-v3.0

---

## DEL-20260426-01

- **ST Item:** ST-05 — Screener Results Page
- **EPIC:** EPIC-02
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #294
- **Branch:** exec/2026-04-25__release-v3.0/EPIC-02
- **Delegated at:** 2026-04-26T00:00:00Z
- **What is needed:** Implement the Screener Results page at route `/screener` per `docs/specs/frontend/pages/screener_results.md` v1.0. The page must show a table of screener results fetched from `GET /screener/results`, with sort/filter controls, freshness badge, manual refresh trigger (calls `POST /screener/run` and polls), skeleton loading, and all empty/error states per §7. Column layout, sort, filter, freshness indicator, skeleton UI, and empty states are all mandatory.
- **Spec reference:** `docs/specs/frontend/pages/screener_results.md` v1.0 §4–§10
- **Base44 prompt draft:**

  **Context:** Swing trading app with a React frontend. The backend `GET /screener/results` API is now live (shipped v3.0 Sprint 1). Implement the Screener Results page.

  **Change required:** Create `src/pages/Screener.js` (or equivalent per project naming). Add a top-level nav item "Screener" linking to `/screener`. The page fetches from `GET /screener/results` and displays results in a sortable/filterable table.

  **API contract:** `docs/specs/api_contracts/screener_api_contract.md`. Key fields: `ticker`, `market`, `price`, `currency`, `atr`, `atr_pct`, `regime_status` (risk_on/risk_off), `signal_score`, `sector`, `proximity_to_entry_zone`, `news_headline_count`, `run_timestamp`. GET endpoint returns `{results: [...], run_id, run_timestamp, total, limit, offset}`. POST `/screener/run` returns 202 Accepted with `{run_id}`.

  **Behaviour rules:**
  - Table columns: Ticker, Market, Price, ATR (with currency suffix), Regime badge (green "Risk On" / red "Risk Off"), Signal score (0.0–1.0 as percentage or bar), Sector, Entry Zone ("Near entry"/"In zone"/"—")
  - Default sort: signal_score descending
  - Sort controls: signal_score, price, ATR (user-selectable)
  - Filter controls: Market (All/US/UK), Regime (All/Risk-On only), Sector (multiselect dropdown)
  - Freshness badge: "Last screened: [relative time]" from run_timestamp; "No screener run yet" if null
  - Manual refresh: "Refresh" button → POST /screener/run → poll GET /screener/results?run_id={run_id} every 5s, max 60s
  - While scanning: button shows "Scanning..." with spinner, disabled
  - Skeleton loading: 8 animated shimmer rows while fetching
  - Empty states: per screener_results.md §7 (no runs, all filtered, no passes, stale >24h)
  - Mobile (<768px): hide Sector and Entry Zone columns
  - News badge: count badge on each US ticker row (hidden for UK); clicking triggers ST-07 panel (defer to ST-07 if not implementing together)

  **Non-functional rules:** No business logic; display-layer only. Do not introduce new data sources. Sort/filter state not persisted across refreshes.

  **Expected outcome:** Navigating to `/screener` shows the results table with data from the API. Empty state shows when no runs exist. Refresh button triggers a new run and updates results.

- **Unblock criteria:** Commit `[EPIC-02][ST-05] …` pushed to `exec/2026-04-25__release-v3.0/EPIC-02`; all acceptance criteria in sprint_backlog.md#ST-05 met; DoQ sign-off block populated with explicit evidence method (local run or staging).
- **Commit format required:** `[EPIC-02][ST-05] <description>` pushed to `exec/2026-04-25__release-v3.0/EPIC-02`
- **Status:** Pending

---

## DEL-20260426-02

- **ST Item:** ST-06 — Watchlist Promotion Flow
- **EPIC:** EPIC-02
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #295
- **Branch:** exec/2026-04-25__release-v3.0/EPIC-02
- **Delegated at:** 2026-04-26T00:00:00Z
- **What is needed:** Add one-click watchlist promotion to each screener result row per `docs/specs/frontend/pages/screener_results.md` v1.0 §8. Each row shows "Add to Watchlist" button. Clicking shows an **inline confirmation popover** (not a modal) with ticker, price, optional target entry price, and optional notes. Confirming calls `POST /watchlist`. On success: row shows "Added ✓" chip and button is disabled. On error: inline error message.
- **Spec reference:** `docs/specs/frontend/pages/screener_results.md` v1.0 §8 (Watchlist Promotion Confirmation Flow)
- **Base44 prompt draft:**

  **Context:** Screener Results page (ST-05) is being implemented. This story adds watchlist promotion to each result row.

  **Change required:** On the Screener Results page, add an "Add to Watchlist" button to each result row. Implement the inline confirmation popover and API call per §8.

  **API contract:** `POST /watchlist` — body: `{ticker, target_entry_price (optional), notes (optional)}`. Returns 201 on success, 409 if already in watchlist.

  **Behaviour rules:**
  - "Add to Watchlist" button on each row
  - Clicking: opens inline confirmation popover (not a full modal — attach to the row, dismiss with Escape/Cancel)
  - Popover fields: Ticker (read-only, pre-populated), Price (read-only, pre-populated), Target entry price (optional, pre-populated with screener price), Notes (optional text area)
  - Confirm button: calls POST /watchlist; shows spinner while loading
  - On success: close popover; row shows "Added ✓" chip; button disabled for session
  - On error: show inline error "Could not add to watchlist — try again"; button re-enabled
  - Tickers already in watchlist (from pre-load): show "In Watchlist" state with greyed button on page load
  - No duplicate promotions: if 409 returned, treat as already-in-watchlist; show "In Watchlist" state

  **Non-functional rules:** Popover must not obstruct other rows. Display-layer only — no new business logic.

  **Expected outcome:** Clicking "Add to Watchlist" shows the inline confirmation popover. Confirming calls the API and row state updates accordingly.

- **Unblock criteria:** Commit `[EPIC-02][ST-06] …` pushed to branch; all AC met; DoQ sign-off with evidence of promotion flow (local run or staging).
- **Commit format required:** `[EPIC-02][ST-06] <description>` pushed to `exec/2026-04-25__release-v3.0/EPIC-02`
- **Status:** Pending

---

## DEL-20260426-03

- **ST Item:** ST-07 — Screener News Panel Attachment
- **EPIC:** EPIC-02
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #296
- **Branch:** exec/2026-04-25__release-v3.0/EPIC-02
- **Delegated at:** 2026-04-26T00:00:00Z
- **What is needed:** Wire the existing `GET /news/{ticker}` endpoint to an inline news panel on the Screener Results page per `docs/specs/frontend/pages/screener_results.md` v1.0 §9. US ticker rows show a news count badge. Clicking the badge expands an inline news panel below the row showing last 10 headlines. UK tickers show "—" (no badge, no panel). Display-only per BLG-GOV-16 §13 — no sentiment labels, no sentiment scores. Strategy Rules Owner counter-sign required at DoQ.
- **Spec reference:** `docs/specs/frontend/pages/screener_results.md` v1.0 §9
- **Base44 prompt draft:**

  **Context:** Screener Results page (ST-05) is in place. This story adds the news panel to US ticker rows using the existing `GET /news/{ticker}` endpoint.

  **Change required:** On the Screener Results page, show a news count badge on US ticker rows using `news_headline_count` from the screener result. Clicking the badge fetches `GET /news/{ticker}` and expands an inline panel below the row.

  **API contract:** `GET /news/{ticker}` — returns `{articles: [{headline, published_at, source}, ...]}`. This endpoint already exists in the backend. No new backend changes needed.

  **Behaviour rules:**
  - US ticker rows: show `news_headline_count` badge (e.g. "3"); hide badge if count is 0
  - UK tickers (.L suffix or market=UK): show "—" in news column; no badge; no panel
  - Clicking badge: fetches GET /news/{ticker}; shows loading spinner on badge; expands inline panel below the row
  - Panel shows: up to 10 headlines with headline text + relative date (e.g. "2 hours ago") + source name if available
  - Empty news state in panel: "No recent news available for [ticker]"
  - Panel has "Close" link at bottom to collapse
  - Only one panel open at a time (opening one panel closes any other open panel)
  - No sentiment labels, no sentiment scores, no advisory text — display-only per BLG-GOV-16 §13

  **Non-functional rules:** Display-only. No new data sources. No sentiment analysis. News source text is display-only.

  **Expected outcome:** Clicking a US ticker's news badge expands an inline news panel with recent headlines. UK tickers show "—" and no badge.

- **Unblock criteria:** Commit `[EPIC-02][ST-07] …` pushed to branch; all AC met; DoQ sign-off with local run evidence of panel toggle (code review insufficient for toggle behaviour); Strategy Rules Owner counter-sign in EPIC-02 DoQ consolidation block.
- **Commit format required:** `[EPIC-02][ST-07] <description>` pushed to `exec/2026-04-25__release-v3.0/EPIC-02`
- **Status:** Pending

---

## DEL-20260426-04

- **ST Item:** ST-11 — Keyboard Shortcuts
- **EPIC:** EPIC-03
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #300
- **Branch:** exec/2026-04-25__release-v3.0/EPIC-03
- **Delegated at:** 2026-04-26T00:00:00Z
- **What is needed:** Implement global keyboard shortcuts (`n`, `w`, `r`) with a sidebar footer hint per `docs/specs/frontend/pages/navigation.md` v1.1 §Keyboard Shortcuts and `docs/design/2026-04-25__release-v3.0/keyboard-shortcuts/ux_spec.md` v1.0. Shortcuts fire on document `keydown` with suppression when focus is in a text input. Sidebar footer shows applicable shortcuts for the current page.
- **Spec reference:** `docs/specs/frontend/pages/navigation.md` v1.1 §Keyboard Shortcuts; `docs/design/2026-04-25__release-v3.0/keyboard-shortcuts/ux_spec.md` v1.0
- **Base44 prompt draft:**

  **Context:** Swing trading app. Add global keyboard shortcuts for common actions and a sidebar footer shortcut reference hint.

  **Change required:** Register a document-level `keydown` event handler. Add a sidebar footer section showing applicable shortcuts for the current page.

  **API contract:** No new API calls. Pure display-layer event handlers.

  **Behaviour rules:**
  - `n` key: open new position form/modal on applicable pages (Positions, Trade History)
  - `w` key: trigger add-to-watchlist on applicable pages (Watchlist, Screener Results)
  - `r` key: trigger page data refresh on all pages that have a primary data endpoint
  - Suppression rule: check `document.activeElement.tagName` — do NOT fire shortcuts when focus is in `INPUT`, `TEXTAREA`, or `SELECT`
  - Sidebar footer hint: show a "Shortcuts" section at the bottom of the left sidebar nav, below all nav group items
  - Format: three rows, each with `[key]` chip + action label
  - Dynamic filtering: show only shortcuts applicable to the current page; hide section if no shortcuts apply
  - Visual: section label "Shortcuts" in uppercase small-caps, secondary muted colour; key chips as small monospace badges with light bg, rounded corners, border; action label in secondary typography
  - Mobile collapsed sidebar: hide hint (shortcuts remain active)

  **Non-functional rules:** Display-layer event handlers only. No changes to business logic, data flows, or routing. No new data sources.

  **Expected outcome:** On the Screener Results page, pressing `w` triggers add-to-watchlist. Pressing `r` refreshes data. The sidebar footer shows applicable shortcuts for the current page. Shortcuts do not fire when typing in input fields.

- **Unblock criteria:** Commit `[EPIC-03][ST-11] …` pushed to branch; all AC met; DoQ sign-off with local run evidence stating which pages were tested.
- **Commit format required:** `[EPIC-03][ST-11] <description>` pushed to `exec/2026-04-25__release-v3.0/EPIC-03`
- **Status:** Pending
