**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Design Gate Record — 2026-03-04__release-v1.8

## Gate Status: PASSED

Completed: 2026-03-04
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed (design artefacts approved)
Head of Specs Team: confirmed (risk_dashboard.md v0.1.0 lifecycle-compliant)

---

## Item Classification Summary

| Item | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|------|-------|----------------|-----------------|---------------|-------------|
| EPIC-01 | Risk Dashboard Page | Design Required | `docs/design/2026-03-04__release-v1.8/risk-dashboard/ux_spec.md` | `docs/specs/frontend/pages/risk_dashboard.md` v0.1.0 | ✅ Cleared |
| EPIC-02 | CI Quality Gates | Design Not Applicable | N/A | N/A | ✅ Cleared |
| EPIC-03 | API & Spec Debt | Design Not Applicable | N/A | N/A | ✅ Cleared |
| EPIC-04 | Governance Docs | Design Not Applicable | N/A | N/A | ✅ Cleared |

---

## Blocked Items

None.

---

## Design Artefacts Produced This Cycle

| Item | Artefact | Location | Approved by |
|------|----------|----------|-------------|
| EPIC-01 | UX Specification — Risk Dashboard Page | `docs/design/2026-03-04__release-v1.8/risk-dashboard/ux_spec.md` | Product Owner — 2026-03-04 |

---

## Frontend Spec Versions Locked for Sprint Planning

| Item | Spec | Version |
|------|------|---------|
| EPIC-01 | `docs/specs/frontend/pages/risk_dashboard.md` | v0.1.0 |

---

## Notes

- ST-01 (EPIC-01) acceptance criteria reference `risk_dashboard.md` v0.1.0 as the authoritative frontend spec.
- ST-02 pre-alignment item remains: confirm whether `portfolio_heat_percent` and prospective heat calculation are available from `GET /portfolio` or require a separate endpoint. This is an engineering confirmation, not a design gate item — it does not block Sprint Planning.
- EPIC-02, EPIC-03, EPIC-04 are Design Not Applicable — no design work or frontend spec updates required.
- ESC-20260304-01 (settings endpoint decision) was resolved prior to this gate: option (a) chosen. ST-09 is unblocked.
