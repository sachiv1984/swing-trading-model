Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-10

# QA Evidence — EPIC-01 (Production Correctness Fixes)

**EPIC:** EPIC-01 — Production Correctness Fixes
**Cycle:** 2026-08-08__release-v8.5
**Sprint goal:** Clear the full ready frontend-correctness, design-consistency, and security-hardening slate across all 25 scoped stories — see `sprint_goal.md`
**Test scenarios used:** `tests/test_trade_plan_tags.py`, `tests/test_api_contracts.py` (trade_plan-scoped subset), `tests/test_api_key_cross_environment.py`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-01 | `docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/tag-performance` | Added missing `ensure_trade_plans_table()` call to `get_tag_performance_endpoint()` in `backend/routers/analytics.py`, matching the pattern every `trade_plans.py` route already uses. Root cause: on a staging DB predating the ST-05/v6.8 `trade_tags` migration, no `/trade-plans/*` route had ever run to lazily create the column, so this endpoint 500'd on "column trade_tags does not exist". | (1) `GET /analytics/tag-performance` returns 200/400/404 (not 500) on a DB where `trade_tags` was never ensured; (2) no regression to existing `trade_plans.py` endpoints' own `ensure_trade_plans_table()` calls; (3) root cause note added to `docs/ops/api_performance_baseline.md`'s entry for this endpoint, confirmed resolved and updated | Pass | None |
| ST-02 | `docs/security/api_key_security_register.md#6. Application X-API-Key`, `.github/workflows/api-key-cross-environment-check.yml` | Inspected the 2026-08-09 scheduled run's real log (run `31299858987`) and confirmed the check genuinely executes daily with real secrets (`STAGING_API_KEY` added 2026-08-08, confirmed via `gh secret list`) — not silently skipping. Found and fixed a different real gap surfaced live in that same log: a `PROD_API_URL` read timeout crashed `scripts/check_api_key_cross_environment.py` with an unhandled exception, which the workflow's alert step could not distinguish from a genuine cross-wired-keys finding — both produced a non-zero exit code, so a transient network timeout triggered a false-positive "keys cross-wired" Telegram alert. Hardened: `probe()` now returns `None` on network/timeout error (never conflated with a real finding); three distinct exit codes (0=OK, 1=CROSS-WIRED, 2=ERROR); missing-secrets skip-guard now fails loud instead of silently exiting 0; two separate, distinctly-worded alert steps route on exit code. | (1) Confirmed via a real run's log that the comparison is executing, not skipping; (2) decision recorded on whether the skip-guard's silent-pass behaviour should be hardened, and if so, implemented | Pass | None |

*(All ACs for both ST items appear in the table above — no AC addressed only in narrative.)*

**QA test coverage:**
- Scenarios run: `tests/test_trade_plan_tags.py` (14 passed), `tests/test_api_contracts.py -k trade_plan` (46 passed, includes `TestTradePlanEndpoints`), `tests/test_api_key_cross_environment.py` (8 passed — 4 pre-existing + 4 new covering the probe-error/exit-code hardening)
- Regression areas checked: `trade_plans.py` route family (all still call their own `ensure_trade_plans_table()` unchanged); `api-key-cross-environment-check.yml` YAML validated with `yaml.safe_load`; live GitHub issue auto-close confirmed for both ST items (#1301, #1302 both `CLOSED` post-push)
- Known deviations filed: None

---

## Autonomous Class Sign-Off (BLG-GOV-19)

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-01 autonomous at planning; ST-02 reclassified `delegated_backend` → `autonomous` at execution time per the mid-sprint reclassification mechanic — the planning-time assumption of needing live external dashboard access did not hold, `gh api` against already-authenticated GitHub Actions job logs was sufficient)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ (ST-01 verified via unit/integration tests; ST-02 verified via GitHub Actions job-log inspection, not a product staging run)
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/components/**` or `src/pages/**` was created or modified — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-10
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous as of execution time, all AC code-review/test/log-verifiable, no frontend changes, engine signer populated). ST-02's reclassification rationale is recorded in `execution_state.json`'s `notes` field for that story.
