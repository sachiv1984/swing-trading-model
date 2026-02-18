# cash_management_modal.md

**Owner:** Frontend Specifications & UX Documentation Owner  
**Status:** Canonical  
**Version:** 1.0
**Last Updated:** February 18, 2026

## Purpose & Usage Context
The Cash Management Modal allows users to record **deposits and withdrawals** so that portfolio cash and P&L remain accurate over time.  
It is typically opened from the Dashboard (by clicking cash balance) or any context where the user needs to adjust cash outside of trade entries and exits.

Users rely on this modal to:
- Record cash **deposits** (adding funds)  
- Record cash **withdrawals** (removing funds)  
- See a historical list of cash movements  
- Understand the running cash total  

---

## Inputs (Conceptual Props)

### Transaction Type (required)
- Radio buttons or segmented control:
  - **Deposit**
  - **Withdrawal**
- Exactly one option must be selected before confirmation.

### Amount (required)
- Number input in **GBP**
- Minimum amount: **0.01**
- Represents the cash value to be added or removed.

### Date (required)
- Date picker  
- Format: `YYYY-MM-DD`  
- Default: today  
- Represents when the cash movement took effect.

### Note (optional)
- Single‑line text input  
- Max 200 characters  
- Used to provide context (e.g., “Broker transfer”, “Fee adjustment”)  

---

## Transaction History Display
Within the modal, users can see a **history of cash transactions** to provide context:

- List of past transactions with:
  - Date  
  - Type (Deposit/Withdrawal)  
  - Amount  
  - Note (if any)  

- Interactions:
  - Sortable by date  
  - Filterable by type (Deposit vs Withdrawal)  
  - Display of a **running total** or summary to show cumulative cash impact  

The history supports quick audits and verification of previous adjustments.

---

## User Interactions & States

### Creating a Transaction
1. User selects **Deposit** or **Withdrawal**.  
2. User enters the **amount**.  
3. User sets the **date** (or accepts default).  
4. Optionally, user adds a **note**.  
5. User confirms to submit the transaction.  

On success:
- The modal updates the transaction list.  
- Portfolio cash summary is refreshed.  

### Validation Errors
- **Transaction Type**  
  - Required; error if no option is selected.

- **Amount**  
  - Must be ≥ 0.01  
  - Show inline error for zero, negative, or missing amount.

- **Date**  
  - Must be a valid date  
  - Show inline error if date parsing fails.

- **Note**  
  - Must not exceed 200 characters.

### Error Handling
- If the API request fails:
  - Show an error banner or message within the modal.  
  - Keep user input intact so they can retry.

---

## Accessibility Considerations
- Radio buttons for transaction type must be keyboard accessible.  
- Form fields have clear text labels.  
- Error messages are associated with their fields.  
- Modal supports focus trapping and ESC/close buttons.  
- Screen readers should announce opening and closing of the modal.  

---

## Visual & UX Notes
- Distinguish **Deposit** and **Withdrawal** visually (e.g., subtle color cue) while maintaining consistency with the overall theme.  
- Make the running total or summary visible but not overwhelming.  
- Keep the form layout simple; users should be able to add a transaction with minimal friction.  
- Ensure that transaction history is easy to scan and interpret, especially on smaller screens.  

---
