**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-08-14__release-v8.8
**Story:** ST-15 (EPIC-03, BLG-FE-163) — also names the first live call site for ST-17 (EPIC-03, BLG-FE-160)

# Decision Record — Ticker Universe Filtering (Search, Sector, Industry)

## 1. Problem

The Ticker Universe page (`ticker_universe.md`) already filters by Market (US/UK) and Active/Inactive via a pill-button filter bar (`data-testid="filter-bar"`, `TickerUniverse.js`). There is no way to narrow the table by typed search text, sector, or industry, even though both fields are already captured on every ticker (`sector`, `industry` — see the Add Ticker form).

## 2. Decision

Extend the existing filter bar rather than introduce a second filter region — all filters read as one control cluster:

| Control | Type | Behaviour |
|---------|------|-----------|
| Search | Text input, placeholder "Search ticker or company…" | Case-insensitive substring match against `ticker` and `company_name`. Debounced 200ms (below the `design_gate_prompt.md` §6 motion/timing threshold for a *new* interaction-flow decision — matches the existing project-wide search-input debounce convention, not a new timing parameter). |
| Sector | `<select>`, "All Sectors" default | Options derived dynamically from the distinct `sector` values present in the currently loaded ticker list — no new endpoint. |
| Industry | `<select>`, "All Industries" default | Same derivation pattern as Sector, from `industry`. |

**Combination rule:** all active filters (existing Market/Active pills plus the 3 new controls) AND-combine, matching the existing `filtered = tickers.filter(...)` chain's behaviour — this is an extension of the existing filter-reduction, not a new filtering model.

**Layout:** Search input first (widest, left-aligned), then Sector and Industry selects, placed in the same `flex flex-wrap gap-2` row as the existing Market/Active pill buttons — one continuous filter bar, not a separate section, per the page's existing single-row filter convention.

**Reset:** when any of the 5 filters is non-default, show a "Clear filters" control. Implemented as `<Badge variant="secondary">Clear filters ×</Badge>` (clickable) — this gives the shadcn `Badge` `secondary` variant its first live call site in the app (previously unused anywhere; see `BLG-FE-160`/ST-17), satisfying that story's "first live call site introduced" condition in the same sprint. Clicking resets all 5 filters to default and hides itself.

**Row count feedback:** the existing "Showing {filtered.length} of {tickers.length} tickers" footer line (already present) requires no change — it already reflects any active filter combination, new or old.

### Card component call site

Not used here — the filter bar remains a plain `<div>` row (existing convention, no card-shell wrapper on filter controls elsewhere in the app). The shadcn `Card` component's own first-live-call-site gap (`BLG-FE-160`) is **not** resolved by this story; it remains open and unaffected by this decision.

## 3. Constraints Checked

- Does not contradict `strategy_rules.md` §13 — client-side filtering only, no automated recommendation.
- Motion/timing clause (`design_gate_prompt.md` §6): the 200ms search debounce is an explicit timing parameter on a new interaction flow — classified Design Required accordingly (this decision record is that required design artefact) rather than waved through as a pure-code addition.
