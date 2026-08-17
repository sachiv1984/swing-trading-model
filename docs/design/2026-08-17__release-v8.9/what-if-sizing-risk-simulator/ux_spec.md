**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-08-17__release-v8.9
**Story:** ST-05 (EPIC-02, BLG-FEAT-91)

# UX Spec — Pre-Commit "What-If" Sizing/Risk Simulator on the Trade Plan Form

## 1. Problem

`BLG-FEAT-91` asks for a way to see position size, R at risk, and portfolio heat impact update live as the user adjusts stop distance/entry price on the trade-plan form, before saving — so sizing/risk trade-offs can be explored during pre-trade planning rather than only at order entry (`TradeEntry.js`'s existing `PositionSizingWidget`).

**Grounding:** `trade_plans` (`docs/specs/data_model.md` — Table: trade_plans) has no `entry_price` or `shares` column — the table is a qualitative pre-trade reasoning document (`setup_thesis`, `entry_rationale`, `r_target`, etc.) plus `stop_level` (added post-base-schema; documented at `trade_plan.md` §5.1). This confirms AC-03 ("no DB write occurs from interacting with the preview alone") is achievable by construction: the simulator's inputs are either the existing persisted `Stop Level` field or new ephemeral, form-local-only state — nothing new is added to the `trade_plans` schema for this story.

## 2. Decision

Add a new collapsible panel, **"What-If Sizing Preview"**, to the Trade Plan creation and edit form (`trade_plan.md`), positioned directly below the Signal Context panel (§5a, when present) / core plan fields, and above the Pre-Trade Entry Checklist (§6) — the same slot precedent used by other advisory-only, non-persisted panels on this form.

### 2.1 Inputs

| Field | Source | Persisted? |
|-------|--------|------------|
| Stop Level | Existing `Stop Level` field (§5.1) | Yes (already persisted) |
| Planned Entry Price | **New**, ephemeral, panel-local numeric input | **No** — form-local React state only, never included in the `POST /trade-plans` / `PUT /trade-plans/{id}` payload |
| Risk % | Same `defaultRiskPercent` settings value used by `PositionSizingWidget`; user-adjustable within the panel, session-local (mirrors `PositionSizingWidget`'s `sessionStorage` behaviour, same key namespace not shared — panel keeps its own to avoid cross-page coupling) | No |

Panel is hidden entirely (no placeholder) until both Planned Entry Price and Stop Level have valid positive values — same "hidden until inputs present" convention as the Signal Context panel (§5a.1).

### 2.2 Calculation

Debounced 300ms after any input change (matches `PositionSizingWidget`'s existing debounce), calls the same `POST /portfolio/size` endpoint used by `PositionSizingWidget` — **not a duplicate/parallel calculation path** — with `{ entry_price: plannedEntryPrice, stop_price: stopLevel, risk_percent: riskPercent, market }`. Reusing the identical backend endpoint is what guarantees AC-02: "Preview value matches what is actually saved when the plan is submitted with the same inputs" — since `TradeEntry.js` (reached via §10 "Start Trade from Plan" hand-off, which pre-fills `stop_price` from `plan.stop_level`) calls the same endpoint with the same computation, entering the same entry price and stop at order time reproduces the identical suggested size.

### 2.3 Output Display

| Element | Source | Format |
|---------|--------|--------|
| Suggested Position Size | `suggested_shares` | "{N} shares" |
| R at Risk | Derived: `(plannedEntryPrice − stopLevel) × suggested_shares`, converted via `fx_rate` for US market same as existing widget | Native-currency, 2dp |
| Portfolio Heat Impact | `response.heat_impact_percent` (or equivalent field already returned by `/portfolio/size` — reuse, do not introduce a second endpoint call) | "+X.X% heat" |
| Concentration reason | `concentration_reason` (ST-04, see companion decision record `docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md`) | Same amber inline-note treatment as ST-04 specifies for `PositionSizingWidget` |

**Loading:** inline skeleton on the three result rows only (inputs remain interactive), matching the widget's existing `sizingLoading` pattern. **Error / invalid inputs:** reuse the widget's existing `AMBER_MESSAGES` / `SYSTEM_MESSAGES` conventions verbatim (e.g. "Stop price must be below entry price").

### 2.4 No Persistence Guarantee (AC-03)

Nothing in this panel triggers `POST /trade-plans` or `PUT /trade-plans/{id}`. `Planned Entry Price` and the panel's own `Risk %` override are never included in the Save Trade Plan payload (§5.2) — confirmed by construction since they are not `trade_plans` columns. `Save Trade Plan` continues to submit exactly the existing §5.1 field set, unchanged.

## 3. Constraints Checked

- **§13 compliance:** display-only, advisory preview of a deterministic calculation the user already sees (in different form) at order entry; no automated action, no write. Consistent with the existing Prospective Heat Panel (`risk_dashboard.md` §7)'s own §13 framing, which this panel is functionally a sibling of (form-embedded rather than dashboard-embedded).
- Does not duplicate `risk_dashboard.md` §7's Prospective Heat Panel — that panel is a standalone, ticker-agnostic hypothetical on the Risk Dashboard; this one is inline on the Trade Plan form, scoped to the specific plan being authored, and reuses the same sizing endpoint as `PositionSizingWidget` rather than the heat-only endpoint. No contradiction; different call sites, same underlying deterministic sizing service.
- No new AI-provider call — §13 boundary pre-check (`design_gate_prompt.md` STEP 1) not applicable.

## 4. Product Owner Approval

Approved 2026-08-17 (design gate session).

## Notes

- Backend: `POST /portfolio/size` must confirm it already returns (or is extended to return, same commit as ST-04/ST-05 backend work) a heat-impact field suitable for reuse here — if not currently present, this is a shared backend dependency between ST-04 and ST-05 and should be sequenced accordingly at sprint planning.
