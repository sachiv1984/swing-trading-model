Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-28
Cycle: 2026-05-27__release-v4.2

---

# Lessons Learnt — 2026-05-27__release-v4.2

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-05-27__release-v4.2
**Section anchor:** `## Phase 3`
**Filed:** 2026-05-28
**Reviewed by:** PMO Lead
**Prior cycle Phase 3 checked:** claude/cycles/2026-05-26__release-v4.1/lessons_learnt_cycle.md — found.

**Prior cycle deferred items check:**
- v4.1 deferred item 1 — null pr_number recovery: **RESOLVED** in v4.1→v4.2. execution_prompt.md v3.29→v3.30 (AUD-2026-05-27-002) added STEP 5.0A Step 1 null pr_number recovery via `gh pr list --search`. This cycle, EPIC-01 pr_status sync was handled by STEP 4 merge gate sync (LL-v3.9-P3-1 via gh pr view), and EPIC-02 pr_number=525 was recovered via git fetch/log at session resume. Recovery path working — no manual intervention required.
- v4.1 deferred item 2 — STEP 5.2 returned_to_backlog in-flight: **RESOLVED** in v4.1→v4.2. execution_prompt.md v3.28→v3.29 (AUD-2026-05-27-003) added the in-flight transition note to STEP 5.2. Validated as a documented pattern; no further action required.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| EPIC-01 and EPIC-02 both merged via GitHub UI between sessions — execution_state.json qa_signed_off and pr_status were stale at resume. STEP 4 merge gate sync (LL-v3.9-P3-1) detected EPIC-01 already merged via gh pr view; EPIC-02 discovered via git fetch showing origin/main had advanced by PR #525. Both recovery paths successful. This is the expected pattern with v3.30's STEP 5.0A guard active. | Phase 3 | E | action-now | Positive: merge gate resume + STEP 5.0A guard working as designed. No action required — document as validated pattern for v4.2. | Sprint Execution Engine | — |
| execution_state.json qa_signed_off field for EPIC-02 was false at session start despite qa_evidence_EPIC-02.md (commit 9090175f) having been committed in a prior session with DoQ sign-off. The field was not updated when the QA evidence was committed. Minor state sync gap. | Phase 3 | C | defer | Add advisory to execution_prompt.md STEP 3.2.A: after creating qa_evidence_EPIC-xx.md and completing DoQ sign-off, update execution_state.json `qa_signed_off: true` in the same commit as the QA evidence file. Currently only enforced as a pre-condition check at STEP 3.2.B and STEP 4, but not as an immediate post-write rule. | Head of Specs Team | v4.3 |
| All 6 delegated items (DEL-20260528-01 through 06) resolved cleanly without retry or escalation — agent-mediated sign-off worked for 8 of 13 stories. Highest delegation density sprint to date with 0 sign-off retries. | Phase 3 | E | action-now | Positive: agent-mediated sign-off remains reliable for governance, ops, and spec review items when criteria are well-defined. Confidence in autonomous class for operational baselines. No change needed. | Sprint Execution Engine | — |
| Branch safety check gap: sprint close artefacts (sprint_close.md, System_status_report.md, lessons_learnt_cycle.md) committed on EPIC-02 exec branch rather than main. STEP 8 of execution_prompt.md does not include a branch safety check — execution can land on any active EPIC branch at sprint close. delivery_verification_prompt.md and post_ship_closure.md have branch safety gates (v2.8, v2.12) but execution_prompt.md STEP 8 does not. | Phase 3 | A | defer | Add branch safety advisory to execution_prompt.md STEP 5.3/STEP 8: if current branch is an exec branch, advise that sprint close artefacts should land on a governance commit to main (or note that the [GOVERNANCE] commit from STEP 8 serves as the closing record). Alternatively, gate STEP 8 commit to require switching to main. Consult Head of Specs Team on preferred resolution. | Head of Specs Team | v4.3 |

**Recurrence Notes:**
- **EPIC PR merged between sessions:** Third occurrence (v4.0 EPIC-02, v4.1 EPIC-03, v4.2 EPIC-01+EPIC-02). However, all three v4.2 EPICs-pending were recovered correctly by the STEP 5.0A guard and merge gate sync — the pattern is now handled. No carry-forward needed.
- **qa_signed_off stale state:** New item this cycle; classified defer to v4.3.
- **Branch safety at sprint close:** New item this cycle; classified defer to v4.3.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-05-27__release-v4.2
**Section anchor:** `## Phase 4`
**Filed:** 2026-05-29
**Reviewed by:** PMO Lead
**Prior cycle Phase 4 checked:** claude/cycles/2026-05-26__release-v4.1/lessons_learnt_cycle.md — found.

**Prior cycle Phase 4 deferred items check:**
- v4.1 Phase 4: All items were `action-now` positive patterns — no deferred patches outstanding. Zero carry-forward items from v4.1 Phase 4.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Zero spec deviations, zero QA Fail results, 13/13 stories done. All ACs verified by document review, code inspection, and live environment measurement. Governance/ops/documentation sprint with no frontend changes — delivery verification completed in a single pass with no escalations. | Phase 4 | E | action-now | Positive: cleanest sprint to date by deviation and QA metrics. Governance/ops scope with well-defined ACs and pre-cleared delegation records is the most reliable delivery pattern. No process change needed. | Sprint Execution Engine | — |
| QA evidence AC numbering consolidation: ST-11 (4 backlog ACs → 3 evidence rows, sign-off in separate section) and ST-13 (5 backlog ACs → 3 evidence rows, sub-items merged). All substantive criteria were met — notation difference only, no scope reduction. However, this created a minor verification cross-reference friction. | Phase 4 | B | defer | Add advisory to qa_evidence_template.md: evidence table rows should map 1:1 to backlog slice ACs. Where consolidation occurs, note which backlog ACs are covered in the evidence row. This prevents traceability cross-reference friction at verification. | Head of Specs Team | v4.3 |
| Phase 3 deferred items (qa_signed_off stale state + branch safety at sprint close) both filed for v4.3. Delivery verification completed same session as sprint close resolution — no coordination friction between DoQ and PO roles. | Phase 4 | E | action-now | Positive: deferred Phase 3 items correctly filed; no recurrence escalations triggered. Verification sign-off coordination friction: none (all agent-mediated for governance-class sprint). No process change needed. | Sprint Execution Engine | — |

**Recurrence Notes:**
- No recurrence items identified. All Phase 4 patterns are either positive (action-now) or new items (defer to v4.3).
- v4.1 deferred items: none — all were action-now positive patterns in v4.1.
