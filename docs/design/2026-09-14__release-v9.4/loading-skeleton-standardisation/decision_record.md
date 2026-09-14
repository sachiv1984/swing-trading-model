**Owner:** Head of UX & Design
**Cycle:** 2026-09-14__release-v9.4
**Story:** ST-25 (BLG-FE-174, EPIC-06)
**Status:** Approved

# Decision Record — Canonical Loading-Skeleton Pattern: Dashboard / Screener / Journal

## Context

Three shared loading-skeleton patterns already exist as documented templates in `base44_prompt_template_library.md` (§7 Label+Value Skeleton Pair, §8 Table/List Row Skeleton, §9 Inline Partial-Value Skeleton), all backed by the shared `Skeleton` primitive (`src/components/ui/Skeleton.js`, `design_system.md` v1.7). Current usage across the 3 named screens diverges in **backing mechanism**, not visual intent:

- **Dashboard** (`DashboardHome.js`): card-level skeletons already composed from the shared `Skeleton` primitive per `design_system.md` v1.7/§7 — conforms today.
- **Screener** (`Screener.js`): `SkeletonRow`/`SkeletonRows`, a page-local custom component pre-dating the shared primitive — the actual source pattern §8's template was extracted *from* (per `base44_prompt_template_library.md`'s own provenance note, v1.4), but never migrated onto the shared `Skeleton` primitive itself.
- **Journal** (`RedFlagJournal.js`): "Skeleton rows (matching event row height)" per `red_flag_journal.md` §Loading — implementation mechanism not confirmed against either the shared primitive or Screener's custom component.

## Decision

1. **Canonical pattern:** the shared `Skeleton` primitive (`src/components/ui/Skeleton.js`) is the single backing component for all loading-placeholder UI app-wide — already established by `design_system.md` v1.7, reaffirmed here as binding for these 3 screens specifically since the AC calls them out as divergent.
2. **Per-screen disposition:**
   - **Dashboard:** already compliant. No change.
   - **Screener:** `SkeletonRow`/`SkeletonRows` must be re-implemented on top of the shared `Skeleton` primitive per the Table/List Row Skeleton template (`base44_prompt_template_library.md` §8) — same visual output (8 rows, per-cell shimmer bars of varied width per `screener_results.md` §10), different backing component. This closes the exact gap `base44_prompt_template_library.md`'s own provenance note (v1.4) flagged as unreconciled.
   - **Journal:** confirmed to follow the same Table/List Row Skeleton template (§8) — row-height-matched shimmer placeholders, shared `Skeleton` primitive.
3. This is a backing-component consolidation, not a visual redesign — no row count, dimension, or animation-timing change to any of the 3 screens' loading states. No new Playwright coverage is required beyond confirming existing loading-state assertions still pass against the re-implemented markup (structural refactor, not a new observable behaviour) — recorded per the CLAUDE.md frontend-visible-change standard as a code-review-eligible change (no visual/behavioural delta claimed) with existing Playwright loading-state assertions re-run as the regression check, per the AC's own "Playwright visual check or recorded staging sign-off confirms no regression" wording.

## Frontend spec updates

- `screener_results.md` §10 — cites the canonical Table/List Row Skeleton template and the shared `Skeleton` primitive as the required implementation, superseding the implicit assumption that `SkeletonRow` is a standalone pattern.
- `red_flag_journal.md` §Loading — same citation added.
- `dashboard.md` — no content change (already conformant); confirmed in this decision record rather than in the spec itself, since there is nothing to correct.

## Rationale

Three screens visually presenting the "same" skeleton pattern but built on two different backing components is the exact drift `base44_prompt_template_library.md`'s loading-skeleton section already exists to prevent going forward — this decision closes the one gap (Screener/Journal not yet migrated onto the shared primitive) that predates the template's authoring.

## Sign-off

Head of UX & Design: Approved, 2026-09-14.
Product Owner: Approved, 2026-09-14.
