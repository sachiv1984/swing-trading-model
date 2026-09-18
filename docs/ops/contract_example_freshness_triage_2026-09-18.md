**Owner:** API Contracts & Documentation Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-18 (ST-26, EPIC-04, v9.5, BLG-SPEC-139 — triage of the 40-finding baseline)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Contract Example-Payload Freshness — Baseline Triage

## 1. Purpose

Disposes of every finding in `docs/ops/contract_example_freshness_baseline_2026-09-08.md`'s 2026-09-08 baseline run (37 POSSIBLE DRIFT + 3 SKIPPED = 40), per the triage this baseline's own §4 filed as `BLG-SPEC-139`.

## 2. Summary

| Stage | POSSIBLE DRIFT | SKIPPED | Total |
|-------|-----------------|---------|-------|
| Baseline (2026-09-08) | 37 | 3 | 40 |
| This session, before any fix | 36 | 3 | 39 (1 already resolved independently since baseline) |
| After fixing the response-example-picking bug (§3.1) | 25 | 3 | 28 |
| After fixing the allOf-composed schema resolution bug (§3.2) | 23 | 3 | 26 |
| After fixing 3 genuine openapi.yaml gaps (§4) | 20 | 3 | 23 |
| After fixing the 202-response-code gap (§3.3) | 20 | 2 | 22 |

**Net: 18 of the original 40 findings resolved this session** (11 false positives from bug §3.1, 2 from bug §3.2, 3 genuine openapi.yaml fixes, 1 SKIPPED resolved via bug §3.3, 1 already independently resolved between 2026-09-08 and this session). The remaining 22 are disposed at §5/§6 below — not left silent.

## 3. Script Bugs Found and Fixed (`scripts/check_contract_example_freshness.py`)

### 3.1 Response-example-picking bug (11 false positives)

The script picked the **last** JSON fence in a heading's section matching a "response"/"schema" text marker, not the first/nearest one. Every contract file in this directory documents its primary 2xx response before any error-response block — but an error-response block (e.g. "### Error Responses", a 429/404/500 example) also contains the word "response", so it matched the same marker regex and silently overrode the real 200 example whenever it appeared later in the section. Concretely: `ai_endpoints.md`'s `POST /ai/daily-briefing` was being checked against its **429 rate-limit example** (`{"status": "error", "message": "..."}`) instead of its actual 200 response, which is why the finding showed only `message`/`status` as "extra" keys — those two words are exactly what a generic error envelope contains, and nothing about the real 200 payload was ever actually being checked.

Confirmed at: `ai_endpoints.md` (×2), `ai_thesis_generation.md`, `gemini_thesis_generation.md` (×2), `digest_endpoints.md`, `arc5_compliance_analytics.md`, `behavioural_drift_contract.md`, `strategy_version_comparison_contract.md`, plus the field set on `market_endpoints.md`/`portfolio_endpoints.md`/`reports_endpoints.md` findings changed (now checking the real response, not an error one).

**Fix:** pick the first response-marker-matched fence, preferring one whose preceding text doesn't itself look like an error marker (`error`, `HTTP/1.1 4xx`, `HTTP/1.1 5xx`). Regression tests added: `test_picks_first_response_fence_in_section`, `test_skips_error_example_even_when_it_appears_last`.

### 3.2 allOf-composed nested/array schema resolution bug (2 false positives)

`schema_top_keys`'s nested-descent logic only expanded a nested property's schema when it declared `type: object` (or `type: array` with `items.type: object`) — but this codebase's own convention for extending a base schema (e.g. `Position` = `PositionSummary` allOf + extra properties) produces a schema with **no sibling `type` key at all**, just `allOf`. Any property or array-item schema composed this way was silently skipped during descent, even though the top-level `schema_top_keys` call already correctly handled `allOf` when called directly on a schema.

Confirmed at: `GET /positions/search/tags` (`data: Position[]`) went from 3 missing-key findings to 0.

**Fix:** added `_is_object_like()`, treating a schema as descend-worthy if it declares `type: object` **or** is composed via `allOf`/`oneOf`/`anyOf`. Regression tests added: `test_descends_into_allof_composed_nested_object`, `test_descends_into_array_of_allof_composed_items`.

### 3.3 202 (async-accepted) response code not checked (1 SKIPPED resolved)

`response_schema_for` only checked `("200", "201")` response codes. `POST /screener/run` declares only a `202` response (an async-accepted pattern) with a real, fully-declared schema — it was reported SKIPPED ("no matching openapi.yaml operation/schema") purely because the script never looked at the 202 entry, not because no schema existed.

**Fix:** added `"202"` to the checked codes. Regression test added: `test_202_response_code_used_for_async_accepted`.

All 3 fixes are covered by regression tests (`tests/test_check_contract_example_freshness.py`, 49/49 passing) that fail on the pre-fix code and pass on the fix, so this class of false positive can't silently regress.

## 4. Genuine openapi.yaml Gaps Found and Fixed (3)

Distinct from the script bugs above — these are real cases where `docs/reference/openapi.yaml`'s declared schema had fallen behind the endpoint's actual (and already markdown-documented) response shape:

