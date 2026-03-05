Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-05

# QA Evidence Log — EPIC-01: Risk Dashboard Page

**EPIC:** EPIC-01 — Risk Dashboard Page
**Cycle:** 2026-03-04__release-v1.8
**Sprint goal:** Ship a fully functional Risk Dashboard page giving the trader daily visibility into portfolio heat, drawdown, grace period status, and per-position risk.
**Test scenarios used:** `docs/testing/risk_dashboard_scenarios.md` (to be created by ST-04)

---

## Per-Story Evidence

---

### ST-01 — Frontend Spec: Risk Dashboard Page

**Spec references:** `docs/specs/frontend/pages/risk_dashboard.md` v0.1.0

**Status:** ✅ COMPLETE — Delivered at Design Gate 2026-03-04. Spec locked at v0.1.0.

**Deviation check:** No deviations. Spec delivered as required.

---

### ST-02 — Backend: Confirm Heat Calculation Availability

**Spec references:** `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio`, `docs/specs/metrics_definitions.md#Portfolio Heat`

**Status:** 🟡 PENDING — Delegated to Head of Engineering (DEL-20260305-01).

**What is needed:**
- Confirm `portfolio_heat_percent` in `GET /portfolio` response
- Formula verified against `metrics_definitions.md §Portfolio Heat`
- Prospective heat approach confirmed

*(To be completed by Head of Engineering — fill in commit SHA and evidence below)*

- **Commit SHA:** _(pending)_
- **What was built:** _(pending)_
- **Deviation check:** _(pending)_

---

### ST-03 — Frontend: Risk Dashboard Page Implementation

**Spec references:** `docs/specs/frontend/pages/risk_dashboard.md` v0.1.0

**Status:** 🟡 PENDING — Delegated to Base44 Frontend Prompt Owner (DEL-20260305-02). Blocked on ST-02.

*(To be completed after Base44 implementation)*

- **Commit SHA:** _(pending)_
- **What was built:** _(pending)_
- **Deviation check:** _(pending)_

---

### ST-04 — QA: Risk Dashboard Acceptance Test Scenarios

**Spec references:** `docs/testing/risk_dashboard_scenarios.md`, `docs/specs/metrics_definitions.md#Portfolio Heat`

**Status:** 🟡 PENDING — Delegated to QA & Testing Owner (DEL-20260305-03). Scenario document may be drafted now; execution requires ST-03 complete.

*(To be completed by QA & Testing Owner and Director of Quality)*

- **Commit SHA:** _(pending)_
- **Scenarios file:** `docs/testing/risk_dashboard_scenarios.md` _(pending)_
- **Director of Quality approval:** _(pending)_

---

## EPIC-Level Consolidation

*(To be completed when all ST items are done)*

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-01 | `risk_dashboard.md` | Frontend spec v0.1.0 (Design Gate) | Spec complete, all 5 sections | Pass ✅ | None |
| ST-02 | `portfolio_endpoints.md`, `metrics_definitions.md` | _(pending)_ | Heat endpoint confirmed | _(pending)_ | _(pending)_ |
| ST-03 | `risk_dashboard.md` | _(pending)_ | Risk Dashboard renders, all AC pass | _(pending)_ | _(pending)_ |
| ST-04 | `risk_dashboard_scenarios.md` | _(pending)_ | All scenarios filed and approved | _(pending)_ | _(pending)_ |

**QA test coverage:**
- Scenarios run: `docs/testing/risk_dashboard_scenarios.md` (once filed)
- Regression areas checked: frontend rendering, heat calculation, colour thresholds, grace period logic
- Known deviations filed: _(to be completed)_

**QA sign-off block:** (Director of Quality completes this)
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] ST-04 scenario document approved
- [ ] Heat gauge colour at boundary values verified
- [ ] No client-side recalculation of metric values confirmed
- Signed off by: Director of Quality
- Date:
- Comments:
