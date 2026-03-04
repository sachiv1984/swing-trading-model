**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Stage 3 — Execution Plan

## Release: v1.8 — Risk Dashboard

---

## Epic Structure

### EPIC-01 — Risk Dashboard Page
**Maps to:** S2-01
**Theme:** Primary user-facing feature — Risk Dashboard page
**Effort:** 3–4 days
**Priority:** P0 (primary release goal)
**Dependencies:** Design Gate must pass before Sprint Planning opens (Phase 1.5)

#### EPIC-01 Tasks

**ST-01 — Frontend Spec: Risk Dashboard Page**
Owner: Frontend Specs & UX Documentation Owner (post Design Gate)
Maps to: S2-01
Effort: ~0.5 day
Description: Author `docs/specs/frontend/pages/risk_dashboard.md` (Class 1 Canonical) based on Design Gate artefacts. Must cover: Portfolio Heat Gauge, Drawdown Summary, Grace Period panel, Position Risk Table, Prospective Heat Indicator. Version: v0.1.0 (new document).
Acceptance Criteria:
- `docs/specs/frontend/pages/risk_dashboard.md` exists and is lifecycle-compliant (Owner, Class, Status, Version, Last Updated)
- All five page sections specified: layout, component states, data sources, edge cases
- Cross-referenced to `metrics_definitions.md` v1.6.0 for heat formula and thresholds
- Head of Specs Team confirms lifecycle compliance
Prerequisite: Design Gate artefact approved by Product Owner

**ST-02 — Backend: Confirm Heat Calculation Availability**
Owner: Head of Engineering
Maps to: S2-01
Effort: ~0.25 day
Description: Confirm whether `GET /portfolio` response already includes `portfolio_heat_percent` or whether a dedicated calculation call is needed. If absent, implement as a new field on the portfolio response or as a new endpoint. Align with `metrics_definitions.md` v1.6.0 formula.
Acceptance Criteria:
- `portfolio_heat_percent` (and optional `portfolio_heat_threshold`) available in API response
- Implementation aligns exactly with `metrics_definitions.md §Portfolio Heat` formula
- No new external dependencies introduced
- Confirmed by API Contracts & Documentation Owner

**ST-03 — Frontend: Risk Dashboard Page Implementation**
Owner: Head of Engineering (Base44 Frontend Prompt Owner for code generation)
Maps to: S2-01
Effort: ~2–3 days
Description: Implement Risk Dashboard page using canonical frontend spec (ST-01 output) and Base44 prompt. Components: Portfolio Heat Gauge (colour-coded per thresholds), Drawdown Summary, Grace Period Status Panel, Position Risk Table, Prospective Heat Indicator.
Acceptance Criteria:
- Risk Dashboard page renders at designated route
- Portfolio Heat Gauge colour matches `metrics_definitions.md` thresholds (green/amber/orange/red)
- Drawdown Summary shows peak-to-current drawdown and days underwater
- Grace Period panel shows all positions in grace period with days remaining
- Position Risk Table shows stop distance, ATR, and state per open position
- Prospective Heat Indicator integrates with Position Sizing Calculator input
- All displayed values sourced from backend — no client-side recalculation
- Passes acceptance test scenarios (ST-04)

**ST-04 — QA: Risk Dashboard Acceptance Test Scenarios**
Owner: QA & Testing Owner
Maps to: S2-01
Effort: ~0.5 day
Description: Author acceptance test scenarios for the Risk Dashboard page. Cover: heat calculation display, threshold colour mapping, grace period display, position risk table, drawdown display, prospective heat indicator. File at `docs/testing/`.
Acceptance Criteria:
- Test scenarios cover all five page sections
- Heat threshold colour scenarios include boundary conditions (exactly 10%, 20%, 30%)
- Grace period edge case: position at day 0, day 10 (expired)
- Position risk table: at least one GRACE, one LOSING, one PROFITABLE state
- Scenarios are derived from `metrics_definitions.md` v1.6.0 — no independent formula interpretation
- Approved by Director of Quality

---

### EPIC-02 — CI Quality Gates
**Maps to:** S2-02, S2-03, S2-04, S2-05
**Theme:** Automated quality gates in CI pipeline
**Effort:** ~2.5 days
**Priority:** P1
**Dependencies:** S2-03 depends on S2-02 (golden baseline must exist first)

#### EPIC-02 Tasks

