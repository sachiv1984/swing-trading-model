**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-14
**Cycle:** 2026-05-14__release-v3.4
**Release:** v3.4
**Sprint Goal:** Deliver the Arc 3 in-trade risk management frontend (lifecycle badge, grace-period alert, stop-trail panel) and new drawdown/concentration risk prompts, while clearing the v3.3 deferred frontend quick wins and v3.4 spec/QA documentation debt.
**Backlog Slice Source:** original stage4_backlog_slice.md

---

# Sprint Backlog — 2026-05-14__release-v3.4

---

## Sprint Scope

---

### EPIC-04 — Spec, QA & Documentation Debt

**Maps to:** S2-05
**Owner:** Head of Specs Team
**Estimated effort:** ~2.0 days
**Risk IDs:** None
**Execution sequence:** 1 (Sprint 1 — ST-11 first, required before EPIC-01 begins)
**Merge order position:** 1st (EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02)

#### ST-11 — Research view component library (BLG-FE-31)

**Owner:** Head of Specs Team
**Estimated effort:** ~0.5 day
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** None — must complete before EPIC-01 execution begins
**Notes:** Delivers component catalogue for PT-02 research view; ST-01/02/03 (EPIC-01) should reference this catalogue before implementation.

---

#### ST-12 — Screener morning routine UX spec (BLG-FE-22)

**Owner:** Head of Specs Team
**Estimated effort:** ~0.5 day
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** None
**Notes:** Aged 2 cycles (v3.2 and v3.3 carried). Promoted to ST-12 in this release per §1.1 age advisory in release_plan.md.

---

#### ST-13 — trade_plan.md §6.2 spec update + AI journal review cadence (BLG-SPEC-28 + BLG-AI-03)

**Owner:** Head of Specs Team
**Estimated effort:** ~0.5 day
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** None
**Notes:** Bundled story (BLG-SPEC-28 + BLG-AI-03); both XS effort. AI review cadence requires OPERATIONAL_GUIDE reference.

---

#### ST-14 — Screener accuracy test protocol (BLG-QA-18)

**Owner:** Director of Quality
**Estimated effort:** ~0.5 day
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** None
**Notes:** Required before any sprint touching screener filter logic. Protocol must be executable by QA & Testing Owner.

---

### EPIC-03 — Frontend Quick Wins

**Maps to:** S2-04
**Owner:** Head of Engineering
**Estimated effort:** ~2.5 days
**Risk IDs:** RISK-04 (release-level capacity)
**Execution sequence:** 2 (Sprint 1 — concurrent with or after EPIC-04)
**Merge order position:** 2nd

#### ST-07 — Research page UK suffix strip + negative earnings days display (BLG-FE-23 + BLG-FE-24)

**Owner:** Head of Engineering
**Estimated effort:** ~0.5 day
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** None
**Notes:** Bundled story (BLG-FE-23 + BLG-FE-24); both XS effort. Existing `stripUkSuffix` utility available. No Playwright scenarios specified in AC — human staging or quick visual check sufficient given minor display fix nature.

---

#### ST-08 — Signals page: default to most recent day's signals (BLG-FE-25)

**Owner:** Head of Engineering
**Estimated effort:** ~0.5 day
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** None
**Notes:** Root cause investigation required if this is a regression. AC requires a "Show all" toggle or date picker — new control added.

---

#### ST-09 — Watchlist research status indicator (BLG-FE-29)

**Owner:** Head of Engineering
**Estimated effort:** ~0.5 day
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** None
**Notes:** Binary indicator only (done/not done). Scope constraint: no freshness or quality signal.

---

#### ST-10 — Trade plan status badges + abandonment UI (BLG-FE-30 + BLG-FEAT-21 frontend)

**Owner:** Head of Engineering
**Estimated effort:** ~1.0 day
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** DS-06 migration + abandonment API from v3.3 ST-17 (both live on main)
**Notes:** Backend is complete. Frontend delivers status badges across plan views and the abandonment UI with required reason input. Active-position guard enforced by existing backend.

---

### EPIC-01 — Arc 3 Frontend Completion

**Maps to:** S2-01
**Owner:** Head of Engineering
**Estimated effort:** ~3.25 days
**Risk IDs:** RISK-02 (TEST-GAP-EPIC-01/02-v33 Playwright scenarios must be authored alongside implementation)
**Execution sequence:** 3 (Sprint 2 — after EPIC-04 ST-11 merged)
**Merge order position:** 3rd

#### ST-01 — Position lifecycle state: frontend display (IT-01)

