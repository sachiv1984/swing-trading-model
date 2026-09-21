**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-21__release-v9.6
**Story:** ST-04 (EPIC-01, BLG-FEAT-98)

# Decision Record — In-App Reminder to Complete a Trade Reflection After 48 Hours

## 1. Problem

Trade reflections feed Arc 4 (PO-02/PO-04), which are gated on data volume, yet completion depends on the operator remembering. The reflection is a **modal opened at trade close** (`trade_reflection.md` §2–3, "Route: None") and is skippable — so after a skip there is currently **no way back to it and no prompt to return**.

## 2. Decision

### 2.1 Surface — the existing Notification Feed, no new variant

A new alert type **`reflection_reminder`** produces an ordinary Notification Feed row (`notifications.md` §Notification List), reusing the existing layout.

| Element | Content |
|---------|---------|
| Icon | Existing alert-type icon slot — journal/pencil glyph |
| Title | `"Reflection Reminder — {TICKER}"` |
| Message | `"{TICKER} closed on {exit date}. Take a few minutes to record what you learned."` |
| Action link | **"Write reflection"** — inline text link beneath the message |
| Unread indicator / Mark as read / timestamp | Unchanged |

### 2.2 Re-entry point (new — required for the link to work)

The link targets `/TradeHistory?reflect={trade_id}`. On load, Trade History reads the param, opens the **existing** `TradeReflectionModal` for that trade (it already pre-populates from `GET /trades/{trade_id}/reflection` and treats 404 as "none saved yet"), then removes the param from the URL (`replace`, so Back does not reopen it). An unknown/foreign `trade_id` is ignored silently (no modal, no toast).

### 2.3 Trigger and suppression rules

| Rule | Behaviour |
|------|-----------|
| Trigger | A closed trade with **no saved reflection** whose close timestamp is ≥ 48 h ago |
| Timing precision | The reminder appears on the **first notification-evaluation run at or after the 48 h mark** — no minute-level promise |
| Cardinality | **At most one reminder per trade, ever** — idempotent per `trade_id`; never re-created after read, dismissal or completion |
| Completed reflection | Saving a reflection **before** the mark → no reminder is created. Saving **after** the reminder exists → the reminder is auto-marked read |
| Dismissal | The existing per-item **"Mark as read"** is the dismiss action. No separate dismiss control |

### 2.4 Preferences — interpretation recorded

The Notification Preferences model governs **email delivery only** (`notifications.md` §Email Preferences); in-app feed rows for existing alert types are always created. `reflection_reminder` follows the same model:

- New row in the Email Preferences list: **"Reflection Reminder"** — `"Notify by email when a closed trade has no reflection after 48 hours."`
- The in-app feed row is **always** created (it is low-intrusion and dismissible).
- **Email toggle defaults to Off** — a newly introduced alert type must not start emailing the operator unasked.

This is the reading of the backlog's "respects `NotificationPreferences`" adopted for this story (recorded in `stage4_backlog_slice_addendum.md`).

### 2.5 Not-a-nag guarantees

No badge count inflation beyond the standard unread count, no toast, no modal, no repeat. The reminder is a prompt only — nothing is auto-created or auto-submitted (`strategy_rules.md` §3).

### 2.6 Motion / timing

The 48 h interval is a business rule, not a UI motion/timing parameter — §6's motion/timing special rule (BLG-FE-131) is not the basis for classification; "new data displayed" is. No animation, debounce or delay is introduced in the UI.

## 3. §13 Compliance

Deterministic, no AI (`trade_reflection.md` design principle "No AI; fully deterministic and testable" is preserved). No AI-provider call is introduced or extended. §13 pre-check does not apply.

## 4. Frontend Spec Impact

- `notifications.md` v0.8 → v0.9: new `reflection_reminder` type in the feed and in Email Preferences; reminder row spec.
- `trade_reflection.md` (Canonical, v0.1) is **not edited at this gate**. The new `/TradeHistory?reflect=` re-entry is a Trade History behaviour and is specified in `notifications.md`; a cross-reference in `trade_reflection.md` §2 (Trigger) is left to the story's own spec-sync commit.
- Backend contract (`alerts_endpoints.md`, `openapi.yaml`, `backend/routers/test.py` registration) is a Sprint Execution obligation per CLAUDE.md §2 and is out of this gate's write scope.

## 5. Testability (CLAUDE.md §2)

Playwright with mocked feed data: reminder row renders with "Write reflection"; link opens the reflection modal for the right trade and clears the param; marking read removes the indicator; no reminder row for a trade with a saved reflection. The 48 h server-side timing is covered by backend tests, not Playwright.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-21.
Product Owner: confirmed, 2026-09-21 (including the email-only preference interpretation and default-Off).
