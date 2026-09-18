Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-18

---

## ⚠️ Known Incomplete: ST-21 not done (deferred, not blocking evidence quality)

**This EPIC is NOT eligible for the standard merge gate yet.** 6 of 7 stories are `done`; `ST-21` is `blocked_decision` (ruled-and-deferred — see below), not `done`. Per `execution_prompt.md` §3.2, an EPIC reaches "done" only when all its ST items are done, and the merge gate's first condition requires "All ST items in EPIC: done (not blocked_*)". This PR is opened anyway, on explicit user instruction, so it is visible and reviewable — it is not expected to pass the merge gate until `ST-21` resolves at the next `run post-ship`.

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
| ST-21 | N/A — target is a sealed prior-cycle artefact, outside this routine's write scope | **Not done.** `BLG-QA-170`'s correction target (`claude/cycles/2026-09-09__release-v9.3/qa_evidence_EPIC-03.md`) is inside an already-Published/sealed cycle — CLAUDE.md §2's sealed-artefact rule and `execution_prompt.md` §7's write-scope restriction both block a direct fix. Ruled by Head of Specs Team (explicit user direction): the sealed file stays untouched permanently; the correction mechanism is Post-Ship Closure Engine's STEP 5.1 cross-cycle deviation consolidation review (precedented at `api_performance_baseline.md` §v2.32). Filed `BLG-GOV-334` to carry the exact correction (28, not 30) forward. | Test count in `qa_evidence_EPIC-03.md` matches actual — **not yet met**; sealed file still reads 30. | **Deferred (not Pass, not Fail)** | `BLG-GOV-334` (tracks the actual correction, scheduled for next `run post-ship`) |

**QA test coverage:**
- Scenarios run: `tests/test_check_contract_example_freshness.py` (45, new, ST-17), `scripts/test_governance_sync_diff_logic.sh` + `scripts/test_governance_sync_close_gate_logic.sh` (3+4 cases, re-verified against the extracted shared lib, ST-16) — plus full backend suite re-run clean: 1519 passed, 10 skipped, 0 failed.
- Regression areas checked: contract-example-freshness drift detection (unaffected — new tests only, no behaviour change to the script itself), governance-sync diff/close-gate logic (behaviourally identical after extraction — both test scripts assert against the real functions, not a copy, and all assertions still pass), Playwright coverage matrix consumers (no code depends on the corrected file inventory; documentation-only).
- Known deviations: None found for ST-15/16/17/18/19/20. `ST-21` is not a deviation in the formal sense (nothing was narrowed or silently unmet within a shipped story) — it is a story that has not shipped, ruled-and-deferred to a different governed routine with a named tracking item (`BLG-GOV-334`).

---

## Sign-Off Block

**This EPIC does not qualify for a standard or autonomous-class sign-off.** 6 of 7 stories pass every check; `ST-21` is genuinely incomplete (not narrowed, not fabricated — simply not done, for reasons outside this routine's authority to resolve). The sign-off below covers ST-15 through ST-20 only, and explicitly withholds sign-off on ST-21 pending its own resolution.

- [x] All acceptance criteria verified against canonical spec — ST-15 through ST-20 (6 of 7 stories)
- [ ] **ST-21 acceptance criteria NOT met** — sealed-artefact correction deferred to next `run post-ship`, tracked via `BLG-GOV-334`
- [x] No unresolved P0 or P1 deviations — `BLG-GOV-334` is P3, non-blocking
- [x] Regression areas checked — full backend suite green after every story (1519 passed, 10 skipped)
- [x] N/A — no frontend component in this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Signed off by: Sprint Execution Engine (agent-mediated, Head of Specs Team role — §5.3, ST-21 ruling only)
- Date: 2026-09-18
- Comments: This sign-off is **partial by design** — it certifies ST-15 through ST-20 as fully verified and certifies that ST-21's incompleteness is honestly disclosed, ruled on by the correct authority, and has a concrete tracked path to resolution (`BLG-GOV-334`), not that ST-21 itself is complete. Per `CLAUDE.md`/`execution_prompt.md` §3.2, this EPIC cannot pass the standard merge gate ("All ST items in EPIC: done") until `ST-21` resolves. This PR is opened on explicit user instruction for visibility and review, not as a claim that the merge gate is satisfied. Full investigation and ruling trail: `delegation_log.md` `DEL-20260916-03-EPIC03` / `DEL-20260916-04-EPIC03`.