| Endpoint | Gap | Fix |
|----------|-----|-----|
| `GET /health` | `OperationalHealthResponse` only declared 4 fields (`status`, `db`, `last_market_status_check`, `last_alert_evaluation`) from its original v2.2/ST-08 authoring. `external_apis`/`ai_journal` were added to the live response and documented in `health_endpoints.md` v1.5 (2026-08-07, ST-05/BLG-SPEC-114) but this schema was never updated to match. | Added `external_apis` (keyed-by-API-name object) and `ai_journal` properties to `OperationalHealthResponse`, matching `health_endpoints.md`'s field notes exactly. |
| `GET /trades` | `TradeHistoryResponse`'s `trades[]` item schema was missing `commission_gbp`, `spread_cost_gbp`, `net_r_multiple` — despite the schema's own description tracking a version history of prior additions (v1.9.0, v2.1.0, v2.2.0), these 3 (documented in `trade_endpoints.md`) were never added. | Added all 3 fields to the `trades[]` item schema, matching `trade_endpoints.md`'s field notes and types exactly. |
| `POST /cash/transaction` | `CashTransactionResponse` was a stub (`{id: uuid}` only) despite `CashTransaction` — a fully-authored schema with the real transaction shape — already existing immediately above it in the same file. | Corrected `CashTransactionResponse` to `{transaction: $ref CashTransaction, new_balance: number}`, matching `cash_endpoints.md`'s documented response exactly. |

All 3 verified via `python3 scripts/openapi_3way_drift_sweep.py` (no drift), `python3 scripts/lint_api_contract_headings.py` (pass), and the full `tests/test_api_contracts.py` + `tests/test_openapi_drift_inverse_case.py` + `tests/test_pilot_contract_schemas.py` suite (116/116 passing) after the change.

## 5. Remaining Findings (20 POSSIBLE DRIFT) — Systemic Pattern, Not Per-Endpoint Drift

The remaining 20 findings are **not** individually-diagnosed drift the way §4's 3 were. Spot-checking a representative sample (`GET /watchlist`, `POST /signals/generate`, `GET /reports/tax-year`, `settings_endpoints.md`'s two entries, plus the 10 schemas across the file that carry an explicit `"Intentionally broad to avoid drift. Canonical nested field definitions live in: <doc>"` description — `Settings`, `UpdateSettingsRequest`, `MarketStatus`, `PositionSizeResponse`, `BacktestRuleChangeRunResult`/`Summary`, `AnalyticsMetricsResponse`, `ValidationResponse`, `EndpointTestResponse`, `UpdateNotificationPreferencesRequest`) confirms a **systemic, established pattern** in this codebase: for complex or volatile response payloads, `openapi.yaml` deliberately declares the outer envelope (`{status, data}`) correctly but leaves the `data` payload itself as a generic `type: object` with no (or minimal) declared properties — sometimes with the explicit "intentionally broad" description, sometimes as a bare `{type: object}` with no description at all (e.g. `GET /watchlist`'s `data[]` items, `GET /reports/tax-year`'s `trades[]`/`summary`). The markdown contract file is the actual source of truth for these payloads' field-level shape, per this directory's own `README.md` framing.

This means most of the remaining 20 are not "someone changed the code and forgot to update the spec" (§4's pattern) — they're "the spec was never given field-level detail for this payload, by an established (if inconsistently-labelled) convention." Re-diagnosing each of the 20 individually to confirm this for certain, and then hand-authoring full field-level schemas for each where it turns out not to hold, is real work beyond this triage story's own S/~0.5-day scope (the schemas involved range from 2 fields to 27+ nested fields each).

## 6. Disposition

- **Fixed this story (§3, §4):** 3 script bugs (with regression tests) + 3 genuine openapi.yaml gaps. 18 of the original 40 findings resolved.
- **Documented, not fixed (§5 — filed as follow-up):** `BLG-SPEC-152` — full field-level openapi.yaml authoring pass for the remaining 20 generic/thin `data` payload schemas, confirming case-by-case whether each is (a) intentionally broad by convention (add the standard description if missing) or (b) genuinely under-authored (fill in real properties). Scoped as its own item given the volume, not folded into this triage.
- **Documented, not fixed (§5 — filed as follow-up):** `BLG-SPEC-153` — the 2 remaining SKIPPED endpoints (`POST /trade-plans`, `DELETE /trade-plans/{id}`) declare no response `content`/`schema` at all in `openapi.yaml` (confirmed — not a script limitation this time), despite both having documented JSON examples in `trade_plan_endpoints.md`.
- **Advisory, not filed as a separate item:** the freshness-check script itself will re-flag all 20 §5 findings on every future run until `BLG-SPEC-152` lands — this is expected/correct (the gap is real, just not urgent), not a new bug.

## 7. Re-run Confirmation

```
python3 scripts/check_contract_example_freshness.py
```
Checked 132 contract response examples against openapi.yaml. POSSIBLE DRIFT: 20. SKIPPED: 2.

## 8. Sign-Off

**API Contracts & Documentation Owner:** Accepted — 40 baseline findings triaged; 18 resolved (3 script bugs fixed with regression tests, 3 genuine openapi.yaml gaps fixed); 22 remaining disposed as documented follow-ups (`BLG-SPEC-152`, `BLG-SPEC-153`), not left silent. 2026-09-18.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-09-18 | 1.0 | Initial triage of the 2026-09-08 baseline (ST-26, EPIC-04, v9.5, BLG-SPEC-139). |
