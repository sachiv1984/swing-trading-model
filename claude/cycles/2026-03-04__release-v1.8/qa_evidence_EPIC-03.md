Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-05

# QA Evidence Log — EPIC-03: API and Spec Debt (Critical)

**EPIC:** EPIC-03 — API and Spec Debt
**Cycle:** 2026-03-04__release-v1.8
**Sprint goal:** Close the highest-priority spec and governance debt carried from v1.7: settings endpoint method drift and openapi.yaml v1.9.0 update.
**Test scenarios used:** Derived from spec + AC (no dedicated scenario file — autonomous spec corrections)

---

## Per-Story Evidence

---

### ST-09 — Settings Endpoint Method Drift Resolution

**Spec references:** `docs/specs/api_contracts/settings_endpoints.md` v1.1.0

**Status:** Complete — committed to exec/2026-03-04__release-v1.8/EPIC-03

**Commit SHA:** cf34273

**What was built:** `settings_endpoints.md` updated from v1.0.x to v1.1.0. `PUT /settings` entry removed. `PATCH /settings/{settings_id}` and `POST /settings` documented as canonical endpoints, each with HTTP method, path, request body schema (field name, type, value), and response schema. Lifecycle header added. Cross-checked against `backend/main.py` router — no divergence between spec and implementation. ESC-20260304-01 resolution (option a: spec follows implementation) applied.

**Deviation check:** No deviations. Spec now matches live implementation exactly.

---

### ST-10 — Update openapi.yaml to v1.9.0

**Spec references:** `docs/reference/openapi.yaml` v1.9.0, `docs/specs/api_contracts/analytics_endpoints.md`, `docs/specs/api_contracts/trade_endpoints.md`, `docs/specs/api_contracts/portfolio_endpoints.md`

**Status:** Complete — committed to exec/2026-03-04__release-v1.8/EPIC-03

**Commit SHA:** 9924f94

**What was built:** `docs/reference/openapi.yaml` updated to version 1.9.0. Changes:
- `PositionSummary` schema updated to v1.9.0 field list per `portfolio_endpoints.md` v1.9.0 (includes `portfolio_heat_percent`, `position_risks[]`, all position fields)
- `ValidationResponse` schema updated to cite `sharpe_ratio_trade_method` and 14 total validated metrics
- `TradeHistoryResponse` updated to include `holding_days` (integer) field
- Settings paths corrected: `PUT /settings` removed; `POST /settings` and `PATCH /settings/{settings_id}` added (coordinates with ST-09)
- No conflicts between openapi.yaml and any markdown contract after update

**Deviation check:** No deviations from AC. ST-08 CI drift check pending (ST-08 is blocked_backend — will verify on completion).

---

## EPIC-Level Consolidation

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-09 | `settings_endpoints.md` v1.1.0 | Spec corrected: PATCH /settings/{id} + POST /settings; PUT removed | Spec matches live implementation; API Contracts owner confirms; version incremented | Pass | None |
| ST-10 | `openapi.yaml` v1.9.0 | openapi.yaml updated: 14 metrics, holding_days, portfolio v1.9.0 fields, settings paths corrected | No conflicts with markdown contracts; all 4 AC dimensions met | Pass | None (ST-08 drift check pending) |

**QA test coverage:**
- Scenarios run: manual acceptance review against AC (autonomous spec corrections)
- Regression areas checked: settings endpoint spec, openapi.yaml contract alignment, analytics/portfolio/trade schema accuracy
- Known deviations filed: None

**QA sign-off block:**
- [x] All acceptance criteria verified against canonical spec — ST-09: `settings_endpoints.md` v1.1.0 spot-checked: GET, POST, PATCH present; PUT absent; schemas present. ST-10: `openapi.yaml` v1.9.0 spot-checked: version field confirmed 1.9.0, `sharpe_ratio_trade_method` present, `holding_days` present, portfolio v1.9.0 fields present, `/settings` and `/settings/{settings_id}` paths present (PUT removed). All four AC dimensions met for both stories.
- [x] No unresolved P0 or P1 deviations — no deviations filed for either story. ST-10 ST-08 drift check is pending (ST-08 is blocked_backend); this is a future verification dependency, not a current defect.
- [x] Regression areas checked — settings endpoint spec cross-checked against implementation; openapi.yaml checked against markdown contracts for analytics, portfolio, trade, and settings; no conflicts found.
- Signed off by: Director of Quality
- Date: 2026-03-05
- Comments: Clean delivery. Both items are autonomous spec corrections with clear, verifiable acceptance criteria. No deviations. ST-10 note: the ST-08 CI drift check will provide additional automated assurance once ST-08 is implemented; the openapi.yaml content is correct as of this sign-off. EPIC-03 QA gate: APPROVED. Recommend merge once Product Owner acceptance is confirmed on PR #29.
