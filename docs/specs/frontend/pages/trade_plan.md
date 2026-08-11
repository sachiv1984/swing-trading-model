**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.4
**Last Updated:** 2026-08-11 (v8.6 design gate — §10.5 Setup Thesis Digest at Order Placement added, ST-02/BLG-FEAT-56); prior — 2026-07-30 (v8.0 design gate — checklist keyboard accessibility + abandon modal focus trap)
**Design Source (v1.4 setup thesis digest):** docs/design/2026-08-11__release-v8.6/ai-thesis-digest-order-placement/ux_spec.md
**Design Source (v1.3 checklist keyboard accessibility):** docs/design/2026-07-30__release-v8.0/entry-checklist-keyboard-accessibility/decision_record.md
**Design Source (v1.3 abandon modal focus trap):** docs/design/2026-07-30__release-v8.0/abandon-modal-focus-trap/decision_record.md
**Design Source (v1.2 print/export PDF):** docs/design/2026-07-20__release-v7.6/print-pdf-export/ux_spec.md
**Design Source (v1.1 bulk actions):** docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v1.0 Start Trade from Plan):** docs/design/2026-07-15__release-v7.2/start-trade-from-plan/ux_spec.md (BLG-FE-109)
**Design Source (v0.1):** docs/design/2026-04-29__release-v3.1/trade-plan/ux_spec.md (v3.1 — artefact reference only; file not present in repo)
**Design Source (v0.2 checklist):** docs/design/2026-05-05__release-v3.2/pre-trade-entry-checklist/ux_spec.md
**Design Source (v0.3 abandonment + badges):** docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §A, §B
**Design Source (v0.5 signal context panel):** docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md
**Design Source (v0.6 quality score):** docs/design/2026-05-18__release-v3.7/quality-score-display/ux_spec.md
**Design Source (v0.7 quality score v2):** docs/design/2026-05-21__release-v3.9/setup-quality-score-v2/ux_spec.md
**Design Source (v0.8 thesis feedback):** docs/design/2026-07-02__release-v6.5/thesis-feedback-mechanism/ux_spec.md
**Design Source (v0.9 tags):** docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md
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
| `GET /trade-plans/tags` | *(v0.9 — ST-05)* Tag autocomplete source for the Trade Plan Tag Editor (§5c) |

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
| Tags | Component (Tag Editor) | No | See §5c |
| Pre-Trade Checklist | Component | No | See §6 |

### 5.2 Actions (Form Footer)

- **"Save Trade Plan"** (primary) — `POST /trade-plans` (new) or `PUT /trade-plans/{id}` (edit)
- **"Cancel"** (secondary) — returns to previous page without saving

---

## 5c. Trade Plan Tags (v0.9 — ST-05 BLG-FEAT-52)

**Design source:** docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md

Independent tag field on `trade_plans` (`trade_tags`) — data-independent from the existing position/journal tags documented in `journal_components.md` (`GET /positions/tags`); same components reused for visual consistency only.

**Edit form / creation form:** Tag Editor (Autocomplete Input) — `journal_components.md` §4 behaviour unchanged (Enter to add, click X to remove, lowercase/hyphen validation, max 20 chars, dedup, tag limit). Autocomplete source: `GET /trade-plans/tags`.

**Detail view (read-only):** Tag List pill display, positioned directly below the core plan fields and above the Pre-Trade Checklist (§6) read-only section. Empty state: "No tags" (muted).

> **§13 Compliance:** Display-only classification field. No automated action taken on tag values.

**Playwright coverage required:** tag add/remove on the edit form (ST-05 AC-05).

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

## 5b. Claude Thesis Generation & Feedback (v0.8 — ST-07 BLG-FE-46)

**Design source:** docs/design/2026-07-02__release-v6.5/thesis-feedback-mechanism/ux_spec.md

> **§13 Compliance:** Generated content is advisory only. The trader may use, edit, or discard it; nothing here gates trade entry or is treated as a recommendation.

Shown in the Setup Thesis field header row (creation and edit form), alongside the local template button:

