**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Stage 4 — Backlog Slice

## Release: v1.8 — Risk Dashboard

<!-- release-plan-marker: RP:v1.8:2026-03-04__release-v1.8 -->

---

## Sprint Backlog — v1.8

### EPIC-01 — Risk Dashboard Page
**Maps to:** S2-01 (Roadmap §3.4)
**Priority:** P0 (primary release goal)
**Effort:** 3–4 days
**Design Gate required:** Yes — frontend spec must be produced by Design Gate Engine before Sprint Planning opens

---

**ST-01 — Frontend Spec: Risk Dashboard Page**
Owner: Frontend Specs & UX Documentation Owner
Effort: ~0.5 day
Status: Pending (prerequisite: Design Gate artefact)

Acceptance Criteria:
- `docs/specs/frontend/pages/risk_dashboard.md` exists, lifecycle-compliant (Owner, Class 1, Status, Version v0.1.0, Last Updated)
- Covers all five sections: Portfolio Heat Gauge, Drawdown Summary, Grace Period Panel, Position Risk Table, Prospective Heat Indicator
- Layout, component states, data sources, and edge cases specified for each section
- Heat gauge colour thresholds cross-referenced to `metrics_definitions.md` v1.6.0 (green <10%, amber 10–20%, orange 20–30%, red ≥30%)
- Head of Specs Team confirms lifecycle compliance

---

**ST-02 — Backend: Confirm Heat Calculation Availability**
Owner: Head of Engineering
Effort: ~0.25 day
Status: Pending

Acceptance Criteria:
- `portfolio_heat_percent` available in `GET /portfolio` response (or dedicated endpoint confirmed)
- Implementation formula verified against `metrics_definitions.md §Portfolio Heat` exactly
- No new external dependencies
- API Contracts & Documentation Owner confirms contract alignment

---

**ST-03 — Frontend: Risk Dashboard Page Implementation**
Owner: Head of Engineering / Base44 Frontend Prompt Owner
Effort: ~2–3 days
Status: Pending (requires ST-01 spec)

Acceptance Criteria:
- Risk Dashboard page renders at designated route
- Portfolio Heat Gauge colour-coded per canonical thresholds (green/amber/orange/red)
- Drawdown Summary displays peak-to-current drawdown percentage and days underwater
- Grace Period panel lists all open positions in grace period with days remaining
- Position Risk Table displays stop distance, ATR multiple, and state (GRACE / LOSING / PROFITABLE) per open position
- Prospective Heat Indicator shows estimated heat impact of a hypothetical new position
- All values sourced from backend responses — zero client-side recalculation
- No console errors on load
- Passes ST-04 acceptance scenarios

---

**ST-04 — QA: Risk Dashboard Acceptance Test Scenarios**
Owner: QA & Testing Owner
Effort: ~0.5 day
Status: Pending

Acceptance Criteria:
- Test scenarios filed at `docs/testing/`
- Cover all five page sections
- Heat threshold boundary conditions included: exactly 0%, 10%, 20%, 30%
- Grace period edge cases: position at day 1, day 10 (boundary), day 11 (expired)
- Position state scenarios: at least one position in each of GRACE, LOSING, PROFITABLE
- Prospective heat: new position would push heat above 20% threshold
- All expected values derived from `metrics_definitions.md` v1.6.0 — no independent interpretation
- Director of Quality sign-off

---

### EPIC-02 — CI Quality Gates
**Maps to:** S2-02 (BLG-NEW-01), S2-03 (BLG-NEW-02), S2-04 (BLG-NEW-05), S2-05 (BLG-NEW-08)
**Priority:** P1
**Effort:** ~2.5 days

---

**ST-05 — Golden Output Regression Baseline**
Owner: Head of Engineering + QA & Testing Owner
Effort: ~1 day
Status: Pending
Maps to: S2-02 (BLG-NEW-01)

Acceptance Criteria:
- `tests/golden_outputs.json` created with golden test cases for stop-loss and position sizing calculations
- All golden values derived from `strategy_rules.md` canonical spec — not from current implementation
- Precision tolerance documented in file: minimum 4 decimal places for share counts, 2 for prices
- CI step added (new workflow or extension of `validate-analytics.yml`) asserting outputs match golden values on every PR
- Build fails if any numeric deviation from golden values detected
- Director of Quality confirms golden coverage is sufficient for stop/sizing logic

---

**ST-06 — Backtest vs Live Stop Reconciliation**
Owner: Head of Engineering
Effort: ~0.5 day
Status: Pending (requires ST-05 complete)
Maps to: S2-03 (BLG-NEW-02)
Dependency: ST-05 must be complete

Acceptance Criteria:
- Automated CI check exists comparing backtest stop calculations vs live system stop calculations for all golden inputs from ST-05
- Any divergence between backtest and live logic fails the check
- Integrated into CI pipeline (same run as or adjacent to golden output check)

---

**ST-07 — Dependency Vulnerability Scanning**
Owner: Head of Engineering
Effort: ~0.5 day
Status: Pending
Maps to: S2-04 (BLG-NEW-05)

Acceptance Criteria:
- CI step scanning Python dependencies for known CVEs runs on every PR
- Tool selected (e.g., `pip-audit`, `safety`) and documented in workflow file
- Severity threshold documented: high/critical CVEs block merge (or produce a mandatory review comment)
- Cybersecurity & Trust Lead acknowledges approach

---

**ST-08 — Automated OpenAPI Drift Detection**
Owner: Head of Engineering
Effort: ~0.5 day
Status: Pending
Maps to: S2-05 (BLG-NEW-08)

