**Owner:** Data Model & Domain Schema Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-16
**Story:** ST-07 (BLG-SPEC-94, EPIC-05, v7.3)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# BLG-FE-118 Pre-Implementation Readiness Pass — Saved Filters & Calendar View

## 1. Purpose

Close every pre-implementation information gap for `BLG-FE-118` (saved filter presets + a calendar view of trading activity) before it can be scoped into a future sprint (candidate: v7.4). This is a spec/scoping pass only — no code is written here. `BLG-FE-118` itself remains deferred (see `stage4_backlog_slice.md#Deferred-Items`).

## 2. AC-01 — Schema Decision: JSON-Column-on-Settings vs. Dedicated Table

**Decision: dedicated table.** Confirmed by reading `docs/specs/data_model.md §6` (`settings` table): it is a **strict singleton** — one row, no `portfolio_id`, no per-user or per-item dimension at all; every column is a scalar preference (`theme`, `min_hold_days`, commission rates, etc.). Saved filter presets are inherently a **collection** — a user may create an arbitrary number of named presets (e.g. "My Winners", "This Month's Trades"). Nesting a growing JSON array of presets inside one column of an otherwise-scalar singleton row conflates two different data shapes and would make every preset CRUD operation a read-modify-write of the entire settings row (lock contention risk, and inconsistent with how every other multi-row concept in this schema — `alert_rules`, `positions`, `trade_plans` — already gets its own table). This is the same structural mismatch already identified and resolved the same way for `BLG-FE-116`'s custom price alerts (`docs/specs/blg_fe_116_pre_implementation_readiness_pass.md §2` — singleton-per-type `alert_rules` cannot represent a many-per-ticker concept either).

**Proposed schema (`saved_filters`):**

```sql
CREATE TABLE saved_filters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    name VARCHAR(100) NOT NULL,
    filter_state JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_saved_filters_portfolio_name UNIQUE (portfolio_id, name)
);

CREATE INDEX idx_saved_filters_portfolio ON saved_filters(portfolio_id);
```

