Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-21

---

# QA Evidence — EPIC-01: Product Features & Frontend Build-and-Ship

**EPIC:** EPIC-01 — Product Features & Frontend Build-and-Ship
**Cycle:** 2026-09-21__release-v9.6
**Sprint goal:** Ship the two build-and-ship product features committed at the 2026-09-19 rebalance — Clone-as-new-plan (`BLG-FEAT-96`) and CSV export for Screener and Watchlist (`BLG-FEAT-97`) — within the full 32-item, 7-EPIC v9.6 scope at the top of confirmed sprint capacity, landing the live-capital trailing-stop formula decision (`BLG-BE-119`) early so the nightly stop-update path can be hardened on a single agreed formula.
**Test scenarios used:**
- `tests/e2e/trade-plan-clone.spec.js` (ST-01, SC-TPC-01–06)
- `tests/e2e/trade-plan-stale-marker.spec.js` (ST-02, SC-TPS-01–05)
- `tests/e2e/screener-watchlist-csv-export.spec.js` (ST-03, SC-CSV-01–08 + 04b)
- `tests/e2e/reflection-reminder.spec.js` (ST-04, SC-RR-01–06)
- `tests/test_reflection_reminder.py` (ST-04, 27 tests)
- `tests/e2e/empty-state-next-action.spec.js` (ST-05, SC-ESN-00–06, 11)
- `tests/e2e/number-format-tables.spec.js` (ST-06, SC-NFT-01–06)
- `tests/e2e/number-format-helper.spec.js` (ST-06, SC-NF-01–07)

**Delegation class:** all six stories `autonomous`. The EPIC contains frontend-visible changes (`src/pages/**`, `src/components/**`), so the Autonomous DoQ sign-off class is unavailable (execution_prompt.md §3.2.A Criterion 3) and the Standard Sign-Off Block applies.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `trade_plan.md` §4.5; `decision_record.md` (trade-plan-clone) | "Clone" action on every Trade Plans list row and on the plan detail header → `/TradePlan?clone_from={id}`; pre-populates an unsaved plan (copy/reset table per the record), info banner, failure toast; opt-in `dismissible` prop on `StandingAlert` | AC-01 Clicking Clone opens a new, unsaved plan pre-populated from the source — SC-TPC-02/04. AC-02 Cloned plan has status `draft` (read `planned` as `draft`, addendum), fresh dates, no `position_id` — SC-TPC-03/04. AC-03 Playwright passes in CI — see CI evidence below | Pass with notes | None (implementation notes 1–4 below) |
| ST-02 | `trade_plan.md` §4.6; `decision_record.md` (trade-plan-stale-marker) | Display-only "Stale (N days)" marker on the four pre-entry statuses when whole days since `updated_at` > 14 (`STALE_PLAN_THRESHOLD_DAYS`) | AC-01 A plan older than the threshold shows the marker; a newer plan does not — SC-TPS-01–05 (15d shows, 10d does not, 14/15 boundary, terminal/active never marked). AC-02 Playwright passes in CI — see CI evidence | Pass | None |
| ST-03 | `screener_results.md` §5.3; `watchlist.md` §CSV Export; `decision_record.md` (csv-export) | Shared "Download CSV" button; client-side RFC 4180 export of the displayed rows; single column arrays drive the header and CSV; formula-injection guard | AC-01 Export downloads a file whose columns equal the visible columns on both pages — SC-CSV-01/05 (header row == rendered header row). Filter+sort, machine-readable values, guard, disabled and failure states — SC-CSV-02/03/04/04b/06/07/08. AC-02 Playwright passes in CI — see CI evidence | Pass with notes | `BLG-SPEC-161`, `BLG-FE-185` (notes 5–7) |
| ST-04 | `alerts_endpoints.md` v0.8; `notifications.md` §Reflection Reminder Row; `data_model.md` DS-19; `decision_record.md` (reflection-reminder) | `reflection_reminder` alert type (server, in `POST /alerts/evaluate`), unique-per-trade index, preference default Off, feed row + "Write reflection" link, `/TradeHistory?reflect=` re-entry, auto-read on reflection save | AC-01 A closed trade without a reflection produces exactly one reminder after 48h — `test_reflection_reminder.py` (48h/30d parameters, no-reflection + one-per-trade filters, ON CONFLICT no-op) and SC-RR-01. AC-02 Completing the reflection or dismissing suppresses it — `upsert_trade_reflection` auto-read tests; SC-RR-04; existing-reminder exclusion. AC-03 Playwright passes in CI — see CI evidence | Pass with notes | `BLG-OPS-168` (SQL never executed live; notes 8–10) |
| ST-05 | `design_system.md` v1.21 §Data States; `analytics.md` §21; `decision_record.md` (empty-state) | Shared `EmptyStateAction`; five new next actions; 9 dashboard cards verified; 2 exclusions recorded; heading period fix | AC-01 0 audited empty states without a next-action link — SC-ESN-00 (source scan of all 20 `emptyHeading` sites, exhaustive), SC-ESN-01–06, SC-ESN-11. AC-02 Playwright passes in CI — see CI evidence | Pass with notes | None (notes 11–12) |
| ST-06 | `design_system.md` v1.21 §Number and Currency Formatting; `decision_record.md` (number-format) | `src/lib/format.js`; migration of Positions table/card/modal, Trade History table/stats, Trade Plans R target | AC-01 The three tables use the helper with identical negative/decimal conventions — SC-NFT-01–06, SC-NF-01–07. AC-02 Playwright passes in CI — see CI evidence | Pass with notes | `BLG-FE-184`, `BLG-SPEC-162` (notes 13–16) |

