**Owner:** Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** Active
**Cycle:** 2026-05-09__release-v3.3
**EPIC:** EPIC-01 — Position Lifecycle State Machine (IT-01)
**Branch:** exec/2026-05-09__release-v3.3/EPIC-01

---

# QA Evidence — EPIC-01

---

## ST-01 — Positions data model: lifecycle state fields and migration

**Delegation class:** autonomous
**Commit:** 9f0f2af2
**GitHub issue:** 350

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | `position_state VARCHAR(20)` column added to positions table | Code review — DS-05 up migration in data_model.md | Pass |
| AC-02 | `state_entered_at TIMESTAMP` column added | Code review — DS-05 up migration | Pass |
| AC-03 | `state_history JSONB NOT NULL DEFAULT '[]'` column added | Code review — DS-05 up migration | Pass |
| AC-04 | Backfill: existing open positions get GRACE (< 10 trading days) or UNKNOWN | Code review — DS-05 backfill CTE with weekday counting | Pass |
| AC-05 | Down migration reverts all three columns | Code review — DS-05 down migration | Pass |
| AC-06 | DS-05 sign-offs recorded | Code review — Data Model owner + Head of Specs sign-off in data_model.md | Pass |

**Deviations:** DEV-01: AC specified "Alembic migration" but project uses direct SQL migrations in data_model.md. Implemented as DS-05 direct SQL migration per established project pattern. Deviation filed in execution_state.json.

---

## ST-02 — Position lifecycle state machine backend service

**Delegation class:** autonomous
**Commit:** 9f0f2af2
**GitHub issue:** 351

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | `compute_position_state()` returns EXIT ZONE, PROFITABLE, LOSING, GRACE, or UNKNOWN | Unit tests — TestComputePositionState (14 tests, all pass) | Pass |
| AC-02 | EXIT ZONE: price >= entry + 2R (requires valid initial_stop < entry) | Unit test `test_exit_zone` | Pass |
| AC-03 | PROFITABLE: price > entry + 0.5 ATR | Unit test `test_profitable` | Pass |
| AC-04 | LOSING: price < entry - 0.5 ATR | Unit test `test_losing` | Pass |
| AC-05 | GRACE: trading days ≤ 10 and within ±0.5 ATR | Unit tests `test_grace_period` (trading days counting) | Pass |
| AC-06 | UNKNOWN: missing ATR, or post-grace neutral zone | Unit tests `test_unknown_no_atr`, `test_unknown_post_grace` | Pass |
| AC-07 | `GET /positions` enriched with position_state, state_entered_at, days_in_state | Code review — main.py GET /positions lifecycle update | Pass |
| AC-08 | `GET /positions/{id}` returns single position with lifecycle fields | Code review — new endpoint in main.py | Pass |
| AC-09 | `POST /positions/{id}/refresh-state` recalculates and persists state | Code review — refresh endpoint in main.py | Pass |
| AC-10 | Both new endpoints registered in routers/test.py | Code review — entries under "Position Lifecycle (v3.3)" | Pass |
| AC-11 | Both new endpoints in openapi.yaml | Code review — `/positions/{position_id}` and `/positions/{position_id}/refresh-state` paths | Pass |
| AC-12 | 22 unit tests pass | Test output — `pytest tests/test_position_lifecycle.py` all pass | Pass |

**Deviations:** None

---

## ST-03 — Position lifecycle state: frontend display

**Delegation class:** delegated_frontend
**Status:** Not started — blocked on ST-16 (EPIC-04) for arc3_lifecycle_display feature flag infrastructure
**GitHub issue:** 352

### Status

ST-03 is deferred to Sprint 2 pending ST-16 (feature flag rollout). ST-16 is now complete on EPIC-04 branch (commit e3a834d1). ST-03 can proceed once EPIC-04 merges.

**Frontend ACs (pending):**
- Position state badge (GRACE/PROFITABLE/LOSING/EXIT ZONE/UNKNOWN) visible on positions page
- Badge gated behind `arc3_lifecycle_display` feature flag
- days_in_state displayed with badge
- Playwright E2E scenario required
- Human staging sign-off required for badge states not covered by Playwright

---

## Consolidation

| Story | Status | Notes |
|-------|--------|-------|
| ST-01 | Pass | Migration spec complete. Alembic deviation documented. |
| ST-02 | Pass | All 12 ACs met. 22 unit tests passing. |
| ST-03 | Pending | Blocked on ST-16 (now complete on EPIC-04). Delegation required. |

**QA readiness for PR:** ST-01 and ST-02 are PR-ready. ST-03 is excluded from this EPIC's PR (blocked/deferred).

**Director of Quality sign-off:** [AWAITING SIGN-OFF — required before PR merge]
