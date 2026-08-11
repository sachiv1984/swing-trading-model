**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-08-11
**Cycle:** 2026-08-11__release-v8.6
**Story:** ST-07 (BLG-FE-150, EPIC-03)

# UX Decision Record — Should Modals/Dialogs Support Light Theme?

## 1. Problem

v8.5's ST-13 dark/light contrast audit found that 4 of 5 checked `Dialog`-based components (`WatchlistModal.js`, `ExportModal.js`, `PositionEntryModal.js`, `WidgetLibrary.js`) hardcode `DialogContent` styling to `bg-slate-900 ... text-white` unconditionally, regardless of the app's active theme setting — a light-theme completeness gap, consistent and long-standing across every consumer checked. The one exception, `CommandDialog` (`src/components/ui/command.js`), correctly uses the shared theme-aware tokens (`bg-background`, `text-foreground`, `text-muted-foreground`). Classified Design Required per `design_gate_prompt.md` §6 (this item *is* the design decision itself, no implementation to classify separately).

## 2. Decision

**Dark-only modal styling is not intentional — it is legacy drift.** Modals/dialogs should adopt the same light/dark theme-awareness as the rest of the app, matching `CommandDialog`'s already-correct pattern.

**Rationale for this direction (not the alternative):**
- The app's overall design direction is full light/dark theme parity, not dark-first with light as an afterthought — this is the explicit subject of multiple other items in this same cycle (`ST-04`/`BLG-FE-147` token registration, `ST-06`/`BLG-FE-149` secondary-text drift fixes) and prior cycles (`ST-06`/v8.5 `-muted` tokens, the v6.7 secondary-text token itself, the v7.8 dark-mode contrast audit). Declaring modals a permanent, intentional dark-only exception would cut directly against that established direction rather than align with it.
- `CommandDialog` already proves the theme-aware pattern works correctly for a `Dialog`-based component in this codebase — this is not a novel pattern requiring new design work, it is applying an already-shipped, already-correct pattern to the 4 remaining consumers.
- No stated product reason exists for modals specifically to be dark-only (e.g. no "modals are always shown over a dark scrim" or similar rationale was found in `design_system.md` or any modal-related design source) — the inconsistency reads as an artefact of each modal being built independently before the shared token pattern existed, not a deliberate choice.

**Follow-up implementation item:** `BLG-FE-156` (filed by PMO Lead, 2026-08-11, outside this gate's own write scope per `design_gate_prompt.md` §5) — convert the 4 hardcoding consumers (`WatchlistModal.js`, `ExportModal.js`, `PositionEntryModal.js`, `WidgetLibrary.js`) from `bg-slate-900`/`text-white` to the shared `bg-background`/`text-foreground`/`text-popover`/`text-popover-foreground` token set — a genuinely new implementation item (this design decision alone does not ship the fix). Sequencing note: this follow-up should land no earlier than `ST-04`/`BLG-FE-147` (this cycle), since `bg-popover`/`text-popover-foreground` are among the tokens `ST-04` registers in `tailwind.config.js` — building the fix before those tokens compile would silently reproduce the exact "empty CSS rule" failure mode `BLG-FE-147` exists to close.

## 3. Documented in `design_system.md`

New sub-entry under §Shared UI Components → (existing) Confirmation Modal area, or a new "Modal / Dialog Theming" note, recording: modals use the shared `bg-background`/`text-foreground` (or `bg-popover`/`text-popover-foreground` where a popover-elevation surface is more appropriate than the page background) token set, consistent with every other themed surface in the app; `CommandDialog` is the canonical reference implementation; the 4 named consumers are known non-compliant instances pending their own follow-up item.

## §13 check

Pure visual/theming decision; no automated decision, no AI call. Not applicable.