**QA test coverage:**
- Scenarios run (local): all eight files above pass — 40 UI scenarios (6 + 5 + 9 + 6 + 8 + 6) + 7 browser-free helper scenarios = 47 Playwright scenarios; `tests/test_reflection_reminder.py` 27 tests (23 at first review + 4 regression tests added for review finding 1). Each new UI spec was mutation-checked (a deliberately broken implementation made the relevant scenarios fail): SC-TPC-03/04, SC-CSV-06, SC-ESN-02, SC-NFT-01/03/06.
- Regression areas checked: full backend suite in stub mode — 1598 passed, 10 skipped, 0 failed (contract drift scripts: heading lint, local OpenAPI completeness, 3-way sweep, API performance baseline — all pass; `openapi.yaml` parses). Frontend regression per story over every spec touching the affected pages: ST-01 281/281; ST-03 262 passed + 3 pre-existing skips; ST-04 232 passed + 2 skips; ST-05 653 passed + 3 skips; ST-06 480 passed + 3 skips. Every failure seen in those runs was either a wall-clock/parallel-load flake that passes in isolation (`SC-NOTIF-02b`, `SC-AC-03`, `SC-STALE-01/02/05` 15/15 over 3 repeats, `SC-AIC-07`) or an intended old-string assertion updated in the same commit (below).
- Known deviations: None found — all six stories' deviation checks completed with nothing to file (`deviations_filed: true` records the check). Follow-ups are tracked as backlog items, not deviations.

**Existing Playwright assertions updated (design record §2.6 requires this list):**
- `tests/e2e/slippage-tracking.spec.js` SC-SLIP-02b and SC-SLIP-04b — `"-0.25%"` → `"−0.25%"` (ASCII hyphen → U+2212), ST-06.
- `tests/e2e/trade-plan-completion-rate.spec.js` SC-TPCR-04 — heading `"No trade plans created yet."` → `"No trade plans created yet"` (trailing period removed), ST-05.

**Cross-spec selector check (execution_prompt.md §3.1.A step 13):** ST-01–ST-06 add elements or change text only; the only selector/text assertions found stale were the three above. `StandingAlert` gained an opt-in prop (default unchanged); `standing-alert.spec.js` passed.

**Environment-parity sub-clause (§3.2.A):** no AC in this EPIC is a focus-restoration, focus-trap, debounce or animation-completion AC. ST-04's 48 h clock is server-side and is covered by backend tests, not Playwright, per the design record.

## Disclosures for the Director of Quality and Product Owner

**Not verified — read before signing:**
- **A. New SQL not executed against the real database (ST-04).** The engine's own tests assert the SQL structurally with mocked cursors only. Its environment did carry a `DATABASE_URL` for the **staging** database (confirmed by the user after the review; credential believed read-only, not verified), but it was deliberately not used, so no v9.6 statement has been run on it — and staging does not yet carry the v9.6 schema changes, which are applied by `ensure_alerts_tables()` at startup after deploy. Partial independent evidence exists: the reviewing agent ran the real `alerts_service.py` / `database.py` against a **throwaway PostgreSQL 18** (migration from a pre-v9.6 schema + idempotent re-run, the `ON CONFLICT` target against the partial index, eligibility windows, savepoint isolation, preference default), and CI Phase B ran the full suite against a real Postgres service. Neither is the staging Supabase database, its version, timezone or data. Staging confirmation queries are in `data_model.md` DS-19; tracked as `BLG-OPS-168` (P2, target v9.6), and `BLG-QA-189` proposes a permanent real-Postgres integration test.
- **B. CI confirmation.** Every story's final AC is "Playwright passes in CI"; the Playwright CI job is path-filtered on push. See CI evidence below.

