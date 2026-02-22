# Phase Gate Document — Quick Wins Bundle

**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.1
**Created:** 2026-02-22
**Last Updated:** 2026-02-22
**Filed:** — (immutable on closure)

**Charter authority:** `docs/team_skills/pmo/processess/pre_alignment_run.md` v2.0

---

## Feature Summary

| Field | Value |
|-------|-------|
| Feature | Quick Wins Bundle — BLG-FEAT-01, 02, 04, 05, 06, 07 |
| Roadmap entry | `docs/product/roadmap.md` — v1.6.1 Quick Wins Bundle |
| Target release | v1.6.1 |
| PMO Lead | PMO Lead |
| Date opened | 2026-02-22 |
| Date shipped | — |

---

## Bundle Items

| Item | Description | Effort |
|------|-------------|--------|
| BLG-FEAT-01 | Current Drawdown Widget | ~30 min |
| BLG-FEAT-02 | R-Multiple Column in Trade History | ~1 hour |
| BLG-FEAT-04 | Best / Worst Trades Widget | ~1 hour |
| BLG-FEAT-05 | Win Rate by Month Chart | ~1 hour |
| BLG-FEAT-06 | Grace Period Indicator | ~1 hour |
| BLG-FEAT-07 | CSV Export of Trade History | ~1 hour |

**Total estimated effort (implementation + spec authoring):** ~8–10.5 hours
*(Revised from ~6–8 hours — spec authoring for BLG-FEAT-01, 06, 07 is additional. See Gate R.5.)*

---

## Current Status

```
Current phase:    AWAITING_MEETING
Gate passed:      Gate R — 2026-02-22
Next gate:        Gate 0 — pre-alignment meeting scheduled and held; all decisions closed
Who acts next:    PMO Lead — schedule pre-alignment meeting; issue invitations to all owners
What they do:     Issue meeting invitation with full D1–D6 agenda + D2a open query
Deadline:         2026-02-23T17:00:00Z
Blockers:         None
```

---

## Phase History

| Phase | Gate condition | Status | Date | Notes |
|-------|---------------|--------|------|-------|
| Phase 0 — Readiness Audit | Audit complete, Go/No-Go issued | ✅ Complete | 2026-02-22 | Gate R passed. All items confirmed. State → AWAITING_MEETING. |
| Phase 1 — Pre-Alignment Meeting | All decisions closed, decisions record committed | 🟡 In progress | — | Awaiting meeting scheduling. |
| Phase 2 — Parallel Spec Delivery | All spec actions complete and committed | ⬜ Not started | — | |
| Phase 3 — QA Review Gate | QA sign-off confirmed | ⬜ Not started | — | |
| Phase 4 — Scope Document | Scope document committed, implementation declared open | ⬜ Not started | — | |
| Implementation | Engineering builds against locked specs | ⬜ Not started | — | |
| Phase 5 — Verification | All criteria pass, Director of Quality final sign-off | ⬜ Not started | — | |
| Shipping Closure | Changelog, roadmap, supersession actions complete | ⬜ Not started | — | |

Status key: ⬜ Not started | 🟡 In progress | ✅ Complete | 🔴 Blocked

---

## Gate R — READINESS_AUDIT → AWAITING_MEETING

**Gate R overall status: ✅ ALL GATE R ITEMS PASS — state transition to AWAITING_MEETING valid**

---

### Gate R.1 — Data model readiness confirmed

*All fields the bundle reads or writes exist in `data_model.md`, or are pre-designed with type, constraint, default, and migration documented.*

---

#### R.1 — BLG-FEAT-01: Current drawdown formula confirmed

Decision: BLG-FEAT-01 displays CURRENT drawdown (live), not historical max drawdown.

- **Formula:** `current_drawdown_percent = (peak_portfolio_value - current_portfolio_value) / peak_portfolio_value × 100`
  where `peak_portfolio_value` = `MAX(portfolio_history.total_value)` (all-time high).
