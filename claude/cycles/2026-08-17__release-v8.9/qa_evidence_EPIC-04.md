Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-18

# QA Evidence Log — EPIC-04 (Test Coverage & QA Hardening)

**EPIC:** EPIC-04 — Test Coverage & QA Hardening
**Cycle:** 2026-08-17__release-v8.9
**Sprint goal:** Ship v8.9: eliminate the two live risk-management stop-price defects on open positions (breakeven-floor ratchet, currency-basis mismatch) and deliver the sector-aware position sizing, pre-commit risk simulator, AI post-trade debrief, and in-app backtesting foundations of the Trade Intelligence Expansion — while clearing this cycle's reliability, QA, ops, and governance debt.
**Test scenarios used:** `tests/test_job_registration_screener_risk_off.py` (4 scenarios, new); `tests/test_trade_plan_setup_type_default.py` (4 scenarios, new); `tests/test_service_layer_direct_coverage.py` (32 scenarios, new); `tests/e2e/whats-new-panel.spec.js` SC-WN-06 (1 scenario, new — appended to existing 5)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-12 | `backend/routers/screener.py`; `backend/main.py#risk_off_alerts_endpoint` | Added `tests/test_job_registration_screener_risk_off.py` (4 tests) covering success + error paths for both `record_nightly_job("screener_refresh", ...)` and `record_nightly_job("risk_off_alerts", ...)` call sites. | Tests added covering success + error paths for both `screener_refresh` and `risk_off_alerts`; QA & Testing Owner sign-off | Pass | None |
| ST-13 | `docs/specs/api_contracts/trade_plan_endpoints.md#Request Body Fields` | Agent-mediated Product Owner decision: normalize null/absent/empty `trade_plans.setup_type` to the existing canonical value `"Other"` server-side, in `create_plan()`'s `_create()` closure (`backend/routers/trade_plans.py`). Covers every creation path (frontend and direct API) at the single choke point. 4 new regression tests. Doc updated v0.12→v0.13. | Decision recorded (required field vs. default value vs. accept-as-is with documented rationale); if a fix is chosen, implemented; Product Owner sign-off | Pass | None |
| ST-14 | `docs/ops/backend_service_layer_test_coverage_report_2026-08-16.md` | Added `tests/test_service_layer_direct_coverage.py` (32 tests) — direct unit tests exercising non-trivial calculation/branching logic in all 4 previously-uncovered modules: `cash_service` (balance arithmetic, validation), `compliance_service` (ATR-ratio/risk-amount calculations, aggregation), `news_service` (credential gating, retry/status-code branching), `validation_service` (`_check`/`_by_severity` — the exact BLG-TECH-02/03 production KeyError logic). | All 4 modules have at least one direct unit test exercising non-trivial logic (not just an HTTP-level smoke test); QA & Testing Owner sign-off | Pass | None |
| ST-15 | `docs/specs/frontend/pages/dashboard.md#§6A`; `tests/e2e/whats-new-panel.spec.js` | Added `SC-WN-06` to the existing `whats-new-panel.spec.js` — end-to-end proof that `changelog_service.py`'s curated `User Impact` column text (not `Description`, not a generic placeholder) renders correctly in `WhatsNewCard` in the browser. | Playwright test added and passing in CI; QA & Testing Owner sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_job_registration_screener_risk_off.py` (4/4 pass, new), `tests/test_trade_plan_setup_type_default.py` (4/4 pass, new), `tests/test_service_layer_direct_coverage.py` (32/32 pass, new) — full backend suite `backend/.venv/bin/python3 -m pytest tests/` 1210 passed / 5 skipped, 0 failed, 0 regressions (final run after all 4 stories). `npx playwright test tests/e2e/whats-new-panel.spec.js` 6/6 pass (5 pre-existing + SC-WN-06 new).
- Regression areas checked: `backend/routers/screener.py`/`backend/main.py` job-registration call sites (both success and error paths, now regression-covered); `backend/routers/trade_plans.py::create_plan()` (`setup_type` default does not override an explicit client value, confirmed by dedicated test); `cash_service`/`compliance_service`/`news_service`/`validation_service` core logic (previously zero direct coverage, now regression-guarded); `WhatsNewCard.js` rendering path (confirmed by agent-mediated mutation testing that SC-WN-06 fails on a broken render, not vacuous).
- Known deviations: None found — all four stories' deviation checks completed with nothing to file.

