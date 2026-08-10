Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-10
Cycle: 2026-08-08__release-v8.5

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-08-08__release-v8.5
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-08-10
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-08-07__release-v8.4 (`lessons_learnt_cycle.md` `## Phase 3`) — 1 friction item + 1 deferred patch: (1) three EPIC-05 items reached `status: done` with `commit_sha: null` despite the LL-v4.8-EX-01 atomic-write rule (Type A, action-now, corrected same session) — **no recurrence**, no null `commit_sha` found in this cycle's `execution_state.json` for any of the 25 items; (2) deferred sub-part — §5.1's in-session provisioning sub-path had no explicit cross-reference back to the LL-v4.8-EX-01 SHA-write rule (Type C, deferred, target "next `execution_prompt.md` revision touching §5.1 or §5.3") — **RESOLVED**: `execution_prompt.md` §5.1 now carries the explicit "Commit-SHA write reminder (LL-v8.4-P3-01)" cross-reference; not directly exercised this cycle (no item used the in-session unblock sub-path), so recurrence is not testable either way, but the gap itself is closed.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Session boundary landed between EPIC-06's PR #1331 merge (confirmed `MERGED` on GitHub, `mergedAt: 2026-08-10T15:43:53Z`) and the routine's own STEP 4 pre-halt persist writes — `execution_state.json` still read `status: done`/`pr_status: open` and `merge_gate.epics_pending: [EPIC-06]` at the start of this session. Cannot confirm from available evidence whether the merge was engine-executed (in which case STEP 4 step 3a's mandatory pre-halt commit was skipped — a recurrence of the LL-v5.5-EX-02 class, previously v5.3/v5.4/v5.5) or performed directly on GitHub outside the routine's own merge action (in which case this is simply the designed STEP 4 resume-sync doing its job, not a rule violation). | Phase 3 | C | action-now | STEP 4's resume-sync protocol (LL-v3.9-P3-1/LL-v6.4-P3-01) handled this correctly this session: `gh pr view` confirmed the merge, `execution_state.json` was synced (`status`/`pr_status`/`merge_gate` all corrected), and the orphaned-post-merge-commit check (LL-v6.8-P3-01) was run against all 6 EPIC branches (0 orphaned commits found). No process patch required — the existing mechanism is exactly what this scenario is designed for and it recovered cleanly in under 10 tool calls | Sprint Execution Engine | — |
| ST-23's agent-mediated Head of Specs Team review (1st pass) caught `OPERATIONAL_GUIDE.md` §14's self-referential Version/Last Updated row still reading a stale value after this session's own ST-22 version bump — the sign-off comment records this as the "9th time" this specific document has needed this exact self-metadata correction. The `governance-drift` skill (`​.claude/skills/governance-drift/SKILL.md` Step 1b) already implements a scripted 3-way self-consistency check (header / §14 self-row / Change Log top row) precisely for this class of drift and already documents 7+ prior recurrences (4.79/80/81/84/85, `AUD-2026-06-10`, `AUD-2026-07-10-002`, `AUD-2026-07-14-001`) — but the skill is not wired into any mandatory invocation point inside `execution_prompt.md` itself (e.g. §3.2.A's DoQ review, or the agent-mediated sign-off protocol in §5.3), so it only catches the drift when an agent happens to run it or a reviewer happens to notice manually, as happened here | Phase 3 | A | defer | Add an explicit instruction to `execution_prompt.md` §3.2.A (or §5.3's agent-mediated sign-off protocol) to invoke the `governance-drift` skill's Step 1b self-consistency check whenever a story's own work bumps `OPERATIONAL_GUIDE.md`'s version (i.e. whenever CLAUDE.md §6's Governance File Edit Checklist fires), rather than relying on a reviewer to catch the 3-way desync by inspection each time. This closes the gap between "a check exists" and "the check is mandatorily run at the moment it matters" | Head of Specs Team | next `execution_prompt.md` revision touching §3.2.A or §5.3 |

**Recurrence Notes:** Neither friction item recurs from `2026-08-07__release-v8.4`'s Phase 3 record (both are newly identified this cycle). The `OPERATIONAL_GUIDE.md` §14 self-referential drift item is, however, a well-established recurring pattern across the project's broader history (9 occurrences per this cycle's own count) — flagged above as `defer` rather than a fresh one-off, since the underlying detection capability already exists and simply needs a mandatory invocation point, not a new mechanism.

## Process improvements actioned this run (Phase 3)

- `execution_state.json` synced for EPIC-06's already-merged PR #1331 (`status`, `pr_status`, `merge_gate.epics_merged`/`epics_pending`/`all_merged`) — see friction item 1 above.
- `OPERATIONAL_GUIDE.md` §14 self-referential Version/Last Updated row corrected in-session during ST-23's 2nd agent-mediated review pass (see friction item 2 above; fix applied to the immediate drift, not to the recurrence mechanism itself, which remains the deferred patch).

## Outstanding deferred patches (Phase 3)

- `governance-drift` skill's Step 1b self-consistency check has no mandatory invocation point inside `execution_prompt.md` — Head of Specs Team, target next `execution_prompt.md` revision touching §3.2.A or §5.3.

## Escalations (Phase 3)

None this cycle.
