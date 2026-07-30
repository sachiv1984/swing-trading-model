**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-07-30
**Cycle:** 2026-07-30__release-v8.0
**Backlog source:** BLG-FE-135
**Maps to:** EPIC-02, ST-06

---

# Decision Record — Pre-Trade Entry Checklist Keyboard Accessibility Fix

## 1. Scope

This is an accessibility/interaction fix to an existing, already-designed component — not a new visual surface. The checklist's layout, labels, and pre-population behaviour (`trade_plan.md` §6) are unchanged and remain governing. This record fixes only the interaction contract for `EntryChecklist.js`'s `CheckItem`.

**In scope:** `CheckItem` within the Pre-Trade Entry Checklist (`trade_plan.md` §6.2), creation and edit forms only. Read-only detail-view state (§6.4) is not interactive today and is out of scope — no checkbox affordance exists there to make keyboard-reachable.

**Out of scope:** any other checklist-like control in the app (e.g. Bulk Actions row-selection checkboxes, §11) — not part of this fix.

## 2. Standard Applied

WAI-ARIA checkbox pattern (native semantics substitute, since `CheckItem` is a custom element rather than `<input type="checkbox">`):

- Rendered as `<button role="checkbox" aria-checked={item.checked}>` (or an element with equivalent `tabIndex="0"` + `role="checkbox"` + `aria-checked` + `onKeyDown` handling for Space/Enter)
- Included in the natural document Tab order alongside the other form fields — no `tabIndex="-1"` or click-only handling
- Visual appearance unchanged: same checkbox glyph, label, and layout as today; this is a semantics/interaction fix, not a redesign

## 3. Interaction Spec

| Input | Behaviour |
|-------|-----------|
| Tab / Shift+Tab | Moves focus onto/off each `CheckItem` in list order, same position in the tab sequence as the visible checkbox today |
| Space | Toggles `checked` state; `aria-checked` updates to match |
| Enter | Toggles `checked` state (same as Space — common convention for custom checkbox-role controls); `aria-checked` updates to match |
| Click | Unchanged — existing mouse toggle behaviour preserved |
| Focus-visible | Existing global `focus-visible` ring token (`design_system.md` §Hover & Focus States, ≥3:1 contrast) applies — no new focus style needed |

No new states are introduced. Pre-population rules (§6.2), the "advisory, user may uncheck" behaviour, and persistence (§6.5) are unaffected.

## 4. Compliance Check

No conflict with `strategy_rules.md §13` — pure accessibility/interaction fix, no automated decision-making or new data surface. Not an analytics/metrics feature.

## 5. Sign-off

- **Head of UX & Design:** Approved — 2026-07-30 (interaction spec per §3; existing visual design in `trade_plan.md` §6 confirmed current and unaffected)
- **Product Owner:** Approved — 2026-07-30 (scope confirmed as accessibility fix only, no new design round-trip required)
