**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.7
**Last Updated:** 2026-05-19
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v0.1):** docs/design/2026-04-29__release-v3.1/trade-plan/ux_spec.md (v3.1 — artefact reference only; file not present in repo)
**Design Source (v0.2 checklist):** docs/design/2026-05-05__release-v3.2/pre-trade-entry-checklist/ux_spec.md
**Design Source (v0.3 abandonment + badges):** docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §A, §B
**Design Source (v0.5 signal context panel):** docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md
**Design Source (v0.6 quality score):** docs/design/2026-05-18__release-v3.7/quality-score-display/ux_spec.md
**Design Source (v0.7 form enhancements):** docs/design/2026-05-19__release-v3.8/trade-plan-form-enhancements/ux_spec.md §A, §B, §C
**Design Source (v0.7 pre-entry validation):** docs/design/2026-05-19__release-v3.8/pre-entry-validation-panel/ux_spec.md
**API contract:** docs/specs/api_contracts/trade_plan_endpoints.md
**v0.4 Sign-off:** Head of Specs Team — 2026-05-14 (BLG-SPEC-28: §6.2 pre-population rules correction)

---

# trade_plan.md — Trade Plan

**Purpose:** The Trade Plan pages cover the trade plan list, creation/edit form, and detail view. Trade Plans capture the pre-trade rationale (ticker, stop level, risk/reward notes, entry checklist) for a prospective or active position. Introduced in v3.1 (PT-01); entry checklist added in v3.2 (PT-05).

---

## 1. Purpose and User Goals

Users should be able to:

- Create a trade plan before opening a position (pre-trade rationale capture)
- Record stop level, risk/reward notes, and complete the pre-trade entry checklist
- View all trade plans and their status
- Edit and update a trade plan as conditions evolve
- Navigate to the research view for the plan's ticker

---

## 2. Navigation and Routes

| Route | Purpose |
|-------|---------|
| `/trade-plans` | Trade plan list |
| `/trade-plans/new` | Create new trade plan (form) |
| `/trade-plans/new?ticker={ticker}` | Create new trade plan pre-populated with ticker |
| `/trade-plans/{id}` | Trade plan detail view |
| `/trade-plans/{id}/edit` | Edit trade plan |

- Top-level nav item: **"Trade Plans"**
- Page title (list): **"Trade Plans"**
- Page title (detail): **"{TICKER} — Trade Plan"**

---

## 3. API Reference

| Endpoint | Purpose |
|----------|---------|
| `GET /trade-plans` | List all trade plans (supports `?ticker={ticker}` filter) |
| `POST /trade-plans` | Create new trade plan |
| `GET /trade-plans/{id}` | Fetch single trade plan |
| `PUT /trade-plans/{id}` | Update trade plan (full replace) |
| `DELETE /trade-plans/{id}` | Delete trade plan |

Canonical contract: `docs/specs/api_contracts/trade_plan_endpoints.md`

---

## 4. Trade Plan List

### 4.1 Page Header

- H1: **"Trade Plans"**
- Right-aligned: **"+ New Trade Plan"** button (primary action)

### 4.2 List Layout

One card or row per trade plan. Default sort: most recently updated first. Abandoned plans shown with muted row styling (opacity 0.7).

| Column | Source | Notes |
|--------|--------|-------|
| Ticker | `ticker` | Uppercase |
| Status | `status` | Badge per §9 Status Badge Scheme |
| Stop Level | `stop_level` | Currency-formatted; `—` if null |
| Notes | `risk_reward_notes` | Truncated to ~60 chars |
| Updated | `updated_at` | Relative timestamp |
| Actions | — | "View" link + "Edit" link (Edit hidden for abandoned plans) |

### 4.3 Empty State

- Heading: **"No trade plans yet."**
- Body: "Create a trade plan before opening your next position."
- **"+ New Trade Plan"** button

### 4.4 Entry Points to Trade Plan Form

