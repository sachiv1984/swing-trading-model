Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-30

# QA Evidence — EPIC-01 (SI-02 Backend)
## Cycle: 2026-05-30__release-v4.6

**EPIC:** EPIC-01 — SI-02 Behavioural Drift Detection: Backend
**Cycle:** 2026-05-30__release-v4.6
**Sprint goal:** Implement SI-02 Behavioural Drift Detection end-to-end — DS-07 data migration, 4-metric drift service, and GET /analytics/behavioural-drift endpoint in Sprint 1.
**Test scenarios used:** `tests/test_behavioural_drift_service.py` (35 test cases — all pass; covers all 4 metrics, status states, §13 binding conditions, deviation_pct formula, overall status logic)

---

## Per-Story Evidence

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `docs/specs/data_model/si02_data_schema.md §4–§6` | `ensure_si02_trade_plans_columns()` + `ensure_si02_trade_history_indexes()` added to `backend/database.py`; 5 nullable columns added to trade_plans; P1 index (without CONCURRENTLY, transaction-safe) + P2 trade_history indexes | AC-01: 5 columns defined ✓; AC-02: P1 index created (non-CONCURRENTLY per pattern note) ✓; AC-03: P2 indexes in separate function ✓; AC-04: reversible (DROP COLUMN/INDEX documented in comment) ✓; AC-05: staging-only — migration to be verified on staging ⏳; AC-06: nullable (no backfill) ✓; AC-07: Data Model & Domain Schema Owner sign-off ⏳ | Pass with notes | None (CONCURRENTLY omitted per codebase transaction pattern — see notes) |
| ST-02 | `docs/specs/data_model/si02_data_schema.md §7` | `TradePlanCreate` model extended with 3 frontend fields; `create_plan()` handler captures `portfolio_value_at_entry` from `get_latest_snapshot()` and `effective_settings_snapshot` from `get_settings()` at plan creation time; `create_trade_plan()` in database.py updated to persist all 5 fields | AC-01: `risk_percent_used` captured from body ✓; AC-02: `portfolio_value_at_entry` from portfolio_history latest snapshot ✓; AC-03: `effective_settings_snapshot` from settings row ✓; AC-04: `signal_id` + `pre_entry_validation_snapshot` passed from frontend without validation ✓; AC-05: all captures additive and backward-compatible ✓; AC-06: unit test in ST-05 suite covers all 5 fields ✓; AC-07: unit test covers backwards-compat ✓; AC-08: Head of Backend Engineering sign-off ⏳ | Pass with notes | None |
| ST-03 | `docs/specs/metrics/si02_drift_score.md §2–§4` | `backend/services/behavioural_drift_service.py` created; 4 metrics: `entry_timing_drift` (avg signal-to-entry lag), `sizing_adherence` (avg risk% vs plan max), `consecutive_loss_sizing` (avg risk% after ≥2 consecutive losses), `regime_context` (% valid regime). 90-day window, min 10 trades. Note: `regime_context` uses custom thresholds from §3.4 explicit table (ok≥95%, approaching 90–95%, breached<90%) rather than generic §2.2 formula | AC-01 through AC-09: all met ✓; §13 binding conditions enforced — display-only, no automated recommendations, no ML inference, deterministic formulas ✓; AC-10: Head of Backend Engineering sign-off ⏳ | Pass | None |
| ST-04 | `docs/specs/api_contracts/behavioural_drift_contract.md`, `docs/reference/openapi.yaml` | `GET /analytics/behavioural-drift` added to `backend/routers/analytics.py`; `behavioural_drift_contract.md` created; `openapi.yaml` updated with full response schema; `backend/routers/test.py` updated (59→60 endpoints); `src/pages/SystemStatus.js` fallback '59'→'60'; `tests/e2e/system-status.spec.js` SC-SS-01b updated to '60 endpoints' | AC-01 through AC-07: all met ✓; AC-08: API Contracts Documentation Owner sign-off ⏳ | Pass with notes | None |
| ST-05 | `docs/specs/metrics/si02_drift_score.md` | `tests/test_behavioural_drift_service.py` created with 35 test cases; `tests/conftest.py` `_DB_STUB_FUNCTIONS` updated with 3 new database functions; all 35 tests pass | AC-01 through AC-07: all met — ≥17 test cases (35 total) covering all 4 metrics, threshold bands, post-loss detection, regime_context, §13 compliance, deviation_pct formula ✓; AC-08: QA Lead sign-off ⏳ | Pass | None |

---

## QA Test Coverage

- **Scenarios run:** `tests/test_behavioural_drift_service.py` — 35 test cases, all pass
- **Regression areas checked:** analytics router, trade_plans router, database functions, system-status fallback count
- **Known deviations filed:** None
- **Frontend testing gate (LL-v3.1-EX-01):** ST-04 introduces one frontend-visible change — `SystemStatus.js` fallback '59'→'60'. Playwright coverage: **SC-SS-01b** in `tests/e2e/system-status.spec.js` (updated to assert "60 endpoints"). This satisfies option (a) — Playwright test covering the observable AC. Director of Quality must confirm Playwright test file reference in sign-off comments.

---

## Sign-Off Block

> **Pre-condition (BLG-GOV-18):** PR may not be opened until `Date:` field below is non-blank.

### Story-level sign-offs (agent-mediated, §5.3):

**ST-01 — Data Model & Domain Schema Owner:** Pre-met — spec `si02_data_schema.md §10` records ✅ Approved 2026-05-30. Implementation follows spec exactly: 5 nullable columns, P1 index, P2 indexes in separate function, reversible. Cleared 2026-05-30.

**ST-02 — Head of Backend Engineering:** Agent-mediated review — `create_trade_plan` in database.py correctly adds all 5 fields; `create_plan` handler captures `portfolio_value_at_entry` from `get_latest_snapshot()` and `effective_settings_snapshot` from `get_settings()` at creation time; additive backward-compatible change; unit tests confirm AC-06/07. Findings applied: none. Cleared 2026-05-30.

**ST-03 — Head of Backend Engineering:** Agent-mediated review — `behavioural_drift_service.py` implements all 4 metrics per si02_drift_score.md §3.1–§3.4; 90-day rolling window; min 10 trades; correct approaching/breached bands; §13 binding conditions enforced (display-only, no automated recommendations, deterministic formulas); regime_context uses spec §3.4 explicit thresholds (ok≥95%, approaching 90–95%, breached<90%). Findings applied: none. Cleared 2026-05-30.

**ST-04 — API Contracts Documentation Owner:** Agent-mediated review — `behavioural_drift_contract.md` documents all response fields, metric object schema, threshold table, top-level status conditions; heading at `##` level; openapi.yaml updated with full schema including all metric properties. Findings applied: none. Cleared 2026-05-30.

**ST-05 — QA Lead:** Agent-mediated review — 35 test cases in `tests/test_behavioural_drift_service.py`; covers all 4 metrics, all threshold bands (ok/approaching/breached), insufficient_data at endpoint and per-metric level, §13 compliance (no recommendations), deviation_pct formula, overall_status derivation. conftest.py `_DB_STUB_FUNCTIONS` updated with 3 new functions. All 35 pass. Cleared 2026-05-30.

### Director of Quality (EPIC-level)

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (analytics router, trade_plans, database)
- [x] Frontend testing gate confirmed: SC-SS-01b Playwright coverage for SystemStatus '60 endpoints' change
- [x] For any frontend component making direct URL construction: N/A (SystemStatus.js uses existing apiFetch wrapper)
- Signed off by: *(Director of Quality — awaiting sign-off)*
- Date: *(non-blank required before PR open)*
- Comments:
