**Owner:** Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** Active
**Cycle:** 2026-05-09__release-v3.3
**EPIC:** EPIC-02 — Arc 3 Decision Support — Grace Period + Stop Management (IT-02, IT-03)
**Branch:** exec/2026-05-09__release-v3.3/EPIC-02

---

# QA Evidence — EPIC-02

---

## ST-04 — Grace Period Decision Support backend

**Delegation class:** autonomous
**Commit:** e0a15543
**GitHub issue:** null

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | `GET /positions/grace-period-alerts` returns positions in GRACE state, days_in_state ≥ 8 | Code review — SQL WHERE position_state='GRACE'; Python filter days_in_state < 8 | Pass |
| AC-02 | Response includes position_id, ticker, days_in_state | Code review — alert dict construction | Pass |
| AC-03 | Response includes trade_plan_id if linked, else null | Code review — LEFT JOIN trade_plans on position_id | Pass |
| AC-04 | trade_plan_summary: setup_thesis excerpt, entry_rationale, stop_level, r_target | Code review — trade_plan_summary dict with all 4 fields | Pass |
| AC-05 | No linked plan: trade_plan_summary returns null | Code review — `if row.get("trade_plan_id"):` guard | Pass |
| AC-06 | Endpoint registered in routers/test.py | Code review — entry present | Pass |
| AC-07 | Endpoint registered in openapi.yaml | Code review — /positions/grace-period-alerts path present | Pass |

**Deviations:** Graceful fallback added: if `state_entered_at` is null (EPIC-01 migration not yet applied), endpoint falls back to counting trading days from entry_date. This ensures the endpoint works on a partially-migrated DB.

---

## ST-05 — Grace Period Decision Support frontend

**Delegation class:** delegated_frontend
**Status:** Not started — pending frontend delegation
**GitHub issue:** null

### Frontend ACs (pending delegation)

- Alert card on positions page / dashboard when GRACE position ≥ day 8
- Card displays: ticker, days_in_state, trade plan context
- Dismissible (localStorage — no backend persistence)
- Link to trade plan detail (if trade_plan_id present)
- §13 display-only: no automated recommendation
- Playwright scenario: alert renders when GRACE state ≥ day 8

---

## ST-06 — Stop Management Workflow backend

**Delegation class:** autonomous
**Commit:** e0a15543
**GitHub issue:** null

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | `GET /positions/{id}/stop-trail` returns current_stop from position record | Code review — SELECT current_stop from positions | Pass |
| AC-02 | `atr_trail_stop = current_price - (ATR × 2.0)` | Code review — `atr_trail_stop = round(current_price - (atr * trail_multiplier), 4)` | Pass |
| AC-03 | `trail_difference = atr_trail_stop - current_stop` (null if current_stop null) | Code review — null guard + round(atr_trail_stop - current_stop, 4) | Pass |
| AC-04 | `trail_r_terms`: difference / R-value (null if no R available) | Code review — initial_stop guard + r_value computation | Pass |
| AC-05 | `recommendation` string: "Raise stop to {atr_trail_stop}" (§13 display-only) | Code review — recommendation constructed as string, not action | Pass |
| AC-06 | current_stop null: trail calculation returns null trail_difference | Code review — null guard | Pass |
| AC-07 | Endpoint registered in routers/test.py | Code review — entry present | Pass |
| AC-08 | Endpoint registered in openapi.yaml | Code review — /positions/{position_id}/stop-trail path present | Pass |

**Deviations:** None

---

## ST-07 — Stop Management Workflow frontend

**Delegation class:** delegated_frontend
**Status:** Not started — pending frontend delegation
**GitHub issue:** null

### Frontend ACs (pending delegation)

- "Trail Stop" button per positions row (PROFITABLE or EXIT ZONE state, current stop set)
- Opens guided panel: current stop, ATR trail stop, difference (price and R-terms), confirmation button
- User must click "Update stop" to proceed; cancel/dismiss available
- "Trail Stop" button disabled with tooltip if current_stop null
- §13: system presents; human confirms; no automated action
- Playwright scenario: trail stop panel opens and confirm button is present

---

## Consolidation

| Story | Status | Notes |
|-------|--------|-------|
| ST-04 | Pass | All 7 ACs met. Fallback for pre-migration state. |
| ST-05 | Pending | Delegated_frontend. Playwright required. |
| ST-06 | Pass | All 8 ACs met. |
| ST-07 | Pending | Delegated_frontend. Playwright required. |

**QA readiness for PR:** Backend stories (ST-04, ST-06) are PR-ready. Frontend stories (ST-05, ST-07) require separate delegation and sign-off before delivery verification.

**QA sign-off checklist:**
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations (null-state fallback in ST-04 is valid graceful degradation, not a spec divergence)
- [x] Regression areas checked — /grace-period-alerts is a new endpoint; route ordering confirmed before /{position_id} to avoid path conflict; /stop-trail null guards prevent failures when current_stop absent
- [x] No frontend component URL construction changes (ST-05/07 excluded from PR; backend-only changes)

- Signed off by: Director of Quality
- Date: 2026-05-12
- Comments: ST-04 and ST-06 verified. Grace period alert logic correct (GRACE state + days_in_state ≥ 8, LEFT JOIN trade_plans). Stop trail formula `current_price - (ATR × 2.0)` confirmed per strategy_rules.md default. §13 compliance confirmed: recommendation is a display string, not an automated action. ST-05/07 excluded from PR per delegation records DEL-20260510-02/03. No P0 or P1 issues. Note: EPIC-02 must merge after EPIC-01 (depends on DS-05 position_state and state_entered_at columns).