Per v3.1 design gate decision:
- Positions table: "Plan" button in Actions column
- Watchlist: "Plan" button in Actions column
- Research view: "Create Trade Plan" CTA (when no plan exists for the ticker)
- Direct URL: `/trade-plans/new`

---

## 5. Trade Plan Creation and Edit Form

### 5.1 Form Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Ticker symbol | Text | Yes | Uppercase-enforced; read-only on edit |
| Market | Radio: UK / US | Yes | |
| Status | Select | Yes | Draft / Active / Closed (Abandoned is set via Abandon action — not in this dropdown) |
| Stop Level | Numeric | No | Positive decimal; native currency |
| Risk/Reward Notes | Textarea | No | Free text; used for pre-population of CHK-04 |
| Setup Type | Select | No | 6 options; see §5c. Defaults to "Momentum Continuation" when opened from signal context |
| Setup Thesis | Textarea | No | Free text rationale; AI-draft generation available via §5d "Generate thesis" button |
| Pre-Trade Checklist | Component | No | See §6 |

### 5.2 Actions (Form Footer)

- **"Save Trade Plan"** (primary) — `POST /trade-plans` (new) or `PUT /trade-plans/{id}` (edit)
- **"Cancel"** (secondary) — returns to previous page without saving

---

## 5a. Signal Context Panel (v3.7 — BLG-FE-34)

**Design source:** docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md

> **§13 Compliance:** Read-only reference panel. No automated position entry or trade recommendation. Pre-population is advisory; the user may edit or clear all pre-populated values.

The Signal Context panel is shown **in the trade plan creation form only**, below the core plan fields (§5.1) and above the Pre-Trade Entry Checklist (§6). It is hidden in edit mode (does not overwrite existing saved values).

### 5a.1 Presence Condition

Shown when a linked signal exists for the trade plan ticker: a signal record where `ticker` matches and `status = "watchlisted"`.

When no linked signal exists: panel is hidden entirely. No placeholder shown. No regression to current form behaviour.

### 5a.2 Panel Content

**Panel header:** "Signal Context" (read-only section, visually distinct — muted background, e.g. `bg-gray-50`)

| Field | Label | Format |
|-------|-------|--------|
| Signal rank | "Rank" | `#N` |
| Momentum % | "Momentum" | `+X.X%` (green) or `−X.X%` (red) |
| Price vs 200-day MA | "vs 200-day MA" | `X.X% above` or `X.X% below` |
| Regime | "Regime" | "On" (green badge) / "Off" (amber badge) |
| ATR (14d) | "ATR (14d)" | Currency-formatted |
| Suggested stop | "Suggested stop" | Currency-formatted; sub-label "entry − 5×ATR" |

### 5a.3 Pre-Population Rules (creation form only)

On initial form load (new trade plan from signal context):

- **`risk_reward_notes`** pre-filled with: `"Rank {N} momentum signal. Price {above/below} 200-day MA by {x.x}%. {US/UK} regime on."` (user-editable)
- **Stop Level** pre-filled with suggested stop: `entry_price − (5 × atr)` (user-editable; not overwritten if already set)

Pre-population does not apply in edit mode. Existing user-set values are never overwritten.

### 5a.4 Error / Loading States

- If signal fetch fails: panel hidden silently; no error shown; form submission unaffected
- While loading: single-line skeleton placeholder
- If no linked signal: panel hidden (not an error)

---

## 5b. News Context Panel (v3.8 — ST-07)

**Design source:** docs/design/2026-05-19__release-v3.8/trade-plan-form-enhancements/ux_spec.md §B

> **§13 Compliance:** Read-only news panel. No recommendation generated. Headlines are informational only.

Shown in the trade plan creation form only, for US tickers when news results are available. Positioned above the Setup Type dropdown (§5c) and Setup Thesis textarea.

### 5b.1 Presence Condition

- Shown when a US ticker is set and `GET /news/{ticker}` returns at least one headline
- Hidden for UK tickers
- Hidden entirely if news API returns no results (not an error state)
- Hidden in edit mode

### 5b.2 Panel Content

