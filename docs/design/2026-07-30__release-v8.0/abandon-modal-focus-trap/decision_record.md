**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-07-30
**Cycle:** 2026-07-30__release-v8.0
**Backlog source:** BLG-FE-136
**Maps to:** EPIC-02, ST-07

---

# Decision Record — Abandon Trade Plan Modal Focus Trap Fix

## 1. Scope

This is an accessibility/interaction fix to an existing, already-designed modal — not a new visual surface. The Abandonment Modal's title, body copy, required-field validation, and actions (`trade_plan.md` §8.2) are unchanged and remain governing. This record fixes only the focus-management contract, by replacing the hand-rolled modal overlay with the existing Radix-based `src/components/ui/dialog.js` `Dialog` primitive already used elsewhere in the app.

**In scope:** Abandonment Modal (`trade_plan.md` §8.2) only.

**Out of scope:** any other hand-rolled modal/overlay in the app — not part of this fix; each would need its own audit if raised separately.

## 2. Standard Applied

WAI-ARIA Dialog (Modal) pattern, delivered via the existing `Dialog` primitive's built-in focus-management (Radix `DialogPrimitive`), which already implements this pattern correctly for every other modal in the app:

- Focus moves into the dialog on open (first focusable element, or the dialog container if none)
- Tab / Shift+Tab cycle only among focusable elements inside the dialog while open — focus cannot land on background page content
- Escape closes the dialog (equivalent to "Cancel" — no change submitted)
- Focus returns to the triggering "Abandon" button on close, whether closed via Cancel, Escape, backdrop click, or successful submission

## 3. Interaction Spec

| Input / Event | Behaviour |
|----------------|-----------|
| Open (click "Abandon") | Focus moves into modal, onto the abandonment-reason textarea (first focusable field) |
| Tab / Shift+Tab | Cycles among textarea → "Cancel" → "Abandon Plan" → dialog close (X) → (wraps back to textarea); never exits to background content. Order corrected post-implementation (2026-07-30) to match the modal's actual, deliberately-unchanged button DOM/visual order (Cancel rendered before the submit action) — reordering to the originally-drafted "Abandon Plan → Cancel" sequence would have required flipping the visual left/right button positions, contradicting this record's own "visual design unaffected" constraint (§1). The Dialog primitive's default corner close (X) button is also part of the cycle, consistent with every other Dialog-based modal in the app. |
| Escape | Closes modal, no change; focus returns to "Abandon" button |
| Cancel click | Closes modal, no change; focus returns to "Abandon" button |
| Backdrop click | Closes modal, no change; focus returns to "Abandon" button (standard `Dialog` primitive behaviour) |
| Successful submit | Modal closes; focus returns to "Abandon" button's prior DOM position — if the button itself is now hidden (§8.3: "Abandon" and "Edit" hidden post-abandonment), focus falls through to the nearest remaining focusable element per the `Dialog` primitive's default fallback (no custom handling needed) |

No new states are introduced. The required-field validation (min 10 chars, inline on blur, confirm button disabled until valid — §8.2) and the amber-outlined, non-primary visual treatment of "Abandon" (§8.1) are unaffected — the `Dialog` primitive is a drop-in replacement for the overlay/positioning/focus mechanics only.

## 4. Compliance Check

No conflict with `strategy_rules.md §13` — pure accessibility/interaction fix, no automated decision-making or new data surface. Not an analytics/metrics feature.

## 5. Sign-off

- **Head of UX & Design:** Approved — 2026-07-30 (interaction spec per §3; existing visual design in `trade_plan.md` §8.2 confirmed current and unaffected)
- **Product Owner:** Approved — 2026-07-30 (scope confirmed as accessibility fix only, no new design round-trip required)
