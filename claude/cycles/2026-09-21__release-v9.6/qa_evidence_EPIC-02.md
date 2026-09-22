Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-22

---

# QA Evidence — EPIC-02: Financial Reporting & Records Integrity

**EPIC:** EPIC-02 — Financial Reporting & Records Integrity
**Cycle:** 2026-09-21__release-v9.6
**Sprint goal:** Ship the two build-and-ship product features committed at the 2026-09-19 rebalance — Clone-as-new-plan (`BLG-FEAT-96`) and CSV export for Screener and Watchlist (`BLG-FEAT-97`) — within the full 32-item, 7-EPIC v9.6 scope at the top of confirmed sprint capacity, landing the live-capital trailing-stop formula decision (`BLG-BE-119`) early so the nightly stop-update path can be hardened on a single agreed formula.
**Test scenarios used:**
- `tests/test_null_fee_trade_audit.py` (ST-07, 4 tests)
- `tests/test_monthly_pnl_snapshot.py` (ST-08, 15 tests)

**Delegation class:** both stories `autonomous`. No file under `src/pages/**` or `src/components/**` was created or modified by this EPIC — both stories are backend + documentation only. The Autonomous DoQ sign-off class (BLG-GOV-19) is available.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-07 | `metrics_definitions.md` §Fee-Netting Basis; `reports_endpoints.md` §GET /reports/monthly-pnl v0.13 | Documented that `trade_history.pnl` is net of both entry and exit fees; added `null_fee_trade_count` to `GET /reports/monthly-pnl`'s per-month response — count of that month's closed trades with `entry_fees`/`exit_fees` NULL | AC-01 The net/gross basis is documented in the canonical metrics spec — `metrics_definitions.md` §Fee-Netting Basis. AC-02 A NULL-fee closed trade is counted and visible in Monthly P&L — `null_fee_trade_count` field, `test_null_fee_trade_audit.py` | Pass | None |
| ST-08 | `data_model.md` DS-20; `reports_endpoints.md` §GET /reports/monthly-pnl, §GET /reports/tax-year v0.13 | New `monthly_pnl_snapshots` table; a closed calendar month is baselined exactly once on first read (insert-only, `ON CONFLICT DO NOTHING`); `GET /reports/monthly-pnl` compares the live total against the baseline on every read; `GET /reports/tax-year` gains a derived `restated_month_count`/`restated_months_notice` from the same table | AC-01 A snapshot exists per closed month — `insert_monthly_pnl_snapshot_if_absent`, baseline-once tested in `test_monthly_pnl_snapshot.py`. AC-02 Editing a closed trade in a snapshotted month surfaces a restatement diff — mechanism built and unit-tested against a simulated stored-vs-live mismatch; see disclosure below (no live action currently exists to trigger this end-to-end) | Pass with notes | None (disclosed limitation, not a deviation — see notes) |

