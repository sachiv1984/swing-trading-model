**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-14
**Cycle:** 2026-04-13__release-v2.7

# Design Gate Record — 2026-04-13__release-v2.7

## Gate Status: PASSED

Completed: 2026-04-14
PMO Lead: confirmed
Head of UX & Design: confirmed

---

## Item Classification Summary

| Item ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|---------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Enable Supabase Supavisor connection pooling | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-02 | Refactor get_portfolio_summary() | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-03 | Require QA evidence sign-off gate | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-04 | Define autonomous DoQ sign-off class | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-05 | Extend governance_sync.yml | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-06 | Fix Playwright page.route() intercepts | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-07 | System Status Playwright spec | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-08 | Market Correlation Analysis | Design Required | `docs/design/2026-04-13__release-v2.7/market-correlation/ux_spec.md` | `docs/specs/frontend/pages/analytics.md` v1.7 | ✅ Cleared |
| ST-09 | Add supplementary indicator fields | Design Required | `docs/design/2026-04-13__release-v2.7/supplementary-indicators/ux_spec.md` | `docs/specs/frontend/pages/signals.md` v0.2 | ✅ Cleared |
| ST-10 | Spec Dependency Map | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-11 | Governance Health Score | Design Not Applicable | N/A | N/A | ✅ Cleared |

All 11 items classified. 2 Design Required (cleared), 9 Design Not Applicable. No blocked items.

---

## Blocked Items

None.

---

## Design Artefacts Produced This Cycle

| Item | Artefact | Location | Approved by |
|------|----------|----------|-------------|
| ST-08 | UX Spec — Market Correlation Analysis | `docs/design/2026-04-13__release-v2.7/market-correlation/ux_spec.md` | Product Owner |
| ST-09 | UX Spec — Supplementary Signal Indicator Columns | `docs/design/2026-04-13__release-v2.7/supplementary-indicators/ux_spec.md` | Product Owner |

---

## Frontend Spec Versions Locked for Sprint Planning

| Item | Spec | Version |
|------|------|---------|
| ST-08 | `docs/specs/frontend/pages/analytics.md` | v1.7 |
| ST-09 | `docs/specs/frontend/pages/signals.md` | v0.2 |

---

## Notes

- ST-01 through ST-07, ST-10, ST-11 are all backend/infrastructure/governance/test items with no user-visible UI change — classified Design Not Applicable unanimously.
- ST-08 (Market Correlation): new §18 section on Analytics page. Per-position Pearson correlation vs. SPY/FTSE benchmark, colour-coded severity (high/moderate/low), lookback control, cached daily. Spec updated to analytics.md v1.7.
- ST-09 (Supplementary Indicators): 4 supplementary context columns added to Signals page table, grouped under informational header. Display-only; does not affect signal rank. Spec updated to signals.md v0.2.
- §13 compliance: ST-09 AC confirms supplementary fields are display-only and do not affect `rank` field. Strategy Rules owner sign-off required in QA evidence before merge (per ST-09 AC).
