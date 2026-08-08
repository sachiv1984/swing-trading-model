**Owner:** Head of Engineering
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-07
**Cycle:** 2026-08-07__release-v8.4 (ST-15 — BLG-FE-142)

---

# Dialog/DialogTitle className-Override Audit — cn()-Has-No-Tailwind-Merge Defect Class

## Purpose

ST-15 (BLG-FE-142): audit every consumer of the shared `Dialog*` primitives (`src/components/ui/dialog.js`) for the defect class first documented in `ComplianceRecheckModal.js` (ST-11, BLG-FE-103, EPIC-03, v8.3) — this project's `cn()` (`src/lib/utils.js`) is plain `clsx` with no `tailwind-merge`, so when a consumer's `className` prop targets the same CSS property as one of `dialog.js`'s own hardcoded base classes, the winner is decided by Tailwind's compiled stylesheet order, not by prop precedence. A later-declared override does **not** reliably beat an earlier base class.

## Method

Every file passing a `className` prop to `DialogContent`, `DialogTitle`, `DialogHeader`, `DialogFooter`, `DialogDescription`, or `DialogOverlay` was enumerated (`grep -rn "Dialog(Content|Title|Header|Footer|Description|Overlay)" src/`) — 13 consumer files, 16 override sites. For each site, the override's classes were compared property-by-property against the corresponding base component's hardcoded classes in `dialog.js`.

Rather than reason about Tailwind's cascade order from documentation (unreliable — depends on this project's actual `tailwind.config.js` theme, which extends but does not fully re-declare the default palette), the project's real `tailwindcss` CLI (`node_modules/.bin/tailwindcss`, v3.4.19) was used to compile a probe stylesheet containing every colliding class pair, using the project's actual `tailwind.config.js` and `src/index.css`. The compiled output was inspected directly to determine, for each pair, which declaration is later in the cascade (and therefore wins, since both sides share equal selector specificity absent an `!` modifier).

## Findings

**16 override sites audited across 13 consumer files. 8 genuine same-property collisions found, across 6 files, all fixed. All other overrides (`bg-slate-900` vs. base `bg-background`, `max-w-md` vs. base `max-w-lg`, `text-xl` vs. base `text-lg`, and all colour-only / new-property overrides) were verified to already win under the compiled build and required no change.**

| # | File | Line(s) | Collision (override vs. base) | Verified outcome pre-fix | Fix |
|---|------|---------|-------------------------------|---------------------------|-----|
| 1 | `src/components/dashboard/WidgetLibrary.js` | `DialogContent` (was 67) | `max-w-2xl` vs. base `max-w-lg` | base wins — modal stuck at `max-w-lg` | `!max-w-2xl` |
| 2 | `src/components/dashboard/WidgetLibrary.js` | `DialogContent` (was 67) | `flex flex-col` vs. base `grid` | base wins — layout is actually `display: grid`, not flex; body's `flex-1 overflow-y-auto` has no flex parent to size against | `!flex !flex-col` |
| 3 | `src/components/dashboard/WidgetLibrary.js` | `DialogTitle` (was 69) | `font-bold` vs. base `font-semibold` | base wins — title renders semibold, not bold | `!font-bold` |
| 4 | `src/components/monitor/MonitorModal.js` | `DialogContent` (was 47) | `max-w-2xl` vs. base `max-w-lg` | base wins | `!max-w-2xl` |
| 5 | `src/components/monitor/MonitorModal.js` | `DialogContent` (was 47) | `flex flex-col` vs. base `grid` | base wins — same `flex-1 overflow-y-auto` body-sizing defect as #2 | `!flex !flex-col` |
| 6 | `src/components/trades/TradeReflectionModal.js` | `DialogContent` (was 112) | `max-w-2xl` vs. base `max-w-lg` | base wins | `!max-w-2xl` |
| 7 | `src/components/trades/TradeReflectionModal.js` | `DialogContent` (was 112) | `flex flex-col` vs. base `grid` | base wins (masked here by an inline `maxHeight` + `overflow-y-auto` workaround on the body, so no visible break, but still incorrect display) | `!flex !flex-col` |
| 8 | `src/components/reports/ExportModal.js` | `DialogTitle` (was 209) | `font-bold` vs. base `font-semibold` | base wins — title renders semibold, not bold | `!font-bold` |
| 9 | `src/pages/TradePlan.js` | `DialogContent` (was 1065) | `rounded-2xl` (unprefixed) vs. base's responsive `sm:rounded-lg` | base wins at `>=640px` (Tailwind emits responsive variants after their unprefixed base classes regardless of source order) — corners revert to the smaller `--radius`-derived value on desktop | `!rounded-2xl` |
| 10 | `src/components/watchlist/WatchlistModal.js` | `DialogFooter` (was 205) | `justify-between` (unprefixed) vs. base's responsive `sm:justify-end` | base wins at `>=640px` — footer buttons collapse to the right instead of spreading, on desktop only | `!justify-between` |

