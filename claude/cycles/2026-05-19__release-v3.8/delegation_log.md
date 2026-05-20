Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-19

# Delegation Log — 2026-05-19__release-v3.8

Append-only. All delegated tasks across Sprint 1 and Sprint 2.

---

## DEL-20260519-01

- **ST Item:** ST-09 — Ticker Universe Management Page
- **EPIC:** EPIC-04
- **Classification:** delegated_frontend
- **Assigned to:** Head of UX & Design
- **GitHub Issue:** #445
- **Branch:** exec/2026-05-19__release-v3.8/EPIC-04
- **Delegated at:** 2026-05-19T10:50:00Z
- **What is needed:** Build the Ticker Universe Management page in the frontend React app. The backend routes and service are already implemented. The engine has removed the `public.tickers` startup sync from `backend/main.py`. The frontend needs a dedicated page (route + nav link) that lets users view, add, toggle inactive, and filter tickers in the universe.

  **Context:** The `ticker_universe` table is now the sole authoritative source for screener and signal generation. The management page must allow users to control which tickers are in scope.

  **Change required:**
  - New page: `src/pages/TickerUniverse.js` (or equivalent)
  - Nav link: add "Ticker Universe" to sidebar navigation
  - Table view: list all tickers (including inactive) with columns: Ticker, Market, Sector, Industry, Active status
  - Actions per row:
    - Toggle active/inactive: use `DELETE /ticker-universe/{ticker}` to deactivate; use `POST /ticker-universe` to re-activate (re-add same ticker)
    - Delete permanently is not needed — soft-delete (DELETE endpoint) is the spec-defined behaviour; label the button "Remove" or "Deactivate" in the UI
  - Add ticker form: fields = Ticker (text), Market (US/UK dropdown); optional Sector, Industry; submit calls `POST /ticker-universe`
  - Filter bar: filter by Market (All/US/UK) and Active status (All/Active/Inactive)
  - When ticker is inactive, row visually distinct (e.g. muted/strikethrough)

  **API contract reference:** `docs/specs/api_contracts/ticker_universe_api_contract.md`
  - `GET /ticker-universe?market=US|UK&active_only=false` — list all tickers (pass active_only=false to show inactive)
  - `POST /ticker-universe` body: `{ "ticker": "AAPL", "market": "US", "sector": "...", "industry": "..." }`
  - `DELETE /ticker-universe/{ticker}` — deactivate (soft-delete sets active=FALSE; returns 404 if already inactive)
  - Re-activate: call `POST /ticker-universe` with same ticker — the service re-activates on conflict

  **Behaviour rules:**
  - Inactive tickers must be visible in the table when "Show All" or "Inactive" filter is selected
  - After adding a ticker, the table must refresh immediately (optimistic update or re-fetch)
  - After deactivating/re-activating, the row state must update immediately
  - If news API returns an error for add, show the API error message
  - UK tickers that do not have `.L` suffix — the API will reject them; show the validation error returned by the API
  - When opened from a momentum signal, this page may be navigated to directly

  **Non-functional rules:**
  - Playwright tests required for: add ticker, toggle inactive, filter by market, filter by active status
  - No networkidle in Playwright tests — use waitFor element patterns per §14 Playwright Test Authoring Standard

  **Expected outcome:** A fully functional Ticker Universe Management page accessible from the sidebar nav, where users can view all tickers, add new ones, toggle active/inactive, and filter by market and active status. The `public.tickers` startup sync has already been removed by the engine.

- **Unblock criteria:** Commit `[EPIC-04][ST-09] ...` pushed to `exec/2026-05-19__release-v3.8/EPIC-04`; GitHub issue #445 closed automatically; Playwright tests for add/toggle/filter scenarios present in `tests/e2e/`; all AC items confirmed met
- **Commit format required:** `[EPIC-04][ST-09] <description>` pushed to `exec/2026-05-19__release-v3.8/EPIC-04`
- **Status:** Pending

---

## DEL-20260519-02

