# journal_components.md

## Purpose & Usage Context
The journal components support all note‑taking and tagging features across the application.  
They appear in multiple contexts:

- Position Detail Modal (viewing/editing entry and exit notes)  
- Trade History expandable journal rows  
- Journal View (dedicated page for reviewing journals)  
- Trade Entry and Exit workflows (inline journal fields)  

These components help users document their reasoning, reflect on decisions, and categorize trades with tags.

---

## Components Overview
This section includes the shared building blocks used for journaling:

1. **Journal Note Display**  
2. **Inline Journal Editor**  
3. **Tag List (Pills)**  
4. **Tag Editor (Autocomplete Input)**  
5. **Expandable Journal Card**  

Each is documented below.

---

## 1. Journal Note Display

### Purpose
Shows the saved entry or exit note for a position or trade.

### Behavior
- Renders plain text, formatted for readability  
- Shows placeholder text (“No entry note”, “No exit note”) when empty  
- Includes an **Edit** button when editing is allowed  
- When editing, transitions to the inline editor component  

### States
- **Default**: read‑only view  
- **Empty**: placeholder message  
- **Editing**: replaced by inline editor  
- **Saving**: disabled state until API returns  

### Accessibility
- Clearly labeled (e.g., “Entry Note”, “Exit Note”)  
- Text is selectable for user reference  
- Edit button accessible via keyboard  

---

## 2. Inline Journal Editor

### Purpose
Allows users to create or update notes for entries and exits.

### Behavior
- Text area replacing the note display  
- Character counter (max 500 characters)  
- Save and Cancel buttons  
- Automatically validates length  
- Keeps focus inside editor while open  

### Validation
- Max 500 characters  
- Empty state allowed (notes optional)  

### Error Handling
- Shows inline error if character limit exceeded  
- API errors preserve the user’s text  

### Accessibility
- Focus automatically moves to the text area  
- Screen readers announce entering “edit mode”  

---

## 3. Tag List (Pills)

### Purpose
Displays tags associated with a position or trade.

### Behavior
- Rendered as small, colored pills  
- Each pill shows the tag name  
- Optional remove button (X) when editing mode is active  
- Tags wrap across multiple lines when needed  

### Tag Rules
- Lowercase only  
- Letters, numbers, hyphens  
- Max 20 characters per tag  
- Max 10 tags total  

### Accessibility
- Remove button is keyboard accessible  
- Tags announced with descriptive text (e.g., “Tag: momentum”)  

---

## 4. Tag Editor (Autocomplete Input)

### Purpose
Allows adding and removing tags with suggestion support.

### Behavior
- Autocomplete dropdown showing existing tags  
- Press **Enter** to add a new tag  
- Click **X** on pill to remove  
- Prevents invalid formats  
- Prevents duplicates  
- Prevents exceeding tag limit  

### Validation
- Format validation: lowercase letters, numbers, hyphens  
- Max 20 characters  
- Max 10 tags  

### Error Handling
- Inline error for invalid tag format  
- Inline error for exceeding tag count  
- API error messages if tag updates fail  

### Accessibility
- Input labeled “Tags” or “Edit Tags”  
- Suggestion list is keyboard navigable  

---

## 5. Expandable Journal Card

### Purpose
Provides long‑form journal review inside Trade History or Journal View.

### Content Sections
- **Entry Analysis** (entry note)  
- **Exit Reflection** (exit note)  
- **Strategy Tags** (tags list)  

### Behavior
- Expands beneath a trade row or card  
- Collapses smoothly when toggled off  
- Supports long text without truncation  
- Displays placeholders when notes are empty  

### Visual Structure
- Headers for each section  
- Color accents for clarity  
- Spaced layout for readability  

### Accessibility
- Expand/collapse accessible via keyboard  
- Section headers provide structure for screen readers  

---

## Interaction Summary

### Editing Flow
1. User opens a position or trade journal  
2. Clicks **Edit Note** or **Edit Tags**  
3. Inline editor or tag editor appears  
4. User updates content  
5. Save triggers API update  
6. UI refreshes and returns to read‑only mode  

### Data Sources
- Notes saved to backend via update endpoints  
- Tags fetched from global tag list  
- Tags updated per‑position or per‑trade  

---

## Visual & UX Notes
- Journaling should feel smooth and lightweight  
- Editing should occur in context — no page navigation  
- Tags should visually enhance readability, not clutter  
- Long notes should remain readable with proper spacing  
- Reflection prompts encourage deeper journaling  

---
