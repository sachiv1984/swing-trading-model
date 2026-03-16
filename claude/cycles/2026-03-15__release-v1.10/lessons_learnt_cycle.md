Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-03-16
Cycle: 2026-03-15__release-v1.10

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-03-15__release-v1.10
**Section anchor:** `## Phase 3`
**Filed:** 2026-03-16
**Reviewed by:** PMO Lead

**Recurrence check:** Prior cycle Phase 3 file: `claude/cycles/2026-03-06__release-v1.9/lessons_learnt_execution.md` — loaded. Prior outstanding patches confirmed resolved (v1.6 re-invocation reminder applied, merge conflict pattern noted).

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Sprint close not triggered after final EPIC merge — `run delivery verification` failed STEP -1 preflight because `execution_state.json.sealed = false` and status = `Executing`. Re-invocation reminder in execution_prompt.md v1.6 STEP 4 exists but did not prevent gap. | Phase 3 | D | defer | Strengthen delivery_verification_prompt.md STEP -1 halt output: when `sealed = false`, include explicit resolution path (`run sprint --cycle <cycle_id>` triggers STEP 5 sprint close). Currently the halt message (shared_standards.md format) does not include this path. | PMO Lead | 2026-03-15__release-v1.10 post-ship or next cycle |
| BLG-API-01 acceptance criteria referenced `GET /portfolio/prospective-heat` endpoint that does not exist in `portfolio_endpoints.md` or backend. ST-05 implementation could not satisfy this AC; P3 deviation DEV-ST05-01 filed. | Phase 3 | B | defer | Backlog item authoring process should cross-check endpoint names against current spec before item is promoted to sprint. Add check note to backlog management prompt §3 item authoring gate: "verify all endpoint references exist in the canonical spec file before adding to sprint scope". | PMO Lead | next `groom backlog` run |
| ST-04 originally classified `delegated_frontend` in sprint backlog; reclassified `autonomous` on PO authority because no UX change was involved (pure data-fetching swap). Reclassification was smooth but reflects conservative initial classification. | Phase 3 | E | defer | Sprint planning engine classification heuristic: if item description is "refactor component X to call backend endpoint Y" with no UX change and the API method already exists client-side, classify as `autonomous` candidate. Add to sprint_planning_prompt.md §5 classification table as a pattern note. | PMO Lead | next sprint planning run touching similar items |

**Recurrence Notes:**
- **Friction item 1 (sprint close re-invocation gap)** is a recurrence of EX-LL-04 from `2026-03-04__release-v1.8`. The prior outstanding action (add re-invocation reminder to STEP 4) was applied and marked Resolved in v1.6. The patch is insufficient — the reminder appears in STEP 4 output (each EPIC merge) but the gap still occurs when the user proceeds directly to `run delivery verification` after the final merge. New deferred patch targets the verification preflight halt output to include explicit resolution path.
- Friction items 2 and 3: No prior recurrence found in prior cycle Phase 3 file.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-03-15__release-v1.10
**Section anchor:** `## Phase 4`
**Filed:** 2026-03-16
**Reviewed by:** PMO Lead

**Recurrence check:** Prior cycle Phase 4 file: `claude/cycles/2026-03-06__release-v1.9/lessons_learnt_cycle.md` — file does not exist (prior cycle used standalone file format pre-IMP-28). Recurrence check not possible from Phase 4 perspective; prior cycle Phase 4 findings are in `lessons_learnt.md` (release planning) — not directly comparable.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| EPIC-02 QA evidence AC table showed "Awaiting QA" / "Pending" on two rows after DoQ had signed off the sign-off block. Sign-off block and AC table were not updated in sync. | Phase 4 | A | defer | Add note to qa_evidence template (execution_prompt.md §qa_evidence template or OPERATIONAL_GUIDE.md §8 qa_evidence authoring): "When completing the sign-off block, update all AC table rows from Pending/Awaiting to Pass or Pass with notes in the same edit." | PMO Lead | next `run sprint` run |
| DEV-ST05-01 was filed in qa_evidence_EPIC-03.md rather than in the canonical spec file. execution_prompt §3.1.A step 10 requires deviations filed in the spec file, but the deviation described an endpoint *absent* from the spec — filing in the spec was semantically ambiguous. | Phase 4 | B | defer | Add clarifying rule to execution_prompt.md §3.1.A step 10 (deviation filing): "If the deviation is 'endpoint/feature absent from spec', file in qa_evidence and backlog only — the spec is not the right home for an absence note. If the deviation is 'implementation differs from what spec requires', file in the spec." | PMO Lead | next `run sprint` run |
| GAP-04 scenario (holding_days in GET /trades) could not be executed on staging because staging has 0 closed trades. Scenario validity is confirmed but staging test data gap blocked execution, leaving an open scenario. | Phase 4 | C | defer | Add a staging test data checklist item to the DoQ sign-off template in OPERATIONAL_GUIDE.md §8.2: before executing backend data-dependent scenarios, confirm staging DB has at least one closed trade and at least one open position. | PMO Lead | next `run sprint` run or `run delivery verification` run |

**Recurrence Notes:**
None from prior Phase 4 file (file not available — pre-IMP-28 format).
