**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8
**Release:** v1.8

---

# Sprint Backlog — 2026-03-04__release-v1.8

**Sprint Goal:** Ship a fully functional Risk Dashboard page giving the trader daily visibility into portfolio heat, drawdown, grace period status, and per-position risk, while simultaneously establishing automated correctness gates (golden output CI, vulnerability scanning, OpenAPI drift detection) and closing the highest-priority spec and governance debt carried from v1.7.

---

## Sprint Scope

---

### EPIC-01 — Risk Dashboard Page

**Maps to:** S2-01
**Owner:** Head of Engineering (frontend/backend); Frontend Specs & UX Documentation Owner (ST-01); QA & Testing Owner (ST-04)
**Estimated effort:** ~3–4 days (ST-01 complete; net ~2.75–3.75 days remaining)
**Risk IDs:** RISK-01 (mitigated), RISK-04 (mitigated)
**Execution sequence:** Wave 1 (ST-02), Wave 2 (ST-03), Wave 3 (ST-04); ST-01 complete

---

#### ST-01 — Frontend Spec: Risk Dashboard Page

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** ~0.5 day
**Delegation class:** autonomous
**Status:** ✅ COMPLETE — delivered at Design Gate 2026-03-04
**Spec locked:** `docs/specs/frontend/pages/risk_dashboard.md` v0.1.0

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `docs/specs/frontend/pages/risk_dashboard.md` exists at v0.1.0; lifecycle-compliant header; all five page sections specified with layout, states, data sources, edge cases |
| Quality | Head of Specs Team confirms spec is testable and unambiguous for each component |
| Security | N/A — specification document only; no security surface changed |
| Verification | Head of Specs Team sign-off on file header compliance and content completeness |

**Dependencies:** Design Gate artefact — ✅ resolved
**Notes:** Complete. Spec locked for Sprint Planning.

---

#### ST-02 — Backend: Confirm Heat Calculation Availability

**Owner:** Head of Engineering
**Estimated effort:** ~0.25 day
**Delegation class:** delegated_backend
**Execution sequence:** Wave 1

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `portfolio_heat_percent` confirmed available in `GET /portfolio` response OR a separate heat endpoint specified; prospective heat calculation endpoint approach confirmed (query param extension vs dedicated endpoint) |
| Quality | Manual test confirms `GET /portfolio` returns `portfolio_heat_percent` with a value matching the `metrics_definitions.md §Portfolio Heat` formula for a known set of open positions |
| Security | N/A — read-only backend confirmation; no new input surface; no security surface changed |
| Verification | API Contracts & Documentation Owner confirms contract alignment; Director of Quality spot-checks formula output against canonical spec |

**Dependencies:** None
**Notes:** Unblocks ST-03. Must complete before frontend wiring begins.

---

#### ST-03 — Frontend: Risk Dashboard Page Implementation

