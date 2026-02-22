# Decisions Record — Quick Wins Bundle

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-02-24
**Roadmap item:** Quick Wins Bundle — BLG-FEAT-01, 02, 04, 05, 06, 07
**Target release:** v1.6.1
**Pre-alignment meeting:** QWB-PA-001, 2026-02-24
**Phase Gate Document:** `docs/product/phase_gates/QWB-quick-wins-bundle-phase-gate.md`

> ⚠️ Standing Notice: This document records decisions made at the pre-alignment
> meeting. All authoritative rules, formulas, field definitions, and constraints
> live in the canonical specifications listed against each decision. This document
> must not be cited as canonical intent — it records the decision rationale only.

---

## Decision Log

---

### D1 — BLG-FEAT-01: Current drawdown formula and data source

**Status:** ✅ Closed — 2026-02-24
**Closed by:** Metrics Definitions owner + API Contracts owner
**Canonical authority after update:** `docs/specs/metrics_definitions.md` v1.5.8, `docs/specs/api_contracts/portfolio_endpoints.md`

**Decision:**
Current drawdown is calculated server-side as:
`current_drawdown_percent = (peak_portfolio_value - current_portfolio_value) / peak_portfolio_value × 100`

where `peak_portfolio_value` = `MAX(portfolio_history.total_value)` (all-time high of recorded snapshots).

Result is zero or negative. Zero means portfolio is at peak.

Served via `GET /portfolio` response — two new fields added:
- `current_drawdown_percent` (float, GBP percentage, ≤ 0.0)
- `peak_portfolio_value` (float, GBP)

Both fields are always present. Default to `0.0` when no `portfolio_history` exists.

Days underwater is **not** calculated by the widget. It reads `advanced_metrics.days_underwater` from `GET /analytics/metrics` (trade-sequence method — canonical per `metrics_definitions.md`).

**Rationale:** Centralises drawdown calculation server-side. Consistent with existing `max_drawdown` pattern. Uses already-required API calls.

---

### D2 — BLG-FEAT-02: R-multiple formula and calculation location

**Status:** ✅ Closed — 2026-02-24
**Closed by:** Metrics Definitions owner
**Canonical authority:** `docs/specs/metrics_definitions.md` v1.5.7 (no update required)

**Decision:**
R-multiple formula is already canonical:
`R = (exit_price - entry_price) / (entry_price - stop_price)`

Calculation location: **frontend-only**. This is confirmed canonical — `metrics_definitions.md` classifies R-multiple as "Tier 1 — Visualisation-Only" and states "Client-side only for visualisation."

No `metrics_definitions.md` update required. No API change required.

`stop_price` is absent from `GET /trades` direct response — sourced from `trades_for_charts` array in `GET /analytics/metrics` (added at contract v1.7.0 specifically for this purpose).

**Rationale:** Spec already governs. Confirmation only.

---

### D2a — BLG-FEAT-02: stop_price field availability

**Status:** ✅ Closed — 2026-02-24
**Closed by:** API Contracts owner
**Canonical authority:** `docs/specs/api_contracts/analytics_endpoints.md` v1.8.1

**Decision:**
`stop_price` is **not** present in `GET /trades` direct response. It is present in `trades_for_charts` within `GET /analytics/metrics`. Implementation reads from `trades_for_charts`. No contract change required.

---

### D3 — BLG-FEAT-04: Best/Worst Trades ranking criterion

**Status:** ✅ Closed — 2026-02-24
**Closed by:** Product Owner
**Canonical authority:** This decisions record

**Decision:**
Best/Worst Trades widget ranks by **R-multiple** (not P&L).
Count: top 3 winners, bottom 3 losers.
Data source: `trades_for_charts` from `GET /analytics/metrics` (same dataset as BLG-FEAT-02).
Frontend-only derivation using the BLG-FEAT-02 R-multiple calculation.
No additional API call required.

**Rationale:** R-multiple is risk-adjusted and more strategically meaningful than raw P&L for a momentum trading system. Shows whether trades were good relative to risk taken, not just absolute size.

---

### D4 — BLG-FEAT-06: grace_days_remaining field

**Status:** ✅ Closed — 2026-02-24
**Closed by:** API Contracts owner
**Canonical authority after update:** `docs/specs/api_contracts/position_endpoints.md`

**Decision:**
Add `grace_days_remaining` (integer | null) to `GET /positions` response.

Formula: `max(0, 10 - holding_days)` when `grace_period = true`; `null` when `grace_period = false`.

Field is always present in the response object. No data model change required — derived at query time from existing `holding_days` and `grace_period` fields.

