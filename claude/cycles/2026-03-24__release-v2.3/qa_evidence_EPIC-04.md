Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-30

---

# QA Evidence Log — EPIC-04 (Frontend Polish)

**Cycle:** 2026-03-24__release-v2.3
**Sprint goal:** Establish a reproducible QA automation layer, deliver user-facing compliance and metrics features, and resolve all outstanding frontend polish and operational spec debt for v2.3.

---

## ST-11 — BLG-FE-04: Alert Thresholds Empty State CTA Button

**Spec reference:** `docs/specs/frontend/pages/notifications.md#Section 2: Alert Rule Thresholds`
**Commit:** fe91153
**Classification:** autonomous (reclassified from delegated_frontend per 2026-03-26 frontend delegation decision)

**What was built:**
CreateForm component added to AlertThresholdsSection: alert type selector + conditional threshold input (stop_loss_approach only) + POST /alerts/rules. threshold input changed to type=text/inputMode=decimal (fixes 'e' bypass); !border-rose-500/60 fixes border colour (cn=clsx only, no tailwind-merge). Playwright SC-ATS-01–05b, 06–11 (13/13 pass). Visual scenarios in docs/testing/alert_thresholds_empty_state_scenarios.md.

**Acceptance criteria:**
- [x] CTA button ("Add alert rule") present in Alert Thresholds empty state
- [x] Clicking the button opens creation form (inline form in empty state section)
- [x] Button hidden when alert rules are present (populated state regression SC-ATS-VIS-06 passed)
- [x] Empty state has neutral styling — verified by Playwright mock; unreachable on staging due to backend auto-seeding (DEV-EPIC02-ST04-01)
- [x] DEV-EPIC02-ST04-01 deviation documented and accepted — empty state only reachable via mock

**Test scenarios:** SC-ATS-01–05b, 06–11 in tests/e2e/ (13/13 passing). Visual scenarios SC-ATS-VIS-01–06 in docs/testing/alert_thresholds_empty_state_scenarios.md.

**Deviations:** DEV-EPIC02-ST04-01 — empty state unreachable on staging due to backend auto-seeding. Accepted; verified by Playwright mock only. Documented in commit notes.

**DoQ sign-off:** Granted 2026-03-26. SC-ATS-VIS-04 (border colour) and SC-ATS-VIS-05 (e validation) passed after fixes. SC-ATS-VIS-06 passed. SC-ATS-VIS-01/02/03 verified by Playwright mock only — accepted per DEV-EPIC02-ST04-01. All 13 Playwright tests passing.

---

## ST-10 — BLG-FE-05: Alert Notification Badge in Nav

**Spec reference:** `docs/specs/frontend/pages/notifications.md#Nav Alert Badge`; `docs/design/2026-03-24__release-v2.3/alert-nav-badge/ux_spec.md`
**Commit:** cbe0848
**Classification:** autonomous (reclassified from delegated_frontend per 2026-03-26 frontend delegation decision)

**What was built:**
Alerts item added to Tools nav group. alertBadge prop suppresses active-state dual-highlight. alertCount fetched from GET /alerts/history vs sessionStorage alerts-last-visit. Badge clears on NOTIFICATIONS_PAGES navigation. Tools header badge color updated to red-500. Playwright SC-ANB-01–08 automated. seed_alerts.sql patched on main (commit 1ab04d8) to seed 5 alert_evaluations rows for staging test precondition.

**Acceptance criteria:**
- [x] Badge visible on Alerts nav item when unacknowledged alerts exist — SC-ANB-VIS-01 pass (badge shows 5 after session storage cleared)
- [x] Badge count accurate (reflects unacknowledged alert count since last visit)
- [x] Badge max display: 99+ — verified by code review (count > 99 renders '99+'); SC-ANB-VIS-03 not verifiable on staging (requires 101+ rows)
- [x] Badge hidden when count = 0 — SC-ANB-VIS-02 pass
- [x] Badge clears on Alerts nav — SC-ANB-VIS-04 pass
- [x] Count persists across non-Alerts navigation — SC-ANB-VIS-05 pass
- [x] Badge propagates to collapsed Tools group header (ST-13 integration) — verified in ST-13 sign-off
- [x] No regression to existing nav layout — Playwright SC-ANB-01–08 all passing

**Test scenarios:** SC-ANB-01–08 automated Playwright (tests/e2e/). Visual scenarios SC-ANB-VIS-01–05 in docs/testing/alert_nav_badge_scenarios.md.

**Deviations:** SC-ANB-VIS-03 (99+ cap) not verifiable on staging — requires seeding 101+ alert_evaluations rows. Verified by code review only. Accepted — deterministic code path.

**DoQ sign-off:** Granted 2026-03-29. SC-ANB-VIS-01/02/04/05 pass on staging. SC-ANB-VIS-03 code-review only (accepted). Playwright SC-ANB-01–08 all passing. Evidence method: staging visual run + code review for SC-ANB-VIS-03.

---

## ST-12 — BLG-FE-02: Loading State Standardisation

**Spec reference:** `docs/specs/frontend/patterns/loading_states.md`; `docs/design/2026-03-24__release-v2.3/loading-states/ux_spec.md`
**Commit:** f6aa41b
**Classification:** autonomous (reclassified from delegated_frontend per 2026-03-26 frontend delegation decision)

**What was built:**
DataState component created at src/components/ui/DataState.js. Applied to all 5 pages: Portfolio (Dashboard.js), Positions, Watchlist, Alerts (Notifications.js), Analytics (PerformanceAnalytics.js). Skeleton loaders replaced with spinner. Error states added to Positions and Analytics. Playwright SC-LS-01–13 all passing.

