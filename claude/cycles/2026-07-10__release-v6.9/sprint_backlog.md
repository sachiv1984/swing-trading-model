# Sprint Backlog — 2026-07-10__release-v6.9

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-10
**Cycle:** 2026-07-10__release-v6.9
**Release:** v6.9
**Sprint Goal:** Give traders on-demand visibility into whether an open position still passes its original SI-01 entry rules and whether it carries overnight/weekend gap risk, closing out both named Product Value Alert pull-forward anchors from the 2026-07-10 rebalance.
**Backlog Slice Source:** Original — `claude/cycles/2026-07-10__release-v6.9/stage4_backlog_slice.md`

## Merge Order

- **EPIC merge sequence:** EPIC-01 → EPIC-02 (independent EPICs; sequence set by execution order in `sprint_planning_notes.md`, may also run in parallel).
- **`execution_state.json` owner:** EPIC-01.
- **Shared files:** `docs/specs/frontend/pages/positions.md` — already merged to v2.1 (both sections) at the design gate; no further shared-file conflict expected. See `sprint_planning_notes.md §Shared file ownership advisory`.

---

## Sprint Scope

### EPIC-01 — On-Demand Pre-Entry (SI-01) Compliance Recheck

**Maps to:** S2-01
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** M (~2–3 days)
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — On-demand pre-entry rule recheck for open positions (BLG-FEAT-64)

**Status at sprint open: ready**

**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** M (~2–3 days)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** New endpoint (`GET /positions/{position_id}/compliance-recheck`) — must be registered in `docs/reference/openapi.yaml` and `docs/specs/api_contracts/` in the same commit, plus `backend/routers/test.py` (representative value: an open position's ID), per CLAUDE.md hard rules. Design gate cleared: `docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md` + `docs/specs/frontend/pages/positions.md` v2.1 (Compliance Recheck Panel, reuses `PreEntryValidationPanel` pass/warn/fail pattern).

**Staging-only ACs:** None — AC-02 is coverable by Playwright (rendering + pass/fail/override states are all deterministic given API response fixtures).

---

### EPIC-02 — Overnight/Weekend Gap Risk Flag

**Maps to:** S2-02
**Owner:** Head of UX & Design; Head of Engineering
**Estimated effort:** M (~2–3 days)
**Risk IDs:** RISK-03
**Execution sequence:** 2

#### ST-02 — Overnight/weekend gap risk flag for open positions (BLG-FEAT-65)

**Status at sprint open: ready**

**Owner:** Head of UX & Design; Head of Engineering
**Estimated effort:** M (~2–3 days)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** No new endpoint anticipated (existing-data read path); if one is introduced during implementation, the same same-commit `openapi.yaml` / `docs/specs/api_contracts/` / `backend/routers/test.py` registration rules apply per CLAUDE.md. Design gate cleared: `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md` + `docs/specs/frontend/pages/positions.md` v2.1 (Gap Risk badge, existing Alerts column, amber-600 `#D97706`).

**Staging-only ACs:** None — AC-01–03 are coverable by Playwright using mocked earnings-calendar/OHLCV fixtures and mocked Friday-close date context.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 days |
| Total estimated effort (in-scope) | ~4–6 days |
| Utilisation | ~30–43% |
| Over-allocation | No |

## Items Deferred This Sprint

None — both named mandatory pull-forwards are in scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| §13 sign-off for ST-01 AC-04 | Strategy Rules & System Intent Owner | No |
| §13 sign-off for ST-02 AC-04 | Strategy Rules & System Intent Owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-07-10
**Scope confirmed:** Confirmed — 2026-07-10 (2 ST items, 2 EPICs, both Firm, within capacity)
**Capacity confirmed:** Confirmed — 2026-07-10 (~4–6 days estimated against ~12–14 days available, no over-allocation)
**Deferred execution blockers accepted (if any):** N/A — none present (`state.json deferred_execution_blockers` empty)
**Signed off by:** Product Owner (delegated authority, consistent with the release plan's own delegated scope decision)
**Date:** 2026-07-10