- **Data source:** Derivable from existing `portfolio_history` table. No new schema fields required.
- **Endpoint:** Add `current_drawdown_percent` and `peak_portfolio_value` fields to `GET /portfolio` response. No new endpoint needed.
- **Days underwater:** Sourced from existing `advanced_metrics.days_underwater` via `GET /analytics/metrics`.
- **Display format:** `"Current drawdown: -8.2% | 12 days underwater"`
- **Spec updates required:**
  - `docs/specs/metrics_definitions.md` — add Current Drawdown section. Version: 1.5.7 → 1.5.8.
  - `docs/specs/api_contracts/portfolio_endpoints.md` — add `current_drawdown_percent` and `peak_portfolio_value` to `GET /portfolio` response schema.

```
Evidence:         Product Owner written confirmation, 2026-02-22.
                  Formula: (peak_portfolio_value - current_portfolio_value) / peak_portfolio_value × 100
                  Source: MAX(portfolio_history.total_value) for peak; latest record for current.
                  Served via: GET /portfolio (two new response fields — no new endpoint).
                  days_underwater: GET /analytics/metrics advanced_metrics.days_underwater (existing).
                  Display format: "Current drawdown: -8.2% | 12 days underwater"
                  metrics_definitions.md update: add Current Drawdown section → v1.5.8
                  portfolio_endpoints.md update: add current_drawdown_percent + peak_portfolio_value
Owner confirmation: Yes — Product Owner, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
```

---

#### R.1 — BLG-FEAT-02: R-multiple formula confirmed

Decision: R-multiple formula is already canonical. Calculation is frontend-only, consistent with existing spec.

- **Formula:** `R = (exit_price - entry_price) / (entry_price - stop_price)`
- **Canonical source:** `metrics_definitions.md` v1.5.7 — R-Multiple section (Tier 1, Visualisation-Only).
- **Calculation location:** Frontend-only. No server-side change required.
- **Fields required:** `entry_price`, `exit_price`, `stop_price` — available in `trades_for_charts` array from `GET /analytics/metrics`. Availability in `GET /trades` direct response to be confirmed at pre-alignment meeting (D2a — non-blocking).
- **No `metrics_definitions.md` update required.** Formula already canonical.
- **No API contract change required** for core implementation.
- **Spec update required:** Trade History table component spec (frontend spec only).

```
Evidence:         Product Owner written confirmation, 2026-02-22.
                  Formula: R = (exit_price - entry_price) / (entry_price - stop_price)
                  Canonical source: metrics_definitions.md v1.5.7 — R-Multiple (Tier 1, Visualisation-Only)
                  Calculation location: frontend-only (canonical)
                  Fields in trades_for_charts: entry_price ✅ exit_price ✅ stop_price ✅
                  D2a (non-blocking): confirm stop_price in GET /trades direct response at meeting
                  No metrics_definitions.md update required.
                  No API contract update required.
                  Frontend spec update required: trade history table component.
Owner confirmation: Yes — Product Owner, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
                  PMO note: D2a added to meeting agenda — non-blocking for Gate R.
```

---

#### R.1 — BLG-FEAT-04: Best/Worst Trades ranking criterion confirmed

Decision: Ranked by R-multiple (not P&L).

- **Ranking:** R-multiple (frontend-calculated, same formula as BLG-FEAT-02). Rationale: risk-adjusted, more strategically meaningful than raw P&L.
- **Count:** Top 3 winners, bottom 3 losers.
- **Data source:** `trades_for_charts` array from `GET /analytics/metrics` (all required fields present).
- **No API change required.** Frontend-only derivation.

```
Evidence:         Product Owner written confirmation, 2026-02-22.
                  Ranking criterion: R-multiple (frontend-calculated)
                  Count: top 3 / bottom 3
                  Data source: trades_for_charts from GET /analytics/metrics (existing)
                  No API change required.
Owner confirmation: Yes — Product Owner, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
```

---

#### R.1 — BLG-FEAT-05: Win rate by month — data source confirmed

Decision: Use existing `monthly_data` array from `GET /analytics/metrics`.

- **Data source:** `monthly_data[].win_rate` — existing field, no backend change.
- **No API change, no schema change, no `metrics_definitions.md` update required.**
- **Frontend bar chart only.**

```
Evidence:         Product Owner written confirmation, 2026-02-22.
                  Data source: monthly_data[].win_rate from GET /analytics/metrics (existing)
                  No API change, no schema change, no metrics_definitions.md update required.
Owner confirmation: Yes — Product Owner, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
```

---

### Gate R.1a — Settings table dependency

*No bundle item reads from or writes to the settings table.*

```
Evidence:         Audit confirmed. No settings dependency across all six items.
Owner confirmation: Yes — PMO Lead, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
```

---

### Gate R.2 — API contract readiness confirmed

*All required endpoints documented, or API Contracts owner has been briefed with sufficient context.*

---

#### R.2 — BLG-FEAT-06: Grace days field — confirmed absent, endpoint update scoped

Audit finding: `GET /positions` currently returns `grace_period: boolean`, `holding_days: integer`, and `display_status: "GRACE"/"PROFITABLE"/"LOSING"`. It does **not** return `grace_days_remaining`.

- **Decision:** Add `grace_days_remaining` (integer | null) to `GET /positions` response.
- **Formula:** `max(0, 10 - holding_days)` when `grace_period = true`; `null` when `grace_period = false`.
- **No data model change required** — derivable at query time.
- **Contract update required:** `docs/specs/api_contracts/position_endpoints.md` — add field to response schema.
- **Display format confirmed:** `"Day {holding_days + 1} of 10"`

```
Evidence:         Product Owner written confirmation, 2026-02-22.
                  Audit of position_endpoints.md: grace_period (bool) ✅ holding_days (int) ✅
                  grace_days_remaining: ABSENT — endpoint update required.
                  New field: grace_days_remaining, type: integer | null
                  Formula: max(0, 10 - holding_days) when grace_period = true; null otherwise
                  Contract file to update: docs/specs/api_contracts/position_endpoints.md
                  Display format: "Day {holding_days + 1} of 10"
                  No data_model.md change required.
Owner confirmation: Yes — Product Owner, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
```

---

#### R.2 — BLG-FEAT-07: CSV export endpoint scope confirmed

Decision: New endpoint `GET /trades/export/csv`.

- **Endpoint path:** `GET /trades/export/csv`
- **Response type:** `Content-Type: text/csv; Content-Disposition: attachment; filename="trade_history.csv"`
- **Scope:** Full closed trade history. No date filter for v1.6.1 (filter is a future enhancement).
- **Fields in CSV:** `ticker`, `market`, `entry_date`, `exit_date`, `shares`, `entry_price`, `exit_price`, `pnl`, `pnl_pct`, `holding_days`, `exit_reason`, `tags` (semicolon-separated), `entry_note`, `exit_note`.
- **No request body. No query parameters** for v1.6.1.
- **Contract update required:** Add new section to `docs/specs/api_contracts/trade_endpoints.md`.
- **`openapi.yaml` update required** in same PR (GI-3).

```
Evidence:         Product Owner written confirmation, 2026-02-22.
                  Endpoint: GET /trades/export/csv
                  Response: text/csv, attachment disposition, filename="trade_history.csv"
                  Fields: ticker, market, entry_date, exit_date, shares, entry_price,
                          exit_price, pnl, pnl_pct, holding_days, exit_reason,
                          tags (semicolon-joined), entry_note, exit_note
                  Scope: full history, no filter (v1.6.1)
                  Contract file: docs/specs/api_contracts/trade_endpoints.md (new section)
                  openapi.yaml: update in same PR per GI-3
Owner confirmation: Yes — Product Owner, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
```

---

### Gate R.3 — Frontend spec readiness confirmed

*Frontend Spec owner has been briefed. Page/component targets confirmed for all six items.*

```
Evidence:         Product Owner written briefing confirmation, 2026-02-22.
                  BLG-FEAT-01 (Drawdown Widget):       Dashboard page — new widget alongside existing stats cards
                  BLG-FEAT-02 (R-Multiple Column):     Trade History table — new column, frontend calculation
                  BLG-FEAT-04 (Best/Worst Widget):     Performance Analytics page — new widget/panel
                  BLG-FEAT-05 (Win Rate by Month):     Performance Analytics page — new bar chart component
                  BLG-FEAT-06 (Grace Period Indicator): Open Positions table — new column, extends grace_period display
                  BLG-FEAT-07 (CSV Export):            Trade History page — new export button, GET /trades/export/csv
                  Relevant specs: positions table spec, trade history table spec,
                                  analytics page spec, dashboard stats spec.
                  Frontend Spec owner to confirm spec currency at pre-alignment meeting.
Owner confirmation: Yes — Product Owner, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
```