Display format: `"Day {holding_days + 1} of 10"` (e.g. "Day 3 of 10").

**Rationale:** `grace_period: boolean` is insufficient for the UI. The remaining days are derivable server-side at zero cost.

---

### D5 — BLG-FEAT-07: CSV export endpoint

**Status:** ✅ Closed — 2026-02-24
**Closed by:** API Contracts owner
**Canonical authority after update:** `docs/specs/api_contracts/trade_endpoints.md`, `docs/reference/openapi.yaml`

**Decision:**
New endpoint: `GET /trades/export/csv`

Response:
- `Content-Type: text/csv`
- `Content-Disposition: attachment; filename="trade_history.csv"`
- No request body. No query parameters for v1.6.1.
- Scope: full closed trade history.

**Final confirmed field list (CSV columns, in order):**
`ticker`, `market`, `entry_date`, `exit_date`, `shares`, `entry_price`, `exit_price`, `pnl`, `pnl_pct`, `holding_days`, `exit_reason`, `tags` (semicolon-separated), `entry_note`, `exit_note`

Note: `stop_price` removed from earlier draft — not stored in `trade_history` table at exit time.

Contract update: new section in `trade_endpoints.md`. `openapi.yaml` updated in same PR.

**Rationale:** All fields are in `trade_history`. No joins required. Serves tax reporting and external analysis use cases.

---

### D6 — BLG-TECH-06: sharpe_ratio_trade_method canonicalisation

**Status:** ✅ Closed — 2026-02-24
**Closed by:** Product Owner

**Decision:**
**Out of QWB scope.** BLG-TECH-06 is a spec documentation fix, not a user-facing feature. Delivered separately by API Contracts owner under existing backlog item. Target: v1.6.1. No scope change to QWB.

---

### D7 — BLG-FEAT-01: days_underwater source

**Status:** ✅ Closed — 2026-02-24
**Closed by:** Metrics Definitions owner + Engineering
**Canonical authority:** `docs/specs/metrics_definitions.md` v1.5.7

**Decision:**
`days_underwater` is sourced from `GET /analytics/metrics` → `advanced_metrics.days_underwater` (trade-sequence method).

The prototype's client-side wall-clock calculation from `peakDate` (`Math.floor(diffMs / 86400000)`) is **discarded**. It diverges from canonical behaviour when trades are sparse.

The widget makes two API calls on load:
1. `GET /portfolio` → `current_drawdown_percent`, `peak_portfolio_value`
2. `GET /analytics/metrics` → `advanced_metrics.days_underwater`, `advanced_metrics.max_drawdown.percent`

Both calls are already made by the Dashboard page.

**Rationale:** Canonical spec must govern. Trade-sequence method is more accurate for a trading system than wall-clock elapsed time.

---

### D8 — BLG-FEAT-01: maxHistoricalDrawdown progress bar

**Status:** ✅ Closed — 2026-02-24
**Closed by:** Product Owner

**Decision:**
**In scope.** Progress bar showing current drawdown relative to historical maximum drawdown is included in BLG-FEAT-01.

Data source: `max_drawdown.percent` from `GET /analytics/metrics` (existing field, no new API change).
Combined with D7 resolution: both fields arrive from the same `GET /analytics/metrics` call already required.

**Rationale:** Adds meaningful risk context at zero additional API cost. The relative position of current vs. worst-ever drawdown is a natural companion metric.

---

### D9 — BLG-FEAT-01: Severity colour thresholds

**Status:** ✅ Closed — 2026-02-24
**Closed by:** Metrics Definitions owner + Product Owner

**Decision:**
Colour thresholds are **implementation detail**. Not added to `metrics_definitions.md`.

Thresholds (green ≤5%, amber ≤10%, orange ≤20%, red >20%) are a UX convention. Engineering owns the values. Frontend spec documents the convention for visual consistency. No canonical spec change required.

If thresholds require future change: frontend spec update only.

**Rationale:** Colour conventions are presentation layer, not business logic. Adding them to `metrics_definitions.md` would conflate analytical definitions with UI behaviour.

---

### D10 — BLG-FEAT-01: dataSource fallback logic

**Status:** ✅ Closed — 2026-02-24
**Closed by:** API Contracts owner + Engineering

**Decision:**
**No fallback required.** `GET /portfolio` always returns `current_drawdown_percent` and `peak_portfolio_value`. When no `portfolio_history` exists, both return `0.0`. The backend guarantees field presence after the contract update.

Prototype `dataSource` prop (`portfolio_history`/`estimated`/`default`) and all associated fallback logic are **removed**. Single data path only.

