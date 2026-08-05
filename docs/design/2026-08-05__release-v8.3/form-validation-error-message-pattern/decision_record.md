**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-08-05
**Cycle:** 2026-08-05__release-v8.3
**Story:** ST-21 (BLG-SPEC-108, EPIC-04)

# UX Decision Record — Canonical Form Validation Error-Message Pattern

## 1. Problem

No canonical spec exists for inline form-validation error styling, placement, trigger timing, or wording. Two shipped instances were checked directly against source and found to diverge on trigger timing:

- `WatchlistModal.js:46` — `"Ticker is required."` shown only on submit attempt (no on-blur validation).
- `TradePlan.js:1097` — `"Reason must be at least 10 characters."` shown on blur (`touched` flag) as well as on submit.

Both use the same visual treatment (`text-xs text-rose-400`, sentence case, ends with a period, directly below the field) — so the wording/placement/style convention is already consistent in practice; only the trigger-timing question is genuinely unresolved, plus a latent contrast gap (below).

## 2. Trigger timing (the one real decision this spec makes)

Canonical rule — unifies both existing entry points rather than deprecating either:

> Show a field's inline error when **(a)** the field has been blurred at least once and is currently invalid, **or (b)** a submit attempt has occurred, regardless of touched state.

This covers `TradePlan.js`'s existing blur-based behaviour and `WatchlistModal.js`'s existing submit-based behaviour as the same rule's two entry paths — an untouched required field only surfaces its error at submit time (matching `WatchlistModal`'s current behaviour); a touched-then-left-invalid field surfaces immediately on blur (matching `TradePlan`'s current behaviour). Neither existing shipped instance needs to change.

## 3. Placement

Directly below the field, above any helper/example text, full field width. No icon (text-only, matching both existing instances).

## 4. Wording convention

- Sentence case, ends with a period.
- States the violated rule in plain language a user without technical context understands (`"Ticker is required."`, `"Reason must be at least 10 characters."`).
- No backend/technical vocabulary (no status codes, no raw field names, no schema terms).
- One message per field at a time — do not stack multiple violated-rule messages under a single field; show the first/most-relevant one.
- Clears immediately on the next input change that satisfies the rule (not gated on the next blur/submit).

## 5. Colour token (closes a latent contrast gap)

Both existing instances use a bare `text-rose-400` with no `dark:`-paired light-mode value — the same dark-only-token defect class already flagged twice elsewhere (`BLG-FE-87/88`, `BLG-FE-95`; `design_system.md` §Color Usage "Secondary/label text" token note, §Accessibility "Consolidated dark-mode contrast audit"). Canonical pair, computed the same way as the existing `text-slate-600 dark:text-slate-400` label-text token (WCAG 2.1 relative-luminance contrast, ≥4.5:1 required for normal-size text):

- **Dark:** `text-rose-400` on `bg-slate-800` — **5.43:1** (unchanged from current shipped value; PASS).
- **Light:** `text-rose-700` on `bg-slate-100` — **5.74:1** (new; `text-rose-600` was checked and measured **4.29:1**, below the 4.5:1 threshold, so `rose-700` is adopted instead for a safe margin, consistent with the existing label-text token's precedent of choosing a stronger shade for light mode rather than a borderline pass).

Canonical class: `text-xs text-rose-700 dark:text-rose-400`.

## 6. Scope boundary

This spec covers tone/placement/wording/trigger-timing/colour only. Cross-field behaviours (e.g. moving focus to the first invalid field on submit) are out of scope — no such behaviour exists today in either checked instance, and inventing one here would exceed the story's acceptance criteria. File a follow-up item if that becomes a real need.

## §13 check

Purely presentational form-validation UI; no automated decision or AI call. Not applicable.

## Sign-off

- Head of UX & Design: approved 2026-08-05
- Product Owner: approved 2026-08-05
- Frontend Specifications & UX Documentation Owner: approved 2026-08-05
