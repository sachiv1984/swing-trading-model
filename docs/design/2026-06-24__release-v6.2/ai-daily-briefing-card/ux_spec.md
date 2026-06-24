**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-06-24
**Approved by:** Product Owner — 2026-06-24
**Story:** ST-07 — AI Daily Briefing card (BLG-FEAT-50)
**Cycle:** 2026-06-24__release-v6.2

---

# UX Specification — AI Daily Briefing Card

## 1. Placement

**Page:** Dashboard Homepage (`/`)
**Position:** New full-width card section below the existing session-summary cards (§4), above the Gate Progress Indicator strip (existing §5).

**Rationale:** The daily flow is: Morning Briefing → Session Summary → AI Briefing → Gate Progress. The AI card synthesises the session-summary data into an action plan — it should follow the raw data, not precede it. Placing it above Gate Progress preserves the latter's passive/low-priority visual weight at the bottom of the page.

---

## 2. Component Identity

**Section label (optional):** No section label — the card header carries the identity.
**Card header:** "Today's Briefing"
**Advisory label:** Amber badge "AI Advisory" + static text "All actions require your confirmation" (muted italic, below header)

---

## 3. Card Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Today's Briefing           [Generated 09:14]  [Regenerate]  │
│ ⚠ AI Advisory — All actions require your confirmation        │
├─────────────────────────────────────────────────────────────┤
│ Summary paragraph (2–4 sentences, plain text)               │
│                                                              │
│ Actions:                                                     │
│  1. [EXIT] AAPL — Trailing stop breached; review position.   │
│  2. [HOLD] MSFT — No action required today.                  │
│  3. [MONITOR] TSLA — Rebalance signal; confirm at month end. │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Element Specification

### Header Bar

| Element | Content | Position |
|---------|---------|----------|
| Title | "Today's Briefing" | Left |
| Timestamp | "Generated HH:MM" (muted text, 12px) | Centre-right |
| Regenerate button | "Regenerate" (secondary/outlined style) | Right |

### Advisory Label

Immediately below the header bar, above the card body:
- Amber warning badge: "AI Advisory" (`#D97706` background, white text)
- Static text inline: "All actions require your confirmation" (muted italic, 12px)

This label is **always visible** — not dismissible.

### Card Body

| Section | Content | Format |
|---------|---------|--------|
| Summary | Briefing summary from `response.summary` | Plain paragraph text |
| Actions list | Each action from `response.actions[]` | Ordered list (numbered) |

**Action item format:**
- Action type chip (see below) + bold ticker + description text
- Chip colours per action type:
  - `EXIT`: red `#DC2626` — "EXIT"
  - `ENTER`: green `#16A34A` — "ENTER"
  - `MONITOR`: amber `#D97706` — "MONITOR"
  - `HOLD`: grey `#6B7280` — "HOLD"

---

## 5. States

### Normal (briefing available)

Card body with summary and action list as specified above.

### Loading (POST /ai/daily-briefing in progress)

- Summary area: skeleton placeholder (2 lines)
- Actions: skeleton placeholder (3 rows)
- Regenerate button: disabled
- Timestamp: hidden
- No spinner text (skeleton conveys loading)

### Error (POST /ai/daily-briefing failed)

- Body: "Unable to generate briefing." (muted text, centre-aligned)
- Sub-text: "Try regenerating."
- Regenerate button: enabled
- Advisory label: still shown

### Empty actions (summary present, `actions` array empty)

- Summary shown normally
- Below summary: "No specific actions required today." (muted text)

### No briefing yet (page load, no prior generation today)

- Body: "No briefing for today. Click Regenerate to generate your daily summary."
- Regenerate button: enabled

---

## 6. Interactions

### Regenerate Button

- Calls `POST /ai/daily-briefing`
- Transitions card to Loading state
- On success: updates card with new summary and actions; updates timestamp
- On error: transitions to Error state
- Button disabled while in Loading state

### Card Content

Display-only. Action items are informational only — no one-click execution. Clicking a ticker in an action item does not navigate or trigger a trade.

---

## 7. Responsive Behaviour

- Full-width card (matches session-summary card container width)
- Desktop: action list in single column
- Mobile: action list in single column, chips above ticker text (stacked)

---

## 8. Constraints

**§13 compliance:** This component is display-only advisory. The system presents AI-generated synthesis; it does not execute any action. The advisory label must be permanently visible. No action type (EXIT, ENTER, MONITOR, HOLD) must be executable from this card.

**AI model:** `claude-sonnet-4-6` (per ST-06 AC-05). This is a backend concern; the frontend renders `response.summary` and `response.actions` as received.

---

## 9. API Dependency

| Endpoint | Direction | Purpose |
|----------|-----------|---------|
| `POST /ai/daily-briefing` | Trigger | Generates briefing; returns `{ summary: string, actions: [{type, ticker, description}], generated_at: ISO-8601, advisory: true }` |

`advisory: true` in the response must be verified client-side — if `advisory: false` or absent, display an error rather than the response body.
