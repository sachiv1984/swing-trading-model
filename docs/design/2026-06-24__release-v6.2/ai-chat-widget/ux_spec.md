**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-06-24
**Approved by:** Product Owner — 2026-06-24
**Story:** ST-09 — AI chat widget (BLG-FEAT-51)
**Cycle:** 2026-06-24__release-v6.2

---

# UX Specification — AI Trade Advisor Chat Widget

## 1. Placement

**Canonical primary page:** Positions (`/positions`) — floating widget, bottom-right of viewport
**Stretch goal (capacity-dependent):** Signals (`/signals`) — same widget pattern, only if sprint capacity allows after Positions implementation is complete

**Sprint planning note:** ST-09 is sized S (~0.5 day). Sprint planning must scope implementation to Positions as the sole target page. Signals placement is a stretch goal and must not be treated as in-scope unless capacity is explicitly confirmed at sprint planning seal. If Signals placement is deferred, it should be filed as a follow-on backlog item.

**Rationale:** The trade advisor answers portfolio questions grounded in live position state. The Positions page is the primary context where users monitor open trades and make daily decisions — placing the widget there gives direct access at the moment of need. The Signals page is a natural secondary placement for discussing new signals in context of existing positions, but is lower priority given the backend grounds responses in portfolio state (ST-08).

---

## 2. Widget States

The widget has two states: **Collapsed** (button) and **Expanded** (panel).

---

## 3. Collapsed State (button)

A fixed-position button rendered at `position: fixed; bottom: 24px; right: 24px; z-index: 100`.

| Element | Spec |
|---------|------|
| Shape | Rounded rectangle (pill) |
| Background | `#1D4ED8` (blue-700) |
| Text | "Ask Advisor" in white, 14px |
| Icon | Chat bubble icon, left of text |
| Size | Auto width (text + padding), 44px height |
| Hover | Darken background to `#1E3A8A` (blue-900) |

Clicking the collapsed button opens the expanded panel.

---

## 4. Expanded State (panel)

The expanded panel replaces the collapsed button at the same bottom-right anchor.

```
┌──────────────────────────────────────┐
│ 💬 AI Trade Advisor   [Advisory] [✕] │  ← header
├──────────────────────────────────────┤
│                                      │
│  Ask about your portfolio, positions,│  ← empty state prompt
│  or signals.                         │
│                                      │
│  ·····  (typing indicator)           │  ← AI responding
│                                      │
│  [User message]                  →   │  ← user bubble
│  ← [AI response]                     │  ← AI bubble
│                                      │
├──────────────────────────────────────┤
│ [Ask about your portfolio…  ] [Ask]  │  ← input row
├──────────────────────────────────────┤
│ AI responses are advisory only.      │  ← footer advisory
│ All trade decisions require human    │
│ confirmation.                        │
└──────────────────────────────────────┘
```

### Panel Dimensions

| Property | Value |
|----------|-------|
| Width | 350px |
| Height | 480px |
| Position | `fixed; bottom: 24px; right: 24px; z-index: 100` |
| Background | White |
| Border | 1px solid `#E5E7EB` (grey-200) |
| Border radius | 12px |
| Box shadow | Elevated shadow (lg) |

### Header

| Element | Spec |
|---------|------|
| Icon | Chat bubble icon (left of title) |
| Title | "AI Trade Advisor" (16px, weight 600) |
| Advisory badge | Small amber pill "Advisory" (`#D97706`, white text, 10px) |
| Close button | ✕ icon, right-aligned; collapses panel to button on click |

### Messages Area

| Message type | Alignment | Style |
|-------------|-----------|-------|
| User message | Right-aligned | Blue bubble (#1D4ED8 bg, white text) |
| AI response | Left-aligned | Light grey bubble (#F3F4F6 bg, dark text) |

Messages area is scrollable. Most recent message at bottom. Auto-scroll to bottom on new message.

### Input Row

| Element | Spec |
|---------|------|
| Input | Multiline text field, placeholder "Ask about your portfolio…" |
| Submit | "Ask" button (primary blue, right of input) |
| Enter key | Submits (Shift+Enter for newline) |

Input field: 1–3 lines, auto-height up to 3 lines, then scrolls.

### Footer Advisory

Static text (always visible, not dismissible):

> "AI responses are advisory only. All trade decisions require human confirmation."

Font size: 11px. Colour: `#6B7280` (grey-500). Italic.

---

## 5. Loading State

During `POST /ai/chat` call:
- Input field disabled
- "Ask" button disabled
- Typing indicator shown in messages area (three animated dots in AI bubble position)

---

## 6. Error State

If `POST /ai/chat` returns error or times out:
- Inline error message in messages area: "Unable to get a response. Please try again." (muted red text, no bubble styling)
- Input re-enabled
- No toast; error is in-context within the widget

---

## 7. Empty State (widget just opened, no messages)

Messages area shows: "Ask about your portfolio, positions, or signals." (muted grey text, centre-aligned in messages area). This text is replaced by the first message/response.

---

## 8. Interactions

| Interaction | Behaviour |
|------------|-----------|
| Collapse button click | Opens expanded panel |
| ✕ close click | Collapses to button; message history cleared (stateless per request — AC-05) |
| Ask button / Enter | Submits question, calls POST /ai/chat |
| Input on error | User can retype and resubmit |

**Message history:** Widget holds in-memory display of the current session's conversation for readability. Each POST /ai/chat call is stateless (no session passed to backend — ST-08 AC-05). Clearing the widget (✕) resets the in-memory display.

---

## 9. Constraints

**§13 compliance:** This widget is read-only advisory. No trade entry, exit, or modification action is triggerable from the widget. AC-03 explicitly prohibits executable trade actions from the widget. The advisory footer is non-dismissible.

**AI model:** `claude-sonnet-4-6` (per ST-08 AC-06). Backend concern only.

---

## 10. Accessibility

- Expanded panel is `role="dialog"` with `aria-label="AI Trade Advisor"`
- Close button has `aria-label="Close AI Trade Advisor"`
- Messages area uses `aria-live="polite"` to announce new responses
- Input has `aria-label="Ask your portfolio question"`
- Advisory footer is `role="note"`

---

## 11. API Dependency

| Endpoint | Purpose |
|----------|---------|
| `POST /ai/chat` | Accepts `{ question: string, context?: { ticker?, position_id? } }`; returns AI response grounded in live portfolio state |
