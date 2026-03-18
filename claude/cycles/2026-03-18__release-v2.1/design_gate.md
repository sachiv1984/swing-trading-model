**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Design Gate Record — 2026-03-18__release-v2.1

## Gate Status: PASSED

Initial run: 2026-03-18 (status: BLOCKED — 6 items pending design artefacts)
Gate cleared: 2026-03-18
PMO Lead: confirmed
Head of UX & Design: confirmed (classification + all 6 artefacts produced)
Product Owner: confirmed (all 6 artefacts approved)
Frontend Specs & UX Documentation Owner: confirmed (all 5 spec files updated/created)
Head of Specs Team: confirmed (lifecycle compliance verified on all spec files)

**Sprint Planning is unblocked.** All Design Required items cleared. `plan sprint` may be issued.

---

## Item Classification Summary

| Item ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|---------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Author async notification delivery ADR | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-02 | Spec: alerts endpoint + notification preference model | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-03 | Backend: alert rules engine | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-04 | Backend: notification delivery (email) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-05 | Frontend: notification preferences page | Design Required | `docs/design/2026-03-18__release-v2.1/notification-preferences/ux_spec.md` | `docs/specs/frontend/pages/notifications.md` v0.1 | ✅ Cleared |
| ST-06 | Frontend: in-app notification feed | Design Required | `docs/design/2026-03-18__release-v2.1/notification-feed/ux_spec.md` | `docs/specs/frontend/pages/notifications.md` v0.1 | ✅ Cleared |
| ST-07 | QA: notification delivery test scenarios | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-08 | Spec: watchlist data model + API endpoints | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-09 | Backend: watchlist implementation | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-10 | Frontend: watchlist UI | Design Required | `docs/design/2026-03-18__release-v2.1/watchlist/ux_spec.md` | `docs/specs/frontend/pages/watchlist.md` v0.1 | ✅ Cleared |
| ST-11 | Implement chart interactivity (CHART-IX) | Design Required | `docs/design/2026-03-18__release-v2.1/chart-interactivity/ux_spec.md` | `docs/specs/frontend/pages/analytics.md` v1.5 | ✅ Cleared |
| ST-12 | BLG-FR-01: Tax Year P&L PDF Export | Design Required | `docs/design/2026-03-18__release-v2.1/pdf-export/ux_spec.md` | `docs/specs/frontend/pages/reports.md` v0.2 | ✅ Cleared |
| ST-13 | BLG-FR-02: Tax Year P&L CSV Export | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-14 | BLG-FEAT-03: Slippage Tracking | Design Required | `docs/design/2026-03-18__release-v2.1/slippage-tracking/ux_spec.md` | `docs/specs/frontend/pages/trade_history.md` v1.2 | ✅ Cleared |
| ST-15 | BLG-OPS-03: Render PR Preview Environments | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-16 | BLG-SPEC-D12: Bulk lifecycle header remediation | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-17 | Spec maintenance batch (D13+G6+D10+D11) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-18 | Author missing test scenario documents | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-19 | BLG-PROC-01: Cross-EPIC branch compliance check | Design Not Applicable | N/A | N/A | ✅ Cleared |

---

## Blocked Items

None. All 6 Design Required items cleared on 2026-03-18.

---

## Design Artefacts Produced This Cycle

| Item | Artefact | Location | Approved by |
|------|----------|----------|-------------|
| ST-05 | Notification Preferences UX Spec | `docs/design/2026-03-18__release-v2.1/notification-preferences/ux_spec.md` | Product Owner |
| ST-06 | Notification Feed UX Spec | `docs/design/2026-03-18__release-v2.1/notification-feed/ux_spec.md` | Product Owner |
| ST-10 | Watchlist UI UX Spec | `docs/design/2026-03-18__release-v2.1/watchlist/ux_spec.md` | Product Owner |
| ST-11 | Chart Interactivity Interaction Spec | `docs/design/2026-03-18__release-v2.1/chart-interactivity/ux_spec.md` | Product Owner |
| ST-12 | PDF Export UX Spec | `docs/design/2026-03-18__release-v2.1/pdf-export/ux_spec.md` | Product Owner |
| ST-14 | Slippage Tracking UX Spec | `docs/design/2026-03-18__release-v2.1/slippage-tracking/ux_spec.md` | Product Owner |

---

## Frontend Spec Versions Locked for Sprint Planning

| Item | Spec | Version | Change |
|------|------|---------|--------|
| ST-05 + ST-06 | `docs/specs/frontend/pages/notifications.md` | v0.1 (new) | New file: notification feed + preferences |
| ST-10 | `docs/specs/frontend/pages/watchlist.md` | v0.1 (new) | New file: watchlist UI |
| ST-11 | `docs/specs/frontend/pages/analytics.md` | v1.5 | §4 drill-down, §5 zoom/pan/reset, §9 tooltip |
| ST-12 | `docs/specs/frontend/pages/reports.md` | v0.2 | Page header controls + Download PDF button spec |
| ST-14 | `docs/specs/frontend/pages/trade_history.md` | v1.2 | Slippage column + Avg Slippage summary stat |

---

## Notes

- ST-05 and ST-06 share a single `notifications.md` spec file (feed and preferences are co-located under the Notifications nav section). Head of Specs Team confirmed this is appropriate.
- ST-11 (chart interactivity): analytics.md §5 (equity curve) already had a tooltip in v1.4; v1.5 adds zoom/pan/reset. §4 (heatmap) already had hover tooltip; v1.5 adds tile click drill-down. §9 (R-multiple client-side) adds tooltip; §16 (R-multiple backend) already had a tooltip from v1.3 — no change needed to §16.
- ST-14 design decision confirmed: per-trade slippage on trade_history.md (new column), portfolio average on summary stats bar. Head of UX & Design selected trade_history as the correct display location.
- trade_history.md lifecycle headers upgraded to Class 1 compliant format as part of this update (header-only change, no content modification to pre-existing content).
- No classification disagreements recorded.
- ESC-DG-20260318-01 in escalations.md is now resolved.
