# settings.md

## Purpose & User Goals
The Settings page allows users to configure **strategy parameters**, **trading fees**, **UI preferences**, and **analytics thresholds** that control how the Position Manager Web App behaves and calculates results.

Users should be able to:
- Adjust core strategy settings (minimum hold days, ATR parameters, stop multipliers).
- Configure commissions, stamp duty, and FX fee rates used in cost and P&L calculations.
- Set the theme preference.
- Define the minimum number of trades required before analytics are displayed.
- Save settings with clear, immediate feedback that changes have been applied.

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
4. **Analytics** (minimum trades for analytics)

---

## Key Components Used

- **PageHeader** – main title, description, and Save button actions.
- **SectionCard** – reusable layout wrapper with motion/animation, icon, title, and content.
- **Form Controls**:
  - `Input` for numeric values (days, multipliers, commissions, rates, thresholds).
  - `Select` for `theme`.
  - `Label` and small helper text for each field.
- **Save Button** (`Button`):
  - Shows `Loader2` icon when saving
  - Shows `CheckCircle2` icon on success
  - Disabled during save mutation

---

## Settings Groups & Fields

### 1. Strategy Parameters

These values define the core risk model and stop logic.

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

> **Important:** Changes to strategy parameters take effect on the **next** call to `GET /positions/analyze`. Open positions are not retroactively affected.

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

### 4. Analytics

Configures when analytics become meaningful enough to display.

**Fields:**

- **Minimum Trades for Analytics**
  - Type: number, integer, `min=1`
  - Default: `10`
  - Helper text: "Minimum number of closed trades required to display analytics"

Analytics views show only once this threshold is met, avoiding misleading statistics on very small samples.

> **Analytics page default period note:** The Analytics page explicitly passes `period=last_month` on initial load as a UX decision — it does not rely on the API's default (`all_time`). This is intentional: `last_month` presents a meaningful recent window rather than the full historical dataset on first view. `all_time` remains available as a user-selectable option on the Analytics page. This note is here because the `min_trades_for_analytics` threshold applies across all period selections; a user who has enough trades all-time may not meet the threshold for `last_month`.

---

## Data Behavior

### Loading Existing Settings
- On load, a query retrieves settings via `GET /settings`.
- The response is an array containing a single settings object (`settings[0]`).
- The form is initialized with a merge of defaults and the stored record.
- If no settings exist, the form is initialized with defaults only.

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
- Helper text clarifies how each parameter is used (ATR multipliers, stamp duty, FX fee, analytics threshold).
- Grouping into Strategy Parameters, Commission & Fees, Preferences, and Analytics mirrors the domain model.
- Save feedback (button state + toast) confirms changes are persisted and applied.
