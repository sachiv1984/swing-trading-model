Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-30

# QA Evidence — EPIC-01 (Data Model & Spec Integrity)

**EPIC:** EPIC-01 — Data Model & Spec Integrity
**Cycle:** 2026-07-30__release-v8.0
**Sprint goal:** Close the platform's outstanding backend error-masking, security-hardening, and FX/data-spec debt while shipping keyboard/focus accessibility fixes to the Trade Plan flow, strengthening QA/CI test infrastructure, hardening operational alerting and disaster-recovery readiness, and fixing the recurring cross-EPIC `execution_state.json` merge-conflict pattern.
**Test scenarios used:** `tests/test_strategy_version_at_entry.py`, `tests/test_fx_audit_trail_completeness.py`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-01 | `docs/specs/data_model.md#DS-11` | Forward-only `strategy_version_at_entry` column on `trade_plans` and `positions`, stamped at row-creation time from `strategy_version_registry.get_current_strategy_version()`. | Migration added; field populated on new trade plans/positions at entry (forward-only, no backfill); `data_model.md` updated. | Pass | None |
| ST-02 | `docs/product/decisions/ds05-fx-handling-review--2026-07-30.md` | Documented review confirming the GBP/USD FX conversion path (`get_live_fx_rate`, Yahoo Finance) is fully decoupled from DS-05's Alpaca-first OHLCV/ATR routing for US tickers. | Review documented confirming no silent position-sizing miscalculation; `strategy_rules.md §4.1.5` confirmed accurate or amendment filed. | Pass | None — §4.1.5 confirmed accurate, no amendment required |
| ST-03 | `docs/product/decisions/fx-audit-trail-completeness-check--2026-07-30.md`, `docs/specs/api_contracts/portfolio_endpoints.md#POST /portfolio/position` (v2.6.0) | Audited every FX conversion code path against `strategy_rules.md §4.1.5`'s auditability requirement. Found and fixed 3 gaps: `POST /portfolio/position`, `GET /portfolio/prospective-heat`, and the `cash_constraint` check in `GET /portfolio/pre-entry-validation` each computed an FX rate but never returned it — all now return `fx_rate_used`. | Audit of all FX conversion code paths complete; any gap found is fixed; Financial Reporting & Records Owner sign-off. | Pass | None — 3 gaps found and fixed within this story per its own AC |

**QA test coverage:**
- Scenarios run: `tests/test_strategy_version_at_entry.py` (6 tests), `tests/test_fx_audit_trail_completeness.py` (8 tests) — all passing. Full backend regression suite re-run (`tests/`, 903 passed / 5 skipped) to confirm no regressions from the two response-shape additions and the new startup migration.
- Regression areas checked: trade-plan creation (`POST /trade-plans`, idempotency-key path), position entry (`POST /portfolio/position`), position sizing (`POST /portfolio/size`), prospective heat (`GET /portfolio/prospective-heat`), pre-entry validation (`GET /portfolio/pre-entry-validation`), red-flag override event write path.
- Known deviations filed: None.

**Backend-only EPIC note:** no `src/pages/**` or `src/components/**` files were created or modified by any story in this EPIC — confirmed via `git diff --name-only` against the branch's full changeset. No frontend-visible change; no staging run or Playwright coverage required.

---

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/components/**` or `src/pages/**` was touched — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-30
- Comments: Autonomous class sign-off — all four qualifying criteria met (all 3 stories autonomous, all AC code-review/test-verifiable, no frontend changes, engine signer populated). Story-level domain sign-offs also recorded: Data Model & Domain Schema Owner + Financial Reporting & Records Owner (ST-01, in `data_model.md` DS-11), Financial Reporting & Records Owner (ST-02 and ST-03, in the respective decision docs) — all agent-mediated per §5.3, pending human confirmation.
