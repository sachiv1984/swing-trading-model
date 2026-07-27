Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

# QA Evidence — EPIC-11 (v7.8)

**EPIC:** EPIC-11 — Contract tests for highest-traffic frontend/backend endpoints
**Cycle:** 2026-07-24__release-v7.8
**Sprint goal:** Ship all 12 v7.8 EPICs with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_pilot_contract_schemas.py`

## ST-11 — Add pilot contract tests for 3 highest-traffic endpoints

**Spec reference:** `docs/testing/pilot_contract_test_approach.md` (new artefact, Case B), `docs/specs/api_contracts/{position,trade,portfolio}_endpoints.md`
**Commit:** (implementation — see `execution_state.json` for full SHA)

**Prerequisite — RISK-03 resolution:** ST-11 was classified `delegated_decision` at sprint planning (no telemetry-backed pilot-endpoint ranking existed). Escalated as `ESC-EXEC-20260727-01` and resolved via agent-mediated Head of Engineering review on 2026-07-27, confirmed pilot endpoints: `GET /positions`, `GET /trades`, `GET /portfolio`. Full reasoning (call-site evidence, and why the "dashboard" candidate resolves to `GET /portfolio` rather than a literal endpoint) is recorded in `claude/cycles/2026-07-24__release-v7.8/execution_escalations.md`. ST-11 reclassified `delegated_decision` → `autonomous` on resolution.

**What was built:** `tests/test_pilot_contract_schemas.py` — schema-contract tests distinct from the existing status/envelope smoke tests in `test_api_contracts.py`. Each of the 3 pilot endpoints is exercised with a realistic **non-empty** mocked response and every field documented in its `docs/specs/api_contracts/*.md` contract is asserted present with the documented type, via a shared `assert_schema()` helper (plain dict/type checks, no new dependency — consistent with this repo's existing lint-style tests). `docs/testing/pilot_contract_test_approach.md` documents the pattern, its explicit scope boundary (catches missing/wrong-typed fields; does not flag undocumented extra fields), and how to extend it to further endpoints in future cycles.

**Findings from writing the pilot (recorded, not silently fixed — full detail in the approach doc):**
1. `GET /positions` does not use the standard envelope despite `position_endpoints.md` claiming it does — pre-existing, already implicitly known via `test_api_contracts.py`'s own comment, re-confirmed here. The pilot test asserts the real (unenveloped) behaviour rather than the doc's claim.
2. `GET /positions` responses include 3 undocumented fields (`position_state`, `state_entered_at`, `days_in_state`) merged in by `get_lifecycle_fields_for_position()`, absent from `position_endpoints.md`.
3. `GET /trades`'s JSON example in `trade_endpoints.md` omits 3 fields (`commission_gbp`, `spread_cost_gbp`, `net_r_multiple`) that its own Field notes table documents and the real service always returns — a doc-example-completeness gap, not a code defect.

None of the 3 findings is P0/P1 (no caller-relied-upon field is missing from any real response) — all are documentation-completeness gaps, left to standard backlog grooming to reconcile rather than fixed in this story (ST-11's scope is adding contract tests, not auditing existing contract docs), consistent with this sprint's RISK-04/EPIC-08 precedent for recording-not-fixing out-of-scope findings.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-11 | `test_pilot_contract_schemas.py` | Schema-contract tests for `GET /positions`, `GET /trades`, `GET /portfolio` | Lightweight contract tests added for the 3 highest-traffic endpoints as a pilot (RISK-03 selection confirmed by Head of Engineering) | Pass | None |
| ST-11 | (same) | 5 tests (3 endpoint schema tests + 2 negative tests confirming the helper itself catches drift), all passing in the full backend suite | Contract tests added and passing in CI for all 3 pilot endpoints | Pass | None |
| ST-11 | `pilot_contract_test_approach.md` | New approach doc: scope boundary, extension steps, priority-candidate method for next cycle | Approach documented for extending to additional endpoints in future cycles | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_pilot_contract_schemas.py` — 5 tests: `GET /positions` schema match (+ real-envelope-behaviour assertion), `GET /trades` schema match (top-level + per-trade record), `GET /portfolio` schema match (top-level + per-position summary record), and 2 negative tests confirming `assert_schema()` actually catches a missing field and a wrong-typed field (required precedent per this sprint's lint-test convention, e.g. `test_lint_api_contract_headings.py`'s deliberately-miscoded-heading test). All 5 pass.
- Regression areas checked: full backend suite (`backend/.venv/bin/python3 -m pytest tests/ --ignore=tests/e2e`) — 759 passed, 2 skipped, no behavioural change to any other endpoint. Initial draft of the new test file included an unnecessary `sys.modules.pop("database", None)` (copied from an existing precedent in `test_api_contracts.py` without checking it was actually needed) which evicted conftest's session-scoped DB stub and broke collection of 2 alphabetically-later test files (`test_pnl_reconciliation_service.py`, `test_price_alerts_service.py`) when the full suite ran together — caught by running the full suite (not just the new file in isolation) before considering this done, and fixed by removing the unnecessary pop (this file only needs `from main import app`, which is already available via the session-scoped stub without forcing a fresh import).
- Known deviations filed: None.

## Autonomous class eligibility check (BLG-GOV-19)

- Criterion 1 (all stories autonomous): ✓ — ST-11 is the only story, reclassified `autonomous` on RISK-03 resolution.
- Criterion 2 (all AC verifiable by code review/tests alone): ✓ — pure backend test + documentation artefact, no UI surface.
- Criterion 3 (no frontend-visible change): ✓ — only `tests/`, `docs/testing/`, and `claude/cycles/**` touched.
- Criterion 4 (engine signer field populated): ✓ — see below.

**All four criteria met — autonomous class applies for the EPIC-level consolidation.** Per BLG-GOV-14, the story-level Head of Engineering domain-authority sign-off (RISK-03 pilot-endpoint confirmation, agent-mediated §5.3) is recorded separately in `execution_escalations.md` — both are recorded.

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-27
- Comments: Autonomous class sign-off — all four qualifying criteria met. Story-level Head of Engineering sign-off (RISK-03 pilot-endpoint selection, agent-mediated §5.3) recorded separately in `execution_escalations.md` (`ESC-EXEC-20260727-01`) per BLG-GOV-14 — confirmed cleared.
