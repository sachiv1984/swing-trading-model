Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-13
Cycle: 2026-08-12__release-v8.7

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-08-12__release-v8.7
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-08-13
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-08-11__release-v8.6 (`lessons_learnt_cycle.md` `## Phase 3`) — 3 friction items, 1 deferred patch. (1) `OPERATIONAL_GUIDE.md` §14 self-consistency check wiring, recurrence-escalated after 2 cycles — resolved action-now that cycle. (2) The "first-pass already-verified claim is factually wrong, caught only by a second review pass" pattern (3 occurrences in v8.6) — **deferred**, target "next `execution_prompt.md` revision touching §5.3". Checked against `prompt_change_log.md` by patch-ID tag (`LL-v8.6-P3-01`) per the §3.7 matching requirement: **applied** 2026-08-12 (`execution_prompt.md` v3.67→v3.68, lifecycle audit AUD-2026-08-12) — §5.3 now carries the quantitative/"already verified" claim second-review-pass requirement. Not carried into this cycle as an open item; no recurrence escalation triggered. (3) ST-21's cron-only-workflow AC pattern, resolved action-now (no prompt change needed) — not recurring this cycle (no comparable AC shape in v8.7's scope).

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Session start found `execution_state.json.merge_gate` stale (`epics_pending: ["EPIC-07"]` despite PR #1391 already merged upstream) — 3rd consecutive cycle (v8.5→v8.6→v8.7) where a session boundary landed between an EPIC's PR merge and the routine's own pre-halt persist writes. | Phase 3 | C | action-now | No new patch — the existing LL-v7.2-P3-01 session-start divergence check + LL-v3.9-P3-1 merge-gate resume-sync again recovered cleanly this cycle (`git fetch`/`checkout`/`pull`, `gh pr view 1391` sync, 0 orphaned commits found across all 7 branches). Confirms, for the 3rd time, that this is by-design recovery behaviour, not a gap — no structural change triggered. | Sprint Execution Engine | — |
| ST-12 (EPIC-04, "SI-04 schema requirements pre-design") was scoped into this sprint's `sprint_backlog.md` even though the feature it targets (SI-04) had already shipped 4 releases earlier (v7.7) and the underlying question (`BLG-BE-30`) was answered at implementation time with no new schema — the story was stale before Sprint Planning sealed it. | Phase 3 | A | defer | Sprint Planning's pre-seal story scoping has no check for "does this story's target feature already exist on `main`" before pulling a backlog item into scope. Recommend a lightweight pre-seal grep/status check in `sprint_planning_prompt.md` (or `groom backlog`'s health check) confirming a story's referenced feature/roadmap item isn't already shipped. `BLG-BE-30` itself flagged for PO/`groom backlog` resolution (retroactive confirmation doc produced this sprint per the story's AC wording, but the story delivered no new work). | Head of Specs Team | next `sprint_planning_prompt.md` revision or `groom backlog` pass |
| ST-08 (EPIC-03) authored new Playwright coverage but could not execute it locally — this sandbox's OS (`ubuntu26.04-x64`) does not support Playwright's browser binaries, a recurring environment-parity gap already governed by LL-v8.3-P3-02's real-CI-confirmation sub-clause. Tests were statically verified (parse, lint, manual selector trace) and disclosed as pending real-CI confirmation in `qa_evidence_EPIC-03.md`; PR #1387 subsequently passed `quality_gate.yml` and merged, confirming the tests passed for real in GitHub Actions. | Phase 3 | C | action-now | No new patch — LL-v8.3-P3-02's existing sub-clause (disclose sandbox-execution limitation, confirm via real CI before/at merge) worked exactly as designed; real CI outcome now recorded here for closure. | Sprint Execution Engine | — |

**Recurrence Notes:** Friction item 1 is the direct continuation of v8.5→v8.6's already-tracked "by design" resume pattern (v8.6 Phase 3 item 1) — 3rd consecutive occurrence, still not treated as a gap since the recovery mechanism itself has never failed to catch it. Friction item 2 is newly identified this cycle (no v8.6 Phase 3 item named this pattern). Friction item 3 is a fresh instance of the general environment-parity class LL-v8.3-P3-02 already covers, not a new pattern — first time its real-CI-confirmation clause has been exercised and closed out end-to-end in this Phase 3 record.

## Process improvements actioned this run (Phase 3)

- `execution_state.json` synced for EPIC-07 (`status`, `pr_status`, `merge_gate.epics_merged`/`epics_pending`/`all_merged`) — see friction item 1 above.
- Orphaned post-merge commit check (LL-v6.8-P3-01) run for all 7 EPIC branches against `origin/main` — 0 orphaned commits found on any branch.
- Confirmed v8.6 Phase 3's deferred §5.3 patch (`LL-v8.6-P3-01`) is live in `execution_prompt.md` v3.68 — no action needed this cycle, closed out in the recurrence check above.

## Outstanding deferred patches (Phase 3)

- Sprint Planning pre-seal "story's target feature already shipped" check (friction item 2 above) — target Head of Specs Team, next `sprint_planning_prompt.md` revision or `groom backlog` pass.

## Escalations (Phase 3)

None this cycle. No `execution_escalations.md` file was required — no blocker went unresolved within a session.
