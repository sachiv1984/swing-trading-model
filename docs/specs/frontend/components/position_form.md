# position_form.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Status:** Canonical
**Version:** 1.2
**Last Updated:** 2026-02-19

## Purpose & Usage Context
The Position Form is used to manually create a new position in the portfolio.
It supports both UK and US markets, with dynamic fields that adjust based on the detected market.
This form appears on the Trade Entry page and is one of the core data‑entry workflows of the application.

Users rely on this form to:
- Enter accurate trade details
- Use the Position Sizing Calculator to determine the right share quantity
- Capture journal context at entry
- Apply strategy tags
- Review calculated fees and stop levels before confirming

---

## Inputs (Conceptual Props)

### Ticker (required)
- Text input
- Auto‑uppercase
- Market auto‑detected based on suffix (e.g., `.L` for UK)
- Max 20 characters

### Entry Date (required)
- Date picker
- Default: today
- Must not be in the future

### Entry Price (required)
- Number input
- In the position's native currency (GBP for UK, USD for US)
- Max 2 decimal places

### FX Rate (conditional)
- Only shown for US stocks
- Auto‑fetched but editable
- Format: 1.XXXX
- Max 6 decimal places

### ATR Value (optional)
- Number input
- Auto‑calculated if available
- User may override

### Stop Price (optional)
- Number input
- Auto‑calculated as: `entry_price - (5 × ATR)`
- User may override

### Position Sizing Calculator (always visible)
See **Position Sizing Calculator** section below.

### Shares (required)
- Number input
- Supports fractional values (e.g., 5.5)
- Minimum 0.0001
- Max 4 decimal places
- May be auto-filled by the Position Sizing Calculator

### Entry Note (optional)
- Text area
- Max 500 characters
- Character counter displayed
- Helps document reasoning, setup, risk, sentiment

### Tags (optional)
- Tag input with autocomplete
- Displayed as pills with remove icon
- Press Enter to add
- Valid tags: lowercase letters, numbers, hyphens
- Max 10 tags total
- Max 20 characters per tag

---

## Form Field Order

Fields render in this sequence:

1. Ticker
2. Entry Date
3. Entry Price + FX Rate (US only, side by side)
4. ATR Value
5. Stop Price
6. **Position Sizing Calculator widget** (always visible, directly above Shares)
7. Shares
8. Entry Note
9. Tags
10. Submit / Cancel

The widget's placement directly above Shares is intentional — it makes the relationship between the suggestion and the target field visually immediate.

---

## Position Sizing Calculator

### Purpose
An always-visible panel within the form that calculates the suggested share quantity based on the user's risk appetite and the trade setup. It calls `POST /portfolio/size` on a debounced basis as the user types. The result auto-fills the Shares field when conditions are met.

The calculator is decision support — it does not block form submission regardless of its state.

### Widget inputs
- **Risk %** — number input, pre-populated from `settings.default_risk_percent` on form load. Editable by the user within the widget. Represents percentage of portfolio value to risk on this trade (e.g. `1.00` = 1%).
- **Entry Price, Stop Price, FX Rate** — read passively from the corresponding form fields above. The widget does not duplicate these inputs.

### Calculation trigger
The widget calls `POST /portfolio/size` 300ms after the user stops typing in any of: Entry Price, Stop Price, FX Rate, or the Risk % field within the widget. The frontend owns and implements the debounce. The backend performs all calculations — the frontend must not derive or recalculate any returned value.

### Widget output fields
When the result is valid, the widget displays:

| Field | Description |
|-------|-------------|
| Suggested shares | Returned as `suggested_shares` (4dp from backend; display to 2dp) |
| Risk amount | `risk_amount` in GBP |
| Estimated cost | `estimated_cost` in GBP |
| Available cash | `available_cash` in GBP |

---

### Widget States

#### Idle
Shown when Entry Price or Stop Price is empty or zero. No API call is made.
- Output values display as `—`
- Risk % field is visible and editable
- No "Use suggested shares" button shown

#### Loading
Shown during the debounce window and while awaiting the API response.
- Output value areas show a shimmer/pulse animation
- Risk % field remains editable
- No "Use suggested shares" button shown
- Minimum display duration: 150ms (prevents flash for fast responses)

#### Valid — Shares field empty
`valid: true`, `cash_sufficient: true`, Shares field is empty.
- All four output values shown
- Shares field is **auto-filled** immediately with `suggested_shares`
- Shares field shows a brief background highlight transition (150ms fade) to signal it was just populated
- No "Use suggested shares" button shown

#### Valid — Shares field already has a value
`valid: true`, `cash_sufficient: true`, user has already manually entered a value in Shares.
- All four output values shown
- Shares field is **not overwritten**
- **"Use suggested shares"** button appears at the bottom of the widget
  - Label: `Use X.XX suggested shares`
  - Style: secondary/outline — understated, not a primary CTA
  - `aria-label`: `Use suggested shares: X.XX`
  - Clicking the button fills Shares with `suggested_shares` and hides the button
  - Button animates in with a 100ms fade