- **"Generate thesis"** (`generate-thesis-btn`) — client-side template fill from setup type/signal/headlines; no model call.
- **"Improve with AI"** (`improve-with-ai-btn`, shown only when `HAS_AI` and a ticker is set) — calls `POST /trade-plans/generate-plan` (Claude Haiku 4.5; see `docs/specs/api_contracts/ai_thesis_generation.md`), populating Setup Thesis, Entry Rationale, Confirmation Criteria, Early Exit Conditions, Regime Context, and R-Target. Sets `isAiDraft = true` and shows the **"AI draft"** badge (violet, `Sparkles` icon).

### 5b.1 Feedback Control

When an AI draft is present (`isAiDraft = true`, Claude-generated — see spec correction note below), a `👍 Useful` / `👎 Not useful` control renders beneath the field label row. Selecting an option highlights it (`emerald-400` / `rose-400`), disables both options, and shows a transient "Thanks — feedback recorded." confirmation. The control is single-shot per generation: editing the thesis textarea clears `isAiDraft` and hides the control; a fresh "Improve with AI" call re-shows it in the un-rated state.

**Spec correction:** `isAiDraft` was previously set by both the local template button and the Claude-backed button, conflating the two. The feedback control must only ever appear for genuine Claude output — implementation distinguishes this via a Claude-specific draft flag, not the shared `isAiDraft` flag alone. See the design source for full rationale.

Feedback is persisted per generation (recommended: `thesis_feedback` field on the corresponding `claude_audit_log` row, via `POST /trade-plans/{plan_id}/thesis-feedback`) and feeds the `thesis_adoption_rate` metric (`docs/specs/metrics/metrics_definitions.md`, BLG-FEAT-41, ST-08).

### 5b.2 States

| State | Behaviour |
|-------|-----------|
| No AI draft | Feedback control not rendered |
| AI draft present, unrated | Both options shown, clickable |
| Feedback given | Selected option highlighted, both disabled, transient confirmation text |
| Thesis edited after feedback | Control hidden (existing `isAiDraft → false` on edit) |
| Draft regenerated | Feedback control resets to unrated |

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

**Keyboard accessibility (v1.3 — ST-06, BLG-FE-135):** Each `CheckItem` is a real `<button role="checkbox" aria-checked={item.checked}>` (or equivalent `tabIndex`/`role`/`aria-checked`/`onKeyDown` handling) — reachable via Tab in list order, toggleable via Space or Enter, `aria-checked` reflects state. Visual appearance and pre-population behaviour unchanged. Design source: `docs/design/2026-07-30__release-v8.0/entry-checklist-keyboard-accessibility/decision_record.md`.

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

- Shows all plan fields in read-only layout
- Tags shown as pill list below core fields, above Pre-Trade Checklist (§5c)
- Pre-trade checklist shown in read-only state (§6.4)
- Setup Quality Score shown (§7a) if EPIC-02 (PT-04) is in scope
- Action buttons: **"Edit"** (primary) + **"Abandon"** (amber outlined — see §8) + **"Delete"** (destructive, with confirmation) + **"Print / Export PDF"** (see §7c)
- **"Review research"** link present if ticker is set
- When `status = 'abandoned'`: "Abandon" and "Edit" buttons hidden; abandonment reason shown (see §8.3)

---

## 7a. Setup Quality Score (v3.9 — PT-04, conditional EPIC-05 gate)

**Design source:** docs/design/2026-05-21__release-v3.9/setup-quality-score-v2/ux_spec.md
**Supersedes:** v3.7 design (docs/design/2026-05-18__release-v3.7/quality-score-display/ux_spec.md)

**Gate condition:** This section activates only when EPIC-05 is confirmed in scope (Product Owner confirms 20+ closed trades at sprint planning). If gate not confirmed: section not implemented.

> **§13 Compliance:** Display-only score labelled as historical reference ("based on your own trade history"). Not a prediction or recommendation. No automated actions.

### Trade Plan Detail View

Displayed below status badge and core fields, above the Pre-Trade Checklist read-only section.

| Element | Source | Display |
|---------|--------|---------|
| Score badge | `GET /trade-plans/setup-quality-score?ticker={plan.ticker}` → `score` | `{N}/100` + qualitative label pill |
| Qualitative label | `score` | Excellent (≥80, green) / Good (60–79, blue) / Fair (40–59, amber) / Low (<40, red) |
| Gate not met | `gate_not_met: true` | "Insufficient trade history (< 20 trades)" — no badge |
| Sub-label | — | "Based on your own trade history" (muted) |
| Expandable detail | Click badge / info icon | Panel shows: "{N} matching trades found", "{X}% win rate", "{X.X}R average profit" |

