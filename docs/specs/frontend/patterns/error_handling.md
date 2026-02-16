# error_handling.md

## Purpose
The Error Handling pattern defines how the application communicates failures, validation issues, and unexpected conditions to users.  
Its goal is to ensure errors are:

- Clear  
- Actionable  
- Consistent across pages and components  
- Non‑disruptive to user workflows  

This pattern applies to all forms, API interactions, modals, and data‑fetching experiences.

---

## When This Pattern Is Used
Use the Error Handling pattern whenever:

- A form field has invalid or missing data  
- An API request fails (GET, POST, PATCH, PUT)  
- Calculations cannot be completed (e.g., insufficient funds)  
- Required data is unavailable or stale  
- The system encounters user‑related or network‑related issues  

---

## UX Rationale
- Users should always know **what went wrong**, **why it happened**, and **how to fix it**.  
- Errors should not feel punitive — tone remains neutral and supportive.  
- Errors must never block unrelated tasks.  
- Inline errors reduce cognitive load by pointing directly to the source.  
- Global errors highlight API or system issues without overwhelming the user.

---

## Error Types & Expected Behavior

### 1. Inline Field Errors
Used when a user enters invalid form data.

**Examples:**
- Invalid ticker  
- Entry date in the future  
- FX rate missing for US stocks  
- Exceeding journal note character limits  
- Invalid tag format  
- Exceeding tag limits  
- Exit date before entry date  

**Behavior:**
- Displayed directly beneath the field  
- Field is highlighted  
- Confirmation buttons remain disabled until resolved  

---

### 2. Global Error Banner
Used when system‑level or API failures occur.

**Examples:**
- Failed request to load portfolio  
- Failure during Exit or Entry submission  
- Failed tag update  
- Network outage  

**Behavior:**
- Displays a persistent banner at the top of the page or modal  
- Includes a brief description and optional “Retry” action  
- Does not clear user input  

---

### 3. Modal‑Specific Errors
Used inside Position Entry, Exit, or Cash modals.

**Behavior:**
- Inline messages appear above the form  
- The modal stays open after failures  
- User input is preserved  

---

### 4. Empty & Missing Data Errors
Shown when data cannot be retrieved or when results are empty due to filters.

**Behavior:**
- Contextual message explaining the issue  
- Option to adjust filters or retry  
- Friendly tone (not technical)

---

## Do / Don’t Guidance

### Do
- Keep messages concise and user‑friendly  
- Explain what caused the error  
- Highlight only the affected fields  
- Provide actionable guidance  
- Preserve the user's work whenever possible  
- Use consistent styling across the app  

### Don't
- Use technical jargon or raw backend error strings  
- Clear entire forms after an error  
- Display errors in multiple locations for the same issue  
- Block unrelated actions on the page  

---

## Reusable Principles Across the App

### 1. Consistency
Every error must follow the same structure:
- Clear message  
- Optional detail  
- User action  

### 2. Visibility
Errors should be:
- Immediately visible  
- Closely tied to their context (inline vs global)  
- Color‑coded with strong contrast  

### 3. Recoverability
Users must be able to:
- Fix the problem  
- Retry submissions  
- Continue using other features  

### 4. Non‑Destructive Handling
- Never erase entered data  
- Never exit a modal automatically unless the user confirms  

### 5. Accessibility
- Screen readers announce errors  
- Fields with errors have ARIA associations  
- Keyboard focus moves to the first error when possible  

---

## Summary
Error handling in the Position Manager Web App is designed to keep users informed without interrupting their flow.  
By following consistent patterns across pages and components, the system ensures clarity, reduces frustration, and helps users recover quickly from mistakes or system issues.

---
