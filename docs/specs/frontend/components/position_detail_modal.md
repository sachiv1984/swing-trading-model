# position_detail_modal.md

## Purpose & Usage Context
The Position Detail Modal provides a focused view of a single position’s key stats and entry context, plus lightweight journaling tools (entry note + tags). It helps users quickly review the position and capture/adjust their thinking without navigating away from the current workflow.

Accessed when a user opens the position details from the Positions experience.

---

## What the User Can Do
Within this modal, the user can:
- Review high-level stats (Days Held, Shares, P&L)
- Review entry details (Entry Date, Entry Price, ATR Value, FX Rate)
- Read or edit the **Entry Note**
- Add/remove **Tags** (up to 5)
- Save changes or cancel/close

---

## Inputs (Conceptual)
### Position (required)
The modal requires a `position` object with enough data to render:

**Header**
- `ticker`
- `market` (used for display and currency symbol)

**For summary stats**
- `entry_date`
- `shares`
- `entry_price`
- `current_price_native`

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
- Displays the market as a small badge (e.g., “UK” or “US”).

### 2) Summary Stats (3-column)
**Days Held**
- Calculated as the number of days between today and the position entry date.

**Shares**
- Displays the position share quantity (supports fractional).

**P&L**
- Calculated using native prices:
  - `(current_price_native - entry_price) * shares`
- Display:
  - Uses the currency symbol based on market:
    - UK → `£`
    - non-UK → `$`
  - Always shows a 2-decimal value.
  - Shows `+` prefix for positive P&L.
  - Styling indicates profit vs loss (green-ish vs red-ish).

> Note: The P&L shown here is a simple native-price calculation for quick reference (not a full “GBP-realized/unrealized” accounting breakdown).

### 3) Entry Details
Displays:
- Entry Date (formatted as “MMM d, yyyy”)
- Entry Price (in native currency with symbol)
- ATR Value:
  - If absent, show “—”
- FX Rate:
  - If absent, show “1.0000”

### 4) Trade Journal
Contains:
- Entry note (read or edit)
- Tags (read or edit)

---

## Journal: Read Mode (Default)

### Entry Note
- If the entry note exists, show it in a bordered card.
- If empty, show: **“No entry note”** (italic/quiet).

### Tags
- If tags exist, show them as pills.
- If there are no tags, tags are simply not displayed in read mode (no explicit empty message).

### Edit action
- “Edit” button appears in the Trade Journal header.
- Clicking Edit switches the journal area into Edit Mode.

---

## Journal: Edit Mode

Edit mode allows changes to **Entry Note** and **Tags**.

### Entry Note Editing
- Field: multiline text area.
- Placeholder:
  - “Why are you entering this trade? What’s your thesis?”
- Character limit:
  - Maximum **500** characters.
  - Input is constrained so users cannot exceed 500.
- Character counter:
  - Displays `current/500`.
  - The counter becomes visually warning-colored when > 450 characters.

### Tags Editing
#### Tag display and removal
- Existing tags are shown as pills with a remove (X) control.
- Clicking the X removes that tag immediately (in edit state).

#### Adding tags
- Tag limit:
  - Users can add tags until there are **5 total** tags.
  - When 5 tags are present, the “add tag” input is not shown.

#### Tag normalization rules (on add)
When a tag is added:
- It is normalized to lowercase.
- Spaces are converted to hyphens.
- Duplicates are not added.

#### Tag suggestions
While typing in the “add tag” input:
- A suggestion list may appear.
- Suggestions exclude tags already selected.
- Only the first 10 suggestions are shown at a time.
- The suggestions include:
  - Tags seen on other positions (to encourage reuse)
  - A small set of default tags (e.g., momentum-style tags)

#### Adding tags via keyboard
- Pressing **Enter** adds the typed tag (if non-empty), applying normalization.

---

## Cancel vs Close Behavior

### “Cancel” inside Journal Edit Mode
- Exits edit mode for the journal section.
- Discards journal edits made during the edit session.
- Restores the journal fields to the position’s current saved values.

### Footer “Cancel”
- Closes the modal (same as onClose).

---

## Saving Behavior

### “Save Changes” (footer)
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
- Entry note: maximum 500 characters (hard limit).
- Tags: maximum 5 tags (hard limit).
- Tags are normalized on add (lowercase, spaces → hyphens).
- Duplicate tags are prevented.

### Error messaging
- No explicit inline error messages are shown for note length or tag limit because inputs are constrained by the UI.
- Save failure handling is not shown in this component; it should be handled by the parent experience that implements `onSave`.

---

## Loading / Empty States
- If no `position` is provided, nothing is rendered.
- Tag suggestions depend on an available set of known tags; if none exist, defaults still provide suggestions.

---

## Accessibility Considerations
- Modal should trap focus while open.
- Keyboard support:
  - Tab navigation through interactive controls.
  - Enter adds a tag while focused in tag input.
- Buttons have clear labels (“Edit”, “Cancel”, “Save Changes”).
- Tag remove control should remain reachable via keyboard navigation.

---

## Consistency Note (Potential Spec Alignment Issue)
This component currently enforces **5 tags max**, while other areas of the product documentation may allow **10**. If the product intent is 10, this should be aligned across components and patterns; otherwise, document the 5-tag limit as the standard pattern.