**Panel header:** "News Context" (muted background `bg-gray-50`)

Per headline (up to 5 most recent): headline text (truncated 100 chars), source name, relative age (e.g. "2h ago").

### 5b.3 Collapsed State

- Collapsible via chevron toggle in panel header
- Collapsed state persisted in `localStorage` keyed by `news-panel-{ticker}`
- Default: expanded on first load for a given ticker

### 5b.4 Loading / Error States

- Loading: single-line skeleton placeholder; panel header visible
- API error: panel hidden silently; form submission unaffected

---

## 5c. Setup Type Classification Field (v3.8 — ST-06)

**Design source:** docs/design/2026-05-19__release-v3.8/trade-plan-form-enhancements/ux_spec.md §A

Positioned above the Setup Thesis textarea, below the News Context Panel (§5b) if present.

### 5c.1 Options

| Value | Display label |
|-------|--------------|
| `breakout` | Breakout |
| `pullback_to_ma` | Pullback to MA |
| `momentum_continuation` | Momentum Continuation |
| `mean_reversion` | Mean Reversion |
| `catalyst_driven` | Catalyst-driven |
| `other` | Other |

Placeholder: "Select setup type…"

### 5c.2 Signal-Driven Default

When the form is opened from a momentum signal context (Signal Context Panel §5a present and active), defaults to **"Momentum Continuation"**. User may change.

### 5c.3 Persistence

- `POST /trade-plans` and `PUT /trade-plans/{id}` accept `setup_type` (string or null)
- `GET /trade-plans/{id}` includes `setup_type`
- Existing plans without `setup_type`: field displays as unset ("—")

### 5c.4 Read View

Shown in Trade Plan detail view: label "Setup Type", display label (not raw key), "—" if unset.

---

## 5d. AI-Assisted Thesis Generation (v3.8 — ST-08)

**Design source:** docs/design/2026-05-19__release-v3.8/trade-plan-form-enhancements/ux_spec.md §C

> **§13 Compliance:** Template-generated draft is explicitly labelled "AI draft". No automated recommendation. User controls generation trigger and may edit or discard output.

### 5d.1 "Generate thesis" Button

- Positioned adjacent to the Setup Thesis textarea label (right of label or below label)
- Visible in creation mode when a ticker is set
- Never auto-triggered; requires explicit user click

### 5d.2 Template Engine (Phase 1 — No API)

On click, populates Setup Thesis textarea from: Setup Type value + Signal Context data + top 2 news headlines + current price. If no context available, a minimal template is generated. Replaces existing textarea content.

### 5d.3 "AI Draft" Badge

- Small grey pill "AI draft" appears adjacent to textarea after generation
- Clears on first user keystroke within the textarea

### 5d.4 "Improve with AI" Button (Phase 2 — Env-Gated)

- Shown **only when** `GEMINI_API_KEY` is configured; hidden entirely (not disabled) otherwise
- Sends current textarea content + trade context to Gemini Flash; replaces content with improved version
- "AI draft" badge re-applied after improvement

### 5d.5 Edit Mode

"Generate thesis" button hidden in edit mode.

---

## 5e. Pre-Entry Validation Panel (v3.8 — ST-03, conditional on ST-01 §13 PASS)

**Design source:** docs/design/2026-05-19__release-v3.8/pre-entry-validation-panel/ux_spec.md

**Gate condition:** This section activates only when ST-01 §13 Review Gate PASSES. If §13 review fails, EPIC-01 is removed from sprint scope and this section is not implemented.

> **§13 Compliance:** Advisory panel — display only. No automated blocking of plan submission. All checks produce informational results only. User may override any advisory result and proceed.

Positioned below the Setup Thesis textarea and above the Pre-Trade Entry Checklist (§6).

### 5e.1 Presence Condition

Shown when both ticker and quantity are set. Hidden otherwise.

### 5e.2 Panel Structure

**Header:** "Pre-Entry Validation" (muted background `bg-gray-50`, amber left border)

