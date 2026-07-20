# settings.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 1.5
**Last Updated:** 2026-07-20
**Design Source (§6 AI Usage & Costs):** docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md (v1.1 addendum)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Purpose & User Goals
The Settings page allows users to configure **strategy parameters**, **trading fees**, **UI preferences**, **analytics thresholds**, and **risk limits** that control how the Position Manager Web App behaves and calculates results.

Users should be able to:
- Adjust core strategy settings (minimum hold days, ATR parameters, stop multipliers).
- Set the default risk percentage pre-populated in the Position Sizing Calculator.
- Configure commissions, stamp duty, and FX fee rates used in cost and P&L calculations.
- Set the theme preference.
- Define the minimum number of trades required before analytics are displayed.
- Configure concentration alert thresholds for position and sector risk limits.
- Save settings with clear, immediate feedback that changes have been applied.
- View Claude API spend for the current month at a glance (read-only, v7.6).

---

## Layout Structure

### Page Header
- **Title:** `Settings`
- **Description:** "Configure your strategy parameters and preferences"
- **Primary action:** `Save Settings` button, with dynamic label:
  - `Save Settings` (idle)
  - `Saving...` (while mutation is in progress)
  - `Saved!` (short success state)

### Content Layout
- Page is constrained to a single column, centered, `max-w-2xl` width with vertical spacing between sections.
- Main content is grouped into **SectionCards**, each with:
  - Icon
  - Title
  - Colored icon background
  - Form fields and helper text inside

Sections:

1. **Strategy Parameters**
2. **Commission & Fees**
3. **Preferences** (theme)
4. **Risk Limits** (concentration alert thresholds)
5. **Analytics** (minimum trades for analytics)
6. **AI Usage & Costs** (read-only, v7.6 — see §6 below)

---

## Key Components Used

- **PageHeader** – main title, description, and Save button actions.
- **SectionCard** – reusable layout wrapper with motion/animation, icon, title, and content.
- **Form Controls**:
  - `Input` for numeric values (days, multipliers, commissions, rates, thresholds, risk percent).
  - `Select` for `theme`.
  - `Label` and small helper text for each field.
- **Save Button** (`Button`):
  - Shows `Loader2` icon when saving
  - Shows `CheckCircle2` icon on success
  - Disabled during save mutation

---

## Settings Groups & Fields

### 1. Strategy Parameters

These values define the core risk model, stop logic, and position sizing defaults.

> These defaults are the backtest-optimised values (26.37% CAGR, 1.29 Sharpe, −25.38% max drawdown). Users should understand the strategy rationale before changing them.

**Fields:**

- **Minimum Hold Days**
  - Type: number
  - Default: `10`
  - Helper text: "Days before stop can trail"
  - Used as the *grace period* before trailing stops become active. With the default of `10`, grace covers days 0–9 inclusive; day 10 is the first day stop logic is active. In general, grace covers days `0` through `min_hold_days − 1`.

- **ATR Period**
  - Type: number
  - Default: `14`
  - Helper text: "Lookback for ATR calculation"

- **Initial Stop (ATR Multiple)**
  - Type: number, step `0.1`
  - Default: `5.0`
  - Helper text: "e.g., 5 = Entry − 5×ATR (wide stop for losing positions)"
  - Applied to positions that are at a loss to give room to recover.

- **Trailing Stop (ATR Multiple)**
  - Type: number, step `0.1`
  - Default: `2.0`
  - Helper text: "e.g., 2 = High − 2×ATR (tight trailing stop for profitable positions)"
  - Applied to positions that are profitable to protect gains.

- **Default Risk %**
  - Type: number, step `0.01`, min `0.01`, max `100`
  - Default: `1.00`
  - Helper text: "Pre-filled in the Position Sizing Calculator on trade entry. This is your default — you can override it per trade."
  - Maps to `default_risk_percent` in `GET /PUT /settings`.
  - This is a **user preference default**, not an enforced limit. The user may type any valid risk percentage on any individual trade entry without restriction.
  - Stored as `DECIMAL(4,2)` — accepts up to two decimal places (e.g. `1.50`, `0.75`).
  - Constraint: must be `> 0` and `<= 100`. Values outside this range are rejected by the API with a `400`.

