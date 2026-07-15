**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-15
**Story:** ST-02 (BLG-SPEC-89, EPIC-02, v7.2)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# BLG-FE-109 Pre-Implementation Readiness Pass — "Start Trade from Plan"

## 1. Purpose

Close every pre-implementation information gap for `ST-03` ("Start Trade from Plan" — `BLG-FE-109`, EPIC-02) before it enters sprint planning. This is a confirmation/scoping pass — no code is written here; each section below documents what was confirmed, what remains a gap, and (where a gap exists) exactly what `ST-03` must build.

## 2. AC-01 — `trade_plan_id` Auto-Link Consistency

**Finding: schema gap confirmed.** The `positions` table (`docs/specs/data_model.md`, `CREATE TABLE positions`) has **no `trade_plan_id` column**. The only existing `trade_plan_id` reference in the schema is inside `trade_history.plan_vs_reality` (JSONB, see `DS-10`), which is populated by `plan_vs_reality_service` **at trade close**, not at entry.

This means "auto-link consistency" cannot reuse an existing field — `ST-03` must add a new nullable `trade_plan_id UUID REFERENCES trade_plans(id)` column to `positions` at entry time. Consistency requirement for `ST-03`: the value written to `positions.trade_plan_id` at open must be the same UUID later read back into `plan_vs_reality.trade_plan_id` at close, so `plan_vs_reality_service` should read the linkage from `positions.trade_plan_id` rather than requiring the user to re-select a plan at exit. This closes a latent data-consistency risk (two independent capture points for the same fact) before `ST-03` is scoped.

## 3. AC-02 — API Contract Entry Pre-Staged

**Finding: no existing `POST /positions` contract heading exists to extend.** Position creation in the current codebase goes through the generic entity CRUD surface (`base44.entities.Position.create(data)` in `src/pages/TradeEntry.js` line 71) — there is no custom backend router endpoint for position creation, and correspondingly no `## POST /positions` heading in `docs/specs/api_contracts/position_endpoints.md` today (only sub-resource actions: `/exit`, `/note`, `/tags`, etc.).

**Pre-staged entry (for `ST-03` to apply, not applied in this pass):** When `ST-03` adds the `trade_plan_id` column, it must add a `Fields` row to whichever contract file documents the Position entity's writable fields (or add one if none exists), naming `trade_plan_id` as an optional UUID field on create. **Do not add a new `## METHOD /path` heading for this** unless `ST-03` also introduces a genuine new backend router endpoint — a heading added without a matching `docs/reference/openapi.yaml` entry and `backend/routers/` implementation would fail the OpenAPI Drift Detection gate for a path that was never actually implemented as a custom route (CLAUDE.md, `## 2`). This scoping note itself is the pre-staged artefact for AC-02; the actual contract-file edit lands with `ST-03`'s implementation commit, in the same commit as the schema change, per standard practice.

## 4. AC-03 — `data_model.md` Field Documentation

Confirmed: `ST-03` must add a new dated entry to `docs/specs/data_model.md` (following the `DS-xx` numbering convention used by `DS-10` immediately above) documenting the new `positions.trade_plan_id` column: type `UUID`, nullable, `REFERENCES trade_plans(id)`, populated at entry time when the trade originates from a plan via "Start Trade from Plan"; `NULL` for manually-entered trades. This is a scoping note, not the entry itself — the entry is filed by `ST-03` alongside its migration, per the same-commit convention already used by prior `DS-xx` entries in this file.

## 5. AC-04 — `TradeEntry.js` Pre-Fill API Surface

**Finding: a directly reusable precedent pattern already exists.** `TradeEntry.js` already supports pre-fill via React Router `location.state`:

```js
const prefill = location.state?.watchlist_prefill || null;
const [formData, setFormData] = useState({
  ticker: prefill?.ticker || "",
  ...
  entry_price: prefill?.entry_price || "",
  stop_price: prefill?.stop_price || "",
  ...
});
```

This is the "Add to Position" pathway from `Watchlist.js`. **`ST-03` should follow this exact pattern** — pass a `location.state.trade_plan_prefill` object (analogous shape: `{ trade_plan_id, ticker, market, planned_entry_price, planned_stop_price, ... }`) from the "Start Trade from Plan" action on `TradePlan.js`/`TradePlans.js`, and extend `TradeEntry.js`'s `formData` initializer to read from it the same way it already reads `watchlist_prefill`. No new API endpoint is required for the pre-fill itself — it is a client-side navigation-state pass, not a server round-trip. The only new server-side surface needed is the `trade_plan_id` field on the eventual `Position.create()` call (see AC-01/AC-02).

