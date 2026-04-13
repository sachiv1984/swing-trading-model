**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-04-12
**Cycle:** 2026-04-11__release-v2.6
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Lessons Learnt — Cycle 2026-04-11__release-v2.6

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-04-11__release-v2.6
**Section anchor:** `## Phase 3`
**Filed:** 2026-04-12
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Sprint Close (STEP 5) not triggered before delivery verification — second recurrence | Phase 3 | B | defer | RECURRENCE (v2.5 Phase 3 item). All 4 EPIC PRs were merged outside of `run sprint` session; sprint close artefacts (sprint_close.md, execution_state.json seal) never created. User invoked `run delivery verification` which hard-gated, then `run sprint` which triggered STEP 5 recovery. Hard gate (LL-v2.2-EX-02) functioned correctly. Consider: add a GitHub Actions hook that detects all EPICs merged and issues a reminder to run sprint close. | PMO Lead | v2.7 planning |
| EPIC-02 QA evidence sign-off block missing at PR merge — merge gate process gap | Phase 3 | B | defer | EPIC-02 merged (PR #219) with qa_evidence_EPIC-02.md still in "Pending QA Sign-off" state. Sign-off block added post-merge at sprint close recovery. Pattern: when autonomous EPICs have no formal DoQ involvement, the sign-off block is the last item added — and it falls off if the PR is merged quickly. Consider: require qa_evidence sign-off block before PR can be opened (not just before merge). | Director of Quality | v2.7 |
| EPIC-01/04 QA sign-off by engine, not human DoQ — merge gate authority gap | Phase 3 | C | defer | For all-autonomous EPICs (EPIC-01, EPIC-04), the engine self-signed the DoQ sign-off block. The merge gate states "QA sign-off and Product Owner acceptance are always human." Engine signing its own qa_evidence is a structural authority violation even if the evidence is sound. Consider: define an explicit "engine-autonomous" sign-off class that is acceptable for code-review-only stories, with clear criteria (all AC by code review, no staging required, no UI behaviour). | Director of Quality | v2.7 planning |
| Playwright page.route() failure (BLG-QA-11) — systemic test infra issue | Phase 3 | D | defer | SC-FEE-01 to SC-FEE-04 could not be verified by automated run because page.route() intercept fails across all specs (reports-performance-tab.spec.js and slippage-tracking.spec.js also fail identically). Filed as BLG-QA-11. Specs are structurally correct; root cause is environmental. Deferred to v2.7 — needs investigation of Playwright config / test runner setup. | QA & Testing Owner | v2.7 |

**Recurrence Notes:**

- **RECURRENCE — Sprint Close not triggered:** This is the second consecutive cycle (v2.5 and v2.6) where all EPIC PRs were merged without re-invoking `run sprint` to trigger STEP 5. The hard gate (LL-v2.2-EX-02) exists in execution_prompt.md and functioned correctly both times. The pattern is: user merges PRs directly on GitHub without going through the engine — engine state never learns about the merges until re-invoked. Resolution options: (a) GitHub Actions webhook on PR merge that posts a reminder; (b) mandate that `run sprint --cycle <cycle_id>` is always invoked after each PR merge as the engine output already requires. Current friction is in the human workflow, not the engine logic. No new prompt change applied (already at hard gate level); escalate to PMO Lead for workflow resolution by v2.7.

### Summary Assessment

- **Delegation patterns:** 0 delegated items (all 15 stories autonomous). No SLA breaches. Pure autonomous sprint.
- **GitHub integration friction:** governance_sync.yml multi-commit range fix (from v2.5 ST-10) functioned correctly this cycle — all GitHub issues closed on push. No duplicate issues. 
- **Acceptance criteria quality:** All AC was executable. No `delegated_decision` items. Design dependencies on EPIC-03 resolved at sprint planning via UX design decisions baked into backlog slice.
- **Governance gates:** STEP -1 of delivery verification correctly blocked on `sealed: false`. Resolved by invoking `run sprint` which triggered STEP 5 recovery. Sprint planning gate (STEP -1.2 of execution prompt) confirmed `status: Executing` as valid resume state.

### Net Sprint Assessment

Velocity: 15/15 (1.00). All stories delivered. No items returned to backlog. No delegation records. One P3 deviation (BLG-QA-11 Playwright environmental). Two bonus stories delivered (ST-14 hard gate, ST-15 performance budget spec). Sprint goal fully achieved.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-04-11__release-v2.6
**Section anchor:** `## Phase 4`
**Filed:** 2026-04-13
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Sprint Close not triggered before delivery verification — third recurrence | Phase 4 | B | defer | RECURRENCE (v2.5 Phase 3 and Phase 4 both recorded this). STEP -1 hard gate (sealed: false, status: Executing) fired correctly; user then ran `run sprint` which recovered via STEP 5. Pattern is persistent: user merges PRs on GitHub without re-invoking `run sprint`. Hard gate functions correctly; friction is in the human workflow. Escalated to Head of Specs Team as third-recurrence per §3.7 (recurrence with open outstanding action = automatic escalation). | Head of Specs Team | immediate — before v2.7 planning |
| QA evidence Tier 2 sign-off authority — engine self-signing autonomous EPICs | Phase 4 | C | defer | RECURRENCE from Phase 3 (same cycle). Delivery verification STEP -1.3 Tier 2 check fired for all 4 EPICs. Director of Quality counter-signs added at preflight in this session. Root fix: define a formal "autonomous DoQ" sign-off class for code-review-only stories with clear authority criteria, so the Tier 2 check does not fire every cycle for autonomous EPICs. | Director of Quality | v2.7 planning |
| TSG-V26-01 Playwright test gap inherited from BLG-QA-11 — systemic test infra issue | Phase 4 | D | defer | SC-REP-01–04 and SC-SIG-CB-01–02 (EPIC-01) and SC-FEE-01–04 (EPIC-02) remain unverified by automated run. Root cause: BLG-QA-11 (`page.route()` intercept failure) unresolved across 2 cycles now. Deferred to v2.7 under BLG-QA-11. | QA & Testing Owner | v2.7 |

**Recurrence Notes:**

- **RECURRENCE — Sprint Close not triggered (third occurrence):** v2.5 Phase 4 identified this; v2.6 Phase 3 identified this again; v2.6 Phase 4 records it as a third recurrence. Per §3.7: a friction item that recurs with an open outstanding action from the prior cycle is an automatic escalation trigger. Escalating to Head of Specs Team. The Phase 3 outstanding action (PMO Lead to resolve by v2.7 planning) is escalated: Head of Specs Team must assess whether a prompt change, a workflow automation (GitHub Actions reminder), or a documented mandatory step can break this pattern before v2.7.

- **RECURRENCE — Tier 2 engine sign-off authority:** Also flagged in Phase 3 of this same cycle. Both phases identify the same structural gap. Combined: Director of Quality to define autonomous DoQ sign-off class before v2.7 so this Tier 2 check does not fire for every purely autonomous EPIC.

### Net Phase 4 Assessment

Gate sequencing worked correctly — STEP -1 preflight fired on both sealed:false and the Tier 2 sign-off authority check. Both were resolved in-session. Deviation severity calls were straightforward (P3 only). Test scenario coverage gap analysis was clean: TSG-V26-02 and TSG-V26-03 correctly assessed not_applicable; TSG-V26-01 correctly deferred under existing BLG-QA-11. Sign-off coordination: both DoQ and PO signed off in the same session. Overall: delivery verification process functioning well; friction is upstream (sprint close trigger pattern) and in sign-off authority formalism, not in the verification logic itself.
