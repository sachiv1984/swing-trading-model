# position_detail_modal.md

**Owner:** Frontend Specifications & UX Documentation Owner  
**Status:** Canonical  
**Version:** 1.0
**Last Updated:** February 18, 2026

## Purpose & Usage Context
The Position Detail Modal provides a focused view of a single position's key stats and entry context, plus lightweight journaling tools (entry note + tags). It helps users quickly review the position and capture/adjust their thinking without navigating away from the current workflow.

Accessed when a user opens the position details from the Positions experience.

---

## What the User Can Do
Within this modal, the user can:
- Review high-level stats (Days Held, Shares, P&L)
- Review entry details (Entry Date, Entry Price, ATR Value, FX Rate)
- Read or edit the **Entry Note**
- Add/remove **Tags** (up to 10)
- Save changes or cancel/close

---

## Inputs (Conceptual)
### Position (required)
The modal requires a `position` object with enough data to render. This object is passed in as a prop from the parent Positions page, which already holds position data from `GET /positions`. The modal does not make its own fetch call for position data.

**Header**
- `ticker`
- `market` (used for display and currency symbol)

**For summary stats**
- `entry_date`
- `shares`
- `entry_price`
- `current_price_native` (for display in entry details)
- `pnl` — authoritative GBP P&L as returned by `GET /positions`. Used directly for the P&L stat. Must not be recalculated client-side

**For entry details**
- `atr_value` (optional)
- `fx_rate` (optional)

**For journal**
- `entry_note` (optional)
- `tags` (optional)

### Modal state + callbacks (required)
- `open` (boolean)
- `onClose()` — closes the modal
- `onSave(updatedPosition)` — persists journal changes (note + tags)

---

## Information Architecture (Visible Sections)

### 1) Header
- Displays the position ticker prominently.
- Displays the market as a small badge (e.g., "UK" or "US").

### 2) Summary Stats (3-column)
**Days Held**
- Calculated as the number of days between today and the position entry date.

**Shares**
- Displays the position share quantity (supports fractional).

**P&L**
- Displays `pnl` from the position prop — the authoritative GBP P&L computed server-side by `GET /positions`.
- Display:
  - Uses `£` prefix (GBP).
  - Always shows a 2-decimal value.
  - Shows `+` prefix for positive P&L.
  - Styling indicates profit vs loss (green-ish vs red-ish).

> **Note:** P&L must be taken from the `pnl` field in the prop. It must not be recalculated client-side using `current_price_native` and `entry_price`. The backend `pnl` value correctly accounts for FX conversion, position lifecycle, and cost basis. A native-price approximation would produce different results for US positions and partial exits, and would violate the system principle that the backend is the single source of truth for financial values.

### 3) Entry Details
Displays:
- Entry Date (formatted as "MMM d, yyyy")
- Entry Price (in native currency with symbol)
- ATR Value:
  - If absent, show "—"
- FX Rate:
  - If absent, show "1.0000"

### 4) Trade Journal
Contains:
- Entry note (read or edit)
- Tags (read or edit)

---

## Journal: Read Mode (Default)

### Entry Note
- If the entry note exists, show it in a bordered card.
- If empty, show: **"No entry note"** (italic/quiet).

### Tags
- If tags exist, show them as pills.
- If there are no tags, tags are simply not displayed in read mode (no explicit empty message).

### Edit action
- "Edit" button appears in the Trade Journal header.
- Clicking Edit switches the journal area into Edit Mode.

---

## Journal: Edit Mode

Edit mode allows changes to **Entry Note** and **Tags**.

### Entry Note Editing
- Field: multiline text area.
- Placeholder:
  - "Why are you entering this trade? What's your thesis?"
- Character limit:
  - Maximum **500** characters.
  - Input is constrained so users cannot exceed 500.
- Character counter:
  - Displays `current/500`.
  - The counter becomes visually warning-colored when > 450 characters.

### Tags Editing
#### Tag display and removal
- Existing tags are shown as pills with a remove (X) control.
- A counter label shows the current count (e.g., `Tags (3/10)`).
- Clicking the X removes that tag immediately (in edit state).

#### Adding tags
- Tag limit: **10 tags maximum** (consistent with API contract and all other surfaces).
- When 10 tags are present, the "add tag" input is not shown.

#### Tag normalization rules (on add)
When a tag is added:
- It is normalized to lowercase.
- Spaces are converted to hyphens.
- Duplicates are not added.

#### Tag suggestions
While typing in the "add tag" input:
- A suggestion list may appear.
- Suggestions are fetched from `GET /positions/tags` (the dedicated tag list endpoint).
- Merged with a small set of default tags (e.g., momentum-style defaults) to provide useful starting suggestions.
- Suggestions exclude tags already selected.
- Only the first 10 suggestions are shown at a time.

#### Adding tags via keyboard
- Pressing **Enter** adds the typed tag (if non-empty), applying normalization.

---

## Cancel vs Close Behavior

### "Cancel" inside Journal Edit Mode
- Exits edit mode for the journal section.
- Discards journal edits made during the edit session.
- Restores the journal fields to the position's current saved values.

### Footer "Cancel"
- Closes the modal (same as onClose).

---

## Saving Behavior

### "Save Changes" (footer)
On save:
- The modal calls `onSave` with:
  - `entry_note`:
    - saved as `null` if empty
    - otherwise saved as the entered string
  - `tags`:
    - saved as `null` if empty
    - otherwise saved as the array of normalized tags

The component assumes persistence happens outside the modal (e.g., API update handled by parent).

---

## Validation & Error Handling (User-Visible)

### Enforced constraints
- Entry note: maximum 500 characters (hard limit enforced in input handler).
- Tags: maximum 10 tags (hard limit — input hidden when limit reached).
- Tags are normalized on add (lowercase, spaces → hyphens).
- Duplicate tags are prevented.

### Error messaging
- No explicit inline error messages are shown for note length or tag limit because inputs are constrained by the UI.
- Save failure handling is not shown in this component; it should be handled by the parent experience that implements `onSave`.

---

## Loading / Empty States
- If no `position` is provided, nothing is rendered.
- Tag suggestions depend on `GET /positions/tags`; if no tags have been used yet, the default tag set still provides suggestions.

---

## Accessibility Considerations
- Modal should trap focus while open.
- Keyboard support:
  - Tab navigation through interactive controls.
  - Enter adds a tag while focused in tag input.
- Buttons have clear labels ("Edit", "Cancel", "Save Changes").
- Tag remove control should remain reachable via keyboard navigation.
