Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-25

---

# QA Evidence Log — EPIC-04 (Frontend Polish)

**Cycle:** 2026-03-24__release-v2.3
**Sprint goal:** Establish a reproducible QA automation layer, deliver user-facing compliance and metrics features, and resolve all outstanding frontend polish and operational spec debt for v2.3.

---

## ST-11 — BLG-FE-04: Alert Thresholds Empty State CTA Button

**Spec reference:** `docs/specs/frontend/pages/notifications.md#Section 2: Alert Rule Thresholds`
**Commit:** Pending — delegated to Base44 Frontend Prompt Owner (DEL-20260325-08)
**Classification:** delegated_frontend

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] CTA button ("Add alert rule") present in Alert Thresholds empty state
- [ ] Clicking the button navigates to alert rule creation flow (or opens creation modal)
- [ ] Button hidden when alert rules are present
- [ ] Empty state has neutral styling (not error styling)
- [ ] DEV-EPIC02-ST04-01 deviation resolved

**Test scenarios:** *Test scenario gap flag: EPIC-04 test_scenarios pending.*

**Deviations:** *To be assessed. DEV-EPIC02-ST04-01 should be resolved.*

---

## ST-10 — BLG-FE-05: Alert Notification Badge in Nav

**Spec reference:** `docs/specs/frontend/pages/notifications.md#Nav Alert Badge`; `docs/design/2026-03-24__release-v2.3/alert-nav-badge/ux_spec.md`
**Commit:** Pending — delegated to Base44 Frontend Prompt Owner (DEL-20260325-09)
**Classification:** delegated_frontend

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] Badge visible on Alerts nav item when unacknowledged alerts exist
- [ ] Badge count accurate (reflects unacknowledged alert count)
- [ ] Badge max display: 99+
- [ ] Badge hidden when count = 0
- [ ] Badge clears (resets to 0) when user navigates to Alerts page
- [ ] Count persists across session navigation
- [ ] Badge propagates to collapsed Tools group header (ST-13 integration)
- [ ] No regression to existing nav layout

**Test scenarios:** *Test scenario gap flag: EPIC-04 test_scenarios pending.*

**Deviations:** *To be assessed at delivery verification.*

---

## ST-12 — BLG-FE-02: Loading State Standardisation

**Spec reference:** `docs/specs/frontend/patterns/loading_states.md`; `docs/design/2026-03-24__release-v2.3/loading-states/ux_spec.md`
**Commit:** Pending — delegated to Base44 Frontend Prompt Owner (DEL-20260325-10)
**Classification:** delegated_frontend

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] Loading state: spinner (centered) on Portfolio, Positions, Watchlist, Alerts, Analytics
- [ ] Empty state: neutral icon + heading + body + optional CTA on all 5 pages
- [ ] Error state: error icon + "Something went wrong" + retry button on all 5 pages
- [ ] Error state visually distinct from empty state (colour, icon, retry button)
- [ ] Retry button re-triggers the failed API call
- [ ] No regression to existing page functionality

**Test scenarios:** Visual AC — requires DoQ visual verification on all 5 pages.

**Deviations:** *To be assessed at delivery verification.*

---

## ST-13 — BLG-UX-01: Sidebar Navigation Overflow

**Spec reference:** `docs/specs/frontend/pages/navigation.md`; `docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md`
**Commit:** Pending — delegated to Base44 Frontend Prompt Owner (DEL-20260325-11)
**Classification:** delegated_frontend

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] Product Owner design decision documented (collapsible section groups — ✓ documented in design gate 2026-03-24)
- [ ] Sidebar navigation accessible on shorter screens without excessive scrolling
- [ ] 4 groups: Trading, Analytics, Tools, System with correct items in each group
- [ ] Active group always expanded; non-active groups collapsible
- [ ] Collapse state persists in sessionStorage
- [ ] Badge from ST-10 visible on collapsed Tools group header
- [ ] No regression to existing navigation links or routes

**Test scenarios:** *Test scenario gap flag: EPIC-04 test_scenarios pending (shared with ST-10 flag).*

**Deviations:** *To be assessed at delivery verification.*

---

## EPIC-04 Consolidation Block

*(To be completed when all ST items are done — pending all 4 items)*

**EPIC:** EPIC-04 — Frontend Polish
**Cycle:** 2026-03-24__release-v2.3

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-11 | notifications.md#Section 2 | Alert thresholds empty state CTA button | CTA present, navigates to creation, DEV-EPIC02-ST04-01 closed | Pending | TBD |
| ST-10 | notifications.md#Nav Alert Badge | Alert notification badge on Alerts nav item | Badge accurate, clears on visit, propagates to group header | Pending | TBD |
| ST-12 | loading_states.md | Loading/empty/error state standardisation (5 pages) | 3 states consistent on all 5 pages, retry button works | Pending | TBD |
| ST-13 | navigation.md | Sidebar nav 4 collapsible groups | Groups correct, collapse works, badge integrated, no nav regression | Pending | TBD |

**Test scenario gap note:** EPIC-04 test_scenarios file pending — QA & Testing Owner to author before next sprint covering ST-10 (alert badge) and ST-13 (sidebar nav groups).

**QA sign-off block:** *(Director of Quality completes this when all 4 items are done)*
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked — navigation routing, page functionality on all 5 pages
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm base URL variable exposed **(LL-v2.0-P3-4)**
- Signed off by: Director of Quality
- Date:
- Comments:
