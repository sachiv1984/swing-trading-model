**Owner:** Head of Engineering; QA & Testing Owner
**Class:** Class 2
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-09-09 (ST-06, BLG-QA-85, v9.3 — extended pilot to 5 endpoints, first 2 sourced from openapi.yaml directly; no longer just a "pilot"); prior — 2026-07-27 (ST-11, EPIC-11, v7.8, RISK-03 — initial 3-endpoint pilot)
**Sprint Item:** ST-11 (EPIC-11, v7.8, RISK-03); extended ST-06 (BLG-QA-85, EPIC-02, v9.3)

---

# Pilot Contract Test Approach

## Purpose

`tests/test_api_contracts.py` already checks HTTP status codes and the standard `{"status": "ok", "data": ...}` envelope for every route, but it does so mostly against **empty** mock payloads (`return_value=[]`, `{"trades": []}`, etc.). An empty payload has no fields to check, so a documented field being silently removed or renamed by a future change would not be caught by that suite alone.

This test file (`tests/test_pilot_contract_schemas.py`) adds a second, narrower kind of test — a **schema-contract test** — now covering 5 endpoints:

- `GET /positions`, `GET /trades`, `GET /portfolio` — the original ST-11 pilot (`ESC-EXEC-20260727-01`, RISK-03), schema sourced from `docs/specs/api_contracts/{position,trade,portfolio}_endpoints.md`.
- `GET /cash/summary`, `GET /signals` — added ST-06 (BLG-QA-85, EPIC-02, v9.3), schema sourced directly from `docs/reference/openapi.yaml`'s `#/components/schemas` (`CashSummary`, `Signal`), per ST-06's specific "openapi.yaml vs actual route behaviour" acceptance criterion. `GET /cash/summary` was already named as a priority next-extension candidate below (v7.8).

Each test mocks a realistic **non-empty** response and asserts every field documented in the relevant contract source is present with the documented type.

## What This Pilot Checks (and Does Not)

**Checked:** every documented field is present on a realistic response, with a value of the documented type (or one of the documented nullable types).

**Not checked (explicitly out of scope for this pilot):**
- Undocumented **extra** fields present on the real response but absent from the contract doc. This pilot already found two real instances of this (see Findings below) but does not fail on them — matching the existing OpenAPI Drift Detection gate's own philosophy of catching removed/renamed fields, not flagging additions.
- Exact numeric values, business-logic correctness, or computed-field correctness (covered elsewhere, e.g. `tests/test_trade_service.py`, `tests/test_portfolio_service.py`).
- Nested nullable-field *combinations* (e.g. "is `grace_days_remaining` non-null exactly when `grace_period` is true") — this pilot checks type, not cross-field invariants.

## Findings From This Pilot (Recorded, Not Silently Fixed)

Writing these tests against the real contract docs surfaced two pre-existing doc/reality gaps, neither introduced by this story and neither blocking:

1. **`GET /positions` does not use the standard envelope**, despite `position_endpoints.md`'s Response (200) section stating "Response uses the standard success envelope from conventions.md." The real handler (`backend/main.py::get_positions_endpoint`) returns the position list directly, no `{"status": "ok", "data": ...}` wrapper — already implicitly known (see `test_api_contracts.py::TestPositionEndpoints`'s own comment) and re-confirmed here. The pilot test asserts the real (unenveloped) behaviour.
2. **`GET /positions` responses include 3 undocumented fields** (`position_state`, `state_entered_at`, `days_in_state`), merged in per-position by `get_lifecycle_fields_for_position()` (`backend/services/position_lifecycle_service.py`) but not listed anywhere in `position_endpoints.md`.
3. **`GET /trades`'s JSON example in `trade_endpoints.md` omits 3 fields** (`commission_gbp`, `spread_cost_gbp`, `net_r_multiple`) that its own Field notes table documents and that `backend/services/trade_service.py::get_trade_history_with_stats()` always includes on every record. A doc-example-completeness gap, not a code defect.

None of these three are P0/P1 (no field is silently *missing* from a response relative to what a caller relies on) — they are documentation-completeness gaps. Filing a lightweight backlog item for the Head of Specs Team to reconcile `position_endpoints.md`/`trade_endpoints.md` is left to standard backlog grooming rather than fixed in this story, since ST-11's scope is adding contract tests, not auditing/rewriting existing contract docs.

### Findings from the ST-06 extension (v9.3, openapi.yaml-sourced endpoints)

Two simple, safe field-level fixes were made **inline** in `docs/reference/openapi.yaml` as part of ST-06 (distinct from the ST-11 findings above, which were left unfixed as bigger documentation-completeness questions):

4. **`Signal.momentum_score` never matched reality.** The real field (`backend/services/signal_service.py`, and already correct in `docs/specs/api_contracts/signal_endpoints.md`'s own JSON example) is `momentum_percent`. Renamed in `openapi.yaml`.
5. **`CashSummary` was missing `current_cash`**, a field already returned by `cash_service.py::get_summary()` and already documented correctly in `cash_endpoints.md`. Added in `openapi.yaml`.

One finding was **not** fixed inline, following the same judgment call as finding #1 above (a bigger behavioural question, not a doc typo):

6. **`GET /signals` does not use the standard envelope**, despite both `openapi.yaml`'s `OkSignalsList` response and `signal_endpoints.md`'s "Response uses the standard success envelope" claim. The real handler (`backend/main.py::get_signals_endpoint`) returns the signal list directly — the same class of drift as finding #1 (`GET /positions`). The ST-06 test asserts the real (unenveloped) behaviour.

Per ST-06's own acceptance criteria (RISK-02): any drift found *beyond* the 5-endpoint sample is filed as a new `BLG-SPEC-*` item rather than resolved inline — none was found beyond the sample in this extension.

## Extending Coverage to Additional Endpoints

To add a 6th (or later) endpoint to this style of contract test:

1. Read the endpoint's schema — either its `## METHOD /path` section in `docs/specs/api_contracts/*.md` (`### Response (200)` `data` schema JSON example + Field notes table), or its component in `docs/reference/openapi.yaml`'s `#/components/schemas` (per ST-06, v9.3 — either source is valid; cross-check both when both exist, as ST-06 did, since they can drift from each other as well as from reality).
2. Build a `<ENDPOINT>_SCHEMA` dict: `{field_name: allowed_type_or_tuple}`. Use the shared `NUM`, `NUM_OR_NONE`, `STR_OR_NONE` aliases already defined in `test_pilot_contract_schemas.py` for common cases (numeric-or-int, nullable-numeric, nullable-string).
3. Build one realistic (non-empty) mock payload literal covering every documented field — copy the doc's own JSON example as a starting point rather than inventing new values, so the test stays anchored to the documented contract rather than to implementation details.
4. Mock the endpoint's underlying service function (patch at the import site inside `main.py`/the relevant router — see `CLAUDE.md`'s patch-target rule) to return the mock payload, call the endpoint via `CLIENT`, and call `assert_schema(response_data, SCHEMA, "<context label>")`.
5. If the response nests sub-objects (e.g. an array of records), validate each sub-object against its own schema dict, as done here for `positions`/`trades` arrays.
6. If the endpoint diverges from the documented envelope (as `GET /positions` and `GET /signals` do), assert the **real** behaviour and leave a comment explaining the discrepancy — a contract test's job is to catch drift against actual behaviour, not to enforce what the doc merely claims.
7. If a genuine field-level drift is found (missing/misnamed field) and the fix is simple and safe (an additive field, an obvious rename matching an already-correct sibling doc), fix it inline in `openapi.yaml` as part of the same story, as ST-06 did — reserve "file as backlog, don't fix inline" (RISK-02) for drift found *beyond* the story's endpoint sample, or for bigger behavioural questions like an envelope mismatch.

## Priority Candidates for the Next Extension

`GET /cash/summary` (added ST-06, v9.3) is no longer a candidate. No telemetry-backed ranking exists in this app (same gap RISK-03 already flagged for this pilot's own selection) — remaining candidates should be judged the same way this pilot's earlier candidates were resolved (`ESC-EXEC-20260727-01`): by frontend call-site count as a traffic proxy. At time of writing, `GET /trade-plans` (used across trade-planning flows) remains a reasonable next candidate by that method — not confirmed, since confirming it is out of scope for this cycle.

---

## Acceptance

- Accepted by: Head of Engineering
- Date: 2026-07-27