---

### Gate R.4 — Strategy rules readiness confirmed

*No bundle item requires changes to `strategy_rules.md`. Grace period lifecycle is already defined there.*

```
Evidence:         Audit confirmed. No strategy_rules.md changes required across all six items.
Owner confirmation: Yes — PMO Lead, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
```

---

### Gate R.5 — Effort estimate reviewed

*Roadmap estimate accounts for all spec, backend, and frontend work.*

Revised estimate breakdown:

| Work stream | Effort |
|-------------|--------|
| Implementation (all six items) | ~6–8 hours |
| `metrics_definitions.md` — BLG-FEAT-01 current drawdown section | ~30 min |
| `portfolio_endpoints.md` — BLG-FEAT-01 two new fields | ~30 min |
| `position_endpoints.md` — BLG-FEAT-06 `grace_days_remaining` field | ~15 min |
| `trade_endpoints.md` — BLG-FEAT-07 new CSV endpoint section | ~45 min |
| `openapi.yaml` — BLG-FEAT-07 update (same PR) | ~15 min |
| **Revised total** | **~8–10.5 hours** |

Notes:
- BLG-FEAT-02 (R-multiple): frontend spec update only — no API spec authoring.
- BLG-FEAT-04 and BLG-FEAT-05: no spec changes required.
- Roadmap entry update required: `docs/product/roadmap.md` — QWB estimated total effort.

```
Evidence:         Product Owner written confirmation, 2026-02-22.
                  Original estimate: ~6–8 hours (implementation only)
                  Spec authoring additions itemised above.
                  Revised total: ~8–10.5 hours
                  Roadmap entry to be updated: docs/product/roadmap.md
Owner confirmation: Yes — Product Owner, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
```

---

### Gate R.6 — Decisions inventory produced

*Preliminary decisions list produced and agreed as meeting agenda.*

```
Evidence:         Readiness audit produced 6 open decisions (D1–D6) plus 1 non-blocking query (D2a).
                  Filed in Preliminary Decisions List below.
Owner confirmation: Yes — PMO Lead, 2026-02-22
PMO validation:   Pass — PMO Lead, 2026-02-22
```

---

## Preliminary Decisions List (Pre-Alignment Meeting Agenda)

| # | Decision | Owner | Pre-condition | Notes |
|---|----------|-------|---------------|-------|
| D1 | BLG-FEAT-01: Formally adopt current drawdown formula and GET /portfolio field additions | Metrics Definitions owner + API Contracts owner | R.1 confirmed — ready | Formula pre-confirmed by Product Owner. Meeting to formally adopt in spec. |
| D2 | BLG-FEAT-02: Formally confirm frontend-only R-multiple; close scope | Metrics Definitions owner | R.1 confirmed — ready | Already canonical — formal close only. |
| D2a | BLG-FEAT-02: Confirm `stop_price` availability in `GET /trades` direct response (not only `trades_for_charts`) | API Contracts owner | — | Non-blocking. If absent: no implementation change needed — `trades_for_charts` sufficient. |
| D3 | BLG-FEAT-04: Formally confirm R-multiple ranking; top 3 / bottom 3 | Product Owner | D2 closed | Pre-confirmed. Formal close only. |
| D4 | BLG-FEAT-06: Formally adopt `grace_days_remaining` field addition to `GET /positions` | API Contracts owner | R.2 confirmed — ready | Formula and field pre-confirmed. Meeting to formally adopt. |
| D5 | BLG-FEAT-07: Formally adopt CSV endpoint definition; confirm field list complete | API Contracts owner | R.2 confirmed — ready | Endpoint, fields, and response type pre-confirmed. Meeting to formally close. |
| D6 | BLG-TECH-06: Confirm whether canonicalisation of `sharpe_ratio_trade_method` is in scope for this bundle or tracked separately | Product Owner + API Contracts owner | — | Backlog item already exists. Decision: bundle or separate delivery? |