**ST-05 — Golden Output Regression Baseline**
Owner: Head of Engineering + QA & Testing Owner
Maps to: S2-02 (BLG-NEW-01)
Effort: ~1 day
Description: Create `tests/golden_outputs.json` with spec-derived golden test cases for stop and sizing calculations. Add CI step to assert outputs match golden values to required precision.
Acceptance Criteria:
- `tests/golden_outputs.json` exists with golden values for: stop-loss calculation, position sizing calculation
- All golden values derived from `strategy_rules.md` canonical spec (not from implementation)
- Precision tolerance documented (minimum 4 decimal places for share counts)
- CI step (`validate-analytics.yml` or new workflow) runs golden assertions on every PR
- Build fails on any numeric deviation from golden values
- Director of Quality confirms coverage is sufficient

**ST-06 — Backtest vs Live Stop Reconciliation**
Owner: Head of Engineering
Maps to: S2-03 (BLG-NEW-02)
Effort: ~0.5 day
Dependency: ST-05 must be complete (golden baseline in place)
Description: Add automated check verifying backtest and live stop logic produce identical results for all golden inputs.
Acceptance Criteria:
- Automated check exists comparing backtest vs live stop calculations for all golden inputs
- Any divergence between backtest and live calculation fails the check
- Integrated into CI pipeline

**ST-07 — Dependency Vulnerability Scanning**
Owner: Head of Engineering
Maps to: S2-04 (BLG-NEW-05)
Effort: ~0.5 day
Description: Add CI step scanning Python dependencies for known CVEs using `pip-audit` or equivalent. Block merge (or require review) on high/critical severity.
Acceptance Criteria:
- Dependency vulnerability scan runs on every PR
- High/critical CVEs block merge or produce required review comment
- Scan tool and severity threshold documented in workflow file

**ST-08 — Automated OpenAPI Drift Detection**
Owner: Head of Engineering
Maps to: S2-05 (BLG-NEW-08)
Effort: ~0.5 day
Description: Add CI step detecting drift between `openapi.yaml` and markdown API contracts. Block merge on detected drift.
Acceptance Criteria:
- CI step detects drift between openapi.yaml and markdown contracts
- Merge blocked if drift detected
- Detection approach (generation vs diff) documented; approach decision confirmed in pre-alignment

---

### EPIC-03 — API & Spec Debt (Critical)
**Maps to:** S2-06, S2-07
**Theme:** Resolve P1 spec drift and update reference artefact
**Effort:** ~1.5 days
**Priority:** P1/P2
**Condition:** ST-09 is GATED on Product Owner decision (option a vs b for settings endpoint). Other tasks may proceed independently.

#### EPIC-03 Tasks

**ST-09 — Settings Endpoint Method Drift Resolution**
Owner: API Contracts & Documentation Owner + Head of Engineering
Maps to: S2-06 (BLG-SPEC-D2)
Effort: ~0.5 day (option a — spec update); ~1 day (option b — backend change)
**GATED:** Requires Product Owner + API Contracts owner decision before execution:
- Option (a): Update `settings_endpoints.md` to document `PATCH /settings/{settings_id}` and `POST /settings` as canonical
- Option (b): Align backend to implement `PUT /settings` as specced (breaking change; decision record required)
Description: Once decision is made, implement chosen option. If option (b), file a breaking change decision record.
Acceptance Criteria:
- `settings_endpoints.md` accurately documents the live HTTP method, path, and schema
- No divergence between spec and implementation
- If option (b): decision record filed at `docs/product/decisions/`
- Cross-referenced from `BLG-SPEC-G1` (settings_model.md) for scoping
Prerequisite: ESC-20260304-01 resolved (Product Owner decision required)

**ST-10 — Update openapi.yaml to v1.9.0**
Owner: API Contracts & Documentation Owner
Maps to: S2-07 (BLG-SPEC-D7)
Effort: ~1 day
Description: Update `docs/reference/openapi.yaml` to v1.9.0 reflecting EPIC-06 changes: add `sharpe_ratio_trade_method` to validated metrics, update portfolio positions schema, add `holding_days` to trade objects.
Acceptance Criteria:
- openapi.yaml version field updated to 1.9.0
- `/validate/calculations` response includes `sharpe_ratio_trade_method` (14 validated metrics total)
- GET /trades trade object includes `holding_days` (integer)
- GET /portfolio positions objects reflect v1.9.0 field list
- No conflicts between openapi.yaml and markdown contracts
- API Contracts & Documentation Owner confirms compliance

