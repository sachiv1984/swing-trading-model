**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-08-05
**Cycle:** 2026-08-05__release-v8.3
**Story:** ST-13 (BLG-FE-126, EPIC-03)

# UX Decision Record — Unified Loading-Skeleton Pattern for Async-Loading Cards

## 1. Problem

`DataState`'s `loading` branch (`src/components/ui/DataState.js`) currently renders a centered spinner only, documented in its own source comment as "no skeleton." No content-shaped skeleton pattern exists anywhere in the codebase or `design_system.md`. This is genuinely new visual/motion design, not a restatement of an existing pattern — and per `design_gate_prompt.md` §6, a new pulse-animation timing parameter is Design Required on that basis alone, independent of any layout change.

## 2. Component

`src/components/ui/Skeleton.js` (new shared primitive) — a single `<div>` block: rounded rectangle, pulsing background, no icon/text.

```
<Skeleton className="h-4 w-3/5" />   // one bar
```

## 3. Card-loading composition

For a card-shaped async region, compose 3 stacked bars in place of the card's real content (card's own outer shell/border stays static — only the inner content area is replaced):

| Bar | Width | Height | Represents |
|-----|-------|--------|------------|
| 1 | `w-3/5` | `h-4` | Title/heading line |
| 2 | `w-full` | `h-3` | Body line 1 |
| 3 | `w-4/5` | `h-3` | Body line 2 |

`gap-2` between bars. This is a default composition, not a mandate — a consumer with a differently-shaped card (e.g. a stat tile) may compose its own bar arrangement from the same `Skeleton` primitive; the primitive is what's canonical, not the 3-bar layout.

## 4. Colour (explicit light+dark pair — no dark-only token)

`bg-slate-700/50 dark:bg-slate-700/50` is insufficient (identical class defeats the theme pairing requirement). Canonical pair:

- Dark: `bg-slate-700/60`
- Light: `bg-slate-300/60`

Both sit on the existing secondary-card shell (`bg-slate-800/50` dark, page background light) at a visible-but-clearly-inert contrast — enough to read as "content is loading here" without competing with real content once loaded.

## 5. Motion (timing-sensitive — Design Required trigger per §6)

- Animation: `animate-pulse` (Tailwind default: opacity 1 → 0.5 → 1, `2s` cubic-bezier(0.4, 0, 0.6, 1) ease, infinite loop).
- No custom duration override — the Tailwind default is adopted as-is rather than inventing a bespoke timing value, since no user complaint or performance reason motivates a deviation.
- `prefers-reduced-motion`: `animate-pulse` already respects Tailwind's reduced-motion handling at the utility level; no additional override needed.

## 6. Integration point

New optional `DataState` prop: `loadingVariant` — `"spinner"` (default, unchanged) | `"skeleton"`. When `"skeleton"`, the `loading` branch renders `loadingSkeleton` (a caller-supplied node, e.g. the 3-bar composition above) instead of the spinner. Existing call sites are unaffected (default unchanged), matching the established non-breaking-optional-prop precedent (`errorHeading`/`errorBody`, v1.5).

## 7. Scope boundary

Per the story's acceptance criteria, this record establishes the pattern and primitive only. **No existing card is retrofitted this cycle** — adoption is per-consumer, future work.

## §13 check

Purely presentational; no automated decision or AI call. Not applicable.

## Sign-off

- Head of UX & Design: approved 2026-08-05
- Product Owner: approved 2026-08-05
