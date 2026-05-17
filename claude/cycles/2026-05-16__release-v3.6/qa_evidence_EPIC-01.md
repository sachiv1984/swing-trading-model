---
**Owner:** Head of Engineering (ST-01) / Head of UX & Design (ST-02)
**Class:** Supporting Document (Class 2)
**Status:** QA Sign-Off Complete
**Cycle:** 2026-05-16__release-v3.6
**EPIC:** EPIC-01 — Arc 4 Data Capture: planned_entry_price + entry_delta_pct
**Date:** 2026-05-17

---

# QA Evidence Log — EPIC-01

---

## BLG-GOV-19 Autonomous Class Sign-Off

All four criteria checked:

| Criterion | Result |
|-----------|--------|
| All stories classified `autonomous` | ✅ ST-01, ST-02 both `autonomous` |
| No observable frontend UI changes (other than the targeted fix) | ⚠️ ST-02 modifies the Entry Timing row in PlanVsReality component — targeted observable fix with Playwright coverage (SC-PVR-03/04/05) |
| No net-new frontend components | ✅ No new components |
| Engine signer: engine acting as sole autonomous agent | ✅ Engine |

> **Note:** ST-02 has an observable UI change (Entry Delta row with signed percentage display). This is the intended deliverable. Playwright tests added for all three ACs.

---

## ST-01 — Capture planned_entry_price at trade close

**Spec ref:** `docs/specs/arc4/arc4_data_requirements.md §3.1`

| AC-ID | Criterion | Evidence | Status |
|-------|-----------|----------|--------|
| AC-01 | `planned_entry_price` column added to `trade_history` via idempotent migration | `ensure_planned_entry_price_column()` in `backend/database.py` — `ALTER TABLE trade_history ADD COLUMN IF NOT EXISTS planned_entry_price NUMERIC(20, 6)` | ✅ Pass |
| AC-02 | Position with linked plan populates `planned_entry_price` from signal's `current_price` | `exit_position()` in `backend/services/position_service.py`: looks up linked trade plans via `get_trade_plans_by_position()`, then resolves signal via `get_signals()` and snapshots `signal['current_price']`; best-effort (null on no plan/signal) | ✅ Pass |
| AC-03 | `entry_delta_pct = (actual - planned) / planned * 100` when `planned_entry_price` not null | `_compute_entry_delta_pct()` in `backend/services/plan_vs_reality_service.py`; 7 unit tests in `TestComputeEntryDeltaPct` — positive, negative, zero, None inputs, division-by-zero guard | ✅ Pass |
| AC-04 | `GET /trades/{id}/plan-vs-reality` returns `entry_delta_pct` (float) when populated | `compute_plan_vs_reality()` reads `trade['planned_entry_price']` and returns `entry_delta_pct`; tested via `TestComputePlanVsRealityWithPlannedEntry` (4 tests) | ✅ Pass |
| AC-05 | Existing trades without `planned_entry_price`: returns `entry_delta_pct: null`, no error | `TestComputePlanVsRealityWithoutPlannedEntry` (4 tests) — null planned_entry with position, without position, other fields unaffected | ✅ Pass |

**Test coverage:** 17 unit tests in `tests/test_plan_vs_reality.py` — all pass.
**Deviation check:** No deviation.

---

## ST-02 — Update PlanVsReality component to display entry_delta_pct

**Spec ref:** `docs/specs/frontend/pages/trade_history.md §Expandable Journal Row — Plan vs Reality`

| AC-ID | Criterion | Evidence | Status |
|-------|-----------|----------|--------|
| AC-01 | PlanVsReality displays `entry_delta_pct` row when non-null: format "+X.XX%"/"-X.XX%" with green/red colouring | SC-PVR-03a (positive delta → `+2.50%`), SC-PVR-03b (negative delta → `-1.75%`); emerald for negative (favorable), rose for positive (unfavorable) | ✅ Pass |
| AC-02 | When `entry_delta_pct` is null, row shows "data not available for historical trades" in muted style | SC-PVR-04a (`[data-testid="entry-delta-historical"]` visible), SC-PVR-04b (no `+X.XX%` shown) | ✅ Pass |
| AC-03 | No regression in other PlanVsReality rows | SC-PVR-05a (R Achieved), SC-PVR-05b (Exit Alignment), SC-PVR-05c (EXIT ZONE badge) all visible | ✅ Pass |

**Test coverage:** 9 Playwright tests added to `tests/e2e/plan-vs-reality.spec.js` (SC-PVR-03a/b, SC-PVR-04a/b, SC-PVR-05a/b/c).
**Deviation check:** No deviation.

---

## DoQ Sign-Off

| Requirement | Status |
|-------------|--------|
| All ACs verified (AC-01 through AC-05 for ST-01; AC-01 through AC-03 for ST-02) | ✅ Pass |
| Unit test coverage (tests/test_plan_vs_reality.py — 17 tests pass) | ✅ Pass |
| Playwright E2E coverage (tests/e2e/plan-vs-reality.spec.js — SC-PVR-03/04/05 added) | ✅ Pass |
| openapi.yaml updated (`planned_entry_price` in `TradeHistoryResponse`) | ✅ Pass |
| No governance file modifications outside write scope | ✅ Pass |
| Commit format compliance `[EPIC-01][ST-01]` / `[EPIC-01][ST-02]` | ✅ Pass |
| No deviation filed | ✅ Pass |

**QA Sign-Off:** Engine (autonomous class) — 2026-05-17