**Loading:** inline skeleton placeholder. **Error:** section hidden silently (does not block page).

---

## 7b. Setup Quality Score — Creation Form (v3.9)

**Design source:** docs/design/2026-05-21__release-v3.9/setup-quality-score-v2/ux_spec.md

**Gate condition:** Same as §7a — only when EPIC-05 in scope.

Shown in the Trade Plan creation form (`/trade-plans/new`) as a read-only panel:
- Hidden when ticker field is empty (initial state)
- Displayed after ticker is entered; refetches on ticker change (debounced 500ms)
- Same badge layout and expandable detail as §7a
- Endpoint: `GET /trade-plans/setup-quality-score?ticker={formTicker}`

---

## 7c. Print / Export PDF (v7.6 — ST-01, BLG-FE-119)

**Design source:** docs/design/2026-07-20__release-v7.6/print-pdf-export/ux_spec.md

A **"Print / Export PDF"** action (outline button, `Printer` icon) is shown in the `PageHeader` actions, alongside "Start Trade from Plan" / "Abandon Plan" / "Back", only in the detail view of an existing, loaded plan (`editId && existingPlan`) — not shown on the creation form.

`onClick` calls `window.print()`. No new backend endpoint — output is produced by a shared global print stylesheet (`@media print`), not server-side PDF rendering. The print stylesheet hides the app nav/sidebar and the `PageHeader` actions themselves (none of the action buttons are meaningful on paper), and forces a white background / dark text regardless of the active theme. Printed output shows: page title/description (ticker, market, status badge) and all read-only detail-view content — core fields, tags (§5c), pre-trade checklist read-only state (§6.4), Setup Quality Score if present (§7a).

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

**Focus management (v1.3 — ST-07, BLG-FE-136):** Implemented via the existing Radix-based `src/components/ui/dialog.js` `Dialog` primitive (replacing the prior hand-rolled overlay), giving this modal the same focus-trap behaviour as every other dialog in the app: focus moves into the modal on open, Tab/Shift+Tab cycle only among elements inside it, Escape closes without saving, and focus returns to the triggering "Abandon" button on close. Title, body copy, validation, and actions unchanged. Design source: `docs/design/2026-07-30__release-v8.0/abandon-modal-focus-trap/decision_record.md`.

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

## 10. Start Trade from Plan (v7.2 — ST-03 BLG-FE-109)

**Design source:** docs/design/2026-07-15__release-v7.2/start-trade-from-plan/ux_spec.md
**Depends on:** ST-02 pre-implementation readiness pass (BLG-SPEC-89)

> **§13 Compliance:** Display-only linkage convenience. The trader confirms or edits every field before submitting a trade via the existing manual entry form; no automated trade execution or recommendation is introduced.

### 10.1 Entry Points

A **"Start Trade"** action is added:

- **Detail view:** primary button in the `PageHeader` actions row (left of "Abandon Plan"/"Edit"/"Back"), icon `TrendingUp`, label "Start Trade".
- **List view:** ghost icon button in the Actions column (`h-7 w-7`, matches existing Edit/Delete icon-button pattern), icon `TrendingUp`, positioned first.

**Visibility:** shown only when `status` is `draft`, `research_pending`, `research_complete`, or `entry_conditions_set`. Hidden when `status` is `active` (a position already exists for this plan), `closed`, or `abandoned` — extends the same logic already used to hide the "Abandon" action (§8.1).

### 10.2 Hand-off to Trade Entry

Clicking "Start Trade" navigates to `/TradeEntry` passing `location.state.trade_plan_prefill` — a sibling pattern to the existing `watchlist_prefill` mechanism:

```js
{ trade_plan_id: plan.id, ticker: plan.ticker, market: plan.market, stop_price: plan.stop_level ?? "" }
```

