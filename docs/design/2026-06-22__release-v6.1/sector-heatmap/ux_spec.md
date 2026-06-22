**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-06-22
**Approved by:** Product Owner — 2026-06-22
**Story:** ST-06 (BLG-FE-76) — Portfolio sector heat-map visualization
**Cycle:** 2026-06-22__release-v6.1

---

# UX Specification — Portfolio Sector Heat Map

## 1. Placement

**Page:** Risk Dashboard (`/risk`)
**Position:** New full-width panel (`§8a Sector Concentration`) inserted between the Position-Level Risk Table (§6) and the Prospective Heat Indicator (§7).

**Rationale:** The Risk Dashboard is the canonical home for portfolio risk data. Sector concentration risk (the risk of over-exposure to one industry) is a direct complement to the existing heat gauge, drawdown, and position-level risk panels. Dashboard (`/`) is already dense; this is a risk-focused visualisation and belongs on the risk page.

---

## 2. Component Identity

**Component name:** `SectorHeatMap.js`
**Section heading:** "Sector Concentration" (card heading, same visual weight as other Risk Dashboard card headings)

---

## 3. Data Source

**Endpoint:** `GET /portfolio/sector-weights` (new endpoint, delivered in ST-06 AC-04)

**Expected response structure:**
```json
{
  "sectors": [
    { "sector_name": "Technology", "position_count": 3, "exposure_pct": 42.5 },
    { "sector_name": "Financials", "position_count": 2, "exposure_pct": 31.0 }
  ],
  "total_positions": 5,
  "concentration_alert": true
}
```

Data is derived from existing positions data and the `sector_name` field on the ticker record. No new data provider required.

---

## 4. Layout

### Desktop (> 768px)

Grid of sector tiles, 4 columns where possible (3 minimum). Tiles equal height. Ordered by `exposure_pct` descending (highest concentration first).

```
[ Technology 42.5%  ] [ Financials 31.0%  ] [ Healthcare 18.2% ] [ Industrials 8.3% ]
[ 3 positions       ] [ 2 positions        ] [ 1 position        ] [ 1 position       ]
   ⚠ Alert                                                                            
```

### Mobile (≤ 768px)

Tiles stack in 2-column grid, same ordering.

---

## 5. Tile Specification

Each tile displays:

| Element | Content | Format |
|---------|---------|--------|
| Sector name | `sector_name` | Title case; truncated with ellipsis if > 20 chars |
| Exposure % | `exposure_pct` | `XX.X%` — primary metric, large text |
| Position count | `position_count` | `N position` / `N positions` — secondary text, muted |

### Tile Colour Coding

| Condition | Tile treatment | Rationale |
|-----------|----------------|-----------|
| `exposure_pct` < 20% | Standard card styling | Low concentration |
| 20% ≤ `exposure_pct` < 40% | Amber left-border accent | Moderate concentration |
| `exposure_pct` ≥ 40% | Amber/orange background tint (`bg-amber-50` dark: `bg-amber-900/20`) + amber border | Concentration alert threshold |

**Concentration threshold: 40% in a single sector.** This matches AC-03. Not configurable in v6.1 MVP.

---

## 6. Section-Level Alert

When `concentration_alert: true` (any sector ≥ 40%):
- Alert bar at the top of the section (below "Sector Concentration" heading, above tiles):
  - Icon: ⚠ amber warning icon
  - Text: "Sector concentration alert: one or more sectors exceed 40% of portfolio"
  - Style: amber background strip, muted but visible

When no alert: no bar shown.

---

## 7. States

| State | Behaviour |
|-------|-----------|
| Loaded | Tile grid renders; alert bar shown if applicable |
| Empty (no open positions) | "No sector data — open at least one position to see sector concentration." Muted text. No tile grid. |
| Loading | Skeleton tile grid (4 placeholder tiles, animated) |
| Error | "Unable to load sector data." + Retry button. Does not affect other Risk Dashboard panels. |

---

## 8. Interactions

- Tiles are **display-only** in v6.1 MVP. No click interaction, no drill-down.
- Concentration alert bar is non-interactive (no dismiss, no link).
- Section is not collapsible (consistent with other Risk Dashboard components).

---

## 9. Constraints

- All exposure values sourced from backend. No client-side recalculation.
- Tile colour thresholds are defined here and must not be changed without a spec version increment.
- `§13 compliance`: display-only, informational. No automated trading recommendation or signal.
- Empty state handles both zero-positions case and no-sector-data case identically.

---

## 10. API Contract Note

`GET /portfolio/sector-weights` is a new endpoint required by ST-06. The endpoint contract must be documented in `docs/specs/api_contracts/` and added to `docs/reference/openapi.yaml` in the same commit as implementation, per CLAUDE.md non-negotiables.
