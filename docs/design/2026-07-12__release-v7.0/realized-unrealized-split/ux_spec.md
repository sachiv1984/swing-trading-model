**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-12
**Approved by:** Product Owner — 2026-07-12
**Story:** ST-14 — Realized vs. unrealized gain distinction in monthly P&L (BLG-FEAT-70)
**Cycle:** 2026-07-12__release-v7.0

---

# UX Specification — Monthly P&L Realised/Unrealised Split

## 1. Context

`get_monthly_pnl_report()` (`backend/services/reports_service.py`) currently returns only `realised_pnl_gbp` per calendar month — closed-trade P&L attributed to the month the trade closed. Unrealised P&L (open positions, as of now) has no month attribution — it cannot be split *per row* into the monthly table. The correct design is to reuse the already-approved separation pattern from the Tax Year P&L tab (§Unrealised P&L Card, `reports.md`, live since v2.1) rather than inventing a new one: keep monthly rows realised-only, and add a single current-snapshot unrealised figure alongside, with an explicit combined total.

## 2. Decision

### Monthly Financial Table (unchanged)

No change to per-row columns — each month row remains realised-only (`realised_pnl_gbp`), consistent with what "monthly" actually means for closed trades.

### Unrealised P&L Card (new — Monthly P&L Report section)

Added directly below the Monthly Financial Table, reusing the Tax Year tab's approved card pattern verbatim:

- Card header: **"Indicative Unrealised P&L (current positions)"**
- Shows `estimated_unrealised_pnl` (GBP) — same field/computation already used on the Tax Year tab (sum of `pnl` across open positions)
- Displays the `unrealised_note` disclaimer text verbatim (same API field)
- Colour: profit `text-emerald-400`, loss `text-rose-400` (matches Open Positions Panel convention, `open-positions-panel/ux_spec.md` v6.4)
- Must be visually distinct from the monthly table — same "must not mistake this figure for a period-scoped value" rule as the Tax Year tab

### Combined Total Line (satisfies AC-02 regression check)

Below the Unrealised P&L Card:

> **"Total (Realised + Unrealised): £X,XXX.XX"**

Computed client-side as `sum(monthly rows' realised_pnl_gbp for displayed range) + estimated_unrealised_pnl` — display-only arithmetic on already-fetched values, no new endpoint required, no server-side recalculation of either source figure (consistent with the page's "must not recalculate P&L" rule).

## 3. §13 Compliance

Display-only. No new automation.

## 4. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-12
- **Product Owner:** Approved — 2026-07-12