**Judgement calls made by the engine where the design record was silent or the code differed:**
1. ST-01 — the app has page-name routes only, so the record's `/trade-plans/new?clone_from=` is implemented as `/TradePlan?clone_from=` (same destination).
2. ST-01 — banner reads "…click Save Plan." (the real button label) rather than the record's "Save Trade Plan".
3. ST-01 — the form has no Cancel button; Back discards, equivalent to "Cancel discards".
4. ST-01 — fields absent from the record's copy list (`setup_type`, `entry_rationale`, `confirmation_criteria`, `early_exit_conditions`, `planned_quantity`) are not copied.
5. ST-03 — the Screener's real desktop table has an Earnings column the record/spec omit; exported per the AC ("columns equal the visible columns"). Spec debt: `BLG-SPEC-161`.
6. ST-03 — column arrays drive the header and CSV, but body-cell JSX was not refactored to read from them (`BLG-FE-185`).
7. ST-03 — Watchlist "Research" and "News" are icon columns with no data value; exported as Yes/No.
8. ST-04 — **30-day look-back** bounds the first evaluation run after deploy so historic trades with no reflection do not flood the feed. The record is silent; Product Owner to confirm or change (`BLG-OPS-168`).
9. ST-04 — the close timestamp is `trade_history.created_at` (when the closure was recorded), falling back to `exit_date`, because `exit_date` can be back-dated.
10. ST-04 — the "email" preference governs Telegram delivery (the deployed channel, `DEV-ST04-01`).
11. ST-05 — four dashboard cards' existing `to` link differs from the record's suggested destination (Portfolio Heat and In Grace → RiskDashboard; Earnings → Positions; Signal Compliance → PerformanceAnalytics). The AC (a link exists) is met; click-through targets were left unchanged — Head of UX & Design may wish to review.
12. ST-05 — "Create a trade plan" targets `/TradePlan` (the new-plan form).
13. ST-06 — Trade History P&L % and the Positions grid card's P&L % moved 2 dp → 1 dp under the "percentage default 1 dp" rule; §2.6 did not enumerate this change (slippage/fee drag stay 2 dp as cost metrics).
14. ST-06 — call-site colour/icon logic is unchanged: zero P&L still takes the ≥ 0 tone (its string is unsigned). Neutral zero tone is a follow-up (`BLG-FE-184`).
15. ST-06 — a current price of exactly 0 now renders `$0.00` rather than an em dash.
16. ST-06 — the advisory pixel-baseline job (`visual-regression-baselines`) has a Positions baseline and was not regenerated; it is not in the blocking suite.

17. ST-04 — **DoQ review finding 1 (P2), fixed in this EPIC (commit `00f98cdf`).** With the preference off, reminder rows were created `delivered = FALSE`, so the generic re-delivery loop would have re-sent every accumulated reminder (including read ones) the first time the operator turned the toggle on. Rows are now created already settled (`delivered = TRUE`, `delivery_error = 'email disabled'`) when the preference is off. 4 regression tests added; the reviewer reproduced the original defect on a scratch PostgreSQL and the fix passed CI (Phase B 1607 passed).
18. Advisory pixel-baseline job: in CI run `35634059096` "Playwright Visual Regression Baselines (advisory)" reported 6 failed / 4 passed — the failing baselines are DashboardHome, TradePlan and PerformanceAnalytics (Settings also diffed in the job log; Positions passed). The workflow marks the job advisory (`continue-on-error`) because its locally generated baselines are expected to diff on the runner. Two of the failing pages (Settings, DashboardHome) are untouched by EPIC-01, which points at environment drift, but earlier-commit logs were unavailable so pre-existing status against `main` is **not confirmed**. Baselines were not regenerated.

