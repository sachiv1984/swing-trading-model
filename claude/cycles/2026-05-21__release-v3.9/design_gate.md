**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-21
**Cycle:** 2026-05-21__release-v3.9

# Design Gate Record — 2026-05-21__release-v3.9

## Gate Status: PASSED

Completed: 2026-05-21
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed
Head of Specs Team: confirmed

---

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Fix Yahoo Finance crumb/401 rate-limiting in screener batch | Design Not Applicable | Purely backend — crumb refresh, backoff, concurrency cap. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Fix sector/industry data silently dropped in screener batch | Design Not Applicable | Backend data fix — sector/industry propagation to compute function. No schema or UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | Remove invalid DAY ticker from ticker universe | Design Not Applicable | Backend/data only — CSV and DB record removal. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Add degraded-run warning banner to screener results page | Design Required | New user-visible UI component (amber warning banner) on screener results page. | `docs/design/2026-05-21__release-v3.9/degraded-run-banner/ux_spec.md` | `docs/specs/frontend/pages/screener_results.md` v1.2 | ✅ Cleared | Head of UX & Design |
| ST-05 | Strip .L suffix from Ticker Universe page display labels | Design Required | User-facing display label change on Ticker Universe page. No existing page spec existed. | `docs/design/2026-05-21__release-v3.9/ticker-universe-enhancements/ux_spec.md` | `docs/specs/frontend/pages/ticker_universe.md` v1.0 (new) | ✅ Cleared | Head of UX & Design |
| ST-06 | Add company_name column to ticker universe and display on management page | Design Required | New data displayed (company name column) on Ticker Universe page. | `docs/design/2026-05-21__release-v3.9/ticker-universe-enhancements/ux_spec.md` | `docs/specs/frontend/pages/ticker_universe.md` v1.0 (new) | ✅ Cleared | Head of UX & Design |
| ST-07 | Red Flag Journal — data model and backend | Design Not Applicable | Backend only — `red_flag_events` table, `GET /portfolio/red-flag-journal` endpoint. No UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Red Flag Journal — frontend display | Design Required | New page (`/red-flag-journal`), new nav item, new component. | `docs/design/2026-05-21__release-v3.9/red-flag-journal/ux_spec.md` | `docs/specs/frontend/pages/red_flag_journal.md` v1.0 (new); `docs/specs/frontend/pages/navigation.md` v1.2 | ✅ Cleared | Head of UX & Design |
| ST-09 | execution_prompt.md patches | Design Not Applicable | Governance prompt modifications only. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | sprint_planning_prompt.md patch | Design Not Applicable | Governance prompt modification only. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | BLG-GOV-25 — Add --dry-run support to plan release and run delivery verification | Design Not Applicable | Governance prompt modifications only. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | QA evidence pre-merge enforcement — PR template checklist item | Design Not Applicable | GitHub PR template addition. No user-facing product UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | PT-04 Setup Quality Score — backend endpoint (conditional) | Design Not Applicable | Backend only — endpoint implementation. No UI change. Conditional on 20+ trades gate. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | PT-04 Setup Quality Score — frontend display (conditional) | Design Required | New UI elements (qualitative labels, tooltip, creation form panel) in existing pages. v3.7 spec existed but required updates for v3.9 ACs (endpoint change, qualitative labels, tooltip, ticker-change refresh, creation form). | `docs/design/2026-05-21__release-v3.9/setup-quality-score-v2/ux_spec.md` | `docs/specs/frontend/pages/pre_trade_research.md` v0.3; `docs/specs/frontend/pages/trade_plan.md` v0.7 | ✅ Cleared | Head of UX & Design |

---

## Blocked Items

None.

---

## Sprint Planning Pre-Condition

All Design Required items have approved artefacts and updated frontend specs. Gate cleared.

Sprint Planning may proceed (`plan sprint --cycle 2026-05-21__release-v3.9`).

---

## Notes

- ST-05 and ST-06 are covered by a single design artefact (`ticker-universe-enhancements/ux_spec.md`) and a single new spec (`ticker_universe.md`), as both affect the same page.
- ST-14 is conditional on the EPIC-05 gate (20+ closed trades confirmed by Product Owner at sprint planning). If gate not confirmed, ST-13 and ST-14 are recorded as `deferred_at_planning` and the §7a/§7b spec sections are not implemented in v3.9.
- navigation.md updated to v1.2 to document the Red Flag Journal nav item (Trading group) for ST-08.
- No design artefacts existed for this cycle prior to this gate run — all four artefact directories created in `docs/design/2026-05-21__release-v3.9/`.
