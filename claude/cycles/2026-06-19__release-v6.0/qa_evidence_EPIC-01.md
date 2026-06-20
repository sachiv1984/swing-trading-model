Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-19

---

# QA Evidence — EPIC-01: Signal Correctness Fast-Track

---

**EPIC:** EPIC-01 — Signal Correctness Fast-Track
**Cycle:** 2026-06-19__release-v6.0
**Sprint goal:** Ship the P0 signal correctness fix and deliver the Trader's Morning Briefing and net-of-costs features to resolve the Product Value Alert, complete Screener data quality telemetry, and advance SI-05 effectiveness reviews as within-sprint gates clear.
**Test scenarios used:** docs/testing/signals_scenarios.md; tests/test_signal_sizing.py (new — added as part of ST-01)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | claude/strategy/strategy_rules.md#4.1; docs/specs/api_contracts/signal_endpoints.md | Replaced cash-allocation model in signal_service.py with calls to sizing_service.size_position(). Removed min/max_position_pct params. Updated main.py. Added tests/test_signal_sizing.py covering AC-02–05. AC-01: Strategy Rules & System Intent Owner sign-off cleared via agent-mediated review (§5.3, 2026-06-19). | AC-01: Strategy Rules owner confirms risk-based formula canonical — Cleared (agent-mediated sign-off). AC-02: signal_service calls size_position() with initial_stop as stop_price — Pass. AC-03: suggested_shares matches entry tab output — Pass (same size_position() function). AC-04: share count independent of concurrent signal count — Pass (risk-based formula doesn't use len(signals)). AC-05: no valid initial_stop → suggested_shares = 0 — Pass (guard check before size_position call). AC-06: cash-allocation model fully removed — Pass. AC-07: existing CI tests pass; test_signal_sizing.py added — Pass. | Pass | None |

**QA test coverage:**
- Scenarios run: tests/test_signal_sizing.py (new — AC-02, AC-03, AC-04, AC-05 covered); existing test_api_contracts.py (mocks generate_momentum_signals, unaffected)
- Regression areas checked: signal generation endpoint (POST /signals/generate); existing GET /signals endpoint (unaffected — mocked in tests)
- Known deviations filed: None

---

## Autonomous class eligibility check (BLG-GOV-19)

- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-01: autonomous)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ (backend correctness fix + unit tests; no live signal generation required to verify)
- [x] Criterion 3: No frontend-visible change — confirmed: only backend/services/signal_service.py, backend/main.py, and tests/test_signal_sizing.py modified; no src/pages/ or src/components/ files touched — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-06-19
- Comments: Autonomous class sign-off — all four qualifying criteria met. AC-01 additionally cleared by Strategy Rules & System Intent Owner via agent-mediated sign-off (§5.3, 2026-06-19). Implementation replaces cash-allocation model with canonical §4.1 risk-based formula — correctness violation resolved.
