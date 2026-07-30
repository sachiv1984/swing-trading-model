**Owner:** Head of UX & Design
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-29
**Cycle:** 2026-07-28__release-v7.10 (ST-20 — BLG-FE-134)

---

# Keyboard Navigation & Focus-Order Audit

## Purpose

ST-20 (BLG-FE-134): audit keyboard navigation and focus order across the app's primary flows — trade entry, trade plan, command palette — and file findings as follow-up items.

## Method

Static code review of `src/pages/TradeEntry.js`, `src/pages/TradePlan.js`, `src/components/CommandPalette.js`, and the shared UI primitives they're built from (`src/components/ui/{dialog,select,command,input,button}.js`). No live browser was available to this audit (chromium is not installable on this environment's OS), so findings are derived from reading the actual interaction-handling code — every finding below was independently verified by reading the exact cited lines, not taken on trust from a single pass.

For each interactive element, checked: (1) real semantic element (`<button>`, native form control) vs. a `<div>`/`<span>` with only `onClick`; (2) for any custom modal, focus trap + restoration + Escape handling; (3) any non-default `tabIndex` or DOM-order/visual-order mismatch; (4) any `outline-none` without a replacement visible focus style; (5) for the command palette specifically, whether the app's own code interferes with the underlying `cmdk`/Radix library's built-in keyboard handling.

## Findings

**4 findings, concentrated entirely in `TradePlan.js`.** `TradeEntry.js` and `CommandPalette.js` had no issues — both are built from semantic HTML and Radix primitives (`Select`, `Dialog`, `cmdk`'s `CommandPrimitive`) that provide correct keyboard behaviour by default, and the app's own wrapper code around the command palette (a global `Cmd/Ctrl-K` listener, correctly suppressed while focus is in a form field) does not interfere with that.

| # | Severity | File | Line | Finding |
|---|----------|------|------|---------|
| 1 | **P1** | `src/components/trades/EntryChecklist.js` | ~14-19 | Pre-Entry Checklist rows are `<div onClick={...}>` with no `onKeyDown`, `role`, or `tabIndex` — completely unreachable and untoggleable by keyboard. Core Trade Plan interaction. Filed: `BLG-FE-135`. |
| 2 | **P1** | `src/pages/TradePlan.js` | ~1051 | "Abandon Plan" modal is a hand-rolled overlay (not the codebase's usual Radix `Dialog`) — no focus trap, no initial focus, no Escape handler, no focus restoration on close. Filed: `BLG-FE-136`. |
| 3 | **P2** | `src/pages/TradePlan.js` | ~775 | Trade-tag suggestion buttons use `onMouseDown` with no `onClick` — Tab+Enter/Space does nothing (mouse-only selection). A keyboard workaround exists (type full tag + Enter). Inconsistent with `TradeEntry.js`'s equivalent buttons, which correctly use `onClick`. Filed: `BLG-FE-137`. |
| 4 | **P3** | `src/pages/TradePlan.js` | 8 locations (306, 319, 682, 692, 767, 796, 989, 1069) | Native form fields use `focus:outline-none` + a border-colour shift instead of the `focus-visible:ring-*` pattern used consistently by this codebase's shared UI primitives — a real but lower-contrast focus cue. Filed: `BLG-FE-138`. |

## Disposition

No P0 found. 2 P1s, 1 P2, 1 P3 — all filed as follow-up items (`BLG-FE-135` through `BLG-FE-138`) per this story's acceptance criteria ("findings filed as follow-up items where gaps are found"), rather than fixed directly in this story: these are behavioural/interaction fixes to production UI flows that would need live-browser or staging verification before merge per CLAUDE.md §2's frontend testing gate, which this audit-only story's own scope and this environment's tooling constraints (no chromium available) don't support doing safely in the same change.

**Overall assessment:** keyboard navigation is fundamentally sound across the three audited flows — the two P1 findings are real and concentrated in one page (`TradePlan.js`), not systemic across the app. `TradeEntry.js` and `CommandPalette.js` (the latter built on `cmdk` + Radix `Dialog`, both keyboard-accessible by design) had no findings.

## Sign-off

**Head of UX & Design:** Confirmed — audit complete across all 3 named primary flows; 4 findings (2 P1, 1 P2, 1 P3), all filed as follow-up items with clear scope and acceptance criteria for remediation. 2026-07-29.