**Owner:** Head of Engineering
**Estimated effort:** ~1.25 days
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** ST-11 (EPIC-04) merged before this EPIC begins; `arc3_lifecycle_display` feature flag on main
**Notes:** Backend live: `GET /positions` returns `lifecycle_state`, `days_in_state`. UX spec: `docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md`. Playwright scenarios SC-LS-01–04 must be authored and pass before PR merge.

---

#### ST-02 — Grace Period Decision Support frontend (IT-02)

**Owner:** Head of Engineering
**Estimated effort:** ~1.0 day
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** ST-11 (EPIC-04) merged; `GET /positions/grace-period-alerts` live on main
**Notes:** UX spec: `docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md`. §13 compliance: display-only, no automated action. Playwright scenarios SC-GP-01–03 required before PR merge.

---

#### ST-03 — Stop Management Workflow frontend (IT-03)

**Owner:** Head of Engineering
**Estimated effort:** ~1.0 day
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** ST-11 (EPIC-04) merged; `GET /positions/{id}/stop-trail` live on main
**Notes:** UX spec: `docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md` (note: backlog slice references stop-trail-panel path — use stop-management-workflow path per design_gate.md). §13 compliance: user must click Confirm. Playwright scenarios SC-TS-01–03 required.

---

### EPIC-02 — Arc 3 Risk Prompts: Drawdown Review & Concentration Limits

**Maps to:** S2-02, S2-03
**Owner:** Head of Engineering
**Estimated effort:** ~3.5 days
**Risk IDs:** RISK-01 (resolved), RISK-03 (low — DS-03 sector data)
**Execution sequence:** 4 (Sprint 2 — after design gate; ST-04 before ST-05)
**Merge order position:** 4th (last)

#### ST-04 — Drawdown-Triggered Review Prompt backend (IT-04)

**Owner:** Head of Engineering
**Estimated effort:** ~1.5 days
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** None (new endpoint, no upstream dependency)
**Notes:** `GET /portfolio/drawdown-status` new endpoint. Must register in `backend/routers/test.py` and `openapi.yaml`. Settings integration for configurable threshold. Recommend completing ST-04 before ST-05 begins.

---

#### ST-05 — Drawdown-Triggered Review Prompt frontend (IT-04)

**Owner:** Head of Engineering
**Estimated effort:** ~1.0 day
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** ST-04 (backend endpoint available); UX spec: `docs/design/2026-05-14__release-v3.4/drawdown-review-prompt/ux_spec.md`
**Notes:** §13 compliance: display-only prompt, no automated changes. Server-side acknowledgement (not localStorage). Playwright E2E or human staging sign-off required per AC.

---

#### ST-06 — Position Concentration Limits (IT-05 — backend + frontend)

**Owner:** Head of Engineering
**Estimated effort:** ~1.0 day
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** DS-03 sector data (shipped v2.9, live on main); UX spec: `docs/design/2026-05-14__release-v3.4/concentration-limits-warning/ux_spec.md`
**Notes:** Combined backend + frontend story (S-effort). Graceful degradation when sector data absent. New endpoints must register in `backend/routers/test.py` and `openapi.yaml`. Playwright E2E or human staging sign-off required.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~10–13 days (mid-point ~11.5) |
| Total estimated effort (in-scope) | ~11.25 days |
| Utilisation | ~98% |
| Over-allocation | No — within capacity band |
| Capacity WARN acknowledged | Yes — Product Owner, 2026-05-14 (release planning) |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| *(none)* | — | All 14 stories within confirmed capacity |

## Deferred Execution Blockers Accepted

*(Section omitted — `deferred_execution_blockers` was empty in state.json)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Merge order (EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02) to be recorded in execution_state.json at Execution STEP 3 | Head of Engineering | No |
| QA evidence branch advisory: check remote branches before flagging missing QA evidence | QA & Testing Owner | No |
| ST-03 UX spec path discrepancy: use `stop-management-workflow/ux_spec.md` not `stop-trail-panel/ux_spec.md` | Head of Engineering | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — "Deliver the Arc 3 in-trade risk management frontend (lifecycle badge, grace-period alert, stop-trail panel) and new drawdown/concentration risk prompts, while clearing the v3.3 deferred frontend quick wins and v3.4 spec/QA documentation debt."
**Scope confirmed:** Confirmed — 14 stories across 4 EPICs; all within capacity band
**Capacity confirmed:** Confirmed — WARN acknowledged at release planning 2026-05-14; risk buffer documented (EPIC-02 slips to v3.5 if Sprint 2 over-runs)
**Deferred execution blockers accepted (if any):** N/A — no deferred execution blockers
**Signed off by:** Product Owner
**Date:** 2026-05-14
