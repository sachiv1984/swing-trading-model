**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-04-14
**Cycle:** 2026-04-13__release-v2.7
**Story:** ST-09 — Supplementary Indicator Fields (BLG-BE-10)
**Approved by:** Product Owner

---

# UX Specification — Supplementary Signal Indicator Columns

## Feature Summary

Four new read-only columns added to the Signals page table as supplementary context. These columns display informational data per signal that does not affect signal rank or ordering. They are labelled clearly as supplementary/informational to avoid misinterpretation.

---

## API Dependency

**Endpoint:** `POST /signals/generate` (existing)

Four new fields added to each signal object in the response:

| Field | Description |
|-------|-------------|
| `relative_strength_pct` | Stock momentum minus benchmark momentum over `lookback_days` (%) |
| `week52_high_proximity_pct` | Distance from 52-week high as a percentage |
| `avg_daily_volume_20d` | Average daily volume over 20 days |
| `price_vs_50d_ma` | Current price versus 50-day moving average (%) |

The frontend must not compute these values. All values sourced from backend.

---

## Signals Table — Column Additions

The four new columns are appended after the existing canonical columns (Ticker, Signal type, Signal score/rank, Date generated, Market/Sector).

**New columns:**

| Column Header | Source field | Format | Notes |
|---------------|-------------|--------|-------|
| Rel. Strength (vs. benchmark) | `relative_strength_pct` | signed %, 1dp (e.g. `+3.4%`) | Tooltip: "Informational only — does not affect signal rank" |
| 52W High Proximity | `week52_high_proximity_pct` | %, 1dp (e.g. `94.2%`) | Tooltip: "% of 52-week high the current price represents" |
| Avg Vol (20d) | `avg_daily_volume_20d` | integer, abbreviated (e.g. `1.2M`, `450K`) | — |
| vs. 50d MA | `price_vs_50d_ma` | signed %, 1dp (e.g. `+2.1%`) | Positive = above MA; negative = below |

---

## Visual Treatment

### Column group label

The four supplementary columns are grouped under a secondary header row labelled:

> **"Supplementary Context (informational — does not affect ranking)"**

This header spans the four columns and is rendered in muted typography (smaller font size, secondary colour per design system).

### Null/missing values

If any supplementary field is `null` or absent in the API response, the cell renders as `—` (em-dash, muted).

### Relative Strength column label

The column header reads: **"Rel. Strength vs. Benchmark (informational)"** to match the AC requirement and the backend label.

Colour treatment for `relative_strength_pct`:
- Positive value: profit colour (green tone per `design_system.md`)
- Negative value: loss colour (red tone per `design_system.md`)
- Zero: neutral (no colour treatment)

Colour treatment for `price_vs_50d_ma`:
- Same as above: positive = green, negative = red.

---

## Rank Column Isolation

The `rank` column (signal ordering) must remain unchanged and visually separated from the supplementary columns. The supplementary column group must not be adjacent to the rank column in a way that implies influence.

The existing column order is preserved: rank always appears immediately after the signal score column.

---

## Responsive Behaviour

On narrow viewports, the supplementary columns are scrollable horizontally within the table. The ticker, signal type, and rank columns are sticky (do not scroll off screen).

---

## States

No new page-level states introduced. The supplementary columns render in all existing loaded states. If the API returns a signal without supplementary fields, all four cells show `—`.

---

## Constraints

- Supplementary fields are display-only. No filtering, sorting, or interaction on these columns.
- These columns must not be used as sort keys.
- The "informational" label is mandatory — it must appear in the column group header and in the tooltip on the Rel. Strength column.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-14 | Initial UX spec. ST-09 / BLG-BE-10. Design gate: 2026-04-13__release-v2.7. |
