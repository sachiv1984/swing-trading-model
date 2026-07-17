**Owner:** Head of Specs Team
**Status:** Active
**Release:** v7.4
**Cycle:** 2026-07-17__release-v7.4
**Last Updated:** 2026-07-17

---

# Stage 4 Backlog Slice — v7.4

<!-- release-plan-marker: RP:v7.4:2026-07-17__release-v7.4 -->

## EPIC-01 — v7.4 UI-heavy release readiness bundle
**Maps to:** S2-01
**Backlog source:** `BLG-SPEC-95`
**Sequencing:** First — gates EPIC-02/03/04/05

### ST-01 — Produce v7.4 readiness pass (dependencies, UX specs, design review, QA/analytics coverage)
**Acceptance Criteria:**
- Dependency pre-flight complete: `cmdk` and `react-day-picker` both added to `package.json` in this same pass
- UX spec written for saved-filters empty state (EPIC-05) and bulk-actions confirmation/undo-window modal (EPIC-04)
- Design review pass completed for command-palette keyboard-navigation affordance (EPIC-02)
- Playwright visual-regression baseline scope defined for all 4 downstream feature surfaces
- Analytics event schema defined for command-palette usage
- Regression-suite CI tagging scheme defined so v7.4 stories can run a scoped subset
- One consolidated readiness-pass document produced covering all 6 items above, referenced by EPIC-02/03/04/05's implementation stories

---

## EPIC-02 — Global command palette / cross-page search
**Maps to:** S2-02
**Backlog source:** `BLG-FE-115`
**Sequencing:** After EPIC-01

### ST-02 — Wire global Cmd/Ctrl-K command palette
**Acceptance Criteria:**
- Cmd/Ctrl-K opens the palette from any page in the app
- Typing a ticker surfaces matches across Watchlist/Positions/TradePlans and navigates to the selected result
- Typing a page name navigates to that page

---

## EPIC-03 — User-defined custom price alerts
**Maps to:** S2-03
**Backlog source:** `BLG-FE-116`
**Sequencing:** After EPIC-01

### ST-03 — Add user-created price-alert data model, UI, and delivery integration
**Acceptance Criteria:**
- User can create a ticker/condition/threshold alert from the UI
- Alert fires via the existing notification delivery channel when its condition is met
- User can view, edit, and delete active alerts

---

## EPIC-04 — Bulk actions on list/table views
**Maps to:** S2-04
**Backlog source:** `BLG-FE-117`
**Sequencing:** After EPIC-01

### ST-04 — Add multi-select and bulk-action toolbar to Watchlist/TradePlans
**Acceptance Criteria:**
- Rows in Watchlist and TradePlans tables are multi-selectable
- A bulk-action toolbar appears once one or more rows are selected
- Bulk tag/archive/remove operations apply to all selected rows in a single action

---

## EPIC-05 — Saved filter views and calendar view
**Maps to:** S2-05
**Backlog source:** `BLG-FE-118`
**Sequencing:** After EPIC-01

### ST-05 — Add named saved filter presets and a calendar view
**Acceptance Criteria:**
- User can save a filter combination by name and reapply it in a later session
- A calendar view renders trade plan dates and key dates, navigable by month

---

## Summary

| EPIC | Story | Backlog item | Effort |
|------|-------|--------------|--------|
| EPIC-01 | ST-01 | BLG-SPEC-95 | L (~5–7 days) |
| EPIC-02 | ST-02 | BLG-FE-115 | M (~1–2 days) |
| EPIC-03 | ST-03 | BLG-FE-116 | L (~3–5 days) |
| EPIC-04 | ST-04 | BLG-FE-117 | M (~1–2 days) |
| EPIC-05 | ST-05 | BLG-FE-118 | L (~3–5 days) |

5 stories total. All frontend-visible (EPIC-02/03/04/05) except EPIC-01 (spec/readiness artefact — no shippable UI itself, though 2 of its sub-items are design-decision-shaped). Design Gate Required — see STEP 4.1 below.
