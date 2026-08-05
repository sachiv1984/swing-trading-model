**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-08-05
**Cycle:** 2026-08-05__release-v8.3
**Story:** ST-12 (BLG-FE-121, EPIC-03)

# UX Decision Record — Shared Modal-Confirmation Component (with optional undo-window)

## 1. Problem

`BLG-FE-117` (bulk actions, not yet in scope) will need a confirmation-modal pattern with an undo window; `BLG-FE-116` (custom price alerts) will likely need a plain confirmation-modal. This story extracts a single reusable component ahead of both, to avoid two near-duplicate implementations shipping in the same release. Two existing confirmation-modal instances already exist in the app (`positions.md` §Exit action, `watchlist.md` §Remove Confirmation Prompt) — neither has an undo window. No prior artefact defines an undo-window countdown pattern; this is genuinely new interaction design, not a restatement of an existing pattern.

## 2. Component

`src/components/ui/ConfirmationModal.js` (new shared primitive).

Props:
| Prop | Type | Notes |
|------|------|-------|
| `message` | string (required) | The confirmation question, sentence case, ends with `?` |
| `confirmLabel` / `cancelLabel` | string | Default `"Confirm"` / `"Cancel"` |
| `destructive` | boolean | Styles the confirm action as destructive (existing destructive-button token) |
| `undoWindow` | `{ enabled: boolean, durationSeconds: number }` | Optional. Default `{ enabled: false }` |

## 3. Interaction — Standard variant (`undoWindow.enabled = false`)

Unchanged from existing precedent (`watchlist.md` §Remove Confirmation Prompt): modal opens → user clicks Confirm → action executes on click, modal closes → or Cancel dismisses without action. No new decision required here; this variant formalises existing shipped behaviour as the component's default.

## 4. Interaction — Undo-window variant (`undoWindow.enabled = true`)

1. User clicks the destructive/consequential action → `ConfirmationModal` opens with the standard Confirm/Cancel choice (the countdown does not run inside the modal — the modal itself behaves exactly as the standard variant).
2. User clicks Confirm → modal closes immediately, action executes optimistically (same optimistic-update pattern already used for "Mark Reviewed" and watchlist "Keep" — `positions.md` §Last Reviewed, `watchlist.md` §Staleness).
3. A toast opens (`sonner`) carrying: the action's past-tense confirmation text (e.g. `"3 positions removed."`) + a visible **"Undo (Ns)"** button, where `N` counts down from `durationSeconds`. The button label itself carries the countdown as text — never a bar/ring alone — so the remaining time is never colour- or shape-only information (per `design_system.md` Accessibility: "colour is never the sole differentiator").
4. **Default `durationSeconds`: 5.** This explicitly overrides `sonner`'s ~4s auto-dismiss default (`design_system.md` §Shared UI Components → Standing Alert) because the toast here is actionable, not purely informational — it needs enough time for a deliberate click, not just a glance.
5. If **Undo** is clicked before expiry: the pending action is reversed client-side (caller supplies the inverse operation — e.g. re-POST the removed item, or cancel a request not yet fired to the server if the implementation defers the network call until the window expires; left to each consumer's own data shape, out of scope for this shared component to prescribe) and the toast is replaced with a brief non-actionable confirmation toast, `"Undone."`, default `sonner` duration.
6. If the window expires without Undo: the toast auto-dismisses, the action is final. No further confirmation is shown (consistent with the optimistic-update precedent already in use elsewhere — success is silent).

## 5. Accessibility

- Modal: focus trap + restoration (existing `Dialog` primitive convention, `TradePlan.js` Abandon modal precedent), Escape = Cancel.
- Undo toast: the "Undo" control is a real focusable/clickable button (not a decorative countdown), reachable via the existing `sonner` toast focus/dismiss handling already used elsewhere in the app.
- Countdown is announced via visible text, not colour or animation alone.

## 6. §13 check

No automated decision or AI call involved — purely a confirm/undo interaction primitive. Not applicable.

## 7. Scope boundary

This record defines the shared component and its two variants. It does **not** design `BLG-FE-116`/`BLG-FE-117`'s specific confirmation copy or which of their actions get the undo-window variant — those are each item's own design-gate pass when they enter scope.

## Sign-off

- Head of UX & Design: approved 2026-08-05
- Product Owner: approved 2026-08-05