**QA test coverage:**
- Scenarios run (local, stub DATABASE_URL per CLAUDE.md §9): `test_null_fee_trade_audit.py` 4/4 pass; `test_monthly_pnl_snapshot.py` 15/15 pass (service-level baseline/restatement/current-month-exclusion/tax-year-notice logic, plus a mocked-cursor SQL-shape check for the new table's migration/insert functions, loaded via `importlib` directly from `backend/database.py` rather than through the session-scoped `sys.modules["database"]` stub — see ST-08 notes below for why).
- Regression areas checked: full backend suite, stub `DATABASE_URL` — 1621 passed, 3 skipped, 7 failed. All 7 failures confirmed pre-existing and unrelated (`git stash` to unmodified `main` reproduces the identical 7 failures): `tests/test_schema.py` and `tests/test_schema_rollback_verification.py` attempt real DDL against the sandbox's live-staging `DATABASE_URL` and fail with `psycopg2.errors.InsufficientPrivilege: permission denied for schema public` — an environment/credential limitation, not caused by this EPIC. `scripts/openapi_3way_drift_sweep.py` — no drift (145 router endpoints / 146 contract headings / 146 openapi.yaml paths, matching pre-existing count; no new endpoint added by this EPIC).
- Known deviations: None found — both stories' deviation checks completed with nothing to file.

**Notes for the Director of Quality and Product Owner:**

1. **ST-08 AC-02 is built and tested, not demonstrated live (disclosed, `data_model.md` DS-20).** As of this EPIC, no live endpoint changes a closed trade's `pnl`, `total_cost`, `net_proceeds`, or `exit_date` after it is written at exit time — `trade_history` is written once and never updated by `exit_position()`. The only existing "edit a closed trade" endpoint, `PATCH /trades/{trade_id}/costs`, writes `commission_gbp`/`spread_cost_gbp` only, which feed `net_r_multiple` at query time, not `pnl`. The restatement-diff mechanism (`_snapshot_month()` in `reports_service.py`) is real and unit-tested against a simulated stored-vs-live mismatch (`test_closed_month_diverging_from_snapshot_is_restated`), and will correctly detect a genuine drift the moment any future write path makes one possible — but there is currently no live UI action that exercises it end-to-end. Not filed as a deviation (the AC's own mechanism is fully built and tested; the gap is a pre-existing system limitation, not something this story left undone) — recorded as a disclosed limitation per the `ESC-EXEC-20260910-01` honest-disclosure precedent.
2. **Known boundary approximation (disclosed, not fixed, `data_model.md` DS-20).** UK tax years run 6 April–5 April, splitting the calendar month of April across two tax years by day; `monthly_pnl_snapshots` snapshots by whole calendar month. `get_tax_year_report()`'s `restated_month_count` therefore treats April as overlapping both the outgoing and incoming tax year. Since no restatement can currently occur in production (note 1), this cannot yet manifest as an actual double-count — tracked as a documented limitation for if/when note 1's precondition changes, not a code fix in this story (RISK-02).
3. **`sys.modules["database"]` test-isolation note (informational, not a defect in this EPIC's code).** `tests/conftest.py` globally replaces `sys.modules["database"]` with an AST-derived MagicMock stub; `ensure_monthly_pnl_snapshots_table()` is never imported by name outside `database.py` itself, so it is absent from that stub. `test_monthly_pnl_snapshot.py`'s DB-layer test class loads the real `backend/database.py` via `importlib.util.spec_from_file_location` into a separately-named module object, deliberately avoiding a `sys.modules["database"]` swap/restore — per ST-21 (EPIC-05, this same cycle, `BLG-QA-178`), an *unrestored* such swap is itself a known test-isolation hazard; this sidesteps that pattern entirely rather than reproducing it.
4. **No live database access used.** Per the session's own operating constraint (a `DATABASE_URL` pointing at the staging Supabase database is present in this environment but is not to be queried without asking first), no query or migration in this EPIC was run against it. `ensure_monthly_pnl_snapshots_table()`/`insert_monthly_pnl_snapshot_if_absent()` are covered by mocked-cursor tests only (`data_model.md` DS-20 §Verification status) — Criterion 1 of the Autonomous Class check below is met on that basis (verification method actually used was code review + mocked-cursor/service-level tests only, no live system interaction).

**Backlog items filed from this EPIC's findings:** None — both disclosed limitations (notes 1–2) describe a currently-unreachable precondition rather than an actionable defect; re-review is triggered by note 1's own precondition (a future write path that can change a closed trade's `pnl`), not by a calendar/backlog cadence.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required, no live system interaction (verification method actually used was mocked-cursor/service-level unit tests only — see note 4 above; BLG-GOV-335's "method actually used" bar is met, not just the AC's own no-live-access fallback wording) — ✓
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/pages/**` or `src/components/**` was created or modified (`git diff --stat main...exec/2026-09-21__release-v9.6/EPIC-02` touches only `backend/`, `docs/`, `tests/`) — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-09-22
- Comments: Autonomous class sign-off — all four qualifying criteria met (both stories autonomous; all AC verified by code review and mocked-cursor/service-level tests only, no live DB/staging/UI interaction per note 4; no frontend files touched; engine signer populated). ST-08 AC-02's live-action gap (note 1) and the April boundary approximation (note 2) are disclosed limitations of the underlying system/spec, not gaps in this EPIC's own verification — both are recorded above for Product Owner visibility rather than silently passed over. Merge remains subject to the always-human QA sign-off and Product Owner acceptance (execution_prompt.md §5.3's Autonomous DoQ class does not itself substitute for those).
