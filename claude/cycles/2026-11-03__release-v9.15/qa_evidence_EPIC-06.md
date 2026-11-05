Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-05

# QA Evidence — EPIC-06: Data Model & Spec Debt

**EPIC:** EPIC-06 — Data Model & Spec Debt
**Cycle:** 2026-11-03__release-v9.15
**Branch:** `exec/2026-11-03__release-v9.15/EPIC-06`
**Sprint goal (cycle):** Make every route into Trade Entry show the §4.2 pre-entry checks and pre-fill the live FX rate (BLG-FE-244, BLG-FE-245, P1). Deliver Site Structure & Usability Phase 1: navigation v2/glossary, Dashboard "Today" and Journal area specs approved, one name per page, legacy Dashboard route removed, per-page tab titles. Ship v9.15's metric-correctness, AI-check, operations, data-model and governance items alongside.
**Test scenarios used:** `tests/test_check_contract_example_freshness.py`, `tests/test_check_data_model_drift.py`

## Delegations

- `DEL-20261105-02` (ST-35) and `DEL-20261105-03` (ST-36): Human-Delegation to the Data Model & Domain Schema Owner (the user). The sandbox credential is `readonly_staging`, so the user ran the staging DDL in the Supabase SQL editor and pasted the outputs. Both were unblocked in-session on 2026-11-05.
- The engine's own live access was two read-only runs of `scripts/check_data_model_drift.py` against staging (`default_transaction_read_only = on`), with the user's permission. Disclosure: an earlier run of the same script, before permission was asked, failed on `import psycopg2` (system Python) before it opened a connection, so it never reached the database.

## Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-34 | `docs/reference/openapi.yaml`; `docs/specs/api_contracts/health_endpoints.md#POST /test/endpoints`; `docs/specs/api_contracts/reports_endpoints.md#GET /reports/tax-year`; `scripts/check_contract_example_freshness.py` | Decided each of the 8 drifts. 7 were checker false positives under `additionalProperties: true` nodes ("Intentionally broad… canonical fields live in the contract"); the checker now accepts keys nested under an open node, lists them as OPEN SCHEMA (info), and still checks keys beside one (10 new unit/integration tests). `openapi.yaml` 3.47.3: `GET /reports/tax-year` declares `data.generated_at` and moves `estimated_unrealised_pnl`/`unrealised_note` under `data.summary` (where `reports_service.py` returns them); `OkEndpointTest` drops the `data` envelope `POST /test/endpoints` never returned. `health_endpoints.md` v1.10 example gains the top-level `status`. Commits `ff08b950`; `1de20439` (DoQ pass 1 fix: a wrapped example with an open `data` payload still flags a stray key beside `data`; 2 tests). | AC 1: `check_contract_example_freshness.py` exits 0 (137 examples, 0 drift). AC 2: corrections recorded in `health_endpoints.md` v1.10 Changelog, the `openapi.yaml` 3.47.3 info comment and `api_changelog.md` v1.29.4 (v9.15.0 entry). Covers AC 1, AC 2. | Pass with notes | None. Scope bullet 2 ("consider adding it to `quality_gate.yml`") was considered and not done in this EPIC, so a gate cannot block sibling EPICs' open PRs mid-sprint; tracked by `BLG-SPEC-222` (decision for the API Contracts & Documentation Owner). Note: `data.summary.estimated_unrealised_pnl` is declared `nullable: true` although the tax-year path always returns a float; kept to match the monthly-pnl sibling schemas. |
| ST-35 | `docs/specs/data_model.md#DS-38` | DS-38 (v2.67): pre-check, reversible Up/Down `SET NOT NULL` migration and verification for `positions.portfolio_id` and `total_cost`, DS-23 pattern. Insert paths checked: `database.create_position()` and both seeds name both columns. Staging run by the user: pre-check 0 / 0, before `YES`/`YES`, after `NO`/`NO`. Fields rows and Drift Triage row 3 annotated. Commit `e5a7f45f`. | AC 1 (staging half): `information_schema` reports `is_nullable = NO` for both columns on staging, recorded in DS-38 Live Confirmation. AC 1 production half is seal-marked `post-merge`, tracked by `BLG-SPEC-217`. AC 2: read-only `check_data_model_drift.py` on staging exits 0 with no nullable mismatch on any table. Covers AC 1 (in-sprint part), AC 2. | Pass | None. Production half planned post-merge (`BLG-SPEC-217`, `execution_prompt.md` §3.2.A seal-marked exception, LL-v9.13-P3-03). |
| ST-36 | `docs/specs/data_model.md#DS-17` | User ran DS-17's Up Migration (with its duplicate pre-check) on staging: no abort. DS-17 records the staging Live Confirmation beside production's. Scope decision: `reset-and-seed-staging.yml`'s migrate step unchanged, because the reset uses `TRUNCATE ... CASCADE`, which keeps indexes. Drift Triage row 1 annotated. Commit `dfee397b`. | AC 1: staging `pg_indexes` lists `idx_positions_open_ticker_entry_date_unique` with DS-17's definition (identical to production). AC 2: DS-17 records the staging confirmation alongside the production one. Read-only drift run no longer lists the index as missing. Covers AC 1, AC 2. | Pass | None |

