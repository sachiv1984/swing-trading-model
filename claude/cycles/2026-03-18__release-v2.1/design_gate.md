**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Design Gate Record — 2026-03-18__release-v2.1

## Gate Status: BLOCKED

Completed: 2026-03-18
PMO Lead: confirmed
Head of UX & Design: confirmed (classification)

**Sprint Planning is blocked.** All 6 Design Required items require design artefacts and frontend spec updates before `plan sprint` may be issued.

---

## Item Classification Summary

| Item ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|---------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Author async notification delivery ADR | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-02 | Spec: alerts endpoint + notification preference model | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-03 | Backend: alert rules engine | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-04 | Backend: notification delivery (email) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-05 | Frontend: notification preferences page | Design Required | PENDING — none exists | PENDING — `notifications.md` absent | ❌ Blocked |
| ST-06 | Frontend: in-app notification feed | Design Required | PENDING — none exists | PENDING — `notifications.md` absent | ❌ Blocked |
| ST-07 | QA: notification delivery test scenarios | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-08 | Spec: watchlist data model + API endpoints | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-09 | Backend: watchlist implementation | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-10 | Frontend: watchlist UI | Design Required | PENDING — none exists | PENDING — `watchlist.md` absent | ❌ Blocked |
| ST-11 | Implement chart interactivity (CHART-IX) | Design Required | PENDING — none exists | PENDING — analytics.md v1.4 has no tooltip/zoom/drill-down spec | ❌ Blocked |
| ST-12 | BLG-FR-01: Tax Year P&L PDF Export | Design Required | PENDING — none exists | PENDING — reports.md v0.1 has no PDF download control defined | ❌ Blocked |
| ST-13 | BLG-FR-02: Tax Year P&L CSV Export | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-14 | BLG-FEAT-03: Slippage Tracking | Design Required | PENDING — none exists | PENDING — no spec covers slippage display | ❌ Blocked |
| ST-15 | BLG-OPS-03: Render PR Preview Environments | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-16 | BLG-SPEC-D12: Bulk lifecycle header remediation | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-17 | Spec maintenance batch (D13+G6+D10+D11) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-18 | Author missing test scenario documents | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-19 | BLG-PROC-01: Cross-EPIC branch compliance check | Design Not Applicable | N/A | N/A | ✅ Cleared |

---

## Blocked Items

| Item ID | Title | Blocker | Artefact Required at | Spec Required at | Owner | Required by |
|---------|-------|---------|----------------------|------------------|-------|-------------|
| ST-05 | Notification preferences page | No design artefact; `notifications.md` spec absent | `docs/design/2026-03-18__release-v2.1/notification-preferences/` | `docs/specs/frontend/pages/notifications.md` | Head of UX & Design → Frontend Specs & UX Documentation Owner | Before `plan sprint` |
| ST-06 | In-app notification feed | No design artefact; `notifications.md` spec absent | `docs/design/2026-03-18__release-v2.1/notification-feed/` | `docs/specs/frontend/pages/notifications.md` | Head of UX & Design → Frontend Specs & UX Documentation Owner | Before `plan sprint` |
| ST-10 | Watchlist UI | No design artefact; `watchlist.md` spec absent | `docs/design/2026-03-18__release-v2.1/watchlist/` | `docs/specs/frontend/pages/watchlist.md` | Head of UX & Design → Frontend Specs & UX Documentation Owner | Before `plan sprint` |
| ST-11 | Chart interactivity (CHART-IX) | No design artefact; analytics.md v1.4 missing tooltip/zoom/drill-down interaction spec | `docs/design/2026-03-18__release-v2.1/chart-interactivity/` | `docs/specs/frontend/pages/analytics.md` (update to vX.X) | Head of UX & Design → Frontend Specs & UX Documentation Owner | Before `plan sprint` |
| ST-12 | Tax Year P&L PDF Export | No design artefact; reports.md v0.1 missing PDF download control UX | `docs/design/2026-03-18__release-v2.1/pdf-export/` | `docs/specs/frontend/pages/reports.md` (update to v0.2) | Head of UX & Design → Frontend Specs & UX Documentation Owner | Before `plan sprint` |
| ST-14 | Slippage Tracking | No design artefact; no spec covers slippage display location or format | `docs/design/2026-03-18__release-v2.1/slippage-tracking/` | Relevant page spec (TBD by Head of UX & Design — positions, trade_history, or analytics) | Head of UX & Design → Frontend Specs & UX Documentation Owner | Before `plan sprint` |

---

## Design Artefacts Produced This Cycle

None produced. All 6 Design Required items are pending design work.

---

## Frontend Spec Versions Locked for Sprint Planning

Pending gate clearance. No items cleared. Locked spec versions will be recorded when the gate is re-run and passes.

---

## Design Required Items — Required Artefact Scope

To clear the gate, the Head of UX & Design must produce artefacts for all 6 blocked items. The following artefact scope is advisory:

| Item | Artefact Scope | Target Path |
|------|---------------|-------------|
| ST-05 | Wireframe: page layout, per-type toggle controls (email/SMS on/off per alert type), settings persistence flow | `docs/design/2026-03-18__release-v2.1/notification-preferences/` |
| ST-06 | Wireframe: feed list layout, notification item format, mark-as-read interaction, empty state | `docs/design/2026-03-18__release-v2.1/notification-feed/` |
| ST-10 | Wireframe: watchlist page layout, ticker row (entry signal, target entry, stop fields), quick-add from position modal, add/edit/remove controls, empty state | `docs/design/2026-03-18__release-v2.1/watchlist/` |
| ST-11 | Interaction spec: tooltip format for each of 3 charts (underwater equity, monthly heatmap, R-multiple), zoom behaviour (equity curve), drill-down behaviour (heatmap → filtered trade list) | `docs/design/2026-03-18__release-v2.1/chart-interactivity/` |
| ST-12 | Wireframe/UX decision: PDF download button placement on reports page (header or per-section), button label, loading/downloading state | `docs/design/2026-03-18__release-v2.1/pdf-export/` |
| ST-14 | Wireframe/UX decision: where slippage is displayed (per-trade row location + portfolio average placement), field label, number format | `docs/design/2026-03-18__release-v2.1/slippage-tracking/` |

---

## To Clear This Gate

1. Head of UX & Design produces artefacts for all 6 blocked items (filed at paths above)
2. Product Owner approves each artefact (one by one — approval of one does not block others)
3. Frontend Specs & UX Documentation Owner updates relevant frontend spec files
4. Head of Specs Team confirms spec updates are lifecycle-compliant (correct class, version increment, Last Updated)
5. PMO Lead re-runs `run design-gate --cycle 2026-03-18__release-v2.1` to record clearance and update gate status to Passed
6. Only then may `plan sprint` be issued

---

## Notes

- ST-05 and ST-06 both require `docs/specs/frontend/pages/notifications.md` (new file). The Head of UX & Design and Frontend Specs owner should co-author this spec covering both features in a single document.
- ST-11 (chart interactivity) requires updating the existing `analytics.md` spec rather than creating a new file. The Head of Specs Team must confirm the version increment is lifecycle-compliant.
- ST-14 (slippage tracking) requires a UX decision on display location before the spec can be updated. The Head of UX & Design must determine which page(s) show slippage — this is the first design decision required.
- No classification disagreements recorded.
- Gate status at prior check: `not_started`. This run establishes `Blocked` as current state.
