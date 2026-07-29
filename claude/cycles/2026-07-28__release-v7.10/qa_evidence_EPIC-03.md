Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-29

# QA Evidence — EPIC-03 (QA & Test Infrastructure Hardening)

**EPIC:** EPIC-03 — QA & Test Infrastructure Hardening
**Cycle:** 2026-07-28__release-v7.10
**Sprint goal:** Materially reduce the platform's production risk surface — closing silent backend error-masking, hardening security posture (secrets scanning, rate-limit and exception hygiene), strengthening QA/CI infrastructure, correcting API contract debt, and clearing a first tranche of frontend technical debt — by delivering all 23 in-scope v7.10 hardening items within the confirmed capacity band.
**Test scenarios used:** `tests/test_red_flag_journal.py` (ST-10); the real `playwright.yml` CI workflow (ST-09, all 4 shards + visual snapshots); `scripts/check_consumer_contract_drift.js` (ST-12, scripted check, not a pytest/Playwright suite)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-09 | `docs/ops/e2e_production_build_migration_2026-07-29.md` | `playwright.config.js`'s `webServer.command` is now CI-conditional: production build+serve (`npx serve`, pinned exact devDependency) in CI, `npm start` locally. Found and fixed 2 build-breaking issues during implementation (CI=true lint-as-error; homepage-subpath asset-path mismatch) before pushing. | CI E2E job builds and serves a production bundle with REACT_APP_* vars injected at build time; static-serve dependency added and pinned; webServer.command CI-conditional; full 677-test suite passes in CI (RISK-04) | Pass | None |
| ST-10 | N/A (regression test, no prior canonical spec) | Auth-required regression test for `GET /portfolio/red-flag-journal` (401 no key, 401 wrong key, 200 valid key). Verified the negative tests actually fail when auth is removed (temporarily confirmed locally, reverted). | Auth-required regression test added; passes in CI; fails if auth check is removed | Pass | Deviation from literal AC file-path wording — see execution_state.json ST-10 notes |
| ST-11 | `docs/ops/endpoint_test_coverage_audit_2026-07-29.md` | Audited all 128 routes against `test.py`'s `test_cases`. 7 safe gaps fixed, 2 deliberately excluded with documented rationale. Fallback count kept in sync (102→109) per the existing drift-detection CI gate. | Audit of `test.py` coverage against every `@router.*` decorator; any gap filed or fixed | Pass | None |
| ST-12 | `docs/ops/consumer_contract_check_2026-07-29.md`, `scripts/check_consumer_contract_drift.js` | New scripted consumer-driven contract check. First run's 14 findings individually triaged: 1 genuine gap found and fixed (`GET /portfolio` missing 2 documented fields), 13 confirmed false positives from disclosed script limitations. | Lightweight contract check implemented; first run's findings triaged | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_red_flag_journal.py` (10 passed, including 3 new auth tests). Real `playwright.yml` CI run on the ST-09 push: all 4 E2E shards + visual snapshots succeeded against the production-served build — direct evidence for RISK-04, not a simulated/local-only claim. `scripts/check_consumer_contract_drift.js` run manually (not yet wired into a CI job — "scripted" satisfies this story's AC, per its own "CI or scripted" wording).
- Regression areas checked: full backend suite re-run after every story (868 passed, 2 skipped throughout — no backend code was touched by any of these 4 stories). `git status` confirmed clean after every local build/serve/auth-removal dry run (no stray build artefacts or reverted-test residue left behind).
- Known deviations filed: ST-10's departure from BLG-QA-96's literal "backend/routers/test.py" file-path wording, documented in the commit message and `execution_state.json` (the literal instruction is structurally incompatible with a missing-key negative test; the actual pytest home for this endpoint's tests was used instead, matching an established codebase pattern).

**Notable finding this EPIC:** ST-09's implementation work surfaced two genuine build-breaking issues (CI=true ESLint-as-error, homepage subpath) that would have silently broken the entire Playwright E2E pipeline had the naive interpretation of the story been shipped — both were found and fixed via local dry runs before any CI push, then independently confirmed by the real CI run succeeding.

---

## Sign-Off Block

**Eligibility note:** all four stories are classified `autonomous`. ST-09 and ST-10 name no specific sign-off authority in their acceptance criteria (BLG-QA-127 and BLG-QA-96 respectively) — covered under the autonomous-class default. ST-11 and ST-12 name "QA & Testing Owner" and "API Contracts & Documentation Owner" respectively — agent-mediated named-role format used for those two, consistent with `qa_evidence_EPIC-01.md`/`qa_evidence_EPIC-02.md`'s precedent this cycle.

- [x] All acceptance criteria verified against canonical spec (or documented as not-applicable)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] No frontend-visible/observable-UI change in this EPIC requiring Playwright/staging sign-off beyond the existing suite (ST-09 changes CI plumbing only, does not alter any page's rendered output)
- Signed off by:
  Sprint Execution Engine (autonomous class) — ST-09, ST-10
  Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3) — ST-11
  Sprint Execution Engine (agent-mediated, API Contracts & Documentation Owner role — §5.3) — ST-12
- Date: 2026-07-29
- Comments: 4/4 stories Pass. ST-09's real CI run succeeding (not merely a local simulation) is the strongest evidence in this EPIC — RISK-04 is genuinely, not just plausibly, satisfied.
