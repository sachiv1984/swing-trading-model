Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-24

# QA Evidence Log — EPIC-11 (v7.7)

## Consolidation Block

**EPIC:** EPIC-11 — Automate endpoint-count drift check (CLAUDE.md §2)
**Cycle:** 2026-07-21__release-v7.7
**Sprint goal:** Ship the four design-gated Strategy Intelligence & Notification UX items and clear seven ready capacity-fill items to fully utilise this sprint's confirmed capacity.
**Test scenarios used:** tests/e2e/system-status.spec.js (SC-SS-01b, updated); local reproduction of both required verification cases (current-state-pass, synthetic-failure)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-11 | `.github/workflows/quality_gate.yml` | New "Endpoint Count Drift Check (ST-11)" job — parses `backend/routers/test.py`'s `test_cases` list via the `ast` module (exact; a naive regex over-counts due to a nested `"body": {"name": "__test__", ...}` payload and a separate `critical_tests` list) and compares its element count against `src/pages/SystemStatus.js`'s hardcoded `totalTests` fallback constant. Discovered and fixed a real pre-existing drift bug in the same commit: the fallback (103) was stale versus the true count (98) — corrected `SystemStatus.js` and `tests/e2e/system-status.spec.js`'s `SC-SS-01b` test to match. | Lint step added to `quality_gate.yml` counting endpoint totals vs. the hardcoded fallback constant; fails on a synthetic mismatch test case; passes on current repository state | Pass | None |

**QA test coverage:**
- Scenarios run: local reproduction of both required cases — current-state-pass (98 == 98, exit 0) and synthetic-failure (fallback temporarily set to 999, mismatch correctly detected, exit 1, then cleanly reverted) — both independently re-verified by agent-mediated review (not just the commit's own claims); `tests/e2e/system-status.spec.js` `SC-SS-01b` updated and confirmed to reference 98 consistently in title, comment, and assertion; `CI=false npm run build` confirmed clean
- Regression areas checked: independent AST recount confirmed 98 (not 103, 99, or any other regex-derived figure); whole-file naive regex was shown to over-count to 104, confirming the `ast`-based approach was the right implementation choice, not an arbitrary one
- Known deviations filed: None — the discovered drift was fixed directly in this same commit rather than deferred

**Frontend-visible change note:** `SystemStatus.js`'s displayed fallback text changes from "103" to "98" — an observable UI change. Covered by the existing (now-updated) `SC-SS-01b` Playwright test per CLAUDE.md's frontend testing gate; no new backlog item required since coverage already existed and was corrected in the same commit.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no URL construction involved (static fallback text change only)
- Signed off by: Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3)
- Date: 2026-07-24
- Comments: `SystemStatus.js` has a frontend-visible change (fallback text 103→98) — BLG-GOV-19 autonomous class does not apply (criterion 3 unmet, `src/pages/**` modified). The observable AC is Playwright-covered via the updated `SC-SS-01b` test. Human Director of Quality review and Product Owner acceptance still required before merge per §5.3 "Always-human gates".

---

## Sprint-Level Note

This is the eleventh and final EPIC completed this sprint (EPIC-01 through EPIC-11, all `status: done`, all PRs open). All eleven ST items (ST-01 through ST-11) now have `acceptance_verified: true` and `qa_signed_off: true` in `execution_state.json`. Remaining work before sprint close is the human merge-gate sign-off (Director of Quality + Product Owner) on each of the 11 open PRs (#1047–#1056 and this EPIC's PR), which the engine cannot perform itself per §5.3's always-human gates.