(Findings 1–2, 4–5, 6–7, and 9, 10 above are grouped by site — 8 distinct property collisions across 6 files, matching the "8 genuine collisions" summary.)

### Not collisions (verified, no change)

- `bg-slate-900` (used in all 11 dark-styled consumers) vs. base `bg-background` — override wins; the extended `background` colour is emitted before `slate-900` in the compiled stylesheet.
- `max-w-md` (used in 7 consumers) vs. base `max-w-lg` — override wins; `max-w-md` is emitted after `max-w-lg`.
- `max-w-lg` (`PositionModal.js`) vs. base `max-w-lg` — identical value, no functional collision.
- `text-xl` (`DialogTitle` in `WidgetLibrary.js`, `ExportModal.js`, `PositionEntryModal.js`) vs. base `text-lg` — override wins.
- `text-slate-600 dark:text-slate-400`, `text-cyan-400`, `text-rose-400`, `text-white` colour overrides on `DialogTitle`/`DialogDescription` — base sets no colour on `DialogTitle`, and base's `text-muted-foreground` on `DialogDescription` generates no CSS at all in this build (`muted-foreground` is referenced only as a raw CSS custom property in `src/index.css`, not registered in `tailwind.config.js`'s `theme.extend.colors` — see Known Gap below), so there is no competing rule either way.
- `border-slate-*` colour overrides vs. base's bare `border` — different CSS property (`border` alone only sets `border-width`, not colour).
- `flex items-center gap-*` on several `DialogTitle` instances (`MonitorModal.js`, `ExitModal.js`, `PositionModal.js`, `PositionEntryModal.js`, `TradeReflectionModal.js`, `WatchlistModal.js`) — base sets no `display` on `DialogTitle`; these are new declarations, not overrides.
- `grid grid-rows-[auto_1fr_auto]` (`ExitModal.js`, `PositionModal.js`) — consistent with base's `grid`; `grid-rows` is a new declaration.
- `p-6 space-y-4 mx-4` (`TradePlan.js`) — `p-6` matches the base value exactly (no functional collision); the others are new declarations.

## Known Gap (out of scope for this story, filed separately)

`text-muted-foreground` — used as `DialogDescription`'s own base colour class in `dialog.js` — generates **no CSS** under the project's actual `tailwind.config.js`: only `background` and `foreground` are registered in `theme.extend.colors` (see the `// (all your Base44 extended colors here)` placeholder comment), while `--muted`/`--muted-foreground` exist only as raw CSS custom properties in `src/index.css`. This is a pre-existing, unrelated defect (a missing theme registration, not a `cn()`-merge collision) that very likely affects other `text-muted-foreground`/`bg-muted`/`border-muted` usages across the app beyond `Dialog*`. Filed as `BLG-FE-145` — out of this story's scope (ST-15 is specifically the `cn()`-merge override-collision defect class on `Dialog*` consumers).

## Disposition

8 genuine collisions found and fixed across 6 files, using the same `!`-prefixed important-modifier pattern already established in `ComplianceRecheckModal.js` (ST-11, v8.3) — confirmed via the real `tailwindcss` build to emit `!important` and therefore win deterministically regardless of future stylesheet-order changes. No `tailwind-merge` dependency was added (broader fix option considered and rejected: touches every `cn()` call site across the app, materially larger blast radius than this story's scope). No visual regression: every fix either (a) had zero visible effect pre/post because the override was already winning in practice for that specific instance, or (b) corrects a base-class value silently leaking through where the developer's override was ignored — the corrected state is the originally-intended rendering, not a new one. Playwright coverage/staging sign-off recorded per CLAUDE.md's frontend-visible-change rule — see `qa_evidence_EPIC-04.md`.

## Sign-off

**Head of Engineering:** Confirmed — 2026-08-07
