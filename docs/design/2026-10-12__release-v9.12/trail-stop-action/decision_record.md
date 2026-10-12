**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-12__release-v9.12
**Story:** ST-10 (EPIC-02, BLG-BE-159)

# Decision Record — Trail Stop Modal: Apply Against a Real Route, or Become Read-Only

## 1. Problem

The Trail Stop modal on Positions applies a recommended stop with `PATCH /positions/{id}` and body `{stop_price}`. No such route exists, so every apply fails with "Failed to update stop". `positions.md` §Trail Stop Action also names a third method (`PUT /positions/{id}`) that does not exist either.

The modal also offers **"Lower stop to {value}"** when `trail_difference` is negative. `strategy_rules.md` §7.3 says stops never move down, so that label must not be offered under any ruling.

ST-10's first sub-step is a Strategy Rules & System Intent Owner ruling on whether a user may set or raise a stop manually (RISK-02). This record designs both outcomes, so the story can ship whichever the ruling picks without a second design pass. It follows the v9.10 ST-14 precedent of a spec section conditional on an in-story disposition.

## 2. Decision

### 2.1 Common to both branches

- The "Lower stop to {value}" label is removed. Nothing in the modal may propose a lower stop.
- When `trail_difference ≤ 0`, the modal shows a note in place of an action (`data-testid="trail-stop-no-raise-note"`, `text-xs text-slate-600 dark:text-slate-400`): "The ATR trail stop is at or below your current stop. Stops never move down (§7.3), so there is nothing to apply."
- The data rows (Current Stop, ATR Trail Stop, Raise by, Trail in R) and the footnote are unchanged. A negative "Raise by" keeps its amber colour, using the paired token `text-amber-700 dark:text-amber-400`.

### 2.2 Branch A — the ruling permits a manual raise

- **Route:** `PATCH /positions/{id}/stop`, body `{ "stop_price": <native> }`. The server rejects with 400 any value at or below the stored `current_stop` (ratchet, §7.3) or at or above the current price. Error body uses the canonical envelope.
- **Confirm button** (primary), shown only when `trail_difference > 0`: "Raise stop to {atr_trail_stop}" (native currency, 2 dp). The button is disabled while the request is in flight, with the label "Raising…".
- **On success:** the modal closes, the positions query is invalidated, and a success toast reads "Stop raised to {value}." (existing toast-timing standard).
- **On failure:** the modal stays open. An error toast shows the server's message (error duration per the toast-timing standard).
- Later system recomputes still apply `max(current, new)`, so a manual raise is never undone by them.

### 2.3 Branch B — the ruling does not permit a manual stop change

- The modal becomes a read-only comparison. The confirm button is removed. The only control is "Close" (secondary), plus Escape and ✕.
- An added line under the footnote (`data-testid="trail-stop-readonly-note"`): "The system updates stops automatically when positions load and each night. This view is for reference only."
- The Actions button is renamed **"View Trail"** so it no longer implies an action. Its visibility and disabled rules are unchanged.
- No route is added, so no registration chain applies.

### 2.4 Supplied entry stop (AC 3)

Trade Entry has sent no `stop_price` since v9.10 (`position_form.md` v1.8), so neither outcome changes the UI. The recommended backend outcome is to **reject** a supplied `stop_price` on `POST /portfolio/position` with a 400: "stop_price is not accepted. The initial stop is set by the system at Entry − 5× ATR (§5)." This matches the read-only Initial Stop panel. Storing it would contradict that panel and needs its own design pass.

## 3. §13 Compliance

Deterministic. No AI. Branch A keeps the human in the loop: the system presents the calculation and the user confirms it. That is the existing §13 constraint on this modal.

## 4. Frontend Spec Impact

`positions.md` v2.15 → v2.16: §Trail Stop Action rewritten with both branches. The story deletes the branch not taken, in the same commit as the code.

## 5. Obligations for Sprint Execution

- Branch A adds a route: a `##` contract heading, an `openapi.yaml` entry, a `backend/routers/test.py` entry, the `SystemStatus.js` fallback count and `SC-SS-01b`, all in the same commit (CLAUDE.md §2, RISK-04).
- Record the ruling before the code change (AC 1).
- ST-15 edits the same stop-cell area and is sequenced after this story.

## 6. Testability (CLAUDE.md §2)

- Playwright, mocked `stop-trail` with a positive difference: Branch A shows "Raise stop to …", the click sends `PATCH /positions/{id}/stop`, and the success toast appears. Branch B shows no confirm button, and the read-only note is visible.
- Playwright, mocked negative difference: no apply button in either branch, and the no-raise note is visible.
- Branch A backend test: a value at or below the stored stop is rejected with 400.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-12.
Product Owner: confirmed, 2026-10-12.
