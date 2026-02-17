# position_detail_modal.md

## Purpose & Usage Context
The Position Detail Modal provides a **single, focused place** for users to understand an individual position’s current state and to review/edit journaling information (notes and tags). It supports decision-making by making the **stop logic, risk context, and P&L** legible without requiring users to navigate away from the Positions page. 

This component is accessed from the **Positions page** when the user selects **“View Journal”** (or equivalent detail action) on a position row/card. 

Users rely on the Position Detail Modal to:
- Confirm the position’s key entry/current metrics at a glance
- Understand *why* the position is in its current status (including grace period)
- Read and update entry/exit notes without leaving context
- Add/remove tags to support later filtering and review 

---

## Inputs (Conceptual Props)
> These are conceptual inputs describing what the modal needs to render and behave correctly. They are not implementation requirements.

### Position Identifier (required)
- A stable identifier for fetching/updating the position and its journals (e.g., `id`, `ticker`, or both) 

### Position Summary Data (required)
Used for the “Position Details” and “Current Status” sections:
- Ticker + market (US/UK indicator)
- Entry date
- Entry price (native currency)
- Shares (fractional supported)
- Total cost (GBP)
- Fees paid
- Current price (native currency)
- Days held
- Grace period indicator (if applicable)
- Stop levels and risk status (as provided by backend logic)
- Unrealized P&L (GBP)
- P&L % 

### Journal Data (optional but expected)
- `entry_note` (string | null)
- `exit_note` (string | null)
- `tags` (string[] | null) 

### Tag Suggestions (optional)
- Autocomplete source list for tags (fetched separately) 

---

## Information Layout (User-Facing Sections)

### 1) Position Details
Displays core entry context:
- Entry date
- Entry price (native currency)
- Shares (fractional)
- Total cost (GBP)
- Fees paid 

### 2) Current Status
Displays current state context:
- Current price (native currency)
- Days held
- Grace period indicator (when applicable)
- Stop levels
- Risk status 

### 3) P&L Breakdown
Shows performance in GBP:
- Unrealized P&L (GBP)
- P&L % 

### 4) Journal Section
Supports review and editing of:
- Entry Note card
- Exit Note card (only if position is closed; if open, it may be absent or shown as empty/disabled depending on product rules)
- Tags section (view + edit) 

### 5) Actions
- Edit Note (entry/exit depending on what is shown)
- Edit Tags
- Save (when edits are active)
- Close 

---

## Journal Editing Behavior

### Entry Note Card
**Read mode**
- Shows the entry note text when present
- If empty: show “No entry note” 

**Edit mode**
- “Edit” triggers inline editor inside the card (not a separate modal)
- Show character count while editing
- Maximum length: **500 characters**
- Save commits changes via the note update API (see API section) 

### Exit Note Card (conditional)
- Only shown when an exit note exists or when the position is in a closed state that supports exit journaling
- If present but empty: show “No exit note”
- “Edit” triggers inline editor
- Character count visible during editing
- Maximum length: **500 characters** 

### Tags Section
**Read mode**
- Tags displayed as colored pills
- If empty: show a lightweight empty state (e.g., “No tags”) 

**Edit mode**
- “Edit Tags” reveals tag input with autocomplete suggestions
- User can add tags (Enter to add)
- User can remove tags (X on pill)
- Show max-tags indicator: **10 tags**
- Tags are normalized to lowercase (behavioral expectation) 

---

## Validation & Error Behavior

### Validation Rules
- Notes:
  - Optional
  - Max **500 characters** (entry and exit) 
- Tags:
  - Max **10 tags**
  - Tag format: lowercase letters, numbers, hyphens only (as documented in overall spec)
  - Max 20 characters per tag (as documented in overall spec) 

> Note: If the backend enforces stricter rules, the UI should mirror them via user-visible validation to prevent surprise failures.

### Inline Error Messages
Displayed near the edited control (note field or tag input):
- “Note exceeds 500 character limit”
- “Invalid tag format”
- “Too many tags (max 10)” 

### API Error Handling
If saving fails:
- Show error banner within the modal
- Keep the modal open and preserve user input
- Provide a retry action 

---

## Data Loading & States

### Initial Loading
- When opened, the modal fetches position details if not already available in context
- While loading:
  - Disable edit/save actions
  - Display a clear loading state for the modal content (skeletons or placeholders) 

### Saving State
- When saving notes/tags:
  - Disable Save while the request is in-flight
  - Keep editor open until success/failure returns
  - On success:
    - Update displayed text/pills immediately to reflect saved state
    - Return to read mode for the edited section 

---

## Confirmation & Safety
This modal is primarily informational/editing-focused. It should feel **safe**:
- Closing the modal should not discard changes silently:
  - If there are unsaved edits, show a lightweight warning or require explicit discard (pattern decision) 

---

## User Interactions & States (Summary)

### Read-only (default)
- All journal content visible as cards/pills
- Edit actions available 

### Editing Note
- Inline editor shown inside the relevant card
- Character counter visible
- Save/Cancel available 

### Editing Tags
- Tag input shown with autocomplete
- Existing tags remain visible and removable
- Save/Cancel available 

### Error State
- Error banner at top of modal content
- Field-level messages near invalid inputs
- User can retry without losing work 

---

## Accessibility Considerations
- Modal traps focus while open
- Keyboard navigation supports:
  - Tab through controls and fields in a logical order
  - Escape closes modal (unless blocked by unsaved changes pattern)
- Buttons and inputs have clear labels for screen readers
- Validation errors are announced and visually distinct
- Tag remove controls are keyboard-accessible and labeled (e.g., “Remove tag momentum”) 

---

## Visual & UX Notes
- Present “Position Details”, “Current Status”, and “P&L” as distinct sections to reduce scanning burden
- Journal cards should feel readable and “document-like” (not cramped form UI)
- Tags should be visually consistent with tags elsewhere (Trade Entry, Trade History filters)
- Grace period indicator should be visible and understandable without requiring tooltip hunting 

---

## Optional: Graph (If Implemented)
- A price history chart may be shown as an optional section
- If included, it must not obscure core journal reading/editing flows 

---

## API Integration
- `GET /positions/{ticker}` — fetch position details including notes/tags (when not available in-memory) 
- `PATCH /positions/{id}/note` — update entry_note or exit_note 
- `PATCH /positions/{id}/tags` — update tags 
- `GET /positions/tags` — fetch tag suggestions for autocomplete 
