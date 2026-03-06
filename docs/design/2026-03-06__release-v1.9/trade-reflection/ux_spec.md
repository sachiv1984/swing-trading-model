# UX Decision Record — Structured Trade Reflection Template (ST-02)

**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-06__release-v1.9
**Last Updated:** 2026-03-06
**Approved by:** Product Owner — 2026-03-06

---

## Feature

A structured reflection form that appears at trade close. Pre-populated with trade data. Guides the user through structured reflection questions.

## Trigger

The reflection form is presented when a trade is closed (position exited). It appears as a modal or dedicated step in the exit flow — not a separate page navigation.

**Implementation approach:** Modal overlay triggered on trade close confirmation. The user may dismiss it (skip) or complete it.

## Layout — Pre-populated Trade Summary (top section, read-only)

```
[ Trade Closed: AAPL ]
─────────────────────────────────────
Ticker:       AAPL           Hold Time:    47 days
Exit Date:    2026-03-06     R-Multiple:   1.8R
Exit Reason:  Stop-loss      Exit State:   PROFITABLE
Entry Price:  £142.30        Exit Price:   £168.40
```

- Read-only data strip at top
- Fields: ticker, entry price, exit price, hold time (days), R-multiple, exit reason (STOP / MANUAL / REGIME), exit state (GRACE / LOSING / PROFITABLE)

## Layout — Reflection Questions (editable section)

Five structured fields, each with a short prompt and a free-text textarea (max 500 chars each):

1. **Trade Rationale** — "Why did you enter this trade? What was the setup?"
2. **What Worked** — "What did the trade do well? Was the setup validated?"
3. **What Didn't Work** — "What went wrong or was unexpected?"
4. **Discipline Assessment** — "Did you follow your rules? Any impulse decisions?"
5. **Key Takeaway** — "One lesson from this trade."

All fields optional. User may submit with any subset completed.

## Interactions

| Action | Behaviour |
|--------|-----------|
| Skip | Dismiss modal; reflection not stored; trade close completes normally |
| Save Reflection | Submit all completed fields; close modal; show brief success toast |
| Submit with empty fields | Permitted; stored as empty strings |

## States

| State | Behaviour |
|-------|-----------|
| Modal open | Pre-populated summary at top; empty text fields |
| Saving | Submit button shows loading; fields disabled |
| Save error | Error message inline; fields re-enabled; user may retry or skip |
| Save success | Modal closes; brief toast notification |

## Storage

Reflection entries stored server-side linked to the trade/position record. Retrievable at any time from trade history view (future enhancement — link not required at v1.9; backend must store and expose the data).

## Acceptance Criteria for UX

- Modal triggers on trade close confirmation
- Pre-populated read-only summary at top with 8 fields
- Five reflection questions with textarea inputs
- Skip button (no storage) and Save button
- Loading, error, and success states per above
- No AI; all deterministic
