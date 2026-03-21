---
owner: PMO Lead
class: Operational Record (Class 3)
status: Filed
last_updated: 2026-03-21
cycle: 2026-03-18__release-v2.1
---

# Lessons Learnt Closure — 2026-03-18__release-v2.1

---

## §1 — Records Reviewed

| Record | Location | Status |
|--------|----------|--------|
| Release Planning lessons | `claude/cycles/2026-03-18__release-v2.1/lessons_learnt.md` | Read — no action items (clean planning phase) |
| Sprint Execution + Verification lessons | `claude/cycles/2026-03-18__release-v2.1/lessons_learnt.md` §Phase 3 + §Phase 4 | Read — 8 items classified |

**Note:** `lessons_learnt_cycle.md` does not exist for this cycle. Phase 3 and Phase 4 sections were appended to `lessons_learnt.md` instead of a separate file. Content is equivalent; file naming is a process note only. No gap in substantive coverage.

---

## §2 — Closure Phase Observations

### Post-ship deviations filed to canonical specs

During STEP 5 (deviation compliance check), two canonical specs were found to have no deviation entries despite deviations being accepted in the verification report:

- `docs/specs/api_contracts/alerts_endpoints.md` — DEV-ST04-01 (Telegram delivery) added. v0.1→v0.2. Spec owner (API Contracts & Documentation Owner) notified via closure record §6.
- `docs/specs/frontend/pages/trade_history.md` — DEV-ST14-01 (StatsCard gradient cosmetic) added. v1.2→v1.3. Spec owner (Frontend Specifications & UX Documentation Owner) notified via closure record §6.

### Specs Index test coverage gaps added

Three test coverage gap entries added to `docs/specs/Specs_Index.md` §9 (TSG-v21-01, TSG-v21-02, TSG-v21-03). All have corresponding backlog items (TEST-GAP-EPIC-02, TEST-GAP-EPIC-03, TEST-GAP-EPIC-05-SLIP).

### Backlog items closed

10 v2.1 backlog items moved to Closed Items table in `backlog.md`. BLG-TECH-05 target updated v2.1→v2.2 (was not shipped).

### ST items without standalone backlog entries (gap record)

The following ST items had no corresponding standalone backlog entry in `backlog.md` (they were directly scoped into the sprint from roadmap items or planned at sprint planning):
- ST-02 through ST-07 (EPIC-02 Alerts — directly scoped from ADR and spec authoring)
- ST-08, ST-09, ST-10 (EPIC-03 Watchlist — directly scoped from roadmap item 4.2)
- ST-11 (EPIC-04 Chart Interactivity — directly scoped from roadmap)

These are recorded as gaps but are acceptable — items scoped directly from roadmap entries during sprint planning do not always have standalone backlog entries.

---

## §3 — Lessons Learnt Action Summary

**Immediate actions applied: 1**

| # | Item | Action | Document | Version |
|---|------|--------|----------|---------|
| LL-v2.1-P4-3 | execution_state sealing guard | STEP 6 guard note added: do not emit Sprint_Complete until sealed = true | `execution_prompt.md` | v2.5→v2.6 |

**Deferred to next cycle: 7**

| # | Item | Owner | Target cycle |
|---|------|-------|--------------|
| LL-v2.1-P3-1 | Branch strategy — cherry-pick vs feature flag | PMO Lead + Product Owner | v2.2 sprint planning |
| LL-v2.1-P3-2 | Base44 @/ alias prompt fix | Head of Specs Team | v2.2 (if Base44 retained) |
| LL-v2.1-P3-3 | Delegation rule self-check (advisory) | PMO Lead | No action required (advisory only) |
| LL-v2.1-P3-4 | Cherry-pick dependency workflow | Head of Engineering | v2.2 sprint |
| LL-v2.1-P3-5 | Delegation log auto-update on item completion | Head of Specs Team | v2.2 (execution_prompt STEP 3 update) |
| LL-v2.1-P4-1 | QA evidence "Scenarios run" field guidance | Head of Specs Team | v2.2 (delivery_verification_prompt update) |
| LL-v2.1-P4-2 | Test scenario AC requirement on frontend/backend stories | PMO Lead + Head of Specs Team | v2.2 sprint planning (sprint_planning_prompt update) |

**Escalated for decision: 0**

---

## §4 — Carry-Forward Items for Next Cycle

1. **Delegation log auto-update (LL-v2.1-P3-5)** — execution_prompt.md STEP 3 needs an explicit step to update delegation log status when marking an item `done`. Currently requires manual update at sprint close. Owner: Head of Specs Team.

2. **Test scenario AC requirement (LL-v2.1-P4-2)** — New feature stories should require a test scenario file to be commissioned alongside DoQ sign-off. Sprint planning template needs updating to make this explicit. Owner: PMO Lead.

3. **QA evidence scenarios run field (LL-v2.1-P4-1)** — "Scenarios run" field in QA evidence logs should be explicit (list scenario IDs or state "manual only"). Applies to delivery_verification_prompt guidance. Owner: Head of Specs Team.

---

## §5 — Filing Confirmation

All 8 action items classified. 1 immediate action applied (with version bump). 7 deferred with owners and target cycles. 0 unreviewed items.

Filed by: PMO Lead
Date: 2026-03-21
