Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-20
Cycle: 2026-07-20__release-v7.6

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-07-20__release-v7.6
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-20
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| API performance baseline advisory (AUD-2026-06-22-006) missed for a new endpoint (`GET /ai/monthly-cost`, EPIC-07/ST-07) — `openapi.yaml` updated but the companion `docs/ops/api_performance_baseline.md` row was forgotten across an 8-file endpoint addition, caught only by the ST-12 CI gate after PR #1035 was already open | Phase 3 | D | action-now | New "API performance baseline pre-PR check (LL-v7.6-P3-01)" added to `execution_prompt.md` STEP 3.2.B (v3.57→v3.58) — mechanical grep check before `gh pr create`, not just a passive advisory. Logged: `prompt_change_log.md`, `changelogs/execution_prompt_changelog.md`, `OPERATIONAL_GUIDE.md` §14 (v4.103→v4.104). | PMO Lead | — |
| None of this sprint's 8 PRs received a formal GitHub approving review before merge (`reviewDecision: REVIEW_REQUIRED` on all) — the governance model's "Product Owner acceptance (comment on PR or in sprint_backlog.md)" condition was satisfied by an in-session chat authorization + PR comment, but GitHub's branch protection requires an actual Review object, forcing every merge through `gh pr merge --admin` to bypass it | Phase 3 | C | defer | Reconcile the documented merge-gate condition ("comment on PR or in sprint_backlog.md" satisfies Product Owner acceptance) against the repo's actual branch protection rule (requires an approving review) — either relax branch protection to accept a PO-authored comment, or update the governance model to require a real GitHub review and stop accepting comment-only acceptance. Whichever direction is chosen, `--admin` bypass should not be the routine path. | Infrastructure & Operations Owner | Next scheduled roadmap rebalance |
| ESC-EXEC-20260720-01 (EPIC-07/ST-07): the story's own AC and PO-approved UX spec assumed Gemini and Claude were two separate cost-generating providers — a premise never verified against the actual codebase (`gemini_service.py` calls only the Anthropic API; no Gemini integration exists anywhere) until sprint execution traced the implementation. Design Gate and sprint planning both passed this story through without catching it. | Phase 3 | B | decision | Escalated and resolved in-session by Product Owner (option (a), single-provider reframe) — not a prompt patch, a one-off content correction. No recurring pattern identified yet (first instance of this specific class of premise error); noting for awareness rather than filing a process patch on a single occurrence. | Product Owner | 2026-07-20 (resolved) |

**Recurrence Notes:**
The API performance baseline omission (row 1) is the same *shape* of friction as prior "documented-advisory-insufficient-under-load" patterns already fixed elsewhere in this prompt (e.g. LL-v3.7-EX-01/EX-02's atomic-write requirements, LL-v5.5-EX-02's persist-before-halt rule) — a passive note in prose is not reliably followed under multi-file task load; the fix pattern (convert to an active pre-step checklist item, ideally with a mechanical grep/check) is consistent with those prior fixes and was applied the same way here. If a third occurrence of "documented advisory missed under load" surfaces in a future cycle across a *different* rule, that would indicate a structural problem with advisory-only guidance in this prompt generally, not just this one rule.
