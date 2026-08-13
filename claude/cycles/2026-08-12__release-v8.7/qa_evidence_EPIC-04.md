Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-13

---

## Consolidation Block

**EPIC:** EPIC-04 — Backend Reliability & Performance Hardening
**Cycle:** 2026-08-12__release-v8.7
**Sprint goal:** Deliver v8.7's user-facing feature and theme-consistency completion work while closing the mandatory trade-plan data-integrity carryover from v8.6, backed by expanded test, security, reliability, and governance coverage across the release's remaining six EPICs.
**Test scenarios used:** `tests/test_gemini_claude_retry_backoff.py` (new), `tests/test_position_lifecycle_n_plus_1_fix.py` (new), `tests/test_position_lifecycle.py` (existing, re-run for regression), `tests/test_api_contracts.py` (existing, re-run for regression)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-10 | `tests/test_gemini_claude_retry_backoff.py` | `backend/services/gemini_service.py::_call_claude()` — the single call site both `generate_full_plan()`/`generate_setup_thesis()` route through — now wrapped in the shared `retry_with_backoff` decorator (`utils/retry.py`, same BLG-BE-57 pattern as other call sites), retrying on `APITimeoutError`, `APIConnectionError`, `RateLimitError`, `InternalServerError` (3 attempts). 4xx client errors (`BadRequestError` etc.) are not retried. | See `stage4_backlog_slice.md#ST-10` | Pass | None — code review confirms this is the sole "Gemini"/Claude external API call site in the codebase (naming note: the service is still named "Gemini" from a prior migration to Anthropic's Claude API, out of scope to rename — documented in the module docstring) |
| ST-11 | `tests/test_position_lifecycle_n_plus_1_fix.py` | Audited `GET /positions` and `GET /trades`. Found and fixed one clearly-attributable N+1: `get_lifecycle_fields_for_position()` (called once per position in `GET /positions`' loop) always called `refresh_position_lifecycle()`, which unconditionally re-fetched the full row via `get_position_by_id()` — even though the caller already had the same row. Fixed by threading an optional `prefetched_position` through both functions; `get_positions_with_prices()` now carries the 3 needed lifecycle columns through (popped before the API response is returned, response shape unchanged). `GET /trades` audited, found clean (single `LEFT JOIN` query, already fixed in a prior story, ST-03/EPIC-02/v6.0/BLG-FEAT-20). External-API fan-out (Yahoo Finance price/sector lookups per position) noted but out of scope — "N+1 query" AC framing is DB-specific. | See `stage4_backlog_slice.md#ST-11` | Pass | None — surgical fix, no broader refactor needed for the one case found |
| ST-12 | `docs/design/2026-07-21__release-v7.7/si04-strategy-version-comparison/data_model_pre_design.md` | **Finding: this story's premise is stale.** SI-04 (Strategy Version Performance Comparison) already shipped in full 4 releases ago (`2026-07-21__release-v7.7`, EPIC-01/ST-01, `BLG-FEAT-75`) — confirmed live in `backend/routers/analytics.py` + `backend/strategy_version_registry.py`. `BLG-BE-30`'s schema question (new table vs FK vs snapshot field) was already answered at implementation time: none of the three — date-range/version-registry attribution, no schema change. Produced a retroactive confirmation document per the AC's own wording, closing the loop rather than silently skipping the story or re-doing already-shipped design work. | See `stage4_backlog_slice.md#ST-12` | Pass with notes | None — see Stale Story Finding section below |

**Requirement (OA-3/ST-03) AC coverage check:** ST-10's 2 ACs — covered (retry pattern applied; failure modes tested). ST-11's 2 ACs — covered (audited; clearly-attributable case fixed; no broader-refactor cases found requiring a follow-up filing). ST-12's 1 AC — covered via the retroactive-closure framing in the row above.

**QA test coverage:**
- Scenarios run: `tests/test_gemini_claude_retry_backoff.py` (8/8 passing), `tests/test_position_lifecycle_n_plus_1_fix.py` (4/4 passing), `tests/test_position_lifecycle.py` + `tests/test_position_lifecycle_states_registry.py` + `tests/test_position_trade_plan_link.py` (43/43 passing, regression check), `tests/test_api_contracts.py` + `tests/test_service_coverage.py` + `tests/test_router_test_registration_check.py` (85/85 passing, regression check including `GET /positions` end-to-end via FastAPI TestClient)
- Regression areas checked: `backend/services/gemini_service.py`, `backend/services/position_lifecycle_service.py`, `backend/services/position_service.py`, `backend/main.py` (`/positions` endpoint)
- Known deviations: None found — all stories' deviation checks completed with nothing to file

---

## Stale Story Finding — ST-12 / `BLG-BE-30`

Not a deviation against a spec — `BLG-BE-30` itself is a stale backlog item whose target feature (SI-04) shipped 4 releases before this one. Recorded here rather than silently worked around:
- `BLG-BE-30` filed 2026-06-03 (idea intake), un-gated 2026-08-11 (roadmap rebalance, DL-078) on the reasoning that its own prior gate ("SI-04 sprint planning imminent") was self-referential.
- SI-04 actually entered a sprint and shipped 2026-07-24 (`2026-07-21__release-v7.7`), i.e. **before** the 2026-08-11 un-gating decision that scheduled `BLG-BE-30` as if SI-04 hadn't yet been planned.
- The un-gating rebalance did not cross-reference the roadmap's own v7.7 "Complete" entry, which already names SI-04 as shipped.
- **Recommendation:** Product Owner or next `groom backlog` pass should mark `BLG-BE-30` resolved, citing this qa_evidence entry and `data_model_pre_design.md` as closing evidence. Out of this story's write scope to edit `BLG-BE-30`'s own entry (`execution_prompt.md` §7 — `backlog.md` write scope is new-item-addition only).

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] No frontend component modified by this EPIC (backend-only changes) — URL-base-variable check not applicable
- Signed off by: Sprint Execution Engine (agent-mediated, Backend Engineering Patterns Owner role — §5.3)
  Sprint Execution Engine (agent-mediated, Data Model & Domain Schema Owner role — §5.3)
- Date: 2026-08-13
- Comments: ST-10/ST-11 fully implemented, tested, and locally verified passing (backend-only, pure Python — no sandbox execution limitation, unlike EPIC-03's Playwright coverage). ST-12 closed via retroactive documentation given its stale premise (SI-04 already shipped v7.7) — see Stale Story Finding above; recommend `BLG-BE-30` be marked resolved by Product Owner / next `groom backlog` pass.

