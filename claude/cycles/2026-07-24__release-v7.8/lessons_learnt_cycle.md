Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-27
Cycle: 2026-07-24__release-v7.8

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-07-24__release-v7.8
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-27
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-07-21__release-v7.7 (`lessons_learnt_cycle.md` `## Phase 4`) — no friction items identified that run; one prior-prior recurrence (stale amendment-tracking fields, v7.6) was confirmed closed and non-recurring. No open Phase 4 item carried into this cycle.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| 3 documentation-completeness gaps against `position_endpoints.md`/`trade_endpoints.md` (found by ST-11 while authoring pilot contract tests, recorded in `qa_evidence_EPIC-11.md`) had no corresponding `backlog.md` entry at sprint close — the story's own framing ("left to standard backlog grooming") did not, in practice, result in a filed item before delivery verification | Phase 4 | C | action-now | Filed `BLG-SPEC-102`, `BLG-SPEC-103`, `BLG-SPEC-104` to `claude/backlog/backlog.md` at delivery verification STEP 4.1, per the "any flagged gap must have a backlog.md entry before the verification report is sealed" rule (`delivery_verification_prompt.md` §7). See `verification_report.md §5(a)`. | Director of Quality | — |

All other STEP -1 through STEP 7 checks completed cleanly: sprint close readiness statement all `Yes`; all 12 QA evidence logs present with compliant, non-blank sign-offs on first read (no Tier 1/Tier 2 issues); zero deviations filed; zero traceability gaps; zero outstanding/delegated items; `deferred_execution_blockers` empty; zero parked items (stale-parked check skipped); test scenario coverage fully accounted for (11 EPICs with confirmed-run scenarios, 1 correctly dispositioned `not_applicable`, no genuine gaps); `docs/System_status_report.md`'s v7.8 section required only the expected routine status-line update, no content corrections. Status determined as `Verified` with no hard blocks encountered.

