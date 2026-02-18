# exit_modal.md

**Owner:** Frontend Specifications & UX Documentation Owner  
**Status:** Canonical  
**Version:** 1.0
**Last Updated:** February 18, 2026

## Purpose & Usage Context
The Exit Modal allows users to **close a position**, either fully or partially.  
It provides real‑time fee calculations, P&L previews, and optional journal notes.  
This component is accessed from the Positions page when the user clicks **Exit** on any active position.

Users rely on the Exit Modal to:
- Enter or adjust exit‑specific data  
- Understand the financial impact before confirming  
- Record exit‑related notes and reasoning  
- Complete the exit safely with appropriate validation  

---

## Inputs (Conceptual Props)

### Shares to Exit (optional)
- Number input  
- Default: all shares in the position  
- Maximum: the number of shares currently held  
- Supports fractional values  
- Display example: “Shares to exit (Total: X.XX)”

### Exit Price (required)
- Number input  
- Pre‑populated with current market price  
- Editable by user  
- Label adapts by market (USD or GBP)  

### Exit Date (optional)
- Date picker  
- Default: today  
- Can be backdated for reconciliation  
- Must not be before the entry date  

### Exit Reason (optional)
Dropdown options include:
- Manual Exit (default)  
- Stop Loss Hit  
- Target Reached  
- Risk‑Off Signal  
- Trailing Stop  
- Partial Profit Taking  

### FX Rate (conditional, required for US positions)
- Number input  
- Shown only for US stocks  
- Pre‑populated with current FX rate  
- Editable  
- Format: 1.XXXX  

### Exit Note (optional)
- Text area  
- Up to 500 characters  
- Character counter shown  
- Pre‑fills with suggested reflection prompts  
- Helps capture thinking, emotions, or strategy adjustments

---

## Validation & Error Behavior

### Validation Rules
- Shares:  
  - Must be > 0  
  - Must not exceed total shares  
- Exit price:  
  - Must be > 0  
- Exit date:  
  - Must be valid  
  - Must be on or after position’s entry date  
- FX rate:  
  - Required for US stocks  
  - Must be > 0  
- Exit note:  
  - Max 500 characters  

### Error Messages
Displayed inline or as a field‑highlight:
- “Insufficient shares”  
- “FX rate required”  
- “Exit price required”  
- “Exit date cannot be before entry date”  

### API Error Handling
If submission fails:
- Modal shows error banner  
- Modal remains open so the user doesn’t lose input  
- Retry action is available  

---

## Preview (Before Confirmation)
The modal continuously recalculates preview values as the user edits fields.

Preview includes:
- Entry cost (pro‑rated for partial exits)  
- Gross proceeds (native currency)  
- Fee breakdown  
  - Commission  
  - FX fee  
- Total fees  
- Net proceeds (native currency and GBP)  
- Realized P&L (GBP)  
- Realized P&L %  

---

## Confirmation Flow
1. User fills the form  
2. Preview updates in real time  
3. User clicks **Confirm Exit**  
4. API call is submitted  
5. On success:  
   - Modal closes  
   - Positions page refreshes  
6. On failure:  
   - Error shown  
   - Form stays open  

---

## User Interactions & States

### Loading State
- Disabled confirm button during API call  
- Preview shows static values until data returns  

### Partial Exit Behavior
- Users can reduce the shares field  
- Remaining shares update automatically after confirmation  
- Trade history receives a record for the exited portion  

---

## Accessibility Considerations
- Labels match input purpose and market context  
- Keyboard‑navigable fields and buttons  
- Focus is trapped inside the modal while open  
- Error states use accessible messaging and clear contrast  
- Buttons and fields announce purpose to screen readers  

---

## Visual & UX Notes
- The fee and P&L preview should visually stand out to ensure clarity  
- Risk‑related exits (Stop Loss Hit, Risk‑Off Signal) may be highlighted but not required  
- Use spacing to separate form inputs from the financial preview  
- Exit note text area should feel inviting and helpful, not burdensome  
- Ensure confirmation action feels safe and reversible only until submission  

---