**Sub-header text (muted):** "Advisory checks based on strategy rules. Non-blocking — you may proceed regardless of results."

### 5e.3 Rule Checks

Five rows, one per rule:

| Rule | Label |
|------|-------|
| Regime gate | "Market regime" |
| Position sizing | "Position size within limits" |
| Sector concentration | "Sector concentration" |
| Earnings proximity | "Earnings proximity" |
| Cash constraint | "Available cash" |

Per row: rule label + status indicator (✅ Pass / ⚠️ Warn / ❌ Advisory fail) + short detail text from API response.

### 5e.4 Aggregate Status Bar

Single line above rule rows: "All checks passed" (green) / "Review warnings before entering" (amber) / "Advisory issues noted — you may still proceed" (red, not blocking).

### 5e.5 Override Flow

When any rule has advisory fail: "Acknowledge and proceed" button (amber outlined) appears. On click: `override_acknowledged: true` recorded on trade plan object; button replaced by muted note. Save button always available regardless.

### 5e.6 API

`GET /portfolio/pre-entry-validation?ticker={ticker}&quantity={n}` — per-rule results and aggregate advisory status. On error: panel hidden silently.

### 5e.7 Edit Mode

Panel hidden in edit mode.

---

## Form Layout Order (Creation Mode — v3.8)

1. Ticker symbol
2. Market
3. Status
4. Stop Level
5. Risk/Reward Notes
6. Signal Context Panel (§5a — conditional on linked signal)
7. News Context Panel (§5b — conditional: US ticker, news results present)
8. Setup Type dropdown (§5c)
9. Setup Thesis textarea + "Generate thesis" button (§5d) + "AI draft" badge + "Improve with AI" button (env-gated)
10. Pre-Entry Validation Panel (§5e — conditional: ticker + quantity set; §13 gate)
11. Pre-Trade Entry Checklist (§6)
12. Save / Cancel

---

## 6. Pre-Trade Entry Checklist (v3.2 — PT-05)

> **§13 Compliance:** This feature has been reviewed and confirmed §13 compliant — see `docs/specs/compliance/pt05_entry_checklist_s13_review.md`. The system presents checklist items; the human confirms each condition; the system records the human-confirmed state. No automated condition evaluation or recommendation is generated. (ST-15, v3.3)

The checklist is embedded as a grouped section within the Trade Plan creation and edit forms, below the core plan fields.

### 6.1 Section Header

"Pre-Trade Checklist"

### 6.2 Checklist Items

| Item ID | Label | Pre-population |
|---------|-------|----------------|
| CHK-01 | Strategy signal confirmed | Never auto-checked |
| CHK-02 | Position size within heat limits | Never auto-checked |
| CHK-03 | Stop level defined | Auto-checked if `early_exit_conditions` is non-null and non-empty |
| CHK-04 | Pre-trade research reviewed | Auto-checked if `r_target` is non-null |

- Each item: checkbox + label
- All items visible regardless of check state
- Pre-population is advisory — user may uncheck any item
- Existing user-set state is not overwritten on re-open

**Pre-population rationale (BLG-SPEC-28):** CHK-03 uses `early_exit_conditions` (not `stop_level`) because exit-condition thinking implies the trader has defined their stop logic even if no numeric stop level is set yet. CHK-04 uses `r_target` (not `risk_reward_notes`) because an explicit R target indicates the risk/reward ratio has been computed — the most meaningful signal that research has been reviewed.

**Test scenario cross-reference:** `tests/e2e/entry-checklist.spec.js` (SC-CL-01 through SC-CL-05) covers pre-population behaviour. Any change to pre-population fields must be reflected in those scenarios.

### 6.3 "Review Research" Link

- Label: "Review research →"
- Target: `/research/{ticker}` for the plan's ticker
- Visible only when the plan has a ticker set
- Present in both creation and edit modes

### 6.4 Read-Only State (Detail View)

In the trade plan detail view (not editing):
- Checklist items shown as read-only indicators (no interactive checkboxes)
- "Review research" link remains active

### 6.5 Persistence