**Recurrence Notes:**
None — this is a fresh (first-occurrence) friction item, not a recurrence of the v7.7 Phase 4 item (which was a stale-state-field issue, unrelated to this cycle's finding).

---

## Recurrence Escalations (Phase 4)

None.

## Process improvements actioned this run (Phase 4)

Filed 3 backlog items (`BLG-SPEC-102`, `BLG-SPEC-103`, `BLG-SPEC-104`) closing the traceability gap identified above — see `action-now` row.

## Outstanding deferred patches (Phase 4)

None.

## Escalations (Phase 4)

None.

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-07-24__release-v7.8
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-27
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-07-21__release-v7.7 (`lessons_learnt_cycle.md` `## Phase 3`) — 3 friction items recorded, all classified `defer`/`decision` with target "next run of this routine" (i.e. this cycle). See Recurrence Notes below for disposition of each.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| The API Performance Baseline pre-PR advisory (LL-v7.6-P3-01, added specifically after this same class of miss in v7.6/EPIC-07) failed to prevent a second occurrence: `GET /ai/spend-trend` (EPIC-06) was added to `openapi.yaml` without a `docs/ops/api_performance_baseline.md` registration entry, caught only by the API Performance Baseline Drift Detection CI gate after the PR was already open, requiring a follow-up commit — the same recovery path the v7.6 note describes | Phase 3 | C | defer | A prose advisory inside a long execution prompt is not a reliable substitute for an automated check — propose converting the `grep -c` pre-PR check already described in LL-v7.6-P3-01 into an actual pre-commit or pre-PR-open script step (not just documented prose the agent must remember to run) so the check fires mechanically rather than depending on the agent recalling a single paragraph under multi-EPIC context load | Head of Specs Team | next run of this routine |
| A live git-merge auto-resolution correctness gap: when two independently-cut branches (EPIC-01, EPIC-06) each bump the same hardcoded fallback constant (`SystemStatus.js`'s endpoint count, `tests/e2e/system-status.spec.js`'s `SC-SS-01b` assertion) to the identical literal value for their own distinct new endpoint, `git merge` treats the two sides as textually identical and auto-merges "cleanly" onto a semantically wrong value — no conflict marker is ever raised, so the error is silent unless someone re-derives the true value independently | Phase 3 | C | action-now | Caught this run only because the AST-based endpoint-count script (added v7.7 EPIC-11) was re-run against the post-merge `backend/routers/test.py` as a matter of habit, not because any gate flagged it. No prompt change applied this run (the existing v7.7-filed proposal below already covers the general fix) — recorded here as a fresh, concrete instance of the same defer item, not a new independent one. | Head of Engineering | — |

**Recurrence Notes:**
Two of the three v7.7 Phase 3 friction items recurred this cycle with their prior outstanding action still unresolved — both are recorded under Recurrence Escalations below, not as new rows in the table above, per the mandatory rule (a friction item recurring with an open prior outstanding action is an automatic escalation, not a fresh deferred item):
1. **execution_state.json cross-EPIC conflict pattern** (v7.7 friction item 1, deferred to Head of Specs Team, target "next run of this routine") — recurred exactly as described: every one of this cycle's 12 EPIC branches was cut before sprint execution progressed on `main`, so every branch (not just siblings 02–11 as in v7.7, but all 12 here) carried an independently-diverging copy of `execution_state.json`. 11 of 12 branches required a manual conflict-resolution pass this session (the 12th, EPIC-11, happened to still be mergeable at merge time). No STEP 2/STEP 4 proactive-rebase mechanism was added between v7.7 and this cycle to address it structurally.
2. **Endpoint-count fallback collision** (v7.7 friction item 2, deferred to Head of Engineering, target "next run of this routine") — recurred in the identical shape (two independently-cut branches, same hardcoded constant, same silent git auto-merge). Documented as a fresh concrete instance in the table above (`action-now` row) since it's the same unresolved defer item recurring, not a new independent friction.

The third v7.7 item (Type E, `decision` classification — whether agent-mediated "acting as Product Owner" PR comments should be disallowed entirely) has not been formally ruled on by Head of Specs Team. This cycle avoided the specific confusion risk the item described (an agent mistaking a proxy PO comment for genuine human acceptance) by a different means: before performing any agent-mediated Director of Quality/Product Owner review this cycle, the repository owner was asked explicitly how sign-off attribution should be labeled, and chose to have every review clearly marked as agent-mediated (not impersonating a human role) with the literal `Signed off by:`/`Date:` sign-off fields left blank for the owner to complete personally — the owner then reviewed and explicitly approved each specific sign-off diff before it was committed. This is a safer variant of the pattern than the one the v7.7 item flagged, but it is a session-level practice, not a codified rule — the underlying policy question (should this class of comment be permitted at all, and if so under what labeling convention) remains open and unruled. Not filed as a fresh recurrence escalation (only 1 cycle old, and no prompt_change_log-trackable deferred patch exists to check the "2+ cycles" threshold against), but carried forward below.

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| execution_state.json cross-EPIC conflict pattern — every EPIC branch cut before sprint execution progresses on `main` accumulates an independently-diverging full copy of the shared state file, requiring a manual per-branch resolve pass at merge time | 2026-07-21__release-v7.7 | Propose an explicit "post-first-merge rebase" step at STEP 2 (Branch Preflight) or STEP 4 resolving this conflict class proactively per-branch instead of leaving it to a scramble at merge-gate time. Owner: Head of Specs Team. Target: next run of this routine (this cycle) — not applied. | Head of Specs Team |
| Endpoint-count (or any AST-derivable hardcoded constant) fallback collision across concurrently-open sibling PRs — independently-cut branches derive the same wrong value against different baselines, and `git merge` cannot detect the resulting semantic conflict when the literal text happens to match | 2026-07-21__release-v7.7 | Propose STEP 3.1.A flag any story hardcoding a value also derivable via an AST/script check, requiring re-derivation (not assumption) of that value at rebase time. Owner: Head of Engineering. Target: next run of this routine (this cycle) — not applied. | Head of Engineering |

## Process improvements actioned this run

None applied this run — both action-eligible items above are recurrences of already-deferred v7.7 items now escalated rather than independently patched; the third (API performance baseline advisory strengthening) is newly deferred, not action-now.

## New files created this run

None.

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | §3.2.B (LL-v7.6-P3-01) | Convert the API performance baseline pre-PR check from prose advisory to an enforced pre-commit/pre-PR-open script step — the advisory has now failed to prevent this exact class of miss twice (v7.6/EPIC-07, v7.8/EPIC-06) | Head of Specs Team | next run of this routine |

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| execution_state.json cross-EPIC conflict pattern (recurrence, 2nd consecutive cycle) | Recurrence | Head of Specs Team | Prior cycle's deferred structural fix (proactive per-branch rebase step at STEP 2/4) was never applied; the friction recurred at greater scale this cycle (11 of 12 branches affected, vs 10 of 11 in v7.7) |
| Endpoint-count/hardcoded-constant fallback collision (recurrence, 2nd consecutive cycle) | Recurrence | Head of Engineering | Prior cycle's deferred structural fix (flag AST-derivable hardcoded values for mandatory re-derivation at rebase time) was never applied; the friction recurred in the identical shape this cycle |
| Whether agent-mediated "acting as Product Owner"/"acting as Director of Quality" PR review comments should be disallowed entirely, and if permitted, under what labeling convention | Authority ambiguity (carried forward, unruled) | Head of Specs Team | v7.7's Phase 3 friction item 3 raised this and was never formally ruled on; this cycle worked around the specific risk via an explicit owner-confirmed labeling convention (agent-mediated, sign-off fields left blank for human completion) rather than a codified rule — not yet a 2nd-cycle recurrence escalation, but unresolved |

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Two consecutive cycles (v7.7, v7.8) have now hit the same execution_state.json cross-EPIC conflict pattern with no structural fix applied between them — the cost scaled up (11/12 branches this cycle vs 10/11 last cycle) rather than down | Sprint Execution should not proceed past a second occurrence of this exact recurrence without either applying the deferred STEP 2/4 fix or explicitly re-confirming with Head of Specs Team that the manual-resolve cost is accepted as a standing cost of this sprint's multi-EPIC-parallel-branch model | Sprint Execution |
| 2 | This cycle's largest real defects (WhatsNewCard double-unwrap bug, EPIC-06's test-isolation bug, the endpoint-count collision, the missing API performance baseline registration) were all caught by *actually executing* tests/CI rather than by reading code or trusting "written but not yet run" disclaimers — the sandbox's initial inability to run Playwright was worked around specifically to make this possible | Sprint Execution should continue treating "get real test execution working, even under a constrained sandbox" as higher-value than accepting untested-but-plausible sign-off language | Sprint Execution |
