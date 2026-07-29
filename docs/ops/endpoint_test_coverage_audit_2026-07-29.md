**Owner:** QA & Testing Owner
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-29
**Cycle:** 2026-07-28__release-v7.10 (ST-11 — BLG-QA-133)

---

# Endpoint Test Suite Coverage Audit

## Purpose

Audit `backend/routers/test.py`'s `test_cases` list coverage against every `@router.*` decorator across `backend/routers/*.py` and every `@app.*` decorator in `backend/main.py`. Any coverage gap found is filed or fixed.

## Method

Enumerated all live HTTP routes (method + path) via AST-adjacent regex extraction of every `@router.*(...)`/`@app.*(...)` decorator across 23 router files plus `backend/main.py` — 128 distinct routes. Cross-referenced against `test_cases`'s registered `(method, path)` entries (109 before this audit's additions, 102 before that — see the running count log in `tests/e2e/system-status.spec.js`'s `SC-SS-01b`), normalising path parameters to compare route *patterns* rather than literal placeholder values.

## Findings

**9 routes found with no corresponding `test_cases` entry.** Each was individually assessed for whether adding it is safe (read-only, or a side effect already accepted for a materially identical sibling entry) before deciding to fix or exclude.

### Fixed (7 — added to `test_cases` this story)

| Route | Rationale for safety |
|-------|----------------------|
| `GET /health/database` | Sibling of already-tested `/health/detailed`, `/health/scheduler`. Conditionally sends a Telegram notification if DB usage is at/above threshold — this is the endpoint's intended monitoring behaviour regardless of caller, not a side effect introduced by testing it. |
| `GET /portfolio/prospective-heat` | Docstring: "Read-only. Does not create a position or mutate any state. Safe to call repeatedly." |
| `GET /positions/search/tags` | Pure DB read (tag search), no mutation. |
| `GET /reports/tax-year` | Pure DB read/report generation, same pattern as already-tested sibling reports (`/reports/daily-pnl`, `/reports/monthly-pnl`). |
| `GET /trades/export/csv` | Pure DB read + CSV serialisation, no mutation (`services/trade_service.py::build_trade_history_csv`). |
| `POST /portfolio/size` | Docstring: "Read-only. Does not create a position or mutate any state. Safe to call repeatedly on debounced keystrokes." Pure calculation endpoint. |
| `POST /trade-plans/generate-plan` | Calls Claude directly (real API cost) and writes an audit-log row — but this is the *exact same* side-effect profile already accepted for its sibling `POST /trade-plans/{id}/generate-thesis`, which is already in `test_cases`. Adding this one is consistency, not new risk exposure. |

### Deliberately excluded (2 — not gaps, documented rationale)

| Route | Why excluded |
|-------|--------------|
| `GET /positions/analyze` | Despite the `GET` verb, `services/position_service.py::analyze_positions()`'s own docstring states it "Updates trailing stops based on profitability... Updates position data in database." Adding this to a smoke test that can run against the live production single-portfolio system would mutate real trailing stops on real live positions on every run. |
| `GET /trades/{trade_id}/reflection` | Always returns HTTP 404 for any placeholder `trade_id` (a reflection only exists once explicitly saved by a user) — this harness's pass criterion is strictly 2xx (`backend/routers/test.py`'s result loop: `if 200 <= response.status_code < 300`). Not expressible as a reliably-passing smoke-test case without depending on live data state; not a "never exercised" gap in the sense the story is scoped to close. |

### Already correctly excluded, not new findings (confirmed during this audit, not re-litigated)

The remaining ~19 uncovered routes are all real-data-mutating endpoints already absent by design, consistent with the pattern this audit confirms rather than disputes: `POST /cash/transaction`, `POST /portfolio/position`, `POST /portfolio/snapshot`, `POST`/`PATCH`/`DELETE /alerts/rules`, `POST /alerts/evaluate`, `POST`/`PATCH /settings`, `POST /signals/generate`, `DELETE /signals/{id}`, `POST /notifications/mark-all-read`, `PATCH /notifications/{id}`, `POST /positions/{id}/exit`, `PATCH /positions/{id}/mark-reviewed`, `PATCH /positions/{id}/note`, `PATCH /positions/{id}/tags`, `PATCH /watchlist/{id}`. All would mutate the live single-portfolio production system's real financial/trading state, or (for `POST /test/endpoints` itself) are a recursive self-call. See the disposition comment block added directly above `test_cases`'s closing bracket in `backend/routers/test.py` for the enumerated list kept in sync with the code.

## Fallback count maintenance (CLAUDE.md §2 / quality_gate.yml "Endpoint Count Drift Check")

`test_cases`'s AST-verified element count moved from 102 to 109 (+7, matching the fixes above). Updated in the same commit:
- `src/pages/SystemStatus.js`: `totalTests || '102'` → `totalTests || '109'`
- `tests/e2e/system-status.spec.js`: `SC-SS-01b` assertion and its running count-history comment updated to 109

Verified via the same AST-parsing method the CI gate uses (`ast.parse` on `test_cases`'s list literal, not a naive `"name":` regex count — that would over-count due to an unrelated nested `{"body": {"name": "__test__", ...}}` payload and a separate smaller `critical_tests` list elsewhere in the same file).

## Disposition

7 fixed, 2 deliberately excluded with documented rationale (not filed as backlog items — these are permanent, correct exclusions, not deferred work), 19 pre-existing exclusions confirmed correct rather than re-litigated. No backlog item filed — this story's own AC ("gap found is filed **or fixed**") is satisfied by fixing directly, since all genuinely-fixable gaps were low-risk and small.

## Sign-off

**QA & Testing Owner:** Confirmed — full coverage audit against all 128 routes; 7 safe gaps fixed, 2 correctly excluded with documented rationale; fallback count kept in sync per the existing drift-detection convention. 2026-07-29.
