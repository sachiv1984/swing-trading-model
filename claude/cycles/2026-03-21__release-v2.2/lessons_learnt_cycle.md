Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-03-24
Cycle: 2026-03-21__release-v2.2

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-03-21__release-v2.2
**Section anchor:** `## Phase 3`
**Filed:** 2026-03-24
**Reviewed by:** PMO Lead

**Cross-cycle recurrence check:** Prior cycle `2026-03-18__release-v2.1` lessons_learnt_cycle.md — no file found. Recurrence check not possible.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Delegation log entries not updated in-flight — all 10 entries remained "Pending" until sprint close, requiring bulk update at STEP 5.0 | Phase 3 | A | defer | Add explicit "update delegation log entry status to Unblocked" substep to execution_prompt.md STEP 3.1.A after merge confirmation — prevents bulk rework at sprint close | Head of Specs Team | 2026-03-21__release-v2.3 |
| ST-13/14/15 entered sprint as blocked_decision with no HoST design authored — required full design sessions (HoST + Challenger) before implementation, adding session overhead mid-sprint | Phase 3 | C | defer | Consider adding sprint planning gate or advisory note in sprint_planning_prompt.md when blocked_decision items are scheduled: "HoST design session should precede sprint start for delegated_decision items to reduce mid-sprint overhead" | Head of Specs Team | 2026-03-21__release-v2.3 |
| Sprint close (STEP 5) not triggered after all EPICs merged — delivery verification invoked directly, causing STEP -1.1 hard gate on execution_state.json.sealed=false | Phase 3 | C | defer | Add advisory note to execution_prompt.md STEP 4 merge gate completion block: "When merge_gate.all_merged=true, STEP 5 Sprint Close must be invoked in the same session before delivery verification can proceed" — prevents the common pattern of going straight to delivery verification | Head of Specs Team | 2026-03-21__release-v2.3 |
| DEV-EPIC02-ST05-02: ST-05 backend commits landed on main rather than EPIC-02 branch — P2 process deviation, no functional impact but indicates merge-order discipline gap | Phase 3 | A | defer | Reinforce branch discipline note in execution_prompt.md §3.1.A or §9 invariants: delegated_backend commits that are tightly coupled to a delegated_frontend item should be coordinated on the same EPIC branch unless specifically authorised as a direct-to-main commit | Head of Specs Team | 2026-03-21__release-v2.3 |

**Recurrence Notes:** None. No prior cycle file — recurrence check not possible.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-03-21__release-v2.2
**Section anchor:** `## Phase 4`
**Filed:** 2026-03-24
**Reviewed by:** PMO Lead

**Cross-cycle recurrence check:** Prior cycle `2026-03-18__release-v2.1` lessons_learnt_cycle.md — no file found. Recurrence check not possible.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| TEST-GAP-007 P1 flag in qa_evidence (ST-12) was already resolved by ST-05 by sprint close — the traceability matrix was authored before ST-05 backend was complete, creating a timing gap in evidence | Phase 4 | B | defer | Add advisory note in execution_prompt.md STEP 3.1.A: when a test gap is identified in a delegated_qa item and the corresponding implementation story is not yet done, the QA evidence should note "pending ST-xx completion" rather than flagging as a P1 gap — this prevents false P1s at delivery verification | Head of Specs Team | 2026-03-21__release-v2.3 |
| ST-02 and ST-11 spec_references fields empty (traceability gaps) — for autonomous items that produce no spec reference (CSP, readiness doc), traceability check fires a flag even when expected | Phase 4 | A | defer | Add note to execution_prompt.md §9.1 schema: for delegated_qa documentation artefacts and autonomous infrastructure items with no prior spec, spec_references may be left empty with a note field value of "no prior spec applicable" — this prevents traceability gap flags for expected cases | Head of Specs Team | 2026-03-21__release-v2.3 |
| DEV-EPIC02-ST05-02 (P2 process deviation): backend commits for a delegated_frontend story went directly to main — required P2 acceptance and backlog item at verification | Phase 4 | A | defer | BLG-GOV-07 filed: reinforce branch discipline in execution_prompt.md §9 invariants (see lessons_learnt Phase 3 row 4) | Head of Specs Team | 2026-03-21__release-v2.3 |

**Recurrence Notes:** None. No prior cycle Phase 4 file — recurrence check not possible.