## 6. AC-05 — Authorization Boundaries

Confirmed: no new authorization surface is introduced. The action reuses the existing authenticated `Position.create()` write path (already gated by the current session/portfolio authorization model — no change to who can create a position). Linking a `trade_plan_id` at creation does not expand what a user can do beyond what "manually enter a trade" already permits; it only removes a manual re-typing step. No gap filed.

## 7. AC-06 — §13 Automated-Execution Boundary

Confirmed against `claude/strategy/strategy_rules.md §13` (System boundaries: "human-in-the-loop by design"; "not an automated trading bot"). "Start Trade from Plan" **pre-fills** the trade entry form from a plan's `planned_entry_price`/`planned_stop_price`/ticker — it does not submit or execute anything automatically. The user still explicitly presses "Save" on `TradeEntry.js` ( `handleSubmit` → `createMutation.mutate(...)`), i.e. the same human confirmation step every manually-entered trade already requires. This does not cross the §13 boundary. No decision escalation required.

## 8. AC-07 — `TradeEntry.js` Regression-Risk Flag

Confirmed and flagged forward to `ST-03` (per `sprint_backlog.md` note). `TradeEntry.js`'s current submit payload (`handleSubmit`, lines 196–215) is a fixed, hand-built object — `ST-03` must add `trade_plan_id: prefill?.trade_plan_id || undefined` to this payload without disturbing the existing required-field validation (`isFormValid`) or the `fill_price`/`stop_price`/`atr_value` optional-field handling already in place. Manually-entered trades (no `trade_plan_prefill`) must produce `trade_plan_id: undefined`, keeping today's behaviour byte-for-byte unchanged. `ST-03` AC-04 ("no regression to existing `TradeEntry.js` validation or submission behaviour") should be tested by confirming the existing manual-entry flow still submits an identical payload shape when no plan prefill is present.

## 9. AC-08 — SI-02 Trade-Count Metric Review

Confirmed. SI-02 (Behavioural Drift Detection) is currently gated on ≥ 20 closed, plan-linked trades (`docs/specs/si02/data_prerequisite_audit.md`); production re-confirms 0/11 plan-linked trades as of 2026-07-13 (SI-02 trade gate, not yet met). "Start Trade from Plan" directly targets this gap: by removing the manual-linking friction, it should increase the plan-linkage rate of new trades going forward. No metric definition change is needed — `ST-03` does not alter how SI-02 counts linked trades (it still reads `trade_history.plan_vs_reality.trade_plan_id` at close, populated from `positions.trade_plan_id` per AC-01). This is a scope confirmation, not a metric redefinition.

## 10. AC-09 — `test.py` Entry Requirement

Confirmed as a forward requirement, not applicable yet. `backend/routers/test.py` currently registers only existing routes (`/endpoints`, `/quick-health`, `/rate-limit-scenarios`). Per CLAUDE.md's endpoint-test-suite rule: **if and only if `ST-03` introduces a new custom backend route** (rather than relying solely on generic entity CRUD for the `trade_plan_id` field), that route must be registered in `backend/routers/test.py` in the same commit, with the `SystemStatus.js` fallback count and `SC-SS-01b` Playwright assertion updated to match. If `ST-03` implements the field purely via the existing generic entity-CRUD surface (no new router endpoint), this requirement does not apply — record which path was taken in `ST-03`'s own execution record for traceability.

## 11. AC-10 — Scope Completeness Summary

All 9 scope points (AC-01 through AC-09) addressed above — each is either documented (schema gap + resolution plan), confirmed-no-gap (AC-05, AC-06), or explicitly scoped forward with exact instructions for `ST-03` (AC-02, AC-03, AC-04, AC-07, AC-09). `ST-03`'s own acceptance criteria (`stage4_backlog_slice.md#ST-03`) should reference this readiness pass (`docs/specs/blg_fe_109_pre_implementation_readiness_pass.md`) as its implementation baseline at the next sprint planning cycle that brings `ST-03` into scope.

## 12. Known Deviations

None. This is a net-new readiness/confirmation artefact; no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-15 | 1.0 | Initial readiness pass (ST-02, EPIC-02, v7.2) |
