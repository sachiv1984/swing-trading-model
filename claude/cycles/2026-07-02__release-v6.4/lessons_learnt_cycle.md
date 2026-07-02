Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-02
Cycle: 2026-07-02__release-v6.4

---

# Lessons Learnt — 2026-07-02__release-v6.4

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-07-02__release-v6.4
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-02
**Reviewed by:** PMO Lead

### What went well

- All 13 stories delivered — zero items returned to backlog. All three EPICs (production correctness/security, audit remediation, Strategy Benchmark UX/QA) merged cleanly.
- `deviations_filed` and `qa_signed_off` atomic-write discipline held throughout the sprint — both flags were correctly set at story/EPIC completion time rather than requiring a batch correction at sprint close, resolving the v6.3 Phase 3 friction items (see Recurrence Notes).
- Three stories (ST-08, ST-09, ST-10) originally classified `delegated_frontend` were cleanly reclassified to `autonomous` per LL-v2.3-CL-01 before any delegation record was created — no delegation log entries were needed for this cycle at all.
- Agent-mediated sign-off resolved across four distinct domain authorities (Cybersecurity & Trust Lead x2, Head of UX & Design x2, Infrastructure & Operations Owner) with zero escalations to a human authority.
- Two CI-caught defects in ST-13's Playwright suite (nav route stubbing, collapsed Analytics nav group) were fixed pre-merge inside the same PR — 24/24 CI checks green at merge, no post-merge rework.
- Sign-off retry loop (§5.3) correctly caught and corrected two section-citation errors in ST-11's Infrastructure & Operations Owner review before clearing — the retry mechanism worked as designed.

### Friction Log

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| STEP 4's "on session resume — merge gate state sync" sub-step has no branch check of its own; a fresh session resuming after an EPIC merge can land on any exec/** branch, and the merge-gate sync write (execution_state.json) happened on the exec/EPIC-03 branch before the STEP 5 branch-ordering gate forced a switch to main — harmless here (branch had no further use) but the write was orphaned on a stale branch and had to be redone against main's post-merge file | Phase 3 | C | defer | Add an explicit branch check to STEP 4's resume-sync sub-step (mirroring STEP 5's branch-ordering gate) so merge-gate state syncs land on main directly, not on the EPIC branch being synced | Head of Specs Team | v6.5 |
| ST-07 commit split: a `git add` pathspec error caused the orphan-file deletion to land in a separate commit (5ab2ee2a) from the rest of the story's changes (5a52c02f); both carried the correct `[EPIC-02][ST-07]` tag so governance_sync.yml still closed the issue, but this is the kind of staging slip the commit-check skill exists to catch | Phase 3 | D | defer | Reinforce /commit-check to explicitly diff `git add`'s target list against the intended file set before committing multi-file governance changes | Head of Specs Team | v6.5 |
| ST-11 sign-off review found two section-citation errors (§19 mis-cited for a staging-404 precedent, §19.2 mis-cited for a regression-threshold methodology) in `api_performance_baseline.md` — both were root-caused to citing from memory rather than verifying section numbers against the actual document during authoring | Phase 3 | A | action-now | Corrected in-session during the Infrastructure & Operations Owner sign-off retry (1 retry) — §19→§4.2, §19.2→§22.2/§22.3; no further action needed | Infrastructure & Operations Owner | — |

**Recurrence Notes:**
- v6.3 Phase 3 friction item 1 (`deviations_filed` not set atomically, requiring batch correction at sprint close, target v6.4): **Resolved — not a recurrence.** All `done` stories in this cycle had `deviations_filed = true` set at the time of their own deviation check; no batch correction was needed at STEP 5.1.
- v6.3 Phase 3 friction item 2 (`qa_signed_off` not set atomically, target v6.4): **Resolved — not a recurrence.** All three EPICs had `qa_signed_off = true` recorded at EPIC completion time, confirmed present before this session began.
- v6.3 Phase 3 friction item 3 (sprint close batch correction overhead, downstream of items 1/2, target v6.4): **Resolved — not a recurrence.** Sprint close required no deviations_filed/qa_signed_off corrections; the only sprint-close-time correction needed was the merge-gate `pr_status`/`epics_pending` resync for EPIC-03, which is a distinct, expected mechanism (LL-v3.9-P3-1), not a recurrence of the v6.3 items.
- New friction items 1–3 above are first-time captures for this cycle — no prior-cycle match found in `claude/cycles/2026-06-26__release-v6.3/lessons_learnt_cycle.md` `## Phase 3`.

---
