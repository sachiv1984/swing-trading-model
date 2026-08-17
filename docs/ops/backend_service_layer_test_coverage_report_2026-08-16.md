**Owner:** Head of Engineering; QA & Testing Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-16
**Story:** ST-19 (BLG-QA-143, EPIC-04, v8.8)

# Consolidated Backend Service-Layer Test-Coverage Report

## 1. Purpose

No consolidated report previously identified which `backend/services/*.py` files lack a direct unit test, making coverage gaps hard to spot without an ad hoc grep each time. This report generates that inventory once and triages every gap found.

## 2. Method

`backend/services/` contains **40** service modules (excluding `__init__.py`). For each, searched `tests/*.py` (107 files) for any reference to the bare module name (`grep -rl "\b<module>\b" tests/*.py`) — this catches both `import services.<module>` and `from <module> import ...` styles, both used interchangeably across this test suite. A module with zero matches has no direct unit test anywhere in the suite (it may still be exercised indirectly through a router-level integration test, noted per-item below where applicable).

## 3. Result

**35 of 40 (87.5%) service modules have at least one direct unit test file.** 5 modules (12.5%) have none:

| Service | Live? (call site) | Indirect coverage | Notes |
|---------|-------------------|--------------------|-------|
| `cash_service.py` | Yes — `backend/main.py:713/737` (`create_transaction`, `get_transaction_history`); `health_service.py` reports its availability | `test_api_contracts.py` hits the cash endpoints at HTTP level (status-code/envelope check only, not calculation correctness) | Real gap — 3 public functions (`create_transaction`, `get_transaction_history`, `get_summary`), none with a dedicated unit test |
| `compliance_service.py` | Yes — `backend/main.py:1363` (`get_position_compliance`) | `test_api_contracts.py` (HTTP-level only) | Real gap — `get_position_compliance()` composes 3 private helpers (`_compute_stop_compliance`, `_compute_stop_age`, `_compute_size_compliance`) with no direct test of any of them |
| `news_service.py` | Yes — `backend/routers/research.py:107-108`, `backend/routers/news.py:9,27` (`get_news_headlines`) | None found | Real gap — no test at any level (router or service) exercises Alpaca-header construction, credential-configured branching, or headline-parsing logic |
| `trade_csv_service.py` | **No live call site found** — `build_trade_history_csv(trades)` is re-exported by `services/__init__.py` but never imported or called by any router. A **second, differently-signatured** function of the exact same name, `trade_service.py::build_trade_history_csv(portfolio_id)`, is the one actually wired to `routers/trades_export.py` | None (nothing to indirectly cover) | **Not a test gap — a dead-code/duplicate-name finding.** Filed separately (§4), not "fix the test," since adding a test for genuinely unreachable code would not close a real risk |
| `validation_service.py` | Yes — `backend/routers/validation.py:19` (`ValidationService.validate_all()`, `GET /validate/calculations`) | `test_api_contracts.py` (HTTP-level only) | Real gap — `ValidationService.validate_all()` and its two helpers (`_check`, `_by_severity`) have no direct unit test of tolerance-threshold or severity-classification logic |

All other 35 modules have at least one dedicated `tests/test_*.py` file (or, for a handful, coverage via a differently-named integration-style file — e.g. `signal_service.py` via `test_formatting.py`, `test_nightly_computations.py`, etc.) confirmed present via the same grep method.

## 4. Gaps Triaged

| Ref | Item | Disposition |
|-----|------|-------------|
| BLG-QA-151 | `cash_service.py`, `compliance_service.py`, `validation_service.py` — no direct unit test for calculation/composition logic (HTTP-level contract tests exist but don't verify correctness of the underlying math/branching) | Filed — see §5 |
| BLG-BE-101 | `trade_csv_service.py::build_trade_history_csv(trades)` appears to be dead/duplicate code — a same-named, differently-signatured function in `trade_service.py` is the one actually used by `routers/trades_export.py` | Filed — see §5 (Head of Engineering to confirm and remove, or document why both exist, following the ST-07/EPIC-02 precedent this same cycle for consolidating divergent duplicate implementations) |
| — | `news_service.py` — no coverage at any level | Rolled into `BLG-QA-151` (same disposition — direct unit test needed) |

## 5. Backlog Items Filed

- **BLG-QA-151** — Add direct unit tests for `cash_service`, `compliance_service`, `news_service`, `validation_service` (P3, QA & Testing Owner)
- **BLG-BE-101** — Confirm `trade_csv_service.py::build_trade_history_csv` is dead code and remove, or document the coexistence with `trade_service.py`'s same-named function (P3, Head of Engineering)

## 6. Sign-Off

- [x] Report generated across all 40 service modules
- [x] Every gap triaged (fixed-now vs filed) — none silently accepted
- [x] Live-call-site check performed for each gap (not just "no test found") — surfaced the `trade_csv_service` dead-code finding this way
- Signed off by: PENDING — see agent-mediated review
- Date: PENDING