> **Important:** Changes to strategy parameters take effect on the **next** call to `GET /positions/analyze`. Open positions are not retroactively affected. Changes to `default_risk_percent` take effect immediately on the next load of the Trade Entry page — no positions are affected.

---

### 2. Commission & Fees

These fields define the fee assumptions used in Trade Entry and Exit previews.

**Fields:**

- **UK Commission (£)**
  - Type: number, step `0.01`
  - Default: `9.95`

- **US Commission ($)**
  - Type: number, step `0.01`
  - Default: `0`

- **UK Stamp Duty Rate**
  - Type: number, step `0.001`
  - Default: `0.005` (0.5%)
  - Helper text: "Default: 0.005 (0.5%)"

- **US FX Fee Rate**
  - Type: number, step `0.0001`
  - Default: `0.0015` (0.15%)
  - Helper text: "Default: 0.0015 (0.15%)"

> Fee changes apply to new transactions only. Existing trade history is not recalculated.

---

### 3. Preferences

Preferences control how the interface is presented.

**Fields:**

- **Theme**
  - Type: select
  - Options: `dark`, `light`
  - Default: `dark`

> **`default_currency`** is a stored field (`GBP` only) that is not user-configurable via this UI. Multi-currency support is position-level (USD positions are tracked in native currency), not portfolio-level. The backend will reject any value other than `"GBP"` if submitted.

---

### 4. Risk Limits

Configures the concentration alert thresholds shown on the Positions page. When a breach is detected, a warning banner appears with a link back to this section.

**Fields:**

- **Position Concentration Limit (%)**
  - Type: number, integer, `min=1`, `max=100`
  - Default: `15`
  - Helper text: "Alert when 1 position exceeds this % of total portfolio heat (default: 15%)"
  - Maps to `concentration_position_threshold_pct` in settings. Read by `GET /portfolio/concentration-status`.

- **Sector Concentration Limit (%)**
  - Type: number, integer, `min=1`, `max=100`
  - Default: `30`
  - Helper text: "Alert when 1 sector exceeds this % of total portfolio heat (default: 30%)"
  - Maps to `concentration_sector_threshold_pct` in settings. Read by `GET /portfolio/concentration-status`.

> Threshold changes take effect on the next poll of `GET /portfolio/concentration-status` (every 2 minutes on the Positions page).

---

### 5. Analytics

Configures when analytics become meaningful enough to display.

**Fields:**

- **Minimum Trades for Analytics**
  - Type: number, integer, `min=1`
  - Default: `10`
  - Helper text: "Minimum number of closed trades required to display analytics"

Analytics views show only once this threshold is met, avoiding misleading statistics on very small samples.

> **Analytics page default period note:** The Analytics page explicitly passes `period=last_month` on initial load as a UX decision — it does not rely on the API's default (`all_time`). This is intentional: `last_month` presents a meaningful recent window rather than the full historical dataset on first view. `all_time` remains available as a user-selectable option on the Analytics page. This note is here because the `min_trades_for_analytics` threshold applies across all period selections; a user who has enough trades all-time may not meet the threshold for `last_month`.

---

### 6. Claude API Usage & Costs (v7.6 — ST-07, BLG-FEAT-77)

**Design source:** docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md (v1.1 addendum)

**Reframed per `ESC-EXEC-20260720-01`:** the original design assumed Gemini and Claude were two separate cost-generating providers, sourced from `gemini_audit_log` and a Claude equivalent respectively, summed into a "Combined Total." Tracing the actual implementation during sprint execution found this codebase integrates only the Anthropic Claude API — `gemini_service.py` (despite its filename) calls only `anthropic`, and no `google-generativeai` package or `GEMINI_API_KEY` exists anywhere in the codebase. `gemini_audit_log` and `claude_audit_log` both log the *same* Claude spend event per call, not two providers' independent costs. The original design would have double-counted one real cost stream as two. This section now shows a single Claude API total.