`ticker`, `market`, and `stop_price` pre-populate the entry form (editable); `entry_price`, `shares`, `fill_price`, `fx_rate`, and `atr_value` are not pre-filled — the trader enters live fill terms at execution time, unchanged from the manual flow. `trade_plan_id` is carried in component state (not a visible/editable field) and included automatically in the trade-creation payload on submit — no additional user action required. A non-editable "Linked to trade plan" indicator pill renders below the ticker field for confirmation.

### 10.3 Manual Entry — Optional Linking

Trades started by direct navigation to `/TradeEntry` (no `trade_plan_prefill` state) are unaffected — no indicator, no `trade_plan_id` in the payload. Once a ticker is entered manually, an optional **"Link to trade plan (optional)"** select appears, populated from `GET /trade-plans?ticker={ticker}` filtered to the same non-terminal, non-active statuses as §10.1. The field does not render at all when no eligible plan exists for the ticker (same "hidden entirely when absent" convention as the Signal Context panel, §5a). Selecting a plan sets `trade_plan_id` and shows the same indicator; ticker/market remain read-only in this path since they drove the query.

### 10.4 Regression Risk

No existing `TradeEntry.js` required-field validation (`ticker`, `shares`, `entry_price`) changes — `trade_plan_id` and the optional link selector are additive, outside the existing validity check. The Signal Context panel (§5a, keyed to a linked *signal*) is unrelated and unaffected; both panels may render simultaneously if applicable.

### 10.5 Setup Thesis Digest at Order Placement (v1.4 — ST-02 BLG-FEAT-56)

**Design source:** docs/design/2026-08-11__release-v8.6/ai-thesis-digest-order-placement/ux_spec.md

> **§13 Compliance:** Reuses the already-cleared Claude thesis generation surface (`docs/specs/api_contracts/ai_thesis_generation.md` §13 compliance note). Advisory text only, operator-reviewed; no automated trade decision; does not gate, block, or modify order submission.

A collapsible **"Setup Thesis Digest"** panel renders in `TradeEntry.js`, directly below the "Linked to trade plan" indicator (§10.2) and above the order form fields. **No new AI call is made at order placement** — the panel surfaces the linked plan's already-generated `setup_thesis` content (from the existing "Improve with AI" flow, §5b), not a fresh inference call.

**Visibility:** renders only when `trade_plan_id` is present (via either §10.2's automatic hand-off or §10.3's manual link) **and** the linked plan has non-empty `setup_thesis` and/or `early_exit_conditions` content. Otherwise, does not render at all — same "hidden entirely when absent" convention as §10.3's optional link selector.

**Contents:**
- Header "Setup Thesis Digest" with collapse/expand chevron (default: expanded); violet "AI draft" badge (§5b convention) shown only when the source plan's `isAiDraft` was `true` at generation time.
- **Setup Thesis** — the plan's `setup_thesis`, truncated to 2–3 sentences if longer.
- **Key Risk Factors** — up to 4 bullets synthesised from the plan's `early_exit_conditions` and `confirmation_criteria` fields (2 from each, prioritising non-empty ones). Section omitted if both fields are empty.
- **"View full plan →"** text link to the plan's detail view. No edit affordance — read-only.

