**Owner:** Head of UX & Design / Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-15
**Story:** ST-08 (BLG-QA-111, EPIC-05, v7.2)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Combined Design Review + Shared Playwright Suite Plan

## 1. Purpose

Scope one combined design review covering `ST-03`, `ST-05`, `ST-06`, `ST-07`, and name one shared Playwright spec file (rather than separate files per story) for the three implementation stories' observable ACs, consistent with CLAUDE.md's frontend Playwright coverage requirement.

## 2. AC-01/AC-03 — Combined Design Review

**Already satisfied — confirmed, not re-run.** Per `claude/cycles/2026-07-15__release-v7.2/design_gate.md` §Notes: "This design-gate run — which classified and, for the three Design Required items, designed all of `ST-03`/`ST-05`/`ST-06` together in a single pass before `plan sprint` — constitutes that combined review." `ST-07` (Design Pre-Approved, audit-only, no design output) was reviewed in the same classification pass. The design gate ran ahead of sprint planning (satisfying AC-03's "scheduled ahead of sprint planning" requirement) and is PMO Lead / Head of UX & Design / Product Owner confirmed (design_gate.md header). No further design review action is required from this story.

## 3. AC-02 — Shared Playwright Spec File Named

**File name:** `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js`

**Rationale for one shared file across two EPICs:** `ST-05` and `ST-06` both modify `DashboardHome.js` cards in the same design-review batch; `ST-03` modifies `TradePlan.js`/`TradePlans.js`/`TradeEntry.js` in the same batch. All three were designed together in one design-gate pass (§2) and share the same v7.2 dual-theme verification requirement (`base44_prompt_template_library.md` §4). Consolidating into one file — rather than three page-scoped files — matches AC-02's explicit "rather than four separate ones" instruction and keeps the small, closely-related-in-time story set's test maintenance in one place.

**Planned scenario groups (for `ST-03`/`ST-05`/`ST-06` implementation to populate — not written in this story, since none of the three implementation stories execute this sprint):**

| Group | Covers | Source AC |
|---|---|---|
| `describe("Start Trade from Plan")` | `TradePlan.js`/`TradePlans.js` action visibility + functional pre-fill hand-off to `TradeEntry.js`; manual-entry regression | `ST-03` AC-01–AC-04 |
| `describe("Dashboard empty states")` | Compact `DataState` empty-state rendering for `OpenPositionsCard`/`GracePeriodCard`/`RecentActivityCard`, light + dark theme | `ST-05` AC-01–AC-02 |
| `describe("Dashboard briefing hierarchy")` | Morning Briefing panel + AI Daily Briefing icon treatment, visual distinction on load, light + dark theme, `dashboard-retry-root` regression | `ST-06` AC-01, AC-03 |

Each group's dual-theme cases should follow the reusable call-out in `base44_prompt_template_library.md` §4 (verify both light and dark, not dark-only).

## 4. AC-04 — Backfill Into `ST-03`/`ST-05`/`ST-06` Sprint-Backlog Entries

**Confirmed not fully closable this sprint** — per `sprint_backlog.md`'s own recorded Outstanding Action: "Name shared Playwright spec file (`ST-08` AC-02) and backfill into `ST-03`/`ST-05`/`ST-06` entries at their future sprint planning run" (Blocker: No). `sprint_backlog.md` is sealed and may not be modified by this routine. The filename determined in §3 above is the artefact to carry forward — whoever runs the sprint planning cycle that brings `ST-03`/`ST-05`/`ST-06` into scope should reference `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js` in each story's sprint-backlog entry at that time.

## 5. Known Deviations

None. This is a net-new planning artefact; the combined design review it confirms was already completed and approved at the design gate.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-15 | 1.0 | Initial combined review confirmation + shared Playwright spec file naming (ST-08, EPIC-05, v7.2) |