Note: Positions.js and PerformanceAnalytics.js include both MetricsStalenessIndicator (ST-02/EPIC-01) and DataState — merge conflict resolved 2026-03-30; both components coexist (staleness indicator above DataState wrapper).

**Acceptance criteria:**
- [x] Loading state: spinner (centered) on Portfolio, Positions, Watchlist, Alerts, Analytics — all 5 pages
- [x] Empty state: neutral icon + heading + body + optional CTA on all 5 pages
- [x] Error state: error icon + "Something went wrong" + retry button on Positions and Analytics
- [x] Error state visually distinct from empty state — SC-LS-VIS series all passed
- [x] Retry button re-triggers the failed API call — onRetry prop wired to refetch
- [x] No regression to existing page functionality — Playwright SC-LS-01–13 passing

**Test scenarios:** SC-LS-01–13 automated Playwright. Visual scenarios SC-LS-VIS-01–13 in docs/testing/ (13/13 passing).

**Deviations:** SC-LS-VIS-01a required spinner alignment fix (addressed in f6aa41b). No further deviations.

**DoQ sign-off:** Granted 2026-03-26. All 13 visual sub-scenarios passed. SC-LS-VIS-01a required one fix pass; all others passed first run.

---

## ST-13 — BLG-UX-01: Sidebar Navigation Overflow

**Spec reference:** `docs/specs/frontend/pages/navigation.md`; `docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md`
**Commit:** 22e77f8 (implementation); 5f871af (DoQ sign-off)
**Classification:** autonomous (reclassified from delegated_frontend per 2026-03-26 frontend delegation decision)

**What was built:**
Collapsible groups implemented in src/Layout.js. 4 groups: Trading, Analytics, Tools, System. sessionStorage persistence. Active group auto-expand. Badge propagation integrated with ST-10. Dashboard ungrouped at top. Playwright SC-SNV-01–08 in tests/e2e/sidebar-nav-groups.spec.js. Visual scenarios in docs/testing/sidebar_nav_scenarios.md v0.2.

**Acceptance criteria:**
- [x] Product Owner design decision documented (collapsible section groups — ✓ documented in design gate 2026-03-24)
- [x] Sidebar navigation accessible on shorter screens without excessive scrolling
- [x] 4 groups: Trading, Analytics, Tools, System with correct items in each group
- [x] Active group always expanded; non-active groups collapsible
- [x] Collapse state persists in sessionStorage
- [x] Badge from ST-10 visible on collapsed Tools group header
- [x] No regression to existing navigation links or routes — Playwright SC-SNV-01–08 (8/8 pass)

**Test scenarios:** SC-SNV-01–08 automated Playwright (tests/e2e/sidebar-nav-groups.spec.js). Visual scenarios SC-SNV-VIS-02 in docs/testing/sidebar_nav_scenarios.md v0.2.

**Deviations:** None.

**DoQ sign-off:** Granted 2026-03-29. SC-SNV-VIS-02 (group labels muted grey uppercase small-caps + chevron direction) verified on staging. Playwright SC-SNV-01–08 all passing (8/8). Evidence method: staging visual run for SC-SNV-VIS-02; Playwright for all other AC.

---

## EPIC-04 Consolidation Block

**EPIC:** EPIC-04 — Frontend Polish
**Cycle:** 2026-03-24__release-v2.3

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-11 | notifications.md#Section 2 | Alert thresholds empty state CTA + form (fe91153) | CTA present, form works, DEV-EPIC02-ST04-01 closed | ✅ Pass | DEV-EPIC02-ST04-01 accepted |
| ST-10 | notifications.md#Nav Alert Badge | Alert notification badge on Alerts nav item (cbe0848) | Badge accurate, clears on visit, propagates to group header | ✅ Pass | SC-ANB-VIS-03 code-review only (accepted) |
| ST-12 | loading_states.md | DataState loading/empty/error standardisation — 5 pages (f6aa41b) | 3 states consistent on all 5 pages, retry button works | ✅ Pass | SC-LS-VIS-01a fixed in f6aa41b |
| ST-13 | navigation.md | 4 collapsible sidebar nav groups in Layout.js (22e77f8) | Groups correct, collapse/persist, badge integrated, no nav regression | ✅ Pass | None |

**Regression areas checked:**
- Navigation routing: all links and routes unchanged — Playwright SC-SNV-01–08 confirm
- Page functionality on all 5 pages: DataState wrapper is pass-through when data present — no functional regression
- Alert badge integration with sidebar: badge propagates to Tools group header when collapsed
- Merge with EPIC-01 (ST-02): MetricsStalenessIndicator coexists with DataState on Positions and Analytics pages; resolved 2026-03-30

**URL construction check (LL-v2.0-P3-4):** No direct URL construction in any EPIC-04 frontend component. All API calls use `api.*` wrapper or `apiFetch`. ✅

**QA sign-off block:**
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked — navigation routing, page functionality on all 5 pages; DataState merge with MetricsStalenessIndicator verified
- [x] For any frontend component making direct URL construction: N/A — all calls via api.* or apiFetch. LL-v2.0-P3-4 satisfied.
- Signed off by: Director of Quality (Engine)
- Date: 2026-03-30
- Comments: ST-10/11/12/13 all delivered with individual DoQ sign-offs on staging or by Playwright. ST-12 merge conflict with EPIC-01 resolved 2026-03-30 — both MetricsStalenessIndicator and DataState coexist correctly. No P0/P1 deviations open. Disposition: ✅ Pass.
