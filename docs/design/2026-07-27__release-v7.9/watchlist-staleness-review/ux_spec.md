**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-07-27
**Cycle:** 2026-07-27__release-v7.9
**Backlog source:** BLG-FEAT-66
**Maps to:** EPIC-01, S2-01

---

# UX Spec — Watchlist Staleness and Decay Review

## 1. Problem

`watchlist.md`'s existing flow (DS-07, shipped v3.0) gives a one-click path from a screener result onto the watchlist, but there is no exit path other than promotion to a trade plan via "Add to Position". Entries can accumulate indefinitely with no forcing function to review or remove them.

## 2. Data

- **Source field:** `added_at` (already captured per entry at add time — no backend schema change required)
- **Derived field:** `days_on_watchlist = today - added_at`, computed the same way as the existing `days_since_added`-style calculations elsewhere in the app (server-computed, not client-derived, consistent with the page's existing "signal status is read-only, sourced from backend" convention)
- **Staleness threshold:** 30 days, default. Server-configurable constant (not user-editable this cycle) — same posture as the Positions page's Last Reviewed column 14-day threshold (`positions.md` §Last Reviewed Column).

## 3. Placement & Layout

New column, **"Added"**, in the Watchlist Table (`watchlist.md` §Watchlist Table), placed after "Research" and before "Target Entry" — the table's existing column order runs signal/status metadata first, then price fields; days-on-watchlist is metadata about the entry itself, not a price field, so it belongs with the former group.

### Display (not stale)

`"{N}d"` — e.g. `"12d"`. Muted secondary-text token (`text-slate-500 dark:text-slate-400`, the same existing secondary-text token used by Positions §Last Reviewed Column, BLG-FE-89 — no new token introduced).

### Display (stale, `days_on_watchlist ≥ 30`)

Text switches to amber (`text-amber-600 dark:text-amber-400`) with a small clock icon prefix and switches label format to `"{N}d, no action"` (matches the problem statement's own example phrasing, "45 days, no action"). Icon + colour only — no separate pill/badge, consistent with the Positions page's equivalent Last Reviewed treatment (kept visually subordinate to true alert badges elsewhere in the app).

`aria-label`: `"On watchlist {N} days with no action — consider Keep or Remove"` (stale) / `"Added {N} days ago"` (not stale).

## 4. Explicit User Actions (AC-03, AC-04)

Two actions render in the Actions column for stale entries only (non-stale entries keep the existing Research / Add to Position / Remove actions unchanged):

| Action | Label | Behaviour |
|--------|-------|-----------|
| Keep | "Keep" (secondary, outlined) | Calls `PATCH /watchlist/{id}` with `{ added_at: now() }` — resets the staleness clock. No confirmation modal (non-destructive, reversible by definition — the clock just starts counting again). Toast: `"{TICKER} kept on watchlist."` Row updates optimistically (badge reverts to non-stale state, "Added" reads "0d"). |
| Remove | "Remove" (existing action, unchanged) | Existing `DELETE /watchlist/{id}` flow and confirmation prompt (`watchlist.md` §Edit Modal / §Remove Confirmation Prompt) — no new confirmation path invented for the stale case. |

**No automatic removal (AC-04):** there is no background job, no scheduled sweep, and no silent expiry. The stale badge is advisory only; the row remains on the table indefinitely until a human clicks Keep or Remove. This mirrors the existing Grace Period Alert Zone / Last Reviewed pattern's "human decides" posture (`positions.md` §13 constraints throughout).

## 5. States

| State | Behaviour |
|-------|-----------|
| Loading | Covered by existing Watchlist skeleton rows — no new loading state |
| `added_at` missing (legacy row predating this feature) | Treat as `added_at = today` on first read (fresh, not stale) rather than null/undefined — avoids mass-flagging every pre-existing watchlist entry the instant this ships, mirroring the reasoning already applied to Positions' `last_reviewed_at` NULL handling (`positions.md` §Last Reviewed Column NULL semantics) |

## 6. Compliance Check

No conflict with `strategy_rules.md §13` — advisory-only display and a manual, human-confirmed action (Keep/Remove). No automated decision-making or removal.

## 7. Out of Scope

- Configurable per-user staleness threshold (fixed at 30 days server-side this cycle)
- Any change to the existing Bulk Actions toolbar (v7.5) — Keep/Remove for stale rows remain single-row actions this cycle; bulk-Keep is a candidate future enhancement, not scoped here

## 8. Sign-off

- **Head of UX & Design:** Approved — 2026-07-27
- **Product Owner:** Approved — 2026-07-27
