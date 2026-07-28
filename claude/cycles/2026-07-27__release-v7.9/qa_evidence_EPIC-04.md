Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

## Consolidation Block

**EPIC:** EPIC-04 — Monthly P&L CSV export: tax-lot cost-basis reconciliation
**Cycle:** 2026-07-27__release-v7.9
**Sprint goal:** Ship all 15 v7.9 EPICs — the two P1 UX anchors and the 13 capacity-fill engineering-hardening items — with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_monthly_pnl_cost_basis.py` (4 tests, all passing, including a hand-computed two-position reconciliation sample).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-04 | `backend/services/reports_service.py#build_monthly_pnl_csv` | Trailing "Cost Basis Method" disclosure row appended after the existing month table (additive only — main table byte-identical to before). Disclosure states the method is "Specific Identification (per-position lot)", not FIFO — verified by tracing `get_monthly_pnl()`, `calculate_realized_pnl()`, and `exit_position()`: each `trade_history.pnl` reflects that specific position's own `total_cost`, prorated by shares exited; no cross-position pooling of the same ticker occurs anywhere. | AC-01: Export documents its cost-basis method — Pass. AC-02: Reconciles against a manually-verified sample — Pass (hand-computed two-position sample: 150.00 + (-20.00) = 130.00, verified independently by Financial Reporting & Records Owner). AC-03: Financial Reporting & Records Owner sign-off — Pass (agent-mediated). | Pass | None |

**QA test coverage:**
- Scenarios run: `backend/.venv/bin/python3 -m pytest tests/test_monthly_pnl_cost_basis.py -v` — 4/4 passed.
- Regression areas checked: `tests/e2e/monthly-pnl-csv-export.spec.js` reviewed — mocks its own CSV response at the network layer, does not source content from the real backend function, so it is unaffected by this change (no update needed; confirmed by inspection, not modified).
- Known deviations filed: None.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-04 only, autonomous)
- Criterion 2: All AC verifiable by code review alone — ✓ (unit tests + manual arithmetic reconciliation; no UI, no staging run — export is a CSV column addition, no in-app UI rendering per Design Gate exemption)
- Criterion 3: No frontend-visible change — confirmed no file under `src/pages/**` or `src/components/**` was created or modified — ✓
- Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-27
- Comments: Autonomous class sign-off — all four qualifying criteria met. Financial Reporting & Records Owner sign-off (AC-03) obtained separately via agent-mediated review (§5.3): Approved, independently traced the code path to confirm the "Specific Identification, not FIFO" claim and independently re-verified the hand-computed reconciliation sample's arithmetic.
