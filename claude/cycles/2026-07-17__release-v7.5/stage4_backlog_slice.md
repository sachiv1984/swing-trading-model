**Owner:** Head of Specs Team
**Status:** Active
**Release:** v7.5
**Cycle:** 2026-07-17__release-v7.5
**Last Updated:** 2026-07-17

---

# Stage 4 Backlog Slice — v7.5

<!-- release-plan-marker: RP:v7.5:2026-07-17__release-v7.5 -->

All 4 items below are **conditional**, not firm — see `release_plan.md` RISK-01. Sprint Planning may not seal any of these stories until `run design-gate --cycle 2026-07-17__release-v7.5` PASSes for each.

## EPIC-01 — Global command palette / cross-page search
**Maps to:** S2-01
**Backlog source:** `BLG-FE-115`
**Sequencing:** Conditional on Design Gate PASS (RISK-01)

### ST-01 — Wire global Cmd/Ctrl-K command palette
**Acceptance Criteria:**
- Cmd/Ctrl-K opens the palette from any page in the app
- Typing a ticker surfaces matches across Watchlist/Positions/TradePlans and navigates to the selected result
- Typing a page name navigates to that page

---

## EPIC-02 — User-defined custom price alerts
**Maps to:** S2-02
**Backlog source:** `BLG-FE-116`
**Sequencing:** Conditional on Design Gate PASS (RISK-01); backend data-model scoping precursor (RISK-03)

### ST-02 — Add user-created price-alert data model, UI, and delivery integration
**Acceptance Criteria:**
- User can create a ticker/condition/threshold alert from the UI
- Alert fires via the existing notification delivery channel when its condition is met
- User can view, edit, and delete active alerts

---

## EPIC-03 — Bulk actions on list/table views
**Maps to:** S2-03
**Backlog source:** `BLG-FE-117`
**Sequencing:** Conditional on Design Gate PASS (RISK-01)

### ST-03 — Add multi-select and bulk-action toolbar to Watchlist/TradePlans
**Acceptance Criteria:**
- Rows in Watchlist and TradePlans tables are multi-selectable
- A bulk-action toolbar appears once one or more rows are selected
- Bulk tag/archive/remove operations apply to all selected rows in a single action

---

## EPIC-04 — Saved filter views and calendar view
**Maps to:** S2-04
**Backlog source:** `BLG-FE-118`
**Sequencing:** Conditional on Design Gate PASS (RISK-01)

### ST-04 — Add named saved filter presets and a calendar view
**Acceptance Criteria:**
- User can save a filter combination by name and reapply it in a later session
- A calendar view renders trade plan dates and key dates, navigable by month

---

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-07-17__release-v7.5",
  "phase": "Release",
  "status": "present",
  "generated_utc": "2026-07-17T18:22:00Z"
}
```