---

### EPIC-04 — Governance Documentation
**Maps to:** S2-08, S2-09
**Theme:** Operational safety and governance documents
**Effort:** ~1 day
**Priority:** P1

#### EPIC-04 Tasks

**ST-11 — Unavailability Failure Mode Documentation**
Owner: Infrastructure & Operations Owner
Maps to: S2-09 (BLG-NEW-03)
Effort: ~0.5 day
Description: Author policy documenting what happens when the system is unavailable during a trading session (backend down, market data unavailable). Covers: system states, user actions, manual fallbacks, data integrity implications.
Acceptance Criteria:
- Unavailability failure mode documented in `docs/ops/unavailability_policy.md` (or equivalent)
- Document is lifecycle-compliant (Owner, Class, Status, Version, Last Updated)
- Registered in appropriate governance index
- Head of Specs Team confirms lifecycle compliance

**ST-12 — Running API Changelog Document**
Owner: API Contracts & Documentation Owner
Maps to: S2-08 (BLG-NEW-07)
Effort: ~0.5 day
Description: Create `docs/specs/api_contracts/api_changelog.md` — running changelog of all API contract changes per version. Backfill from v1.8.x → v1.9.0 (EPIC-06 changes). Document maintenance obligation.
Acceptance Criteria:
- `docs/specs/api_contracts/api_changelog.md` exists and is lifecycle-compliant
- v1.9.0 EPIC-06 changes backfilled: `sharpe_ratio_trade_method`, portfolio field alignment, `holding_days`
- Maintenance obligation documented alongside contract spec authoring workflow
- Registered in `Specs_Index.md`

---

## Risk Register

| RISK ID | Description | Likelihood | Impact | Mitigation | Relates to |
|---------|-------------|------------|--------|------------|------------|
| RISK-01 | Portfolio Heat formula canonicalization | Resolved | N/A | v1.7 EPIC-03 delivered `metrics_definitions.md` v1.6.0 with formula and thresholds | EPIC-01 |
| RISK-02 | Settings endpoint decision not made before EPIC-03 | Medium | Low | Escalation ESC-20260304-01 raised; EPIC-03 gated; other EPICs unblocked | EPIC-03/ST-09 |
| RISK-03 | No timebox/capacity specified; scope may exceed 2-week window | Medium | Medium | Standard assumption applied (2 weeks, solo-dev evenings); formal capacity check at Stage 4.5 | Release-level |
| RISK-04 | Frontend spec for Risk Dashboard not yet authored | Low | Low | Expected at this stage; Design Gate Engine (Phase 1.5) produces spec before Sprint Planning | EPIC-01/ST-01 |
| RISK-05 | openapi.yaml update (ST-10) may have wider conflicts than anticipated | Low | Medium | API Contracts owner reviews all contract files before update; approach confirmed in pre-alignment | EPIC-03/ST-10 |

---

## Sequencing and Dependencies

```
EPIC-01 (Risk Dashboard)
  └── ST-01 (Design Gate artefact required — Phase 1.5 pre-condition)
  └── ST-02 (confirm heat endpoint — early)
  └── ST-03 (implement — depends on ST-01 spec)
  └── ST-04 (test scenarios — can draft in parallel with ST-03)

EPIC-02 (CI Quality)
  └── ST-05 (golden baseline — no dependency)
  └── ST-06 (reconciliation — depends on ST-05)
  └── ST-07 (vulnerability scan — independent)
  └── ST-08 (OpenAPI drift CI — independent; complements ST-10)

EPIC-03 (Spec Debt)
  └── ST-09 (settings decision — GATED on ESC-20260304-01)
  └── ST-10 (openapi update — independent of ST-09; do early)

EPIC-04 (Governance Docs)
  └── ST-11 (unavailability policy — independent)
  └── ST-12 (API changelog — independent; coordinate with ST-10)
```

---

## Execution Order (Recommended)

1. **Pre-sprint:** Design Gate Engine run (ST-01 prerequisite)
2. **Sprint start:** ST-02, ST-05, ST-07, ST-08, ST-10, ST-11, ST-12 (parallel, no dependencies)
3. **After ST-05:** ST-06
4. **After Design Gate:** ST-03, ST-04 (in parallel)
5. **After ESC-20260304-01 resolved:** ST-09