Widget retains the "Establishing Peak" empty state for when `peak_portfolio_value === 0` (i.e. no history yet) — this is a valid display state, not a fallback path.

**Rationale:** Fallback logic adds complexity that contradicts the spec contract. If the API guarantees the field, the frontend should not second-guess it.

---

### D11 — WidgetLibrary / customisable dashboard

**Status:** ✅ Closed — 2026-02-23 (pre-meeting)
**Closed by:** Product Owner

**Decision:**
**Out of scope.** Customisable dashboard architecture (widget catalogue, add/remove, persistence, sizing) is not part of QWB. The roadmap deferral of "Customisable Dashboard Layout" stands.

Each QWB item ships as a direct, fixed addition to its target page:
- BLG-FEAT-01: Dashboard stats row
- BLG-FEAT-02: Trade History table (new column)
- BLG-FEAT-04: Performance Analytics page (new panel)
- BLG-FEAT-05: Performance Analytics page (new chart)
- BLG-FEAT-06: Open Positions table (new column)
- BLG-FEAT-07: Trade History page (new export button)

`WidgetLibrary.jsx` prototype is discarded.

---

### D12 — BLG-FEAT-01: "New Peak!" at-peak display state

**Status:** ✅ Closed — 2026-02-24
**Closed by:** Product Owner

**Decision:**
**In scope.** At-peak display state included. Positive reinforcement when portfolio is at all-time high is appropriate UX.

Display text and emoji styling are implementation detail for Frontend Spec owner to govern for visual consistency with the rest of the product.

---

## Summary Table

| # | Decision | Item | Outcome |
|---|----------|------|---------|
| D1 | Current drawdown formula + endpoint | BLG-FEAT-01 | `(peak-current)/peak×100` via GET /portfolio (2 new fields) |
| D2 | R-multiple formula + location | BLG-FEAT-02 | Canonical, frontend-only, no spec change |
| D2a | stop_price in GET /trades | BLG-FEAT-02 | Absent — use trades_for_charts |
| D3 | Best/Worst ranking | BLG-FEAT-04 | R-multiple, top 3 / bottom 3 |
| D4 | grace_days_remaining field | BLG-FEAT-06 | New field on GET /positions, derived server-side |
| D5 | CSV export endpoint | BLG-FEAT-07 | GET /trades/export/csv, 14 fields, full history |
| D6 | BLG-TECH-06 scope | — | Out of QWB, separate delivery |
| D7 | days_underwater source | BLG-FEAT-01 | GET /analytics/metrics (trade-sequence), prototype discarded |
| D8 | Progress bar scope | BLG-FEAT-01 | In scope, max_drawdown from GET /analytics/metrics |
| D9 | Colour thresholds | BLG-FEAT-01 | Implementation detail, Engineering owns |
| D10 | dataSource fallback | BLG-FEAT-01 | No fallback, GET /portfolio always returns fields |
| D11 | WidgetLibrary / dashboard | QWB | Out of scope, roadmap deferral stands |
| D12 | New Peak! state | BLG-FEAT-01 | In scope, styling is impl detail |

---

## Spec Update Actions Triggered by These Decisions

| Spec file | Change required | Owner | Decision source |
|-----------|----------------|-------|-----------------|
| `docs/specs/metrics_definitions.md` | Add Current Drawdown section (v1.5.7 → v1.5.8) | Metrics Definitions owner | D1 |
| `docs/specs/api_contracts/portfolio_endpoints.md` | Add `current_drawdown_percent` + `peak_portfolio_value` to GET /portfolio | API Contracts owner | D1 |
| `docs/specs/api_contracts/position_endpoints.md` | Add `grace_days_remaining` to GET /positions | API Contracts owner | D4 |
| `docs/specs/api_contracts/trade_endpoints.md` | Add GET /trades/export/csv section | API Contracts owner | D5 |
| `docs/reference/openapi.yaml` | Update for D5 endpoint (same PR as trade_endpoints.md) | API Contracts owner | D5 |
| Frontend spec — trade history component | Document R-multiple column, colour thresholds | Frontend Spec owner | D2, D9 |
| Frontend spec — dashboard stats | Document drawdown widget placement, data sources, states | Frontend Spec owner | D1, D7, D8, D10, D12 |
| Frontend spec — positions table | Document grace_days_remaining display column | Frontend Spec owner | D4 |
| Frontend spec — analytics page | Document Best/Worst widget + Win Rate chart | Frontend Spec owner | D3 |
| Frontend spec — trade history page | Document CSV export button | Frontend Spec owner | D5 |
