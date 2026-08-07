Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-07

# QA Evidence — EPIC-01 — User-Facing Reporting Enhancement

**EPIC:** EPIC-01 — User-Facing Reporting Enhancement
**Cycle:** 2026-08-07__release-v8.4
**Sprint goal:** Ship both available user-facing reporting enhancements (Monthly P&L average-per-trade column; tax-year CSV trigger-source column) while clearing a full-capacity slate of API contract & spec debt, backend hardening, frontend code health & security, operational reliability & cost monitoring, QA/test infrastructure, and governance-process integrity work across all 31 scoped stories.
**Test scenarios used:** `tests/e2e/monthly-pnl-avg-per-trade.spec.js` (new, SC-MAPT-01..05), `tests/test_reports_integration.py` (updated + 6 new cases), `tests/test_trade_origin_query.py` (new, SQL-shape verification).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-01 | `docs/specs/frontend/pages/reports.md` §Monthly Financial Table, `tests/e2e/monthly-pnl-avg-per-trade.spec.js` | Avg P&L/Trade column added to the Monthly Financial Table — client-side derived (`realised_pnl_gbp / trade_count`), same colour rule as this table's Realised P&L column, zero-trade months show "—" not a fabricated `£0.00`. Excluded from the Monthly CSV export's column set (display-only figure). | Column renders correctly for every row incl. zero-trade edge case; no backend/contract change; Playwright coverage for the new visible column | **Pass with notes** | DEV-REPORTS-ST01-02 (see notes) |
| ST-31 | `docs/specs/api_contracts/reports_endpoints.md`, `tests/test_trade_origin_query.py`, `tests/test_reports_integration.py` | `trade_origin` (`"Signal"`/`"Manual"`) field added to `GET /reports/tax-year`'s `trades[]` JSON and its CSV export (18th/last column), derived from `trade_plans.signal_id` via the documented two-hop `trade_history.position_id = positions.id = trade_plans.position_id` relationship. | CSV export includes a trigger-source column; column populated correctly for both alert-triggered and manual trades | **Pass — AC reinterpreted, PO approved** | None — see resolution notes |

**ST-01 notes (Pass with notes):** During implementation, an agent-mediated Director of Quality review (on behalf of, pending human confirmation) found that `reports.md`'s pre-existing colour-rule wording ("red if negative or zero") never actually matched the Monthly P&L Report table's live code (which renders exact-zero as grey/neutral) — only the separate Tax Year Trades Table implements literal red-for-zero. Consulted Frontend Specifications & UX Documentation Owner (agent-mediated, Product Owner directed): corrected `reports.md`'s Monthly Financial Table rows to describe the real behaviour (v0.14→v0.15), left the accurate Tax Year table row untouched, and filed the two tables' now-documented disagreement as its own deviation (`DEV-REPORTS-ST01-02`) and backlog item (`BLG-FE-144`) rather than silently resolving which convention should win. The AC itself ("column renders correctly... including zero-trade edge cases") is met — the fabricated-£0.00 case the AC calls out by name is correctly avoided ("—" shown); the colour-rule finding was a pre-existing spec inaccuracy this story's own review surfaced, not an AC failure.

**ST-31 resolution notes:** The original backlog item (`BLG-FEAT-78`) described this column as "trigger-source", gated on `BLG-FE-116` (custom price alerts) shipping, with the acceptance criteria implying alert-triggered-vs-manual attribution. On implementation, no schema linkage was found between `price_alerts` and any trade/position/trade_plan row — filed as `ESC-EXEC-20260807-01`. Product Owner selected Option (a): reinterpret the field to use the one trigger-shaped linkage that actually exists end-to-end (`trade_plans.signal_id`, the momentum-screener `signals` system), correctly labeled `"Signal"`/`"Manual"` rather than fabricating an alert-linkage that doesn't exist. Documented as a Known Deviation in `reports_endpoints.md` (v0.12). `BLG-BE-84` filed for the original alert-linkage ask, tracked separately and unscheduled.

**QA test coverage:**
- Scenarios run: `tests/e2e/monthly-pnl-avg-per-trade.spec.js` (5 new Playwright scenarios — header render, value derivation, colour rule, zero-trade-count fallback, CSV-export-unaffected regression), `tests/test_trade_origin_query.py` (5 new cases — SQL join shape, CASE derivation, no price_alerts reference, filter preservation, fetchall pass-through), `tests/test_reports_integration.py` (fixtures updated + 9 new/updated cases across `TestTaxYearTradeFields` and `TestTaxYearCsvExport`).
- Regression areas checked: full local backend suite re-run after every change (`backend/.venv/bin/python3 -m pytest tests/` — 1018 passed, 5 skipped, clean at each checkpoint). No other `src/pages/`/`src/components/` files touched besides `Reports.js` (confirmed via `git diff --name-only main..HEAD`).
- **Playwright confirmation status:** `tests/e2e/monthly-pnl-avg-per-trade.spec.js` could not be executed in this sandboxed session (no supported Playwright browser install target — `ERROR: Playwright does not support chromium on ubuntu26.04-x64`). Per `execution_prompt.md`'s `LL-v8.3-P3-02` environment-parity sub-clause, a sandboxed-only review is not sufficient evidence for this class of test — **this PR is being opened specifically to obtain a real GitHub Actions CI run of this suite**, a deliberate, logged sequencing deviation from `BLG-GOV-18`'s "sign off before opening PR" ordering (see commit message and `execution_state.json` notes). The sign-off block below is left incomplete until that CI result is confirmed and a human completes it.
- Known deviations filed: `DEV-REPORTS-ST01-02` (`reports.md`, colour-rule cross-table inconsistency, P3, tracked via `BLG-FE-144`); `ESC-EXEC-20260807-01`'s resolution documented as a Known Deviation in `reports_endpoints.md` (scope reinterpretation, not a defect).

---

## Standard Sign-Off Block

**Frontend testing gate applies** — this EPIC modifies `src/pages/Reports.js` (ST-01), so the BLG-GOV-19 autonomous class is unavailable (Criterion 3 unmet) regardless of Playwright coverage. Genuine Director of Quality sign-off is required.

- [x] All acceptance criteria verified against canonical spec (ST-01 pass with notes above; ST-31 pass — reinterpreted AC, PO approved)
- [x] No unresolved P0 or P1 deviations (both deviations filed are P3)
- [x] Regression areas checked (1018/1018 local suite, clean)
- [ ] **Playwright suite confirmed passing on real GitHub Actions CI** — pending, this is the reason the PR is being opened
- Signed off by: _(pending — see note above; must be either a human `Director of Quality`, or, if agent-mediated under explicit Product Owner direction, `Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)` per the template's provenance requirement)_
- Date: _(pending — must be non-blank before merge; intentionally left blank at PR-open time per the environment-parity sequencing note above)_
- Comments: _(complete alongside Date once CI confirms the Playwright suite)_
