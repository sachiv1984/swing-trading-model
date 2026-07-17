**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-17
**Cycle:** 2026-07-17__release-v7.4
**Amendment:** AMD-20260717-01
**Supersedes:** claude/cycles/2026-07-17__release-v7.4/stage4_backlog_slice.md (for sprint planning purposes)
**Ratified:** 2026-07-17 by Product Owner and Head of Specs Team

> This amended backlog slice supersedes the original stage4_backlog_slice.md for the purposes
> of Sprint Planning. The original sealed artefact is unchanged and remains the historical record
> of the published release plan.

## Amendment Summary

| Change | Item | Type | Reason |
|--------|------|------|--------|
| Removed | ST-02 — Wire global Cmd/Ctrl-K command palette | hard-blocker | Design Gate BLOCKED — no approved artefact; review scheduled as in-sprint work that cannot pre-satisfy the gate |
| Removed | ST-03 — Add user-created price-alert data model, UI, and delivery integration | hard-blocker | Design Gate BLOCKED — no design artefact exists or is scheduled anywhere in the v7.4 plan |
| Removed | ST-04 — Add multi-select and bulk-action toolbar to Watchlist/TradePlans | hard-blocker | Design Gate BLOCKED — no UX spec for the confirmation/undo-window modal; scheduled as in-sprint work |
| Removed | ST-05 — Add named saved filter presets and a calendar view | hard-blocker | Design Gate BLOCKED — no UX spec for the empty state (in-sprint) and no design review scheduled for the calendar view |

---

<!-- release-plan-marker: RP:v7.4:2026-07-17__release-v7.4 -->
<!-- amendment-marker: AMD:v7.4:2026-07-17__release-v7.4:AMD-20260717-01 -->

# Stage 4 Backlog Slice — v7.4 (Amended)

## EPIC-01 — v7.4 UI-heavy release readiness bundle
**Maps to:** S2-01
**Backlog source:** `BLG-SPEC-95`
**Sequencing:** First — gates EPIC-02/03/04/05 (now deferred; see below)

### ST-01 — Produce v7.4 readiness pass (dependencies, UX specs, design review, QA/analytics coverage)
**Acceptance Criteria:**
- Dependency pre-flight complete: `cmdk` and `react-day-picker` both added to `package.json` in this same pass
- UX spec written for saved-filters empty state (EPIC-05) and bulk-actions confirmation/undo-window modal (EPIC-04)
- Design review pass completed for command-palette keyboard-navigation affordance (EPIC-02)
- Playwright visual-regression baseline scope defined for all 4 downstream feature surfaces
- Analytics event schema defined for command-palette usage
- Regression-suite CI tagging scheme defined so v7.4 stories can run a scoped subset
- One consolidated readiness-pass document produced covering all 6 items above, referenced by EPIC-02/03/04/05's implementation stories

**Note (AMD-20260717-01):** EPIC-02/03/04/05 implementation stories are removed from this sprint's scope (see below). This story's acceptance criteria are unchanged — the design/spec work it produces remains valid forward-looking preparation for whichever future release re-introduces those EPICs, and does not require re-scoping under §4 of `amendment_cycle_prompt.md` (acceptance criteria for existing items are not amendable; this note is informational only).

---

## EPIC-02 — Global command palette / cross-page search — REMOVED

~~### ST-02 — Wire global Cmd/Ctrl-K command palette~~ — **Removed by `AMD-20260717-01`:** Design Gate BLOCKED (2026-07-17) — no approved design-review artefact; review scheduled inside EPIC-01/ST-01 sprint-execution work, which cannot pre-satisfy a gate required to clear before Sprint Planning. `BLG-FE-115` remains valid backlog scope for a future release once a design artefact exists.

---

## EPIC-03 — User-defined custom price alerts — REMOVED

~~### ST-03 — Add user-created price-alert data model, UI, and delivery integration~~ — **Removed by `AMD-20260717-01`:** Design Gate BLOCKED (2026-07-17) — no design artefact exists or is scheduled anywhere in the v7.4 plan. `BLG-FE-116` remains valid backlog scope for a future release once a design artefact exists.

---

## EPIC-04 — Bulk actions on list/table views — REMOVED

~~### ST-04 — Add multi-select and bulk-action toolbar to Watchlist/TradePlans~~ — **Removed by `AMD-20260717-01`:** Design Gate BLOCKED (2026-07-17) — no UX spec for the confirmation/undo-window modal; scheduled inside EPIC-01/ST-01 sprint-execution work. `BLG-FE-117` remains valid backlog scope for a future release once a design artefact exists.

---

## EPIC-05 — Saved filter views and calendar view — REMOVED

~~### ST-05 — Add named saved filter presets and a calendar view~~ — **Removed by `AMD-20260717-01`:** Design Gate BLOCKED (2026-07-17) — no UX spec for the saved-filters empty state (in-sprint only) and no design review scheduled for the calendar view. `BLG-FE-118` remains valid backlog scope for a future release once a design artefact exists.

---

## Summary

| EPIC | Story | Backlog item | Effort | Status |
|------|-------|--------------|--------|--------|
| EPIC-01 | ST-01 | BLG-SPEC-95 | L (~5–7 days) | In scope |
| EPIC-02 | ST-02 | BLG-FE-115 | M (~1–2 days) | Removed (`AMD-20260717-01`) |
| EPIC-03 | ST-03 | BLG-FE-116 | L (~3–5 days) | Removed (`AMD-20260717-01`) |
| EPIC-04 | ST-04 | BLG-FE-117 | M (~1–2 days) | Removed (`AMD-20260717-01`) |
| EPIC-05 | ST-05 | BLG-FE-118 | L (~3–5 days) | Removed (`AMD-20260717-01`) |

1 story in scope for Sprint Planning under this amendment (down from 5). Design Gate re-run required against this amended slice before Sprint Planning may proceed.