- **ST Item:** ST-06 — Setup Type Classification Field
- **EPIC:** EPIC-03
- **Classification:** delegated_frontend
- **Assigned to:** Head of UX & Design
- **GitHub Issue:** #446
- **Branch:** exec/2026-05-19__release-v3.8/EPIC-03
- **Delegated at:** 2026-05-19T11:00:00Z
- **What is needed:** Add a "Setup Type" dropdown to the trade plan creation and edit form. The engine has already committed all backend changes: `setup_type VARCHAR(50)` column in `trade_plans` table, `POST /trade-plans` and `PUT /trade-plans/{id}` both accept and persist `setup_type`, `GET /trade-plans/{id}` returns it in the response.

  **Context:** The setup type helps users classify their trade setup before writing the thesis. It also feeds into the AI thesis generator (ST-08).

  **Change required:**
  - Add "Setup Type" dropdown to the trade plan creation form, positioned above the "Setup Thesis" textarea
  - Dropdown options (exactly): `Breakout`, `Pullback to MA`, `Momentum Continuation`, `Mean Reversion`, `Catalyst-driven`, `Other`
  - Field is optional/nullable — existing plans without `setup_type` show the field as unset (placeholder text)
  - When the trade plan is opened from a momentum signal, pre-select "Momentum Continuation" as the default
  - `setup_type` visible in trade plan read/detail view
  - Wire up field to `POST /trade-plans` (create) and `PUT /trade-plans/{id}` (update) — include `setup_type` in the request body

  **API contract reference:** `docs/specs/api_contracts/trade_plan_endpoints.md#POST /trade-plans`
  - `POST /trade-plans` body includes `"setup_type": "Momentum Continuation"` (nullable)
  - `PUT /trade-plans/{id}` body includes `"setup_type": "..."` (nullable)
  - `GET /trade-plans/{id}` response includes `"setup_type"` field

  **Behaviour rules:**
  - Dropdown is optional — user can skip it and save plan without a setup type
  - If `setup_type` is null/unset, display as blank/placeholder in form and detail view
  - When pre-populating from a signal, only "Momentum Continuation" should auto-select
  - User can change the pre-selected value

  **Non-functional rules:**
  - Playwright tests required: verify dropdown renders, saves, and displays correctly
  - No networkidle in Playwright tests

  **Expected outcome:** Trade plan form has a Setup Type dropdown above the thesis textarea. Selected value persists through create and update cycles. Pre-selected as "Momentum Continuation" when opened from a momentum signal.

- **Spec reference:** `docs/specs/api_contracts/trade_plan_endpoints.md#POST /trade-plans`, `docs/specs/frontend/pages/trade_plan.md#5. Trade Plan Creation and Edit Form`
- **Unblock criteria:** Commit `[EPIC-03][ST-06] ...` pushed to `exec/2026-05-19__release-v3.8/EPIC-03`; Playwright test for dropdown render/save/display present; all AC items confirmed met
- **Commit format required:** `[EPIC-03][ST-06] <description>` pushed to `exec/2026-05-19__release-v3.8/EPIC-03`
- **Status:** Pending

---

## DEL-20260519-03

- **ST Item:** ST-07 — News Context Panel on Trade Plan Form
- **EPIC:** EPIC-03
- **Classification:** delegated_frontend
- **Assigned to:** Head of UX & Design
- **GitHub Issue:** #447
- **Branch:** exec/2026-05-19__release-v3.8/EPIC-03
- **Delegated at:** 2026-05-19T11:00:00Z
- **What is needed:** Add a collapsible "News Context" panel to the trade plan creation form. The backend endpoint `GET /news/{ticker}` already exists and is registered. The frontend needs to fetch and display recent headlines when a US ticker is set.

  **Context:** Providing recent news headlines in the trade plan form gives the user context for their thesis and feeds into AI thesis generation (ST-08).

  **Change required:**
  - Add "News Context" panel to the trade plan form, positioned above the Setup Thesis field
  - Panel appears only when a US ticker is set (hide for UK tickers or when no ticker set)
  - Fetch up to 5 most recent headlines from `GET /news/{ticker}?limit=5`
  - Display as read-only list with: headline title, source name, relative age (e.g. "2h ago", "3d ago")
  - Panel is collapsible (expand/collapse toggle)
  - Collapsed state persisted in localStorage per ticker key (e.g. `news_panel_{ticker}`)
  - If API returns empty headlines array (no news or UK ticker), hide panel entirely — do NOT show "No news" message
  - Existing pre-population of setup thesis and entry rationale fields must be unchanged

  **API contract reference:** `GET /news/{ticker}?market=US&limit=5`
  - Response: `{ "ok": true, "data": { "ticker": "AAPL", "headlines": [...], "count": N } }`
  - Headline object fields: `title`, `source`, `created_at` (ISO timestamp for relative age)

  **Behaviour rules:**
  - Panel visible only for US tickers; if ticker changes from US to UK (or cleared), hide panel
  - Collapsed/expanded state must persist in localStorage — key per ticker
  - On ticker change, re-fetch headlines for new ticker
  - Error from API: hide panel (treat same as no results)

  **Non-functional rules:**
  - Playwright tests required: panel renders for US ticker; panel hidden when no news returned
  - No networkidle in Playwright tests

  **Expected outcome:** Collapsible news panel above thesis field showing up to 5 Alpaca headlines for US tickers. Hidden for UK tickers and when no news available.

