**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Cycle:** 2026-05-18__release-v3.7
**Story:** ST-02 (EPIC-01) — BLG-FE-33 frontend
**Sources:** BLG-FE-33 (backlog), signals.md v0.2, ST-01 (PATCH /signals/{id} watchlisted support)
**Approved by:** Product Owner
**Approved date:** 2026-05-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Signals Page: Add to Watchlist CTA (BLG-FE-33)

This spec defines the frontend interaction model for replacing the "Add Position" CTA on signal cards with "Add to Watchlist", enforcing the signal → watchlist → research → plan → entry workflow.

---

## 1. Design Intent

Replace the "Add Position" primary action on new signal cards with "Add to Watchlist". When the user acts on a signal, it is routed to the watchlist for further research before any position entry decision. This enforces the disciplined entry funnel introduced in Arc 2.

The signal card must make the workflow direction unambiguous: a new signal goes to the watchlist first; a watchlisted signal is navigated to via the watchlist.

---

## 2. Signal Card States

### 2.1 New Signal (default state — not yet actioned)

The primary action is **"Add to Watchlist"** (replaces the previous "Add Position" button).

| Element | Spec |
|---------|------|
| Primary CTA | "Add to Watchlist" button — primary styling |
| Secondary CTA | "Dismiss" button — secondary/ghost styling |
| Visibility rule | Shown on all signal cards where `status ≠ watchlisted` and `status ≠ dismissed` |

### 2.2 Watchlisted State

When a signal has been successfully added to the watchlist (after "Add to Watchlist" is clicked and the API calls complete), the card transitions to watchlisted state:

| Element | Spec |
|---------|------|
| Status indicator | "Added to Watchlist" label (muted, non-interactive) or equivalent visual indicator |
| Navigation CTA | **"View in Watchlist"** link — navigates to `/watchlist` |
| Action buttons | No action buttons remain (neither "Add to Watchlist" nor "Dismiss") |
| Persistence | Watchlisted state persists across page refreshes (backend-driven via `signal.status = "watchlisted"`) |

---

## 3. Interaction Flow — "Add to Watchlist"

**Trigger:** User clicks "Add to Watchlist" on a new signal card.

**Step 1 — Watchlist entry creation:**
Call `POST /watchlist` with:
- `ticker` — from signal
- `market` — from signal
- `initial_stop_price` — pre-filled from signal's suggested stop value (if available); otherwise null

**Step 2 — Signal status update:**
On successful `POST /watchlist` response, call:
`PATCH /signals/{id}` with `{ "status": "watchlisted" }`

**Step 3 — Card state transition:**
Signal card transitions to watchlisted state (§2.2). "View in Watchlist" link shown.

**Loading state:** Button shows loading indicator (disabled) during the `POST /watchlist` call.

**Error handling:**
- If `POST /watchlist` fails: show inline error on the card ("Could not add to watchlist. Try again."); card remains in new state.
- If `PATCH /signals/{id}` fails after successful watchlist add: card transitions to watchlisted state regardless (watchlist entry was created; signal status update failure is non-blocking). No error shown to user.

---

## 4. Duplicate Add Handling

If the ticker is already on the watchlist (`POST /watchlist` returns a 409 or equivalent duplicate response):

- Toast notification: **"Already on your watchlist"**
- Proceed with `PATCH /signals/{id} status=watchlisted` regardless
- Card transitions to watchlisted state (the intent is fulfilled — the ticker is on the watchlist)

---

## 5. Dismiss Flow (unchanged)

"Dismiss" button behaviour is unchanged from the current implementation:
- Calls `PATCH /signals/{id}` with `{ "status": "dismissed" }` (or equivalent existing mechanism)
- Card transitions to dismissed state

The "Dismiss" button is retained as a secondary action on new signal cards.

---

## 6. Non-Regression Rules

- No signal card should show "Add Position" as a CTA (this CTA is removed from the signals page entirely)
- Dismissed signal cards are unaffected — dismissal flow unchanged
- Watchlisted signal cards rendered from backend `status = "watchlisted"` must show the watchlisted state on page load (not just post-click)
- Other pages (Watchlist, Trade Plans, Positions) are unaffected by this change

---

## 7. §13 Compliance

This feature is a workflow routing change — it changes the destination of user intent (watchlist instead of direct position entry) but does not automate any trading decision. The user retains full control of all downstream actions (research, plan creation, position entry). No automated position entry or trade recommendation is generated.

---

## 8. Accessibility

- "Add to Watchlist" button has descriptive text (no icon-only pattern)
- "View in Watchlist" link has descriptive text
- Loading state: button `aria-busy="true"` or `disabled` attribute during API call
- Toast notification is announced via `aria-live` region (consistent with existing toast pattern)
