Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-15
Cycle: 2026-09-14__release-v9.4

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-09-14__release-v9.4
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-09-15
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-09-09__release-v9.3 (`lessons_learnt_cycle.md` `## Phase 3`) — 1 friction item filed: `ESC-EXEC-20260910-01`'s non-blocking-but-SLA-breached status went unsurfaced mid-sprint, with the deferred fix recommendation targeted at `execution_prompt.md`/`shared_standards.md §16.4`'s next revision. Checked `prompt_change_log.md` by patch-ID search and by re-reading the actual entries dated around this cycle's own lifecycle audit (`AUD-2026-09-14`): the underlying gap was closed, but via `release_planning_prompt.md` v2.49→v2.50 (a STEP -1.6 hard gate reading `.claude_current_state.json.open_escalations` for any `Open` entry past its `sla_due_utc`, regardless of `blocks_execution`) rather than the originally-named `execution_prompt.md`/`shared_standards.md §16.4`. This closes the actual observed failure mode (an SLA-breached escalation crossing Delivery Verification and Post-Ship Closure unhalted) at a broader, more structural point than the narrower fix originally proposed. Treated as applied, not a recurrence — the gap is closed, even though the implementing file differs from the friction item's own suggestion.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| A cross-file pytest test-isolation leak (`test_ai_output_sampling_service.py`'s module-level `sys.modules.pop("database", None); import database` permanently overwrote the shared stub for the rest of the pytest session, alphabetically leaking into `test_alerts_service.py` and attempting a real Postgres connection) was invisible locally and only surfaced as a live CI Phase B failure post-push on EPIC-05/ST-23. Root-caused and fixed correctly (isolated-copy + scoped `patch.dict` pattern already established by `test_position_audit_log.py`), and the same latent pattern was proactively found and filed for a twin case (`test_trade_plan_audit_log.py`, `BLG-QA-178`) — but nothing in the Playwright/pytest authoring standard (`shared_standards.md §18`) currently tells a story author *up front* to use the isolated-copy pattern whenever a new test needs to reimport `database`, rather than discovering the collection-order hazard after a live CI failure. | Phase 3 | B | defer | Add an explicit rule to `shared_standards.md §18` (or a new pytest-authoring-standard subsection): any test file that needs to reimport `database` for stub/mock isolation must use `importlib.util.spec_from_file_location` + scoped `patch.dict`, never a bare `sys.modules.pop(...); import database` at module level — cite `test_position_audit_log.py` as the canonical pattern. Needs Head of Specs Team confirmation on exact placement before wording lands. | Head of Specs Team | next `shared_standards.md` revision touching pytest authoring standards |

**Recurrence Notes:**
None — the test-isolation friction item above did not appear in `2026-09-09__release-v9.3`'s Phase 3 record (it is a new failure mode, first observed this cycle). Separately, two mechanisms were re-confirmed working exactly as designed this cycle, not requiring any new fix: (1) both EPIC-05 (PR #1666) and EPIC-06 (PR #1667) were merged directly by the human via GitHub rather than through the engine's own STEP 4 flow — in both cases the mid-session re-sync rule (`AUD-2026-08-21-010`) correctly detected the stale `pr_status`/`merge_gate` state on the next turn, found zero orphaned post-merge commits on either branch, and reconciled cleanly; (2) the always-human merge gate (`execution_prompt.md §5.3` / CLAUDE.md §2) held throughout — both PRs reached 100% green CI and a correctly-labeled agent-mediated advisory review before the actual human merge decision, and the engine never attempted to self-approve either merge.