Checklist state stored as `checklist` array on the trade plan record. Submitted with `POST /trade-plans` and `PUT /trade-plans/{id}`.

---

## 7. Trade Plan Detail View

- Shows all plan fields in read-only layout: ticker, market, status, stop level, setup type (§5c.4), risk/reward notes, setup thesis
- Pre-trade checklist shown in read-only state (§6.4)
- Setup Quality Score shown (§7a) if EPIC-02 (PT-04) is in scope
- Action buttons: **"Edit"** (primary) + **"Abandon"** (amber outlined — see §8) + **"Delete"** (destructive, with confirmation)
- **"Review research"** link present if ticker is set
- When `status = 'abandoned'`: "Abandon" and "Edit" buttons hidden; abandonment reason shown (see §8.3)

---

## 7a. Setup Quality Score (v3.7 — PT-04, conditional EPIC-02 gate)

**Design source:** docs/design/2026-05-18__release-v3.7/quality-score-display/ux_spec.md

**Gate condition:** This section activates only when EPIC-02 is confirmed in scope (Product Owner confirms 20+ closed trades). If EPIC-02 is deferred to v3.8, this section is not implemented.

> **§13 Compliance:** Display-only score labelled as historical reference ("based on your own trade history"). Not a prediction or recommendation. No automated actions.

Displayed in the Trade Plan detail view below status badge and core fields, above the Pre-Trade Checklist read-only section.

| Element | Source | Display |
|---------|--------|---------|
| Label | — | "Setup Quality Score" |
| Value | `GET /trade-plans/{id}/quality-score` → `score` | `{N}/100`; colour-coded: 0–39 red, 40–69 amber, 70–100 green |
| Insufficient history | Response: `score: null, reason: "insufficient_history"` | "N/A — insufficient history" |
| Sub-label | — | "Based on your own trade history" (muted) |

**Loading:** inline skeleton placeholder. **Error:** field hidden silently (does not block page).

---

## 8. States

| State | Behaviour |
|-------|-----------|
| Loading (list) | Skeleton rows |
| Loading (detail/form) | Skeleton form fields |
| Error | Inline error message + Retry |
| Empty (list) | See §4.3 |

---

## 8. Trade Plan Abandonment (v3.3 — ST-17 BLG-FEAT-21)

**Design source:** docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §A

### 8.1 Trigger

"Abandon" action button shown in Trade Plan detail view below "Edit":
- Style: secondary, amber outlined (warning-adjacent — not primary; not red)
- Hidden when `status = 'active'` (linked open position; backend enforces with 400 guard)

### 8.2 Abandonment Modal

**Title:** "Abandon trade plan for {TICKER}?"

**Body text:** "This plan will be marked as abandoned. You will not be prompted to enter this position again based on this plan."

**Required field:** Abandonment reason (textarea, 3 rows, min 10 chars). Inline validation on blur. Confirmation button disabled until valid.

**Actions:**
- "Abandon Plan" (primary, amber) — submits `PUT /trade-plans/{id}` with `{status: 'abandoned', abandonment_reason: <text>}`
- "Cancel" (secondary) — closes modal; no change

### 8.3 Abandoned Plan Display

In the detail view when `status = 'abandoned'`:
- Status badge: Abandoned (red — §9)
- Read-only field below status: "Reason for abandoning: {abandonment_reason}"
- "Abandon" and "Edit" hidden; "Delete" remains
- List view row: muted styling (opacity 0.7)

---

## 9. Status Badge Scheme (v3.3 — ST-17 BLG-FE-30)

**Design source:** docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §B

Applied in Trade Plan List and Trade Plan Detail View:

| Status | Badge Label | Colour | Hex |
|--------|------------|--------|-----|
| `draft` | Draft | Grey | `#6B7280` |
| `research_pending` | Research Pending | Amber | `#D97706` |
| `research_complete` | Research Complete | Blue | `#2563EB` |
| `entry_conditions_set` | Entry Ready | Purple | `#7C3AED` |
| `active` | Active | Green | `#16A34A` |
| `closed` | Closed | Slate (muted) | `#94A3B8` |
| `abandoned` | Abandoned | Red | `#DC2626` |

