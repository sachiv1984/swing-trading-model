Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-16

---

## Consolidation Block

**EPIC:** EPIC-01 — Backend & Platform Engineering Debt
**Cycle:** 2026-09-15__release-v9.5
**Sprint goal:** Clear the full v9.5 debt-reduction scope — 43 items across 6 EPICs — at the top of confirmed sprint capacity, resolving the cycle's two genuine ungated P1 items first. See `sprint_goal.md`.
**Test scenarios used:** `tests/test_changelog_service.py`, `tests/test_json_log_formatter.py`, `tests/test_root_logging_config.py`, `tests/test_correlation_id_propagation.py`, `tests/test_router_error_envelope_conformance.py`, plus the full backend suite (`tests/` minus `tests/e2e/`).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-01 | N/A — no governing spec, verification only | `BLG-BE-117`/ST-01 was already resolved by commit `58a8d53c` (2026-09-14), before this cycle's Release Planning ran — carried into v9.5 scope as a stale duplicate. Re-verified: `test_real_changelog_is_parseable` passes; last 10 CI runs on `main` green. No code change. | Both AC bullets met (pre-existing fix). | Pass | None |
| ST-02 | `docs/specs/structured_logging_standards.md#Structured Log Format` | `backend/main.py` now installs `JsonLinesFormatter` (new `backend/utils/json_log_formatter.py`) on the root logger, replacing the plain-text format string. `service` field revised from a stale 5-value enum to the dotted logger name (spec bumped 0.1.1→0.2.0). Resolves `DEV-v9.3-ST03-01`. | Both AC bullets met — JSON Lines output conforms to spec; no monitoring/alerting found to depend on the prior plain-text layout (confirmed by repo-wide search). | Pass | None |
| ST-03 | N/A — bug fix, no new artefact (`screener_api_contract.md` unchanged) | `backend/routers/screener.py`'s `GET /screener/results` and `GET /screener/history` now return HTTP 400 `INVALID_PARAMS` for a negative `limit` or `offset`. Swept all other routers for the same pattern. | Both AC bullets met — negative values rejected with 400; the "any other endpoint" sweep found one further gap (`backend/routers/backtest_rule_change.py`), filed as `BLG-BE-118` rather than fixed in-scope. | Pass | `BLG-BE-118` (follow-up, different endpoint) |
| ST-04 | `claude/strategy/strategy_rules.md#7.2 Profit-aware stop logic` | **Blocked, not in this PR.** Diffing the 3 named implementations (production `calculate_trailing_stop`, backtest tool `position_manager.py`, and `tests/test_stop_reconciliation.py`'s spec-formula test helper) per this story's own Notes instruction surfaced a genuine, previously-uncaught divergence: production applies an entry-price floor for profitable positions that neither the canonical spec nor the backtest tool implements. This is a live-trading risk-logic correctness question the engine cannot resolve unilaterally. Filed as `BLG-BE-119`; reclassified `autonomous` → `delegated_decision` (`DEL-20260916-01`); story remains open, to resume once Strategy Rules & System Intent Owner ratifies which formula is correct. | Not evaluated — blocked before implementation. | Blocked | `BLG-BE-119` (blocking) |

**QA test coverage:**
- Scenarios run: `tests/test_changelog_service.py` (6), `tests/test_json_log_formatter.py` (9, new), `tests/test_root_logging_config.py` (4), `tests/test_correlation_id_propagation.py` (9), `tests/test_router_error_envelope_conformance.py` (Screener subset, 5, 4 new) — plus full backend suite re-run clean after each story: 1495 passed (ST-02), 1499 passed (ST-03), 10 skipped throughout, 0 failed.
- Regression areas checked: root logger configuration/handler behaviour (unaffected by the formatter swap — verified by existing tests), correlation-ID propagation (unaffected), screener pagination upper-bound behaviour (unaffected — existing `limit > 200` tests still pass).
- Known deviations: `DEV-v9.3-ST03-01` resolved this EPIC (ST-02). No new deviation filed against a shipped story. ST-04 blocked on `BLG-BE-119` (not a deviation against shipped work — the story itself has not shipped).

---

## Sign-Off Block

**Mixed-Class EPIC** (ST-04 `delegated_decision`, blocked/excluded from this PR; ST-01/ST-02/ST-03 `autonomous`, shipped) — per the Mixed-Class EPIC Signer Format Note, the BLG-GOV-19 autonomous class is unavailable (Criterion 1 fails: EPIC contains a non-autonomous story) even though every story actually shipped in this PR is autonomous. Using the agent-mediated format for full transparency about ST-04's status.

- [x] All acceptance criteria verified against canonical spec — for the 3 shipped stories (ST-01/02/03); ST-04 excluded and tracked open
- [x] No unresolved P0 or P1 deviations — `BLG-BE-118`/`BLG-BE-119` are P3/P2 follow-ups, not blockers to shipping ST-01–03
- [x] Regression areas checked — full backend suite green after each shipped story
- [x] N/A — no frontend component in this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-16
- Comments: This EPIC's PR covers ST-01, ST-02, ST-03 only. ST-04 is explicitly excluded pending `BLG-BE-119` resolution — see Consolidation Block row above and `delegation_log.md` `DEL-20260916-01`. Agent-mediated sign-off performed per §5.3 protocol (subagent review against `director_of_quality.md` §5 quality bar); findings: none blocking — see review notes below.