A **read-only** section showing Claude API spend for the current calendar month. Unlike sections 1–5, this section has no form fields and does not participate in the `Save Settings` mutation — it loads via its own independent query and is excluded from the Save button's scope.

**Fields (read-only):**

| Row | Source | Format |
|-----|--------|--------|
| Claude API spend (current month) | `GET /ai/monthly-cost` — aggregates `claude_audit_log.cost_usd` for the current calendar month | `$X.XX`, bold |

**Loading:** inline skeleton within the card only — does not block the rest of the Settings page.
**Error:** card shows "AI cost data unavailable" — no numeric fallback is rendered (never shown as `$0.00` or `—`); rest of the page is unaffected.

---

## Data Behavior

### Loading Existing Settings
- On load, a query retrieves settings via `GET /settings`.
- The response is an array containing a single settings object (`settings[0]`).
- The form is initialized with a merge of defaults and the stored record.
- If no settings exist, the form is initialized with defaults only.
- `default_risk_percent` defaults to `1.00` if not present in the stored record.
- `concentration_position_threshold_pct` defaults to `15` if not present in the stored record.
- `concentration_sector_threshold_pct` defaults to `30` if not present in the stored record.

### Saving Settings
- On save:
  - If `formData.id` exists, a `PUT /settings` update call is made.
  - Otherwise, a create call is made (first time settings are saved).
- On success:
  - Settings query is invalidated/refetched.
  - A success toast appears: "Settings saved successfully".
  - Button temporarily shows "Saved!".

---

## States

### Loading State
- When `isLoading` is true or `formData` is not yet created:
  - The page shows a centered spinner with muted text.
  - No inputs are visible yet.

### Ready State
- When `formData` is available: all SectionCards render with fields populated from `formData`.

### Saving State
- While a save mutation is in progress: Save button is disabled, shows spinner + "Saving…".

### Saved State
- After successful save: button shows icon + "Saved!" briefly, toast notifies the user.

### Error State
- If saving fails: global banner / toast informs the user. Form data is preserved.

---

## Responsive Behavior
- Container is `max-w-2xl` and centered — naturally responsive.
- Field groups use `grid grid-cols-2 gap-4`, stacking to a single column on smaller viewports.

---

## UX Notes
- Defaults match the canonical strategy parameters. Users can adopt them without changes.
- Helper text clarifies how each parameter is used (ATR multipliers, stamp duty, FX fee, analytics threshold, risk percent default).
- The `default_risk_percent` field helper text makes clear it is a convenience default, not a hard limit — users retain full control per trade.
- Grouping into Strategy Parameters, Commission & Fees, Preferences, Risk Limits, Analytics, and (v7.6) AI Usage & Costs mirrors the domain model.
- Save feedback (button state + toast) confirms changes are persisted and applied.
- AI Usage & Costs (§6) is read-only monitoring, not configuration — deliberately placed last and excluded from Save, so its presence doesn't imply the figures are editable.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.5 | 2026-07-20 | v7.6 sprint execution (ST-07, EPIC-07, BLG-FEAT-77) — reframed §6 per `ESC-EXEC-20260720-01`: title changed from "AI Usage & Costs" to "Claude API Usage & Costs"; removed the Gemini row and client-side Combined Total (both premised on a Gemini provider that does not exist in this codebase — `gemini_service.py` calls only the Anthropic Claude API); now shows a single `GET /ai/monthly-cost` figure. Sprint Execution Engine, agent-mediated Director of Quality sign-off. |
| 1.4 | 2026-07-20 | v7.6 design gate — added §6 AI Usage & Costs (ST-07, BLG-FEAT-77): read-only SectionCard showing Gemini + Claude current-month spend and a client-side-summed Combined Total; independent query, excluded from Save Settings scope. Sections list corrected to include the pre-existing Risk Limits section (previously missing from the top-of-file summary). Design source: consolidated-ai-cost-view/ux_spec.md. Approved: Product Owner 2026-07-20. Design gate: 2026-07-20__release-v7.6. Head of Specs Team confirmed. |