---

## Action Register

| # | Action | Owner | Deadline | Status | Blocked on |
|---|--------|-------|----------|--------|------------|
| A-PRE-01 | Drawdown formula confirmed — see Gate R.1 | Product Owner | 2026-02-22T23:59:00Z | ✅ COMPLETE | — |
| A-PRE-02 | R-multiple formula + frontend-only decision confirmed — see Gate R.1 | Product Owner | 2026-02-22T23:59:00Z | ✅ COMPLETE | — |
| A-PRE-03 | Grace days field in `GET /positions` confirmed absent; update scoped — see Gate R.2 | Product Owner | 2026-02-22T23:59:00Z | ✅ COMPLETE | — |
| A-PRE-04 | CSV export endpoint scope confirmed — see Gate R.2 | Product Owner | 2026-02-22T23:59:00Z | ✅ COMPLETE | — |
| A-PRE-05 | Frontend Spec owner briefing + page/component targets confirmed — see Gate R.3 | Product Owner | 2026-02-22T23:59:00Z | ✅ COMPLETE | — |
| A-PRE-06 | Revised effort estimate confirmed — see Gate R.5 | Product Owner | 2026-02-22T23:59:00Z | ✅ COMPLETE | — |
| A-PRE-07 | All deadlines confirmed and GI-2 compliant | Product Owner | 2026-02-22T23:59:00Z | ✅ COMPLETE | — |
| A-001 | Issue pre-alignment meeting invitation with D1–D6 + D2a agenda to all owners | PMO Lead | 2026-02-23T17:00:00Z | 🔴 OPEN | — |

> GI-2 compliant: All deadlines are UTC-dated. No ASAP, TBC, or relative expressions.

---

## Stakeholder Next Steps

**As of 2026-02-22:**

| Role | Action | By when |
|------|--------|---------|
| **PMO Lead** | Issue pre-alignment meeting invitation with full D1–D6 + D2a agenda | 2026-02-23T17:00:00Z |
| **API Contracts owner** | Prepare for meeting: confirm `stop_price` in `GET /trades` direct response (D2a); prepare draft CSV endpoint contract section | Before meeting |
| **Frontend Spec owner** | Review target page/component specs for all six items; flag any currency gaps to PMO Lead before meeting | Before meeting |
| **Metrics Definitions owner** | Review current drawdown formula as pre-confirmed; ready to formally adopt at meeting | Before meeting |
| **Product Owner** | Attend pre-alignment meeting; close all decisions | At meeting |
| **Engineering** | No current action | — |
| **QA Lead** | No current action | — |

---

## Open Blockers

**No open blockers.**

---

## Defect & Observation Register

*Populated during Phase 5 (verification). Empty until then.*

---

## Decisions Record Reference

Pre-alignment decisions: `docs/product/decisions/QWB-quick-wins-bundle.md`
*(to be created at Phase 1 — pre-alignment meeting)*

Key decisions summary *(for stakeholder orientation — full rationale in decisions record)*:

| # | Decision | Confirmed by |
|---|----------|-------------|
| D1–D6 | See Preliminary Decisions List above | To be closed at pre-alignment meeting |

---

## State Transition Log

| # | From | To | Date | Time (UTC) | Declared by | Gate passed |
|---|------|----|------|------------|-------------|-------------|
| 1 | PRE-LOGGED | READINESS_AUDIT | 2026-02-22 | 00:00:00Z | PMO Lead | — (Product Owner nomination received) |
| 2 | READINESS_AUDIT | AWAITING_MEETING | 2026-02-22 | 23:59:00Z | PMO Lead | Gate R — all items pass |

---

## Shipping Closure Checklist

*Completed by PMO Lead once Director of Quality final sign-off is confirmed.*

- [ ] Changelog entry added (`docs/product/changelog.md`)
- [ ] Roadmap updated — all six items → ✅ Complete, version bumped, estimated effort updated
- [ ] Scope document status → Superseded
- [ ] Decisions record status → Superseded
- [ ] Head of Engineering notified
- [ ] Lessons learnt review scheduled
- [ ] This phase gate document status → Shipped, date filed
