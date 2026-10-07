Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-07
Cycle: 2026-10-06__release-v9.10

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-10-06__release-v9.10
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-10-07
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-09-30__release-v9.9 (`lessons_learnt_cycle.md` `## Phase 3`). It filed 3 friction items. Each was re-checked against `prompt_change_log.md` as of this run, by patch ID and by reading the named target file directly:
1. **Cross-EPIC commits merged through one PR (`BLG-GOV-368`).** **Applied:** `execution_prompt.md` v3.81→v3.82 (2026-10-06, `LL-v9.9-P3-01`, `prompt_change_log.md` row dated 2026-10-06). The new §3.2.B pre-PR check ran for PR #1918 and found no foreign commits. No cross-EPIC commit reached `main` this cycle. **Resolved; not a recurrence.**
2. **`claude/roadmap/*` / existing-`backlog.md`-item write-scope boundary (`BLG-GOV-362`).** It was escalated at v9.9. The Head of Specs Team gave a named-file ruling at Sprint Planning (`ESC-CLOSE-20261006-01`), so ST-20's `current_roadmap.md` edit went ahead without a mid-sprint halt and the boundary did not fire this cycle. However, the prompt patches (the `execution_prompt.md` §7 named-file exception and the `sprint_planning_prompt.md` pre-seal check) are still unapplied. `prompt_change_log.md` has no `BLG-GOV-362` row, and `execution_prompt.md` §7 still carves out only `workforce_capacity.md`. That makes this a deferred patch carried 2 cycles (v9.8 → v9.9 → v9.10) without a change-log entry, so it is escalated again under §3.7 (Recurrence Escalations below).
3. **Escalation SLA breaches went unseen between sessions.** The deferred patch (`shared_standards.md` §16.4.1 scheduled reminder) targets the next lifecycle audit at cycle count 87; the count is 86 now, so it is not yet due. All six escalations this cycle were resolved before their SLA. **Not a recurrence.**

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| ST-18's live fire depended on `staging-smoke-test.yml`, which had failed at its env check on all 126 prior runs because the `STAGING_API_URL` secret was never set. The delegation (DEL-20261006-03) was raised without checking that the workflow could run at all. The first real run then produced a false-positive `STALE STAGING DEPLOY`, because the check compared staging against `main`'s tip and a governance-only commit never redeploys staging. Blast radius: 1 story (ST-18) blocked ~18h, with 1 out-of-sprint P1 ops fix (BLG-OPS-180) and 1 in-story code fix (`23c6810f`); recovery cost was 1 session; propagation path is a Human-Delegation live-fire AC → a workflow that was already broken. | Phase 3 | Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced | defer | `execution_prompt.md` §3.1.B (delegated items): before raising a Human-Delegation record for a live-fire or workflow-dispatch AC, run `gh run list --workflow <file> --limit 10` and record the workflow's last successful run in the delegation record. If it has no recent success, raise the prerequisite fix as part of the same delegation. Ops follow-ups: BLG-OPS-180, BLG-OPS-181, BLG-OPS-182. | Head of Specs Team | Post-ship closure `2026-10-06__release-v9.10` STEP 8 |
| The EPIC-04 consolidated QA evidence graded ST-18 and ST-20 as `Pass` even though each row's own AC column recorded a narrowed AC (ST-18 AC 1) or a partly-met AC (ST-20 AC 2). The agent-mediated DoQ pass returned Blocked on that basis. `Pass_with_deviation` has existed in `qa_evidence_template.md` since v1.13, but STEP 3.2.A has no self-check that applies it before sign-off is requested. Blast radius: 2 stories, 1 extra DoQ review round (~15 min); propagation path is consolidation → DoQ sign-off. Had the DoQ pass missed it, the over-statement would have reached delivery verification. | Phase 3 | Type A — Governance Drift: A rule existed but was not applied | defer | `execution_prompt.md` §3.2.A (EPIC consolidation): before requesting DoQ sign-off, scan every evidence row. Any row whose AC column records a narrowed, partly-met or not-met AC must be graded `Pass_with_deviation` (or `Fail`), and its `Deviations` cell must name the tracking BLG ID. | Head of Specs Team | Post-ship closure `2026-10-06__release-v9.10` STEP 8 |
| ST-19 added Reports and Notifications to the axe scan, but its own new test failed (`scrollable-region-focusable`) on every EPIC-04 code commit. The failure was found only at the STEP 3.2.A real-CI check, after all 7 stories were already marked `done`. Playwright runs only in CI, and §3.1.A does not require checking the branch's CI result on a story's commit before marking a Playwright-bearing story `done`. Blast radius: 1 story and 1 fix commit (`b8ced55f`) before the PR could open; recovery cost was low; propagation path is story `done` → EPIC consolidation. The backstop worked as designed. | Phase 3 | Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced | defer | `execution_prompt.md` §3.1.A (autonomous items): when a story adds or changes a Playwright spec, record the branch's Playwright workflow conclusion for the story's commit (`gh run list --branch <branch> --workflow playwright.yml --limit 1`) before setting `done`. If the run is still pending, set `done` with a `ci_pending` note that STEP 3.2.A must clear. | Head of Specs Team | Post-ship closure `2026-10-06__release-v9.10` STEP 8 |

**Recurrence Notes:**
The v9.9 Friction Item 2 deferred patch (`BLG-GOV-362`) is a §3.7 recurrence escalation. It has been carried 2 cycles with no `prompt_change_log.md` entry, though the boundary itself did not fire this cycle because of the Sprint Planning ruling. All three friction items above are new this cycle. The v9.9 Friction Item 1 (`BLG-GOV-368`) is resolved by `execution_prompt.md` v3.82 and was exercised at PR #1918. The v9.9 Friction Item 3 is not yet due.

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|-----------------|---------------------------|---------------|
| `claude/roadmap/*` / existing-`backlog.md`-item write-scope boundary needs a per-story or per-cycle ruling whenever a sealed AC names such a file | 2026-09-28__release-v9.8 (earlier single instances at v9.7 and v8.5, per `BLG-GOV-362`) | Ruling given (`ESC-CLOSE-20261006-01`, named-file ruling, 2026-10-06), but the `BLG-GOV-362` prompt patches (`execution_prompt.md` §7 exception; `sprint_planning_prompt.md` pre-seal check) are still unapplied after 2 carries. The Sprint Planning outstanding action "Ship `BLG-GOV-362` prompt patches" has no target date | Head of Specs Team |

---
