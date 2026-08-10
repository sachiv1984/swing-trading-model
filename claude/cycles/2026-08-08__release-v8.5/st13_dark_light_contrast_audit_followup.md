Owner: Frontend Specifications & UX Documentation Owner
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-10
Cycle: 2026-08-08__release-v8.5
Story: ST-13 (BLG-FE-100, EPIC-04)

# ST-13 — Dark/Light Theme Contrast Audit Follow-Up

## 1. Purpose

Targeted follow-up contrast audit, scoped to confirm no further secondary-text (or similar) contrast gaps remain beyond `BLG-FE-87`/`BLG-FE-88`/`BLG-FE-89`'s known fixes. Audit-only completion is a valid, complete outcome per this story's Notes (RISK-02) — any drift found is filed as a follow-up, not fixed in-story (distinct from ST-09, whose own audit findings this story cross-checks and extends).

## 2. Cross-check of ST-09's secondary-text token audit

ST-09 (this same EPIC) ran a `grep`-based audit for drift against the v6.7 canonical secondary-text token (`text-slate-600 dark:text-slate-400`) and found 6 instances, filed as `BLG-FE-149`. This story's own independent spot-check (different sampling method — reviewing rendered contrast at the component level rather than class-string grep) did not surface any additional secondary-text instances beyond ST-09's 6. ST-09's audit is confirmed thorough for its scoped class pattern.

## 3. New finding — dialog/modal theming inconsistency (connects to ST-06's dark-mode-portal fix)

While verifying ST-06's `document.documentElement` dark-class-portal fix (this EPIC, same cycle — see `qa_evidence_EPIC-03.md`'s "Critical finding" section), this audit checked how real `Dialog`-based components style their `DialogContent` and found a consistent but unexamined pattern:

| Component | `DialogContent` className |
|-----------|---------------------------|
| `WatchlistModal.js` | `bg-slate-900 border-slate-700 text-white max-w-md` |
| `ExportModal.js` | `bg-slate-900 border-slate-700 text-white max-w-md` |
| `PositionEntryModal.js` | `bg-slate-900 border-slate-700 text-white max-w-md` |
| `WidgetLibrary.js` | `bg-slate-900 border-slate-700 text-white !max-w-2xl ...` |
| `CommandDialog` (`command.js`) | `overflow-hidden p-0` (no colour override — relies on the shared `bg-background`/`text-foreground`/`text-muted-foreground` tokens) |

Four of five consumers hardcode `bg-slate-900`/`text-white` — always dark-styled, unconditionally, regardless of the app's light/dark theme setting. This is internally high-contrast (white text on a dark slate background is always legible) so it is **not a WCAG contrast failure** — it is a **light-theme completeness gap**: a user with light theme selected still sees a dark-styled modal. This is long-standing, consistent, pre-existing behaviour across every hardcoding consumer checked (not introduced this cycle), and is a design/scope question (should modals adopt light theme, or is dark-only intentional for this surface?) rather than a contrast defect this story's AC covers.

`CommandDialog` is the one consumer that does NOT hardcode — it relies on the shared theme-aware tokens, which is why it was the one place ST-06's dark-mode-portal bug was actually observable (confirmed via that story's real CI failure and fix).

## 4. Disposition

- No new WCAG contrast gap found beyond ST-09's `BLG-FE-149` (already filed).
- The modal light-theme-completeness pattern (§3) is filed as `BLG-FE-150` (P3, informational/design-scope question) — not a contrast defect, not fixed in-story, requires a design decision (does this app intend modals to support light theme at all?) before any code change.
