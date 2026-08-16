Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-16

# QA Evidence Log — EPIC-04 (Quality & Test-Coverage Debt)

**EPIC:** EPIC-04 — Quality & Test-Coverage Debt
**Cycle:** 2026-08-14__release-v8.8
**Sprint goal:** Close the two live P1 data-integrity gaps (stale screener refresh, stuck RISK OFF badge) and ship the full v8.8 debt-closure slice — 29 stories across 7 EPICs — within the confirmed ~24–28 day capacity band.
**Test scenarios used:** tests/test_router_test_registration_check.py (12 scenarios, incl. 2 new regression tests for ST-21's fix); full backend suite (1160 passed / 5 skipped) as regression coverage for the script-level fix

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-18 | `docs/ops/arc6_prerequisite_field_population_audit_2026-08-16.md` | Audited `regime_context_at_entry` (structurally near-guaranteed — auto-derived from `GET /market/status` at submission, read-only in the UI, no gap) and `setup_type` (real gap — only defaults via the linked-watchlisted-signal pre-population path; all other creation paths save `null`). Live check: production `GET /trade-plans` currently has 0 rows (disclosed, not a population-rate measurement). | Audit complete; gaps fixed or filed; QA & Testing Owner sign-off | Pass | None — gap filed (`BLG-QA-150`), not a spec deviation |
| ST-19 | `docs/ops/backend_service_layer_test_coverage_report_2026-08-16.md` | Audited all 40 `backend/services/*.py` modules (2 independent grep passes); 35/40 (87.5%) have direct unit test coverage. 5 zero-coverage found: `cash_service`, `compliance_service`, `news_service`, `trade_csv_service`, `validation_service`. 4 are real test gaps (filed `BLG-QA-151`); `trade_csv_service`'s `build_trade_history_csv` found to be dead/duplicate code (a second, differently-signatured function of the same name in `trade_service.py` is the one actually wired to a router) — not a test gap, filed `BLG-BE-101`. | Report generated; gaps triaged; QA & Testing Owner sign-off | Pass | None |
| ST-20 | `docs/ops/test_environment_parity_check_2026-08-16.md` | Compared local/CI/staging across Python version, Node version, DB engine, frontend env vars. Real drift found: local dev Python 3.14.4 vs CI (all 4 workflows) and staging (`render.yaml`) both pinned 3.11 — no `.python-version` file anywhere in the repo. DB engine and Node version confirmed consistent. `.env.production` missing `PUBLIC_URL` present in staging/`render.yaml` — flagged as advisory-only (production env vars are dashboard-only, not repo-visible, so unconfirmed rather than asserted as a defect). Production itself explicitly out of repo-comparable scope (disclosed, not silently skipped). | Audit complete; drift fixed or documented as intentional; QA Lead sign-off | Pass | None — gap filed (`BLG-OPS-146`), not a spec deviation |
| ST-21 | `docs/ops/endpoint_test_coverage_audit_2026-08-16.md` | Re-derived all 84 `@router.*` routes independently of the July 2026 audit; 8 uncovered — 7 re-confirmed as already-documented mutation-risk exclusions, 1 genuine undocumented gap (`PATCH /notifications/preferences`, predates the audit that introduced the exclusion comment but was missed by it) fixed via `test.py` comment update. Also found and fixed 2 compounding regex bugs in the enforcement script itself (`scripts/check_router_test_registration.py`) — the path-capture group required 1+ chars, silently failing to match `@router.get("")`-style empty-path decorators, and a downstream trailing-slash bug that would have false-flagged even a correctly-registered empty-path route once the first bug was fixed. 2 new regression tests added. | Re-audit complete against all `@router.*` decorators; any gap fixed; QA & Testing Owner sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_router_test_registration_check.py` (12 tests, 2 new for ST-21); full backend suite `backend/.venv/bin/python3 -m pytest` (1160 passed / 5 skipped, 0 regressions); `python3 scripts/check_router_test_registration.py` and `python3 scripts/check_api_performance_baseline_drift.py` both pass with no staged changes.
- Regression areas checked: router-registration enforcement script (ST-21's own fix area), full backend service layer (ST-19's audit scope), no frontend changes in this EPIC.
- Known deviations: None found — all 4 stories' deviation checks completed with nothing to file (each finding was either fixed directly or filed as a backlog item, not a spec deviation — none of these stories has a governing canonical spec to diverge from; they are audit/QA-process stories per `execution_prompt.md` §3.1.A Case E).

**No frontend-visible changes in this EPIC** — `src/pages/` and `src/components/` untouched by all 4 stories. The `execution_prompt.md` §3.2.A frontend testing gate does not apply.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend changes in this EPIC

> **Delegated-QA sign-off pattern (BLG-GOV-69/74) — Format (i), individual sign-off:**

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: PENDING
- Comments: PENDING — story-level sign-offs from QA & Testing Owner (ST-18, ST-19, ST-21) and QA Lead (ST-20) pending below; EPIC-level DoQ acknowledgement to follow once both are recorded.

### Story-level authority sign-offs (BLG-GOV-14 — required in addition to, not instead of, the EPIC-level block above)

**QA & Testing Owner** (ST-18, ST-19, ST-21):
- Signed off by: PENDING
- Date: PENDING
- Comments: PENDING

**QA Lead** (ST-20):
- Signed off by: PENDING
- Date: PENDING
- Comments: PENDING
