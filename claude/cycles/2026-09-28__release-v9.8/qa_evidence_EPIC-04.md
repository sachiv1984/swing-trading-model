Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-29

---

## Consolidation Block

**EPIC:** EPIC-04 — Operations & Security Hardening
**Cycle:** 2026-09-28__release-v9.8
**Sprint goal:** Clear the full v9.8 full-capacity debt slice — 39 stories across 6 EPICs spanning frontend/UX consistency, backend reliability, QA/test coverage, operations/security hardening, spec & API contract debt, and governance/process debt — with no anchor feature, at exactly the top of the confirmed ~24–28 day sprint capacity band.
**Test scenarios used:** tests/test_non_registry_dependency_check.py, tests/test_health_response_schema.py, tests/test_staging_smoke_test.py

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-17 | docs/specs/api_contracts/health_endpoints.md; docs/ops/staging_deploy_notes.md | `deployed_commit_sha` added to `GET /health/detailed` (Render `RENDER_GIT_COMMIT`, falling back to local `git rev-parse HEAD`); `staging-smoke-test.yml` extended (`EXPECTED_COMMIT_SHA: ${{ github.sha }}`) to compare it against the merged commit on every scheduled run and fail/alert on mismatch (`scripts/staging_smoke_test.py`'s `check_deployed_commit()`). | "A merge to `main` that should have redeployed staging but did not produces a visible failure or alert"; "The check and its trigger are documented, including the known limits of what can be verified from the repo alone" | Pass_with_deviation | BLG-OPS-171 (staging-only evidence that the alert fires on a real stale-staging condition — cannot be reproduced in CI; deferred per `sprint_backlog.md` ST-17 Notes / CLAUDE.md §2 analogue) |
| ST-18 | docs/infrastructure/staging_setup.md | §8 gained a pre-approved query-pattern allow-list: `SELECT COUNT(*)`-shaped aggregates (no row-level columns) against a table already named in an existing `current_roadmap.md` gate condition — today `trade_history`/`trade_plans` (SI-02's own gate query). Documentation-only. | "`docs/infrastructure/staging_setup.md` §8 states which query patterns a governed session may run against the staging read-only role without seeking additional confirmation each time" | Pass | None |
| ST-19 | scripts/check_non_registry_dependencies.py | Hardened against every form BLG-SEC-39 named as missed (pip `git+http`/`hg+`/`svn+`/`bzr+` any transport, bare VCS schemes, direct URL references, bare URL lines, relative/absolute local paths, `-r`/`--requirement` includes; npm `github:` prefix, bare `user/repo` shorthand, tarball URLs); fixed the reported trailing-comment false positive; added `package-lock.json` scanning (previously unscanned). | "Each missed form above is rejected by a test, and the trailing-comment line is accepted"; "`main()` exits non-zero on a violation and zero on the current repo tree, asserted by a test" | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_non_registry_dependency_check.py` (32 tests — every missed form individually, the trailing-comment acceptance case, `main()`'s exit code), `tests/test_health_response_schema.py` (5 new tests — `deployed_commit_sha` schema/derivation), `tests/test_staging_smoke_test.py` (9 new tests — `check_deployed_commit()` and its `main()` wiring). Full backend suite (`tests/`, excluding `tests/e2e/`) re-run after all 3 stories: 1941 passed, 12 skipped, 0 failed.
- Regression areas checked: OpenAPI/contract drift (`scripts/check_openapi_drift.py` — PASSED, 147/147/147), API performance baseline drift (`scripts/check_api_performance_baseline_drift.py` — PASSED), backend routers/health endpoints, dependency-guard CI gate (`.github/workflows/non-registry-dependency-check.yml`), staging smoke-test workflow (`.github/workflows/staging-smoke-test.yml`).
- Known deviations: ST-17's AC-01 staging-only evidence deferred to `BLG-OPS-171` (see table above) — all other deviation checks completed with nothing to file.

**Incidental finding (not a deviation of this EPIC's own work):** `BLG-QA-203` filed — `tests/test_api_contracts.py::TestReportsEndpoints::test_get_tax_year_report_returns_ok` fails when run in isolation but passes as part of the full suite (test-order dependency), pre-existing and unrelated, found while checking ST-17 for regressions.

**Delegation note:** ST-17 and ST-18 were both sealed as `delegated_decision` in `sprint_backlog.md` (RISK-01 design-decision-vehicle choice for ST-17; a security-sensitive staging-DB query policy call for ST-18) — neither was engine-determinable. Both were escalated per STEP 3.1.D (`ESC-EXEC-20260929-01`/`-02`, `execution_escalations.md`) and resolved in-session by the Infrastructure & Operations Owner via `AskUserQuestion` (2026-09-29T12:35:00Z), then reclassified `autonomous` and implemented. See `execution_escalations.md` for the full resolution record.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations (ST-17's single deviation is P3-equivalent, staging-only-evidence class, tracked via `BLG-OPS-171`)
- [x] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via `api.*` wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend-visible change in this EPIC
- Signed off by: Director of Quality
- Date: <fill in — must be non-blank>
- Comments:

**Autonomous class eligibility check (BLG-GOV-19) — not applicable, standard sign-off used:**
- Criterion 1 (all stories `autonomous`): ✓ — met, but see Criterion 2.
- Criterion 2 (all AC verifiable by code review alone, no staging run required): ✗ — ST-17's own AC-01 explicitly carries a `[staging-only evidence]` tag per `sprint_backlog.md`; confirming the alert fires on a real stale-staging condition requires a staging run (deferred to `BLG-OPS-171`), so this criterion is not met and the BLG-GOV-19 autonomous class does not apply to this EPIC.
- Criterion 3 (no frontend-visible change): ✓ — no story touches `src/components/**` or `src/pages/**`.
