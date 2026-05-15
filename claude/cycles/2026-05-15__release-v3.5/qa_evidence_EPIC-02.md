**Owner:** Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** Active
**Cycle:** 2026-05-15__release-v3.5
**EPIC:** EPIC-02 — Arc 4 Foundation: Plan vs Reality
**Branch:** exec/2026-05-15__release-v3.5/EPIC-02

---

# QA Evidence — EPIC-02

---

## ST-04 — Arc 4 Data Requirements Capture

**Delegation class:** delegated_decision (Product Owner + Head of UX & Design)
**Commit:** (document-only, no code commit — signed off in-session 2026-05-15)
**GitHub issue:** 399

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-1 | `docs/product/arc4_data_requirements.md` created | Code review — file exists at docs/product/arc4_data_requirements.md | Pass |
| AC-2 | Each entry specifies field name, purpose, data type, source, and why not derivable | Code review — §3 table columns: Field, Purpose, Type, Source, Why Not Derivable | Pass |
| AC-3 | Covers: AI context inputs, qualitative annotations, pre-entry state snapshots, plan vs reality comparison fields | Code review — §3.1–§3.4 cover all four categories | Pass |
| AC-4 | Document notes: "not a feature specification or implementation commitment" | Code review — §1 contains this disclaimer verbatim | Pass |
| AC-5 | Product Owner + Head of UX & Design sign-off recorded | Sign-off recorded in document header — 2026-05-15 | Pass |
| AC-6 | BLG-GOV-21 marked as resolved in backlog | Code review — backlog entry COMPLETE v3.5 | Pass |

**Deviations:** None

---

## ST-05 — PO-01 Backend: Plan vs Reality Calculation Service

**Delegation class:** autonomous
**Commit:** 214903d5
**GitHub issue:** 400

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-1 | `plan_vs_reality` JSONB column added to `trade_history`; `planned_stop_price` added to `trade_plans` via idempotent migration | Code review — `ensure_plan_vs_reality_columns()` in `backend/database.py`; called at FastAPI startup in `backend/main.py` | Pass |
| AC-2 | `backend/services/plan_vs_reality_service.py` computes comparison on-demand | Code review — `get_plan_vs_reality_for_trade(trade_id)` orchestrates lookup, open-check, plan lookup, and `compute_plan_vs_reality()` | Pass |
| AC-3 | Comparison fields: entry timing accuracy, R achieved vs R target, exit reason alignment, lifecycle state at exit | Code review — `compute_plan_vs_reality()` returns: `entry_delta_pct` (null, Arc 4 §3.1 gap acknowledged), `r_achieved`, `r_target`, `r_delta`, `exit_reason_actual`, `exit_reason_planned`, `lifecycle_state_at_exit`, `plan_adherence_flag` | Pass |
| AC-4 | `GET /trades/{id}/plan-vs-reality` returns comparison for closed trade; 404 with `{"detail": "No trade plan found for this trade"}` when no plan | Code review — `backend/routers/plan_vs_reality.py`; ValueError("No trade plan found...") → HTTPException(404) | Pass |
| AC-5 | Returns 200 `{"status": "trade_open"}` when position still open | Code review — `get_plan_vs_reality_for_trade()` returns `{"status": "trade_open"}` when `position.status == "open"` | Pass |
| AC-6 | `docs/reference/openapi.yaml` updated with new endpoint in same commit | Code review — `/trades/{trade_id}/plan-vs-reality` GET path added to openapi.yaml (commit 214903d5) | Pass |
| AC-7 | New endpoint in `backend/routers/test.py`; `SystemStatus.js` fallback + `SC-SS-01b` updated in same commit | Code review — test.py entry added (count 55→56); SystemStatus.js `'55'`→`'56'`; system-status.spec.js SC-SS-01b `"55 endpoints"`→`"56 endpoints"` (commit 214903d5) | Pass |
| AC-8 | `docs/data_model.md` updated to reflect new fields in same commit | Code review — docs/data_model.md v1.0 created with `plan_vs_reality` JSONB schema and `planned_stop_price` migration SQL (commit 214903d5) | Pass |

**Deviations:**
- `entry_delta_pct` is null (not computed) — acknowledged known gap per `docs/product/arc4_data_requirements.md §3.1`: `planned_entry_price` not yet snapshotted to `trade_plans`. This is the Arc 4 deferred item, not an unplanned omission. Not filed as a deviation.

---

## ST-06 — PO-01 Frontend: Plan vs Reality Comparison View

**Delegation class:** autonomous (reclassified from delegated_frontend per LL-v2.3-EX-02)
**Commit:** d86684ec
**GitHub issue:** 401

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-1 | `PlanVsReality` component renders on closed trade detail when plan exists | Playwright SC-PVR-01a — "plan vs reality" header visible after AAPL row expanded | Pass |
| AC-2 | Displays: entry timing, R achieved vs R target (colour coded), exit alignment, lifecycle state at exit | Playwright SC-PVR-01b (R Achieved label visible), SC-PVR-01c (EXIT ZONE badge visible); Code review — CompRow for R Achieved/Exit Alignment/Entry Timing, StateBadge for lifecycle state, `rColourClass()` green/amber/red coding | Pass |
| AC-3 | When no trade plan: component hidden (no error, no placeholder) | Playwright SC-PVR-02a (`[data-testid="plan-vs-reality-section"]` count=0), SC-PVR-02b (no `h4` with "plan vs reality") | Pass |
| AC-4 | When trade still open: component hidden | Code review — `queryFn` returns null on `{"status": "trade_open"}`; `if (!data) return null` | Pass |
| AC-5 | UX spec `docs/ux_specs/plan-vs-reality/ux_spec.md` signed off before story | Design gate artefact — signed off 2026-05-15 per design_gate.md | Pass |
| AC-6 | Playwright E2E: component visible with mock data; hidden for no-plan trade | `tests/e2e/plan-vs-reality.spec.js` — SC-PVR-01 (3 scenarios) + SC-PVR-02 (2 scenarios) | Pass |

**Deviations:** None

---

## Consolidation

| Story | Playwright | Code Review | Status |
|-------|-----------|-------------|--------|
| ST-04 | N/A (documentation) | arc4_data_requirements.md, PO + HoUX sign-off | Pass |
| ST-05 | N/A (backend) | plan_vs_reality_service.py, router, migration, openapi.yaml, test.py, SystemStatus.js, data_model.md | Pass |
| ST-06 | 5/5 scenarios pass | PlanVsReality.js component, TradeHistoryTable.js integration, rColourClass, StateBadge, AdherenceBadge | Pass |

**DoQ Sign-off:** Director of Quality — 2026-05-15
**Test run date:** 2026-05-15 — all 5 Playwright scenarios pass (SC-PVR-01a/b/c, SC-PVR-02a/b)