**Frontend testing gate (execution_prompt.md §3.2.A):** ST-15 adds Playwright coverage for an existing, unmodified component (`WhatsNewCard.js` itself was not changed — only new test coverage was added). No story in this EPIC creates or modifies any file under `src/pages/**` or `src/components/**`. SC-WN-06 satisfies the observable-AC coverage requirement for the User Impact rendering behaviour it documents.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no story in this EPIC constructs URLs directly

> **Mixed-Class EPIC Signer Format (ST-11 / LL-v5.2-P4-01):** EPIC-04 contains both a `delegated_decision` story (ST-13) and `autonomous` stories (ST-12, ST-14, ST-15) — agent-mediated format required. (The `delegated_decision` classification also independently disqualifies the BLG-GOV-19 autonomous class per its own criterion 1.)

- Signed off by: Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3)
  Sprint Execution Engine (agent-mediated, Product Owner role — §5.3)
- Date: 2026-08-18
- Comments: Story-level sign-offs provided by QA & Testing Owner (ST-12, ST-14, ST-15) and Product Owner (ST-13), agent-mediated per §5.3 — see below. ST-13 was raised as escalation ESC-EXEC-20260818-01 (delegated_decision) and resolved same-session, well within the 24h SLA. All four stories Approved on first pass; reviewed and acknowledged in aggregate — all acceptance criteria met, no unresolved P0/P1 gaps.

### Story-level authority sign-off (BLG-GOV-14 — required in addition to, not instead of, the EPIC-level block above)

**QA & Testing Owner** (ST-12, ST-14, ST-15):
- Signed off by: Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3)
- Date: 2026-08-18
- Comments: ST-12 Approved — verified the 4 tests genuinely exercise the real `record_nightly_job()` call sites; confirmed not vacuous by temporarily breaking an assertion (wrong job name) and confirming the failure occurred on the value comparison, proving `BackgroundTasks` executes synchronously before `TestClient.post()` returns. ST-14 Approved — hand-verified `compliance_service` arithmetic across multiple tests (all correct); empirically confirmed the `validation_service` `_by_severity` test would have caught the documented BLG-TECH-02/03 production `KeyError` by reverting to direct indexing, reproducing the exact error, and restoring. ST-15 Approved — confirmed SC-WN-06's fixture text is byte-identical to `test_changelog_service.py`'s `SAMPLE_CHANGELOG` User Impact cell (meaningfully distinct from `Description`-column/generic-placeholder style); confirmed not vacuous via mutation testing (broke `WhatsNewCard.js`'s rendering, confirmed the test correctly failed, reverted); confirmed CI coverage via `playwright.yml`'s automatic glob discovery.
- Known deviations: None found for ST-12, ST-14, or ST-15.

**Product Owner** (ST-13):
- Signed off by: Sprint Execution Engine (agent-mediated, Product Owner role — §5.3)
- Date: 2026-08-18
- Comments: Approved. Decision: normalize null/absent/empty `setup_type` to the existing canonical value `"Other"` server-side. Rationale grounded in reading the actual code: `"Other"` already exists as the 6th canonical `SETUP_TYPE_OPTIONS`/`SETUP_TYPES` value in both backend and frontend, so this costs nothing in new UI/enum/spec, and applying it server-side (not just in the frontend form) covers direct API use too — which a required-field frontend change alone would not reach. Confirmed this does not trigger a design-gate return per sprint_backlog.md's RISK-04 note (no new UI pattern; `Other` is already a live, selectable dropdown option on this exact form).
- Known deviations: None found.