`filter_state` itself is JSONB (the filter criteria shape — ticker, date range, tags, etc. — varies by which page's filters are being saved, so a flexible blob is appropriate **within** the row; it is only the top-level "one row per preset" structure that must not be flattened into `settings`). `UNIQUE (portfolio_id, name)` prevents duplicate preset names, consistent with the `uq_alert_rules_portfolio_type` precedent pattern in `data_model.md §8`.

## 3. AC-02 — Formal Spec: Calendar View (Date Sourcing, Navigation Model)

**Finding: UI primitive already exists, but is missing its dependency — same gap class as the command palette.** `src/components/ui/calendar.js` already wraps `react-day-picker` (`DayPicker` component, shadcn-style). **Gap found:** `react-day-picker` is imported by `calendar.js` but is **not** declared in `package.json` (checked directly — absent, same class of gap as `cmdk` for `BLG-FE-115`, see `blg_fe_115_pre_implementation_readiness_pass.md §2`). `npm install react-day-picker` (pinned to a React-19-compatible version) must be the first commit of `BLG-FE-118`'s implementation.

**Date sourcing:** `GET /reports/monthly-pnl` (`docs/specs/api_contracts/reports_endpoints.md`) already computes month-by-month **realised** P&L from `trade_history.exit_date` (`data_model.md` line 152/191 — `exit_date DATE NOT NULL` on closed trades). The calendar view's day-level realised P&L should reuse this same source data at day granularity — either by extending `monthly-pnl`'s grouping to also return a day-bucketed array, or a new `GET /reports/daily-pnl` endpoint following the identical `trade_history.exit_date` grouping logic already implemented for the monthly report (implementation-time decision for `BLG-FE-118`; both are equally valid extensions of already-proven grouping logic — no new computation is required, only a different `GROUP BY` granularity).

**Navigation model:** Standard month-grid view (`DayPicker`'s default `mode` — no `range`/`multiple` selection mode needed for a read-only activity calendar), prev/next month navigation via the component's built-in `nav_button_previous`/`nav_button_next` (already styled in `calendar.js`). Each day cell should render a compact realised-P&L indicator (e.g. a coloured dot or small figure) sourced from the day-bucketed data above; clicking a day navigates to (or filters) the relevant trade history for that date — reusing `TradeHistory.js`'s existing filtering rather than building a new detail view.

## 4. AC-03 — Feasibility: Realised/Unrealised P&L Split in the Calendar View

**Finding: realised P&L is date-attributable; unrealised P&L is not — same constraint already solved by `GET /reports/monthly-pnl`.** Realised P&L is naturally date-anchored via `trade_history.exit_date` (per AC-02) — directly feasible per calendar day. Unrealised P&L, by contrast, is a **current-snapshot-only** figure with no date dimension: `reports_service.py`'s `get_estimated_unrealised_pnl()` sums `pnl` across currently-open positions "at time of report generation, not positions open during the specified [period]" (confirmed via the function's own docstring and `UNREALISED_NOTE` constant — explicitly "Indicative only", reused verbatim by both the Tax Year and Monthly P&L reports per the locked v7.0 design decision, `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md`). `reports_endpoints.md`'s own `GET /reports/monthly-pnl` documentation states this explicitly: unrealised P&L is "shown once, alongside the monthly table, not per row" — i.e. the exact same per-bucket infeasibility this readiness pass is being asked to re-assess for the calendar view has already been assessed and resolved the same way for the monthly table.

**Recommendation for `BLG-FE-118`:** reuse the identical pattern — render realised P&L per calendar day (feasible, date-attributable), and show unrealised P&L once as a single "as of today" figure alongside the calendar (e.g. a summary banner), not attributed to any individual day cell. Do not attempt to retroactively attribute unrealised P&L to past dates — the system has no historical daily mark-to-market snapshot to source that from (confirmed: no `daily_position_snapshot`-style table exists in `data_model.md`). This is a confirmed feasibility with a named constraint, not a blocker.

## 5. AC-04 — QA Acceptance-Criteria Template (BLG-FE-40 localStorage-Envelope Pattern)

**Distinguishing two persistence concerns this story touches:** (a) the **currently active** filter state on whichever page the calendar/filter UI lives on — this is ephemeral, device-local, cross-reload-only state, and should reuse `BLG-FE-40`'s versioned-localStorage-envelope pattern exactly as implemented for `RedFlagJournal.js` (`src/pages/RedFlagJournal.js`; test precedent `tests/e2e/red-flag-journal-filter-persistence.spec.js`) — including its graceful stale/corrupt-state recovery behaviour. (b) **saved, named presets** — these are the AC-01 `saved_filters` table rows, intentionally server-side (not localStorage) so they persist across devices/sessions, unlike the ephemeral active-filter cache.

**QA acceptance-criteria template (for `BLG-FE-118`'s own AC, drafted here for reuse):**
- Reloading the page preserves the currently-active filter selection (localStorage envelope, versioned, BLG-FE-40 pattern) — verify via the same test structure as `red-flag-journal-filter-persistence.spec.js`.
- A corrupted or version-mismatched localStorage envelope is cleared gracefully, not surfaced as an error to the user (BLG-FE-40 precedent behaviour).
- Saving a named preset persists it server-side (`saved_filters` row) and it is available after a full logout/login or on a different device/session (distinguishing it from (a) above).
- Deleting a saved preset removes it from the list without affecting the currently-active filter state.

## 6. AC-05 — API Contract Stub

**No new `## METHOD /path` heading is added to `docs/specs/api_contracts/` in this pass**, per the same rationale established in the three prior readiness passes this sprint (`blg_fe_109`, `blg_fe_115 §6`, `blg_fe_116 §9`): no backend router implementation exists yet.

**Pre-staged shape (for `BLG-FE-118` to apply, in the same commit as its `docs/reference/openapi.yaml` entry and `backend/routers/` implementation):**
- `GET /saved-filters` — list all `saved_filters` rows for the portfolio.
- `POST /saved-filters` — create one; body `{ name, filter_state }`; `400` if `name` already exists for this portfolio (per the `UNIQUE (portfolio_id, name)` constraint in AC-01).
- `DELETE /saved-filters/{id}` — per `conventions.md §12` DELETE convention (`{ deleted: true, id }`).
- `GET /reports/daily-pnl` (or a day-granularity extension of the existing `GET /reports/monthly-pnl`, per AC-02) — day-bucketed realised P&L plus the single current-snapshot `estimated_unrealised_pnl` field, mirroring `monthly-pnl`'s existing top-level-sibling pattern (AC-03).
- All endpoints follow the standard `{ status, data }` / `{ status, message }` envelopes and `X-API-Key` auth per `conventions.md §1`/`§2` — no new exemption.
- New route(s) must be registered in `backend/routers/test.py` and `SystemStatus.js`'s hardcoded fallback count updated, per CLAUDE.md's endpoint-test-suite rule, in the same commit as the implementation (not this pass).

## 7. AC-06 — `DataState` Empty-State Reuse ("No Events")

Confirmed reusable without a new variant. An empty calendar (no closed trades in the visible month) is a standard full-page/section empty state — the existing default-sized `DataState` (`design_system.md` line 132, `py-16`/`w-10 h-10` default sizing) is a direct fit, same conclusion as `BLG-FE-116`'s "no alerts configured" state (`blg_fe_116_pre_implementation_readiness_pass.md §AC-09`) and unlike the command palette's compact-list context, which needed a new-variant decision. No `design_system.md` change required for this AC.

## 8. Scope Completeness Summary

All 6 acceptance criteria (AC-01 through AC-06) addressed: AC-01 (dedicated `saved_filters` table decided with rationale grounded in `settings`'s confirmed singleton structure — not deferred to execution kickoff, per RISK-05/LP-14), AC-02 (calendar spec authored — date sourcing reuses `monthly-pnl`'s proven `trade_history.exit_date` grouping logic; `react-day-picker` dependency gap flagged as an implementation-time blocker, same class of gap as `cmdk`), AC-03 (feasibility confirmed with a named constraint — realised P&L is date-attributable per day, unrealised is not, resolved using the same pattern already shipped in `GET /reports/monthly-pnl`), AC-04 (QA AC template drafted, correctly distinguishing the BLG-FE-40 ephemeral-localStorage concern from the AC-01 server-side named-preset concern), AC-05 (contract stub pre-staged as prose with explicit no-heading rationale), AC-06 (confirmed no-gap). `BLG-FE-118`'s own acceptance criteria at its next sprint planning cycle should reference this readiness pass as its implementation baseline.

## 9. Known Deviations

None. This is a net-new readiness/confirmation artefact; no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-16 | 1.0 | Initial readiness pass (ST-07, EPIC-05, v7.3) |
