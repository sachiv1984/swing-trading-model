Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-02

# QA Evidence — EPIC-01 (Backend Correctness & Security Hardening)

**EPIC:** EPIC-01 — Backend Correctness & Security Hardening
**Cycle:** 2026-07-02__release-v6.4
**Sprint goal:** Deliver v6.4's mandatory production correctness fix, AI prompt-injection security hardening, full AUD-2026-07-01 lifecycle-audit remediation, and the Strategy Benchmark Open Positions panel (with accessibility contrast and Playwright coverage fixes) in a single sealed sprint.
**Test scenarios used:** `tests/test_signal_sizing.py`, `tests/test_nightly_computations.py`, `tests/test_ai_chat_schema.py`, `tests/test_signal_write_sanitization.py` (new — ST-03)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-01 | `docs/specs/api_contracts/signal_endpoints.md#POST /signals/generate`, `docs/specs/api_contracts/ticker_universe_api_contract.md` | `signal_service.generate_momentum_signals()` now sources its ticker universe via `services.ticker_universe_service.get_all_tickers(active_only=True)` instead of the deprecated `database.get_all_tickers()` (`tickers` table). | AC-01 (source from `ticker_universe`): Pass. AC-02 (live parity, verified via Ticker Universe Management add/deactivate): Pass with notes — staging-only per `sprint_planning_notes.md`, not CI-reproducible; deferred to post-merge staging sign-off. AC-03 (no regression to signal fields/sizing): Pass — full backend suite green both before and after change. | Pass with notes | None |
| ST-02 | `docs/specs/security/ai_injection_risk_assessment.md#Input 2 — context_opts.ticker (POST /ai/chat only)`, `docs/specs/api_contracts/ai_endpoints.md#POST /ai/chat` | `ai_service.ai_chat()` validates `context_opts.ticker` via `_validate_context_ticker()` before system-prompt interpolation — rejects (HTTP 422) any value not fully matching `[A-Z0-9.:/-]{1,20}` using `re.fullmatch`. | AC-01 (validated before insertion): Pass. AC-02 (newline/injection rejected 422): Pass. AC-03 (unit test added): Pass — 15 tests in `test_ai_chat_schema.py`. AC-04 (Cybersecurity & Trust Lead sign-off): Pass — cleared after 1 retry (see Findings below). | Pass | None |
| ST-03 | `docs/specs/security/ai_injection_risk_assessment.md#Input 5 — Signal ticker and market strings` | `database._sanitize_signal_string()` strips characters outside `[A-Za-z0-9.\-/:]` and caps at 12 chars; applied in `create_signal()`, `create_rebalance_exit_signal()`, and `update_signal()` (all three signal write/mutate paths). | AC-01 (write path validates ticker/market): Pass — covers all 3 write paths. AC-02 (existing signals reviewed): Pass with notes — live-DB task outside CI reach, deferred and tracked as `BLG-SEC-07`. AC-03 (Cybersecurity & Trust Lead sign-off): Pass — cleared after 1 retry (see Findings below). | Pass with notes | None (2 new backlog items filed: `BLG-SEC-07`, `BLG-SEC-08` — see Findings) |

**QA test coverage:**
- Scenarios run: `tests/test_signal_sizing.py` (26), `tests/test_nightly_computations.py`, `tests/test_ai_chat_schema.py` (15, incl. 7 new ST-02 tests), `tests/test_signal_write_sanitization.py` (11, new — ST-03). Full backend suite: **569 passed, 2 skipped, 0 failed** (`pytest tests/ --ignore=tests/e2e`).
- Regression areas checked: signal generation pipeline (ticker sourcing, sizing), AI chat context handling, all signal write/mutate paths (INSERT and PATCH).
- Known deviations filed: None (no spec-vs-implementation divergence). Two backlog items filed for scope explicitly deferred/discovered during execution — see Findings.

**Findings from Cybersecurity & Trust Lead sign-off review (both retried once, then cleared):**
- ST-02: first-pass review caught a regex bypass — `re.match(r'^[A-Z0-9.:/-]{1,20}$')` matches before a trailing `\n` in Python, so `"AAPL\n"` was incorrectly accepted. Fixed by switching to `.fullmatch()` on an unanchored pattern; added a regression test for the exact bypass case.
- ST-03: first-pass review caught that `PATCH /signals/{id}` (`database.update_signal()`) was a second, unprotected signal write path bypassing the INSERT-time sanitization entirely. Fixed by sanitizing `ticker`/`market` keys in `update_signal()` before building the SQL `SET` clause; added 3 regression tests. A secondary, broader finding (arbitrary dict keys used as unvalidated SQL column names in `update_signal()`) was scoped out of this story and filed as `BLG-SEC-08` for follow-up.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend component in this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-07-02
- Comments: EPIC-01 is not eligible for the BLG-GOV-19 autonomous class — ST-01 AC-02 requires a staging run (not verifiable by code review alone), which fails Criterion 2. Standard sign-off applied via agent-mediated Director of Quality review (§5.3) of the consolidated evidence above, including the two Cybersecurity & Trust Lead story-level sign-offs (ST-02 AC-04, ST-03 AC-03) and their associated findings/fixes. Two staging-only ACs (ST-01 AC-02, ST-03 AC-02) are tracked for post-merge follow-up — ST-01 AC-02 via staging sign-off, ST-03 AC-02 via `BLG-SEC-07`.
