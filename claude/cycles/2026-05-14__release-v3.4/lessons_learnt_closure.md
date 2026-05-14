Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-14
Cycle: 2026-05-14__release-v3.4

---

# Lessons Learnt Closure Record — 2026-05-14__release-v3.4

**Invoking routine:** post_ship_closure.md v2.6
**Phase:** Post-Ship
**Cycle:** 2026-05-14__release-v3.4
**Prior cycle checked:** 2026-05-09__release-v3.3 (lessons_learnt_closure.md present — recurrence check complete)

---

## Records Reviewed

| Record | Location | Status |
|--------|----------|--------|
| Release Planning lessons | claude/cycles/2026-05-14__release-v3.4/lessons_learnt.md | Read |
| Phase 3 (Sprint Execution) | claude/cycles/2026-05-14__release-v3.4/lessons_learnt_cycle.md §Phase 3 | Read |
| Phase 4 (Delivery Verification) | claude/cycles/2026-05-14__release-v3.4/lessons_learnt_cycle.md §Phase 4 | Read |
| Amendment sections | N/A — no amendments this cycle | N/A |

---

## Closure-Phase Observations

1. **Document location (scope + decisions):** Both the scope document and decisions record were located at their canonical paths on first read. No friction.
2. **Deviation compliance:** trade_plan.md Known Deviations table used an older format (`| ID | Description | Priority | Status |`) rather than the full §3 Known Deviation Standard schema. The DEV-v3.4-01 row was missing Canonical requirement, Target resolution, and Owner as separate columns. Corrected at STEP 5 (standard mode — fields added, table header updated). No hard gate fired. Notification to document owner (Frontend Specifications & UX Documentation Owner) noted in closure record §6.
3. **Test gap resolution:** TSG-v33-01 and TSG-v33-02 (v3.3 open items) were fully resolved by v3.4 EPIC-01 delivery. Specs Index updated.
4. **Endpoint coverage drift:** 2 new endpoints (GET /portfolio/drawdown-status, GET /portfolio/concentration-status) absent from api_performance_baseline.md. BLG-OPS-13 updated to include them. `/portfolio` prefix already handled in categorizeEndpoint() — no new prefix flag needed.
5. **Velocity:** v3.4 achieved 1.00 (14/14). Rolling 6-cycle average updated to 0.97 (v2.9–v3.4).

---

## Consolidated Action Summary

### Immediate Actions Applied: 1

| # | Action | Document | Version | Applied by |
|---|--------|----------|---------|-----------|
| 1 | CLAUDE.md §2 — added co-update rule: when updating SystemStatus.js `totalTests \|\| 'N'` fallback, also update SC-SS-01b in system-status.spec.js in same commit | CLAUDE.md | N/A (runtime config) | Head of Specs Team (action-now, Phase 3 execution session) |

*Note: This action-now was applied during the sprint execution phase (not this post-ship run), as documented in lessons_learnt_cycle.md Phase 3 item #2 and prompt_change_log.md. Recorded here for completeness.*

---

### Deferred to Next Cycle (v3.5): 7

| # | Action | Source | Owner | Target |
|---|--------|--------|-------|--------|
| 1 | BLG-GOV-22: Update sprint_planning_prompt.md with shared execution_state.json ownership rule (first EPIC branch creates; others check for existence before creating) | LL Phase 3 item #1 (recurrence) | Head of Specs Team | v3.5 |
| 2 | BLG-GOV-22: sprint_backlog.md template — note merge order and shared file ownership for shared pages (e.g. Positions.js) | LL Phase 3 item #4 | Head of Specs Team | v3.5 |
| 3 | execution_prompt.md §3.1.A step 10 — add advisory: before filing a deviation, verify implementation matches spec intent (not just literal draft wording); if spec and implementation agree, record as implementation note only | LL Phase 4 item #2 (over-filing) | Head of Specs Team | v3.5 |
| 4 | execution_prompt.md §3.1.A step 10 — add advisory: when filing a deviation, also add Known Deviations section to the canonical spec in the same commit (shift work to execution time, reduce verification overhead) | LL Phase 4 item #6 | Head of Specs Team | v3.5 |
| 5 | execution_prompt.md or lessons_learnt_prompt.md §3.3 — add ID uniqueness check: before filing new backlog IDs in lessons_learnt Phase 3, verify ID is unoccupied in backlog.md | LL Phase 4 item #1 (BLG-GOV-21 ID conflict) | Head of Specs Team | v3.5 |
| 6 | LL-v3.3 CF-01: sprint_close "Deviations Filed" table priority must match DoQ assessment (deviation severity consistency check) | LL Release Planning carry-forward item 1 | Head of Specs Team | v3.5 |
| 7 | LL-v3.3 CF-02: Protocol checkbox verification — sprint_close check for "backlog item filed" completeness | LL Release Planning carry-forward item 2 | PMO Lead | v3.5 |

---

### Escalated for Decision: 0

None.

---

## Recurrence Check

**Prior cycle (v3.3) lessons_learnt_closure.md checked:** Present.

- Cross-EPIC merge conflict (execution_state.json + shared pages): **Recurrence** from v3.3 Phase 3. BLG-GOV-22 filed as backlog item; deferred to v3.5 per prior cycle disposition. No escalation triggered (still within one-cycle deferral; not 2+ cycles unchecked).
- Deviation severity consistency: **NOT RECURRED** ✅ (v3.4 all deviations P3, no contest between sprint_close and DoQ).
- Known Deviations sync: Pattern noted (v3.4 first occurrence); deferred to v3.5.

---

## Carry-Forward

| # | Description | Target | Owner | Notes |
|---|-------------|--------|-------|-------|
| 1 | BLG-GOV-22 — sprint_planning_prompt.md shared execution_state.json ownership rule | v3.5 | Head of Specs Team | P2 backlog item filed |
| 2 | execution_prompt.md over-filing deviation guidance | v3.5 | Head of Specs Team | Per LL Phase 4 item #2 |
| 3 | execution_prompt.md Known Deviations advisory at implementation time | v3.5 | Head of Specs Team | Per LL Phase 4 item #6 |
| 4 | ID uniqueness check before filing backlog IDs in lessons_learnt | v3.5 | Head of Specs Team | Per LL Phase 4 item #1 |
| 5 | LL-v3.3 CF-01 (deviation priority consistency) | v3.5 | Head of Specs Team | 2nd carry-forward; still within cadence |
| 6 | LL-v3.3 CF-02 (protocol backlog-item checkbox) | v3.5 | PMO Lead | 2nd carry-forward; still within cadence |
