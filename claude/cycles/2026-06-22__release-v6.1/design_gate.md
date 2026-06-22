**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-22
**Cycle:** 2026-06-22__release-v6.1

# Design Gate Record — 2026-06-22__release-v6.1

## Gate Status: PASSED

Completed: 2026-06-22
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed
Head of Specs Team: confirmed

---

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Release planning: Design Gate Required flag | Design Not Applicable | Governance prompt edit; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Sprint planning: Design Gate hard gate at preflight | Design Not Applicable | Governance prompt edit; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | Governance overhead ceiling metric | Design Not Applicable | Internal proposal document only; no UI implementation in this story | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Register morning-briefing.spec.js and screener-quality.spec.js | Design Not Applicable | CI/CD workflow edit; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | Add PATCH /trades/{id}/costs to api_performance_baseline.md | Design Not Applicable | Ops documentation / measurement; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | Portfolio sector heat-map visualization | Design Required | New user-facing component (SectorHeatMap.js); new data displayed; delegation class `delegated_frontend` | `docs/design/2026-06-22__release-v6.1/sector-heatmap/ux_spec.md` v1.0 | `docs/specs/frontend/pages/risk_dashboard.md` v0.1.9 | ✅ Cleared | Head of UX & Design; Product Owner |
| ST-07 | Trade gate proximity indicator on dashboard | Design Required | New data displayed (trade count vs gate threshold) on Dashboard homepage; placement confirmation required | `docs/design/2026-06-22__release-v6.1/gate-proximity-indicator/ux_spec.md` v1.0 | `docs/specs/frontend/pages/dashboard.md` v2.2 | ✅ Cleared | Head of UX & Design; Product Owner |
| ST-08 | Setup Quality Score — backend engine | Design Not Applicable | Backend API endpoint only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Setup Quality Score — frontend display | Design Pre-Approved | Frontend spec fully updated in v3.9 design gate (2026-05-21). `pre_trade_research.md` v0.3 §5 and `trade_plan.md` v0.7 §7a/7b already specify the Setup Quality Score. Design source confirmed current: `docs/design/2026-05-21__release-v3.9/setup-quality-score-v2/ux_spec.md`. Conditional on gate ≥20 closed trades (EPIC-04 conditional). | `docs/design/2026-05-21__release-v3.9/setup-quality-score-v2/ux_spec.md` (existing) | `pre_trade_research.md` v0.3; `trade_plan.md` v0.7 (locked spec references) | ✅ Cleared | Head of UX & Design |

---

## Blocked Items

None.

---

## Placement Decisions (Design Gate Outputs)

### ST-06 — Portfolio Sector Heat-Map
- **Page:** Risk Dashboard (`/risk`)
- **Position:** Full-width panel between Position-Level Risk Table (§6) and Prospective Heat Indicator (§7), labelled "§8a Sector Concentration"
- **Rationale:** Risk Dashboard is the canonical home for portfolio risk data. Sector concentration extends the existing risk surface (heat, drawdown, position risk) coherently. Dashboard (`/`) is already dense.
- **Alert threshold:** 40% single-sector exposure (per AC-03)
- **Interaction:** Display-only MVP (no tile click, no drill-down)

### ST-07 — Trade Gate Proximity Indicator
- **Page:** Dashboard Homepage (`/`)
- **Position:** Compact full-width strip below the 5 session-summary cards (new §5 Gate Progress)
- **Rationale:** Dashboard is the daily entry point; the trade gate is a user milestone visible daily. System Status page is appropriate for infrastructure health; Dashboard is appropriate for user milestone progress.
- **Interaction:** Display-only. Error hidden silently (gate-metrics failure must not block Dashboard primary content).
- **Autonomous classification confirmed:** ST-07 proceeds as autonomous (display-only, reads existing endpoint). Design gate advisory role is fulfilled by this placement record.

---

## Notes

- ST-09 (Setup Quality Score frontend) is classified Design Pre-Approved. The v3.9 design gate (2026-05-21__release-v3.9) fully specified this feature. Sprint planning must reference `pre_trade_research.md` v0.3 and `trade_plan.md` v0.7 as locked spec versions for EPIC-04 conditional stories.
- EPIC-04 (ST-08, ST-09) remains conditional. Sprint planning must verify ≥20 closed trades before including these stories as firm capacity.
- No disagreements between Product Owner and Head of UX & Design recorded.
- No escalations.