- **Spec reference:** `docs/specs/frontend/pages/trade_plan.md#5. Trade Plan Creation and Edit Form`
- **Unblock criteria:** Commit `[EPIC-03][ST-07] ...` pushed to `exec/2026-05-19__release-v3.8/EPIC-03`; Playwright tests for render and no-news cases present; all AC items confirmed met
- **Commit format required:** `[EPIC-03][ST-07] <description>` pushed to `exec/2026-05-19__release-v3.8/EPIC-03`
- **Status:** Pending

---

## DEL-20260519-04

- **ST Item:** ST-08 — AI-Assisted Thesis Generation
- **EPIC:** EPIC-03
- **Classification:** delegated_frontend
- **Assigned to:** Head of UX & Design
- **GitHub Issue:** #448
- **Branch:** exec/2026-05-19__release-v3.8/EPIC-03
- **Delegated at:** 2026-05-19T11:00:00Z
- **What is needed:** Add a "Generate thesis" button adjacent to the setup thesis textarea. Phase 1 is a pure frontend template engine — no API key or external AI call required. An optional Gemini Flash integration is hidden entirely when `REACT_APP_GEMINI_API_KEY` is not set.

  **Context:** ST-08 depends on ST-06 (setup type dropdown) and ST-07 (news context panel) being complete — the template engine uses setup_type and top news headlines as inputs.

  **Change required:**
  - "Generate thesis" button positioned adjacent to the setup thesis textarea label
  - Button click generates a draft thesis from template using available data:
    - Setup type (from ST-06 dropdown, if set)
    - Top 2 news headlines from the news panel (if ST-07 panel is visible and expanded)
    - Signal metrics (if trade plan was opened from a signal — use pre-populated context)
    - Current price/ATR data (if available from position or signal context)
  - Template engine (Phase 1 — no API call): assemble structured thesis text from above inputs
  - Generated text populates the setup thesis textarea
  - "AI draft" badge appears on the textarea after generation; badge disappears on first user edit (keydown)
  - "Improve with AI" button: hidden entirely when `REACT_APP_GEMINI_API_KEY` env var is not set — do NOT show as disabled; hide completely
  - No thesis auto-generated without user clicking the button
  - Saved plan stores user's final (potentially edited) version, not the original AI draft

  **Behaviour rules:**
  - If neither setup type nor news are available, generate a minimal template ("Setup type not specified; no recent news available.")
  - Badge on generated text: visible immediately after generation; clears permanently on first user keydown in the textarea
  - "Generate thesis" button label changes to "Regenerate thesis" after first generation (optional UX improvement — not a hard AC)

  **Non-functional rules:**
  - Playwright tests required: button visible; generated text populates textarea; badge clears on edit
  - No networkidle in Playwright tests
  - No external API calls in Phase 1 — template engine must work fully offline

  **Expected outcome:** Trade plan form has a "Generate thesis" button that produces a structured template draft. Badge marks the generated text. Badge clears on first edit. Gemini integration is hidden when no API key configured.

- **Spec reference:** `docs/specs/frontend/pages/trade_plan.md#5. Trade Plan Creation and Edit Form`
- **Unblock criteria:** Commit `[EPIC-03][ST-08] ...` pushed to `exec/2026-05-19__release-v3.8/EPIC-03`; ST-06 and ST-07 must be done first; Playwright tests for button/badge/generate flow present; all AC items confirmed met
- **Commit format required:** `[EPIC-03][ST-08] <description>` pushed to `exec/2026-05-19__release-v3.8/EPIC-03`
- **Status:** Pending

---

## DEL-20260519-05

- **ST Item:** ST-01 — §13 Review Gate for SI-01 Pre-Entry Rule Validation
- **EPIC:** EPIC-01
- **Classification:** delegated_decision
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #449
- **Branch:** exec/2026-05-19__release-v3.8/EPIC-01
- **Delegated at:** 2026-05-19T11:15:00Z
- **Escalation record:** ESC-20260519-01
- **What is needed:** §13 System Intent review decision on SI-01 Pre-Entry Rule Validation. The advisory panel is non-blocking (read-only, never prevents trade entry). Decision: PASS (proceed with binding conditions) or FAIL (park ST-02 and ST-03).

  **If PASS:** Create decision record at `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md` listing any binding conditions (rules to validate, severity classifications, exclusions). Set ST-01 → `done`. ST-02 (autonomous backend) and ST-03 (frontend delegation) will then proceed.

  **If FAIL:** Park ST-02 and ST-03 via backlog. Set ST-01 → `done` (gate evaluated: fail).

  **Relevant strategy context:** `claude/strategy/strategy_rules.md`

- **Unblock criteria:** Decision document created at `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md`; ST-01 set to `done` in `execution_state.json`; ST-02 and ST-03 status updated accordingly
- **SLA:** 72 hours (by 2026-05-22T11:15:00Z)
- **Status:** Pending
