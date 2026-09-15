Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-15 (delivery verification — Phase 4 section added)
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

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-09-14__release-v9.4
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-09-15
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-09-09__release-v9.3 (`lessons_learnt_cycle.md` `## Phase 4`) — 1 friction item filed: `qa_evidence_EPIC-05.md`'s ST-22 used a free-text label (`Pass, with open escalation`) not in `delivery_verification_prompt.md` STEP 2.1's enumerated Result set, deferred to a prompt revision adding a formal value. Checked and confirmed applied: `delivery_verification_prompt.md` v3.10→v3.11 (2026-09-14, post-ship closure of `2026-09-09__release-v9.3`) added `Pass, escalation open` to STEP 2.1's enumerated values with defined semantics (requires the Comments field to name the open escalation ID). Treated as applied, not a recurrence of the *same* gap — but see this cycle's own new friction item below, a distinct misapplication of the newly-added value.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `qa_evidence_EPIC-01.md`'s ST-05 row uses the newly-formalised `Pass, escalation open` Result value (v3.11), but its Deviations column names `BLG-OPS-160` — a **backlog item ID**, not an open escalation ID (`ESC-*`). STEP 2.1/2.3's definition of this value requires the Comments field to name an *open escalation*; no escalation was actually raised for ST-05 (its own AC is independently fully met — this is an incidental out-of-scope finding surfaced during the story's own inventory work, structurally identical to a routine "AC met, secondary finding filed separately" case that other rows this same cycle correctly recorded as plain `Pass` with the backlog item noted in Deviations, e.g. EPIC-06's ST-24/ST-26). The v3.11 enumeration closed the *label-shape* gap from v9.3's Phase 4 finding but did not add guidance distinguishing "AC met, adjacent open escalation" from "AC met, incidental backlog-item finding filed" — the latter should use plain `Pass`, not `Pass, escalation open`. | Phase 4 | B | defer | Add a disambiguation note to `qa_evidence_template.md` (and/or `delivery_verification_prompt.md` STEP 2.1) clarifying that `Pass, escalation open` is reserved for a named, open `ESC-*` record only — an AC-met story that merely surfaces a new backlog item during its own work should use plain `Pass` (or `Pass with notes`) with the backlog item cited in Deviations/Comments, not the escalation-specific value. | Head of Specs Team | next `delivery_verification_prompt.md`/`qa_evidence_template.md` revision touching §2.1 |

**Recurrence Notes:**
Related to, but distinct from, `2026-09-09__release-v9.3`'s Phase 4 friction item (see "Prior cycle checked" above) — that item's fix (adding the enumerated value) shipped and is confirmed working as intended for its own originating case (ST-22/`ESC-EXEC-20260910-01`, a genuine open escalation, unaffected this cycle). This cycle's finding is a second-order gap in the same enumeration: the newly-added value's own definition was clear enough to close the original label-shape problem but not to prevent a second author from applying it to a different, non-escalation shape. No verification-status impact — flagged in `verification_report.md §3`, not a blocker.
