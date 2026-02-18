# position_form.md

## Purpose & Usage Context
The Position Form is used to manually create a new position in the portfolio.  
It supports both UK and US markets, with dynamic fields that adjust based on the detected market.  
This form appears on the Trade Entry page and is one of the core data‑entry workflows of the application.

Users rely on this form to:
- Enter accurate trade details  
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

### Shares (required)
- Number input  
- Supports fractional values (e.g., 5.5)  
- Minimum 0.0001  
- Max 4 decimal places  

### Entry Price (required)
- Number input  
- In the position’s native currency (GBP for UK, USD for US)  
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
- Auto‑calculated as:  
  `entry_price - (5 × ATR)`  
- User may override  

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

## User Interactions & States

### Dynamic Market Logic
- Entering a ticker triggers market detection  
- For US stocks:
  - FX Rate field appears  
  - ATR may be auto‑calculated  

### Real-Time Calculations
The form updates:
- Stop level (if ATR or price changes)  
- Total cost including fees  
- Any applicable stamp duty or FX fees  
- Preview of entry note and tags  

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

---

## Visual & UX Notes
- The form should feel lightweight and clean, even with dynamic fields  
- Use tooltips or helper text for ATR, FX rate, and tags  
- Keep a clear distinction between optional and required fields  
- The confirmation button should only activate when all validation passes  
- Error messages should be concise and contextual  
- Preview elements (e.g., fees, stop levels) should update instantly as the user types  

---
