Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-25

---

# QA Evidence Log — EPIC-01 (User Features: Compliance & Metrics)

**Cycle:** 2026-03-24__release-v2.3
**Sprint goal:** Establish a reproducible QA automation layer, deliver user-facing compliance and metrics features, and resolve all outstanding frontend polish and operational spec debt for v2.3.

---

## ST-01 — BLG-FEAT-11: Strategy Compliance Score (Display-Only)

**Spec reference:** `docs/specs/frontend/pages/positions.md#Strategy Compliance Panel`; `docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md`
**Commit:** Pending — delegated to Base44 Frontend Prompt Owner (DEL-20260325-06)
**Classification:** delegated_frontend

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] Collapsible compliance panel visible below Positions table in Table View
- [ ] Panel shows overall status header (Compliant/Needs Attention/Review Required) with colour coding
- [ ] Per-position table: Ticker | Stop Compliance | Stop Age | Size Compliance
- [ ] Panel hidden in Grid View and Journal View
- [ ] Panel hidden when no open positions
- [ ] Display-only — no actions available from panel (§13.3 constraint)
- [ ] Backend provides compliance flags — no frontend-side ATR computation
- [ ] Loading state: spinner while data loads
- [ ] All compliant: panel collapsed by default; any non-compliant: expanded by default
- [ ] User can manually toggle regardless of default state

**Test scenarios:** *Test scenario gap flag: EPIC-01 test_scenarios pending — QA & Testing Owner to author before next sprint on compliance/staleness domain.*

**Deviations:** *To be assessed at delivery verification. Note: SPS=4 — Strategy Rules & System Intent Owner DoQ sign-off required at delivery verification.*

---

## ST-02 — BLG-FEAT-09: Metrics Staleness Indicator

**Spec reference:** `docs/specs/frontend/pages/analytics.md#Metrics Staleness Indicator`; `docs/design/2026-03-24__release-v2.3/staleness-indicator/ux_spec.md`
**Commit:** Pending — delegated to Base44 Frontend Prompt Owner (DEL-20260325-07)
**Classification:** delegated_frontend

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] Staleness indicator visible on Analytics page (below title, above period selector)
- [ ] Staleness indicator visible on Portfolio/Positions page (below title, inline with view controls)
- [ ] Fresh state (< 4 hours): grey text `"Data as of N mins ago"`
- [ ] Stale state (≥ 4 hours): amber badge `"⚠ Data as of Nh ago — may be outdated"`
- [ ] Hover tooltip shows absolute ISO timestamp
- [ ] Relative time format: < 1 min → "just now"; 1–59 min → "N mins ago"; 1–23 hrs → "Nh ago"; ≥ 24 hrs → "N days ago"
- [ ] Absent/null `last_sync_at`: indicator hidden entirely
- [ ] Backend `last_sync_at` field present on analytics and portfolio API responses

**Test scenarios:** *Test scenario gap flag: EPIC-01 test_scenarios pending (shared with ST-01 flag).*

**Deviations:** *To be assessed at delivery verification.*

---

## EPIC-01 Consolidation Block

*(To be completed when all ST items are done — pending ST-01 and ST-02 delegation)*

**EPIC:** EPIC-01 — User Features: Compliance & Metrics
**Cycle:** 2026-03-24__release-v2.3

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-01 | positions.md#Strategy Compliance Panel | Strategy compliance panel (Positions Table View) | Panel visible, display-only, §13.3 compliant | Pending | TBD |
| ST-02 | analytics.md#Metrics Staleness Indicator | Staleness indicator on Analytics + Portfolio pages | Indicator accurate, states correct | Pending | TBD |

**Test scenario gap note:** EPIC-01 test_scenarios file pending — QA & Testing Owner to author before next sprint covering ST-01 (compliance panel) and ST-02 (staleness indicator).

**QA sign-off block:** *(Director of Quality completes this when ST-01 and ST-02 are done — with Strategy Rules & System Intent Owner co-sign for ST-01)*
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] ST-01: §13.3 display-only constraint verified (no automated actions)
- [ ] ST-01: Strategy Rules & System Intent Owner sign-off recorded
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction: confirm base URL variable exposed
- Signed off by: Director of Quality
- Date:
- Comments:
