**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-19
**Approved by:** Product Owner — 2026-06-19
**Cycle:** 2026-06-19__release-v6.0
**Story:** ST-03 (EPIC-02)

---

# UX Spec — Net-of-Costs Performance Tracking (ST-03)

## Purpose

Allow users to record brokerage costs (commission and spread) against individual closed trades, and surface a net-of-costs R-multiple alongside the existing gross R-multiple wherever trades are displayed. Performance report breakdowns gain a gross vs net comparison row where cost data is available.

## Design Principle

Cost data is optional. The system must never degrade the existing experience for trades without cost data. When cost data is absent, gross R remains the sole displayed metric and no net R column or label appears.

---

## Surface 1 — Cost Field Capture (Trade History Detail / Edit Form)

### New Fields

Two new optional numeric input fields on the trade record edit form:

| Field | Label | Type | Required | Format |
|-------|-------|------|----------|--------|
| `commission_gbp` | **Commission (£)** | Decimal numeric | No | Currency, 2dp (e.g. 6.00) |
| `spread_cost_gbp` | **Spread Cost (£)** | Decimal numeric | No | Currency, 2dp (e.g. 2.40) |

### Placement

Both fields appear in a new **"Brokerage Costs"** subsection within the trade detail edit form, below the existing P&L fields.

### States

| State | Behaviour |
|-------|-----------|
| Both fields empty | No net R calculated or displayed on save; gross R unchanged |
| One or both fields populated | Net R calculated on save; displayed alongside gross R in trade history |
| Non-numeric input | Inline validation: "Enter a number (e.g. 6.00)" |
| Zero entered | Valid — zero cost is not an error |

---

## Surface 2 — Net R Display (Trade History Table and Detail)

### Condition

Net R is displayed **only when** at least one of `commission_gbp` or `spread_cost_gbp` is non-null and non-zero on the trade record.

### Table Column

In the trade history table, the existing gross R column:
- Retains its current label and value when no cost data exists
- When cost data exists: gross R is shown in normal weight; net R is shown directly below it in smaller, muted text: "Net: –0.85R" where the value incorporates cost drag

### Detail Expand View

In the expanded trade row, two rows appear in the R-multiple section:

| Label | Value |
|-------|-------|
| Gross R | +1.2R (existing display; unchanged) |
| Net R (after costs) | +0.9R _(shown only if cost data present)_ |

### Net R Colour

- Net R positive: green (same tone as gross R positive)
- Net R negative: red (same tone as gross R negative)
- Net R = 0: neutral grey

---

## Surface 3 — Gross vs Net Comparison (Reports Page)

### Condition

The gross vs net comparison appears **only when** the currently selected tax year's trade set contains at least one trade with cost data.

### Placement

New row in the existing summary stats table on the Reports page, below the Win Rate row:

| Metric | Gross | Net (after costs) |
|--------|-------|-------------------|
| Average R-multiple | +0.72R | +0.54R |

- "Net (after costs)" column shows `—` for individual trades without cost data; average is computed only across trades that have cost data
- Footnote below the row: _(Net figures based on N trades with brokerage cost data recorded.)_

### Year-Level Toggle

No toggle required. The gross vs net row is visible as-is. Users can add cost data incrementally — the average updates on each save.

---

## Playwright Test Scenarios

- **SC-NOC-01a**: Commission and spread cost fields appear in trade edit form
- **SC-NOC-01b**: Saving with no cost data: no Net R column or label visible in trade history
- **SC-NOC-01c**: Saving with commission_gbp = 6.00, spread_cost_gbp = 2.40: Net R appears below Gross R in table and detail view
- **SC-NOC-01d**: Trade with cost data: Net R colour is green when positive, red when negative
- **SC-NOC-01e**: Reports page: gross vs net row absent when selected year has no trades with cost data
- **SC-NOC-01f**: Reports page: gross vs net row present with footnote when ≥1 trade in year has cost data
