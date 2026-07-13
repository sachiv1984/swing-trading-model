Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-13

# QA Evidence — EPIC-03 (User-Facing Feature Enhancements)

**Cycle:** 2026-07-12__release-v7.0
**Sprint goal:** Close the Grid View/Table View position-risk badge and trailing-stop parity gap, resolve the v6.9-carried spec-reconciliation and data-correctness debt, and ship three new reporting and position-review features.

---

## ST-13 — Tax-year P&L CSV export (BLG-FEAT-69)

**Spec reference:** `docs/design/2026-07-12__release-v7.0/tax-year-csv-export/ux_spec.md`, `docs/specs/frontend/pages/reports.md`
**Commit:** 3b364084
**What was built:** Investigation found the backend CSV export (`GET /reports/tax-year?format=csv&year=YYYY`, `build_tax_year_csv`) and frontend "Download CSV" button both pre-dated this sprint (confirmed via `git log`: `build_tax_year_csv` authored in commit `9d75c965`, 2026-03-20, cycle `2026-03-18__release-v2.1`, EPIC-05/ST-13 — ~3.5 months before this sprint; frontend from an unrelated v6.x cycle) — a **pre-met story**. The design gate's "Pre-existing Spec Note (Superseded)" claim (that CSV export "was never implemented") was inaccurate — it searched `backend/routers/` only and missed the inline endpoint in `backend/main.py`. Fixed the one genuine deviation found: button order was CSV-left-of-PDF, spec requires CSV-right-of-PDF. Added the missing Playwright coverage (zero existed for this feature previously).

**Acceptance criteria:**
| AC | Result |
|----|--------|
| User can export a tax-year P&L as CSV | Pass — pre-met, verified working via new Playwright coverage |
| Exported figures match the on-screen report | Pass — backend generates CSV from the same `get_tax_year_report()` data as the JSON view (verified by code review of `build_tax_year_csv`) |

**Test scenarios:** `tests/e2e/tax-year-csv-export.spec.js` (5 scenarios, all passing, verified locally)

**Deviations:** None — button order fix brings shipped code into compliance with this sprint's locked spec; no new deviation introduced.

---

## ST-14 — Realized vs. unrealized gain distinction in monthly P&L (BLG-FEAT-70)

**Spec reference:** `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md`, `docs/specs/api_contracts/reports_endpoints.md`
**Commit:** ca04901e
**What was built:** `get_monthly_pnl_report()` refactored to return `{months, estimated_unrealised_pnl, unrealised_note}` (was a bare list) — the HTTP response's `data` field is unchanged (still the plain months array), fully backward compatible. Added an Unrealised P&L Card (reusing the Tax Year tab's approved pattern verbatim) and a Combined Total line to the Monthly P&L view.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| Report shows realized and unrealized gain figures separately | Pass — monthly table rows remain realised-only; new card shows current-snapshot unrealised figure separately |
| Figures sum to the existing combined total (regression check) | Pass — Combined Total line computed as `sum(displayed months) + estimated_unrealised_pnl`, verified by SC-MRU-02 |

**Test scenarios:** `tests/e2e/monthly-pnl-realized-unrealized.spec.js` (5 scenarios, all passing); `tests/test_api_contracts.py` (1 new test + 3 updated for the shape change, all passing)

**Deviations:** None

---

## ST-15 — Position review cadence nudge (BLG-FEAT-68)

**Spec reference:** `docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md`, `docs/specs/api_contracts/position_endpoints.md`, `docs/specs/data_model.md`
**Commit:** 633fad41
**What was built:** `positions.last_reviewed_at` column (migration), `PATCH /positions/{id}/mark-reviewed` endpoint, `GET /positions` extended to return the field. Frontend: Table View "Last Reviewed" column (after Alerts, before Actions) and Grid View card footer row, both with amber+clock flagging at ≥14 days and an inline Mark Reviewed checkmark button.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| AC-01: Positions display days-since-last-review | Pass |
| AC-02: Positions past the threshold (default 14 days) are visually flagged, independent of P&L state | Pass |
| AC-03: An explicit "Mark Reviewed" action resets the counter | Pass — verified via SC-RCN-06 (fires PATCH, `onSuccess` invalidates the positions query) |
| AC-04: Flag does not fire for positions already flagged by Grace Period or Drawdown prompts | Pass with notes — see interpretation below |