Acceptance Criteria:
- CI step detects drift between `docs/reference/openapi.yaml` and markdown API contract files
- Approach (generation vs diff) documented in workflow; approach confirmed during pre-alignment
- Merge blocked if drift detected
- Complements ST-10 (openapi.yaml update) — both must ship together

---

### EPIC-03 — API & Spec Debt (Critical)
**Maps to:** S2-06 (BLG-SPEC-D2), S2-07 (BLG-SPEC-D7)
**Priority:** P1/P2
**Effort:** ~1.5 days
**Note:** ST-09 is GATED on ESC-20260304-01 (Product Owner decision on settings endpoint method). ST-10 is independent and may proceed.

---

**ST-09 — Settings Endpoint Method Drift Resolution**
Owner: API Contracts & Documentation Owner + Head of Engineering
Effort: ~0.5 day (option a) / ~1 day (option b)
Status: GATED — awaiting ESC-20260304-01 resolution
Maps to: S2-06 (BLG-SPEC-D2)

Gate condition: Product Owner must declare option (a) or (b):
- (a) Update `settings_endpoints.md` to document `PATCH /settings/{settings_id}` and `POST /settings` as canonical
- (b) Align backend to implement `PUT /settings` as specced (breaking change — decision record required)

Acceptance Criteria:
- `settings_endpoints.md` accurately documents the live HTTP method, path, and request/response schema
- No divergence between spec and implementation
- If option (b): decision record filed at `docs/product/decisions/settings-method-change-v1.8.md`
- API Contracts & Documentation Owner confirms compliance

---

**ST-10 — Update openapi.yaml to v1.9.0**
Owner: API Contracts & Documentation Owner
Effort: ~1 day
Status: Pending (independent — does not require ESC-20260304-01)
Maps to: S2-07 (BLG-SPEC-D7)

Acceptance Criteria:
- `docs/reference/openapi.yaml` version field updated to 1.9.0
- `/validate/calculations` response includes `sharpe_ratio_trade_method` (14 validated metrics total)
- `GET /trades` trade object includes `holding_days` (integer)
- `GET /portfolio` positions objects reflect v1.9.0 field list from `portfolio_endpoints.md` v1.9.0
- No conflicts between openapi.yaml and markdown contracts
- API Contracts & Documentation Owner confirms compliance
- ST-08 CI drift check passes after this update

---

### EPIC-04 — Governance Documentation
**Maps to:** S2-08 (BLG-NEW-07), S2-09 (BLG-NEW-03)
**Priority:** P1
**Effort:** ~1 day

---

**ST-11 — Unavailability Failure Mode Documentation**
Owner: Infrastructure & Operations Owner
Effort: ~0.5 day
Status: Pending
Maps to: S2-09 (BLG-NEW-03)

Acceptance Criteria:
- `docs/ops/unavailability_policy.md` (or equivalent path) created and lifecycle-compliant
- Covers: system states during unavailability, user required actions, manual fallback procedures, data integrity implications
- Registered in appropriate governance or ops index
- Head of Specs Team confirms lifecycle compliance (Owner, Class, Status, Version, Last Updated)

---

**ST-12 — Running API Changelog Document**
Owner: API Contracts & Documentation Owner
Effort: ~0.5 day
Status: Pending
Maps to: S2-08 (BLG-NEW-07)

Acceptance Criteria:
- `docs/specs/api_contracts/api_changelog.md` created and lifecycle-compliant
- v1.9.0 EPIC-06 changes backfilled: `sharpe_ratio_trade_method` in analytics, portfolio v1.9.0 field list, `holding_days` in trades
- Maintenance obligation documented: API Changelog must be updated alongside every contract version bump
- Registered in `docs/specs/Specs_Index.md`
- Head of Specs Team confirms lifecycle compliance

---

## Sprint Summary

| EPIC | Title | Tasks | Effort | Priority |
|------|-------|-------|--------|----------|
| EPIC-01 | Risk Dashboard Page | ST-01 to ST-04 | 3–4 days | P0 |
| EPIC-02 | CI Quality Gates | ST-05 to ST-08 | ~2.5 days | P1 |
| EPIC-03 | API & Spec Debt | ST-09 (gated), ST-10 | ~1.5 days | P1/P2 |
| EPIC-04 | Governance Docs | ST-11, ST-12 | ~1 day | P1 |
| **Total** | | **12 tasks** | **~8–9 days** | |

## Deferred from v1.8

| ID | Title | Priority | Deferred To | Rationale |
|----|-------|----------|-------------|-----------|
| BLG-NEW-04 | AI-Assisted Workflow Governance Policy | P2 | v1.9 | P2; capacity constraint |
| BLG-SPEC-D1 | API Contracts README version | P3 | v1.9 | P3 housekeeping |
| BLG-SPEC-D3 | GET /market/status undocumented | P2 | v1.9 | Capacity; lower urgency than CI items |
| BLG-SPEC-D4 | GET /positions/search/tags undocumented | P3 | v1.9 | P3 |
| BLG-SPEC-D8 | System_status_report.md lifecycle header | P3 | v1.9 | P3 |
| BLG-SPEC-D9 | process_index/Specs_Index wrong path refs | P3 | v1.9 | P3 |
| BLG-SPEC-G1 | settings_model.md missing | P2 | v1.9 | Blocked on D2 decision |
| BLG-SPEC-G2 | Error Response Standard not defined | P2 | v1.9 | Significant scope; separate initiative |
| BLG-SPEC-G3 | structured_logging_standards not in index | P3 | v1.9 | P3 |
| BLG-SPEC-G4 | ADR-002 wrong location | P3 | v1.9 | P3 |
| BLG-SPEC-G5 | validation_system.md owner non-compliant | P3 | v1.9 | P3 |
