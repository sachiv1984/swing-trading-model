Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-13

---

## Consolidation Block

**EPIC:** EPIC-03 — Test Coverage for Shipped UI & Financial Correctness
**Cycle:** 2026-08-12__release-v8.7
**Sprint goal:** Deliver v8.7's user-facing feature and theme-consistency completion work while closing the mandatory trade-plan data-integrity carryover from v8.6, backed by expanded test, security, reliability, and governance coverage across the release's remaining six EPICs.
**Test scenarios used:** `tests/e2e/shadcn-token-remaining-families.spec.js` (new, SC-TOK-01..04), `tests/test_tax_year_boundary_completeness.py` (extended, new test added)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-08 | `tests/e2e/shadcn-token-remaining-families.spec.js` | Playwright coverage for 5 of 7 remaining shadcn token families (`ring`, `accent`, `destructive`, `border` — new; `popover` — cross-referenced from existing `modal-theming-token-conversion.spec.js` SC-MTC-05/06). `card` and `secondary` have zero reachable live call sites (verified via exhaustive grep + a minimal `tailwindcss` build empirically confirming which classes win CSS-cascade conflicts against hardcoded overrides) — code-reviewed only, `BLG-FE-160` filed. | See `stage4_backlog_slice.md#ST-08` | Pass with notes | None — `BLG-FE-160` is a scoped future-work item (no live call site to test against today), not a spec deviation |
| ST-09 | `tests/test_tax_year_boundary_completeness.py` | New test (`test_boundary_row_from_mocked_db_cursor_appears_exactly_once_in_correct_years_report`) mocking `get_trade_history_by_tax_year()`'s DB cursor (not the function itself, per the AC's own wording) with a fabricated boundary-day row, exercising the full real chain through `get_tax_year_report()` and asserting the row appears exactly once in the correct year's real `trades` list, zero times in the adjacent year's. Ran locally via `backend/.venv/bin/python3 -m pytest` — passes (4/4 in the file, including the 3 pre-existing v8.6 tests, no regressions). | See `stage4_backlog_slice.md#ST-09` | Pass | None found — all stories' deviation checks completed with nothing to file |

**Requirement (OA-3/ST-03) AC coverage check:** ST-08's 7-family AC — 5 rows covered by Playwright (ring, accent, destructive, border directly; popover by cross-reference), 2 families (card, secondary) explicitly named as unmet-this-cycle in the row above and in `BLG-FE-160`, not silently absent. ST-09's AC — covered in the row above (Pass, locally verified).

**QA test coverage:**
- Scenarios run: `tests/e2e/shadcn-token-remaining-families.spec.js` (SC-TOK-01..04 — **not executed locally**, see Sandbox Execution Limitation below); `tests/test_tax_year_boundary_completeness.py` (4/4 passing, executed locally via `backend/.venv/bin/python3 -m pytest`)
- Regression areas checked: `tests/e2e/modal-theming-token-conversion.spec.js` (cross-referenced, not modified); `backend/services/reports_service.py`, `backend/database.py` (read-only, no code changes — test-only story)
- Known deviations: None found — all stories' deviation checks completed with nothing to file

---

## Sandbox Execution Limitation — ST-08 Playwright Tests (disclosed, not silently assumed passing)

This execution sandbox's OS (`ubuntu26.04-x64`) is not supported by Playwright 1.58.2 (`npx playwright install chromium` fails with "ERROR: Playwright does not support chromium on ubuntu26.04-x64") — the new Playwright spec (`shadcn-token-remaining-families.spec.js`) could not be run locally in this session, unlike `test_tax_year_boundary_completeness.py` (pure Python, no browser dependency, run and confirmed passing above).

Mitigations applied given this constraint:
- `npx playwright test --list` confirms the file parses correctly and all 4 scenarios are discovered (no syntax errors).
- `npx eslint` run against the file — the only findings (`no-undef` on `require`/`window`) are a pre-existing repo-wide gap in the `tests/e2e/` ESLint config, confirmed identical on the already-merged `modal-theming-token-conversion.spec.js`, not specific to this new file.
- Every selector, mock route, and navigation helper was manually traced against the actual source it targets (see the spec file's own header comment for the full live-call-site audit methodology, including a minimal `tailwindcss` build used to empirically resolve a CSS-cascade-override question rather than assume an answer).
- One logic error was caught and fixed during this manual trace (SC-TOK-02's original draft read the "unfocused" comparison item's background *before* moving keyboard focus, when Radix Select actually auto-focuses the initially-selected item on open — the comparison would have been focused-vs-focused, not unfocused-vs-focused. Corrected to read both backgrounds after the keyboard move.)

**This is not equivalent to a real CI pass.** Per the LL-v8.3-P3-02 precedent (a sandboxed-pass is not a fully reliable predictor of real-CI Playwright outcomes), the actual pass/fail result for SC-TOK-01..04 will only be known once `quality_gate.yml` runs against PR #<TBD — filled at PR open>. **Action required before this EPIC's sign-off is treated as final:** re-check the real GitHub Actions run for this PR and record the outcome (run URL/SHA, or the specific fix applied if a test needed correction) in this file's sign-off Comments field before merge.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec — ST-09 verified via local pytest run; ST-08's 5 covered families verified via manual code-trace (real CI run pending, see limitation above); ST-08's 2 uncovered families (card, secondary) explicitly disclosed, not silently treated as met
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] No frontend component modified by this EPIC (test-file-only changes; `src/components/**`/`src/pages/**` untouched) — URL-base-variable check not applicable
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-13
- Comments: **PENDING — update after real CI run confirms SC-TOK-01..04 on PR #<TBD>.** ST-09 (`test_tax_year_boundary_completeness.py`) independently confirmed passing locally, 4/4, no regressions. ST-08's Playwright coverage is authored and statically verified (parses, lints consistently with existing precedent, every selector/mock manually traced against source) but not executed in this sandbox (Playwright unsupported on this sandbox's OS) — real-CI confirmation is the outstanding condition for full sign-off, per the frontend testing gate's own standard (execution_prompt.md §3.2.A) and the LL-v8.3-P3-02 precedent that a sandboxed pass is not a substitute for an observed real-CI pass.