**Owner:** Head of Engineering / Base44 Frontend Prompt Owner
**Estimated effort:** ~2–3 days
**Delegation class:** delegated_frontend
**Execution sequence:** Wave 2 (after ST-02)

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Risk Dashboard renders at designated route; Portfolio Heat Gauge colour-coded per canonical thresholds (#22c55e, #f59e0b, #f97316, #ef4444); Drawdown Summary shows current drawdown % and days underwater; Grace Period panel shows all GRACE positions with colour-coded days remaining (green ≥5, amber 2–4, red ≤1), sorted by days remaining ascending; Position Risk Table shows all open positions with ticker, state badge, prices, stop distance %, holding days — sorted GRACE→LOSING→PROFITABLE then by stop distance; Prospective Heat Indicator is collapsible, calculates server-side, shows projected % and increase |
| Quality | ST-04 acceptance scenarios all pass; heat gauge colour at boundary values (exactly 10%, 20%, 30%) verified; each component renders its error state independently on API failure; no console errors on clean load |
| Security | Prospective Heat Indicator inputs (shares, entry price, stop price) validated: positive integers/decimals, stop < entry enforced client-side before submission; all validation also enforced server-side; no XSS risk — numeric inputs only; no new authentication surface introduced |
| Verification | Director of Quality executes ST-04 test scenarios and confirms pass; spot-checks heat gauge colour at each threshold boundary; confirms no client-side recalculation of metric values by reviewing network requests |

**Dependencies:** ST-01 (spec locked ✅), ST-02 (heat endpoint confirmed)
**Notes:** Base44 prompt to be authored from `risk_dashboard.md` v0.1.0 before code generation.

---

#### ST-04 — QA: Risk Dashboard Acceptance Test Scenarios

**Owner:** QA & Testing Owner
**Estimated effort:** ~0.5 day
**Delegation class:** delegated_qa
**Execution sequence:** Wave 3 (after ST-03 ready for testing)

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Test scenarios filed at `docs/testing/risk_dashboard_scenarios.md`; lifecycle-compliant header; covers all five page sections |
| Quality | Scenarios include: heat threshold boundaries (0%, 10%, 20%, 30%); grace period at day 1, day 10, day 11; all three position states simultaneously; prospective heat crossing a threshold boundary; all API error states per component; empty state (no open positions) |
| Security | N/A — test documentation only |
| Verification | Director of Quality reviews and confirms scenarios are sufficient for ST-03 sign-off; explicitly approves the scenario document |

**Dependencies:** ST-03 (scenarios can be drafted in parallel; execution requires ST-03 built)
**Notes:** Scenario document may be drafted before ST-03 completes; execution and sign-off requires ST-03 available.

---

### EPIC-02 — CI Quality Gates

**Maps to:** S2-02, S2-03, S2-04, S2-05
**Owner:** Head of Engineering (ST-05–ST-08); QA & Testing Owner (ST-05 co-owner)
**Estimated effort:** ~2.5 days
**Risk IDs:** RISK-03 (capacity — accepted)
**Execution sequence:** Wave 1 (ST-05, ST-07, ST-08), Wave 2 (ST-06, ST-08 coordination with ST-10)

---

#### ST-05 — Golden Output Regression Baseline

**Owner:** Head of Engineering + QA & Testing Owner
**Estimated effort:** ~1 day
**Delegation class:** delegated_backend
**Execution sequence:** Wave 1

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `tests/golden_outputs.json` exists; contains golden test cases for stop-loss calculation and position sizing calculation; precision tolerance documented (≥4 decimal places for share counts, 2 for prices); CI step added to workflow asserting all golden outputs match on every PR; build fails on any numeric deviation |
| Quality | Golden values independently derived from `strategy_rules.md` canonical spec (not reverse-engineered from implementation); Director of Quality confirms golden set covers all stop/sizing calculation paths |
| Security | N/A — CI test configuration; no production security surface changed |
| Verification | Director of Quality reviews `tests/golden_outputs.json` and confirms: (a) values match spec derivation, (b) coverage is sufficient, (c) CI step fails correctly on a known-bad input |

**Dependencies:** None
**Notes:** Unblocks ST-06. Golden values must be derived from spec, not implementation — this is the critical correctness property.

---

#### ST-06 — Backtest vs Live Stop Reconciliation

**Owner:** Head of Engineering
**Estimated effort:** ~0.5 day
**Delegation class:** delegated_backend
**Execution sequence:** Wave 2 (after ST-05)

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Automated CI check comparing backtest stop calculations vs live system stop calculations for all golden inputs from ST-05; any divergence fails the check; integrated into CI pipeline |
| Quality | Check tested with a deliberately introduced divergence to confirm it catches the defect class; confirmed passing on current codebase |
| Security | N/A — CI assertion only; no production security surface changed |
| Verification | Director of Quality confirms check runs in CI and that a synthetic divergence causes failure |

**Dependencies:** ST-05 (golden baseline must exist)
**Notes:** The reconciliation check is only as good as the golden baseline; ST-05 must be correct first.

---

#### ST-07 — Dependency Vulnerability Scanning

**Owner:** Head of Engineering
**Estimated effort:** ~0.5 day
**Delegation class:** delegated_backend
**Execution sequence:** Wave 1

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | CI step scanning Python dependencies for known CVEs runs on every PR; tool selected and documented in workflow file (e.g., `pip-audit`); high/critical CVEs block merge or produce a mandatory review comment |
| Quality | Confirmed scan runs and produces output; severity threshold applied correctly; test with a known-vulnerable version (if safe to do so in CI environment) or confirm scan output format is correct |
| Security | This step IS the security control; severity threshold (high/critical = block) documented and confirmed with Cybersecurity & Trust Lead |
| Verification | Cybersecurity & Trust Lead acknowledges approach and severity threshold; Director of Quality confirms CI integration |

**Dependencies:** None
**Notes:** Tool choice (pip-audit vs safety) to be made during execution; document the decision in the workflow file.

---

#### ST-08 — Automated OpenAPI Drift Detection

**Owner:** Head of Engineering
**Estimated effort:** ~0.5 day
**Delegation class:** delegated_backend
**Execution sequence:** Wave 2 (ship alongside or after ST-10)

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | CI step detects drift between `docs/reference/openapi.yaml` and markdown API contract files; approach documented in workflow (generation vs diff); merge blocked on detected drift |
| Quality | Drift check passes after ST-10 update (openapi.yaml at v1.9.0); confirmed to fail if a known drift is introduced synthetically |
| Security | N/A — CI tooling; no production security surface changed |
| Verification | Director of Quality confirms CI step runs, passes on clean state (post ST-10), and blocks correctly on synthetic drift |

**Dependencies:** ST-10 (openapi.yaml must be updated before drift check can pass on clean state)
**Notes:** Must ship alongside or immediately after ST-10. Approach decision (generation vs diff) confirmed during execution pre-alignment.

---

### EPIC-03 — API & Spec Debt (Critical)

**Maps to:** S2-06, S2-07
**Owner:** API Contracts & Documentation Owner; Head of Engineering (ST-09 co-owner)
**Estimated effort:** ~1.5 days
**Risk IDs:** RISK-05 (ST-10 openapi conflicts — active, mitigated by pre-alignment)
**Execution sequence:** Wave 1 (ST-09, ST-10 both independent)

---

#### ST-09 — Settings Endpoint Method Drift Resolution

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** ~0.5 day
**Delegation class:** autonomous
**Execution sequence:** Wave 1

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `docs/specs/api_contracts/settings_endpoints.md` updated to document: `PATCH /settings/{settings_id}` (update single setting by ID) and `POST /settings` (create new setting); HTTP method, path, request body schema (field name, type, value), and response schema documented for both; `PUT /settings` entry removed or marked superseded |
| Quality | Spec cross-checked against `backend/main.py` router implementation; no field, path, or method discrepancy between spec and implementation |
| Security | N/A — spec document update only; no code change; no security surface changed |
| Verification | API Contracts & Documentation Owner confirms compliance; Head of Specs Team confirms lifecycle compliance (version increment to next minor, Last Updated updated) |

**Dependencies:** ESC-20260304-01 resolved ✅ (option a — 2026-03-04)
**Notes:** Option (a) chosen: spec follows implementation. No decision record required. Version must be incremented per document_lifecycle_guide.md.

---

#### ST-10 — Update openapi.yaml to v1.9.0

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** ~1 day
**Delegation class:** autonomous
**Execution sequence:** Wave 1

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `docs/reference/openapi.yaml` version field updated to 1.9.0; `/validate/calculations` response schema includes `sharpe_ratio_trade_method` (total: 14 validated metrics); `GET /trades` trade object schema includes `holding_days` (integer); `GET /portfolio` positions schema reflects v1.9.0 field list per `portfolio_endpoints.md` v1.9.0 |
| Quality | No conflicts between openapi.yaml and any markdown contract after update; ST-08 CI drift check passes on updated file |
| Security | N/A — reference document update only; no security surface changed |
| Verification | API Contracts & Documentation Owner confirms no conflicts; ST-08 CI check passes (green) after this update is merged |

**Dependencies:** None (ST-08 must pass after this is merged — sequencing coordination)
**Notes:** RISK-05 — API Contracts owner to review all three contract files in scope before updating openapi.yaml. Ship before or alongside ST-08.

---

### EPIC-04 — Governance Documentation

**Maps to:** S2-08, S2-09
**Owner:** Infrastructure & Operations Owner (ST-11); API Contracts & Documentation Owner (ST-12)
**Estimated effort:** ~1 day
**Execution sequence:** Wave 1 (both independent)

---

#### ST-11 — Unavailability Failure Mode Documentation

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** ~0.5 day
**Delegation class:** autonomous
**Execution sequence:** Wave 1

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `docs/ops/unavailability_policy.md` (or Head of Specs Team-approved equivalent path) created; lifecycle-compliant header (Owner, Class, Status, Version, Last Updated); covers: system states during unavailability, user required actions, manual fallback procedures, data integrity implications; registered in appropriate index |
| Quality | Document covers at minimum: backend down, market data feed unavailable, partial degradation (one service down); each scenario includes user action and data integrity implication |
| Security | N/A — policy document only |
| Verification | Head of Specs Team confirms lifecycle compliance; Infrastructure & Operations Owner confirms operational accuracy |

**Dependencies:** None

---

#### ST-12 — Running API Changelog Document

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** ~0.5 day
**Delegation class:** autonomous
**Execution sequence:** Wave 1 (coordinate with ST-10)

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `docs/specs/api_contracts/api_changelog.md` created; lifecycle-compliant header; v1.9.0 EPIC-06 changes backfilled: `sharpe_ratio_trade_method` in analytics, portfolio v1.9.0 field list, `holding_days` in trades; maintenance obligation documented; registered in `docs/specs/Specs_Index.md` |
| Quality | Changelog entries reference the contract file versions and EPIC/ST that introduced each change; no missing v1.9.0 changes |
| Security | N/A — documentation only |
| Verification | Head of Specs Team confirms lifecycle compliance and Specs_Index.md registration |

**Dependencies:** Coordinate with ST-10 (changelog should reflect same version state as openapi.yaml after ST-10)

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity (milestone-based) | ~10–12 full-time equivalent days |
| Total estimated effort (in-scope, net of ST-01) | ~7.75–8.75 days |
| Utilisation | ~65–88% (within milestone-based envelope) |
| Over-allocation (strict 2-week) | Yes — accepted by Product Owner (milestone-based delivery) |

## Items Deferred This Sprint

None — all 12 items included.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| ST-02: confirm heat endpoint approach | Head of Engineering | No — confirm at execution start |
| ST-08/ST-10: agree OpenAPI approach (generation vs diff) | Head of Engineering + API Contracts owner | No — confirm at execution start |

No blockers outstanding. ✅

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-03-04
**Scope confirmed:** Confirmed — all 12 items; over-allocation acknowledged; milestone-based delivery
**Capacity confirmed:** Confirmed — WARN accepted; milestone-based envelope
**Signed off by:** Product Owner
**Date:** 2026-03-04
