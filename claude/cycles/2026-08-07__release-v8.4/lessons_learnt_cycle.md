Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-08
Cycle: 2026-08-07__release-v8.4

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-08-07__release-v8.4
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-08-08
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-08-05__release-v8.3 (`lessons_learnt_cycle.md` `## Phase 3`) — 3 friction items + 1 recurrence escalation: (1) `DoQ Sign-off Staleness Lint` self-referential false positive (Type A, action-now, resolved same session, commit `428782d6`) — **no recurrence**, no new self-referential lint pattern hit this cycle; (2) sandboxed-review-vs-real-CI environment-parity gap for focus/interaction-timing ACs (Type C, deferred, target "next `execution_prompt.md` revision touching the frontend-testing-gate") — **partially addressed**: `execution_prompt.md` §3.2.A now carries the "Environment-parity sub-clause for focus/interaction-timing ACs (LL-v8.3-P3-02)" naming this exact gap; no EPIC in this cycle hit a focus-restoration AC to test it against, so recurrence is not checkable either way this cycle; (3) no scripted way to distinguish infra-outage CI failures from real ones (Type C, deferred, target "next CI/workflow-tooling pass") — **no recurrence**, no GitHub-wide outage encountered this cycle; (4) backlog write-scope tension, 3rd+ consecutive recurrence escalation to Head of Specs Team (Type C) — **RESOLVED this cycle**: `execution_prompt.md` §7 and `CLAUDE.md` §2 now both carry a formal, sanctioned new-item-addition write path to `claude/backlog/backlog.md` for genuinely out-of-scope mid-sprint findings (Option (a) from the escalation), closing out a gap that had been deferred across v8.1/v8.2/v8.3. This cycle used that sanctioned path 9 times (`BLG-FE-143`, `BLG-FE-144`, `BLG-FE-145`, `BLG-FE-146`, `BLG-BE-84`, `BLG-BE-85`, `BLG-BE-86`, `BLG-BE-87`, `BLG-OPS-134`) with no process friction.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Three EPIC-05 items (ST-20, ST-21, ST-23 — a mix of `delegated_decision` and `delegated_backend`, all unblocked in-session per LL-v8.2-P3-04) reached `status: done` with `commit_sha: null` in `execution_state.json`, even though each had an identifiable implementation commit already pushed and merged to `main` (`77e39e4f`, `104a7445`, `0c8d56d5` respectively). LL-v4.8-EX-01's atomic post-push commit-SHA write was skipped for all three. Not caught until this session's STEP 5.1 acceptance summary pass, well after the items were marked done and their EPIC merged — the field sat wrong for up to a full day without surfacing anywhere the merge gate or delivery verification preflight would have caught it, since neither checks `commit_sha` non-null as a hard-gate condition | Phase 3 | A | action-now | Corrected directly in `execution_state.json` by cross-referencing `git log --oneline` for each story's `[EPIC-05][ST-xx]`-prefixed commit. See `execution_state.json.process_notes` for the correction record. No prompt change applied this run — see Root Cause Note below for why a process-level fix, not a one-off correction, is still owed | Sprint Execution Engine | — |
| Root Cause Note (same friction item, deferred sub-part): LL-v8.2-P3-04's in-session credential/action provisioning sub-path (§5.1) documents the delegation-log entry requirements for in-session unblocks in detail, but does not explicitly re-state the LL-v4.8-EX-01 commit-SHA-write requirement as part of its own unblock sequence — an agent following the in-session path's own listed steps has no direct pointer back to the SHA-write rule at the moment it applies. All three misses this cycle occurred specifically on in-session-unblocked items (none on the cycle's standard-flow autonomous items), suggesting the gap is with that sub-path's own step list, not the general rule | Phase 3 | C | defer | Add an explicit cross-reference to LL-v4.8-EX-01 inside §5.1's in-session provisioning sub-path (either as an inline reminder in the existing step list or a "see also" note), so the SHA-write requirement is visible at the exact point an agent is executing that path, not only in the general STEP 3.1.A/B flow it's easy to assume was already followed | Head of Specs Team | next `execution_prompt.md` revision touching §5.1 or §5.3 |

**Recurrence Notes:** None of this cycle's friction items recur from `2026-08-05__release-v8.3`'s Phase 3 record — both are newly identified this cycle. The prior cycle's 3rd+ consecutive backlog write-scope recurrence escalation is now resolved (see Prior cycle checked note above) — no further escalation required.

## Process improvements actioned this run (Phase 3)

- `execution_state.json` corrected for ST-20/ST-21/ST-23's missing `commit_sha` fields (see friction item 1 above).

## Outstanding deferred patches (Phase 3)

- LL-v4.8-EX-01 cross-reference missing from §5.1's in-session provisioning sub-path — Head of Specs Team, target next `execution_prompt.md` revision touching §5.1 or §5.3.
- Sandboxed-review-vs-real-CI environment-parity gap for focus/interaction-timing ACs (carried from v8.3, partially addressed via LL-v8.3-P3-02) — Base44 Frontend Prompt Owner, target next EPIC that ships a focus-restoration AC to actually test the new sub-clause against.

## Escalations (Phase 3)

None this cycle.

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-08-07__release-v8.4
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-08-08
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-08-05__release-v8.3 (`lessons_learnt_cycle.md` `## Phase 4`) — no friction items, no open deferred patches. **Nothing to check forward this run** — the prior cycle's Phase 4 record closed clean with zero outstanding items.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| EPIC-01's `execution_state.json.test_scenarios` field was left `[]` despite genuine, real-CI-confirmed Playwright/pytest coverage existing and being documented in `qa_evidence_EPIC-01.md` (`tests/e2e/monthly-pnl-avg-per-trade.spec.js`, `tests/test_trade_origin_query.py`, `tests/test_reports_integration.py`) — the field was populated correctly at the per-story `spec_references` level but never rolled up to the EPIC-level `test_scenarios` array. Caught this session at STEP 5 (Test Scenario Coverage Assessment) by independently cross-referencing `qa_evidence_EPIC-01.md`'s own "Test scenarios used" header and confirming the cited files exist on disk — not by trusting the field at face value. Had this gone unnoticed, a future audit or verification run reading `execution_state.json` alone would have logged a false "no scenarios available" coverage read against an EPIC that in fact has full real-browser evidence | Phase 4 | A | defer | Add an explicit cross-reference in `execution_prompt.md` (STEP 3.1.A or its post-push write step) requiring the EPIC-level `execution_state.json.test_scenarios` array to be populated with every runnable test file already listed in that EPIC's stories' own `spec_references`, not left `[]` by default whenever at least one story's spec_references includes a test file | Head of Specs Team | next `execution_prompt.md` revision touching STEP 3.1.A or STEP 5 |

**Recurrence Notes:** None — this is a newly identified friction item; the prior cycle's Phase 4 record had nothing outstanding to recur.

## Recurrence Escalations (Phase 4)

None.

## Process improvements actioned this run (Phase 4)

None applied this run — the friction item above is deferred (execution_state.json is a sealed artefact this routine may not modify; the fix belongs in execution_prompt.md's record-population step, not in this cycle's record).

## Outstanding deferred patches (Phase 4)

- EPIC-level `test_scenarios` roll-up from story-level `spec_references` missing from `execution_prompt.md`'s record-population step — Head of Specs Team, target next `execution_prompt.md` revision touching STEP 3.1.A or STEP 5.

## Escalations (Phase 4)

None this cycle.
