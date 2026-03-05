Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-05

# QA Evidence Log — EPIC-03: API & Spec Debt

**EPIC:** EPIC-03 — API & Spec Debt (Critical)
**Cycle:** 2026-03-04__release-v1.8
**Sprint goal:** Ship a fully functional Risk Dashboard page... and closing the highest-priority spec and governance debt carried from v1.7.
**Test scenarios used:** Derived from spec + acceptance criteria (no pre-existing test scenario files for EPIC-03)

---

## Per-Story Evidence

---

### ST-09 — Settings Endpoint Method Drift Resolution

**Spec references:** `docs/specs/api_contracts/settings_endpoints.md` v1.1.0

**Acceptance criteria:**
- `settings_endpoints.md` documents `PATCH /settings/{settings_id}` and `POST /settings` (live methods)
- `PUT /settings` entry removed or marked superseded
- No divergence between spec and implementation
- Version incremented per document_lifecycle_guide.md

**Commit SHA:** cf34273

**What was built:** `settings_endpoints.md` rewritten as a lifecycle-compliant Class 1 Canonical document at v1.1.0. `PUT /settings` section removed. `POST /settings` section added documenting the create endpoint. `PATCH /settings/{settings_id}` section added documenting update by ID with path parameter. Cross-checked against `backend/main.py` which confirms routes at lines 122, 143, 157: `GET /settings`, `POST /settings` (create_settings_endpoint), `PATCH /settings/{settings_id}` (update_settings_endpoint). No field, path, or method discrepancy.

**Deviation check:** No deviations. Implementation matches the spec change.

---

### ST-10 — Update openapi.yaml to v1.9.0

**Spec references:** `docs/reference/openapi.yaml`, `docs/specs/api_contracts/analytics_endpoints.md#POST /validate/calculations`, `docs/specs/api_contracts/trade_endpoints.md#GET /trades`, `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio`

**Acceptance criteria:**
- `docs/reference/openapi.yaml` version field updated to 1.9.0
- `/validate/calculations` response includes `sharpe_ratio_trade_method` (14 validated metrics total)
- `GET /trades` trade object includes `holding_days` (integer)
- `GET /portfolio` positions objects reflect v1.9.0 field list
- No conflicts between openapi.yaml and markdown contracts

**Commit SHA:** 9924f94

**What was built:** `openapi.yaml` updated from v1.8.1 to v1.9.0. Four changes made:
1. Version field: `1.8.1` → `1.9.0`
2. `ValidationResponse` schema description updated to cite `sharpe_ratio_trade_method` as the 4th critical metric and total 14 validated metrics
3. `TradeHistoryResponse` description updated to note `holding_days` field at v1.9.0
4. `PositionSummary` schema replaced with v1.9.0 field list matching `portfolio_endpoints.md`: removed `current_price_native`, `stop_price`, `stop_price_native`, `pnl_percent`; added `current_value`, `current_stop`, `pnl_pct`, `fx_rate`, `live_fx_rate`
5. Settings paths: `PUT /settings` removed; `POST /settings` and `PATCH /settings/{settings_id}` added (coordinated with ST-09)

**Deviation check:** No deviations. All changes align with canonical markdown contracts.

---

## EPIC-Level Consolidation

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-09 | `settings_endpoints.md` | settings_endpoints.md v1.1.0: PATCH/POST replacing PUT | Spec matches live implementation; version incremented | Pass | None |
| ST-10 | `openapi.yaml`, `analytics_endpoints.md`, `trade_endpoints.md`, `portfolio_endpoints.md` | openapi.yaml v1.9.0: PositionSummary updated, sharpe_ratio_trade_method cited, holding_days noted, settings paths corrected | Version 1.9.0; 14 metrics; holding_days; v1.9.0 positions; no conflicts | Pass | None |

**QA test coverage:**
- Scenarios run: manual acceptance review (spec comparison, route verification)
- Regression areas checked: API contracts spec domain, openapi.yaml reference consistency
- Known deviations filed: None

**QA sign-off block:** (Director of Quality completes this)
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- Signed off by: Director of Quality
- Date:
- Comments:
