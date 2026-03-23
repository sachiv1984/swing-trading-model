Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-22

---

# QA Evidence — EPIC-03: Bug Fixes & Operational Quick Wins

**Cycle:** 2026-03-21__release-v2.2

---

## EPIC-Level Consolidation

**EPIC:** EPIC-03 — Bug Fixes & Operational Quick Wins
**Cycle:** 2026-03-21__release-v2.2
**Sprint goal:** Ship a secured, observable alert system: authenticate the Render API against public access, complete the alert engine with configurable thresholds and evaluation history, close QA scenario gaps from v2.1, and deliver three governance process improvements that streamline all future cycles.
**Test scenarios used:** Derived from spec + AC (no pre-existing EPIC-03 scenario file)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-06 | docs/specs/api_contracts/trade_endpoints.md#GET /trades/export/csv | Fixed incorrect import `get_all_trade_history` → `get_all_closed_trades_for_csv_export` in backend/services/trade_service.py (import + call site) | AC-1: incorrect import confirmed present; AC-2: import corrected; AC-3–4: GET /trades/export/csv returns valid CSV without ImportError (AC-3–4 staging verification pending) | Pass (code review) | None |
| ST-07 | docs/specs/frontend/pages/trade_history.md#Avg Slippage StatsCard | Replaced unsupported `color="cyan"` with supported `gradient="violet"` in TradeHistory.js null/zero branch | AC-1: StatsCard renders with supported key (violet); AC-2: no regression to cell-level emerald/rose colouring; AC-3: code review sufficient | Pass | None |
| ST-08 | docs/specs/api_contracts/health_endpoints.md#GET /health | New `get_operational_health()` in health_service.py; GET /health updated to return `{status, db, last_market_status_check, last_alert_evaluation}`; `record_alert_evaluation()` wired in alerts router; `record_market_status_check()` wired in market status endpoint; openapi.yaml updated with OperationalHealthResponse schema; DEV-HEALTH-001 deviation filed | AC-1: schema correct; AC-2: DB check via get_portfolio() lightweight query; AC-3: last_alert_evaluation null on fresh process; AC-4: openapi.yaml updated; AC-5: staging run pending | Pass (code review) | DEV-HEALTH-001 (P2) — implementation differs from prior health_endpoints.md v1.0 schema |

**QA test coverage:**
- Scenarios run: Agent-mediated code review (Director of Quality, 2026-03-22)
- Regression areas checked: CSV export path, StatsCard gradient rendering, health endpoint schema, openapi.yaml drift
- Known deviations filed: DEV-HEALTH-001 (P2 — health_endpoints.md spec update deferred to API Contracts & Documentation Owner)

**Outstanding staging verification actions (non-blocking for code review approval):**
- ST-06 AC-4: Confirm GET /trades/export/csv returns valid CSV without ImportError on staging
- ST-08 AC-5: Confirm GET /health returns HTTP 200 with new schema on staging or local run
- ST-07: Visual check of Avg Slippage StatsCard with null slippage (preferred; not blocking)

**QA sign-off block:**
> **Authoring note (LL-v1.10-P4-1):** All AC table rows have been set to "Pass" or "Pass (code review)" consistent with the sign-off below. Rows marked "staging verification pending" are noted as outstanding actions above, not as failures.

- [x] All acceptance criteria verified against canonical spec (code review; runtime deferral noted above)
- [x] No unresolved P0 or P1 deviations (DEV-HEALTH-001 is P2)
- [x] Regression areas checked: CSV, StatsCard, health endpoint, openapi.yaml
- [x] For any frontend component making direct URL construction: not applicable to EPIC-03 items **(LL-v2.0-P3-4)**
- Signed off by: Director of Quality (agent-mediated, 2026-03-22)
- Date: 2026-03-22
- Comments: All three autonomous items cleared by code review. ST-06 and ST-08 require staging verification of runtime paths (AC-4 and AC-5 respectively) as outstanding actions before final sprint close. DEV-HEALTH-001 (P2) filed — spec update to health_endpoints.md v1.1 to be completed by API Contracts & Documentation Owner in a follow-up cycle.
