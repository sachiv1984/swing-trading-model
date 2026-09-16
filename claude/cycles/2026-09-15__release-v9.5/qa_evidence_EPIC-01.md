Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-16

---

## Consolidation Block

**EPIC:** EPIC-01 — Backend & Platform Engineering Debt
**Cycle:** 2026-09-15__release-v9.5
**Sprint goal:** Clear the full v9.5 debt-reduction scope — 43 items across 6 EPICs — at the top of confirmed sprint capacity, resolving the cycle's two genuine ungated P1 items first. See `sprint_goal.md`.
**Test scenarios used:** `tests/test_changelog_service.py`, `tests/test_json_log_formatter.py`, `tests/test_root_logging_config.py`, `tests/test_correlation_id_propagation.py`, `tests/test_router_error_envelope_conformance.py`, `tests/test_trailing_stop_breakeven_floor.py`, `tests/test_stop_reconciliation.py`, plus the full backend suite (`tests/` minus `tests/e2e/`).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-01 | N/A — no governing spec, verification only | `BLG-BE-117`/ST-01 was already resolved by commit `58a8d53c` (2026-09-14), before this cycle's Release Planning ran — carried into v9.5 scope as a stale duplicate. Re-verified: `test_real_changelog_is_parseable` passes; last 10 CI runs on `main` green. No code change. | Both AC bullets met (pre-existing fix). | Pass | None |
| ST-02 | `docs/specs/structured_logging_standards.md#Structured Log Format` | `backend/main.py` now installs `JsonLinesFormatter` (new `backend/utils/json_log_formatter.py`) on the root logger, replacing the plain-text format string. `service` field revised from a stale 5-value enum to the dotted logger name (spec bumped 0.1.1→0.2.0). Resolves `DEV-v9.3-ST03-01`. | Both AC bullets met — JSON Lines output conforms to spec; no monitoring/alerting found to depend on the prior plain-text layout (confirmed by repo-wide search). | Pass | None |
| ST-03 | N/A — bug fix, no new artefact (`screener_api_contract.md` unchanged) | `backend/routers/screener.py`'s `GET /screener/results` and `GET /screener/history` now return HTTP 400 `INVALID_PARAMS` for a negative `limit` or `offset`. Swept all other routers for the same pattern. | Both AC bullets met — negative values rejected with 400; the "any other endpoint" sweep found one further gap (`backend/routers/backtest_rule_change.py`), filed as `BLG-BE-118` rather than fixed in-scope. | Pass | `BLG-BE-118` (follow-up, different endpoint) |
| ST-04 | `claude/strategy/strategy_rules.md#7.2 Profit-aware stop logic` (v1.9→v1.10) | Diffing the 3 named implementations surfaced production's entry-price floor diverging from the spec's literal text (filed `BLG-BE-119`, `DEL-20260916-01`). On resolving (§5.3, acting as Strategy Rules & System Intent Owner on explicit user direction), found `BLG-BE-102` (archived, P0, v8.9) had already investigated and settled this exact question: the floor is intentional live behaviour, and `position_manager.py`'s simpler backtest formula is a deliberate, already-tested exception. Ratified the floor into `strategy_rules.md` §7.2 (documentation-only, no live code change) — see `DEL-20260916-02`. | Both AC bullets met — single shared implementation confirmed to already exist for the 2 production call sites; the test-helper "3rd site" is intentionally independent (not a consolidation gap). | Pass | `BLG-BE-119` (resolved this session, awaiting `groom backlog` retirement) |

**QA test coverage:**
- Scenarios run: `tests/test_changelog_service.py` (6), `tests/test_json_log_formatter.py` (9, new), `tests/test_root_logging_config.py` (4), `tests/test_correlation_id_propagation.py` (9), `tests/test_router_error_envelope_conformance.py` (Screener subset, 5, 4 new), `tests/test_trailing_stop_breakeven_floor.py` + `tests/test_stop_reconciliation.py` (20, re-confirmed unaffected by ST-04's documentation-only resolution) — plus full backend suite re-run clean after each story: 1495 passed (ST-02), 1499 passed (ST-03), 10 skipped throughout, 0 failed.
- Regression areas checked: root logger configuration/handler behaviour (unaffected by the formatter swap — verified by existing tests), correlation-ID propagation (unaffected), screener pagination upper-bound behaviour (unaffected — existing `limit > 200` tests still pass), trailing-stop breakeven-floor and backtest reconciliation behaviour (unaffected — ST-04 changed documentation only, no code).
- Known deviations: `DEV-v9.3-ST03-01` resolved this EPIC (ST-02). No new deviation filed against a shipped story.

---

## Sign-Off Block

**Mixed-Class EPIC** (ST-04 `delegated_decision`; ST-01/ST-02/ST-03 `autonomous`) — per the Mixed-Class EPIC Signer Format Note, the BLG-GOV-19 autonomous class is unavailable (Criterion 1 fails: EPIC contains a non-autonomous story). Using the agent-mediated format.

- [x] All acceptance criteria verified against canonical spec — all 4 stories
- [x] No unresolved P0 or P1 deviations — `BLG-BE-118`/`BLG-BE-119` are P3/P2 follow-ups (both resolved or filed as tracked follow-ups, neither blocking)
- [x] Regression areas checked — full backend suite green after every story; trailing-stop suites re-confirmed after ST-04
- [x] N/A — no frontend component in this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Signed off by: Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3, on explicit user direction)
- Date: 2026-09-16
- Comments: All 4 stories now shipped in this PR. ST-04 was initially blocked pending a strategy decision (`DEL-20260916-01`); on resuming (user: "act as relevant agent and resolve"), found the decision had already been made and validated at `BLG-BE-102`/v8.9 — resolved as a documentation-only fix to `strategy_rules.md` §7.2, no live code change (`DEL-20260916-02`). Director of Quality sign-off performed per §5.3 protocol (independent subagent review of ST-01–03, Approved — re-ran full suite live, 1499 passed); Strategy Rules & System Intent Owner sign-off for ST-04 performed by this engine directly on explicit user direction, following the precedent already established for `qa_evidence_EPIC-04.md` ST-15 at `2026-09-14__release-v9.4`.
