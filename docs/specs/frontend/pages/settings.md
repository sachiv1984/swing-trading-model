# settings.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 1.8
**Last Updated:** 2026-10-06 (ST-01, EPIC-01, v9.10, BLG-BE-138 — ruling (a) applied: the four Strategy Parameters are read-only §11 values; branches (b)/(c) removed); prior — 2026-10-06 (v9.10 design gate — ruling-conditional editability presentation); prior — 2026-07-24
**Design Source (§1 Strategy Parameter Editability):** docs/design/2026-10-06__release-v9.10/stop-parameter-settings-presentation/decision_record.md
**Design Source (§6a AI Spend Trend Chart):** docs/design/2026-07-24__release-v7.8/ai-spend-trend-chart/ux_spec.md
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

> Minimum Hold Days, ATR Period and the two ATR multiples are the backtest-optimised `strategy_rules.md` §11 values (26.37% CAGR, 1.29 Sharpe, −25.38% max drawdown). Since v9.10 (ST-01, parameter-authority ruling (a)) they are fixed and shown read-only. They change only through a §12.3 strategy change. Default Risk % stays an editable user preference.

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

#### Strategy Parameter Presentation (v9.10 — ST-01, BLG-BE-138, ruling (a))

- The four Strategy Parameters (Minimum Hold Days `10`, ATR Period `14`, Initial Stop `5.0`, Trailing Stop `2.0`) render as **read-only values, not disabled inputs**, with their existing labels and helper text (`data-testid="strategy-param-{min-hold-days|atr-period|atr-multiplier-initial|atr-multiplier-trailing}"`).
- Caption under the section header (`data-testid="strategy-params-fixed-caption"`): "These parameters are fixed by the strategy rules (§11) and are shown for reference."
- The displayed values come from `src/lib/strategyParameters.js`, the display mirror of the backend source `backend/utils/strategy_parameters.py`; `tests/test_strategy_parameter_parity.py` fails if the two drift. The values no longer come from the settings row, so a stored row cannot show a different number.
- Save omits these four fields. Any values still stored in the `settings` row are ignored by every stop path (`settings_endpoints.md`).
- Default Risk % stays editable.

> **Important:** Changes to `default_risk_percent` take effect on the next load of the Trade Entry page. No positions are affected.

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
| 1.8 | 2026-10-06 | ST-01 (EPIC-01, BLG-BE-138): parameter-authority ruling (a), 2026-10-06 (`ESC-EXEC-20261006-01`). The four Strategy Parameters are read-only §11 values with the fixed caption; Save omits them. The ruling-conditional (b)/(c) branches are removed, as the design record requires. The Important note no longer says strategy-parameter changes take effect on the next analyze call. |
| 1.7 | 2026-10-06 | v9.10 design gate — ST-01 (EPIC-01, BLG-BE-138): §1 gains Strategy Parameter Fallbacks and Editability. Fallbacks must equal the §11 values; editability is presented per the pending ST-01 parameter-authority ruling (a/b/c branches). Design source: `docs/design/2026-10-06__release-v9.10/stop-parameter-settings-presentation/decision_record.md`. Head of UX & Design sign-off: 2026-10-06. Product Owner approved: 2026-10-06. Head of Specs Team confirmed. |
| 1.6 | 2026-07-24 | v7.8 design gate — ST-06 (EPIC-06, BLG-FEAT-82): §6a AI Spend Trend Chart added below the current-month figure, inside the existing §6 card — bar chart of Claude API spend across the last 6 release cycles (or fewer if less history exists), reusing the `analytics.md` §12 Win Rate by Month fixed-axis bar chart pattern. Naming resolved: chart shows Claude spend only (no separate Gemini stream exists, per v1.5 reframing). New spend-by-cycle aggregation endpoint required (not new data collection) — flagged as a sprint-execution implementation dependency requiring an API contract entry in the same commit. Design source: `docs/design/2026-07-24__release-v7.8/ai-spend-trend-chart/ux_spec.md`. Head of UX & Design sign-off: 2026-07-24. Product Owner approved: 2026-07-24. Head of Specs Team confirmed. |
| 1.5 | 2026-07-20 | v7.6 sprint execution (ST-07, EPIC-07, BLG-FEAT-77) — reframed §6 per `ESC-EXEC-20260720-01`: title changed from "AI Usage & Costs" to "Claude API Usage & Costs"; removed the Gemini row and client-side Combined Total (both premised on a Gemini provider that does not exist in this codebase — `gemini_service.py` calls only the Anthropic Claude API); now shows a single `GET /ai/monthly-cost` figure. Sprint Execution Engine, agent-mediated Director of Quality sign-off. |
| 1.4 | 2026-07-20 | v7.6 design gate — added §6 AI Usage & Costs (ST-07, BLG-FEAT-77): read-only SectionCard showing Gemini + Claude current-month spend and a client-side-summed Combined Total; independent query, excluded from Save Settings scope. Sections list corrected to include the pre-existing Risk Limits section (previously missing from the top-of-file summary). Design source: consolidated-ai-cost-view/ux_spec.md. Approved: Product Owner 2026-07-20. Design gate: 2026-07-20__release-v7.6. Head of Specs Team confirmed. |
