**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-19
**Cycle:** 2026-06-19__release-v6.0

# Design Gate Record — 2026-06-19__release-v6.0

## Gate Status: PASSED

Completed: 2026-06-19
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

---

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Align signal_service suggested_shares to risk-based sizing model | Design Not Applicable | Backend calculation fix only; signal card already displays suggested_shares; no new component, layout, or interaction change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Trader's Morning Briefing dashboard | Design Required | New UI section with 5 intelligence cards (Screener Hits, Positions to Act On, Red Flags, Earnings Alert, Compliance) added at top of DashboardHome.js; horizontal desktop layout; vertical mobile stack; per-card loading/error/empty states | `docs/design/2026-06-19__release-v6.0/morning-briefing/ux_spec.md` v1.0 | `docs/specs/frontend/pages/dashboard.md` v2.1 | ✅ Cleared | Head of UX & Design |
| ST-03 | Net-of-costs performance tracking | Design Required | New optional brokerage cost fields (commission_gbp, spread_cost_gbp) on trade edit form; net-of-costs R-multiple displayed alongside gross R when cost data present; gross vs net average comparison row in Reports summary bar | `docs/design/2026-06-19__release-v6.0/net-of-costs-tracking/ux_spec.md` v1.0 | `docs/specs/frontend/pages/trade_history.md` v1.10; `docs/specs/frontend/pages/reports.md` v0.5 | ✅ Cleared | Head of UX & Design |
| ST-04 | Screener data quality telemetry | Design Required | Replaces v3.9 degraded-run banner (boolean) with structured Run Quality Panel covering FULL/DEGRADED/FAILED states; FULL: green badge + loaded ratio; DEGRADED: amber badge + ratio + expandable failed ticker list; FAILED: red badge + retry; stale advisory cross-state | `docs/design/2026-06-19__release-v6.0/screener-quality-telemetry/ux_spec.md` v1.0 | `docs/specs/frontend/pages/screener_results.md` v1.3 | ✅ Cleared | Head of UX & Design |
| ST-05 | SI-05 deep link AC-04 staging confirmation | Design Not Applicable | Ops staging verification of existing Telegram deep links; no UI changes | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | RFJ design review pre-brief | Design Not Applicable | Produces a planning/governance document (design review brief); no UI implementation in this story | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | Red Flag Journal visual design review | Design Not Applicable | Produces a design recommendation document; any UI implementation routed to a separate backlog item (AC-03 explicit) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | SI-05 digest weekly cadence review | Design Not Applicable | Governance document production; no UI changes | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | SI-05 digest actionability metric definition | Design Not Applicable | Metrics definition document production; no UI changes | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | SI-05 Phase 2 activation decision scope | Design Not Applicable | Formal decision document production; no UI changes | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | SI-05 service production p99 latency baseline review | Design Not Applicable | Ops measurement and documentation; no UI changes | N/A | N/A | ✅ Cleared | Head of UX & Design |

---

## Blocked Items

None.

---

## Frontend Specs Updated This Run

| Spec File | Old Version | New Version | Story |
|-----------|-------------|-------------|-------|
| `docs/specs/frontend/pages/dashboard.md` | v2.0 | v2.1 | ST-02 |
| `docs/specs/frontend/pages/trade_history.md` | v1.9 | v1.10 | ST-03 |
| `docs/specs/frontend/pages/reports.md` | v0.4 | v0.5 | ST-03 |
| `docs/specs/frontend/pages/screener_results.md` | v1.2 | v1.3 | ST-04 |

---

## Design Artefacts Produced This Run

| Artefact Path | Story | Status |
|---------------|-------|--------|
| `docs/design/2026-06-19__release-v6.0/morning-briefing/ux_spec.md` | ST-02 | Approved — Product Owner 2026-06-19 |
| `docs/design/2026-06-19__release-v6.0/net-of-costs-tracking/ux_spec.md` | ST-03 | Approved — Product Owner 2026-06-19 |
| `docs/design/2026-06-19__release-v6.0/screener-quality-telemetry/ux_spec.md` | ST-04 | Approved — Product Owner 2026-06-19 |

---

## Notes

- Prior status anomaly resolved: `.claude_current_state.json` was in `Sprint_Planning_In_Progress` (an out-of-schema state) with `design_gate_status = not_started` when this engine was invoked. Lifecycle guard halted; state restored to `Release_Planning_Complete` per PMO Lead direction (Option A). Sprint planning artefacts from prior uncommitted session are superseded — `plan sprint` must be re-run after this gate passes.
- ST-04 design supersedes the v3.9 degraded-run banner artefact (`docs/design/2026-05-21__release-v3.9/degraded-run-banner/ux_spec.md`). The old artefact is retained for history; `screener_results.md §12` now references the v6.0 quality panel.
- ST-03 updates two frontend specs (trade_history.md and reports.md) due to the cross-surface nature of cost tracking: capture on trade records, display in trade history, summary comparison in reports.
