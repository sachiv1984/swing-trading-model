**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-16
**Cycle:** 2026-05-16__release-v3.6
**Release:** v3.6
**Sprint Goal:** Complete Arc 4 data pipeline integrity by capturing planned_entry_price at trade entry and surfacing entry_delta_pct in the Plan vs Reality view, clear three cycles of QA and spec debt in the research domain, and apply four deferred governance prompt patches from v3.5.
**Backlog Slice Source:** original — claude/cycles/2026-05-16__release-v3.6/stage4_backlog_slice.md

---

# Sprint Backlog — 2026-05-16__release-v3.6

## Sprint Scope

### Merge Order

**Merge sequence:** EPIC-04 → EPIC-03 → EPIC-01

**execution_state.json owner:** EPIC-04 (first in execution order; EPIC-03 and EPIC-01 branches must check for file existence and append, not overwrite)

**Shared file advisory:**
- `openapi.yaml`: modified by both EPIC-03 (ST-07) and EPIC-01 (ST-01). EPIC-03 merges first (canonical owner). EPIC-01 branch must rebase onto `origin/main` after EPIC-03 PR merges before finalising openapi.yaml changes.
- `backend/routers/test.py`: modified by EPIC-01 (ST-01). EPIC-01 must rebase after EPIC-03 merges.

---

### EPIC-04 — Governance Maintenance

**Maps to:** S2-04
**Owner:** Head of Specs Team
**Estimated effort:** XS–S (~0.5 day total)
**Risk IDs:** None
**Execution sequence:** 1 (first to merge)
**Sprint:** 1

#### ST-09 — execution_prompt.md §13 gate story pattern formalisation

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.25 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Must precede ST-10 (both touch execution_prompt.md; coordinate as sequential steps in same branch or same commit). AC-04 adds 4 missing prompt_change_log.md entries for OA-RP-01–04.

---

#### ST-10 — execution_prompt.md metadata + sprint_close + Phase 3 patches

**Owner:** Head of Specs Team
**Estimated effort:** XS–S (~0.25 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** ST-09 (same file — must be sequential or same commit)

**Notes:** Three patches from v3.5 LL deferred actions 2–4: deviations_filed semantics, sprint_close three-field block, Phase 3 section reference. Version bump coordinated with ST-09 — single version bump if same commit.

---

### EPIC-03 — QA, Spec & UX Debt Clearance

**Maps to:** S2-03
**Owner:** QA & Testing Owner (ST-06) / API Contracts & Documentation Owner + Head of Engineering (ST-07) / Head of UX & Design (ST-08)
**Estimated effort:** S (~1 day total)
**Risk IDs:** RISK-03
**Execution sequence:** 2 (merges after EPIC-04)
**Sprint:** 1

#### ST-06 — SC-RV-18 and SC-RV-19 Playwright coverage

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Closes BLG-FE-32 and TEST-GAP-EPIC-03-v33. Both scenarios must pass in CI (AC-05). Protocol files updated: research_view_protocol.md §2.3 and research_view_regression_protocol.md §2.2.

---

#### ST-07 — Research endpoint HTTP error code differentiation

**Owner:** API Contracts & Documentation Owner + Head of Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Closes BLG-SPEC-27. openapi.yaml must be updated in same commit per CLAUDE.md §2 (AC-05). RISK-03: partial-failure behaviour (200 with nulls) must not regress (AC-03). Frontend 404/503 handling required (AC-06).

---

#### ST-08 — Research page UX fix: regime lozenge and font consistency

**Owner:** Head of UX & Design
**Estimated effort:** XS (~0.25 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Closes BLG-FE-26. AC-02 (font conformance) requires human staging side-by-side comparison with design_system.md. Playwright visual check acceptable for AC-01 (lozenge single-line constraint).

---

### EPIC-01 — Arc 4 Data Capture Foundation

**Maps to:** S2-01
**Owner:** Head of Engineering
**Estimated effort:** M (~1.5–2 days total)
**Risk IDs:** RISK-01
**Execution sequence:** 3 (merges last; must rebase onto main after EPIC-03 merges)
**Sprint:** Sprint 1 (ST-01), Sprint 2 (ST-02)

#### ST-01 — Capture planned_entry_price at trade entry

**Owner:** Head of Engineering
**Estimated effort:** S–M (~1 day)
**Delegation class:** autonomous
**Sprint:** 1

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (EPIC-03 merges first — rebase required before finalising openapi.yaml and backend/routers/test.py)

**Notes:** RISK-01: nullable field + conditional display; regression test with existing null trades (AC-05). Schema migration required — planned_entry_price added as nullable to trades table. openapi.yaml and backend/routers/test.py must be updated in same commit per CLAUDE.md §2. SystemStatus.js hardcoded fallback and SC-SS-01b in system-status.spec.js must also be updated.

---

#### ST-02 — Update PlanVsReality component to display entry_delta_pct

**Owner:** Head of Engineering
**Estimated effort:** XS–S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 2

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01 (backend field and API response required before frontend display)

**Notes:** AC-01 and AC-02 require Playwright tests. AC-03 requires Playwright regression on other PlanVsReality rows. Historical trade null case must show "Entry delta: data not available for historical trades" (muted style).

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~3–4 days (solo-dev, 2 sprints) |
| Total estimated effort (in-scope) | ~3.25–3.5 days (7 stories) |
| Utilisation | ~85–100% |
| Over-allocation | No (WARN acknowledged; Sprint 2 has buffer) |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-03 | EPIC-02 | Design gate: PO confirmed <20 closed trades (2026-05-16); PT-04 gate not met; defers to v3.7 |
| ST-04 | EPIC-02 | Depends on ST-03 spec; deferred with EPIC-02 to v3.7 |
| ST-05 | EPIC-02 | Depends on ST-03 + ST-04; deferred with EPIC-02 to v3.7 |

## Deferred Execution Blockers Accepted

*(No deferred execution blockers — `deferred_execution_blockers` was empty in state.json)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| scored_initiatives.md refresh (Arc 3/4 entries; v3.5 LL carry-forward) | Facilitator / PMO Lead | No |
| OA-RP-01–04: prompt change log gaps for 4 prompts | Head of Specs Team | No — addressed by EPIC-04 ST-09 AC-04 within this sprint |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** ✅ Confirmed
**Scope confirmed:** ✅ Confirmed — 7 stories (EPIC-01 ST-01/02, EPIC-03 ST-06/07/08, EPIC-04 ST-09/10); EPIC-02 deferred to v3.7 via design gate
**Capacity confirmed:** ✅ Confirmed — WARN acknowledged (standard mode); phased delivery within 2-sprint capacity
**Deferred execution blockers accepted (if any):** N/A — no deferred execution blockers
**Signed off by:** Product Owner
**Date:** 2026-05-16