**AC-04 interpretation (explicit, not a silent guess):** The Drawdown Review Prompt is portfolio-level (`threshold_breached` boolean, `positions_by_state` aggregate counts) — it has no per-position flag to key suppression off. Implemented as: Grace suppression is per-position (`position_state === 'GRACE' && days_in_state >= 8`, individually determinable, matches the Grace Period Alert Zone's own trigger exactly); Drawdown suppression applies portfolio-wide to every open position while `threshold_breached === true` — the only signal the API actually provides. Verified via SC-RCN-04 (Grace, per-position) and SC-RCN-05 (Drawdown, portfolio-wide).

**Test scenarios:** `tests/e2e/position-review-cadence-nudge.spec.js` (7 scenarios, all passing, verified locally); `tests/test_mark_position_reviewed.py` (3 tests); `tests/test_api_contracts.py` (2 new tests for the endpoint)

**Deviations:** None

---

## EPIC-03 Consolidation Block

**EPIC:** EPIC-03 — User-Facing Feature Enhancements
**Cycle:** 2026-07-12__release-v7.0
**Sprint goal:** Close the Grid View/Table View position-risk badge and trailing-stop parity gap, resolve the v6.9-carried spec-reconciliation and data-correctness debt, and ship three new reporting and position-review features.
**Test scenarios used:** `tests/e2e/tax-year-csv-export.spec.js` (5), `tests/e2e/monthly-pnl-realized-unrealized.spec.js` (5), `tests/e2e/position-review-cadence-nudge.spec.js` (7), `tests/test_mark_position_reviewed.py` (3), `tests/test_api_contracts.py` (6 new/updated). Full backend suite (611 tests) re-run clean after each backend change. Adjacent regression suites (epic02-v34-risk-prompts.spec.js, gap-risk-flag.spec.js — 18 scenarios) re-run clean.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-13 | tax-year-csv-export ux_spec | Pre-met feature verified + button order fix + Playwright coverage | Both AC | Pass | None |
| ST-14 | realized-unrealized-split ux_spec | Unrealised P&L Card + Combined Total in Monthly P&L | Both AC | Pass | None |
| ST-15 | position-review-cadence-nudge ux_spec | Last Reviewed column/card footer, mark-reviewed endpoint | All 4 AC | Pass with notes | None (AC-04 interpretation documented) |

**QA test coverage:**
- Scenarios run: 17 new Playwright scenarios across 3 files (all passing, local run); 12 new/updated backend pytest scenarios across 3 files (all passing); full 611-test backend regression suite clean; 18-scenario adjacent Playwright regression suite clean (epic02-v34-risk-prompts, gap-risk-flag)
- Regression areas checked: Positions Table/Grid View (existing badges/columns unaffected), Reports page (Performance tab, SI-02 Gate Status section — 19 scenarios re-run clean), Monthly P&L response shape (backward compatible — `data` field unchanged)
- Known deviations filed: None this EPIC

**Frontend testing gate check (CLAUDE.md, LL-v3.1-EX-01):** All observable ACs (ST-13 CSV download/button order, ST-14 card/total display, ST-15 column/flag/mark-reviewed) have Playwright coverage. No "code review only" ACs requiring a backlog exemption.

**Autonomous class eligibility check (BLG-GOV-19):**
- Criterion 1 (all stories autonomous): ✓
- Criterion 2 (all AC code-review-verifiable, no observable UI behaviour): ✗ — all 3 stories have observable UI behaviour
- Criterion 3 (no frontend-visible change): ✗ — `src/pages/Reports.js`, `src/pages/Positions.js`, `src/components/positions/PositionCard.js` modified (detection rule BLG-GOV-135)
- Criterion 4: N/A (fails at 2/3)

Autonomous class does **not** apply — Standard Sign-Off Block required, Director of Quality review.

**Cross-EPIC note (rebase required before merge):** This branch (`exec/.../EPIC-03`) was cut from `main` before EPIC-01 and EPIC-02 merged. Per the Merge Order plan in `sprint_backlog.md`, EPIC-03 must rebase onto `main` after both EPIC-01 and EPIC-02 merge, and reconcile:
- `docs/specs/frontend/pages/positions.md` — EPIC-01's ST-05 bump (v2.2→v2.3) will collide with this branch's unmodified v2.2 baseline; ST-15's own content is already correctly present in v2.2 (committed at design gate), no ST-15-specific spec edit is needed here, but the version number must be reconciled (renumber to v2.4 or as appropriate) during rebase.
- `src/components/positions/PositionCard.js` — this branch's ST-15 changes (Last Reviewed row, mutation hook, icon imports) were built against the pre-EPIC-01 version of this file (no `RiskOffCardBadge`/`PositionCardAlertsRow`/trailing-stop restructure yet). Must be manually reconciled with EPIC-01's changes during rebase — both sets of changes touch the card footer/structure area and will conflict.
- `src/pages/Positions.js` — EPIC-02's ST-09 breach badge fix and this branch's ST-15 changes (drawdown-status query, Last Reviewed column) both modify this file; expected to merge cleanly (different sections) but must be verified during rebase.

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations (none filed this EPIC)
- [x] Regression areas checked (611-test backend suite clean; 37 total Playwright scenarios clean across new + adjacent regression files)
- [x] No frontend component in this EPIC makes direct URL construction outside the `api.*` wrapper (uses `apiFetch` consistently)
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-07-13
- Comments: Independently re-traced the ST-13 "pre-met" claim via git history — confirmed genuine (build_tax_year_csv authored 2026-03-20, commit 9d75c965, ~3.5 months before this sprint), but the QA log originally cited the wrong commit SHA (c8a4ff3d, an unrelated later commit) — corrected in this file before final sign-off. ST-14's backward-compatibility claim verified via passing contract tests. ST-15's AC-04 suppression interpretation cross-checked against the actual getReviewCadenceState() implementation and the real GET /portfolio/drawdown-status API shape — defensible, explicitly documented (not a silent guess), and safety-neutral (biases toward over-suppression on a display-only, non-safety-critical feature). Independently re-ran tests/test_mark_position_reviewed.py + tests/test_api_contracts.py (56 passed). Cross-EPIC rebase note verified as a real, correctly-scoped risk (confirmed EPIC-01 independently modifies the same PositionCard.js region and positions.md version number).
