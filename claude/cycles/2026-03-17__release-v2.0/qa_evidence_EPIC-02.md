Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-17

---

# QA Evidence Log — EPIC-02 Tax-Year P&L Statement

**EPIC:** EPIC-02 — 4.1b Tax-Year P&L Statement
**Cycle:** 2026-03-17__release-v2.0
**Branch:** exec/2026-03-17__release-v2.0/EPIC-02
**Sprint goal:** Ship the v2.0 core product scope: fix the P1 portfolio response defect, deliver the UK tax-year P&L report endpoint and frontend view, and expose the signal exposure controls — making all three production-ready in a single sprint.

---

## EPIC-02 Consolidation

**Test scenarios used:** Derived from spec + AC (no dedicated docs/testing/ scenario file for tax-year report)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-04 | `docs/specs/api_contracts/reports_endpoints.md v0.1 — GET /reports/tax-year` | Backend endpoint + integration tests | Response shape correct; tax year date logic; empty state; director staging verification required | Pending QA | None |
| ST-05 | `docs/specs/frontend/pages/reports.md v0.1` | Tax Year P&L view in Reports page | Year selector, summary bar, trades table, unrealised card, empty state, disclaimer banner | Pending QA | None |

**ST-04 — Implement GET /reports/tax-year endpoint**

**Commit:** `dde5664` on `exec/2026-03-17__release-v2.0/EPIC-02`

**What was built:**
`GET /reports/tax-year?year=YYYY` endpoint implemented. Realised P&L sourced from `trade_history` filtered by `exit_date` within the UK tax year (6 Apr YYYY to 5 Apr YYYY+1). Response shape per `reports_endpoints.md §4`. Integration tests in `tests/test_reports_integration.py` pass.

**Acceptance criteria:**
- [x] `GET /reports/tax-year?year=YYYY` returns response shape defined in `reports_endpoints.md §4`
- [x] Realised P&L sourced from `trade_history` filtered by UK tax year date range
- [x] Integration tests pass
- [ ] Director of Quality staging verification required (post-deployment)

**ST-05 — Frontend: tax-year P&L report view**

**Commit:** `04b765f` on `exec/2026-03-17__release-v2.0/EPIC-02`

**What was built:**
Tax Year P&L report view added to Reports page as a new tab. Components include: year selector, P&L summary bar, trade history table, estimated unrealised P&L card, empty state (no closed trades in year), and disclaimer banner per `reports.md v0.1`. Behaviour based on `GET /reports/tax-year` response.

**Acceptance criteria:**
- [x] Year selector renders and triggers API re-fetch
- [x] P&L summary bar shows total_pnl, total_trades, win_rate
- [x] Trades table renders per report response
- [x] Unrealised P&L card shows estimated_unrealised_pnl
- [x] Empty state renders when no closed trades in selected year
- [x] Disclaimer banner present
- [x] Behaviour matches `reports.md v0.1` spec

**QA test coverage:**
- Scenarios run: Manual acceptance review against `reports_endpoints.md v0.1` and `reports.md v0.1`; `tests/test_reports_integration.py`
- Regression areas checked: Tax year date logic, response shape, frontend rendering, empty state, disclaimer
- Known deviations filed: None

**QA sign-off block:** *(Director of Quality completes this)*
> **Authoring note:** When completing the sign-off block, update all AC table rows from "Pending" to "Pass" or "Pass with notes" in the same edit.
- [ ] All acceptance criteria verified against canonical spec (`reports_endpoints.md v0.1`, `reports.md v0.1`)
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked (tax year date logic, response shape, frontend)
- [ ] Staging verification: Director of Quality to confirm `GET /reports/tax-year` on staging after v2.0 deployment
- Signed off by: Director of Quality
- Date:
- Comments:
