**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-15
**Cycle:** 2026-07-15__release-v7.2
**Release:** v7.2
**Sprint Goal:** Clear every pre-implementation dependency for v7.2's dashboard and trade-plan UX work in a single sprint: complete the mobile responsiveness baseline assessment (EPIC-01), the trade-plan-linkage and dashboard-UX readiness/spec passes (EPIC-02 `ST-02`, EPIC-03 `ST-04`), the notification surface consolidation audit (EPIC-04), and the combined design-review/shared-Playwright-suite plan (EPIC-05) — so the three UI implementation stories (`ST-03`, `ST-05`, `ST-06`) are fully unblocked and ready to enter sprint planning next.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

## Merge Order

- **EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05
- **`execution_state.json` owner:** EPIC-01 (first in execution order — EPIC-02/EPIC-03/EPIC-04/EPIC-05 branches must check for existence and append rather than overwrite)
- **Shared files across EPICs:** None identified — see `sprint_planning_notes.md §Shared file ownership advisory` for the full per-EPIC file ownership breakdown

## Sprint Scope

### EPIC-01 — Mobile Responsiveness Baseline

**Maps to:** S2-01
**Owner:** Head of UX & Design
**Estimated effort:** 1.5 days
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Mobile responsiveness baseline assessment

**Owner:** Head of UX & Design
**Estimated effort:** 1.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None

**Notes:** Sequenced first per roadmap recommendation — findings may inform `ST-02`/`ST-04`'s readiness-pass approach and will reach the Product Owner before `ST-03`/`ST-05`/`ST-06` (deferred this sprint) begin. AC-03 gate condition (Arc 5 completeness) is explicitly not yet met — this is a Product Owner priority override, not a gate resolution; proceed per backlog note.

**Staging-only ACs:** None — output is a written report, no code/UI change to verify visually.

---

### EPIC-02 — Trade-Plan-to-Execution Linkage

**Maps to:** S2-02
**Owner:** Head of Specs Team
**Estimated effort:** 2.5 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-02 — BLG-FE-109 pre-implementation readiness pass

**Owner:** Head of Specs Team
**Estimated effort:** 2.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** `ST-03` (implementation) is deferred out of this sprint per the EPIC-02 sequencing constraint in `stage4_backlog_slice.md` — `ST-03` may not enter sprint planning until `ST-02` completes execution. See `sprint_planning_notes.md §Deferred Items`. AC-10 requires all 9 scope points addressed before `ST-03`'s own sprint planning; AC-07 flags `TradeEntry.js` validation as a specific regression-risk AC for `ST-03`.

**Staging-only ACs:** None — documentation/confirmation pass, no UI to verify visually.

---

### EPIC-03 — Dashboard UX Hardening

**Maps to:** S2-04
**Owner:** Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 days
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-04 — BLG-FE-110/111 pre-implementation spec & instrumentation pass

**Owner:** Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 (S–M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** `ST-05`/`ST-06` (implementation) are deferred out of this sprint per the EPIC-03 sequencing constraint in `stage4_backlog_slice.md` — neither may enter sprint planning until `ST-04` completes execution. See `sprint_planning_notes.md §Deferred Items`. Per `design_gate.md` Notes: treat `dashboard-empty-states/ux_spec.md §2.1` (the `compact` prop pattern already specified for `ST-05`) as the source to generalise into `design_system.md` and the Base44 prompt template library, rather than re-deriving the pattern independently.

**Staging-only ACs:** None — documentation/spec pass, no UI to verify visually.

---

### EPIC-04 — Notification Surface Consolidation Review

**Maps to:** S2-07
**Owner:** Head of UX & Design / Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 days
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-07 — Notification/digest surface consolidation review

**Owner:** Head of UX & Design / Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 (M, audit only)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None — fully independent of all other EPICs this sprint

**Notes:** Implementation of any consolidation recommendation is explicitly out of scope this release (AC-03) — file as a follow-up backlog item if the audit recommends it.

**Staging-only ACs:** None — output is a written report, no code/UI change to verify visually.

---

### EPIC-05 — Combined Design Review & Shared QA Suite Planning

**Maps to:** S2-08
**Owner:** Head of UX & Design / Director of Quality
**Estimated effort:** 0.75 days
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-08 — Combined design review + shared Playwright suite plan

**Owner:** Head of UX & Design / Director of Quality
**Estimated effort:** 0.75 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** AC-01/AC-03 (combined design review) substantively satisfied by `design_gate.md`'s own run this cycle — see that document's Notes section. AC-04 (shared Playwright spec file named in `ST-03`/`ST-05`/`ST-06`'s sprint-backlog entries) cannot be fully closed this sprint since those three stories are deferred out of scope — the spec file name scoped under AC-02 should be backfilled into their entries at the sprint planning run that brings them in. Tracked in `sprint_planning_notes.md §Outstanding Actions`.

**Staging-only ACs:** None — process/planning item, no UI to verify visually.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12-14 days |
| Total estimated effort (in-scope) | 7.75 days (midpoint); ~10.0 days pessimistic |
| Utilisation | ~55-65% (midpoint) |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-03 | EPIC-02 | Blocked — `stage4_backlog_slice.md` EPIC-02 sequencing constraint; `ST-02` must complete execution first |
| ST-05 | EPIC-03 | Blocked — `stage4_backlog_slice.md` EPIC-03 sequencing constraint; `ST-04` must complete execution first |
| ST-06 | EPIC-03 | Blocked — `stage4_backlog_slice.md` EPIC-03 sequencing constraint; `ST-04` must complete execution first |

## Deferred Execution Blockers Accepted

*(section omitted — `deferred_execution_blockers` was empty)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Name shared Playwright spec file (`ST-08` AC-02) and backfill into `ST-03`/`ST-05`/`ST-06` entries at their future sprint planning run | Head of UX & Design / Director of Quality | No |
| Reconcile `.claude_current_state.json.design_gate_status` write gap | Head of Specs Team | No |
| Add prepended `prompt_change_log.md` row for `sprint_planning_prompt.md` v3.12→v3.13 | Head of Specs Team | No |
| Finalise v7.1 post-ship closure (on file but not marked complete) | PMO Lead | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-07-15
**Scope confirmed:** Confirmed — 5 EPICs (2 partial), 5 stories in scope; `ST-03`/`ST-05`/`ST-06` deferred per sequencing constraint, 2026-07-15
**Capacity confirmed:** Confirmed — PASS, no WARN, 2026-07-15
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-07-15
