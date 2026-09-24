Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-24

# QA Evidence — EPIC-03 (Backend Reliability & Financial Correctness)

**EPIC:** EPIC-03 — Backend Reliability & Financial Correctness
**Cycle:** 2026-09-23__release-v9.7
**Sprint goal:** Ship PO-05 Lightweight Replay Mode end-to-end and clear the full-capacity, category-balanced debt-clearance slice across 7 EPICs, 29 stories.
**Test scenarios used:** tests/test_money_arithmetic_golden.py, tests/test_reflection_reminder.py, tests/test_alerts_service.py, tests/test_month_closure_clock_source.py, tests/test_monthly_pnl_snapshot.py

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-08 | spec_reference_not_applicable (Case E — bug fix, no prior canonical spec) | `calculate_uk_entry_fees`/`calculate_us_entry_fees`/`calculate_uk_exit_fees`/`calculate_us_exit_fees` now round `stamp_duty`/`fx_fee`/`total` via a new `_round_half_up()` helper (Decimal + ROUND_HALF_UP) instead of leaving float rounding to the caller. | All four fee functions round via Decimal/ROUND_HALF_UP; documented discrepancy tests no longer reproduce; full fee/sizing suite passes | Pass | None |
| ST-09 | docs/specs/api_contracts/alerts_endpoints.md v0.9 | `_evaluate_reflection_reminders` defers `enqueue_delivery` until after `RELEASE SAVEPOINT` succeeds and resets `notifications_created`/`delivery_tasks_enqueued` to 0 on a mid-loop rollback; documented the pre-existing NULL-portfolio exclusion as intentional. | Forced mid-loop failure reports 0 created/0 enqueued and schedules nothing; NULL-portfolio behaviour documented and asserted by a test | Pass | None |
| ST-10 | docs/specs/api_contracts/alerts_endpoints.md v0.10 | Generic re-delivery query gains `AND read = FALSE`, in addition to the existing `delivered = FALSE`/`delivery_attempts < 3`. | A read notification is never re-enqueued for delivery; unread, undelivered notifications still retried up to 3 times | Pass | None |
| ST-11 | spec_reference_not_applicable (Case E — bug fix, no prior canonical spec) | `database.get_monthly_pnl()`'s 1-year window bound derives "today" via `(NOW() AT TIME ZONE 'UTC')::date` instead of bare `CURRENT_DATE`, aligning with `reports_service._is_closed_month`'s UTC-based clock. | A test asserts the same (year, month) clock source is used by both the SQL window and the closed-month check regardless of server timezone setting | Pass | None |
| ST-12 | spec_reference_not_applicable (Case E — performance fix, no prior canonical spec) | `get_monthly_pnl_snapshot`/`insert_monthly_pnl_snapshot_if_absent`/`ensure_monthly_pnl_snapshots_table` accept an optional shared `conn`; `get_monthly_pnl_report()` opens at most one additional connection (only when a closed month is present) and reuses it for every closed month. | `GET /reports/monthly-pnl` opens at most one additional connection regardless of how many closed months are in the response | Pass | None |
| ST-13 | docs/specs/api_contracts/ai_endpoints.md v1.14 | Reviewed and documented, as intentional, that `latency_ms`/`elapsed_ms` around retried Anthropic calls includes retry backoff sleep time — no code behaviour change. | Disposition recorded: won't-fix/intentional, applied consistently across `ai_service.py`, `gemini_service.py`, `debrief_service.py` (all three cross-reference the same decision) | Pass | None |

**QA test coverage:**
- Scenarios run: tests/test_money_arithmetic_golden.py (32), tests/test_reflection_reminder.py (30), tests/test_alerts_service.py (35), tests/test_month_closure_clock_source.py (2), tests/test_monthly_pnl_snapshot.py (16), plus broader regression sweeps (sizing/fee/calculation: 98; monthly-pnl/reports/tax-year: 99; alerts: 98; ai_service/gemini/debrief: 49) — all via `backend/.venv/bin/python3 -m pytest` per CLAUDE.md §9, no live DB or network calls.
- Regression areas checked: money-arithmetic/sizing, alerts evaluation (reflection reminders, generic re-delivery), monthly P&L reporting (clock source, snapshotting/connection reuse), AI service latency logging.
- Known deviations: None found — all six stories' deviation checks completed with nothing to file.
- Out-of-scope finding filed during this EPIC: BLG-QA-192 (pre-existing, unrelated `inspect.getsource()`-against-a-mock gap in `tests/test_null_fee_trade_audit.py`, confirmed reproducing on `main` before any of this EPIC's changes — not fixed here, filed per CLAUDE.md §2's out-of-scope-finding exception).

---

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-08 through ST-13, all six)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required, no live system interaction — ✓ (all verification was via mocked/unit tests; no live or staging database was queried for any of the six stories)
- [x] Criterion 3: No frontend-visible change — ✓ (no file under `src/components/**` or `src/pages/**` touched; all changes are in `backend/`, `tests/`, and `docs/specs/api_contracts/`)
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-09-24
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review/test-verifiable with no live-system interaction, no frontend changes, engine signer populated). Still subject to the STEP 4 merge gate; Product Owner acceptance remains a separate, always-human gate (CLAUDE.md §2) not satisfied by this sign-off.
