Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-18

---

## Update (2026-09-18): ST-21 resolved, EPIC now fully done

The original disposition below (ST-21 deferred to "next `run post-ship`") turned out to depend on a mechanism that doesn't actually exist — Post-Ship Closure's STEP 5.1 corrects living documents' deviation-status drift, not sealed `claude/cycles/<cycle_id>/` content, and no other routine in this framework can edit a sealed artefact either (by design, no override path exists). Head of Specs Team + Product Owner re-ruled (2026-09-18): the sealed source is never edited, permanently, and the true fact stands recorded via `BLG-GOV-334` itself, which now carries that resolution. `ST-21` is accepted done on that basis. See the ST-21 row and Sign-Off Block below for the final state; superseded reasoning is struck through, not deleted, for the audit trail.

---

## Consolidation Block

**EPIC:** EPIC-03 — QA & Test Coverage Debt
**Cycle:** 2026-09-15__release-v9.5
**Sprint goal:** Clear the full v9.5 debt-reduction scope — 43 items across 6 EPICs — at the top of confirmed sprint capacity, resolving the cycle's two genuine ungated P1 items first. See `sprint_goal.md`.
**Test scenarios used:** `tests/test_check_contract_example_freshness.py`, `tests/test_governance_sync_diff_logic.sh`, `tests/test_governance_sync_close_gate_logic.sh`, plus the full backend suite (`tests/` minus `tests/e2e/`).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-15 | `docs/qa/arc4_e2e_test_strategy_po02_03_04.md` | Pre-design E2E test strategy for PO-02/03/04 (none built yet, all gate-blocked) — mocking approach explicitly extends the existing, approved BLG-QA-37 Claude Playwright mock strategy without deviation. | Strategy doc produced; mocking approach defined and consistent with BLG-QA-37; reviewed by Director of Quality. | Pass | None |
| ST-16 | `scripts/governance_sync_lib.sh`, `.github/workflows/governance_sync.yml` | Extracted `detect_newly_done_st_ids()`/`is_story_done()` from 3 independent hand-maintained copies (the workflow + 2 test scripts) into one shared, sourced script. | Diff-detection and close-gate logic each live in exactly one place; both regression test scripts still pass, now exercising the real extracted functions. | Pass | None |
| ST-17 | `tests/test_check_contract_example_freshness.py` | 45 new unit tests for `scripts/check_contract_example_freshness.py` (previously untested despite being pure logic). | New test file exists and passes. | Pass | None |
| ST-18 | `docs/qa/playwright_coverage_matrix.md` | Fully re-derived §2 Spec File Index against `tests/e2e/` directly: 39 (stale) → 104 files, 874 total scenarios. | Per-file table matches actual `tests/e2e/` contents; running total corrected; Version/Last Updated bumped. | Pass | None |
| ST-19 | `docs/qa/cross_browser_playwright_matrix_evaluation_20260909.md` | Corrected a stale pre-sharding CI baseline citation (~133s, 2026-05-29) to the current 163.0s (8-way shard, `ci_pipeline_baseline.md` §9) figure. | Document cites the current CI baseline, not the superseded one. | Pass | None |
| ST-20 | `docs/qa/regression_test_suite_baseline.md` | Real `time npx playwright test` before/after measurement for the SignalCard consolidation's "runtime reduced" claim — found a nuanced correction (isolated test-exec time ~8% faster; total wall-clock roughly a wash under default per-file worker allocation), not a clean confirmation. | Real before/after runtime number recorded, substantiating (or correcting) the original claim. | Pass | None |
| ST-21 | N/A — target is a sealed prior-cycle artefact, permanently outside any routine's write scope | `BLG-QA-170`'s correction target (`claude/cycles/2026-09-09__release-v9.3/qa_evidence_EPIC-03.md`) is inside an already-Published/sealed cycle — CLAUDE.md §2's sealed-artefact rule has no override path anywhere in this framework, confirmed on a second, more careful pass after an initially-proposed mechanism (Post-Ship STEP 5.1) turned out not to apply. Ruled by Head of Specs Team, accepted by Product Owner (2026-09-18): the sealed file stays untouched, permanently, by design; the true fact (28, not 30) is permanently recorded via `BLG-GOV-334` itself instead. | Test count "matches actual" — **AC reinterpreted, not silently waived**: satisfied by the true count being permanently and discoverably recorded, since the literal wording (editing the sealed source) can never be met and the AC's original intent (don't let the wrong number stand uncorrected) is fully served this way. | Pass (accepted disposition) | `BLG-GOV-334` (the permanent correction record; both items closed on this disposition) |

**QA test coverage:**
- Scenarios run: `tests/test_check_contract_example_freshness.py` (45, new, ST-17), `scripts/test_governance_sync_diff_logic.sh` + `scripts/test_governance_sync_close_gate_logic.sh` (3+4 cases, re-verified against the extracted shared lib, ST-16) — plus full backend suite re-run clean: 1519 passed, 10 skipped, 0 failed.
- Regression areas checked: contract-example-freshness drift detection (unaffected — new tests only, no behaviour change to the script itself), governance-sync diff/close-gate logic (behaviourally identical after extraction — both test scripts assert against the real functions, not a copy, and all assertions still pass), Playwright coverage matrix consumers (no code depends on the corrected file inventory; documentation-only).
- Known deviations: None found for ST-15/16/17/18/19/20. `ST-21` is not a deviation in the formal sense (nothing was narrowed or silently unmet within a shipped story) — its AC was reinterpreted under Head of Specs Team + Product Owner authority once the sealed-artefact constraint was discovered, and the reinterpreted disposition is fully met (see ST-21 row above).

---

## Sign-Off Block

**Full sign-off — all 7 stories.** `ST-21`'s disposition was reinterpreted (not waived or silently marked done) under explicit Head of Specs Team ruling and Product Owner acceptance, both recorded in `delegation_log.md`.

- [x] All acceptance criteria verified against canonical spec — ST-15 through ST-20 as originally written; ST-21 against its reinterpreted (Head of Specs Team + Product Owner accepted) disposition
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked — full backend suite green after every story (1519 passed, 10 skipped)
- [x] N/A — no frontend component in this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Signed off by: Sprint Execution Engine (agent-mediated, Head of Specs Team role — §5.3, ST-21 ruling)
- Signed off by: Sprint Execution Engine (agent-mediated, Product Owner role — §5.3, ST-21 acceptance, explicit user direction)
- Date: 2026-09-18
- Comments: ST-15–ST-20 verified as originally scoped, no changes. ST-21's original plan (defer to Post-Ship STEP 5.1) was found, on re-verification, to rely on a mechanism that doesn't exist — STEP 5.1 corrects living-document deviation-status drift, not sealed cycle content, and no routine in this framework can edit a sealed artefact. Re-ruled: the sealed `2026-09-09__release-v9.3/qa_evidence_EPIC-03.md` stays untouched permanently (no exception exists to CLAUDE.md §2's sealed-artefact rule); the true fact (28, not 30 tests) is permanently and discoverably recorded via `BLG-GOV-334` itself, which now carries this resolution directly rather than a plan to act later. Product Owner accepted this as satisfying ST-21's underlying intent (the wrong number not standing uncorrected) even though its literal AC wording could never be met once the constraint was found. This EPIC now satisfies `execution_prompt.md` §3.2 ("all ST items done") in full. Full investigation and ruling trail: `delegation_log.md` `DEL-20260916-03-EPIC03` / `DEL-20260916-04-EPIC03` / `DEL-20260918-03-EPIC03`.