**Collapse state:** session-only (not persisted to `localStorage` — distinct from the Behavioural Drift panel's persisted collapse, §20 `analytics.md`, since this panel is seen once per order rather than revisited across sessions).

---

## 11. Bulk Actions (v7.5 — ST-03 BLG-FE-117)

**Design source:** docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md
**Depends on:** docs/specs/blg_fe_117_pre_implementation_readiness_pass.md (batch-mutation endpoint pattern, §13 pre-check PASS)

### Row Selection

A checkbox is added as the first column of the Trade Plan List (§4). The header row gains a header checkbox: checked selects all rows in the current filtered/visible view. Selected rows render with a subtle persistent background tint.

### Bulk-Action Toolbar

Renders above the list only when 1+ rows are selected (no "0 selected" state — toolbar presence is the indicator). Actions: **Bulk Tag**, **Bulk Archive**, **Bulk Delete**.

**Bulk Archive** maps to the existing Abandonment transition (§8) applied to each selected plan — reuses existing single-plan abandonment semantics, not a new status. Any selected plan with `status = 'active'` is excluded from the archive action (mirrors §8.1's single-item hide rule); the toolbar shows `"{N} active plan(s) excluded — cannot be archived."` and archives only the eligible subset.

### Bulk Tag

Inline expand with the existing Tag Editor (§5c), reusing its validation rules. Tags are added to (not replacing) each selected plan's existing `trade_tags`. Submits to the trade-plan bulk-tag endpoint with `{ ids, tags }`.

### Bulk Delete / Bulk Archive — Confirmation

Both destructive. Confirmation dialog: `"{Delete / Archive} {N} selected trade plan(s)?"` — primary destructive button confirms and fires `DELETE /trade-plans/bulk` (`{ ids }`) or the bulk-archive equivalent; "Cancel" dismisses (selection retained).

### Partial-Failure Feedback

Batch response returns `{ succeeded: [...], failed: [{id, reason}] }`. All-succeeded: toast `"{N} plans updated."`, rows updated/removed, selection cleared. Partial failure: toast `"{N} succeeded, {M} failed."` with expandable per-row detail (IDs + reasons) — never a single opaque message.

### §13 Compliance

User-initiated batch of the same manual mutations already available one plan at a time (tag, abandon, delete). No new automated decision-making.

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
| 1.4 | 2026-08-11 | v8.6 design gate — added §10.5 Setup Thesis Digest at Order Placement (ST-02, BLG-FEAT-56): collapsible "Setup Thesis Digest" panel in `TradeEntry.js`, below the "Linked to trade plan" indicator (§10.2); reuses the linked plan's already-generated `setup_thesis` (no new AI call at order placement); "Key Risk Factors" synthesised from `early_exit_conditions`/`confirmation_criteria`; read-only, link to full plan; hidden entirely when no plan linked or no thesis content. §13 compliant (reuses `ai_thesis_generation.md`'s already-cleared generation surface). Design source: ai-thesis-digest-order-placement/ux_spec.md. Approved: Product Owner 2026-08-11. Design gate: 2026-08-11__release-v8.6. Head of Specs Team confirmed. |
| 1.3 | 2026-07-30 | v8.0 design gate — accessibility/interaction fixes to two existing components, visual design unchanged: §6.2 Pre-Trade Entry Checklist `CheckItem` gains real keyboard semantics (`role="checkbox"`, `aria-checked`, Tab-reachable, Space/Enter toggle — ST-06, BLG-FE-135); §8.2 Abandonment Modal migrated to the existing Radix `Dialog` primitive for focus-trap/restoration (ST-07, BLG-FE-136). Design sources: entry-checklist-keyboard-accessibility/decision_record.md, abandon-modal-focus-trap/decision_record.md. Approved: Product Owner 2026-07-30. Design gate: 2026-07-30__release-v8.0. Head of Specs Team confirmed. |
| 1.2 | 2026-07-20 | v7.6 design gate — added §7c Print / Export PDF (ST-01, BLG-FE-119): "Print / Export PDF" outline button in the detail-view PageHeader actions, `window.print()`-based (shared global print stylesheet, no new backend endpoint); §7 action buttons row updated. Design source: print-pdf-export/ux_spec.md. Approved: Product Owner 2026-07-20. Design gate: 2026-07-20__release-v7.6. Head of Specs Team confirmed. |
| 1.1 | 2026-07-17 | v7.5 design gate — added §11 Bulk Actions (ST-03, BLG-FE-117): row checkboxes on the list, bulk-action toolbar (renders only when 1+ selected), Bulk Tag (reuses §5c Tag Editor), Bulk Archive (reuses §8 Abandonment, active plans excluded), Bulk Delete (destructive, confirmation required), per-row partial-failure feedback. New bulk-mutation endpoints. Design source: bulk-actions-toolbar/ux_spec.md. Approved: Product Owner 2026-07-17. Design gate: 2026-07-17__release-v7.5. Head of Specs Team confirmed. |
| 1.0 | 2026-07-15 | v7.2 design gate — added §10 Start Trade from Plan (ST-03, BLG-FE-109): "Start Trade" action on detail view (primary button) and list view (icon button), visible only for non-active/non-terminal plans; hands off to `/TradeEntry` via a new `trade_plan_prefill` navigation-state object (sibling to existing `watchlist_prefill`) pre-filling ticker/market/stop; `trade_plan_id` carried automatically, non-editable "Linked to trade plan" indicator shown; manual entry gains an optional "Link to trade plan" selector when an eligible plan exists for the entered ticker. No change to existing required-field validation. Depends on ST-02 readiness pass (BLG-SPEC-89). Design source: start-trade-from-plan/ux_spec.md. Approved: Product Owner 2026-07-15. Head of Specs Team confirmed. |
| 0.9 | 2026-07-08 | v6.8 design gate — added §5c Trade Plan Tags (ST-05, BLG-FEAT-52): new independent `trade_tags` field on `trade_plans` (data-independent from existing position/journal tags), Tag Editor on edit form, Tag List (read-only) on detail view, new `GET /trade-plans/tags` autocomplete endpoint. Reuses `journal_components.md` §4 Tag Editor and §1-equivalent pill display for visual consistency only. §5.1 form fields table and §7 detail view updated. Design source: trade-tagging/ux_spec.md. Approved: Product Owner 2026-07-08. Head of Specs Team confirmed. |
| 0.8 | 2026-07-02 | v6.5 design gate — added §5b Claude Thesis Generation & Feedback (ST-07, BLG-FE-46): documents the previously-unspecified "Improve with AI" button (Claude Haiku 4.5, `POST /trade-plans/generate-plan`) and a new 👍/👎 feedback control on generated drafts, single-shot per generation, feeding `thesis_adoption_rate` (ST-08). Notes a spec correction: the shared `isAiDraft` flag conflates the local template button and the Claude-backed button — implementation must gate the feedback control on a Claude-specific signal. Design source: thesis-feedback-mechanism/ux_spec.md. Approved: Product Owner 2026-07-02. Head of Specs Team confirmed. |
| 0.7 | 2026-05-21 | v3.9 design gate — updated §7a Setup Quality Score (ST-14, conditional EPIC-05): endpoint changed to ticker-based `GET /trade-plans/setup-quality-score?ticker={plan.ticker}`; qualitative labels added (Excellent/Good/Fair/Low); expandable detail panel (matching_trades, win_rate, average_R); gate_not_met message replaces "N/A" text. Added §7b: score panel in creation form (shown after ticker entered, debounced refetch). Design source: setup-quality-score-v2/ux_spec.md. Approved: Product Owner 2026-05-21. Head of Specs Team confirmed. |
| 0.6 | 2026-05-18 | v3.7 design gate — added §7a Setup Quality Score (PT-04: score display on detail view, 0–100 or "N/A — insufficient history", §13 compliant). Conditional on EPIC-02 gate. Design source: quality-score-display/ux_spec.md. Approved: Product Owner 2026-05-18. |
| 0.5 | 2026-05-18 | v3.7 design gate — added §5a Signal Context Panel (BLG-FE-34: read-only signal data panel in creation form; pre-population of rationale and stop fields; conditional on linked signal). Design source: signal-context-panel/ux_spec.md. Approved: Product Owner 2026-05-18. |
| 0.4 | 2026-05-14 | BLG-SPEC-28 (ST-13, v3.4) — corrected §6.2 pre-population rules: CHK-03 uses `early_exit_conditions` (not `stop_level`); CHK-04 uses `r_target` (not `risk_reward_notes`). Added rationale note and test scenario cross-reference. Authority: Head of Specs Team. |
| 0.3 | 2026-05-09 | v3.3 design gate — added §8 Trade Plan Abandonment (BLG-FEAT-21: abandon action, modal, abandoned display); added §9 Status Badge Scheme (BLG-FE-30: 7-state badge set including Abandoned). Design source: trade-plan-quick-wins/ux_spec.md §A, §B. Approved: Product Owner 2026-05-09. |
| 0.2 | 2026-05-05 | v3.2 design gate — added Pre-Trade Entry Checklist section (§6) for EPIC-02 (ST-05, ST-06). Design source: pre-trade-entry-checklist/ux_spec.md. Also: initial file creation (recovering v3.1 gap — trade_plan.md v0.1 was stated as created in v3.1 design gate but not committed). |
| 0.1 | 2026-04-29 | Initial spec intent — v3.1 design gate (ST-03 — Trade Plan creation flow + detail view). File not committed at the time; recovered at v3.2. |
