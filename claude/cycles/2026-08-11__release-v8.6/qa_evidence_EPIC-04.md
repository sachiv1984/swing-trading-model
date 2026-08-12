Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-12

# QA Evidence Log — EPIC-04 (Financial-Correctness & QA-Coverage Carryover)

**EPIC:** EPIC-04 — Financial-Correctness & QA-Coverage Carryover
**Cycle:** 2026-08-11__release-v8.6
**Sprint goal:** Ship all 26 scoped v8.6 stories — trade-plan completion-rate tracking and an AI-assisted order-placement thesis digest, trade-plan-to-position linkage enforced with a DB-level integrity safeguard, the remaining shadcn design-token and secondary-text drift debt closed, and the financial-correctness, QA-coverage, and governance-debt carryover from v8.5 fully resolved
**Test scenarios used:** `tests/test_screener_batch_service.py`, `tests/test_tax_year_boundary_completeness.py`, `tests/test_multi_currency_cost_basis_rounding_audit.py`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-11 | `tests/test_screener_batch_service.py` | Corrected `get_regime_distribution()`'s docstring, which claimed a NULL-exclusion behaviour that is unreachable (`run_screener()` always substitutes a real `risk_off` string on regime-fetch failure, never persists NULL). Added `test_run_screener_persists_risk_off_not_null_on_regime_fetch_failure` covering the real fetch-failure path. | Docstring matches actual behaviour; test covers the real failure scenario | Pass | None |
| ST-12 | `docs/specs/data_model.md`, `docs/product/decisions/multi-currency-cost-basis-rounding-audit--2026-08-12.md` | Systematic multi-currency cost-basis rounding audit across `add_position()`, `exit_position()`, and `reports_service.py`'s P&L consumers. Found the delegation's own starting hypothesis (US-vs-UK entry-side asymmetry) does not survive `NUMERIC(12,2)` DB rounding; the real rounding source is market-symmetric (partial-exit proportional allocation), quantified and tested as bounded (≤£0.02 worst-case, non-compounding). | Audit complete (systematic); any inconsistency found is fixed or documented as immaterial with a quantified bound; Financial Reporting & Records Owner sign-off recorded | Pass with notes | None — documented-as-immaterial is a valid AC outcome per the delegation's own criterion (b) |
| ST-13 | `tests/test_tax_year_boundary_completeness.py` | New regression tests exercising the real `get_tax_year_report()`/`get_trade_history_by_tax_year()` to prove no gap/overlap between adjacent tax years and no omission/double-count for a trade exiting exactly on a boundary day; confirmed the CSV export path transitively covered. | No boundary gap/overlap/omission found or all found are fixed | Pass | Non-blocking finding filed as `BLG-QA-148` (mocked-row end-to-end assertion vs current real-bounds composition) |
| ST-14 | `.github/workflows/dependency-vuln-rescan.yml`, `scripts/check_dependency_vuln_rescan.py` | `check_dependency_vuln_rescan.py` now emits distinguishable `pip_audit_status`/`npm_audit_status` (`ok`/`failed`), and the workflow fails the job visibly when either audit tool didn't produce a usable result, instead of silently reporting "0 findings" for a failed scan. | All 4 named scenarios (missing pip-audit file, non-JSON npm output, npm missing-lockfile error, true 0-findings control) produce distinguishable, correct output | Pass | None — automated unit test coverage for the script deferred to EPIC-05/ST-17 (already separately scheduled this sprint), per this story's own AC being satisfied by the behavioural fix + manual verification of all 4 scenarios |

**QA test coverage:**
- Scenarios run: `tests/test_screener_batch_service.py` (20 tests, ST-11), `tests/test_tax_year_boundary_completeness.py` (ST-13), `tests/test_multi_currency_cost_basis_rounding_audit.py` (5 tests, ST-12); full backend suite `tests/` (1071 passed, 5 skipped, 0 failed) confirmed no regressions across all 4 stories.
- Regression areas checked: none of the 4 stories altered any existing calculation or persisted value (ST-11/ST-14 are behaviour-preserving documentation/observability fixes; ST-13 is test-only; ST-12 is audit-only, no code change). No pre-existing tests required updates.
- Known deviations filed: `BLG-QA-148` (ST-13, non-blocking). ST-14's deferred automated unit coverage is tracked by the already-scheduled EPIC-05/ST-17, not a new backlog item.

**Agent-mediated review trail (2026-08-11 to 2026-08-12):**
1. **Financial Reporting & Records Owner** (ST-13, 2026-08-11): CONFIRMED. Residual non-blocking finding filed as `BLG-QA-148`.
2. **Financial Reporting & Records Owner** (ST-12, 2026-08-12, independent subagent invocation): first pass **NOT CONFIRMED** — one blocking finding: `tests/test_multi_currency_cost_basis_rounding_audit.py`'s docstring cited a nonexistent `docs/specs/data_model.md` "DS-13" entry and a stale test function name instead of the actual decision-record file and real test names. Remediated in-session (docstring corrected; added an explicit caveat that the Postgres round-vs-truncate claim rests on documented semantics, not live-verified behaviour, since this sandbox has no Postgres access). The reviewer independently re-derived the rounding mechanism across a much wider parameter sweep (share counts to ~20,000, position sizes to £5,000,000) and confirmed the audit's ≤£0.02 bound is conservative — real worst-case drift is far smaller — and confirmed the audit is genuinely systematic (it disproves rather than rubber-stamps the delegation's own starting hypothesis).

**Director of Quality** (this sign-off): confirms both remediated Financial Reporting & Records Owner findings are resolved by direct inspection of the diffs, and that ST-11/ST-14 (already-`done` autonomous-class stories, reviewed at completion time in this same session) show no unresolved issues. Full backend suite green post-remediation.

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked — full backend suite green (1071 passed, 5 skipped)
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, backend-only EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-12
- Comments: Standard sign-off block used (BLG-GOV-19 autonomous class does not apply — ST-12 is `delegated_backend`, failing Criterion 1). Joint with the Financial Reporting & Records Owner's domain-correctness reviews above (agent-mediated, §5.3) for ST-12 and ST-13, both required per those stories' own unblock/AC criteria. Product Owner acceptance remains outstanding as a separate, always-human merge-gate condition.
