**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-29
**Cycle:** 2026-04-29__release-v3.1

---

# Design Gate Record — 2026-04-29__release-v3.1

## Gate Status: PASSED

Completed: 2026-04-29
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed (ST-03 trade plan flow, ST-06 UK ticker fix, ST-08 earnings calendar, ST-11 monthly P&L — all design artefacts approved)

---

## Item Classification Summary

| Item ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|---------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Trade Plan spec authoring: data model + API contract | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-02 | Trade Plan backend: migration + CRUD + tests | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-03 | Trade Plan frontend: creation flow + detail view | Design Required | `docs/design/2026-04-29__release-v3.1/trade-plan/ux_spec.md` v1.0 | `docs/specs/frontend/pages/trade_plan.md` v0.1 (new) | ✅ Cleared |
| ST-04 | Pre-Trade Research View API contract spec | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-05 | Pre-Trade Research View backend | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-06 | Fix screener UK ticker display + watchlist promotion | Design Required | `docs/design/2026-04-29__release-v3.1/uk-ticker-display/ux_spec.md` v1.0 | `docs/specs/frontend/pages/screener_results.md` v1.1 (§4 + §8 updated) | ✅ Cleared |
| ST-07 | Earnings Calendar backend + OpenAPI | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-08 | Earnings Calendar frontend | Design Required | `docs/design/2026-04-29__release-v3.1/earnings-calendar/ux_spec.md` v1.0 | `screener_results.md` v1.2 (§4.1); `watchlist.md` v0.2 (§Earnings Column); `positions.md` v1.5 (§Table View) | ✅ Cleared |
| ST-09 | Screener accuracy test protocol | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-10 | Screener scenario library | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-11 | Monthly P&L summary report | Design Required | `docs/design/2026-04-29__release-v3.1/monthly-pnl/ux_spec.md` v1.0 | `docs/specs/frontend/pages/reports.md` v0.3 (§Monthly Breakdown) | ✅ Cleared |
| ST-12 | External API security policy docs | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-13 | execution_prompt.md §3.1.A patch (CF-01) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-14 | execution_prompt.md STEP 8.5 fix (CF-02) | Design Not Applicable | N/A | N/A | ✅ Cleared |

---

## Blocked Items

None.

---

## Design Artefacts Produced This Cycle

| Item | Artefact | Location | Approved by |
|------|----------|----------|-------------|
| ST-03 | Trade Plan creation flow + detail view UX decision record | `docs/design/2026-04-29__release-v3.1/trade-plan/ux_spec.md` | Product Owner — 2026-04-29 |
| ST-06 | UK ticker display fix UX decision record | `docs/design/2026-04-29__release-v3.1/uk-ticker-display/ux_spec.md` | Product Owner — 2026-04-29 |
| ST-08 | Earnings Calendar frontend UX decision record | `docs/design/2026-04-29__release-v3.1/earnings-calendar/ux_spec.md` | Product Owner — 2026-04-29 |
| ST-11 | Monthly P&L summary report UX decision record | `docs/design/2026-04-29__release-v3.1/monthly-pnl/ux_spec.md` | Product Owner — 2026-04-29 |

---

## Frontend Spec Versions Locked for Sprint Planning

| Item | Spec | Version |
|------|------|---------|
| ST-03 | `docs/specs/frontend/pages/trade_plan.md` | v0.1 (new) |
| ST-06 | `docs/specs/frontend/pages/screener_results.md` | v1.1 |
| ST-08 | `docs/specs/frontend/pages/screener_results.md` | v1.2 |
| ST-08 | `docs/specs/frontend/pages/watchlist.md` | v0.2 |
| ST-08 | `docs/specs/frontend/pages/positions.md` | v1.5 |
| ST-11 | `docs/specs/frontend/pages/reports.md` | v0.3 |

---

## Classification Rationale Notes

**ST-03 (Design Required → Cleared):** New user-facing interaction flow (creation form, slide-in drawer, position detail panel, two entry points). Entry point was explicitly designated "TBD by design gate" in the AC. Design gate resolved: entry from Positions Table View ("Plan" button in Actions column) and from Watchlist ("Plan" button in Actions column). Head of UX & Design produced `ux_spec.md` v1.0. Product Owner approved. Frontend Specs owner authored `trade_plan.md` v0.1. Head of Specs Team confirmed compliant.

**ST-06 (Design Required → Cleared):** Bug fix with UI-visible behavior change (`.L` suffix stripping from screener display and watchlist popover) plus a design decision (font treatment: `font-mono` for ticker column). Classified as Design Required per default rule (not Design Pre-Approved) because: (a) screener_results.md had no prior UK ticker display spec, (b) a font treatment decision was required. Head of UX & Design produced `ux_spec.md` v1.0 confirming display rules and font treatment. screener_results.md updated to v1.1 (§4 + §8).

**ST-08 (Design Required → Cleared):** New UI elements across three pages (screener results table column, watchlist table column, positions table cell badge). No prior spec existed for earnings proximity display. Head of UX & Design produced `ux_spec.md` v1.0 specifying column placement, badge thresholds (≤5d red, 6–30d amber on screener/watchlist; ≤5d red, 6–7d amber on positions), and null handling. Three frontend specs updated: screener_results.md v1.2, watchlist.md v0.2, positions.md v1.5.

**ST-11 (Design Required → Cleared):** New UI section on the Reports page (monthly breakdown table). No prior spec existed for this section. Head of UX & Design produced `ux_spec.md` v1.0 specifying placement (below Unrealised P&L Card), table columns, scope constraint (rolling 12-month, not tax-year-scoped), and states. reports.md updated to v0.3.

---

## Notes

- screener_results.md received two separate version increments this design gate (v1.1 for ST-06, v1.2 for ST-08). Both are committed together.
- ST-06 font treatment (`font-mono` for ticker column) is consistent with the design intent for financial identifiers. No regression to US ticker display.
- ST-08 earnings data for positions uses a 7-day display threshold (6–7d amber) vs. a 5-day hard warning (≤5d red). The 7-day advisory level is a design decision — not stated in the ST-08 AC — made by Head of UX & Design to give the user a useful early-awareness window.
- Trade Plan `position_id` nullable: the spec explicitly supports pre-position plans (entry from Watchlist), consistent with the ST-01 data model schema.
