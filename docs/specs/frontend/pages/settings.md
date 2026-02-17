# settings.md

## Purpose & User Goals
The Settings page allows users to configure **strategy parameters**, **trading fees**, **UI preferences**, and **analytics thresholds** that control how the Position Manager Web App behaves and calculates results. 

Users should be able to:
- Adjust core strategy settings (minimum hold days, ATR parameters, stop multipliers). 
- Configure commissions, stamp duty, and FX fee rates used in cost and P&L calculations. 
- Set the default display currency and theme preference. 
- Define the minimum number of trades required before analytics are displayed (from the Settings implementation code).  
- Save settings with clear, immediate feedback that changes have been applied (from the Settings implementation code).

---

## Layout Structure

### Page Header
- **Title:** `Settings` (from Settings component code)  
- **Description:** “Configure your strategy parameters and preferences” (from Settings component code)  
- **Primary action:** `Save Settings` button, with dynamic label:
  - `Save Settings` (idle)
  - `Saving...` (while mutation is in progress)
  - `Saved!` (short success state)  
  (From Settings implementation code.)

### Content Layout
- Page is constrained to a single column, centered, with a `max-w-2xl` width and vertical spacing between sections (from Settings implementation code).
- Main content is grouped into **SectionCards**, each with:
  - Icon
  - Title
  - Colored icon background
  - Form fields and helper text inside  
  (From Settings implementation code.)

Sections:

1. **Strategy Parameters** 
2. **Commission & Fees** 
3. **Preferences** (default currency and theme) 
4. **Analytics** (minimum trades for analytics) (from Settings implementation code)

---

## Key Components Used

- **PageHeader** – provides the main title, description, and Save button actions (from Settings implementation code).  
- **SectionCard** – reusable layout wrapper with motion/animation, icon, title, and content (from Settings implementation code).  
- **Form Controls**:
  - `Input` for numeric values (days, multipliers, commissions, rates, thresholds). 
  - `Select` for `default_currency` and `theme`. 
  - `Label` and small helper text for each field (from Settings implementation code).  
- **Save Button** (`Button`):
  - Shows `Loader2` icon when saving
  - Shows `CheckCircle2` icon on success
  - Disabled during save mutation  
  (From Settings implementation code.)

---

## Settings Groups & Fields

### 1. Strategy Parameters

These values define the core risk model and stop logic. 

**Fields:**

- **Minimum Hold Days**
  - Type: number  
  - Default: `5` (from defaults object and spec minimum hold days) 
  - Helper text: “Days before stop can trail” (from Settings implementation code).  
  - Used as the *grace period* before trailing stops become active. 

- **ATR Period**
  - Type: number  
  - Default: `14` (from defaults and spec ATR period) 
  - Helper text: “Lookback for ATR calculation” (from Settings implementation code).  

- **Initial Stop (ATR Multiple)**
  - Type: number, step `0.1`  
  - Default: `2` (from defaults and spec ATR multiplier initial) 
  - Helper text: “e.g., 2 = Entry - 2×ATR” (from Settings implementation code).  

- **Trailing Stop (ATR Multiple)**
  - Type: number, step `0.1`  
  - Default: `3` (from defaults and spec ATR multiplier trailing) 
  - Helper text: “e.g., 3 = High - 3×ATR” (from Settings implementation code).  

These values align with the strategy parameters described in the original specification (minimum hold days, ATR multipliers, ATR period). 

---

### 2. Commission & Fees

These fields define the fee assumptions used in Trade Entry and Exit previews. 

**Fields:**

- **UK Commission (£)**
  - Type: number, step `0.01`  
  - Default: `9.95` (matches spec UK commission) 

- **US Commission ($)**
  - Type: number, step `0.01`  
  - Default: `0` (matches spec US commission) 

- **UK Stamp Duty Rate**
  - Type: number, step `0.001`  
  - Default: `0.005` (0.5%) 
  - Helper text: “Default: 0.005 (0.5%)” (from Settings implementation code).  

- **US FX Fee Rate**
  - Type: number, step `0.0001`  
  - Default: `0.0015` (0.15%) 
  - Helper text: “Default: 0.0015 (0.15%)” (from Settings implementation code).  

These settings correspond to the “Trading Fees” section defined in the original specs (UK commission, US commission, stamp duty rate, FX fee rate). 

---

### 3. Preferences

Preferences control how values and the interface are presented. 

**Fields:**

- **Default Currency**
  - Type: select  
  - Options: `GBP (£)`, `USD ($)` (from Settings implementation code)  
  - Default: `GBP` (matches spec default currency) 

- **Theme**
  - Type: select  
  - Options: `dark`, `light` (from Settings implementation code)  
  - Default: `dark` (matches spec default dark mode with optional light mode) 

These map directly to “UI Preferences: Default currency (GBP), Theme preference (Dark/Light)” from the original settings specification. 

---

### 4. Analytics

Configures when analytics become meaningful enough to display.

**Fields:**

- **Minimum Trades for Analytics**
  - Type: number, integer, `min=1`  
  - Default: `10` (from defaults and code: `min_trades_for_analytics: 10`)  
  - Helper text: “Minimum number of closed trades required to display analytics” (from Settings implementation code).  

Analytics views (e.g., Analytics page) should only surface once this threshold is met, avoiding misleading statistics on very small samples.

---

## Data Behavior

### Loading Existing Settings
- On load, a query retrieves settings via `base44.entities.Settings.list()` (corresponding to `GET /settings`). 
- If a settings record exists (`settings[0]`), the form is initialized with a merge of **defaults** and that record.  
- If no settings exist, the form is initialized with **defaults** only. (From Settings implementation code.)

### Saving Settings
- On save:
  - If `formData.id` exists, an update call is made (aligns with `PUT /settings`). 
  - Otherwise, a create call is made (first time settings are saved).  
- On success:
  - Settings query is invalidated/refetched.  
  - A success toast appears: “Settings saved successfully”.  
  - Button temporarily shows “Saved!”.  
  (From Settings implementation code.)

---

## States

### Loading State
- When `isLoading` is true or `formData` is not yet created:
  - The page shows a centered spinner (`Loader2`) with muted text color.  
  - No inputs are visible yet.  
  (From Settings implementation code.)

### Ready State
- When `formData` is available:
  - All SectionCards render with their fields populated from `formData`.  

### Saving State
- While a save mutation is in progress:
  - Save button is disabled.  
  - Label shows spinner + “Saving…”.  
  (From Settings implementation code.)

### Saved State
- After a successful save:
  - Button shows icon + “Saved!” for a short duration.  
  - Toast notifies the user that settings were saved.  
  (From Settings implementation code.)

### Error State
- If saving fails, the implementation uses the same error‑handling pattern as the rest of the app (global banner / toast) to inform the user, without clearing form data. 

---

## Responsive Behavior
- Page container is `max-w-2xl` and centered, making the layout naturally responsive. (From Settings implementation code.)  
- Field groups use `grid grid-cols-2 gap-4`, which will stack in a single column on smaller viewports following the app’s standard responsive behavior (forms stack vertically on mobile). 

---

## UX Notes
- Defaults are sensible and match the original specification, so users can adopt recommended settings without changes. 
- Helper text clarifies *how* each parameter is used (e.g., ATR multipliers, stamp duty rate, FX fee rate, analytics threshold). (From Settings implementation code.)  
- Grouping settings into **Strategy Parameters**, **Commission & Fees**, **Preferences**, and **Analytics** mirrors the domain model and helps users understand impact. 
- Save feedback (button state + toast) reassures users that configuration changes are persisted and applied. (From Settings implementation code.)  

---
