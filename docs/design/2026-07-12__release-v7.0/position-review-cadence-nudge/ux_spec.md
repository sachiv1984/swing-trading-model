**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-12
**Approved by:** Product Owner — 2026-07-12
**Story:** ST-15 — Position review cadence nudge (BLG-FEAT-68)
**Cycle:** 2026-07-12__release-v7.0

---

# UX Specification — Position Review Cadence Nudge

## 1. Purpose

Existing prompts (Grace Period Alert Zone, Drawdown Review Prompt) only fire on price/performance triggers — a quietly-performing position (neither in grace, nor losing, nor drawdown-flagged) can go unreviewed indefinitely. This adds a low-priority, ongoing per-position indicator, not a new Alert Zone banner — it must not compete visually with the existing higher-priority safety alerts (RISK OFF, GAP RISK, Trail Stop breach, Grace Period).

## 2. Placement

**Table View:** New "Last Reviewed" column, positioned after "Alerts" and before "Actions" — lowest visual priority of the alert-adjacent columns, consistent with this being an informational nudge rather than a risk flag.

**Grid View:** Added to card footer, after the existing alert-icon row, before the Actions row.

## 3. Display

| Element | Spec |
|---|---|
| Data source | `last_reviewed_at` (ISO timestamp, nullable) — new field on `GET /positions` |
| Display (not flagged) | "Reviewed {N}d ago" — plain text, `text-slate-500 dark:text-slate-400` (existing secondary-text token, BLG-FE-89) |
| Display (never reviewed) | "Not yet reviewed" — same styling |
| Flag threshold | `days_since_review ≥ 14` (default; server-configurable constant, not user-editable this cycle) |
| Flagged display | Text switches to amber (`text-amber-600 dark:text-amber-400`) + a small clock icon prefix; label unchanged ("Reviewed {N}d ago" / "Not yet reviewed") — icon + colour only, no separate badge/pill (keeps it visually subordinate to the Alerts column's pill badges) |
| `aria-label` | "Position not reviewed in {N} days — consider reviewing" (flagged) / "Last reviewed {N} days ago" (not flagged) |

## 4. Mark Reviewed Action

- Small icon-button (checkmark) inline next to the Last Reviewed text — not a full Actions-column button, to keep it lightweight for a non-safety-critical action
- Click → `PATCH /positions/{id}/mark-reviewed` (sets `last_reviewed_at = now()` server-side) → text resets to "Reviewed 0d ago", flag/amber state clears immediately (optimistic update)
- No confirmation modal — reversible-in-spirit, low-stakes action; matches the precedent set by other low-friction display toggles on this page

## 5. Suppression Rule (AC-04)

The review-cadence flag (amber state) does **not** fire when the position is already surfaced by:

- Grace Period Alert Zone (`position_state = 'GRACE'` AND `days_in_state ≥ 8`), or
- Drawdown Review Prompt (position included in the portfolio-level drawdown banner's position count)

Rationale: both existing prompts already ask the user to review the position for a more urgent reason — a second, lower-priority nudge for the same position is noise, not signal. The "Last Reviewed" text itself still renders (informational), but never switches to the flagged/amber state while either condition holds. `days_since_review` continues counting underneath — if the position later exits GRACE/drawdown scope while still stale, the flag can fire on the next refresh.

## 6. §13 Compliance

Display-only. No automated action beyond timestamp update on explicit user click. No recommendation, no directional signal.

## 7. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-12
- **Product Owner:** Approved — 2026-07-12