All badges: filled pill, white text. Contrast ≥ 4.5:1 (WCAG AA) for all combinations.

---

## Known Deviations

| ID | Description | Canonical requirement | Priority | Target resolution | Owner | Backlog reference |
|----|-------------|----------------------|----------|-------------------|-------|------------------|
| DEV-01 | v3.1 design gate claimed creation of this spec at v0.1, but the file was not committed to the repository. Recovered at v3.2 design gate. | Spec must exist at committed path | P2 | Resolved — file created at v3.2 design gate | Head of Specs Team | N/A |
| DEV-v3.4-01 | EPIC-03 ST-10 (v3.4): React Query v5 removed `onSuccess` from `useQuery`. `isAbandoned` derived from `existingPlan?.status` (query data) rather than a post-fetch callback. Functional behaviour — abandonment state derived correctly on initial load — matches spec §8.1 intent. Codebase scan for other `onSuccess` usages tracked in BLG-SPEC-31. | §8.1: isAbandoned derived from onSuccess callback | P3 | v3.5 — codebase scan; full resolution per BLG-SPEC-31 | Head of Engineering | BLG-SPEC-31 |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.7 | 2026-05-19 | v3.8 design gate — added §5b News Context Panel (ST-07: collapsible news panel for US tickers, localStorage collapsed state), §5c Setup Type Classification Field (ST-06: 6-option dropdown, signal-driven default, detail view display), §5d AI-Assisted Thesis Generation (ST-08: template engine, AI draft badge, Gemini env-gated), §5e Pre-Entry Validation Panel (ST-03: advisory 5-rule panel, override flow, §13 compliant; conditional ST-01 §13 PASS). Updated §5.1 form fields table; added Form Layout Order section; updated §7 detail view. Design sources: trade-plan-form-enhancements/ux_spec.md, pre-entry-validation-panel/ux_spec.md. Approved: Product Owner 2026-05-19. |
| 0.6 | 2026-05-18 | v3.7 design gate — added §7a Setup Quality Score (PT-04: score display on detail view, 0–100 or "N/A — insufficient history", §13 compliant). Conditional on EPIC-02 gate. Design source: quality-score-display/ux_spec.md. Approved: Product Owner 2026-05-18. |
| 0.5 | 2026-05-18 | v3.7 design gate — added §5a Signal Context Panel (BLG-FE-34: read-only signal data panel in creation form; pre-population of rationale and stop fields; conditional on linked signal). Design source: signal-context-panel/ux_spec.md. Approved: Product Owner 2026-05-18. |
| 0.4 | 2026-05-14 | BLG-SPEC-28 (ST-13, v3.4) — corrected §6.2 pre-population rules: CHK-03 uses `early_exit_conditions` (not `stop_level`); CHK-04 uses `r_target` (not `risk_reward_notes`). Added rationale note and test scenario cross-reference. Authority: Head of Specs Team. |
| 0.3 | 2026-05-09 | v3.3 design gate — added §8 Trade Plan Abandonment (BLG-FEAT-21: abandon action, modal, abandoned display); added §9 Status Badge Scheme (BLG-FE-30: 7-state badge set including Abandoned). Design source: trade-plan-quick-wins/ux_spec.md §A, §B. Approved: Product Owner 2026-05-09. |
| 0.2 | 2026-05-05 | v3.2 design gate — added Pre-Trade Entry Checklist section (§6) for EPIC-02 (ST-05, ST-06). Design source: pre-trade-entry-checklist/ux_spec.md. Also: initial file creation (recovering v3.1 gap — trade_plan.md v0.1 was stated as created in v3.1 design gate but not committed). |
| 0.1 | 2026-04-29 | Initial spec intent — v3.1 design gate (ST-03 — Trade Plan creation flow + detail view). File not committed at the time; recovered at v3.2. |