#### Insufficient cash
`valid: true`, `cash_sufficient: false`.
- Suggested shares shown with muted/strikethrough styling
- Risk amount shown normally
- Estimated cost shown in amber — signals it exceeds available cash
- Available cash shown normally
- Informational line below the grid: `Maximum affordable: X.XX shares based on available cash`
  - Styled in muted text (not amber, not red)
  - Uses `max_affordable_shares` from response
- Shares field is **not auto-filled**
- "Use suggested shares" button is **not shown**

#### Invalid — user input condition
`valid: false` with reason code `INVALID_STOP_DISTANCE`, `INVALID_ENTRY_PRICE`, `INVALID_STOP_PRICE`, or `INVALID_RISK_PERCENT`.
- Output values show `—`
- Inline amber message below the Risk % input

| Reason code | User-facing message |
|-------------|---------------------|
| `INVALID_STOP_DISTANCE` | Stop price must be below entry price |
| `INVALID_ENTRY_PRICE` | Enter a valid entry price above zero |
| `INVALID_STOP_PRICE` | Enter a valid stop price above zero |
| `INVALID_RISK_PERCENT` | Risk % must be greater than zero |

- Amber styling (not red) — these are input states, not errors
- Shares field not auto-filled; "Use suggested shares" button not shown

#### Invalid — system condition
`valid: false` with reason code `NO_PORTFOLIO_VALUE_SNAPSHOT`.
- Output values show `—`
- Inline muted grey message (not amber — not the user's fault):
  `Portfolio value unavailable — sizing calculator requires a portfolio snapshot`
- Shares field not auto-filled; "Use suggested shares" button not shown

#### Form submitted / reset
After successful position creation:
- Widget resets to Idle state
- Risk % field **retains** the value last used (does not reset to settings default)
- This preserves workflow continuity when entering multiple trades in sequence

### Form submission behaviour
An invalid or cash-constrained sizing widget state does **not block form submission**. The user may enter shares manually and submit the form at any time. The sizing calculator is decision support, not a gate.

### Network failure behaviour
If the API call fails (network error, 500): the widget shows `—` in all output fields without an error message. The calculation retries automatically on the user's next keystroke after the debounce.

### Accessibility
- Risk % input has an associated `<label>` element
- Output areas that update dynamically use `aria-live="polite"`
- Loading state uses opacity/visibility rather than conditional rendering to preserve screen reader focus
- "Use suggested shares" button has a descriptive `aria-label` including the share count
- Amber and muted text must meet WCAG AA contrast against the dark panel background

---

## User Interactions & States

### Dynamic Market Logic
- Entering a ticker triggers market detection
- For US stocks:
  - FX Rate field appears
  - ATR may be auto‑calculated
  - Sizing calculator passes `market: "US"` to `POST /portfolio/size`

### Real-Time Calculations
The form updates:
- Stop level (if ATR or price changes)
- Total cost including fees
- Any applicable stamp duty or FX fees
- Sizing calculator output (debounced, 300ms)

### Validation Errors
All validation failures show inline error messages:
- Missing or invalid ticker
- Entry date in the future
- Shares zero or negative
- Price invalid or too many decimals
- Insufficient funds (with remaining cash shown)
- FX rate missing for US trades
- Tag format or tag count errors
- Entry note exceeding character limit

### Error Banner
Shown when the API request to create a position fails.

---

## Output (What the Component Produces)
After successful validation and confirmation:
- Position is created with:
  - Ticker
  - Market
  - Entry date
  - Shares
  - Entry price
  - FX rate (US only)
  - ATR value
  - Stop price
  - Entry note
  - Tags
- Fees and total cost are calculated and returned
- User is redirected to the Positions page

---

## Accessibility Considerations
- All fields have clear labels
- Required fields are explicitly indicated
- Number inputs use accessible formatting
- Tag pills include keyboard-accessible remove buttons
- Notes area supports keyboard navigation and screen reader cues
- Form works fully via keyboard only
- Sizing calculator output areas use `aria-live="polite"` for dynamic updates

---

## Visual & UX Notes
- The form should feel lightweight and clean, even with dynamic fields
- Use tooltips or helper text for ATR, FX rate, and tags
- Keep a clear distinction between optional and required fields
- The confirmation button should only activate when all required field validation passes
- Error messages should be concise and contextual
- Preview elements (e.g., fees, stop levels) should update instantly as the user types
- The sizing calculator widget sits in a visually contained card panel with a subtle background tint and border radius — distinct from the surrounding form fields but not jarring
- The widget uses a two-column grid for output values and full-width for the Risk % input and informational lines
