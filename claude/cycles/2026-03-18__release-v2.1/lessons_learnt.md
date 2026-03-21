**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-18

---

# Lessons Learnt — Release Planning Phase

**Phase:** Release Planning
**Cycle:** 2026-03-18__release-v2.1
**Filed:** 2026-03-18
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-03-17__release-v2.0 (lessons_learnt_closure.md)

---

## What Worked Well

- **No deferred patch carry-forward:** All 4 action-now items from v2.0 post-ship closure were confirmed in prompt_change_log.md before planning opened. Zero carry-forward obligations. Clean preflight.
- **Roadmap rebalance pre-work:** The 2026-03-18__item-4.3 rebalance cycle cleaned up stale ideas (19 disposed), added BLG-FR-01/02 to backlog, and corrected initiative_register.md — all before release planning opened. Release planning STEP 2 scope extraction was consequently clean with no surprise backlog state.
- **EPIC-01 as explicit prerequisite:** Modelling BLG-TECH-08 (ADR) as EPIC-01 with a sprint planning hard gate (Pre-sprint Required Decision) makes the Alerts gate explicit at the planning level rather than deferring the problem to sprint execution. This is the right pattern for architectural prerequisites.

---

## Friction Log

No friction items in this release planning cycle. STEP -1 through Publish Gate all passed cleanly.

---

## Prior Cycle Deferred Lessons Status

| Patch | Status |
|-------|--------|
| LL-v2.0-RP-1 (Spec authoring in Sprint 1 advisory) | Advisory only — no action required. Noted in prior cycle summary. No prompt change warranted. Confirmed closed. |

No OVERDUE items. No escalations from prior cycle.

---

## Deferred Patches (for next governance session)

None.

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-03-18__release-v2.1",
  "phase": "Release",
  "filed_utc": "2026-03-18T00:00:00Z",
  "friction_item_count": 0,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```

---

## Phase 3 — 2026-03-18__release-v2.1 (Sprint Execution)

| # | Area | Friction / Observation | Recommendation | Priority | Action taken this run |
|---|------|----------------------|----------------|----------|-----------------------|
| LL-v2.1-P3-1 | Branch strategy | EPIC-03 branch diverged far from main before all its content was needed on staging. Cherry-pick was required because the branch would have reverted EPIC-02/05/06 work on merge. | For future cycles where staging deployment is needed mid-sprint, consider committing directly to main on a feature flag, or ensuring EPIC branches are regularly rebased onto main after each EPIC merges. | P2 | Deviation recorded in execution_state; BLG-UX-01 filed as a staging observation. |
| LL-v2.1-P3-2 | Frontend tooling | Base44 used `@/` alias imports which do not resolve in this project. Every generated file required manual import path correction before integration. | Add a note to the Base44 prompt template requiring relative imports. Alternatively, if Base44 is retired, this friction disappears. | P2 | Frontend development guide created at docs/development/frontend_development_guide.md §3. |
| LL-v2.1-P3-3 | Delegation — frontend | Base44 was the delegated frontend tool. For ST-10 (watchlist UI), the engine implemented directly rather than generating a Base44 prompt first. User had to correct the process. | The `delegated_frontend` classification requires a Base44 prompt to be produced, not a direct implementation. Rule is in execution_prompt.md §5.1. Re-enforce on every frontend classification. | P2 | No prompt change needed — rule already documented. Engine should self-check on frontend classification. |
| LL-v2.1-P3-4 | Backend table creation | Watchlist backend (ST-09) was not included in the main branch cherry-pick that landed the frontend (ST-10). This caused staging to show "Unable to load watchlist" until manually identified and fixed. | When cherry-picking a frontend commit that depends on a backend commit, always cherry-pick both in the same operation. Add a dependency check to the cherry-pick workflow. | P2 | Fixed in session — cherry-picked dc856c1 to main. |
| LL-v2.1-P3-5 | Delegation log hygiene | Three delegation entries (ST-02, ST-13, ST-14) remained as `Pending` at sprint close despite the items being done. Sprint close was blocked until they were manually updated. | The execution engine should update delegation log status to `Unblocked` at the same time it marks an item `done` in execution_state. | P3 | Updated at STEP 5.0 of sprint close. |

---

## Phase 4 — 2026-03-18__release-v2.1 (Delivery Verification)

| # | Area | Friction / Observation | Recommendation | Priority | Action taken this run |
|---|------|----------------------|----------------|----------|-----------------------|
| LL-v2.1-P4-1 | Test scenario execution | notifications_scenarios.md was authored (ST-07) but not formally executed against staging and referenced in the QA evidence log. The scenarios existed but their execution status was ambiguous at verification. | When QA evidence is written, the "Scenarios run" field should explicitly list scenario IDs executed or state "manual acceptance review only — no scenario file." Do not leave the field blank when a scenario file exists. | P2 | TEST-GAP-EPIC-02 backlog item created. |
| LL-v2.1-P4-2 | Test coverage — new features | Watchlist (EPIC-03) and slippage tracking (ST-14) were delivered with no test scenario files. Both are core user journeys. | For any new feature delivering a core user journey, a test scenario file should be commissioned alongside (or immediately after) the DoQ sign-off, not deferred to post-ship verification. Consider adding "test scenario file exists or commissioned" as an explicit AC on frontend/backend stories involving new user-facing flows. | P2 | TEST-GAP-EPIC-03 and TEST-GAP-EPIC-05-SLIP backlog items created. |
| LL-v2.1-P4-3 | Execution state sealing | execution_state.json had `sealed: false` at verification preflight. The sprint close step set `status: Completed` but did not set `sealed: true`. | Add `sealed: true` and `sealed_utc` as explicit steps in the execution engine's STEP 5 sprint close sequence. The delivery verification preflight hard-gates on this field — it must be set before the cycle transitions to Sprint_Complete. | P3 | Fixed inline at verification preflight. |
