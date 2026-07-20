Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-20

# QA Evidence Log — EPIC-08 (v7.6)

## Consolidation Block

**EPIC:** EPIC-08 — Ticker/market input sanitisation regression suite
**Cycle:** 2026-07-20__release-v7.6
**Sprint goal:** Ship print/PDF export for WeeklyDigest and TradePlan (BLG-FE-119) and clear six ready backend/QA/documentation items to fully utilise this sprint's confirmed capacity.
**Test scenarios used:** `tests/test_ticker_market_sanitization_regression.py` (7 scenarios, new — this item's deliverable) + `tests/test_signal_write_sanitization.py` and `tests/test_ai_chat_schema.py` (pre-existing, exhaustive per-path coverage, confirmed still passing and still covering all 4 paths).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-08 | `tests/test_ticker_market_sanitization_regression.py` | A dedicated, clearly-named regression suite consolidating coverage of all 4 previously-vulnerable ticker/market write paths (`create_signal`, `create_rebalance_exit_signal`, `update_signal`, AI chat `context_opts.ticker`) — one high-signal assertion per attack class per path. Confirmed the CI-trigger AC is already satisfied by the existing unconditional `pytest tests/` run in `ci-tests.yml` Phase B (no path filter — runs on every PR regardless of files changed, a superset of the named trigger paths). | Regression suite covers all 4 previously-vulnerable paths; suite runs in CI on every PR touching `signal_service.py`, `database.py`, or `ai_service.py`; Director of Quality sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_ticker_market_sanitization_regression.py` — 7/7 passing (`DATABASE_URL=<dummy> pytest tests/test_ticker_market_sanitization_regression.py`)
- Regression areas checked: cross-verified against `tests/test_signal_write_sanitization.py` (BLG-SEC-02/BLG-SEC-08, 3 paths) and `tests/test_ai_chat_schema.py` (BLG-SEC-01, 1 path) — no duplication of their exhaustive coverage, this suite is a focused consolidated guard sitting alongside them
- Known deviations filed: None

## CI Trigger Verification (Quality AC)

Read `.github/workflows/ci-tests.yml` directly (not assumed): `pytest-phase-b` runs `python -m pytest tests/ -v --tb=short` unconditionally on every `pull_request` to `main`/`develop` and every `push` to `exec/**`/`main`/`develop` — no `paths:` filter restricts it to specific files. This means the regression suite (and its 2 sibling files) already runs on every PR, which is a strict superset of "every PR touching `backend/services/signal_service.py`, `database.py`, or `ai_service.py`." No CI configuration change was required or made.

## Autonomous Class Eligibility Check (BLG-GOV-19)

- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-08 only, autonomous)
- [x] Criterion 2: All AC verifiable by code review alone plus the local pytest run recorded above — ✓
- [x] Criterion 3: No frontend-visible change — ✓ (only `tests/test_ticker_market_sanitization_regression.py` touched; no files under `src/components/**` or `src/pages/**`)
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-20
- Comments: Autonomous class sign-off — all four qualifying criteria met. Confirmed both underlying security fixes (BLG-SEC-01, BLG-SEC-02) already had dedicated test files with the exact injection/trailing-newline-bypass/invalid-value coverage the AC describes, and confirmed via direct workflow-file read (not assumption) that CI already runs the full test suite unconditionally on every PR. This item's value-add is the consolidated, single-file entry point the AC asks for — 7 focused regression tests, all passing, with no duplication of the existing exhaustive per-path coverage.