**Live outputs (supplied by the user, 2026-11-05, staging):**
- ST-35 pre-check: `{"null_portfolio_id_rows": 0, "null_total_cost_rows": 0}`. Before: `portfolio_id YES`, `total_cost YES`. After: `portfolio_id NO`, `total_cost NO`.
- ST-36 verification: `idx_positions_open_ticker_entry_date_unique` — `CREATE UNIQUE INDEX idx_positions_open_ticker_entry_date_unique ON public.positions USING btree (portfolio_id, ticker, entry_date) WHERE ((status)::text = 'open'::text)`.
- Drift check after both (read-only, engine): missing indexes `IF` (parser false positive, `BLG-QA-247`), `idx_portfolio_history_portfolio`, `idx_position_audit_log_position_id`, `idx_sector_regime_history_portfolio_date`, `idx_trade_plan_audit_log_trade_plan_id`, `idx_trade_plans_ticker`, `idx_trade_reflections_trade`; missing CHECK `settings_risk_percent_check`. All except `IF` are already dispositioned in `data_model.md` §Drift Detector Triage. No column mismatches.

## QA Test Coverage

- Scenarios run: `DATABASE_URL=<stub> backend/.venv/bin/python3 -m pytest tests/test_check_contract_example_freshness.py tests/test_check_data_model_drift.py tests/test_positions_open_ticker_entry_date_unique_migration.py tests/test_fees_paid_not_null_invariant.py` → 88 passed (after `1de20439`). `check_contract_example_freshness.py`, `check_openapi_drift.py`, `check_api_performance_baseline_drift.py` and `check_local_openapi_contract_completeness.py` all exit 0. CI per commit: see Comments.
- Regression areas checked: OpenAPI drift and contract completeness (no endpoint added or removed), API performance baseline (unchanged), `positions` insert paths (app and seeds) against the new NOT NULLs, staging reset behaviour for the DS-17 index.
- Known deviations: None found — all stories' deviation checks completed with nothing to file. Follow-up filed: `BLG-SPEC-222` (quality_gate.yml decision). From the PR #2193 review: `BLG-QA-248` (nested keys under closed objects never checked, pre-existing), `BLG-QA-249` (no seed/insert invariant guard for the DS-38 NOT NULLs). Out-of-scope findings filed: `BLG-SPEC-221` (`Specs_Index.md` freshness check exits 1 on `main`: `journal.md` unlisted, stale `qa_evidence_EPIC-xx.md` reference), `BLG-QA-247` (drift check's index regex reports a prose `CREATE INDEX IF NOT EXISTS` mention as an index named `IF`).
- Frontend testing gate: N/A. No story changes `src/**`.

## Agent-Mediated Director of Quality Review

- Pass 1 (2026-11-05): **Blocked**, 1 blocking finding:
  1. When `data` was an open node, the checker accepted every key, including a stray key beside `data` in a wrapped example (8 endpoints affected; reproduced on POST /settings). Fixed in `1de20439` with 2 tests; the real corpus still exits 0.
- Non-blocking: the `quality_gate.yml` follow-up had no tracker, now `BLG-SPEC-222`; `nullable: true` on `data.summary.estimated_unrealised_pnl` kept to match the monthly-pnl siblings (noted in the ST-34 row).
- Pass 2 (2026-11-05): **Approved**. Re-ran the POST /settings probe (now `POSSIBLE DRIFT (1) -> warnings`, rc 1), the real corpus (exit 0), the 88-test run, the backlog integrity check and the execution-state consistency check.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object. N/A, no frontend change.
- [x] **Strategy values checked:** N/A — no stop/grace/ATR/exit/sizing logic touched. ST-35/ST-36 change `positions` constraints only; no stop, grace, ATR, exit or sizing value or formula.
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-11-05
- Comments:
  - Pass 1: Blocked (1 blocking; fixed in `1de20439`). Pass 2: Approved.
  - Story grades: ST-34 Pass with notes (`BLG-SPEC-222`); ST-35 Pass (production half seal-marked post-merge, `BLG-SPEC-217`); ST-36 Pass.
  - Story-level authority: Data Model & Domain Schema Owner (the user) ran the staging DDL for ST-35/ST-36 in session (`DEL-20261105-02`, `DEL-20261105-03`, both unblocked in-session).
  - CI on the story commits: `ff08b950` 7/7 success (CI Pytest 42004971230); `e5a7f45f`, `dfee397b` and `1de20439` all workflows success. Later `[GOVERNANCE]` commits' CI is to be confirmed on the PR head before merge.
  - This agent-mediated sign-off does not satisfy the always-human merge-gate rows (QA sign-off and PO acceptance).

## Merge Gate Confirmations

- **Director of Quality QA sign-off:**
  - Given by the human repository owner, acting as Director of Quality, in session on 2026-11-05 at about 12:48Z ("give DOQ and PO approval"), before the merge.
  - It accepts this evidence: ST-34 Pass with notes (`BLG-SPEC-222`), ST-35 Pass (production half post-merge, `BLG-SPEC-217`), ST-36 Pass.
  - That includes the agent-mediated sign-off block above (pass 2 Approved) and the agent-mediated PR #2193 review (comment 6655878279, both roles ⚠️ Approved with Comments, no blocking findings; follow-ups `BLG-QA-248`, `BLG-QA-249`).
  - At head `dce12815`, all 33 PR checks were green.
- **Product Owner acceptance:**
  - Given by the human repository owner, acting as Product Owner, in session at the same time.
  - It accepts ST-34 to ST-36 against `stage4_backlog_slice.md`, with ST-35's production confirmation carried post-merge under `BLG-SPEC-217`.
- **Merge:** pending — to be performed by the human repository owner. The merge commit is recorded on `main` once it exists.