**Reviewer P3 notes recorded as backlog scope (not defects against the sealed design):** the CSV formula guard covers the four record-listed characters but not a leading TAB/CR (`BLG-FE-185`); `formatCurrency(true)` returns `£1.00` and an unknown currency silently falls back to `£` (`BLG-FE-184`).

**Opportunistic in-file fixes (disclosed in commit messages):** backfilled the missing v0.7 changelog row in `alerts_endpoints.md`; added the missing `custom_price_alert` value and `context` field to `openapi.yaml`'s `NotificationItem`; trimmed two `**Last Updated:**` headers to the retention limit.

**Backlog items filed from this EPIC's findings:** `BLG-SPEC-161`, `BLG-SPEC-162`, `BLG-FE-184`, `BLG-FE-185`, `BLG-OPS-168`, `BLG-QA-188`, `BLG-QA-189`.

**Environment finding (not a story defect):** the execution environment's `DATABASE_URL` points at the **staging** Supabase database (confirmed by the user after this evidence was first written; the credential is believed to be read-only but that is unverified). It was **not** used. All backend test runs were made with a `stub` URL (which the suite's own Phase-A convention skips real-DB tests on) because `tests/conftest.py` would otherwise let `tests/test_schema.py` connect to it and attempt DDL (which would alter staging if the credential can write, or fail noisily if it is read-only). Filed as `BLG-QA-188`.

## CI evidence

Real CI (GitHub Actions), branch `exec/2026-09-21__release-v9.6/EPIC-01`:

| Head SHA | Run | Result |
|----------|-----|--------|
| `9cfc5463782a4821ac98ab25c6c2c1b386dd7c11` (all six stories' code; last frontend change) | Playwright E2E Acceptance Tests, run `35634059096`, 8 shards | success — 920 tests, 0 failed, 3 skipped; all 47 new scenarios (SC-TPC, SC-TPS, SC-CSV, SC-RR, SC-ESN, SC-NFT, SC-NF) appear as passed |
| `9cfc5463…` | CI Pytest Suite, run `35634059170` | success — Phase B (real Postgres service) 1603 passed, 5 skipped |
| `9cfc5463…` | Critical-Path Smoke Tests, Service Layer Coverage Gate, Golden Output Regression Gate, Portfolio Integration Tests, Endpoint Coverage Report, Governance Sync Loop | success |
| `9cfc5463…` | Playwright Visual Regression Baselines (advisory) | 6 failed / 4 passed, non-blocking — see disclosure 18 |
| `00f98cdf760a70f2c0e12d13c7f64f283ebf16d6` (review finding 1 fix; backend + docs only) | CI Pytest Suite, run `35635707322`, plus Smoke, Coverage, Golden, Integration, Endpoint Coverage, Governance Sync | success — Phase B 1607 passed, 5 skipped (1603 + 4 new regression tests) |

The Playwright job is path-filtered on push, so it did not re-run for `00f98cdf` (no `src/` change since `9cfc5463`). The Playwright and pytest results for the **PR head** must be re-confirmed green at the merge gate; this file cannot state a result for a commit that does not exist yet.

---

## Standard Sign-Off Block

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — new fetches (`TradePlan.js` clone read) use the existing `apiFetch(`${API_BASE}/…`)` pattern with `API_BASE` defined in the file; no new direct URL construction
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-21
- Comments: Independent agent-mediated Director of Quality review (execution_prompt.md §5.3), not a human sign-off. Decision was "Approved with conditions"; all four conditions are met in this commit: (1) review finding 1 (P2, stale reminders re-sent when the email preference is turned on) fixed in `00f98cdf` with 4 regression tests; (2) scenario count corrected to 40 UI + 7 helper; (3) CI evidence recorded above with the tested head SHAs; (4) `backlog.md`, this file and `execution_state.json` (`qa_signed_off: true`) committed together. The reviewer verified each AC against existing scenarios, the server-side 48h / one-reminder-per-trade rules against a throwaway PostgreSQL 18, and CI run `35634059096` on head `9cfc5463` (920 Playwright tests, 0 failed, all 47 new scenarios green; Phase B pytest 1603 passed). The reviewer did NOT verify behaviour on the real Supabase database (`BLG-OPS-168` remains open) and did not run Playwright locally. The advisory pixel-baseline job was red (disclosure 18). Playwright/pytest on the PR head are to be re-confirmed at the merge gate. Merge remains subject to the always-human QA sign-off and Product Owner acceptance.
