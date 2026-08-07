Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-07

# QA Evidence — EPIC-02 — API Contract & Spec Debt Closure

**EPIC:** EPIC-02 — API Contract & Spec Debt Closure
**Cycle:** 2026-08-07__release-v8.4
**Sprint goal:** Ship both available user-facing reporting enhancements while clearing a full-capacity slate of API contract & spec debt, backend hardening, frontend code health & security, operational reliability & cost monitoring, QA/test infrastructure, and governance-process integrity work across all 31 scoped stories.
**Test scenarios used:** No `tests/`/`tests/e2e/` runnable files apply — this EPIC is documentation/spec-debt closure only. Verification method per story: `yaml.safe_load` structural checks, `scripts/openapi_3way_drift_sweep.py`, and code-review cross-checks against the live backend implementation (`backend/database.py`, `backend/services/*.py`, `backend/main.py`).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-02 | `docs/reference/openapi.yaml` | Relocated ~23 endpoints from inside `components:` back under `paths:`; `yaml.safe_load` path count now matches raw-text scan (116→118 after ST-07's additions). Fixed 2 endpoints (`GET /test/quick-health`, `POST /test/rate-limit-scenarios`) surfaced as newly-visible drift once parsing was corrected. | `components:` has 0 path-shaped keys; parsed/raw path counts match; Drift Detection CI gate passes; BLG-OPS-133 list re-verified; owner sign-off | Pass | None |
| ST-03 | `docs/specs/api_contracts/settings_endpoints.md` | Added `created_at`/`updated_at` to `GET /settings` example with representative ISO-8601 values and field notes. | Example includes both fields with representative values | Pass | None |
| ST-04 | `docs/specs/api_contracts/position_endpoints.md` | Added `total_cost`, `sector`, `industry`, `exit_reason`, `stop_reason` to `GET /positions` example and field notes, cross-checked against `position_service.py`. | All 5 fields listed with descriptions; cross-checked against live dict | Pass | None |
| ST-05 | `docs/specs/api_contracts/health_endpoints.md` | Added `external_apis` and `ai_journal` nested objects to `GET /health` example, matching `health_service.get_operational_health()`. | Example reflects full live response shape including both nested objects | Pass | None |
| ST-06 | `docs/specs/api_contracts/watchlist_endpoints.md` | Corrected stale `GET /watchlist` JSON example: added `company_name`, `tags`, `updated_at`, `added_at`, `days_on_watchlist`, `is_stale`; removed `portfolio_id` (not returned). | Example includes the 6 named fields; `portfolio_id` removed; field table/version history unchanged | Pass | None |
| ST-07 | `docs/reference/openapi.yaml`, `docs/specs/api_contracts/conventions.md` | Audited all authenticated endpoints against `backend/main.py`'s `api_key_middleware`. Fixed 2 gaps: `GET /changelog/latest` wrongly marked `security: []`; `GET /health/scheduler` referenced undefined `ApiKeyAuth` scheme instead of `ApiKey`. `conventions.md` §1.4/1.5 already correct. | Audit complete; documentation gaps fixed; owner sign-off | Pass | None |
| ST-08 | `docs/specs/data_model.md` | Added canonical sections for `backtest_trades` (+ 2 sibling tables), `idempotency_keys`, `gemini_audit_log`, `ai_journal_entries` (documented as externally-provisioned, no `CREATE TABLE` in codebase, per `db_index_audit_arc4_2026-08-06.md` Finding 4). | Section added for each of the 4 named tables (columns/types/nullability/purpose/populating function); owner sign-off | Pass | None |
| ST-09 | `docs/specs/schema_versioning_trade_plan_position.md` | New canonical doc indexing `data_model.md`'s existing `trade_plans`/`positions` migration history (DS-04 through DS-11 + numbered migrations touching either table); establishes column-level deprecation policy. Registered in `Specs_Index.md` §3.2. | Schema-versioning doc created covering migration history and field deprecation; owner sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: N/A — documentation/spec-debt EPIC. Verification via `python3 -c "import yaml; yaml.safe_load(...)"`, `python3 scripts/openapi_3way_drift_sweep.py` (0 drift findings after ST-02/ST-07), and direct code-review cross-checks against `backend/database.py`, `backend/services/position_service.py`, `backend/services/watchlist_service.py`, `backend/services/health_service.py`, `backend/main.py`.
- Regression areas checked: OpenAPI structural validity (`yaml.safe_load` parses cleanly, 118 paths), OpenAPI Drift Detection gate (0 findings), no frontend files touched (`src/pages/`, `src/components/` — confirmed via `git diff --name-only`).
- Known deviations filed: None. BLG-OPS-133's endpoint list was re-derived (raw regex scan, 22 candidate gaps) as part of ST-02 but **not written to `backlog.md`** — editing an existing backlog item's content is outside this engine's write scope (`execution_prompt.md` §7 permits only new-item addition to `backlog.md`). The authoritative correction of BLG-OPS-133 is deferred to ST-20 (EPIC-05), which is explicitly gated to begin only after this EPIC merges and performs the live staging measurement pass BLG-OPS-133 itself requires.

---

## Autonomous Class Sign-Off Block (BLG-GOV-19)

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-02 through ST-09, all 8 stories)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ (yaml/CI-script checks + source-code cross-reference for every story)
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/pages/` or `src/components/` was created or modified (`git diff --name-only main..HEAD` — only `docs/`, `claude/`, and `.claude_current_state.json` touched) — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-07
- Comments: Autonomous class sign-off — all four qualifying criteria met (all 8 stories autonomous, all AC code-review/CI-script-verifiable, no frontend changes, engine signer populated). Domain-specific authorities named per-story in the Sprint Backlog (API Contracts & Documentation Owner for ST-02/03/04/05/06/07; Data Model & Domain Schema Owner for ST-08/09) are recorded in `execution_state.json`'s per-story `sign_off_record` fields, consistent with the EPIC-level consolidation note (BLG-GOV-14).
